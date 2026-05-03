"""Static HTML page renderer — dark-theme, no external dependencies."""

from pathlib import Path
from typing import Any

CSS = """
:root {
  --bg:           #05070A;
  --bg2:          #0A0F14;
  --bg3:          #0D1319;
  --border:       rgba(126, 151, 160, 0.14);
  --border-str:   rgba(126, 151, 160, 0.22);
  --text:         #E8EEF2;
  --text-dim:     #A5B4BD;
  --text-muted:   #70818C;
  --text-faint:   #4F5C61;
  --accent:       #19D6B0;
  --accent-soft:  #30E2BF;
  --warn:         #E26A6A;
  --risk:         #D8B34B;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 15px;
  line-height: 1.6;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; color: var(--accent-soft); }
header {
  background: var(--bg2);
  border-bottom: 1px solid var(--border-str);
  padding: 14px 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}
header .logo { font-size: 1.15rem; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
header .logo span { color: var(--accent); }
header nav { margin-left: auto; display: flex; gap: 24px; }
header nav a { color: var(--text-muted); font-size: 13px; letter-spacing: 0.01em; }
header nav a:hover { color: var(--text); text-decoration: none; }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 24px; }
h1 { font-size: 1.85rem; font-weight: 700; margin-bottom: 6px; letter-spacing: -0.02em; }
h2 {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  margin: 32px 0 16px;
}
h3 { font-size: 1rem; font-weight: 600; margin: 20px 0 8px; }
p { color: var(--text-dim); margin-bottom: 12px; }
.subtitle { font-size: 0.95rem; color: var(--text-muted); margin-bottom: 32px; }
.badge {
  display: inline-block;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 2px 8px;
  font-size: 10px;
  font-weight: 500;
  color: var(--text-muted);
  margin-right: 6px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.badge.green { color: var(--accent); border-color: rgba(25, 214, 176, 0.35); background: rgba(25, 214, 176, 0.06); }
.badge.blue  { color: var(--accent); border-color: rgba(25, 214, 176, 0.35); background: rgba(25, 214, 176, 0.06); }
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 32px;
}
.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px 22px;
}
.card .label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.18em;
  margin-bottom: 10px;
}
.card .value { font-size: 28px; font-weight: 600; color: var(--accent); letter-spacing: -0.02em; line-height: 1.1; }
.card .sub { font-size: 12px; color: var(--text-faint); margin-top: 4px; }
.links { display: flex; gap: 10px; flex-wrap: wrap; margin: 24px 0; }
.links a {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px 18px;
  color: var(--text-dim);
  font-size: 13px;
  font-weight: 500;
}
.links a:hover { border-color: rgba(25, 214, 176, 0.35); color: var(--accent); text-decoration: none; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  margin-bottom: 24px;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
th {
  background: var(--bg3);
  border-bottom: 1px solid var(--border-str);
  padding: 9px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.18em;
}
td {
  border-bottom: 1px solid var(--border);
  padding: 11px 14px;
  color: var(--text);
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--bg3); }
.rank { font-weight: 600; color: var(--text-faint); }
.score-high { color: var(--accent); font-weight: 700; }
.score-mid  { color: var(--risk);   font-weight: 600; }
.score-low  { color: var(--text-muted); font-weight: 500; }
.disclaimer {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 2px solid var(--warn);
  border-radius: 8px;
  padding: 14px 18px;
  font-size: 13px;
  color: var(--text-muted);
  margin: 24px 0;
}
.stream-event {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 8px;
}
.stream-event:hover { border-color: var(--border-str); }
.stream-event .evt-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.stream-event .evt-title { font-weight: 600; color: var(--text); font-size: 14px; }
.stream-event .evt-meta { font-size: 12px; color: var(--text-muted); }
.dir-bullish { color: var(--accent); }
.dir-bearish { color: var(--warn); }
.dir-neutral { color: var(--text-muted); }
.dir-mixed   { color: var(--risk); }
footer {
  border-top: 1px solid var(--border);
  padding: 20px 32px;
  text-align: center;
  font-size: 12px;
  color: var(--text-faint);
  margin-top: 56px;
}
""".strip()


