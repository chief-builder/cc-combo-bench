# Canonical prompts

These are the exact prompt texts for every combo run, per PLAN.md: prompt
wording must never be a confound, so it is fixed here and passed verbatim —
the main agent is instructed to hand the sub-agent prompt over unchanged,
never to write its own.

In each file, everything below the `---` line is the prompt; everything
above it is meta and is not part of the prompt.

## Placeholders

Fill mechanically (find-and-replace) before use. The filled text must be
identical across combos except `{{SUBAGENT_MODEL}}` — that is the axis
being varied.

| Placeholder | Value |
|---|---|
| `{{SUBAGENT_MODEL}}` | sub-agent model for the combo (see matrix below) |
| `{{WORKTREE}}` | absolute path of the combo's worktree |
| `{{MAIN_REPO}}` | absolute path of this repo |
| `{{SPEC_DIR}}` | spec dir, relative to the worktree (per tier, below) |
| `{{ACCEPTANCE_SUITE}}` | acceptance suite path, relative to `{{MAIN_REPO}}` |
| `{{SMOKE_SCRIPT}}` | smoke script path, relative to `{{MAIN_REPO}}` |
| `{{PORT}}` | the combo's unique port (see matrix below) |
| `{{RESULTS_FILE}}` | the combo's results filename (see matrix below) |
| `{{NUM_PHASES}}` | kickoff-per-phase-multi.md only: the spec's phase count |

`{{PHASE}}` / `{{PREV_PHASE}}` in subagent-phase-later.md are NOT part of
this fill — the main agent fills them per phase at run time.

## Per-tier values

| Tier | `{{SPEC_DIR}}` | `{{ACCEPTANCE_SUITE}}` | `{{SMOKE_SCRIPT}}` |
|---|---|---|---|
| 1 | specs/tier1-spendlog | acceptance/tier1/test_spec.py | scripts/smoke_tier1.sh |
| 2 | specs/tier2-expensehub | acceptance/tier2/test_spec.py | scripts/smoke_tier2.sh |
| 3 | specs/tier3-invoicedesk | acceptance/tier3/test_spec.py | scripts/smoke_tier3.sh |

## Round-1 combo matrix (tier 1)

| # | Kickoff file | Sub-agent prompt file(s) | `{{SUBAGENT_MODEL}}` | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|---|
| 1 | kickoff-single.md | subagent-both-phases.md | sonnet | 8101 | cc_sonnet-5_sonnet-5.md |
| 2 | kickoff-per-phase.md | subagent-phase1.md, subagent-phase2.md | sonnet | 8102 | cc_sonnet-5_sonnet-5x2.md |
| 3 | kickoff-per-phase.md | subagent-phase1.md, subagent-phase2.md | haiku | 8103 | cc_sonnet-5_haiku-4.5x2.md |
| 4 | kickoff-single.md | subagent-both-phases.md | haiku | 8104 | cc_sonnet-5_haiku-4.5.md |
| 5 | kickoff-single.md | subagent-both-phases.md | opus | 8105 | cc_sonnet-5_opus-5.md |
| 6 | kickoff-per-phase.md | subagent-phase1.md, subagent-phase2.md | opus | 8106 | cc_sonnet-5_opus-5x2.md |

The two-phase files (kickoff-per-phase.md, subagent-phase1.md,
subagent-phase2.md) are tier 1's and stay frozen for round-to-round
comparability. Specs with 3+ phases (tier 2: 3, tier 3: 4) use
kickoff-per-phase-multi.md + subagent-phase1.md +
subagent-phase-later.md instead.

Prompt-wording history: after round 1, the kickoffs gained the
mktemp-unique-temp-file sentence (round 1's parallel batch collided on
shared scratch paths) — round-1 results files record the exact text
their runs used, so the delta is auditable.

## Round-2 matrix (tier 1 — vary MAIN agent, sub-agent fixed at single Sonnet 5)

Round 1's combo 1 (Sonnet 5 main) is the reference point on this axis.

| Run | Kickoff | Main agent | `{{SUBAGENT_MODEL}}` | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|---|
| R2-haiku | kickoff-single.md | Haiku 4.5 | sonnet | 8107 | cc_haiku-4.5_sonnet-5.md |
| R2-opus | kickoff-single.md | Opus 5 | sonnet | 8108 | cc_opus-5_sonnet-5.md |

## Cross-provider runs (main agent Sonnet 5, non-Anthropic sub-agents)

Uses kickoff-single-xp.md; the sub-agent prompt files are unchanged
(provider-neutral — that is the control). `{{SUBAGENT_CLI}}` values:

