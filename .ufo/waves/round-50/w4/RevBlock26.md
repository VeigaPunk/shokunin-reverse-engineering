# RevBlock26 — round 50 attempt 2 wave 4 (falsify) — SKILL rule block 26 vs frozen R50-C3 claims

**Verdict: LANDING HOLDS at the assigned tip `c67b741e8f6bd8d64adbdb15e059d47fde004c77`.** Every frozen-detail check on block 26 matches, the scoring claim reproduces exactly (after 0 mismatches, before 19 = 4 v2ns + 7 v3_broadcom + 8 v3_nonstandard), the disclosed residue reconciles with the reader-census receipt down to the "8 labels" what-if, and both the committed mutation battery and my own independent mutations are caught. One disclosed post-tip drift (instrument guard-fix `1a7cc5c3`, sha `ef4633c5→f29eb920`) is reported as a calibration note, not a defect; two hygiene observations are reported for the L1. Seat: RevBlock26, 2026-10-29T21:43Z. Scratch `/fast/scratch/hyaku/kaidoku-r50/w4-RevBlock26` (removed after receipts copied here).

## Checks against the frozen claims (`plans/round-50-attempt2-claims.md`, sha256 `0cf4047443575a982ae8f0a8ce87ce3c785fe9a7064c151c9258e53f12fe22de`)

| # | Claim detail | Result | Evidence |
|---|---|---|---|
| 1 | `legacy-body-failure` failing-handler cell exactly `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt` | HOLDS | `SKILL.md:560` at tip (byte-exact, single comma-list, no spaces) |
| 2 | no-reader set exactly {`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`} | HOLDS | header sentence (`:548`), `no-reader-failure` row (`:561`), `clean-unverified` row (`:568`) |
| 3 | actions vocabulary line carries `record-unverified` and `preserve-unresolved` | HOLDS | `SKILL.md:551`; instrument enforces it — my mutant dropping `record-unverified` refused exit 2: `action 'record-unverified' is not declared in the vocabulary line` (`m1-actvocab.log`) |
| 4 | both new rows present with the named actions | HOLDS | `no-reader-failure`/`preserve-unresolved` (`:561`), `clean-unverified`/`record-unverified` (`:568`) |
| 5 | every cause cell carries a `->` | HOLDS (17/17 rows, mechanical parse); instrument-enforced | my arrow-strip mutant refused exit 2: `cause -> action cell has no "->" separator` (`m4-arrow.log`) |
| 6 | every source cell names a resolvable citation | HOLDS | 15 carried rows cite `SKILL.md table v4 row 1..15` — v4 table at tip has exactly 15 data rows and the citations map 1:1 in order; `S112/S118/S119/S120/S121/S122/S124` each resolve in `corpus/SOURCES.md`; the two new rows cite `R50-C3` (claims section exists), `round-49 W2Skill.md F1/F2` (`.ufo/waves/round-49/w2/W2Skill.md` exists) and the claims path |
| 7 | status numbers 19/126/26/51 | HOLDS, reproduced | before receipt `pair_mismatch_count 19` (4/7/8 composition verified from `c3-before.json`); after `n_envelopes 126`, `pair_mismatches 0`; my reruns of the four w3 control tables give exit 1 with exactly 19/126/26/51 (`ctl-*-rerun.json`); all-`clean` junk variant refuses exit 2 duplicate-label (`ctl-junk-parse-refusal.log`, matches my rerun of `w3/ExecTriageControls/ctl-junk.skill.md` exit 2) |
| 8 | instrument sha256 `ef4633c5…3ed0` at tip; `--selftest` 18 cases | HOLDS at tip | `git show c67b741e:tools/round-50-c3/sqfs-triage-v5.py \| sha256sum` = `ef4633c5…3ed0`; selftest `18 cases, pass 18, fail 0` on the tip-extracted bytes (`selftest-tip.log`) |
| 9 | disclosed residue vs reader-census receipt | HOLDS | block: "six of seven ddwrt fixtures and seven of eight broadcom fixtures have no complete reader" — census family table: ddwrt `6/7 NO-READER`, broadcom `7/8 PARTIAL` (`.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`); failed body `dmg_Z3_v3ddwrt_inode_table` routes `legacy-body-failure`/`cross-read-legacy` under table AND evaluator (after receipt envelope entry) |
| 10 | supersession sentence (block 21 defers) | HOLDS | block 26 header: "Block 21 stays as history; from 2026-10-29 every decision this block makes, block 21 defers to it." Block 21 is untouched (frozen claim required history only, no reciprocal note) |
| 11 | registry: exactly one `instrument-registry v2` row | HOLDS | one row for `tools/round-50-c3/sqfs-triage-v5.py` (`SKILL.md:1800` at tip) |

## Counting-command re-runs (named-allowed C3 re-runs only; no REA invoked)

