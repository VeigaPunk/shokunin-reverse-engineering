# CN-1 — arc3-loop1-round8 reconciliation verdict

## Basis and disposition

I measured the current checkout (`HEAD=904b724258fc9396a016bd9952b5cd40225fb7d8`) and resolved frozen work object (`7deeb36045209f3fbeb4460edd7aef5b5270af22`), rechecked the current gate and Command A, and reconciled the delivered C1/C2/C3 reports. The working tree still has no C1, C2, or C3 landing. **Overall: integration HOLD.** C1's blind spot and candidate behavior are reproduced on scratch, C2's live locator is verified but its correction is not landed, and C3's bounded experiment is reproduced but its corpus entry/map token and 87/87 after-measurement are pending.

This verdict is the only file written by this seat. I did not change the gate, `PROVINCE.md`, corpus, receipt path, `SKILL.md`, `SCORECARD.md`, or `LOG.md`; the pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification is untouched. The local `AGENTS.md` asks for a LOG entry, but the frozen wave write fence permits only this verdict artifact, so no LOG change is made.

## C1 — operability: `ptr_check` reachability

**REPRODUCED — baseline collector blind spot.** The current gate is 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`. In `.ufo/gates/c1-census-v10.py:511-514`, pointer matches are collected only under `if not occ`; the pin/version already in the `PROVINCE.md:18` unit therefore suppresses the full path pointer. Direct classification returns no pointer assertion for that line. The actual live/dead helper checks are:

```text
ptr_check(config.toml:3546)=stale; line holds no rea-agents pin: 'max_output_size = 64000'
ptr_check(config.toml:4126)=ok; pins 6.7.0
ptr_check(config.toml:999999)=unresolved; line 999999 beyond EOF (4150 lines)
```

**DISCREPANCY — current HEAD baseline is not PASS.** I reran `python3 .ufo/gates/c1-census-v10.py --json` at HEAD; it exits 1 / `FAIL` before any R8 source landing. The single undeclared unit is `SCORECARD.md:1776-1783`, with ambiguous `6.4.0` and `6.7.0` assertions at line 1780. Current counts are PROVINCE `162 lines/6 loci`, SCORECARD `1813/10`, SKILL `413/2`; G21 is 14 rows with no errors and G2 is true. The frozen work object has a different SCORECARD extent (1,757 lines / 9 loci) and its unmodified gate baseline passes; the failure is the R7 record now present on HEAD, beyond the declared SCORECARD scope ending at gate lines 274-276.

```text
HEAD=904b724258fc9396a016bd9952b5cd40225fb7d8
work=7deeb36045209f3fbeb4460edd7aef5b5270af22
baseline verdict=FAIL; undeclared=SCORECARD.md:1776-1783; G21=14/errors=0; G2=true
```

**REPRODUCED — candidate patch and seeded-fault behavior on scratch; UNVERIFIABLE — landing.** EX-1/PL-1 and EX-2/RV-2 each provide candidate behavior that, paired with a scratch-only `PROVINCE.md:18` re-anchor, returns clean PASS and fails a seeded dead pointer. I independently reconstructed and ran the narrow RV-2 form against current HEAD; CR-4 independently reran the same candidate (SHA-256 `1cc82e78c91700966b9ffb68239a8c878359521121ad24dafa733f49278a0d83`) and reproduced PASS on the simulated `:4126` anchor and UNRESOLVED/FAIL on `:999999`. CN-2 separately reran the broader EX-1/PL-1 candidate with the same clean/fault outcomes. These are scratch results, not a committed gate change.

**DISCREPANCY — candidate scope and receipt contract need reconciliation.** EX-1/PL-1 declare the entire dated R7 SCORECARD record (`1759-1813`, marker at its heading `1759`) and apply a stale-pointer-to-historical fallback for `DATED` scope. RV-2 limits collection to `CURRENT` pointers when a unit already has another locus and adds a narrow `1776-1783` `DATED` row (marker `1777`). CR-4 prefers RV-2's smaller behavior change; CN-2 prefers EX-1/PL-1's whole-record boundary. Both were tested on scratch; they are not equivalent and their hunks should not be mixed without a new full test. Gate lines `.ufo/gates/c1-census-v10.py:41-45` require an appended bound to be re-keyed as a DATED row with the section's own round/date marker; confirm whether RV-2's line-1777 marker meets that convention, or use the heading marker with a newly tested minimal collector patch. RV-1 leaves the independent HEAD scope failure unresolved; PL-2's clean result is on the older work snapshot, while its current-HEAD run still fails on the R7 block. See `.ufo/waves/arc3-loop1-round8/claims/c1/EX-1.md`, `.ufo/waves/arc3-loop1-round8/claims/c1/EX-2.md`, `.ufo/waves/arc3-loop1-round8/claims/c1/PL-1.md`, `.ufo/waves/arc3-loop1-round8/claims/c1/PL-2.md`, `.ufo/waves/arc3-loop1-round8/claims/c1/RV-1.md`, `.ufo/waves/arc3-loop1-round8/claims/c1/RV-2.md`, `.ufo/waves/arc3-loop1-round8/claims/verdicts/CN-2.md`, and `.ufo/waves/arc3-loop1-round8/claims/verdicts/CR-4.md`.

The R8 candidates both call live `ptr_check()` and the tested scratch case therefore grades `:4126` as `current-ok`; the R7 EX-1 candidate instead included a receipt-file digest check, and R7 RV-2 carried an explicit receipt tuple. No delivered R8 candidate demonstrates a gate-side read/validation of the new C2 line-content receipt. The frozen C1/C2 wording says the receipt anchor must exist for the instrument to grade it, but does not unambiguously say whether the gate itself must validate that hash. If gate-side validation is required, the R8 scratch PASSes do not meet that part; if a same-commit durable receipt is an evidence companion and live `ptr_check()` is the grade, it remains a landing prerequisite. Resolve this interpretation before accepting C1; do not represent the two roles as equivalent.

**DISCREPANCY — counter wording.** The tested candidate forms preserve the 19-key JSON schema, `counts`/line-locus totals, G21 (14/no errors), and G2. They correctly increase `current_ok_per_file` from `17/14/3` to `20/17/3` for EX-1/PL-1 (or `20/15/3` for RV-2), because previously unreachable assertions are newly counted. Thus “all existing counters intact” is satisfied as preserved fields/structural counters, not as bit-for-bit equality of every numeric current-ok value. If the frozen wording means identical numeric current-ok counts, that stricter condition is not met and must be resolved rather than hidden.

**UNVERIFIABLE — C1 acceptance/landing.** No candidate gate patch, live-pointer correction, durable receipt, or seeded-fault test on a landed combined revision exists in the checkout. Resolve the candidate/receipt interpretation, then rerun the exact chosen patch with C2 on the actual landing revision before accepting C1.

## C2 — freshness: live pointer and receipt

**VERIFIED — live anchor and hash.** The current 4,150-line Kimi config has one `rea-agents@` match at line 4126:

```text
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
sha256(line content, excluding LF)=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
sha256(line record, including LF)=eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
```

`PROVINCE.md:18` still cites `~/.kimi-code/config.toml:3546`, which resolves to `max_output_size = 64000`, not the REA pin. The proposed one-token change `:3546` → `:4126` is line-neutral: one occurrence on line 18 changes; line count remains 162; file size remains 19,908 bytes; changed line remains 198 bytes. The C2 reports `.ufo/waves/arc3-loop1-round8/claims/c2/EX-3.md`, `.ufo/waves/arc3-loop1-round8/claims/c2/EX-4.md`, `.ufo/waves/arc3-loop1-round8/claims/c2/EX-5.md`, `.ufo/waves/arc3-loop1-round8/claims/c2/EX-6.md`, `.ufo/waves/arc3-loop1-round8/claims/c2/CR-1.md`, and `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2.md` independently agree on the live target and content hash.

**DISCREPANCY — frozen scope description.** `.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-45` calls `PROVINCE.md:15-26` DATED, but the actual gate declares it CURRENT at `.ufo/gates/c1-census-v10.py:255-257`. The live instrument therefore must evaluate line 18 against the current config; it cannot waive the stale locator as historical. This scope correction is consistent with the requested live `ptr_check()` result.

**CORRECTED — proposed pointer; UNVERIFIABLE — source/receipt landing.** The proposed correction is supported by the live line and hash, but the tracked source remains stale and the receipts remain seat artifacts. CR-2's receipt is present at `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2/receipt.txt`; `.ufo/receipts/` is absent. No same-commit C1/C2 landing has been made, so no report may claim the receipt is yet a durable instrument anchor.

**DISCREPANCY — receipt chronology.** CR-2 records capture `2026-10-19T17:55:09Z`, while `PROVINCE.md:18` calls the `17:55:49Z` receipt historical. The capture precedes that cited time by 40 seconds. Current UTC at this review is `2026-10-19T18:06:11Z`, so the named time has since elapsed; that does not establish that the receipt existed at the earlier capture. Reconcile or re-derive the timestamp at integration. This does not change the verified `:4126` locator or hash.

## C3 — coverage: one corpus Unknown

**REPRODUCED — bounded K8/Vyper experiment.** The selected open question is at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`. The independent builds in `.ufo/waves/arc3-loop1-round8/claims/c3/EX-7.md`, `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8.md`, `.ufo/waves/arc3-loop1-round8/claims/c3/SC-1.md`, `.ufo/waves/arc3-loop1-round8/claims/c3/SC-2.md`, `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3.md`, and `.ufo/waves/arc3-loop1-round8/claims/verdicts/CR-3.md`, plus EX-9's recheck, agree on the synthetic K8 fixture, Vyper `0.4.3+commit.bff19ea2`, and eight selector matches. Source SHA-256 is `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; compiler executable SHA-256 is `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`.

