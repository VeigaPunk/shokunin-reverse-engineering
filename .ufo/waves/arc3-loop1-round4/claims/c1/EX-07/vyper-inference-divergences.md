# Observation — Vyper-carrier inference divergences vs the compiled Vyper ABI (c1, round 4, seat EX-07)

Status: RESULT-class measurement, first-hand, 3 Vyper carriers (EX-02 `Smoke` K=4,
EX-04 `CarrierV` K=15, EX-03 `Steward` K=22) plus PL-1's `CarrierW` K=9 cross-check.
Selector recovery is K/K on all four; the divergences below are in the *inference
fields only* and are recorded, not repaired — no defect claim is made, and none of
them affects the recovered selector set.

## 1. Mutability: the probe reads `payable` where Vyper's ABI declares non-payable

On `CarrierV` (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/abi.json`), the
probe reports `inferred_state_mutability: "payable"` for functions the Vyper ABI
declares `nonpayable`, `view` or `pure` — 10 of 15 functions. The reported value
tracks the **body-entry shape**, not the ABI: where the entry byte after the
`JUMPI` selector test is `0x60` (a `PUSH1`-led body) the probe says `payable`; where
it is `0x34` (`CALLVALUE` — a non-payable guard) it says `view`/`nonpayable`
correctly. Measured on all 15 rows in `compare-legs.out` §4 and the per-row table
in this seat's `carrier-divergences.txt`.

Note this is *not* the pure/view collapse already recorded in r3 for solc carriers
(there, `pure` was reported as `view`). Here the whole `nonpayable`/`view`/`pure`
class collapses to `payable` on one side of the body-shape split. Both readings are
"consistent with an inference over dispatch structure", and neither is verified ABI
mutability — but the r3 entry's phrase "inferred ... mutability consistent with the
compiled ABI" should not be read as holding for Vyper carriers.

## 2. Argument types: `address` is inferred as `uint256`

`CarrierV`: `balances(address)`, `balance_of(address)`, `is_owner(address)` all
report `inferred_arguments: "uint256"` where the ABI declares `address` (3 of 15).
`Steward`: `approve(address,uint256)`, `transfer(address,uint256)`,
`transferFrom(address,address,uint256)`, `balanceOf(address)`,
`allowance(address,address)`, `mint(address,uint256)`, `set_steward(address)`,
`is_steward(address)` report `uint256` for every `address` slot (8 rows).
`CarrierW`: `seen(address)` → `uint256`; and `tag(string,bytes,uint256[2],bool)` →
`"bytes,bytes,uint256,uint256,uint256"` — the `string` and the fixed array are
flattened into `bytes`/`uint256` slots.

Control: on the **solc** carrier `VaultB.opt200` the same probe reports `address`
correctly (`0x27e235e3 address`, `0x3d96e276 address,uint256`, `0xcbf9fe5f address`).
So the collapse is Vyper-carrier-specific in this sample, not a general tool
behavior. Arity is preserved in every case (the argument *count* is right); only
the type word is wrong.

## 3. Not a defect — the record should say "typed divergence", not "wrong"

The tool's own limitation line (present in every envelope) states: "Recovered
selectors, argument strings and mutability are upstream inferences, not verified
ABI signatures or names." Under that declared scope, §1 and §2 are exactly the
class the limitation warns about, now measured with a second compiler family as
the counter-example. What *is* new information: the divergence direction and the
byte-level correlate (body shape for mutability; the Vyper ABI encoder's use of
plain 32-byte words for `address` for arguments), and the fact that a solc control
on the same host, same pin, same probe does not show it.

## Evidence

- `.ufo/waves/arc3-loop1-round4/claims/c1/EX-07/legs/V-{hex,raw}-{6.4.0,6.5.0,6.7.0}.json`
  (8 CarrierV legs), `X3-*` (6 Steward legs), `XW-*` (6 CarrierW legs),
  `S-*` (Smoke legs), plus `A-*`/`B-*`/`C-*` solc controls.
- `compare-legs.out` §1/§4; `carrier-divergences.txt` (per-row ABI-vs-probe table).
- ABI sources: `EX-04/out/abi.json` `c7902147…`, `EX-03/abi.json`, `PL-1/evidence/CarrierW.abi.json`,
  `EX-02/smoke/Smoke.abi.json`; my selector re-derivations (own pure-Python keccak,
  self-tested) in `vyper-selector-sets.json` — 50/50 agree with the peers' own
  Vyper CLI outputs.
