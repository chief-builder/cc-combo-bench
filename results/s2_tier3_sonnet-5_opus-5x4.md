# s2 — tier3-invoicedesk — orchestrator: sonnet-5, sub-agents: opus-5 x4

## Prompts used

### Phase 1

```
Implement Phase 1 of the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07/specs/tier3-invoicedesk/.
Work only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 — create every file there, never in any
other directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 1 of the roadmap exactly as written — file names, routes,
status codes, defaults, CDN links, and template contents are requirements,
not suggestions. Do not start any later phase.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 1 calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

### Phase 2

```
The roadmap through Phase 1 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 2 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 2 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 2 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 3

```
The roadmap through Phase 2 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 3 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 3 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 3 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 4

```
The roadmap through Phase 3 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 4 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 4 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 4 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-07 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

## Review findings

No incidents (no duplicate spawns). Each phase's sub-agent was reviewed
against the roadmap immediately after it finished and before the next
sub-agent was spawned.

### Phase 1 — Home Page

No defects found. `app.py`, `templates/base.html`, `templates/home.html`,
and `tests/test_app.py` match the roadmap: correct doctype/lang, meta
tags, Bootstrap CDN links, python.org favicon, navbar links, title block
defaulting to "InvoiceDesk", jumbotron with the exact tagline, and the
`uvicorn.run("app:app", reload=True)` block.

### Phase 2 — Invoice Board + Detail Pages

No defects found. `models.py` dataclasses, `STATUSES`,
`ALLOWED_TRANSITIONS`, and helper functions match the spec signatures.
Seed data (`models.py:27-101`) satisfies the stated rules: invoice 1
(`paid`) has payments summing to exactly its $1450.00 amount
(`models.py:70-82`); payments exist only on `sent`/`paid` invoices
(none on draft invoices 3 or 5); 5 payments spread across 3 invoices
(1, 2, 4), meeting the "4-6 payments across at least 2 invoices"
requirement. `GET /invoices` (`app.py:16-33`) and
`GET /invoices/{invoice_id}` (`app.py:36-49`) implement the filter/400
and 404 behavior correctly. Templates (`templates/invoices.html`,
`templates/invoice_detail.html`) match the required content, badge
color mapping, `$P.PP of $A.AA paid` line, and exact
`Balance due: $X.XX` text.

### Phase 3 — Create Invoices, Record Payments, Work the Lifecycle

No defects found. `app.py` route ordering places `GET /invoices/new`
before `GET /invoices/{invoice_id}` so the literal path is matched
first. `parse_amount` (`app.py:23-32`) correctly parses via `float()`,
checks `math.isfinite`, and requires `> 0`, giving 422 on non-numeric,
`nan`, and `inf`/`-inf` amounts. `POST /invoices` (`app.py:91-130`),
`POST /invoices/{invoice_id}/payments` (`app.py:141-170`), and
`POST /invoices/{invoice_id}/status` (`app.py:173-195`) all follow the
roadmap's check order (404 → 400 → 422 where applicable) and produce
the exact `HTTPException` detail strings specified. Lifecycle buttons
in `templates/invoice_detail.html` are driven by `ALLOWED_TRANSITIONS`
and correctly show no button on a paid invoice. `invoice_new.html` and
the payment form preserve submitted values and apply
`is-invalid`/`invalid-feedback` correctly. Tests cover every case the
roadmap lists.

### Phase 4 — Stats Page + JSON API

No defects found. `GET /stats` (`app.py`, appended after Phase 3's
routes) computes per-status counts (all three shown, zero counts
included), `Total invoiced`, `Total collected`, and `Outstanding`
correctly rounded to two decimals. `GET /api/invoices` returns the
seven required fields per invoice, `created_at` via `.isoformat()`,
sorted by `id` ascending. `templates/stats.html` matches the required
heading, per-status cards, and exact money-line text.

## Verification

### 1. Implementation's own tests

Command: `cd .../s2-07 && .venv/bin/python -m pytest tests/ -v`

**Result: PASS — 22 passed, 9 warnings in 0.16s**

All 22 tests passed (2 from Phase 1, 5 from Phase 2, 13 from Phase 3, 2
from Phase 4). The 9 warnings are all the same pre-existing
`DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated...`
originating from FastAPI's `routing.py` under Python 3.14, unrelated to
the application code.

### 2. Held-out acceptance suite

Command:
`APP_DIR=.../s2-07 .venv/bin/pytest .../acceptance/tier3/test_spec.py -v`

**Result: PASS — 32 passed, 9 warnings in 0.16s**

All 32 acceptance tests passed, covering base layout, models/seed data,
invoice board/detail pages, invoice creation, payment recording,
lifecycle transitions with money rules, stats page, and the JSON API.
Same FastAPI/Python 3.14 deprecation warnings as above.

### 3. Smoke script

Command: `.../scripts/smoke_tier3.sh .../s2-07 8707`

**Result: PASS — SMOKE PASS**

```
ok    GET / (200, tagline)
ok    GET /invoices (200, heading)
ok    GET /invoices?status=draft (200)
ok    GET /invoices?status=bogus (400)
ok    GET /invoices/999999 (404)
ok    POST /invoices (303 to detail)
ok    new invoice detail shows client
ok    payment on draft invoice (400)
ok    draft -> sent (303)
ok    payment on sent invoice (303)
ok    payment visible on detail
ok    sent -> paid (303)
ok    GET /stats (200)
ok    GET /api/invoices (200, paid_total field)
SMOKE PASS
```

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 64 | 38 | 128 | 138,567 | 2,662,308 | 16,201 | $1.562 |
| Sub-agent session 1 | claude-opus-5 | 13 | 9 | 26 | 50,221 | 329,333 | 9,336 | $0.712 |
| Sub-agent session 2 | claude-opus-5 | 23 | 14 | 46 | 66,116 | 691,489 | 16,991 | $1.184 |
| Sub-agent session 3 | claude-opus-5 | 25 | 17 | 50 | 89,118 | 837,067 | 24,009 | $1.576 |
| Sub-agent session 4 | claude-opus-5 | 18 | 13 | 36 | 58,145 | 578,817 | 6,911 | $0.826 |
| **Total** | | | | | | | | **$5.860** |

Wall-clock (main-agent session span): 444s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b5fd4a3a-a70/agent-a45e17ce7f2067abc.jsonl`
- Sub-agent session 1: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-07/7e63b128-67a1-4560-b099-16049299cf53.jsonl`
- Sub-agent session 2: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-07/54368dbf-5b36-4c1e-bf5c-bb615a8d476f.jsonl`
- Sub-agent session 3: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-07/c1aed312-eef2-4d5b-9498-105ef2c9f729.jsonl`
- Sub-agent session 4: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-07/7e29b1e5-b8bb-4fa4-b7b8-b1bac6de1cb7.jsonl`
