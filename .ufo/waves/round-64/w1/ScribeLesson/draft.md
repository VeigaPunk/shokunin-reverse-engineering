# ScribeLesson — r64 w1: lesson `## Mistakes` rows and one QUALITY candidate

Read-only survey of bytes already on disk; no instrument run, no fixture, no scratch, no writes
outside this directory. Lane working tree clean for `corpus/QUALITY.md`
(sha256 `f0d8e5df7a77166399c3a1ec5d3522929951a02050d7f494b343e73ee30c1d80`).

## 0. Numbering measured before drafting

`grep -E '^\| [0-9]+ ' corpus/QUALITY.md` lists table rows 1–74 and 77–93. The appended correction
blocks (`## Corrections appended — round 20 wave 2`, lines 116–133; `## Corrections appended —
round 34 run-6`, lines 133–162) carry list-style rows 75–79 and 94–101. Highest number used
anywhere in the file: **101** (`grep -c 'Row 101' corpus/QUALITY.md` → `1`).
**Next free number: 102** (`grep -n 'Row 102' corpus/QUALITY.md` → no match at this read).

The seat brief said the criteria "run to #74"; #74 is only where the *table* stopped before rows
77–93 landed. Measured highest is 101, so the candidate below is #102, not #75.

## 1. Mistakes rows — verbatim, for `corpus/lessons/round-64.md` `## Mistakes`

Header to match the lane's file:
`| id | class | evidence pointer | captured-by | fix / demonstrated limit |`

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M64-1 | stale premise / scope — the staged entry's caveat calls the View8 output "approximate JavaScript" and warns only that variable names and control flow may differ, but the probe run's output is not parseable JavaScript at all; the round's own frozen `PREDICTED` table already labels the probe cells `node-fail`, so the entry is behind the freeze it sits beside | `.ufo/waves/round-64/l1/prefreeze-probe/view8-probe.log` (View8 exits 0 and prints "Parsing completed successfully." then "Decompiling 1 functions." then "Done.") against `.ufo/waves/round-64/l1/prefreeze-probe/probe-view8.js:3` (sha256 `c9a0965c8590bcefe3969b84d371bae041c049f99f90da51a1c86712ad730135`), where `node --check` exits 1 with `SyntaxError: Unexpected token ':'` at `ConstPool[0:0x311d0101e235 <FixedArray[4]>]`; the stale premise is `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md` § Claim, which reads the README's "JavaScript 近似源码" as a caveat about naming and control flow only; the same freeze predicts the failure — `tools/round-64/jsc-route-matrix.py:69-76` has probe D1 and D2 as `dump-ok`, `view8-ok`, `node-fail` | none — no QUALITY criterion requires a parser verdict on a reconstruction claim: #5 (`corpus/QUALITY.md:15`) makes decompiler output inference and #79 governs a predicate over its own candidate, and neither admits or rejects a claim on whether the emitted text parses; drafted as #102 below | QUALITY #102 (§ 2), plus the entry correction it implies: `jsc-mapper-cli-contract.md` must state that the reconstruction is not syntax-valid on the probe run (`node --check` exit 1) instead of leaving "approximate" to carry it; the r64 claim needs no change — its predicate scores the frozen labels and `node-fail` is one of them |
| M64-2 | process — the frozen pin check verifies bytes, not executability and not the runtime data files of two of the three builds, so a binary whose sha256 matches while it cannot run is reported as a dump failure of the artifact rather than as an environment defect | `tools/round-64/jsc-route-matrix.py:147-165` (`check_pins`) compares `sha256_file` only — comparisons at lines 148, 156, 161, 164; no `os.access(path, os.X_OK)`, no `stat().st_mode` — and lines 158-163 pin `snapshot_blob.bin` and `icudtl.dat` for D1 alone, so D2 and D3 carry no pin on the files they need at runtime although all three directories hold both (`ls` of each toolchain dir); the exit-126 and missing-`icudtl.dat` events assigned to this row have no retained receipt in the round tree (`grep -rn 'exit 126' .ufo/waves/round-64` → no match; `grep -rln icudtl .ufo/waves/round-64` → `claims.json`, `w1/ExecMatrixRun/pins-pre.txt`, `gen-w1.py` and the two prompt copies only), and the three `d8` binaries are mode 755 at this read | none — the instrument's 22-case `selftest()` (`tools/round-64/jsc-route-matrix.py:235-292`) covers six `classify_dump` codes, three `classify_view8`, two `classify_check`, two `compose`, six `verdict` and three `check_pins` refusals, and has no executability case and no missing-runtime-file case | record the receipt gap in the lesson — an unretained environment failure is evidence of nothing about the artifact; for a future instrument revision add the candidate case in § 4; `check_pins` stays byte-only for r64 because the instrument is frozen at sha256 `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` and its `PREDICTED` table was written before any run |

## 2. QUALITY candidate — row 102

