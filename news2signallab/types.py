"""Shared constants and type definitions."""

from dataclasses import dataclass, field
from typing import Any, Optional

VALID_EVENT_TYPES = frozenset({
    "central_bank", "inflation", "earnings", "regulation",
    "geopolitical", "supply_chain", "crypto_policy",
    "company_guidance", "macro_growth",
})

VALID_DIRECTIONS = frozenset({"bullish", "bearish", "neutral", "mixed"})

VALID_TIME_HORIZONS = frozenset({"intraday", "short_term", "medium_term", "long_term"})

VALID_ASSET_TYPES = frozenset({
    "equity", "equity_etf", "crypto", "commodity_etf", "bond", "forex",
})

DATASET_REQUIRED_FIELDS = [
    "id", "headline", "event_type", "asset",
    "expected_direction", "time_horizon",
]

PREDICTION_REQUIRED_FIELDS = [
    "id", "model", "predicted_direction",
]


@dataclass
class DatasetRow:
    id: str
    headline: str
    event_type: str
    asset: str
    expected_direction: str
    time_horizon: str
    source_type: str = "synthetic"
    asset_type: str = ""
    confidence: float = 0.0
    summary: str = ""
    published_at: str = ""


@dataclass
class Prediction:
    id: str
    model: str
    predicted_direction: str
    predicted_event_type: str = ""
    predicted_asset: str = ""
    predicted_time_horizon: str = ""
    predicted_confidence: float = 0.0
    reasoning: str = ""


@dataclass
class ScoreResult:
    model: str
    dataset: str
    total: int
    overall: float
    direction_accuracy: float
    event_type_accuracy: float
    asset_match: float
    time_horizon_match: float
    correct_direction: int
    correct_event_type: int
    correct_asset: int
    correct_time_horizon: int
    failed_examples: list[dict[str, Any]] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "dataset": self.dataset,
            "total": self.total,
            "overall": round(self.overall, 4),
            "direction_accuracy": round(self.direction_accuracy, 4),
            "event_type_accuracy": round(self.event_type_accuracy, 4),
            "asset_match": round(self.asset_match, 4),
            "time_horizon_match": round(self.time_horizon_match, 4),
            "correct_direction": self.correct_direction,
            "correct_event_type": self.correct_event_type,
            "correct_asset": self.correct_asset,
            "correct_time_horizon": self.correct_time_horizon,
            "failed_examples": self.failed_examples,
            "notes": self.notes,
        }
