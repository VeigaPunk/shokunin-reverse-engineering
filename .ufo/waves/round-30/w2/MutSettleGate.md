# MutSettleGate — round 30, wave 2
## Scope and verdict
**[OBSERVATION] 12 single-clause mutants: 5 killed, 7 survived, 0 inconclusive.** The same `--selftest` detector was run on pristine, mutated and exactly restored bytes for every mutant (36 invocations, 13 fixtures each). All 24 pristine/restored controls exited 0. All mutants completed the fixture suite; none was counted as killed by syntax error, crash or timeout.
**Attack:** the sensitivity of the settlement gate’s own selftest, including its line-266 claim, “Fixtures for every finding and error path”. **Verdict: fails for mutation sensitivity:** M06–M12 all retain `selftest cases=13 failures=0`, exit 0. This is a selftest-coverage finding, not a measured failure of the pristine gate or permission to change its contract.
Axes: selftest sensitivity; single-clause isolation; exact-byte restoration; read-only lane safety. Mutations touched only the assigned scratch copy. The lane gate, lane index and sibling sources were not edited. No Git/JJ commands, agents, REA, carriers, foreign binaries, services or background jobs were used. Python 3.14.8 was already installed; no tool installs/updates.
## Detector and recording protocol
Source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py`. Scratch: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py`. No selftest fixture or expectation was changed. Each mutation replaces exactly the one line listed below; the reconstructed one-line mutant hash equals the hash recorded immediately before that mutated run.
For every literal ID M01–M12, the recorder was invoked for phases `before`, `mutated`, `restored` in that order, with the byte edit/restoration between the corresponding invocations. Each wrapper command was bounded by 85 seconds:
```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py <ID> <phase>
```
The identical bounded detector argv in every run was:
```text
/usr/bin/timeout --kill-after=5s 60s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py --selftest
```
The recorder set `TMPDIR` to a unique directory under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/tmp/`. Every JSON receipt contains the exact command including that absolute TMPDIR, full stdout/stderr, detector exit code, start/end UTC and before/after source/scratch SHA-256. Table exit codes below are the **detector’s** codes, not the recorder’s successful capture exit. Temporary fixture trees were removed after capture; retained receipts remain. All invocations completed synchronously; there is no started process tree left running.
## Mutant table
| ID | Source line | Single-line change | Expected detector |
|---|---:|---|---|
| M01 | 220 | `elif got != row["sha"]:` → `elif got == row["sha"]:` | Existing green returned-report cases and red-r28-report-changed-after-filing should fail. |
| M02 | 222 | `elif exists and not row["note_present"]:` → `elif exists and row["note_present"]:` | Existing red-cancelled-report-without-note and green-cancelled-report-with-note should fail. |
| M03 | 228 | `if findings:` → `if len(findings) > 1:` | Existing one-finding red cases should fail. |
| M04 | 198 | `if len(index[name]) > 1:` → `if len(index[name]) > 2:` | Existing error-ambiguous-bare-key should fail. |
| M05 | 145 | `if name in rows:` → `if name in rows and row["status"] == rows[name]["status"]:` | Existing error-duplicate-row (returned then cancelled) should fail. |
| M06 | 149 | `if not UTC_RE.match(row["utc"]):` → `if not row["utc"]:` | A malformed nonempty utc must yield exit 2; no such fixture is visible in selftest. |
| M07 | 156 | `if row["status"] == "returned" and sha is None:` → `if row["status"] == "returned" and sha == "":` | Returned rows without a settled report hash must yield exit 2; no such fixture is visible in selftest. |
| M08 | 160 | `row["note_present"] = bool(note) and note != "-"` → `row["note_present"] = bool(note)` | A cancelled/dead seat leaving a report with note='-' must yield REPORT_WITHOUT_NOTE; no such fixture is visible in selftest. |
| M09 | 222 | `elif exists and not row["note_present"]:` → `elif exists and row["status"] == "cancelled" and not row["note_present"]:` | A dead seat with a report and no note must yield REPORT_WITHOUT_NOTE; no such fixture is visible in selftest. |
| M10 | 102 | `if data.get("reportDir") is not None:` → `if data.get("reportDir") is None:` | A registry with a distinct valid reportDir must locate its returned report there; all selftest reportDir values equal the registry directory. |
| M11 | 111 | `if not regs:` → `if regs is None:` | An existing round with no swarm registry must yield exit 2; no such fixture is visible in selftest. |
| M12 | 147 | `if row["status"] not in STATUSES:` → `if row["status"] not in STATUSES + ("running",):` | A running status must yield exit 2; the sole invalid-status selftest uses done. |

## Actual mutant outputs
All UTC values are recorded observations. The exact producing wrapper command for each row is also listed below. Full underlying gate output is preserved in the corresponding JSON receipt.
| ID | Mutated run start (UTC) | Exit | Exact stdout summary | Verdict |
|---|---|---:|---|---|
| M01 | 2026-10-23T03:14:30.279773Z | 1 | `selftest cases=13 failures=4` | **killed** |
| M02 | 2026-10-23T03:14:46.660153Z | 1 | `selftest cases=13 failures=3` | **killed** |
| M03 | 2026-10-23T03:15:02.907601Z | 1 | `selftest cases=13 failures=5` | **killed** |
| M04 | 2026-10-23T03:15:17.502427Z | 1 | `selftest cases=13 failures=1` | **killed** |
| M05 | 2026-10-23T03:15:32.382937Z | 1 | `selftest cases=13 failures=1` | **killed** |
| M06 | 2026-10-23T03:15:43.935185Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M07 | 2026-10-23T03:15:55.931831Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M08 | 2026-10-23T03:16:09.169008Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M09 | 2026-10-23T03:16:22.381709Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M10 | 2026-10-23T03:16:35.100334Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M11 | 2026-10-23T03:16:47.763089Z | 0 | `selftest cases=13 failures=0` | **survived** |
| M12 | 2026-10-23T03:17:00.547642Z | 0 | `selftest cases=13 failures=0` | **survived** |

### Exact producing commands and excerpts

**M01 — [OBSERVATION], 2026-10-23T03:14:30.279773Z, detector exit 1:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M01 mutated
FAIL green-clean got=1 want=0 code='<absent>'
FAIL red-r28-report-changed-after-filing got=1 want=1 code='<absent>'
FAIL green-qualified-keys-two-waves got=1 want=0 code='<absent>'
FAIL green-stray-row-warns got=1 want=0 code='WARN STRAY_ROW Ghost'
selftest cases=13 failures=4
```

