# ExecControls — round 68, w1: extra controls and re-derivation

- Seat: ExecControls (leaf). Scope: re-derive the six committed controls, score three new
  controls (two shortcut controls A/B plus degenerate control C), and state the false-green
  value each blocks. No claim was judged; no after-arm was run; no lane file was edited.
- Base pin used by every re-derivation: `fcbe200f6739c38939e0dabf3f251de2cc6bd727`.
  Operative freeze: `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.
- Worktree HEAD observed at run time: `6ffa9ce1119ec01c953494d8f5b28e419efad646`
  (observation; the worktree also carried an uncommitted `SKILL.md` modification by
  another seat, which this seat did not read as claim input or touch).
- Runtime: Python 3.14.8, stdlib only, every invocation `python3 -I -B`. No tool was
  installed or upgraded, no pacman transaction ran, and this seat spawned no REA or upx
  process.

## 1. Frozen-input identity (observed)

| input | pinned sha256 | re-hashed |
|---|---|---|
| `tools/round-68/registry-conformance.py` | `a300d831…c6e8315` | match |
| `tools/round-68/packed-elf.py` | `48ef4c68…e5276e` | match |
| `tools/round-68/controls.py` | `0657ee08…618fb4` | match |

## 2. Selftests and case inventories (observed)

| instrument | cases | failed | ok | rc |
|---|---|---|---|---|
| `registry-conformance.py --selftest` | 11 | `[]` | `true` | 0 |
| `packed-elf.py --selftest` | 13 | `[]` | `true` | 0 |

Counts alone are not treated as an inventory. A trace hook captured the selftest frame's
own `cases` local on its return event, so the executed list is the runtime list in order:

| instrument | registered | executed | names equal | all case booleans true |
|---|---|---|---|---|
| registry-conformance | 11 | 11 | **true** | true |
| packed-elf | 13 | 13 | **true** | true |

First/last executed names: `clean` … `case-inventory` and `sections-none` … `case-inventory`.
Receipt: `case-inventory.json` (includes both printed selftest payloads).

## 3. The six committed arms, re-derived (observed)

`controls.py --json-out controls-rerun.json` → rc 0, `control_arms` 6, `green` 6, `ok` true.
Compared field for field against `.ufo/waves/round-68/l1/pre/controls-at-base.json`:
`differences: []`, arm order equal, per-id equality true for all six, both payloads
`ok: true` with 6/6 green. The driver reads the census inputs from git at the base pin, so
the uncommitted worktree edit could not move these numbers.

| arm | expected | observed | ok |
|---|---|---|---|
| `c1-base` | mismatches 2, names r67 pair | mismatches 2; `unregistered` = `tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`; scope 69; rows 73 | true |
| `c1-shortcut-self` | mismatches 0 | mismatches 0; scope 72 | true |
| `c1-constant-zero` | mismatches 0 | mismatches 0 | true |
| `c2-packed-only` | met false | matched 0/2, control_ok true, met false | true |
| `c2-no-identity` | met false | matched 0/2, control_ok true, met false | true |
| `c2-real` | met true, matched 2 | matched 2/2, control_ok true, met true | true |

## 4. New arms (observed)

Driver `drivers/new_arms.py` imports the committed modules and calls their own functions;
arm A additionally materialised the base-revision `SKILL.md` and `plans/*.md` into a scratch
tree, mutated the table there, and re-read the fixture from disk before censusing it.

### Arm A — registry junk fixture (shortcut control: table pollution)

Baseline fixture = base table (73 rows) + the two round-67 gap rows with full verdicts →
mismatches 0, scope 69, rows 75 (the fixture is clean before planting; it is not the claim's
repair). Junk fixture = baseline + one row for `tools/round-68/never-built.py` (a path that is
neither in plan scope nor in the tree) + one row for `tools/round-40/c1-counter.py` whose
verdict cell is `0=met` only.

| probe | observed |
|---|---|
| junk census, in memory | mismatches **2**; `row_absent` = `[tools/round-68/never-built.py]`; `thin` = `[tools/round-40/c1-counter.py]`; `unregistered` `[]`; `duplicate_rows` `[]` |
| junk census, fixture re-read from disk | mismatches **2**, same two names |
| sum of only `unregistered` + `duplicate_rows` | **0** ← false-green value |
| table-with-itself shortcut on the junk fixture | mismatches 2 (both planted defects are row-visible, so this shortcut catches them here) |
| full-verdict row for existing out-of-scope `tools/round-40/sqfs-list.py` | mismatches **0** (accepted silently) |

Arm verdict: **true** — the census's own `census()` flags exactly the two planted defects,
and only those. False-green value it blocks: **0** from a counter that summed only the
omission classes. The committed counter cannot produce 0 because `mismatches` is the literal
sum `len(unregistered) + len(duplicate_rows) + len(row_absent) + len(thin)`, where
`row_absent` diffs every table row against the `git ls-tree` blob set and `thin` runs the
three `VERDICT_RE` bullets over the row's own verdict cell — neither list consults the plan
scope, so fabricated and thin rows add 1 each even when no plan mentions them.

Caveats stated as observation, not defect: the fixture's `registry_rows 77` is an artefact of
73 + 2 baseline + 2 junk rows and is **not** the claim's measured-revision 77. The
out-of-scope probe shows the census deliberately validates existence and verdict grammar of
every row but not its relevance to plan scope; a fabricated row for an existing out-of-scope
path would not be caught. That is a residual surface for the attack seats, not a claim
failure (the claim's predicates are about scope coverage and the two named omissions).

### Arm B — packed inventory equals the original's (shortcut control)

Synthetic carriers were built from the committed base dry-run receipt
(`pre/c2-dryrun-at-base.json`, itself `met_target true`): per carrier, `before_ok` was
recomputed with the committed expression over a packed inventory set equal to the original's,
then `carrier_arms`/`fold` were called on the result.

| sub-case | observed | ok |
|---|---|---|
| B1 packed counts == original (`jq` 167/30/190, `xxd` 99/29/103) | `before_ok` false on both (floors 50 / 25); carriers matched **0**/2; met **false** | true |
| B2 packed inventory absent (`{}` → `counts_from` None) | `before_ok` false on both; matched **0**/2; met **false** | true |
| fabricated all-true carriers (the wrong counter) | matched 2/2, met **true** ← false-green value | — |

