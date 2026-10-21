# ResC2Gate-2 — R24-C2 freeze-gate / claim-freezes.tsv falsification (lane 69e82c48)

Seat: KagiR27-2.ResC2Gate-2 (critic, read-only). Scratch: `/fast/scratch/kaidoku-r24/seats/ResC2Gate-2`
(independent deriver `rederive.py`, gate outputs, patched-gate probe). No installs or updates.

## Verdict

**No disagreement on any of the 11 ledger rows. Round-24 CLEAN holds on the real history. The
supersession 9fb4eacd is honest, with one consequence it does not state. The gate itself is
falsifiable: falsifier #1, "instrument absent at freeze reported CLEAN", can be reached with
inputs that follow the lane's own `<LANE>/` convention.** That last point is a fixable defect for
the gate going forward. It does not reach the r14–r24 verdicts, because no historical claims list
uses a form the gate cannot see. I do not call the round verified.

## Findings

### F1 — independent re-derivation agrees 11/11 (observation)
The tool is `rederive.py`, written without the gate's code. For each freeze it takes the first
`--diff-filter=A` commit. It then reads every string in the frozen file, including top-level keys,
with a wider script-token regex (py/sh/mjs/cjs/js/ts/rs/bash/jq/awk/pl/rb, any prefix). For each
token it checks: exact blob at the freeze commit, basename candidates, sha256 against the pin, and
`rev-list freeze..69e82c48`. Every round has exactly one add and no delete.

| round | freeze | re-derived | ledger |
|---|---|---|---|
| r14 | 3e99fbd6 | claims list names no script → NONE | agree |
| r15, r16 | 856d193b, 27b8fc13 | no script token anywhere → NONE | agree |
| r17 | 27116747 | 4 bare names → UNRESOLVED | agree |
| r18 | eb6c2668 | 4 bare names in claims → UNRESOLVED | agree |
| r19 | 85589ac7 | c1-census-v10 present, unpinned, revised once (808cbb31). province-pins (2 later commits) and routed-r18 (4 later commits) absent. `tools/swiss-misread.py` never at that path (the file is `.ufo/waves/round-18/tools/swiss-misread.py`) | agree |
| r20 | d1d981d2 | c1-census present, unpinned, revised once. Revisions after freeze: measure.py 2, routed-r19.py 6, verb-coverage.py 3; all three absent at freeze | agree |
| r21 | f4e95af9 | battery.py absent at freeze, then fe11e4df | agree |
| r22 | 75f04a44 | both counters present, unpinned, then 2ee3d9f5 and e9db7e2d | agree (see F5) |
| r23 | a3c92eb6 | count-c1.py absent at freeze, then 2b40aec5, 9d64b953, fe18f13f | agree |
| r24 | 5dc49bfe | both instruments are blobs at 97ade2e5, the parent of the freeze. Pins equal the blob sha256 (count-c1 f1859605…, gate 1e2a9370…). count-c1 has no later commit. The gate's only later commit is 9fb4eacd, which is disclosed. | CLEAN, agree |

Command `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root . --rev 69e82c48 --require-clean round-24 --disclosures corpus/claim-freezes.tsv` exited 0: exact 11/11, no strays.

Side notes, none of which changes a verdict:
- r14's top-level `before_census` names `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. It is outside the lane and outside `claims`, and it is a precondition census rather than a claim instrument.
- Resolving the r17/r18 bare names by basename finds a unique file for 7 of the 8. The exception is `verify.py`, with 5 candidates at freeze. All 8 are unpinned, and 6 were revised after freeze (for example `routed-defects.py`: b2aad08c, db4bdb16, 4f6c73f8). `UNRESOLVED` is consistent with the gate's definition but understates these files' actual state.

### F2 — supersession 9fb4eacd is honest (observation, one inference)
- The disclosed path, commit and sha256 `8a71fe84…` equal `git show 9fb4eacd:…freeze-gate.py | sha256sum`, and also equal the working-tree file.
- The diff of 97ade2e5 against 9fb4eacd only adds `BARE` / `INSTRUMENT_UNRESOLVED` and a summary key. The pin, disclosure and revision logic is untouched.
- "Changes only r17/r18 NONE→UNRESOLVED" holds:
  - At fe10219: `before-c2.json` (frozen gate) and `before-c2-rev1.json` (revised gate) differ only in the r17/r18 codes. Both exit 1 with 0/10 disclosed.
  - At 69e82c48: running the frozen gate and the revised gate gives verdicts equal everywhere, and codes that differ only for r17/r18.
- "Recorded before any after-measurement": the git reflog and `jj --ignore-working-copy op log` are consistent with this. `corpus/claim-freezes.tsv` first appears in the snapshot at op 6bd0da50 (13:58:59), after the 9fb4eacd commit (13:54:36). jj snapshots only at commit times, so this is unfalsified, not proven.
- **Unstated consequence:** the frozen gate run at 69e82c48 against the committed ledger exits **1**, with exact 9/11 and r17/r18 mismatched (`$S/gate-orig-head.json`). The target text is unchanged, as the reason says. But the claim passes only under the revised instrument, because the ledger was written to it. [INFERENCE] The pass depends on how the ledger was authored, not on any gate weakness: a ledger with NONE rows would pass under the frozen gate.

