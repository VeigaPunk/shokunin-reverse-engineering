# Round 99 — frozen claims (L1 KaidokuR99, attempt 1)

Base revision B = `de098f51cd73d3b9b4a895840da8f2bb0a386db8` (lane `main` at round start; clean tree).
Axes: every owned axis is recorded at 10.0 (SCORECARD `## Owned axes`), but the round-98
closure observed the coverage head as stale (claims 10.0 and 168/168; the stem recipe
observes 9.67, 176/182). Under the head as observed, coverage (9.67) is the lowest
non-retired axis; both claims bear on it: C1 repairs the self-assessment of it
(calibration), C2 moves its surface (coverage). Inputs: round-98 closure routed defects
1, 3, 4, 5 (`corpus/lessons/round-98-verifier-spotcheck.md` §5).

Disclosure (pre-freeze): the C2 candidate was drafted in scratch and dry-run once against
the frozen battery in `worktree` mode before this file was committed (label met). The
battery bytes did not change after that run; the forgeries were generated from that
draft. The landed measurement is at a commit, read through `git show`.

## R99-C1 — calibration: self-assessment mismatches 17 → 0

Self-assessment surfaces: the SCORECARD coverage head, the README coverage map's rows,
and the SKILL.md gate registry rows for the round-97/98/99 tools.

- Counter (frozen): `tools/round-99/self-assessment-audit.py` (atoms A1 head-score, A2
  head-fraction, A3 map-rows, A4 registry; docstring is the definition).
- Command: `python3 -I -B tools/round-99/self-assessment-audit.py --root . --rev <rev> --json-out <receipt>`
- Predicate (frozen, one sentence): the receipt's `mismatches` is 0 and the exit is 0 at the
  measured revision.
- Kill rule: `mismatches` > 0 or exit ≠ 0 at the landing revision → C1 not met (honest stop).
- Do-nothing control at B: `mismatches 17; head-score mismatch; head-fraction mismatch;
  map-rows 176 of 182; registry 0 of 9`, exit 1 (`.ufo/waves/round-99/pre/c1-do-nothing-at-base.json`).
- Forgery control (scratch clone, fixture commit; diff `.ufo/waves/round-99/pre/c1-forgery-control.diff`):
  the six stems as prose lines and stem-only rows, the head fraction edited to 182/182,
  path-only registry rows → `mismatches 15; head-score ok; head-fraction ok; map-rows 176 of
  182; registry 0 of 9`, exit 1 (`.ufo/waves/round-99/pre/c1-forgery-control.json`). The
  round-66 stem recipe alone is fooled by that forgery (head atoms ok).
- Selftest: 9 cases, 0 failures (`.ufo/waves/round-99/pre/c1-selftest.txt`), forgery classes
  F1–F8 in memory.

## R99-C2 — coverage: truncated UPX-packed PE payloads (frontier → core, refusal)

Surface moved: the Round-98 frontier note's "truncated payloads stay Frontier"
(`corpus/README.md`, Round-98 frontier note). The round-98 repair answers `ok intact`, exit 0,
on packs cut inside their sections, where `upx -t` fails with `OverlayException: invalid
overlay size` (closure routed defect 4). New decision: refuse `truncated` by the packer's own
arithmetic — `overlay = file_size - ALIGN_UP(last.rawdataptr + last.SizeOfRawData,
FileAlignment)`, invalid when negative (S324 `PeFile::unpack0` 3046-3049; S326
`Packer::checkOverlay` 431-433, opened this round) — while still repairing every round-98
tamper on a population the round-98 forgeries do not pass (closure routed defect 3: a
PackHeader at offset 517, four DLLs, `UPX2` third sections, runtime-random overlays, a
checksum-invalid decoy), plus the typed CLI envelope (three rc-1 crash paths).

- Counter (frozen): `tools/round-99/pe-upx-trunc-battery.py` (docstring is the definition).
- Command: `python3 -I -B tools/round-99/pe-upx-trunc-battery.py --root . --repair tools/round-99/upx-pe-repair.py --rev <rev> --work $HYAKU_SCRATCH/kaidoku-r99/<seat>/c2 --json-out <receipt>`
- Predicate (frozen, one sentence): the label equals
  `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79`
  and the exit is 0.
- Kill rule: any other label or exit ≠ 0 at the landing revision → C2 not met (honest stop;
  no re-pinning, no narrowing).
- Controls, scored at the freeze commit before the candidate is committed
  (`.ufo/waves/round-99/pre/c2-*.json`): do-nothing identity copy; the round-98 repair; red
  fixtures `tools/round-99/forgeries/g2…g8` (refuse-all, truncation-only, fixed offset 992,
  size cache over the pinned carriers, lazy anchor, over-refusal, oracle-caller). Every one
  must exit 1.
- Sourced: S326 (UPX 5.2.0 `src/packer.cpp`), opened this round.

## Not claimed (carried)

Round-97 routed defects 2–5 and 7 (kill rule honest leg, `ownrec`, imported pins, K-ownrun /
K-cwd) stay open. Round-98 routed defect 2 (raw v7/v8 selftest outputs) is housekeeping, not a
claim. Mach-O packs, other UPX versions, and non-truncation payload corruption stay Frontier.
