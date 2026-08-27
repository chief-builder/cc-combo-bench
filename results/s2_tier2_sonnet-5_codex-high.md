# s2 / tier2-expensehub / sonnet-5 (main) + codex-high (sub-agent)

## Prompts used

**Spawn command:**

```
cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-12 && codex exec --full-auto --skip-git-repo-check -c 'model_reasoning_effort="high"' - < <tmpfile>
```

(tmpfile was created via `mktemp` in the scratchpad and passed verbatim.)

**Sub-agent prompt (verbatim):**

```
Implement the app specified in /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-12/specs/tier2-expensehub/. Work only
inside /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-12 — create every file there, never in any other
directory. Read mission.md, tech-stack.md, and roadmap.md, then implement
ALL phases of the roadmap exactly as written — file names, routes, status
codes, defaults, CDN links, and template contents are requirements, not
suggestions.

- Use the virtual environment at /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv for everything you
  run.
- Write the tests the roadmap calls for and run them with
  `cd /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench-worktrees/s2-12 && /Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/.venv/bin/python -m pytest tests/ -v`
  until they pass.
- Do not start a long-running server; the tests use TestClient.
- Do not add features, files, or dependencies the roadmap doesn't ask for.
- When finished, reply with a brief summary: the files you created and the
  final test output.
```

## Review findings

### Critical / functional
None found. `app.py` and `models.py` implement all three roadmap phases correctly: routes (`/`, `/expenses`, `/expenses/{id}`, `GET /expenses/new`, `POST /expenses`), 404 handling for unknown ids, category filtering with correctly recomputed totals, and the money-validation rules (non-empty strip checks, `float()` parse failure, `<= 0`, and `math.isfinite` rejecting `nan`/`inf`/`-inf`) all match the spec (`app.py:68-101`, `models.py:65-70`).

### Spec-conformance
None found. Checked against roadmap line items:
- `templates/base.html:1-27` — doctype, `lang="en"`, viewport, Bootstrap 5 CSS CDN, favicon link to `https://www.python.org/static/favicon.ico`, navbar with Home/Expenses links, `{% block content %}`, Bootstrap JS bundle at bottom — all present.
- `templates/home.html` — tagline "Know where it all goes." present.
- `templates/expenses.html:18` — `Total: $X.XX` line present via `"%.2f"|format(total)`; category badges are links to `/expenses?category={category}` (`expenses.html:31`); heading swaps to `Expenses in "{category}"` with a "Show all" link when filtered (`expenses.html:8-13`).
- `templates/expense_detail.html` — title, payee, formatted `spent_at`, amount, category badge link, notes, and "Back to expenses" link all present.
- `templates/expense_new.html` — `is-invalid` class and `invalid-feedback` div per field, values preserved including raw amount text, form posts to `/expenses`.
- `models.py:16-62` — 5 seed expenses, ids 1..5, 3 distinct categories (`food`, `transport`, `software`), realistic cent amounts.
- `app.py:116-117` — `if __name__ == "__main__": uvicorn.run("app:app", reload=True)` present.
- `requirements.txt`/`requirements.lock` untouched — no new dependencies added, consistent with tech-stack.md.

### Minor / style / process
- **Out-of-scope destructive change (process anomaly, not a code defect):** the sub-agent's git worktree at `s2-12` had 55 tracked repository-infrastructure files deleted from its working tree — `PLAN.md`, all three `acceptance/tier*/test_spec.py` files, all `prompts/*.md`, all `results/*.md`, and all `scripts/*.sh` (confirmed via `git status`/`git diff --stat` in the worktree: "55 files changed, 8998 deletions(-)"). These are files the roadmap never mentioned and the prompt never asked to touch. This did **not** affect verification because the acceptance suite and smoke script are invoked against the main repo's copies (`/Users/chiefbuilder/Documents/Projects/cloud_to_local_course/cc-combo-bench/...`), which were confirmed intact and untouched. Still, this is unexplained destructive behavior on tracked files outside the sub-agent's assigned scope and is worth flagging.
- `expense_new.html` includes an `{% if errors.notes %}` branch (`expense_new.html:36`) even though `notes` can never carry a validation error per the roadmap (notes is optional). Harmless dead branch, not a defect.

