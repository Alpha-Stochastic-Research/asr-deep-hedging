## Summary

Describe the change and why it is needed.

## Scientific scope

Check every convention affected by this pull request:

- [ ] Loss, premium, financing, or terminal liquidation
- [ ] Transaction-cost function or temporal indexing
- [ ] CVaR/VaR estimator or boundary convention
- [ ] GBM/Heston simulator or random-number construction
- [ ] Policy architecture, information set, or gradients
- [ ] Benchmark definition or validation calibration
- [ ] Statistical inference, seeds, or checkpoint selection
- [ ] Tables, figures, manuscript claims, or reviewer response
- [ ] No scientific convention changed

## Reproducibility

- [ ] Configuration files and deterministic seeds are committed
- [ ] Validation and test samples remain separated
- [ ] Raw outputs or checksums are included where appropriate
- [ ] Manuscript artifacts were regenerated where required

## Validation

- [ ] `make lint`
- [ ] `make test`
- [ ] `make gradient-check`
- [ ] `make smoke`
- [ ] `make paper` when manuscript files changed
