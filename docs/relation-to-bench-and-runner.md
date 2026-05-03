# Relationship to News2SignalBench and SignalEvalRunner

News2SignalLab is part of a three-project ecosystem for financial news-to-signal evaluation research.

## The Three Projects

### News2SignalBench — Benchmark Foundation

News2SignalBench defines the benchmark contract:

- Dataset schema (JSONL format, required fields, allowed label values)
- Evaluation task definition (given a news headline and context, predict direction, event type, asset, time horizon)
- Ground truth labeling conventions
- Benchmark versioning and dataset release format

News2SignalBench is the authoritative source for what "correct" means in this evaluation domain.

### SignalEvalRunner — Standalone Runner

SignalEvalRunner provides standalone evaluation runner primitives:

- Loading and validating datasets and predictions
- Computing per-metric scores
- Generating score summary outputs
- Designed to be embedded in other pipelines or CI workflows

SignalEvalRunner focuses on the evaluation computation layer without prescribing a full workflow.

### News2SignalLab — Integrated Reference Lab

News2SignalLab brings the full workflow together into one end-to-end local lab:

- Provides a complete working example of how to use the benchmark and runner concepts
- Adds static HTML output (leaderboard, per-model reports, stream viewer)
- Adds synthetic event stream generation
- Provides a one-command `demo` mode that runs everything end-to-end
- Designed as a reference implementation and starting point for research

## How They Relate

```
News2SignalBench          SignalEvalRunner
  (dataset format)          (scoring primitives)
        │                         │
        └──────────┬──────────────┘
                   │
                   ▼
           News2SignalLab
           (integrated lab)
           ├── demo pipeline
           ├── HTML leaderboard
           ├── Markdown reports
           └── synthetic streams
```

## What News2SignalLab Is Not

- It is not a replacement for News2SignalBench. The benchmark definitions live in News2SignalBench.
- It is not a replacement for SignalEvalRunner. The core evaluation primitives are inspired by SignalEvalRunner concepts.
- It is not a production evaluation service. It is a local-first reference lab.

## Which Project Should You Use?

| Goal | Recommended Project |
|------|---------------------|
| Define a benchmark dataset standard and evaluation contract | **News2SignalBench** |
| Embed a scoring runner into your own pipeline or CI | **SignalEvalRunner** |
| Run the complete local workflow end-to-end out of the box | **News2SignalLab** |
| Learn how the full benchmark-to-report pipeline fits together | **News2SignalLab** |

News2SignalLab is the right entry point for most users who want a working, runnable evaluation lab rather than individual building blocks.

## Using News2SignalLab Without the Other Projects

News2SignalLab is fully self-contained. You do not need News2SignalBench or SignalEvalRunner installed. The demo dataset, scoring logic, and report generation all work standalone from a single `pip install -e .`.

The conceptual relationship is one of inspired design and compatible schema — not a hard dependency chain. You can use all three projects together or each independently.
