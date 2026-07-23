#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deep_hedging.heston_surface import build_heston_delta_surface, save_surface


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    grid = cfg["grid"]
    params = cfg["heston"]
    surface = build_heston_delta_surface(
        tau_grid=np.asarray(grid["tau"], dtype=float),
        log_moneyness_grid=np.asarray(grid["log_moneyness"], dtype=float),
        variance_grid=np.asarray(grid["variance"], dtype=float),
        strike=cfg["strike"],
        kappa=params["kappa_v"],
        theta=params["theta_v"],
        xi=params["xi"],
        rho=params["rho"],
        rate=cfg.get("rate", 0.0),
        integration_limit=cfg.get("integration_limit", 120.0),
    )
    save_surface(args.output, surface)
    print(f"Saved Heston delta surface to {args.output}")


if __name__ == "__main__":
    main()
