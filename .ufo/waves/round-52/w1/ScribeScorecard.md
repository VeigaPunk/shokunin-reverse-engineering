# ScribeScorecard — round-52 SCORECARD section skeleton

**Verdict:** the skeleton is drafted and every BEFORE cell is filled from committed bytes; **no
verdict is pre-filled** and no AFTER/measured-commit cell carries a value. The L1 fills the 21
angle-bracket placeholders from receipts only.

**Artifact:** `.ufo/waves/round-52/w1/ScribeScorecard/section.md` (the `## Round 52 (2026-10-30)`
section skeleton: base, claims draft, wave shape, the two-row claims table, owned-axes head
update, learning-trend lines, limits, `planned (round 53)`, `retired`).

## What the skeleton contains

- Base `c525de54a53eb3c4fee28ede2721da4527cf8ece`, claims draft `ab0eafedc41402b43b41a4362084119578dfe7ce`
  (the claims file is named as authoritative over any summary).
- Wave shape as placeholders: w1 = 64 seats, v2 policy band 64–128, role mix from
  `.ufo/waves/round-52/w1-dispatch.json` (executor 21, scribe 8, reviewer 8, scout 7, critic 7,
  mutation-tester 4, connector 3, sentinel 3, revenger 2, simplifier 1; attack roles 24/64 = 37.5 %,
  above the 25 % floor); the w2 falsify wave (32–64 seats) or the ≤8-seat residual call is a
  placeholder, plus the round total ≤128.
- Claims table with R52-C1 (coverage) and R52-C2 (depth), AFTER / verdict / counting-command /
  measured-commit columns left as placeholders.

## BEFORE column, filled from committed bytes

**R52-C1 — committed and measured.** `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`:
`carriers_matched 2` of target 4, `exit_code 1`, `met_target false`, failing
`g7581:gaps_ok`, `g7581:projection_ok`, `g7582:gaps_ok`; `bindings_false` =
`[province_core_section, province_core_row]`; `frozen_path_changed []`;
`counter_sha256 9820811b…`. Per-carrier: c6430 and c6490 `gaps_ok true`/`projection_ok true`;
g7581 both false; g7582 `gaps_ok false` only. The frozen rule's single silent char-device
allowance is `247:0` (Cable class); the FRITZ!Box class carries thirteen char-devices, so twelve
rows are unaccounted.

**R52-C2 — committed bytes, measured routing (mine).** The claims draft declares the frozen
executability audit's before-state as **1 violation** naming `dmg_Z3_v3ddwrt_inode_table`. That
count is a *declared* before-state: the v6 audit instrument does not exist in committed bytes yet,
so the skeleton marks the count as declared and leaves `<C2-BEFORE-RECEIPT>` open for the L1.
What I did measure is the routing the violation is about: the committed v5 instrument over the
frozen 126-envelope corpus at the claims-draft SKILL bytes labels `dmg_Z3_v3ddwrt_inode_table`
`legacy-body-failure` / `cross-read-legacy` (step 7), `pair_mismatches 0`, `evaluator_missing 0`,
label distribution `legacy-body-failure 7`. In the same run the two clean ddwrt no-pad `_ddefault`
envelopes (`…be.nopad_ddefault`, `…le.nopad_ddefault`) are `clean` / `none`, so the v6 route change
is confined to the one FAILED-body pair.

**`census_outside 0` both sides (measured).** `tools/round-51/census3.py --root . --rev <REV> --check`
exits 0 with `registry_paths 56`, `census_paths 56`, `census_outside []`,
`census_unregistered []`, `duplicates []` at the round base `c525de54…` **and** at the claims draft
`ab0eafed…`. The skeleton records it as a no-regression binding inherited from round 51, not a
claimed move.

## Coverage head and other head lines

