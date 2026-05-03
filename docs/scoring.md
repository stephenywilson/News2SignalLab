# Scoring

The `score` command computes deterministic, transparent metrics by comparing predictions against dataset ground truth.

## Metrics

### Direction Accuracy

```
direction_accuracy = correct_direction / total_evaluated
```

The fraction of examples where `predicted_direction` exactly matches `expected_direction`.

Direction is the primary signal metric. It measures whether the model correctly identifies the expected market impact direction (bullish, bearish, neutral, mixed).

### Event Type Accuracy

```
event_type_accuracy = correct_event_type / total_evaluated
```

Only computed when `predicted_event_type` is present in the prediction file. Measures whether the model correctly categorizes the event type (earnings, inflation, central_bank, etc.).

### Asset Match

```
asset_match = correct_asset / total_evaluated
```

Only computed when `predicted_asset` is present. Measures whether the predicted asset ticker matches the dataset asset.

### Time Horizon Match

```
time_horizon_match = correct_time_horizon / total_evaluated
```

Only computed when `predicted_time_horizon` is present. Measures whether the predicted time horizon matches the ground truth horizon.

### Overall Score

```
overall = mean(all included metrics)
```

The arithmetic mean of all metrics that were computed. If only direction is present, overall equals direction accuracy. If all four metrics are present, overall is the mean of all four.

## Score JSON Format

```json
{
  "model": "simple-baseline",
  "dataset": "demo",
  "total": 32,
  "overall": 0.6250,
  "direction_accuracy": 0.5938,
  "event_type_accuracy": 0.6250,
  "asset_match": 0.7813,
  "time_horizon_match": 0.5000,
  "correct_direction": 19,
  "correct_event_type": 20,
  "correct_asset": 25,
  "correct_time_horizon": 16,
  "failed_examples": [...],
  "notes": ""
}
```

## Failed Examples

The `failed_examples` list contains all examples where direction was incorrectly predicted. Each entry includes:

- `id` — example ID
- `headline` — original headline
- `expected_direction` — ground truth direction
- `predicted_direction` — model prediction
- `expected_event_type` — ground truth event type
- `predicted_event_type` — model prediction
- `asset` — target asset

## Limitations

- Reasoning quality is not evaluated in v0.1.
- Confidence calibration is not evaluated in v0.1.
- Scoring is exact-match only — no partial credit for "close" predictions.
- All metrics are weighted equally in the overall score.
- Results on the 32-row demo dataset are not statistically meaningful for real model comparisons.
- Not financial advice. Synthetic demo data only.
