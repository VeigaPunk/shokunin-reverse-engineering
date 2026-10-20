# RunCarriers18 — round-18 run-carriers.sh + carriers.tsv (rev 2, L1 R1/F9/F10)

Files written:
- `.ufo/waves/round-18/run-carriers.sh` (new, executable)
- `.ufo/waves/round-18/predictions/carriers.tsv` (new; 15 rows, 4th sha256 column on the 3 non-synthetic rows)
- `.ufo/waves/round-18/w1/RunCarriers18.md` (this report)

## Contract surface (contract.md:133–136) + L1 revisions

1. **Selftest can now fail.** `fail()` accumulates `fails` and the terminal line is
   `SELFTEST: FAILED cases=N fails=M` with exit 1 (`run-carriers.sh:32`, `159-163`;
   CLEAN path `:163`). Proven red: a `/tmp` copy with the stub `carrier-run`
   mutated to `sys.exit(2)` printed
   `SELFTEST: FAILED selector-run exit (expected 0, got 1)` /
   `SELFTEST: FAILED fakeA carrier-run exit (expected 0, got 2)` /
   `SELFTEST: FAILED cases=19 fails=2` and exited 1 (run before the newest two
   cases were added; current green run is 21 cases).
2. **TSV shape gate.** Missing trailing newline → exit 2 (`:186-188`); zero
   non-empty rows → exit 2 (`:189-192`). Both selftest cases exist (`:143-147`).
3. **Per-row carrier sha256.** `synthetic-*` rows: expected sha looked up by
   carrier basename in `SHA256SUMS` (`:228-234`); absent entry → exit 2. Other
   rows: expected sha from the optional 4th TSV column when present (`:235`).
   Mismatch → message + `carrier-run.exit`=2 + skip (`:238-243`). Green proof:
   full 15-row dry-check, all rows sha-verified, exit 0. Red proof: bogus
   `calib-aether` sha → `carrier-run.exit`=2, row skipped, overall 1.
4. **Pin every W17 tool + producer.json.** `W17_TOOLS` lists carrier-run.py,
   pins.py, log-extract.py, compare.py, receipt-validate.py (`:30`); all five
   are preflighted (`:172-178`) and passed as `--pin` (`:199-200`, `:273`).
   Before each run, `$out/producer.json` records `branch`/`branch_tip` from
   `git -C LANE rev-parse refs/heads/main^{commit}` plus sha256 of those five
   tools, `swiss-misread.py` and `selection.py` (`:246-263`). Dry-check:
   `jq .` exit 0, `branch_tip` = `9011581d…` (baseline), `tool_sha256` = 7 keys.
   (First version emitted a literal `\n` separator — invalid JSON; fixed at
   `:257-258`, and the selftest now asserts `jq`-equivalent parse + key count.)
5. **Startup timeout for every label.** `env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000`
   prefixes every `carrier-run.py` invocation (`:269`), not just `pro-op`.
6. **rm guard.** `outabs` normalised with `realpath -m` and refused unless under
   `$W/runs/` or `/tmp/` before `rm -rf`/`mkdir` (`:210-216`). Red proof in
   selftest with a `$HOME` RUNS_DIR (`:149-155`): exit 1, dir never created.
   Note: the first draft's guard test used `$root/evil/..`, which is under
   `/tmp` and therefore *allowed*; replaced with `$HOME`.

Order in the loop: out-guard → carrier/prediction existence → sha256 → producer.json
→ run. A skipped row leaves `carrier-run.exit`=2 and forces overall exit 1.

## Deliverable semantics (unchanged from r17)

- Labels/paths/kinds/sha from `W18/predictions/carriers.tsv`; output
  `${RUNS_DIR:-runs}/<label>` resolved against W18 (`:206-210`).
- `carrier-run.py` from `$W17/tools` (`:24`); receipt → `jq .bound_sessions[0]`
  → `log-extract.py` → `compare.py`; exit 0 iff every selected row has
  carrier-run=0 and compare=0, else 1 (`:276-286`).
- Explicit `--pin` set: carrier realpath, prediction, swiss-misread.py, r16
  selection.py, all five W17 tools, every Go data file (`:271-273`). r17
  `carrier-run.py:320` already default-pins carrier+selection and dedupes.

## carriers.tsv (15 rows)

- 12 synthetic rows: 8 `synthetic-minimal-pair` + 4 `synthetic-nethttp`, all
  matching the current `SHA256SUMS` (which now has 12 entries) — verified by
  `comm -3`, zero diff on names.
- `calib-aether`, `calib-notesmd-cli`, `real-kimi-webbridge` carry a 4th-column
  sha256: `06c91f55…`, `412dc532…` (both equal the r17 receipts'
  `carrier.sha256_pre`), `71067480…` (live `sha256sum`).
- Kind words for the L1-added rows are kept exactly as L1 wrote them.

## Commands run (all exits, this rev)

| Command | Result |
|---|---|
| `bash -n run-carriers.sh` | exit 0 |
| `bash run-carriers.sh --selftest` | exit 0; last line `SELFTEST: CLEAN cases=21` |
| Forced-red `/tmp` copy (stub carrier-run exit→2) | exit 1; last line `SELFTEST: FAILED cases=19 fails=2` (pre-newest-cases run) |
| 15-row dry-check (stub tools, real tsv+carriers+SUMS, RUNS_DIR=/tmp) | exit 0; 15 dirs; every row passed sha256 |
| Same dry-check with `calib-aether` sha set `deadbeef` | exit 1; `carrier-run.exit`=2 for that row, stderr mismatch line with real sha |
| `jq -e . $runs/calib-aether/producer.json` | exit 0; `.branch_tip` `9011581d…`, `tool_sha256|length` 7 |

No REA, no Ghidra, no carrier execution, no installs, no git writes.

## Risks / blockers

- `W18/tools/swiss-misread.py` still absent (sibling seat): preflight exits 1
  naming it until it lands. All `*.prediction.json` files are other seats'
  outputs; missing ones skip with `carrier-run.exit`=2.
- `real-kimi-webbridge` has no SUMS entry by design, so its check relies solely
  on the TSV column; if L1 rebuilds that binary the row must be updated.
- Preflight treats a missing `SUMS` as fatal (1); that is intentional since
  every synthetic row would otherwise be unverifiable.