def _nav(current: str = "") -> str:
    pages = [
        ("index.html", "Home"),
        ("leaderboard.html", "Leaderboard"),
        ("streams.html", "Streams"),
    ]
    links = []
    for href, label in pages:
        if label == current:
            links.append(f'<a href="{href}" style="color:var(--text)">{label}</a>')
        else:
            links.append(f'<a href="{href}">{label}</a>')
    return "\n".join(links)


def _wrap(title: str, body: str, current: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — News2SignalLab</title>
<style>
{CSS}
</style>
</head>
<body>
<header>
  <div class="logo">News2Signal<span>Lab</span></div>
  <nav>
    {_nav(current)}
  </nav>
</header>
<div class="container">
{body}
</div>
<footer>
  News2SignalLab v0.1.0 &mdash; &copy; 2024-2026 Catalayer AI &mdash; Apache-2.0
</footer>
</body>
</html>"""


def _score_class(v: float) -> str:
    if v >= 0.85:
        return "score-high"
    if v >= 0.70:
        return "score-mid"
    return "score-low"


def render_index(
    dataset_count: int,
    pred_count: int,
    best_score: float,
    report_count: int,
    output_path: str | Path,
) -> None:
    body = f"""
<h1>News2SignalLab</h1>
<p class="subtitle">A complete local lab for turning financial news into structured signal evaluations.</p>

<div class="card-grid">
  <div class="card">
    <div class="label">Dataset Rows</div>
    <div class="value">{dataset_count}</div>
    <div class="sub">demo.jsonl</div>
  </div>
  <div class="card">
    <div class="label">Prediction Files</div>
    <div class="value">{pred_count}</div>
    <div class="sub">example baselines</div>
  </div>
  <div class="card">
    <div class="label">Best Overall Score</div>
    <div class="value">{best_score * 100:.1f}%</div>
    <div class="sub">oracle-baseline</div>
  </div>
  <div class="card">
    <div class="label">Generated Reports</div>
    <div class="value">{report_count}</div>
    <div class="sub">Markdown + HTML</div>
  </div>
</div>

<div class="links">
  <a href="leaderboard.html">&#x1F4CA; Leaderboard</a>
  <a href="streams.html">&#x1F300; Synthetic Streams</a>
  <a href="reports/oracle-baseline.html">&#x1F4C4; Oracle Report</a>
  <a href="reports/simple-baseline.html">&#x1F4C4; Baseline Report</a>
</div>

<h2>What is News2SignalLab?</h2>
<p>
News2SignalLab is a complete, offline-first evaluation lab for financial news-to-signal tasks.
It combines benchmark-style datasets, scoring, Markdown reports, a static HTML leaderboard,
and synthetic market-news streams into one end-to-end local workflow.
</p>

<h2>Ecosystem</h2>
<table>
<tr><th>Project</th><th>Role</th></tr>
<tr><td><strong>News2SignalBench</strong></td><td>Benchmark foundation — dataset format and evaluation contracts</td></tr>
<tr><td><strong>SignalEvalRunner</strong></td><td>Standalone evaluation runner — scoring and reporting primitives</td></tr>
<tr><td><strong>News2SignalLab</strong></td><td>Integrated reference lab — full end-to-end workflow in one CLI</td></tr>
</table>

<div class="disclaimer">
  <strong>Research only.</strong> All data in this lab is synthetic and for evaluation research purposes only.
  This is not financial advice, trading signals, or real market data.
  No API keys, no external model calls, no real news.
</div>
"""
    from .utils import write_text
    write_text(output_path, _wrap("Home", body, "Home"))


def render_leaderboard(
    entries: list[dict[str, Any]],
    output_path: str | Path,
) -> None:
    rows_html = ""
    for i, e in enumerate(entries, 1):
        model = e.get("model", "")
        overall = e.get("overall", 0.0)
        direction = e.get("direction_accuracy", 0.0)
        event_type = e.get("event_type_accuracy", 0.0)
        asset = e.get("asset_match", 0.0)
        horizon = e.get("time_horizon_match", 0.0)
        total = e.get("total", 0)
        notes = e.get("notes", "")
        report_link = f'reports/{model}.html'
        cls = _score_class(overall)
        rows_html += f"""
<tr>
  <td class="rank">{i}</td>
  <td><a href="{report_link}">{model}</a></td>
  <td class="{cls}">{overall * 100:.1f}%</td>
  <td>{direction * 100:.1f}%</td>
  <td>{event_type * 100:.1f}%</td>
  <td>{asset * 100:.1f}%</td>
  <td>{horizon * 100:.1f}%</td>
  <td>{total}</td>
  <td style="color:var(--text-muted);font-size:12px">{notes[:60]}</td>
</tr>"""

    body = f"""
<h1>Leaderboard</h1>
<p class="subtitle">Rankings by overall score across the demo benchmark dataset.</p>

<div class="disclaimer">
  <strong>Demo data only.</strong> These scores are computed against a synthetic 32-row dataset.
  They do not reflect real model capabilities. Not financial advice.
</div>

<table>
<tr>
  <th>Rank</th><th>Model</th><th>Overall</th><th>Direction</th>
  <th>Event Type</th><th>Asset Match</th><th>Time Horizon</th><th>Total</th><th>Notes</th>
</tr>
{rows_html}
</table>

<h2>Metric Definitions</h2>
<table>
<tr><th>Metric</th><th>Definition</th></tr>
<tr><td>Overall</td><td>Mean of all available per-metric scores</td></tr>
<tr><td>Direction</td><td>Fraction of examples with correct bullish/bearish/neutral/mixed prediction</td></tr>
<tr><td>Event Type</td><td>Fraction of examples with correct event category prediction</td></tr>
<tr><td>Asset Match</td><td>Fraction of examples where predicted asset matches ground truth</td></tr>
<tr><td>Time Horizon</td><td>Fraction of examples with correct intraday/short/medium/long horizon</td></tr>
</table>
"""
    from .utils import write_text
    write_text(output_path, _wrap("Leaderboard", body, "Leaderboard"))


def render_model_report(
    score_data: dict[str, Any],
    output_path: str | Path,
) -> None:
    model = score_data.get("model", "unknown")
    overall = score_data.get("overall", 0.0)
    direction = score_data.get("direction_accuracy", 0.0)
    event_type = score_data.get("event_type_accuracy", 0.0)
    asset_match = score_data.get("asset_match", 0.0)
    horizon = score_data.get("time_horizon_match", 0.0)
    total = score_data.get("total", 0)
    correct_dir = score_data.get("correct_direction", 0)
    correct_evt = score_data.get("correct_event_type", 0)
    correct_asset = score_data.get("correct_asset", 0)
    correct_horizon = score_data.get("correct_time_horizon", 0)
    failed = score_data.get("failed_examples", [])
    notes = score_data.get("notes", "")
    cls = _score_class(overall)

    failed_rows = ""
    for ex in failed[:20]:
        headline = ex.get("headline", "")[:65]
        expected = ex.get("expected_direction", "")
        predicted = ex.get("predicted_direction", "")
        asset = ex.get("asset", "")
        failed_rows += f"""
<tr>
  <td style="font-size:12px;color:var(--text-muted)">{ex.get('id','')}</td>
  <td style="font-size:13px">{headline}</td>
  <td class="dir-{expected}">{expected}</td>
  <td class="dir-{predicted}">{predicted}</td>
  <td>{asset}</td>
</tr>"""

    body = f"""
<h1>Report — {model}</h1>

<div class="disclaimer">
  Research only. Synthetic demo data. Not financial advice.
</div>

<div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr))">
  <div class="card">
    <div class="label">Overall Score</div>
    <div class="value {cls}">{overall * 100:.1f}%</div>
    <div class="sub">{total} examples</div>
  </div>
  <div class="card">
    <div class="label">Direction</div>
    <div class="value">{direction * 100:.1f}%</div>
    <div class="sub">{correct_dir}/{total}</div>
  </div>
  <div class="card">
    <div class="label">Event Type</div>
    <div class="value">{event_type * 100:.1f}%</div>
    <div class="sub">{correct_evt}/{total}</div>
  </div>
  <div class="card">
    <div class="label">Asset Match</div>
    <div class="value">{asset_match * 100:.1f}%</div>
    <div class="sub">{correct_asset}/{total}</div>
  </div>
  <div class="card">
    <div class="label">Time Horizon</div>
    <div class="value">{horizon * 100:.1f}%</div>
    <div class="sub">{correct_horizon}/{total}</div>
  </div>
