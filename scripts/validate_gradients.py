#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deep_hedging.losses import hedging_loss_and_gradient
from deep_hedging.network import TanhMLP


def check_network():
    rng = np.random.default_rng(12)
    net = TanhMLP(2, 4, 1.5, 7)
    x = rng.normal(size=(5, 2))
    upstream = rng.normal(size=5)
    y, cache = net.forward(x)
    ana = net.backward(upstream, cache)
    eps = 1e-6
    worst = 0
    for name, p in net.params.items():
        for idx in np.ndindex(p.shape):
            old = p[idx]
            p[idx] = old + eps
            plus = np.dot(net.forward(x)[0], upstream)
            p[idx] = old - eps
            minus = np.dot(net.forward(x)[0], upstream)
            p[idx] = old
            fd = (plus - minus) / (2 * eps)
            worst = max(worst, abs(fd - ana[name][idx]))
    return worst


def check_loss():
    rng = np.random.default_rng(4)
    p = 100 * np.exp(np.c_[np.zeros(6), np.cumsum(rng.normal(scale=0.01, size=(6, 3)), axis=1)])
    d = rng.normal(scale=0.2, size=(6, 3))
    loss, g, _ = hedging_loss_and_gradient(p, d, strike=100, kappa=0.03, cost_kind="quadratic")
    eps = 1e-6
    worst = 0
    for k in range(3):
        dp = d.copy()
        dm = d.copy()
        dp[:, k] += eps
        dm[:, k] -= eps
        lp = hedging_loss_and_gradient(p, dp, strike=100, kappa=0.03, cost_kind="quadratic")[0]
        lm = hedging_loss_and_gradient(p, dm, strike=100, kappa=0.03, cost_kind="quadratic")[0]
        worst = max(worst, float(np.max(abs((lp - lm) / (2 * eps) - g[:, k]))))
    return worst


if __name__ == "__main__":
    a = check_network()
    b = check_loss()
    print(f"network max abs error: {a:.3e}\nloss max abs error: {b:.3e}")
    raise SystemExit(0 if max(a, b) < 1e-7 else 1)
