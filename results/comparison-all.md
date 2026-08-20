# Combo comparison — finance campaign: rounds 1-2, replicates, tiers, axis-cross

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

## Replicates — the clean pair, second draws

| Cell | Run | Acceptance | Crit | Conf | Minor | Est. $ | Wall-clock |
|---|---|---|---|---|---|---|---|
| single Opus 5 | original | 16/16 | 0 | **0** | **0** | $1.41 | 199s |
| | replicate | 16/16 | 0 | **0** | **0** | $1.76 | 156s |
| Sonnet 5 ×2 per-phase | original | 16/16 | 0 | **0** | **0** | $1.79 | 269s |
| | replicate | 16/16 | 0 | 1 | 0 | $1.52 | 174s |

- **Single Opus 5 is the campaign's first cell fully clean at n=2** —
  0/0/0 both draws, fastest both draws (199s, 156s), $1.41-$1.76.
- **Per-phase Sonnet 5 is near-clean at n=2**: full acceptance and
  defect-free application code in both draws; the replicate's one
  blemish is the recurring weak-test class (a 303 asserted without its
  redirect target) — test quality, not app quality.
- Verdict on the round-1 close call: at this tier the two are
  effectively tied on app correctness; Opus is faster and its record
  is spotless, Sonnet's costs overlap Opus's band. Pick Opus for
  single-shot speed + cleanliness, per-phase Sonnet if the phase
  structure matters downstream (it was the higher-tier consistency
  pick last campaign).

## Round 2 — the main-agent axis (tier 1, single Sonnet 5 sub)

| Main agent | Acceptance | Crit | Conf | Minor | Est. $ | Wall-clock |
|---|---|---|---|---|---|---|
| **Haiku 4.5** | 16/16 | 0 | **0** | **0** | **$0.66** | **169s** |
| Sonnet 5 (r1 combo 1 ref) | 15/16 | 1 | 1 | 1 | $1.00 | 229s |
| Opus 5 | 16/16 | 0 | **0** | **0** | $1.63 | 186s |

