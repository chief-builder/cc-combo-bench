#!/usr/bin/env bash
# Tier-2 (ExpenseHub) smoke check. Every combo runs this exact script —
# do not improvise a different one. Each combo must get a unique port.
#
# Usage: scripts/smoke_tier2.sh <app_dir> <port>
set -u

APP_DIR="${1:?usage: smoke_tier2.sh <app_dir> <port>}"
PORT="${2:?usage: smoke_tier2.sh <app_dir> <port>}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
BASE="http://127.0.0.1:$PORT"
TAGLINE="Know where it all goes."

cd "$APP_DIR"
"$PY" -m uvicorn app:app --port "$PORT" >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null' EXIT

for _ in $(seq 1 40); do
  curl -s -o /dev/null "$BASE/" && break
  sleep 0.25
done

FAILS=0

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
check "GET /expenses (200, heading)" 200 "All Expenses" "$BASE/expenses"
check "GET /expenses/1 (200)" 200 "" "$BASE/expenses/1"
check "GET /expenses/999999 (404)" 404 "" "$BASE/expenses/999999"

OUT=$(curl -s -o /dev/null -w "%{http_code} %{redirect_url}" \
  --data-urlencode "title=Smoke expense" \
  --data-urlencode "payee=Smoke Vendor" \
  --data-urlencode "amount=12.50" \
  --data-urlencode "category=smoke" \
  --data-urlencode "notes=Posted by the smoke script." \
  "$BASE/expenses")
CODE="${OUT%% *}"
LOC="${OUT#* }"
if [ "$CODE" = "303" ] && [ -n "$LOC" ]; then
  echo "ok    POST /expenses (303 to detail)"
else
  echo "FAIL  POST /expenses — expected 303 with Location, got $CODE '$LOC'"
  FAILS=$((FAILS + 1))
  LOC="$BASE/__missing__"
fi
check "new expense detail shows post" 200 "Smoke expense" "$LOC"

check "POST /expenses bad amount (422, is-invalid)" 422 "is-invalid" \
  --data-urlencode "title=T" \
  --data-urlencode "payee=P" \
  --data-urlencode "amount=abc" \
  --data-urlencode "category=smoke" \
  --data-urlencode "notes=" \
  "$BASE/expenses"

if [ "$FAILS" -eq 0 ]; then
  echo "SMOKE PASS"
else
  echo "SMOKE FAIL ($FAILS check(s))"
  exit 1
fi