</div>

{f'<h2>Failed Examples ({len(failed)})</h2><table><tr><th>ID</th><th>Headline</th><th>Expected</th><th>Predicted</th><th>Asset</th></tr>{failed_rows}</table>' if failed else ''}

{f'<h2>Notes</h2><p style="color:var(--text)">{notes}</p>' if notes else ''}

<h2>Limitations</h2>
<ul style="color:var(--text-muted);padding-left:20px;line-height:2">
  <li>Scores are against a 32-row synthetic demo dataset.</li>
  <li>Reasoning quality is not evaluated in v0.1.</li>
  <li>Results do not represent real-world model performance.</li>
  <li>Not financial advice.</li>
</ul>

<p style="margin-top:24px"><a href="../leaderboard.html">&larr; Back to Leaderboard</a></p>
"""
    from .utils import write_text
    write_text(output_path, _wrap(f"Report — {model}", body))


def render_streams_page(
    stream_samples: list[dict[str, Any]],
    output_path: str | Path,
) -> None:
    events_html = ""
    for ev in stream_samples[:15]:
        direction = ev.get("expected_direction") or ev.get("signal", {}).get("direction", "neutral")
        asset = ev.get("asset", "")
        event_type = ev.get("event_type", "")
        headline = ev.get("headline", "")
        ts = ev.get("timestamp", "")[:19].replace("T", " ")
        summary = ev.get("summary", "")[:120]
        strength = ev.get("signal", {}).get("strength", "")
        events_html += f"""
