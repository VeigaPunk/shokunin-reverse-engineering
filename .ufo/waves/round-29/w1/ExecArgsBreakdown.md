# R29-C1 no-name rows: argument breakdown

## Scope and evidence

Classified the 30 primary-rule abstentions using the committed `tally.json` and selector-specific OpenChain responses at `18be864a528873b2b70d8c94e31f880290249e90`. The classifier reads each input via read-only `git show`; no live lookup or REA run was made. Entry statements checked: `corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md:48-63`.

Producing command: `python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecArgsBreakdown/classify.py` — exit 0; classifier timestamp `2026-10-22T20:22:01Z`. Exact stdout excerpts:

```text
source_rev=18be864a528873b2b70d8c94e31f880290249e90 tally=corpus/evidence/round-29/c1/tally.json primary=openchain_sole_unfiltered_args_consistent no_name_rows=30
7ecebe00 nonces(address) address tie: multiple unfiltered candidates arguments match nonces(address) | _$_$$_$__$$$$$$$$__$__$$_$$$_$$$(address)
a22cb465 setApprovalForAll(address,bool) address,bool tie: multiple unfiltered candidates arguments match setApprovalForAll(address,bool) | niceFunctionHerePlzClick943230089(address,bool)
d21220a7 token1() <empty> tie: multiple unfiltered candidates arguments match token1() | detectabilityAntiauthoritarianism()
da95691a propose(address[],uint256[],string[],bytes[],string) address[],uint256[],bytes[],bytes[],bytes other argument mismatch string[]->bytes[],string->bytes <none>
classification_counts={"bytes32 as uint256": 24, "other argument mismatch": 1, "string as bytes": 2, "tie: multiple unfiltered candidates": 3}
summary=rows=30 classified=30
```

In the excerpt, columns are tab-separated. `matching_unfiltered_candidates` lists only candidates with `filtered: false` whose parameter types equal the inferred list. The script compares every no-name row's ABI and inferred parameter lists and reads the associated pinned OpenChain response.

## Classification table

These are disjoint row groups; `propose` is separated because it has both a scalar and an array mismatch.

| Row classification | Rows | Selectors / ABI function |
|---|---:|---|
| ABI `bytes32` inferred as `uint256` | 24 | `d505accf` permit; `248a9ca3` getRoleAdmin; `2f2ff15d` grantRole; `36568abe` renounceRole; `91d14854` hasRole; `d547741f` revokeRole; `01d5062a` schedule; `134008d3` execute; `13bc9f20` isOperationReady; `2ab0f529` isOperationDone; `31d50750` isOperation; `584b153e` isOperationPending; `8065657f` hashOperation; `c4d252f5` cancel; `d45c4435` getTimestamp; `0178b8bf` resolver; `02571be3` owner; `06ab5923` setSubnodeOwner; `14ab9038` setTTL; `16a25cbd` ttl; `1896f70a` setResolver; `5b0fc9c3` setOwner; `cf408823` setRecord; `f79fe538` recordExists. |
| ABI `string` inferred as `bytes`, with no additional differing argument | 2 | `7b3c71d3` castVoteWithReason; `55f804b3` setBaseURI. |
| ABI `string[]` inferred as `bytes[]`, and ABI `string` inferred as `bytes` | 1 | `da95691a` propose. |
| Inferred arguments match, but multiple unfiltered candidates have that parameter list | 3 | `7ecebe00` nonces; `a22cb465` setApprovalForAll; `d21220a7` token1. |
| Other reason / other argument mismatch | 0 | — |

Totals: 24 + 2 + 1 + 3 = 30. Thus there are 27 ABI/inference mismatch rows; three rows match arguments but abstain on ties. The three rows containing a scalar `string`→`bytes` mismatch are castVoteWithReason, propose, and setBaseURI.

## Entry claim check and verdict

- **24 bytes32 rows:** holds. The 24 selectors above have only `bytes32`→`uint256` type differences (some rows have two such parameters). The cited `getRoleAdmin(bytes32)` example is accurate. The cited concentration—9 TimelockController rows (`n12`) and 9 ENS registry rows (`n15`)—also matches the row list; the other six are one `permit` row and five `n05` rows.
- **3 string-as-bytes rows:** the count holds if it means rows with a scalar `string`→`bytes` mismatch. One row is under-described: `propose` also changes `string[]` to `bytes[]`. This is an additional mismatch within that row, not an extra row; it does not change the 27-row mismatch total.
- **3 ties:** holds. The named tied candidates are exact: `nonces(address)` / `_$_$$_$__$$$$$$$$__$__$$_$$$_$$$(address)`, `setApprovalForAll(address,bool)` / `niceFunctionHerePlzClick943230089(address,bool)`, and `token1()` / `detectabilityAntiauthoritarianism()`. Each pair is unfiltered and has matching parameter types. Other unfiltered candidates in those responses have different parameter lists and do not add to the tie.

**Verdict:** the counts and named examples hold. The entry's explanation is incomplete for the `propose` row because it omits the `string[]`→`bytes[]` mismatch; it does correctly identify that row's scalar `string`→`bytes` mismatch.

## Files and tooling

- Lane file changed: `.ufo/waves/round-29/w1/ExecArgsBreakdown.md` (this report only).
- Scratch analysis artifact: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecArgsBreakdown/classify.py` — SHA-256 `a3b320f78c5b67a9fa7e9803c0d2b53024de71caa61ad7f39025b57e6e273507`.
- No tools installed or updated. No builds, tests, linters, formatters, network requests, or REA runs.
