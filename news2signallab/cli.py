"""CLI entry point — argparse-based command dispatcher."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .utils import err, pkg_root


def _root() -> Path:
    return pkg_root()


def cmd_demo(args: argparse.Namespace) -> int:
    from .pipeline import run_demo
    run_demo(base_dir=_root())
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    from .validate import validate_dataset, validate_predictions, ValidationError

    try:
        rows = validate_dataset(args.dataset)
        print(f"  [ok] Dataset valid: {len(rows)} rows ({args.dataset})")
    except ValidationError as exc:
        err(str(exc))
        return 1

    if args.predictions:
        try:
            prows = validate_predictions(args.predictions, rows)
            print(f"  [ok] Predictions valid: {len(prows)} rows ({args.predictions})")
        except ValidationError as exc:
            err(str(exc))
            return 1

    return 0


def cmd_score(args: argparse.Namespace) -> int:
    from .score import score as run_score
    from .validate import ValidationError

    output = args.output or str(
        _root() / "outputs" / "scores" / (Path(args.predictions).stem + ".json")
    )
    try:
        result = run_score(args.dataset, args.predictions, output)
    except (ValidationError, ValueError) as exc:
        err(str(exc))
        return 1

    print(f"  [ok] Scored {result.total} examples")
    print(f"       overall={result.overall:.1%}  direction={result.direction_accuracy:.1%}")
    print(f"       event_type={result.event_type_accuracy:.1%}  asset={result.asset_match:.1%}  time_horizon={result.time_horizon_match:.1%}")
    print(f"       Output: {output}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    from .report import generate_report

    output = args.output or str(
        _root() / "outputs" / "reports" / (Path(args.score).stem + ".md")
    )
    try:
        generate_report(args.score, output)
    except Exception as exc:
        err(str(exc))
        return 1

    print(f"  [ok] Report written: {output}")
    return 0


def cmd_board(args: argparse.Namespace) -> int:
    from .board import build_board
    from .utils import load_jsonl

    stream_samples = []
    streams_path = _root() / "outputs" / "streams"
    if streams_path.exists():
        for sf in sorted(streams_path.glob("*.jsonl"))[:2]:
            try:
                stream_samples.extend(load_jsonl(sf)[:3])
            except Exception:
                pass

    dataset_path = _root() / "datasets" / "demo.jsonl"
    dataset_count = 0
    if dataset_path.exists():
        try:
            from .utils import load_jsonl as lj
            dataset_count = len(lj(dataset_path))
        except Exception:
            pass

    try:
        build_board(
            scores_dir=args.input,
            output_dir=args.output,
            dataset_count=dataset_count,
            stream_samples=stream_samples,
        )
    except Exception as exc:
        err(str(exc))
        return 1

    print(f"  [ok] Site built at {args.output}/")
    return 0


def cmd_stream(args: argparse.Namespace) -> int:
    from .stream import generate_stream, list_scenarios

    if args.list:
        print("Available scenarios:")
        for s in list_scenarios():
            print(f"  {s}")
        return 0

    output = args.output or str(
        _root() / "outputs" / "streams" / f"{args.scenario}-stream.jsonl"
    )
    try:
        events = generate_stream(args.scenario, count=args.count, output_path=output, seed=args.seed)
    except ValueError as exc:
        err(str(exc))
        return 1

    print(f"  [ok] Generated {len(events)} events for scenario '{args.scenario}'")
    print(f"       Output: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="news2signallab",
        description="News2SignalLab — complete local lab for financial news-to-signal evaluation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  news2signallab demo\n"
            "  news2signallab validate --dataset datasets/demo.jsonl\n"
            "  news2signallab score --dataset datasets/demo.jsonl --predictions examples/predictions/simple-baseline.jsonl\n"
            "  news2signallab report --score outputs/scores/simple-baseline.json\n"
            "  news2signallab board --input outputs/scores --output site\n"
            "  news2signallab stream --scenario fed --count 20\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # demo
    p_demo = sub.add_parser("demo", help="Run the full end-to-end demo pipeline")
    p_demo.set_defaults(func=cmd_demo)

    # validate
    p_val = sub.add_parser("validate", help="Validate dataset and/or prediction files")
    p_val.add_argument("--dataset", required=True, metavar="PATH", help="Path to dataset JSONL")
    p_val.add_argument("--predictions", metavar="PATH", help="Path to predictions JSONL (optional)")
    p_val.set_defaults(func=cmd_validate)

    # score
    p_score = sub.add_parser("score", help="Score predictions against dataset")
    p_score.add_argument("--dataset", required=True, metavar="PATH")
    p_score.add_argument("--predictions", required=True, metavar="PATH")
    p_score.add_argument("--output", metavar="PATH", help="Output score JSON path (optional)")
    p_score.set_defaults(func=cmd_score)

    # report
    p_report = sub.add_parser("report", help="Generate Markdown report from score JSON")
    p_report.add_argument("--score", required=True, metavar="PATH", help="Path to score JSON file")
    p_report.add_argument("--output", metavar="PATH", help="Output Markdown path (optional)")
    p_report.set_defaults(func=cmd_report)

    # board
    p_board = sub.add_parser("board", help="Build static HTML leaderboard site")
    p_board.add_argument("--input", required=True, metavar="DIR", help="Directory containing score JSON files")
    p_board.add_argument("--output", required=True, metavar="DIR", help="Output site directory")
    p_board.set_defaults(func=cmd_board)

    # stream
    p_stream = sub.add_parser("stream", help="Generate synthetic market-news event stream")
    p_stream.add_argument("--scenario", default="fed", metavar="NAME",
                          help="Scenario name (fed, cpi, earnings, crypto-policy, regulation)")
    p_stream.add_argument("--count", type=int, default=20, metavar="N", help="Number of events to generate")
    p_stream.add_argument("--output", metavar="PATH", help="Output JSONL path (optional)")
    p_stream.add_argument("--seed", type=int, default=None, metavar="INT", help="Random seed for reproducibility")
    p_stream.add_argument("--list", action="store_true", help="List available scenarios")
    p_stream.set_defaults(func=cmd_stream)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))
