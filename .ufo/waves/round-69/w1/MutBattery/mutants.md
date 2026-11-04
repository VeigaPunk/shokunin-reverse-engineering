# Round 69 / w1 / MutBattery — new mutants of `tools/round-69/packed-elf.py`

Seat: mutation-tester (MutBattery). Target: `tools/round-69/packed-elf.py` at the frozen
bytes `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` (operative freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`).
**The frozen file was never edited**: every patch was applied to a copy under
`/fast/scratch/hyaku/kaidoku-r69/MutBattery/`; the lane file re-hashed to the same
sha256 after the run (restoration evidence at the end).

## Baseline (pristine copy, before any patch)

- `--selftest`: rc 0, cases 20, failed [].
- `--check-receipt` on the frozen control fixtures and on the extended receipts:

| receipt | pristine rc | pristine failing |
|---|---|---|
| `dupe` | 0 | `[]` |
| `exec3` | 1 | `["no shared-object carrier: kinds ['executable']"]` |
| `ids` | 0 | `[]` |
| `loose` | 1 | `["libz: before_ceiling_ratio 0.9 > 0.75"]` |
| `metfalse` | 1 | `["met_target not true"]` |
| `nocounts` | 1 | `["libz: counts absent"]` |
| `nofail` | 1 | `["failing not empty: None"]` |
| `nullarm` | 1 | `["jq:identity_ok false"]` |
| `pass` | 0 | `[]` |
| `r68` | 1 | `["target 2 != 3", "carriers_matched 2 != 3", "no shared-object carrier: kinds [None]", "jq: before_ceiling_ratio None > 0.75", "xxd: before_ceiling_ratio None > 0.75"]` |
| `ratio_liar` | 0 | `[]` |

| preflight probe | pristine rc | unevaluable |
|---|---|---|
| `A1_missing_node` | 2 | `missing_tool: node` |
| `A2_work_unusable` | 2 | `work_unusable: not writable (/fast/scratch/hyaku/kaidoku-r69/MutBattery/ro: PermissionError)` |
| `combined_node_and_work` | 2 | `missing_tool: node` |

End-to-end pristine measurement of the scratch copy (65 s, REA 6.5.0, upx 5.2.0):
`met_target true, carriers_matched 3, control_ok true, failing []`, ratios
`0.0599 / 0.101 / 0.6522` (jq / xxd / libz), libz `shared-object` — identical to atom A8.
`--check-receipt` on that receipt: `met true`, `failing []`.

Anchor: the frozen five at the same revision (`mutation-check.py --patch-set r69`,
work re-run this seat) give `survivors []`, pristine.cases 20, kills naming [['arm-pack-identity-false'], ['arm-pack-recovery-false'], ['arm-pack-detected-false'], ['arm-pack-before-false'], ['arm-pack-control-false']]. The frozen battery is live at this revision.

## Mutants (20, all new; none of the five frozen sites is re-used)

Legend: **frozen** = does a frozen detector fire? The frozen set is the 20-case
`--selftest`, the three receipts the controls already drive (`c3-synthetic-met` = `pass`,
`c3-loose-ceiling` = `loose`, `c3-do-nothing` = the round-68 landing receipt = `r68`), and
contract arms A1/A2. **ext** = which of this seat's ten extra receipts fire. **arms** = the
preflight observation that moved, if any.

| # | mutant | site | patch | selftest | frozen | ext | arms | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `MB01_control_default` | carrier_arms default control_ok | control_ok: bool = True -> = False (default) | green | no | no | - | **SURVIVED** |
| 2 | `MB02_fold_empty_control` | fold empty-set control | drop bool(carriers) and from the fold's control_ok | green | no | no | - | **SURVIVED** |
| 3 | `MB03_fold_missing_control_arm` | fold absent control arm | arms["control_ok"] -> arms.get("control_ok", True) | green | no | no | - | **SURVIVED** |
| 4 | `MB04_fold_matched_ge` | fold matched == target | matched == target -> matched >= target | green | no | no | - | **SURVIVED** |
| 5 | `MB05_receipt_ratio_bound` | check_receipt ratio bound | ratio > 0.75 -> ratio > 1.0 | green | FIRES on loose | loose | - | **KILLED** |
| 6 | `MB06_receipt_shared_object` | check_receipt shared-object clause | "shared-object" not in kinds -> "executable" not in kinds | green | no | exec3 | - | **SURVIVED** |
| 7 | `MB07_elf_format_len` | elf_format completeness | len(found) == 4 -> len(found) >= 3 | green | no | no | - | **SURVIVED** |
| 8 | `MB08_preflight_order` | preflight node/before-work order | work-root block moved ahead of the node/git/readelf, upx and rea checks | green | no | no | combined_node_and_work -> 'work_unusable: not writable (/fast/scratch/hyaku/kaidoku-r69/MutBattery/ro: PermissionError)' | **SURVIVED** |
| 9 | `MB09_preflight_tool_order` | preflight tool tuple order | tool tuple (node, git, readelf) -> (git, node, readelf) | green | no | no | - | **SURVIVED** |
| 10 | `MB10_section_branch_sentinel` | section_count no-sections sentinel | sentinel string There are no sections in this file -> There are no section headers ... | green | no | no | - | **SURVIVED** |
| 11 | `MB11_section_branch_return` | section_count no-sections return | no-sections branch return 0 -> return 1 | FAILED ['sections-none'] | FIRES: selftest ['sections-none'] | - | - | **KILLED** |
| 12 | `MB12_refusal_code_floor` | refusal 200-byte floor | refusal_code_bytes > 200 -> > 0 | green | no | no | - | **SURVIVED** |
| 13 | `MB13_refusal_unpacked_rc` | refusal unpacked_rc clause | drop refusal_unpacked_rc == 0 from refusal_ok | green | no | no | - | **SURVIVED** |
| 14 | `MB14_receipt_met_target` | check_receipt met_target clause | delete the met_target is not True clause | green | no | metfalse | - | **SURVIVED** |
| 15 | `MB15_receipt_failing_truthiness` | check_receipt failing == [] | failing != [] -> failing (truthiness) | green | no | nofail | - | **SURVIVED** |
| 16 | `MB16_receipt_counts` | check_receipt counts presence | counts absent failure -> pass | green | no | nocounts | - | **SURVIVED** |
| 17 | `MB17_receipt_arm_value` | check_receipt arm value identity | value is not True -> value is False | green | no | nullarm | - | **SURVIVED** |
| 18 | `MB18_ratio_constant` | score() ratio derivation | ratio expression -> round(0.0, 4) | green | no | no | - | **SURVIVED** |
| 19 | `MB19_check_work_false` | preflight work gate | check_work=not skip_run -> check_work=False | green | FIRES on A2 | no | A2_work_unusable -> None | **KILLED** |
| 20 | `MB20_version_fallback` | preflight version pin fallback | empty version -> UPX_VERSION_PIN | green | no | no | - | **SURVIVED** |

Killed by the frozen detector set: **3 of 20** (`MB05_receipt_ratio_bound`, `MB11_section_branch_return`, `MB19_check_work_false`).
Survivors: **17 of 20**; 15 of them are behaviour-bearing under some
input the frozen detectors never feed (the rest are equivalent or over-strict).

## Survivors — the exact false claim each admits, and a cheap kill route

### `MB01_control_default` — over-strict

- Site: carrier_arms default control_ok.
- False claim admitted: none reachable: no caller omits `control_ok`; a caller that did would mark a green carrier false (false alarm, not a false pass).
- Route (do not edit the frozen instrument; add for the next freeze): selftest case calling `carrier_arms(True, True, True, True, None)` (5 args, default exercised) and asserting `control_ok` true.

### `MB02_fold_empty_control` — latent

- Site: fold empty-set control.
- False claim admitted: `fold([], 0)` -> control_ok true and met_target true: a composite verdict with no carrier at all; unreachable while target is `len(CARRIERS)` = 3.
- Route (do not edit the frozen instrument; add for the next freeze): selftest case `fold([], 0)['control_ok'] is False and fold([], 0)['met_target'] is False`.

### `MB03_fold_missing_control_arm` — latent

- Site: fold absent control arm.
- False claim admitted: a carrier record with no `control_ok` arm folds to met_target true (pristine raises KeyError: the missing arm currently crashes rather than rejects).
- Route (do not edit the frozen instrument; add for the next freeze): harden fold to `c['arms'].get('control_ok') is not True` (also closes the KeyError crash) and add case `fold-missing-control-arm`.

### `MB04_fold_matched_ge` — latent

- Site: fold matched == target.
- False claim admitted: `carriers_matched` above target counts as met (4 ok carriers, target 3 -> met true); unreachable with three carriers, but it would let a duplicated 4th carrier pass the composite verdict.
- Route (do not edit the frozen instrument; add for the next freeze): selftest case `fold([ok_model] * 4, 3)['met_target'] is False`.

### `MB06_receipt_shared_object` — behaviour-bearing

- Site: check_receipt shared-object clause.
- False claim admitted: a receipt whose carrier set has no `shared-object` kind would be scored met: C3's shared-object clause is enforced by this one predicate.
- Route (do not edit the frozen instrument; add for the next freeze): extract the kinds clause into `receipt_kinds_ok(kinds)` and add case `receipt-no-shared-object` (kinds `['executable']` -> false), or add a control arm `c3-no-shared-object`.

### `MB07_elf_format_len` — conditional

- Site: elf_format completeness.
- False claim admitted: a 3-of-4 `readelf -h` parse is recorded as a complete format; identical on healthy headers (4-of-4), and A5 would reject the mismatch if it ever occurred.
- Route (do not edit the frozen instrument; add for the next freeze): selftest case `elf_format(three_field_header) is None`.

### `MB08_preflight_order` — contract-order

- Site: preflight node/before-work order.
- False claim admitted: with a missing `node` AND an unwritable `--work`, the refusal names work_unusable instead of missing_tool: node (both exit 2, only the class name moves).
- Route (do not edit the frozen instrument; add for the next freeze): contract-probe arm A7: PATH without node AND a 0500 --work root, asserting the refusal names `node` (and a second A8 for PATH without node and git).

### `MB09_preflight_tool_order` — contract-order

- Site: preflight tool tuple order.
- False claim admitted: with both `node` and `git` absent, the refusal names git instead of node; A1 removes only node, so the arm is blind.
- Route (do not edit the frozen instrument; add for the next freeze): same A7/A8 composition: PATH with neither node nor git must still name node.

### `MB10_section_branch_sentinel` — equivalent

- Site: section_count no-sections sentinel.
- False claim admitted: none on real readelf output: any `readelf -SW` text carrying the sentinel has no bracket rows, so the regex count is 0 as well (sentinel-only observed 0 == 0); a synthetic sentinel-plus-row text differs (pristine 0, mutant 1).
- Route (do not edit the frozen instrument; add for the next freeze): not needed for correctness (equivalent); to pin the branch, case `section_count(sentinel + one section row) == 0`.

### `MB12_refusal_code_floor` — behaviour-bearing

- Site: refusal 200-byte floor.
- False claim admitted: a refusal that returns a 1..200-byte decompilation with the symbol present is scored as recovered code; the 200-byte floor is not enforced.
- Route (do not edit the frozen instrument; add for the next freeze): selftest model `address=0x1000, refusal_packed_rc=1, refusal_unpacked_rc=0, symbol_present=True, refusal_code_bytes=50` -> `refusal_ok` false.

### `MB13_refusal_unpacked_rc` — behaviour-bearing

- Site: refusal unpacked_rc clause.
- False claim admitted: a refusal whose unpacked decompile FAILED (rc != 0) but left symbol bytes is scored as recovered code.
- Route (do not edit the frozen instrument; add for the next freeze): selftest model with `refusal_unpacked_rc=7`, symbol present, 400 bytes -> `refusal_ok` false.

### `MB14_receipt_met_target` — receipt-honesty

- Site: check_receipt met_target clause.
- False claim admitted: a receipt that self-declares `met_target: false` while every other field is green is scored met; the predicate does not name receipt.met_target, but the checker stops noticing an inconsistent receipt.
- Route (do not edit the frozen instrument; add for the next freeze): add a control arm with a synthetic receipt carrying `met_target: false` (expect exit 1).

### `MB15_receipt_failing_truthiness` — predicate-relevant

- Site: check_receipt failing == [].
- False claim admitted: a receipt with NO `failing` key (None) satisfies the predicate's `failing []` clause: absent is scored as empty.
- Route (do not edit the frozen instrument; add for the next freeze): add a control arm with a synthetic receipt carrying no `failing` key (expect exit 1).

### `MB16_receipt_counts` — receipt-honesty

- Site: check_receipt counts presence.
- False claim admitted: a carrier with no `orig_counts`/`packed_counts` is accepted as inventory evidence.
- Route (do not edit the frozen instrument; add for the next freeze): add a control arm with a synthetic receipt whose carrier has no counts (expect exit 1).

### `MB17_receipt_arm_value` — receipt-honesty

- Site: check_receipt arm value identity.
- False claim admitted: an arm whose value is `null` is accepted as true; note contract-probe A5 shares the hole (`any(v is False)`), so the null arm is invisible to both instruments.
- Route (do not edit the frozen instrument; add for the next freeze): add a control arm with a synthetic receipt whose arm is null (expect exit 1); fix A5 to `value is not True`.

### `MB18_ratio_constant` — predicate-relevant

- Site: score() ratio derivation.
- False claim admitted: every carrier records `before_ceiling_ratio` 0.0 regardless of ceiling/original, so the predicate's 0.75 clause is satisfied by a constant; the receipt still carries ceiling and orig_procedures, so the relation is recomputable but never re-derived.
- Route (do not edit the frozen instrument; add for the next freeze): extract `ceiling_ratio(ceiling, orig)` and add selftest cases (10/167 -> 0.0599, 10/99 -> 0.101, 120/184 -> 0.6522); have check_receipt recompute the ratio from `before_ceiling`/`orig_counts` instead of trusting the record.

### `MB20_version_fallback` — equivalent

- Site: preflight version pin fallback.
- False claim admitted: a packer whose `--version` prints nothing gets the pin substituted for the version string; the sha256 pin still refuses it (observed), so no false pass is reachable.
- Route (do not edit the frozen instrument; add for the next freeze): not needed (equivalent under the sha256 pin); optionally a pure `version_pin(version)` case.

## Receipts (all paths relative to the lane root)

- `.ufo/waves/round-69/w1/MutBattery/results.json` — every mutant row, all rc/failing values,
  the baseline table, receipt paths, restoration hashes.
- `.ufo/waves/round-69/w1/MutBattery/pure-probe.json` — direct calls to the pure helpers with
  the inputs the selftest omits (fold empty/over-target/missing-arm, elf_format 3-of-4,
  section sentinel+rows, refusal short code, refusal failed unpacked rc).
- `.ufo/waves/round-69/w1/MutBattery/preflight-variants.json` — tool-tuple order and silent
  packer version observations (pristine / MB09 / MB20).
- `.ufo/waves/round-69/w1/MutBattery/frozen-five-r69.json` — anchor run of the frozen five.
- `.ufo/waves/round-69/w1/MutBattery/receipt-live-pristine.json` and
  `receipt-live-MB18.json` — the two end-to-end receipts (pristine vs the ratio-constant
  mutant), same work dir, 65 s each.
- `.ufo/waves/round-69/w1/MutBattery/receipts/` — the ten synthetic receipts plus
  `receipt-nullarm-live.json` (a live-shaped receipt with one `null` arm, used for the A5
  blind-spot observation).
- `.ufo/waves/round-69/w1/MutBattery/mutate.py` — the driver that produced all of it.

### Pristine-vs-mutant observations worth carrying

- The frozen checker accepts a receipt whose carriers are renamed (`carrier-0..2`), a receipt
  that duplicates `jq` and still reports `carriers_matched 3`, and a receipt whose libz
  `before_ceiling_ratio` is `0.0001` while the same receipt says ceiling 120 / 184
  procedures. All three are pristine behaviour (rc 0) observed this seat, not mutants:
  the checker validates shape, not carrier identity and not the ratio derivation.
- MB18's end-to-end receipt records `before_ceiling_ratio 0.0` for all three carriers while
  `before_ceiling`/`orig_procedures` still say 10/167, 10/99, 120/184, and the frozen
  checker scores it `met true`. The 0.75 clause is inferred from a self-reported number.
- contract-probe A5 uses `any(v is False for v in arms.values())`: a `null` arm is not
  `False`, so A5 is blind to a null arm exactly as MB17 makes check_receipt blind.

## Restoration evidence

- frozen file sha256 before: `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`
- frozen file sha256 after:  `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` (re-hashed at the end of the run)
- the scratch pristine copy was rewritten from the frozen bytes and re-hashed to the same
  value (`matches_frozen: true`, recorded in the driver's restoration phase)
- scratch dir `/fast/scratch/hyaku/kaidoku-r69/MutBattery/` deleted after the receipts were
  copied into this wave directory.

## Survivors named for the next freeze

- `MB01_control_default` (over-strict): none reachable: no caller omits `control_ok`.
- `MB02_fold_empty_control` (latent): `fold([], 0)` -> control_ok true and met_target true: a composite verdict with no carrier at all.
- `MB03_fold_missing_control_arm` (latent): a carrier record with no `control_ok` arm folds to met_target true (pristine raises KeyError: the missing arm currently crashes rather than rejects).
- `MB04_fold_matched_ge` (latent): `carriers_matched` above target counts as met (4 ok carriers, target 3 -> met true).
- `MB06_receipt_shared_object` (behaviour-bearing): a receipt whose carrier set has no `shared-object` kind would be scored met: C3's shared-object clause is enforced by this one predicate.
- `MB07_elf_format_len` (conditional): a 3-of-4 `readelf -h` parse is recorded as a complete format.
- `MB08_preflight_order` (contract-order): with a missing `node` AND an unwritable `--work`, the refusal names work_unusable instead of missing_tool: node (both exit 2, only the class name moves).
- `MB09_preflight_tool_order` (contract-order): with both `node` and `git` absent, the refusal names git instead of node.
- `MB12_refusal_code_floor` (behaviour-bearing): a refusal that returns a 1..200-byte decompilation with the symbol present is scored as recovered code.
- `MB13_refusal_unpacked_rc` (behaviour-bearing): a refusal whose unpacked decompile FAILED (rc != 0) but left symbol bytes is scored as recovered code.
- `MB14_receipt_met_target` (receipt-honesty): a receipt that self-declares `met_target: false` while every other field is green is scored met.
- `MB15_receipt_failing_truthiness` (predicate-relevant): a receipt with NO `failing` key (None) satisfies the predicate's `failing []` clause: absent is scored as empty.
- `MB16_receipt_counts` (receipt-honesty): a carrier with no `orig_counts`/`packed_counts` is accepted as inventory evidence.
- `MB17_receipt_arm_value` (receipt-honesty): an arm whose value is `null` is accepted as true.
- `MB18_ratio_constant` (predicate-relevant): every carrier records `before_ceiling_ratio` 0.0 regardless of ceiling/original, so the predicate's 0.75 clause is satisfied by a constant.

