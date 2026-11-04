# Round 69 / w1 / MutBattery — new mutants of the round-69 route

Seat: mutation-tester (MutBattery), leaf, no subagent dispatch.
Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-69/packed-elf.py`,
frozen bytes `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`,
operative freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`.
All work was done on copies under `/fast/scratch/hyaku/kaidoku-r69/MutBattery/`; the
lane file was never opened for writing, and its sha256 is unchanged (restoration
evidence below).

Labels: **[observation]** = executed and recorded this seat; **[inference]** = follows
from the observed code/behaviour but was not itself executed; **[unknown]** = not
determined.

## Summary

- 20 new mutants, each a single textual patch at a site the frozen five do not touch;
  every patch site matched exactly once in the frozen source **[observation]**.
- The **frozen detector set** — the 20-case `--selftest`, the three receipts the controls
  already drive (`c3-synthetic-met`, `c3-loose-ceiling`, `c3-do-nothing` = the round-68
  landing receipt), and contract arms A1/A2 — kills **3 of 20**: `MB05_receipt_ratio_bound`,
  `MB11_section_branch_return`, `MB19_check_work_false` **[observation]**.
- With this seat's extended receipt battery (11 receipts) the score is **8 killed, 12
  survived** **[observation]**.
- Of the 17 frozen-set survivors, 2 are equivalent (`MB10`, `MB20`), 1 is over-strict
  (`MB01`), and 14 change behaviour under an input no frozen detector feeds
  **[observation for the behaviour; inference for "no frozen detector feeds it", which rests
  on the full run of every mutant against every frozen fixture]**.
- The strongest survivor is `MB18_ratio_constant`: an end-to-end run of the mutant writes
  `before_ceiling_ratio 0.0` for all three carriers while the same receipt still says
  ceiling/original = 10/167, 10/99, 120/184, and the **frozen checker scores it `met true`,
  `failing []`** **[observation]**.

Full per-mutant table, patches, detector firings and kill routes: `MutBattery/mutants.md`.

## Runs executed

| run | command shape | rc | result |
|---|---|---|---|
| pristine selftest | `python -I -B pristine-packed-elf.py --selftest` | 0 | cases 20, failed `[]` |
| pristine `--check-receipt` × 11 | same binary, one receipt each | 0/1 as tabled | see baseline below |
| pristine preflight A1/A2 + combined | instrument with PATH without `node`, and with a `0500` work root | 2 | `missing_tool: node` / `work_unusable: not writable` / combined names `node` |
| pristine end-to-end | `--root <lane> --rev f15998… --pkg <REA> --work <scratch>/run-work --json-out receipt-live-pristine.json` | 0 | `met_target true, carriers_matched 3`, 64.8 s; ratios 0.0599 / 0.101 / 0.6522; libz `shared-object` |
| MB18 end-to-end | same, mutant binary | 0 | `met_target true`; **ratios 0.0 / 0.0 / 0.0**; 66.8 s |
| frozen checker on MB18 receipt | `pristine-packed-elf.py --check-receipt receipt-live-MB18.json` | 0 | `met true`, `failing []` |
| 20 × selftest | one per mutant | 0 except MB11 | MB11 fails case `sections-none` |
| 20 × 11 receipts | one per mutant | as tabled | 6 mutants flip a receipt exit code (MB05, MB06, MB14, MB15, MB16, MB17) |
| 20 × 3 preflight probes | A1, A2, combined node+work | as tabled | MB19 breaks A2 (rc 1, traceback); MB08/MB09 move only the combined probe's reported class |
| (1) C1 anchor r69 | `mutation-check.py --tool tools/round-69/packed-elf.py --patch-set r69 --rev f15998…` | 0 | `survivors []`, pristine.cases 20, kills name their arm-false cases |
| (2) C1 anchor r68 | `mutation-check.py --tool tools/round-68/packed-elf.py --patch-set r68 --rev d7d9a62…` | 0 | `survivors [M1_identity, M2_recovery, M3_detected, M4_before, M5_control]`, pristine.cases 13, tool sha `48ef4c68…` |

(1) and (2) are an anchor for this seat, not a claim verification: they reproduce both
halves of the frozen C1 predicate on this clock **[observation]**. The C2 and C3 after-arms
belong to the L1 and were not run here.

## Baseline (observation)

`--check-receipt` on the scratch pristine copy (`rc`, `failing`):

