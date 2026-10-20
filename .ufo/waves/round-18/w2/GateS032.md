# GateS032 — falsify routed-defects.py R17-S032-DIGEST check set

**VERDICT: BROKEN** — the R17-S032-DIGEST check set validates shape, not substance. Both disjuncts demonstrated with reproducing commits: (1) the defect flips closed at baseline with two fabricated files and zero real work; (2) at the delivered revision the defect class is re-introduced by a one-token edit while the tool still reports `open_count: 0`.

Axes worked: calibration (tool verdict vs. reality), operability (every finding has a paste-able command), depth (4 distinct commits + 2 function-level observations).

## Setup (observation)

```
d=$(mktemp -d /tmp/gates032.XXXXXX) && git clone --no-local --quiet /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$d/clone" && git -C "$d/clone" remote remove origin
# → exit 0; clone at /tmp/gates032.7k6xvj/clone (origin removed; no jj commands; no writes outside clone+report)
```

Tool under test, run read-only against the clone only:
`python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev <REV>` (exit 0 both times below).

- At baseline `9011581d`: R17-S032-DIGEST **open** (all 3 checks fail), `open_count: 6`.
- At REV `b2aad08c`: R17-S032-DIGEST **closed**, `open_count: 0`.

The wave-1 fix (commit `b2aad08c`, "pre-falsify") added the S033 superseding row (`corpus/SOURCES.md:39`) and the evidence file `.ufo/waves/round-18/evidence/s032-digests.json`. **The S032 row itself is byte-identical between baseline and REV** — `diff <(git show 9011581d:corpus/SOURCES.md | grep "^| S032") <(git show b2aad08c:corpus/SOURCES.md | grep "^| S032")` → `IDENTICAL`, exit 0. It still reads "page sha256 `436c0f63…`" with no fetch-time qualification (`corpus/SOURCES.md:38`, cells[5]); the closure rests entirely on supersession.

## Check surface (observation, routed-defects.py at REV)

- `routed-defects.py:706-714` `_s032_superseding_rows`: scans **every** `|`-leading line of the whole file (not the registry table); requires 11 cells, cells[6] starting `"supersedes S032 —"`, `"fetch-time"` anywhere in cells[5]. Row id, tier, and the other 9 cells unconstrained.
- `routed-defects.py:739-745` `s033-anchor-commit`: passes if cells[5] contains **any** 40-hex substring — never checked against git objects, the PR, or the repo.
- `routed-defects.py:760-778` `s032-digests-evidence`: passes if the JSON parses and ≥2 distinct 64-hex strings appear **anywhere** in it — content never cross-checked.
- `routed-defects.py:187-195` `_defect`: open = any named or substance check failing; closed requires both green.
- The tool's own closed fixture uses fabricated constants (`routed-defects.py:947-948`: `{"page_digests": ["1"*64, "2"*64]}`), and its token-only mutations test removal (`:1108-1116`, `:1222-1223`), not fabrication — shape-only validation is by design [INFERENCE from fixture text].

## Findings

### F1 (disjunct 1 — cheapest flip-closed, no fix): commit `f46bda6` on baseline
Diff (+9 lines, 2 files; S032 row untouched — defect not fixed):
```
 corpus/SOURCES.md                              | 2 ++
 .ufo/waves/round-18/evidence/s032-digests.json | 7 +++++++
```
- `corpus/SOURCES.md:69` (appended at EOF, **outside the registry table**, under "## Leads (unopened)"): `| S033 | fabricated-anchor | docs | A | no fetch performed | fetch-time only; anchor commit `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` is fabricated | supersedes S032 — digest was fetch-time only | mined | 2026-10-20 | 90d | none |`
- `s032-digests.json` (new): `{"note": "...no fetches were performed...", "page_digests": ["0"*64, "1"*64]}` — same shape as the tool's own selftest fixture.

Reproduce: `git -C /tmp/gates032.7k6xvj/clone checkout -q attackA && python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py --root /tmp/gates032.7k6xvj/clone --rev f46bda68f09480b9c0e3d701415eda557a8a3c49` → exit 0:
```
named superseding-row ok=True | row S033: teaches='supersedes S032 — digest was fetch-time only'
substance s033-anchor-commit ok=True | row S033 anchor pins a 40-hex commit
substance s032-digests-evidence ok=True | 2 distinct 64-hex page digests
S032 open: False ... open_count: 5   (was 6 at baseline)
```
R17-S032-DIGEST is counted closed at a revision whose only new content is fabricated. [Observation: tool output; the "no fix" claim is the diff itself.]

