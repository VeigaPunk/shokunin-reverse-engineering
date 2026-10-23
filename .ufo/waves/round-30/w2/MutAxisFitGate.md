# MutAxisFitGate — round 30, wave 2
## Result
**[Observation] 12 single-clause mutants exercised; 6 killed, 6 survived, 0 inconclusive (50% kill rate).** The attacked invariant was that the gate's own selftest rejects plausible regressions in its pass/fail clauses. **Verdict: fails for this mutation set:** M03, M04, M05, M06, M09 and M11 passed the unchanged selftest. This is a selftest coverage finding, not a finding that the pristine gate or either frozen lane claim is false.
Axes: behavioral discrimination, clause coverage, and exact-byte restoration/isolation.
## Scope and method
- Target source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/axis-fit-gate.py`. All source mutations and detector Git fixture writes were isolated under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/`.
- Each mutant changes one clause on one source line, all before the fixture/selftest implementation. The detector and its expectations were not changed. Each row used the same scratch source pathname for pristine, mutant, and restored phases.
- [Observation] 36 bounded `--selftest` invocations completed (12 pristine, 12 mutated, 12 restored). All 24 pristine/restored invocations printed `selftest cases=18 failures=0`, exited 0, and had empty stderr. No detector timeout occurred. Four independent scratch targets ran concurrently.
- Every detector command used `timeout --kill-after=5 60`; the supervising command was bounded to 600 seconds. All detector subprocesses were reaped and their process groups cleaned up in the runner's finally path. Generated Git fixture directories were removed. No subagents, REA operations, carrier/mutant binaries, C1/C2 counters, network sources, or lane Git/jj writes were used.
- [Observation] No tools installed or updated. Installed tools used included Python 3.14.8 and Git 2.56.0.
### Runner bookkeeping correction (not a detector rerun)
Producing runner command:

```text
timeout --kill-after=10 600 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/run-probes.py
```
[Observation] UTC 2026-10-23T03:15:25.650902Z to 2026-10-23T03:15:36.954732Z; runner exit 1. Its initial classification was wrong because it required **19** cases, whereas the pristine detector actually reported **18**, exit 0. Its stdout included `M01 inconclusive exits=0/1/0 selftest cases=18 failures=1` and `counts={"inconclusive": 12, "killed": 0, "survived": 0}`. This was not a baseline failure.
Original `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/results.json` and all raw logs remain unchanged. A read-only analysis of those recorded exit codes, summaries, failure lines and restoration hashes produced `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/classified-results.json` at 2026-10-23T03:16:37.420166Z. It derives the case count from the actual baseline instead of assuming 19. **No selftest was rerun to obtain the corrected counts.**
## Mutant table
[Observation] B/M/R are pristine/mutated/restored detector exits. Expected detector names refer to the existing selftest; missing cases are described separately as unrun inferences. Source line numbers refer to pristine bytes.
| ID | Line | Single-clause change | Expected detector | B/M/R exits | Mutant stdout summary | Verdict |
|---|---:|---|---|---|---|---|
| M01 | 59 | `^(coverage\|depth)\b` → `^(coverage)\b`; Drops depth-axis claims | red-control-missing | 0/1/0 | `selftest cases=18 failures=1` | killed |
| M02 | 130 | `claim[key].strip()` → `claim[key]`; Accepts whitespace-only fields | red-surface-blank | 0/1/0 | `selftest cases=18 failures=1` | killed |
| M03 | 128 | `key not in claim or not isinstance(claim[key], str)` → `key not in claim`; Drops field-type guard | Missing non-string-field case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M04 | 160 | `met_target.lower() != 'no'` → `met_target.lower() == 'yes'`; Only rejects yes, not other invalid tokens | Missing invalid-met_target case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M05 | 148 | `len(cells) != 4 or not cells[0].strip() or not cells[1].strip()` → `len(cells) != 4 or not cells[0].strip()`; Drops nonempty receipt-control guard | Missing blank-control-cell case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M06 | 231 | `isinstance(x, str) and x.strip()` → `isinstance(x, str)`; Drops nonblank required-control guard | Missing blank-required-control case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M07 | 261 | `r_add[1] < e_add[1]` → `r_add[1] <= e_add[1]`; Allows equal committer timestamps | red-receipts-same-commit | 0/1/0 | `selftest cases=18 failures=1` | killed |
| M08 | 179 | `len(heads[head]) == 1` → `len(heads[head]) >= 1`; Allows ambiguous shortened control names | red-control-head-ambiguous | 0/1/0 | `selftest cases=18 failures=1` | killed |
| M09 | 177 | `(claim_id, name) in cells` → `any(cell[1] == name for cell in cells)`; Exact control matching loses claim scope | Missing cross-claim exact-name case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M10 | 140 | `lines[0].split('\t') != RECEIPTS_HEADER` → `len(lines[0].split('\t')) != len(RECEIPTS_HEADER)`; Checks only header column count | red-header-invalid (finding code) | 0/1/0 | `selftest cases=18 failures=1` | killed |
| M11 | 119 | `len(rest) >= 3` → `len(rest) == 3`; Ignores envelope files in nested subdirectories | Missing nested-envelope-ordering case | 0/0/0 | `selftest cases=18 failures=0` | survived |
| M12 | 296 | `0 if not findings else 1` → `0 if findings else 1`; Reverses audit exit-code selection | green-basic and 14 other cases | 0/1/0 | `selftest cases=18 failures=15` | killed |

