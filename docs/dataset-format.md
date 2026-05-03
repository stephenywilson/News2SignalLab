# Dataset Format

Datasets are JSONL files — one JSON object per line.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the example |
| `headline` | string | News headline text |
| `event_type` | string | Event category (see allowed values) |
| `asset` | string | Target asset ticker |
| `expected_direction` | string | Ground truth direction label |
| `time_horizon` | string | Expected signal time horizon |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `source_type` | string | Data origin — always `"synthetic"` in v0.1 |
| `asset_type` | string | Asset class classification |
| `confidence` | float | Annotator confidence 0.0–1.0 |
| `summary` | string | Brief explanation of the event |
| `published_at` | string | ISO 8601 timestamp |

## Allowed Values

### `event_type`
```
central_bank
inflation
earnings
regulation
geopolitical
supply_chain
crypto_policy
company_guidance
macro_growth
```

### `expected_direction`
```
bullish
bearish
neutral
mixed
```

### `time_horizon`
```
intraday     (same trading session)
short_term   (1–5 trading days)
medium_term  (1–4 weeks)
long_term    (1–6 months)
```

## Example Row

```json
{
  "id": "n007",
  "headline": "Apple reports record quarterly revenue, beats EPS estimates by 8%, raises guidance",
  "source_type": "synthetic",
  "event_type": "earnings",
  "asset": "AAPL",
  "asset_type": "equity",
  "expected_direction": "bullish",
  "time_horizon": "intraday",
  "confidence": 0.90,
  "summary": "Apple beat both revenue and earnings estimates by wide margins and raised full-year guidance.",
  "published_at": "2024-10-31T21:00:00Z"
}
```

## Validation Rules

The `validate` command checks:

1. Valid JSONL — each line parses as JSON
2. All required fields are present and non-empty
3. `id` values are unique across the dataset
4. `expected_direction` is one of the four allowed values
5. `event_type` is one of the nine allowed values
6. `time_horizon` is one of the four allowed values

## Demo Dataset

`datasets/demo.jsonl` contains 32 rows covering:

- 9 event types
- 10 assets (SPY, QQQ, AAPL, TSLA, NVDA, BTC, ETH, GLD, US10Y, EURUSD)
- 4 directions
- 4 time horizons
- Confidence scores 0.55–0.92