| Provider | `{{SUBAGENT_CLI}}` |
|---|---|
| OpenAI Codex CLI | `codex exec --full-auto --skip-git-repo-check -` |
| opencode | (candidate — command TBD when its provider config is verified) |

| Run | Tier | Sub-agent | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|
| XP1 | 1 | Codex CLI (gpt-5.6-sol recorded) | 8171 | cc_sonnet-5_codex.md |
| XP2 | 2 | Codex CLI | 8181 | cc_tier2_sonnet-5_codex.md |
| XP3 | 3 | Codex CLI | 8182 | cc_tier3_sonnet-5_codex.md |

Effort sweep (same model; `-c 'model_reasoning_effort="<e>"'` added to
`{{SUBAGENT_CLI}}`; medium = the XP runs above). A model sweep is
blocked under ChatGPT-subscription auth — all alternative `--model`
values return 400; it needs OPENAI_API_KEY auth.

| Run | Tier | Effort | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|
| XE-low-t1 | 1 | low | 8201 | cc_sonnet-5_codex-low.md |
| XE-low-t2 | 2 | low | 8202 | cc_tier2_sonnet-5_codex-low.md |
| XE-low-t3 | 3 | low | 8203 | cc_tier3_sonnet-5_codex-low.md |
| XE-high-t1 | 1 | high | 8204 | cc_sonnet-5_codex-high.md |
| XE-high-t2 | 2 | high | 8205 | cc_tier2_sonnet-5_codex-high.md |
| XE-high-t3 | 3 | high | 8206 | cc_tier3_sonnet-5_codex-high.md |

Cross-provider stats schema (no Anthropic transcripts for the sub):
wall-clock, provider-reported token usage (stdout / provider session
logs under ~/.codex/sessions/), and the provider's model id. No $
estimate under subscription (ChatGPT-login) auth — noted per run. Main
agent stats still come from its own transcript as usual.

## Axis-crossing runs (main agent Haiku 4.5)

| Run | Tier | Kickoff | `{{SUBAGENT_MODEL}}` | `{{NUM_PHASES}}` | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|---|---|
| X1 | 1 | kickoff-single.md | haiku | — | 8151 | cc_haiku-4.5_haiku-4.5.md |
| X2 | 2 | kickoff-per-phase-multi.md | sonnet | 3 | 8152 | cc_tier2_haiku-4.5_sonnet-5x3.md |
| X3 | 3 | kickoff-per-phase-multi.md | sonnet | 4 | 8153 | cc_tier3_haiku-4.5_sonnet-5x4.md |

X1 probes the cheapest corner; X2/X3 test whether the cheap
orchestrator survives multi-phase orchestration (3-4 spawns plus
per-phase reviews) over the consistency-pick sub-agent.

## Tier-2/3 runs (round-1 leaders, main agent Sonnet 5)

| Run | Tier | Kickoff | `{{SUBAGENT_MODEL}}` | `{{NUM_PHASES}}` | `{{PORT}}` | `{{RESULTS_FILE}}` |
|---|---|---|---|---|---|---|
| T2-haiku | 2 | kickoff-single.md | haiku | — | 8121 | cc_tier2_sonnet-5_haiku-4.5.md |
| T2-sonnet | 2 | kickoff-per-phase-multi.md | sonnet | 3 | 8122 | cc_tier2_sonnet-5_sonnet-5x3.md |
| T3-haiku | 3 | kickoff-single.md | haiku | — | 8131 | cc_tier3_sonnet-5_haiku-4.5.md |
| T3-sonnet | 3 | kickoff-per-phase-multi.md | sonnet | 4 | 8132 | cc_tier3_sonnet-5_sonnet-5x4.md |

`{{SUBAGENT_MODEL}}` is the claude CLI model alias (`sonnet` / `haiku`
/ `opus`): the kickoff prescribes the exact spawn command (`claude -p
--model {{SUBAGENT_MODEL}} --permission-mode acceptEdits --allowedTools
"Bash" ...`, run from the worktree), per the 2026-08-18 pilot — main
agents have no nested Agent tool, and without the Bash allowlist the
sub-agent cannot run its own tests. The sub-agent prompt files contain
no model reference, so their text is byte-identical across all combos
of the same spawn strategy.

Worktrees are created with `scripts/new_worktree.sh <path>`, which
strips PLAN.md, acceptance/, prompts/, scripts/, and results/ so the
sub-agent cannot read the held-out suite or these prompts.
