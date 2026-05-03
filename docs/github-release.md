# GitHub Release Guide

Reference for publishing the first public GitHub release of News2SignalLab.

---

## Repository

```
https://github.com/stephenywilson/News2SignalLab
```

---

## Suggested GitHub Description

```
Complete local lab for financial news-to-signal evaluation, reports, static leaderboards, and synthetic market-news streams.
```

---

## Suggested Topics

```
financial-news
market-intelligence
ai-evaluation
llm-evaluation
benchmark
leaderboard
static-site
synthetic-data
python
cli
catalayer
```

---

## Initial Release Title

```
News2SignalLab v0.1.0 — Complete Local News-to-Signal Evaluation Lab
```

---

## Initial Release Notes

```markdown
## News2SignalLab v0.1.0

Complete local lab for financial news-to-signal evaluation, reports, static leaderboards, and synthetic market-news streams.

### What's Included

- **6 CLI commands**: `demo`, `validate`, `score`, `report`, `board`, `stream`
- **32-row synthetic demo dataset** — 9 event types, 10 assets, 4 directions, 4 time horizons
- **3 synthetic demo prediction baselines**: oracle (~97.7%), noisy (~78.1%), simple (~62.5%)
- **Markdown reports** with per-metric breakdowns and failed example analysis
- **Static dark-theme HTML leaderboard site** — no server required
- **Synthetic event stream generation** — 5 scenarios (fed, cpi, earnings, crypto-policy, regulation)
- **Zero external dependencies** — Python 3.10+ standard library only
- **No API keys required** — fully offline
- **GitHub Actions CI** — smoke test on Python 3.10 and 3.11

### Quick Start

```bash
pip install -e .
news2signallab demo
```

Open `site/index.html` in any browser — no server needed.

### Ecosystem

| Project | Role |
|---------|------|
| News2SignalBench | Benchmark foundation |
| SignalEvalRunner | Standalone runner |
| News2SignalLab | Complete integrated lab (this project) |

### Important Disclaimer

> Research only. All data is synthetic and for evaluation research purposes only.
> Not financial advice. No real news. No trading execution.
> oracle-baseline, noisy-local-model, and simple-baseline are synthetic demo baselines —
> not official real model benchmark results.
> Results from this lab cannot and should not be cited as real model performance benchmarks.
```

---

## Pre-Release Checklist

- [ ] `python -m news2signallab demo` runs cleanly
- [ ] `bash scripts/smoke_test.sh` — all 37 checks pass
- [ ] Privacy scan clean: no absolute paths, no API keys, no private data
- [ ] README renders correctly on GitHub (SVG image displays)
- [ ] `site/index.html` opens in browser without errors
- [ ] LICENSE file is present (Apache-2.0)
- [ ] CHANGELOG.md is up to date
- [ ] pyproject.toml version matches tag (`0.1.0`)
- [ ] CONTRIBUTING.md is present
- [ ] SECURITY.md is present
- [ ] `.github/workflows/smoke.yml` is present
- [ ] No `catalayer-ai` repository references remaining
- [ ] No generated artifacts in `outputs/` or `site/` except `.gitkeep`

---

## Git Commands (First Commit and Push)

```bash
cd News2SignalLab   # or wherever you cloned the repo

# Initialize and set default branch
git init
git branch -M main

# Stage all source files (generated artifacts are gitignored)
git add .

# Review what's staged
git status

# First commit
git commit -m "Initial release: News2SignalLab v0.1.0

Complete local lab for financial news-to-signal evaluation.
- 6 CLI commands: demo, validate, score, report, board, stream
- 32-row synthetic demo dataset
- 3 synthetic demo prediction baselines
- Markdown reports + static dark-theme HTML leaderboard
- Synthetic event stream generation (5 scenarios)
- Zero external dependencies, zero API keys
- GitHub Actions CI smoke test on Python 3.10 and 3.11"
```

After creating the GitHub repository at https://github.com/stephenywilson/News2SignalLab:

```bash
git remote add origin https://github.com/stephenywilson/News2SignalLab.git
git push -u origin main

# Create and push the release tag
git tag -a v0.1.0 -m "News2SignalLab v0.1.0 — Complete Local News-to-Signal Evaluation Lab"
git push origin v0.1.0
```

---

## .gitignore Notes

`outputs/*` and `site/*` are ignored so generated artifacts are not committed.
`outputs/.gitkeep` and `site/.gitkeep` preserve directory structure.

Users generate outputs locally by running `news2signallab demo`.
