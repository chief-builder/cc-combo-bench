# Benchmark plan — agent/subagent/model combo comparison

This project compares Claude Code agent/sub-agent/model combinations
(and cross-provider sub-agents) against fixed specs, captures cost +
quality stats per run, and ends with a comparison + recommendation
across combos.

This file is the authoritative, portable copy of the plan — write it
here (not only in Claude Code memory) because memory is scoped to the
exact project directory path.

Every run pairs a **main agent** (orchestrator: spawns, reviews,
verifies — never writes implementation code) with one or more
**sub-agents** (implementers). All runs build the same apps from the
same specs, so outcome differences come from the configuration, not
the task.

## The specs under test

Three app specs of increasing complexity, each a `mission.md` +
`tech-stack.md` + `roadmap.md` triple on the same stack (FastAPI,
Jinja2, Bootstrap 5, in-memory, no DB, no auth), single-prompt
implementable, verifiable by the same fully scripted process:

| Tier | App | Complexity | Dir |
|---|---|---|---|
| 1 | SpendLog (spending journal) | 1 entity, 3 routes, 1 form, running total; 2 phases | specs/tier1-spendlog |
| 2 | ExpenseHub (expense browser) | detail pages + 404, category filtering with live totals, 422 validation incl. numeric amounts; 3 phases | specs/tier2-expensehub |
| 3 | InvoiceDesk (invoice tracker) | 2 related entities (Invoice+Payment), lifecycle with a money gate (can't mark paid until payments cover the amount), billing stats, JSON API; 4 phases | specs/tier3-invoicedesk |

(Personal-finance family; replaced the original Agent*-themed specs on
2026-08-19 with mechanics mapped 1:1 plus money-math upgrades.)

Each roadmap deliberately plants one-line requirements with classic
footguns as high-signal probes (tier 1: the per-instance timestamp
default; tier 2: `/expenses/new` registered before the int path route;
tiers 1-3: exact two-decimal money lines whose values must be computed,
not pattern-matched). Every behavior a roadmap requires must also
appear in its test list — an omission there reads as an agent miss
when it's really a spec bug.

Suite changelog: 2026-08-25 — the tier-2/3 newest-first sort tests
assumed unique seed client names/titles (independent `find()`
positions), which the roadmaps never require; a run with two seeds
sharing a client name failed the sort test despite a correct sort.
Fixed to a sequential search robust to duplicates; the affected run's
grader re-ran the corrected suite (31/32 → 32/32). Same instrument-bug
class as the 2026-08-20 money-formatter fix: the suite demanded
something the roadmap's letter does not.

Spec changelog: 2026-08-20 — tier-2/3 roadmaps now explicitly require
rejecting non-finite amounts (`nan`/`inf`; check with
`math.isfinite`), with matching test-list bullets and acceptance
tests (tier-2 suite: 25 tests; tier-3: 32). Promoted from a cross-run
observation: 9 of 10 graded tier-2/3 runs let non-finite floats past
"amount > 0" validation (`nan <= 0` is False). Scorecards recorded
before this date graded it as minor under the old letter and stand as
recorded; runs after this date face it as a scored requirement, and
pre/post acceptance denominators differ accordingly.

## Fixed across every combo (the control)

- Same spec (per tier), same clean starting state (a stripped worktree
  of this repo's initial commit).
- Canonical prompts in `prompts/` (see its README for the placeholder
  convention and per-run matrices). Kickoffs are filled mechanically
  and passed verbatim; sub-agent prompt files are provider- and
  model-neutral. Prompts differ across combos only on the axis being
  varied.
- Sub-agents implement; the main agent reviews only, never fixes. The
  in-run review is combo behavior under test; the official scorecard
  comes from the separate blind grading pass.

## Verification — fully scripted, no human relay, ever

1. **Held-out acceptance suite** per tier (`acceptance/tierN/
   test_spec.py`), run as `APP_DIR=<worktree> .venv/bin/pytest
   acceptance/tierN/test_spec.py`. Primary quality metric — agent-
   written tests aren't comparable across runs. Never present in
   worktrees (stripped at creation) or it isn't held out.
2. **Smoke script** per tier (`scripts/smoke_tierN.sh <worktree>
   <port>`), each run on a unique port (parallel runs collide
   otherwise).
3. The implementation's own tests: `cd <worktree> && .venv/bin/python
   -m pytest tests/ -v` (`python -m` puts the worktree on sys.path;
   the bare pytest binary doesn't).

## Quality scorecard (uniform blind grading pass)

Filled after runs complete by a single grader over shuffled anonymized
copies (app.py/models.py/templates/tests only — grader must not count
missing files the copies exclude, e.g. requirements.txt), fixed
checklist derived from each roadmap, all three scripted checks re-run
by the grader. Never by each run's own main agent.

| Metric | How counted |
|---|---|
| Acceptance tests passing | X / N, held-out suite (primary) |
| Own tests passing | X / X (secondary) |
| Critical/functional | runtime behavior wrong |
| Spec-conformance | letter violated, app still works |
| Minor/style | no spec violation or runtime effect |
| Smoke | pass/fail |

Standing uniformity rulings: `field(default_factory=...)` for
timestamp defaults is correct (a `None`+`__post_init__` workaround is
one conformance defect; a plain import-time default is critical);
inert Bootstrap-4-era class names are not counted; the rubric must not
infer test requirements beyond the roadmap's literal test list.

## Cost stats

Per run, appended post-run from real transcripts: turns, tool calls,
four-way token split (fresh in / cache write / cache read / output),
estimated $ at standard per-MTok rates (never intro pricing), exact
model IDs, wall-clock (main-agent session span). Sub-agent transcripts
live in `~/.claude/projects/<worktree-path-slug>/` — one dir per
worktree; per-run cost sums ALL sessions in that dir, so never reuse a
worktree path across runs. Cross-provider sub-agents have no Anthropic
transcript: record provider-reported tokens and model id; no $ under
subscription auth (main-agent $ still applies).

## Execution mechanism (validated)

The `Workflow` tool runs one main agent per run (`agentType:
general-purpose`, model = the combo's main agent). Worktrees are
created BEFORE the run with `scripts/new_worktree.sh <path>` (explicit
`git worktree add --detach` + stripping of PLAN.md, acceptance/,
prompts/, scripts/, results/) — never `isolation: 'worktree'`, whose
path is assigned too late to fill prompts.

- **Sub-agent spawning**: workflow agents have no nested Agent tool;
  the main agent shells out. Claude subs:
  `claude -p --model <alias> --permission-mode acceptEdits
  --allowedTools "Bash" --output-format text` (without the Bash
  allowlist the sub cannot run its own tests). Codex subs:
  `codex exec --full-auto --skip-git-repo-check -` (+
  `-c 'model_reasoning_effort="<e>"'` to vary effort).
- **Spawn hygiene** (each lesson was learned from a real failure):
  prompt temp files via `mktemp` only (shared scratch paths collide
  across parallel runs); spawn exactly once (kill and record any
  accidental duplicate); run the spawn in the FOREGROUND with an
  explicit long timeout — backgrounding + monitors do not survive the
  workflow environment and orphan the sub-agent.
- **venv**: worktrees have no `.venv`; everything uses the main repo's
  venv by absolute path.
- Results files are written to the MAIN repo's `results/`; cost stats
  and blind scorecards are appended post-run.
- **Pilot first**: any new harness element (provider, spawn mechanism,
  tier) gets one pilot run before a matrix.

## Failure/retry policy (decided up front)

- Hard failure = recorded failure, no retry — except one clean re-run
  for harness-caused failures (early-exit orphaning, port/scratch
  collisions, worktree setup), noted in the results file with the
  aborted attempt's cost.
- n=1 per cell is noisy: small deltas are inconclusive; replicate
  decision-relevant cells before ranking on them.

## Results file convention

`results/cc_[tierN_]<main>_<sub(s)>[_repK].md` containing: scope note,
verbatim prompts + exact spawn command, review findings, verification
output, provider stats (cross-provider), then appended cost stats and
blind scorecard, and source transcript paths.

## Run matrices

See `prompts/README.md` for the canonical matrices (round 1: spawn
strategy × sub-agent model under a Sonnet 5 main; round 2: main-agent
model; tier scaling; axis-cross; cross-provider XP; Codex effort
sweep), with per-run ports and results filenames. All cells are
PENDING on this clean bench — prior executions were archived and
removed (see History).

## Cross-provider status

- **Codex CLI**: ready (ChatGPT auth). Model is pinned to its default
  under subscription auth — every alternative `--model` returns 400; a
  true model sweep needs `OPENAI_API_KEY`. Reasoning effort IS
  sweepable via `-c model_reasoning_effort`.
- **opencode**: installed, zero credentials — needs an interactive
  `opencode auth login` before it can be a sub-agent.
- **Local models**: blocked until an agentic wrapper (e.g. Ollama +
  aider) is installed — a bare LLM CLI can't write files.

## Final deliverable

`results/comparison-all.md` once cells are run — cross-run table (cost
+ quality), cost-vs-quality view, per-use-case recommendation, honest
caveats (n per cell, re-runs, pricing basis, grading provenance).

## History

Methodology v2 was developed here through a full 31-run campaign
(2026-08-18/19) plus its predecessor in the sibling `agent-complaints`
project. That campaign's repo history, results, and reports were
archived to `../cc-combo-bench-history-20260819.bundle` and removed
for a clean bench; every harness lesson it produced is folded into the
sections above. The published "Combo Bench" artifact still documents
that campaign.