### F3 — falsifier #1 reachable: absent or unpinned instrument reported CLEAN (observation, clone)
In a clone, a synthetic `round-25` claims file names one pinned script normally. A second string
names another script in one of 9 forms. In every case the round came out CLEAN.

The forms were:
- `./.ufo/…/v2.py`
- `/home/…/kaidoku-shokunin/.ufo/…/v3.py`
- `$LANE/.ufo/…`
- `<LANE>/.ufo/…`
- `scripts/hid.py`
- `.ufo/…/h.ts`
- `python3 -m tools.v5`
- a directory argument
- `v7.PY`

The case `python3 <LANE>/.ufo/waves/round-25/tools/never-committed.py`, a script that was never
committed, also came out CLEAN. Run with `--require-clean round-25`, it gave `required_failed []`
and exit 0.

**Cause:** both `SCRIPT` and `BARE` have a `(?<![…/…])` lookbehind, so any path that has a prefix,
or sits after a `/`, is invisible to both regexes.

**Scope:** the gate's limits clause only excludes paths "named only in prose outside claims.json".
These names are inside claims.json. `selftest.py` has no case for any of these forms (searched:
nothing found).

### F4 — gate accepts any disclosure entry and does not see claims-text edits (observation, clone)
- **CE-A:** I appended a revision of count-c1.py, then added a supersession entry with the real commit, `sha256: "00"` and `reason: "x"`. Result: CLEAN, 11/11, exit 0. The sha256 field is never checked, and any non-empty reason is accepted.
- **CE-B:** I weakened the r24 target and the C1 total after freeze, without disclosing it. Result: CLEAN.

For the real r24, the claims.json diff 5dc49bfe..69e82c48 only appends `instrument_supersessions`, and the disclosed sha256 is correct. So neither case harms round 24.

### F5 — QUALITY33 "committed before its claims file" is not enforced (observation)
The gate tests whether an instrument is present at the freeze commit, not whether it was present in
the freeze commit's parent. So an instrument added in the same commit as the claims file passes:
the clone test gave CLEAN.

In real history, r22's `count-c1.py` and `count-c2.py` were **added in the freeze commit 75f04a44**
and are absent in `75f04a44^`. The r22 ledger row ("both counters present at freeze") is true but
omits this. Its verdict stays FLAGGED. For r24, the instruments are in the parent (97ade2e5), so r24
meets this rule.

### F6 — scope and provenance gaps around "round-24 CLEAN" (observation)
- `.ufo/waves/round-24/tools/run-rea.py` is the C1 producer named in `tool-pins.json:41`. It has no sha256 pin anywhere and is not in claims.json `instruments`, so CLEAN does not cover it. It is unchanged since 97ade2e5; its current sha256 is `3fe771ae…`.
- `.ufo/waves/round-24/tools/selftest.py`, the L1 selftest, is **untracked** at 69e82c48 and not ignored, so it cannot be audited from Git. Its current sha256 is `4d7cf12d…`.
- Twelve retained `.ufo/waves/arc3-loop1-round{1..12}/claims-frozen.md` freezes are outside the gate's `round-*/claims.json` scope. Three of them name scripts (rounds 2, 6, 7: c1-census-v10.py, scope-diff.py). The scope "(r14..r24)" is stated, but neither the lesson nor the ledger says these freezes were excluded. Lesson line 43 ("the lane's freezes did not, by themselves, fix the instrument") reads as if it covers all freezes. This bears on the falsifier "historical freeze silently skipped".

Impacted axis: calibration.

## Recommended L1 action

1. **Keep R24-C2 at 11/11 exact and round-24 CLEAN** on the current data: F1 and F2 found no disagreement.
2. **Add one sentence to the supersession reason or lesson**: the frozen gate run at the final revision against the committed ledger exits 1 (9/11, r17/r18). This is F2.
3. **Route a gate supersession 2 to the next round** rather than revising after measurement. It needs four parts:
   - Strip `./`, `<LANE>/`, `$LANE/` and the absolute lane root before path matching.
   - Treat any other script-extension token (any prefix, any case, plus ts/rs/cjs/bash/pl/rb) as `INSTRUMENT_UNRESOLVED`.
   - Add `INSTRUMENT_NOT_PRIOR` when the blob in `freeze^` differs from the blob at freeze.
   - Check that each disclosure's `sha256` equals the blob at its commit.

   I probed this in `$S/gate-patched.py`:
   - At 69e82c48 every verdict is unchanged and round-24 stays CLEAN.
   - The only code change is that r22 gains `INSTRUMENT_NOT_PRIOR`, so that ledger row would need updating.
   - It catches 7 of the 9 blind forms. `-m module` and directory arguments stay uncovered and must be stated as limits.
   - Add selftest cases for each of these.
4. **Commit or pin `selftest.py`, and pin `run-rea.py`'s sha256 in `instruments`** (F6). Then state the arc3 `claims-frozen.md` exclusion explicitly in the lesson and the ledger header prose.
