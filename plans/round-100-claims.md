# Round 100 — frozen claims (L1 KaidokuR100, attempt 1)

Base revision B = `6371c88633f6ce6692eaeff17e256b80ad21ece0` (lane `main` at round start; clean tree,
`jj-lane.sh state`: `ahead=0 behind=0 tracked=0 untracked=0`).
Axes: every owned axis is recorded at 10.0 (SCORECARD `## Owned axes`), a tie for lowest; a
capability entered at round 99, so the stagnation nudge does not waive the lowest-axis duty.
C2 works calibration, whose recorded 10.0 is contradicted at B by seven registry rows whose stated
self-test case count the tool itself does not print (measured below, before any edit). C1 moves
coverage (frontier → core) and is the round's sourced claim (S327, opened this round).
Inputs: round-99 closure `corpus/lessons/round-99-verifier-spotcheck.md` §5 (defects 1–6) and the
round-99 lesson `## Named limits` 1–2.

Disclosure (pre-freeze): the C1 candidate was drafted in scratch and dry-run once against the
frozen battery in `worktree` mode before this file was committed (label met, exit 0). The battery
bytes did not change after that run; the red fixtures were generated from that draft by
`tools/round-100/gen-forgeries.py`. The landed measurement is at a commit, read through `git show`.

## R100-C1 — coverage: payload corruption at intact length of UPX-packed PE (frontier → core, refusal)

Surface moved: the Round-99 frontier note's "payload corruption at intact length" (`corpus/README.md`,
Round-99 frontier note: Still Frontier). At B the round-99 repair answers `ok intact`, exit 0, on a
pack with one byte flipped inside its compressed data, where `upx -t` fails with
`Exception: checksum error` (probe at round start: four random offsets in a `t32.exe` pack, all
four `ok intact` rc 0 vs `upx -t` rc 1). New decision: refuse `checksum` by the packer's own rule —
`ph_decompress` compares `upx_adler32(in, ph.c_len, ph.saved_c_adler)` with `ph.c_adler` before
decompressing (UPX 5.2.0 `src/packhead.cpp` 334-338, **S327**, opened this round); the compressed
data is read right after the 32-byte PackHeader (`src/pefile.cpp` 3053, S324; header size,
`packhead.cpp` 94-101). Process-level guard (round-99 named limit 2, CriticC2 fg/fg3): every
candidate invocation runs under `strace`; any exec beyond the interpreter fails the `exec` leg.

- Counter (frozen): `tools/round-100/pe-upx-corrupt-battery.py` (docstring is the definition; the
  round-99 arms are kept unchanged as the regression population).
- Command: `python3 -I -B tools/round-100/pe-upx-corrupt-battery.py --root . --repair tools/round-100/upx-pe-repair.py --rev <rev> --work $HYAKU_SCRATCH/kaidoku-r100/<seat>/c1 --json-out <receipt>`
- Predicate (frozen, one sentence): the label equals
  `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; exec 1 of 1; effective 119 of 119`
  and the exit is 0.
- Kill rule: any other label or exit ≠ 0 at the landing revision → C1 not met (honest stop; no
  re-pinning, no narrowing).
- Controls, scored at the freeze commit before the candidate is committed
  (`.ufo/waves/round-100/pre/c1-controls-at-freeze.txt`, receipts `pre/c1-*.json`): the round-99
  repair (do-nothing successor); red fixtures `tools/round-100/forgeries/h0…h6` (identity copy,
  refuse-all, off-by-header window, u_adler confusion, aliased-`os` `upx -t` oracle, length test
  without checksum, the candidate plus one harmless aliased exec). Every one must exit 1.
- Sourced: S327 (UPX 5.2.0 `src/packhead.cpp`), opened this round
  (`.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp`, sha256
  `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a`).

## R100-C2 — calibration: registry self-test case counts checked against the tools, 7 → 0

Self-assessment surface: the self-test column of the `SKILL.md` instrument registry. The round-99
counter checked presence and shape, not truth (round-99 named limit 1, L1/L6; closure §2). This
counter runs each claim-bearing row's documented self-test at the measured revision (in a
`git clone --shared` under `--work`) and compares the count the tool prints with the count the
row states.

- Counter (frozen): `tools/round-100/registry-selftest-truth.py` (docstring is the definition;
  population: the 93 registry rows that state a case count at B, each with its documented argv and
  the sha256 of the tool and of the script it executes, pinned at B; none excluded — every one ran
  green and printed a parseable count at B).
- Command: `python3 -I -B tools/round-100/registry-selftest-truth.py --root . --rev <rev> --work $HYAKU_SCRATCH/kaidoku-r100/<seat>/c2 --json-out <receipt>`
- Predicate (frozen, one sentence): the label equals
  `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`
  and the exit is 0.
- Kill rule: any other label or exit ≠ 0 at the landing revision → C2 not met.
- Do-nothing control at B: `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 86 of 93; mismatches 7`,
  exit 1 (`.ufo/waves/round-100/pre/c2-do-nothing-at-base.json`). The seven: `tools/round-46/attest.py`
  15→18, `tools/round-47/record.py` 9→10, `tools/round-71/packed-elf.py` 31→32,
  `tools/round-71/seam-probe.py` 7→9, `tools/round-76/record-audit.py` 17→18,
  `tools/round-76/plan-command.py` 3→7, `tools/round-89/upx-field-value-repair.py` 16→22 (stated→printed).
- Forgery controls (scratch fixture repo, fixture bytes committed under
  `.ufo/waves/round-100/pre/forgery/`, receipts `pre/c2-forgery-*.json`, transcript
  `pre/c2-forgery-controls.txt`), each exit 1, `mismatches 7`:
  F-drop (the seven count phrases deleted: `claimed 86 of 93`), F-tool (the round-89 tool edited to
  print the stale 16: its row agrees but the pin fails), F-dup (corrected duplicate rows appended,
  stale rows kept: the row atom fails for all seven). Fixture revisions are scratch-only and are
  not cited as identities; the committed bytes are (lesson M99-j).
- Selftest: 22 cases, 0 failures (`.ufo/waves/round-100/pre/c2-selftest.txt`); the banner prints
  `len(cases)` (M99-h); receipts are written through mkstemp (M99-g).

## Frontier step and housekeeping (inside the claim cap)

- SOURCES: S327 new (tier A). Round-99 closure defect 1: the S327-candidate rejection drafted by
  round-99 ScoutSources (no row; would have duplicated S326) and a round-99/100 search-log note go
  into the `## Search log` and the lesson `## Gate`. Defect 2: the census W04 for S326/S310 is
  recorded as a correction.
- Mistake mined into `corpus/lessons/round-100.md` `## Mistakes`.

## Not claimed (carried)

Round-99 closure defect 5 (recipe A restated or retired), round-99 named limits not listed above
(C1 counter L2–L5; repair FIFO/MemoryError; non-power-of-two FileAlignment; phantom section),
round-97 routed defects 2–5 and 7. Mach-O, other UPX versions, a corrupted pack whose `c_adler`
is forged to match (needs the codec for `u_adler`) stay Frontier.