<div class="stream-event">
  <div class="evt-header">
    <span class="badge blue">{event_type}</span>
    <span class="badge">{asset}</span>
    <span class="badge dir-{direction}">{direction}</span>
    {f'<span class="badge">{strength}</span>' if strength else ''}
    <span class="evt-meta">{ts}</span>
  </div>
  <div class="evt-title">{headline}</div>
  {f'<div class="evt-meta" style="margin-top:6px">{summary}</div>' if summary else ''}
</div>"""

    body = f"""
<h1>Synthetic Streams</h1>
<p class="subtitle">Market-news event streams generated locally from scenario definitions.</p>

<div class="disclaimer">
  <strong>Synthetic data only.</strong> All events shown here are generated from scenario templates.
  They do not represent real news, real market data, or real financial signals.
  Do not use these for trading or investment decisions.
</div>

<h2>What are Synthetic Streams?</h2>
<p>
  Synthetic streams simulate market-news event sequences for testing and evaluation.
  Each event has a headline, event type, asset, expected direction, and signal metadata.
  Streams are generated from scenario JSON files and written as JSONL.
</p>

<h2>Available Scenarios</h2>
<table>
<tr><th>Scenario</th><th>Theme</th><th>Typical Assets</th></tr>
<tr><td>fed</td><td>Federal Reserve policy decisions and commentary</td><td>SPY, US10Y, GLD, EURUSD</td></tr>
<tr><td>cpi</td><td>Consumer Price Index releases and inflation data</td><td>GLD, SPY, US10Y, ETH</td></tr>
<tr><td>earnings</td><td>Corporate earnings beats, misses, and guidance</td><td>AAPL, TSLA, NVDA, QQQ</td></tr>
<tr><td>crypto-policy</td><td>Regulatory actions and policy affecting crypto</td><td>BTC, ETH</td></tr>
<tr><td>regulation</td><td>Sector-specific regulatory announcements</td><td>NVDA, QQQ, BTC</td></tr>
</table>

<h2>Sample Events</h2>
{events_html}

<h2>CLI Usage</h2>
<pre style="background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:16px;font-size:13px;overflow-x:auto">
news2signallab stream --scenario fed --count 20 --output outputs/streams/fed-stream.jsonl
news2signallab stream --scenario cpi --count 15 --output outputs/streams/cpi-stream.jsonl
news2signallab stream --scenario earnings --count 10 --output outputs/streams/earnings-stream.jsonl
</pre>
"""
    from .utils import write_text
    write_text(output_path, _wrap("Synthetic Streams", body, "Streams"))
