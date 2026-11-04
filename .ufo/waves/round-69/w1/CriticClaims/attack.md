# CriticClaims — predicate attacks, round 69 wave w1

Leaf seat. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; every `tools/...` command
below was run with that as cwd. Scratch `/fast/scratch/hyaku/kaidoku-r69/CriticClaims/` (removed at
seat end). No tool was installed; no pacman transaction was run.

Labels: **obs** = observed by a command recorded here; **inf** = inference from observed bytes;
**unk** = not run.

## 0. Frozen-input verification (obs)

| input | measured | pin / expectation | verdict |
|---|---|---|---|
| `tools/round-69/packed-elf.py` @ HEAD | `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` | same | matches |
| `tools/round-69/mutation-check.py` @ HEAD | `51b64c56c48899d5d2d707298431861f8465e5422e53ee7dceb903d1b56d33c2` | same | matches |
| `tools/round-69/contract-probe.py` @ HEAD | `e609d85d0fc4604ef582ae886da38b4d335c558a1954c12344df0e468669061d` | same | matches |
| `tools/round-69/controls.py` @ HEAD | `1f8f78c177b33196cb2a4cb6c9c4c999e70d07c4c158ddac250dae2a0196b918` | same | matches |
| `tools/round-68/packed-elf.py` @ base `d7d9a62` | `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` | its own round | matches |
| `.ufo/waves/round-69/claims.json` @ freeze `f1599810` and worktree | `ebc68ac5…` both | frozen container | matches |

After-arms were run at `3f3d20fc065b5be62f676028b9a38d316ddfe8fd` (HEAD when run; the A9 landing
commit does not exist at w1). `tools/round-69/` first appears at `616a5f2f`, so the base revision is
unusable for `git show <rev>:tools/round-69/...`; the tool blob at HEAD is byte-identical to the
pin, so the after values are expected to be revision-stable (inf).

## 1. C3 — fixtures that satisfy the predicate sentence without the capability

Counter: `python3 -I -B tools/round-69/packed-elf.py --check-receipt <fixture>` (obs).

| fixture | what it fabricates | rc | checker says |
|---|---|---|---|
| `fixtures/f1_fabricated_counts.json` | 3 rows, ids jq/xxd/libz, invented packed counts (1/1/1), declared ceilings 10/10/120 | 0 | `met true`, target 3, matched 3, kinds [executable, shared-object] |
| `fixtures/f2_relabelled_executable.json` | libz row is `/usr/bin/xxd` relabelled `kind: shared-object`, name `libz`, pin = xxd's sha | 0 | `met true` |
| `fixtures/f3_ceiling_inconsistent.json` | libz `packed_counts.procedure_count 183`, `before_ceiling 120`, declared ratio 0.6522 | 0 | `met true` |
| `fixtures/f4_anonymous_empty.json` | 3 rows with no `id`, `orig_counts {}`, `packed_counts.procedure_count 0` | 0 | `met true` |
| `fixtures/f7_two_rows_declared_three.json` | only **two** carrier rows while `carriers_matched` declares 3 | 0 | `met true` |
| `fixtures/f5a_boundary_075.json` | declared ratio exactly 0.75 | 0 | `met true` (consistent with "at or below") |
| `fixtures/f5b_boundary_07501.json` | declared ratio 0.7501 | 1 | `libz: before_ceiling_ratio 0.7501 > 0.75` |
| `fixtures/f6_no_shared_object.json` | all three kinds `executable` | 1 | `no shared-object carrier` |

`check_receipt()` (packed-elf.py:265–316) reads `target`, `carriers_matched`, `control_ok`,
`met_target`, `failing`, each row's `ok`/`arms`/`before_ceiling_ratio`, and the presence of two
count dicts. It never checks the row count, the carrier id/pin/source against `CARRIERS`, the
receipt's `instrument.sha256`/`rev`, or the relation between `before_ceiling_ratio`,
`before_ceiling`, `orig_counts.procedure_count` and `packed_counts.procedure_count`. `f3` proves the
last point directly: a packed inventory *above* its declared ceiling passes.

The round's own do-nothing control set contains the same fact: `c3-synthetic-met`
(`controls.py:57–75`, invoked at `controls.py:149–159`; observed rc 0 in `receipts/controls-head.json`) is the synthetic
three-row receipt passing with no run behind it.

