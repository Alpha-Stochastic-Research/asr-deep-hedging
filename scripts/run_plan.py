#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    base = json.loads((ROOT / plan["base_config"]).read_text(encoding="utf-8"))
    plan_out = ROOT / "results/generated" / plan["name"]
    plan_out.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []

    for policy in plan.get("policy_types", [base.get("policy_type", "state")]):
        for kappa in plan.get("kappas", [base["kappa"]]):
            for seed in plan["network_seeds"]:
                cfg = copy.deepcopy(base)
                cfg["kappa"] = kappa
                cfg["policy_type"] = policy
                cfg["train"]["network_seed"] = seed
                cfg["train"]["sim_seed"] = plan["simulation_seed_base"] + seed * 10_000
                cfg["test"]["seed"] = plan["test_seed"]
                cfg["experiment_name"] = f"{plan['name']}/{policy}/kappa_{kappa:g}/seed_{seed}"
                with tempfile.NamedTemporaryFile(
                    "w", suffix=".json", delete=False, encoding="utf-8"
                ) as handle:
                    json.dump(cfg, handle)
                    temp_path = Path(handle.name)
                try:
                    subprocess.run(
                        [
                            sys.executable,
                            str(ROOT / "scripts/run_experiment.py"),
                            "--config",
                            str(temp_path),
                        ],
                        check=True,
                    )
                finally:
                    temp_path.unlink(missing_ok=True)

                result_path = ROOT / "results/generated" / cfg["experiment_name"] / "metrics.json"
                result = json.loads(result_path.read_text(encoding="utf-8"))
                for strategy, metrics in result["metrics"].items():
                    records.append(
                        {
                            "policy_type": policy,
                            "kappa": kappa,
                            "seed": seed,
                            "strategy": strategy,
                            **metrics,
                        }
                    )

    keys = sorted({(row["policy_type"], row["kappa"], row["strategy"]) for row in records})
    aggregate: list[dict] = []
    for policy, kappa, strategy in keys:
        rows = [
            row
            for row in records
            if (row["policy_type"], row["kappa"], row["strategy"]) == (policy, kappa, strategy)
        ]
        cvar = np.asarray([row["cvar"] for row in rows], dtype=float)
        aggregate.append(
            {
                "policy_type": policy,
                "kappa": kappa,
                "strategy": strategy,
                "n_seeds": len(rows),
                "cvar_mean": float(cvar.mean()),
                "cvar_sd": float(cvar.std(ddof=1)) if len(cvar) > 1 else None,
                "cvar_median": float(np.median(cvar)),
            }
        )

    (plan_out / "records.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    (plan_out / "aggregate.json").write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
