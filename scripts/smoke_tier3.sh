#!/usr/bin/env bash
# Tier-3 (AgentHelpdesk) smoke check. Every combo runs this exact script —
# do not improvise a different one. Each combo must get a unique port.
#
# Usage: scripts/smoke_tier3.sh <app_dir> <port>
set -u

APP_DIR="${1:?usage: smoke_tier3.sh <app_dir> <port>}"
PORT="${2:?usage: smoke_tier3.sh <app_dir> <port>}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
BASE="http://127.0.0.1:$PORT"
TAGLINE="File a ticket. A mediator agent will be with you shortly."

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
check "GET /tickets (200, heading)" 200 "Ticket Board" "$BASE/tickets"
check "GET /tickets?status=open (200)" 200 "" "$BASE/tickets?status=open"
check "GET /tickets?status=bogus (400)" 400 "" "$BASE/tickets?status=bogus"
check "GET /tickets/999999 (404)" 404 "" "$BASE/tickets/999999"

# create a ticket: expect 303 whose Location is the new detail page
OUT=$(curl -s -o /dev/null -w "%{http_code} %{redirect_url}" \
  --data-urlencode "title=Smoke ticket" \
  --data-urlencode "agent_name=Smoke Bot" \
  --data-urlencode "description=Filed by the smoke script." \
  "$BASE/tickets")
CODE="${OUT%% *}"
LOC="${OUT#* }"
if [ "$CODE" = "303" ] && [ -n "$LOC" ]; then
  echo "ok    POST /tickets (303 to detail)"
else
  echo "FAIL  POST /tickets — expected 303 with Location, got $CODE '$LOC'"
  FAILS=$((FAILS + 1))
  LOC="$BASE/__missing__"
fi
check "new ticket detail shows post" 200 "Smoke ticket" "$LOC"

check "POST comment (303)" 303 "" \
  --data-urlencode "author=Smoke Mediator" \
  --data-urlencode "text=Smoke check comment" \
  "$LOC/comments"
check "comment visible on detail" 200 "Smoke check comment" "$LOC"

check "illegal transition open->resolved (400)" 400 "" \
  --data-urlencode "new_status=resolved" "$LOC/status"
check "legal transition open->in_progress (303)" 303 "" \
  --data-urlencode "new_status=in_progress" "$LOC/status"

check "GET /stats (200)" 200 "Helpdesk Stats" "$BASE/stats"
check "GET /api/tickets (200, comment_count field)" 200 '"comment_count"' "$BASE/api/tickets"

if [ "$FAILS" -eq 0 ]; then
  echo "SMOKE PASS"
else
  echo "SMOKE FAIL ($FAILS check(s))"
  exit 1
fi
