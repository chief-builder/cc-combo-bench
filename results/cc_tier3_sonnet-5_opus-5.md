# cc_tier3_sonnet-5_opus-5

Main agent: Sonnet 5 (orchestrator). Sub-agent: Opus 5, single spawn, all 4 phases.
Spec: `specs/tier3-invoicedesk`. Worktree: `cc-combo-bench-worktrees/t3-opus-single`.

## Prompts used

Verbatim sub-agent prompt (from `prompts/subagent-both-phases.md`, placeholders filled):

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t3-opus-single/specs/tier3-invoicedesk/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t3-opus-single — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t3-opus-single && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

Spawn command (foreground, 600000ms timeout):

```
cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t3-opus-single && claude -p --model opus --permission-mode acceptEdits --allowedTools "Bash" --output-format text < <tmpfile>
```

## Review findings

Reviewed `app.py`, `models.py`, all five templates, and `tests/test_app.py` against
`specs/tier3-invoicedesk/roadmap.md` phase by phase.

**Critical/functional:** none found.

**Spec-conformance:** none found.

**Minor/style:** none found.

Notes on things specifically checked and found conformant:
- `Invoice`/`Payment` dataclass field order and defaults match the roadmap exactly;
  `created_at`/`paid_at` use `field(default_factory=lambda: datetime.now(timezone.utc))`
  (per PLAN.md's standing ruling, this is the correct form, not the plain-import-time
  footgun).
- `STATUSES` and `ALLOWED_TRANSITIONS` module constants match verbatim.
- Seed data: 5 invoices (id 1-5) covering all three statuses (2 paid, 1 sent, 2 draft);
  5 payments across 3 invoices (1, 2, 5). Every paid seed invoice's payments sum to
  at least its amount (invoice 1: 2400.00 == 2400.00; invoice 5: 980.00 == 980.00).
  Payments exist only on sent/paid invoices (none on draft invoices 3, 4).
- `GET /invoices/new` (app.py:72) is registered before `GET /invoices/{invoice_id}`
  (app.py:121), so `/invoices/new` is not swallowed by the int path parameter — the
  route-ordering footgun the roadmap plants (per PLAN.md) is avoided.
- Status-filter validation (app.py:53-69), 404 on unknown invoice (app.py:121-126),
  payment-status gate returning the exact `Cannot record a payment on a {status}
  invoice` detail message (app.py:139-143), lifecycle transition and money-gate
  checks with the exact `Cannot move invoice from {x} to {y}` and `Cannot mark
  invoice paid: $P.PP of $A.AA paid` detail messages (app.py:163-174), and the
  `/api/invoices` route sorted by id with all seven required fields
  (app.py:199-212) all match the roadmap literally.
- 422 re-renders preserve raw submitted text for both the invoice-create form
  (`invoice_new.html`) and the payment form (`invoice_detail.html`), including
  non-numeric amount text.
- No dependencies added; `requirements.txt`/`requirements.lock` unchanged from
  the stripped worktree baseline.

## Verification

### 1. Implementation's own tests

`cd t3-opus-single && .venv/bin/python -m pytest tests/ -v`

**Result: PASS — 18 passed, 9 warnings in 0.15s** (warnings are an
`asyncio.iscoroutinefunction` deprecation from FastAPI 0.115.10 on Python 3.14,
internal to the library, unrelated to the implementation).

### 2. Held-out acceptance suite

`APP_DIR=t3-opus-single .venv/bin/pytest acceptance/tier3/test_spec.py -v`

**Result: FAIL — 29 passed, 2 failed** (31 total).

Both failures are the same class of mismatch, in `test_board_shows_seed_filter_links_and_paid_line`
and `test_stats_page_money_lines`: the acceptance suite's `money()` helper formats with a
thousands separator (`f"${round(x, 2):,.2f}"`, e.g. `$2,400.00`), while the app renders
amounts via `"%.2f"|format(...)` (e.g. `$2400.00`, no comma) — matching the roadmap's
literal `$X.XX` format spec, which never mentions a thousands separator anywhere in
`roadmap.md`. This reads as an acceptance-suite requirement beyond the roadmap's literal
text rather than an implementation miss, per PLAN.md's own note that "the rubric must not
infer test requirements beyond the roadmap's literal test list" — flagged here for the
blind grading pass to adjudicate, not adjudicated by this run.

Failing assertions:
- `assert '$2,400.00 of $2,400.00 paid' in <invoices board HTML>` — actual text contains
  `$2400.00 of $2400.00 paid`.
- `assert 'Total invoiced: $6,726.50' in <stats HTML>` — actual text contains
  `Total invoiced: $6726.50` (and likewise for `Total collected`/`Outstanding`).

### 3. Smoke script

`scripts/smoke_tier3.sh t3-opus-single 8143`

**Result: PASS — SMOKE PASS**, all 14 checks `ok` (home tagline, invoice board, status
filter valid/invalid, 404 on unknown invoice, create-invoice redirect, payment-on-draft
400, draft→sent, payment-on-sent, payment visible, sent→paid, stats page, API paid_total
field).

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 47 | 30 | 94 | 141,112 | 1,824,951 | 11,855 | $1.255 |
| Sub-agent | claude-opus-5 | 31 | 19 | 62 | 78,042 | 1,058,596 | 38,619 | $1.983 |
| **Total** | | | | | | | | **$3.238** |

Wall-clock (main-agent session span): 315s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_1d3374ec-f82/agent-ac0b8ba68276401f1.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-t3-opus-single/5b702c09-0001-447d-883f-01070f0a7ecb.jsonl`

## Quality scorecard (uniform blind grading pass, 2026-08-20)

Graded as anonymized tree "N" (port 8153), shuffled within its tier
pair, fixed checklist derived from the roadmap (post money()-fix
suite), all three scripted checks re-run by the grader.

| Metric | Value |
|---|---|
| Acceptance tests passing | 31 / 31 |
| Own tests passing | 18 / 18 |
| Critical/functional mistakes | 0 |
| Spec-conformance defects | 0 |
| Minor/style issues | 1 |
| Smoke script | pass |

Defects:
- minor, app.py:25-33 — parse_amount accepts nan/inf; non-finite invoice and payment amounts slip past validation.

Note: this run's in-run verification recorded 29/31 acceptance; both
failures were the suite's thousands-separator bug, fixed in commit
0df5f2c — the corrected suite passes 31/31, as re-run by the grader.
