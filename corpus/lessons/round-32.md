# Round 32 — ARM64X native-view coverage and repertoire-summary calibration

Author: kaidoku L1, attempt 2. Base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`. Attempt 1's three landed freeze commits (`9a73680a`, `9d54070b`, `f382e3b7`) are part of this round. Its 36 w1 seats died with omp SIGSEGV at 06:19:06Z; no reports are used or identities replaced. Attempt 2 preserves the freezes and re-checks their bytes and baseline measurements (`.ufo/waves/round-32/a2before/`).

Wave evidence paths abbreviated as `a2audit/...`, `controls/...`, `claims*.json` or `a2after/...` below are relative to `.ufo/waves/round-32/`.

## Claims

- **R32-C1 — coverage:** ARM64X hybrid PE moves from the PROVINCE Frontier reserve to bounded Core coverage through REA 6.5.0 `inspect`. Frozen predicate `P1-pass`, target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0, in `.ufo/waves/round-32/claims.json` (freeze `9a73680a`). The novelty statement is a bounded absence of a recorded hybrid REA run, not absence of naming or an ARM64X-targeted linker attempt. The widened historical audit is `a2audit/A2NoveltyFull.md`.
- **R32-C2 — calibration:** reconcile four outside-recorded capabilities with SCORECARD's `## Capabilities` summary. Frozen predicate `P2-match`, target `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0, in `claims-v3.json` (freeze `f382e3b7`). **Honest stop:** an explicitly negative assessment meets that target. The measure cannot support a calibration improvement; it is not re-frozen, re-scaled or relabelled exploratory. Complete counterexample and receipt landed at `411f3a80a1efefabe2ba12f227147023cfbce4bd` (`controls/c2-negative/`, `a2audit/A2C2False.md`); the independent five-word-bag shortcut also passes (`A2C2Labels.md`).

The owned axes are tied at 10 at the base, none retired, so both declared axes satisfy the lowest-axis rule. Unlike rounds 30–31, this round has no new reader verb or refusal-table claim: it addresses a hybrid PE edge class and the lane's own repertoire assessment. The SCORECARD numeric proxies are not a mastery claim.

## Gate

- **Admit as a source, not as capability evidence:** Microsoft Arm64X documentation and LLVM's paired load-config assembler inputs, reopened in `a2audit/A2SourcesPrimary.md`. The source snapshot is retained under `corpus/evidence/round-32/sources/`; generated carrier outcomes remain separate evidence.
- **Reject as authority for CHPE offset/tag values:** the Microsoft PE Format specification. Its served bytes name ARM64X machine types but contain no `CHPEMetadataPointer`, `CodeMap`, or `0xC8`; `a2audit/A2SourceReject.md` retains the bounded search and flip. The page is not rejected for other scopes.
- **Reject as a claim measure:** C2v3's five-word lexical description condition. `A2C2False` scores 4/4 while denying all four capabilities; `A2C2Labels` scores 4/4 on alphabetized word bags. The frozen predicates remain unchanged and these are failed discrimination controls, not successful repairs.
- Outside admit/reject spot-check: not performed by this L1 or its seats. Author-dispatched reviewers are still the lane; final admission belongs to the non-author closure.

### Opened source rows

All new rows were opened on **2026-10-23**; existing source rows have no status/recheck/used-by changes. New rows: S098/S099 `mined`, S100 `rejected` (tier A for each stated scope). Used-by: S098/S099 the round-32 hybrid entry; S100 this lesson.