**M02 — [OBSERVATION], 2026-10-23T03:14:46.660153Z, detector exit 1:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M02 mutated
FAIL green-clean got=1 want=0 code='<absent>'
FAIL red-cancelled-report-without-note got=0 want=1 code='<absent>'
FAIL green-cancelled-report-with-note got=1 want=0 code='<absent>'
selftest cases=13 failures=3
```

**M03 — [OBSERVATION], 2026-10-23T03:15:02.907601Z, detector exit 1:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M03 mutated
FAIL red-missing-row got=0 want=1 code='MISSING_ROW w1/ScoutD'
FAIL red-returned-report-absent got=0 want=1 code='REPORT_ABSENT w1/ExecA'
FAIL red-r28-report-changed-after-filing got=0 want=1 code='REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix'
FAIL red-cancelled-report-without-note got=0 want=1 code='REPORT_WITHOUT_NOTE w1/CriticC'
FAIL red-no-ledger got=0 want=1 code='MISSING_LEDGER'
selftest cases=13 failures=5
```

**M04 — [OBSERVATION], 2026-10-23T03:15:17.502427Z, detector exit 1:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M04 mutated
FAIL error-ambiguous-bare-key got=1 want=2 code='<absent>'
selftest cases=13 failures=1
```

**M05 — [OBSERVATION], 2026-10-23T03:15:32.382937Z, detector exit 1:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M05 mutated
FAIL error-duplicate-row got=1 want=2 code='<absent>'
selftest cases=13 failures=1
```

**M06 — [OBSERVATION], 2026-10-23T03:15:43.935185Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M06 mutated
selftest cases=13 failures=0
```

**M07 — [OBSERVATION], 2026-10-23T03:15:55.931831Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M07 mutated
selftest cases=13 failures=0
```

**M08 — [OBSERVATION], 2026-10-23T03:16:09.169008Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M08 mutated
selftest cases=13 failures=0
```

**M09 — [OBSERVATION], 2026-10-23T03:16:22.381709Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M09 mutated
selftest cases=13 failures=0
```

**M10 — [OBSERVATION], 2026-10-23T03:16:35.100334Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M10 mutated
selftest cases=13 failures=0
```

**M11 — [OBSERVATION], 2026-10-23T03:16:47.763089Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M11 mutated
selftest cases=13 failures=0
```

**M12 — [OBSERVATION], 2026-10-23T03:17:00.547642Z, detector exit 0:**

```text
timeout --kill-after=5s 85s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py M12 mutated
selftest cases=13 failures=0
```