```text
--no-optimize runtime: 617 B; SHA-256 1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
-O codesize runtime: 360 B; SHA-256 bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5
selectors: 8 ABI = 8 method IDs = 8 REA rows
noopt: 8 opcode-boundary PUSH4 / EQ selector legs
codesize: PUSH4=0, EQ=1, MOD=1, CODECOPY=2; 61-byte tail at 0x12b
noopt == -O none: byte-identical for this fixture/compiler
```

The codesize tail is a 5-byte header plus eight 7-byte selector/target/`0x25` records; each target is a JUMPDEST. EX-9's fresh output also measures a distinct `-O gas` control. This is evidence only for the retained synthetic source/compiler/options, not general Vyper behavior or execution: REA labels are inferred, mutability disagrees with the ABI (view vs payable, 0/8), and no runtime execution/deployment check is claimed. See `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8.md:11-20`, `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3.md:11-21`, and `.ufo/waves/arc3-loop1-round8/claims/c3/EX-9/recheck-output.txt:8-58` for the detailed byte-walk and envelopes.

**VERIFIED — Command A baseline; UNVERIFIABLE — post-landing coverage.** I reran the SCORECARD recipe (`SCORECARD.md:88-124`) against both HEAD and the frozen work commit. Both return 86 knowledge files, 86 mapped, no missing/dangling tokens, and 15/15 citation rules:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"904b724258fc9396a016bd9952b5cd40225fb7d8","rule_blocks":15}
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"7deeb36045209f3fbeb4460edd7aef5b5270af22","rule_blocks":15}
```

An in-memory entry/map projection is not a Command A after-run; no actual 87/87 is established. No delivered corpus draft is ready to copy verbatim. EX-8 (`.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/entry-draft.md`) freshly tests `-O none` against `--no-optimize`, but its source inventory at line 1 lists `rederive.sh` and `measure.py` under `evidence/` although the files are at the EX-8 artifact root. SC-1 (`.ufo/waves/arc3-loop1-round8/claims/c3/SC-1/entry-draft.md`) has a narrower two-option scope and valid recheck paths, but the entry itself does not give the absolute source path required by `corpus/QUALITY.md:14`. RV-3 (`.ufo/waves/arc3-loop1-round8/claims/c3/RV-3.md:42-77`) gives the absolute K8 source path and hash and reconciles the 27-byte prefix/61-byte full-tail distinction, but proposes an R7-stamped token and has shorthand evidence paths/counts that need review. All three drafts make numeric claims without consistently applying the corpus rule `<number> — <command> <date>` (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:33-37`).

