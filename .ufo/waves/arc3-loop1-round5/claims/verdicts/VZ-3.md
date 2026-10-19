# VZ-3 — arc3-loop1-round5 convergence verdict

HEAD at the direct checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. I re-derived the measurements below from Git objects, current files, or retained bytecode/evidence. Peer reports are used for reconciliation, not as a substitute for the independent checks. This seat writes only this verdict artifact; it did not execute targets, launch the gated retest, or change corpus/source files.

## Summary

| Frozen claim | Ruling |
|---|---|
| C1 calibration sweep | **DISCREPANCY**: object-level counts and landed gates reproduce, but the custody command syntax, hash grouping, exact nine-needle result, and Vyper `CODECOPY` description need correction. Required `claims/c1/sweep-report.md` is absent. |
| C2 corpus audit | **UNVERIFIABLE-with-cause** at chain level. Selected carrier claims and named correction candidates were independently rechecked, but the required per-claim `claims/c2/audit.md` is absent and the frozen 16-seat audit scope is not complete. |
| C3 carried-debt dispositions | **STOPPED-with-reason / DISCHARGED-BY-PRECEDENT / CARRIED-forward (partial)**, respectively. Roster identity and the generic counting-lesson rationale remain discrepant. Required `claims/c3/disposition.md` is absent. |

The frozen contract requires the three aggregate artifacts and specifies C1/C2/C3 scope at `claims-frozen.md:17-79`. A refreshed path inventory found no `claims/c1/sweep-report.md`, `claims/c2/audit.md`, `claims/c3/disposition.md`, or prior VZ-3 artifact. Current individual inventory: C1 has all 16 frozen reports plus unrostered TB-1..TB-4; C2 has 13/16 (EX-9, CR-3, RV-8 absent); C3 has all 16 frozen reports. Individual seats do not replace their required aggregate deliverables.

## C1 — calibration

### Command A — REPRODUCED per object; round grouping corrected

I reran the `SCORECARD.md:88-124` recipe against the named Git objects and HEAD. Every object had empty `missing`/`dangling` sets and coverage/depth scores `10.0/10.0`:

| Hash | Mapped / knowledge files | Resolved / rule blocks |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| `71668cc` (HEAD) | 84/84 | 14/14 |

The table values reproduce, but the frozen grouping is not a work-commit chronology: `5be4a26` is a hygiene-only child of `c418be0`, and `520341d` is the parent of `40de383`. Associate the admitted work measurements with r1 `fbbbd45`, r2 `28aa7a9`, r3 `c418be0`, and r4 `40de383`; retain the intermediate hashes as measured trees, not as separate round work. Git parent/subject evidence is independently reported at `claims/c1/EX-3.md:7-18` and `claims/c1/TB-4.md:7-18`.

### Landed gates — REPRODUCED with custody invocation discrepancy

- `python3 .ufo/gates/c1-census-v10.py --root .` passed: `stale=0 ambiguous=0 undeclared=0 unresolved=0`; `PROVINCE.md` is 162 lines.
- Citation drift default returned `reported findings=0 exit=0`; strict returned `clean findings=0 exit=0`.
- Frozen `custody-pair.py --selftest` exits 2 because the parser requires a subcommand. Supported `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm` passes `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. The test reproduces; the specified spelling is a **DISCREPANCY**. The C1 peer command outputs agree (`claims/c1/EX-3.md:20-24`).

### PROVINCE literals — DISCREPANCY: 8/9 absent

I searched the exact nine needles from `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` against the full current `PROVINCE.md` with dedicated literal-pattern searches, not a shell `grep -F` invocation: eight are absent; `JEB (unprobed)` remains at `PROVINCE.md:88`. The SCORECARD also records JEB as NO-CHANGE (`SCORECARD.md:1603-1606`), and the R2 capability matrix records an `inspect-jeb-client` attempt ending in `fetch failed` (`corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99`). This falsifies the exact whole-file “9/9 absent” result, not the operator-owned status; it is not a reason to remove JEB. Some peer 9/9 sweeps used alternate lists that omit JEB (`claims/c1/SC-4.md:56-70`, `claims/c1/EX-4.md:31-32`), so those do not test the frozen nine-item set.

### Vyper CarrierV — bytes and selector result VERIFIED; copy-length wording corrected

The retained CarrierV runtime is 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; the three saved 6.4-hex, 6.4-raw, and 6.7-hex probes recover the planted 15/15 selector set. The 13 two-byte table entries at `0x600` point to JUMPDESTs, with sentinel `0x5e7` repeated three times. This is a bounded static check of saved bytes, not a fresh provider invocation or target execution (`claims/c1/EX-3.md:28-32`; `claims/c1/SC-4.md:74-81`).

The entry's `CODECOPY` description needs precision: the prefix `5f3560e01c6002600d820660011b61060001601e395f5156` pushes copy length **2**. The runtime copies only the selected two-byte entry at `0x600 + 2*(selector % 13)` to memory offset `0x1e`; it does not copy the entire 13-entry table to memory as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21` currently says. The table remains in the runtime tail. This agrees with the byte-level correction candidate in `claims/c1/EX-3.md:30`.

