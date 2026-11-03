# ExecMatrixRun — R64-C1 frozen 18-run matrix (scoped result)

Seat: ExecMatrixRun (leaf, w1). Ran the frozen instrument **once**, end to end, with the counting command.
No instrument or claims edit; no second run.

Instrument: `tools/round-64/jsc-route-matrix.py`
sha256 before `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`
sha256 after `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` — equal, equals the frozen pin.

## Result

| field | value |
|---|---|
| exit | **0** |
| runs_matching / runs_total | **18 / 18** |
| mismatches | **none** |
| verified | true |
| stderr | 0 bytes |
| wall time (shell job, pins + 18 cells) | 383.54 s |
| `--skip-run` | false |

Every pin re-checked equal before the run (probe, typora, D1/D2/D3 d8, D1 snapshot_blob.bin, D1 icudtl.dat,
View8 view8.py); independent `sha256sum` record in `ExecMatrixRun/pins-pre.txt`.

Labels, all 3 reps identical per cell:

| cell | predicted | observed |
|---|---|---|
| probe\|D1 | dump-ok\|view8-ok\|node-fail | matches (2882 B dump, 213 B View8, node-fail) |
| probe\|D2 | dump-ok\|view8-ok\|node-fail | matches (2882 B / 213 B) |
| probe\|D3 | dump-exit-139\|view8-skipped\|node-skipped | matches (SEGV, 0 B stdout) |
| typora\|D1 | dump-exit-134\|view8-skipped\|node-skipped | matches (libc++ `__n < size()` → SIGABRT) |
| typora\|D2 | dump-exit-134\|view8-skipped\|node-skipped | matches (same assertion) |
| typora\|D3 | dump-exit-134\|view8-skipped\|node-skipped | matches (same assertion) |

The two cells unobserved before the freeze (`probe×D2`, `typora×D2`) both reproduced their predictions.

Observation worth carrying: probe dumps are 2882 B on every rep but not byte-identical — diffs are confined
to heap/pointer-cage addresses (same opcodes, offsets, sizes); View8 output is 213 B and differs the same way.
The pre-freeze `l1/prefreeze-probe/dump-probe.txt` (2882 B, sha256 `cd06b72a…`) differs from the matrix dumps
in exactly the same address literals. The predicate counts labels, so 18/18 stands; the per-cell dump copies
are not byte-stable receipts.

## Files written (inside the seat paths)

- `.ufo/waves/round-64/w1/ExecMatrixRun.md` (this report)
- `.ufo/waves/round-64/w1/ExecMatrixRun/findings.md` (full receipts table, observations, scope)
- `.ufo/waves/round-64/w1/ExecMatrixRun/matrix-run.json` (3,970 B, sha256 `c65f81b5…`) and
  `matrix-run.stdout` (identical bytes) / `matrix-run.stderr` (0 B)
- `.ufo/waves/round-64/w1/ExecMatrixRun/pins-pre.txt`, `instrument-post.txt`
- `.ufo/waves/round-64/w1/ExecMatrixRun/cells/<artifact>-<build>-r<rep>/`: 6 × `dump.txt` (2,882 B),
  6 × `reconstruction.js` (213 B), 12 × empty `dump.txt` (0 B); no file hit the 2 MB cap

Scratch `/fast/scratch/hyaku/kaidoku-r64/ExecMatrixRun` deleted after copying the cells. No tool installs.
No git mutation. No re-run.

## Risks

- Only label classes are frozen; the exact dump/reconstruction bytes vary per process (ASLR). A future check
  that compares dump bytes instead of labels would fail spuriously against the pre-freeze receipt.
- `node --check` and `parse` versions are not pinned by the instrument (node v24.21.0, parse 1.22.4 used here);
  a future node that accepts pseudo-Ignition text would change the `node-*` label without a pin failing.
- Nothing found that requires an edit to the instrument or the claims file.
