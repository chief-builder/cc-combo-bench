# Combo comparison — SpendLog campaign, round 1

Round 1 on the personal-finance specs (2026-08-20): spawn strategy ×
sub-agent model, main agent held at Sonnet 5, tier-1 SpendLog. Quality
numbers are the official blind-graded ones (single grader, shuffled
anonymized trees, fixed checklist, all scripted checks re-run);
per-run detail in each `cc_*.md`. $ at standard per-MTok rates;
wall-clock = main-agent session span. Defect columns: Crit = runtime
behavior wrong; Conf = letter violated, app works; Minor = style only.

## Round 1 — spawn strategy × sub-agent model (tier 1, Sonnet 5 main)

| # | Combo | Acceptance | Own | Crit | Conf | Minor | Est. $ | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| 1 | single Sonnet 5 | **15/16** | 4/4 | **1** | 1 | 1 | $1.00 | 229s |
| 2 | Sonnet 5 ×2 per-phase | 16/16 | 4/4 | 0 | **0** | **0** | $1.79 | 269s |
| 3 | Haiku 4.5 ×2 per-phase | 16/16 | 8/8 | 0 | 2 | 1 | $1.30 | 291s |
| 4 | single Haiku 4.5 | **15/16** | 8/8 | 0 | 1 | 2 | **$1.02** | 273s |
| 5 | single Opus 5 | 16/16 | 4/4 | 0 | **0** | **0** | $1.41 | **199s** |
| 6 | Opus 5 ×2 per-phase | 16/16 | 5/5 | 0 | 1 | 0 | $2.06 | 270s |

All smoke checks pass. Zero harness anomalies (the foreground-spawn
and mktemp hardening, applied from run one this campaign, held).

## Findings

- **Two fully clean scorecards in the opening round** — per-phase
  Sonnet 5 (combo 2) and single Opus 5 (combo 5). Per-phase Sonnet
  repeating as the conformance-clean configuration matches the prior
  campaign's "correctness pick"; single Opus improved on its prior
  showing (and was this round's fastest).
- **The timestamp canary transferred to the new domain — and caught a
  different model.** Single Sonnet shipped the *worst* variant (a plain
  import-time default: every entry shares one frozen timestamp — the
  round's only critical defect), while single Haiku repeated its
  familiar `None` + `__post_init__` conformance miss. The canary is
  model-agnostic bait; who bites is run-to-run variance.
- **The weak-test pattern reappeared in new clothes**: redirect tests
  that assert the 303 but never the target (combos 3, 6), and an
  after-POST test that never asserts the updated total (combo 3). The
  airtight test lists in the new roadmaps make these unambiguous
  agent misses, not spec gaps — the money-line assertions are doing
  their job.
- **The in-run-review false positive recurred and was neutralized
  again**: combo 4's main agent blamed the intentional worktree strip
  on its sub-agent. The blind pass (implementation-only copies) is the
  established antidote.
- Cost order this round: single Sonnet/Haiku cheapest (~$1.00), then
  per-phase Haiku, single Opus, per-phase Sonnet, per-phase Opus most
  expensive ($2.06).

## Caveats

- n = 1 per cell. The prior campaign showed cell-level results (esp.
  who trips the canary) swing between draws — replicate before ranking
  on single-defect margins. The decision-relevant close call this
  round: combo 2 vs combo 5 (both clean; $1.79/269s vs $1.41/199s).
- Grading is blind and checklist-driven but performed by the same
  model family being benchmarked; scripted checks are re-run by the
  grader as mitigation.
- Sonnet 5 intro pricing not applied; standard rates throughout.

## Next steps

1. Replicate combos 2 and 5 (the clean pair) if the ranking is to be
   acted on.
2. Round 2 (main-agent axis) and tier scaling (ExpenseHub /
   InvoiceDesk) per PLAN.md — the tier-2 numeric-validation and tier-3
   money-gate canaries are still unexercised.
3. Cross-provider: Codex (ready) and opencode (needs `opencode auth
   login`).
