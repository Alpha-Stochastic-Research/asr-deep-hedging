# Changelog

All notable changes to this project are documented here.

## 0.2.0 - 2026-07-24

- Expanded the documented package-root API so training, optimization, benchmark,
  evaluation, feature, risk, simulator, and inventory-policy objects can be
  imported directly from `deep_hedging`.
- Preserved all existing module-level import paths for backward compatibility.
- Added a public-API contract test covering `__all__`, documented imports, and
  the package version.
- Updated the README with PyPI installation, Jupyter upgrade instructions,
  version-0.2.0 imports, API reference, examples, and troubleshooting guidance.
- Updated package metadata, ASR organization URLs, PyPI links, paper DOI, and
  citation metadata.
- Fixed the documentation/package mismatch that caused root-level imports such
  as `train_step`, `Adam`, `black_scholes_delta`, and `evaluate_positions` to
  fail in version 0.1.0.

## 0.1.0 - 2026-07-20

- Published the initial package and research repository.
- Reframed the manuscript as a transparent partial replication.
- Added exact finite-sample CVaR and corrected transaction-cost gradients.
- Added GBM and fully specified full-truncation Heston simulators.
- Added state-only and inventory-aware neural policies with manual gradients.
- Added cost-aware benchmarks, validation-only calibration, paired bootstrap,
  multi-seed plans, and a claim register.
- Added unit tests, gradient checks, reproducibility smoke runs, LaTeX CI,
  release automation, issue forms, CODEOWNERS, citation metadata, and review
  documentation.
