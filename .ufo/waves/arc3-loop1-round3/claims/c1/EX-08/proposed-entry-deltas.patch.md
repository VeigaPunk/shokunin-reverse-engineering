# Proposed entry deltas — arc3-loop1-round3 C1 corpus entry (PATCH TEXT, NOT APPLIED)

Seat EX-08 (chain c1, executor), wave `arc3-loop1-round3`, 2026-10-19. Three
proposed Observation lines for the round's C1 knowledge entry, each measured on
this seat's pins. Land only what this round's entry can cite with fresh
identities; re-derive every number against the bytes that land (rule #14).

Evidence root (this seat): `.ufo/waves/arc3-loop1-round3/claims/c1/EX-08/`
(`vaultb/` chain carrier B corroboration; `aux/` carriage of the lines below).

## Delta 1 — id domain (resolves the r1 entry's `ev_` Unknown, jointly with EX-11)

Proposed text (entry Observation):

> **Observation (id domain, `inspect-evm-interface` @6.4.0):** same bytes and
> same path re-derive the `ev_` id across reruns and CWDs; same bytes at a
> different path mint a different id (`ev_69b6f8e4…` → `ev_269833f9…`,
> `claims/c1/EX-08/aux/id-domain.json`), and a different pin mints a different
> id for identical bytes (PL-1 A7, `seats/PL-1.md`). The id is content+path
> keyed; cross-seat/cross-pin comparison is by `subject.digest.sha256`
> (rule #14). Corroborated independently on the r1 carrier by EX-11
> (`seats/EX-11.md`).

## Delta 2 — mutability inference on delegatecall-bearing and library shapes

Proposed text (entry Observation, extending the pre-measured `pure → nonpayable`):

> **Observation (mutability inference deltas, upstream inference — not a
> defect):** on a library-bound carrier (`claims/c1/EX-08/aux/CarrierB.sol`) the
> tool reports `nonpayable` for `survey(uint256)` (ABI `view`) and `beacon()`
> (ABI `pure`) — both bodies DELEGATECALL the pinned library — and `payable`
> for the library's own `pure` entry points (`scale`, `tag`;
> `probe-HarborLib-runtime-hex-6.4.0.json`). `depth/limit/keeper` infer `view`
> correctly; `donate` infers `payable` correctly. The recovered selector sets
> are unaffected (K/K with zero extras on every leg).

## Delta 3 — dispatch-layout boundary datum (K=8, both optimizer states)

Proposed text (entry Observation, refining the K=5/6-linear vs K=11-binary
framing):

> **Observation (layout datum):** a K=8 spread-selector carrier
> (`claims/c1/EX-08/aux/CarrierB.runtime.hex`, 1448 B / same source noopt
> 2492 B) shows the GT-split + EQ-chunk layout in **both** optimizer states
> (prologue class `5f3560e01c` at offset 13 unchanged); r1's K=6 clustered
> carriers were linear. The optimizer is not the discriminator; whether the
> switch keys on selector count, selector spread, or both is **not measured**
> (open). Both layouts parse K/K.

## Notes for the merger

- Line 3's carrier is this seat's aux carrier, not the chain's `VaultB`; keep
  it scoped to the pinned bytes named.
- No pointer-table / expected.json / census-scope change is proposed.
- Cross-seat numbers cited above are pointers to those seats' artifacts; the
  entry should re-derive from the envelopes cited, not from this patch text.