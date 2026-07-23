from __future__ import annotations

import numpy as np

from .features import build_features
from .losses import hedging_loss_and_gradient
from .risk import empirical_cvar_weights


def inventory_positions(network, features: np.ndarray):
    """Semi-recurrent target-position policy delta_k=F(x_k, delta_{k-1})."""
    features = np.asarray(features, float)
    B, n, _ = features.shape
    deltas = np.empty((B, n))
    caches = []
    prev = np.zeros(B)
    for k in range(n):
        inp = np.c_[features[:, k, :], prev]
        current, cache = network.forward(inp)
        deltas[:, k] = current
        caches.append(cache)
        prev = current
    return deltas, caches


def inventory_policy_step(
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
    features = build_features(prices, strike=strike, maturity=maturity, variances=variances)
    deltas, caches = inventory_positions(network, features)
    losses, direct, detail = hedging_loss_and_gradient(
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
    carry = np.zeros(losses.size)
    for k in range(deltas.shape[1] - 1, -1, -1):
        upstream = weights * direct[:, k] + carry
        g, input_grad = network.backward(upstream, caches[k], return_input=True)
        for name in grads:
            grads[name] += g[name]
        carry = input_grad[:, -1]
    grad_norm = float(np.sqrt(sum(np.sum(v * v) for v in grads.values())))
    optimizer.step(network.params, grads)
    return float(np.dot(weights, losses)), losses, deltas, detail, grad_norm