**Reconciliation:** land exactly one corrected entry, preferably with the shared R8 destination/token `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes` proposed by EX-8 and SC-1. Use the fresh EX-8/EX-9 evidence for the fixture-scoped `-O none` equality if retained; retain RV-3's absolute source identity and 61-byte full-tail reconciliation; correct every source/evidence path and attach the required command/date to each count before landing. EX-7 proposes `...arc3-r8-vyper-optimizer-forms`; SC-2/RV-3 propose the competing `...arc3-r7-vyper-optimizer-forms`. These are alternative names for the same investigation, not separate Unknowns. Do not land multiple entries/tokens. Then run Command A against the actual commit.

**UNVERIFIABLE — C3 landing/claim closure.** No corpus entry or matching map token has landed; the corpus coverage claim remains open despite reproduced research evidence.

## Peer reconciliation and integration order

- CN-2 (`.ufo/waves/arc3-loop1-round8/claims/verdicts/CN-2.md`) agrees on HOLD and selects EX-1/PL-1 for C1 and EX-8 for C3. CR-4 (`.ufo/waves/arc3-loop1-round8/claims/verdicts/CR-4.md`) selects RV-2 and SC-1 and flags receipt-binding ambiguity; CR-3 (`.ufo/waves/arc3-loop1-round8/claims/verdicts/CR-3.md`) also prefers RV-2 and recommends RV-3 as a technical draft base, subject to corpus-contract fixes. Thus C1 has competing tested scope variants; C3 has competing draft texts and names, with EX-8/SC-1 sharing the R8 destination/token. VZ-1/VZ-2's earlier “not present” statements are point-in-time snapshots superseded by later deliveries.
- Final inventory includes C1 EX-1/EX-2/PL-1/PL-2/RV-1/RV-2; C2 EX-3/EX-4/EX-5/EX-6/CR-1/CR-2; C3 EX-7/EX-8/SC-1/SC-2/RV-3 and EX-9 evidence; verdicts VZ-1/VZ-2/CN-2/CR-3/CR-4. All verdict seats are now visible; no missing peer verdict is inferred.
- Resolve the C1 candidate and receipt-binding interpretation, then land the gate change, C2 `PROVINCE.md:18` correction, and durable refreshed receipt together; run clean and seeded-fault gate tests against that exact revision. Separately land one corrected corpus entry using the single R8 token, fix its source/evidence references and count notation, then measure Command A at the actual landing revision. Until those steps complete, all three claim landings remain pending.
