**DEFECTS FOUND** (bookkeeping, not claim-level) — I attacked the two author verdicts and the round-40
owned-axis numbers, then drafted the two surfaces that carry them. C1 `3/4` **NOT MET** and C2 `26/26`
**MET** both reproduce from the committed receipts; the defects are that the landed C1 numbers hold only
at `42c10a58` (no later round-40 revision satisfies the frozen C1 documentation clauses, and the
supplementary gate's `frontier_content` also goes false at the demotion), and that the lane's
`SKILL.md` carried an uncommitted `+19`-line edit at measurement time. I wrote no lane file outside my
artifacts.

# R40W2Scorecard — round 40 wave 2 scribe

Seat: scorecard/log scribe. Deliverables: the `SCORECARD.md` `## Round 40` section and the `LOG.md`
round-40 entry as drafts under `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/`. I did not edit
`SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/`, `tools/` or `plans/`.

## What I measured, and what I only read

I did **not** re-run `c1-counter.py`, `c1-extra.py` or `c2-counter.py`; every claim number below is
quoted from their committed scores/receipts in `.ufo/waves/round-40/l1/scores/`. What I executed myself
is the owned-axis recipe (command A, `SCORECARD.md:92-124`, unmodified), the frozen v2 interpreter
against the base `SKILL.md`, and two document-condition evaluations against `PROVINCE.md` bytes at two
revisions. All reads are Git objects or committed files; no VCS mutation.

## Commands and outcomes (exact)

1. **Command A** (the recipe at `SCORECARD.md:92-124`, `REV` varied, cwd = lane, `cd` inside the lane;
   output `artifacts/R40W2Scorecard/cmdA.txt`):

   | REV | knowledge files | mapped | missing | dangling | rule blocks | resolved | cov / depth |
   |---|---|---|---|---|---|---|---|
   | `fa6a8a3f…` (base) | 128 | 128 | `[]` | `[]` | 18 | 18 | 10.0 / 10.0 |
   | `52b0eb29…` (round-39 tip) | 128 | 128 | `[]` | `[]` | 18 | 18 | 10.0 / 10.0 |
   | `7fce3086…` (freeze) | 129 | 129 | `[]` | `[]` | 19 | 19 | 10.0 / 10.0 |
   | `42c10a58…` (landing) | 130 | 130 | `[]` | `[]` | 19 | 19 | 10.0 / 10.0 |
   | `4d62ee5a…` (honest-stop record) | 130 | 130 | `[]` | `[]` | 19 | 19 | 10.0 / 10.0 |

   Exit 0 on every revision. So the owned-axis moves are coverage **128/128 → 130/130** (both round-40
   entries mapped) and depth **18/18 → 19/19** (`citation_resolved_rules 19`); the freeze already reads
   129/129 and 19/19 because the triage entry and block 19 land at the freeze.

2. **Craft-section bounds at `4d62ee5a`** (same split as command A): heading `SKILL.md:81`
   (`## Queue-drain craft (rounds 5-12, distilled in round 13)`), next `## ` heading `:380`, last
   non-blank line `:375`, section 27 868 bytes, v2 marker `:361`, action line `:362`, 11 table rows
   `:365-375`. Round 39's range was `81-343` with 18 blocks.

3. **Frozen v2 interpreter on the base `SKILL.md`** (`git show fa6a8a3f:SKILL.md` to scratch):
   `python3 -I -B tools/round-40/sqfs-triage-v2.py --skill <scratch>/base-SKILL.md --table-only` →
   `sqfs-triage-v2: marker '<!-- sqfs-triage-table v2 -->' absent from the craft section`, **exit 2**.
   This reproduces the C2 "surface unmoved" command from the claims file.

4. **Frozen document conditions on `PROVINCE.md` bytes** (evaluated directly, not by running the
   counters; `artifacts/R40W2Scorecard/revision-checks.txt`):
   `42c10a58` → `frontier_content=True`, `province_core_section=True` (heading appears twice: the
   heading plus the frontier note citing it); `4d62ee5a` → `frontier_content=False`,
   `province_core_section=False`, heading occurrences 0. The conditions are `tools/round-40/c1-extra.py`
   `frontier_content` (`:118-126`: a `Round-40 frontier note` line containing `## Round-40 additions to
   Core`, the entry stem and `supersede`) and `tools/round-40/c1-counter.py` `CORE_HEADING` (`:193`,
   used at `:1138-1139` for `province_core_section`/`province_core_row`).

5. **`git diff --stat 42c10a58 4d62ee5a`** → 9 files: `PROVINCE.md`, `corpus/README.md`, the C1 entry,
   and the six score/receipt files. Carrier, oracle, non-regular table and REA receipt bytes are
   untouched, so `carriers_matched 3` cannot move with the demotion.

6. **`corpus/SOURCES.md` row census** (`grep -c '^| S[0-9][0-9][0-9] '` at four revisions):
   122 base → 123 freeze (S123) → 126 landing (S124–S126) → 126 at the record. Appends only.

7. **Read-only inspection of the committed scores and controls** (quoted, not re-run):
   `c1-at-42c10a58.json` (`carriers_matched 3`, `target 4`, `met_target false`, `exit_code 1`,
   `frozen_path_changed []`, all document bindings true); per carrier V1 `697/697`, V2 `8/8`,
   L1 `7/7`, L2 `6/6` oracle hits, L2 `matched false` with `nonregular_unpublished_ok false` and
   `nonregular_published ['firmware.bin_extract/usr/bin/busy']`; `c1-extra-at-42c10a58.json`
   (`met true`, exit 0, `oracle_rederived` ok on V1/V2/L1/L2); `c2-at-42c10a58.json` (`matched 26`,
   `n 26`, `bindings_false []`, `frozen_paths_changed []`, `met_target_consistent true`, exit 0,
   13 classes × 2, `distinct_decisions 12`, `unclassified_expected/observed 2/2`, v1 3086 B and v2
   6603 B `identical`, manifest first add `2d1ac5bc`); controls `ctl-c1-0-do-nothing.json`
   (`carriers_matched 0`, exit 1), `c2-counter-at-freeze.json` (exit 2 `no_manifest_at_rev`),
   `c2-dev-scores.json` (best control 24/26); selftest receipts `c1-counter` 70 cases (5 green/65 red,
   `failures []`), `c1-extra` 7/7, `fetch-vendor` 8/8; L2 `after.json` `extraction_gaps` = one
   `depth-limited` + two `unpublished-entry` at `firmware.bin_extract/bin/busy` and
   `firmware.bin_extract/usr/bin/ls`.

## Gates

| gate | what I checked | result |
|---|---|---|
| owned-axis proxy (command A) | coverage map + craft citation resolution at 5 revisions | exit 0, values above |
| C1 claim (frozen counter, read) | `carriers_matched` vs `target`, bindings, exit code | **not met** (3/4, exit 1) — reproduces author |
| C1 supplementary (frozen counter, read) | three bindings at `42c10a58` | met (exit 0) — reproduces author |
| C2 claim (frozen counter, read) | `matched`/`n`, `bindings_false`, `frozen_paths_changed`, exit | **met** (26/26, exit 0) — reproduces author |
| freeze integrity (read) | `frozen_path_changed []` / `frozen_paths_changed []` in both scores | clean at `42c10a58` |
| score receipts (read) | exit code recorded per score (R39-CL6) | present on all four receipts |
| surface-unmoved probes | counter at freeze 0/4; C2 counter at freeze exit 2; interpreter on base exit 2 | all three reproduce |

## Findings

**F1 (defect, calibration) — the landed C1 numbers are valid only at `42c10a58`; the draft says so
explicitly.** The demotion commit `4d62ee5a` renamed `## Round-40 additions to Core` to
`## Round-40 measured, not promoted (R40-C1 honest stop)`. Under the frozen code that makes
`province_core_section` and `province_core_row` false (`c1-counter.py:193,1138-1139`) and also makes
`c1-extra.py`'s `frontier_content` false (`:118-126`), so `c1-extra` at the tip reads `met false`, while
the lane's scorecard sentence "the supplementary gate met" is only true at `42c10a58`. Measured by
applying the frozen conditions to the two revisions' bytes; I did not re-run either counter (that is
`R40W2C1Rescore`/`R40W2C1SuffixAudit` territory). The honest stop itself is unaffected and is in fact
cleaner at the tip: no round-40 revision reads `met_target true`. Consequence for the section: every C1
number is bound to `42c10a58`, and the "core row" language must be demoted throughout.

