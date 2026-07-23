<div align="center">

# ASR Deep Hedging

### Auditable neural option hedging under transaction costs

[![CI](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/ci.yml/badge.svg)](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/ci.yml)
[![Paper](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/paper.yml/badge.svg)](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/paper.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.1.0-0F766E)](CHANGELOG.md)
[![PyPI](https://img.shields.io/badge/PyPI-publication%20pending-F59E0B?logo=pypi&logoColor=white)](#installation)
[![Code license](https://img.shields.io/badge/code-MIT-16A34A)](LICENSE)
[![Manuscript license](https://img.shields.io/badge/manuscript-CC%20BY%204.0-64748B)](LICENSE-manuscript.txt)

**A transparent NumPy library for discrete-time option hedging, exact empirical CVaR optimization, transaction-cost modelling, and reproducible simulation experiments.**

[Installation](#installation) · [Library quick start](#library-quick-start) · [Public API](#public-python-api) · [Experiments](#repository-experiments) · [Manuscript](#manuscript)

</div>

---

## Overview

`asr-deep-hedging` is an installable research library for studying neural hedging under discrete rebalancing and transaction costs. It is designed for researchers, students, and quantitative developers who need an implementation whose loss convention, risk estimator, simulation scheme, policy gradients, and evaluation protocol can be inspected directly.

The repository combines:

- the installable distribution `asr-deep-hedging`;
- the Python import package `deep_hedging`;
- Geometric Brownian Motion and Heston simulators;
- proportional and quadratic transaction costs;
- exact finite-sample empirical CVaR weighting;
- state-only and inventory-aware neural policies;
- manual NumPy forward and backward passes;
- classical hedging benchmarks and evaluation utilities;
- automated tests, reproducible configurations, figures, and manuscript sources.

> **Scientific scope.** This software is intended for methodological research, numerical validation, and reproducibility. The legacy numerical values retained in `results/legacy/` are exploratory single-run outputs. They are not evidence of general trading superiority and are not intended for live trading or investment decisions.

## Package identity

The name used by `pip` is different from the name used in Python imports:

```text
Distribution name:  asr-deep-hedging
Import package:     deep_hedging
Current version:    0.1.0
Required Python:    3.11 or newer
```

After installation, import the library as follows:

```python
import deep_hedging

print(deep_hedging.__version__)
```

Expected output:

```text
0.1.0
```

## Installation

### Current installation from GitHub

Until the first public PyPI release is completed, install the package directly from the ASR repository:

```bash
python -m pip install --upgrade pip
python -m pip install \
  "asr-deep-hedging @ git+https://github.com/Alpha-Stochastic-Research/asr-deep-hedging.git"
```

After the corresponding release tag exists, install that exact version with:

```bash
python -m pip install \
  "asr-deep-hedging @ git+https://github.com/Alpha-Stochastic-Research/asr-deep-hedging.git@v0.1.0"
```

### PyPI installation

Once version `0.1.0` has been published to PyPI, the standard installation command will be:

```bash
python -m pip install asr-deep-hedging
```

The PyPI workflow is already included in the repository, but the command above becomes publicly available only after the first release has successfully been published.

### Installation from a wheel

Build or download the wheel, then run:

```bash
python -m pip install ./asr_deep_hedging-0.1.0-py3-none-any.whl
```

### Editable development installation

```bash
git clone https://github.com/Alpha-Stochastic-Research/asr-deep-hedging.git
cd asr-deep-hedging

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Conda

```bash
conda env create -f environment.yml
conda activate asr-deep-hedging
python -m pip install -e '.[dev]'
```

### Docker

```bash
docker build -t asr-deep-hedging .
docker run --rm asr-deep-hedging
```

## Library quick start

### Simulate GBM paths and compute empirical CVaR

```python
import numpy as np

from deep_hedging import empirical_cvar, simulate_gbm

prices = simulate_gbm(
    n_paths=20_000,
    n_steps=30,
    s0=100.0,
    maturity=30 / 252,
    mu=0.0,
    sigma=0.20,
    seed=42,
)

strike = 100.0
losses = np.maximum(prices[:, -1] - strike, 0.0)

cvar_95 = empirical_cvar(losses, alpha=0.95)
print(f"Empirical CVaR 95%: {cvar_95:.6f}")
```

`simulate_gbm` returns an array with shape `(n_paths, n_steps + 1)`. The first column contains the initial spot and the final column contains the terminal spot.

### Evaluate a Black--Scholes delta hedge

```python
from deep_hedging import (
    black_scholes_delta,
    evaluate_positions,
    simulate_gbm,
)

maturity = 30 / 252

prices = simulate_gbm(
    n_paths=30_000,
    n_steps=30,
    s0=100.0,
    maturity=maturity,
    sigma=0.20,
    seed=2026,
)

deltas = black_scholes_delta(
    prices,
    strike=100.0,
    maturity=maturity,
    sigma=0.20,
)

metrics, losses = evaluate_positions(
    prices,
    deltas,
    strike=100.0,
    kappa=0.01,
    cost_kind="linear",
    alpha=0.95,
)

for name, value in metrics.items():
    print(f"{name}: {value}")
```

Returned metrics include the number of paths, mean loss, loss standard deviation, empirical VaR, empirical CVaR, average absolute trade, and mean total transaction cost.

### Train one state-only neural policy step

```python
from deep_hedging import Adam, TanhMLP, simulate_gbm, train_step

maturity = 30 / 252
network = TanhMLP(input_dim=2, hidden=16, delta_max=1.5, seed=1)
optimizer = Adam(network.params, lr=3e-3)

prices = simulate_gbm(
    n_paths=4_096,
    n_steps=30,
    s0=100.0,
    maturity=maturity,
    sigma=0.20,
    seed=100,
)

cvar, losses, deltas, details, grad_norm = train_step(
    network,
    optimizer,
    prices=prices,
    strike=100.0,
    maturity=maturity,
    alpha=0.95,
    kappa=0.01,
    cost_kind="linear",
)

print(f"CVaR: {cvar:.6f}")
print(f"Gradient norm: {grad_norm:.6f}")
print(f"Positions shape: {deltas.shape}")
```

For GBM, the state-only policy uses two inputs: normalized time to maturity and log-moneyness.

## Main capabilities

### Market simulation

- Exact grid-point Geometric Brownian Motion simulation.
- Full-truncation Euler variance dynamics with log-Euler spot updates for Heston.
- Reproducible random seeds.
- Optional Heston substepping.
- Diagnostics for auxiliary variance states and terminal variance.

### Risk and loss functions

- Exact empirical CVaR for finite samples.
- Fractional weighting at the empirical tail boundary.
- Stable sorting for deterministic tie handling.
- Empirical VaR.
- Terminal hedging loss and pathwise position gradients.
- Proportional and quadratic transaction costs.
- Optional initial premium and terminal liquidation cost.

### Neural policies

- Shared-weight two-hidden-layer `tanh` network.
- State-only target-position policy.
- Inventory-aware semi-recurrent policy.
- Manual feedforward and backward passes.
- Backpropagation through the inventory state.
- NumPy implementation of Adam.

### Benchmarks and evaluation

- No hedge.
- Black--Scholes delta.
- Shrunk Black--Scholes delta.
- Reduced-frequency rebalancing.
- No-trade-band rule.
- Instantaneous-volatility delta under stochastic volatility.
- Mean loss, standard deviation, VaR, CVaR, turnover, and transaction-cost metrics.
- Paired bootstrap confidence intervals for CVaR differences.

## Core mathematical conventions

### Terminal loss

For a short European call with payoff `H(S_T)`, initial premium `p_0`, positions `delta_k`, and transaction costs `c_k`, the implemented terminal loss is:

```math
L_T
=
H(S_T)-p_0
-
\sum_{k=0}^{n-1}\delta_k\left(S_{k+1}-S_k\right)
+
\sum_k c_k\left(\delta_k-\delta_{k-1}\right).
```

The default numerical convention uses `premium=0.0` and `terminal_liquidation=False`.

### Exact empirical CVaR

For losses sorted from largest to smallest,

```math
L_{[1]} \geq L_{[2]} \geq \cdots \geq L_{[B]},
```

let

```math
q=(1-\alpha)B,
\qquad
r=\lfloor q\rfloor,
\qquad
\lambda=q-r.
```

The library computes:

```math
\widehat{\mathrm{CVaR}}_{\alpha,B}
=
\frac{1}{q}
\left(
\sum_{j=1}^{r}L_{[j]}
+
\lambda L_{[r+1]}
\right),
```

with the fractional boundary term omitted when `lambda = 0`. The same weights are used to construct a valid empirical subgradient away from sorting ties.

## Detailed library examples

### Compute hedging losses and position gradients

```python
import numpy as np

from deep_hedging import hedging_loss_and_gradient, simulate_gbm

prices = simulate_gbm(
    n_paths=5_000,
    n_steps=30,
    s0=100.0,
    maturity=30 / 252,
    sigma=0.20,
    seed=7,
)

deltas = np.zeros((prices.shape[0], prices.shape[1] - 1))

losses, position_gradient, details = hedging_loss_and_gradient(
    prices,
    deltas,
    strike=100.0,
    kappa=0.01,
    cost_kind="linear",
    premium=0.0,
    terminal_liquidation=False,
)

print(losses.shape)             # (5000,)
print(position_gradient.shape)  # (5000, 30)
print(details.trades.shape)     # (5000, 30)
print(details.costs.shape)      # (5000, 30)
```

### Train a state-only policy over multiple iterations

```python
from deep_hedging import Adam, TanhMLP, simulate_gbm, train_step

strike = 100.0
maturity = 30 / 252
network = TanhMLP(input_dim=2, hidden=16, delta_max=1.5, seed=1)
optimizer = Adam(network.params, lr=3e-3)

for iteration in range(200):
    prices = simulate_gbm(
        n_paths=4_096,
        n_steps=30,
        s0=100.0,
        maturity=maturity,
        sigma=0.20,
        seed=10_000 + iteration,
    )

    cvar, losses, deltas, details, grad_norm = train_step(
        network,
        optimizer,
        prices=prices,
        strike=strike,
        maturity=maturity,
        alpha=0.95,
        kappa=0.01,
        cost_kind="linear",
    )

    if iteration % 25 == 0:
        print(
            f"iteration={iteration:03d} "
            f"cvar={cvar:.6f} "
            f"grad_norm={grad_norm:.6f}"
        )
```

Each training step:

1. constructs market-state features;
2. evaluates the policy at every trading date;
3. computes terminal losses and transaction-cost-coupled position gradients;
4. assigns exact empirical-CVaR tail weights;
5. accumulates network gradients across dates;
6. applies one Adam update.

### Train an inventory-aware policy

The inventory-aware policy receives the previous position as an additional input. Under GBM, the network therefore uses three inputs rather than two.

```python
from deep_hedging import Adam, TanhMLP, inventory_policy_step, simulate_gbm

maturity = 30 / 252
network = TanhMLP(input_dim=3, hidden=16, delta_max=1.5, seed=2)
optimizer = Adam(network.params, lr=3e-3)

prices = simulate_gbm(
    n_paths=4_096,
    n_steps=30,
    maturity=maturity,
    sigma=0.20,
    seed=123,
)

cvar, losses, deltas, details, grad_norm = inventory_policy_step(
    network,
    optimizer,
    prices=prices,
    strike=100.0,
    maturity=maturity,
    alpha=0.95,
    kappa=0.01,
    cost_kind="linear",
)

print(f"CVaR: {cvar:.6f}")
print(f"Average absolute trade: {abs(details.trades).mean():.6f}")
```

### Simulate Heston paths

```python
from deep_hedging import simulate_heston_full_truncation

prices, variances, diagnostics = simulate_heston_full_truncation(
    n_paths=20_000,
    n_steps=30,
    s0=100.0,
    maturity=30 / 252,
    v0=0.04,
    kappa_v=2.0,
    theta_v=0.04,
    xi=0.5,
    rho=-0.7,
    substeps=4,
    seed=42,
)

print(prices.shape)
print(variances.shape)
print(diagnostics)
```

For state-only Heston training, instantiate `TanhMLP(input_dim=3, ...)` and pass `variances=variances` to `train_step`. The three features are normalized time to maturity, log-moneyness, and truncated instantaneous variance.

### Compare two strategies with a paired bootstrap

```python
from deep_hedging import paired_bootstrap_cvar_difference

comparison = paired_bootstrap_cvar_difference(
    loss_a=losses_strategy_a,
    loss_b=losses_strategy_b,
    alpha=0.95,
    n_boot=2_000,
    seed=42,
)

print(comparison)
```

The returned dictionary contains the estimated CVaR difference and the 2.5% and 97.5% bootstrap quantiles.

## Public Python API

The following objects are exported directly from `deep_hedging`:

```python
from deep_hedging import (
    Adam,
    HestonDiagnostics,
    LossBreakdown,
    TanhMLP,
    TrainRecord,
    black_scholes_delta,
    build_features,
    empirical_cvar,
    empirical_cvar_weights,
    empirical_var,
    evaluate_positions,
    hedging_loss_and_gradient,
    instantaneous_vol_delta,
    inventory_policy_step,
    inventory_positions,
    no_hedge,
    no_trade_band,
    paired_bootstrap_cvar_difference,
    policy_positions,
    reduced_frequency,
    shrunk_delta,
    simulate_gbm,
    simulate_heston_full_truncation,
    train_step,
)
```

### API summary

| Category | Public objects |
|---|---|
| Simulation | `simulate_gbm`, `simulate_heston_full_truncation`, `HestonDiagnostics` |
| Risk | `empirical_var`, `empirical_cvar`, `empirical_cvar_weights` |
| Losses | `hedging_loss_and_gradient`, `LossBreakdown` |
| Features | `build_features` |
| Networks | `TanhMLP` |
| Optimization | `Adam`, `TrainRecord`, `train_step`, `policy_positions` |
| Inventory-aware policy | `inventory_policy_step`, `inventory_positions` |
| Benchmarks | `no_hedge`, `black_scholes_delta`, `shrunk_delta`, `reduced_frequency`, `no_trade_band`, `instantaneous_vol_delta` |
| Evaluation | `evaluate_positions`, `paired_bootstrap_cvar_difference` |

### Core array conventions

| Object | Shape | Meaning |
|---|---:|---|
| `prices` | `(B, n + 1)` | Initial spot plus prices at all trading endpoints |
| `variances` | `(B, n + 1)` | Truncated Heston variance observations |
| `features` | `(B, n, d)` | Policy state at every decision date |
| `deltas` | `(B, n)` | Position held over every trading interval |
| `trades` | `(B, n)` | Position changes from the previous holding |
| `losses` | `(B,)` | Terminal loss by path |
| `position_gradient` | `(B, n)` | Pathwise derivative of loss with respect to each position |

Here, `B` is the number of simulated paths, `n` the number of trading intervals, and `d` the feature dimension.

## Repository experiments

The package API can be used independently, while the `scripts/` directory provides reproducible command-line experiments.

### Smoke experiment

```bash
python scripts/run_experiment.py \
  --config configs/smoke_gbm_linear.json \
  --output results/generated/smoke_gbm_linear
```

### Inventory-aware smoke experiment

```bash
python scripts/run_experiment.py \
  --config configs/smoke_gbm_inventory.json \
  --output results/generated/smoke_gbm_inventory
```

### Heston smoke experiment

```bash
python scripts/run_experiment.py \
  --config configs/smoke_heston_linear.json \
  --output results/generated/smoke_heston_linear
```

### Confirmatory experiment plan

```bash
python scripts/run_plan.py \
  --plan configs/plans/confirmatory_gbm_cost_sweep.json
```

Before running a confirmatory campaign, freeze the source commit, environment, seeds, validation rule, and output directory as described in [`docs/reproducibility.md`](docs/reproducibility.md).

### Benchmark calibration

```bash
python scripts/calibrate_benchmarks.py \
  --config configs/confirmatory_gbm_linear_k001.json \
  --output results/generated/benchmark_calibration.json
```

Calibration paths must remain separate from final evaluation paths.

### Heston delta surface

```bash
python scripts/precompute_heston_delta.py \
  --config configs/heston_delta_surface_example.json \
  --output results/generated/heston_delta_surface.npz
```

Reference the generated file through `heston_delta_surface` in the corresponding Heston experiment configuration.

## Verification

Run the complete local validation suite:

```bash
make lint
make test
make gradient-check
make smoke
make paper
```

Equivalent direct commands include:

```bash
ruff check src tests scripts
pytest
python scripts/validate_gradients.py
python scripts/reproduce_all.py --profile smoke
```

The repository validates:

- finite-sample CVaR boundary weighting;
- cash translation;
- deterministic GBM simulation;
- GBM mean behavior;
- Heston output constraints and pricing bounds;
- transaction-cost indexing;
- feedforward-network derivatives;
- pathwise hedging-loss gradients;
- inventory-aware backpropagation.

The finite-difference validator checks the feedforward-network backward pass, the quadratic pathwise hedging-loss gradient, and transaction-cost coupling across adjacent dates. The repository does not claim an independent automatic-differentiation verification of the complete profiled empirical-CVaR parameter gradient.

## Build the package

```bash
python -m pip install --upgrade build
python -m build
```

The command creates a source distribution and a wheel under `dist/`.

Test the wheel in a clean virtual environment:

```bash
python -m venv .package-test
source .package-test/bin/activate
python -m pip install dist/asr_deep_hedging-0.1.0-py3-none-any.whl
python -c "import deep_hedging; print(deep_hedging.__version__)"
```

## Publish to PyPI

The repository contains `.github/workflows/publish-pypi.yml`, configured for PyPI Trusted Publishing through OpenID Connect.

Required publisher values:

```text
PyPI project:       asr-deep-hedging
GitHub owner:       Alpha-Stochastic-Research
GitHub repository:  asr-deep-hedging
Workflow file:      publish-pypi.yml
Environment:        pypi
```

After the trusted publisher is configured, create and push the release tag:

```bash
git tag -a v0.1.0 -m "ASR Deep Hedging v0.1.0"
git push origin v0.1.0
```

The workflow builds and verifies the wheel and source distribution before publishing them. No long-lived PyPI API token is required.

After the workflow succeeds, users will be able to install the package with:

```bash
python -m pip install asr-deep-hedging
```

## Repository structure

```text
asr-deep-hedging/
├── src/deep_hedging/       # Installable Python research library
├── scripts/                # Experiments, diagnostics, tables, and figures
├── configs/                # Smoke and confirmatory configurations
├── tests/                  # Unit, gradient, simulator, and package tests
├── paper/                  # Editable LaTeX and compiled manuscript
├── results/legacy/         # Archived exploratory outputs
├── results/generated/      # Outputs produced by the current code
├── docs/                   # Reproducibility and review documentation
└── authorship/             # Machine-readable CRediT contribution record
```

## Manuscript

The compiled manuscript is available at [`paper/manuscript.pdf`](paper/manuscript.pdf).

Build it locally with:

```bash
make paper
```

The paper presents the implementation conventions, empirical-CVaR treatment, analytic derivatives, archived exploratory experiments, validation status, and scientific limitations.

## Reproducibility policy

Every numerical claim intended for the manuscript should include:

1. a committed configuration and deterministic seeds;
2. raw per-seed outputs and software metadata;
3. an explicit validation and checkpoint-selection rule;
4. paired uncertainty estimates on common test paths;
5. regenerated tables, figures, and manuscript;
6. a clean CI run on the exact reported commit.

Related documentation:

- [`docs/reproducibility.md`](docs/reproducibility.md)
- [`docs/claims-register.md`](docs/claims-register.md)
- [`docs/experiment-matrix.md`](docs/experiment-matrix.md)
- [`docs/model-card.md`](docs/model-card.md)
- [`docs/release-checklist.md`](docs/release-checklist.md)

## Scientific limitations

The library prioritizes transparency and numerical auditability over production-scale performance. Current limitations include:

- exploratory legacy results based on individual training runs;
- incomplete multi-seed confirmatory results;
- no independent autodiff validation of the full profiled-CVaR training gradient;
- simplified liquidity and transaction-cost models;
- an exploratory Heston comparison with asymmetric information sets;
- no modelling of live execution, market impact, latency, or production risk controls.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). GitHub displays the recommended citation in the repository sidebar.

## Contributing

Scientific changes must disclose whether they alter:

- the terminal-loss or premium convention;
- the simulator or stochastic parameters;
- the policy information set;
- the empirical risk estimator;
- benchmark calibration;
- reported numerical results.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## Security and model-risk reporting

Use [`SECURITY.md`](SECURITY.md) for security, numerical-integrity, and model-risk reports. Do not include credentials, confidential datasets, or exploitable details in a public issue.

## License

- Source code: [MIT License](LICENSE).
- Manuscript text: [CC BY 4.0](LICENSE-manuscript.txt).
- Third-party publisher templates, articles, datasets, and figures are not redistributed unless their licenses explicitly permit it.

