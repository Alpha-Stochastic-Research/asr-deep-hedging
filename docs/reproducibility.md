# Reproducibility protocol

1. Record the git commit, Python version, operating system, BLAS library, dtype,
   and dependency versions.
2. Freeze train/validation/test seeds before confirmatory evaluation.
3. Use validation paths for hyperparameters and checkpoint selection only.
4. Use common test paths for all policies within a comparison.
5. Store `config.resolved.json`, `metrics.json`, `losses.npz`, and
   `positions.npz` for each seed.
6. Report absolute CVaR differences, paired bootstrap intervals, and the
   distribution across training seeds.
7. Regenerate the manuscript tables and figures from these files.
8. Treat `results/legacy/` as historical, not confirmatory.

The exact empirical CVaR uses descending stable sorting and fractional weight
on the boundary observation when `(1-alpha) * B` is non-integer. Linear-cost
subgradients use zero at an exactly zero trade. The baseline charges no terminal
liquidation fee unless the configuration explicitly changes that convention.
