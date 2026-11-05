# MutCounter: round-92 mutation test of the frozen counters (R92-C1, R92-C2)

Lane `kaidoku`, round 92, attempt 1. Revision under test `11f8606178dfd9e72001b31daf412c5463106a63`
(declaration commit; base `73a882712907606eba074377b536c6dd82517e25`). Scratch clone at that commit; the
lane was not written. Seat deliverables: `.ufo/waves/round-92/w1/MutCounter/` (`kill-matrix.json`,
`commands.txt`, `receipts/`, `mutants/`, `SHA256SUMS-seat.txt`).

## Verdict

- Both frozen counters detect every assigned repair-side and refusal-side failure except the two membership
  counterfeits below. 9 of 11 assigned mutants are killed; both controls behave as declared.
- **Two assigned counterfeits survive the calibration counter (M1, M2).** The counter admits any refusal
  oracle whose accepted set is exactly the public carrier set, including one that names the unseen carrier.
  This is a named limit on R92-C2, not something this seat tuned away.
- **One extra C1 variant survives (N1i).** A carrier-table repair that passes intact input through meets the
  C1 label. C1 measures output bytes on five pinned carriers; it does not check that a repair is decided by
  `upx -t`. This is a named limit on R92-C1's coverage reading.
- The real C1 candidate, `tools/round-92/upx-stop-boundary-search-repair.py`, does not exist at this commit.
  C1 was exercised only through the stand-in mutants below; no measurement of a real candidate is claimed.

## Inputs verified (read-only)

- `tools/round-92/stop-boundary-battery-v2.py` sha256 `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`
  (= claims pin). Re-checked in lane and clone after all runs: unchanged.
- `tools/round-92/stop-boundary-repair-battery.py` sha256 `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`
  (= claims pin). Re-checked after all runs: unchanged.
- Packer `/usr/bin/upx` sha256 `cf2f6e7c...c969` (UPX 5.2.0, pinned). Carrier `/usr/bin/xz` sha256 `24c47749...1bda`.
- Interpreter Python 3.14.8. Packing is byte-deterministic: the five pristine carrier packed images
  reproduce the lane's pre-receipt `packed_sha256` values exactly (jq, xxd, libz, dinit, xz-unseen).

## Harness validity (controls and cross-checks)

| run | counter | repair | exit | label | result |
|---|---|---|---|---|---|
| B0 positive control | v2 | round-91 refusal tool | 0 | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | met True (holds) |
| B1 do-nothing control | C1 | round-91 repair tool | 1 | `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | met False (holds) |
| CA CHEAT-A clone | v2 | carrier-read, 4 carriers | 1 | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5` | reproduces lane pre label |
| CB CHEAT-B clone | v2 | hash table, 4 hashes | 1 | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5` | reproduces lane pre label |
| CC CHEAT-C clone | v2 | rc 2 to exit 1 | 1 | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5` | reproduces lane pre label |

The lane counterfeit scripts hard-code the lane root, so clone copies were used; the three reproduce the
lane's pre labels exactly (`harness_crosscheck` in `kill-matrix.json`).

## Kill matrix

Verdict rule (fixed before reading results): `met_target` False means KILLED; True means SURVIVED.
Full command lines and exit codes: `.ufo/waves/round-92/w1/MutCounter/commands.txt`.

| id | class | counter | exit | label as emitted | verdict |
|---|---|---|---|---|---|
| M1 | assigned: CHEAT-A plus unseen xz on carrier list | v2 | 0 | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | **SURVIVED** |
| M2 | assigned: CHEAT-B, five fresh packed sha256 | v2 | 0 | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | **SURVIVED** |
| M3 | assigned: rc 2, plain-text last line | v2 | 1 | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5` | KILLED (typed gate) |
| M4 | assigned: rc 2 that also writes output | v2 | 1 | `refused 0 of 10; typed 0; unsafe 0; intact 5 of 5` | KILLED (refused gate) |
| M5 | assigned: rc 2 JSON without `refused` | v2 | 1 | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5` | KILLED (typed gate) |
| M6 | assigned: exit 1 on all refusals (CHEAT-C variant) | v2 | 1 | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5` | KILLED (typed gate) |
| N1 | assigned: pinned-image table, intact refused | C1 | 1 | `repaired 10 of 10; wrong 0; unsafe 0; intact 0 of 5; far-refused 10 of 10` | KILLED (intact gate) |
| N2 | assigned: sentinel outside window, rc 0 | C1 | 1 | `repaired 0 of 10; wrong 0; unsafe 10; intact 0 of 5; far-refused 10 of 10` | KILLED (unsafe gate) |
| N3 | assigned: window rewritten to non-pristine, rc 0 | C1 | 1 | `repaired 0 of 10; wrong 10; unsafe 0; intact 0 of 5; far-refused 10 of 10` | KILLED (wrong gate) |
| N4 | assigned: far cells repaired, intact refused | C1 | 1 | `repaired 10 of 10; wrong 0; unsafe 0; intact 0 of 5; far-refused 0 of 10` | KILLED (far, intact gates) |
| N5 | assigned: intact with one byte changed | C1 | 1 | `repaired 10 of 10; wrong 0; unsafe 0; intact 0 of 5; far-refused 10 of 10` | KILLED (intact gate) |
| N1i | extra: pinned-image table, intact identity | C1 | 0 | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | **SURVIVED** |
| N4i | extra: far repaired, intact identity | C1 | 1 | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 0 of 10` | KILLED (far gate alone) |
| X1 | extra: tampered cells rc 0 with sentinel | v2 | 1 | `refused 0 of 10; typed 0; unsafe 10; intact 5 of 5` | KILLED (unsafe gate) |
| CA/CB/CC | cross-checks (above) | v2 | 1 | see table above | KILLED, reproducing lane labels |