## Survivors as missing cases
**[INFERENCE]** The following are concrete missing-case specifications derived from the unchanged contract and the isolated mutant. They were **not** executed as additional detectors or added to the lane. Survival itself is observed above. Expected behavioral differences below are source-based inferences.

- **M06, line 149:** Returned row with correct report hash and utc='yesterday': require exit 2 and not ISO-8601 Zulu. With correct report/hash, the suggested malformed nonempty timestamp changes expected gate exit 2 to mutant exit 0.

- **M07, line 156:** Returned row with report_sha256='-' (also blank), valid utc and existing report: require exit 2 and records no report_sha256. With an existing report, the missing settled hash changes expected gate exit 2 to mutant exit 1 (REPORT_SHA_MISMATCH), not necessarily a false PASS. The selftest still misses the required error classification.

- **M08, line 160:** Cancelled seat with existing report and note='-': require exit 1 and REPORT_WITHOUT_NOTE. Repeat for dead. The sentinel note changes expected gate exit 1 to mutant exit 0.

- **M09, line 222:** Dead row, existing report, valid sha/utc, omitted or blank note: require exit 1 and REPORT_WITHOUT_NOTE. The dead/no-note report changes expected gate exit 1 to mutant exit 0. The existing dead-seat green fixture carries a note and cannot distinguish this mutant.

- **M10, line 102:** Place a returned report in a valid nondefault reportDir and require exit 0; omit reportDir with report beside registry and require exit 0. A report only in a nondefault reportDir changes expected gate exit 0 to mutant exit 1 (REPORT_ABSENT). An omitted reportDir would also expose the inverted lookup via an uncaught KeyError. Current fixtures set reportDir equal to the registry directory.

- **M11, line 111:** Existing round directory, valid header-only settle.tsv, no swarm-registry.json: require exit 2 and no swarm-registry.json under. An existing round with a header-only ledger and no registry changes expected gate exit 2 to mutant exit 0.

- **M12, line 147:** Seat has no report and a row with status='running', valid utc and sha='-': require exit 2 and status. A running seat with no report changes expected gate exit 2 to mutant exit 0; the existing invalid-status test checks only done.

## Pristine and restoration controls
**[OBSERVATION]** Every before/restored run produced the following byte-identical stdout, exit 0, empty stderr:

```text
ok green-clean got=0 want=0 code='settle: PASS'
ok red-missing-row got=1 want=1 code='MISSING_ROW w1/ScoutD'
ok red-returned-report-absent got=1 want=1 code='REPORT_ABSENT w1/ExecA'
ok red-r28-report-changed-after-filing got=1 want=1 code='REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix'
ok red-cancelled-report-without-note got=1 want=1 code='REPORT_WITHOUT_NOTE w1/CriticC'
ok green-cancelled-report-with-note got=0 want=0 code='settle: PASS'
ok red-no-ledger got=1 want=1 code='MISSING_LEDGER'
ok green-qualified-keys-two-waves got=0 want=0 code='settle: PASS'
ok error-ambiguous-bare-key got=2 want=2 code='is ambiguous'
ok error-bad-status got=2 want=2 code='status'
ok error-bad-sha got=2 want=2 code='not a sha256'
ok error-duplicate-row got=2 want=2 code='duplicate ledger row'
ok green-stray-row-warns got=0 want=0 code='WARN STRAY_ROW Ghost'
selftest cases=13 failures=0
```
| ID | Pristine run start UTC / exit | Restored run start UTC / exit |
|---|---|---|
| M01 | 2026-10-23T03:14:24.417138Z / 0 | 2026-10-23T03:14:36.676957Z / 0 |
| M02 | 2026-10-23T03:14:36.746065Z / 0 | 2026-10-23T03:14:52.647581Z / 0 |
| M03 | 2026-10-23T03:14:52.748068Z / 0 | 2026-10-23T03:15:09.643991Z / 0 |
| M04 | 2026-10-23T03:15:09.721079Z / 0 | 2026-10-23T03:15:25.125393Z / 0 |
| M05 | 2026-10-23T03:15:25.220261Z / 0 | 2026-10-23T03:15:38.351416Z / 0 |
| M06 | 2026-10-23T03:15:38.428886Z / 0 | 2026-10-23T03:15:50.340351Z / 0 |
| M07 | 2026-10-23T03:15:50.424791Z / 0 | 2026-10-23T03:16:03.181565Z / 0 |
| M08 | 2026-10-23T03:16:03.261188Z / 0 | 2026-10-23T03:16:15.946902Z / 0 |
| M09 | 2026-10-23T03:16:16.014858Z / 0 | 2026-10-23T03:16:28.686699Z / 0 |
| M10 | 2026-10-23T03:16:28.754754Z / 0 | 2026-10-23T03:16:41.554757Z / 0 |
| M11 | 2026-10-23T03:16:41.624759Z / 0 | 2026-10-23T03:16:55.030522Z / 0 |
| M12 | 2026-10-23T03:16:55.108855Z / 0 | 2026-10-23T03:17:11.047371Z / 0 |

