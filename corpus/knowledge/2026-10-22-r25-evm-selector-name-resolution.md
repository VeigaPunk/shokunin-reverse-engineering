source: S075 4byte.directory API documentation; S076 Sourcify 4byte signature service OpenAPI (openchain-compatible lookup); S077 EVMole interpretation reference; S078 Sourcify 2025 Recap (openchain takeover and database seeding); S021 Solidity ABI specification (Function Selector, opened 2026-10-19)
verified-at: 2026-10-22, round 25 attempt 3; REA `rea-agents@6.5.0` envelopes replayed byte-equal in `corpus/evidence/round-25/a3/c2/rea-replay/`; lookups saved 2026-10-22T08:28:09Z–08:31:37Z with sha256 per response in each `db/manifest.json`
recheck: python3 -I -B tools/round-25/a3/tally-resolution.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin (offline; reads only saved envelopes, saved lookups and compiler ABIs; expected output equals `corpus/evidence/round-25/a3/c2/analyze/tally.json`)

# EVM selector names are labelled candidates from a signature database, never a recovered fact

Coverage-map ground: EVM selector naming, which `PROVINCE.md` Frontier listed
as missing ("selectors stay bare hashes (no signature DB → no name
resolution)"). REA's `inspect-evm-interface` (EVMole 0.9.3 inside REA 6.5.0)
recovers four-byte selectors, inferred argument lists and inferred state
mutability from runtime bytecode. It returns no function names. This entry
records an offline naming procedure scored on six lane-compiled carriers whose
compiler ABIs are the ground truth. It claims no accuracy on deployed
third-party contracts, no live lookup service, and no verified name.

## What the sources say

- EVMole's own interpretation reference (S077): "A selector is a four-byte
  dispatch value found by static bytecode analysis. It does not supply a
  verified function name." It also says argument types are "likely ABI types
  inferred from calldata use". REA's envelopes name this provider
  (`evmole-interface`, version `evmole@0.9.3`).
- The Solidity ABI specification (S021) defines the selector as the first
  four bytes of the Keccak-256 hash of the canonical signature. Four bytes is
  32 bits, so distinct signatures can share one selector.
- 4byte.directory (S075) maps text signatures to selectors, accepts public
  submissions without authentication and filters `hex_signature` by exact
  match. The page says nothing about result order.
- The openchain lookup takes a `filter` parameter described as "Whether or
  not to filter out junk results"; each match carries `filtered` and
  `hasVerifiedContract` flags (S076). Sourcify now answers openchain lookups
  and seeded that database with the openchain, 4byte.directory and etherface
  data (S078), so the two lookups below are not independent witnesses.

## The measured procedure

Inputs, all committed: the six carriers in
`corpus/evidence/round-25/a2/c2/carriers.tsv` (four compiled with solc: two
ERC-20 shapes, an optimizer-200 vault and a carrier contract; two compiled
with Vyper: `stewardtoken` and `carrierv`); one REA 6.5.0 envelope per
carrier; 138 saved lookup responses (one complete 4byte.directory page and one
openchain `filter=false` response per selector, all HTTP 200, every sha256
re-checked equal to its manifest). `tools/round-25/a2/resolve-selectors.py`
(standard-library Keccak-256, selftest 9/9 including a SHA3-256 negative
control) labels every candidate `keccak-mismatch`, `args-mismatch` or
`consistent`; `tools/round-25/a3/tally-resolution.py` scores five naming rules
against the ABI.

Counts from `corpus/evidence/round-25/a3/c2/analyze/tally.json`. The first
number is per carrier row (69 rows); the number in brackets is per distinct
selector (43), because shared ERC-20 selectors appear in up to four carriers.
The bracketed count keeps each selector's first carrier in `carriers.tsv`
order; REA's arguments can differ by carrier for one selector, so another
choice moves one cell (the 4byte parameter-list rule becomes 29 named, 28
right, 1 wrong, because `a9059cbb` is read correctly on the solc carriers and
wrongly on the Vyper token):

| naming rule | named | right | wrong | no name |
|---|---|---|---|---|
| first 4byte.directory result | 59 (34) | 33 (22) | 26 (12) | 10 (9) |
| the only 4byte candidate whose parameter list matches REA | 48 (29) | 47 (29) | 1 (0) | 21 (14) |
| first openchain result (`filter=false` order) | 62 (37) | 61 (36) | 1 (1) | 7 (6) |
| the only openchain candidate with `filtered=false` | 55 (34) | 54 (33) | 1 (1) | 14 (9) |
| the only `filtered=false` openchain candidate whose parameter list matches REA | 49 (31) | 49 (31) | 0 (0) | 20 (12) |

