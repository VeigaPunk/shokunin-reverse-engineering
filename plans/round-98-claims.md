# Round 98 — frozen claims (L1 KaidokuR98, attempt 1)

Base revision B = `d0aebc288621b0072ac3eb2a79a62ad26bfa837a` (lane `main` at round start).
Axes: every owned axis sits at 10.0 (SCORECARD `## Owned axes`); the stagnation nudge
applies (AXES.md *The stagnation nudge*): C1 is a frontier → core move. C2 repairs the
round-97 calibration harm (closure routed defect 1).

## R98-C1 — coverage: packed PE inputs (frontier → core)

Surface moved: the round-92 frontier note's `PE and Mach-O packed inputs` clause
(`corpus/README.md:393`), for UPX 5.2.0 `--best` win32/pe and win64/pe under three
anti-unpack tampers (PackHeader magic zeroed, `UPX*` section names renamed, both).
The lane's held repair `tools/round-87/upx-magic-repair.py` is ELF-only.

- Counter (frozen): `tools/round-98/pe-upx-tamper-battery.py`.
- Command: `python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd tools/round-98/upx-pe-repair.py --work $HYAKU_SCRATCH/kaidoku-r98/<seat>/c1 --json-out <receipt> --rev <rev>`
- Predicate (frozen, one sentence): the label equals
  `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` and the exit is 0.
- Oracle: unpack equivalence by the pinned packer (`upx -d` sha256 of the repaired file equals
  `upx -d` sha256 of the untampered packed file); the candidate never sees the untampered file.
- Kill rule: any other label, or exit ≠ 0, at the landing revision → C1 not met (honest stop;
  no narrowing, no re-pinning).
- Do-nothing controls (committed before the candidate exists, at B):
  - identity copy (`tools/round-98/controls/identity-copy.py`):
    `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18`, exit 1
    (`.ufo/waves/round-98/pre/c1-identity-control.json`).
  - held ELF repair (`tools/round-87/upx-magic-repair.py`):
    `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18`, exit 1
    (`.ufo/waves/round-98/pre/c1-r87-control.json`).
- Sourced: the repair rule rests on UPX 5.2.0 `src/pefile.cpp` (`PeFile::canUnpack0`:
  the `"UPX"` prefix test on section 0 and `readPackHeader(1024)` from
  `isection[1].rawdataptr - 64`; section naming at pack time), a SOURCES row opened this round.

## R98-C2 — calibration: the stop-boundary counter accepts its own honest verdict

Routed defect 1 (round-97 closure): v7's counts allow-list has nine keys, the verdict emits
fourteen, so the honest public run exits 1.

- Counter (frozen): `tools/round-98/allowlist-check.py`.
- Command: `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev <rev> --work $HYAKU_SCRATCH/kaidoku-r98/<seat>/c2 --json-out <receipt>`
- Predicate (frozen, one sentence): the label equals
  `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1` and the exit is 0.
- Kill rule: any other label or exit at the landing revision → C2 not met.
- Do-nothing control (at B, v7 unchanged): `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1`,
  exit 1 (`.ufo/waves/round-98/pre/c2-v7-control.json`). A blanket-refusing candidate fails
  `public` and `real14` by construction (positive legs retained).

## Not claimed (routed, open)

Round-97 routed defects 3–6 (kill-rule `ownrec` slot, imported-pin revision binding,
K-ownrun/K-cwd legs, clean-checkout before-side) are not claimed this round; they stay open
and are named in the report. Defect 7 (local-source gate on S082/S302/S321) stays open.
