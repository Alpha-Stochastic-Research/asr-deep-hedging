from __future__ import annotations

import numpy as np
from scipy.special import ndtr


def _delta_from_sigma(prices, strike, maturity, sigma, rate=0.0):
    p = np.asarray(prices, float)
    n = p.shape[1] - 1
    tau = np.maximum(maturity - np.arange(n) * maturity / n, 1e-15)
    sig = np.asarray(sigma, float)
    if sig.ndim == 0:
        sig = np.full((p.shape[0], n), float(sig))
    else:
        sig = np.broadcast_to(sig, (p.shape[0], n))
    safe = np.maximum(sig, 1e-12)
    d1 = (np.log(p[:, :-1] / strike) + (rate + 0.5 * safe * safe) * tau) / (safe * np.sqrt(tau))
    deterministic = (p[:, :-1] > strike * np.exp(-rate * tau)).astype(float)
    return np.where(sig > 1e-12, ndtr(d1), deterministic)


def black_scholes_delta(
    prices: np.ndarray, *, strike: float, maturity: float, sigma: float, rate: float = 0.0
) -> np.ndarray:
    return _delta_from_sigma(prices, strike, maturity, sigma, rate)


def instantaneous_vol_delta(
    prices: np.ndarray, variances: np.ndarray, *, strike: float, maturity: float, rate: float = 0.0
):
    v = np.asarray(variances, float)
    if v.shape != np.asarray(prices).shape:
        raise ValueError("variances must match prices")
    return _delta_from_sigma(prices, strike, maturity, np.sqrt(np.maximum(v[:, :-1], 0.0)), rate)


def no_hedge(prices: np.ndarray) -> np.ndarray:
    return np.zeros((prices.shape[0], prices.shape[1] - 1))


def shrunk_delta(prices: np.ndarray, *, shrink: float, **kwargs) -> np.ndarray:
    return float(shrink) * black_scholes_delta(prices, **kwargs)


def no_trade_band(target: np.ndarray, band: float) -> np.ndarray:
    target = np.asarray(target, float)
    out = np.empty_like(target)
    prev = np.zeros(target.shape[0])
    for k in range(target.shape[1]):
        move = target[:, k] - prev
        take = np.abs(move) > band
        prev = np.where(take, target[:, k], prev)
        out[:, k] = prev
    return out


def reduced_frequency(target: np.ndarray, every: int) -> np.ndarray:
    if every <= 0:
        raise ValueError("every must be positive")
    out = np.empty_like(target)
    prev = np.zeros(target.shape[0])
    for k in range(target.shape[1]):
        if k % every == 0:
            prev = target[:, k]
        out[:, k] = prev
    return out