## 2. C2 — fabricated receipt passes the receipt-derived arms

Counter: `python3 -I -B tools/round-69/contract-probe.py --root . --rev 3f3d20fc --tool
tools/round-69/packed-elf.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
--work <scratch> --receipt <fixture>` (obs).

| fixture | fabrication | rc | arms |
|---|---|---|---|
| `fixtures/c2_fabricated_receipt.json` | 3 rows from real host sources, but `instrument.sha256 = 0*64`, `rev = e*40`, invented `runs` | 0 | **6/6** |
| `fixtures/c2_fabricated_one_carrier.json` | same, **one** carrier | 0 | **6/6** |
| `fixtures/c2_noncarrier_receipt.json` | single row whose source is `/bin/ls` (not a declared carrier) | 0 | **6/6**; A5 observed the `/bin/ls` pin/format |
| `fixtures/c2_fabricated_probe_receipt.json` | six rows, `observed: {"invented": true}` | 0 (`--validate`) | defect-free |

A5 re-derives pin/format from the *receipt's own* `source` string on the live host; A6 compares the
*receipt's* packer block to the host upx. Neither arm binds the receipt to the instrument bytes or
the measured revision, although the real payload carries `instrument.sha256` and `rev`. A5 also
never requires the three pinned ids; `c2_noncarrier_receipt.json` shows a non-carrier passing.

Before-arm context: the same probe against `tools/round-68/packed-elf.py` at the base revision with
`.ufo/waves/round-68/l1/scores/c2-at-landing.json` is **0/6**, all six named
(`receipts/rederive-c2-r68-base.json`, rc 1). Against the round-69 instrument with the *old* receipt
it is **4/6** (A5/A6 false) — so the after-target does not follow from the do-nothing receipt
(`receipts/rederive-c2-r69-head-oldreceipt.json`, rc 1).

## 3. C1 — receipt and bytes attacks

Counter used: `python3 -I -B tools/round-69/mutation-check.py ... --patch-set r69` (obs).

| fixture | construction | result |
|---|---|---|
| `fixtures/c1_fabricated_green_battery.json` | five `killed` rows, `survivors []`, `pristine_ok true`, `target_sha 0*64` | `--validate` rc **0**, defects [] |
| fixture repo `…/fixture-repo` @ `0a9c2d07e97ac72b9c7085317baf5dc00c3daa48` | round-69 route with the five arm-false case assertions gated by a sha256 of the `evaluate_carrier` body (not by feeding a false model); pristine green | battery rc **0**: `survivors []`, all five `killed` naming their declared cases, `pristine.cases 20`, `ok true`; `target_sha256 2368bbc3…` ≠ pin `4ac0d83b…` (`receipts/fixture-c1-doctored.json`) |

Serial re-derivations (obs):

- before-arm: `--rev d7d9a62 --tool tools/round-68/packed-elf.py --patch-set r68` → rc 0,
  survivors exactly `[M1_identity, M2_recovery, M3_detected, M4_before, M5_control]`,
  `pristine.cases 13`, `target_sha256 48ef4c68…` (`receipts/serial-c1-r68-base.json`);
- after-arm: `--rev 3f3d20fc --tool tools/round-69/packed-elf.py --patch-set r69` → rc 0,
  survivors `[]`, five kills with exactly `arm-pack-identity-false`, `arm-pack-recovery-false`,
  `arm-pack-detected-false`, `arm-pack-before-false`, `arm-pack-control-false`, `pristine.cases 20`,
  `pristine.ok true` (`receipts/serial-c1-r69-head.json`).

Two counter hazards found while doing this (both routed, neither is a claim change):