**The Haiku-main headline replicates on a second domain**: cheapest
(beating even the prior campaign's $0.73), fastest, and blind-graded
fully clean — while the Sonnet-main reference draw happened to be the
one that shipped the frozen-timestamp critical. Both round-2 mains
produced 0/0/0 runs: the orchestrator-is-overhead finding now holds
across two campaigns and two domains at tier 1.

## Tier scaling — round-1 leaders on ExpenseHub and InvoiceDesk

| Run | Tier | Acceptance | Crit | Conf | Minor | Est. $ | Wall-clock |
|---|---|---|---|---|---|---|---|
| single Opus 5 | 2 | 24/24 | 0 | **0** | 2 | $2.17 | 278s |
| Sonnet 5 ×3 per-phase | 2 | 24/24 | 0 | **0** | 2 | $3.27 | 350s |
| single Opus 5 | 3 | 31/31 | 0 | **0** | 1 | $3.24 | 315s |
| — replicate | 3 | 31/31 | 0 | **0** | 1 | $3.41 | 306s |
| Sonnet 5 ×4 per-phase | 3 | **30/31** | **1** | 0 | 0 | $5.01 | 540s |
| — replicate | 3 | **30/31** | **1** | 0 | 4 | $5.15 | 522s |

- **Single Opus 5 held clean at every tier** — 16/16, 24/24, 31/31,
  zero critical/conformance defects across the whole campaign, at
  roughly two-thirds of per-phase Sonnet's cost and much better
  wall-clock. The campaign's correctness pick, decisively.
- **The route-order trap bit per-phase Sonnet at tier 3 — implicitly,
  and now 2-for-2.** Tier 2's explicit `/expenses/new` plant was
  dodged by everyone, but at tier 3 the same class arose *across
  phases*: phase 2 registers the int path route, phase 3 appends
  `/invoices/new` after it, and the form page 422s at runtime. The
  replicate reproduced the identical critical (both draws 30/31), the
  in-run per-phase reviews missed it both times, and the sub-agents'
  own tests never hit the route either time. At n=2 this is a
  systematic per-phase failure mode, not variance: phase handoffs
  create integration seams no single sub-agent sees, and code review
  without execution misses route-registration bugs. Single Opus,
  seeing the whole app at once, ordered the routes correctly in both
  draws (31/31 twice, ~$3.3 vs per-phase's ~$5.1, ~40% faster).
- **The new numeric canary registered across the board, as minors**:
  6 of 6 tier-2/3 runs (replicates included) let `nan`/`inf` past
  their positive-amount validation (`nan <= 0` is False — a single
  tree in the campaign guarded with `math.isfinite`), and both tier-2
  runs shipped un-URL-encoded category links. Outside the roadmap's
  letter (hence minor), but a consistent, teachable blind spot:
  agents validate the happy path of "a number", not the pathological
  floats.
- **Instrument note**: the tier-3 in-run acceptance counts (29/31,
  28/31) each included failures from a suite bug — the `money()`
  helper demanded thousands separators the roadmap never specified
  (invisible at tiers 1-2 where amounts stay under $1,000). Fixed in
  commit `0df5f2c` before grading; the grader re-ran the corrected
  suite. Second campaign in a row where a cross-run "failure" pattern
  audit found the instrument, not the agents — audit the spec/suite
  whenever a miss goes cross-configuration.

## Axis-cross — Haiku main over the leaders at tiers 2-3

| Run | Tier | Acceptance | Crit | Conf | Minor | Est. $ | vs Sonnet main | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| Haiku main + single Opus | 2 | 24/24 | 0 | **0** | 2 | **$1.21** | −44% ($2.17) | 223s |
| Haiku main + Sonnet ×3 | 2 | 24/24 | 0 | **0** | 2 | $2.26 | −31% ($3.27) | 370s |
| Haiku main + single Opus | 3 | 31/31 | 0 | **0** | 2 | **$1.85** | −45% (~$3.3) | 302s |
| Haiku main + Sonnet ×4 | 3 | **29/31** | **3** | 0 | 4 | $3.70 | −27% (~$5.1) | 589s |

- **Cheap orchestration survives multi-phase on this domain too.** The
  Haiku main managed every spawn (1, 3, 1, 4) exactly once with no
  anomalies, and quality tracked the *sub-agent*, not the orchestrator:
  Opus subs stayed perfect at both tiers, at 44-45% below the
  Sonnet-main equivalents. **Haiku main + single Opus is the campaign's
  best cost-quality point at every tier** ($1.21 t2, $1.85 t3, clean).
- **The per-phase tier-3 route-ordering critical is now 3-for-3**
  across two different orchestrators (two Sonnet mains, one Haiku
  main) — orchestrator-independent, definitively a property of the
  per-phase strategy meeting this spec shape. This draw compounded it
  with plain import-time timestamp defaults on *both* dataclasses (two
  C2 criticals) — per-phase Sonnet's worst tier-3 showing of the
  campaign.
- The NaN-past-validation minor is now present in 9 of 10 graded
  tier-2/3 runs.

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

- n = 1 per cell except combos 2 and 5 (both n=2, see Replicates).
  The prior campaign showed cell-level results (esp. who trips the
  canary) swing between draws — replicate before ranking on
  single-defect margins.
- Grading is blind and checklist-driven but performed by the same
  model family being benchmarked; scripted checks are re-run by the
  grader as mitigation.
- Sonnet 5 intro pricing not applied; standard rates throughout.

## Next steps

1. Cross-provider: Codex (ready) and opencode (needs `opencode auth
   login`).
2. Consider promoting the NaN/Infinity guard to the roadmaps' letter
   (currently a consistent cross-run minor) if it should discriminate
   rather than lurk.