| row / decision | URL opened this round | located contiguous quote, at most 25 words | source identity / limit |
|---|---|---|---|
| S098 / admit input provenance | https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s (paired loadconfig-arm64.s also reopened) | ARM64EC line 20: `.xword __chpe_metadata` | SHA-256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4`; paired `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`; bytes equal the committed inputs. References are not populated-map or reader-result proof |
| S099 / admit definition/default-view scope | https://learn.microsoft.com/en-us/windows/arm/arm64x-pe | retained Markdown line 50: “Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.” | SHA-256 `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66`; `corpus/evidence/round-32/sources/arm64x-pe.md`; line 64 separately explains default Arm64 appearance |
| S100 / reject CHPE offset/tag authority | https://learn.microsoft.com/en-us/windows/win32/debug/pe-format and its MicrosoftDocs/win32 docs Markdown | retained Markdown line 131: “Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file.” | HTML SHA-256 `d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1`; Markdown `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0`; both retained under `corpus/evidence/round-32/sources/`. Machine types are documented, CHPE offset/tags are not |

The S100 flip requires both reopened representations to explicitly document the PE32+ CHPEMetadataPointer offset 200/0xC8 and numeric code-map tag bit meanings. A different page or one conjunct does not flip it. The exact bounded absence census is `a2audit/A2SourceReject.md`; a forbidden/failed GitHub search is not absence evidence.

## Mistakes

| id / class | evidence | captured-by | fix / able-to-fail evidence |
|---|---|---|---|
| M32-1 / stale-premise | Round-31 verifier defect 1: the CLI spelling exists in README and an l7-04 filename outside the old content-only sweep | QUALITY 56 was too narrow | QUALITY 57 supersedes 56, adding README and filenames; `a2audit/A2R31Corrections.md` retains the widened red-before sweep |
| M32-2 / vacuous | `a2audit/A2C2False.md`, `A2C2Labels.md`: negative prose and vocabulary bags meet the unchanged C2v3 target | pre-data adversarial control wave; frozen claim-sizing rule | Honest stop, frozen counter unchanged; actual false-accept receipt and full fixture committed at `411f3a80`. No semantic gate repair is claimed in this round |
| M32-3 / reference-drift | A2C1 control scoring from Eval initially inherited no GHIDRA_INSTALL_DIR/JAVA_HOME, unlike Bash | control seats reported provider failures instead of crediting discrimination | Record the actual environment and resolve the missing keys explicitly before a new scoring run. Original failures are retained as unevaluable discrimination, not evidence that committed-envelope checks rejected the control |

## Round-31 routed defects

1. Novelty sweep widened via QUALITY 57; correction appended to the positive entry.
2. Lesson's 3/23 ceiling corrected by an appended 7/23 erratum.
3. SKILL's stale “not run” sentence corrected to cite the three live 6.7.0 requests.
4. Report erratum: stray Git command was w1 `CriticSeparability`, not w2. No commit landed. No tool enforces the seat no-Git-write instruction; M31-7 remains not shown able to fail.
5. A new run of the cited-runs gate over the filed round-31 report is assigned to `A2CitedReport`; only its retained observed receipt is evidence, never retroactive proof of pre-filing execution.
6. The frozen new C1 counter explicitly makes write mode exit 3 and print no target line; its measure-mode result, not its write result, decides the claim.
7. Controls commit time corrected to 04:18:47Z; the unstamped old census instant is withdrawn. Attempt-2 receipts retain UTC start/end internally.

## Forensic corrections appended before data

- The introduction's “36 w1 seats died” overstates the evidence. The registry contains **36 planned items** with null IDs and no reports. `a2audit/A2AttemptForensics.md` identifies one accepted 12-seat chunk, one later refused 12-seat chunk, and 12 with no later-start evidence. The assignment supplies the SIGSEGV cause for started seats; only one exact accepted runtime ID survives. All 36 planned items remain excluded, but unstarted/unknown items are not counted as observed deaths.
- Frozen C1 motivation prose says six asymmetric native/EC export-count carriers. The fixed roster contains **seven** (`k04,k05,k07,k08,k09,k10,k12`), as `a2audit/A2AxisCoverage.md` notes. The predicate, 12-carrier target and predictions do not depend on the erroneous six; they remain byte-unchanged.
- C2's reverse check covers scalar-lane closure numbers 12–31, not every historical kaidoku closure or namespace. `a2audit/A2ReverseDomain.md` identifies 11 map-identified closures omitted by the selector and confirms no fifth capability item is lost. Four-item alignment is not whole-repertoire calibration.

## Producer and instrument limits

All ten fresh control reports and `controls/a2-receipts.tsv` landed at `33393e594f1e278777fa49020b42c66ac4fa352e` before C1's producer ran. Five C1 controls score 0/12 with both doc gates green; C2 empty/junk/no-reader controls score 0/4, while negative prose and word bags score 4/4. Four C1 seats first encountered the missing Eval-provider environment; those failures are retained separately and are not discrimination credit.

The post-control producer stores original envelopes and per-call argv/UTC/package identity. Its write-mode receipt `a2after/c1-write.txt` exits 3 and prints no target line. `a2audit/A2CitedReport.md` closes the missing round-31 report run with an observed gate exit 0 (seven recognized assertions) and 17/17 selftest, not universal report-result coverage or retroactive timing proof.

Frozen-instrument findings are retained, not silently repaired:
- `a2audit/A2LivePredicate.md`: first-added ordering uses committer timestamps, not DAG ancestry; inherited GIT_DIR can redirect the counter's own Git calls; plumbing errors can look like predicate misses. The lane measurement unsets Git routing variables and records actual commit/run order.
- `a2audit/A2CHPEBits.md`: metadata-only ARM64X classification accepts forged map tags on a pure ARM64 fixture. The actual frozen carriers have an independently reproduced dual-object build/LLVM hybrid-view witness, but the classifier alone proves declared structure, not valid EC instruction/ABI content or Windows loading.
- `a2audit/A2SelftestHoles.md`: five of eight bounded mutations survive the existing selftests; four concern C1 committed/source clauses and one C2's exact five-word threshold. These are frozen-test limitations, not claimed repairs.
- `a2audit/A2FreezeBytes.md`: C2's word tokenizer admits hyphens while prose says letters; Core exclusion matching is case-sensitive. These are disclosed boundary differences, not post-freeze amendments.
- The reused freeze-integrity gate has no self-invocation mode; its registry names that conformance limitation.
