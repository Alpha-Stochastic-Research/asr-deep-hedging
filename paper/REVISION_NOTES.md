# Revision notes

This version was edited to make the manuscript cleaner and deliberately modest
in its claims.

## Main changes

- Reframed the paper as an auditable implementation and exploratory study.
- Removed language implying novelty, general superiority, robustness, or a
  definitive replication.
- Corrected the abstract typo and removed precise percentage claims from the
  abstract.
- Explicitly labelled every numerical table as an archived single-run result.
- Reconciled the two different neural-policy CVaR values at `kappa = 0.01` by
  stating that they come from separate training runs.
- Replaced claims such as "reduces", "outperforms", and "direct evidence" with
  point-estimate language supported by the archive.
- Separated completed code validation from planned confirmatory experiments.
- Recorded the local validation result: 14 tests passed; the standalone
  finite-difference validator returned maximum absolute errors of `3.208e-10`
  for the network and `5.410e-10` for the quadratic pathwise loss gradient.
- Kept the missing multi-seed inference, independent autodiff check, tuned
  cost-aware benchmark results, and balanced Heston comparison as explicit
  outstanding work rather than inventing results.
- Standardized author-contribution, funding, conflict-of-interest, and code
  availability statements.
