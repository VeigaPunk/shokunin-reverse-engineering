# ReopenS088 — Re-open SOURCES row S088, match to carrier n04

Seat: `KaidokuR29.ReopenS088` (leaf, wave 1). Item: verify row S088 of
`corpus/SOURCES.md` (lane `corpus/SOURCES.md:94`) and the Gate row in
`corpus/lessons/round-29.md:30` against a fresh fetch, and compare the
spec's method list to `corpus/evidence/round-29/c1/compiled/Erc4626.abi.json`
at the measured tip `18be864a528873b2b70d8c94e31f880290249e90`.

All work read-only on the lane; fetched bytes and extracted ABI stored under
`/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReopenS088/`.

## Verdict: **admit**

Every checkable cell of S088 and its Gate row matches the re-fetched bytes,
and the spec's method set equals the n04 carrier's ABI function set exactly
(16/16 names, input-type sequences identical in order).

## Evidence

### 1. Fetch and hash (observation)

- Command: `curl -sS -L -o .../erc-4626.md https://raw.githubusercontent.com/ethereum/ERCs/3c0f7076cf20d70bdd6142f012d8e03322f4518c/ERCS/erc-4626.md`
  — HTTP 200, 24,417 bytes (separate `curl -w '%{http_code} %{size_download}'`
  probe at 2026-10-22T20:23:26Z). Exit 0.
- Command: `sha256sum erc-4626.md` →
  `698c05bff73bfb796f59cd7c4732edccdf7e40176f9bb027c19a0bbe7251e10a` — exit 0,
  2026-10-22T20:23Z. **Matches** the hash recorded in SOURCES row S088 and in
  the lesson Gate row.
- Access date: 2026-10-22. Source opened by ordinary means (plain curl GET);
  no bot challenge encountered.

### 2. Gate quote at `:18` (observation)

- Command: `sed -n '18p' erc-4626.md` →
  `This standard is an extension on the EIP-20 token that provides basic functionality for depositing`
- The lesson Gate row (`corpus/lessons/round-29.md:30`) records the quote
  `This standard is an extension on the EIP-20 token that provides basic
  functionality for depositing` at `:18`, Abstract — **exact match** with the
  served bytes, 17 words (≤ 25-word gate limit per QUALITY row 42
  convention). Line 18 is inside `## Abstract` (heading `:14`); the row's
  "Abstract" section label is correct.

### 3. Row-cell line references (observation)

Row S088 evidence cell claims: `## Specification` `:29`; per-method YAML
blocks from `asset` `:54` to `redeem` `:481`; `deposit` `:224-237` with
inputs `uint256 assets`, `address receiver`.

- `grep -n '^## Specification'` → `:29`. MATCH.
- `grep -n '^#### asset'` → `:54` (first method heading). MATCH.
- `grep -n '^#### redeem'` → `:462`; its ` ```yaml ` block runs `:480-:496`,
  with `- name: redeem` on `:481`. The row's `:481` cites the block's YAML
  name line, not the `####` heading — internally consistent as "from `asset`
  heading `:54` to `redeem` block `:481`", and the range covers all 16
  method blocks. Minor style note only; not a defect (observation +
  inference on convention).
