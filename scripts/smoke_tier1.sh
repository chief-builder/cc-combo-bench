#!/usr/bin/env bash
# Tier-1 (AgentClinic) smoke check. Every combo runs this exact script —
# do not improvise a different one. Each combo must get a unique port.
#
# Usage: scripts/smoke_tier1.sh <app_dir> <port>
set -u

APP_DIR="${1:?usage: smoke_tier1.sh <app_dir> <port>}"
PORT="${2:?usage: smoke_tier1.sh <app_dir> <port>}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
BASE="http://127.0.0.1:$PORT"
TAGLINE="Come in. Sit down. Tell us about your human."

cd "$APP_DIR"
"$PY" -m uvicorn app:app --port "$PORT" >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null' EXIT

for _ in $(seq 1 40); do
  curl -s -o /dev/null "$BASE/" && break
  sleep 0.25
done

FAILS=0

# check <name> <expected_http_code> <required_body_text|""> [curl args...]
check() {
  local name="$1" want_code="$2" needle="$3"
  shift 3
  local body_file code
  body_file=$(mktemp)
  code=$(curl -s -o "$body_file" -w "%{http_code}" "$@")
  if [ "$code" != "$want_code" ]; then
    echo "FAIL  $name — expected HTTP $want_code, got $code"
    FAILS=$((FAILS + 1))
  elif [ -n "$needle" ] && ! grep -qF "$needle" "$body_file"; then
    echo "FAIL  $name — body missing: $needle"
    FAILS=$((FAILS + 1))
  else
    echo "ok    $name"
  fi
  rm -f "$body_file"
}

check "GET / (200, tagline)" 200 "$TAGLINE" "$BASE/"
check "GET /complaints (200, heading)" 200 "Complaints Board" "$BASE/complaints"
check "POST /complaints (303)" 303 "" \
  --data-urlencode "agent_name=Smoke Bot" \
  --data-urlencode "text=Smoke check complaint" \
  "$BASE/complaints"
check "new complaint visible" 200 "Smoke check complaint" "$BASE/complaints"

if [ "$FAILS" -eq 0 ]; then
  echo "SMOKE PASS"
else
  echo "SMOKE FAIL ($FAILS check(s))"
  exit 1
fi
