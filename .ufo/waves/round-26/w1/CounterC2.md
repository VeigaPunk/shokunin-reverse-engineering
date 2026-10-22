# CounterC2 — R26-C2 calibration counting instrument

Seat: KaidokuR26.CounterC2 (executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Base a0639d8e61e486e2a716ff94cddd89a73200a02c; claims frozen at c27f445e70cedbaf5300b2fd0a53e821d9b659a9.
Read-only on the lane: Git objects only (`git cat-file`, `git ls-tree`, `git rev-parse`, with `GIT_OPTIONAL_LOCKS=0`); `.git/index` sha256 and mtime identical before and after the runs (4746b06e08244668de1adc8f854bac75d038f4488b9fb07720533c64b5ad5ca7, 2026-10-22 09:01:21.708936449).
No REA call, no web source, no tool installed; the lane's working tree shows sibling-seat edits and this seat wrote only this report.

## Deliverable

- Script for the L1 to commit at `tools/round-26/c2-calibration.py`: `/fast/scratch/hyaku/kaidoku-r26/seats/CounterC2/c2-calibration.py`, sha256 `3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e` (34117 bytes).
- Standard library only; runs under `python3 -I -B` (Python 3.14.8). CLI `--root <LANE> --rev <REV>`
  and `--selftest`; JSON: `items`, `mismatches`, `command_a_at_rev`, per item `id`, `result`
  (pass/mismatch), `stated`, `observed`, `note`. Exit 0 iff mismatches == 0, exit 1 otherwise,
  exit 2 on input error (bad revision, unreadable required blob, missing `--root`/`--rev`;
  argparse usage errors also exit 2).

## Real runs — before count

`python3 -I -B c2-calibration.py --root <LANE> --rev <REV>` at 2026-10-22T12:23:32Z (base), 12:23:33Z (frozen):

| REV | items | mismatches | K1 | K2 | K3 | K4 | K5 | K6 | exit |
|---|---|---|---|---|---|---|---|---|---|
| a0639d8e (base) | 6 | 5 | mismatch | mismatch | pass | mismatch | mismatch | mismatch | 1 |
| c27f445e (claims frozen) | 6 | 5 | mismatch | mismatch | pass | mismatch | mismatch | mismatch | 1 |

**Before mismatch count: 5 of 6; K3 is the only pass.** This matches the frozen `before_expected` ("5 of 6 by reading at base (K3 expected to hold)") and seat KaidokuR26.MutR25Calib's independent preview. c27f445e differs from the base only by `.ufo/waves/round-26/claims.json` and `corpus/evidence/round-26/before/census-start.txt`, so both runs read the same card bytes.

Observed at base (from `final-a0639d8e….json`): K1 depth row first N/M token 9/9 while command A
gives rule_blocks 17 and citation_resolved_rules 17 → mismatch. K2 craft span at base is
`SKILL.md:81-314` (heading line 81, next `## ` at 319, last non-blank line 314); the depth evidence
cell holds `SKILL.md:77-191` and `SKILL.md:81-318`, not `SKILL.md:81-314` → mismatch. K3 hex after
"measured" in the depth evidence cell = `638fb211`, resolves, command A there gives rule_blocks 9 and
citation_resolved_rules 9, equal to the K1 N (9) → pass. K4 coverage row first N/M token 108/108,
command A at base gives mapped 108 and knowledge_files 108 (headline holds), but the hex after
"measured" is `3395b6d`, which resolves and gives 78/78 → mismatch. K5 hex after "measured" in the
calibration evidence cell = `75af886a`; `measured_revision` in
`evidence/round-1-2026-10-15/result.json` at base is `c265db9bd3c0883fbaf4487f839559c85a736826`;
not a prefix → mismatch. K6 SHONEN box line is line 11 (`- [~] No cross-domain bleed`); the next
line has `PROVINCE.md:95-116` (inside PROVINCE.md's 303 lines) but also the word "contested" → mismatch.

Command A is a port of `SCORECARD.md` `## Measurement recipes` recipe A read from Git objects through `--root`. Port check: recipe A extracted verbatim at c27f445e (`commandA.py`, sha256 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01, the same sha256 seat C1Cherrypick reported) and the port produced byte-identical JSON at 8 revisions: a0639d8e, c27f445e, 638fb211, 3395b6d, 3e99fbd6, 08c7a729, a79945c4, 66455858.

## Selftest

`python3 -I -B c2-calibration.py --selftest` → exit 0, `cases 18, failures 0` (full JSON in
`selftest.json`). One red fixture per item, each giving exactly one mismatch with the expected item
id: k1-red (depth N/M 2/3), k2-red (span `SKILL.md:3-8`), k3-red (measured revision resolves but
command A there gives 3 rule blocks against N 2), k4-red (coverage 3/3 against command A 2/2), k5-red
(calibration measured revision `abcdef01`), k6-red (pointer `PROVINCE.md:2-9` against a 5-line
PROVINCE.md), k6-contested-red ("contested" kept), k4-duplicate-row-inside-owned-axes (two
`| coverage |` rows inside `## Owned axes`), plus the m6 case (box promoted to `- [x]`, "contested"
kept, red only through the retained word) and the m9 case (box promoted, clause reworded as
"settled", expected green: the measured box-mark gap), both from MutR25Calib's fixtures. The green
fixture carries a decoy `| coverage |` row claiming 9/9 outside `## Owned axes` that must not be read
(green stays 0 mismatches; a separate check asserts the decoy exists and is outside the section).
bad-revision-is-input-error → exit 2.

## Fixtures received from KaidokuR26.MutR25Calib (included)

Their nine patch files were read (sha256s match their report), applied to a sandbox clone
(`/fast/scratch/hyaku/kaidoku-r26/seats/CounterC2/clone`) and measured; at the frozen commit the
instrument already fails K1, K2, K4, K5, K6, so at base every mutant except M9 shows the same 5
failing items; M9 (box checked, "contested" rewritten as "settled") shows 4, because K6 then passes.
Their M1, M5, M8 paths are rebuilt as selftest cases and are killed: M1 (decoy before `## Owned axes`
plus wrong owned-axes row) → K4 mismatch; M5 (README map stem removed) → K4 mismatch; M8 (wrong
owned-axes row) → K4 mismatch. M6 (box promoted to `- [x]`, "contested" clause untouched) is killed
by K6 only for an inherited reason: the frozen base line after the box still carries "contested", so
K6 already fails there; the box promotion itself is observed by no K rule. M9 is the sharper probe
for that gap (it removes "contested" and still promotes the box) and it survives. M3, M4, M7 have no
counterpart in K1-K6. M2 and M9 are not observable to the frozen rules (see limits).

## Validation on real lane bytes (repair simulation)

`repair-simulation.py` runs only in the sandbox clone. It simulates the repair the L1 owns
(SCORECARD `## Owned axes` rows and one SHONEN line) on top of c27f445e, then mutates that repaired
state (`repair-simulation.json`); results as exit/mismatches/failing:

- simulated repair → 0/0/none; decoy `| coverage |` rows outside `## Owned axes` (before the heading and in a later section) → 0/0/none.
- owned-axes coverage row 99/99 plus a decoy → 1/1/K4; two `| coverage |` rows inside `## Owned axes` → 1/1/K4; depth row count 16/17 → 1/2/K1,K3.
- SHONEN pointer `PROVINCE.md:95-316` (outside the 303-line file) → 1/1/K6; pointer `PROVINCE.md:119-160` (Core tables, inside the file) → 0/0/none (limit); box `- [x]` with the clause reworded as settled → 0/0/none (limit).
- calibration row keeps `75af886a` → 1/1/K5; depth measured revision pointing at a 9/9 revision → 1/1/K3.

The repair that reaches 0: depth observable 17/17 with measured revision `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`, depth evidence cell containing `SKILL.md:81-314`, coverage row 108/108 with a measured revision that command A also gives 108/108 at (`08c7a729…`), calibration row measured at `c265db9b`, and the SHONEN asserted line without "contested". The L1 owns that edit; per the claims' causal-separation note the coverage row must be restated from command A where C1 lands.

## Interpretations of the frozen rules

1. "Cells split on ' | '" is taken literally: observable cell = `cells[2]`, evidence cell = `cells[3]`. No cell of the three real rows contains " | ".
2. Row scope: the section starts at the first line starting with "## Owned axes" and ends before the next line starting with "## "; rows elsewhere are never read.
3. The rule speaks of "the row" per axis, so zero rows or two rows for an axis make that item a mismatch with an explicit reason, not a silent first-row or last-row choice. This closes the round-25 first-row false accept (routed defect 3) in the strict direction.
4. "The first N/M token" is the first `\d+/\d+` match in the observable cell; the score cell ("10 → 10") is not read.
5. "The first 7-40 hex revision following the word 'measured'": the first maximal hex run of length 7 to 40 after the first occurrence of the word "measured" (word boundaries, so "measured_revision" does not count). Runs shorter than 7 (for example the "a" of "at") are skipped; a maximal run longer than 40 is not a valid revision and is skipped. No such run exists in the lane's rows.
6. K3 uses the K1 N, so a wrong depth count also turns K3 red (the "depth row count 16/17" case); that follows the rule text.
7. Command A is ported to read Git objects of the named revision through `--root`; output-identical to the verbatim recipe at 8 revisions. Craft span: H is the line of the first line starting with "## Queue-drain craft" in SKILL.md at REV; L is the last non-blank line before the next line starting with "## " (trailing blanks excluded, L never below H); at base 81-314.
8. "Inside PROVINCE.md's line count" means the pointer's start and end lie between 1 and the number of lines of PROVINCE.md at REV (303 at base). Section bounds inside PROVINCE.md are not read, as the rule says.
9. K6 accepts "- [~] No cross-domain bleed" and "- [x] No cross-domain bleed" as the box line and reads the line after it; a box line at end of file, or an asserted line with no PROVINCE.md pointer, is a mismatch. Unreadable required blobs (SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, evidence/round-1-2026-10-15/result.json, corpus/README.md, corpus/knowledge/*) or a result.json without `measured_revision` are input errors (exit 2), not mismatches; a missing or duplicated axis row is a mismatch.
10. The instrument reads only the frozen files; it never reads C1's evidence files, as the claims require.

## Limits and risks (disclosed, not fixed: the rules are frozen)

- M2 shape (SHONEN pointer to the Core tables, inside PROVINCE.md's line count) passes K6: the frozen rule bounds pointers by the line count only, as C1Cherrypick predicted for the round-25 I5 rule (a pointer such as `PROVINCE.md:119-131` covers Core tables rather than refusals and passes), so this is a carried-over limit of K6 and of I5. M9 shape (a checked `- [x]` box with the stale clause reworded) also passes K6, since no K rule reads the box mark — at base it even turns K6 green, because dropping "contested" satisfies the letter of the rule while the row stays false in substance. M6 is killed only through the inherited "contested" word, not through the box mark.
- M3, M4, M7 (round-25 items about the round-24 outside verdict) have no counterpart in K1-K6, so wording changes there are not observable.
- K4 reads the coverage count command A gives at the revision under test; when C1 lands and the knowledge count changes, the coverage row must be restated from command A at that commit or K4 turns red again. A count of 0 means those six statements agree with the observed state at that revision; it is not a claim that SCORECARD.md or SHONEN.md is calibrated in general.

## Artifacts (under /fast/scratch/hyaku/kaidoku-r26/seats/CounterC2/)

- c2-calibration.py sha256 3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e; selftest.json sha256 272b0c9ef3377dffe5324b9885938e4c88adcd2fb280005519f8fbcceb5840bd; final-a0639d8e61e486e2a716ff94cddd89a73200a02c.json sha256 bc5cf07b67f3f15354f932568dc5e57a87de2dbf63c84a96dab6970c72974a51; final-c27f445e70cedbaf5300b2fd0a53e821d9b659a9.json sha256 226f6c0a756631e1509848464745ce7e188d778cd881bd9e766099b443c1cb97
- repair-simulation.py sha256 4722e7c7b39faff2962648286c8dc5f7c81883ed7ccfe84ba92a5963aa4bcdc0; repair-simulation.json sha256 57317bad6d48ec5e98a8d4c5b4ca7e28d535ca5281f55cb5a7d7cd715aba141e; commandA.py (recipe A extracted verbatim) sha256 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01; scorecard-at-frozen.txt sha256 cfe8b5257c90b14b3f7cbe1349d6117a78494632096ab1fa2594e189038d977a
- clone/ — sandbox clone of the lane holding the mutant and repair-simulation commits; the lane itself was not modified by this seat.
