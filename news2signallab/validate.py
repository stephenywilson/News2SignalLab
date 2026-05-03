"""Dataset and prediction validation."""

from pathlib import Path
from typing import Any

from .types import (
    DATASET_REQUIRED_FIELDS,
    PREDICTION_REQUIRED_FIELDS,
    VALID_DIRECTIONS,
    VALID_EVENT_TYPES,
    VALID_TIME_HORIZONS,
)
from .utils import load_jsonl


class ValidationError(Exception):
    pass


def validate_dataset(path: str | Path) -> list[dict[str, Any]]:
    rows = load_jsonl(path)
    if not rows:
        raise ValidationError(f"Dataset is empty: {path}")

    errors: list[str] = []
    seen_ids: set[str] = set()

    for i, row in enumerate(rows, 1):
        rid = row.get("id", f"<row {i}>")

        for field in DATASET_REQUIRED_FIELDS:
            if field not in row or row[field] in (None, ""):
                errors.append(f"Row {i} (id={rid}): missing required field '{field}'")

        if str(rid) in seen_ids:
            errors.append(f"Row {i}: duplicate id '{rid}'")
        seen_ids.add(str(rid))

        direction = row.get("expected_direction", "")
        if direction and direction not in VALID_DIRECTIONS:
            errors.append(
                f"Row {i} (id={rid}): invalid expected_direction '{direction}' "
                f"— allowed: {sorted(VALID_DIRECTIONS)}"
            )

        event_type = row.get("event_type", "")
        if event_type and event_type not in VALID_EVENT_TYPES:
            errors.append(
                f"Row {i} (id={rid}): invalid event_type '{event_type}' "
                f"— allowed: {sorted(VALID_EVENT_TYPES)}"
            )

        horizon = row.get("time_horizon", "")
        if horizon and horizon not in VALID_TIME_HORIZONS:
            errors.append(
                f"Row {i} (id={rid}): invalid time_horizon '{horizon}' "
                f"— allowed: {sorted(VALID_TIME_HORIZONS)}"
            )

    if errors:
        raise ValidationError(
            f"Dataset validation failed with {len(errors)} error(s):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    return rows


def validate_predictions(
    pred_path: str | Path,
    dataset_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    rows = load_jsonl(pred_path)
    if not rows:
        raise ValidationError(f"Prediction file is empty: {pred_path}")

    errors: list[str] = []
    seen_ids: set[str] = set()

    for i, row in enumerate(rows, 1):
        rid = row.get("id", f"<row {i}>")

        for field in PREDICTION_REQUIRED_FIELDS:
            if field not in row or row[field] in (None, ""):
                errors.append(f"Row {i} (id={rid}): missing required field '{field}'")

        if str(rid) in seen_ids:
            errors.append(f"Row {i}: duplicate prediction id '{rid}'")
        seen_ids.add(str(rid))

        direction = row.get("predicted_direction", "")
        if direction and direction not in VALID_DIRECTIONS:
            errors.append(
                f"Row {i} (id={rid}): invalid predicted_direction '{direction}'"
            )

    if dataset_rows is not None:
        dataset_ids = {str(r["id"]) for r in dataset_rows}
        for i, row in enumerate(rows, 1):
            pid = str(row.get("id", ""))
            if pid and pid not in dataset_ids:
                errors.append(
                    f"Prediction row {i} (id={pid}): id not found in dataset"
                )

    if errors:
        raise ValidationError(
            f"Prediction validation failed with {len(errors)} error(s):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    return rows
