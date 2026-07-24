"""Auditable NumPy implementation for discrete-time deep hedging."""

from .benchmarks import (
    black_scholes_delta,
    instantaneous_vol_delta,
    no_hedge,
    no_trade_band,
    reduced_frequency,
    shrunk_delta,
)
from .evaluation import (
    evaluate_positions,
    paired_bootstrap_cvar_difference,
)
from .features import build_features
from .losses import LossBreakdown, hedging_loss_and_gradient
from .network import TanhMLP
from .optim import Adam
from .recurrent import inventory_policy_step, inventory_positions
from .risk import empirical_cvar, empirical_cvar_weights, empirical_var
from .simulators import (
    HestonDiagnostics,
    simulate_gbm,
    simulate_heston_full_truncation,
)
from .training import TrainRecord, policy_positions, train_step

__all__ = [
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
]

__version__ = "0.2.0"
