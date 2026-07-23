from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .costs import trade_costs


@dataclass
class LossBreakdown:
    payoff: np.ndarray
    gains: np.ndarray
    costs: np.ndarray
    trades: np.ndarray


def hedging_loss_and_gradient(
    prices: np.ndarray,
    deltas: np.ndarray,
    *,
    strike: float,
    kappa: float,
    cost_kind: str = "linear",
    premium: float = 0.0,
    terminal_liquidation: bool = False,
) -> tuple[np.ndarray, np.ndarray, LossBreakdown]:
    p = np.asarray(prices, float)
    d = np.asarray(deltas, float)
    costs, trades = trade_costs(p, d, kappa, cost_kind, terminal_liquidation)
    ds = np.diff(p, axis=1)
    payoff = np.maximum(p[:, -1] - strike, 0.0)
    gains = np.sum(d * ds, axis=1)
    total_cost = np.sum(costs, axis=1)
    losses = payoff - premium - gains + total_cost

    B, n = d.shape
    grad = -ds.copy()
    # current cost derivative c_k'(u_k)
    if cost_kind == "linear":
        current = kappa * p[:, :-1] * np.sign(trades)
    elif cost_kind == "quadratic":
        current = 2.0 * kappa * p[:, :-1] * trades
    else:
        raise ValueError("cost_kind must be linear or quadratic")
    grad += current
    # next cost derivative uses S_{k+1}, never S_k
    if n > 1:
        next_trades = trades[:, 1:]
        if cost_kind == "linear":
            nxt = kappa * p[:, 1:n] * np.sign(next_trades)
        else:
            nxt = 2.0 * kappa * p[:, 1:n] * next_trades
        grad[:, :-1] -= nxt
    if terminal_liquidation:
        u = -d[:, -1]
        if cost_kind == "linear":
            cprime = kappa * p[:, -1] * np.sign(u)
        else:
            cprime = 2.0 * kappa * p[:, -1] * u
        grad[:, -1] -= cprime
    return losses, grad, LossBreakdown(payoff, gains, costs, trades)