## Exact mutated-output excerpts
[Observation] Each command below is identified as `D-<ID>-mutated` in the full command ledger. These are exact stdout lines, not reconstructed diagnostics. UTC is the actual mutated invocation interval. Full stdout/stderr is retained in the hashed logs.

### M01 — killed

Command: `D-M01-mutated`; UTC 2026-10-23T03:15:26.644207Z to 2026-10-23T03:15:28.169906Z; detector exit 1.

```text
FAIL red-control-missing exit=0 findings=- want_exit=1 want=CONTROL_MISSING
selftest cases=18 failures=1
```

### M02 — killed

Command: `D-M02-mutated`; UTC 2026-10-23T03:15:26.648793Z to 2026-10-23T03:15:28.210767Z; detector exit 1.

```text
FAIL red-surface-blank exit=0 findings=- want_exit=1 want=SURFACE_EMPTY
selftest cases=18 failures=1
```

### M03 — survived

Command: `D-M03-mutated`; UTC 2026-10-23T03:15:26.648173Z to 2026-10-23T03:15:28.128375Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M04 — survived

Command: `D-M04-mutated`; UTC 2026-10-23T03:15:26.651006Z to 2026-10-23T03:15:28.168102Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M05 — survived

Command: `D-M05-mutated`; UTC 2026-10-23T03:15:30.477045Z to 2026-10-23T03:15:31.640417Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M06 — survived

Command: `D-M06-mutated`; UTC 2026-10-23T03:15:30.556266Z to 2026-10-23T03:15:31.695516Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M07 — killed

Command: `D-M07-mutated`; UTC 2026-10-23T03:15:30.562499Z to 2026-10-23T03:15:31.733471Z; detector exit 1.

```text
FAIL red-receipts-same-commit exit=0 findings=- want_exit=1 want=RECEIPTS_NOT_BEFORE_ENVELOPES
selftest cases=18 failures=1
```

### M08 — killed

Command: `D-M08-mutated`; UTC 2026-10-23T03:15:30.897295Z to 2026-10-23T03:15:31.997173Z; detector exit 1.

```text
FAIL red-control-head-ambiguous exit=0 findings=- want_exit=1 want=CONTROL_MISSING
selftest cases=18 failures=1
```

### M09 — survived

Command: `D-M09-mutated`; UTC 2026-10-23T03:15:34.035342Z to 2026-10-23T03:15:35.395388Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M10 — killed

