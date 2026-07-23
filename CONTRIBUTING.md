# Contributing

Thank you for improving this research artifact. Contributions are welcome when
they preserve scientific traceability and do not overstate numerical evidence.

## Before opening a pull request

1. Open an issue for changes to the scientific specification.
2. State whether the proposal changes the loss convention, transaction costs,
   terminal liquidation, risk estimator, simulator, policy information set,
   benchmark calibration, statistical procedure, or manuscript claim.
3. Keep validation, calibration, and final test samples separate.
4. Add or update a committed configuration and deterministic seeds.
5. Add the smallest test that would fail without the proposed change.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Optional pre-commit hooks:

```bash
python -m pip install pre-commit
pre-commit install
```

## Required checks

```bash
make lint
make test
make gradient-check
make smoke
```

Run `make paper` whenever LaTeX, bibliography, tables, figures, or reported
results change.

## Numerical claims

A new manuscript claim requires:

- a configuration file and deterministic seeds;
- raw per-seed outputs or a documented external archive;
- software and hardware metadata;
- a predefined validation and checkpoint-selection rule;
- paired uncertainty estimates on common test paths;
- regenerated tables, figures, manuscript, and claim register.

Exploratory values must be labeled as exploratory and must not be silently
promoted into confirmatory tables.

## Pull requests

Use the repository pull-request template. Keep changes focused. Explain the
scientific impact, not only the code diff. Do not commit reviewer-confidential
material, proprietary data, secrets, publisher-owned templates, or third-party
figures without permission.
