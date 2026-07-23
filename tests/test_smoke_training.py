from deep_hedging.network import TanhMLP
from deep_hedging.optim import Adam
from deep_hedging.simulators import simulate_gbm
from deep_hedging.training import train_step


def test_one_training_step_finite():
    p = simulate_gbm(n_paths=64, n_steps=4, seed=3)
    n = TanhMLP(2, 4, seed=2)
    o = Adam(n.params)
    value, *_ = train_step(n, o, prices=p, strike=100, maturity=30 / 252, alpha=0.95, kappa=0.01)
    assert value == value
