# ScribeLesson — round 64 wave w1

Seat: ScribeLesson. Read-only to the lane; the only writes are this report and `draft.md` beside it.
No scratch dir was created (no clone, dump, or fixture); the heaviest command was `node --check` on a
213-byte file, so no disk-guard pass was needed and nothing had to be deleted.

## Behavior

Assigned: draft the round-64 lesson's `## Mistakes` rows (M64-1, M64-2) and one QUALITY candidate
from evidence already on disk, plus, per row, the command that resolves its evidence pointer.

Read (absolute paths, no instrument run):

- `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md` — the staged entry: `jsc2js` → patched d8 dump → customised View8 → "JavaScript 近似源码", caveat limited to variable names and control flow.
- `.ufo/waves/round-64/l1/prefreeze-probe/probe-view8.js` (213 B, sha256 `c9a0965c…`) — View8's output for the probe.
- `.ufo/waves/round-64/l1/prefreeze-probe/view8-probe.log` (sha256 `c94a25a2…`) — exit-0 path: `Parsing completed successfully.` / `Decompiling 1 functions.` / `Done.`
- `.ufo/waves/round-64/l1/prefreeze-probe/dump-probe.txt` (sha256 `cd06b72a…`) — the `Start SharedFunctionInfo` … `End BytecodeArray` dump the log refers to.
- Also read for the rows' pointers: `dump-probe-ctrl.txt` vs `dump-probe.txt` (differ only in heap addresses: `0x311d…` vs `0x0381…`, same `BytecodeArray[43]`), `dump-match.err` (libc++ hardening assertion → signal 6), `dump-typora-x7.err` (same, under `d8-14.7.173`), `dump-probe-x7.txt` (0 bytes), `jsc2js-main.txt` (`01fc264d22055865a460b322399a15d84b71f5aa refs/heads/main`).
- `corpus/QUALITY.md` numbering, and `tools/round-64/jsc-route-matrix.py` `PINS` / `PREDICTED` / `check_pins` / `selftest` (sha256 `29efef4f…`, matching its pin).

Ran (exact, both reproduce their pointer):

- `node --check /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/l1/prefreeze-probe/probe-view8.js` → exit **1**, `probe-view8.js:3 SyntaxError: Unexpected token ':'` at `ConstPool[0:0x311d0101e235 <FixedArray[4]>]` (Node v24.21.0).
- `grep -nE 'sha256_file|X_OK|os\.access|S_IX|st_mode' tools/round-64/jsc-route-matrix.py` → 5 matches, all `sha256_file` (definition at 81; comparisons at 148, 156, 161, 164); no executability test.
- `grep -rn 'exit 126' .ufo/waves/round-64` → no match; `grep -rln icudtl .ufo/waves/round-64` → `claims.json`, `w1/ExecMatrixRun/pins-pre.txt`, `gen-w1.py`, and the two prompt copies only.
- `stat -c '%A %a %n'` on the three `d8` binaries → `-rwxr-xr-x 755` for all three.
- `grep -c '^        check("\|^    check("' tools/round-64/jsc-route-matrix.py` → 22 selftest cases.
- Read-only git: `git -C … status --porcelain -- corpus/QUALITY.md` (empty) and `log --oneline -4 -- corpus/QUALITY.md` (newest `fa4cd112`, "QUALITY row 101").

## Gates

- **Numbering gate.** `grep -E '^\| [0-9]+ ' corpus/QUALITY.md` → table rows 1–74 and 77–93; the appended correction blocks carry list rows 75–79 and 94–101. Highest anywhere = **101**; `grep -n 'Row 102'` → no match. Candidate is **#102**, not #75 — the brief's "#74" is where the table stopped, not the file's highest number.
- **Lesson-citation gate.** #102's "why" cell cites `corpus/lessons/round-64.md` Mistakes M64-1; that file does not exist yet (newest is `round-63.md`), so the row is inadmissible until the lesson lands. Stated in the draft.
- **Freeze gate.** The instrument is pinned at `29efef4f…` and its `PREDICTED` table was written before any run; the drafted selftest case is marked "NOT applied". Nothing in `tools/round-64/`, `plans/round-64-claims.md`, `.ufo/waves/round-64/claims.json` or `corpus/QUALITY.md` was written.
- No git/jj mutation, no network, no pacman, no writes to `~/.local/bin` or the toolchain (read and `stat` only).

## Touched surfaces

- `.ufo/waves/round-64/w1/ScribeLesson/draft.md` (new)
- `.ufo/waves/round-64/w1/ScribeLesson.md` (this report)

## Findings

1. **View8's success is not validity.** `view8-probe.log` exits 0 and prints `Done.` over a 213-byte output that `node --check` rejects (exit 1, `SyntaxError` at line 3). M64-1 as drafted cites both, and the staged entry's "approximate JavaScript" caveat does not cover syntactic invalidity.
2. **The round's own freeze already predicted this.** `tools/round-64/jsc-route-matrix.py:69-76` has probe D1 and D2 as `dump-ok`, `view8-ok`, **`node-fail`**. So R64-C1 is not implicated; the defect is the staged knowledge entry's description, and M64-1 says so explicitly.
3. **The pin check is byte-only and D1-only for runtime data.** `check_pins` (lines 147–165) compares `sha256_file` at 148/156/161/164 with no `os.X_OK` and no mode test, and the `snapshot_blob.bin`/`icudtl.dat` pins apply to D1 alone (line 158) although D2 and D3 hold both files too. A correctly hashed but unrunnable `d8` would surface as a dump-failure mismatch, not as an environment defect.
4. **The 126 / missing-`icudtl.dat` events have no retained receipt** in `.ufo/waves/round-64` (grep commands above), and the three binaries are mode 755 at this read. The M64-2 row therefore states the checkable pin gap and names the receipt gap rather than asserting that the events occurred.
5. **No criterion currently requires a parser verdict on a reconstruction claim**: #5 (`corpus/QUALITY.md:15`) makes decompiler output inference; #79 governs a predicate over its own candidate. That absence is what M64-1's "captured-by: none" rests on, and #102 closes it.

## Out of scope

- The R64-C1 matrix itself (18 cells, pins, verdict) — not run, not scored, not re-predicted here; that is the executor seats' and L1's receipt.
- The instrument's `PREDICTED`/`PINS` values, the claims file and `corpus/QUALITY.md` — read only; a finding that needs an edit is reported, never made.
- Any correction to the staged package under `/home/vgpnk/Projects/shokuknow` — read only, cited as the stale premise.

## Artifacts

- `.ufo/waves/round-64/w1/ScribeLesson/draft.md` — the two Mistakes rows verbatim (5-column lane shape), QUALITY candidate #102 (4-column table shape), per-row resolving commands, the proposed (unapplied) selftest case, and L1 handoff notes.
- `.ufo/waves/round-64/w1/ScribeLesson.md` — this report.
