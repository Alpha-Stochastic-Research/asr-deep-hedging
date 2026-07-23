import numpy as np

from deep_hedging.benchmarks import (
    black_scholes_delta,
    instantaneous_vol_delta,
    no_trade_band,
    reduced_frequency,
)


def test_delta_bounds():
    p = np.full((3, 5), 100.0)
    d = black_scholes_delta(p, strike=100, maturity=1, sigma=0.2)
    assert np.all((d >= 0) & (d <= 1))


def test_band_and_frequency_shapes():
    t = np.array([[0.1, 0.12, 0.4, 0.41]])
    assert no_trade_band(t, 0.05).shape == t.shape
    assert reduced_frequency(t, 2).shape == t.shape


def test_instantaneous_vol_delta_shape():
    p = np.full((2, 5), 100.0)
    v = np.full_like(p, 0.04)
    d = instantaneous_vol_delta(p, v, strike=100, maturity=1)
    assert d.shape == (2, 4)
