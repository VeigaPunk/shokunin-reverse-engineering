# PriorEvmEntries — the R25 naming entry against the eight prior EVM entries

Seat `KaidokuR25a3.PriorEvmEntries`, 2026-10-22. Object: `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`. Prior entries are the eight tokens in the README `EVM` row (`corpus/README.md:38`); the new entry has its own row at `corpus/README.md:74`. Verdicts are review judgments; every observation names its command or file.

Revisions compared, because the lane file changed under this read-only seat: **CLAIM** = commit `08c7a72`, `git show HEAD:<file>` blob `3a888b15…`, 109 lines. **WT** = working tree at 2026-10-22T10:56Z, sha256 `9d4361f8d0b506e65b02dbf6f89258feef3d3fdc5b906c74c8717584877de641`, 164 lines, `git status --porcelain` = ` M …/2026-10-22-r25-evm-selector-name-resolution.md`; it also read `fed299eb…` at 10:54Z, so it is being edited live by another party. I made no lane write.

| axis attacked | verdict |
|---|---|
| Carrier/compiler census | **FAILS on CLAIM** (one Vyper carrier where the corpus records two); fixed in WT |
| Vyper argument inference | Fact holds; prior measurement uncited and scope understated on CLAIM `[both]` |
| Dispatch shapes | Holds; no shape claim, none contradicted; the K/K completeness warrant is uncited `[both]` |
| Fallback misses | No bearing on naming; no contradiction. r4's phantom `__default__()` is the relevant fact, uncited `[both]` |
| Evidence-id domain | Byte-equality holds; it is same-path determinism, not corroboration; r7 uncited `[both]` |
| Table counts | Holds — all five rows reproduce exactly from saved evidence |

## 1. Carrier/compiler census — contradiction (CLAIM), fixed in WT

