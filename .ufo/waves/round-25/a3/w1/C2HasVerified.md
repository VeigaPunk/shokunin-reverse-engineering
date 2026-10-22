# C2 alternative naming rules using openchain `hasVerifiedContract`

Seat KaidokuR25a3.C2HasVerified. Round 25 attempt 3, wave 1. Lane
/home/vgpnk/Projects/shokunin/kaidoku-shokunin, read-only except this report.
Offline only: saved lookups in `corpus/evidence/round-25/a2/c2/` and the carrier
ABIs. No network request was made.

## Verdict

Rule C (the only openchain candidate that is `filtered=false`, has
`hasVerifiedContract=true` and whose parameter list matches REA) **dominates
rule 5** on this corpus: 52 named, 52 right, 0 wrong over 69 rows, against
rule 5's 49 named, 49 right, 0 wrong. It names three rows that rule 5 leaves
unnamed and loses none. Rules A (sole `hasVerifiedContract=true`, any filtered
state) and B (sole `filtered=false` and `hasVerifiedContract=true`) do **not**
dominate: A names fewer rows than rule 5 (43 vs 49) and B introduces one
wrong name. The flag can add to the parameter-list check but not replace it.

## Table: alternative rules over the 69 carrier rows

| rule | named | right | wrong | no name | dominates rule 5 |
|---|---|---|---|---|---|
| rule 5: sole unfiltered, args-consistent (baseline) | 49 | 49 | 0 | 20 | baseline |
| A: sole candidate with `hasVerifiedContract=true` | 43 | 42 | 1 | 26 | no (fewer named, +1 wrong) |
| B: sole candidate with `filtered=false` and `hasVerifiedContract=true` | 62 | 61 | 1 | 7 | no (+1 wrong) |
| C: sole candidate `filtered=false`, `hasVerifiedContract=true`, args-consistent | 52 | 52 | 0 | 17 | **yes** (+3 named, 0 wrong) |

Over the 43 distinct selectors (lane carrier order): rule 5 31/31/0, A
28/27/1, B 37/36/1, C 33/33/0. An extra rule D (sole verified and
args-consistent, no filter constraint) scores 38/38/0 over rows and 25/25/0
over distinct selectors, so it dominates neither. Both readings of rule C
agree: "exactly one candidate that is unfiltered, verified and
args-consistent" and "exactly one unfiltered+verified candidate exists and it
is args-consistent" give the same 52 rows, since every row with candidates has
exactly one unfiltered+verified candidate.

## Where rule C gains (3 rows, 2 distinct selectors)

| carrier | selector | rule C name | ABI truth | why rule 5 abstained |
|---|---|---|---|---|
| carrierv | 2e1a7d4d | `withdraw(uint256)` | `withdraw(uint256)` | two unfiltered args-consistent candidates |
| vaultb-opt200 | 2e1a7d4d | `withdraw(uint256)` | `withdraw(uint256)` | same pair |
| kdxtoken | 40c10f19 | `mint(address,uint256)` | `mint(address,uint256)` | two unfiltered args-consistent candidates |

The tie is always broken by the flag: `withdraw(uint256)` is
`hasVerifiedContract=true` while `OwnerTransferV7b711143(uint256)` is `false`,
and `mint(address,uint256)` is `true` while `cat642998653(address,uint256)` is
`false`. Rule C loses no row that rule 5 named.

## Where rules A and B fail (counterexample)

Carrier `carrierv`, selector `6e8efde2`: the ABI truth is `fee_quote(uint256)`,
but openchain returns only `hasStreamed(address)`, `filtered=false`,
`hasVerifiedContract=true`, `label=args-mismatch`. Rules A and B name it and
are wrong. The truth is absent from openchain here, so no openchain rule could
have named it. The parameter-list check rejects the collision, the flag does
not: the collision name also occurs in some verified contract.

## Structural facts measured on the saved corpus

