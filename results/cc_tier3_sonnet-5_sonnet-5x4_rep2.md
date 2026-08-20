# Tier 3 — InvoiceDesk — sonnet-5 orchestrator / sonnet-5 x4 sub-agents (rep 2)

## Prompts used

### Phase 1

```
Implement Phase 1 of the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet/specs/tier3-invoicedesk/.
Work only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet — create every file there, never in any
other directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 1 of the roadmap exactly as written — file names, routes,
status codes, defaults, CDN links, and template contents are requirements,
not suggestions. Do not start any later phase.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 1 calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

### Phase 2

```
The roadmap through Phase 1 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 2 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 2 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 2 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 3

```
The roadmap through Phase 2 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 3 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 3 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 3 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 4

```
The roadmap through Phase 3 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet/specs/tier3-invoicedesk/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 4 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 4 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 4 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/rep-t3-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

## Review findings

### Phase 1 — Home Page
No defects found. `app.py`, `templates/base.html`, `templates/home.html`, and
`tests/test_app.py` conform exactly to the roadmap: FastAPI instance, Jinja2
templates, Bootstrap 5 CDN CSS/JS, python.org favicon, navbar with the three
required links, hero tagline, `uvicorn.run` block, and the smoke test.

### Phase 2 — Invoice Board + Detail Pages
- **Minor/style** — `templates/invoices.html:27` and
  `templates/invoice_detail.html:10,19`: `created_at` and `paid_at` are
  rendered with the raw Python `str(datetime)` representation (e.g.
  `2026-08-01 09:00:00+00:00`) rather than a human-friendly format. The
  roadmap calls for "formatted `created_at`"; this is technically rendered
  but not attractively formatted. Borderline, not a hard violation.
- No functional or spec-conformance defects. `models.py` dataclasses,
  constants, helper functions, and seed data (5 invoices across all three
  statuses, 6 payments across 4 invoices, both `paid` seed invoices' payments
  sum to their full amount, no payments on the `draft` seed invoice) all
  match the roadmap. Routes, status filtering, 400/404 handling, badge
  colors, and the "$P.PP of $A.AA paid" / "Balance due: $X.XX" lines are all
  correct.

### Phase 3 — Create Invoices, Record Payments, Work the Lifecycle
- **Critical/functional** — `app.py:42` (`GET /invoices/{invoice_id}`, typed
  `int`) is registered *before* `app.py:54` (`GET /invoices/new`). Starlette
  matches routes in registration order; `/invoices/new` matches the
  `{invoice_id}` path pattern first, and FastAPI then fails to parse `"new"`
  as an int, returning **422** instead of serving the new-invoice form.
  Verified directly:
  ```
  GET /invoices/new -> 422
  {"detail":[{"type":"int_parsing","loc":["path","invoice_id"], ...,"input":"new"}]}
  ```
  This breaks the roadmap-required `GET /invoices/new` route and the "New
  invoice" button on the invoice board (`templates/invoices.html:8`) that
  links to it. Not caught by the Phase 3 sub-agent's own test suite because
  no test exercises `GET /invoices/new` directly (only `POST /invoices` is
  tested). Confirmed by the held-out acceptance suite (`test_new_invoice_form`
  failed with `422 != 200`).
- No other functional or spec-conformance defects. Validation rules,
  422/400/303 status codes, error re-rendering with preserved input,
  lifecycle transition buttons/labels, and the payment/status POST routes
  otherwise match the roadmap exactly.

### Phase 4 — Stats Page + JSON API
No defects found. `GET /stats` (`app.py:169`) and `templates/stats.html`
show all three status cards (including zero counts) and correctly computed
`Total invoiced` / `Total collected` / `Outstanding` lines. `GET
/api/invoices` (`app.py:187`) returns the correct 7-field JSON objects,
sorted by `id`, with ISO 8601 `created_at` and correct `paid_total`. The
Phase 3 route-ordering bug (above) persists unchanged, as expected since the
Phase 4 sub-agent was not asked to touch unrelated routes.

## Verification

### 1. Implementation's own tests — PASS
`cd rep-t3-sonnet && .venv/bin/python -m pytest tests/ -v`

```
19 passed, 9 warnings in 0.15s
```
All 19 tests (across all four phases) pass. Warnings are a pre-existing
`asyncio.iscoroutinefunction` deprecation notice from FastAPI on Python
3.14, unrelated to the implementation.

### 2. Held-out acceptance suite — FAIL (1 of 31)
`APP_DIR=rep-t3-sonnet .venv/bin/pytest acceptance/tier3/test_spec.py -v`

```
30 passed, 1 failed, 9 warnings in 0.18s

FAILED acceptance/tier3/test_spec.py::test_new_invoice_form - assert 422 == 200
```
The single failure is the route-ordering bug documented under Phase 3 above:
`GET /invoices/new` returns 422 instead of 200 because it is shadowed by the
earlier-registered `GET /invoices/{invoice_id}: int` route.

### 3. Smoke script — PASS
`scripts/smoke_tier3.sh rep-t3-sonnet 8162`

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
The smoke script does not exercise `GET /invoices/new` directly (it creates
invoices via `POST /invoices`), so it does not surface the route-ordering
bug.

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 53 | 29 | 106 | 123,238 | 2,125,729 | 14,905 | $1.324 |
| Sub-agent session 1 | claude-sonnet-5 | 15 | 11 | 30 | 30,206 | 393,321 | 4,334 | $0.296 |
| Sub-agent session 2 | claude-sonnet-5 | 26 | 16 | 52 | 67,054 | 775,801 | 16,743 | $0.735 |
| Sub-agent session 3 | claude-sonnet-5 | 35 | 23 | 70 | 143,127 | 1,321,990 | 80,752 | $2.145 |
| Sub-agent session 4 | claude-sonnet-5 | 22 | 14 | 44 | 76,372 | 666,523 | 10,728 | $0.647 |
| **Total** | | | | | | | | **$5.148** |

Wall-clock (main-agent session span): 522s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_137ac7f7-28a/agent-ad8e0193fcc1c6e2e.jsonl`
- Sub-agent session 1: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-rep-t3-sonnet/f997f5ec-fca7-4739-a029-c276af91c49c.jsonl`
- Sub-agent session 2: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-rep-t3-sonnet/4167b836-e5e4-419d-82fe-734af1379462.jsonl`
- Sub-agent session 3: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-rep-t3-sonnet/92b118dc-4a8e-4121-9aab-7b38f61fe2ce.jsonl`
- Sub-agent session 4: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-rep-t3-sonnet/9bd1f37f-b1e6-4db3-8628-18a5e97dd38a.jsonl`

## Quality scorecard (uniform blind grading pass, 2026-08-20)

Graded as anonymized tree "Q" (port 8164), shuffled pair, same
InvoiceDesk rubric, all three scripted checks re-run by the grader.

| Metric | Value |
|---|---|
| Acceptance tests passing | 30 / 31 |
| Own tests passing | 19 / 19 |
| Critical/functional mistakes | 1 |
| Spec-conformance defects | 0 |
| Minor/style issues | 4 |
| Smoke script | pass |

Defects:
- C1, app.py:42 vs app.py:54 — GET /invoices/{invoice_id} registered before GET /invoices/new; /invoices/new shadowed and 422s (own tests never hit the route). The same implicit cross-phase route-ordering critical as the original draw — 2-for-2.
- minor, app.py:77,124 — float(amount) lets nan/inf past the > 0 validation.
- minor, templates/invoices.html:29 + invoice_detail.html:13,45 — raw unformatted datetimes where the roadmap says "formatted".
