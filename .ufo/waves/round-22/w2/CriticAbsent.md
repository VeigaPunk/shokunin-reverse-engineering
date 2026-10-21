# CriticAbsent — false-client provider controls vs. actual-absence claims (R22-C1/C2)

Seat `KaidokuR22R.CriticAbsent-6`, critic, leaf. I judged only the evidence authored at lane HEAD
`2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, plus the uncommitted working-tree text where noted.
I edited nothing in the lane. I ran no target execution, device contact or REA probes; the only REA
inspection was reading the static source under the npx cache. No installs.

## Verdict

The PROVINCE prose is honest: it does not claim absent devices or providers. But the C2
counter cannot enforce that honesty. In four places a row's `observed` predicate is equally
satisfied by a receipt that contradicts the row's `reason`. The counter's 14/14 therefore certifies
agreement between receipt and row, not that each gap is named correctly. Five of the 14 rows are
fixed by construction: `/usr/bin/false` fails the same way on every host, so those receipts carry no
information about devices. One cited receipt has no retained producer.

## Commands and observed exits

| argv (cwd = lane) | exit | observed |
|---|---|---|
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root $PWD --rev HEAD` | 0 | accounted 14/14, mismatched [], foreign [] |
| `python3 -I -B .ufo/waves/round-22/frozen/count-c2.py --root $PWD --rev HEAD` | 0 | accounted 14, mismatched [] |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root $PWD --rev HEAD` | 1 | t1_exercised [identify-flutter-build], 1/6, catalog_zero 19 (meets frozen k>=1) |
| `command -v tshark capinfos adb cutter Cutter rizin gdb sigrok-cli frida prlimit` | — | absent: tshark, capinfos, cutter, Cutter, sigrok-cli, frida CLI. Present: /usr/bin/adb, rizin, gdb, prlimit. This is my PATH at review time, not the capture PATH |
| `cat /proc/sys/kernel/pid_max` | 0 | 4194304, so PID 2147483647 cannot exist |
| scratch clone `/tmp/criticabsent-*` (since removed), counterexample commit (CE1–CE3 below), `tools/count-c2.py --rev HEAD` | 0 | accounted 14, mismatched []. All three contradicting receipts were `matched` |
| same clone, real receipts + proposed `devices=` predicate (F2) | 0 | accounted 14, list-frida-devices `matched` |
| same clone, proposed predicate + empty-devices receipt | 1 | accounted 13, list-frida-devices `observed_mismatch` |

## Findings

### F1. ADB rows: the receipt alone cannot tell a false-client control from a real broken client (calibration)

- **Evidence.** PROVINCE.md:194–198 use `error:capability_unavailable`. The receipts
  (`evidence/c2/{inspect-adb-package,list-adb-services,inspect-adb-window,start-adb-activity,stop-adb-app}.json`)
  contain only `details.{provider_id,operation,reason}`. None carries `selected_binary`, `/usr/bin/false`
  or `REA_ADB_PATH`; I checked with grep. The selection is recorded only in `*.run.json` `env_overrides`.
  count-c2.py never reads `.run.json` (no match for `run.json` or `env_overrides` in either counter).
- **Source.** In `rea-agents@6.5.0` `dist/adb/AdbConfiguration.js:72-86`, ENOENT produces
  `binary_missing` ("was not found"). Any other version-probe failure produces the receipt's message,
  "did not report a usable version".
- **Counterexample.** A real `/usr/bin/adb` whose `version` call fails (for example, a broken shared
  library) produces byte-identical receipts apart from `duration`, and would match these rows.
  - A truly absent adb does give a different message, but the counter checks only `error.code`,
    which is the same `capability_unavailable` in both cases.
  - So the counter accepts all three worlds: the false-client control, a broken client, and an
    absent client.
- **By construction.** `/usr/bin/false` fails on every host, so these five outcomes cannot vary.
  They name the gap but cannot falsify the `frontier-blocked` placement.
  - The actual basis for the placement is PROVINCE.md:149–150 (round-4 "22/24 verbs need a live
    device", r4u-06) and PROVINCE.md:130 (real adb 37.0.0 is held).
  - The rows do not cite that basis.
  - This is a contract-mandated tradeoff, not a fixable counter defect. The canonical judge should
    weigh C2's 14/14 as 9 informative receipts plus 5 control receipts.
- **Axes:** calibration.
- **Smallest safe correction (prose only; the counter stays frozen):**
  - Append to each ADB `reason` cell: "control outcome fixed by construction; frontier basis
    PROVINCE:149 (r4u-06)".
  - State in SCORECARD/LOG that 5 of the 14 rows are construction-fixed controls.

### F2. `list-frida-devices` predicate is vacuous with respect to its reason (calibration)

- **Evidence.** PROVINCE.md:191 has `ok-field:cleanup_error=null`, and its reason is "Provider
  successfully enumerated local descriptors".
- **Counterexample CE1.** Receipt `{"ok":true,"data":{"devices":[],"cleanup_error":null},...}`
  produced `matched` (scratch run, exit 0). A zero-device enumeration passes the row that claims
  enumeration.
- **Smallest safe correction (exercised).** Replace the observed cell with:
  `ok-field:devices=[{"deviceId":"local","name":"Local System","type":"local"},{"deviceId":"socket","name":"Local Socket","type":"remote"},{"deviceId":"barebone","name":"GDB Remote Stub","type":"remote"}]`
  - The real receipt still gives `matched`, 14/14, exit 0.
  - CE1 gives `observed_mismatch`, 13/14, exit 1.
  - This works with the frozen grammar: `strict(literal)` equality at count-c2.py:114–116, and the
    cell contains no `|`.

### F3. `list-frida-processes` predicate is vacuous with respect to its reason (calibration)

- **Evidence.** PROVINCE.md:192 has `ok-field:device_id="local"`, and its reason is "Provider
  returned local process names/PIDs".
- **Counterexample CE2.** `{"ok":true,"data":{"device_id":"local","processes":[]},...}` produced
  `matched`.
- **Limit of the grammar.** `dig` (count-c2.py:79–84) walks only dicts, so a non-empty check or
  `processes.0` cannot be expressed. A full-list literal would work, but it would mean a ~7 KB cell of
  host process names.
- **Smallest safe correction.** Narrow the reason to what the counter checks: "ok envelope for
  device local; process-list contents are in the receipt and not counter-checked".

### F4. `instrument-with-frida`: the row accepts the exact absence its reason denies (calibration)

- **Evidence.** PROVINCE.md:193 has `error:capability_unavailable`, with the reason "missing-process
  refusal is not provider absence".
- **Source.** `dist/frida/FridaInstrumentationManager.js:1036-1063` (`providerError`) maps every
  non-input cause to `capability_unavailable`. The module-load failure at `:39`, `:744-749`
  (`import("frida")`) follows the same path. Only `details.reason` discriminates between them.
- **Counterexample CE3.** The same envelope with `details.reason:"Cannot find module 'frida'"`
  produced `matched`.
- **What actually supports the reason:**
  - The discriminating facts are outside this row's predicate: the receipt's
    `details.reason:"Unable to find process with pid 2147483647"`, `pid_max=4194304`, and the
    separate list-frida-devices receipt.
  - The Frida provider is the bundled npm module `frida` 17.23.2 under
    `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/frida`. That corroborates the uncommitted lesson:
    `REA_FRIDA_PYTHON` is not an isolation control (`verify/frida-unsupported-env.json`).
- **Gap in the record.** `verify/frida-unsupported-env.json` is untracked at HEAD, so the provider
  control it records, which failed, is not yet in the record.
- **Smallest safe correction:**
  - Reason cell: "missing-process refusal per details.reason; non-absence rests on
    list-frida-devices receipt (counter checks only error.code)".
  - L1 commits `verify/frida-unsupported-env.json`.

### F5. The cited Cutter receipt has no retained producer or environment record (false provenance)

- **Evidence.**
  - PROVINCE.md:190 cites `evidence/c2/cutter-command-missing.json`.
  - Its `.run.json` keys are only `argv, exit, stderr, stdout`; there is no `verb` and no
    `env_overrides`.
  - `tools/capture-probes.py:30` issues only the malformed `kaidoku-r22-nonexistent` call.
  - `runs.json` and `verify/capture-probes.json` contain no `ffffffff-…` argv; the only occurrence is
    inside the UUID regex text.
- **Contradicted statements:**
  - PROVINCE.md:181: "Each producing argv/env/stdout/stderr/exit is beside its receipt".
  - LOG.md:2473: "`capture-probes.py` records fourteen explicit T2 request outcomes". The cited
    Cutter outcome is not one of them.
  - The uncommitted `corpus/lessons/round-22.md` text: "All producing commands and exact envelopes
    are retained".
- **The reason itself holds up.** It is supported by source, not by the receipt
  ([INFERENCE] from static reading):
  - The `ffff…` UUID and generation `0` pass both zod schemas (`dist/cli/cutterCommands.js`,
    `dist/contracts/cutterToolContracts.js:8-16`).
  - The bridge client's `#find` throws "unavailable or stale" (`dist/cutter/CutterBridgeClient.js:397-399`),
    which maps to `invalid_request` (`dist/cutter/CutterBridgeService.js:133-136`).
  - A failure to read descriptors would instead be `capability_unavailable` (`:395-396`).
  - However, a service-level schema rejection (`CutterBridgeService.js:46-48`) emits the same
    `invalid_request` envelope.
