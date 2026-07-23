from __future__ import annotations

import numpy as np


def build_features(
    prices: np.ndarray, *, strike: float, maturity: float, variances: np.ndarray | None = None
) -> np.ndarray:
    p = np.asarray(prices, float)
    B, n1 = p.shape
    n = n1 - 1
    tau = (maturity - np.arange(n) * maturity / n) / maturity
    logm = np.log(p[:, :-1] / strike)
    out = [np.broadcast_to(tau, (B, n)), logm]
    if variances is not None:
        v = np.asarray(variances, float)
        if v.shape != p.shape:
            raise ValueError("variances must match prices")
        out.append(v[:, :-1])
    return np.stack(out, axis=-1)