The coverage observable is **141/141** before this round: command A at both `c525de54…` and
`ab0eafed…` reports `knowledge_files 141`, `mapped 141`, `missing []`, `dangling []`,
`rule_blocks 26`, `citation_resolved_rules 26`, `coverage_score 10.0`, `depth_score 10.0`
(`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 141 at both revs; the
claims draft adds exactly one path, `plans/round-52-claims.md` — `git diff --name-status` between
the two revs). The skeleton carries the in-place `## Owned axes` coverage-row update as
**141/141 → 142/142 once the entry lands**, with the explicit instruction that a missed claim
leaves the head at 141/141 and says the promotion did not happen.

## Placeholders the L1 must resolve (24)

`HEADLINE`, `FREEZE-HASH`, `LANDING-HASH`, `LANDING-REV`, `W2-OR-RESIDUAL`, `AFTER-C1`, `AFTER-C2`,
`COUNTING-CMD-C1`, `COUNTING-CMD-C2`, `MEASURED-AT-C1`, `MEASURED-AT-C2`, `C2-BEFORE-RECEIPT`,
`COVERAGE-SCORE`, `COVERAGE-HEAD-UPDATE`, `DEPTH-SCORE`, `DEPTH-HEAD-UPDATE`,
`CALIBRATION-SCORE`, `CALIBRATION-HEAD-UPDATE`, `EXPANSION-TREND`,
`QUALITY-TREND`, `DISCERNMENT-TREND`, `LIMITS-PARAGRAPH`, `PLANNED-NEXT-ROUND`, `RETIRED`.
Each must be replaced by a measured value or the cell deleted; an unfilled token may not ship.
The three owned-axis **score** cells (`COVERAGE-SCORE`, `DEPTH-SCORE`, `CALIBRATION-SCORE`) are
placeholders too — even the `10 → 10` pair is a measured statement about the landing, not a
constant the round may assume.

## Scope and honesty notes

- I read the lane tree read-only; the only writes are my seat directory
  `.ufo/waves/round-52/w1/ScribeScorecard/` and this report. `git status --porcelain` in the lane
  shows only the untracked `.ufo/waves/round-52/` wave directories (other seats' and the L1's),
  no tracked-file change. No commit, push, stage or stash; no mutating git/jj command; no REA run,
  no `--data-run`, no download, no `corpus/evidence/` write, no tool install.
- No verdict is asserted: the two claim rows carry no AFTER value, no `met`/`not met` word, and no
  measured-commit hash.
- The C2 BEFORE cell deliberately separates *declared* (the claims draft's `executability_violations 1`)
  from *measured* (the v5 routing I reproduced). If the L1 prefers the section to cite only the
  declared count, the `<C2-BEFORE-RECEIPT>` token is where its own receipt goes.
- One judgement the L1 may want to overrule: I put the "the two clean ddwrt no-pad `_ddefault`
  envelopes keep `clean`" measurement into the BEFORE cell because it bounds the v6 route change to
  a single pair; the claims draft asserts it, and my run confirms it over the committed corpus.

## Receipts (each entry carries argv, cwd, UTC, exit code, stdout sha256)

`ScribeScorecard/receipts.json`:

| entry | exit | stdout sha256 |
|---|---|---|
| `census3-check-at-round-base` | 0 | `05fd7281c9cc723ad57a37d0dac670670fb3110807991be5c6a95e9756f1aaef` |
| `census3-check-at-claims-draft` | 0 | `6b2484fc157f52e6327d686cf3c36b54c55874a825af52c5b5ecdf47fef07bff` |
| `c2-v5-baseline-at-claims-draft` | 0 | `0d5985165972868c9bc10a1cb43121cd3dd206ea50033ff393dca7cc446ac172` |
| `git-diff-base-to-claims-draft` | 0 | `e6e6d5148327c7834e617044c3af91dc83a81a24f3da84c42e43ade89ed0fc6f` |
| `git-ls-tree-knowledge-count-base` | 0 | `85a0e6eb5530a682fa88345a5e7a144248f49e5b71b3eb587a9db5cd2957495a` |

Full v5 run output: `ScribeScorecard/v5-baseline-claims-draft.json`
(sha256 `18a213927be4652848a38afc1486309145da2bfce5a2d01fcd359c8ac068ef49`).

Commands, verbatim:

```
python3 -I -B tools/round-51/census3.py --root . --rev c525de54a53eb3c4fee28ede2721da4527cf8ece --check
python3 -I -B tools/round-51/census3.py --root . --rev ab0eafedc41402b43b41a4362084119578dfe7ce --check
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --skill $S/SKILL-claims-draft.md \
  --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes \
  --json-out $S/v5-baseline.json --work $S/work
git diff --name-status c525de54a53eb3c4fee28ede2721da4527cf8ece ab0eafedc41402b43b41a4362084119578dfe7ce
git ls-tree -r --name-only c525de54a53eb3c4fee28ede2721da4527cf8ece corpus/knowledge | grep -c '\.md$'
```

`$S/SKILL-claims-draft.md` is `git show ab0eafedc41402b43b41a4362084119578dfe7ce:SKILL.md`
(329 164 bytes) written into scratch — a scratch copy of a committed blob, not a lane edit.

Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeScorecard` removed after the receipts were
copied into the seat directory. `disk-guard.sh status` was read before the pass (no heavy pass
was needed; `/fast` at 47 %).
