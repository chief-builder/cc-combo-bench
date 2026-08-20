# Tier 2 — ExpenseHub — Sonnet 5 (orchestrator) / Codex (sub-agent, single-shot)

## Prompts used

Verbatim sub-agent prompt (built from `prompts/subagent-both-phases.md` with
placeholders filled: `{{WORKTREE}}` =
`/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2`,
`{{SPEC_DIR}}` = `specs/tier2-expensehub`, `{{MAIN_REPO}}` =
`/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench`):

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2/specs/tier2-expensehub/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

The sub-agent was spawned exactly once, in the foreground, via:

```
cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2 && codex exec --full-auto --skip-git-repo-check - < <tempfile>
```

No duplicate spawn occurred.

## Review findings

Files reviewed: `app.py`, `models.py`, `templates/base.html`,
`templates/home.html`, `templates/expenses.html`,
`templates/expense_detail.html`, `templates/expense_new.html`,
`tests/test_app.py`.

The implementation matches the roadmap closely across all three phases:
file/route names match, status codes (200/303/404/422) match, the
`base.html` head (charset, viewport, Bootstrap 5 CDN CSS/JS, favicon,
title block, navbar) matches the spec verbatim, the money-validation
logic uses `math.isfinite()` exactly as the roadmap's hint requires
(rejecting non-numeric text, zero, negatives, `nan`, and `inf`), and the
`GET /expenses/new` route is registered before the parametrized
`GET /expenses/{expense_id}` route so it is not shadowed by the int
path-converter.

**Critical/functional**

- None found.

**Spec-conformance**

- None found — every roadmap bullet for Phase 1–3 has a corresponding,
  correctly wired implementation (independently confirmed by the
  held-out acceptance suite, 25/25 passing).

**Minor/style**

- `templates/expenses.html:27` and `templates/expense_detail.html:11` —
  the category badge link interpolates `expense.category` directly into
  the query string (`/expenses?category={{ expense.category }}`) without
  URL-encoding. Jinja2 autoescaping covers HTML entities but not URL
  encoding, so a category containing `&`, `#`, `+`, or a space would
  produce a broken or misparsed link. Harmless with the current seed
  data (single-word lowercase categories: food, transport, software) and
  not exercised by any test, but a latent bug if a user later submits a
  multi-word category via the add-expense form (categories are free text,
  unvalidated beyond non-empty).
- `app.py:60-64` / `expense_new.html:31` — `notes` has no `errors["notes"]`
  branch ever populated (notes is optional per spec), so the
  `{% if errors.notes %}` block in the template is permanently dead code.
  Harmless, matches spec intent (notes has no validation), just a minor
  unreachable-branch smell.

No extraneous files, dependencies, or features were added beyond what
the roadmap specifies. Files created: `app.py`, `models.py`,
`templates/base.html`, `templates/home.html`, `templates/expenses.html`,
`templates/expense_detail.html`, `templates/expense_new.html`,
`tests/test_app.py`.

## Verification

All three checks pass.

**1. Implementation's own tests** — PASS (10/10)

```
tests/test_app.py::test_home_page PASSED
tests/test_app.py::test_expense_list PASSED
tests/test_app.py::test_expense_detail PASSED
tests/test_app.py::test_missing_expense_returns_404 PASSED
tests/test_app.py::test_category_filter PASSED
tests/test_app.py::test_create_expense PASSED
tests/test_app.py::test_empty_title_is_rejected_and_preserves_notes PASSED
tests/test_app.py::test_non_numeric_amount_is_rejected_and_preserved PASSED
tests/test_app.py::test_negative_amount_is_rejected PASSED
tests/test_app.py::test_non_finite_amount_is_rejected PASSED

======================== 10 passed, 5 warnings in 0.14s ========================
```
(Warnings are an upstream FastAPI `DeprecationWarning` on Python 3.14, unrelated to this code.)

**2. Held-out acceptance suite** — PASS (25/25)

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
acceptance/tier2/test_spec.py::test_post_expense_non_finite_amount_422 PASSED

======================== 25 passed, 5 warnings in 0.15s ========================
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

## Provider stats

Codex CLI printed the following at the end of its run:

```
OpenAI Codex v0.146.0
--------
workdir: /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/xp2
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: medium
reasoning summaries: none
```

```
tokens used
38,243
```

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 52 | 30 | 104 | 102,188 | 1,735,520 | 14,231 | $1.118 |
| **Total** | | | | | | | | **$1.118** |

Wall-clock (main-agent session span): 339s

Note: Sub-agent is OpenAI Codex CLI (gpt-5.6-sol, reasoning effort medium): no Anthropic transcript exists; provider-reported usage is 38,243 tokens (see Provider stats above). No $ estimate for the sub-agent under ChatGPT-subscription auth, so the total above covers the main agent only.

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_a2fd607f-7ba/agent-a69449795009bc175.jsonl`

## Quality scorecard (uniform blind grading pass)

Graded as treeA in a shuffled anonymized batch of 3 (key:
scratchpad/grading-key-xp.txt); grader re-ran all scripted checks on
the anonymized copy (port 8291).

| Metric | Result |
|---|---|
| Acceptance tests passing | 25/25 |
| Own tests passing | 10/10 |
| Critical/functional | 0 |
| Spec-conformance | 0 |
| Minor/style | 2 |
| Smoke | pass |

Minors: (1) templates/expenses.html:27 + expense_detail.html:11 —
category interpolated into filter-link query strings without
URL-encoding (the recurring cross-run minor; roadmap literally
specifies `/expenses?category={category}`, seed data unaffected);
(2) app.py:100-103 — stored fields `.strip()`ed on create (roadmap
silent, no runtime effect).

First run graded against the amended spec letter (25-test suite):
`math.isfinite` + strictly-positive validation present (app.py:82-96),
both `nan` and `inf` asserted in own tests (tests/test_app.py:124-137).
Route `/expenses/new` correctly declared before `/expenses/{expense_id}`.
