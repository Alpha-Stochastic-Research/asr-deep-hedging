# Response to Reviewers

- Previous version: initial single-file manuscript
- Revised version: `AKToure/asr-deep-hedging` repository version
- Commit SHA: recorded at release
- Date: 2026-07-20

## Summary of major revisions

1. Reframed the contribution as a transparent partial replication rather than a full reproduction.
2. Corrected the discrete-time benchmark interpretation, cash convention, empirical CVaR, transaction-cost indexing, liquidation convention, and Heston claims.
3. Added a complete reproducibility repository with executable NumPy code, cost-aware benchmarks, tests, CI, configurations, bootstrap inference, and manuscript-generation scripts.

## Major comment 1: Black--Scholes at zero cost

**Reviewer comment**

> The discretized Black--Scholes delta is not necessarily CVaR-optimal, so a neural policy can legitimately outperform it at zero cost.

**Response**

Agreed. All claims of theoretical optimality or of a bug when the neural policy wins were removed. The benchmark is now described as classical and informative, but not as the optimizer of the discrete-time CVaR problem.

**Changed files and lines**

- `paper/sections/01_introduction.tex`
- `paper/sections/05_results.tex`
- `paper/sections/08_conclusion.tex`

**Status:** Resolved

## Major comment 2: Unequal Heston information

**Response**

The historical Heston result is now explicitly labeled a deliberately misspecified-benchmark experiment. The repository adds benchmark and feature-ablation hooks; confirmatory claims require equal information sets, instantaneous-volatility and model-consistent baselines, and distribution-shift tests.

**Changed files and lines**

- `paper/sections/04_data.tex`
- `paper/sections/06_robustness.tex`
- `configs/smoke_heston_linear.json`

**Status:** Resolved in design; confirmatory numerical reruns remain pending

## Major comment 3: CVaR threshold profiling

**Response**

The paper now distinguishes population CVaR from the expectation of profiled mini-batch objectives. The code computes exact finite-sample Expected Shortfall weights, including the fractional boundary observation and deterministic tie handling.

**Changed files and lines**

- `paper/sections/03_methodology.tex`
- `src/deep_hedging/risk.py`
- `tests/test_risk.py`

**Status:** Resolved

## Major comment 4: Transaction-cost gradient

**Response**

The next transaction cost is explicitly indexed by `S_{k+1}`. Boundary cases and terminal liquidation are documented and covered by finite-difference tests.

**Changed files and lines**

- `paper/sections/03_methodology.tex`
- `src/deep_hedging/losses.py`
- `tests/test_losses.py`

**Status:** Resolved

## Major comment 5: Statistical inference and benchmarks

**Response**

A benchmark ladder, paired pathwise bootstrap, multi-seed confirmatory protocol, machine-readable outputs, and a distinction between legacy and generated results were added. Historical numbers remain explicitly exploratory until the confirmatory configurations are executed across all seeds.

**Changed files and lines**

- `src/deep_hedging/benchmarks.py`
- `src/deep_hedging/evaluation.py`
- `paper/sections/06_robustness.tex`
- `results/legacy/README.md`

**Status:** Partially resolved; full computational campaign remains pending

## Major comment 6: Initial premium and translation dependence

**Response**

The manuscript now defines terminal P&L and loss with an explicit initial cash amount. A proposition proves cash translation of CVaR, distinguishes invariant absolute differences from convention-dependent percentage reductions, and identifies the historical tables as using `p0 = 0`.

**Changed files and lines**

- `paper/sections/03_methodology.tex`
- `src/deep_hedging/losses.py`
- `tests/test_risk.py`

**Status:** Resolved

## Major comment 7: Terminal liquidation convention

**Response**

The terminal position is set to zero conceptually, while the historical experiment is identified as imposing a zero terminal liquidation fee. The implementation exposes `terminal_liquidation` as a configuration choice and includes the corresponding derivative in the last position.

**Changed files and lines**

- `paper/sections/03_methodology.tex`
- `src/deep_hedging/costs.py`
- `src/deep_hedging/losses.py`

**Status:** Resolved

## Major comment 8: State-only policy cannot learn an inventory-dependent no-trade region

**Response**

Agreed. The interpretation was narrowed to a smoother or less aggressive state map. An executable inventory-aware policy, receiving the previous position and trained by manual backpropagation through time, was added. Its full gradient is checked by finite differences.

**Changed files and lines**

- `src/deep_hedging/recurrent.py`
- `tests/test_recurrent.py`
- `paper/sections/06_robustness.tex`
- `configs/plans/confirmatory_gbm_cost_sweep.json`

