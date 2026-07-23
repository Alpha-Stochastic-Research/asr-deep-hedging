from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .features import build_features
from .losses import hedging_loss_and_gradient
from .risk import empirical_cvar_weights


@dataclass
class TrainRecord:
    iteration: int
    cvar: float
    mean_loss: float
    avg_abs_trade: float
    grad_norm: float


def policy_positions(network, features):
    B, n, d = features.shape
    deltas = np.empty((B, n))
    caches = []
    for k in range(n):
        deltas[:, k], cache = network.forward(features[:, k, :])
        caches.append(cache)
    return deltas, caches


def train_step(
    network,
    optimizer,
    *,
    prices,
    strike,
    maturity,
    alpha,
    kappa,
    cost_kind="linear",
    variances=None,
    premium=0.0,
    terminal_liquidation=False,
):
    feat = build_features(prices, strike=strike, maturity=maturity, variances=variances)
    deltas, caches = policy_positions(network, feat)
    losses, dld, detail = hedging_loss_and_gradient(
        prices,
        deltas,
        strike=strike,
        kappa=kappa,
        cost_kind=cost_kind,
        premium=premium,
        terminal_liquidation=terminal_liquidation,
    )
    weights = empirical_cvar_weights(losses, alpha)
    grads = network.zero_grads()
    for k, cache in enumerate(caches):
        g = network.backward(weights * dld[:, k], cache)
        for name in grads:
            grads[name] += g[name]
    grad_norm = float(np.sqrt(sum(np.sum(v * v) for v in grads.values())))
    optimizer.step(network.params, grads)
    return float(np.dot(weights, losses)), losses, deltas, detail, grad_norm
