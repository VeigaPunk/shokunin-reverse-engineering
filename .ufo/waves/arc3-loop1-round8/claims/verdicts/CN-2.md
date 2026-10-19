# CN-2 — arc3-loop1-round8 verdict and reconciliation

Seat CN-2 · verdict/reconciliation · `kaidoku-shokunin` · 2026-10-19.

## Basis and disposition

Measured against checkout `HEAD=904b724258fc9396a016bd9952b5cd40225fb7d8`; the frozen work object resolves to `7deeb36045209f3fbeb4460edd7aef5b5270af22`. I re-derived the values below from the live config, source tree, scratch candidates under `/var/tmp`, and the R8 K8/Vyper evidence. Git was read-only. This seat wrote only this verdict; none of the gate, province, corpus, map, or receipt landing paths was changed.

**Overall: integration HOLD.** C1's reachability defect and a passing candidate/fault test are reproduced, but only in scratch. C2's live anchor and content hash are verified, but the source pointer and same-commit receipt are not landed. C3's bounded Vyper experiment and the 86/86 baseline are reproduced, but its entry and map token remain drafts; 87/87 has not been measured after landing.

## C1 — `ptr_check` reachability and candidate

**REPRODUCED — blind spot.** `.ufo/gates/c1-census-v10.py` is 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`. In `classify()` at lines 511–514, `PTR.finditer()` runs only under `if not occ`. The pin/version occurrence on `PROVINCE.md:18` therefore prevents its `~/.kimi-code/config.toml:3546` pointer from becoming an assertion. The source itself remains unchanged.

**VERIFIED — live and fault anchors.** The live config has 4,150 lines; the unique `rea-agents@` match is line 4126, `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. Direct helper checks returned `ptr_check(:3546)=stale`, `ptr_check(:4126)=ok (pins 6.7.0)`, and `ptr_check(:999999)=unresolved (line 999999 beyond EOF (4150 lines))`. The live-line content digest excluding LF is `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1`; including LF it is `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`.

**REPRODUCED — candidate behavior on scratch; NOT LANDED.** I independently reran the candidate gate copies and seeded-fault cases from EX-1, EX-2, PL-1, and RV-2, under `/var/tmp`:

- The unmodified current-HEAD gate exits 1 / FAIL on undeclared `SCORECARD.md:1776-1783` (R7 tail); it reports 14 G21 rows, no frontier errors, and 19 JSON keys.
- The clean candidate trees exit 0 / PASS after the candidate scope declaration and a scratch-only `PROVINCE.md:18` update to `:4126`. The proposed EX-1/PL-1 form collects all full pointers and treats stale DATED-scope pointers as historical; its bounded DATED row covers `SCORECARD.md:1759-1813`. It reports the unchanged base line/locus counts (PROVINCE `162/6`, SCORECARD `1813/10`, SKILL `413/2`), 14 G21 rows with no frontier errors, G2 true, and the same 19 JSON keys. The `current_ok_per_file` values become PROVINCE 20 / SCORECARD 17 / SKILL 3 because newly reachable assertions are now counted. Thus the output shape and census/G21 counts are preserved, but a literal requirement that every assertion counter retain its old numeric value would not be met.
- A seeded in-range re-key from `:4126` to `:3546` fails as `STALE`; an out-of-range re-key to `:999999` fails as `UNRESOLVED` / beyond EOF.

I recommend EX-1's broader collection with DATED-only historical fallback and its R7-tail scope declaration: it reaches the target while preserving dated-pointer treatment. EX-2/RV-2 use a narrower CURRENT filter/scope, so their `current_ok` counts differ (SCORECARD 15 rather than 17); this is not evidence that the assertion totals should remain frozen. Candidate patch and recorded detailed runs: `.ufo/waves/arc3-loop1-round8/claims/c1/EX-1.md:19-58,60-89`; other candidate reports are in `claims/c1/{EX-2,PL-1,RV-2}.md`.

**UNVERIFIABLE — integration acceptance.** No candidate gate change or `:4126` PROVINCE pointer is in the actual source tree, and no same-commit C1/C2 landing exists. The scratch PASS is conditional on both the proposed gate scope/collector changes and the simulated pointer correction; it does not satisfy the frozen landing condition by itself.

