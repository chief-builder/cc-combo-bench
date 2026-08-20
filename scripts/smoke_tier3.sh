#!/usr/bin/env bash
# Tier-3 (InvoiceDesk) smoke check. Every combo runs this exact script —
# do not improvise a different one. Each combo must get a unique port.
#
# Usage: scripts/smoke_tier3.sh <app_dir> <port>
set -u

APP_DIR="${1:?usage: smoke_tier3.sh <app_dir> <port>}"
PORT="${2:?usage: smoke_tier3.sh <app_dir> <port>}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
BASE="http://127.0.0.1:$PORT"
TAGLINE="Bill it. Send it. Get paid."

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
check "GET /invoices (200, heading)" 200 "Invoices" "$BASE/invoices"
check "GET /invoices?status=draft (200)" 200 "" "$BASE/invoices?status=draft"
check "GET /invoices?status=bogus (400)" 400 "" "$BASE/invoices?status=bogus"
check "GET /invoices/999999 (404)" 404 "" "$BASE/invoices/999999"

OUT=$(curl -s -o /dev/null -w "%{http_code} %{redirect_url}" \
  --data-urlencode "client=Smoke Client Co" \
  --data-urlencode "description=Filed by the smoke script." \
  --data-urlencode "amount=250.00" \
  "$BASE/invoices")
CODE="${OUT%% *}"
LOC="${OUT#* }"
if [ "$CODE" = "303" ] && [ -n "$LOC" ]; then
  echo "ok    POST /invoices (303 to detail)"
else
  echo "FAIL  POST /invoices — expected 303 with Location, got $CODE '$LOC'"
  FAILS=$((FAILS + 1))
  LOC="$BASE/__missing__"
fi
check "new invoice detail shows client" 200 "Smoke Client Co" "$LOC"

check "payment on draft invoice (400)" 400 "" \
  --data-urlencode "note=too early" --data-urlencode "amount=10.00" "$LOC/payments"
check "draft -> sent (303)" 303 "" \
  --data-urlencode "new_status=sent" "$LOC/status"
check "payment on sent invoice (303)" 303 "" \
  --data-urlencode "note=Smoke payment" --data-urlencode "amount=250.00" "$LOC/payments"
check "payment visible on detail" 200 "Smoke payment" "$LOC"
check "sent -> paid (303)" 303 "" \
  --data-urlencode "new_status=paid" "$LOC/status"

check "GET /stats (200)" 200 "Billing Stats" "$BASE/stats"
check "GET /api/invoices (200, paid_total field)" 200 '"paid_total"' "$BASE/api/invoices"

if [ "$FAILS" -eq 0 ]; then
  echo "SMOKE PASS"
else
  echo "SMOKE FAIL ($FAILS check(s))"
  exit 1
fi
