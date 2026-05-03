# Security Policy

## Overview

News2SignalLab is a **local-first, offline evaluation research tool**. It does not run a server, does not connect to external services in v0.1.0, and does not require API keys or credentials of any kind.

---

## v0.1.0 Security Properties

| Property | Status |
|----------|--------|
| API keys required | None |
| External model provider calls | None |
| Network connections | None |
| Server or daemon process | None |
| Real financial data | None — synthetic demo data only |
| User authentication | None |
| Database | None |
| Generated outputs sent externally | Never |

---

## What This Project Is Not

- Not a trading system
- Not a financial advice system
- Not a backend service
- Not connected to any broker, exchange, or data provider

All dataset rows are clearly labeled `"source_type": "synthetic"`. All generated outputs are local files.

---

## What You Should Not Do

- Do not commit API keys, access tokens, or credentials to this repository.
- Do not add real private financial datasets or proprietary news content.
- Do not expose the `outputs/` or `site/` generated directories publicly if they contain local experiment information you consider sensitive.
- Do not modify this project to connect to external services without clearly documenting the change.

The `.gitignore` excludes `outputs/*` and `site/*` to help prevent accidental commits of local run artifacts.

---

## Reporting a Security Concern

If you discover a security issue with News2SignalLab — for example, if a dependency introduces a vulnerability, if a generated output unexpectedly leaks local information, or if the code does something unintended — please report it through:

**GitHub Issues:** https://github.com/stephenywilson/News2SignalLab/issues

For sensitive concerns, you may label the issue **[Security]** or contact the maintainer directly via the GitHub profile:
**https://github.com/stephenywilson**

---

## Supported Versions

| Version | Status |
|---------|--------|
| 0.1.0 | Active — current release |

---

## Disclaimer

News2SignalLab is a research tool. It does not handle real financial transactions, real user credentials, or real market data. Security expectations should be calibrated accordingly.

© 2024-2026 Catalayer AI
