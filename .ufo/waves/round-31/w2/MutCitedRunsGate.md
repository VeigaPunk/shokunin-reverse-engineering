# MutCitedRunsGate — bounded mutation probe

## Scope and verdict

- **Observation — 16 isolated, single-point mutants tested: 8 killed, 8 survived, 0 inconclusive.** Each mutant copy ran both assigned detectors on pristine, mutated and restored bytes (96 top-level detector runs total).
- **Attack verdict: fails** for the bounded proposition that the embedded selftest plus the historical rejection detects all sixteen plausible regressions. The eight survivors below are missing selftest cases, not a request to alter the gate contract.
- **Observation — historical rejection holds on pristine/restored bytes:** every baseline and restoration returned selftest exit 0 and historical-report exit 1. The selftest has 17 cases. No baseline failure was counted as a kill.
- **Observation — M15 alone changed the historical report exit verdict** (1 to 0). All eight kills were also selftest failures. Changes to finding counts while retaining exit 1 were not counted as historical-verdict kills.
- **Unknown:** the proposed extra cases below were not executed or integrated. No claim is made that this sample exhausts the gate defects or establishes either SQLite claim.
- Axes: isolated one-point defects; sensitivity of the fixed detectors; exact-byte restoration and reproducible evidence. No REA invocation, external fetch, package installation/update, lane Git write, or subagent dispatch was performed.

## Instrument identity and bounded commands

Original source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/cited-runs-gate.py`.
Original/pristine/restored SHA-256: `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83`.
Historical input: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md`.
Historical report SHA-256: `8accd794d27e2218255ef47de0283569e1099a4fab6aec1917ae2af20190d90d`.
Revision argument `c369242f` resolved by the detector to `c369242fee9f559f895e3f7956b1242076c7b1be`.

Every command below ran with working directory `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate`, all inherited `GIT_*` variables removed, and `TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/tmp`. Selftests created and removed their throw-away Git repositories beneath their scratch copy directories, never beneath the lane. Each detector had a 180-second timeout and a five-second termination grace; outer harness invocations were capped at 900 seconds. Four independent scratch copies ran concurrently; each copy was tested serially.

For each row, command `Sxx` is its selftest and command `Rxx` is its historical-report detector. These are the exact same argv in all three phases; full argv, UTC start/end times, stream hashes and exit codes are also retained in the per-run JSON artifacts.

```text
S01: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/cited-runs-gate.py --selftest
R01: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S02: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/cited-runs-gate.py --selftest
R02: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S03: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/cited-runs-gate.py --selftest
R03: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S04: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/cited-runs-gate.py --selftest
R04: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S05: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/cited-runs-gate.py --selftest
R05: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S06: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/cited-runs-gate.py --selftest
R06: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S07: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/cited-runs-gate.py --selftest
R07: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S08: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/cited-runs-gate.py --selftest
R08: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S09: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/cited-runs-gate.py --selftest
R09: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S10: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/cited-runs-gate.py --selftest
R10: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S11: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/cited-runs-gate.py --selftest
R11: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S12: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/cited-runs-gate.py --selftest
R12: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S13: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/cited-runs-gate.py --selftest
R13: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S14: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/cited-runs-gate.py --selftest
R14: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S15: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/cited-runs-gate.py --selftest
R15: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
S16: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/cited-runs-gate.py --selftest
R16: /usr/bin/timeout --signal=TERM --kill-after=5s 180s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/cited-runs-gate.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c369242f
```

## Killed / survived table

All table results are observations. Expected-detector descriptions refer to existing cases when present, or to the inferred missing case detailed below.

| Mutant | Source line; single-point defect | Expected detector | Mutant selftest exit | Mutant R30 exit | Verdict |
|---|---|---|---:|---:|---|
| M01 | 45: Delete the trailing PASS word-boundary assertion. | A nonassertion containing PASSWORD must remain assertion-free; missing case. | 0 | 1 | **survived** |
| M02 | 109: Use PASS_RE.fullmatch(line), not search(line). | Existing uncited-pass / backed-pass cases. | 1 | 1 | **killed** |
| M03 | 48: Remove the optional _code alternative from exit-zero recognition. | Uncited exit_code=0 must fail; missing case. | 0 | 1 | **survived** |
| M04 | 89: Test CLEAN negation against the whole text, not the preceding context. | Existing red-receipt-clean case. | 1 | 1 | **killed** |
| M05 | 47: Remove re.IGNORECASE from CLEAN negation recognition. | Lowercase not CLEAN remains negative; missing case. | 0 | 1 | **survived** |
| M06 | 111: Detect report-side CLEAN without checking negation. | A report stating NOT CLEAN alone is not an assertion; missing case. | 0 | 1 | **survived** |
| M07 | 137: Replace the wave shorthand fallback with the evidence fallback. | Existing shorthand-relative case. | 1 | 1 | **killed** |
| M08 | 138: Replace the evidence shorthand fallback with the wave fallback. | Existing seeded evidence receipt reached by c1/ok.txt; missing case. | 0 | 1 | **survived** |
| M09 | 43: Add tools/ to the allowed citation prefixes. | Existing outside-prefix case. | 1 | 1 | **killed** |
| M10 | 164: Use HEAD, not --rev, for the cat-file type lookup. | Existing path-present-at-base-rev case. | 1 | 1 | **killed** |
| M11 | 165: Remove the requirement that the resolved Git object is a blob. | Citation to a tree must be rejected even if its listing contains PASS; missing case. | 0 | 1 | **survived** |
| M12 | 115: Read only the first counter pair on each report line. | Correct first counter followed by a wrong second counter; missing case. | 0 | 1 | **survived** |
| M13 | 50: Reduce accepted counter width from six digits to five. | An uncited six-digit counter must fail; missing case. | 0 | 1 | **survived** |
| M14 | 119: Remove the lambda default that freezes each counter label. | Existing counter-miscount case. | 1 | 1 | **killed** |
| M15 | 292: Return exit 0 rather than exit 1 when findings exist. | Existing negative cases, plus the historical report verdict. | 1 | 0 | **killed** |
| M16 | 234: Return exit 1 rather than exit 2 on usage errors. | Existing three usage-error cases. | 1 | 1 | **killed** |

## Producing output excerpts and UTC evidence

These excerpts are exact served process output, not reconstructed expected output. A selftest summary is stdout; the historical summary is stderr. Stream files in the artifact inventory preserve complete output. Each command label above uniquely names its producing command.

### M01

- `S01`: UTC 2026-10-23T04:32:01.022670Z → 2026-10-23T04:32:01.627272Z; exit 0.
- `R01`: UTC 2026-10-23T04:32:01.627540Z → 2026-10-23T04:32:01.675667Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M02

