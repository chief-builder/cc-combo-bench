# Benchmark Results: cc_tier2_haiku-4.5_sonnet-5x3

## Prompts used

### Phase 1 prompt

```
# Sub-agent — implement Phase 1 only

Used by combos 2, 3, 6 (spawned from kickoff-per-phase.md). Contains no
model reference, so it is byte-identical across sub-agent models.

---

Implement Phase 1 of the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet/specs/tier2-expensehub/.
Work only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet — create every file there, never in any
other directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 1 of the roadmap exactly as written — file names, routes,
status codes, defaults, CDN links, and template contents are requirements,
not suggestions. Do not start any later phase.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 1 calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

### Phase 2 prompt

```
# Sub-agent — implement one later phase (specs with 3+ phases)

Used by kickoff-per-phase-multi.md for every phase after Phase 1.
2 = the phase number to implement; 1 = the highest
phase already implemented (2 - 1). Tier-1 runs keep using
subagent-phase2.md unchanged for round-to-round comparability. Contains
no model reference, so it is byte-identical across sub-agent models.

---

The roadmap through Phase 1 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet/specs/tier2-expensehub/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 2 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 2 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 2 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

### Phase 3 prompt

```
# Sub-agent — implement one later phase (specs with 3+ phases)

Used by kickoff-per-phase-multi.md for every phase after Phase 1.
3 = the phase number to implement; 2 = the highest
phase already implemented (3 - 1). Tier-1 runs keep using
subagent-phase2.md unchanged for round-to-round comparability. Contains
no model reference, so it is byte-identical across sub-agent models.

---

The roadmap through Phase 2 of the app specified in
/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet/specs/tier2-expensehub/ is already implemented in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet. Work
only inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then
implement Phase 3 of the roadmap exactly as written — file
names, routes, status codes, defaults, CDN links, and template contents
are requirements, not suggestions. Do not start any later phase. Modify
existing files only where Phase 3 requires it; leave the rest
of the earlier code as you found it, even if you disagree with it.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests Phase 3 calls for and run the full suite with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until it passes.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created or
  changed and the final test output.
```

## Review findings

No critical, functional, spec-conformance, or minor/style defects identified across all three phases.

**Phase 1**: All roadmap requirements met. App instance, base template with Bootstrap CDN, favicon, navbar, home page with tagline, root route, smoke test.

**Phase 2**: All roadmap requirements met. Expense dataclass with timezone-aware UTC default for spent_at, 6 seed expenses across 3+ categories with realistic amounts, helper functions, `/expenses` list route with newest-first sort and correct total formatting, expense detail route with 404 handling, and all required template content and tests.

**Phase 3**: All roadmap requirements met. Category filtering with query param and conditional heading, category badges as links, form page with validation (title/payee/category non-empty, amount positive numeric), 422 error responses with preserved input, 303 redirect on success, and all required tests.

## Verification

### Implementation's own tests

```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-8.3.4, pluggy-1.6.0 -- /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/x-t2-sonnet
plugins: anyio-4.14.2
collecting ... collected 9 items

tests/test_app.py::test_home_page PASSED                                 [ 11%]
tests/test_app.py::test_expenses_list PASSED                             [ 22%]
tests/test_app.py::test_expense_detail PASSED                            [ 33%]
tests/test_app.py::test_expense_detail_not_found PASSED                  [ 44%]
tests/test_app.py::test_expenses_filtered_by_category PASSED             [ 55%]
tests/test_app.py::test_create_expense_valid_redirects_and_shows_amount PASSED [ 66%]
tests/test_app.py::test_create_expense_empty_title_returns_422 PASSED    [ 77%]
tests/test_app.py::test_create_expense_non_numeric_amount_returns_422 PASSED [ 88%]
tests/test_app.py::test_create_expense_negative_amount_returns_422 PASSED [100%]

========================== 9 passed, 5 warnings in 0.13s ==========================
```

**Result: PASS** — All 9 tests passing.

### Held-out acceptance suite