**C1 ruling:** substantive measurements reproduce, with the discrepancies above. The absent consolidated sweep means C1 is not closed at the frozen deliverable level.

## C2 — coverage audit

### Independently verified subset

- **r1 Rv2Token:** 5/5 unique ABI-dispatch selectors at both checked hex pins; decoded runtime 1,943 bytes, SHA-256 `c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74`. The saved probe and planted set agree (`.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json:1`, `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt:1-6`; peer summary `claims/c2/EX-10.md:7`).
- **r3 VaultB opt200:** 13/13 at the checked pins, matching planted selectors and the 1,621-byte runtime SHA-256 `b24a01153af943ff8ebf26a678a3bfc0b1d70e1fc563d17b05c7cc064ae340b6` (`.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-hex-6.4.0.json:1`; `claims/c2/EX-10.md:11`).
- **r4 CarrierV:** 15/15 on 6.4 hex/raw and 6.7 hex, matching the same 1,562-byte runtime identity above (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/`; `claims/c2/EX-12.md:19-20`).

These spot checks verify only the named carriers, not every C2 claim or secondary matrix leg.

### Correction candidates and peer disagreement

- **Smoke units (r1):** `Smoke_sol_Smoke.bin` is 1,370 bytes of hex text with file SHA-256 `530efc7bb166fd47e42fe9623ee347234b99a65691b0a0ad42d2682702986a5f`; decoded initcode is 685 bytes with SHA-256 `08299f31203e05e5dcdcd2453f9dd5a105a97fd94f2b48194ba18e963c368ebd`. The r1 line pairs the decoded byte count with the text-file hash (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:15`; `claims/c2/RV-6.md:23`). Report both units distinctly in any append-only correction.
- **CBOR vs. code PUSH4 (r3):** VaultB nopt's code ends at byte 3,110 and has 15 code-region PUSH4 sites, all selector sites; Rv2TokenOpt's code ends at byte 925 and has six sites (five selectors plus panic `4e487b71`). `43000825` occurs at offsets 3,157 and 972 in terminal CBOR, not as executable code-region PUSH4s (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:26`; `claims/c2/RV-6.md:24`).
- **Creation/initcode phrasing:** runtime bytes are embedded in creation blobs at offsets 28 (r1 Rv2Token), 34 (r3 VaultB opt200), and 20 (r4 CarrierV), while the probes return zero functions for those creation inputs. That is “parsed-and-empty,” not proof of byte-level absence or execution of the embedded runtime (`claims/c2/EX-12.md:31`; `claims/c2/CN-2.md:61-66`). The live r4 false wording is at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`; r1 has an append-only correction at r1 `:31`. **EX-12 miscites r3 `:24`:** that line is the Rv2TokenOpt observation, not a creation/initcode claim (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24`; `claims/c2/EX-12.md:31`). Do not route an r3 correction to that pointer.
- **Ex09Vault dispatch disagreement:** EX-10's report leaves two selectors unresolved from the cited parser walk (`claims/c2/EX-10.md:19`). I independently followed the six table heads at runtime offset `0x239` (`0x18, 0x204, 0x220, 0x1e9, 0xf7, 0x1b8`); each is a JUMPDEST. Walking mismatch edges recovers all seven planted/probed selectors, including the two that the checked-in `dispatch-structure.txt` marked absent; buckets 0 and 4 each hold two selectors, while bucket 2 is empty. Thus the 7/7 count is not in conflict with the raw dispatcher; EX-10's parser conclusion that two selectors are missing is **DISCREPANT**. This is static byte inspection of `.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.bin`, not execution.
- **Core scope:** the r1/r3 entries say RESULT-only/no Core promotion (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:33`; r3 `:35`), while `PROVINCE.md:91-93` calls real solc r1/r3 carriers Core. That is a real status conflict for r1/r3. The same PROVINCE line names the Vyper r4 carrier without an explicit Core tag; do not overstate the r4 part of this conflict. `claims/c2/RV-6.md:25` flags this boundary.
- **Inventory ambiguity:** the frozen scope names dated r1/r3/r4 entries plus “r2/r3 errata” (`claims-frozen.md:38-45`). The current `2026-10-19-arc3-r*.md` set is r1/r3/r4; the Ghidra correction is appended to a separate older-named entry, and no standalone `2026-10-19-arc3-r2` file exists (`claims/c2/RV-6.md:7,27-29`). Whether that older erratum is the intended fourth audit unit needs a resolvable pointer; do not silently treat it as a missing standalone r2 file.

**C2 ruling: UNVERIFIABLE-with-cause.** Thirteen individual C2 reports exist, but EX-9, CR-3, and RV-8 are absent and the required one-row-per-load-bearing-claim `claims/c2/audit.md` is absent (`claims-frozen.md:47-53`). Peer work is substantive; it does not establish full chain coverage or erase the correction candidates above.

## C3 — arc2 carried-debt dispositions

1. **Mid-leg faithful retest — STOPPED-with-reason.** My bounded `free -b` sample was `free=998944768` bytes and `available=21574037504` bytes. The “≥20G free RAM” wording is ambiguous: the literal free column is under 1 GB, while available memory is only slightly over 20 GiB. More decisively, no affirmative operator host-cost authorization is present. Since the frozen condition requires both, no expensive retest was launched (`claims-frozen.md:60-66`). Peer samples differ slightly, but also lack authorization (`claims/c3/PL-2.md:9-18`; `claims/c3/EX-14.md:7-17`).
2. **r10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with discrepancies.** Independent expansion of the frozen roster and current report set gives 64 slots, 59 reports, no extras, missing `CR1,E1,E17,E28,R7`. The reconciliation receipt instead lists P1, CR1, E1, E17, and an unnamed seat; P1 is present in the current tree. The frozen range also contains malformed/ambiguous `SC1-S2`. The R5 freeze specifically permits discharge by precedent unless the sweep shows r10 findings are needed (`claims-frozen.md:67-70`); record this status under that specific instruction, **not** as authorized by the generic counting lesson, which instead calls for re-dispatch per unresolved seat and states no interruption exception (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`). Keep exact interruption-time identities unresolved and reopen if the missing C2 audit establishes a need for r10 findings. Primary records: `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:3`, `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1`, `SCORECARD.md:1277-1281,1330-1332`; peer cross-check `claims/verdicts/CN-2.md:79-89`.
3. **Full hyper-vs-Devin census — CARRIED-forward (partial).** The E19 table still has `<fill>` cells at `.ufo/waves/arc2-loop1-round10/E19.md:212-217`; retained dispatch arrays/denominators are unavailable in the checked-in evidence. Report counts cannot supply the historical per-seat comparison. Do not upgrade the partial samples to a completed census (`claims/c3/PL-2.md:32-38`; `claims/c3/EX-14.md:27-37`).

The required aggregate `claims/c3/disposition.md` is absent, so these per-item rulings do not close the frozen C3 deliverable.

## Peer reconciliation and overall ruling

- C1 EX-3, TB-4, CN-2 and CN-4 independently report the corrected custody subcommand, 8/9 JEB result, and hash-grouping correction. SC-4/EX-4's alternate needle lists do not override the exact frozen set. EX-3 also identifies the two-byte `CODECOPY` correction.
- C2 EX-10's Ex09 parser “two missing” conclusion is resolved by the raw-byte walk above. EX-12/RV-6 supply useful unit, CBOR, initcode, Core-status, and inventory findings; the r3 initcode pointer in EX-12 is wrong. CN-2/CN-4/VZ-2/VZ-4 statements that C2 reports were absent or only EX-12/RV-6 existed are time-qualified snapshots, superseded by the present 13-report inventory; the absent aggregate `audit.md` remains current. CR-6 supports a partial overall status but repeats the incorrect r3 `:24` pointer (`claims/verdicts/CR-6.md`); do not propagate that pointer.
- C3 peers PL-2 and EX-14 agree on STOPPED-with-reason, recorded discharge, and carrying the census forward. Their samples do not resolve the RAM wording or operator authorization; the report-count identity and generic-lesson attribution discrepancies remain.

**Overall:** no all-chain completion claim is justified. C1 has reproduced measurements plus named discrepancies; C2 remains **UNVERIFIABLE-with-cause** pending its aggregate audit; C3 has explicit item-level dispositions but no required aggregate disposition file and retains roster/census caveats. No other seat artifact, corpus entry, PROVINCE, SCORECARD, LOG, or source path was changed by this verdict seat.
