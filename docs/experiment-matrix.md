# Confirmatory experiment matrix

| Axis | Levels |
|---|---|
| Policy state | State-only; previous-position aware |
| Cost type | Proportional; quadratic |
| Proportional cost | 0, 1, 5, 10, 50, 100, 200, 400 bps |
| Benchmark | No hedge; BS; shrunk BS; no-trade band; reduced frequency |
| Price model | GBM; Heston |
| Heston benchmark | Fixed vol; instantaneous vol; interpolated Heston delta |
| Variance feature | Included; removed; permuted; perturbed |
| Heston substeps | 1, 2, 4 |
| Training seeds | At least 10 per cell |
| Test design | Common paths within each paired comparison |
| Primary metric | Absolute empirical CVaR difference |
| Secondary metrics | VaR, mean, standard deviation, cost, turnover |
