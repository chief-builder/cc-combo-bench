# Tier 2 — ExpenseHub — Sonnet 5 (orchestrator) / Sonnet 5 (sub-agent, per-phase x3)

## Prompts used

Each sub-agent prompt was built from the canonical prompt files with
placeholders filled: `{{WORKTREE}}` =
`/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase`,
`{{SPEC_DIR}}` = `specs/tier2-expensehub`, `{{MAIN_REPO}}` =
`/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench`.
Each was saved to a unique `mktemp` temp file and passed verbatim via:

```
cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase && claude -p --model sonnet --permission-mode acceptEdits --allowedTools "Bash" --output-format text < <tempfile>
```

Each sub-agent was spawned exactly once, in the foreground. No duplicate
spawn occurred.

### Phase 1 prompt (from `prompts/subagent-phase1.md`)

```
Implement Phase 1 of the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase/specs/tier2-expensehub/.
Work only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase — create every file there, never in any
other directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 1 of the roadmap exactly as written — file names, routes,
status codes, defaults, CDN links, and template contents are requirements,
not suggestions. Do not start any later phase.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 1 calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

### Phase 2 prompt (from `prompts/subagent-phase-later.md`, `{{PHASE}}`=2, `{{PREV_PHASE}}`=1)

```
The roadmap through Phase 1 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase/specs/tier2-expensehub/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 2 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 2 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 2 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 3 prompt (from `prompts/subagent-phase-later.md`, `{{PHASE}}`=3, `{{PREV_PHASE}}`=2)

```
The roadmap through Phase 2 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase/specs/tier2-expensehub/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 3 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 3 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 3 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/t2-sonnet-perphase && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

## Review findings

Files reviewed after each phase: `app.py`, `models.py`,
`templates/base.html`, `templates/home.html`, `templates/expenses.html`,
`templates/expense_detail.html`, `templates/expense_new.html`,
`tests/test_app.py`.

### Phase 1

All roadmap bullets satisfied: `app.py` with `/` route, `templates/base.html`
with doctype, `lang="en"`, charset/viewport meta, Bootstrap 5 CSS CDN,
favicon link to `python.org`'s favicon, default title block ("ExpenseHub"),
navbar with brand + Home/Expenses links, `{% block content %}`, Bootstrap
JS bundle at the bottom; `templates/home.html` extending base with the
exact tagline "Know where it all goes." and a welcoming paragraph; the
`if __name__ == "__main__"` block calling `uvicorn.run("app:app",
reload=True)`; smoke test checking 200 + tagline text.

- **Critical/functional** — none found.
- **Spec-conformance** — none found.
- **Minor/style** — none found.

### Phase 2

`models.py`'s `Expense` dataclass uses `field(default_factory=lambda:
datetime.now(timezone.utc))` for `spent_at` — the plan's standing ruling
treats this as correct. Seed data has 5 expenses across 3 categories
(`food`, `transport`, `software`) with realistic cent amounts and IDs 1-5.
`get_expense`/`new_expense_id` helpers match spec. `GET /expenses` sorts
newest-first and computes a rounded total; `GET /expenses/{expense_id}`
(typed `int`) 404s via `HTTPException` on a missing id.
`templates/expenses.html` renders the exact `Total: $X.XX` line and
Bootstrap cards with title link, payee/date, amount, and category badge.
`templates/expense_detail.html` has all required fields plus the "Back to
expenses" link. Tests match the roadmap's phase-2 list exactly.

- **Critical/functional** — none found.
- **Spec-conformance** — none found.
- **Minor/style** — none found.

### Phase 3

`app.py:16-25` — `GET /expenses` now accepts an optional `category` query
param, filters and totals correctly, and the template renders `Expenses
in "{category}"` + "Show all" link when filtered. `app.py:28-32` — `GET
/expenses/new` is registered **before** `GET /expenses/{expense_id}`
(app.py:88), correctly sidestepping the planted routing-order footgun
called out in the plan. `app.py:35-85` — `POST /expenses` validates
`title`/`payee`/`category` via `.strip()` non-empty checks, parses
`amount` with `float()`, rejects `<= 0`, re-renders the form with 422 +
preserved raw values on failure, and on success rounds to 2 decimals,
creates the `Expense`, appends it, and does a 303 redirect to the detail
page. `templates/expense_new.html` has `is-invalid`/`invalid-feedback`
per field and preserves all submitted values including the raw amount
text. Category badges in both `expenses.html` and `expense_detail.html`
now link to `/expenses?category={category}`. Tests cover category
filtering (with total), a valid POST + redirect + detail-page check, and
all three 422 cases (empty title, non-numeric amount, negative amount),
matching the roadmap's phase-3 test list exactly.

- **Critical/functional** — none found.
- **Spec-conformance** — none found.
- **Minor/style**:
  - `app.py:60-66` — amount parsing uses bare `float(amount)` with only a
    `<= 0` check. `float("nan")` succeeds and `nan <= 0` evaluates
    `False`, so a `POST` with `amount=nan` slips past validation and
    creates an expense with a `NaN` amount instead of being rejected, and
    `float("inf")` is likewise accepted as a valid positive amount.
    Neither the roadmap's own test list nor the held-out acceptance suite
    exercises these inputs, so it does not fail verification, but it is a
    latent gap against the "reject non-numeric text" requirement's intent.
  - `templates/expenses.html:23` and `templates/expense_detail.html:7` —
    the category badge link interpolates `expense.category` directly into
    the query string without URL-encoding. Jinja2 autoescaping covers HTML
    entities but not URL encoding, so a category containing `&`, `#`, or a
    space would produce a broken link. Harmless with the current
    single-word lowercase seed categories and not exercised by any test.

