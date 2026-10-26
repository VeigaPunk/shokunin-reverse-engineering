# R36MutantC2 — mutation test of `tools/round-36/c2-counter.py` (round 36, wave 1)

Seat: R36MutantC2 (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Target of test: the frozen R36-C2 counter at `tools/round-36/c2-counter.py` (340 lines).
Detector: the counter's own bounded behavioral selftest (`python3 -I -B … --selftest`, 13 cases: 1 green, 12 red; exit 0 iff every case lands on its expected verdict). The detector itself was never modified; each mutant is a single-point edit of a scratch copy.

## Method

- Scratch: `S=/fast/scratch/hyaku/kaidoku-r36/R36MutantC2`; `TMPDIR` and `HYAKU_SCRATCH` pointed into `S`, so the selftest's fixture repos (`tempfile.mkdtemp(dir=$S/kaidoku-r36)` → `git -C D init -q`) stayed inside my seat scratch. The counter's selftest already enforces the fixture rule itself: it checks `git -C D rev-parse --show-toplevel` equals `D` before the first commit and raises `SystemExit('fixture toplevel mismatch')` otherwise (counter lines 309–312). All fixtures were removed by the selftest's own `finally: shutil.rmtree`; the whole `S` was removed at the end (evidence below).
- Per mutant: `cp` pristine → `mNN.py`, one surgical string replacement, run `--selftest`, record output JSON + exit code + sha256. Lane file opened read-only throughout.

## Baseline (pristine)

- sha256 `tools/round-36/c2-counter.py` = `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` (identical hash for all 14 scratch copies before mutation).
- `--selftest`: `{"selftest": "c2-counter", "cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}`, exit 0. Baseline passes, so every mutant result below is conclusive (no inconclusive runs).

## Results — 14 mutants: 7 killed, 7 survived

Verdict rule: killed = selftest exit 1 (at least one case flips to the wrong verdict); survived = exit 0, byte-identical observable behavior to pristine on all 13 cases.

| ID | Site (pristine line) | Mutation | sha256 (12) | Selftest result | Verdict |
|----|----|----|----|----|----|
| m01 | `measure` L230 | `met_target = mismatches == 0 and guards_ok` → `mismatches == 0` (guards_ok dropped) | `a325a91ce5b8` | exit 1; killed by `unresolved pointer deleted (fewer pointers)` and `substituted by other document` (both want 1 got 0) | **killed** |
| m02 | `measure` L228 | `guards_ok` expression `total >= base_total` → `total > base_total` | `50da5f876014` | exit 1; killed by `green: repaired by document` (want 0 got 1; green has total == base_total == 6) | **killed** |
| m03 | `measure` L222 | repair test `…endswith('/' + path)` → `os.path.basename(p2)==os.path.basename(path)` | `a33560b681d3` | exit 0; `cases 13, green_ok 1, red_ok 12, failures []` | **SURVIVED** |
| m04 | `resolves` L115 | `return 1 <= lo <= hi <= cache[p]` → `return True` (range check skipped) | `636830be7bb7` | exit 1; killed by `range beyond file` (want 1 got 0) | **killed** |
| m05 | `measure` L186 | Adjacent stop rule `startswith('#')` → `startswith('## ')` (runs through `### Sub`) | `bc7c346d93ab` | exit 1; killed by `green` and `adjacent range wrong` | **killed** |
| m06 | `section` L45–46 | heading absent → `return lines` instead of `None` ("absent → match") | `6f5adf9015d6` | exit 0; `failures []` | **SURVIVED** |
| m07 | `measure` L197 | O1 count regex `(\d+)/(\d+) knowledge files mapped` → `(\d+)\s*(?:/|of)\s*(\d+) …` (regex relaxation) | `61853b8f129b` | exit 0; `failures []` | **SURVIVED** |
| m08 | `units` L77–78 | Capabilities table-end `elif started: break` → `pass` | `1c5f7c4f62cf` | exit 0; `failures []` | **SURVIVED** |
| m09 | `units` L85 | SHONEN continuation `l.startswith('  ')` → `l.startswith(' ')` | `380ce315dc1a` | exit 0; `failures []` | **SURVIVED** |
| m10 | `resolves` L107 | existence check dropped: `if not p or not exists(...)` → `if not p:` | `0200cc82059c` | exit 1; killed by `substituted by other document` and `new unresolved pointer` (both want 1 got 0) | **killed** |
| m11 | `measure` L212 | `missing_units = sorted(set(B) - set(U))` → `[]` (unit-census guard emptied) | `1b56320d7381` | exit 0; `failures []` | **SURVIVED** |
| m12 | `measure` L230 | `mismatches == 0` → `mismatches <= 1` | `60b9b70ca00d` | exit 1; killed by 7 cases (`junk count`, `count deleted`, `adjacent range wrong`, `range beyond file`, `new unresolved pointer`, `calibration count wrong`, `SHONEN rule count wrong`) | **killed** |
| m13 | `measure` L229 | `mismatches = len(unresolved) + len(failed)` → `len(failed)` (unresolved dropped) | `a1078d761cd3` | exit 1; killed by `range beyond file` and `new unresolved pointer` | **killed** |
| m14 | `units` L68 | owned header skip `first_cell(l) != 'Axis'` → `!= 'axis'` | `557a8fe21d74` | exit 0; `failures []` | **SURVIVED** |

Expected-vs-actual: all 14 verdicts matched pre-registered predictions (recorded before running; predicted survivors m03/m06/m07/m08/m09/m11/m14, killed m01/m02/m04/m05/m10/m12/m13). No inconclusive results.

## Real-lane shortcut each survivor would admit (P36-C2, frozen sentence)

- **m03 (basename repair match).** The "repaired by a resolving pointer to the same document" clause is enforced only by directory-suffix equality. A base-unresolved pointer such as `ScoutSkillPlacement.md` (SHONEN box 4's base defect) could be "repaired" by a pointer to a *different* file that happens to share the basename, e.g. `docs/archive/ScoutSkillPlacement.md` — the counter would pass it. The selftest only probes substitution by a different-basename document (`d/y.md` for `x.md`), so this shortcut is unguarded.
- **m06 (absent heading matches whole file).** Deleting or renaming the `## Owned axes` / `## Capabilities` headings: pristine `section()` returns `None` → units vanish → `missing_units` guard fails → red. The mutant scans the whole SCORECARD, finds the same rows, reproduces identical unit keys → green. Headline structure of the self-assessment surfaces can be destroyed without a mismatch.
- **m07 (count-regex relaxation).** The coverage row's stated count may drift off the frozen format (`3 of 3 knowledge files mapped`, `3 / 3 …`): pristine parses nothing (stated `None` → assertion mismatch → red); the relaxed regex parses it and compares numbers only. Count-string format drift on the live SCORECARD is admitted as long as the digits are right — i.e. the surface can be rewritten in a deviant syntax without detection.
- **m08 (no table-end break).** Rows below the first non-`|` line of the Capabilities section stop being units in pristine code. A lane could move the real capability row below an interleaved prose line (unit disappears → `missing_units` → red in pristine) or append junk pseudo-tables after the table (pristine stops at the break; mutant absorbs them as capability rows). Table placement/structure drift is admitted.
- **m09 (one-space continuation).** SHONEN box payload lines indented with one space are ignored by pristine (stated `None` → red) but attached by the mutant → counts/ranges parse → green. Box payload formatting drift (the two-space continuation rule) is admitted.
- **m11 (unit census emptied).** `missing_units` is the *only* guard over a unit that carries no counted assertion and no pointer delta — concretely a Capabilities row without backticked pointers (no O1–O4/R1–R3 check covers it; pointer total unchanged). Pristine kills any unit deletion via `missing_units`; the mutant only catches deletions that also trip a count/range/pointer check. Note the selftest's `box removed` case stays red under the mutant only because R3 redundantly covers BOX4 — deletion redundancy means no case isolates the census guard.
- **m14 (header-row case lock).** The header-skip guard is exact-match `'Axis'`; header-row edits (case drift, or pointers ever embedded in a header cell) silently flip the header between "skipped" and "phantom unit `owned:Axis`". Because guards derive from the same parser, no cross-check exists and no case exercises header recognition — header manipulation is unobservable.

Killed-mutant notes (what the current cases do pin down): m01 shows exactly two cases (`unresolved pointer deleted`, `substituted by other document`) depend solely on `guards_ok`; m02 shows the green case is the only equality-boundary probe for the pointer-count guard; m04/m13 show `range beyond file` is detected *only* by `resolves`' range check; m05 shows both the green and the `adjacent range wrong` cases depend on the `#`-stop rule; m10 shows every extension-less pointer token depends on the `cat-file -e` existence check; m12 shows 7 of 12 red cases carry exactly one mismatch each (good fault isolation). [INFERENCE: real-lane shortcut phrasings map fixture behavior onto the lane surfaces named in the frozen claims; the mutants were only exercised against selftest fixtures.]

## Findings (coverage / calibration axes)

1. **Coverage finding (7/14 survivors).** The 13-case selftest does not constrain: same-basename substitution repair (m03), heading deletion (m06), stated-count format drift (m07), post-table row placement (m08), one-space box continuations (m09), isolated unit deletion (m11), header-row recognition (m14). Each survivor is a counter behavior a future edit could silently break while `--selftest` stays green. These are detector-coverage gaps, not defects in the frozen counter; per the mutation-testing contract the counter/predicate is unchanged.
2. **Calibration observation.** No survivor flipped any existing case's verdict (all survivors are behavior-identical on the fixture set), so no false-positive/false-negative risk was demonstrated *on the 13 cases themselves*; the exposure is the real-lane shortcut set above. m12 additionally shows the red cases are minimal (single-mismatch), so a `<=1` tolerance — the most plausible calibration slip — is caught by 7 independent cases.
3. **Suggested (non-binding) case additions for any future unfreeze**, one per survivor: substitution by same-basename different-directory document; delete a `## ` heading keeping rows; stated count in deviant format; capability row moved below a prose line inside the section; box payload with one-space indent; delete a pointer-less capability row; header-row recognition probe.

## Bounds compliance / restoration evidence

- Lane file untouched: sha256 before `f079aff1…c9b078f` == sha256 after all runs `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f`. All mutation happened on scratch copies.
- No VCS-mutating commands run by this seat (no git add/commit/checkout/reset/stash/pull/push; no jj). The only git invocations were the counter selftest's internal fixture `git -C D init/ls-files/add/commit/rev-parse` inside `S/kaidoku-r36/c2-selftest.*` temp dirs, with its own toplevel equality check.
- No tools installed or upgraded (none needed; pacman untouched). sasquatch not touched. No REA runs (out of scope for this seat).
- Scratch removed: `rm -rf -- /fast/scratch/hyaku/kaidoku-r36/R36MutantC2` → `rm_exit=0`, path confirmed gone. Mutated copies were declared disposable by the tasking scratch rule; the sole evidence artifacts (outputs, hashes) are embedded above.
- Files written: only this report (`​.ufo/waves/round-36/w1/R36MutantC2.md`).
