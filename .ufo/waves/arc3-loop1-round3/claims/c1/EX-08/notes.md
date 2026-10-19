# EX-08 — chain c1, executor (arc3-loop1-round3) — seat notes

Wave `arc3-loop1-round3` (kaidoku-shokunin), 2026-10-19. Repo HEAD at work:
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. Scratch `/var/tmp/ex08-r3/` (never
`/tmp`); no git mutations; no custody-path reads; nothing written outside this
seat directory, `seats/EX-08.md`, and scratch.

Seat line: *probe carrier B (hex + raw) on one pin; full envelopes under
claims/c1/EX-08/.* (chain plan `.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/plan.md`;
carrier-B author: seat EX-04, `seats/EX-04.md`.)

## Carrier identity used

- The chain's carrier B is **`VaultB`** (EX-04-authored, 2-of-3 multisig vault,
  K=11 selectors, optimizer-enabled opt200 leg). Identity of the two runtime
  files this seat probed, re-derived at read (rule #14) from
  `claims/c1/EX-04/evidence/`:
  - `carrierB.runtime-opt200.bin` 1850 B sha256
    `aaf85ceaf124bac2d3a32428927194158c9211e4472a0cf06f88a721cf239412`
    (== EX-04's recorded pin; hex twin sha256 `7dc26d4d…`).
  - `carrierB.runtime-noopt.bin` 3872 B sha256
    `679678e9a67aee701094a4bfeafd2a02311460658aa4b400202340b47d83d005`.
- EX-04 probed carrier B at `rea-agents@6.4.0` and its report names 6.7.0 as
  unexamined *by that seat* (`seats/EX-04.md` §4 "Not examined by this seat, by
  scope"). This seat's pin is therefore **6.7.0**.
- Third-seat replication: seat EX-10 (a carrier-B reconciliation seat) probed
  the **same** EX-04 carrier mid-wave at both pins
  (`claims/c1/EX-10/probe/probe-EX04carrierB-opt200-{hex,rawbin}-6.7.0.json`).
  This seat's 6.7.0 envelopes are payload-identical to EX-10's — same 11
  selectors, same offsets, same mutability/args, same bytecode digest — while
  the `ev_` ids differ because the subject path differs
  (`ev_d9883150…` mine vs `ev_a94c0e87…` EX-10): independent confirmation of
  both the recovery result and the measured path-keying of the id.

## Chain carrier B corroboration — VaultB @6.7.0 (`vaultb/`)

Pinned runner `vaultb/run-probes-vaultb.sh` (invokes the npx-cache
`rea-agents@6.7.0` `rea.mjs` directly — no install, no network; sha256
`ed06cee49505b95a3cc5fceb1b4b279167e26df86227c644bb366ffffdbaf738`, the pin r1
EX-08 recorded). Disk-backed `TMPDIR=/var/tmp/ex08-r3/tmp`. All runs exit 0,
stderr 0 B.

| leg | evidence_id | fns | missing | extra | bytecode.sha256 == runtime file | offsets == EX-04 @6.4.0 |
|---|---|---|---|---|---|---|
| opt200 hex | `ev_d9883150f3f35414258798bc44bc100a770b2abc7e75986d57c53ccb93a2aae6` | 11/11 | [] | [] | yes | yes |
| opt200 raw | `ev_e8572678472ee33bd3b2c70896df472838b309c4042a91bb8bc3efee0e52cb47` | 11/11 | [] | [] | yes | yes |
| noopt hex | `ev_b9b8f62af18cfcb6f42c99aaada248b8895ee809aad275209e27d5a81cb25f8d` | 11/11 | [] | [] | yes | n/a (other bytes) |
| rerun-a (same path) | `ev_d9883150…` re-derived | 11/11 | [] | [] | yes | yes |
| raw-on-hex-file trap | `ev_b6d6e6e4ebc5a0488119547eb31e32900af5ad4abe3dca491f99833cbc76b857` | 0 | — | — | bytecode digest == the hex FILE's sha256 (`7dc26d4d…`), `kind:"unknown"`, parsed-and-empty — the r1 trap class reproduces at 6.7.0 |

Reconciliation `vaultb/vaultb-6.7.0-reconciliation.json` (runner
`vaultb/reconcile-vaultb.py`) compares against EX-04's frozen
`planted-B-opt200.json` (K=11) and EX-04's 6.4.0 envelope: set-equal,
zero extras, and **all 11 `bytecode_offset` values identical** across seats and
pins. Independent layout re-derivation by this seat
(`vaultb/push4-census-vaultb-opt200.json`, linear sweep): 13 PUSH4 sites — GT
split @19 on `59bf77df` (target 0x62=98), 11 EQ legs @30–144, and the
non-dispatch Panic constant `4e487b71` @1777; every reported offset is an
EQ-leg JUMPI target whose byte is `5b` (JUMPDEST). EX-04's dispatcher-shape and
offset-semantics claims re-derived, not copied.

## Seat-side auxiliary carrier — `HarborBound` (`aux/`, tag `CarrierB` in-scratch)

Distinct non-ERC-20 shape: payable `receive`+`fallback`, mixed mutability
(pure/view/payable/nonpayable), custom errors, and **library-bound calls**
(external `HarborLib.scale/tag` → DELEGATECALL with a pinned link address
`0x…0042`). Compiled on-host with the receipted r1 solc prefix
(`0.8.37+commit.f401782d`, `solcjs` sha256 `188c3fdca72b…`), standard JSON,
optimizer `{enabled:true, runs:200}` (opt) and off (noopt) twins.
Source `aux/CarrierB.sol` sha256 `19c9cf1555f2c0d3e3a48e6728e0355ae05ef8e4805d66a1cc85b70efc049f36`.

- opt: runtime 1448 B `69292866ce55b8cbf8f927076b589c8f8b5896ee2a2a5736fdd97575af8a4563`;
  noopt: 2492 B `db93b92dabb8755379e5783507f128aed06daa03920ea870440e55d23e730c6e`;
  library runtime: 264 B `528d03166dea2f16b41f482edb86a4e8f718249db2d088796c05518b0fbbb9d8`.
- Planted K=8 recorded **pre-probe** (scratch mtimes: 13:07:57Z vs first
  envelope 13:08:48Z; the claim-dir copies preserve bytes, not mtimes):
  `aux/planted-K.json`, js-sha3 keccak × solc `methodIdentifiers` 0 mismatches.

| leg | fns | missing/extra | offsets JUMPDEST | note |
|---|---|---|---|---|
| opt hex @6.4.0 | 8/8 | 0/0 | 8/8 | `probe-CarrierB-runtime-hex-6.4.0.json` |
| opt raw @6.4.0 | 8/8 | 0/0 | 8/8 | raw ≡ decode; subject digest == bytecode digest |
| opt hex @6.7.0 | 8/8 | 0/0 | 8/8 | cross-pin agreement |
| noopt hex @6.4.0 | 8/8 | 0/0 | 8/8 | optimizer not load-bearing for this set |
| library hex @6.4.0 | 2/2 | 0/0 | 2/2 | library runtime has its own dispatch |

Mechanism (independently derived, `aux/push4-census.json`, `aux/disasm.py`):
dispatcher is a **GT-split + EQ-chunk layout** (`DUP1 PUSH4 <sel> GT/EQ PUSH2
<dst> JUMPI`) — 9 compare sites for 8 selectors (the median `a4d66daf` appears
twice: GT @19, EQ @30); the 9th site's split target 0x4d=77 is a JUMPDEST.
Prologue class `5f3560e01c` at offset 13 (the r1 class; r1's offset was 25 —
offset is carrier-dependent, class invariant). **Datum, not a mechanism claim:**
r1's K=6 clustered-selector carriers were linear; this K=8 spread set is
split — the same layout appears with the optimizer on *and* off, so the
optimizer is not the discriminator; count vs selector-density is not isolated
by these two points (recorded as open).

False-positive controls: the four non-dispatch PUSH4 constants in the opt
runtime — library selectors `6e69f38c`/`51f91066` (DELEGATECALL calldata),
mask `ffffffff`, Panic `4e487b71` — are all absent from the reported set;
`extra=[]` on every leg. `receive`/`fallback` produce no pseudo-selectors.

Mutability deltas vs the compiled ABI (upstream-inference, recorded not
counted as failure): `survey(uint256)` (ABI `view`) and `beacon()` (ABI `pure`)
both report `nonpayable` — their bodies DELEGATECALL the library; the
library's own `pure` entry points report `payable`. `depth/limit/keeper`
report `view` correctly; `donate` reports `payable` correctly. This extends the
plan's pre-measured `pure → nonpayable` delta with the delegatecall-bearing
sub-class and the library-entry-point sub-class.

## Controls

- **Cross-wave regression control** (`aux/probe-control-KdxToken-runtime-hex-6.4.0.json`,
  `aux/control-kdx.js`): r1's KdxToken rebuilt from its retained source
  (`c2980385…`) is **byte-identical** to r1's recorded runtime pin
  (`9c40940e…`, 1789 B), and this seat's runner reproduces r1's 6.4.0 result
  exactly — 6/6, offsets 100/148/178/226/254/302 (r1 `run-hex-6.4.0.json`).
  The harness is the same harness that measured the r1 legs.
- **Id domain** (`aux/id-domain.json`): same content + same path re-derives the
  `ev_` id across rerun and across CWD (repo root); same content + different
  path mints a new id (`ev_69b6f8e4…` → `ev_269833f9…`). Corroborates EX-11's
  independent path-keying measurement (`seats/EX-11.md`); cross-pin ids differ
  (PL-1 A7). Compare by `subject.digest.sha256` per rule #14.

## Proposed changes

`proposed-entry-deltas.patch.md` (patch text, NOT applied) — three proposed
Observation lines for the round's C1 corpus entry: the id-domain resolution,
the delegatecall mutability sub-class, and the K=8 layout datum. No repo file
was modified by this seat.

## Out of scope / not examined

Creation-blob legs for the aux carrier (r1 + EX-04 classes already recorded);
`receive`/`fallback`-only carrier; selector-density mechanism isolation;
chain/deployment identity (never claimed by the tool). Size datum for the r1
"above the probed class" Unknown: the aux legs probed 1448 B (below r1's
1.8–1.9 KB class) and 2492 B (above it), both K/K — the entry may scope this
as the aux carrier's own sizes, not a general size claim. The aux carrier is a
seat-side extension, not the chain carrier.

## File map

`vaultb/` chain carrier B corroboration (envelopes verbatim + reconciliation +
runner + census). `aux/` seat-side carrier, twins, library, controls, planned-K,
id-domain, reconciler, and the compile/probe runners as executed. Envelope
`.err` files are 0 B by construction; rerun-a/b/c legs of the aux carrier
captured stdout only (ids and payloads recorded in `aux/reconciliation.json`).