- 216 openchain candidates over the 62 rows that have any; 7 rows have no
  candidate at all. 69 are `filtered=false`, 62 are `filtered=false` and
  `hasVerifiedContract=true`, exactly one in each of those 62 rows.
- 153 candidates have `hasVerifiedContract=true` but only 61 equal the ABI
  truth: the flag alone picks the truth in 40 percent of cases. It is precise
  only when combined with `filtered=false`. All 61 truth candidates present in
  openchain are `filtered=false` and `hasVerifiedContract=true`; on 8 rows the
  truth is absent from openchain, and all 49 rule-5 names carry the flag,
  which is why rule C can keep them.
- Rule C's 17 unnamed rows split into: 7 rows with no candidate at all; 9 rows
  where the sole unfiltered+verified candidate is the truth but REA's inferred
  argument types are wrong (the parameter-list check discards a correct name);
  1 row (6e8efde2) where the sole unfiltered+verified candidate is the wrong
  collision.
- 4byte.directory responses carry no verified flag, so every rule above is
  openchain-only by construction.

The entry's sentence about 0x2e1a7d4d, "neither the flag nor the arguments
separate them", is too strong: the `filtered` flag does not separate them but
`hasVerifiedContract` does. Observation, saved response of 2026-10-22.

## Limits

- Six lane-compiled carriers, 43 distinct selectors, one snapshot
  (2026-10-22T08:28Z-08:30Z); the gain of rule C is 3 rows and 2 distinct
  selectors, a small margin.
- `hasVerifiedContract=true` means the signature occurs in some verified
  contract, not that this carrier is verified. It is a popularity signal: the
  true names here are common ERC-20 style names the databases already hold,
  the junk names are rare. [inference] The gain may not transfer to deployed
  or obfuscated contracts.

## Commands and evidence (all exit 0, UTC 2026-10-22)

1. `10:45:15Z` sha256 of all 138 saved responses against the six
   `db/manifest.json` files: `responses_checked 138 mismatches 0`.
2. `10:45:16Z` `python3 -I -B tools/round-25/a3/tally-resolution.py --root
   <lane> --out <seat>/analyze`: exit 0. Baseline reproduced, rule 5 `named
   49, right 49, wrong 0, no_name 20`; my `analyze/tally.json` equals the
   committed `corpus/evidence/round-25/a3/c2/analyze/tally.json`.
3. `10:45:16Z` `python3 -I -B <seat>/hasverified-rules.py <seat>/analyze
   <lane>` (the table above) and `python3 -I -B <seat>/independent-check.py
   <lane>`: exit 0 both. The second implementation reads the saved envelopes,
   responses and ABIs directly and recomputes Keccak and the parameter check
   itself; it reproduces every number in the tables, including the one wrong
   name of rules A and B.

## Artifacts (seat dir, the L1 integrates)

- `hasverified-rules.py` b8883440dcc0dcc8dcf09b5b9c891d98a225609205eda08c82626ec141390f10
- `independent-check.py` 95439bebb9f0ce5af61eb4b114ef00b624d89e52070c06f31cecf9e4cda5c298
- `run-evidence.sh` 4c8b7bcf36eb88fb9e7c4c092ad693706b8710f73be19bac34022a4feb31e64f
- `evidence.log` 1871c7ad6bd86c88761673dc0533a201d4e15654fccbffe2dd30cfb05c5bc848
- `hasverified-report.json` 6c3c6eda1edb288beadebdae9a8d86c5744300a3d8fe3b1edfca69dce3a3d3b0
- `independent-check.json` 9a0acd0063adb6f67362f2a0e3c3919d2963eb0b9845fae65e6f8aacf1acd1b7
- `analyze/tally.json` 479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc
  plus `analyze/<carrier>.json` for the six carriers.
Tooling: nothing installed; system `python3` 3.14.8 standard library only.
Report: .ufo/waves/round-25/a3/w1/C2HasVerified.md