- `S02`: UTC 2026-10-23T04:32:01.022548Z → 2026-10-23T04:32:01.611775Z; exit 1.
- `R02`: UTC 2026-10-23T04:32:01.611892Z → 2026-10-23T04:32:01.656128Z; exit 1.

```text
SELFTEST case backed-pass: FAIL (stdout missing /cited-runs-gate: ok assertions=1/)
SELFTEST FAIL cases=17 passed=11
cited-runs-gate: FAIL findings=6 assertions=7 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M03

- `S03`: UTC 2026-10-23T04:32:01.022985Z → 2026-10-23T04:32:01.627102Z; exit 0.
- `R03`: UTC 2026-10-23T04:32:01.627234Z → 2026-10-23T04:32:01.675755Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M04

- `S04`: UTC 2026-10-23T04:32:01.023841Z → 2026-10-23T04:32:01.626664Z; exit 1.
- `R04`: UTC 2026-10-23T04:32:01.626836Z → 2026-10-23T04:32:01.677333Z; exit 1.

```text
SELFTEST case red-receipt-clean: FAIL (exit 0 != 1; stdout missing /^UNBACKED 1: \.ufo/waves/round-30/red\.txt lacks CLEAN$/)
SELFTEST FAIL cases=17 passed=16
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M05

- `S05`: UTC 2026-10-23T04:32:01.656830Z → 2026-10-23T04:32:02.304157Z; exit 0.
- `R05`: UTC 2026-10-23T04:32:02.304264Z → 2026-10-23T04:32:02.353524Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M06

- `S06`: UTC 2026-10-23T04:32:01.677234Z → 2026-10-23T04:32:02.314337Z; exit 0.
- `R06`: UTC 2026-10-23T04:32:02.314395Z → 2026-10-23T04:32:02.362213Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M07

- `S07`: UTC 2026-10-23T04:32:01.677596Z → 2026-10-23T04:32:02.307197Z; exit 1.
- `R07`: UTC 2026-10-23T04:32:02.307256Z → 2026-10-23T04:32:02.348938Z; exit 1.

```text
SELFTEST case shorthand-relative: FAIL (exit 1 != 0; stdout missing /cited-runs-gate: ok assertions=1/)
SELFTEST FAIL cases=17 passed=16
cited-runs-gate: FAIL findings=9 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M08

- `S08`: UTC 2026-10-23T04:32:01.678504Z → 2026-10-23T04:32:02.306363Z; exit 0.
- `R08`: UTC 2026-10-23T04:32:02.306435Z → 2026-10-23T04:32:02.347795Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M09

- `S09`: UTC 2026-10-23T04:32:02.348590Z → 2026-10-23T04:32:02.985763Z; exit 1.
- `R09`: UTC 2026-10-23T04:32:02.985837Z → 2026-10-23T04:32:03.043342Z; exit 1.

```text
SELFTEST case outside-prefix: FAIL (exit 0 != 1; stdout missing /^UNCITED 1:/)
SELFTEST FAIL cases=17 passed=16
cited-runs-gate: FAIL findings=13 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M10

- `S10`: UTC 2026-10-23T04:32:02.349800Z → 2026-10-23T04:32:02.983026Z; exit 1.
- `R10`: UTC 2026-10-23T04:32:02.983116Z → 2026-10-23T04:32:03.035261Z; exit 1.

```text
SELFTEST case path-present-at-base-rev: FAIL (exit 1 != 0; stdout missing /cited-runs-gate: ok assertions=1/)
SELFTEST FAIL cases=17 passed=16
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M11

- `S11`: UTC 2026-10-23T04:32:02.354515Z → 2026-10-23T04:32:02.987749Z; exit 0.
- `R11`: UTC 2026-10-23T04:32:02.987816Z → 2026-10-23T04:32:03.038883Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M12

- `S12`: UTC 2026-10-23T04:32:02.363112Z → 2026-10-23T04:32:02.990145Z; exit 0.
- `R12`: UTC 2026-10-23T04:32:02.990215Z → 2026-10-23T04:32:03.039978Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M13

- `S13`: UTC 2026-10-23T04:32:03.036486Z → 2026-10-23T04:32:03.648084Z; exit 0.
- `R13`: UTC 2026-10-23T04:32:03.648236Z → 2026-10-23T04:32:03.702380Z; exit 1.

```text
SELFTEST ok cases=17 passed=17
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M14

- `S14`: UTC 2026-10-23T04:32:03.039767Z → 2026-10-23T04:32:03.653515Z; exit 1.
- `R14`: UTC 2026-10-23T04:32:03.653577Z → 2026-10-23T04:32:03.703788Z; exit 1.

```text
SELFTEST case counter-miscount: FAIL (exit 0 != 1; stdout missing /^UNBACKED 1: \.ufo/waves/round-30/green\.txt lacks carriers=15$/)
SELFTEST FAIL cases=17 passed=16
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M15

- `S15`: UTC 2026-10-23T04:32:03.040842Z → 2026-10-23T04:32:03.651191Z; exit 1.
- `R15`: UTC 2026-10-23T04:32:03.651327Z → 2026-10-23T04:32:03.703010Z; exit 0.

```text
SELFTEST case uncited-pass: FAIL (exit 0 != 1)
SELFTEST FAIL cases=17 passed=9
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### M16

- `S16`: UTC 2026-10-23T04:32:03.044144Z → 2026-10-23T04:32:03.648581Z; exit 1.
- `R16`: UTC 2026-10-23T04:32:03.648730Z → 2026-10-23T04:32:03.700976Z; exit 1.

