from __future__ import annotations

import json
from pathlib import Path


def load_config(path):
    with Path(path).open(encoding="utf-8") as f:
        cfg = json.load(f)
    required = {
        "experiment_name",
        "model",
        "n_steps",
        "maturity",
        "s0",
        "strike",
        "alpha",
        "kappa",
        "cost_kind",
        "train",
        "test",
    }
    missing = required - cfg.keys()
    if missing:
        raise ValueError(f"missing config keys: {sorted(missing)}")
    return cfg