Command: `D-M10-mutated`; UTC 2026-10-23T03:15:34.097115Z to 2026-10-23T03:15:35.433725Z; detector exit 1.

```text
FAIL red-header-invalid exit=1 findings=CONTROL_MISSING want_exit=1 want=RECEIPTS_HEADER_INVALID,CONTROL_MISSING
selftest cases=18 failures=1
```

### M11 — survived

Command: `D-M11-mutated`; UTC 2026-10-23T03:15:34.216606Z to 2026-10-23T03:15:35.499516Z; detector exit 0.

```text
selftest cases=18 failures=0
```

### M12 — killed

Command: `D-M12-mutated`; UTC 2026-10-23T03:15:34.654758Z to 2026-10-23T03:15:35.816575Z; detector exit 1.

```text
FAIL green-basic exit=1 findings=- want_exit=0 want=-
selftest cases=18 failures=15
```

## Survivors as missing cases
**[Inference; not run]** The following additional fixtures are predicted to distinguish pristine from each survivor, using the existing contract and finding codes. No production fix, new contract, or passing witness run is claimed.

- **M03:** Supply a non-string surface (for example integer 17), and separately a non-string unmoved_command, in an otherwise valid axis claim. Pristine code should exit 1 with SURFACE_MISSING or UNMOVED_COMMAND_MISSING; the mutant reaches .strip() on a non-string and should instead become exit 2/unevaluable. The existing suite tests absent and blank surface values, but not these non-string values.

- **M04:** Replace one otherwise valid receipt's met_target with maybe (also useful: an empty token). Expect exit 1 and MET_TARGET_INVALID. The mutant only enters the rejection branch for yes and should accept this receipt. Current cases cover no and yes only.

- **M05:** Append a four-cell receipt row with a valid claim id, an empty/whitespace control cell, integer counter_exit, and met_target no to otherwise complete receipts. Expect exit 1 and RECEIPTS_ROW_INVALID. The mutant should accept the unused malformed row. The existing red-row-invalid has only three cells, so the remaining length guard still rejects it.

- **M06:** Use controls_required_before_data containing a whitespace-only string. Expect CONTROLS_LIST_INVALID. A fixture with only the existing calibration claim isolates a pass/fail difference: pristine should exit 1, whereas the mutant's no-axis path should exit 0. An axis-bearing variant can also assert the exact invalid-list finding rather than merely a nonzero exit.

- **M09:** Adapt red-control-missing so C1 records the full frozen name junk-row (entry without envelopes), while C2 lacks that control. Expect exit 1 and CONTROL_MISSING for C2. The mutant should reuse C1's exact-name receipt for C2. The current missing-control fixture supplies C1's shortened junk-row cell, which does not exercise the mutated exact-match branch.

- **M11:** Commit an envelope at the absolute proposed fixture path `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/proposed-nested-envelope/corpus/evidence/round-99/c1/envelopes/nested/e1.json` inside an isolated fixture repository at T0, then claims and valid receipts at T1. Expect exit 1 and RECEIPTS_NOT_BEFORE_ENVELOPES. The mutant should ignore the deeper envelope, declare ordering vacuous, and exit 0. Current envelope fixtures have no nested directory below envelopes.

## Restoration evidence
[Observation] Source SHA-256 before and after the wave, and every pristine/restored scratch source SHA-256, were identical:

