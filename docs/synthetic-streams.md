# Synthetic Streams

The `stream` command generates synthetic market-news event sequences as JSONL files.

## What Are Synthetic Streams?

Synthetic streams simulate the sequence of market-moving news events that might occur around a specific theme (a Fed meeting cycle, earnings season, an inflation data release, etc.).

Each event has:
- A realistic-sounding headline (generated from templates)
- Event type, asset, expected direction, and time horizon
- A signal block with direction, strength, and rationale
- A timestamp sequence

All events are clearly labeled `"source_type": "synthetic"`. They are not real news, not real market data, and should not be used for trading or investment decisions.

## Event Schema

```json
{
  "id": "stream-fed-0001",
  "timestamp": "2025-01-06T09:30:00Z",
  "headline": "Fed raises benchmark rate by 25 basis points, signals data-dependent path",
  "source_type": "synthetic",
  "source_name": "Synthetic Wire",
  "event_type": "central_bank",
  "asset": "SPY",
  "asset_type": "equity_etf",
  "expected_direction": "bearish",
  "time_horizon": "intraday",
  "confidence": 0.55,
  "summary": "[Synthetic] ... Signal for SPY: bearish over intraday horizon.",
  "signal": {
    "direction": "bearish",
    "strength": "weak",
    "rationale": "Rate hike signal tightens financial conditions, pressuring SPY valuations."
  }
}
```

## Available Scenarios

| Scenario | Event Type | Primary Assets |
|----------|-----------|----------------|
| `fed` | central_bank | SPY, US10Y, GLD, EURUSD |
| `cpi` | inflation | GLD, SPY, US10Y, ETH, EURUSD |
| `earnings` | earnings | AAPL, TSLA, NVDA, QQQ, SPY |
| `crypto-policy` | crypto_policy | BTC, ETH |
| `regulation` | regulation | NVDA, QQQ, BTC, SPY |

## CLI Usage

```bash
# Generate 20 Fed scenario events
news2signallab stream --scenario fed --count 20

# Generate with custom output path
news2signallab stream --scenario cpi --count 15 --output outputs/streams/cpi-stream.jsonl

# Reproducible output with fixed seed
news2signallab stream --scenario earnings --count 10 --seed 42

# List available scenarios
news2signallab stream --list
```

## v0.1 Limitations

- Streams are generated from templates, not language models.
- Events cycle through template banks — large `--count` values repeat patterns.
- No real-time streaming, WebSocket, or SSE in v0.1.
- All headlines are clearly synthetic and not representative of any real financial event.

## Future Directions

- Custom scenario YAML definitions
- Larger template banks with more variation
- Scenario chaining (multi-event narratives)
- Timing simulation (burst patterns, quiet periods)
