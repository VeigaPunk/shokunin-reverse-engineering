source: S088 ERC-4626 Tokenized Vaults standard text (ethereum/ERCs `3c0f7076`, the published list behind carrier n04); the round-25 entry's rows S075, S076, S077, S078 for the databases; S084/S087 for the `filtered` flag
verified-at: 2026-10-22, round 29 (R29-C1); 16 REA `rea-agents@6.5.0` `inspect-evm-interface` calls 20:03:21Z–20:03:37Z (`corpus/evidence/round-29/c1/runs.tsv`), 304 saved lookups 20:03:39Z–20:08:52Z (`corpus/evidence/round-29/c1/db/manifest.json`, every one HTTP 200 on its first try), all after the claim froze at lane commit dbd87cfa
recheck: python3 -I -B tools/round-29/c1-fresh-naming.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> (offline over committed bytes; expected `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1`, exit 0)

# The round-25 EVM naming rule on 16 fresh carriers of published interfaces: named 122, right 122, wrong 0

Round 28 scored the round-25 primary naming rule on the lane's own carriers, whose names were
mostly lane-invented, and missed its frozen target on one carrier that REA refuses
(`corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md`). This round compiled 16 new
carriers that hold published function lists (ERC-20 with EIP-2612, ERC-721, ERC-1155, ERC-4626
from S088, Ownable/AccessControl/Pausable, Uniswap V2 pair, router and factory, WETH9, Multicall3
block getters, Chainlink aggregator, TimelockController, GovernorBravo, Safe owner manager, ENS
registry, ERC-2981 with NFT-drop admin), screened them, and froze the selector list before any run
or lookup. Tally: `corpus/evidence/round-29/c1/tally.json`. Scoring code: the round-25 rule
definitions, unchanged, in `tools/round-29/c1-fresh-naming.py` (copied from the round-28 counter).

## What was frozen, and how it was screened (lane commit dbd87cfa)

- Carriers: `tools/round-29/make-carriers.py` wrote one Solidity contract per interface whose
  functions only read their arguments, and compiled them with solcjs 0.8.37 (standard JSON, no
  optimizer). No contract calls a library, so no link placeholder can occur.
- Hex screen before the freeze (QUALITY row 43): `tools/round-28/hex-screen.py` → `carriers=16
  fail=0`, exit 0 (`.ufo/waves/round-29/before/hex-screen-c1.txt`).
- Held-out selectors (QUALITY row 44): of the 178 distinct ABI selectors, 19 are in round 25's 43
  or round 28's 187 and 7 more appear as a word somewhere in the lane at the base (for example
  `3644e515` DOMAIN_SEPARATOR(), `c45a0155` factory()); all 26 were dropped. `tools/round-29/preseen.py
  --kind name` on the remaining 152 → `overlap=0`, exit 0
  (`.ufo/waves/round-29/before/preseen-c1-name.txt`). Carrier n09 (WETH9) keeps a run but no
  held-out row: both its selectors were dropped.

## Result (152 held-out selectors on 16 carriers)

| rule (round-25 name) | named | right | wrong | no name |
|---|---|---|---|---|
| `openchain_sole_unfiltered_args_consistent` (primary) | 122 | 122 | 0 | 30 |
| `openchain_sole_unfiltered` | 116 | 116 | 0 | 36 |
| `openchain_first` | 152 | 152 | 0 | 0 |
| `fourbyte_sole_args_consistent` | 123 | 123 | 0 | 29 |
| `fourbyte_first` | 152 | 116 | 36 | 0 |

REA recovered all 152 selectors (`recovered_by_rea 152`), and its inferred argument list equals
the ABI's on 125 of them (`args_match_abi 125`). Every selector has the true name in at least one
database (`truth_in_some_database 152`).

Primary triple for the frozen claim: **named 122, right 122, wrong 0**. Both reported hypotheses
hold: H1 (wrong at most 5% of named) and H2 (named at least half of 152).

## Why 30 rows get no name

- 24 rows: the ABI has a `bytes32` argument and REA 6.5.0 infers `uint256` for it (for example
  `getRoleAdmin(bytes32)` inferred `uint256`), so no candidate is argument-consistent. This is most
  of carrier n12 (TimelockController, 9 rows) and n15 (ENS registry, 9 rows).
- 3 rows: a `string` argument is inferred as `bytes` (`castVoteWithReason`, `propose`,
  `setBaseURI`).
- 3 rows: REA's arguments match, but openchain returns more than one unfiltered candidate with
  that argument list, so the rule abstains. `nonces(address)` competes with
  `_$_$$_$__$$$$$$$$__$__$$_$$$_$$$(address)`, `setApprovalForAll(address,bool)` with
  `niceFunctionHerePlzClick943230089(address,bool)`, and `token1()` with
  `detectabilityAntiauthoritarianism()` (`corpus/evidence/round-29/c1/db/openchain-7ecebe00.json`,
  `-a22cb465.json`, `-d21220a7.json`).

No row with an argument mismatch got a name (27 mismatches, 0 named). The abstention costs
recall; it never produced a wrong name here or in round 28.

## The filter step is inert on these rows

None of the 152 selectors is a key of the canonical list, so openchain marks every candidate
`filtered: false` (S084, S087; R29-C2 observed 0 of 199 entries on these selectors marked
filtered). The filter step therefore removes nothing; the abstentions above come from argument
consistency and from spam collisions that the canonical list does not cover.

## Reading against round 28

Round 28 (lane-invented names) gave named 137, right 137, wrong 0 with 50 no-name rows of 187.
Here, with published names, the rule names 122 of 152 (80%) and is still never wrong. On these
rows `openchain_first` is also never wrong (152/152), while `fourbyte_first` is wrong on 36: the
first 4byte.directory result is often a spam collision, so "take the first 4byte hit" is unsafe.

## Limits

- Carriers are compiled stubs that hold a published function list; they are not deployed contracts
  and carry no events or custom errors. One compiler (solcjs 0.8.37, no optimizer), one REA pin,
  one lookup snapshot.
- The screen removes selectors the lane has written down, not names the L1 or the databases'
  users know. The names are well known by design, so this measures the rule on public names; an
  obscure or private name is the round-28 case.
- `openchain_first` scoring 152/152 here is not a rule to adopt: it has no abstention, and on the
  round-25 rows it was wrong once where the primary rule was not
  (`corpus/evidence/round-25/a3/c2/analyze/tally.json`: named 62, right 61, wrong 1); in round 28
  it was not wrong (145/145).
- Only carrier n04's interface list has a source row (S088); the other 15 lists were written by
  the L1 from the published standards without opening them this round. The ground truth for
  every row is still the compiler ABI, not the standard text.

## Use

To name an EVM selector from bytecode, use the round-25 primary rule: take the only openchain
candidate with `filtered: false` whose parameter list matches REA's inferred arguments. Expect it
to abstain when an argument is `bytes32` (REA infers `uint256`) or `string` (REA infers `bytes`),
and when a spam name shares the same argument list. On these 152 fresh rows it named 80% and was
never wrong.