## C2 — PROVINCE pointer and receipt

**VERIFIED / CORRECTED — live anchor.** The current `PROVINCE.md:18` pointer is still `~/.kimi-code/config.toml:3546`, which is stale. The live line is `:4126` with `rea-agents@6.7.0`; its measured content hash is the value above. The proposed one-token substitution `:3546` → `:4126` is line-neutral: `PROVINCE.md` remains 162 lines and 19,908 bytes, and the changed line remains 198 bytes. The current pointer must be corrected to `:4126`.

**UNVERIFIABLE — same-commit landing.** CR-2's captured receipt text and hash are present at `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2/receipt.txt`, but the PROVINCE edit and a canonical `.ufo/receipts/` receipt have not landed with C1. A seat receipt is evidence/proposal, not proof of the required same-commit record. The whole-config digest was not captured or claimed.

**DISCREPANCY — receipt chronology.** CR-2 records capture time `2026-10-19T17:55:09Z`, while the existing PROVINCE prose calls a `17:55:49Z` receipt historical. The cited event is 40 seconds later than that capture. This chronology discrepancy is unresolved and should be explicitly checked at integration; it does not alter the live line or its content hash.

Patch and receipt details: `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2.md:7-11,33-63` and `claims/c2/CR-2/receipt.txt`.

## C3 — Vyper optimizer-form Unknown

**REPRODUCED — bounded experiment.** I freshly compiled the retained synthetic K8 source with Vyper `0.4.3+commit.bff19ea2` and ran the retained REA 6.7.0 probes. Eight independently Keccak-derived selectors matched compiler method identifiers and all three REA result sets (8/8); decoded runtime hashes matched the fresh output. The no-optimize runtime is 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`, with eight `PUSH4; DUP2; EQ; ISZERO; PUSH2; JUMPI` legs. Its offsets are PUSH4 PC + 12 and land on CALLVALUE.

The codesize runtime is 360 bytes, SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`; it has no opcode-boundary PUSH4, one EQ, one MOD, and two CODECOPY operations. The first CODECOPY copies 27 bytes from `0x12b`, but the **full tail at `0x12b` is 61 bytes**: a 5-byte header plus eight 7-byte selector/target/`0x25` records. All eight selectors match and every target is a JUMPDEST. REA reports shared offset 65 (`DUP1`) for the selectors, not their distinct table targets. The 27-byte copied prefix is not the full table-tail size.

Scope is limited to this synthetic source and Vyper 0.4.3; REA output is static inference, not execution evidence. The compiler ABI says `view`, while REA infers `payable` (0/8 agreement), so mutability is not established.

**VERIFIED — Command A baseline; UNVERIFIABLE — post-landing count.** I independently ran the `SCORECARD.md:88-124` recipe at HEAD and the frozen work commit. Both return 86 knowledge files, 86 mapped, `missing=[]`, `dangling=[]`, and 15/15 citation-resolved rules. An in-memory projection adding a proposed filename and map token gives 87/87, but it is only a projection, not a landing measurement.

**Recommendation and integration boundary.** Use EX-8's R8 draft/token, `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes`, as the one canonical entry: it reconciles the alternative R7 names, freshly tests both `--no-optimize` and `-O none` (byte-identical for this fixture), and carries the bounded evidence. The entry remains a draft at `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/entry-draft.md`; no corpus entry/map token is landed and actual 87/87 remains unverified. Evidence and exact measurements: `claims/c3/EX-8/evidence/measure.txt:1-40`, `command-a-before.txt:1-19`; draft limitations at `claims/c3/EX-8/entry-draft.md:9-17`.

## Integration handoff

1. Integrate the recommended C1 collector/scope patch and C2 pointer/receipt together; remeasure the live line and recompute the receipt at the actual landing revision. Resolve the timestamp chronology discrepancy.
2. Run the C1 clean and seeded-fault checks against the exact combined candidate; confirm G21/JSON contract and note that newly detected assertions change `current_ok_per_file`.
3. Land only the EX-8 corpus entry and matching map token, then run Command A at that commit. Do not report the projected 87/87 as measured before this run.