### F2 (disjunct 2 — cheapest re-open-while-closed): commit `7f5e864` on REV, one token
Diff: `corpus/SOURCES.md:39`, anchor cell: `head commit `a214355498e84aa86280be0c31c955aaf94f2d12`` → `head commit `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`` (1 line changed).
The row continues to assert "(`git ls-remote … refs/pull/9348/head`, 2026-10-20T15:38Z)" for a hash that is not any git object: `git cat-file -t deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` → exit 128, "could not get object info". [Observation]
Reproduce: `git -C /tmp/gates032.7k6xvj/clone checkout -q attackB && python3 -I -B …routed-defects.py --root /tmp/gates032.7k6xvj/clone --rev 7f5e8644489c43d647a5dac447bec8701e68609e` → exit 0: all three checks ok, `open_count: 0`.
The row now keys the PR on a fabricated identity — the exact defect class S032 routed (asserting an unverifiable identity as anchor) — while the tool reports closed. [The class judgment is inference; the green output and the cat-file failure are observations.]

### F3 (disjunct 2 — evidence destroyed): commit `9ad52ae` on REV
Diff: `.ufo/waves/round-18/evidence/s032-digests.json` 5(+)/21(−) — all real fetch evidence (9 page digests, patch digests, pull head, seat observations) replaced by two fabricated constants.
Reproduce: `git -C /tmp/gates032.7k6xvj/clone checkout -q attackC && python3 -I -B …routed-defects.py --root /tmp/gates032.7k6xvj/clone --rev 9ad52ae18973b757ad52a1937e6c7b6a11609d52` → exit 0: `s032-digests-evidence ok=True | 2 distinct 64-hex page digests`, `open_count: 0`. [Observation]
The fetch-time-only qualification in S033 now rests on evidence that no longer exists; tool says closed.

### F4 (disjunct 2 — structural gaming): commit `afbe50b` on REV
Diff: `corpus/SOURCES.md` 3(+)/1(−): the real S033 row's teaches cell prefix `supersedes S032 — ` stripped (registry no longer contains any superseding correction) and the F1 fake row appended at EOF (line 79, outside the table).
Reproduce: `git -C /tmp/gates032.7k6xvj/clone checkout -q attackD && python3 -I -B …routed-defects.py --root /tmp/gates032.7k6xvj/clone --rev afbe50b1731153bae1418ac1cebb4b7a84d1654e` → exit 0: `named superseding-row ok=True | row S033: teaches='supersedes S032 — digest was fetch-time only'`, `open_count: 0`. [Observation]
Proves the named check is a file-global text scan unbound to the registry table or the real row.

### Function-level observations (no commit needed)
- `m._hex64s_in({"s032_recorded_digest": "436c0f63…", "arbitrary": "f"*64})` → 2 distinct → the `s032-digests-evidence` threshold is met by the **unreproducible digest itself** plus any constant. [Observation via importlib on routed-defects.py]
- The 40-hex anchor check would equally pass with the 40-hex prefix of the 64-hex patch digest or any embedded hex run flanked by non-hex chars — shape, not identity. [Observation of `_HEX40` at `routed-defects.py:31` + `:739`]

## Cheapest commit (answer to the target)

- Disjunct 1: **`f46bda6`** (F1) — 9 fabricated lines on baseline, S032 counted closed, defect untouched.
- Disjunct 2: **`7f5e864`** (F2) — one-token substitution on REV, defect class re-introduced, tool still `open_count: 0`.

## Residual risk / verification gaps

- I did not audit whether any *other* lane instrument (verify.py, citation-drift-probe, receipt-validate) would catch the fabricated anchor or digests; C1's stated falsifier is routed-defects.py alone, and that instrument is gamed. [INFERENCE, scope-bounded]
- Minimal hardening directions (not implemented, out of a falsifier's write scope): resolve the anchor 40-hex with `git cat-file -e <hash>^{commit}` or bind it to the recorded `pull_head` in the digests JSON; require the superseding row inside the `## Registry` table with row-id continuity; pin the digests JSON's own blob hash at a frozen rev or re-derive ≥2 digests from a retained command transcript.
- No tool installs were performed (none needed). Lane untouched except this report; all git writes happened inside `/tmp/gates032.7k6xvj/clone` (origin removed at creation; branches attackA–attackD local-only).

Report: .ufo/waves/round-18/w2/GateS032.md
