<div align="center">

# ASR Deep Hedging

### Auditable neural option hedging under transaction costs

[![CI](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/ci.yml/badge.svg)](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/ci.yml)
[![Paper](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/paper.yml/badge.svg)](https://github.com/Alpha-Stochastic-Research/asr-deep-hedging/actions/workflows/paper.yml)
[![PyPI version](https://img.shields.io/pypi/v/asr-deep-hedging?logo=pypi&logoColor=white)](https://pypi.org/project/asr-deep-hedging/)
[![Python versions](https://img.shields.io/pypi/pyversions/asr-deep-hedging?logo=python&logoColor=white)](https://pypi.org/project/asr-deep-hedging/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21519919.svg)](https://doi.org/10.5281/zenodo.21519919)
[![Code license](https://img.shields.io/badge/code-MIT-16A34A)](LICENSE)
[![Manuscript license](https://img.shields.io/badge/manuscript-CC%20BY%204.0-64748B)](LICENSE-manuscript.txt)
[![ASR](https://img.shields.io/badge/Alpha%20Stochastic%20Research-0F172A)](https://www.asr-lab.online/)

**A transparent NumPy research library for discrete-time option hedging, empirical CVaR optimization, transaction-cost modelling, stochastic simulation, and reproducible numerical experiments.**

[Install](#installation) · [Quick start](#quick-start) · [Public API](#public-api-in-version-020) · [API reference](#python-api-reference) · [Experiments](#repository-experiments) · [Paper](#research-paper) · [Troubleshooting](#troubleshooting)

</div>

---

## Overview

`asr-deep-hedging` is an open-source quantitative-finance research package for studying neural option hedging under discrete rebalancing and transaction costs.

The project is designed for researchers, students, reviewers, and quantitative developers who need an implementation whose assumptions and numerical operations can be inspected directly. The code deliberately prioritizes transparency and auditability over production-scale abstraction.

The repository contains:

- an installable Python distribution named `asr-deep-hedging`;
- a Python import package named `deep_hedging`;
- Geometric Brownian Motion and Heston simulators;
- proportional and quadratic transaction-cost models;
- exact finite-sample empirical CVaR weights;
- pathwise hedging-loss gradients;
- manually implemented neural-network forward and backward passes;
- state-only and inventory-aware hedging policies;
- classical hedging benchmarks;
- evaluation and paired-bootstrap utilities;
- tests, configurations, figures, scripts, and manuscript sources.

> [!IMPORTANT]
> This repository is a research and educational implementation. It is not a live-trading system, investment recommendation, execution engine, or claim of universal hedging superiority.

## Research paper

**Deep Hedging under Transaction Costs: An Auditable NumPy Implementation and Exploratory Study**

- Paper DOI: <https://doi.org/10.5281/zenodo.21519919>
- GitHub repository: <https://github.com/Alpha-Stochastic-Research/asr-deep-hedging>
- PyPI package: <https://pypi.org/project/asr-deep-hedging/>

The manuscript documents the implemented loss convention, empirical-CVaR estimator, transaction-cost coupling, neural policies, stochastic simulators, numerical validation, exploratory experiments, and scientific limitations.

## Package identity

The name passed to `pip` is not the same as the Python import name:

```text
Distribution name:  asr-deep-hedging
Import package:     deep_hedging
Current release:    0.2.0
Required Python:    3.11 or newer
```

After installation:

```python
import deep_hedging

print(deep_hedging.__version__)
```

Expected output for the current release:

```text
0.2.0
```

---

## Installation

### Install from PyPI

```bash
python -m pip install --upgrade pip
python -m pip install asr-deep-hedging
```

Upgrade an existing installation:

```bash
python -m pip install --upgrade asr-deep-hedging
```

Verify the installation:

```bash
python -c "import deep_hedging; print(deep_hedging.__version__)"
```

### Install the latest GitHub version

```bash
python -m pip install --upgrade \
  "asr-deep-hedging @ git+https://github.com/Alpha-Stochastic-Research/asr-deep-hedging.git"
```

Install the exact `v0.2.0` tag:

```bash
python -m pip install \
  "asr-deep-hedging @ git+https://github.com/Alpha-Stochastic-Research/asr-deep-hedging.git@v0.2.0"
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

### Conda environment

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

### Jupyter Notebook installation

Install the package in the Python interpreter used by the current notebook:

```python
import sys

print(sys.executable)
!{sys.executable} -m pip install --upgrade asr-deep-hedging
```

After installation or upgrade, restart the Jupyter kernel before importing the package again.

---

## Public API in version 0.2.0

Version `0.2.0` exposes the documented research API directly from the package root. The most commonly used simulators, risk estimators, neural-policy components, benchmark strategies, training functions, and evaluation utilities can now be imported consistently from `deep_hedging`.

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

Module-level imports remain supported for users who prefer explicit namespaces:

```python
from deep_hedging.benchmarks import black_scholes_delta
from deep_hedging.evaluation import evaluate_positions
from deep_hedging.optim import Adam
from deep_hedging.training import train_step
```

### Migration from version 0.1.0

Version `0.1.0` exported only a small subset of the library from `deep_hedging`. Code such as:

```python
from deep_hedging import train_step
```

raised an `ImportError` even though the function existed in `deep_hedging.training`.

Version `0.2.0` resolves that mismatch. After upgrading and restarting the Python or Jupyter process, the root-level import works directly:

```python
from deep_hedging import Adam, TanhMLP, simulate_gbm, train_step
```


---

## Quick start

### 1. Simulate GBM paths and compute empirical CVaR

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
terminal_prices = prices[:, -1]
losses = np.maximum(terminal_prices - strike, 0.0)

cvar_95 = empirical_cvar(losses, alpha=0.95)
print(f"Empirical CVaR 95%: {cvar_95:.6f}")
```

`simulate_gbm` returns a two-dimensional NumPy array:

```text
prices.shape == (n_paths, n_steps + 1)
```

For example, `20_000` paths and `30` time steps produce:

```text
(20000, 31)
```

The additional column contains the initial price at time zero.

### 2. Evaluate a Black--Scholes delta hedge

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
    mu=0.0,
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

The returned metrics are:

| Metric | Meaning |
|---|---|
| `n_paths` | Number of simulated price paths |
| `mean_loss` | Average terminal hedging loss |
| `std_loss` | Sample standard deviation of terminal losses |
| `var` | Empirical Value at Risk at level `alpha` |
| `cvar` | Empirical Conditional Value at Risk at level `alpha` |
| `avg_abs_trade` | Average absolute position change |
| `mean_total_cost` | Average total transaction cost per path |

### 3. Train one state-only neural policy step

```python
from deep_hedging import Adam, TanhMLP, simulate_gbm, train_step

maturity = 30 / 252

network = TanhMLP(
    input_dim=2,
    hidden=16,
    delta_max=1.5,
    seed=1,
)

optimizer = Adam(
    network.params,
    lr=3e-3,
)

prices = simulate_gbm(
    n_paths=4_096,
    n_steps=30,
    s0=100.0,
    maturity=maturity,
    mu=0.0,
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
print(f"Losses shape: {losses.shape}")
print(f"Positions shape: {deltas.shape}")
print(f"Trades shape: {details.trades.shape}")
```

For a GBM state-only policy, `input_dim=2` because the network receives:

1. normalized remaining time to maturity;
2. log-moneyness.

---

## Reading the examples

### What does `seed=42` mean?

The simulations use pseudo-random numbers. A seed fixes the random-number sequence:

```python
seed=42
```

Running the same function with the same parameters and seed generates the same simulated paths. This makes numerical experiments reproducible.

The number `42` is not mathematically special. Any integer can be used:

```python
seed=1
seed=2026
seed=10_000
```

Use different seeds for independent repeated experiments.

### What does `prices[:, -1]` mean?

For a two-dimensional NumPy array:

```python
prices[:, -1]
```

means:

- `:`: select every row, therefore every simulated path;
- `-1`: select the last column, therefore the terminal price.

The result is the vector of terminal prices:

```python
terminal_prices = prices[:, -1]
```

Related indexing examples:

```python
prices[0, :]   # every date for the first path
prices[:, 0]   # initial price for every path
prices[0, -1]  # terminal price of the first path
```

### What is `std_loss`?

`std` is an abbreviation for **standard deviation**, or **écart-type** in French.

The package computes:

```python
losses.std(ddof=1)
```

This is the sample standard deviation:

```math
s
=
\sqrt{
\frac{1}{B-1}
\sum_{i=1}^{B}
\left(L_i-\overline{L}\right)^2
}.
```

The variance is the square of the standard deviation:

```math
s^2
=
\frac{1}{B-1}
\sum_{i=1}^{B}
\left(L_i-\overline{L}\right)^2.
```

A larger `std_loss` means that terminal losses are more dispersed across simulated paths. It does not, by itself, isolate extreme tail losses; this is why the library also reports VaR and CVaR.

### What is `alpha=0.95`?

The value:

```python
alpha=0.95
```

sets the risk confidence level to 95%.

The empirical CVaR then averages the most severe 5% of losses, with exact fractional weighting when the tail contains a non-integer number of observations.

### What is `kappa`?

`kappa` controls the strength of transaction costs.

For proportional costs, a larger `kappa` makes trading more expensive. The policy must then balance hedging accuracy against turnover and execution cost.

### What are `n_paths` and `n_steps`?

```python
n_paths=20_000
n_steps=30
```

- `n_paths` is the number of independently simulated market scenarios;
- `n_steps` is the number of trading intervals between time zero and maturity.

More paths generally reduce Monte Carlo noise but increase memory use and execution time.

---

## Main capabilities

### Market simulation

- Geometric Brownian Motion on a discrete time grid.
- Heston stochastic-volatility simulation.
- Full-truncation Euler treatment of the variance process.
- Log-Euler spot updates.
- Optional Heston substeps.
- Deterministic random seeds.
- Heston variance diagnostics.

### Risk measurement

- Empirical Value at Risk.
- Exact finite-sample empirical CVaR.
- Fractional weighting at the empirical tail boundary.
- Stable sorting for deterministic tie treatment.
- Empirical-CVaR path weights for gradient aggregation.

### Hedging loss and costs

- Short European call payoff.
- Discrete self-financing trading gains.
- Optional initial premium.
- Proportional transaction costs.
- Quadratic transaction costs.
- Optional terminal liquidation.
- Pathwise derivatives with respect to positions.

### Neural policies

- Shared-weight, two-hidden-layer `tanh` network.
- Bounded position output through `delta_max`.
- State-only target-position policy.
- Inventory-aware semi-recurrent policy.
- Manual NumPy forward propagation.
- Manual NumPy backward propagation.
- Backpropagation through the previous-position state.
- NumPy implementation of Adam.

### Benchmarks and evaluation

- No hedge.
- Black--Scholes delta.
- Shrunk Black--Scholes delta.
- Reduced-frequency rebalancing.
- No-trade-band strategy.
- Instantaneous-volatility delta under stochastic volatility.
- Mean loss, standard deviation, VaR, CVaR, trading, and cost metrics.
- Paired bootstrap confidence intervals for CVaR differences.

---

## Core mathematical conventions

### Simulated GBM dynamics

The GBM simulator uses:

```math
S_{t+\Delta t}
=
S_t
\exp\left[
\left(\mu-\frac{1}{2}\sigma^2\right)\Delta t
+
\sigma\sqrt{\Delta t}\,Z
\right],
\qquad Z\sim\mathcal N(0,1).
```

### Terminal hedging loss

For a short European call with payoff `H(S_T)`, premium `p_0`, positions `delta_k`, and transaction costs `c_k`, the implemented terminal loss is:

```math
L_T
=
H(S_T)-p_0
-
\sum_{k=0}^{n-1}
\delta_k\left(S_{k+1}-S_k\right)
+
\sum_k c_k.
```

The current numerical defaults are:

```python
premium=0.0
terminal_liquidation=False
```

These conventions must be kept fixed when comparing strategies.

### Exact finite-sample empirical CVaR

Let the losses be sorted from largest to smallest:

```math
L_{[1]}\ge L_{[2]}\ge\cdots\ge L_{[B]}.
```

Define:

```math
q=(1-\alpha)B,
\qquad
r=\lfloor q\rfloor,
\qquad
\lambda=q-r.
```

The estimator is:

```math
\widehat{\operatorname{CVaR}}_{\alpha,B}
=
\frac{1}{q}
\left(
\sum_{j=1}^{r}L_{[j]}
+
\lambda L_{[r+1]}
\right).
```

When `lambda = 0`, the fractional boundary term is omitted.

---

## Detailed examples

### Compute losses and position gradients

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

### Train a state-only policy over several iterations

```python
from deep_hedging import Adam, TanhMLP, simulate_gbm, train_step

strike = 100.0
maturity = 30 / 252

network = TanhMLP(
    input_dim=2,
    hidden=16,
    delta_max=1.5,
    seed=1,
)

optimizer = Adam(
    network.params,
    lr=3e-3,
)

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

1. constructs the market-state features;
2. evaluates the neural policy at each trading date;
3. computes terminal losses and position gradients;
4. constructs the exact empirical-CVaR weights;
5. accumulates parameter gradients across dates;
6. applies one Adam update.

### Train an inventory-aware policy

The inventory-aware policy receives the previous position as an additional input. Under GBM, use `input_dim=3`.

```python
from deep_hedging import TanhMLP, simulate_gbm
from deep_hedging.optim import Adam
from deep_hedging.recurrent import inventory_policy_step

maturity = 30 / 252

network = TanhMLP(
    input_dim=3,
    hidden=16,
    delta_max=1.5,
    seed=2,
)

optimizer = Adam(
    network.params,
    lr=3e-3,
)

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
    mu=0.0,
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

For state-only Heston training, use:

```python
network = TanhMLP(input_dim=3, hidden=16, delta_max=1.5, seed=1)
```

and pass:

```python
variances=variances
```

to `train_step`. The three state features are normalized time to maturity, log-moneyness, and truncated instantaneous variance.

### Compare two strategies using a paired bootstrap

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

The result contains:

```text
estimate
ci_low
ci_high
```

The confidence interval is built from paired resampling, so the two strategies should be evaluated on the same market paths.

---

## Python API reference

### Package-root API in version 0.2.0

| Category | Public objects |
|---|---|
| Simulation | `simulate_gbm`, `simulate_heston_full_truncation`, `HestonDiagnostics` |
| Risk | `empirical_var`, `empirical_cvar`, `empirical_cvar_weights` |
| Losses | `hedging_loss_and_gradient`, `LossBreakdown` |
| Features | `build_features` |
| Neural network | `TanhMLP` |
| Optimization and training | `Adam`, `TrainRecord`, `train_step`, `policy_positions` |
| Inventory-aware policy | `inventory_policy_step`, `inventory_positions` |
| Benchmarks | `no_hedge`, `black_scholes_delta`, `shrunk_delta`, `reduced_frequency`, `no_trade_band`, `instantaneous_vol_delta` |
| Evaluation | `evaluate_positions`, `paired_bootstrap_cvar_difference` |

All objects above are available directly from `deep_hedging`. Their original module-level import paths remain valid.

### Module-level API

| Category | Module | Main objects |
|---|---|---|
| Simulation | `deep_hedging.simulators` | `simulate_gbm`, `simulate_heston_full_truncation`, `HestonDiagnostics` |
| Risk | `deep_hedging.risk` | `empirical_var`, `empirical_cvar`, `empirical_cvar_weights` |
| Losses | `deep_hedging.losses` | `hedging_loss_and_gradient`, `LossBreakdown` |
| Features | `deep_hedging.features` | `build_features` |
| Network | `deep_hedging.network` | `TanhMLP` |
| Optimizer | `deep_hedging.optim` | `Adam` |
| State-only training | `deep_hedging.training` | `train_step`, `policy_positions`, `TrainRecord` |
| Inventory policy | `deep_hedging.recurrent` | `inventory_policy_step`, `inventory_positions` |
| Benchmarks | `deep_hedging.benchmarks` | `no_hedge`, `black_scholes_delta`, `shrunk_delta`, `reduced_frequency`, `no_trade_band`, `instantaneous_vol_delta` |
| Evaluation | `deep_hedging.evaluation` | `evaluate_positions`, `paired_bootstrap_cvar_difference` |

### Core array conventions

| Object | Shape | Meaning |
|---|---:|---|
| `prices` | `(B, n + 1)` | Initial spot and all subsequent prices |
| `variances` | `(B, n + 1)` | Truncated Heston variance observations |
| `features` | `(B, n, d)` | Policy state at every decision date |
| `deltas` | `(B, n)` | Position held during each trading interval |
| `trades` | `(B, n)` | Position changes relative to the previous holding |
| `losses` | `(B,)` | Terminal loss for every path |
| `position_gradient` | `(B, n)` | Derivative of pathwise loss with respect to each position |

Here:

- `B` is the number of simulated paths;
- `n` is the number of trading intervals;
- `d` is the number of policy features.

---

## Repository experiments

The Python API can be used independently. The `scripts/` directory provides command-line experiments and validation utilities.

### GBM smoke experiment

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

Before running a confirmatory experiment campaign, freeze:

- the source commit;
- the software environment;
- the simulation seeds;
- the training and validation rules;
- the evaluation paths;
- the output directory.

See [`docs/reproducibility.md`](docs/reproducibility.md).

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

---

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

The repository tests include:

- finite-sample CVaR boundary weighting;
- deterministic CVaR tie handling;
- cash translation;
- deterministic GBM simulation;
- GBM mean behavior;
- Heston dimensions and variance constraints;
- pricing-bound checks;
- transaction-cost indexing;
- neural-network backward derivatives;
- pathwise hedging-loss gradients;
- inventory-aware backpropagation.

The project validates several analytic derivatives using centered finite differences. It does not claim an independent automatic-differentiation validation of the entire profiled empirical-CVaR parameter gradient.

---

## Build the package

```bash
python -m pip install --upgrade build
python -m build
```

The command creates a source distribution and wheel under `dist/`.

Test the wheel in a clean environment:

```bash
python -m venv .package-test
source .package-test/bin/activate
python -m pip install dist/asr_deep_hedging-0.2.0-py3-none-any.whl
python -c "import deep_hedging; print(deep_hedging.__version__)"
```

---

## Repository structure

```text
asr-deep-hedging/
├── src/deep_hedging/       # Installable Python research library
├── scripts/                # Experiments, diagnostics, tables, and figures
├── configs/                # Smoke and confirmatory configurations
├── tests/                  # Unit, simulator, gradient, and package tests
├── paper/                  # Editable LaTeX and compiled manuscript
├── results/legacy/         # Archived exploratory outputs
├── results/generated/      # Outputs generated by the current code
├── docs/                   # Reproducibility and scientific-review documents
└── authorship/             # Machine-readable contribution records
```

---

## Reproducibility policy

Every numerical result intended for scientific reporting should include:

1. a committed experiment configuration;
2. deterministic and documented random seeds;
3. the exact source commit;
4. software and hardware metadata;
5. raw per-seed outputs;
6. a predefined validation and checkpoint-selection rule;
7. evaluation on paths not used for calibration;
8. uncertainty estimates based on common test paths;
9. regenerated tables, figures, and manuscript;
10. a clean CI run for the reported commit.

Related documents:

- [`docs/reproducibility.md`](docs/reproducibility.md)
- [`docs/claims-register.md`](docs/claims-register.md)
- [`docs/experiment-matrix.md`](docs/experiment-matrix.md)
- [`docs/model-card.md`](docs/model-card.md)
- [`docs/release-checklist.md`](docs/release-checklist.md)

---

## Scientific limitations

The implementation prioritizes auditability and methodological clarity. Current limitations include:

- exploratory legacy results based on individual training runs;
- incomplete multi-seed confirmatory evidence;
- no independent automatic-differentiation validation of the full profiled-CVaR training gradient;
- simplified proportional and quadratic cost models;
- an exploratory Heston comparison with potentially asymmetric information sets;
- no live execution, market impact, latency, order-book, funding, or production-risk model;
- no claim that the learned strategy is globally optimal;
- no claim that historical or simulated performance predicts future performance.

---

## Troubleshooting

### `ImportError` for `train_step`, `Adam`, `black_scholes_delta`, or `evaluate_positions`

These objects are exported directly from `deep_hedging` beginning with version `0.2.0`.

Check the installed version:

```python
import deep_hedging

print(deep_hedging.__version__)
```

Upgrade the package in the active Python environment:

```bash
python -m pip install --upgrade asr-deep-hedging
```

For Jupyter, install through the active kernel and then restart the kernel:

```python
import sys

!{sys.executable} -m pip install --upgrade asr-deep-hedging
```

After upgrading, the following imports should work:

```python
from deep_hedging import (
    Adam,
    black_scholes_delta,
    evaluate_positions,
    train_step,
)
```

Module-level imports remain a compatible fallback:

```python
from deep_hedging.benchmarks import black_scholes_delta
from deep_hedging.evaluation import evaluate_positions
from deep_hedging.optim import Adam
from deep_hedging.training import train_step
```


### Confirm which package Jupyter is loading

```python
import deep_hedging
import sys

print("Python:", sys.executable)
print("Version:", deep_hedging.__version__)
print("Package file:", deep_hedging.__file__)
```

### Upgrade inside the active Jupyter kernel

```python
import sys

!{sys.executable} -m pip install --upgrade asr-deep-hedging
```

Restart the kernel after the installation finishes.

### Inspect the current top-level API

```python
import deep_hedging

print(deep_hedging.__all__)
```

### Verify the version 0.2.0 public API

```python
from deep_hedging import (
    Adam,
    black_scholes_delta,
    evaluate_positions,
    train_step,
)

print("Version 0.2.0 public imports successful")
```

---

## Citation

When using the software or methodology, cite the paper:

> Alpha Kabinet TOURÉ. *Deep Hedging under Transaction Costs: An Auditable NumPy Implementation and Exploratory Study*. Alpha Stochastic Research, 2026. DOI: 10.5281/zenodo.21519919.

BibTeX:

```bibtex
@misc{toure2026deephedging,
  author       = {Alpha Kabinet TOURÉ},
  title        = {Deep Hedging under Transaction Costs: An Auditable NumPy Implementation and Exploratory Study},
  year         = {2026},
  publisher    = {Alpha Stochastic Research},
  doi          = {10.5281/zenodo.21519919},
  url          = {https://doi.org/10.5281/zenodo.21519919}
}
```

Machine-readable citation metadata are available in [`CITATION.cff`](CITATION.cff).

---

## Contributing

Scientific changes must state whether they alter:

- the payoff, premium, or terminal-loss convention;
- the transaction-cost definition;
- the simulator or stochastic parameters;
- the policy information set;
- the empirical risk estimator;
- the training procedure;
- benchmark calibration;
- validation or checkpoint selection;
- reported numerical results.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## Security and model-risk reporting

Use [`SECURITY.md`](SECURITY.md) for security, numerical-integrity, and model-risk reports. Do not include credentials, confidential datasets, or exploitable details in a public issue.

## License

- Source code: [MIT License](LICENSE)
- Manuscript text: [CC BY 4.0](LICENSE-manuscript.txt)
- Third-party articles, datasets, templates, and figures remain subject to their original licenses.

## Maintainer

**Alpha Kabinet TOURÉ**  
Founder, Alpha Stochastic Research

- Website: <https://www.asr-lab.online/>
- GitHub: <https://github.com/Alpha-Stochastic-Research>
- Repository: <https://github.com/Alpha-Stochastic-Research/asr-deep-hedging>
- Paper: <https://doi.org/10.5281/zenodo.21519919>
- PyPI: <https://pypi.org/project/asr-deep-hedging/>

---

<div align="center">

**Research → Modelling → Analysis → Impact**

Developed by [Alpha Stochastic Research](https://www.asr-lab.online/).

</div>

