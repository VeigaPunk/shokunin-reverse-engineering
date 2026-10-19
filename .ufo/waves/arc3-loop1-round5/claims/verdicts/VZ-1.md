# VZ-1 — arc3-loop1-round5 convergence verdict

HEAD at the checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. The measurements below are my own re-derivations from Git objects, current files, saved bytecode/probe evidence, and read-only commands. Peer reports are used for reconciliation, not as proof. This was a static review: no new REA provider call and no high-memory retest. I wrote only this verdict artifact.

## Rulings

| Frozen claim | Ruling |
|---|---|
| C1 — calibration | **DISCREPANCY / PARTIAL.** Core counts and most gates reproduce, but there are command, revision-attribution, literal-scan, and Vyper wording discrepancies. Required `claims/c1/sweep-report.md` is absent. |
| C2 — coverage | **UNVERIFIABLE-with-cause.** All 16 frozen seat reports are now present, but the consolidated `claims/c2/audit.md` is absent, the “r2/r3 errata” scope is ambiguous, and two late peer audits misattribute r3 initcode wording. |
| C3 — freshness | **PARTIAL.** Item rulings are STOPPED-with-reason / DISCHARGED-BY-PRECEDENT with caveats / CARRIED-forward. Required `claims/c3/disposition.md` is absent. |

The frozen claims require the three aggregate paths (`claims-frozen.md:29-53,75-79`). Direct inventory at this check found 20 C1 reports (the 16 names in the frozen C1 roster plus `TB-1..TB-4`), all 16 C2 reports, and all 16 C3 reports. The aggregates `sweep-report.md`, `audit.md`, and `disposition.md`, and `verdicts/VZ-1.md` before this write, were absent. The frozen roster table omits the four TB reports (`claims-frozen.md:81-86`), although the seat-assignment text maps TB to C1; this roster/assignment boundary is ambiguous, and I do not count them as frozen-roster seats. Individual reports do not satisfy the named aggregate deliverables.

## C1 — calibration

### Command A — REPRODUCED, with a revision-label discrepancy

I reran the recipe at `SCORECARD.md:88-124` against the named Git objects and HEAD. Each result had `missing=[]`, `dangling=[]`, and `coverage_score=10.0`, `depth_score=10.0`:

| Revision | Knowledge files / mapped | Resolved rules / rule blocks |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| HEAD `71668cc` | 84/84 | 14/14 |

The measurement rows reproduce, but the frozen grouping is misleading: `5be4a26` is a hygiene-only child of `c418be0` (generated-pyc removal and `.gitignore`), not an r2 work commit; `520341d` is the parent of r4 work commit `40de383`. `28aa7a9` is the r2 work state. Thus the counts are valid for the hashes, but their round attribution needs correction.

### Landed gates — REPRODUCED with one invocation correction

- Census: `python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; `PROVINCE.md lines=162`.
- Citation drift: default → `reported findings=0 exit=0`; `--strict` → `clean findings=0 exit=0`.
- The frozen custody command `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 with `the following arguments are required: cmd`. The supported `.../custody-pair.py selftest` passes: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. The source requires the positional subcommand (`custody-pair.py:1313,1329-1333`); the test result reproduces, the specified spelling does not.

### PROVINCE and Vyper spot-checks