No extraneous files, dependencies, or features were added beyond what the
roadmap specifies in any phase. No later-phase work was started early by
any sub-agent.

## Verification

All three checks pass.

**1. Implementation's own tests** — PASS (9/9)

```
tests/test_app.py::test_home_page PASSED
tests/test_app.py::test_expenses_list PASSED
tests/test_app.py::test_expense_detail PASSED
tests/test_app.py::test_expense_detail_not_found PASSED
tests/test_app.py::test_expenses_filtered_by_category PASSED
tests/test_app.py::test_post_expense_valid_redirects_and_shows_amount PASSED
tests/test_app.py::test_post_expense_empty_title_is_invalid PASSED
tests/test_app.py::test_post_expense_non_numeric_amount_is_invalid PASSED
tests/test_app.py::test_post_expense_negative_amount_is_invalid PASSED

======================== 9 passed, 5 warnings in 0.13s =========================
```
(Warnings are an upstream FastAPI `DeprecationWarning` on Python 3.14, unrelated to this code.)

**2. Held-out acceptance suite** — PASS (24/24)

```
acceptance/tier2/test_spec.py::test_home_returns_200_with_tagline PASSED
acceptance/tier2/test_spec.py::test_html_lang_en PASSED
acceptance/tier2/test_spec.py::test_bootstrap5_css_cdn PASSED
acceptance/tier2/test_spec.py::test_bootstrap5_js_bundle PASSED
acceptance/tier2/test_spec.py::test_favicon_link PASSED
acceptance/tier2/test_spec.py::test_default_title PASSED
acceptance/tier2/test_spec.py::test_navbar_links PASSED
acceptance/tier2/test_spec.py::test_app_has_uvicorn_run_block PASSED
acceptance/tier2/test_spec.py::test_expense_is_dataclass_with_spec_fields PASSED
acceptance/tier2/test_spec.py::test_spent_at_defaults_to_aware_utc_now PASSED
acceptance/tier2/test_spec.py::test_seed_expenses PASSED
acceptance/tier2/test_spec.py::test_get_expense_helper PASSED
acceptance/tier2/test_spec.py::test_new_expense_id_helper PASSED
acceptance/tier2/test_spec.py::test_expenses_page_heading_seeds_newest_first_and_total PASSED
acceptance/tier2/test_spec.py::test_expense_titles_link_to_detail_and_badges PASSED
acceptance/tier2/test_spec.py::test_detail_page PASSED
acceptance/tier2/test_spec.py::test_detail_unknown_id_404 PASSED
acceptance/tier2/test_spec.py::test_category_filter_includes_excludes_and_totals PASSED
acceptance/tier2/test_spec.py::test_category_badges_link_to_filter PASSED
acceptance/tier2/test_spec.py::test_new_expense_form PASSED
acceptance/tier2/test_spec.py::test_post_expense_round_trip PASSED
acceptance/tier2/test_spec.py::test_post_expense_empty_title_422_preserves_notes PASSED
acceptance/tier2/test_spec.py::test_post_expense_non_numeric_amount_422_preserves_raw_text PASSED
acceptance/tier2/test_spec.py::test_post_expense_negative_amount_422 PASSED

======================== 24 passed, 5 warnings in 0.14s ========================
```

**3. Smoke script** — PASS

```
ok    GET / (200, tagline)
ok    GET /expenses (200, heading)
ok    GET /expenses/1 (200)
ok    GET /expenses/999999 (404)
ok    POST /expenses (303 to detail)
ok    new expense detail shows post
ok    POST /expenses bad amount (422, is-invalid)
SMOKE PASS
```

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 57 | 37 | 114 | 136,615 | 2,265,194 | 16,501 | $1.440 |
| Sub-agent session 1 | claude-sonnet-5 | 20 | 13 | 40 | 36,375 | 526,982 | 5,385 | $0.375 |
| Sub-agent session 2 | claude-sonnet-5 | 24 | 15 | 48 | 59,735 | 662,231 | 12,282 | $0.607 |
| Sub-agent session 3 | claude-sonnet-5 | 25 | 17 | 50 | 69,039 | 728,009 | 24,345 | $0.843 |
| **Total** | | | | | | | | **$3.265** |

Wall-clock (main-agent session span): 350s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_1d3374ec-f82/agent-a73c5bc8dd3e6ba16.jsonl`
- Sub-agent session 1: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-t2-sonnet-perphase/19dcb1b2-4c82-4b8f-8a50-7eab906c1761.jsonl`
- Sub-agent session 2: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-t2-sonnet-perphase/4c10b89e-f94c-400b-85c1-49aaf7a14078.jsonl`
- Sub-agent session 3: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-t2-sonnet-perphase/7d5abd17-5a40-46e0-9f19-4c1158a02df9.jsonl`

## Quality scorecard (uniform blind grading pass, 2026-08-20)

Graded as anonymized tree "L" (port 8151), shuffled within its tier
pair, fixed checklist derived from the roadmap (post money()-fix
suite), all three scripted checks re-run by the grader.

| Metric | Value |
|---|---|
| Acceptance tests passing | 24 / 24 |
| Own tests passing | 9 / 9 |
| Critical/functional mistakes | 0 |
| Spec-conformance defects | 0 |
| Minor/style issues | 2 |
| Smoke script | pass |

Defects:
- minor, app.py:62-66 — float() accepts nan/inf (nan <= 0 is False); non-finite amounts slip past validation.
- minor, templates/expenses.html:23 (also expense_detail.html:7) — category badge links un-URL-encoded.
