import numpy as np

from deep_hedging.risk import empirical_cvar, empirical_cvar_weights


def test_fractional_boundary_weights():
    x = np.arange(10.0)
    w = empirical_cvar_weights(x, 0.75)  # q=2.5
    assert np.isclose(w.sum(), 1)
    assert np.isclose(w[9], 0.4)
    assert np.isclose(w[8], 0.4)
    assert np.isclose(w[7], 0.2)
    assert np.isclose(empirical_cvar(x, 0.75), 8.2)


def test_translation():
    x = np.array([1.0, 2.0, 7.0, 9.0])
    assert np.isclose(empirical_cvar(x + 3, 0.5), empirical_cvar(x, 0.5) + 3)
