from __future__ import annotations

import numpy as np

from .losses import hedging_loss_and_gradient
from .risk import empirical_cvar, empirical_var


def evaluate_positions(
    prices, deltas, *, strike, kappa, cost_kind="linear", alpha=0.95, premium=0.0, terminal_liquidation=False
):
    losses, _, detail = hedging_loss_and_gradient(
        prices,
        deltas,
        strike=strike,
        kappa=kappa,
        cost_kind=cost_kind,
        premium=premium,
        terminal_liquidation=terminal_liquidation,
    )
    return {
        "n_paths": int(losses.size),
        "mean_loss": float(losses.mean()),
        "std_loss": float(losses.std(ddof=1)),
        "var": empirical_var(losses, alpha),
        "cvar": empirical_cvar(losses, alpha),
        "avg_abs_trade": float(np.abs(detail.trades).mean()),
        "mean_total_cost": float(detail.costs.sum(axis=1).mean()),
    }, losses


def paired_bootstrap_cvar_difference(loss_a, loss_b, *, alpha=0.95, n_boot=1000, seed=0):
    a = np.asarray(loss_a, float)
    b = np.asarray(loss_b, float)
    if a.shape != b.shape:
        raise ValueError("paired losses must have same shape")
    rng = np.random.default_rng(seed)
    vals = np.empty(n_boot)
    n = a.size
    for j in range(n_boot):
        idx = rng.integers(0, n, n)
        vals[j] = empirical_cvar(a[idx], alpha) - empirical_cvar(b[idx], alpha)
    return {
        "estimate": empirical_cvar(a, alpha) - empirical_cvar(b, alpha),
        "ci_low": float(np.quantile(vals, 0.025)),
        "ci_high": float(np.quantile(vals, 0.975)),
    }
