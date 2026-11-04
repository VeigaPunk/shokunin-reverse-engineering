# ExecControls — scoped findings (round 68, w1)

Role: leaf executor. Assignment: score two more shortcut controls the round did not commit,
re-derive the six committed arms, confirm both selftests and their case inventories, and state
each new arm's false-green value. No lane file, fleet file, index, or external substrate was
modified; nothing was committed or pushed.

- Base pin: `fcbe200f6739c38939e0dabf3f251de2cc6bd727`. Freeze: `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.
- Worktree HEAD observed: `6ffa9ce1119ec01c953494d8f5b28e419efad646`. Python 3.14.8, `-I -B` everywhere.
  No installs, no pacman, no REA/upx process.
- Full detail: `.ufo/waves/round-68/w1/ExecControls/report.md`.

## Frozen-input identity (observation)

`registry-conformance.py` `a300d831…c6e8315`, `packed-elf.py` `48ef4c68…e5276e`,
`controls.py` `0657ee08…618fb4` — all three re-hashed and matching their pins.

## Selftests (observation)

| instrument | cases | failed | ok | rc | executed names == REGISTERED_CASES |
|---|---|---|---|---|---|
| registry-conformance | 11 | `[]` | **true** | 0 | **true** (11/11, in order) |
| packed-elf | 13 | `[]` | **true** | 0 | **true** (13/13, in order) |

Executed names were read from the selftest frame's own `cases` local on its return event, so
this is the runtime inventory, not a source re-reading. Receipt: `case-inventory.json`.

## Six committed arms, re-derived (observation)

`controls.py --json-out …/controls-rerun.json` → rc 0, 6 arms, 6 green, `ok: true`. Compared
field for field with `.ufo/waves/round-68/l1/pre/controls-at-base.json`: `differences: []`,
arm order equal, per-id equality true for all six, both payloads 6/6 green and `ok: true`.
Because the driver reads census inputs from git at the base pin, the uncommitted worktree
`SKILL.md` edit could not move these values.

| arm | observed | ok |
|---|---|---|
| `c1-base` | mismatches 2; `unregistered` = r67 pair exactly; scope 69; rows 73 | true |
| `c1-shortcut-self` | mismatches 0; scope 72 | true |
| `c1-constant-zero` | mismatches 0 | true |
| `c2-packed-only` | matched 0/2, control_ok true, met false | true |
| `c2-no-identity` | matched 0/2, control_ok true, met false | true |
| `c2-real` | matched 2/2, control_ok true, met true | true |

## New arms (observation)

| arm | kind | expected | observed | ok |
|---|---|---|---|---|
| A `A-registry-junk-fixture` | shortcut: table pollution | 2 mismatches, exactly one `row_absent` + one `thin` | baseline clean (0, scope 69, rows 75); junk census **2** = `row_absent [tools/round-68/never-built.py]` + `thin [tools/round-40/c1-counter.py]`; identical from the on-disk fixture; `unregistered`/`duplicate_rows` empty | **true** |
| B `B-packed-inventory-equals-original` | shortcut: detection from a packed count | met false | B1 packed counts == original → `before_ok` false both carriers, matched 0/2, met **false**; B2 packed inventory absent → same | **true** |
| C `C-all-false` | degenerate | met false | all arms false → matched 0/2, met false; all-true with `control_ok` false → met false; 1 carrier of target 2 → met false | **true** |

### False-green values and why the committed counter cannot emit them

- **A** — a counter summing only `unregistered` + `duplicate_rows` scores **0** on the junk
  table (false green), while the committed `census()` scores 2. The committed `mismatches` is
  the sum of four independent lists; `row_absent` diffs every row against the `git ls-tree`
  blob set and `thin` runs the three `VERDICT_RE` bullets over the row's own verdict cell, so
  neither consults plan scope and each planted defect adds 1. Note (observed): the
  table-with-itself shortcut scores 2 on this fixture — its false green is confined to
  omission, which `c1-shortcut-self` already controls at base (0 vs truth 2).
- **B** — scoring `before_ok` as "a packed inventory exists" and reusing the original's
  sha/counts gives all-true arms and a fold of **met true / matched 2** (false green). The
  committed counter cannot: `before_ok` is `packed procedure_count < min_orig_procedures//2`
  (50/25; packed-equals-original is 167/99), `identity_ok` needs `sha256(unpacked)` equal to
  the pin while `upx -d` refuses a non-packed original (control rcs 2/2), `recovery_ok` needs
  a fresh analyze of that unpacked file to equal `orig_counts`, and `control_ok` requires both
  packer refusals.
- **C** — counting carriers instead of `all(arms.values())`, or dropping `control_ok`, greens
  both cases; the committed `ok` and `met_target` expressions make both impossible.

## Residual risks (labelled)

- **Observation:** the census accepts a full-verdict row for an existing out-of-scope tool
  (`tools/round-40/sqfs-list.py` → mismatches 0). A fabricated row naming a real out-of-scope
  path would pass. Consistent with the registry cataloguing beyond plan scope; recorded for
  the attack seats, not asserted as a claim failure.
- **Inference:** arm B re-folds the committed base dry-run receipt; the numeric floors and
  packer rcs are the L1's measurements, not re-measured here (no REA/upx spawned by this seat).
- **Unknown:** the measured-revision after-arm (`scope_size 71`, `registry_rows 77`) — the
  L1's to run, deliberately not duplicated.

## Files written (all under this seat's wave dir)

`.ufo/waves/round-68/w1/ExecControls/`: `report.md`, `controls-rerun.json`,
`controls-compare.json`, `case-inventory.json`, `new-arms.json`, `fixture-planted-rows.json`,
`drivers/{case_inventory,compare_controls,new_arms}.py`.

Receipt hashes (sha256):
`controls-rerun.json` `c89b7f29…b7481ed`, `controls-compare.json` `392aa7a1…294fdc0f`,
`case-inventory.json` `7afdb031…910a6609`, `new-arms.json` `8f93ab5b…d9c78ac5`,
`fixture-planted-rows.json` `2b903740…08155ce8`.

Scratch `/fast/scratch/hyaku/kaidoku-r68/ExecControls/` was removed before yield.

## Blockers

None.