```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-8.3.4, pluggy-1.6.0 -- /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench
plugins: anyio-4.14.2
collecting ... collected 24 items

acceptance/tier2/test_spec.py::test_home_returns_200_with_tagline PASSED [  4%]
acceptance/tier2/test_spec.py::test_html_lang_en PASSED                  [  8%]
acceptance/tier2/test_spec.py::test_bootstrap5_css_cdn PASSED            [ 12%]
acceptance/tier2/test_spec.py::test_bootstrap5_js_bundle PASSED          [ 16%]
acceptance/tier2/test_spec.py::test_favicon_link PASSED                  [ 20%]
acceptance/tier2/test_spec.py::test_default_title PASSED                 [ 25%]
acceptance/tier2/test_spec.py::test_navbar_links PASSED                  [ 29%]
acceptance/tier2/test_spec.py::test_app_has_uvicorn_run_block PASSED     [ 33%]
acceptance/tier2/test_spec.py::test_expense_is_dataclass_with_spec_fields PASSED [ 37%]
acceptance/tier2/test_spec.py::test_spent_at_defaults_to_aware_utc_now PASSED [ 41%]
acceptance/tier2/test_spec.py::test_seed_expenses PASSED                 [ 45%]
acceptance/tier2/test_spec.py::test_get_expense_helper PASSED            [ 50%]
acceptance/tier2/test_spec.py::test_new_expense_id_helper PASSED         [ 54%]
acceptance/tier2/test_spec.py::test_expenses_page_heading_seeds_newest_first_and_total PASSED [ 58%]
acceptance/tier2/test_spec.py::test_expense_titles_link_to_detail_and_badges PASSED [ 62%]
acceptance/tier2/test_spec.py::test_detail_page PASSED                   [ 66%]
acceptance/tier2/test_spec.py::test_detail_unknown_id_404 PASSED         [ 70%]
acceptance/tier2/test_spec.py::test_category_filter_includes_excludes_and_totals PASSED [ 75%]
acceptance/tier2/test_spec.py::test_category_badges_link_to_filter PASSED [ 79%]
acceptance/tier2/test_spec.py::test_new_expense_form PASSED              [ 83%]
acceptance/tier2/test_spec.py::test_post_expense_round_trip PASSED       [ 87%]
acceptance/tier2/test_spec.py::test_post_expense_empty_title_422_preserves_notes PASSED [ 91%]
acceptance/tier2/test_spec.py::test_post_expense_non_numeric_amount_422_preserves_raw_text PASSED [ 95%]
acceptance/tier2/test_spec.py::test_post_expense_negative_amount_422 PASSED [100%]

========================== 24 passed, 5 warnings in 0.14s =========================
```

**Result: PASS** — All 24 acceptance tests passing.

### Smoke script

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

**Result: PASS** — All smoke checks passing.

## Summary

- **Verification outcome**: Full pass — 9/9 implementation tests, 24/24 acceptance tests, smoke script.
- **Code quality**: No defects found in review. All roadmap requirements implemented correctly across three phases.
- **Phase compliance**: Phase 1 (home page), Phase 2 (expense list/detail), Phase 3 (category filtering, form with validation) all complete and correct.

Cost stats and blind grading scorecard to be appended post-run.

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-haiku-4-5-20251001 | 83 | 36 | 670 | 78,200 | 2,342,816 | 14,219 | $0.404 |
| Sub-agent session 1 | claude-sonnet-5 | 16 | 10 | 32 | 34,615 | 421,447 | 6,611 | $0.356 |
| Sub-agent session 2 | claude-sonnet-5 | 20 | 14 | 40 | 47,412 | 534,004 | 10,211 | $0.491 |
| Sub-agent session 3 | claude-sonnet-5 | 26 | 17 | 52 | 84,859 | 767,537 | 30,914 | $1.012 |
| **Total** | | | | | | | | **$2.263** |

Wall-clock (main-agent session span): 370s

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_53dc66f7-3e1/agent-a6595e9fa953ea41d.jsonl`
- Sub-agent session 1: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-x-t2-sonnet/fb306dd4-fa6c-4be5-a39a-a927c0867c97.jsonl`
- Sub-agent session 2: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-x-t2-sonnet/18b3b9c1-60d1-4504-a2a1-e83b16b4d3c7.jsonl`
- Sub-agent session 3: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-x-t2-sonnet/575442da-f847-4a2c-9c80-96c755c5668a.jsonl`

## Quality scorecard (uniform blind grading pass, 2026-08-20)

Graded as anonymized tree "R" (port 8175), shuffled within its tier
pair, same tier rubric as prior passes, all three scripted checks
re-run by the grader.

| Metric | Value |
|---|---|
| Acceptance tests passing | 24 / 24 |
| Own tests passing | 9 / 9 |
| Critical/functional mistakes | 0 |
| Spec-conformance defects | 0 |
| Minor/style issues | 2 |
| Smoke script | pass |

Defects:
- minor, app.py:57-58 — nan/inf pass amount validation.
- minor, templates/expenses.html:21 (also expense_detail.html:8) — category filter links not URL-encoded.
