import numpy as np

from deep_hedging.losses import hedging_loss_and_gradient


def test_quadratic_position_gradient_finite_difference():
    rng = np.random.default_rng(4)
    p = 100 * np.exp(np.c_[np.zeros(7), np.cumsum(rng.normal(scale=0.02, size=(7, 4)), axis=1)])
    d = rng.normal(scale=0.2, size=(7, 4))
    _, g, _ = hedging_loss_and_gradient(p, d, strike=100, kappa=0.04, cost_kind="quadratic")
    eps = 1e-6
    for k in range(4):
        dp = d.copy()
        dm = d.copy()
        dp[:, k] += eps
        dm[:, k] -= eps
        lp = hedging_loss_and_gradient(p, dp, strike=100, kappa=0.04, cost_kind="quadratic")[0]
        lm = hedging_loss_and_gradient(p, dm, strike=100, kappa=0.04, cost_kind="quadratic")[0]
        assert np.max(abs((lp - lm) / (2 * eps) - g[:, k])) < 1e-7


def test_next_cost_uses_next_price():
    p = np.array([[100.0, 110.0, 120.0]])
    d = np.array([[0.2, 0.5]])
    _, g, _ = hedging_loss_and_gradient(p, d, strike=100, kappa=0.1, cost_kind="quadratic")
    expected0 = -(10) + 2 * 0.1 * 100 * 0.2 - 2 * 0.1 * 110 * (0.3)
    assert np.isclose(g[0, 0], expected0)
