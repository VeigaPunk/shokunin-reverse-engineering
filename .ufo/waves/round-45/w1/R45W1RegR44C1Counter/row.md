# R45-C2 registry row — `tools/round-44/c1-counter.py`

Seat `R45W1RegR44C1Counter`, round 45 wave 1. Instrument read from source at the freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (`git show f762b72:tools/round-44/c1-counter.py`,
sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`; the blob
`9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569` is byte-identical at HEAD).
Land this as the **replacement** for the existing row at `SKILL.md:1636`, not as an addition:
the frozen counter keeps the *first* row per path.

## Ready to paste

One line, seven columns. The frozen R45-C2 counter takes the path from cells[0]
(`ROW_TOOL`) and requires the tokens `0`, `1`, `2` in cells[2] (`exits_ok`).

| `tools/round-44/c1-counter.py` | gate — R44-C1 coverage: re-derives the four frozen unblob SquashFS v1/v2 carriers (layout, carve, oracle census, gap rule) and re-runs REA `extract-firmware` to compare the plus-extractor projection; `--dev-arm` is the positive control on captured or freshly run envelopes; `--verify-receipt` re-checks a receipt's own identity | `0` met — every carrier clause and binding true (`failing == []`, `bindings_false == []`); `1` not met — a named false clause or binding, a red selftest case, or a receipt whose `counter_sha256` does not describe its `counter`; `2` could-not-evaluate — unusable or absent `--root`/`--rev`/`--freeze`/`--pkg65`, `rerun_disabled` under `--no-rerun`, `rerun_env_error`, `frozen_path_changed`, unreadable receipt, or a failed self-stamp. Caveat: the selftest's start-up refusals (missing `xpin-attribute.mjs`, undiscoverable `--pkg65` or node, xpin mint failure) and any uncaught exception exit 1 with no JSON receipt, so a broken harness reads as "not met" | `python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` — exit 0, `cases` 47, `failures` [] (2026-10-28) | `tools/round-44/carriers.json` (ids, paths, handler and sha256 pins for the four carriers, whose bytes live under `corpus/evidence/round-42/c2/fixtures/`) and `corpus/evidence/round-44/c1/` at the freeze; `FROZEN_PATHS`/`FROZEN_PREFIXES` in the counter | `--json-out` and `--work` only; selftest fixtures under `$HYAKU_SCRATCH/kaidoku-r44/counter` | kaidoku |

row sha256 (single line, no trailing newline): `2f2ea910c9c6cb86ea5b5ea389dd2cfa571821d21299a91cbcc6997efed0a931`

## Column provenance

| column | what the row asserts | command that verified it | exit |
|---|---|---|---|
| 1 tool | the path exists at the freeze and is the exact first cell | `git ls-tree -r --name-only f762b72 -- tools/round-44` (lists `tools/round-44/c1-counter.py`) | 0 |
| 2 gate/probe | coverage gate over four carriers — layout, carve, oracle census, gap rule — plus the REA rerun projection; `--dev-arm` positive control; `--verify-receipt` probe | source at the freeze: `EXPECTED_IDS = ('v1le','v1be','v2le','v2be')`, `CLAUSES` (22, incl. `layout_ok`/`carve_ok`/`oracle_hits_ok`/`gaps_ok`/`projection_ok`), `BINDINGS` (12) | — |
| 3 verdict map | `0` met / receipt verified; `1` not met or red selftest, plus the message-only guard exits; `2` could-not-evaluate | probes `help`→0, `no-args`→2, `unknown-option`→2, `--no-rerun`→2, `--verify-receipt` 0/1/2, malformed `carriers.json`→2 `unevaluable` | 0 and 1 and 2 all observed |
| 4 self-test | `--selftest` green: 47 cases, `failures []`, rc 0 | `python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; stdout sha `fbe23fef...`, reproduced identically twice | 0 |
| 5 pinned-value path | `tools/round-44/carriers.json` pins the four carriers (ids, paths, handler, sha256) whose bytes live under `corpus/evidence/round-42/c2/fixtures/`; the expected trees are `corpus/evidence/round-44/c1/`; the counter also hard-codes `FROZEN_PATHS` (10 paths) and `FROZEN_PREFIXES` (`tools/round-44/`, `corpus/evidence/round-44/oracle/`) | `git ls-tree -r --name-only f762b72 -- tools/round-44/carriers.json` (1 file), `-- corpus/evidence/round-44/c1` (126 files); `carriers.json` parsed: 4 carriers, handlers `squashfs_v1`/`v2`, paths under `corpus/evidence/round-42/c2/fixtures/` | 0 |
| 6 write scope | `--json-out` and `--work`/`$HYAKU_SCRATCH/kaidoku-r44/counter` only; never the lane tree | `grep -n "open([^)]*['\"]wb\?['\"]"` → 6 write sites, all rooted at `work` (609, 614, 1876, 2288, 2732, 3305); `scratch_root()` reads `--work` → `$HYAKU_SCRATCH/kaidoku-r44/counter` → `/fast/scratch/hyaku`, never `tempfile.gettempdir()` | — |
| 7 owner | `kaidoku` | lane identity | — |

## Landability, measured against the frozen R45-C2 counter

- Clean fixture (`SKILL.md` = this row first for the path + the five other registry rows,
  one commit, `--rev == --freeze`): exit **0**, `registered` = all six scope paths,
  `thin []`, `unregistered []`, `scope_size 6`, `registry_rows 6`.
- Thin mutation (cells[2] = `non-zero on failure`): exit **1**,
  `thin ['tools/round-44/c1-counter.py']`.
- Wrong-path mutation (cells[0] = another tool): exit **1**,
  `unregistered ['tools/round-44/c1-counter.py']`.
- First-match shadowing is real: with the live `SKILL.md` (row at line 1636) plus this row
  appended, `by_tool` resolves to the incumbent (`first_match_is_existing: True`,
  `dup_rows_for_path: 2`). Replace, do not append.

## Exit paths that are not verdicts

Across 16 probes the observed exit codes are exactly `{0,1,2}` — no code outside that set.
The defect is overloading, not range: **four start-up refusals exit 1** with a bare stderr
message, empty stdout and no JSON receipt, indistinguishable from "target not met":

1. `xpin-attribute.mjs not found from <dir>` (`find_xpin`, only reachable from a relocated copy)
2. `selftest needs --pkg65 (a rea-agents 6.5.0 package root)` (no `--pkg65`, none discoverable)
3. `xpin mint failed: ...` (a `--pkg65` that is not a 6.5.0 package)
4. an uncaught exception, e.g. `--work /proc/self/nope` → `FileNotFoundError` traceback

The module docstring promises `2 unevaluable (bad args, git/node failure, ...)` for that class,
so document and code disagree. Scoring mode *does* honour the map (`--no-rerun` → 2,
malformed `carriers.json` → 2), so the overloading bites `--selftest` and `--dev-arm` harness
failures only. Cells[2] names the caveat rather than hiding it. Signals are not modelled
(`SIGINT` → 130 by CPython default) and were not exercised.
