#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deep_hedging.benchmarks import (
    black_scholes_delta,
    instantaneous_vol_delta,
    no_hedge,
    no_trade_band,
    reduced_frequency,
    shrunk_delta,
)
from deep_hedging.config import load_config
from deep_hedging.evaluation import evaluate_positions, paired_bootstrap_cvar_difference
from deep_hedging.features import build_features
from deep_hedging.heston_surface import HestonDeltaSurface
from deep_hedging.io import save_json, save_losses
from deep_hedging.network import TanhMLP
from deep_hedging.optim import Adam
from deep_hedging.recurrent import inventory_policy_step, inventory_positions
from deep_hedging.simulators import simulate_gbm, simulate_heston_full_truncation
from deep_hedging.training import policy_positions, train_step


def sim(cfg, n, seed):
    common = dict(
        n_paths=n,
        n_steps=cfg["n_steps"],
        s0=cfg["s0"],
        maturity=cfg["maturity"],
        mu=cfg.get("mu", 0.0),
        seed=seed,
    )
    if cfg["model"] == "gbm":
        return simulate_gbm(**common, sigma=cfg["sigma"]), None, None
    p, v, d = simulate_heston_full_truncation(**common, **cfg["heston"], substeps=cfg.get("substeps", 1))
    return p, v, d.__dict__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    cfg = load_config(args.config)
    out = Path(args.output or ROOT / "results/generated" / cfg["experiment_name"])
    out.mkdir(parents=True, exist_ok=True)
    train = cfg["train"]
    input_dim = 3 if cfg["model"] == "heston" else 2
    policy_type = cfg.get("policy_type", "state")
    net_input = input_dim + 1 if policy_type == "inventory" else input_dim
    net = TanhMLP(net_input, train.get("hidden", 16), train.get("delta_max", 1.5), train["network_seed"])
    opt = Adam(net.params, train.get("lr", 3e-3), eps=train.get("adam_eps", 1e-8))
    history = []
    for it in range(1, train["iterations"] + 1):
        p, v, _ = sim(cfg, train["batch_size"], train["sim_seed"] + it)
        step_fn = inventory_policy_step if policy_type == "inventory" else train_step
        cvar, loss, d, detail, gn = step_fn(
            net,
            opt,
            prices=p,
            variances=v,
            strike=cfg["strike"],
            maturity=cfg["maturity"],
            alpha=cfg["alpha"],
            kappa=cfg["kappa"],
            cost_kind=cfg["cost_kind"],
            premium=cfg.get("premium", 0.0),
            terminal_liquidation=cfg.get("terminal_liquidation", False),
        )
        if it == 1 or it % train.get("log_every", 10) == 0 or it == train["iterations"]:
            history.append(
                {
                    "iteration": it,
                    "cvar": cvar,
                    "mean_loss": float(loss.mean()),
                    "avg_abs_trade": float(abs(detail.trades).mean()),
                    "grad_norm": gn,
                }
            )
    p, v, hdiag = sim(cfg, cfg["test"]["n_paths"], cfg["test"]["seed"])
    feat = build_features(p, strike=cfg["strike"], maturity=cfg["maturity"], variances=v)
    learned, _ = inventory_positions(net, feat) if policy_type == "inventory" else policy_positions(net, feat)
    kwargs = dict(
        strike=cfg["strike"],
        kappa=cfg["kappa"],
        cost_kind=cfg["cost_kind"],
        alpha=cfg["alpha"],
        premium=cfg.get("premium", 0.0),
        terminal_liquidation=cfg.get("terminal_liquidation", False),
    )
    metrics = {}
    losses = {}
    metrics["deep_hedging"], losses["deep_hedging"] = evaluate_positions(p, learned, **kwargs)
    bs = black_scholes_delta(
        p,
        strike=cfg["strike"],
        maturity=cfg["maturity"],
        sigma=cfg.get("sigma", np.sqrt(cfg.get("heston", {}).get("theta_v", 0.04))),
    )
    candidates = {
        "black_scholes": bs,
        "no_hedge": no_hedge(p),
        "shrunk_delta": shrunk_delta(
            p,
            shrink=cfg.get("benchmark_shrink", 0.8),
            strike=cfg["strike"],
            maturity=cfg["maturity"],
            sigma=cfg.get("sigma", 0.2),
        ),
        "no_trade_band": no_trade_band(bs, cfg.get("benchmark_band", 0.05)),
        "reduced_frequency": reduced_frequency(bs, cfg.get("benchmark_every", 5)),
    }
    if v is not None:
        candidates["instantaneous_vol_delta"] = instantaneous_vol_delta(
            p, v, strike=cfg["strike"], maturity=cfg["maturity"]
        )
        if cfg.get("heston_delta_surface"):
            surface = HestonDeltaSurface.load(cfg["heston_delta_surface"])
            candidates["heston_delta_surface"] = surface.evaluate(
                p, v, strike=cfg["strike"], maturity=cfg["maturity"]
            )
    for name, pos in candidates.items():
        metrics[name], losses[name] = evaluate_positions(p, pos, **kwargs)
    comparisons = {
        name: paired_bootstrap_cvar_difference(
            losses["deep_hedging"],
            loss,
            alpha=cfg["alpha"],
            n_boot=cfg["test"].get("bootstrap", 200),
            seed=cfg["test"]["seed"] + 77,
        )
        for name, loss in losses.items()
        if name != "deep_hedging"
    }
    save_json(out / "config.resolved.json", cfg)
    save_json(
        out / "metrics.json",
        {"metrics": metrics, "comparisons": comparisons, "heston_diagnostics": hdiag, "history": history},
    )
    save_losses(out / "losses.npz", **losses)
    save_losses(out / "positions.npz", deep_hedging=learned, **candidates)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