| Command | Exit | Key output | Receipt (sha256) |
|---|---|---|---|
| `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <lane> --rev c67b741e… --freeze 435d41fd… --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --work $S/w --json-out $S/tip.json` (seat-spec parse-check, work-tree instrument) | 0 | `pair_mismatches 0`, `evaluator_missing 0`, 126 envelopes | `tip-parsecheck-worktree-instr.json` = `83d77183…` |
| same, but instrument extracted from the tip blob (pinned pair) | 0 | `pair_mismatches 0`; receipt's own `instrument_sha256 ef4633c5…` | `tip-parsecheck-pinned.json` = `83d77183…` (byte-identical to the work-tree run → the post-tip guard fix changed no scoring output) |
| `… --selftest --work $S/w-st-tip` (tip bytes) | 0 | 18/18 | `selftest-tip.log` = `46240261…` |
| `… --selftest --work $S/w-st-head` (HEAD bytes f29eb920) | 0 | 18/18 | `selftest-head.log` |
| `… --controls …` (tip bytes) | 0 | 9 controls all red in some scope; do-nothing red(19) on corpus and names the four v2ns `_ddefault` | `controls-tip.log` = `2f1824e2…` |

## Mutation tests (mine, beyond the committed battery) — tip table copies via `--skill`, tip instrument

| Mutant | Exit | Observation |
|---|---|---|
| m1 actions-vocabulary drops `record-unverified` | 2 | refused: undeclared action — vocabulary line enforced |
| m2 renames `<!-- sqfs-triage-table v5 -->` marker | 1 | falls back to the v4 marker → 19 mismatches (documented RED-BEFORE fallback; v3/v2/v1 markers are refused) |
| m3 adds `squashfs_v3_ddwrt` to the `clean-unverified` handler cell | 1 | **7** pair flips, exactly the envelopes whose measured handler is `squashfs_v3_ddwrt` (6 `ddwrt_*_ddefault` + `dep_A2_squashfs_v3.be.nopad`); the two `ddwrt_squashfs_v3_{le,be}_ddefault` envelopes measure handler `squashfs_v3` (census shows their bytes equal the standard-v3 fixtures, sha `0161351caec8`) so they stay `clean`. Reconciles the claims' "exactly those 8 labels": 7 clean pairs + the failed body `dmg_Z3` (HF=`squashfs_v3_ddwrt`, would move to `no-reader-failure` under a both-rules move, keeping `pair_mismatches 0`) |
| m4 strips `->` from the `clean` row cause | 2 | refused: separator enforced on every cause cell |
| m6 replaces the legacy comma-list with `;` separators | 2 | refused: each comma-alternative must be a glob/plain name — any-of-exact semantics confirmed |

Committed battery (`--controls`, re-run above): do-nothing 19, guard-row-deleted 19, legacy-glob-widened VACUOUS-on-corpus/RED(1)-on-fixtures, new-row-actions-swapped 19, no-reader-family-moved-to-clean 7, precedence-order-swapped 19, no-reader-failure-row-deleted VACUOUS/RED(1), legacy-row-deleted 7, junk-table 126. The two corpus-VACUOUS controls are RED on the committed synthetic fixtures, matching the claims' disclosure that the corpus holds zero no-reader extractor-failure envelopes.

## Findings by severity

- **None (no actionable defect in scope at the tip).**
- **LOW / calibration (disclosed drift):** the lane HEAD is now `92ec6e6d`, past the assigned tip. `1a7cc5c3` ("C3 guard fix … sha f29eb920") replaced the instrument (`ef4633c5→f29eb920`; diff confined to the `claim_counting_command_is_consistent` selftest case — scoring/evaluator/table code untouched, which my byte-identical re-runs confirm) and rewrote the `instrument_sha256` field in `c3-{before,after}.json`, the SKILL status line, and the lesson guard-defect note. The frozen claims file still names `ef4633c5…` — stale at HEAD, but the claims are frozen and the correction is disclosed in `corpus/lessons/round-50.md`; the tip-state contract I was assigned is internally consistent. Suggest the round report note the claims-vs-live sha discrepancy explicitly.
- **LOW / hygiene (reported, untouched):** the lane working tree carries ~13–25 uncommitted modifications under `.ufo/waves/round-50/w3/ExecTriageControls/receipts/` and w3/w4 reports (count grew 13→25 during this seat — live sibling re-measurement). Fleet rule: L1 owns deletions; I changed nothing outside my seat dir.
- **INFO / residual design note:** the v5→v4 marker fallback is red-by-design on this corpus (19) but a v5 marker typo on a no-reader-free corpus would silently re-score as v4; v3/v2/v1 markers are refused outright. Consider refusing an absent-v5-marker when `--rev` is expected to carry one. Not a claim violation.
- **INFO:** receipts carry `instrument_sha256_at_freeze: null` / `instrument_unchanged: null` — by design (`tools/round-50-c3/` sits outside the C1/C2 frozen `tools/round-50/` walk); `instrument_sha256_at_rev` transparently records the blob at the measured rev (`a2ebb5a4…` at `1439dfe9`).

## Verification gaps

- C1 counter and C2 battery not re-run by this seat (C1 invokes REA — L1-owned; C2 re-run is a sibling seat's named duty). Their receipts were read only: `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (miss, exit 1), `c2-final-attempt2.json` (green).
- New SOURCES rows S243/S244/S245/S249 re-opened read-only: all four rows present in `corpus/SOURCES.md` (156-row registry, matching the claims' 152→156), each `used-by` lists `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, and the entry/coverage-map/SCORECARD rows exist; URL re-fetch was not repeated (scribe seats own it).
- No REA run was invoked; lane tree read-only except my seat dir; scratch removed after artifact copy.