Summary: assigned mutants 9 of 11 killed (M1, M2 survive; N1 is killed only by its intact gate). Extras: N4i
and X1 killed; N1i survives. The lane-counterfeit cross-checks CA, CB and CC are killed and reproduce the lane
pre labels. Every gate of both counters is exercised by at least one killing mutant: v2 refused (M4), typed
(M3, M5, M6), unsafe (X1), intact (CA, CB); C1 repaired (N2, N3), wrong (N3), unsafe (N2), intact (N1, N5),
far-refused (N4, N4i). X1 was added because no assigned mutant reached the v2 `unsafe` gate; M4 lands in `other`.

## Named limits (survivors)

**LIM-1 (R92-C2, calibration; M1).** A counterfeit that reads the public carrier list and refuses by
membership passes v2 exactly once the unseen carrier `/usr/bin/xz` is on that list. Its intact control is
identity on all five carriers, and its tampered cells are typed refusals on all five. The unseen-carrier
defence therefore only excludes counterfeits written without that carrier; it is not a property of the
counter. Evidence: `receipts/M1.json` (5 intact identity true; 10 typed refusals).

**LIM-2 (R92-C2, calibration; M2).** A hash table of the five pinned packed sha256 values passes v2 exactly.
Any oracle that accepts exactly the battery's packed carriers and refuses everything else is indistinguishable
from the honest refusal on this battery. The claim "admitted 0 of 3" holds for the three declared
counterfeits; it does not bound membership oracles over the public carrier set. Evidence: `receipts/M2.json`.

**LIM-3 (R92-C1, coverage; N1i, extra).** A carrier-table repair writes the pinned packed image for tampered
cells, passes intact input through, and refuses far cells by a delta check. It meets the C1 label exactly.
C1 scores output bytes only; it cannot see whether the repair is decided by `upx -t`, which the claim names as
the decision rule. A `repaired 10 of 10` reading is therefore coverage of five pinned carriers, not evidence of
a general packer-verdict search. Evidence: `receipts/N1i.json`; table in `mutants/pinned/table.json`.

These are finite-proxy limits of the frozen batteries. Per the assignment the counters were not tuned,
re-declared or re-targeted, and the claims were not edited.

## Method and provenance

- Mutants: wrapper and standalone scripts under `$S/clone/.ufo/mut/` (scratch), copied to
  `.ufo/waves/round-92/w1/MutCounter/mutants/` with `SHA256SUMS`. Shared helper `mutlib.py` identifies the
  carrier by comparing to pinned packed images built by `build_pins.py` with the frozen v2 `pack` and `layout`.
  Counterfeits M1–M6 wrap the round-91 refusal tool (`tools/round-91/upx-stop-boundary-repair.py`, sha256
  `3779d35f...e238`) by monkey-patching `upx_test` or the return path, as the lane controls do.
- Driver: `run_matrix.sh` runs 17 counter invocations plus 2 baseline controls, each with
  `python3 -I -B <counter> --root <clone> --repair-cmd <mutant> --work $S/work/<id> --rev 11f8606... --expect "<frozen label>" --json-out <receipt>`,
  `TMPDIR=$S/tmp`. Total wall time about 31 s. Exit codes are the counter's exit; `met_target` in each receipt agrees.
- Matrix builder: `build_matrix.py` reads only receipts and the lane's pre receipts (read-only) and writes
  `kill-matrix.json`. Mutation design intent for M1, M2 and N1i (survival) was derived before the run; the
  run confirmed each.
- Receipts: `.ufo/waves/round-92/w1/MutCounter/receipts/` (`<id>.json`, `<id>.stdout`, `<id>.stderr`,
  `matrix.log`, and the two baselines `B0-positive-v2-round91.json`, `B1-do-nothing-c1-round91.json`).

## Scope notes and not done

- The assigned C1 mutants N1–N5 are stand-ins for a candidate repair, not the candidate itself (see Verdict).
- Lane writes: none. Only `.ufo/waves/round-92/w1/MutCounter/` and this file were written. Scratch
  `/fast/scratch/hyaku/kaidoku-r92/MutCounter` was removed after receipts were copied.
- Host: no sysctl, kernel, namespace, service or pacman change. No tools were installed or upgraded; the
  counters need only `python3`, `/usr/bin/upx` (5.2.0, pre-existing) and `/usr/bin/xz` (pre-existing).
- Named needs for the host: none.
- Suggested for a later round (not implemented here): a counter-side defence against membership oracles
  would need carriers the candidate cannot enumerate, for example fresh packed binaries generated at run time
  and not shipped in the repository. Left as a recommendation; the frozen counters stay as declared.
