"""Scoring logic — compares predictions against dataset ground truth."""

from pathlib import Path
from typing import Any

from .types import ScoreResult
from .utils import load_jsonl, pct, write_json
from .validate import validate_dataset, validate_predictions


def score(
    dataset_path: str | Path,
    predictions_path: str | Path,
    output_path: str | Path | None = None,
) -> ScoreResult:
    dataset_rows = validate_dataset(dataset_path)
    pred_rows = validate_predictions(predictions_path, dataset_rows)

    ground_truth: dict[str, dict[str, Any]] = {
        str(r["id"]): r for r in dataset_rows
    }
    predictions: dict[str, dict[str, Any]] = {
        str(r["id"]): r for r in pred_rows
    }

    model_name = pred_rows[0].get("model", Path(predictions_path).stem) if pred_rows else "unknown"
    dataset_name = Path(dataset_path).stem

    correct_direction = 0
    correct_event_type = 0
    correct_asset = 0
    correct_time_horizon = 0
    failed_examples: list[dict[str, Any]] = []
    evaluated = 0

    for rid, gt in ground_truth.items():
        pred = predictions.get(rid)
        if pred is None:
            continue
        evaluated += 1

        direction_ok = pred.get("predicted_direction", "") == gt.get("expected_direction", "")
        event_ok = (
            pred.get("predicted_event_type", "") == gt.get("event_type", "")
            if pred.get("predicted_event_type")
            else False
        )
        asset_ok = (
            pred.get("predicted_asset", "") == gt.get("asset", "")
            if pred.get("predicted_asset")
            else False
        )
        horizon_ok = (
            pred.get("predicted_time_horizon", "") == gt.get("time_horizon", "")
            if pred.get("predicted_time_horizon")
            else False
        )

        if direction_ok:
            correct_direction += 1
        if event_ok:
            correct_event_type += 1
        if asset_ok:
            correct_asset += 1
        if horizon_ok:
            correct_time_horizon += 1

        if not direction_ok:
            failed_examples.append({
                "id": rid,
                "headline": gt.get("headline", ""),
                "expected_direction": gt.get("expected_direction", ""),
                "predicted_direction": pred.get("predicted_direction", ""),
                "expected_event_type": gt.get("event_type", ""),
                "predicted_event_type": pred.get("predicted_event_type", ""),
                "asset": gt.get("asset", ""),
            })

    has_event = any(p.get("predicted_event_type") for p in pred_rows)
    has_asset = any(p.get("predicted_asset") for p in pred_rows)
    has_horizon = any(p.get("predicted_time_horizon") for p in pred_rows)

    direction_acc = pct(correct_direction, evaluated)
    event_acc = pct(correct_event_type, evaluated) if has_event else None
    asset_acc = pct(correct_asset, evaluated) if has_asset else None
    horizon_acc = pct(correct_time_horizon, evaluated) if has_horizon else None

    components = [direction_acc]
    if event_acc is not None:
        components.append(event_acc)
    if asset_acc is not None:
        components.append(asset_acc)
    if horizon_acc is not None:
        components.append(horizon_acc)

    overall = round(sum(components) / len(components), 4)

    result = ScoreResult(
        model=model_name,
        dataset=dataset_name,
        total=evaluated,
        overall=overall,
        direction_accuracy=direction_acc,
        event_type_accuracy=event_acc if event_acc is not None else 0.0,
        asset_match=asset_acc if asset_acc is not None else 0.0,
        time_horizon_match=horizon_acc if horizon_acc is not None else 0.0,
        correct_direction=correct_direction,
        correct_event_type=correct_event_type,
        correct_asset=correct_asset,
        correct_time_horizon=correct_time_horizon,
        failed_examples=failed_examples,
        notes=(
            "event_type/asset/time_horizon fields not present in all predictions"
            if not (has_event and has_asset and has_horizon)
            else ""
        ),
    )

    if output_path:
        write_json(output_path, result.to_dict())

    return result