1. **Concurrency.** `check()` uses the fixed directory `<work>/mutation-check` (mutation-check.py:124) and
   `rmtree`s it at start. Two battery runs sharing one `--work` (my first r68 and r69 runs) raced: the r68 receipt
   recorded `pristine.cases 20` (the round-69 tool's count) while its mutant rows were round-68
   bytes — `receipts/raced-c1-r68-base.json`, `target_sha256 48ef4c68…`, `ok true`. A receipt can
   therefore carry a green `pristine` block that did not run the bytes `target_sha256` names.
2. **`ok` ignores the pristine case count.** `check()` sets
   `ok = len(survivors) == expected and not wrong` (mutation-check.py:158); `EXPECTED_SURVIVORS`
   (line 74) has no case-count entry.
   The C1 predicate requires `pristine.cases 20` (r69) / `13` (r68), but the counter's exit 0 does
   not enforce either number. The L1 must read `pristine.cases` from the receipt, not just rc.

Within the pinned bytes the five kills are genuine (the mutants change `evaluate_carrier`, each
serial run's `failed` list is exactly the declared case, and the base run survives all five). The
doctored-bytes fixture only passes because the counter does not bind `target_sha256` to the declared
pin; the container A1 pin and the kill rule's "post-freeze instrument edit" clause exclude it
outside the counter.

## 4. Before-arms reproducible from committed bytes at `d7d9a62` (obs)

- C1: yes — five survivors, pristine 13, rc 0 (above); matches `pre/c1-at-base.json`.
- C2: yes — `rederive-c2-r68-base.json`: `arms_passed 0`, target 6, `failed` names all six,
  `instrument_sha256 48ef4c68…`, rc 1; matches `pre/c2-at-base.json`.
- C3: yes — `receipts/rederive-c3-r68-receipt.json`: rc 1,
  `target 2`, `carriers_matched 2`, `kinds [null]`, failing `target 2 != 3`, `carriers_matched 2 !=
  3`, `no shared-object carrier`, both `before_ceiling_ratio None > 0.75`; matches
  `pre/c3-at-base.json`.
- Controls: `controls.py --rev 3f3d20fc` → rc 0, all seven arms ok (`receipts/controls-head.json`),
  observations equal `pre/controls-at-base.json` (c1-do-nothing 5 survivors; c2-do-nothing 0/6;
  c3-do-nothing target 2; c3-synthetic-met met; c3-loose-ceiling rejected).

## 5. C3 arithmetic and the libz ceiling (obs)

Declared ceilings (A8 / plan): jq 10/167 = 0.059880, xxd 10/99 = 0.101010, libz 120/184 = 0.652174
— no ratio exceeds 0.75. Independent re-derivation in scratch with `/usr/bin/upx` 5.2.0 and REA
6.5.0 (`rea.mjs analyze`) on `/usr/lib/libz.so.1.3.2` (sha256 `6c78c5e5…`, matching the pin):
original 184/29/199, packed 98/6/136 — the plan's numbers. The libz ceiling 120 ≥ measured packed 98
(headroom 22; measured packed/original = 0.5326), so the declared ceiling is justified as a class
bound with headroom. The counter does not verify that relation (`f3`), and it does not verify the
declared ratio is `ceiling / orig` at all.

## 6. Verdict sentences

- **R69-C1 — not falsified as written.** With the pinned bytes and a serial run, the battery reports
  exactly the predicate's after values at HEAD and exactly the predicate's before values at the base.
  The passing doctored-bytes fixture (`2368bbc3…`) is excluded by the container pin A1 and the kill
  rule's post-freeze-edit clause; the receipt-only fixture is rejected by `--validate`. Residual
  counter defects are routed: `ok` does not check `pristine.cases`, and the fixed scratch path is not
  concurrency-safe (a raced run can record `pristine.cases 20` for round-68 bytes).
- **R69-C2 — falsified as a counter proposition.** `arms_passed 6` rc 0 is reachable with a fabricated
  receipt the instrument never wrote (invented `instrument.sha256`/`rev`, one carrier, even a
  non-carrier `/bin/ls`); the predicate's "the measured run's receipt" is unenforceable by the
  counter. Routed correction: compare `receipt["instrument"]["sha256"]` with the committed tool blob
  the probe already hashes (`instrument_sha256`) and `receipt["rev"]` with the measured rev, and
  require the three pinned carrier ids.
- **R69-C3 — falsified as a counter proposition.** `--check-receipt` returns `met true` on invented
  counts, a relabelled executable claiming `kind: shared-object`, a packed count above its ceiling,
  anonymous empty inventories, and two rows while declaring three. Routed correction: derive the
  ratio from `before_ceiling`/`orig_counts.procedure_count`, require
  `packed_counts.procedure_count <= before_ceiling`, require the three pinned ids/pins/sources, and
  bind the receipt's `instrument.sha256`/`rev` (the checker takes no revision today).

Impacted axes: C1 calibration (counter robustness only); C2 operability (A5/A6 receipt provenance);
C3 coverage (every arm is receipt-declared). No predicate was narrowed, widened or re-frozen.
