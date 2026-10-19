# proposed record correction — EX-07's `Rv2TokenOpt.planted-K.json` (rv-2 reviewer finding)

Status: **proposal text only — NOT applied** by RV-2 (reviewer). Target of the
correction is seat EX-07's artifact tree
(`.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.planted-K.json` and its
`/var/tmp/ex07/` twin), or a parent-side record note if the seat is closed.

## Finding (measured, 2026-10-19)

The file's planted-K values are **NIST sha3_256 digests**, not Ethereum
**keccak256** digests. Verified with the receipted solc prefix tree's
`js-sha3@0.8.0`:

```
sha3_256("approve(address,uint256)") = a613914d04c3c5f7cbddda84cb2f623c03717c21b5b691408fb22184c8850f8a
keccak256("approve(address,uint256)") = 095ea7b334ae44009aa867bfb386f5c3b4b443ac6f0ee573fa91c4608fbadfba
```

The file's own note says the first write stored full 32-byte hashes and was
"corrected" at 13:08:45.590Z (mtime 10:08:53 -03). Measured: the *pre-probe*
generation (quoted in `optB-compare.txt` as `PLANTED-K (pre-probe, recorded
2026-10-19T13:07:45.306Z)`) is the sha3_256 **full 32-byte** digest set
(`a613914d…`, `1d7976f3…`, `1f1881f8…`, `4b40e901…`, `31f2e679…`); the
"correction" truncated the same wrong-family digests to 8 hex chars. Both
generations are wrong-family; the corrected file is also post-probe. The
file itself flags `oracle_set_match: false` — the flag is correct, the
conclusion it invites (probe/planted disagreement) is not: the probe recovered
the true set.

## Ground truth (RV-2, independent)

`js-sha3 keccak256` over the ABI at `/var/tmp/ex07/Rv2TokenOpt.abi.json`
(5 functions) gives exactly the probe's recovered set:
`095ea7b3 18160ddd 23b872dd 70a08231 a9059cbb` — identical to the r1 oracle
(`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-sels.sorted`) and to the
r1 KdxToken/Rv2Token records. Probe legs: `ev_6ed8aa4e…` (hex@6.4.0),
`ev_43529582…` (raw@6.4.0), `ev_49dc43c9…` (hex@6.7.0) — all 5/5, all
`dispatch:"abi"`, all re-derived by RV-2 (see
`claims/c1/RV-2/evidence/verify-ids-and-envelopes.txt`).

## Proposed correction (for the record)

Replace the file's `selectors` array with the keccak256-truncated set above and
replace the note with:

> CORRECTED (RV-2 reviewer, 2026-10-19): the first write and the 13:08:45Z
> correction both used sha3_256, not keccak256. The planted set was re-derived
> with keccak256 (js-sha3@0.8.0) from the ABI: 095ea7b3 18160ddd 23b872dd
> 70a08231 a9059cbb (K=5), matching the r1 oracle. The probe legs recovered
> the same set K/K, zero extras; no probe-side mismatch exists.

If the artifact tree is frozen at landing, this text can land as a record note
in the round report instead — the claim's K/K stands on the ABI/keccak oracle
and the probe legs either way. Misread risk to close: a reader seeing
`oracle_set_match: false` should not conclude the probe failed.

## Evidence pointers (RV-2 side)

- `claims/c1/RV-2/evidence/verify-ids-and-envelopes.txt` (29/29 id + envelope match)
- `claims/c1/RV-2/evidence/kk-check-set1.txt` (optB legs: K=5 set OK)
- `claims/c1/RV-2/tools/selectors.js` (keccak derivation from ABI)
- `claims/c1/RV-2/evidence/my-optB-hex-6.4.0.json` vs
  `claims/c1/EX-07/optB-hex-6.4.0.json` (field-identical)
- Sha3_256/keccak256 probe outputs quoted above: rerun of `tools/selectors.js`
  and the one-liner in section "Finding".