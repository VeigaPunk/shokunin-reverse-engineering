# RevB9Registry — instrument-registry B9 review at base (round 50, attempt 2, wave 3)

**Verdict: `b9-at-base: green`** — 0 findings. All 12 census paths (`tools/round-49/**` + `tools/round-50/**`,
`.py`/`.sh`, control fixtures excluded) are cell-0 of exactly one 7-cell registry row with a `gate|probe` kind,
an entry command naming the path, a verdict map binding 0/1/2, a self-test spelling, and a pinned-value path.
The 12 rows added at the attempt-1 landing (commit `11ccdb72`, registry 42→54 rows) show no cell-shape drift
the counter's parser could miss. SKILL.md is byte-identical at base `f890bbea` and current HEAD `6f4aba63`;
`c2-record.py` is byte-identical at base and the C1 freeze `435d41fd`.

## Method

Base = `f890bbead20ca2c549487167f56876ae47f1e1a4` (attempt-2 claims commit; SKILL.md blob `a72ed0c0fbd7a3f3d6766e7e32d14c0d858972d5`).
I hand-replicated atom `b9` of `tools/round-50/c2-record.py` (its full derivation logic: `vis`, `cells`,
`registry_region`, `census_paths`, `meaning_classes`, and the per-row checks at lines 826–895, with the
constants at lines 131–152) against the real `SKILL.md` and tool trees at base — the counter's `--selftest`
covers fixture shape, not this live tree, so the atom's logic was executed verbatim against the lane bytes
(`b9-replica.py`, exit 0, 0 findings). A second pass (`drift-scan.py`) audited the raw bytes of every row line
in the marker-bound region for shapes the parser tolerates silently: extra columns, nested/escaped pipes,
trailing whitespace, inline comments (NUL substitution), non-table interlopers, and padding drift.
A third pass (`attempt1-cells.py`) dumped the parsed cells of the 12 attempt-1 rows for eyeball confirmation
against the atom's five sub-checks. Read-only git only; no REA, no instrument runs, no lane writes outside
this seat's `.ufo` directory.

## Findings table

Exit codes are semantic (0 met/clean, 1 not met/violation, 2 could-not-evaluate). `diff` exit 1 below is the
tool's "inputs differ" meaning and is the expected result for the attempt-1 delta receipt. The two empty
stdout receipts (`e3b0c442…`) are expected-empty. All sha256s are of stdout. Full receipt records (exact
commands, UTC times, byte counts) are in `RevB9Registry/receipts.json`.

| # | check | command (abbrev) | exit | stdout sha256 |
|---|-------|------------------|------|---------------|
| 1 | census paths at base | `git ls-tree -r --name-only f890bbea -- tools/round-49 tools/round-50 \| grep -E '\.(py\|sh)$' \| grep -v control-fixtures \| sort` | 0 | `9533b7564d1ba55c…` |
| 2 | row count per commit | `for c in 845e0586 11ccdb72 f890bbea; do … grep -c '^\\| \`tools/' …; done` | 0 | `83e220e4cddf7c97…` (42/54/54) |
| 3 | attempt-1 delta | `diff <(…845e0586…) <(…11ccdb72…)` (registry cell-0 sets) | 1 | `3cff4dd257a46a33…` (`42a43,54`, 12 rows) |
| 4 | stability base vs landing | `diff <(…11ccdb72…) <(…f890bbea…)` | 0 | `1e00073b48fe3b36…` (`IDENTICAL`) |
| 5 | B9 hand-replica | `python3 b9-replica.py` (mirrors atom b9 at base) | 0 | `eabb2e9592d4be75…` (0 findings) |
| 6 | raw drift scan, all 54 rows | `python3 drift-scan.py` | 0 | `2d956e51969b87bf…` (no anomalies) |
| 7 | parsed cells, 12 attempt-1 rows | `python3 attempt1-cells.py` | 0 | `2b69e682a0351597…` (7 cells each, padding clean) |
| 8 | header/separator bytes | `git show f890bbea:SKILL.md \| sed -n '1715,1718p' \| cat -A` | 0 | `464ed4b48f74448d…` (7-cell header, 7-col rule) |
| 9 | SKILL.md blob base vs HEAD | `git rev-parse f890bbea:SKILL.md 6f4aba63:SKILL.md` | 0 | `632652c410ff6f02…` (both `a72ed0c0…`) |
| 10 | counter blob base vs C1 freeze | `git rev-parse f890bbea:tools/round-50/c2-record.py 435d41fd:…` | 0 | `3b86e76971a2b0ef…` (both `214f2065…`) |
| 11 | round-49 tree counter-BASE vs base | `git diff --name-only 7c678ae6 f890bbea -- tools/round-49` | 0 | `e3b0c44298fc1c14…` (empty: unchanged) |
| 12 | marker span | `git show f890bbea:SKILL.md \| grep -n 'instrument-registry v2\\|/instrument-registry'` | 0 | `a3439866116c1851…` (lines 1715/1774, single pair) |