The source and every pristine/restored scratch state share SHA-256:

```text
1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5
```
Each of all 36 receipts also records identical before/after scratch hashes for its own detector run and the same unchanged lane-source hash above. Final restored detector: 2026-10-23T03:17:11.047371Z–2026-10-23T03:17:11.087008Z, exit 0.
Independent restoration command, observed at 2026-10-23T03:17:11Z, exit 0 (the `cmp` emitted no output):

```text
timeout 20 sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py /home/vgpnk/.omp/agent/RULES.md /home/vgpnk/.agents/skills/godspeed/SKILL.md && timeout 20 date -u +%Y-%m-%dT%H:%M:%SZ && timeout 20 cmp -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py
1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py
1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py
2026-10-23T03:17:11Z
```
The excerpt omits the two ancillary rules/skill hash lines, reproduced in the source table below.

### Mutant byte hashes

| ID | Mutated SHA-256 |
|---|---|
| M01 | `9a6ddb02695b4611ebae1bdcbe9cb81b9b8a56eb5824ced4b173929c69db61a5` |
| M02 | `11569d85265ffbe8a6090cfaa9befe600ceb9828ecbff9314484f018d1b86077` |
| M03 | `17f00748876f3e8bbdb522d65371757b79971abc0161e65245e111dc8c4b97c0` |
| M04 | `a1623528c90335e78def7a03ac9c0b3af5a53e5d9dee7eb215d987e93dc7edd1` |
| M05 | `d5391786fa75dcd8550870aba6b32dae71ad2fdf6aeb2e3db9afc7ec80e91215` |
| M06 | `992f4841e6592c2a80c7d0a81354a1df050c11c0388e098f41b006f805107ce8` |
| M07 | `200479fa466be6c8e15cae4882e573990f7a9d5e04345ad807c9a1fb1e1e1c1a` |
| M08 | `3447e3e0e0ebe3082b0b0915a32881f2f5f9dd6d300696be1159236f7d167db5` |
| M09 | `a18c33080fba5332f7e850806285e7ed0070644bf04065966c8d149f3159d79b` |
| M10 | `95cf06b9d73e8a6b449dc8c71d53a8667d62b3e3eb6b1218103b3a389cdb6db2` |
| M11 | `e0144b2f08871e7ae9ec170c314292b8120da7ccf7d1bdedda13351bb8fe201d` |
| M12 | `9a9e643e5630b72d1fb58a73f652f21bbe1eb9632cab55f7a97bc684fb297f65` |

## Opened primary local sources
Access date: **2026-10-23**. Ordinary local reads only; no network sources or access-control bypass. Quotes are at most 25 contiguous words from served bytes.
| URL | SHA-256 (whole file) | Located quote |
|---|---|---|
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/settle-gate.py | `1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5` | Line 266: “Fixtures for every finding and error path, including the round-28 shape” |
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 4: “helps its task or is a strict upgrade, with full privilege, without asking first.” |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 12: “Name the axes.” |

## Retained artifact SHA-256 inventory
All 39 retained scratch files are listed below; temporary fixtures were removed. The scratch gate is restored, not a surviving mutant. The report itself is the only lane write.