- **Cutter itself.** Cutter is absent from my PATH. Neither line 189 nor line 190 names the missing
  Cutter binary as the real blocker; the empty discovery is consistent with "not installed".
- **Smallest safe correction:**
  - PROVINCE.md:181: append "except cutter-command-missing, an ad hoc invocation outside
    capture-probes.py whose inherited environment was not recorded".
  - LOG.md:2473: say "thirteen of the fourteen cited outcomes".
  - Optionally note that Cutter was not on PATH, observed at review time only.

### F6. Inherited environment and PATH are unrecorded for every receipt (minor provenance)

- **Evidence.** `tools/capture-probes.py:44-48` passes `dict(os.environ, **overrides)` but records
  only `overrides`.
- **Consequence.** The TShark rows (PROVINCE.md:185–188) are real configuration/PATH absences, not
  false-client controls. "ENOENT" and "REA_TSHARK_COMMAND unset" are therefore relative to a PATH and
  environment that were never recorded. The receipts' own text establishes them only for that
  invocation. The reasons are correctly scoped, so no rewrite is needed.
- **Correction (future producers only).** Record `PATH` and every `REA_*` key name and value
  (excluding secrets) in each `.run.json`.

### F7. Counter identity: `counting_command` bytes changed after the freeze (duplicate authority, noted)

