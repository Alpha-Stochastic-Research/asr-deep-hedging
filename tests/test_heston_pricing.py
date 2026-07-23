from deep_hedging.heston_pricing import heston_call_price, heston_delta_fd


def test_heston_price_bounds_and_delta():
    params = dict(v=0.04, kappa=2.0, theta=0.04, xi=0.5, rho=-0.7, rate=0.0)
    c = heston_call_price(100, 100, 30 / 252, **params, integration_limit=80)
    d = heston_delta_fd(100, 100, 30 / 252, **params, integration_limit=80)
    assert 0 < c < 100
    assert 0 < d < 1
