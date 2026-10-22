source: S086 Solidity docs, Library Linking (unlinked placeholder, cause of the h09 refusal); S084 and S085 Sourcify filter code and canonical list (why the filter step is inert on these rows); the round-25 entry's rows S075, S076, S077, S078, S021
verified-at: 2026-10-22, round 28 (R28-C1); 61 REA `rea-agents@6.5.0` `inspect-evm-interface` calls 17:17Z (`corpus/evidence/round-28/c1/runs.tsv`), 374 saved lookups (`corpus/evidence/round-28/c1/db/manifest.json`), all after the counter froze at lane commit 87d3dfb6 (17:17:16Z)
recheck: python3 -I -B tools/round-28/c1-heldout-naming.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> (offline over committed bytes; at the round-28 tip it prints `runs_ok=60/61 rows_complete=186/187 tally_equal=1` and exits 1: the frozen claim is missed)

# The round-25 EVM naming rule, scored once on held-out selectors: named 137, right 137, wrong 0

The round-25 entry (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`) picked
its primary naming rule on the same 69 rows it scored. This round scored that rule, unchanged, on
carriers and selectors frozen before any run or lookup. The scoring code is the round-25
definition, re-used by `tools/round-28/c1-heldout-naming.py`. Tally:
`corpus/evidence/round-28/c1/tally.json`.

## Claim status: missed (honest stop)

The frozen claim (`.ufo/waves/round-28/claims.json`) needed 61/61 valid runs and 187/187 complete
rows. It reached **60/61 and 186/187**. REA 6.5.0 refused carrier h09
(`.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/out/Cr1LibUser.noopt.runtime.hex`) with
`invalid_format` ("Hex carrier requires complete hexadecimal byte pairs …";
`corpus/evidence/round-28/c1/envelopes/h09.json`). The file holds one unlinked-library
placeholder, `__$a2bad93077572174e8e5044433a5a7d5f3$__`, which is solc's form for a library
address not yet linked (S086 `:74`) and is not hex. The carrier list was frozen without a hex
screen (mistake M28-1). The target is not narrowed and the counter is not changed. The numbers
below are the observed held-out result, and they do not make the claim met.

## Held-out result (187 selectors on 61 carriers)

| rule (round-25 name) | named | right | wrong | no name |
|---|---|---|---|---|
| `openchain_sole_unfiltered_args_consistent` (primary) | 137 | 137 | 0 | 50 |
| `openchain_sole_unfiltered` | 143 | 143 | 0 | 44 |
| `openchain_first` | 145 | 145 | 0 | 42 |
| `fourbyte_sole_args_consistent` | 90 | 90 | 0 | 97 |
| `fourbyte_first` | 96 | 94 | 2 | 91 |

Other tally fields: REA recovered 186 of 187 selectors (the missing one is h09's `useIt(uint256)`).
For 167 selectors, REA's inferred arguments match the ABI. For 145, the true name is in some
database, and 42 have no candidate in either database. Both `fourbyte_first` errors are spam
names returned first: `burn(uint256)` came back as `collate_propagate_storage(bytes16)` (h10),
and `transferOwnership(address)` as `_SIMONdotBLACK_(int8[],uint256,address,bytes8,int96)` (h59).

Pre-registered hypotheses (claims.json, reported, not targets):
- H1, primary wrong ≤ 5% of named: **holds**, 0 of 137.
- H2, primary names fewer than half of 187: **fails**. It named 137 of 187. Many lane-invented
  names such as `f0(uint256)` are present in openchain. Why they are there is not established
  (inference: earlier submissions; not tested).

## Why the filter step changed nothing here

None of the 187 held-out selectors is one of Sourcify's 36 canonical keys (S085). The service
marks `filtered` only on those keys (S084), so on these rows "sole unfiltered" equals "sole".
The 145 → 143 → 137 steps come from the sole-candidate check (2 rows) and the argument check
(6 more rows). See `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`.

## Limits

- The carriers were compiled by this lane (arc3-loop1) for other tests, and most names are
  lane-invented. This is not a test on deployed contracts.
- One lookup snapshot, one REA pin, one compiler-ABI ground truth per carrier
  (`tools/round-28/select-heldout.py` pairing rule).
- The claim missed. This entry records a measurement, not an admitted claim.

## Use

- The round-25 primary rule kept a zero error count out of sample (0 of 137), at a cost of 50
  unnamed rows. When a name must be right, prefer it over `fourbyte_first`, which was wrong twice.
- Before freezing any EVM carrier list, screen every runtime file for non-hex bytes (`__$` linker
  placeholders). Link the file (`solc --link`, S086 `:91`) or leave it out before the freeze, not
  after.
