import numpy as np

from deep_hedging.simulators import simulate_gbm, simulate_heston_full_truncation


def test_gbm_seed_reproducible():
    a = simulate_gbm(n_paths=8, n_steps=4, seed=5)
    b = simulate_gbm(n_paths=8, n_steps=4, seed=5)
    assert np.array_equal(a, b)


def test_gbm_martingale_mean():
    p = simulate_gbm(n_paths=100000, n_steps=5, mu=0, sigma=0.2, maturity=30 / 252, seed=1)
    assert abs(p[:, -1].mean() - 100) < 0.12


def test_heston_shapes_nonnegative_observed_variance():
    p, v, d = simulate_heston_full_truncation(n_paths=50, n_steps=4, seed=2)
    assert p.shape == (50, 5)
    assert v.shape == (50, 5)
    assert np.all(p > 0)
    assert np.all(v >= 0)
    assert 0 <= d.negative_aux_fraction <= 1