```text
1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63
```
- Lane before: `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63`; lane after: `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63`. These are source-byte measurements, not an assertion about a Git revision.
- All twelve scratch `.py` targets were restored byte-for-byte; their baseline/restored hashes are in the phase receipts and their final hashes are in the artifact table. Archived `.mutant.bytes` files intentionally preserve the exact tested mutant bytes and were not executed.
| Mutant | Mutated-byte SHA-256 | Restored-byte SHA-256 |
|---|---|---|
| M01 | `5e5eb02a0c4a33b56603763c7601802daaf4fd93927bb04e8d169db46ee057c0` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M02 | `d8a560fc544544df3f908ff2c0753163ee5befd48ff4f624d0210f09a4a84825` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M03 | `0bb7f9b20d77624d5a89bc5c3effe9fb121a6232ccaca7f252af1b037228c9d1` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M04 | `1cc3a0bcf11a9316fbff545a2b3d7200c080f25b7bbe5564204aebcabb2ab979` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M05 | `4c8561b1380447031be56d37002ad45658174913e54046ee44f0b86170cd663c` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M06 | `38d2f5ddc1234e390111c8935943ab756a3ebc6ce5bd31f52f0fa63f9172a3b4` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M07 | `c8d0703254df741c093ec5c893279bc6af1b1542f6c33092fdf35ff6001b6630` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M08 | `3278a1515d66d283c69a93cb9bea3ff4b16a6b83bb01860ba51e6789a688bf3c` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M09 | `8c24fd1780d50c71e42b4f4317e94b318edc35ca446bc68156d7c3303e93a1d5` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M10 | `dfd15f0d1787a6fd376d43d12ea7bd83522202540fcd0b9e47bb0a5c7dd4c70f` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M11 | `1b1f0b36a5d4b3af280a73c4b63e2f4969dd7c602788f500749932a568840619` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| M12 | `0cc13818ddc4a96577433112c95e64cd7e691942cdd2119a61123d3ef254d731` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |

## Full detector command ledger
[Observation] The command, exact UTC interval, exit, and final stdout line for every actual invocation follow. Each full receipt also stores source-byte SHA-256, complete selftest stdout and stderr.

### D-M01-baseline

UTC 2026-10-23T03:15:25.652904Z to 2026-10-23T03:15:26.614773Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M01/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01.py --selftest
```

### D-M01-mutated

UTC 2026-10-23T03:15:26.644207Z to 2026-10-23T03:15:28.169906Z; exit 1; stdout tail `selftest cases=18 failures=1`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M01/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01.py --selftest
```

### D-M01-restored

UTC 2026-10-23T03:15:28.191762Z to 2026-10-23T03:15:29.701127Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M01/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01.py --selftest
```

### D-M02-baseline

UTC 2026-10-23T03:15:25.652827Z to 2026-10-23T03:15:26.616699Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M02/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02.py --selftest
```

### D-M02-mutated

UTC 2026-10-23T03:15:26.648793Z to 2026-10-23T03:15:28.210767Z; exit 1; stdout tail `selftest cases=18 failures=1`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M02/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02.py --selftest
```

### D-M02-restored

UTC 2026-10-23T03:15:28.224295Z to 2026-10-23T03:15:29.406291Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M02/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02.py --selftest
```

### D-M03-baseline

UTC 2026-10-23T03:15:25.652852Z to 2026-10-23T03:15:26.616958Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M03/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03.py --selftest
```

### D-M03-mutated

UTC 2026-10-23T03:15:26.648173Z to 2026-10-23T03:15:28.128375Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M03/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03.py --selftest
```

### D-M03-restored

UTC 2026-10-23T03:15:28.144074Z to 2026-10-23T03:15:29.330031Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M03/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03.py --selftest
```

### D-M04-baseline

UTC 2026-10-23T03:15:25.652976Z to 2026-10-23T03:15:26.619997Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M04/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04.py --selftest
```

### D-M04-mutated

UTC 2026-10-23T03:15:26.651006Z to 2026-10-23T03:15:28.168102Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M04/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04.py --selftest
```

### D-M04-restored

UTC 2026-10-23T03:15:28.189627Z to 2026-10-23T03:15:29.386238Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M04/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04.py --selftest
```

### D-M05-baseline

UTC 2026-10-23T03:15:29.341004Z to 2026-10-23T03:15:30.466758Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M05/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05.py --selftest
```

### D-M05-mutated

UTC 2026-10-23T03:15:30.477045Z to 2026-10-23T03:15:31.640417Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M05/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05.py --selftest
```

### D-M05-restored

