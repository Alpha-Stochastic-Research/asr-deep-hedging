#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["smoke", "confirmatory"], default="smoke")
    args = ap.parse_args()
    configs = sorted((ROOT / "configs").glob(f"{args.profile}_*.json"))
    if not configs:
        raise SystemExit("no matching configurations")
    for cfg in configs:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/run_experiment.py"), "--config", str(cfg)], check=True
        )


if __name__ == "__main__":
    main()
