"""Auditable NumPy implementation for discrete-time deep hedging."""

from .losses import hedging_loss_and_gradient
from .network import TanhMLP
from .risk import empirical_cvar, empirical_cvar_weights
from .simulators import simulate_gbm, simulate_heston_full_truncation

__all__ = [
    "empirical_cvar",
    "empirical_cvar_weights",
    "simulate_gbm",
    "simulate_heston_full_truncation",
    "hedging_loss_and_gradient",
    "TanhMLP",
]
__version__ = "0.1.0"
