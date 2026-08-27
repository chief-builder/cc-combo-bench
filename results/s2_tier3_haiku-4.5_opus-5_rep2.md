# Benchmark Run: Tier 3 (InvoiceDesk) — Haiku 4.5 (main) + Opus 5 (sub) — Rep 2

## Prompts used

### Sub-agent prompt (verbatim)

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-03/specs/tier3-invoicedesk/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-03 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-03 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

## Review findings

No defects found. The implementation correctly follows the roadmap specification:

- All four phases implemented completely
- Data model (Invoice and Payment dataclasses) with correct fields and defaults
- All routes implemented with correct HTTP methods, status codes, and response formats
- Form validation with `math.isfinite` correctly rejects nan/inf/non-positive amounts
- Lifecycle enforcement: status transitions respect ALLOWED_TRANSITIONS, sent→paid transition guards against insufficient payment
- Templates follow Bootstrap 5 structure with correct styling and formatting
- All money lines formatted to exactly two decimals and computed (not pattern-matched)
- Seed data consistent with rules (paid invoices have sufficient payments, payments exist only on sent/paid invoices)
- Tests comprehensive and passing

## Verification

### Implementation's own tests

**Result: PASS** (20/20)

```
======================== 20 passed, 9 warnings in 0.16s ========================
```

Tests covered all phases:
- Phase 1: home page with tagline
- Phase 2: invoice board, filtering, detail pages with 404 handling
- Phase 3: invoice creation with validation, payment recording, lifecycle transitions with money gate
- Phase 4: stats page with computed totals, JSON API with paid_total

### Held-out acceptance suite

**Result: PASS** (32/32)

```
======================== 32 passed, 9 warnings in 0.16s ========================
```

Full spec compliance verified including:
- HTML structure (lang=en, charset, viewport, favicon, Bootstrap CDN, title blocks)
- Data model fields and defaults with correct datetime handling
- Seed data consistency checks
- Route handling and status codes
- Form validation and error re-rendering with input preservation
- Status badges with correct color mapping
- Money calculations and formatting
- Lifecycle enforcement with payment-total gate
- Non-finite amount rejection (nan/inf)

### Smoke script

**Result: PASS**

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

All 14 smoke checks passed. Full end-to-end happy path verified including invoice creation, payment recording, status transitions, stats computation, and API response.

## Summary

**Verification: PASS** — All three verification steps succeeded.

- Implementation tests: 20/20 passed
- Acceptance suite: 32/32 passed  
- Smoke script: 14/14 checks passed

**Review findings: None** — Implementation conforms fully to roadmap specification. All four phases complete with correct routing, data model, validation, lifecycle enforcement, and formatting.

**Files created:**
- `app.py` — FastAPI application with 8 routes (home, invoices board with filtering, invoice detail, new form, create, payments, status transitions, stats, JSON API)
- `models.py` — Invoice/Payment dataclasses with 5 seed invoices and 5 seed payments, helper functions for lookups and calculations
- 6 templates (base, home, invoices, invoice_detail, invoice_new, stats)
- `tests/test_app.py` — 20 comprehensive tests

Cost stats will be appended from session transcript.

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-haiku-4-5-20251001 | 55 | 26 | 448 | 167,414 | 1,717,870 | 10,467 | $0.434 |
| Sub-agent | claude-opus-5 | 26 | 17 | 52 | 70,571 | 887,384 | 34,542 | $1.749 |
| **Total** | | | | | | | | **$2.182** |

Wall-clock (main-agent session span): 312s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b5fd4a3a-a70/agent-a45624abc3503e98f.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-s2-03/0b17a61c-e2a3-42f4-bef3-39a637ada4e4.jsonl`
