# Tier 2 ExpenseHub - Haiku 4.5 / Opus 5 - Rep 2

## Prompts used

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/pa-t2-opus/specs/tier2-expensehub/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/pa-t2-opus — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/pa-t2-opus && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

## Review findings

No defects found. The implementation fully satisfies the roadmap:

- All three phases (Home Page, Expense List + Detail Pages, Category Filtering + Add Expense) are complete
- All required files created: app.py, models.py, base.html, home.html, expenses.html, expense_detail.html, expense_new.html, test_app.py
- All routes implemented with correct status codes (200, 303, 404, 422)
- Form validation for title, payee, category (non-empty), and amount (numeric, finite, positive) is correct
- Category filtering works with dynamic heading and "Show all" link
- Amount rounding to 2 decimals implemented
- Seed data includes 5 expenses across 3 categories with realistic cent amounts
- Datetime defaults correctly using timezone-aware UTC
- Error handling preserves form input on validation failure
- Non-finite number validation (nan, inf, -inf) correctly rejects via math.isfinite()
- Route order correct: /expenses/new declared before /expenses/{expense_id} so literal path matches first

## Verification

### Implementation's own tests (tests/test_app.py)

**Result: PASS**

```
11 passed, 5 warnings in 0.18s
```

All tests pass:
- test_home_page_shows_tagline
- test_expenses_list_shows_titles_and_total
- test_expense_detail_shows_notes
- test_missing_expense_returns_404
- test_category_filter_shows_only_that_category
- test_new_expense_form_renders
- test_valid_post_redirects_to_detail_page
- test_empty_title_returns_422_and_preserves_notes
- test_non_numeric_amount_returns_422_and_preserves_raw_text
- test_negative_amount_returns_422
- test_non_finite_amounts_return_422

(Warnings are deprecation notices from FastAPI's asyncio.iscoroutinefunction check, not from implementation code)

### Acceptance tests (acceptance/tier2/test_spec.py)

**Result: PASS**

```
25 passed, 5 warnings in 0.14s
```

All acceptance tests pass, covering:
- HTML structure and attributes (lang="en", Bootstrap CDN, favicon, title block, navbar)
- Data model correctness (Expense dataclass fields, timezone-aware datetime)
- Seed data presence (4-6 expenses, 3+ categories)
- Helper functions (get_expense, new_expense_id)
- Expense list page (sorting, total calculation, category filtering)
- Detail page (404 handling, content rendering, category links)
- Form handling (empty fields, invalid amounts, nan/inf/negative values, input preservation)
- Redirect behavior (303 on success, 422 on validation failure)

### Smoke script (smoke_tier2.sh)

**Result: PASS**

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

Runtime verification confirms:
- Home page returns 200 with tagline
- Expense list page returns 200 with heading
- Detail pages load correctly
- 404 handling works for non-existent expenses
- Form submission redirects to detail page (303)
- New expense data persists and displays correctly
- Validation failures return 422 with error indication

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-haiku-4-5-20251001 | 42 | 20 | 348 | 153,255 | 864,257 | 9,943 | $0.328 |
| Sub-agent | claude-opus-5 | 26 | 17 | 52 | 67,099 | 754,450 | 19,394 | $1.282 |
| **Total** | | | | | | | | **$1.610** |

Wall-clock (main-agent session span): 188s

Note: Post-amendment replicate: first Claude draw of this cell against the amended spec letter (non-finite amounts scored; tier-2 suite 25 tests).

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_f4158d54-ede/agent-a96d7479af8f0071a.jsonl`
- Sub-agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench-worktrees-pa-t2-opus/b4e2cebf-e48c-4090-b29b-ea427bafb609.jsonl`

## Quality scorecard (uniform blind grading pass)

Graded as treeB in a shuffled anonymized batch of 2 (key:
scratchpad/grading-key-pa.txt); grader re-ran all scripted checks on
the anonymized copy (port 8295).

| Metric | Result |
|---|---|
| Acceptance tests passing | 25/25 |
| Own tests passing | 11/11 |
| Critical/functional | 0 |
| Spec-conformance | 0 |
| Minor/style | 2 |
| Smoke | pass |

Minors: (1) templates/expenses.html:31-32 + expense_detail.html:12-13 —
category badge links interpolate the category into `?category=...`
without `|urlencode` (roadmap letter satisfied; the recurring
cross-run/cross-provider minor); (2) tests/test_app.py — no data-reset
fixture; tests mutate shared seed state and pass only in file order
(no roadmap requirement violated).

Amendment outcome: `math.isfinite` present at app.py:75 (after
`float()`, before the positivity check); own tests assert all three of
`nan`/`inf`/`-inf` (tests/test_app.py:125-137). The NaN blind spot the
original draw carried as a minor is closed under the amended letter.
