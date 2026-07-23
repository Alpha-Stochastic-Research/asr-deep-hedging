import numpy as np

from deep_hedging.network import TanhMLP


def test_network_gradient():
    rng = np.random.default_rng(9)
    net = TanhMLP(2, 3, 1.2, 3)
    x = rng.normal(size=(4, 2))
    up = rng.normal(size=4)
    _, cache = net.forward(x)
    a = net.backward(up, cache)
    eps = 1e-6
    for name, p in net.params.items():
        for idx in np.ndindex(p.shape):
            old = p[idx]
            p[idx] = old + eps
            plus = net.forward(x)[0] @ up
            p[idx] = old - eps
            minus = net.forward(x)[0] @ up
            p[idx] = old
            assert abs((plus - minus) / (2 * eps) - a[name][idx]) < 1e-7
