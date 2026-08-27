# s2_tier3_sonnet-5_sonnet-5

Tier 3 (InvoiceDesk), main agent: sonnet-5, sub-agent: sonnet-5.

## Prompts used

Verbatim sub-agent prompt (from `prompts/subagent-both-phases.md` with placeholders filled):

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-04/specs/tier3-invoicedesk/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-04 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-04 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

## Review findings

Reviewed `models.py`, `app.py`, and all six templates (`base.html`,
`home.html`, `invoices.html`, `invoice_detail.html`, `invoice_new.html`,
`stats.html`) line-by-line against `specs/tier3-invoicedesk/roadmap.md`
Phases 1–4, plus `tests/test_app.py` for coverage of every roadmap-listed
test case.

### Critical / functional

- None found. All routes, status codes, redirect codes, validation rules
  (including the `math.isfinite` nan/inf/-inf checks required in Phase 3),
  and lifecycle-transition enforcement in `app.py` match the roadmap
  exactly.

### Spec-conformance

- None found. `models.py:23-24` reproduces `STATUSES` and
  `ALLOWED_TRANSITIONS` verbatim. Seed data (`app.py:26-97`) has 5
  invoices covering all three statuses and 4 payments spread across 3
  invoices (2, 3, 5), satisfying "4-6 payments spread across at least 2
  invoices"; both seed `paid` invoices (`id=3` sums to 800/800, `id=5`
  sums to 650/650) have payments summing to at least their amount, and
  payments exist only on `sent`/`paid` invoices (none on draft `id=1`).
  Exact required strings match: `Balance due: $X.XX`
  (`templates/invoice_detail.html:11`), the two `Cannot ...` HTTPException
  detail messages (`app.py:208-211`, `app.py:246-257`), and the `/stats`
  money lines (`templates/stats.html:18-20`).

### Minor / style

- `templates/invoices.html:26` and `templates/invoice_detail.html:9,29` —
  `created_at`/`paid_at` are rendered via Jinja's default `str(datetime)`
  (e.g. `2024-01-05 00:00:00+00:00`) rather than a friendlier format.
  The roadmap only says "formatted `created_at`" without specifying a
  format, so this is not a violation, just a plain rendering choice.
- `app.py:191-192` — the detail route always passes `form: None, errors:
  None` into the template context even on the happy-path `GET`; harmless,
  matches what the payment-form re-render path expects, just slightly
  redundant on the success path.

## Verification

### 1. Implementation's own tests — PASS

```
cd .../s2-04 && .venv/bin/python -m pytest tests/ -v
...
20 passed, 9 warnings in 0.14s
```
(Warnings are the pre-existing FastAPI/Starlette `asyncio.iscoroutinefunction`
deprecation notice, unrelated to the implementation.)

### 2. Held-out acceptance suite — PASS

```
APP_DIR=.../s2-04 .venv/bin/pytest acceptance/tier3/test_spec.py -v
...
32 passed, 9 warnings in 0.16s
```

### 3. Smoke script — PASS

```
scripts/smoke_tier3.sh .../s2-04 8704
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
| Main agent | claude-sonnet-5 | 40 | 25 | 80 | 108,478 | 1,431,955 | 9,308 | $0.976 |
| Sub-agent | claude-sonnet-5 | 49 | 27 | 98 | 76,246 | 1,873,931 | 37,127 | $1.405 |
| **Total** | | | | | | | | **$2.382** |

Wall-clock (main-agent session span): 285s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b5fd4a3a-a70/agent-a2f6b565296005609.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-04/ab26bb09-6a24-4490-bdab-6aa9d5d2d22b.jsonl`