No saved candidate failed the Keccak check (0 `keccak-mismatch` rows): both
databases returned only selector-correct text, so the Keccak check alone
never removes a wrong name here.

**How these rules were chosen.** All five rules were written and scored on
these same 69 rows in one step; no rule was frozen before the data was seen.
The 0 wrong of the last rule is a score on the sample it was picked from, not
a measured error rate. For 21 of its 31 distinct names openchain returned a
single candidate, so the rule had no choice to make.

## Decision rule

1. Report the selector, REA's inferred arguments and every Keccak-correct
   candidate with its database and both openchain flags. Never print one
   candidate as "the name".
2. When exactly one `filtered=false` openchain candidate matches REA's
   parameter list, label it "sole unfiltered argument-consistent openchain
   candidate (snapshot UTC)". It is still an inference. On these carriers that
   label went to 49 of 69 rows (31 of 43 distinct) with none wrong, and 20
   rows got no label.
3. Never take the first 4byte.directory result: 26 of its 59 row names (12 of
   34 distinct) were wrong. The default order is newest submission first: all
   26 saved pages with two or more results run by `created_at` descending,
   and live requests honour `ordering=created_at` but ignore `ordering=id`
   (seat report `C2FourbyteOrder.md`). For `transfer(address,uint256)` the
   first saved result was `workMyDirefulOwner(uint256,uint256)`.
   `[inference]` Popular selectors attract junk submissions over time, so
   newest-first puts junk on top.
4. No candidate in either database is **UNKNOWN**, not evidence that the
   function has no public name: 6 distinct selectors (7 rows) had no candidate,
   among them `fee_of(uint256,uint256)` (`0c751377`) and
   `note(bytes32,uint256)` (`3efdef66`).
5. Neither flag is a verifier. `filtered=false` still let through 4 wrong
   candidates out of 40 distinct unfiltered ones, and `hasVerifiedContract`
   was true on 92 candidate rows that are not the ABI name.

## Error patterns seen on the carriers