**Status:** Resolved in code; full numerical ablation remains pending

## Major comment 9: The title overstates reproduction

**Response**

The title now says “Transparent NumPy Implementation and Partial Replication.” A dedicated scope table compares policy state, time parameterization, architecture, instruments, benchmark, and objective with Bühler et al. The paper no longer claims experimental equivalence.

**Changed files and lines**

- `paper/main.tex`
- `paper/sections/01_introduction.tex`
- `paper/sections/08_conclusion.tex`

**Status:** Resolved

## Major comment 10: Cost-aware benchmarks are missing

**Response**

The repository adds no hedge, shrunk delta, no-trade band, reduced-frequency delta, instantaneous-volatility delta, and an optional interpolated Heston delta surface. A validation-only calibration script selects classical benchmark parameters before final testing.

**Changed files and lines**

- `src/deep_hedging/benchmarks.py`
- `scripts/calibrate_benchmarks.py`
- `src/deep_hedging/heston_pricing.py`
- `src/deep_hedging/heston_surface.py`

**Status:** Resolved in the pipeline; confirmatory calibrated outputs remain pending

## Major comment 11: Statistical uncertainty and run-to-run variance

**Response**

The manuscript no longer asserts that discrepancies are within expected run-to-run variance without evidence. The code now provides paired pathwise CVaR bootstrap intervals, fixed common test paths, and a multi-seed campaign runner that reports mean, median, and standard deviation across training seeds.

**Changed files and lines**

- `src/deep_hedging/evaluation.py`
- `scripts/run_plan.py`
- `configs/plans/confirmatory_gbm_cost_sweep.json`
- `paper/sections/06_robustness.tex`

**Status:** Resolved in design; the expensive campaign is not fabricated or precomputed

## Major comment 12: The unhedged-mean validation is overstated

**Response**

The revised results calculate the Monte Carlo standard error and note that the historical difference from the analytic price is about 3.1 standard errors. It is no longer described as a strong validation check. The simulator test separately verifies the risk-neutral martingale mean on a large deterministic-seed sample.

**Changed files and lines**

- `paper/sections/05_results.tex`
- `tests/test_simulators.py`

**Status:** Resolved

## Major comment 13: Heston discretization is not reproducible

**Response**

The full-truncation recurrence, correlated shocks, log-price update, observable positive variance, and auxiliary negative-variance diagnostics are implemented explicitly. The simulator accepts substeps and returns the minimum auxiliary variance, negative-state frequency, and mean terminal variance. The confirmatory protocol requires substep sensitivity.

**Changed files and lines**

- `src/deep_hedging/simulators.py`
- `tests/test_simulators.py`
- `paper/sections/04_data.tex`
- `docs/reproducibility.md`

**Status:** Resolved

## Major comment 14: Heston variance-feature use is not identified

**Response**

The manuscript now requires with/without-variance, permuted-feature, and perturbed-feature ablations. The executable pipeline supplies fixed-volatility and instantaneous-volatility deltas; a Heston delta surface can be precomputed from the included semi-closed-form pricer.

**Changed files and lines**

- `paper/sections/05_results.tex`
- `paper/sections/06_robustness.tex`
- `src/deep_hedging/benchmarks.py`
- `scripts/precompute_heston_delta.py`

**Status:** Partially resolved; final ablation outputs remain pending

## Major comment 15: Transaction-cost levels need economic context

**Response**

The text now identifies one and four percent as stress levels rather than universal liquid-equity calibrations. The confirmatory plan adds 1, 5, 10, and 50 basis-point regimes and reports cumulative monetary cost and turnover.

**Changed files and lines**

- `paper/sections/03_methodology.tex`
- `paper/sections/07_limitations.tex`
- `configs/plans/confirmatory_gbm_cost_sweep.json`

**Status:** Resolved

## Major comment 16: Quadratic-cost calibration is not matched

**Response**

The revised paper explicitly states that the historical representative costs differ by a factor of about 3.3 and do not constitute a matched calibration. It proposes matching expected, median, or quantile total cost under a fixed reference strategy before comparison.

**Changed files and lines**

- `paper/sections/05_results.tex`

**Status:** Resolved in interpretation; matched rerun remains pending

## Minor and reproducibility comments

**Response**

The PDE wording, CVaR definition, “best closed-form approximation,” stochastic-gradient terminology, turnover definition, Heston skew language, and generality of the conclusion were narrowed. The repository now includes a pinned scientific specification, configurations, environment declarations, CI, release checklist, CRediT file, licensing, code of conduct, security notice, raw-output conventions, and a generated review PDF.

**Status:** Resolved
