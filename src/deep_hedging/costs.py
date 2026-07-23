from __future__ import annotations

import numpy as np


def trade_costs(
    prices: np.ndarray,
    deltas: np.ndarray,
    kappa: float,
    kind: str = "linear",
    terminal_liquidation: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    prices = np.asarray(prices, float)
    deltas = np.asarray(deltas, float)
    if (
        prices.ndim != 2
        or deltas.ndim != 2
        or prices.shape[0] != deltas.shape[0]
        or prices.shape[1] != deltas.shape[1] + 1
    ):
        raise ValueError("prices must have shape (B,n+1) and deltas (B,n)")
    prev = np.c_[np.zeros(deltas.shape[0]), deltas[:, :-1]]
    trades = deltas - prev
    if kind == "linear":
        costs = kappa * prices[:, :-1] * np.abs(trades)
    elif kind == "quadratic":
        costs = kappa * prices[:, :-1] * trades**2
    else:
        raise ValueError("kind must be linear or quadratic")
    if terminal_liquidation:
        u = -deltas[:, -1]
        terminal = kappa * prices[:, -1] * (np.abs(u) if kind == "linear" else u**2)
        costs = np.c_[costs, terminal]
    return costs, trades
