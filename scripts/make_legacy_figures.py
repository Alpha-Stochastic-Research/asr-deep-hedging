#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "results/legacy"
OUT = ROOT / "paper/figures"
OUT.mkdir(parents=True, exist_ok=True)


def baseline() -> None:
    frame = pd.read_csv(LEGACY / "baseline.csv").set_index("strategy")
    plot = frame.rename(columns={"mean_loss": "Mean loss", "std_loss": "Std. loss", "cvar_095": "CVaR 0.95"})
    ax = plot.plot(kind="bar", figsize=(7.2, 4.3))
    ax.set_ylabel("Loss units")
    ax.set_xlabel("")
    ax.set_title("Legacy single-run GBM point estimates")
    ax.tick_params(axis="x", rotation=0)
    ax.figure.tight_layout()
    ax.figure.savefig(OUT / "fig_baseline_summary.pdf")
    plt.close(ax.figure)


def sweep() -> None:
    frame = pd.read_csv(LEGACY / "kappa_sweep.csv")
    fig = plt.figure(figsize=(6.8, 4.2))
    ax = fig.add_subplot(111)
    ax.plot(frame["kappa"], frame["deep_avg_abs_trade"], marker="o", label="Deep Hedging")
    ax.plot(frame["kappa"], frame["bs_avg_abs_trade"], marker="o", label="Black-Scholes")
    ax.set_xlabel("Proportional-cost coefficient")
    ax.set_ylabel("Average absolute trade")
    ax.set_title("Legacy single-run turnover estimates")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig_kappa_turnover.pdf")
    plt.close(fig)

    fig = plt.figure(figsize=(6.8, 4.2))
    ax = fig.add_subplot(111)
    ax.plot(frame["kappa"], frame["deep_cvar"], marker="o", label="Deep Hedging")
    ax.plot(frame["kappa"], frame["bs_cvar"], marker="o", label="Black-Scholes")
    ax.set_xlabel("Proportional-cost coefficient")
    ax.set_ylabel("Empirical CVaR 0.95")
    ax.set_title("Legacy single-run tail-risk estimates")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig_kappa_cvar.pdf")
    plt.close(fig)


def extensions() -> None:
    frame = pd.read_csv(LEGACY / "extensions.csv")
    for experiment, filename, title in [
        ("quadratic", "fig_quadratic_summary.pdf", "Quadratic-cost legacy point estimates"),
        ("heston_fixed_vol", "fig_heston_summary.pdf", "Heston fixed-volatility comparison"),
    ]:
        part = frame[frame["experiment"] == experiment].set_index("strategy")
        fig = plt.figure(figsize=(5.8, 4.0))
        ax = fig.add_subplot(111)
        part["cvar_095"].plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Empirical CVaR 0.95")
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=0)
        fig.tight_layout()
        fig.savefig(OUT / filename)
        plt.close(fig)


if __name__ == "__main__":
    baseline()
    sweep()
    extensions()
    print(f"Wrote legacy figures to {OUT}")
