"""Static HTML leaderboard builder — reads score JSON files, emits site/."""

import glob
from pathlib import Path
from typing import Any

from .render import CSS, render_leaderboard, render_model_report, render_index, render_streams_page
from .utils import load_jsonl, read_json, write_json, write_text, pkg_root


def build_board(
    scores_dir: str | Path,
    output_dir: str | Path,
    dataset_count: int = 0,
    stream_samples: list[dict[str, Any]] | None = None,
) -> None:
    scores_dir = Path(scores_dir)
    output_dir = Path(output_dir)

    score_files = sorted(scores_dir.glob("*.json"))
    entries: list[dict[str, Any]] = []
    for sf in score_files:
        try:
            data = read_json(sf)
            entries.append(data)
        except Exception:
            continue

    entries.sort(key=lambda e: e.get("overall", 0.0), reverse=True)

    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "data").mkdir(parents=True, exist_ok=True)
    (output_dir / "assets").mkdir(parents=True, exist_ok=True)

    write_json(output_dir / "data" / "leaderboard.json", entries)

    write_text(output_dir / "assets" / "style.css", CSS)

    leaderboard_path = output_dir / "leaderboard.html"
    render_leaderboard(entries, leaderboard_path)

    for entry in entries:
        model = entry.get("model", "unknown")
        model_path = output_dir / "reports" / f"{model}.html"
        render_model_report(entry, model_path)

    best_score = entries[0].get("overall", 0.0) if entries else 0.0
    pred_count = len(entries)
    report_count = len(entries)

    index_path = output_dir / "index.html"
    render_index(
        dataset_count=dataset_count,
        pred_count=pred_count,
        best_score=best_score,
        report_count=report_count,
        output_path=index_path,
    )

    streams_path = output_dir / "streams.html"
    render_streams_page(
        stream_samples=stream_samples or [],
        output_path=streams_path,
    )