`wc -l PROVINCE.md` returns `162`. I checked the nine literal needles listed in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10`: eight are absent; `JEB (unprobed)` remains at `PROVINCE.md:88`. Therefore the whole-file result is **8/9 absent**, not “all nine cleared” (`SCORECARD.md:1603-1606`). This is a reporting discrepancy, not a reason to remove the existing operator-owned JEB status.

For CarrierV, the retained runtime is 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`. The three saved probe envelopes recover the same 15 selectors; `dispatch-census.py` agrees 15/15 on bodies and offsets. The runtime has a 13-entry table at `0x600`, but decoding the prefix shows `CODECOPY` copies only the selected two-byte entry (`src=0x600+2*(selector%13)`, `dst=0x1e`, `size=2`), not all 26 table bytes. This corrects the memory-copy wording in the r4 entry (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21`); it does not negate the table’s presence or 15/15 result. Evidence: `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin`, `EX-04/evidence/probe/`, `EX-04/evidence/dispatch-census.py`. This is static byte/probe-evidence checking, not a new provider run.

## C2 — corpus coverage

All 16 top-level C2 reports are now present, matching the frozen roster (`claims-frozen.md:84`), but `claims/c2/audit.md` remains absent. A current glob of `corpus/knowledge/2026-10-19-arc3-r*.md` returns only the r1, r3, and r4 entries. The fourth apparent unit is the appended Ghidra erratum; there is no separate r2 entry in that pattern. The frozen “r2/r3 errata” wording does not identify a separate r2 corpus entry unambiguously.

My bounded byte rechecks found these corrections or qualifications:

- **Smoke unit/hash mismatch:** `Smoke_sol_Smoke.bin` is 1,370 bytes of hex-text carrier with SHA-256 `530efc7b…`; decoding yields 685 bytes with SHA-256 `08299f31…`. The r1 entry pairs the decoded size with the text-carrier digest at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:15`; clarify both byte domains append-only.
- **Embedded runtime vs. parsed-and-empty:** Rv2Token runtime (1,943 B) occurs in its 1,971 B creation blob at offset 28; VaultB opt200 runtime (1,621 B) occurs in its 1,655 B creation blob at offset 34; CarrierV runtime (1,562 B) occurs in its 1,637 B creation blob at offset 20. The r1 statement at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24` is already corrected by its append-only erratum at `:31`; r4 `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17` still incorrectly says initcode carries no runtime dispatch table. The r3 line cited by EX-9, RV-8, and EX-12 (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24`) is about Rv2TokenOpt, not an initcode-absence statement; do not append an r3 correction against that line. Embedded bytes do not establish that initcode executes the runtime dispatcher.
- **CBOR vs. opcode claim:** in the r3 VaultB nopt bytes, executable code ends at byte 3,110 and contains 15 code-region `PUSH4` sites; `43000825` is at byte 3,157 in the CBOR trailer. Rv2TokenOpt’s code ends at 925 with six code-region `PUSH4` sites; the marker occurs at byte 972 in its trailer. This contradicts the r3 description of `43000825` as an executable non-dispatch `PUSH4` (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26`), without changing the selector results.
- **Ex09Vault support walk:** my raw-byte traversal of the six-entry table and planted K set found seven selector legs, `missing=[]`, `extra=[]`, matching the 7/7 probe. The retained note `.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/analysis/dispatch-structure.txt:12-21` contradicts this by saying two selectors were absent; its underlying support record needs correction, not the corpus’s 7/7 selector count.
- **Core-status conflict:** the r1/r3 entries say “no Core promotion” (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:33`, `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:35`), while `PROVINCE.md:91-93` labels real-solc arc3-r1/r3 Core. The r4 Vyper entry says no Core promotion (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:30`), but PROVINCE does not explicitly label r4 Core; I do not infer a contradiction for r4.

These checks do not constitute a full audit of every selector/hash claim in all entries. Peer reconciliation: CR-3, EX-9, and RV-8 are now present and materially extend the per-entry audit; EX-12, RV-6, CR-6, VZ-2, and CN-2 also contain substantive findings. EX-9 and RV-8 arrived after the earlier C2 inventory snapshots; the live count is now 16/16, while the aggregate audit remains absent. EX-9 (`claims/c2/EX-9.md:28,38,50`) and RV-8 (`claims/c2/RV-8.md:36`) both misattribute the r3 initcode wording to line 24. CR-6 is internally inconsistent: it first describes r3:24 as that wording, then correctly observes at `claims/verdicts/CR-6.md:66` that the line is Rv2TokenOpt and the r3 entry has no such phrase; its own correction at that later line is the applicable one. Peer-reported details beyond the byte checks above remain peer evidence, not this seat’s independent verification. The missing aggregate keeps the full C2 claim unclosed.

## C3 — arc2 carried-debt disposition

1. **Mid-leg faithful retest — STOPPED-with-reason.** A fresh bounded `free -b` sample returned `free=2008842240` and `available=20211113984` bytes. “≥20G free RAM” is ambiguous between the `free` and `available` measures and between decimal GB and GiB; regardless of interpretation, the separate operator host-cost authorization required by `claims-frozen.md:60-66` is not evidenced. I did not launch the uncapped retest. This is an honest stop, not a retest result.
2. **r10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with caveats.** My roster/file comparison returned `roster=64 reports=59 missing=CR1,E1,E17,E28,R7 extras=[]`. `P1.md` exists although the older reconciliation receipt says P1 is missing (`arc2-loop1-round10/receipts/roster-reconciliation.txt:1`); the corrected exact missing set should supersede that receipt for this ruling. The frozen R5 option permits recording the interruption disposition if the sweep does not need the missing findings (`claims-frozen.md:67-70`). I accept that administrative disposition, not 64/64 delivery. The general counting lesson requires replacement for a true shortfall and states no interruption exception (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`), so the “per the lesson” rationale is not supported; the specific frozen R5 option is the basis here.
3. **Full hyper-vs-Devin census — CARRIED-forward (partial).** The table still has `<fill>` at `arc2-loop1-round10/E19.md:212-217`; searches of arc2 r1-r4 for `dispatch*` and `*.jsonl` found no checked-in payloads from which to reconstruct the dispatch denominator. Saved samples and report counts do not establish full dispatch completion. This is a partial-census disposition, not a claim that external session logs do not exist.

Peer reconciliation: PL-1/EX-19 and VZ-2/CR-6 agree on stopping without operator clearance, the five-file r10 deficit, and carrying the dispatch-level census forward. PL-1’s report-count comparison is useful as a file census, but EX-19 correctly distinguishes it from a dispatch-denominator comparison (`EX-19.md:60-89`). Their reports do not replace the absent aggregate `claims/c3/disposition.md`.

## Overall

The frozen C1/C2/C3 positive claims are **not closed at the aggregate-artifact level**. C1 measurements mostly reproduce with named discrepancies; C2 has partial item-level corrections but remains UNVERIFIABLE-with-cause; C3 has three recorded item dispositions with the caveats above. The three required aggregate paths were absent at inventory, so no overall completion verdict is justified.