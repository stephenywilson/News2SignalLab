# Contributing to News2SignalLab

Thank you for your interest in News2SignalLab. Contributions are welcome, especially around dataset formats, scoring improvements, documentation, and synthetic stream scenarios.

## Important Reminders

- **Synthetic data only.** Do not submit real financial news, proprietary datasets, or private market data.
- **No secrets.** Do not commit API keys, credentials, or private tokens.
- **Research only.** News2SignalLab is an evaluation research tool, not a trading system.
- **No paid data sources.** All datasets and examples must be freely shareable.

---

## Local Setup

```bash
# Clone the repository
git clone https://github.com/stephenywilson/News2SignalLab.git
cd News2SignalLab

# Install in editable mode (no external dependencies required)
python -m pip install -e .

# Verify installation
python -m news2signallab --help

# Run the full demo pipeline
python -m news2signallab demo

# Run the smoke test
bash scripts/smoke_test.sh
```

Requires **Python 3.10+**. No API keys, no external services.

---

## What Contributions Are Welcome

| Type | Examples |
|------|---------|
| Bug fixes | Scoring edge cases, CLI argument parsing, HTML rendering issues |
| Documentation | Clearer explanations, more examples, typo fixes |
| Synthetic dataset rows | Additional diverse synthetic examples (must follow the demo.jsonl schema) |
| New stream scenarios | New scenario JSON files (synthetic events only) |
| Scoring improvements | New metrics, better report formatting |
| CI/tooling | Improved test coverage, additional smoke checks |

**Not currently accepted:**
- Real news data or real financial datasets
- External API integrations that require paid keys
- Trading execution logic of any kind
- Claims of real model benchmark results

---

## Code Style

- Python 3.10+ standard library only — no new external dependencies without discussion
- Follow the existing module structure (see [docs/architecture.md](docs/architecture.md))
- Keep functions small and testable
- No inline comments unless the reason is non-obvious

---

## Dataset and Prediction Format

Before adding examples, read:
- [docs/dataset-format.md](docs/dataset-format.md)
- [docs/prediction-format.md](docs/prediction-format.md)

All dataset rows must include `"source_type": "synthetic"` and must not contain real headlines or real market events.

---

## Reporting Issues

Open an issue at:
**https://github.com/stephenywilson/News2SignalLab/issues**

When reporting a bug, include:
- Python version (`python --version`)
- Operating system
- The command you ran
- The full error output

---

## Pull Requests

1. Fork the repository
2. Create a branch: `git checkout -b fix/your-description`
3. Make your changes
4. Run `bash scripts/smoke_test.sh` — all checks must pass
5. Open a pull request with a clear description

---

## License

By contributing, you agree that your contributions will be licensed under the [Apache-2.0 License](LICENSE).

© 2024-2026 Catalayer AI
