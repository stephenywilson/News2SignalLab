# Prediction Format

Prediction files are JSONL files — one JSON object per line.

Each prediction row must have an `id` matching an example in the dataset being evaluated.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Must match a dataset row `id` |
| `model` | string | Model or system name |
| `predicted_direction` | string | Predicted direction label |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `predicted_event_type` | string | Predicted event category |
| `predicted_asset` | string | Predicted target asset |
| `predicted_time_horizon` | string | Predicted time horizon |
| `predicted_confidence` | float | Prediction confidence 0.0–1.0 |
| `reasoning` | string | Free-text reasoning or chain-of-thought |

## Scoring Behavior

- `predicted_direction` is always scored (required).
- `predicted_event_type`, `predicted_asset`, `predicted_time_horizon` are scored **only if present** in at least one prediction row.
- If none of a file's rows include `predicted_event_type`, event type accuracy is excluded from the overall score.
- `overall` score is the mean of all included metrics.
- `reasoning` is stored but not evaluated in v0.1.

## Allowed Values

`predicted_direction` must be one of: `bullish`, `bearish`, `neutral`, `mixed`

`predicted_event_type` must be one of the nine allowed event type values (see dataset-format.md).

`predicted_time_horizon` must be one of: `intraday`, `short_term`, `medium_term`, `long_term`

## Example Row

```json
{
  "id": "n007",
  "model": "simple-baseline",
  "predicted_direction": "bullish",
  "predicted_event_type": "earnings",
  "predicted_asset": "AAPL",
  "predicted_time_horizon": "intraday",
  "predicted_confidence": 0.70,
  "reasoning": "Keyword 'beats' reliably matched to bullish AAPL earnings."
}
```

## Example Prediction Files

| File | Description | Target Overall |
|------|-------------|----------------|
| `oracle-baseline.jsonl` | Near-perfect upper bound | ~97% |
| `simple-baseline.jsonl` | Keyword-heuristic style | ~62% |
| `noisy-local-model.jsonl` | Moderate quality demo | ~77% |

These are synthetic demo files. They do not represent real model performance.