- **Evidence.**
  - `claims.json` names `tools/count-c{1,2}.py`, frozen at `75f04a4`.
  - In `2ee3d9f` those files changed: sha256 `ded1a0e8…` and `5fbc6868…`.
  - The frozen originals are kept as `frozen/` (`d3bec8db…` and `d7f67075…`, equal to the `75f04a4`
    blobs).
- **Assessment.** Both successors are strictly tighter: verb==probe at count-c2.py:104, and C1 source
  linkage. On C2 the frozen and successor counters give the same 14/14. No absence-related harm. The
  judge should still read `frozen/` as the declared authority.

## Not found (checked)

- No authored text at HEAD claims an actual absent device. PROVINCE.md:176–180 and LOG.md:2473–2476
  explicitly disclaim it.
- The r22 knowledge entry (`2026-10-21-r22-flutter-static-boundary.md:15`) claims no device or
  provider absence.
- C1 involves no false-client control. Its unclaimed debugger/signal verbs are left unclaimed
  (PROVINCE.md:203–204), not called absent.

## Addendum: re-review of the current bytes after the parent's message

The parent asked me to review the actual bytes rather than replacing them, and not to repeat
identical REA probes. I ran no REA probes; I only re-ran the counters, the selftests and scratch
counterexamples.

HEAD is still `2ee3d9f`. Several working-tree files are uncommitted and still changing:
- `tools/count-c1.py`: sha256 `a7ec076a…`
- `tools/count-c2.py`: sha256 `0d51a87f…`
- `tools/counter-fixtures.py`: sha256 was `c5b49567…` when I first read it and `4ad9e192…` at my
  selftest run, so it changed during this review
- `verify.py`, `LOG.md`, `corpus/SOURCES.md` (S054), the r22 knowledge entry and the round-22 lesson
- `PROVINCE.md` is unchanged from HEAD

### What changed and what didn't

- **`count-c2.py` vs HEAD.** Only the docstring changed (it now states probe == verb) and an unused
  `import re` was removed. The predicate code is byte-identical, so F1–F5 apply to the current bytes.