| 102 | **Row 102 (a reconstruction claim names its output's syntax class and shows a parser verdict).** A claim that a decompiler, disassembler or view8-class tool reconstructs source must name the syntax class of the text it emits and show a parser verdict for at least one run, because a tool that prints a success line and exits 0 over output no parser accepts is evidence about that tool's completeness and not about the artifact's source. | `corpus/lessons/round-64.md`, Mistakes M64-1; `.ufo/waves/round-64/l1/prefreeze-probe/view8-probe.log` (exit 0, "Done.") against `probe-view8.js` sha256 `c9a0965c…`, `node --check` exit 1 `SyntaxError: Unexpected token ':'` | sharpens 5 |

Notes on the row's shape: four columns, as the table has; "sharpens 5" rather than a supersede
because #5's observation/inference labelling stands and this adds a verdict requirement; the lesson
cell cites `corpus/lessons/round-64.md`, which does not exist yet (`ls corpus/lessons` → newest is
`round-63.md`), so the row is inadmissible until that lesson lands with M64-1 in it.

## 3. Commands that resolve each evidence pointer

M64-1 (all read-only; run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`):

```
node --check .ufo/waves/round-64/l1/prefreeze-probe/probe-view8.js; echo "exit=$?"
#   probe-view8.js:3   SyntaxError: Unexpected token ':'
#   Node.js v24.21.0   exit=1        (observed at this seat)
sed -n '1,6p' .ufo/waves/round-64/l1/prefreeze-probe/view8-probe.log
#   "Parsing completed successfully." / "Decompiling 1 functions." / "Done."  (exit 0 path)
sed -n '69,76p' tools/round-64/jsc-route-matrix.py
#   ("probe", "D1"): "dump-ok|view8-ok|node-fail"   and the same for D2
sed -n '1,40p' /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md
#   "JavaScript 近似源码"; caveat text names variable names and control flow only
sha256sum .ufo/waves/round-64/l1/prefreeze-probe/probe-view8.js
#   c9a0965c8590bcefe3969b84d371bae041c049f99f90da51a1c86712ad730135
```

M64-2 (same cwd):

```
grep -nE 'sha256_file|X_OK|os\.access|S_IX|st_mode' tools/round-64/jsc-route-matrix.py
#   5 matches: line 81 (def) plus 148, 156, 161, 164 — all sha256_file; no executability test
sed -n '147,165p' tools/round-64/jsc-route-matrix.py
#   D1-only pin loop over snapshot_blob.bin and icudtl.dat
grep -rn 'exit 126' .ufo/waves/round-64 ; echo "rc=$?"
#   no match (rc=1): the 126 event has no retained receipt
grep -rln icudtl .ufo/waves/round-64
#   claims.json, w1/ExecMatrixRun/pins-pre.txt, gen-w1.py, r64-w1-dispatch.json, r64-w1-spec.json
stat -c '%A %a %n' /home/vgpnk/.local/share/kaidoku-jsc/d8-14.8.178.14/d8 \
                   /home/vgpnk/.local/share/kaidoku-jsc/d8-14.8.178.1/d8 \
                   /home/vgpnk/.local/share/kaidoku-jsc/d8-14.7.173/d8
#   -rwxr-xr-x 755 for all three
grep -c '^        check("\|^    check("' tools/round-64/jsc-route-matrix.py
#   22
```

Numbering (§ 0):

```
grep -E '^\| [0-9]+ ' corpus/QUALITY.md | grep -oE '[0-9]+ ' | tr '\n' ' '
#   1..74 then 77..93
grep -c 'Row 101' corpus/QUALITY.md      # 1
grep -n 'Row 102' corpus/QUALITY.md      # no match
```

## 4. Candidate selftest case for M64-2 (NOT applied — the instrument is frozen)

Proposal only, for a future instrument revision. Order matters: the bytes check runs first so a
wrong binary still reports `pin mismatch d8`, and a right-bytes-unrunnable binary reports an
environment defect instead of being scored as a `dump-exit-126` mismatch.

```python
def check_runnable(d8: Path) -> str | None:
    """Return an error message when a pinned d8 cannot be executed."""
    if not os.access(d8, os.X_OK):
        return f"not executable d8: {d8}"
    return None

# call site, immediately after the sha256 comparison at line 156:
#     if (msg := check_runnable(d8)):
#         return msg

# in selftest(), inside the existing TemporaryDirectory block:
nonexec = Path(scratch) / "d8"
nonexec.write_bytes(b"")
nonexec.chmod(0o644)
check("runnable-not-executable", (check_runnable(nonexec) or "").split(":")[0],
      "not executable d8")
check("runnable-ok", check_runnable(Path(sys.executable)), None)
```

The `icudtl.dat` half is not a selftest case: D2 and D3 need their own pins (`D2-snapshot`,
`D2-icudtl`, `D3-snapshot`, `D3-icudtl`) added to `PINS`, which changes the freeze. That belongs to
a new round's declaration, not to r64.

## 5. Handoff notes for L1

- Row #102's lesson citation (`corpus/lessons/round-64.md`, M64-1) must exist at landing; the lane's
  rule is that every criterion cites the lesson that produced it. Without it, drop the row.
- Numbering collision at this read: `w1/` held only `swarm-registry.json` and no sibling draft
  directory existed, so no other seat was visibly drafting a number. Re-check
  `grep -n 'Row 10[2-9]' corpus/QUALITY.md` at integration; L1 arbitrates.
- Never edit `tools/round-64/jsc-route-matrix.py` to add § 4: its sha256 is the frozen pin.
- M64-1 is not a defect in the r64 claim. The claim's predicate scores the frozen labels, and
  `node-fail` is a frozen label for the probe cells — the matrix is consistent with the freeze. The
  defect is that the staged knowledge entry describes the artefact class as parseable.
- M64-2's 126/ICU details are assigned to this row but unretained in the round tree; the row as
  drafted states what is checkable and names the gap instead of asserting the events.