UTC 2026-10-23T03:15:31.649976Z to 2026-10-23T03:15:32.704603Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M05/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05.py --selftest
```

### D-M06-baseline

UTC 2026-10-23T03:15:29.398639Z to 2026-10-23T03:15:30.541111Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M06/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06.py --selftest
```

### D-M06-mutated

UTC 2026-10-23T03:15:30.556266Z to 2026-10-23T03:15:31.695516Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M06/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06.py --selftest
```

### D-M06-restored

UTC 2026-10-23T03:15:31.707883Z to 2026-10-23T03:15:32.758769Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M06/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06.py --selftest
```

### D-M07-baseline

UTC 2026-10-23T03:15:29.417442Z to 2026-10-23T03:15:30.548402Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M07/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07.py --selftest
```

### D-M07-mutated

UTC 2026-10-23T03:15:30.562499Z to 2026-10-23T03:15:31.733471Z; exit 1; stdout tail `selftest cases=18 failures=1`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M07/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07.py --selftest
```

### D-M07-restored

UTC 2026-10-23T03:15:31.744477Z to 2026-10-23T03:15:32.805088Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M07/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07.py --selftest
```

### D-M08-baseline

UTC 2026-10-23T03:15:29.714392Z to 2026-10-23T03:15:30.881402Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M08/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08.py --selftest
```

### D-M08-mutated

UTC 2026-10-23T03:15:30.897295Z to 2026-10-23T03:15:31.997173Z; exit 1; stdout tail `selftest cases=18 failures=1`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M08/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08.py --selftest
```

### D-M08-restored

UTC 2026-10-23T03:15:32.007503Z to 2026-10-23T03:15:33.047296Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M08/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08.py --selftest
```

### D-M09-baseline

UTC 2026-10-23T03:15:32.715502Z to 2026-10-23T03:15:34.014675Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M09/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09.py --selftest
```

### D-M09-mutated

UTC 2026-10-23T03:15:34.035342Z to 2026-10-23T03:15:35.395388Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M09/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09.py --selftest
```

### D-M09-restored

UTC 2026-10-23T03:15:35.405817Z to 2026-10-23T03:15:36.567290Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M09/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09.py --selftest
```

### D-M10-baseline

UTC 2026-10-23T03:15:32.770287Z to 2026-10-23T03:15:34.070361Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M10/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10.py --selftest
```

### D-M10-mutated

UTC 2026-10-23T03:15:34.097115Z to 2026-10-23T03:15:35.433725Z; exit 1; stdout tail `selftest cases=18 failures=1`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M10/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10.py --selftest
```

### D-M10-restored

UTC 2026-10-23T03:15:35.444546Z to 2026-10-23T03:15:36.594816Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M10/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10.py --selftest
```

### D-M11-baseline

UTC 2026-10-23T03:15:32.815069Z to 2026-10-23T03:15:34.195381Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M11/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11.py --selftest
```

### D-M11-mutated

UTC 2026-10-23T03:15:34.216606Z to 2026-10-23T03:15:35.499516Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M11/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11.py --selftest
```

### D-M11-restored

UTC 2026-10-23T03:15:35.510172Z to 2026-10-23T03:15:36.639641Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M11/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11.py --selftest
```

### D-M12-baseline

UTC 2026-10-23T03:15:33.057852Z to 2026-10-23T03:15:34.637283Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M12/baseline timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12.py --selftest
```

### D-M12-mutated

UTC 2026-10-23T03:15:34.654758Z to 2026-10-23T03:15:35.816575Z; exit 1; stdout tail `selftest cases=18 failures=15`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M12/mutated timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12.py --selftest
```

### D-M12-restored

UTC 2026-10-23T03:15:35.828761Z to 2026-10-23T03:15:36.944748Z; exit 0; stdout tail `selftest cases=18 failures=0`; stderr empty.

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/tmp/M12/restored timeout --kill-after=5 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12.py --selftest
```

## Opened-source ledger
All sources were local file reads; access date **2026-10-23**. Each quote is at most 25 contiguous words from the opened bytes.

