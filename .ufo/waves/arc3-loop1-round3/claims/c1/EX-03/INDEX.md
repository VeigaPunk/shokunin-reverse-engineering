# INDEX — claims/c1/EX-03 (arc3-loop1-round3, seat EX-03, chain c1)

Path-stability note: this seat's tree was assembled in stages; files that other seats
read at ~13:09–13:12Z may have since moved under `carrier-A-EX02/` or
`carrier-A-plan-prototype-OptVault/`. **No file content changed** — the sha256 of every
compiled artifact is identical to its first landing.

## Which "carrier A" is which (three readings existed in the round)

| reading | source | sha256 | runtime | K | tree here |
|---|---|---|---|---|---|
| dispatch reading (EX-02 authored "carrier A"; EX-06 probed it as A/2; EX-07 names it legC) | `source/carrierA.sol` | `05b2cbb0c6fd97ae6463b0a4f1be56f217ea64cf4cbdbd2c36da94c0fe6eee41` | 1426 B `9f7392ac…23741a` | 9 | `carrier-A-EX02/` |
| PL-1 plan §1.A carrier A (prototype) | `source/OptVault.sol` | `40af90c9f66288b33804f5e08397601db6518b9b293022e847641af8391a764d` | 776 B `544469b7…95dfde7f` | 5 | `carrier-A-plan-prototype-OptVault/` |
| r1 CR-1 hand-assembled control `carrier-A.hex` (not a solc compile; not this seat's) | r1 tree | `36dc8246…01b9b3d2` | — | 3+decoys | not here |

Both solc carriers are compiled by this seat with the same literal flag form
(`--bin --abi --optimize --optimize-runs 200`) and are probe-ready.

## Path map (first landing at 13:08/13:14Z → final)

- `carrierA.cli.bin|.cli.abi|.creation.*|.runtime.*|.abi.json|.methodIdentifiers.json`,
  `planted-selectors.txt`, `evidence/transcript-main.txt`, `transcript-stdjson.txt`,
  `transcript-verify.txt` → now under `carrier-A-EX02/` (evidence under `carrier-A-EX02/evidence/`)
- `evidence/optimizer-paired-legs/*` (13:10Z landing) → now `carrier-A-EX02/paired/*`
- `evidence/cross-leg-EX02-comparison.txt` → unchanged path under `evidence/`
- OptVault legs → `carrier-A-plan-prototype-OptVault/` (+ `evidence/`)

## Read first

- `compile-receipt.txt` — flags, commands, all hashes, equivalence anchors, cross-leg
  agreement, the optimizer-on/off delta, scope/limits.
- `MANIFEST.sha256` — `sha256sum -c` clean (regenerated after every write).
- `evidence/sweep-both-carriers.txt` — dispatch/PUSH4 inventory for both carriers.
- `evidence/push4-attribution-notes.txt` — encoded-constant and metadata-boundary notes.