## What was verified (substance)

1. **Census** — 12 paths at base: `tools/round-49/{c1-controls,c1-counter,c1-oracle,c1-run}.py`,
   `c1-run.sh`, `c2-mismatch.py`; `tools/round-50/{c1-controls,c1-counter}.py`, `c1-run.sh`,
   `c2-record.py`, `fetch-vendor.py`, `selftest-r49-c2.py`. Identical under the atom's own BASE constant
   `7c678ae6` (receipt 11: `tools/round-49` untouched between the two bases).
2. **Exactly-one-row, 7 cells** — `registry_region` at base keys 54 rows, all unique; each census path
   matches exactly one row's backticked cell-0 (`rows.get(p)` single hit, `len(cs)==7`).
3. **Kind** — all 12 rows open `gate —` or `probe —` (case-insensitive `gate|probe\b` check passes).
4. **Entry command** — cells 1–4 of every row contain `python3 -I -B <path> …` or `bash <path> …` with the
   path followed by a non-word boundary (negative-lookahead check passes; e.g. the r50 `c1-run.sh` row's
   `run as bash tools/round-50/c1-run.sh after --id ID …`).
5. **Verdict map** — all 12 rows' cell 2 parses as `0=…;1=…;2=…` with three distinct meanings; exit-0 arms
   name a success word, exit-1 a not-met word, exit-2 an unevaluable word (`meaning_classes` returns None
   for all 12).
6. **Self-test spelling** — 7 rows carry `python3 -I -B <path> … --selftest` (`c1-counter` r49/r50,
   `c1-controls` r49/r50, `c1-oracle` r49, `fetch-vendor` r50, `c2-record` r50); 5 rows carry
   `none — <reason>` (`c1-run.py`, both `c1-run.sh`, `c2-mismatch.py`, `selftest-r49-c2.py` — the last is
   itself the self-test).
7. **Pinned-value path** — 10 rows name a pinned path (e.g. `tools/round-50/carriers.json`, the
   `selftest-r49-c2.expected.json` pin); 2 rows carry `none — <reason>` (`c2-mismatch.py`, `c2-record.py`,
   pinned-in-source).
8. **Attempt-1 landing shape** — the 12 added rows (lines 1762–1773 at base) each have exactly 8 unescaped
   pipes → 7 cells, zero escaped pipes, no nested pipes, no trailing whitespace, no inline comments/NULs,
   uniform single-space padding, header and separator both declare 7 columns, and the rows were not touched
   between `11ccdb72` and base (receipts 3–4). No extra columns, no drift.

## Calibration notes (not defects)

- The r50 `c1-controls.py` row passes the self-test spelling check only because its cell literally contains
  the string `--selftest` inside the prose "no --selftest flag; 20 cases…"; the instrument's real self-test
  is the positional `selftest` subcommand. The atom is a spelling rule, so this is per-spec — but the regex
  cannot distinguish an invocation from a mention of the flag.
- `b9` checks cell shape and spelling only. It does not verify that stated entry/self-test commands actually
  run or that the pinned files exist (they do — visible in the tree — but no instrument was executed this
  wave, by design).

## Residual risk and verification gaps

- Replica fidelity: `b9-replica.py` transcribes the atom's regexes and constants verbatim from the frozen
  counter (blob `214f2065…`); the only un-cross-checked step is my transcription, mitigated by copying the
  code regions directly. The counter's own `--selftest` (fixture shape) was not run — my task names the
  hand-derivation against the live tree instead, which is the deeper check.
- No semantic execution of registry-stated commands (forbidden this wave: no REA, quiet-load rule).
- Nothing blocking. `b9-at-base: green` stands.

Artifacts: `receipts.json` (all 12 receipts with exact commands/UTC), `b9-replica.{py,json}`,
`drift-scan.{py,json}`, `attempt1-cells.{py,json}`, `census-paths.txt`, `collect-receipts.py`.