## Verification

All three checks passed.

**1. Implementation's own tests** — PASS (11/11)
```
tests/test_app.py::test_home_page PASSED
tests/test_app.py::test_expense_list PASSED
tests/test_app.py::test_expense_detail PASSED
tests/test_app.py::test_unknown_expense_returns_404 PASSED
tests/test_app.py::test_category_filter PASSED
tests/test_app.py::test_create_expense PASSED
tests/test_app.py::test_empty_title_returns_422_and_preserves_notes PASSED
tests/test_app.py::test_non_numeric_amount_returns_422_and_preserves_raw_amount PASSED
tests/test_app.py::test_negative_amount_returns_422 PASSED
tests/test_app.py::test_non_finite_amount_returns_422[nan] PASSED
tests/test_app.py::test_non_finite_amount_returns_422[inf] PASSED
======================== 11 passed, 5 warnings in 0.13s ========================
```

**2. Held-out acceptance suite** — PASS (25/25)
```
======================== 25 passed, 5 warnings in 0.14s ========================
```
(All 25 tests in `acceptance/tier2/test_spec.py` passed, covering base layout, dataclass fields, seed data, helper functions, list/detail/filter pages, form rendering, and all validation edge cases.)

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

```
tokens used
33,560
```

(From the codex CLI header: `model: gpt-5.6-sol`, `provider: openai`, `reasoning effort: high`, `reasoning summaries: none`, `sandbox: workspace-write [workdir, /tmp, $TMPDIR]`.)

## Cost stats (added post-run from session transcripts)

Pricing basis: standard per-MTok rates (Sonnet 5 $3 in / $15 out; Opus 5 $5 / $25;
Haiku 4.5 $1 / $5); cache write billed at 1.25x input rate, cache read at 0.1x.
Sonnet 5 has intro pricing ($2 / $10) through 2026-08-31; standard rates are used
here for long-run comparability.

| Role | Model | Turns | Tool calls | Fresh in | Cache write | Cache read | Output | Est. $ |
|---|---|---|---|---|---|---|---|---|
| Main agent | claude-sonnet-5 | 40 | 23 | 80 | 93,734 | 1,315,375 | 8,977 | $0.881 |
| **Total** | | | | | | | | **$0.881** |

Wall-clock (main-agent session span): 284s

Note: Sub-agent is OpenAI Codex CLI (gpt-5.6-sol, reasoning effort high): no Anthropic transcript exists; provider-reported usage is 33,560 tokens. No $ estimate for the sub-agent under ChatGPT-subscription auth, so the total covers the main agent only.

## Source transcripts

- Main agent: `/Users/chiefbuilder/.claude/projects/-Users-chiefbuilder-Documents-Projects-cloud-to-local-course-cc-combo-bench/1cd203d2-4e3b-44ad-94a1-90213d51bbbf/subagents/workflows/wf_b5fd4a3a-a70/agent-a1e72e56511320e86.jsonl`


## Quality scorecard (uniform blind grading pass)

Graded in a shuffled anonymized batch of 12 (key: scratchpad/grading-key-s2.txt)
by three parallel graders (trees A-D / E-H / I-L), all scripted checks re-run
on the anonymized copies. Standing rubric rulings applied uniformly (see
PLAN.md and prior scorecards).

Graded as treeE (port 8905).

| Metric | Result |
|---|---|
| Acceptance tests passing | 25/25 |
| Own tests passing | 11/11 |
| Critical/functional | 0 |
| Spec-conformance | 0 |
| Minor/style | 2 |
| Smoke | pass |

Minors: un-URL-encoded category links ×2 — notably, Season 1's Codex-high t2 draw was the only tree ever to URL-encode them; this draw did not. That behavior is draw variance, not a stable model trait.
