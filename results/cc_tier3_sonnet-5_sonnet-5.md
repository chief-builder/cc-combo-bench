# cc_tier3_sonnet-5_sonnet-5

Tier 3 (InvoiceDesk), main agent: sonnet-5, sub-agent: sonnet-5.

## Prompts used

Verbatim sub-agent prompt (from `prompts/subagent-both-phases.md` with placeholders filled):

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-sonnet/specs/tier3-invoicedesk/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/nc-t3-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

## Review findings

### Critical / functional

- None found. All routes, status codes, validation rules, and lifecycle
  transitions in `app.py` match the roadmap exactly (checked against
  `roadmap.md` Phases 1–4).

### Spec-conformance

- `models.py:91-98` — Seed invoice `id=5` ("Riverbend Bakery", "Monthly
  bookkeeping — April") reuses the exact same client name as seed invoice
  `id=3` ("Riverbend Bakery", "Monthly bookkeeping — March", `models.py:75-82`).
  The roadmap only requires "5 invoices ... covering all three statuses,
  realistic cent amounts" and does not explicitly require unique client
  names, so this is not a strict violation of the written roadmap text.
  However, it causes the held-out acceptance test
  `test_board_sorted_newest_first` to fail (see Verification below):
  the test locates each invoice's card on the board by searching the
  HTML for its client name, and two identical client-name substrings
  collapse to the same `str.find()` position, making the position list
  look out of order even though the underlying `created_at`-descending
  sort in `GET /invoices` (`app.py:44`) is implemented correctly and
  matches the roadmap. This is a seed-data choice that inadvertently
  defeats a natural verification approach for a roadmap-mandated
  behavior (newest-first sorting).

### Minor / style

- `templates/invoice_detail.html:25-27` — references an `error` template
  variable (`{% if error %}...{% endif %}`) that is never passed by any
  route in `app.py` (only `payment_errors` is passed on the payment-form
  failure path). Dead template code; harmless but unused.
- `app.py:30` — the `badge_class` Jinja filter falls back to
  `text-bg-secondary` for unrecognized statuses; since `STATUSES` is a
  closed set of three values enforced everywhere, this fallback branch
  is unreachable in practice. Not a bug, just defensive code beyond what
  the roadmap asks for (roadmap says "do not add features... the roadmap
  doesn't ask for," though this is trivial enough not to flag as a real
  violation).

### Not defects (verified, pre-existing environment state)

- The worktree is missing many top-level repo files (`PLAN.md`,
  `prompts/`, `scripts/`, `results/`, `acceptance/tier1..3/test_spec.py`,
  etc. — 48 files reported as deleted by `git status`). Verified this is
  a pre-existing condition of the worktree setup shared across all
  sibling worktrees (`nc-t3-haiku`, `nc-t3-hh`, `nc-t3-opusx4` all show
  the identical 50 deletions and a missing `PLAN.md`), not something
  introduced by the sub-agent during this run. Not counted as a defect.

## Verification

### 1. Implementation's own tests — PASS

```
cd .../nc-t3-sonnet && .venv/bin/python -m pytest tests/ -v
...
19 passed, 9 warnings in 0.15s
```
(Warnings are pre-existing FastAPI/Starlette `asyncio.iscoroutinefunction`
deprecation notices, unrelated to the implementation.)

### 2. Held-out acceptance suite — FAIL (1 of 32)

```
APP_DIR=.../nc-t3-sonnet .venv/bin/pytest acceptance/tier3/test_spec.py -v
...
31 passed, 1 failed
FAILED acceptance/tier3/test_spec.py::test_board_sorted_newest_first
  AssertionError: assert [1507, 1996, 2471, 2954, 1996] == [1507, 1996, 1996, 2471, 2954]
```

Cause: seed invoices `id=3` and `id=5` share the identical client name
"Riverbend Bakery" (see Review findings above), which defeats the test's
client-name-substring position check even though the board's actual
sort-by-`created_at`-descending logic (`app.py:44`) matches the roadmap.

### 3. Smoke script — PASS

```
scripts/smoke_tier3.sh .../nc-t3-sonnet 8501
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
| Main agent | claude-sonnet-5 | 54 | 32 | 108 | 124,045 | 1,987,313 | 13,959 | $1.271 |
| Sub-agent | claude-sonnet-5 | 28 | 17 | 56 | 58,076 | 904,503 | 24,480 | $0.857 |
| **Total** | | | | | | | | **$2.128** |

Wall-clock (main-agent session span): 262s

Note: In-run acceptance was 31/32; the one failure was an instrument bug (sort test assumed unique seed client names, which the roadmap does not require — fixed in commit 5f069d8, same class as the 2026-08-20 money-formatter fix). The corrected suite passes 32/32; the grader re-ran it.

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b3ddfecb-3f1/agent-a6aec14eeeafb906b.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-nc-t3-sonnet/27de0cbc-f22d-4e80-8742-6cbd826277a1.jsonl`

## Quality scorecard (uniform blind grading pass)

Graded in a shuffled anonymized batch of 4 (key: scratchpad/grading-key-nc.txt)
by two parallel graders (trees A-B / C-D), all scripted checks re-run on the
anonymized copies against the corrected suite (commit 5f069d8). Standing
rulings applied: required Form() for the optional note field = conformance;
payment form rendered only on sent invoices = minor (per the XP3 precedent);
duplicate seed client names = permitted, not a defect; weak tests (roadmap-
listed behavior not actually asserted) = conformance.

Graded as treeB (port 8512).

| Metric | Result |
|---|---|
| Acceptance tests passing | 32/32 |
| Own tests passing | 19/19 |
| Critical/functional | 0 |
| Spec-conformance | 1 |
| Minor/style | 3 |
| Smoke | pass |

Conformance: tests/test_app.py:51-59 — the roadmap-listed "contains a seed
payment's note" is never actually asserted: the test picks seed invoice 1
(draft, zero payments) and guards the assertion with `if payment_list:`,
which is dead for that invoice.

Minors: dead `{% if error %}` template block; unused `request` param on
update_status; order-dependent tests + unused import.

All canaries dodged: `math.isfinite` at both validation points, `/invoices/
new` before the id route, `default_factory` datetimes, exact detail
strings, consistent seed money. In-run acceptance was 31/32 solely due to
the suite's unique-client-name assumption (instrument bug, fixed in
5f069d8): single Sonnet's app code is fully conformant at tier 3.