| receipt | rc | failing |
|---|---|---|
| `pass` (= `c3-synthetic-met` shape) | 0 | `[]` |
| `loose` (= `c3-loose-ceiling` shape) | 1 | `libz: before_ceiling_ratio 0.9 > 0.75` |
| `r68` (= `c3-do-nothing`) | 1 | `target 2 != 3`, `carriers_matched 2 != 3`, `no shared-object carrier: kinds [None]`, two ratio lines |
| `exec3` (three executables) | 1 | `no shared-object carrier: kinds ['executable']` |
| `metfalse` | 1 | `met_target not true` |
| `nofail` (no `failing` key) | 1 | `failing not empty: None` |
| `nocounts` | 1 | `libz: counts absent` |
| `nullarm` (one arm `null`) | 1 | `jq:identity_ok false` |
| `ids` (carriers renamed) | **0** | `[]` |
| `dupe` (jq duplicated, still `carriers_matched 3`) | **0** | `[]` |
| `ratio_liar` (libz ratio 0.0001, ceiling 120 / orig 184) | **0** | `[]` |

## Detector map (what "frozen" means here)

1. `--selftest`: 20 registered cases, including `arm-pack-*` false-model cases.
2. `--check-receipt` over the three receipts the frozen controls drive: `c3-synthetic-met`,
   `c3-loose-ceiling`, `c3-do-nothing` (the round-68 landing receipt).
3. Contract arms A1–A6, of which this seat replicated A1/A2 shapes (the probe reads the
   instrument from `git show`, so the exact driver was replicated by invocation, not by
   `--root` fixture).

## Killed (3)

- `MB05_receipt_ratio_bound` (`ratio > 0.75` → `ratio > 1.0`): fires on `loose`; the frozen
  control `c3-loose-ceiling` would fail. **[observation]**
- `MB11_section_branch_return` (`return 0` → `return 1` in the no-sections branch): selftest
  case `sections-none` fails, rc 1. **[observation]**
- `MB19_check_work_false` (`check_work=not skip_run` → `check_work=False`): the unwritable
  `--work` root escapes as `PermissionError` with rc 1 and no `unevaluable` payload, so
  `A2_work_unusable` fails exactly as the round-68 base receipt records it. **[observation]**

## Survivors — exact false claim admitted (full detail in `mutants.md`)

Predicate-relevant:

- `MB15_receipt_failing_truthiness` (`failing != []` → truthiness): a receipt with **no**
  `failing` key satisfies the predicate's `failing []` clause. Absent is scored as empty.
- `MB18_ratio_constant` (score() ratio → `round(0.0, 4)`): every carrier records 0.0, so
  "`before_ceiling_ratio` at or below 0.75" is satisfied by a constant while the receipt's
  own `before_ceiling`/`orig_procedures` say 0.0599 / 0.101 / 0.6522.
- `MB06_receipt_shared_object` (`"shared-object" not in kinds` → `"executable"`): a receipt
  whose carrier set has no shared object is scored met. Live only if the instrument's carrier
  set ever regresses; the frozen C3 measurement itself is unaffected because its receipt does
  carry libz.

Receipt honesty (predicate-neutral, still unenforced):

- `MB14_receipt_met_target`: a receipt that self-declares `met_target: false` is scored met.
- `MB16_receipt_counts`: a carrier with no inventory counts is accepted as evidence.
- `MB17_receipt_arm_value` (`value is not True` → `value is False`): a `null` arm is accepted
  as true. The same hole exists in contract-probe A5 (`any(v is False …)`); executed on a
  live-shaped receipt with one `null` arm, A5 reports `ok true`, `failures []` **[observation]**,
  while the frozen `check_receipt` rejects it.

Arm floors:

- `MB12_refusal_code_floor` (`> 200` → `> 0`): a 1..200-byte decompilation with the symbol
  present counts as recovered code.
- `MB13_refusal_unpacked_rc` (drop `unpacked_rc == 0`): a refusal whose unpacked decompile
  failed still counts as recovered code.

Preflight order:

- `MB08_preflight_order` (work block before the tool loop) and `MB09_preflight_tool_order`
  (`node` after `git`): with **two** defects present the typed refusal names a different
  prerequisite; no frozen arm composes two defects, so both survive. Both still exit 2 — no
  false pass, only a moved class name.

Latent / conditional / equivalent:

- `MB02_fold_empty_control`: `fold([], 0)` → `control_ok true, met_target true`.
- `MB03_fold_missing_control_arm`: a carrier record with no `control_ok` folds to met; the
  pristine helper raises `KeyError` on the same input (observed by direct call).
- `MB04_fold_matched_ge`: `carriers_matched 4` against `target 3` is met.
- `MB07_elf_format_len`: a 3-of-4 `readelf -h` parse is recorded as a complete format;
  identical on healthy headers.
