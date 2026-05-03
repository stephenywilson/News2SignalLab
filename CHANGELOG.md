# Changelog

All notable changes to News2SignalLab are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] — 2026-05-03

### Added
- Full CLI with six commands: `demo`, `validate`, `score`, `report`, `board`, `stream`
- `demo` command runs the complete end-to-end pipeline in one shot
- `validate` command checks dataset and prediction JSONL for schema compliance
- `score` command computes direction, event-type, asset, time-horizon accuracy
- `report` command generates Markdown score reports with failed-example details
- `board` command generates static HTML leaderboard site
- `stream` command generates synthetic market-news event streams as JSONL
- `datasets/demo.jsonl` — 32-row benchmark-style demo dataset
- Three example prediction files: oracle-baseline, simple-baseline, noisy-local-model
- Three example synthetic streams: fed-scenario, cpi-scenario, earnings-scenario
- Five scenario definitions: fed, cpi, earnings, crypto-policy, regulation
- Static dark-theme HTML site: index, leaderboard, per-model reports, streams page
- Seven documentation pages under `docs/`
- `scripts/smoke_test.sh` for CI-style local verification
- Apache-2.0 license
- Zero external dependencies, zero API keys required

---

## Roadmap

### [0.2.0] — Planned
- Multi-dataset support (load arbitrary JSONL via `--dataset`)
- Weighted scoring with configurable metric weights
- Batch score command for entire prediction directories
- CSV export for leaderboard data
- Confidence calibration metrics

### [0.3.0] — Planned
- Reasoning quality scoring via deterministic heuristics (no judge model)
- Event-category drill-down in reports
- Per-asset-class breakdown tables
- JSON Schema validation with `jsonschema` (optional dependency)

### [0.4.0] — Planned
- Scenario YAML editor for custom synthetic streams
- Stream replay CLI with timing simulation
- Extended dataset with 200+ rows

### [1.0.0] — Future
- Stable public API
- Plugin interface for custom scorers
- Docker-based reproducible environment
