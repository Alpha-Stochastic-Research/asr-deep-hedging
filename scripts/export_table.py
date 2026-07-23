#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result-dir", required=True)
    args = ap.parse_args()
    obj = json.loads((Path(args.result_dir) / "metrics.json").read_text())["metrics"]
    print("strategy,mean_loss,std_loss,var,cvar,avg_abs_trade,mean_total_cost")
    for n, m in obj.items():
        print(
            ",".join(
                [n]
                + [
                    str(m[k])
                    for k in ["mean_loss", "std_loss", "var", "cvar", "avg_abs_trade", "mean_total_cost"]
                ]
            )
        )


if __name__ == "__main__":
    main()
