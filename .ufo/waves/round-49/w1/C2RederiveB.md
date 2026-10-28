# C2RederiveB — independent re-derivation of C2 atoms A4–A6 (pre-freeze, wave 1)

**Verdict: no disagreement. A4, A5 and A6 as drafted (docstring, counter code, `c2-after.py` GREEN fixture lines) match my independent derivation byte-for-byte.** Two low-severity looseness notes in the A6 code, nothing vacuous in A4/A5. I did not import or run `c2-mismatch.py`; the derivation is `w1/C2RederiveB/rederive.py` (stdlib, reads git objects at base `e4f2cfa5…` plus the committed draft snapshot, writes nothing).

Run: `cd w1/C2RederiveB && python3 -I -B rederive.py > rederive.out` — exit 0, 2026-10-28T21:10:36Z, stdout sha256 `b60bec66f3632aea0c2ceb2155b26057c9f5c4830e73ec403fcb84d5696fefe7` (`rederive.out` beside it).

| Atom | Derived value (command / source) | Draft says | Agree |
|---|---|---|---|
| A4 seats | `results.json` (`git show e4f2cfa5:.ufo/waves/round-48/r48-w1-results.json`): top-level `seats` 75, `len(results)` 75, 75 unique names | `seats=75` (`c2-after.py:30`) | yes |
| A4 reports | 72 seats have a `.md` at `w1/<seat>.md` or under `w1/<seat>/` (68 top-level `.md`; 4 dir-only: C1IdsArms/report.md, C2Quote/report.md, C2Gold/report.md, ExecGateRun/ExecGateRun.md). Strict variant (depth-1 only) gives the same 72 | `reports=72` | yes |
| A4 missing | C1Battery, C1Meaning, ScribeReportNumbers. C1Meaning has a dir with only `receipt.json`; C1Battery has no `.md` anywhere (`C1Battery-2/` = receipt.json only; `C1Battery-2` is not a seat, `LabC1Meaning(.md)` is not a seat); ScribeReportNumbers has nothing. The `w1` tree has 494 files at base | `missing=C1Battery,C1Meaning,ScribeReportNumbers` (counter compares sorted sets) | yes |
| A4 vs closure | closure "Routed defects" 7: "72/75 … C1Meaning, C1Battery and ScribeReportNumbers" | same | yes |
| A5 c1 raw / stripped | `git show e4f2cfa5:…/c1-final-33f65a91.json \| sha256sum`: raw `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e`, stripped (one trailing `\n` removed) `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77`; 2589 B, ends `\n` | counter derives the same way (`b[:-1]` if endswith `\n`) | yes |
| A5 c2 raw / stripped | raw `d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914`, stripped `c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8`; 2710 B, ends `\n` | same | yes |
| A5 report quote | fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kaidoku.md` lines 34/35 quote the full **stripped** digests (`3cc2d72d…`, `c30628ae…`); neither raw digest appears anywhere in it. So `report_c1=3cc2d72d report_c2=c30628ae` (stripped[:8]); the counter's test `stripped[:8]==q and raw[:8]!=q` is satisfiable only by the right answer | `report_c1={c1s[:8]}` | yes |
| A6 snapshot | `sha256sum …/draft/snapshots/popper.html` = `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`, 118135 B — equals the S145 row pin and the closure's re-fetch | pin in S147 anchor | yes |
| A6 quote | present exactly once (tag-tolerant search, text-level count 1). Raw HTML is `…take <em>falsifiability</em> as his criterion…` so a naive raw-byte `grep` finds 0; needs tag stripping (the counter's `html_norm` does). 21 whitespace tokens (≤25). Continues `…it is scientific; conversely, a theory which is compatible with all such observations, either because…, is unscientific.` (the full clause is >25 words, so the draft's truncated quote is the right choice) | `q1` in `c2-after.py`, "(21 words)" | yes |
| A6 heading | nearest heading above (raw offset 20949): `<h2 id="BackPoppThou">2. Backdrop to Popper&rsquo;s Thought</h2>` (offset 17272); it is an **h2**, no h3 between; headings above: h1 Karl Popper, h2 `1. Life`, h2 `2. Backdrop…`. Next heading below is h2 `3. The Problem of Demarcation` at 21661, 712 B after the quote. Unescaped heading contains U+2019 (curly) | S147 anchor `2. Backdrop to Popper’s Thought` (curly) | yes |
| A6 S145 | base row S145 anchor `2. The Problem of Demarcation`, quote 22 words, pin same sha — the wrong locator the closure routed (§2 is Backdrop; Demarcation is §3) | S145 left byte-identical, S147 supersedes | yes |

## Looseness in the A6 code (not disagreements; fold or ignore)
1. `a6` (c2-mismatch.py:403-405) checks `head in c[5]` only: an anchor naming **both** `2. The Problem of Demarcation` (the old wrong locator) and the right heading passes. Nothing asserts the wrong locator is absent from S147's anchor. The mutation "anchor names the wrong section" only catches replacement, not addition.
2. The heading match is a substring on the unescaped text, so it requires the curly `’` (U+2019). An anchor typed with straight `'` goes red with message `(2. Backdrop to Popper’s Thought)`. Not vacuous — the landing text must copy the curly form (`c2-after.py` does).
3. The "(N words)" parenthetical in the anchor is not cross-checked against the real count (only the ≤25 bound is). Minor.
4. Page revision stamp in the snapshot: `First published Thu Nov 13, 1997; substantive revision Fri Jul 31, 2026` — the closure asked for a version/publication anchor; S147's drafted anchor has only the sha256 + access date. Optional to add.

## Not run
Did not run `c2-mismatch.py`, `mkclone.sh`, or any green/red fixture. No tool installed. Scratch `/fast/scratch/hyaku/kaidoku-r49/C2RederiveB` removed.
