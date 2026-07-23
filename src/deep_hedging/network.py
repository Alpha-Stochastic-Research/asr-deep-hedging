from __future__ import annotations

import numpy as np


class TanhMLP:
    """Two-hidden-layer MLP with an analytically implemented backward pass."""

    def __init__(self, input_dim: int, hidden: int = 16, delta_max: float = 1.5, seed: int | None = None):
        if input_dim <= 0 or hidden <= 0 or delta_max <= 0:
            raise ValueError("invalid network dimensions")
        rng = np.random.default_rng(seed)
        self.delta_max = float(delta_max)
        self.params = {
            "W1": rng.normal(0, 1 / np.sqrt(input_dim), (input_dim, hidden)),
            "b1": np.zeros(hidden),
            "W2": rng.normal(0, 1 / np.sqrt(hidden), (hidden, hidden)),
            "b2": np.zeros(hidden),
            "W3": rng.normal(0, 1 / np.sqrt(hidden), (hidden, 1)),
            "b3": np.zeros(1),
        }

    def forward(self, x: np.ndarray):
        x = np.asarray(x, float)
        if x.ndim != 2 or x.shape[1] != self.params["W1"].shape[0]:
            raise ValueError("input has incompatible shape")
        z1 = x @ self.params["W1"] + self.params["b1"]
        a1 = np.tanh(z1)
        z2 = a1 @ self.params["W2"] + self.params["b2"]
        a2 = np.tanh(z2)
        z3 = a2 @ self.params["W3"] + self.params["b3"]
        t3 = np.tanh(z3)
        delta = (self.delta_max * t3)[:, 0]
        return delta, (x, a1, a2, t3)

    def backward(self, upstream: np.ndarray, cache, *, return_input: bool = False):
        x, a1, a2, t3 = cache
        g = np.asarray(upstream, float).reshape(-1, 1)
        gz3 = g * self.delta_max * (1 - t3 * t3)
        out = {"W3": a2.T @ gz3, "b3": gz3.sum(axis=0)}
        gz2 = (gz3 @ self.params["W3"].T) * (1 - a2 * a2)
        out.update({"W2": a1.T @ gz2, "b2": gz2.sum(axis=0)})
        gz1 = (gz2 @ self.params["W2"].T) * (1 - a1 * a1)
        out.update({"W1": x.T @ gz1, "b1": gz1.sum(axis=0)})
        input_grad = gz1 @ self.params["W1"].T
        return (out, input_grad) if return_input else out

    def zero_grads(self):
        return {k: np.zeros_like(v) for k, v in self.params.items()}

    def copy(self):
        other = TanhMLP(self.params["W1"].shape[0], self.params["W1"].shape[1], self.delta_max, 0)
        other.params = {k: v.copy() for k, v in self.params.items()}
        return other
