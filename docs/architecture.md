# Architecture

News2SignalLab is a CLI-first, static-output evaluation lab. All computation runs locally; no external services, no API keys, no runtime servers.

## Pipeline

```
datasets/demo.jsonl
        │
        ▼
   [validate]   ← news2signallab validate
        │
        ▼
examples/predictions/*.jsonl
        │
        ▼
   [score]      ← news2signallab score
        │
        ▼
outputs/scores/*.json
        │
        ├──► [report]   ← news2signallab report  →  outputs/reports/*.md
        │
        └──► [board]    ← news2signallab board   →  site/
                                                      ├── index.html
                                                      ├── leaderboard.html
                                                      ├── reports/*.html
                                                      ├── streams.html
                                                      ├── data/leaderboard.json
                                                      └── assets/style.css

scenarios/*.json
        │
        ▼
   [stream]     ← news2signallab stream  →  outputs/streams/*.jsonl
```

## Module Responsibilities

| Module | Role |
|--------|------|
| `cli.py` | argparse entry point, dispatches to subcommands |
| `types.py` | Constants (valid labels), dataclasses for ScoreResult |
| `validate.py` | JSONL parsing, field presence, allowed values, id uniqueness |
| `score.py` | Pairwise comparison of predictions vs ground truth, metric computation |
| `report.py` | Markdown report generation from score JSON |
| `render.py` | Static HTML page templates (dark theme, inline CSS) |
| `board.py` | Reads all score JSON files, calls render.py for each page |
| `stream.py` | Synthetic event generation from named scenario configs |
| `pipeline.py` | Orchestrates the full `demo` command end-to-end |
| `utils.py` | JSONL/JSON I/O, path helpers, print helpers |

## Output Directories

```
outputs/
  scores/          JSON score files, one per prediction file
  reports/         Markdown report files
  streams/         Synthetic stream JSONL files

site/
  index.html       Summary dashboard
  leaderboard.html Ranked leaderboard table
  reports/         Per-model HTML report pages
  streams.html     Synthetic stream viewer
  data/            leaderboard.json (machine-readable)
  assets/          style.css
```

## Design Decisions

**No external dependencies.** The project uses only Python's standard library. This keeps it installable everywhere and removes supply-chain risk for a public demo tool.

**Static HTML over web framework.** The output is a folder of HTML files openable in any browser without running a server. This is intentional — the lab is for local offline use.

**Score JSON as interchange.** Score files are plain JSON. The report and board commands read score files independently, so each step can be run separately or piped into other tools.

**Inline CSS in HTML.** Each generated HTML page embeds its own CSS, so the site works even if `assets/style.css` is missing. The CSS file in `assets/` exists for external linking if needed.

**Synthetic streams as JSONL.** Streams are plain JSONL for maximum portability. No real-time server, no WebSocket. v0.1 is a static generator only.
