from __future__ import annotations

import deep_hedging
from deep_hedging.benchmarks import black_scholes_delta
from deep_hedging.evaluation import evaluate_positions
from deep_hedging.optim import Adam
from deep_hedging.training import train_step

EXPECTED_PUBLIC_API = {
    "Adam",
    "HestonDiagnostics",
    "LossBreakdown",
    "TanhMLP",
    "TrainRecord",
    "black_scholes_delta",
    "build_features",
    "empirical_cvar",
    "empirical_cvar_weights",
    "empirical_var",
    "evaluate_positions",
    "hedging_loss_and_gradient",
    "instantaneous_vol_delta",
    "inventory_policy_step",
    "inventory_positions",
    "no_hedge",
    "no_trade_band",
    "paired_bootstrap_cvar_difference",
    "policy_positions",
    "reduced_frequency",
    "shrunk_delta",
    "simulate_gbm",
    "simulate_heston_full_truncation",
    "train_step",
}


def test_version_is_0_2_0() -> None:
    assert deep_hedging.__version__ == "0.2.0"


def test_documented_public_api_is_exported() -> None:
    assert set(deep_hedging.__all__) == EXPECTED_PUBLIC_API

    for name in EXPECTED_PUBLIC_API:
        assert hasattr(deep_hedging, name), f"missing public export: {name}"


def test_root_exports_match_module_objects() -> None:
    assert deep_hedging.Adam is Adam
    assert deep_hedging.black_scholes_delta is black_scholes_delta
    assert deep_hedging.evaluate_positions is evaluate_positions
    assert deep_hedging.train_step is train_step
