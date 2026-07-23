#!/usr/bin/env bash
set -euo pipefail

REPO="AKToure/asr-deep-hedging"
DESCRIPTION="Auditable NumPy implementation and partial replication of deep hedging under transaction costs and stochastic volatility."
TOPICS="deep-hedging,option-hedging,cvar,heston-model,numpy,reproducible-research,quantitative-finance,transaction-costs"

command -v gh >/dev/null 2>&1 || {
  echo "GitHub CLI is required: https://cli.github.com/" >&2
  exit 1
}

gh auth status

if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "Repository $REPO already exists."
else
  gh repo create "$REPO" \
    --public \
    --description "$DESCRIPTION" \
    --source . \
    --remote origin
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "https://github.com/${REPO}.git"
else
  git remote add origin "https://github.com/${REPO}.git"
fi

git push -u origin main --follow-tags

gh repo edit "$REPO" \
  --description "$DESCRIPTION" \
  --enable-issues \
  --enable-discussions \
  --delete-branch-on-merge \
  --add-topic "$TOPICS"

cat <<'MSG'
Repository published.

Complete the protected-branch settings in:
  Settings -> Branches -> Add branch protection rule

Require the Tests, Reproducibility smoke run, and Build manuscript checks before merging.
MSG
