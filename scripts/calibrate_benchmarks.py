#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deep_hedging.benchmarks import black_scholes_delta, no_trade_band, reduced_frequency
from deep_hedging.config import load_config
from deep_hedging.evaluation import evaluate_positions
from deep_hedging.simulators import simulate_gbm, simulate_heston_full_truncation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    cfg = load_config(args.config)

    n_paths = cfg.get("validation", {}).get("n_paths", 10_000)
    seed = cfg.get("validation", {}).get("seed", 70_001)
    if cfg["model"] == "gbm":
        prices = simulate_gbm(
            n_paths=n_paths,
            n_steps=cfg["n_steps"],
            s0=cfg["s0"],
            maturity=cfg["maturity"],
            mu=cfg.get("mu", 0.0),
            sigma=cfg["sigma"],
            seed=seed,
        )
    else:
        prices, _, _ = simulate_heston_full_truncation(
            n_paths=n_paths,
            n_steps=cfg["n_steps"],
            s0=cfg["s0"],
            maturity=cfg["maturity"],
            mu=cfg.get("mu", 0.0),
            seed=seed,
            substeps=cfg.get("substeps", 1),
            **cfg["heston"],
        )

    sigma = cfg.get("sigma", cfg.get("heston", {}).get("theta_v", 0.04) ** 0.5)
    bs = black_scholes_delta(prices, strike=cfg["strike"], maturity=cfg["maturity"], sigma=sigma)
    eval_kwargs = {
        "strike": cfg["strike"],
        "kappa": cfg["kappa"],
        "cost_kind": cfg["cost_kind"],
        "alpha": cfg["alpha"],
        "premium": cfg.get("premium", 0.0),
        "terminal_liquidation": cfg.get("terminal_liquidation", False),
    }

    candidates: dict[str, object] = {}
    calibration = cfg.get("calibration", {})
    for shrink in calibration.get("shrink_grid", [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]):
        candidates[f"shrink:{shrink}"] = shrink * bs
    for band in calibration.get("band_grid", [0.01, 0.025, 0.05, 0.075, 0.1]):
        candidates[f"band:{band}"] = no_trade_band(bs, band)
    for every in calibration.get("frequency_grid", [1, 2, 3, 5, 10]):
        candidates[f"frequency:{every}"] = reduced_frequency(bs, every)

    scores = {
        name: evaluate_positions(prices, positions, **eval_kwargs)[0]
        for name, positions in candidates.items()
    }
    best = min(scores, key=lambda name: scores[name]["cvar"])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "best": best,
                "scores": scores,
                "validation_seed": seed,
                "n_paths": n_paths,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
