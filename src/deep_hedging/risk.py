from __future__ import annotations

import numpy as np


def empirical_cvar_weights(losses: np.ndarray, alpha: float = 0.95) -> np.ndarray:
    """Return exact finite-sample Expected Shortfall weights.

    Losses are sorted from largest to smallest. If (1-alpha)*B is non-integer,
    the boundary observation receives fractional weight. Stable sorting gives
    deterministic tie handling and therefore one valid subgradient.
    """
    x = np.asarray(losses, dtype=float)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("losses must be a non-empty one-dimensional array")
    if not 0.0 <= alpha < 1.0:
        raise ValueError("alpha must satisfy 0 <= alpha < 1")
    q = (1.0 - alpha) * x.size
    if q <= 0.0:
        raise ValueError("tail mass must be positive")
    order = np.argsort(-x, kind="mergesort")
    r = int(np.floor(q + 1e-14))
    lam = q - r
    w = np.zeros_like(x, dtype=float)
    if r:
        w[order[:r]] = 1.0 / q
    if lam > 1e-14 and r < x.size:
        w[order[r]] = lam / q
    return w


def empirical_cvar(losses: np.ndarray, alpha: float = 0.95) -> float:
    x = np.asarray(losses, dtype=float)
    return float(np.dot(empirical_cvar_weights(x, alpha), x))


def empirical_var(losses: np.ndarray, alpha: float = 0.95) -> float:
    x = np.asarray(losses, dtype=float)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("losses must be a non-empty one-dimensional array")
    return float(np.quantile(x, alpha, method="higher"))
