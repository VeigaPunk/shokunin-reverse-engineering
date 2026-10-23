# R34FreezeSchema — strict claims-schema successor for `freeze-integrity`

## Scope and verdict

Routed defect 3 of `corpus/lessons/round-33-verifier-spotcheck.md` (routed-defects list,
item 3, first bullet) records that **seven empty or malformed freeze maps are falsely
CLEAN, so add claims-schema validation**. The underlying experiment is
`.ufo/waves/round-33/w1/WFreezeMalformed.md` against the frozen instrument
`tools/round-33/freeze-integrity.py`. This seat produced a successor copy, not an edit of
the frozen instrument, and measured it once on bounded disposable Git fixtures:

- old instrument: all seven survivor shapes exit **0** and print CLEAN (`pins=0`, or
  `pins=1` for the coerced pair list) — red reproduced;
- successor: all seven exit **3** with a distinct schema finding and never print CLEAN or
  `ok<TAB>` — green;
- four valid historical pin-map shapes produce byte-identical CLEAN rows and pin counts
  under old and new gates;
- successor `--selftest`: **PASS cases=25**, exit 0, 0.97 s.

No production gate was run, no lane file outside this seat's output directory was written,
no claim, admission, judgment, or R33-C1 revival is made. `U064N008Hf47eb933` stayed held
and untouched.

## Measured source

