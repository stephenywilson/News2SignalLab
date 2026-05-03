#!/usr/bin/env bash
# News2SignalLab smoke test
# Run from the project root: bash scripts/smoke_test.sh

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

check() {
    local label="$1"
    local condition="$2"
    if eval "$condition"; then
        echo "  [PASS] $label"
        PASS=$((PASS + 1))
    else
        echo "  [FAIL] $label"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "News2SignalLab Smoke Test"
echo "========================="
echo "Root: $ROOT"
echo ""

# ---- Install check ----
echo "[Step 1] Checking install..."
if ! python3 -m news2signallab --version 2>/dev/null; then
    echo "  Package not installed. Running: python3 -m pip install -e ."
    python3 -m pip install -e . -q
fi
check "python3 -m news2signallab --version" "python3 -m news2signallab --version 2>&1 | grep -q '0.1.0'"
check "news2signallab --help returns zero" "python3 -m news2signallab --help > /dev/null 2>&1"

# ---- Demo pipeline ----
echo ""
echo "[Step 2] Running demo pipeline..."
python3 -m news2signallab demo

# ---- Output directory checks ----
echo ""
echo "[Step 3] Checking outputs..."
check "outputs/scores/ exists" "[ -d outputs/scores ]"
check "outputs/reports/ exists" "[ -d outputs/reports ]"
check "outputs/streams/ exists" "[ -d outputs/streams ]"

check "outputs/scores/oracle-baseline.json" "[ -f outputs/scores/oracle-baseline.json ]"
check "outputs/scores/simple-baseline.json" "[ -f outputs/scores/simple-baseline.json ]"
check "outputs/scores/noisy-local-model.json" "[ -f outputs/scores/noisy-local-model.json ]"

check "outputs/reports/oracle-baseline.md" "[ -f outputs/reports/oracle-baseline.md ]"
check "outputs/reports/simple-baseline.md" "[ -f outputs/reports/simple-baseline.md ]"
check "outputs/reports/noisy-local-model.md" "[ -f outputs/reports/noisy-local-model.md ]"

check "outputs/streams/fed-stream.jsonl" "[ -f outputs/streams/fed-stream.jsonl ]"
check "outputs/streams/cpi-stream.jsonl" "[ -f outputs/streams/cpi-stream.jsonl ]"
check "outputs/streams/earnings-stream.jsonl" "[ -f outputs/streams/earnings-stream.jsonl ]"

# ---- Site checks ----
echo ""
echo "[Step 4] Checking static site..."
check "site/index.html" "[ -f site/index.html ]"
check "site/leaderboard.html" "[ -f site/leaderboard.html ]"
check "site/streams.html" "[ -f site/streams.html ]"
check "site/data/leaderboard.json" "[ -f site/data/leaderboard.json ]"
check "site/assets/style.css" "[ -f site/assets/style.css ]"
check "site/reports/oracle-baseline.html" "[ -f site/reports/oracle-baseline.html ]"
check "site/reports/simple-baseline.html" "[ -f site/reports/simple-baseline.html ]"

# ---- Validate command ----
echo ""
echo "[Step 5] Testing validate command..."
check "validate dataset" "python3 -m news2signallab validate --dataset datasets/demo.jsonl 2>&1 | grep -q 'valid'"
check "validate dataset + predictions" "python3 -m news2signallab validate --dataset datasets/demo.jsonl --predictions examples/predictions/simple-baseline.jsonl 2>&1 | grep -q 'valid'"

# ---- Score command ----
echo ""
echo "[Step 6] Testing score command..."
python3 -m news2signallab score \
    --dataset datasets/demo.jsonl \
    --predictions examples/predictions/simple-baseline.jsonl \
    --output /tmp/n2sl_smoke_score.json
check "score produces JSON output" "[ -f /tmp/n2sl_smoke_score.json ]"
check "score JSON has overall field" "python3 -c \"import json; d=json.load(open('/tmp/n2sl_smoke_score.json')); assert 'overall' in d\""

# ---- Report command ----
echo ""
echo "[Step 7] Testing report command..."
python3 -m news2signallab report \
    --score /tmp/n2sl_smoke_score.json \
    --output /tmp/n2sl_smoke_report.md
check "report produces Markdown output" "[ -f /tmp/n2sl_smoke_report.md ]"
check "report contains model name" "grep -q 'simple-baseline' /tmp/n2sl_smoke_report.md"

# ---- Board command ----
echo ""
echo "[Step 8] Testing board command..."
python3 -m news2signallab board \
    --input outputs/scores \
    --output /tmp/n2sl_smoke_site
check "board produces index.html" "[ -f /tmp/n2sl_smoke_site/index.html ]"
check "board produces leaderboard.html" "[ -f /tmp/n2sl_smoke_site/leaderboard.html ]"
check "board produces leaderboard.json" "[ -f /tmp/n2sl_smoke_site/data/leaderboard.json ]"
check "board produces style.css" "[ -f /tmp/n2sl_smoke_site/assets/style.css ]"

# ---- Stream command ----
echo ""
echo "[Step 9] Testing stream command..."
check "stream list" "python3 -m news2signallab stream --list 2>&1 | grep -q 'fed'"
python3 -m news2signallab stream --scenario fed --count 5 --seed 42 --output /tmp/n2sl_smoke_stream.jsonl
check "stream produces JSONL" "[ -f /tmp/n2sl_smoke_stream.jsonl ]"
check "stream JSONL has 5 lines" "[ \$(wc -l < /tmp/n2sl_smoke_stream.jsonl) -eq 5 ]"

# ---- Privacy scan ----
echo ""
echo "[Step 10] Privacy scan..."
SCAN_INCLUDE="--include=*.py --include=*.json --include=*.jsonl --include=*.md --include=*.toml --include=*.sh --include=*.css"
if grep -r $SCAN_INCLUDE "$HOME" README.md docs examples datasets scenarios news2signallab pyproject.toml scripts/smoke_test.sh 2>/dev/null | grep -qv "scripts/smoke_test.sh"; then
    echo "  [FAIL] no absolute home paths in source"
    FAIL=$((FAIL + 1))
else
    echo "  [PASS] no absolute home paths in source"
    PASS=$((PASS + 1))
fi
if grep -r $SCAN_INCLUDE "OPENAI_API_KEY\|ANTHROPIC_API_KEY\|sk-proj-\|Bearer sk-" README.md docs examples datasets scenarios news2signallab pyproject.toml 2>/dev/null | grep -q .; then
    echo "  [FAIL] no API key references in source"
    FAIL=$((FAIL + 1))
else
    echo "  [PASS] no API key references in source"
    PASS=$((PASS + 1))
fi

# ---- No API keys required verification ----
echo ""
echo "[Step 11] Verifying no external calls required..."
check "OPENAI_API_KEY not set or irrelevant" "! (python3 -m news2signallab demo 2>&1 | grep -qi 'openai')"

# ---- Summary ----
echo ""
echo "========================="
echo "Results: $PASS passed, $FAIL failed"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "All checks passed. News2SignalLab smoke test SUCCEEDED."
    exit 0
else
    echo "Some checks failed. Review output above."
    exit 1
fi
