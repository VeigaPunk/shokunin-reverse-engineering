# ExecMatrix — R65-C1 closure matrix run (w1)

Ran the frozen instrument `tools/round-65/jsc-closure-matrix.py` exactly once, end to end, unmodified (sha256 before == after == `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`), with `TMPDIR`/`--work` under `/fast/scratch/hyaku/kaidoku-r65/ExecMatrix` (disk-guard checked first: 404.5G free). Runtime 5m21s.

## Result: exit 0 — verified

- **runs_matching/runs_total = 18/18**, mismatches `[]` — every run reproduced its frozen predicted label (`dump|view8|check` composed labels; probe D1/D2 = `dump-ok|view8-ok|node-fail` ×6, probe D3 = `dump-exit-139|view8-skipped|node-skipped` ×3, typora D1/D2/D3 = `dump-exit-134|view8-skipped|node-skipped` ×9)
- **closure: 30/30 entries match count and sha256, findings none** (0 missing, 0 pin mismatch), and **no Python bytecode cache present** before the run
- **census delta: equal** — added 0, removed 0, changed 0 across the whole toolchain root
- **cache-after count = 0** (`__pycache__`/`*.pyc` under `/home/vgpnk/.local/share/kaidoku-jsc` after the run)
- `matrix-run.stderr` empty

R65-C1 predicate clauses (i), (ii), (iii) all hold on this run.

## Evidence

- Full JSON: `.ufo/waves/round-65/w1/ExecMatrix/matrix-run.json` (`exit:0`, `verified:true`, receipts per cell)
- Counting: `instrument-before.txt` / `instrument-after.txt` (identical), `cache-after.txt` (0 lines), `matrix-run.stdout`, `matrix-run.stderr` (0 B)
- Cell artifacts: `.ufo/waves/round-65/w1/ExecMatrix/cells/<artifact>-<build>-r<rep>/` — all 18 dirs; `reconstruction.js` (212–213 B) + `dump.txt` (2838–2882 B) for the six dump-ok cells, empty `dump.txt` for the twelve crash cells; every copied file under 2 MB
- Detail log: `.ufo/waves/round-65/w1/ExecMatrix/findings.md`

Note for calibration seats: dump payload byte sizes vary a few bytes across reps of the same cell (e.g. probe D1: 2882/2882/2861) while labels stay identical — the labels, not dump bytes, are the frozen claim surface.

Scratch deleted before yield. Exit was 0, so the no-re-run guard (stop on exit 2) never triggered.

Report: .ufo/waves/round-65/w1/ExecMatrix.md
