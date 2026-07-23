# GitHub publication settings

Repository: `AKToure/asr-deep-hedging`

Description:

> Auditable NumPy implementation and partial replication of deep hedging under transaction costs and stochastic volatility.

Recommended topics:

- `deep-hedging`
- `option-hedging`
- `cvar`
- `heston-model`
- `numpy`
- `reproducible-research`
- `quantitative-finance`
- `transaction-costs`

Recommended repository settings:

1. Use `main` as the default branch.
2. Enable Issues and Discussions.
3. Disable the wiki unless it is actively maintained.
4. Require pull requests before merging into `main`.
5. Require the `test`, `smoke`, and `latex` status checks.
6. Require conversation resolution and prevent force pushes to `main`.
7. Enable Dependabot security updates and secret scanning where available.
8. Create signed or annotated releases from frozen confirmatory commits.
9. Archive a release with a DOI provider only after confirmatory outputs are regenerated.

## One-command publication

After installing and authenticating GitHub CLI, run from the repository root:

```bash
./scripts/publish_github.sh
```

The script creates the public repository when absent, pushes `main` and all
tags, sets the description and topics, enables Issues and Discussions, and
enables automatic deletion of merged branches. Branch-protection rules still
need to be selected in the GitHub repository settings because required check
names become available only after the first workflow run.
