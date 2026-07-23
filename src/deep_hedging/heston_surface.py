from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from .heston_pricing import heston_delta_fd


@dataclass
class HestonDeltaSurface:
    tau_grid: np.ndarray
    log_moneyness_grid: np.ndarray
    variance_grid: np.ndarray
    delta_values: np.ndarray

    @classmethod
    def load(cls, path: str | Path) -> HestonDeltaSurface:
        data = np.load(path)
        return cls(
            data["tau_grid"],
            data["log_moneyness_grid"],
            data["variance_grid"],
            data["delta_values"],
        )

    def evaluate(
        self,
        prices: np.ndarray,
        variances: np.ndarray,
        *,
        strike: float,
        maturity: float,
    ) -> np.ndarray:
        p = np.asarray(prices, dtype=float)
        v = np.asarray(variances, dtype=float)
        if p.shape != v.shape:
            raise ValueError("prices and variances must have identical shapes")
        n = p.shape[1] - 1
        tau = maturity - np.arange(n) * maturity / n
        logm = np.log(p[:, :-1] / strike)
        vv = np.maximum(v[:, :-1], 0.0)
        tau_b = np.broadcast_to(tau, logm.shape)
        tau_b = np.clip(tau_b, self.tau_grid[0], self.tau_grid[-1])
        logm = np.clip(logm, self.log_moneyness_grid[0], self.log_moneyness_grid[-1])
        vv = np.clip(vv, self.variance_grid[0], self.variance_grid[-1])
        interp = RegularGridInterpolator(
            (self.tau_grid, self.log_moneyness_grid, self.variance_grid),
            self.delta_values,
            bounds_error=False,
            fill_value=None,
        )
        points = np.column_stack([tau_b.ravel(), logm.ravel(), vv.ravel()])
        return interp(points).reshape(logm.shape)


def build_heston_delta_surface(
    *,
    tau_grid: np.ndarray,
    log_moneyness_grid: np.ndarray,
    variance_grid: np.ndarray,
    strike: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
    rate: float = 0.0,
    integration_limit: float = 120.0,
) -> HestonDeltaSurface:
    tau_grid = np.asarray(tau_grid, dtype=float)
    log_moneyness_grid = np.asarray(log_moneyness_grid, dtype=float)
    variance_grid = np.asarray(variance_grid, dtype=float)
    values = np.empty((tau_grid.size, log_moneyness_grid.size, variance_grid.size), dtype=float)
    for i, tau in enumerate(tau_grid):
        for j, logm in enumerate(log_moneyness_grid):
            spot = strike * np.exp(logm)
            for h, variance in enumerate(variance_grid):
                values[i, j, h] = heston_delta_fd(
                    spot,
                    strike,
                    tau,
                    v=variance,
                    kappa=kappa,
                    theta=theta,
                    xi=xi,
                    rho=rho,
                    rate=rate,
                    integration_limit=integration_limit,
                )
    return HestonDeltaSurface(tau_grid, log_moneyness_grid, variance_grid, values)


def save_surface(path: str | Path, surface: HestonDeltaSurface) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        p,
        tau_grid=surface.tau_grid,
        log_moneyness_grid=surface.log_moneyness_grid,
        variance_grid=surface.variance_grid,
        delta_values=surface.delta_values,
    )