- **A real collision with a wrong sole candidate.** `0x6e8efde2` is both
  `fee_quote(uint256)` (the carrier's ABI) and `hasStreamed(address)`
  (Keccak-checked by the resolver). openchain returned only
  `hasStreamed(address)`, unfiltered, so "first" and "sole unfiltered" both
  named it wrongly. REA inferred `uint256`, which rejected it: the
  parameter-list check is what caught it.
- **Same parameter list, two unfiltered names.** `0x2e1a7d4d` returned
  `withdraw(uint256)` and `OwnerTransferV7b711143(uint256)`, both unfiltered
  and both matching REA's `uint256`. The rule gives no name. In this snapshot
  only `withdraw(uint256)` had `hasVerifiedContract=true`, so that flag would
  separate them; see the limits for why this is not adopted as a rule.
- **REA's argument inference is often wrong on Vyper.** REA 6.5.0 inferred an
  argument list different from the ABI on 12 of 69 rows: 11 on the two Vyper
  carriers (mostly `address` read as `uint256`) and 1 on solc `carrierb`
  (`note(bytes32,uint256)` read as `uint256,uint256`). On the Vyper token,
  `0xa9059cbb` (`transfer(address,uint256)`) was inferred as
  `uint256,uint256`, so the 4byte parameter-list rule returned
  `workMyDirefulOwner(uint256,uint256)`; the openchain rule returned nothing
  for that row because the only unfiltered candidate did not match. When REA's
  arguments are wrong, the parameter-list check rejects the true name.
  Cause (seat report `VyperArgsCause.md`, bytecode and source traced):
  EVMole 0.9.3 types an argument as `address` only from a 160-bit AND mask on
  the calldata word; Vyper 0.4.3 instead rejects non-zero high bits with
  `x >> 160` (SHR), which 0.9.3 does not read, so the type falls back to
  `uint256`. The arc3-r4 Vyper entry already recorded `address` read as
  `uint256` on this carrier family
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`); this round adds
  the cause and its effect on naming.
- **The Vyper misses are fixed upstream, not in REA.** Run directly, EVMole
  0.9.4 (npm, published 2026-10-13) recovered every ABI argument list on both
  Vyper carriers; REA 6.3.0, 6.4.0, 6.5.0 and 6.7.0 all pin `evmole` 0.9.3
  (`npm view rea-agents@<v> dependencies.evmole`). Recomputed over the same
  saved lookups with 0.9.4 arguments, the openchain parameter-list rule named
  57 of 69 rows with none wrong. Source: round-25 wave-1 seat report
  `.ufo/waves/round-25/a3/w1/C2EvmoleDirect.md`; this is a direct EVMole run,
  not an REA capability.
- **REA 6.7.0 gives the same analysis, a different evidence id.** On all six
  carriers REA 6.7.0 returned the same selectors, arguments and mutability as
  6.5.0, so every count above is unchanged; the `evidence_id` differs because
  6.7.0 hashes a different projection (seat report `C2Rea67.md`). The
  byte-equal replay in the header holds for 6.5.0 only.

## Limits

- Six carriers compiled by this lane, 43 distinct selectors; most are common
  ERC-20 or short names that the databases already held. Rates on deployed or
  obfuscated contracts are not measured. The failure the rule cannot catch
  (the true name absent, a colliding name present, REA's arguments matching
  the collider) did not occur here and is not ruled out.
- The lookups are one snapshot (2026-10-22T08:28:09Z–08:31:37Z); a re-fetch of all
  43 selectors at 10:45Z was byte-identical (wave-1 seat report
  `C2LiveDrift.md`). Both databases take public submissions, so a later
  lookup can add a colliding or junk entry and change any count above.
- The six carriers were compiled in arc3-loop1 rounds 1, 3 and 4 (solc
  0.8.37 and Vyper 0.4.3) for other tests; their names were not chosen to
  collide with database entries, and no inclusion rule for these six out of
  the lane's other runtime carriers was recorded (seat report
  `CarrierProvenance.md`).
- The rules read the per-match `filtered` flag from `filter=false`
  responses. A later `filter=true` request for all 43 distinct selectors
  (2026-10-22T10:44Z–10:45Z, `corpus/evidence/round-25/a3/c2/filter-true/`)
  returned exactly the `filtered=false` subset for every selector, so rules 4
  and 5 give the same counts either way on this snapshot. That equality is
  observed here, not documented by S076.
- A rule that also requires `hasVerifiedContract=true` scored 52 of 69 named,
  none wrong, on the same rows (seat report `C2HasVerified.md`). It was found
  after the data was seen, like the five above, so it is recorded and not
  adopted.
- The ground truth is each carrier's compiler ABI file, not a deployed
  verification record. Sending selectors to the two public services reveals
  which selectors were looked up.
- Seat reports cited by file name above are in `.ufo/waves/round-25/a3/w1/`.

## Correction (round 26 wave 1): the 138 saved responses are per carrier-selector row

The sentence in "The measured procedure" (line 41) — "138 saved lookup responses (one complete
4byte.directory page and one openchain `filter=false` response per selector, all HTTP 200, every
sha256 re-checked equal to its manifest)" — is wrong in one word: "per selector". It reads as one
pair of responses per distinct selector, which would be 86. The 138 responses are two per
carrier-selector row, and there are 69 such rows over the six carriers; the six carriers use 43
distinct selectors. A selector shared by three carriers therefore contributes six saved responses,
not two.

Command (read-only, committed evidence under `corpus/evidence/round-25/a2/c2/`):

    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l        # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' | wc -l    # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' -printf '%f\n' \
      | sed -E 's/^4byte-(.*)-p[0-9]+\.json$/\1/' | sort -u | wc -l            # 43

69 rows x 2 responses = 138 saved responses; 138 = 2 x 69 carrier-selector rows, not 2 x 43
distinct selectors. Per kind, 16 of the 43 selectors were fetched for more than one carrier
(26 extra copies); those copies are byte-identical across carriers, so the 138 files hold 43
distinct 4byte bodies and 43 distinct openchain bodies. All 138 manifest entries still re-check
equal to their manifest `sha256` with `status` 200. `corpus/evidence/round-25/a3/c2/analyze/
tally.json` carries the same pair: `per_carrier_rows.selector_rows` = 69 and
`distinct_selectors.selector_rows` = 43. Apart from the carrier count below, nothing else in the entry changes: the rule scores are per
carrier row (69) and per distinct selector (43) as stated, and the `filter=true` re-fetch under
"Limits" was already once per distinct selector (43 responses in
`corpus/evidence/round-25/a3/c2/filter-true/manifest.json`).

Second correction (round 26 wave-1 seat `.ufo/waves/round-26/w1/EntryNumbers.md`): line 51 says shared ERC-20 selectors "appear in up to four carriers". The measured maximum is three (selectors per carrier count: 27 on one carrier, 6 on two, 10 on three, none on four; for example `095ea7b3` on rv2token, kdxtoken and stewardtoken).