| URL | SHA-256 | Located quote |
|---|---|---|
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/axis-fit-gate.py | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` | Line 261: `if r_add[1] < e_add[1]:` |
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 9: "never pipe an unverified remote script into a shell." |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 12: `**Name the axes.**` |

## Artifact inventory and SHA-256
[Observation] `timeout 10 sha256sum` was run with the following 64 absolute filenames as its arguments, in displayed order. UTC 2026-10-23T03:17:54.005437Z to 2026-10-23T03:17:54.011670Z; exit 0. These are all retained scratch files. The `.py` mutant targets listed here contain restored pristine bytes; the `.mutant.bytes` files are evidence snapshots.

| Absolute artifact path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01-baseline.log` | `ce6fc7e5a2d4a6851dea584679ea79347ad9b88b94c2078faa92e9bcd7ce41f8` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01-mutated.log` | `b13646bacee0d8f744dab09f98ef069fa789f725137a6731e3193bd3c335e5df` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01-restored.log` | `cbbd4e21d12086d54101870649303630f5fbd21aaabbda5ebe0737d11a3855f7` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01.mutant.bytes` | `5e5eb02a0c4a33b56603763c7601802daaf4fd93927bb04e8d169db46ee057c0` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M01.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02-baseline.log` | `1ee0932a6c6be2611b92c4175490d4e80ddb57e4b6b0ab40b4ff8073945188e3` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02-mutated.log` | `ffc8be1803dd15d40638f99646f3b2ee75807eccd094c7938cd0117be636c6d3` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02-restored.log` | `eb500ebaff57c40470f9173fd20b8e13da387736474d81f098a22d5dc78aaf31` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02.mutant.bytes` | `d8a560fc544544df3f908ff2c0753163ee5befd48ff4f624d0210f09a4a84825` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M02.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03-baseline.log` | `a72493c7f16cfe2bba9dbd623fb26500fa0ba556f425dae4e1dc8f9280407798` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03-mutated.log` | `ae6cf251bf0142126587ff292a8d346e48c4e94c0b8523e2de46fb57476ce8d7` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03-restored.log` | `9a54becf6b31ce754e4f5024596b6d44a7e205d0638ef25a477544e9312624c2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03.mutant.bytes` | `0bb7f9b20d77624d5a89bc5c3effe9fb121a6232ccaca7f252af1b037228c9d1` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M03.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04-baseline.log` | `f7c07451bf1a284fcc859e5aca48c8ed6c5dd4b1ae084f07bdab9cd076bede05` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04-mutated.log` | `064f6cbfa7049e0ac2d67c8caeec969f926a3313fa88dc068e6ef0a89bb1d986` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04-restored.log` | `3bc843d6c82ff5174813d2876c247a7fe53252a09b8ac064e543b3bf930ca515` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04.mutant.bytes` | `1cc3a0bcf11a9316fbff545a2b3d7200c080f25b7bbe5564204aebcabb2ab979` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M04.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05-baseline.log` | `b13495b37bec5fdb5c58667d0d40a6b95f76e147de5ceddea7377a58121ed4c5` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05-mutated.log` | `22fe21c2f41f9bd67771d7c18c5de80b912bb8576eab8f5c79e9bbdff3846522` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05-restored.log` | `7ac2f1b6ecbd6df1700b09946fa5a240bd25cbacfe79a08947dc0bc49063c85f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05.mutant.bytes` | `4c8561b1380447031be56d37002ad45658174913e54046ee44f0b86170cd663c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M05.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06-baseline.log` | `fbe78b30732d9f9fce548b77e09513d225d8a7db5241e61d05ecc862f8fd0cd1` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06-mutated.log` | `28e7780e476f2964c4d85fed49046cc359e9e59a7cca53f4ec6caefb45ee20f7` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06-restored.log` | `96f4b61a9581739ebca6984860227da48c951f5a325a6d05c01d6e970b21fb0b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06.mutant.bytes` | `38d2f5ddc1234e390111c8935943ab756a3ebc6ce5bd31f52f0fa63f9172a3b4` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M06.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07-baseline.log` | `6c036012de8bab5bac0ae2cb282f371a65890e5f09e2201cad805376eb94d581` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07-mutated.log` | `6909b3d88f83bb922bddc5719c1ea82c0d7cbc0d6adf1a2dfdf7bc8d8fe48a38` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07-restored.log` | `9dc8c8015253fd5b4a54473225a461f97453203426b295f8a41e7bd880e4aa01` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07.mutant.bytes` | `c8d0703254df741c093ec5c893279bc6af1b1542f6c33092fdf35ff6001b6630` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M07.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08-baseline.log` | `0fd5113e603a0094893aa4c790caf9344542ea92e1910b7218a00ca2964dc12a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08-mutated.log` | `6e53262a62c77887434d06bc19f63d55dce48d20a95859bd2386c3fef9a2ab4a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08-restored.log` | `7c4b1996cd669d30f241be223ca2bec6a4754b1637c63ac14fa9b8425e6eeac9` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08.mutant.bytes` | `3278a1515d66d283c69a93cb9bea3ff4b16a6b83bb01860ba51e6789a688bf3c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M08.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09-baseline.log` | `cf04e75a887ed904db5e81ee44ace9103fcbaf83ccaef12bc49033abb7a9b869` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09-mutated.log` | `50ee1039653a3a1d8555cd56b907f75970c092cb4bf8dc09d5fe52d40ab2de31` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09-restored.log` | `fb77ec6e6c82155884b58b59ead2c5f8446e1fc76aaab3762557178581c591a2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09.mutant.bytes` | `8c24fd1780d50c71e42b4f4317e94b318edc35ca446bc68156d7c3303e93a1d5` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M09.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10-baseline.log` | `074f20d91d1504a8aa53a1af41a269c596e9de63448a4e7c3b71222f9bfa261c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10-mutated.log` | `0590cd5f0e2f1b365a36d53472eddd2a6eb0b586ce116c12ea736342d3583c0d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10-restored.log` | `35857bd5fc045b8168b405450cd8e9d77392f9c5862c31707f178a86f503c8a2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10.mutant.bytes` | `dfd15f0d1787a6fd376d43d12ea7bd83522202540fcd0b9e47bb0a5c7dd4c70f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M10.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11-baseline.log` | `f5428baf4425f0d76209f473fa07dec97748284b4b6f7ba1ffdbf1494c2cd54f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11-mutated.log` | `d9ac29613f48e9a7e034bcedc887e022be2e46f6e6984334208536e99b184426` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11-restored.log` | `7bef5eb44246d60532f0827a63645fe39f3f3872d74ce628420fd1bd9aa79c6e` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11.mutant.bytes` | `1b1f0b36a5d4b3af280a73c4b63e2f4969dd7c602788f500749932a568840619` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M11.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12-baseline.log` | `dbc7bbdc0a536da545689cf42cb4b248b4676f92b24664b8923209beaae03473` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12-mutated.log` | `b0930b715fe340ac69b698c89f17b55edbee45c8f685226a3ed989ac368aa895` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12-restored.log` | `bbd98b929acae20b0bde0d42bf0224f587dd6652a3fcf6f9b70e2e97ba6faa51` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12.mutant.bytes` | `0cc13818ddc4a96577433112c95e64cd7e691942cdd2119a61123d3ef254d731` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/M12.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/classified-results.json` | `7d18dddcf3126207366b2f9872fd1d2f642f6d010cec6308c835a4305fe3bd82` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/pristine.py` | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/results.json` | `a5409cf90cf58095afc6f1843cd17719f7c3f245606668fc171396c6f1002eb2` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w2/MutAxisFitGate/run-probes.py` | `603cef0edbc9031be388b3582d5f20c4dc6efd529b1111a7019b57d9a0124b8e` |

[Unknown] Behavior of the proposed missing-case fixtures was not exercised. No claim beyond this assigned mutation probe is made.
