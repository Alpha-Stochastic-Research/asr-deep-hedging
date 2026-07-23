# Claims register

| Claim | Evidence currently available | Status allowed in manuscript | Confirmatory requirement |
|---|---|---|---|
| Turnover decreases as proportional cost rises | Five archived single-run point estimates | Descriptive | Multiple seeds and confidence intervals |
| Neural policy beats cost-blind BS at positive costs | Archived point estimates | Descriptive comparison only | Cost-aware calibrated benchmarks and multi-seed inference |
| BS must win at zero cost | None; statement is theoretically false in discrete-time CVaR | Prohibited | Compare without claiming theoretical ordering |
| Policy learns a no-trade region | State-only architecture cannot identify this | Prohibited for historical policy | Inventory-aware ablation and policy-surface diagnostics |
| Heston result proves robustness | Training and testing use the same Heston generator | Prohibited | Distribution-shift experiments |
| Variance feature creates Heston gain | No feature ablation in archived results | Not established | With/without/permuted variance experiments |
| Batch quantile equals population CVaR objective | False at finite batch size | Prohibited | Distinguish empirical profiling from population objective |
| Manual gradients are correct | Unit and finite-difference tests | Supported for tested smooth cases | Preserve CI and add independent autodiff check for release |
| Full reproduction of Bühler et al. | Architecture and instruments differ | Prohibited | Use “partial replication” unless original design is matched |
