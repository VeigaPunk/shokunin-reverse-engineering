# CR-6 — arc3-loop1-round5 verdict chain

HEAD at direct checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. I re-derived the measurements below from Git objects, retained evidence, and read-only tools, then reconciled the current seat reports. This was a static review; I made no new REA provider call.

## Rulings

| Claim | Ruling |
|---|---|
| C1 — calibration | **DISCREPANCY / PARTIAL.** Command-A values and landed-tree gates reproduce, but the frozen custody invocation is invalid, the whole-file literal result is 8/9 rather than 9/9, and one revision is misgrouped. The required `claims/c1/sweep-report.md` is absent. |
| C2 — corpus audit | **CORRECTED / PARTIAL.** Per-seat reports and the retained-data re-derivation substantiate the selector, byte-identity, and dispatch checks, but several wording/status corrections remain. The required `claims/c2/audit.md` is absent; scope for a separate r2 entry is unresolved. |
| C3 — carried debt | **STOPPED / DISCHARGED-BY-PRECEDENT / CARRIED-FORWARD**, respectively, for the retest, r10 shortfall, and full census. The evidence supports those recorded dispositions with roster/rationale caveats. The required `claims/c3/disposition.md` is absent. |

**Overall: not closed at the frozen artifact level.** Individual reports now provide substantial evidence, but they do not replace the three named aggregate deliverables.

## C1 — calibration

### Command A — REPRODUCED

I ran the recipe at `SCORECARD.md:88-124` against immutable Git objects. Every row had empty `missing` and `dangling` lists and coverage/depth scores of 10.0/10.0:

| Revision | Mapped / knowledge files | Resolved / rule blocks |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| HEAD `71668cc` | 84/84 | 14/14 |

**Revision-grouping correction:** `git show -s --format='%h %p %s' 5be4a26` identifies `c418be0` as its parent and describes a hygiene-only change (ignore generated `__pycache__`, remove committed `.pyc`). It is not an r2 work snapshot as grouped at `claims-frozen.md:21-22`; the 83/83 value is an r3 child state. `520341d` is parent of r4 work commit `40de383` (its subject records the r4 custody-pair residual closure). The r2 work snapshot `28aa7a9` itself reproduces at 82/82, 14/14. This is an attribution discrepancy, not a metric discrepancy.

### Landed-tree checks — REPRODUCED with one command correction