**F2 (defect, hygiene) — uncommitted `SKILL.md` edit in the lane at measurement time.** `git status`
at `0b15c8b2` shows `M SKILL.md`, `+19` lines: a `### Round-40 instrument registry` section appended
after `:1383`. It does not touch the craft section (81-375) or the v2 table block, so command A and the
C2 table bindings at `4d62ee5a` are unaffected; but if it is committed after this section lands, the
`SKILL.md` blob moves without a stated reason. Not my edit; L1 decides commit-or-drop.

**F3 (observation, corroborates the author) — the C1 false negative is visible inside the frozen
evidence, not only in the author's prose.** L2's own receipt records two `unpublished-entry` gaps for its
two symlinks (`bin/busy`, `usr/bin/ls`) while the same counter's `nonregular_published` lists the
*regular* file `usr/bin/busy` as the symlink `bin/busy`; `same_rel` is equality or
`candidate.endswith('/' + rel)` (`c1-counter.py:606-607`, call at `:643-650`, use at `:1090-1092`). The
two clauses contradict each other in one score file, and no symlink path appears in the published set.
So "counter false negative, honest stop" is the reading the bytes support, not just the author's claim.

**F4 (limit) — no committed C2 selftest receipt.** The C2 case counts (c2-counter 42, interpreter 45,
generator 6) are declared in `plans/round-40-claims.md` and the round-40 registry; the only 42-case run
on the record is wave-1 build evidence (`w1/R40C2Counter.md` §E1, `cases 42 pass 42 fail 0`, exit 0).
The controls directory holds C1 selftest receipts and the C2 freeze counter, not C2 selftests. The draft
states this rather than implying a controls receipt.

