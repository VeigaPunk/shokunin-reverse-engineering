# ExecMatrix — R65-C1 frozen closure matrix, single end-to-end run

Seat: ExecMatrix (w1, kaidoku-shokunin round 65 attempt 1). Base c99e907cb5576c13a7b22755d776b356fdfc1752.
Instrument: `tools/round-65/jsc-closure-matrix.py`, run ONCE, unmodified, with the seat counting command.

## Command

```
S=/fast/scratch/hyaku/kaidoku-r65/ExecMatrix; mkdir -p "$S" <report dir>
sha256sum .../tools/round-65/jsc-closure-matrix.py > instrument-before.txt
TMPDIR=$S timeout 3000 python3 -I -B .../tools/round-65/jsc-closure-matrix.py \
  --probe .../waves/round-64/inputs/probe-electron.jsc --work "$S/cells" \
  --out .../w1/ExecMatrix/matrix-run.json > matrix-run.stdout 2> matrix-run.stderr; echo "exit=$?"
sha256sum .../tools/round-65/jsc-closure-matrix.py > instrument-after.txt
find /home/vgpnk/.local/share/kaidoku-jsc -name '__pycache__' -o -name '*.pyc' | sort > cache-after.txt; wc -l < cache-after.txt
```

All paths absolute; toolchain root untouched except reads (scratch only under `$S`).

## Headline

- **exit = 0** (wrapper printed `exit=0`; service runtime 5m21s; exit code 0 = verified)
- **runs_matching/runs_total = 18/18**, mismatches = `[]`
- **closure: 30 entries (27 CLOSURE + probe + node + interpreter), ok=true, findings=[]** — missing 0, pin_mismatch 0, cache_present 0
- **census delta: equal=true, added=0, removed=0, changed=0**
- **cache-after line count = 0** (required 0)
- **instrument sha256 before == after** = `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` (matches frozen pin)
- matrix-run.stderr: 0 bytes
- verified = true, skip_run = false → **R65-C1 predicate clauses (i), (ii), (iii) all hold**

## Label histogram (observed, 18 runs)

| label | count |
|---|---|
| `dump-ok\|view8-ok\|node-fail` | 6 |
| `dump-exit-139\|view8-skipped\|node-skipped` | 3 |
| `dump-exit-134\|view8-skipped\|node-skipped` | 9 |

Predicted map (frozen, unchanged from r64): probe|D1 = probe|D2 = `dump-ok|view8-ok|node-fail`; probe|D3 = `dump-exit-139|view8-skipped|node-skipped`; typora|D1 = typora|D2 = typora|D3 = `dump-exit-134|view8-skipped|node-skipped`. Every observed label equals its cell's prediction; no re-prediction occurred.

## Per-cell receipts

| cell | label | dump_rc | dump_bytes | view8_out_bytes |
|---|---|---|---|---|
| probe D1 r1 | dump-ok\|view8-ok\|node-fail | 0 | 2882 | 213 |
| probe D1 r2 | dump-ok\|view8-ok\|node-fail | 0 | 2882 | 213 |
| probe D1 r3 | dump-ok\|view8-ok\|node-fail | 0 | 2861 | 213 |
| probe D2 r1 | dump-ok\|view8-ok\|node-fail | 0 | 2882 | 213 |
| probe D2 r2 | dump-ok\|view8-ok\|node-fail | 0 | 2838 | 212 |
| probe D2 r3 | dump-ok\|view8-ok\|node-fail | 0 | 2840 | 213 |
| probe D3 r1–r3 | dump-exit-139\|view8-skipped\|node-skipped | 139 | 0 | — |
| typora D1 r1–r3 | dump-exit-134\|view8-skipped\|node-skipped | 134 | 0 | — |
| typora D2 r1–r3 | dump-exit-134\|view8-skipped\|node-skipped | 134 | 0 | — |
| typora D3 r1–r3 | dump-exit-134\|view8-skipped\|node-skipped | 134 | 0 | — |

dump_bytes vary a few bytes between reps of the same cell (2838–2882) while the composed label stays stable — dump output is not byte-reproducible, labels are.

## Artifacts written (this report dir)

- `matrix-run.json` — full instrument JSON (also echoed to `matrix-run.stdout`)
- `matrix-run.stderr` — empty (0 bytes)
- `instrument-before.txt`, `instrument-after.txt` — identical sha256 lines
- `cache-after.txt` — 0 lines
- `cells/<artifact>-<build>-r<rep>/` — all 18 cell dirs; `reconstruction.js` + `dump.txt` for the 6 dump-ok cells (largest file 2882 B, all far under 2 MB); `dump.txt` only (0 B) for the 12 crash cells (view8 skipped, no reconstruction produced)

Scratch `/fast/scratch/hyaku/kaidoku-r65/ExecMatrix` deleted before yield. No matrix re-run, no instrument edit, no writes outside the report dir and scratch.
