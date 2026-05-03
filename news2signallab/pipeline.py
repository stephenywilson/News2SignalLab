"""Full demo pipeline — runs all steps end-to-end."""

from pathlib import Path
from typing import Any

from .board import build_board
from .report import generate_report
from .score import score
from .stream import generate_stream, list_scenarios
from .utils import load_jsonl, ok, info, pkg_root, write_jsonl
from .validate import validate_dataset, validate_predictions


def run_demo(base_dir: str | Path | None = None) -> None:
    root = pkg_root() if base_dir is None else Path(base_dir)

    dataset_path = root / "datasets" / "demo.jsonl"
    pred_dir = root / "examples" / "predictions"
    out_scores = root / "outputs" / "scores"
    out_reports = root / "outputs" / "reports"
    out_streams = root / "outputs" / "streams"
    site_dir = root / "site"

    out_scores.mkdir(parents=True, exist_ok=True)
    out_reports.mkdir(parents=True, exist_ok=True)
    out_streams.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)

    print("\nNews2SignalLab v0.1.0 — Demo Pipeline\n" + "=" * 42)

    print("\n[1/5] Validating dataset...")
    dataset_rows = validate_dataset(dataset_path)
    ok(f"Dataset valid: {len(dataset_rows)} rows in {dataset_path.name}")

    pred_files = sorted(pred_dir.glob("*.jsonl"))
    if not pred_files:
        info("No prediction files found in examples/predictions/")
        pred_files = []

    print("\n[2/5] Validating predictions...")
    for pf in pred_files:
        validate_predictions(pf, dataset_rows)
        ok(f"Predictions valid: {pf.name}")

    print("\n[3/5] Scoring prediction files...")
    score_paths: list[Path] = []
    for pf in pred_files:
        model_name = pf.stem
        out_path = out_scores / f"{model_name}.json"
        result = score(dataset_path, pf, out_path)
        score_paths.append(out_path)
        ok(f"{model_name}: overall={result.overall:.1%} direction={result.direction_accuracy:.1%}")

    print("\n[4/5] Generating Markdown reports...")
    for sp in score_paths:
        model_name = sp.stem
        out_path = out_reports / f"{model_name}.md"
        generate_report(sp, out_path)
        ok(f"Report: {out_path.name}")

    print("\n[4b/5] Generating synthetic streams...")
    all_stream_samples: list[dict[str, Any]] = []
    for scenario in list_scenarios():
        stream_path = out_streams / f"{scenario}-stream.jsonl"
        events = generate_stream(scenario, count=20, output_path=stream_path, seed=42)
        all_stream_samples.extend(events[:3])
        ok(f"Stream: {stream_path.name} ({len(events)} events)")

    print("\n[5/5] Building static HTML site...")
    build_board(
        scores_dir=out_scores,
        output_dir=site_dir,
        dataset_count=len(dataset_rows),
        stream_samples=all_stream_samples,
    )
    ok(f"site/index.html")
    ok(f"site/leaderboard.html")
    ok(f"site/streams.html")
    for sp in score_paths:
        ok(f"site/reports/{sp.stem}.html")

    print("\n" + "=" * 42)
    print("Demo complete.\n")
    print(f"  Scores:   {out_scores}/")
    print(f"  Reports:  {out_reports}/")
    print(f"  Streams:  {out_streams}/")
    print(f"  Site:     {site_dir}/index.html")
    print()