CLAIM `:35-36` lists "two solc ERC-20 shapes, an optimizer-200 vault, two carrier contracts, one Vyper token". `corpus/evidence/round-25/a2/c2/carriers.tsv` plus the sources show **four solc and two Vyper** carriers: `stewardtoken` is `token.vy` (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/token.vy`, compile receipt `compile-receipt.txt`) and `carrierv` is `CarrierV.vy` (`…/EX-04/src/CarrierV.vy`), both built by `vyper 0.4.3+commit.bff19ea2` (`2026-10-19-arc3-r4-evm-vyper-leg.md:11`); `carrierb` is the solc-0.8.37 optimizer-200 contract (`2026-10-19-arc3-r3-evm-optimizer-shapes.md:22`). Consequence: CLAIM's Vyper error pattern ("On the Vyper token", `:90`) covers 22 of 69 rows when 37 of 69 are Vyper. WT `:38-40` states the correct split.
The pins the ground truth depends on: solc `0.8.37+commit.f401782d` (`2026-10-19-arc3-r1-evm-real-solc.md:11`) and Vyper `0.4.3+commit.bff19ea2` (`…-r4-evm-vyper-leg.md:11`). WT now names "solc 0.8.37 and Vyper 0.4.3" in a limit (WT:146-147), without the commit-hash pins.

## 2. Vyper argument inference — fact holds, prior measurement uncited

CLAIM `:90-95` presents one incident ("On the Vyper token, REA inferred `uint256,uint256` for `0xa9059cbb` … it was wrong here"). The corpus measured the class: `…-r4-evm-vyper-leg.md:24` records `inferred_arguments` on the Vyper family reading `uint256` for `address` parameters, "the same divergence class noted on solc carriers", including the Ex09Vault repeat (2 of 7). My run over the six saved envelopes: 57 of 69 rows equal, 12 divergent — 8 of 8 address-argument rows on `stewardtoken`, 3 of 3 on `carrierv` (all read `uint256` for `address`), plus solc `carrierb`'s `note(bytes32,uint256)` read as `uint256,uint256`. WT `:107-110` adds the same 12-of-69 count (11 on the two Vyper carriers) plus a traced cause, but still cites no prior entry, and the cause does not change that the divergence itself was already corpus knowledge.
This qualifies the decision rule, not just the citation. Rules 2/5 filter on "the candidate's parameter list matches REA's inference" (`tools/round-25/a2/resolve-selectors.py:185-190`), a conjunction with an inference the corpus already knows is wrong on every address-argument row of these carriers. Rule 5 named 12 of 22 `stewardtoken` rows and 8 of 15 `carrierv` rows — all rows whose REA arguments equalled the ABI, since a "right" name forces that equality. The 49/49 result is not a property of the rule independent of REA.

## 3. Dispatch shapes — holds; the 69-row warrant is uncited

The entry makes no dispatcher-shape claim and uses no `bytecode_offset` (the resolver keeps only selector, arguments and mutability, `resolve-selectors.py:115-121`). That is the safe choice: the corpus records five offset readings (`2026-10-13-r3-evm-interface.md:149-155`; `…-r4-evm-vyper-leg.md:22`; `…-r6-viair-dispatch-shape.md:24`; `…-r8-vyper-optimizer-dispatch-shapes.md:13-14`).
Missing is why 69 is the complete denominator. It is exactly the six carrier sets the prior entries measured K/K against planted selectors: 5/5 and 6/6 (`…-r1-evm-real-solc.md:17,23`), 13/13 and 8/8 (`…-r3-evm-optimizer-shapes.md:19,22`), 15/15 and 22/22 (`…-r4-evm-vyper-leg.md:19,20`); `tally.json` `carriers` shows 5/6/13/8/22/15. Rows are REA's output, so a shape-blocked miss would silently shrink the sample; the K/K record is what rules that out, and the extractor is shape-sensitive (r3:28; r4:21; r6:22).

## 4. Fallback misses — no bearing, no contradiction

`2026-10-19-arc3-r9-viair-fallback-miss.md:9-15` is scoped to the solc-0.8.37 viaIR final `SUB`-leg miss branch. None of the six carriers is viaIR (r1/r3/r4 pins), so r9 supports nothing here and needs no citation. Four ABIs do carry `fallback`/`receive` entries (VaultB, CarrierB both; `stewardtoken`, `carrierv` `fallback`), and r3/r4 measured those carriers K/K, so a fallback adds no selector row. The fallback-adjacent fact worth citing is `…-r4-evm-vyper-leg.md:23`: vyper `method_identifiers` carries a phantom `__default__()` (`89402a72`) absent from the runtime. The entry's ground truth is the ABI, and `abi_signatures` filters `type == "function"` (`resolve-selectors.py:104-111`), correctly excluding it; `method_identifiers` would have made 70 rows on these carriers.

## 5. Evidence-id domain — byte-equality holds, weight and version scope unstated

CLAIM `:2`: "REA `rea-agents@6.5.0` envelopes replayed byte-equal". Verified: all six saved envelopes and replays are byte-identical (sha256 plus `cmp`, 10:54:08Z), and `parameters.path` is identical because the replay used the same absolute carrier paths. That is what `2026-10-19-arc3-r7-evm-evidence-id-domain.md:9-11,17-18,22` predicts (the id hashes a projection containing `parameters.path`; same path and request re-derive, another path mints another id), and `…-r4-evm-vyper-leg.md:26` names it "same-path determinism, not independent corroboration". The replay does establish something the entry omits: the saved envelopes' `environment` is `null`, so the 6.5.0 producer pin rests on the replay.
Two scope cautions from r7: the formula was derived for 6.4.0 and 6.7.0 only (`r7:26`), and the 6.5.0 envelope already contains `relationship_coverage` (observed key list), the field r7:11 places outside the 6.4.0 projection. The entry makes no formula claim, so nothing is wrong; but "byte-equal" should carry the same-path qualifier and a note that these ids are not comparable to the prior entries' 6.4.0/6.7.0 ids (compare decoded `bytecode.sha256` and payload, as `…-r1-evm-real-solc.md:7` and `…-r6-viair-dispatch-shape.md:30` say). WT's new 6.7.0 paragraph cites a seat report, not r7.
Reproducibility gap: `recheck:` runs only the offline tally, while the REA leg needs a disk-backed `TMPDIR` (a `/tmp`-defaulted run fails EDQUOT, errno -122), standing since `…-r1-evm-real-solc.md:7` and repeated at `…-arc3-r3-evm-optimizer-shapes.md:7` and `…-r4-evm-vyper-leg.md:7`; `corpus/evidence/round-25/a3/c2/rea-replay/runs.txt` records argv but not `TMPDIR`.

## 6. Counts — hold

My independent aggregation over the saved evidence and ABIs reproduces the CLAIM table exactly: 59/33/26/10, 48/47/1/21, 62/61/1/7, 55/54/1/14, 49/49/0/20. The distinct-selector block in `tally.json` matches WT's bracketed numbers. No arithmetic conflict with any prior entry.

## 7. Minor mismatches against its own cited evidence (not prior-entry conflicts)

- `:37` / WT `:42` — "138 … per selector": the 138 files are 2 × 69 carrier-selector rows (69 4byte + 69 openchain, counted), not 2 × 43 distinct selectors (86). Write "per carrier-selector row"; both revisions still say "per selector".
- `:2`, `:102` / WT `:142` — "08:28Z–08:30Z": all 138 manifest entries are status 200 with matching sha256, and the range is `08:28:09Z`–`08:31:37Z`.
- `:9` — quotes PROVINCE "selectors stay bare hashes (no signature DB → no name resolution)"; that text is `PROVINCE.md:93` at baseline `18e7eb6` and claims-freeze `7ef837a`, and is absent from the working tree because the C2 commit replaced it. Anchor the quote to `7ef837a:93`.
- `:51` — the table label drops "keccak and" from the tool's rule text (`tally-resolution.py:26`, "whose keccak and parameter list match REA"), describing a different rule than the one scored.
- `:69-71` — the ordering rationale is borne out on the saved `transfer` page: ids descend `1111734 … 145`, first result `workMyDirefulOwner(uint256,uint256)`, true name last (`corpus/evidence/round-25/a2/c2/stewardtoken/db/4byte-a9059cbb-p0.json`). No prior entry contradicts it; keep it as an observation with that page as the pointer.

## 8. Facts the entry should cite (all verified in the prior entries)

- Compiler pins: r1:11 (solc 0.8.37+commit.f401782d); r4:11 (Vyper 0.4.3+commit.bff19ea2).
- Per-carrier K/K warrant: r1:17,23; arc3-r3:19,22; r4:19,20.
- Vyper argument-type divergence: r4:24 (includes the Ex09Vault repeat).
- ABI-not-method_identifiers choice: r4:23 (phantom `__default__()`).
- ev_ identity and path sensitivity: r7:9-11,17-18,22,26; r4:26; arc3-r3:30.
- Tool returns no names / bare-hash premise: `2026-10-13-r3-evm-interface.md:68,142-143`.
- Keccak provenance: `resolve-selectors.py:5` names RV-1's `keccak_ref.py`; r1:27 records RV-1's two independent oracles and ERC-20 vector table.
- TMPDIR/EDQUOT: r1:7; arc3-r3:7; r4:7.

## 9. Working-tree drift (recorded, not judged as a claim)

WT fixes the census (1), adds the 12-of-69 count and cause (2), distinct-selector brackets, `hasVerifiedContract`, filter=true, 6.7.0 and live re-fetch paragraphs, S078 (`corpus/SOURCES.md:84`) and a seat-report note. Its new claims are sourced to seat reports (`.ufo/waves/round-25/a3/w1/{C2EvmoleDirect,C2Rea67,VyperArgsCause,C2LiveDrift,CarrierProvenance}.md`), not retained envelopes; prior entries support claims from retained envelopes, so those additions need evidence paths before they are claim-grade. Unresolved in WT: the r4/r7/r3 citations, the 138 wording, the 08:30Z bound, the PROVINCE anchor, the replay's same-path weight, `TMPDIR`.

## Producing commands and artifacts

All times UTC; read-only; exit codes recorded.
- `python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/KaidokuR25a3.PriorEvmEntries/compare.py` (2026-10-22T10:53:52Z, exit 0): `TOTAL rows 69 rea_args_eq_abi 57 divergent 12`; `address-arg rows 25 divergent 11`; the five `AGG` lines quoted above. Each row came from `python3 -I -B tools/round-25/a2/resolve-selectors.py analyze` over the saved envelope, saved responses and carrier ABI; output retained in `compare.out`.
- Envelope identity loop over the six carriers (2026-10-22T10:54:08Z): six `BYTE-IDENTICAL` lines, saved digest e.g. `stewardtoken 1de20e9604885579…`.
- Manifest audit (2026-10-22T10:50:19Z, exit 0): `entries 138 min 2026-10-22T08:28:09Z max 2026-10-22T08:31:37Z bad_status [] bad_hash []`.
- Read-only git: `git show 18e7eb6:PROVINCE.md | grep -n 'bare hashes'` → `93:`; `git show 7ef837a:PROVINCE.md | grep -n` → `93:`; working-tree `grep` → exit 1; `git show HEAD:<entry> | wc -l` → `109`; `stat` plus `git status --porcelain` for WT drift.

Artifacts under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/KaidokuR25a3.PriorEvmEntries/`:
- `compare.py` sha256 `9871d6af76a5bd582751b1f63c7fb76ae5ab2e2e00012a29dfab2bf4a7bb7147`
- `compare.out` sha256 `f6be7ca26f29b1be53424693d5d3b77bf860f7f6fdd2864e981de419a5d5ac27`
- `envelope-identity.txt` sha256 `aa805d53a6ac05e4555845f90bd1f4af34f5a961dea5407c3f24e6df4371afb0`

No tools were installed or upgraded; no web page was opened. Remaining unknown: whether the rule rates hold on carriers outside these six — outside this seat's question.