Arm verdict: **true**. False-green value it blocks: `met_target true`, `carriers_matched 2`.
The committed counter cannot produce it: `before_ok` is `packed procedure_count is not None
and < min_orig_procedures // 2` (50 for `jq`, 25 for `xxd`), and a packed count equal to the
original's is 167/99; `identity_ok` needs `sha256(unpacked) == the carrier pin` while `upx -d`
refuses a non-packed original (measured control `decompress_rc` 2/2 in the receipt), so no
unpacked file exists to hash; `recovery_ok` needs a fresh REA analyze of that file to equal
`orig_counts`; `control_ok` additionally requires `upx -l` and `-d` to fail on the original.

Scope note (observation): arm B re-folds numbers already recorded in the committed base
receipt. This seat ran no REA and no upx; the numeric floors and control rcs are the L1's
dry-run measurements, not re-measured here.

### Arm C — degenerate all-false control

| sub-case | observed | ok |
|---|---|---|
| every arm false, two carriers | carrier `ok` false; matched 0/2; met **false** | true |
| all arms true but `control_ok` false | matched 2/2; met **false** | true |
| one carrier true, target 2 | matched 1/2; met **false** | true |

Arm verdict: **true**. False-green value it blocks: `met_target true` for the first two cases.
The committed counter cannot produce them because each carrier's `ok = all(arms.values())`,
`fold` counts only `c["ok"]`, and `met_target = matched == target and bool(control_ok)`.

## 5. Conclusions

- **Observation:** both frozen selftests print `ok: true` at 11 and 13 cases, and their runtime
  executed names equal `REGISTERED_CASES` in order, not merely by count.
- **Observation:** the six committed arms re-derive byte-for-byte identically to the L1's pre
  receipt (zero field differences), including the base-leg truth `mismatches 2` naming exactly
  `tools/round-67/avm-le-counter.py` and `tools/round-67/mutation-battery.py`.
- **Observation:** the three new controls land where their declarations require, and each has
  a named false-green value that the committed expressions cannot emit.
- **Inference:** the two shortcut controls exercise the two shortcut surfaces the committed
  round did not cover — fabricated/thin registry rows (this round only controlled omission via
  `c1-shortcut-self`) and a packed count that equals the original's (this round only controlled
  arm-dropping via `c2-packed-only` / `c2-no-identity`). They are additive, not replacements.
- **Unknown:** whether the measured-revision after-arm reports `scope_size 71` /
  `registry_rows 77`; that is the L1's after-arm and was deliberately not duplicated here. The
  worktree `SKILL.md` was seen to carry 77 table rows, but that is a text count, not a census.

## 6. Receipt index (absolute paths, sha256)

All under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/ExecControls/`:

| file | sha256 |
|---|---|
| `controls-rerun.json` | `c89b7f298bdc65955ec1302047951e4f2c7e61a327713e33890a4d928b7481ed` |
| `controls-compare.json` | `392aa7a14c6c603b4aa90263bd2d1f6c4c2dec0c2036e7edf3d6678d294fdc0f` |
| `case-inventory.json` | `7afdb0314c9f92c6bc05ced61da0ed2bfe04da15d505bcd57bf425da910a6609` |
| `new-arms.json` | `8f93ab5bc621eb441c25db75ae1be656952cd695a7b863f684ac77ddd9c78ac5` |
| `fixture-planted-rows.json` | `2b9037402e2da5c1bedbda88dc2ad3256b5dd4b6e0c4c3a5690a0c5808155ce8` |
| `drivers/case_inventory.py` | `20ee72480b8c700e2410dece3a5ba020fcaae5a85a8c0c3e6dbefbd38a809ed0` |
| `drivers/compare_controls.py` | `2bbcba1a5c403bac35f11a854c93382e4e8730661ce82fe3689db89c4c9ea12a` |
| `drivers/new_arms.py` | `c0ef03ce0cbd43782a6b0126a12eab1a21f56b419357d034264b85496be743b4` |

## 7. Residual risks / blockers

- The census does not police the relevance of an existing out-of-scope row (arm A probe). A
  fabricated row naming a real, out-of-scope tool passes. Consistent with the registry
  cataloguing beyond plan scope; recorded for the attack seats.
- Arm B's evidence is a re-fold of committed receipt data, not a fresh pack/unpack run (seat
  scope). If the L1 wants a fresh numeric floor on the packed-count shortcut, that is an
  after-arm run, not this seat's.
- No blockers. No tooling changes. Scratch
  `/fast/scratch/hyaku/kaidoku-r68/ExecControls/` was removed before yield; the fixture's
  planted rows and its SKILL.md hash are preserved in `fixture-planted-rows.json`.