| Input | Value observed |
|---|---|
| Lane HEAD at run | `ec3125ad3d130d92f888a4128dfaa2982f36fff7` (base stated in the task) |
| Old instrument | `tools/round-33/freeze-integrity.py`, SHA-256 `a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2` (matches WFreezeMalformed's pinned gate bytes), unchanged before and after |
| Successor | `freeze-integrity.py` (this seat's copy), 21 181 bytes, SHA-256 `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138`, 472 lines |
| Probe driver | `probe-schema-matrix.py`, 13 534 bytes, SHA-256 `922d52818f6d16e76669c959feacfa30660976851528fa8208ada47246bdc706`, 314 lines |
| Python / Git | `3.14.8` / `git version 2.56.0` |
| Old behavior cited | `fallback = json.loads(text).get(key, {})` then `pins.update(...)`; zero merged pins → CLEAN at the old exit-0 line |

## Successor behavior

The gate keeps the old CLI (`--root`, `--round`, `--claims`, `--rev`, `--selftest`), the
per-pin `ok`/`FAIL` rows, and the CLEAN/FAIL summary wording. Before any pin row it
validates the claims document read **at the freeze commit** (the same commit the old gate
took pins from):

1. claims text must parse as JSON (`claims_not_json`), and the top level must be an object
   (`claims_not_object`);
2. `instruments` must be present (`instruments_missing`), a JSON object
   (`instruments_not_object`), and non-empty (`instruments_empty`);
3. `frozen_inputs` may be absent, but if present must be a JSON object
   (`frozen_inputs_not_object`); the empty object is valid;
4. every pin key must be a non-empty string (`pin_key_empty`), a repo-relative path with no
   leading `/`, no `..` segment, and no NUL (`pin_path_not_relative`);
5. every digest must be exactly 64 lowercase hex characters (`pin_digest_format`);
6. a path pinned in both maps is rejected (`pin_path_duplicate`), instead of the old
   silent last-writer-wins `dict.update`.

Exit codes: **0** CLEAN, **1** FAIL (digest/history), **2** absent freeze commit, **3**
claims schema error. A schema error prints exactly one line and returns 3:

```text
freeze-integrity: ERROR schema code=<code> claims=<claims path> where=<detail>
```

It prints no `ok` row and no CLEAN. A `git show` failure for the claims at the freeze
commit also returns 3 as `code=claims_unreadable` instead of being ignored.

`--selftest` now runs 25 cases with frozen expected exits/findings: the five preserved
round-33 cases, three historical-shape compatibility cases, and seventeen schema rejects
(the table `_SCHEMA_CASES` pairs each claims byte string with its expected exit and
finding substring). Each schema case also asserts that CLEAN and `ok<TAB>` never appear.
The selftest base moved to `/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest`; the
round-33 base is not touched.

## Compatibility decisions

1. **`instruments` mandatory and non-empty.** Every historical claims file that carries
   pin maps (twelve files, rounds 24-32 including `round-25/a2`, `round-28/claims-c2`,
   `round-32/claims-v2.json`, `round-32/claims-v3.json`) has at least one instrument. A
   zero-instrument file cannot certify a freeze; CLEAN pins=0 is the defect class.
2. **`frozen_inputs` optional; absent allowed.** Rounds 24, 25, 25/a2, 27, 28, 28-c2 and
   29 carry only `instruments`. Requiring the key would break those valid shapes.
3. **`frozen_inputs: {}` valid.** Round-32 v2/v3 pin the empty object; WFreezeMalformed
   explicitly did not propose requiring every map to be nonempty.
4. **Pin keys repo-relative.** All keys in all twelve pin-bearing files pass (checked over
   the base revision); none is absolute, empty, or contains `..`.
5. **Digests exactly 64 lowercase hex.** All historical values pass. A malformed digest
   now exits 3 (`pin_digest_format`) instead of the old exit-1 digest-mismatch FAIL; both
   are nonzero, and the WFreezeMalformed `bad_digest` row moves from an uncontrolled FAIL
   to a controlled schema reject.
6. **Cross-map duplicate path rejected.** No historical file duplicates a path across
   `instruments`/`frozen_inputs`; the old code would silently let `frozen_inputs` win.
7. **Malformed JSON and non-object top levels are controlled exit 3.** Previously they
   were unhandled tracebacks (exit 1). The five WFreezeMalformed exception rows are now
   covered by frozen selftest cases.
8. **Schema is checked at the freeze commit only**, matching the old pin source; claims
   edited after the freeze remain invisible to this gate (pre-existing scope, unchanged).
9. **Output for valid maps is byte-identical:** `ok<TAB>path<TAB>sha=<12><TAB>commits_after_freeze=…`
   rows and `freeze-integrity: CLEAN pins=K freeze=… rev=…` / `FAIL …` lines are untouched.
10. **Files without pin maps now fail `instruments_missing`.** This includes
    `round-26/claims.json` (which carries `freeze_kind` but no pin maps) and rounds 14-23.
    Those files never carried pins, so any CLEAN from them was vacuous (`pins=0`); they
    are rejected as non-certificates, not treated as historical pin shapes.
11. **Clean cutover at integration:** the successor is a full replacement with the old
    name (`freeze-integrity.py`); no alias, shim, `--strict` flag, or dual mode. The
    round-33 file remains frozen and unedited for historical reproduction.
12. **Selftest writes only to the round-34 scratch base**, drops every fixture, and takes
    no `--root`/`--round`.

## Measured old-red/new-green run

One driver invocation, captured in full. Driver argv:

```text
/usr/bin/python -I -B
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34FreezeSchema-files/probe-schema-matrix.py
--out
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts
```

Start `2026-10-23T10:26:29.271980+00:00`, end `2026-10-23T10:26:31.185735+00:00`,
1.913765 s, driver exit **0**, stderr empty, no timeout. Bounds: 60 s per command, 300 s
overall alarm (not fired), child `RLIMIT_AS` 512 MiB driver / 256 MiB gate, `RLIMIT_CPU`
120 s driver / 60 s gate, `RLIMIT_FSIZE` 8 MiB driver / 1 MiB gate, `RLIMIT_CORE` 0,
`RLIMIT_NOFILE` 256/128, process groups SIGKILLed after every command. `GIT_DIR`,
`GIT_WORK_TREE` and `GIT_INDEX_FILE` were dropped; `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0`.

Every fixture is a one-commit repository under
`/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaProbe.w8w4be9x` (removed after the run,
`scratch_removed: true`; the empty selftest base directory remains). Each shape was built
from independently generated payloads, so its commit IDs and payload digests differ from
WFreezeMalformed's; the seven **shapes** are reproduced, not its byte streams.

Exact rows (full stdout/stderr/argv are in `receipts/receipt.json`):

| Shape (class) | Old exit / output | New exit / output |
|---|---:|---:|
| `empty_maps` (`instruments={}`) | 0 / `freeze-integrity: CLEAN pins=0 freeze=9a178bdb57f9 rev=HEAD` | 3 / `... code=instruments_empty ... where=instruments` |
| `omitted_instruments` | 0 / CLEAN pins=0 | 3 / `code=instruments_missing` |
| `no_pin_keys` (`{}`) | 0 / CLEAN pins=0 | 3 / `code=instruments_missing` |
| `empty_list_map` (`instruments=[]`) | 0 / CLEAN pins=0 | 3 / `code=instruments_not_object` |
| `empty_string_map` (`instruments=""`) | 0 / CLEAN pins=0 | 3 / `code=instruments_not_object` |
| `pair_list_map` (`[["artifact.txt", digest]]`) | 0 / `ok\tartifact.txt\tsha=eaefba247108\tcommits_after_freeze=0` + `CLEAN pins=1` | 3 / `code=instruments_not_object` |
| `empty_list_frozen_inputs` (`frozen_inputs=[]`) | 0 / CLEAN pins=1 | 3 / `code=frozen_inputs_not_object` |
| `valid_single_pin` (1 pin) | 0 / `CLEAN pins=1` | 0 / `CLEAN pins=1` |
| `valid_instruments_only` (no `frozen_inputs` key) | 0 / `CLEAN pins=1` | 0 / `CLEAN pins=1` |
| `valid_empty_frozen_2` (`frozen_inputs={}`) | 0 / `CLEAN pins=2` | 0 / `CLEAN pins=2` |
| `valid_round32_4_4` (4 instruments + 4 inputs) | 0 / `CLEAN pins=8` | 0 / `CLEAN pins=8` |

The driver classifies 7/7 survivor rows `red`→`green` and 4/4 valid rows green under both
gates; it fails on any stderr output, timeout, wrong exit, wrong finding, or CLEAN/ok row
on a reject. New-gate stdout for `valid_round32_4_4` is the eight unchanged `ok` rows plus
`freeze-integrity: CLEAN pins=8 freeze=5256954f25b8 rev=HEAD`.

Successor selftest (one of the 23 recorded commands), exit 0:

```text
freeze-integrity-selftest: PASS cases=25 elapsed_s=0.97 base=/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest
```

Its 25 lines are retained verbatim in `receipts/receipt.json` (`selftest.stdout`), e.g.
`case clean: PASS freeze=4c52b82af19e pins=2 exit=0`,
`case schema_empty_instruments: PASS exit=3 code=instruments_empty`,
`case compat_round32_shape: PASS exit=0 pins=8`.

Historical-byte compatibility (read-only `git show` at the base revision; the successor's
`load_pins` executed in-process from compiled source, no fixture writes): 25 tracked
`claims*.json` files parsed; **12/12 pin-bearing files accepted** with their expected pin
counts — round-24 2, 25/a2 2, 25 1, 27 2, 28-c2 1, 28 1, 29 2, 30 6, 31 5, 32 8, 32-v2 2,
32-v3 2 — and the 13 files without pin maps rejected as `instruments_missing`. Full rows
and per-file SHA-256 are in `receipts/compat-historical.json`.

## Retained evidence

Lane root is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; paths below are relative to
it.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/freeze-integrity.py` | 21181 | `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/probe-schema-matrix.py` | 13534 | `922d52818f6d16e76669c959feacfa30660976851528fa8208ada47246bdc706` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/receipt.json` | 21037 | `36bbf3843f0793ae01225d56076d45ebcb5699fedfaaff4c2148ac2d63e46880` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/receipt.txt` | 1301 | `4e7d1199061f0d450e593c234edcd608509f472d0beb9b1526ef217a83a98e12` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/driver.argv.txt` | 248 | `bb5efe4fdfb7ea0c70f84c9443777063654ff5b05c2a5d27c6025756387da559` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/driver.stdout.txt` | 1301 | `4e7d1199061f0d450e593c234edcd608509f472d0beb9b1526ef217a83a98e12` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/driver.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/driver.exit.txt` | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/driver.meta.json` | 834 | `30b5a020dcdd44fc585e2d01b185bb79e9e5c3355c6d38a2f64ff3d3d86765fa` |
| `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/compat-historical.json` | 5580 | `0b9031ce7b0f18c81cc0eb0071eefed043446d910378c151866b3622235ff8c0` |

`receipt.json` retains every subprocess argv, cwd-independent start/end UTC, duration,
exit, stdout, stderr and timeout flag for the 22 gate invocations and the selftest, plus
old/new gate hashes before and after and the scratch cleanup result. `receipt.txt` and
`driver.stdout.txt` are the same 1301-byte summary.

## Containment and limits

- No lane or fleet Git/jj write: the lane was read-only (`git show`, `git ls-tree`,
  `rev-parse` only, all outside this seat's receipts); every fixture repository was
  created under `/fast/scratch/hyaku/kaidoku-r34/` with the three Git override variables
  removed, and the probe tree was deleted before exit.
- `tools/round-33/freeze-integrity.py` was executed read-only and its SHA-256 is identical
  before and after. No production gate, production fixture, carrier manifest, held data,
  or REA/MCP call was used.
- Fixture payloads are at most a few dozen bytes; per-command and overall timeouts,
  address-space, CPU, file-size, core and descriptor caps are recorded above. No
  background jobs, subagents, or installs (Python 3.14.8 and Git 2.56.0 were already
  present).
- The probe exercises single-commit root fixtures, not descendant tamper/restore history
  for the schema path; the five preserved selftest cases continue to cover those gate
  paths. The historical compatibility check exercised only `load_pins`, not full history
  verification against a lane clone.
- Duplicate JSON object keys are still resolved by the parser (last value wins); the
  schema rejects duplicate paths **across** the two maps but does not detect duplicate
  keys within one JSON object. No historical claims file has duplicate keys (checked over
  the base revision).
- The run is one host/toolchain sample; the old gate's own `--selftest` was deliberately
  not run because it writes to the round-33 scratch base.
- No safety refusal, reroute, or provider error occurred. Runtime context reports model
  `opencode-go/deepseek-v4.1-flash`; this is the actual answering model for this seat.

## Blockers

None. Integration (copying the successor to `tools/round-34/`, registry row, and the
post-integration gate run) belongs to Main.