```text
SELFTEST case usage-no-args: FAIL (exit 1 != 2)
SELFTEST FAIL cases=17 passed=14
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

## Pristine and restored detector evidence

| Phase | UTC start | UTC end | Copies | Selftest exit | R30 exit |
|---|---|---|---:|---:|---:|
| baseline | 2026-10-23T04:31:13.140527Z | 2026-10-23T04:31:16.134379Z | 16 | 0 | 1 |
| restored | 2026-10-23T04:32:07.224243Z | 2026-10-23T04:32:09.964491Z | 16 | 0 | 1 |

Baseline example `S01` at 2026-10-23T04:31:13.140527Z–04:31:14.020959Z, exit 0:

```text
SELFTEST case backed-pass: PASS (exit 0)
SELFTEST case uncited-pass: PASS (exit 1)
SELFTEST case path-absent-at-rev: PASS (exit 1)
SELFTEST case path-present-at-base-rev: PASS (exit 0)
SELFTEST case token-absent: PASS (exit 1)
SELFTEST case red-receipt-clean: PASS (exit 1)
SELFTEST case counter-backed: PASS (exit 0)
SELFTEST case counter-miscount: PASS (exit 1)
SELFTEST case exit0-equals-form: PASS (exit 0)
SELFTEST case exit0-red: PASS (exit 1)
SELFTEST case shorthand-relative: PASS (exit 0)
SELFTEST case outside-prefix: PASS (exit 1)
SELFTEST case mixed-lines: PASS (exit 1)
SELFTEST case no-assertion: PASS (exit 0)
SELFTEST case usage-no-args: PASS (exit 2)
SELFTEST case usage-bad-rev: PASS (exit 2)
SELFTEST case usage-missing-report: PASS (exit 2)
SELFTEST ok cases=17 passed=17
SELFTEST repo=/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/cited-runs-gate-selftest-0ie8y8ib (removed)
```

Baseline example `R01` at 2026-10-23T04:31:14.021056Z–04:31:14.070852Z, exit 1; full stdout:

```text
UNBACKED 16: .ufo/waves/round-30/settle.tsv lacks PASS
UNCITED 59: | R30-C2 | `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <REV>` | exit 2 (predictions absent)...
UNCITED 64: - `axis-fit-gate` exit 0.
UNCITED 65: - `prefreeze-gate` CLEAN.
UNCITED 66: - `settle-gate` PASS.
UNCITED 67: - `tools/round-29/prefile-check.sh`: `prefile: tree clean`, both freeze ledgers exit 0, `prefile: PASS`, exit 0 (reru...
UNCITED 82: - Round start: `kaidoku ok`, six W04 warnings, exit 0.
UNCITED 83: - Round end: `kaidoku ok`, exit 0, with the W04 warnings unchanged plus a new one: S090 and S083 share the same tarba...
```

Full stderr:

```text
note: line 16 asserts 'PASS'; cited .ufo/waves/round-30/settle.tsv lack(s) it at c369242f
note: line 59 cites no path that is a blob at c369242f; tried .ufo/waves/round-30/tools/round-30/c2-rust-refusals.py, corpus/evidence/round-30/tools/round-30/c2-rust-refusals.py, .ufo/waves/round-30/verb/entry, corpus/evidence/round-30/verb/entry
note: line 67 cites no path that is a blob at c369242f; tried .ufo/waves/round-30/tools/round-29/prefile-check.sh, corpus/evidence/round-30/tools/round-29/prefile-check.sh
cited-runs-gate: FAIL findings=8 assertions=9 report=/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md rev=c369242fee9f559f895e3f7956b1242076c7b1be
```

### Per-copy restoration observations

The table records SHA-256 before mutation (common hash above), while mutated, and after exact restoration. The restoration detector rerun used the same command labels, not a different oracle. Every active copy was unchanged during its detector runs and restored byte-for-byte to the pristine snapshot. Mutant bytes remain only as non-executable `.txt` evidence snapshots with matching SHA-256, plus one-line diffs; the active `.py` copies are pristine.

| Copy | Mutated SHA-256 | Restored SHA-256 | Restored selftest / R30 exits | Exact restoration |
|---|---|---|---|---|
| M01 | `a5c1544ea78d2b578aadf37a4efb4f2b9fc9d12947c20ba5d573675aad40c852` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M02 | `687801b4abe15b8f817727bf5bbf9dc8491da9dc89dfb58fadcd1c5e1c5b3f7e` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M03 | `0e647c12f4ee0ef95d24ac0e7436d63d65696c47e0123cfd7f7ccb9c2d15848b` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M04 | `bd0e1c4cb729e684feb68f46dc9fd1356715104c89a707439366dcdd9b62c2c6` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M05 | `19674f571baf0790a1ad1254ce5b7a1b34fe689719568b4606e5757ed068d6b8` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M06 | `7556fa08f1276c6ff37f302eaa444d734983f832197c1b097618875b0082591b` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M07 | `7f3d61e5bea778c2ed393297b305d798aec53971ea1f6730c03149e4054ae623` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M08 | `e117f65769d393a97de1a631d3a18852afe4f2a2242aae43190e5206891ce508` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M09 | `07733687b26bbd7698dc4e51fcd3ebf79cb2bd93920a8052c4ffd85deebe2469` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M10 | `4d03f2a24a056095e8063cae7e32fcd2a02a7cae239b4da6980ca002b0395de5` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M11 | `80f4d5ec486888ce6c2b82b5e436e7e860e802ed3f0ea49cd61c43bdfa5210ad` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M12 | `459c3b5a4f88d308aa442dc2cb5569419f6d51bf8816bd2bc002bf3ec7524aec` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M13 | `4b67d9a9d1b5e6a74d1336a23f5a4de369dd9e0a47fb409813695066a3be101c` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M14 | `66d3e420f5ce9138b7b79b203a0358923f339c51c37f972ec0fc94f27fdff8e3` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M15 | `9f289711d6b763aafc93873d5a8f052e9d098f17b1bac822c046a4758d115087` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |
| M16 | `140c62d544a61eec5180a465c4c9e65de2f83fe65dd13af28493c979758a90a2` | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | 0 / 1 | True |

All 96 detector subprocesses completed and were reaped by the harness; no timeout occurred and no persistent service was started. The selftest receipts report their temporary repositories removed. The production lane source and historical report were read-only inputs throughout.

## Survivors as missing selftest cases

**Inference, not additional executed evidence:** these cases distinguish the intended pristine behavior from the observed surviving mutants. No production fix, contract change, or test-suite edit was made.

- **M01:** Add an uncited report line `- PASSWORD.` (or `- PASSAGE.`), expecting exit 0 and `assertions=0`. The mutant wrongly recognizes a PASS prefix. Also cover the equivalent receipt-side false backing.
- **M03:** Add an uncited line `- gate exit_code=0.`, expecting exit 1 and `UNCITED 1:`. The current COUNTER_RE loop excludes exit_code, so losing the EXIT0_RE alternative otherwise silently removes this assertion.
- **M05:** Add a report `- gate not CLEAN.`, expecting exit 0 and `assertions=0`; additionally use a committed receipt containing `prefile: tree not CLEAN` against a positive CLEAN claim, expecting UNBACKED. This covers the case-insensitive behavior present in the pristine implementation.
- **M06:** Add the uncited report `- prefile: tree NOT CLEAN (3 paths)`, expecting exit 0 and `assertions=0`. The existing negative-CLEAN test covers a receipt, not a negative report line.
- **M08:** Use the already seeded receipt under the evidence root: report `- requests=23 matches=23 target=23 entry_ok=1 skill_ok=1 (c1/ok.txt)`, expecting exit 0 and `assertions=1`. The existing shorthand case exercises only the wave root.
- **M11:** Seed a child named PASS inside an evidence-directory tree, then cite the tree itself in a PASS assertion. Expect exit 1 and `UNCITED 1:` because a Git tree is not a blob. Without the type guard, git show can expose a matching filename and falsely back the claim.
- **M12:** Add `- carriers=16 pass=15 target=16` citing the existing green receipt, expecting exit 1 and `UNBACKED ... lacks pass=15`. The existing miscount changes only the first pair, which does not expose truncation of later pairs.
- **M13:** Add an uncited `- carriers=100000`, expecting exit 1 and `UNCITED 1:`. Cover the existing six-digit acceptance boundary rather than asserting a new numeric domain.

The strongest direct missing checks are report-side NOT CLEAN (M06), the non-first counter on a line (M12), the second citation root fallback (M08), and Git tree-versus-blob identity (M11). Survival says the supplied detectors lack coverage; it does not establish that those defects exist in the unmutated gate.

## Opened-source provenance

Access date for each local primary/context source: **2026-10-23**. All were opened by ordinary local file reads; no remote source was fetched. Each quote is at most 25 contiguous words from the named file and line.

| URL | SHA-256 of file bytes | Located quote |
|---|---|---|
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/cited-runs-gate.py | `f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83` | Line 16: “Every assertion line must cite at least one lane path” |
| file:///home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kaidoku.md | `8accd794d27e2218255ef47de0283569e1099a4fab6aec1917ae2af20190d90d` | Line 63: “Gates at the tip:” |
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | Line 14: “Record every install or update” |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | Line 12: “Name the axes.” |
| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | Line 11: “Use REA when a claim depends on a shipped binary or package, decompilation,” |

## Artifact inventory

All scratch scripts, snapshots, diffs, raw outputs, command/phase records and inventories are listed below by absolute path and SHA-256. The two manifest files list the remaining 392 artifacts and intentionally omit their own hashes; their hashes appear here. This report is the only write inside the lane.

```text
SHA256  ABSOLUTE_PATH
248b8c4874c5f0fd4c5c3c014221dcdc013f435b241b95ecedc06bf2300606c1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/round30.stdout
9298bf68a31807194fd6edeb00465e9d424b06dd9d191e31f71aa697caf0218a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/selftest.stderr
036622aa5a9fbfdc9643feed6cd335e576045f5b955d539803d42641e4e8fe4b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/selftest.stdout
103cd4c8936b9d83b4f3d889305713aac49a95b1b9abf805cc20f16c636176ca  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/cited-runs-gate.py
a5c1544ea78d2b578aadf37a4efb4f2b9fc9d12947c20ba5d573675aad40c852  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/mutant-source.py.txt
57ebd94e34084f0b2435650f3e3096ffd7206c2d368346232835448031e35c77  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/mutation.diff
c74bf955e7dd705dc56a1a315f748e6a5ac980a471fed07253f7b9aff6de24d5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/round30.stdout
ca1024f7abc1ef3f0490799e70265ad1c0edcef5d818d174cb0a3045722641d0  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/selftest.stderr
97d307f792655bbe8934a377843262ba3a068aa9c793bcdb11c49bfeef5e58b8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/selftest.stdout
cb51283af53888527d059c5c8b431c4c3a2c4db86302919ea063c6dc997e501a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/mutated/state.json
541cfe39cff8995f76db8e7a9fd99f03dc52e8151f8e21c37ed88ba299ef525b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/round30.stdout
c4b0bea0a86a148b3672457c483155febfe53f61292fc3193fd39afea9cb6c97  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/selftest.stderr
1f1d28147eb63f2a25681609c2ecf1329dbe03e606d83e8e13740e3f6e8a18fa  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/selftest.stdout
da6f56bebcfb46f0a8dde4347acf3d87cac60d8a88ff7182118f8d00294fb1d7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M01/restored/state.json
6735d5251b11f913eddd013f4b686f013092cda0b9f8472beab5121ac9f01b74  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/round30.stdout
6b088913389a39ab45eb1bfcde9aa0f339f316a8492db05e11a74d2db536c0f5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/selftest.stderr
cfc39cea10b76eedfa4b1b8c3d0fce7c271535842b1c08580751d8bfb9c6262e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/selftest.stdout
a8e75eb3ac751c7a6e6144f9a036089f57d7f18ef2ddbf61d47ed5464d01d31d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/cited-runs-gate.py
687801b4abe15b8f817727bf5bbf9dc8491da9dc89dfb58fadcd1c5e1c5b3f7e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/mutant-source.py.txt
df4ac4d08d558323f6e48948c1892143c7a7948acc3c376f2a9c987a1e695b48  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/mutation.diff
c350660bef1eb39f4ee5755f916e23422663e489be81bd0813db9c1bede76701  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/round30.json
682f6acb7b6aa946405f697d131b472ccb566003ce20298704941eb0748a8aa8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/round30.stderr
11126aa9e50394bb5a997311388d712cf1af779cddf722fe57944f56bc1cf74e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/round30.stdout
77b0d2d48cb80a009e0ba9165e364a08ed79ccfaf90fe8af6d2091a906e955de  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/selftest.stderr
f517f51a63fb23a81b035755db55284b7ba738186de0b4457beadb3c15bc7f1a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/selftest.stdout
a781f5f389b331624b0742d90bfeab848087e11f31b47ff9186b94be6824f4f1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/mutated/state.json
538126ab00dd2528281c50e3f365cae1b4e133ec2da86dc0c3007f165efac80b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/round30.stdout
dec3d6674e681bc5f7f70a29b7818221d701b1d66c0a3445b15af2320af4ef03  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/selftest.stderr
dd98a6474aab9fb988a0e9f4f6c025120d05322a67725b26bc92462661467f68  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/selftest.stdout
9acb42c4b69094f511f2bcd0126e28e4144ab7a3fceb4c5b188e845b06ace3ad  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M02/restored/state.json
7de60b1299863a7bc527e20cba1aa3882910a80e9b0a870bacc3db1a06a8d4d2  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/round30.stdout
1e344e6eb366985c9c3c589878997bf0247de945c9070face8b9eb920c52287c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/selftest.stderr
e7949a62c67d5fe060c5df38dad8840ee0d1051592262a9a64cd4f56105e4de6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/selftest.stdout
0c533d5a5bc92a17cbdb4ccc82d807ef300140831401897e3eb11f7d09178ff1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/cited-runs-gate.py
0e647c12f4ee0ef95d24ac0e7436d63d65696c47e0123cfd7f7ccb9c2d15848b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/mutant-source.py.txt
54e110c477607e31345f61c46803718a37b50b4459720ccaf8235928a9bf82a8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/mutation.diff
9f265265eff832398436199879ae33c2ff4ef60cf2f498deb679c5831e6a932b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/round30.stdout
e0adfae1385854e7d5c601d9da48c8e1d4424ca47dae0b180426e8873bf6b2ac  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/selftest.stderr
217c126d7e4d1e0a1d3e3d800ec6892ed5a8a663a9e230f98045d22dde49b7d8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/selftest.stdout
223e051f20b443f64ae3aacc4f18986118720d9503b22e790993a2b0ffda737d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/mutated/state.json
f336d9cfee94a400f18ca3a0792fb0bd3f076c919e8fa6754ceadc2ec4da2509  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/round30.stdout
b5f89a0ba5bfdca891c79a51846d83a7b9d1a4c720ee07ce3cd340d41bdaa6b6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/selftest.stderr
255c77394a2a7a644f47b1c2a7a6e83748cbaed2a414834bc1bfaf998e3d2732  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/selftest.stdout
437d85b3691b346f48191a7528d50a75e5ea970dd140ff4b9d783eeaddbf3d6a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M03/restored/state.json
e3328f6db55abda5b863d5d6df02c10ee012e32032ebe84e3d07df03eaa583be  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/round30.stdout
ddcbe2c67c8df53056b1996236aae98390a9802a0bf45e7d67871384c430398e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/selftest.stderr
7ea6b358fd76fe830544a9d0ad32c16359366a0354fd3b196a0a59ff5eb1b54d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/selftest.stdout
d80ff9128de5091c7bbc93f7859d5a629240d421c89cbedba79cfe7d061f66f9  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/cited-runs-gate.py
bd0e1c4cb729e684feb68f46dc9fd1356715104c89a707439366dcdd9b62c2c6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/mutant-source.py.txt
fc0bfa340ac539cef7e991f4d7d969c828bdda601821b8ff97110a9f8e1b55a7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/mutation.diff
229676c162b6d51e30534c1b00322b0a7681ee7e0705e88881f239aa8133130d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/round30.stdout
23913a3587225b9543e9b61e2aef47f43a8bee7ce6bf306bbb13c0b0c23902a7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/selftest.stderr
9f1873f57c99e816bbbcd1953dabcfdc7c92068758a78b265e45e5153a2403e3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/selftest.stdout
cecf2aa3bffb54f0913d78a34a05ccc727e5a738f3196c96d6013416d9178f2f  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/mutated/state.json
ca42faec6fbd9d59ab43fae3c5097fa1b8f07adc580a11f67f0202e4587f4100  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/round30.stdout
00091f15ade3d5f914b427eefd214380ebd9f1ea5ec32a3c424de3ada55938fe  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/selftest.stderr
8a71e4085090bc47d9761f2ad49aee35217c6eb85fc91e79920d66c1d6133369  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/selftest.stdout
e645c5c158d526f141955c557cbc62d4801c0baca1d73ca73037f6e463c455a0  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M04/restored/state.json
1e08b341f5a7b664f8183aeb775f8736b4e1b1f3e267d4a0aca5e4ac7c4355d7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/round30.stdout
65e7add72f81dc7bcb2612f40769e09e54e41c4e9ed25b6268610454cb0c7f6c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/selftest.stderr
9ba83f7f97f27d49e8e394608f562b0979e57357141584eb7e85391e26ad5b6a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/selftest.stdout
35cd20264357ac074b5a13b1f570e361f0e73c41dddfac736dc039d630eda511  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/cited-runs-gate.py
19674f571baf0790a1ad1254ce5b7a1b34fe689719568b4606e5757ed068d6b8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/mutant-source.py.txt
bd2c3aceaea59eebcce3d7f7e4638f97a456ad7f0cd0d578e2e256b01e82f2d1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/mutation.diff
47373146f32b354fb3876a737469fd883e7cd98250ffda66e0a8c6c10a5000d4  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/round30.stdout
90be7901abe3785166e204efe73466a1332986be2ec3a01a286dfc448d6315c5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/selftest.stderr
fa68ae664fc6bd02800934762ae755fe3694977ecd66b4320e9d8dc81f77be89  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/selftest.stdout
ef309ab51c6d6f28714921889ad4f44d49c7a5731319c131bfc1637cd571015a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/mutated/state.json
69a607ab552914bc0cfc09f995ea96615e8161ed8b513e7472008104ee34fe23  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/round30.stdout
ee0e71d56ecf079bd91c81a80c689873cdb6249d439d6378cceb5edede32cae8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/selftest.stderr
507115dadd1ffe63e1bdd26f7ad9032cd2b29bfb7b0560e4f7f7826676d1e5ab  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/selftest.stdout
1d717d5293a1f2712a691279579c6ca84f431c09efa514217357ca9db61784f7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M05/restored/state.json
030eed5d8c9039ff090113185de9ec24d27ca5a32f471995b0a9a2dc530f20d3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/round30.stdout
532e5afda56332ba7939825b6817587e436bcc5fa63710e9f945bee5f4af157a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/selftest.stderr
8d0d13dbc991274b997fa004a5c89e591ffd57ad108b4b0517e8205b2938b276  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/selftest.stdout
a27d2a006a8515b601e3939048e24225b15b529c6e4851c43795a24632183ebb  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/cited-runs-gate.py
7556fa08f1276c6ff37f302eaa444d734983f832197c1b097618875b0082591b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/mutant-source.py.txt
2ba22def2d236d3313f21dd02f2b156b7caf0500db413aaedc011c34a47ccdc7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/mutation.diff
4781abe794a4d12525afe149217ff7ad17f2a6b3697ebacb1ab37ce879d077b1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/round30.stdout
1e0cbcbc57299a405160aaba680c83ad982f80d27ba7fc2dacb389ac6230649e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/selftest.stderr
5f6011fc2bfa2117f0c6c49c6e4730c88a33862a0e2456827a03fb2223778504  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/selftest.stdout
4d7322d081ff0a3f0a47dda15f2d887e0161251197666606cde521ac9bfb53cc  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/mutated/state.json
742d521bcdf62650bd62060c319766713f90119d2956b085e7a9c7731ff981b6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/round30.stdout
64190d04892f3c96be1a40ddc479141e28ae0a2e197d4704a31137f9120fa64b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/selftest.stderr
11728ce1d1bb2477c9867bcf411dad319175bcbd2ff5287f3579f522f9d23b8e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/selftest.stdout
3a904c612694f8cf74a04e6935d070d73617bee8119c57a40047bcce41644e51  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M06/restored/state.json
1308fc7146eb6dc644dff387ad2663e1ff2e6a1a22cdd810f80b27e9c1402b21  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/round30.stdout
23d3ce05e8d5b3f1643da3aa785ec5f53302d93682b25bbe62ca8e4c0e37bc35  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/selftest.stderr
1443bdf151e4054da176621c75292efed960e8bd91dc3bdf425101469e7d8b62  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/selftest.stdout
67ab1eb03d97407ce64c5f1b4c486ffb8186a309b108270a1e097b2d9b165e87  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/cited-runs-gate.py
7f3d61e5bea778c2ed393297b305d798aec53971ea1f6730c03149e4054ae623  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/mutant-source.py.txt
154d22878a27866613a61c16e4c0eb9f8951e3dca52369de6bf87b1dae7d7c32  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/mutation.diff
529c81df643702ada233b9f64b2836d56597562167268f906e530c8368071f27  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/round30.json
ac270df8148d898bc6dad0da48784370e5b634875e00a5946a8773152a8227f7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/round30.stderr
935620619183282f6da62087b899a350d78de7affcda00714dcb8ce45d2ca1a8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/round30.stdout
ebc80e4d536a7c73b73d5bf316fd1c9c91904d2bd25edcf954818ad7d1e018b3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/selftest.stderr
066ae4850d8441438d763fffca5b26533decb97eae73a8956762dbf6bfe32a2c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/selftest.stdout
6f8877849abeed359f427fd708805c97fd991f6b6a484c0b6ecfb7bdd3d562d8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/mutated/state.json
40b47f5485533dc6baa8748bbf5179f17807251bbfeab652eca5b57e7bf0a098  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/round30.stdout
fe9776760540bf14da262a01d132c36e18a7a07c980b8adb90170eec230abd80  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/selftest.stderr
cfe281c3f6ba891f5319aca6e2f52d4bcd8e13cbd605a5dca9a13eddca124adf  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/selftest.stdout
46c0be753bec87893970eefb4287630cdd20cc48a2685bffcdea6760834cf14b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M07/restored/state.json
c1c2262f24c626e70232f55ab30dd8dd4f945516ad9dba646e54c899028bcece  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/round30.stdout
c74bb3c533d8faaa16f4be29009395bbb3b63e48fa9bc94efc3fb36a2320c754  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/selftest.stderr
bbcd4ba22bbcc16b86b2ebdc2f357a9976653c067abc2e0d4959676277b61a2c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/selftest.stdout
cfe440174c67755c7cbacb808b823031ce553b56453dab486bfeef7640b51285  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/cited-runs-gate.py
e117f65769d393a97de1a631d3a18852afe4f2a2242aae43190e5206891ce508  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/mutant-source.py.txt
868720cc2c839eb2e595e6032e499d797720f78da48f23b4b77a84026ba8d0b3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/mutation.diff
135d8c52f9f024a07e28d972637735736e4dad64ae92be4eb57ec67baf038331  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/round30.json
557ea92592eb0bcf02ebfd2d90693c7c7e75e75940a63df4eb68d1920cc33f7d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/round30.stdout
7eb2b14934bccdcdfcb0805767bd16219ac83f42d2ec4794af8541453fb9a120  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/selftest.stderr
b0c2d130c28c521f06e6f38be3bb187da6404463774d08fc347d05cd1dfa3870  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/selftest.stdout
953cb6b6de8249da522a410995343a8c49c135a9af810055bb24ba700217a12f  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/mutated/state.json
532afbbef1c623ef9f3c99aae39ddb23eb9b84970ff473602c078d7b317939f1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/round30.stdout
e7928a6d521149df069f401beb413d30c9234eca0452f2af90d9b2b6b42b412d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/selftest.stderr
31f1889136f7756af3eb145f199feec4d31fd29bf47c737eaba2f724431ba085  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/selftest.stdout
8d68e8471b81fcdb3aa62603a4d8d80fc65a8bc7854f1308520c6d763c63bf24  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M08/restored/state.json
59737e148cec042290fb10ed184f05dfc1d7ac012cb2f37823f7b2d52b57d53a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/round30.stdout
f9f6bc689ec81c87bbfb64526e8c67c35d8c75a30ba16629265d3331eed9cb5b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/selftest.stderr
e6417f1dae57c20d113a031186a375524efcf7ce8186bb08c254ef07d5738115  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/selftest.stdout
6d8bcc4d7e7bbf3b90e33bfe7e6b0d0e8aad8f83d55b236165f1dc3cea47db4c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/cited-runs-gate.py
07733687b26bbd7698dc4e51fcd3ebf79cb2bd93920a8052c4ffd85deebe2469  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/mutant-source.py.txt
f20486343a291407c26ef311f233da87adcfa3285b2b25e09cea8abc4eba55cd  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/mutation.diff
ec50e986d66b56dac3bebd3bf0b5d696dc4b2941303e600846d5eb1d590d6cc1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/round30.json
bac8d197183d39bde2b1cc36e95d6869bf8c006d357208ae0aa277c0e5887170  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/round30.stderr
f6b7ce92309fa0cb9fa264a04429bf926f552781671a7a84dc133a3237cbb4de  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/round30.stdout
77f03bf7e2675e1c3582743a6e6de4a183397deaec75db0b7bf52e27aa3c447a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/selftest.stderr
6725f858182df521141f93563d29f7d732ed40428e7ceb913eca687337751265  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/selftest.stdout
c2e44b2ba0edcc4fbe3d99a1c4076021ef28cdb6592b3cf83c47b7bb8a2d5e82  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/mutated/state.json
b5e20b70a674991dbabb4ebde52a1e995d56b265eb475a2511d2bb8cf9b6627c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/round30.stdout
2afb3010bb452e87033fbf51a93111a9596f54a4bd18b1983a211e52f38b5c4f  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/selftest.stderr
aa899ab9d2b60e4d2c879b62210f9a99ddffa756621f4e8bff203b7bf80bd278  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/selftest.stdout
93f6584b2d9f1adbdde8f7378047e25e6070472fa36d4e6dc0510589bf172646  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M09/restored/state.json
b03077801f657ae99b3d17a72d782a78fc0533eb66cfe9bee997c502d510bccd  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/round30.stdout
effc9449190d81d0867058554c2340f3e77452c5f2ee791015a63d954da22766  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/selftest.stderr
a82f13cd54d35e27a3e6e1e3f1f26552f1ad3927261168e788622d824dfcc2a6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/selftest.stdout
dcdcccf436792c98e63efe776e9d2ef2e7594b40f03c97760dab11a4baf11a12  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/cited-runs-gate.py
4d03f2a24a056095e8063cae7e32fcd2a02a7cae239b4da6980ca002b0395de5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/mutant-source.py.txt
4ca504494a48585cfef7719d32ed0177598e7ccf7612e10ec0e587103bce79a3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/mutation.diff
f942cbf307be62aa799a4cfd23ee369e04d46cfdebad47bd1889cf32bf06dc0d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/round30.stdout
538a982943f470f06bbd98a576522349c852eb39b5d1c85e46d6f65b8a2ccb9d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/selftest.stderr
485ae75943d775a15fa4187ae320d7cb2465d0a14ce2dd44e5389fc571bd3945  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/selftest.stdout
211a8a6d7dab36ecb838a666a37da43b690855ef14f2aff2668373c5a46a77cc  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/mutated/state.json
2622e4d62d88c4dd880ee76d31e6a23c2a39cca8ffdb6a9bdc905fe41d4e59f1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/round30.stdout
0463e47302ad706612acfcc72ad6787f0de0a5be3c9bc24e7c307e05683a5bc1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/selftest.stderr
5fec1f5cc7b51e9818ca789cb64224340f388fe330517006162d9656f04db7c0  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/selftest.stdout
341fb6fe1e51788a5d988f26999a930a27c74e8a83a8bfdd67cd5e1a15d99655  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M10/restored/state.json
45c560bf2b9c29ac466b17745fda1bb110df0a9d069da8a08388f616111fb9db  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/round30.stdout
e3e0e83d4a9f1583c6bdd11546617e97dc487089175197721fcda2c683fa9524  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/selftest.stderr
160286451fcca0ea0d2be9f97397135d62f8d2b6a2b97896e0c1854230fd2aab  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/selftest.stdout
031a7cd393196cbbb26579130836e64b03cf6645bb447412be646a5c9db1e8e6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/cited-runs-gate.py
80f4d5ec486888ce6c2b82b5e436e7e860e802ed3f0ea49cd61c43bdfa5210ad  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/mutant-source.py.txt
041674749161ca941c8c65875206dd5beffd3c541c589d3f2e4096839a60947e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/mutation.diff
18854385d731bf4bc3cc0ec5a8260106a2a447c74a0e00688172814d5066f005  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/round30.stdout
edd5feb74cbee0ae1a2ebceb360c4696cfbd3d1f60ef5735a4daa41e8d3de334  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/selftest.stderr
a14e7a853bd5589df23276fa2a96809278bb33992dab863b57112bf322be0ed9  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/selftest.stdout
bfe40d4e2373fb364cf7b263d5e8fe28db5899ab6e5ceef5615d374bd9f78adf  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/mutated/state.json
e63ae01e73ed56030ff5d509006f2a87ed4ea1adac41120dd39c793016457f0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/round30.stdout
9370ab9de3032fde75e755790057fdb73b524f40bb463f4f52ffdc51ed24842d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/selftest.stderr
b29f2247b0f5df4cd8271a94880236b295a7953c5b2cbd328002f0ad475c8dc4  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/selftest.stdout
8947148316fa229d061de6884ce2a179871749dfeefd9a157d13adfa872f1205  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M11/restored/state.json
4ed6a92fcb9096ee831a0729f7c687df00db02e5279a2862ad6f7ee1f8de4788  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/round30.stdout
3ee7ff34325d93671ad345ca13343fb2de256db7359f441e8eb441bb28760612  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/selftest.stderr
f6aab46f165a0f0ab13bf8bf11fc2c69855f8711e3c0c5762f705cca2dda6e12  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/selftest.stdout
e45d833dfd75bf0eb03e075eb4e05fca8b82e98e66bb75acca9f05e53cd659a6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/cited-runs-gate.py
459c3b5a4f88d308aa442dc2cb5569419f6d51bf8816bd2bc002bf3ec7524aec  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/mutant-source.py.txt
7166845bca42e8049a7027b40560be1d73d47f380d82d5f52c9eb54fb2e9df31  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/mutation.diff
7ba83b86e31f6bc4cd4d202fa627d42285e4dae21c503e5718a827c3b8d0db96  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/round30.stdout
48265d5fbca37aea4799aecbd09e5cf884717069675e019aaea880248e96cca6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/selftest.stderr
ff102ac6b3bb0043bc98f030c21c26a175db79256bbbe71a5a3a6059c1d628b5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/selftest.stdout
d84df15602264df385586d4ab53228b561d4cac0db4cc8d4c109306e3f53edb7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/mutated/state.json
c98cd6be3b9f050015dc2e1ef241f454b6f49b10cfb177d953416d7210ddab99  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/round30.stdout
e3c1506ee3f7a69f0ed981b7cc6d00769b680a2365146a08f93328f8aa6addbf  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/selftest.stderr
5d21f8205cab807ed3c43f712e6f130e9953fd384d77b25d747030415377cef5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/selftest.stdout
a5766907ecf514cc335409b44fbe94015af1b1f0e62727ff5880c0530879f119  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M12/restored/state.json
a4a34547f443fcc9fe5c42402a125a3be75a74d14b99d0fa8d7298c50c51f3ae  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/round30.stdout
7ab338adab3f6fd5e1c840e19001c4a0bfffc369c9a811cbf22aa9cc629b18f8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/selftest.stderr
875b833c7bda89cd1cdde9f73509a8286bb9a2e248a76974a6886b0e296f6b78  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/selftest.stdout
e24426c9c15f33bfb11b98d0133eda5db7ce374e342bd05961e9ec9b6b5a7978  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/cited-runs-gate.py
4b67d9a9d1b5e6a74d1336a23f5a4de369dd9e0a47fb409813695066a3be101c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/mutant-source.py.txt
eb445473466356dac314942594cf19c5cab80d28b90442073fb3cdbc216d46c6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/mutation.diff
0e8f8d5b7fcf335a33fc78bdb8257d61f713c4216b54633e75ad0fe6539f4767  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/round30.stdout
7b70fb960ad6ff408cdb28b171a81dbc2da2e75121ee88168050475bfdd20246  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/selftest.stderr
6ba568c2e16cabfaeac323f9752f070e10518cca4cb068c7041fdcdca3554894  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/selftest.stdout
da7584b7e3aa4aff51ce5318e6d35b248d4b49cf6824406aeb121872e32bb350  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/mutated/state.json
4ed6a5bbe1cbfd038579d3801b89865c07894989e1210a422d522d9dd0595d96  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/round30.stdout
6cee272318d022acbeafe8841b043d531d42677443a9468357573963117afa4e  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/selftest.stderr
4ab82aab909fc904ad221d45d32e3c1714575c06fe89f25ff55b8b90240bc017  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/selftest.stdout
15b61706bb083101ad80cbf205343be55b123afa3647f30b00db44aa45ec5d03  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M13/restored/state.json
95ff9d520a8c203710106e52efc0ecf6d442769046d4ebb6bf4c28ee19badee4  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/round30.stdout
7e90657fe3832f4532b9d1f859fbd965ed2be1ea410e756d3803f3c8143fc522  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/selftest.stderr
dd13acf35c4b0033f3bc63d179beda1459156b39ceefedb6cd29dc0b565d5cfb  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/selftest.stdout
373f7ffac3fc3063b375a33626f84823d3fc9632263a6f9496d9c2a00d2037c7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/cited-runs-gate.py
66d3e420f5ce9138b7b79b203a0358923f339c51c37f972ec0fc94f27fdff8e3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/mutant-source.py.txt
55f911a7be48321d695fcf5f63553557dca8d6be07bf59ffc9fd5d7903b35672  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/mutation.diff
1f56b9568ff449c4b93bd70deb3f5fa283f4b18b06aca985b986ae582130435a  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/round30.stdout
c805c3cac7a895ae4628eb05c4d22769a07ecd153701a612626016ec2c64fe70  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/selftest.stderr
236b8db8f72def5dd58ee63a3bc8f21865af3f8ef2aede9507c78d267bdcd178  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/selftest.stdout
d46ea7bf70f22fc75059f57c0ac25cc90d569b97b2f1777d0f8bc5a5c9934e06  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/mutated/state.json
303632ca64d4c58be903045680f0ffb6d2af57f12acd8b27d91979e7d6649cbd  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/round30.stdout
a3e45962f0b169de0fafbffc3aad41f64a86cb95190318d81e5f2aa0d0384421  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/selftest.stderr
5dc824d6f80a2ad5ccbc5cd32bed70f319665be736c36c04ec3b251677ef96f5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/selftest.stdout
bc8ead4736df16f0c0745642a2c7c26e0079e7a66189dc1710818374d1485136  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M14/restored/state.json
6ccf9247c692c162ebace6860e1ca6e357dc3c84c0a6edc9344f9e3a93383c25  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/round30.stdout
cceee83f52b7688de6197cb5cd865c155ae016511f7dc38cceaabe5536461517  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/selftest.stderr
f9c5a58b3255bbd2ed5d51ec99357d0ff58c798b944944acb2b9e05afe382789  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/selftest.stdout
661b7e2f8c3ea3e16893ebfb428667df62c31b1f1c1de3033e31f1adae14813f  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/cited-runs-gate.py
9f289711d6b763aafc93873d5a8f052e9d098f17b1bac822c046a4758d115087  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/mutant-source.py.txt
b82dd489eb0de2b53d27db09fc5845eb88c39cccafeb11496e5d2dbf166ab98d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/mutation.diff
c9e3080d6ed2a2840e07c32275ab9b670a1ec971fe8ef40da8ac22331f57c1eb  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/round30.stdout
027e940ca7a7f6f49b610eaf42667505433fbb3dad98b64361166bfb8a82fbd1  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/selftest.stderr
2571ef95d0c81cd4ae168460c74b6b1ac62f5ac29f646fc039fa452b73cec75d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/selftest.stdout
f784623e18d6ab4b9195daf58cba2ed50aa93f014a7b24e7e70a2db30fb87b80  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/mutated/state.json
6488ec33a1cf202f5c54a0eaf8aca4f19cb28a763f069cb2a584f782785ed247  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/round30.stdout
84bb348feab5ea9624577f118b3543f30d6980ab870cf61fb258040b2730c6f7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/selftest.stderr
94a39bc66ec60c9a111cb826780989f008779ac2acba892628fe057765c8bc13  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/selftest.stdout
166e4630208fb95994b39c026c3d0b872c490101836b0be8f042153a32093496  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M15/restored/state.json
ba5f51433ee67244ad7b7f741e147c4c3162be94b2be23a1bdfca47c077247c8  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/round30.stdout
09cb38393fd97659f13faddf5068266ed0fc1d73b0c779401b512280f9e26c78  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/selftest.stderr
3c2500e5cd096f1942374abde2e11f9d8966bb2c0ea8520a63ffb5c8bde9bbe6  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/selftest.stdout
69b6c5e9ca42bbd0ac4c2ed4b61452598f5f44dfc590c9e70a05a6908e2ab40c  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/baseline/state.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/cited-runs-gate.py
140c62d544a61eec5180a465c4c9e65de2f83fe65dd13af28493c979758a90a2  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/mutant-source.py.txt
396d0a29b855dd823a795924f06e39098a83c519a13406c77aba50c9939442bb  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/mutation.diff
ed0503b52feefab7df8374c318c7d32ca52233a08759e30044ed26023ec53ba7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/round30.stdout
546b1e7741b06b7ad4e8cb877f8293056b043d04903c1530170d80c6817f3d03  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/selftest.stderr
d1c04ca2b5861bc02ac736ffe2438e41eff9084ffd72ef94a25a82d8632ad0cd  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/selftest.stdout
947c80722d0a703dc2621eb01a97383dec070f77b48be7dff89744e4aacb15c0  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/mutated/state.json
e9b973a930e97a3e73fa7b08d353d088feac8bc39a4a0f15df42dbde043a4732  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/round30.json
32ad18918c508ab323cc745f87739589185bf3749040aa3d350f80dc55d1eb0b  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/round30.stderr
d8b2fff287f163000d4bf683a0c3ce040c742c694ef050ac7869e09cd4a6dad5  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/round30.stdout
16cce708c83ac0094819d64612f08825e41b98b55283cf2b4910c86d29c47eee  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/selftest.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/selftest.stderr
abe69c54be39ec0a982583afca0517d9978b4f819d506b44d789301da6019d33  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/selftest.stdout
63e0d0d98643c96707dc35046a5ed6c4c4b6714b23f5788a8356c59adb71815d  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/M16/restored/state.json
c0ee9e439e1c7438b2637f2be8a5ef693e089ca45fc7e01404edd8d04e75fcd2  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/artifact-manifest.json
d501ec6a93134bb41beffd853b8f7fd6c35c0317b675f307c3625e6abd60e663  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/artifact-manifest.tsv
6f5e66ed7f5587a738aaa1ba5bc0a477663dfff25925cbde40e584b446187f25  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/baseline-results.json
3e5485f35a2ddda02c8ffa4b5e46e339eb7cadace4bea7628d2082d531d58ab3  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/harness.py
0294a9734491b56e0b17b4ada19b94d655fb39e6f249bc62acceb2c65614ef33  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/mutated-results.json
7e4fe12c4faefc00667f70c846adfedb7988c0c2d10b69a2d1df614845941ade  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/prepared.json
f025ac052da465935a2f9cededda67e6a13c5203fdd116dc117b971db4418b83  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/pristine/cited-runs-gate.py
120a0c42c7189b44f42e4e7e3f4a92486620ef4bf770faf51953785589abe434  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/restored-results.json
014197b15d522e951a137a71d89f4f9d4c7741291220615928040978312cd530  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/sources.json
9bca15c9e7a316b3f64e22efc601cdebe319566887dd0f4558c394472761e4c7  /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutCitedRunsGate/summary.json
```

## Handoff

Assigned mutation probe complete. Missing cases are findings only; no integration or shipping action taken. No tool installs/updates to report.
