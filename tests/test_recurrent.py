import numpy as np

from deep_hedging.features import build_features
from deep_hedging.losses import hedging_loss_and_gradient
from deep_hedging.network import TanhMLP
from deep_hedging.recurrent import inventory_positions
from deep_hedging.risk import empirical_cvar_weights


def test_inventory_bptt_gradient_finite_difference():
    rng = np.random.default_rng(8)
    p = 100 * np.exp(np.c_[np.zeros(8), np.cumsum(rng.normal(scale=0.01, size=(8, 3)), axis=1)])
    feat = build_features(p, strike=100, maturity=30 / 252)
    net = TanhMLP(3, 3, 1.2, 2)
    d, caches = inventory_positions(net, feat)
    loss, direct, _ = hedging_loss_and_gradient(p, d, strike=100, kappa=0.02, cost_kind="quadratic")
    weights = empirical_cvar_weights(loss, 0.75)
    grads = net.zero_grads()
    carry = np.zeros(8)
    for k in range(2, -1, -1):
        g, ig = net.backward(weights * direct[:, k] + carry, caches[k], return_input=True)
        for name in grads:
            grads[name] += g[name]
        carry = ig[:, -1]
    eps = 1e-6
    for name, param in net.params.items():
        for idx in np.ndindex(param.shape):
            old = param[idx]
            param[idx] = old + eps
            dp, _ = inventory_positions(net, feat)
            lp = hedging_loss_and_gradient(p, dp, strike=100, kappa=0.02, cost_kind="quadratic")[0] @ weights
            param[idx] = old - eps
            dm, _ = inventory_positions(net, feat)
            lm = hedging_loss_and_gradient(p, dm, strike=100, kappa=0.02, cost_kind="quadratic")[0] @ weights
            param[idx] = old
            assert abs((lp - lm) / (2 * eps) - grads[name][idx]) < 2e-7
