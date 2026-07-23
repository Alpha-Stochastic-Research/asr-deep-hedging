#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result-dir", required=True)
    ap.add_argument("--output-dir", default="paper/figures")
    args = ap.parse_args()
    r = Path(args.result_dir)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    obj = json.loads((r / "metrics.json").read_text())
    hist = obj.get("history", [])
    if hist:
        x = [z["iteration"] for z in hist]
        y = [z["cvar"] for z in hist]
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("Iteration")
        plt.ylabel("Batch empirical CVaR")
        plt.tight_layout()
        plt.savefig(out / "training_cvar.pdf")
        plt.close()
    names = list(obj["metrics"])
    vals = [obj["metrics"][n]["cvar"] for n in names]
    plt.figure(figsize=(7, 4))
    plt.bar(names, vals)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Empirical CVaR")
    plt.tight_layout()
    plt.savefig(out / "benchmark_cvar.pdf")
    plt.close()


if __name__ == "__main__":
    main()