- **`count-c1.py`.** It now loads helpers from the requested revision and binds only the original CLI
  envelope (`ok`, `meta.command`, refusal ancestry), mapping gdb/rizin to `gdb-console` and
  `rizin-debug-command`. None of this affects absence claims. C1 makes no device or provider
  absence claim.
- **LOG.md working-tree addendum** (lines 2486–2505). It corrects the W1 parent-death narrative but
  does not touch F5: LOG.md:2473 still says `capture-probes.py` recorded all fourteen outcomes.

### Re-run on current bytes

| argv (cwd = lane) | exit | observed |
|---|---|---|
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --selftest` | 0 | `counter_controls_clean`: all_fourteen, probe_alias, wrong_code, duplicate_row, outside_path, duplicate_json, empty_section all pass |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --selftest` | 0 | `counter_controls_clean`: 11 cases pass, including wrong_command, extraction_only, refused_with_extraction, forged_debug_operation (4), helper_drift (6) |
| `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root $PWD --rev HEAD` | 0 | 14/14, mismatched [], foreign [] |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root $PWD --rev HEAD` | 1 | [identify-flutter-build], 1/6 |
| scratch clone at `2ee3d9f` with four contradicting receipts, current `count-c2.py` bytes (sha `0d51a87f…` copied before running) | 0 | 14/14; all four `matched` (details below) |

The four contradicting receipts in the scratch clone:
- CE1: list-frida-devices with `devices:[]`
- CE2: list-frida-processes with `processes:[]`
- CE3: instrument-with-frida with `details.reason:"Cannot find module 'frida'"`
- CE4 (new): inspect-adb-package with the real-absence message "The selected adb binary was not
  found: /usr/bin/adb", which is the `binary_missing` path

CE4 shows the current counter accepts an actual-absence receipt on a row whose reason says it is a
false-client control. The F1 conflation is no longer just inferred from source; it was observed.

### F8. The C2 selftest never exercises the `ok-empty`/`ok-field` branches (coverage of the controls)

- **Evidence.** `counter-fixtures.py` (current bytes) has `c2_files()` writing all 14 receipts as
  `{'ok':False,'error':{'code':'capability_unavailable'}}` with `error:capability_unavailable` rows.
  Its six mutants change only the code, the probe, duplication, the path, JSON, or the section.
  Grep finds no `ok-empty` or `ok-field` fixture.
- **Effect.** The three real rows that use those branches (PROVINCE.md:189, 191, 192) depend on
  `dig` and `strict(literal)` (count-c2.py:79–84, 111–116), and no green or red control covers
  them. CE1 and CE2 are exactly the missing reds.
- **Smallest safe correction (fixtures only; the counter is unchanged):** add four C2 cases.
  - `ok_empty_nonempty`: `ok-empty:sessions` row with a receipt where `sessions:[{}]`; expect
    `observed_mismatch`, 13, exit 1.
  - `ok_field_wrong`: `ok-field:device_id="local"` with `device_id:"usb"`; expect
    `observed_mismatch`, 13, exit 1.
  - `ok_field_missing_path`: same row with no `device_id`; expect `observed_mismatch`
    (`KeyError` path), 13, exit 1.
  - `ok_false_with_field`: `ok:false` plus matching data; expect `observed_mismatch`, 13, exit 1.

  Keep `all_fourteen` green. If F2's `devices=[...]` predicate is adopted, also add CE1 as a red.

### Status of the earlier findings

| finding | status on current bytes |
|---|---|
| F1 ADB control vs real absence | open; observed by CE4 |
| F2 devices predicate vacuous | open; the fix is still compatible |
| F3 processes predicate vacuous | open |
| F4 Frida absent-provider receipt accepted | open; `verify/frida-unsupported-env.json` still untracked |
| F5 Cutter receipt producer unretained | open; LOG.md:2473 and PROVINCE.md:181 unchanged |
| F6 inherited environment unrecorded | open; `capture-probes.py` unchanged (sha `33bdd36b…`) |
| F7 counter identity changed after freeze | still applies; `tools/` changed further in the working tree, and the measurements need to name their source sha |
| F8 ok-branch controls missing | new |

Blocker: none. The working tree is moving, so these observations are valid only for the shas listed
above.

## Impacted axes

- **Calibration:** F1–F5.
- **Coverage:** F8 (coverage of the counter's own controls). Lane knowledge coverage: none.
- **Provenance/identity:** F5 and F6 (provenance), F7 (counter identity).