- Census v10: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; reported `PROVINCE.md` 162 lines, `SCORECARD.md` 1631, `SKILL.md` 390.
- Citation drift: default `reported findings=0 exit=0`; strict `clean findings=0 exit=0`.
- Custody-pair: the frozen `python3 -B .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 because the CLI requires a positional subcommand. The supported `... custody-pair.py selftest` passes all 28 cases (`CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`). Thus the test result reproduces, but the frozen invocation is a discrepancy.
- `wc -l PROVINCE.md` returns 162.

### Nine-literal check — DISCREPANCY

I counted the exact literals from `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` against the current `PROVINCE.md`. Eight are absent; `JEB (unprobed)` occurs once at `PROVINCE.md:88` in the current operator-owned alternate-provider status. The correct result is **8/9 absent**, not nine absent as claimed at `SCORECARD.md:1603-1606`. Do not remove the current JEB status to satisfy the broad substring test.

### Vyper spot-check — REPRODUCED from retained bytes

I ran the retained `EX-04/evidence/dispatch-census.py` against `EX-04/out/runtime.hex`, `planted-K.json`, and the saved 6.4.0 probe. It reproduced 1,562 runtime bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, 15 unique planted selectors recovered 15/15, all `dispatch="abi"`, and probe/body-offset agreement 15/15. The modulo-13 table at `0x600` has 13 entries; all point to JUMPDEST bytes, with the empty-bucket target `0x05e7` repeated three times. The 15 XOR-chain offsets are `PUSH4 pc + 11`, not JUMPDESTs. This is a static byte/evidence check, not a new provider probe.

**Artifact gap:** individual C1 reports such as `claims/c1/SC-2.md` and `TB-4.md` are present and agree on these results, but the frozen aggregate `claims/c1/sweep-report.md` is absent at inspection.

## C2 — corpus audit

I ran `PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/arc3-loop1-round5/claims/c2/CR-2/evidence/rederive.py`. Its 21 retained probe/asset cases reproduced the listed selector counts, decoded byte sizes and SHA-256 values; planted/ABI comparisons matched where recorded. The representative family totals are r1 Rv2Token/KdxToken/Rv2Many 5/6/11, r3 VaultB variants/carrierB variants/CarrierB/CarrierBErr/Rv2TokenOpt 13/11/8/8/5, and r4 CarrierV/Ex09Vault/StewardToken/CarrierW/Smoke 15/7/22/9/4. The direct results complement EX-12 (`claims/c2/EX-12.md:7-35`) and RV-6 (`claims/c2/RV-6.md:11-29`); they do not make the frozen aggregate path exist.

Corrections / qualifications to reconcile:

1. **Initcode wording — CORRECT r3 and r4 append-only.** I compared the runtime bytes with the retained creation carriers: Rv2Token runtime (1,943 B) occurs in its 1,971 B creation blob at offset 28; r3 VaultB opt200 runtime (1,621 B) occurs in its 1,655 B creation blob at offset 34; r4 CarrierV runtime (1,562 B) occurs in its 1,637 B creation blob at offset 20. Thus the r3 claim at `2026-10-19-arc3-r3-evm-optimizer-shapes.md:24` and r4 claim at `2026-10-19-arc3-r4-evm-vyper-leg.md:17` that initcode carries no runtime dispatch table is false as a byte-level statement. The zero-function probes establish only “parsed-and-empty”; they do not mean the runtime bytes are absent or that initcode executes the copied runtime dispatcher. The existing r1 append at `2026-10-19-arc3-r1-evm-real-solc.md:31` already makes this distinction.
2. **r1 carrier-vs-decoded units — append clarification.** The `Rv2Token.creation.hex` text carrier is 3,942 B (SHA `e6517fb7…`), while decoded initcode is 1,971 B (SHA `04e07f54…`). The `Smoke_sol_Smoke.bin` hex-text carrier is 1,370 B (SHA `530efc7b…`), while decoded initcode is 685 B (SHA `08299f31…`). The r1 entry uses the decoded size with the text-carrier digest for Smoke (`:15`), and calls out a different unit for the same Rv2Token path between `:12` and `:31`. Add an append-only unit clarification; do not rewrite the entry.
3. **r3 CBOR/PUSH4 claim — CORRECT append-only.** Direct instruction decoding of the r3 VaultB nopt evidence gives code end 3,110 and 15 code-region PUSH4 sites; `43000825` is only at byte 3,157 in the trailer, not a code-region PUSH4. Rv2TokenOpt has code end 925 and six code-region PUSH4 sites (five selectors plus panic); `43000825` occurs only at byte 972 in its trailer. This contradicts the r3 entry’s characterization of that CBOR value as a non-dispatch PUSH4 in executable code (`:26`). Distinguish metadata bytes from opcode-boundary immediates in an append-only correction. The measured selectors/dispatch results are unaffected.
4. **Core-status conflict — parent adjudication required.** The r1/r3/r4 entries explicitly say “RESULT-class, no Core promotion” (r1 `:33`, r3 `:35`, r4 `:30`), while `PROVINCE.md:92-93` labels the real-solc arc3-r1/r3 carriers “Core.” Both statements cannot describe the same status. Reconcile the lane summary with the corpus boundary; this review does not promote or demote the evidence.
5. **Ex09Vault original carrier pointer — evidence identity caveat, not decoded-byte failure.** The original round-4 probe records `/var/tmp/ex09-r4/carriers/Ex09Vault.runtime.hex`; its input digest does not match the committed hex carrier (`EX-09/vyper/Ex09Vault.runtime.hex`, 1,165 B, SHA `05a29536…`; the earlier input was recorded as 1,163 B with a different digest). The decoded 581-byte runtime still matches SHA `54b14e306bbaf7614d062c06522e88327177aba576309905008e63a90ad199ee`. The later R5 witness `claims/c2/EX-7/r4-ex09vault.json:1` binds the committed file digest and returns seven unique ABI-dispatched functions equal to planted K=7. Treat this as a stale/original carrier pointer, not a selector or decoded-bytecode failure.
6. **Scope of the “r2/r3 errata” wording.** The current corpus has dated arc3 r1/r3/r4 entries and the separate appended Ghidra correction; no standalone arc3-r2 knowledge file was found. If the frozen wording intended an additional r2 entry beyond those errata, that part is not verifiable from the current scoped corpus. The Ghidra correction and current 34 count are covered by EX-12/RV-6.

EX-12 and RV-6 are now present, so CN-2 and VZ-4’s earlier “no C2 report” observations are superseded point-in-time snapshots. The current `claims/c2/audit.md` is still absent; neither seat report is that frozen aggregate. No corpus correction was made by this seat.

## C3 — arc2 carried-debt disposition

1. **Mid-leg faithful retest — STOPPED-with-reason.** I read the original sampler metadata at `/var/tmp/arc2-l6r6-E9-mid/meta.txt:12`: `peak_tree_rss_kb=19149984`, or 18.262848 GiB. The faithful retest was not run. Peer bounded memory samples show `MemAvailable` above 20 GiB but the literal `free` field below it; more importantly, no affirmative operator host-cost authorization is present in the inspected task/records. The required conjunction is not satisfied. This agrees with PL-2/PL-3/PL-4 and EX-13/EX-14/EX-15; it is a stop, not a failed retest.
2. **r10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with discrepancies.** A direct expansion of the roster classes and current top-level report enumeration gives 64 roster IDs, 59 reports, and five currently absent names: `CR1,E1,E17,E28,R7`; `P1.md` is present. The old `receipts/roster-reconciliation.txt:1` instead lists P1 and leaves one seat unnamed. Thus cardinality reproduces, but the historical slot identities do not. I accept the recorded no-backfill disposition under the frozen option at `claims-frozen.md:67-70`, because the arc3 C1/C2 sweep does not identify an r10 finding requiring replacement reports; I do not claim 64/64 delivery. Correct the rationale: `SCORECARD.md:1277-1281,1330-1332` records the operator interruption/no-backfill decision, but `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51` says to re-dispatch for a true shortfall and has no operator-interruption exception. The claimed “per the counting lesson” attribution is not supported by that lesson. EX-14 also flags range-format ambiguity in the frozen roster, which limits confidence in the exact historical ID set.
3. **Full hyper-vs-Devin census — CARRIED-FORWARD (partial).** A local read-only scan found no retained `dispatch*` or `.jsonl` files in arc2 rounds 1–4. The R10 draft still has `<fill>` cells for the hyper measurements at `arc2-loop1-round10/E19.md:212-217`; report counts and E10/E11 samples cannot replace missing dispatch arrays/cutoff evidence. This confirms the partial-census ruling and does not establish that external session logs do not exist.

PL-2/PL-3/PL-4 and EX-13/EX-14/EX-15 converge on no high-memory retest without clearance and on carrying the census forward. Their r10 counts converge at 64 versus 59; the historical missing-name list and lesson rationale remain the reconciliation points above. CN-2’s earlier C2-dependent conditional predated the current EX-12/RV-6 reports, but those reports do not alter the local r10 roster discrepancy. The required aggregate `claims/c3/disposition.md` remains absent.

No REA workload or high-memory retest was launched. I wrote only this verdict artifact; the pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` and all other files were left untouched.