- `MB01_control_default`: an unused default flipped to `False` — over-strict, no false pass.
- `MB10_section_branch_sentinel` and `MB20_version_fallback`: equivalent on real inputs; the
  sentinel branch is redundant with the regex count (a real `readelf -SW` text carrying the
  sentinel has no bracket rows; only a synthetic text with both shows a difference: pristine
  0, mutant 1), and the version fallback is dominated by the sha256 pin (a silent-version
  packer is still refused on sha256 — observed).

## Cross-cutting observations on the frozen counter (pristine, not mutants)

- The frozen checker validates shape, not identity: renamed carriers (`ids`) and a duplicated
  `jq` (`dupe`) both score `met true` **[observation]**. R69-C3's "(libz)" attribution
  therefore rests on the instrument's `CARRIERS`, not on the checker.
- The 0.75 clause is not re-derived: `ratio_liar` (0.0001 vs 0.6522) scores `met true`
  **[observation]**. Atom A8 says the relation is "the counter's check, never re-derived from
  the data"; the implementation matches that declaration, so this is a declared boundary, not
  a defect of the frozen claim. `MB18` is the instrument-side version of the same boundary.
- A null per-carrier arm is invisible to A5 and visible to `check_receipt`; the two
  instruments do not share the clause's strength **[observation]**.

## What this does and does not say about the three claims

- Nothing here edits, replaces or re-freezes an instrument. The three predicates are judged on
  the frozen bytes, and the frozen bytes are intact.
- The mutants measure **detector sensitivity**, not the truth of this round's measurement. A
  surviving mutant says: if the route acquired this defect, the frozen counter would not
  notice. It does not say the route currently has the defect.
- The one claim-adjacent executed check is the C1 anchor in the run table (both halves
  reproduced) and the pristine end-to-end run reproducing A8's numbers; both are consistent
  with the frozen text **[observation]**. C2's six arms and C3's landing receipt are the L1's
  measurements and were not re-run by this seat.

## Unknowns

- [unknown] `MB07`'s effect if `readelf -h` ever degrades: not exercised end-to-end; A5 would
  compare the probe's `None` against a partial dict and reject it [inference from source].
- [unknown] `MB03`'s `KeyError` path is unreachable from `score()` today (the route always
  supplies the arm); only the direct call was observed.
- [unknown] whether the L1's landing receipt reproduces the same values on its own run; this
  seat's pristine run is a scratch-copy measurement, not the landing receipt.

## Tooling

- No tool was installed or upgraded. No pacman transaction, no `npx`, no `uv`.
- REA was only invoked through the frozen instrument's own `node …/scripts/rea.mjs` calls.
- No `git`/`jj` mutation anywhere; the only git use was the read-only `git log`/`git show`
  inside the frozen instruments plus `sha256sum`/`rev-parse` style reads by hand.

## Evidence index (relative to the lane root)

- `.ufo/waves/round-69/w1/MutBattery/mutants.md` — the table, patches, detector firings,
  per-survivor false claim and cheap kill route, survivors named for the next freeze.
- `MutBattery/results.json` — all 20 mutant rows (patch, shas, selftest, 11 receipt exits,
  3 preflight probes, deviations, match counts), baseline tables, restoration hashes.
- `MutBattery/pure-probe.json` — direct helper calls the selftest omits.
- `MutBattery/preflight-variants.json` — `MB09` (no node, no git → `missing_tool: git`) and
  `MB20` (silent-version packer → refused on sha256).
- `MutBattery/frozen-five-r69.json`, `MutBattery/frozen-five-r68-base.json` — the C1 anchor.
- `MutBattery/receipt-live-pristine.json`, `MutBattery/receipt-live-MB18.json` — the two
  end-to-end receipts (same work root, 65–67 s each).
- `MutBattery/receipts/` — the ten synthetic receipts plus `receipt-nullarm-live.json`.
- `MutBattery/{mutate,gen_md,probe_pure,probe_preflight,add_r68}.py` — the drivers.

## Restoration evidence

- `sha256sum tools/round-69/packed-elf.py` before the seat: `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`
- after the seat: the same value (the driver re-hashed the lane file at the end of the run and
  the wave-copy staging re-checked it).
- The scratch pristine copy was rewritten from the frozen bytes and re-hashed to the same
  value (`matches_frozen: true` in the driver's restoration phase).
- `/fast/scratch/hyaku/kaidoku-r69/MutBattery/` was deleted after the receipts were copied
  into this wave directory.
