"""Synthetic market-news event stream generator."""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .utils import pkg_root, write_jsonl


_SCENARIOS: dict[str, dict[str, Any]] = {
    "fed": {
        "theme": "Federal Reserve policy",
        "events": [
            {
                "headline_templates": [
                    "Fed raises benchmark rate by 25 basis points, signals data-dependent path",
                    "Federal Reserve holds rates steady amid mixed inflation signals",
                    "Fed minutes reveal hawkish tilt among policymakers",
                    "Federal Reserve Chair signals willingness to cut rates if growth slows",
                    "Fed raises rates by 50bps in emergency response to inflation spike",
                    "Federal Reserve pauses hiking cycle, markets rally on pivot hopes",
                    "Fed Governor signals additional rate hikes may be warranted",
                    "Federal Reserve cuts rates for first time since 2020 amid recession fears",
                    "Fed dot plot projects higher rates for longer than markets expected",
                    "Federal Reserve holds rates, upgrades economic outlook",
                ],
                "event_type": "central_bank",
                "assets": ["SPY", "US10Y", "GLD", "EURUSD"],
                "directions": {
                    "SPY": ["bearish", "bullish", "neutral", "bearish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish"],
                    "US10Y": ["bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish"],
                    "GLD": ["bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "neutral"],
                    "EURUSD": ["bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bullish"],
                },
                "horizons": ["intraday", "short_term", "short_term", "medium_term", "intraday", "short_term", "short_term", "medium_term", "medium_term", "short_term"],
            }
        ],
    },
    "cpi": {
        "theme": "Consumer Price Index and inflation data",
        "events": [
            {
                "headline_templates": [
                    "US CPI rose 0.4% in {month}, above consensus estimate of 0.3%",
                    "Core inflation falls to 2.8% year-over-year, softening from prior month",
                    "CPI surprise: headline inflation jumps to 4.2% on energy price surge",
                    "Inflation data in line with expectations at 3.1%, markets steady",
                    "PPI rose sharply, suggesting future consumer price pressures ahead",
                    "Services inflation remains sticky despite cooling goods prices",
                    "CPI drops to 2.3%, nearing Fed's 2% target",
                    "Shelter costs push CPI above forecasts for third consecutive month",
                    "Eurozone inflation falls faster than expected, raising ECB cut bets",
                    "US inflation expectations rise in University of Michigan survey",
                ],
                "event_type": "inflation",
                "assets": ["GLD", "SPY", "US10Y", "ETH", "EURUSD"],
                "directions": {
                    "GLD": ["bullish", "bearish", "bullish", "neutral", "bullish", "bullish", "bearish", "bullish", "bearish", "bullish"],
                    "SPY": ["bearish", "bullish", "bearish", "neutral", "bearish", "bearish", "bullish", "bearish", "bullish", "bearish"],
                    "US10Y": ["bearish", "bullish", "bearish", "neutral", "bearish", "bearish", "bullish", "bearish", "bullish", "bearish"],
                    "ETH": ["bearish", "neutral", "bearish", "neutral", "bearish", "bearish", "bullish", "bearish", "neutral", "bearish"],
                    "EURUSD": ["neutral", "neutral", "bearish", "neutral", "neutral", "neutral", "bullish", "neutral", "bullish", "neutral"],
                },
                "horizons": ["intraday", "short_term", "intraday", "intraday", "short_term", "medium_term", "short_term", "intraday", "short_term", "medium_term"],
            }
        ],
    },
    "earnings": {
        "theme": "Corporate earnings results and guidance",
        "events": [
            {
                "headline_templates": [
                    "Apple reports quarterly revenue beat, raises full-year guidance",
                    "Tesla misses earnings estimates, cites production ramp challenges",
                    "NVIDIA posts record data center revenue, AI demand exceeds forecasts",
                    "Apple warns of revenue headwinds from China market softness",
                    "Tesla raises delivery forecast for Q3, shares surge pre-market",
                    "NVIDIA trims outlook citing export control uncertainty",
                    "Mixed tech earnings drag QQQ lower in extended trading",
                    "Strong consumer spending lifts S&P 500 earnings season outlook",
                    "Software sector earnings broadly beat as cloud demand accelerates",
                    "Energy company misses on earnings as oil prices retreat",
                ],
                "event_type": "earnings",
                "assets": ["AAPL", "TSLA", "NVDA", "QQQ", "SPY"],
                "directions": {
                    "AAPL": ["bullish", "neutral", "neutral", "bearish", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral"],
                    "TSLA": ["neutral", "bearish", "neutral", "neutral", "bullish", "neutral", "neutral", "neutral", "neutral", "neutral"],
                    "NVDA": ["neutral", "neutral", "bullish", "neutral", "neutral", "bearish", "neutral", "neutral", "bullish", "neutral"],
                    "QQQ": ["bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bearish", "bullish", "bullish", "bearish"],
                    "SPY": ["bullish", "bearish", "bullish", "bearish", "bullish", "bearish", "bearish", "bullish", "bullish", "bearish"],
                },
                "horizons": ["intraday", "intraday", "intraday", "short_term", "intraday", "short_term", "intraday", "short_term", "short_term", "intraday"],
            }
        ],
    },
    "crypto-policy": {
        "theme": "Cryptocurrency regulation and policy",
        "events": [
            {
                "headline_templates": [
                    "SEC approves spot Bitcoin ETF applications from major asset managers",
                    "Congressional bill proposes comprehensive crypto framework",
                    "G20 nations agree on stablecoin reporting standards",
                    "SEC files enforcement action against major crypto exchange",
                    "Federal court rules proof-of-work mining is not a security",
                    "Treasury proposes new crypto wallet reporting requirements",
                    "EU MiCA regulation takes full effect, clarity for European crypto firms",
                    "US Senate crypto bill stalls amid partisan disagreement",
                    "CFTC claims jurisdiction over Ethereum, triggers market uncertainty",
                    "Bipartisan support emerges for crypto market structure bill",
                ],
                "event_type": "crypto_policy",
                "assets": ["BTC", "ETH"],
                "directions": {
                    "BTC": ["bullish", "neutral", "neutral", "bearish", "bullish", "bearish", "bullish", "neutral", "bearish", "bullish"],
                    "ETH": ["bullish", "neutral", "neutral", "bearish", "neutral", "bearish", "bullish", "neutral", "bearish", "bullish"],
                },
                "horizons": ["short_term", "medium_term", "medium_term", "short_term", "short_term", "short_term", "medium_term", "short_term", "short_term", "medium_term"],
            }
        ],
    },
    "regulation": {
        "theme": "Sector-specific regulatory announcements",
        "events": [
            {
                "headline_templates": [
                    "Commerce Department expands AI chip export restrictions to additional countries",
                    "EU AI Act enforcement begins, compliance deadline passes",
                    "FTC opens antitrust investigation into large tech mergers",
                    "US adds new semiconductor companies to entity list",
                    "EU Digital Markets Act designation forces platform changes",
                    "Biotech sector faces new FDA accelerated approval scrutiny",
                    "Banking regulators propose higher capital requirements for large banks",
                    "CFPB finalizes open banking data-sharing rule",
                    "DOJ files antitrust suit targeting major software licensing practices",
                    "New ESG disclosure rules finalized by SEC for large companies",
                ],
                "event_type": "regulation",
                "assets": ["NVDA", "QQQ", "BTC", "SPY"],
                "directions": {
                    "NVDA": ["bearish", "neutral", "neutral", "bearish", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral"],
                    "QQQ": ["bearish", "bearish", "bearish", "bearish", "bearish", "neutral", "bearish", "neutral", "bearish", "neutral"],
                    "BTC": ["bearish", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral", "neutral"],
                    "SPY": ["bearish", "bearish", "bearish", "bearish", "bearish", "bearish", "bearish", "neutral", "bearish", "bearish"],
                },
                "horizons": ["medium_term", "medium_term", "medium_term", "short_term", "medium_term", "medium_term", "medium_term", "medium_term", "medium_term", "medium_term"],
            }
        ],
    },
}

_MONTHS = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]

_SOURCE_NAMES = [
    "Synthetic Wire", "DemoSignal Feed", "SyntheticMarket News",
    "Lab Event Stream", "Demo Financial Wire",
]

_STRENGTHS = ["weak", "moderate", "strong", "strong", "moderate"]


def _rationale(event_type: str, direction: str, asset: str) -> str:
    templates = {
        ("central_bank", "bearish"): f"Rate hike signal tightens financial conditions, pressuring {asset} valuations.",
        ("central_bank", "bullish"): f"Dovish pivot reduces discount rate expectations, lifting {asset} outlook.",
        ("central_bank", "neutral"): f"In-line Fed decision removes uncertainty without changing rate trajectory for {asset}.",
        ("inflation", "bearish"): f"Hot inflation data raises probability of tighter monetary policy, weighing on {asset}.",
        ("inflation", "bullish"): f"Inflation beat supports {asset} as inflation hedge amid rising price pressures.",
        ("inflation", "neutral"): f"Inflation data broadly in line, limited directional impact on {asset}.",
        ("earnings", "bullish"): f"Earnings beat with raised guidance signals strong demand tailwind for {asset}.",
        ("earnings", "bearish"): f"Earnings miss and guidance cut reduce near-term growth expectations for {asset}.",
        ("earnings", "mixed"): f"Mixed earnings report — beat on revenue but miss on margins — creates uncertainty for {asset}.",
        ("regulation", "bearish"): f"Regulatory action adds compliance costs and limits revenue opportunity for {asset}.",
        ("geopolitical", "bullish"): f"Risk-off geopolitical event increases safe-haven demand, supporting {asset}.",
        ("geopolitical", "bearish"): f"Geopolitical escalation raises risk premium and reduces risk appetite for {asset}.",
        ("geopolitical", "neutral"): f"Geopolitical development contained; limited direct exposure for {asset}.",
        ("supply_chain", "bearish"): f"Supply disruption raises input costs and constrains production capacity for {asset}.",
        ("crypto_policy", "bullish"): f"Positive regulatory clarity or ETF approval expands institutional access to {asset}.",
        ("crypto_policy", "bearish"): f"Restrictive regulatory action reduces market liquidity and sentiment for {asset}.",
        ("crypto_policy", "neutral"): f"Regulatory framework provides operational clarity without major impact on {asset} price.",
        ("company_guidance", "bullish"): f"Raised forward guidance reflects management confidence in demand for {asset}.",
        ("company_guidance", "bearish"): f"Lowered guidance signals demand weakness or cost pressure headwinds for {asset}.",
        ("macro_growth", "bullish"): f"Strong growth data supports risk-on sentiment, lifting {asset} outlook.",
        ("macro_growth", "bearish"): f"Disappointing growth data raises recession concerns, weighing on {asset}.",
        ("macro_growth", "mixed"): f"Mixed growth signals create uncertainty about near-term trajectory for {asset}.",
    }
    key = (event_type, direction)
    return templates.get(key, f"Synthetic signal: {event_type} event with {direction} implication for {asset}.")


def generate_stream(
    scenario: str,
    count: int = 20,
    output_path: str | Path | None = None,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    if scenario not in _SCENARIOS:
        scenario_keys = list(_SCENARIOS.keys())
        raise ValueError(
            f"Unknown scenario '{scenario}'. Available: {scenario_keys}"
        )

    if seed is not None:
        random.seed(seed)

    cfg = _SCENARIOS[scenario]
    event_cfg = cfg["events"][0]
    templates = event_cfg["headline_templates"]
    assets = event_cfg["assets"]
    event_type = event_cfg["event_type"]
    horizons = event_cfg["horizons"]
    directions_map = event_cfg["directions"]

    events: list[dict[str, Any]] = []
    base_time = datetime(2025, 1, 6, 9, 30, 0, tzinfo=timezone.utc)

    for i in range(count):
        idx = i % len(templates)
        asset = assets[i % len(assets)]
        headline = templates[idx].replace("{month}", _MONTHS[i % 12])
        direction = directions_map[asset][idx % len(directions_map[asset])]
        horizon = horizons[idx % len(horizons)]
        strength = _STRENGTHS[i % len(_STRENGTHS)]
        ts = base_time + timedelta(hours=i * 2 + random.randint(0, 3))

        events.append({
            "id": f"stream-{scenario}-{i + 1:04d}",
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "headline": headline,
            "source_type": "synthetic",
            "source_name": _SOURCE_NAMES[i % len(_SOURCE_NAMES)],
            "event_type": event_type,
            "asset": asset,
            "asset_type": _asset_type(asset),
            "expected_direction": direction,
            "time_horizon": horizon,
            "confidence": round(0.55 + (i % 9) * 0.05, 2),
            "summary": f"[Synthetic] {headline} Signal for {asset}: {direction} over {horizon.replace('_', ' ')} horizon.",
            "signal": {
                "direction": direction,
                "strength": strength,
                "rationale": _rationale(event_type, direction, asset),
            },
        })

    if output_path:
        write_jsonl(output_path, events)

    return events


def _asset_type(asset: str) -> str:
    mapping = {
        "SPY": "equity_etf", "QQQ": "equity_etf",
        "AAPL": "equity", "TSLA": "equity", "NVDA": "equity",
        "BTC": "crypto", "ETH": "crypto",
        "GLD": "commodity_etf", "US10Y": "bond", "EURUSD": "forex",
    }
    return mapping.get(asset, "equity")


def list_scenarios() -> list[str]:
    return list(_SCENARIOS.keys())
