# Tier 3 — InvoiceDesk — main: Sonnet 5, sub-agent: Haiku 4.5

## Prompts used

Verbatim sub-agent prompt (from `prompts/subagent-both-phases.md`, placeholders filled):

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-haiku/specs/tier3-invoicedesk/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-haiku, create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-haiku && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

Spawn command:

```
cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-haiku && claude -p --model haiku --permission-mode acceptEdits --allowedTools "Bash" --output-format text < <temp file>
```

## Review findings

Reviewed `app.py`, `models.py`, all five templates, and `tests/test_app.py`
against `specs/tier3-invoicedesk/roadmap.md` line by line. No
critical/functional or spec-conformance defects found. The implementation
matches the roadmap's file names, route signatures, status codes, HTTPException
detail strings (verbatim, e.g. `Cannot mark invoice paid: ${paid:.2f} of
${amount:.2f} paid`), status-badge color mapping, transition rules, and
`/invoices/new` route registered before `/invoices/{invoice_id}` (avoids the
int-path-shadowing footgun). `created_at`/`paid_at` use
`field(default_factory=lambda: datetime.now(timezone.utc))`, which the
project's standing ruling treats as correct. Non-finite amount rejection
(`math.isfinite`) is present on both the invoice-creation and payment routes.

**Critical/functional:** none found.

**Spec-conformance:** none found.

**Minor/style:**
- `models.py:60` — seed payment `Payment(invoice_id=1, amount=0.00, note="Correction adjustment", ...)` records a $0.00 payment in seed data. Not a spec violation (seed data bypasses the route-level "amount > 0" validation, and invoice 1's payments still sum to at least its amount), but a $0.00 payment line is an odd/unrealistic seed fixture.
- `templates/invoices.html:11` and `templates/stats.html:7` hardcode `["draft", "sent", "paid"]` in the Jinja loop instead of passing `STATUSES` from `models.py` into the template context. Harmless today since the literal list matches `STATUSES` exactly, but it duplicates the constant rather than referencing it.
- `app.py` — `paid_total(invoice_id)` is computed twice in both `invoice_detail` and `record_payment` (once for `balance_due`, once for the template context value); a trivial redundant call, no functional effect.

## Verification

**1. Implementation's own tests** — `python -m pytest tests/ -v`
Result: **PASS — 39 passed**, 0 failed (34 deprecation warnings, unrelated to app logic — `asyncio.iscoroutinefunction` and Starlette `TemplateResponse` argument-order deprecations).

**2. Held-out acceptance suite** — `acceptance/tier3/test_spec.py`
Result: **PASS — 32 passed / 32**, 0 failed.

**3. Smoke script** — `scripts/smoke_tier3.sh <worktree> 8502`
Result: **PASS — SMOKE PASS**, all 14 checks `ok` (home tagline, invoice board, status filter incl. 400 on bogus, 404 on unknown id, invoice creation round trip, payment-on-draft 400, draft→sent, payment recording, sent→paid, stats page, JSON API `paid_total` field).

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 46 | 27 | 92 | 205,499 | 1,550,133 | 13,039 | $1.432 |
| Sub-agent | claude-haiku-4-5-20251001 | 50 | 20 | 403 | 91,601 | 1,429,435 | 37,930 | $0.447 |
| **Total** | | | | | | | | **$1.879** |

Wall-clock (main-agent session span): 276s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b3ddfecb-3f1/agent-a5c8ec44112a062e7.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-nc-t3-haiku/952d11d6-7805-470d-af91-b4bce42281be.jsonl`

## Quality scorecard (uniform blind grading pass)

Graded in a shuffled anonymized batch of 4 (key: scratchpad/grading-key-nc.txt)
by two parallel graders (trees A-B / C-D), all scripted checks re-run on the
anonymized copies against the corrected suite (commit 5f069d8). Standing
rulings applied: required Form() for the optional note field = conformance;
payment form rendered only on sent invoices = minor (per the XP3 precedent);
duplicate seed client names = permitted, not a defect; weak tests (roadmap-
listed behavior not actually asserted) = conformance.

Graded as treeD (port 8514).

| Metric | Result |
|---|---|
| Acceptance tests passing | 32/32 |
| Own tests passing | 39/39 |
| Critical/functional | 0 |
| Spec-conformance | 3 |
| Minor/style | 5 |
| Smoke | pass |

Conformance: (1) app.py:112 — `note: str = Form(...)` makes the optional
note field required; (2) three roadmap-listed 303 assertions converted to
followed-200 assertions (`follow_redirects=True`, tests/test_app.py:151,
176, 232) — a direct-200 implementation would pass; (3) the "reduced
Balance due" behavior is never asserted — the reset fixture makes that test
check static seed data.

Minors: conditional payment form (per precedent), unused import, deprecated
TemplateResponse arg order, redundant re-parse, hardcoded status list.

App code itself is fully conformant — every canary dodged. The largest own
test suite of the batch (39 tests), but the extra count comes from
splitting, not coverage: quality gap is test rigor, not app behavior.