- `deposit`: heading `:210`, YAML block `:223-:237`; the row's `:224-237`
  cites `- name: deposit` (`:224`) through the closing ` ``` ` (`:237`) —
  same convention as `redeem`. Inputs in block: `assets uint256`,
  `receiver address` (`:227-:230`). MATCH.
- Event blocks also exist: `Deposit` `:506-:523`, `Withdraw` `:531-:551`
  (headings `:500`, `:525`) — the row describes "per-method YAML blocks"
  and does not claim the events' absence; the events are out of the row's
  stated scope ("The published function list and argument types").
- `git ls-remote` re-check not part of this item's Work list (S087's item
  covered ls-remote); the row's pinned commit was fetched verbatim.

### 4. Method comparison: spec YAML vs n04 ABI (observation)

ABI extracted read-only:
`git -C <lane> show 18be864a…:corpus/evidence/round-29/c1/compiled/Erc4626.abi.json`
→ sha256 `0260e4e9cb7d872f87d0ede56fd492ac04f8793720aa1f80e67ad18a17d9f085`,
identical to the `n04` row's abi hash in
`corpus/evidence/round-29/c1/carriers.tsv:5`. Lane working-tree HEAD is
`18be864a…` (`git rev-parse HEAD`, read-only).

Parsing: regex ` ```yaml …``` ` over the served file → 18 blocks (16
functions + 2 events); `inputs:` name/type lists extracted per block.
ABI: 16 `type:"function"` entries, 0 events (param names stripped to
`a0…`, so comparison is on name + ordered input types only).

| # | Spec method (`####` line) | Spec input types | ABI input types | Verdict |
|---|---|---|---|---|
| 1 | `asset` (:54) | — | — | match |
| 2 | `totalAssets` (:74) | — | — | match |
| 3 | `convertToShares` (:96) | uint256 | uint256 | match |
| 4 | `convertToAssets` (:126) | uint256 | uint256 | match |
| 5 | `maxDeposit` (:156) | address | address | match |
| 6 | `previewDeposit` (:182) | uint256 | uint256 | match |
| 7 | `deposit` (:210) | uint256, address | uint256, address | match |
| 8 | `maxMint` (:239) | address | address | match |
| 9 | `previewMint` (:265) | uint256 | uint256 | match |
| 10 | `mint` (:293) | uint256, address | uint256, address | match |
| 11 | `maxWithdraw` (:322) | address | address | match |
| 12 | `previewWithdraw` (:346) | uint256 | uint256 | match |
| 13 | `withdraw` (:374) | uint256, address, address | uint256, address, address | match |
| 14 | `maxRedeem` (:410) | address | address | match |
| 15 | `previewRedeem` (:434) | uint256 | uint256 | match |
| 16 | `redeem` (:462) | uint256, address, address | uint256, address, address | match |

- Spec methods absent from ABI: **none**. ABI functions absent from spec:
  **none**. 16/16 = the row's "`Erc4626`, 16 functions" cell. MATCH.
- Spec events `Deposit` (inputs address,address,uint256,uint256) and
  `Withdraw` (address,address,address,uint256,uint256) have no ABI
  entries — consistent with `corpus/evidence/round-29/c1/src/Erc4626.sol`,
  which declares only the 16 functions and no events (`grep -n function`
  `:15-30`, all `external`, types matching the spec order). The ABI JSON
  contains no event entries at all. Not a mismatch — the row scopes S088
  to the function list.
- Spec `indexed` flags and output params are outside the comparison (the
  stripped ABI has no outputs); input types are the claim-relevant axis
  ("argument types", and selectors depend only on them).

### 5. Carrier identity (observation)

`carriers.tsv:5`: `n04 … compiled/Erc4626.abi.json … 0260e4e9…` — n04 ↔
`Erc4626` ↔ the spec's 16 methods. The row's claim "the source of R29-C1
carrier `n04`" is supported: the carrier source file implements exactly
the standard's function signatures (types and arity; names `a0/a1/a2`
are synthetic).

## Residual risk / gaps

- The spec's semantic requirements (MUST NOT revert, output names like
  `assets`/`shares`, event emission) are not exercised by an ABI
  comparison — out of scope for this row's stated claim.
- `:481` vs `####`-heading `:462` convention noted above; harmless.
- Outputs stripped in the carrier ABI, so the row's "argument types"
  claim is verified for inputs only; output-name cells (e.g.
  `assetTokenAddress`) were not checked against anything and make no
  claim about the ABI.

## Artifacts (sha256)

- `698c05bff73bfb796f59cd7c4732edccdf7e40176f9bb027c19a0bbe7251e10a` —
  `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReopenS088/erc-4626.md`
  (served bytes, 612 lines, 24,417 bytes)
- `0260e4e9cb7d872f87d0ede56fd492ac04f8793720aa1f80e67ad18a17d9f085` —
  `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReopenS088/Erc4626.abi.json`
  (`git show` output at measured tip)

## Tooling

No installs. Used preinstalled `curl`, `sha256sum`, `git` (read-only),
`python3` (regex/JSON parse). Pacman untouched per host pause.

No network lookups to 4byte.directory or openchain; no REA run.
