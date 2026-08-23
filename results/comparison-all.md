# Combo comparison — finance campaign: rounds 1-2, replicates, tiers, axis-cross, cross-provider, effort sweep

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
| Haiku main + single Opus — rep2, post-amendment | 2 | 25/25 | 0 | **0** | 2 | $1.61 | — | 188s |
| Haiku main + single Opus — rep2, post-amendment | 3 | 32/32 | 0 | **0** | 1 | $2.44 | — | 295s |

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
  tier-2/3 runs — all pre-amendment.
- **The post-amendment replicates (2026-08-20, suites 25/32) answered
  the amendment question for Claude**: both Opus subs wrote
  `math.isfinite` (t2 app.py:75; t3 at both validation points) and
  asserted `nan`/`inf`/`-inf` in their own tests — the blind spot is
  closed by an explicit spec bullet, for Claude exactly as for Codex.
  Both draws blind-graded clean (0 critical / 0 conformance), making
  **Haiku main + single Opus clean at n=2 at both tiers 2 and 3**.
  Post-amendment costs ($1.61 t2, $2.44 t3) sit above the original
  draws ($1.21, $1.85) — the amended roadmaps are slightly longer and
  draws vary — but still ~26-31% below the Sonnet-main equivalents.
  The recurring un-URL-encoded category-link minor recurred at tier 2
  (now 4-for-4 across models and providers).

## Cross-provider — Codex CLI as the implementer (Sonnet 5 main)

Single Codex sub-agent (OpenAI Codex CLI, gpt-5.6-sol, medium effort)
under a Sonnet 5 main, all three tiers (XP1 pilot first, then XP2/XP3
in parallel). Same provider-neutral sub-agent prompts — that
neutrality is the control.

| Run | Tier | Acceptance | Crit | Conf | Minor | Main-agent $ | Codex tokens | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| XP1 | 1 | 16/16 | 0 | **0** | 1 | $0.73 | 26,339 | 200s |
| XP2 | 2 | 25/25 | 0 | **0** | 2 | $1.12 | 38,243 | 339s |
| XP3 | 3 | 32/32 | 0 | **0** | 2 | $1.39 | 56,992 | 870s |

- **The campaign's first perfect cross-tier sweep**: full acceptance
  and zero critical/conformance defects at all three tiers in one
  batch, with only 5 minors total. Every canary was dodged —
  `default_factory` timestamps, route ordering, exact money lines,
  consistent money-gate seed data.
- **These are the first runs graded against the amended spec letter**
  (non-finite amounts; tier-2 suite now 25 tests, tier-3 32) — and
  Codex wrote the `math.isfinite` guard at both tiers and asserted
  `nan`/`inf` in its own tests. The explicit bullet works; whether
  Claude subs also pick it up post-amendment is the natural next
  replicate.
- The recurring un-URL-encoded category-link minor reappeared at tier
  2 — cross-provider now, so it is a spec-shape blind spot, not a
  model family trait.
- **Cost caveat**: XP $ totals cover the Sonnet 5 main agent only —
  Codex ran under ChatGPT-subscription auth, which reports tokens
  (26k/38k/57k) but no price. Not comparable to the all-Anthropic
  totals; the honest comparison is quality + wall-clock. Tier-3
  wall-clock (870s) was the campaign's slowest run despite the clean
  result.
- **Harness note**: both the XP2 and XP3 main agents noticed the
  intentional worktree strip, checked the Codex transcript, and
  correctly reported it as pre-existing rather than blaming the
  sub-agent — the first campaign in three where no main agent
  produced the strip false positive.

## Codex effort sweep — low/high vs the medium XP runs

Same harness and model (Codex CLI, gpt-5.6-sol, single sub under a
Sonnet 5 main), reasoning effort varied via
`-c 'model_reasoning_effort="<e>"'`. Six runs (2026-08-23), all against
the amended specs. Main-agent $ only, as with all Codex cells.

| Effort | Tier | Acceptance | Crit | Conf | Minor | Codex tokens | Main $ | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| low | 1 | 16/16 | 0 | **0** | 0 | 23,464 | $0.87 | 181s |
| low | 2 | **24/25** | **1** | 1 | 1 | 22,942 | $0.63 | 215s |
| low | 3 | 32/32 | 0 | 3 | 1 | 33,593 | $0.99 | 298s |
| medium (XP) | 1 | 16/16 | 0 | **0** | 1 | 26,339 | $0.73 | 200s |
| medium (XP) | 2 | 25/25 | 0 | **0** | 2 | 38,243 | $1.12 | 339s |
| medium (XP) | 3 | 32/32 | 0 | **0** | 2 | 56,992 | $1.39 | 870s |
| high | 1 | 16/16 | 0 | **0** | 0 | 33,529 | $0.85 | 255s |
| high | 2 | 25/25 | 0 | **0** | 0 | 29,176 | $1.18 | 297s |
| high | 3 | 32/32 | 0 | **0** | 0 | 52,045 | $1.17 | 375s |

- **High effort swept spotless**: 0 defects of any kind at all three
  tiers — the campaign's first 0/0/0 sweep — and its tier-2 tree was
  the **first in the campaign to URL-encode the category links**,
  closing the blind spot that was 4-for-4 across models and providers.
- **Low effort degrades tier-sensitively, and in an instructive shape**:
  clean at tier 1; at tier 2 it shipped the plain import-time timestamp
  default (the canary's worst variant — the first time it caught Codex,
  and the sweep's only acceptance failure) plus a required-notes
  conformance; at tier 3 the app code was fully conformant but the test
  suite compressed to 7 broad functions and dropped two roadmap-listed
  assertions (weak-test conformance ×2, plus the required-note ruling).
  Effort buys canary-dodging and test rigor, not basic capability.
- **The amended spec letter held at every effort level**:
  `math.isfinite` present in all four tier-2/3 trees, including both
  low-effort ones. Explicit bullets survive effort reduction; unwritten
  expectations are what low effort trips on — the sharpest form of the
  campaign's spec-writing lesson.
- Token spend did not scale monotonically (low t2 22.9k < high t2
  29.2k < medium t2 38.2k); medium's tier-3 870s wall-clock remains
  the campaign's slowest, with high at 375s — effort and latency are
  not the same axis.
- Grading provenance: two parallel graders (trees A-C / D-F) after the
  single grader stalled twice on infra watchdog errors; standing
  uniformity rulings applied across both (see per-run scorecards).

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

1. opencode as a second cross-provider sub-agent (blocked on an
   interactive `opencode auth login`).
2. ~~Codex effort sweep~~ — done 2026-08-23 (see Effort sweep); a true
   Codex model sweep still needs `OPENAI_API_KEY`.
3. DeepSeek as a sub-agent via Claude Code + DeepSeek's
   Anthropic-compatible endpoint (isolates the model axis with the
   harness held constant; restores real $ for a non-Anthropic sub) —
   blocked on `DEEPSEEK_API_KEY`.
3. ~~Post-amendment Claude replicates at tiers 2-3~~ — done
   2026-08-20: the explicit bullet fixed the blind spot for Claude
   subs at both tiers (see Axis-cross).
