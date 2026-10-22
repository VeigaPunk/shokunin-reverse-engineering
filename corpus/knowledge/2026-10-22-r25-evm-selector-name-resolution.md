source: S075 4byte.directory API documentation; S076 Sourcify 4byte signature service OpenAPI (openchain-compatible lookup); S077 EVMole interpretation reference; S021 Solidity ABI specification (Function Selector, opened 2026-10-19)
verified-at: 2026-10-22, round 25 attempt 3; REA `rea-agents@6.5.0` envelopes replayed byte-equal in `corpus/evidence/round-25/a3/c2/rea-replay/`; lookups saved 2026-10-22T08:28Z–08:30Z with sha256 per response in each `db/manifest.json`
recheck: python3 -I -B tools/round-25/a3/tally-resolution.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin (offline; reads only saved envelopes, saved lookups and compiler ABIs; expected output equals `corpus/evidence/round-25/a3/c2/analyze/tally.json`)

# EVM selector names are labelled candidates from a signature database, never a recovered fact

Coverage-map ground: EVM selector naming, which `PROVINCE.md` Frontier listed
as missing ("selectors stay bare hashes (no signature DB → no name
resolution)"). REA's `inspect-evm-interface` (EVMole 0.9.3 inside REA 6.5.0)
recovers four-byte selectors, inferred argument lists and inferred state
mutability from runtime bytecode. It returns no function names. This entry
holds a measured, offline naming procedure on six lane-compiled carriers whose
compiler ABIs are the ground truth. It claims no accuracy on deployed
third-party contracts, no live lookup service, and no verified name.

## What the sources say

- EVMole's own interpretation reference (S077): "A selector is a four-byte
  dispatch value found by static bytecode analysis. It does not supply a
  verified function name." It also says argument types are "likely ABI types
  inferred from calldata use".
- The Solidity ABI specification (S021) defines the selector as the first
  four bytes of the Keccak-256 hash of the canonical signature. Four bytes is
  32 bits, so distinct signatures can share one selector.
- 4byte.directory (S075) maps text signatures to selectors, accepts public
  submissions and filters `hex_signature` by exact match. Its documentation
  states no result order.
- The openchain lookup, now served by Sourcify (S076), takes a `filter`
  parameter described as "Whether or not to filter out junk results"; each
  match carries `filtered` and `hasVerifiedContract` flags.

## The measured procedure

Inputs, all committed: the six carriers in
`corpus/evidence/round-25/a2/c2/carriers.tsv` (two solc ERC-20 shapes, an
optimizer-200 vault, two carrier contracts, one Vyper token); one REA 6.5.0
envelope per carrier; 138 saved lookup responses (one 4byte.directory page and
one openchain `filter=false` response per selector, all HTTP 200, every
sha256 re-checked equal to its manifest). `tools/round-25/a2/resolve-selectors.py`
(standard-library Keccak-256, selftest 9/9 including a SHA3-256 negative
control) labels every candidate `keccak-mismatch`, `args-mismatch` or
`consistent`; `tools/round-25/a3/tally-resolution.py` scores five naming rules
against the ABI.

Counts over 69 per-carrier selector rows (43 distinct selectors), from
`corpus/evidence/round-25/a3/c2/analyze/tally.json`:

| naming rule | named | right | wrong | no name |
|---|---|---|---|---|
| first 4byte.directory result | 59 | 33 | 26 | 10 |
| the only 4byte candidate whose parameter list matches REA | 48 | 47 | 1 | 21 |
| first openchain result (`filter=false` order) | 62 | 61 | 1 | 7 |
| the only openchain candidate with `filtered=false` | 55 | 54 | 1 | 14 |
| the only `filtered=false` openchain candidate whose parameter list matches REA | 49 | 49 | 0 | 20 |

No saved candidate failed the Keccak check (0 `keccak-mismatch` rows): both
databases returned only selector-correct text, so the Keccak check alone
never removes a wrong name here.

## Decision rule

1. Report the selector, REA's inferred arguments and every Keccak-correct
   candidate with its database and flags. Never print one candidate as "the
   name".
2. A name may be called the **leading candidate** only when exactly one
   `filtered=false` openchain candidate matches REA's parameter list. On these
   carriers that rule named 49 of 69 rows with 0 wrong; it is still an
   inference, and 20 rows got no name.
3. Never take the first 4byte.directory result: 26 of its 59 names were wrong.
   The saved pages list higher ids first, and for `transfer(address,uint256)`
   the first saved result was `workMyDirefulOwner(uint256,uint256)`.
   `[inference]` Popular selectors attract junk submissions over time.
4. No candidate in either database is **UNKNOWN**, not evidence that the
   function has no public name: 6 distinct selectors (7 rows) had no candidate,
   among them `fee_of(uint256,uint256)` (`0c751377`) and
   `note(bytes32,uint256)` (`3efdef66`).

## Error patterns seen on the carriers

- **A real collision with a wrong sole candidate.** `0x6e8efde2` is both
  `fee_quote(uint256)` (the carrier's ABI) and `hasStreamed(address)`
  (Keccak-checked by the resolver). openchain returned only
  `hasStreamed(address)`, unfiltered, so "first" and "sole unfiltered" both
  named it wrongly. REA inferred `uint256`, which rejected it: the
  parameter-list check is what caught it.
- **Same parameter list, two unfiltered names.** `0x2e1a7d4d` returned
  `withdraw(uint256)` and `OwnerTransferV7b711143(uint256)`, both unfiltered
  and both matching REA's `uint256`. The rule gives no name; neither the flag
  nor the arguments separate them.
- **Wrong REA arguments pick the wrong name.** On the Vyper token, REA inferred
  `uint256,uint256` for `0xa9059cbb` (`transfer(address,uint256)`), so the
  4byte parameter-list rule returned `workMyDirefulOwner(uint256,uint256)`.
  The openchain rule returned nothing for that row because no unfiltered
  candidate matched. The argument check depends on REA's inference being
  right, and it was wrong here.

## Limits

- Six carriers compiled by this lane, 43 distinct selectors; many are common
  ERC-20 names that databases already know. Rates on deployed or obfuscated
  contracts are not measured.
- The lookups are one snapshot (2026-10-22T08:28Z–08:30Z). Both databases take
  public submissions, so a later lookup can add a colliding or junk entry and
  change any count above.
- openchain responses were requested with `filter=false` and the rule reads
  the per-match `filtered` flag; a `filter=true` request was not saved, so its
  server-side behaviour is not measured here.
- The ground truth is each carrier's compiler ABI file, not a deployed
  verification record.