```text
1e37592a3a5df1c7e34999ff8ff3fe9238bb983cef012373fc85f386b24e5e14  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M01-before.json
c5b84d5484a6f631c13bcbe702ccf47bd1e471cb92b2dad44d7071f7f61e67a9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M01-mutated.json
2c46463c40e0b14f1fd34cec14bb34fe6cecfaf9660983f3fb67b5ab51cfc2c7  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M01-restored.json
de4482a05d0cd245cb90e350352b4ceaf67e303b84b6c1fc2e98c6870c213687  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M02-before.json
25a72fd99407603ba7086391092268a00b5634cb214043fe8c4d8fccd19a3ff6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M02-mutated.json
983f70603e15c889b861aa9dda0c72b2ce4653d9366b4265e67a0a297ede6797  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M02-restored.json
3300a13575f0abf392d16c2beb285144b616d7161479ab8940d6c5b031a4eeca  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M03-before.json
2c41c2d1fca203d60f33f1f90818297433714eb2bc103834609e605b8a03c748  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M03-mutated.json
836650229cd0d100cee2d23c191a0b3f8ca5f1bfad378a3ce2b27bf7f611090b  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M03-restored.json
ddc99d30f4bc653198e110b92c4677d26d8e3f61b56fd073d7127ddb4f8339da  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M04-before.json
477e12c3d4da2e3a8bce0ad2dc048b35798cfb88030593771454c37ae0df48ea  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M04-mutated.json
253215810482f89f10ce0ad4dca12f11f21026bf484df828afb751de34b9c0f0  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M04-restored.json
babcc7fde21ac3a344d459b5f4289a6bc532777942dfaa06504b7ea54c83d1b4  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M05-before.json
19135d3833f50806742b4dff5a43843c070dbfa79f7c95e6e7680267bae5b494  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M05-mutated.json
42f6f2a88404147b7fbc8b263d373424fa04ab4538d000c906e58e263f8176bd  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M05-restored.json
78abe1ad6ad998843c13ad7bea0bd44e7a9b93d836bd28111049f5e879de67b6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M06-before.json
e5dbc8f5fb163ad82939e87aad951791a7f27c4a257ffbd42afab0c12b7783fd  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M06-mutated.json
ae627bf1666f51b7ffd90d73ee76d0c21a7fdd6187b96721444b0540baae0a8e  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M06-restored.json
6ee06d21c33b7ecc743f932a6ecd1ce8d80dd02a3500d3d89d166a5b92770a46  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M07-before.json
debd9d13d559a6ff8dd79bff0630f4b6c770b0805265d2a6485d6f4ccff45f70  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M07-mutated.json
aeca975b918f1f65b8df23287c5f93b908aec7abf9c6bbb7096f8d4c5a8ec2ff  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M07-restored.json
46778fa4a7d3b3f5100243d1013350b90907c6db052362518a20a2fd13680717  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M08-before.json
cb48e82e768c4e23ba6f501c5ae8325c39091f639dd4976d8c39a8bee18fa673  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M08-mutated.json
2768771fd16f8e4c240e48c0e54984efa72a27f74f4f21d6fa09c6e6bab28f83  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M08-restored.json
8710b1309375fd6f94c6d2dad36bcefc86cb531f8458370754a40cff8434cd90  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M09-before.json
05c1d15bf95e10fdd69dd100e9c2a506aedf18390e3501355dd72d64f3740ee9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M09-mutated.json
295a472e2c6c2e3a6c21d859de27e61420980b1b1cf2dad99fcbcfa03cc82dc2  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M09-restored.json
8558a2a76b105ba66cce217f03ea042f0f2f4a8faad015be9b82491db637b2bc  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M10-before.json
d4067716c60afa6ccc5c4b8a0dd7aed6f79fed48afdac88282562341c666cae6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M10-mutated.json
8b83fb9aa73280a379b45d2516e4af876cb33b49992b51e7e238b10c4f0ad4c9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M10-restored.json
5d07c7b7c5f7e66192d5aaa23411d0c530316e2d78ebce996169976d4767d555  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M11-before.json
1ef0cf9a9156f5652815b6fbd3f61fc875ca1d12cdce417e2a0bb32957a818e1  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M11-mutated.json
bb6e50f8d368ccfb7df63da1e104664f8c2a592c62506af0b8930dea3e64b1d9  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M11-restored.json
39ba9b1af22f8e20c0337639b5b4470bada22fd0893dc77d48f224342c3e5c8e  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M12-before.json
c54224bf0d93331422e5933e38c073e26d0bc41d4076e5b253373eef0d6a2273  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M12-mutated.json
0d07c71ee830018e6f3365b2eb7b1fb09ce75dea595bcdb9a6895f6ce572e5af  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/logs/M12-restored.json
5e8a5167560e71ef2edd64f32bf3a66e9a5d64c172d6a152ac252121a7ecaeb6  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/mutants.json
4271f77c1597a973e8e6f944a3cd6884414c70e451438085e19f9c4000bdc7fb  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/run-probe.py
1121e48b226689d2aaa6eec97752eacbee2d3b844b36c9da43bf691b29a598f5  /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutSettleGate/settle-gate.py
```

**[UNKNOWN / not exercised]** The proposed missing cases were not run; no wider gate integration, filing workflow, C1/C2 counter or REA behavior was evaluated. No contract or production fix was made. The probe is complete at the restored bytes.
