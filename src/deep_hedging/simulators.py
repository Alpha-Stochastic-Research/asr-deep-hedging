from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class HestonDiagnostics:
    min_aux_variance: float
    negative_aux_fraction: float
    mean_terminal_variance: float


def simulate_gbm(
    *,
    n_paths: int,
    n_steps: int,
    s0: float = 100.0,
    maturity: float = 30 / 252,
    mu: float = 0.0,
    sigma: float = 0.2,
    seed: int | None = None,
) -> np.ndarray:
    if n_paths <= 0 or n_steps <= 0 or s0 <= 0 or maturity <= 0 or sigma < 0:
        raise ValueError("invalid GBM parameters")
    rng = np.random.default_rng(seed)
    dt = maturity / n_steps
    z = rng.standard_normal((n_paths, n_steps))
    inc = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    log_s = np.c_[np.zeros(n_paths), np.cumsum(inc, axis=1)]
    return s0 * np.exp(log_s)


def simulate_heston_full_truncation(
    *,
    n_paths: int,
    n_steps: int,
    s0: float = 100.0,
    maturity: float = 30 / 252,
    mu: float = 0.0,
    v0: float = 0.04,
    kappa_v: float = 2.0,
    theta_v: float = 0.04,
    xi: float = 0.5,
    rho: float = -0.7,
    substeps: int = 1,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray, HestonDiagnostics]:
    """Full-truncation Euler for variance and log-Euler for price.

    The auxiliary variance may become negative. Its positive part is used in
    the drift/diffusion and is the observable variance feature.
    """
    if n_paths <= 0 or n_steps <= 0 or substeps <= 0 or s0 <= 0 or maturity <= 0:
        raise ValueError("invalid Heston dimensions")
    if v0 < 0 or theta_v < 0 or kappa_v < 0 or xi < 0 or abs(rho) > 1:
        raise ValueError("invalid Heston parameters")
    rng = np.random.default_rng(seed)
    total = n_steps * substeps
    dt = maturity / total
    s = np.full(n_paths, float(s0))
    v_aux = np.full(n_paths, float(v0))
    prices = np.empty((n_paths, n_steps + 1), float)
    variances = np.empty_like(prices)
    prices[:, 0] = s
    variances[:, 0] = np.maximum(v_aux, 0.0)
    min_v = float(v_aux.min())
    neg_count = 0
    obs_count = 0
    out_idx = 1
    for j in range(total):
        z1 = rng.standard_normal(n_paths)
        z2_ind = rng.standard_normal(n_paths)
        z2 = rho * z1 + np.sqrt(max(0.0, 1.0 - rho * rho)) * z2_ind
        vp = np.maximum(v_aux, 0.0)
        s *= np.exp((mu - 0.5 * vp) * dt + np.sqrt(vp * dt) * z1)
        v_aux = v_aux + kappa_v * (theta_v - vp) * dt + xi * np.sqrt(vp * dt) * z2
        min_v = min(min_v, float(v_aux.min()))
        neg_count += int(np.count_nonzero(v_aux < 0.0))
        obs_count += n_paths
        if (j + 1) % substeps == 0:
            prices[:, out_idx] = s
            variances[:, out_idx] = np.maximum(v_aux, 0.0)
            out_idx += 1
    diag = HestonDiagnostics(min_v, neg_count / obs_count, float(variances[:, -1].mean()))
    return prices, variances, diag
