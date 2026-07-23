# Research model card

## Intended use

Research on discrete-time option hedging under simulated frictions. The code is
not a production trading, pricing, capital, or regulatory risk system.

## Inputs

Time to maturity, log-moneyness, optional instantaneous variance, and optional
previous position. Inputs are generated from GBM or full-truncation Heston paths.

## Outputs

Target underlying positions. The objective is exact finite-sample empirical
Expected Shortfall of terminal loss under the configured accounting and cost
conventions.

## Known limitations

Scenario dependence, tail-estimation noise, simplified market impact, no live
execution model, no discrete contract sizes, and historical results that have
not yet been regenerated as a multi-seed confirmatory campaign.

## Safe interpretation

Use absolute metric differences and paired uncertainty. Do not infer causal or
out-of-distribution robustness from in-distribution simulation results.
