# Round 32 — ARM64X native-view coverage and repertoire-summary calibration

Author: kaidoku L1, attempt 2. Base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`. Attempt 1's three landed freeze commits (`9a73680a`, `9d54070b`, `f382e3b7`) are part of this round. Its 36 w1 seats died with omp SIGSEGV at 06:19:06Z; no reports are used or identities replaced. Attempt 2 preserves the freezes and re-checks their bytes and baseline measurements (`.ufo/waves/round-32/a2before/`).

## Claims

- **R32-C1 — coverage:** ARM64X hybrid PE moves from the PROVINCE Frontier reserve to bounded Core coverage through REA 6.5.0 `inspect`. Frozen predicate `P1-pass`, target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0, in `.ufo/waves/round-32/claims.json` (freeze `9a73680a`). The novelty statement is a bounded absence of a recorded hybrid REA run, not absence of naming or an ARM64X-targeted linker attempt. The widened historical audit is `a2audit/A2NoveltyFull.md`.
- **R32-C2 — calibration:** reconcile four outside-recorded capabilities with SCORECARD's `## Capabilities` summary. Frozen predicate `P2-match`, target `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0, in `claims-v3.json` (freeze `f382e3b7`). **Honest stop:** an explicitly negative assessment meets that target. The measure cannot support a calibration improvement; it is not re-frozen, re-scaled or relabelled exploratory. Complete counterexample and receipt landed at `411f3a80a1efefabe2ba12f227147023cfbce4bd` (`controls/c2-negative/`, `a2audit/A2C2False.md`); the independent five-word-bag shortcut also passes (`A2C2Labels.md`).

The owned axes are tied at 10 at the base, none retired, so both declared axes satisfy the lowest-axis rule. Unlike rounds 30–31, this round has no new reader verb or refusal-table claim: it addresses a hybrid PE edge class and the lane's own repertoire assessment. The SCORECARD numeric proxies are not a mastery claim.

## Gate

- **Admit as a source, not as capability evidence:** Microsoft Arm64X documentation and LLVM's paired load-config assembler inputs, reopened in `a2audit/A2SourcesPrimary.md`. The source snapshot is retained under `corpus/evidence/round-32/sources/`; generated carrier outcomes remain separate evidence.
- **Reject as authority for CHPE offset/tag values:** the Microsoft PE Format specification. Its served bytes name ARM64X machine types but contain no `CHPEMetadataPointer`, `CodeMap`, or `0xC8`; `a2audit/A2SourceReject.md` retains the bounded search and flip. The page is not rejected for other scopes.
- **Reject as a claim measure:** C2v3's five-word lexical description condition. `A2C2False` scores 4/4 while denying all four capabilities; `A2C2Labels` scores 4/4 on alphabetized word bags. The frozen predicates remain unchanged and these are failed discrimination controls, not successful repairs.
- Outside admit/reject spot-check: not performed by this L1 or its seats. Author-dispatched reviewers are still the lane; final admission belongs to the non-author closure.

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