**F5 (observation) — the round-40 section did not exist before this draft** (no round-40 commit touches
`SCORECARD.md`/`LOG.md`; the last change to both is round 39), so the owned-axis move is still
unreadable in the lane's own scorecard. Same shape as the round-39 wave-2 finding D1; the two drafts
discharge it.

## Touched surfaces

Written (all inside my bounds):

- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/scorecard-section.md` — draft `## Round 40` section
  (claim table with before/after/counting command/measured revision/verdict, the paste-ready capability
  row, the owned-scores paragraph, the wave-2 record skeleton with the two draft-state facts, planned /
  retired bullets).
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/log-entry.md` — draft `## 2026-10-26 — round 40`
  entry in the round-39 form.
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/cmdA.txt` — verbatim command A output, five
  revisions.
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/revision-checks.txt` — base-interpreter exit 2, the
  two-revision document-condition evaluation, the `42c10a58..4d62ee5a` file list and the worktree state.
- `.ufo/waves/round-40/w2/R40W2Scorecard.md` — this report.

Nothing was written into `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
`SKILL.md`, `LOG.md`, the fleet repo, sibling lanes or `/home/vgpnk/Projects/shokuknow`. No VCS
mutation; no fixture clone was needed (command A reads Git objects). Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2Scorecard` was removed. No tool was installed or updated by this
seat (the pinned toolchain — sasquatch/sasquatch-v4be 4.5.1, unblob 26.6.4, rea-agents 6.5.0 — was only
read).

## Out of scope (named, not done)

- Re-running the frozen C1/C2 counters at any revision (other wave-2 seats own that; F1 is derived from
  the frozen code and the two revisions' bytes, not from a new run).
- Re-building vendor carriers with `fetch-vendor.py`, any REA or unblob run, any envelope re-derivation.
- Deciding whether the uncommitted `SKILL.md` registry section (F2) is committed.
- Completing the scorecard's `### Wave-2 falsification record`: it needs the settled 38-seat wave and is
  L1's text. My draft states only what is observable now.
- `PROVINCE.md` / `corpus/README.md` wording repairs (the draft's demotion language is already in the
  lane; nothing more is proposed).

## Limits

- The claim numbers are quoted from receipts I did not produce; I checked their internal consistency
  (per-carrier fields, gap lists, table byte counts, bindings) and their receipt exit codes, not the
  provenance of each REA run. [INFERENCE] where I say a re-score *would* fail a binding at the tip: I
  evaluated the frozen conditions on the bytes, not the counters' full control flow.
- Command A measures an index proxy (mapped stems, citation resolution), not domain truth; a perfect
  finite proxy retires no axis, which is why all three owned scores stay at 10.
- The C1 3/4 versus 4/4 question is not mine to settle: the predicate's non-regular clause is what it is,
  and both readings (counter false negative, or clause doing its job) are argued by other seats.
- One lane fact I could not date: whether the uncommitted `SKILL.md` edit predates or postdates the
  wave-2 dispatch commit `0b15c8b2`.

## Artifact paths (relative to the lane)

- `.ufo/waves/round-40/w2/R40W2Scorecard.md`
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/scorecard-section.md`
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/log-entry.md`
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/cmdA.txt`
- `.ufo/waves/round-40/w2/artifacts/R40W2Scorecard/revision-checks.txt`
