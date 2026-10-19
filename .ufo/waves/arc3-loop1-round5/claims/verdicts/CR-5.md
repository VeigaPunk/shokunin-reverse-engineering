# CR-5 — arc3-loop1-round5 per-item verdict

HEAD at direct checks: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. This is an item-level reconciliation of the frozen claims, direct checks, retained bytes, and peer reports. It does not assign a scalar score. Bytecode findings below are static; they do not establish deployed identity or runtime behavior. Unless otherwise noted, `claims/...` paths below are relative to `.ufo/waves/arc3-loop1-round5/`.

## C1 — calibration

| Frozen item | Verdict | Re-derived result |
|---|---|---|
| (a) Command A at named revisions | **REPRODUCED; attribution DISCREPANCY** | Replayed `SCORECARD.md:88-124` against Git objects and HEAD. Every row had `missing=[]`, `dangling=[]`, and coverage/depth `10.0/10.0` (table below). `5be4a26` is a hygiene child of `c418be0`, not an r2 work commit; `520341d` is parent of the r4 work commit `40de383`. Keep counts attached to hashes rather than the frozen round grouping. |
| (b) Custody-pair selftest | **TEST REPRODUCED; INVOCATION DISCREPANCY** | Frozen `python3 -B .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2: `error: the following arguments are required: cmd`. Supported `TMPDIR=/dev/shm PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm` passes `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`; scratch remained under `/dev/shm`. |
| (c) Citation drift, both modes | **REPRODUCED** | Default: `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; `--strict`: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`. |
| (d) Census v10 | **REPRODUCED** | `python3 -B .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; current line counts: PROVINCE 162, SCORECARD 1631, SKILL 390. |
| (e) PROVINCE hold and exact nine needles | **LINE COUNT REPRODUCED; ABSENCE DISCREPANCY (8/9)** | `wc -l PROVINCE.md` → `162`. Exact substring scan against the nine needles at `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` → `needles=9 absent=8 hits=[('JEB (unprobed)', [88])]`. Do not remove the current operator-owned JEB status to satisfy the broad literal assertion; it is at `PROVINCE.md:87-88`. |
| (f) Vyper CarrierV identity, selectors, dispatch | **VERIFIED STATICALLY, with wording DISCREPANCY** | `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin` is 1,562 B, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; the saved probe set at `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json:1` is 15/15 and all `dispatch="abi"`. The prologue has a 13-entry table at `0x600`; all targets are JUMPDESTs, sentinel `0x5e7` occurs three times, and the 15 reported offsets are `PUSH4 pc + 11` (none is itself a JUMPDEST). The entry at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21` says the whole table is copied to memory; actual `CODECOPY` length is 2 and it copies only the selected two-byte entry to `0x1e` (`claims/c1/EX-3/evidence/vyper-table-independent.txt:14-23,38-56`; `claims/c1/EX-3.md:28-30`). |

Command A output (revision → mapped/knowledge files; resolved/rule blocks):

```text
fbbbd45  82/82; 13/13
28aa7a9  82/82; 14/14
5be4a26  83/83; 14/14
c418be0  83/83; 14/14
520341d  83/83; 14/14
40de383  84/84; 14/14
HEAD     84/84; 14/14
```

Git metadata output: `5be4a26 parents=c418be0 hygiene: drop committed pyc + root-ignore __pycache__`; `40de383 parents=520341d arc3-loop1-round4: work — Vyper knowledge entry ...`. The fresh gate commands and outputs are also captured in `claims/verdicts/CR-6.md:19-38`; the Vyper byte-level table correction is corroborated by `claims/verdicts/VZ-3.md:43-49`.

**C1 chain status:** substantial measurements reproduce with the listed corrections, but the required aggregate `claims/c1/sweep-report.md` was absent at the final inventory. At that inventory all 16 named C1 reports existed; `TB-1..TB-4` were additional unrostered files, not substitutes for any missing seat.

## C2 — corpus correctness audit

The following separates retained-byte results from wording and scope issues. Current peer reports substantially audit the artifacts, but do not constitute the frozen consolidated audit.

| Frozen C2 item | Verdict | Evidence and qualification |
|---|---|---|
| r1 solc selector sets / decoded runtime identities | **VERIFIED** | Retained results reproduce Rv2Token 5/5 (1,943 B, `c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74`), KdxToken 6/6 (1,789 B, `9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e`), and Rv2Many 11/11 (1,288 B, `04930d00ac26c1e523e910e6d04c5427e0d2b59de33e5a6eeb238eff58c019f4`); see the entry `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:12-23` and independent re-derivations `claims/c2/CR-3.md:13-18`, `CR-2.md:11-16`. |
| r1 Smoke carrier size/digest | **CORRECTED — append-only wording needed** | `Smoke_sol_Smoke.bin` is 1,370 B of hex text, SHA-256 `530efc7bb166fd47e42fe9623ee347234b99a65691b0a0ad42d2682702986a5f`; decoded creation code is 685 B, SHA-256 `08299f31203e05e5dcdcd2453f9dd5a105a97fd94f2b48194ba18e963c368ebd`. I re-decoded and hashed the carrier; r1 line 15 pairs the decoded size with the text-file digest. Keep both byte domains explicit (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:15`; `claims/c2/CR-3.md:17`). |
| r1 creation/PUSH4 interpretation | **CORRECTED by existing append** | The original creation probe is parsed-and-empty, but decoded Rv2Token initcode is 1,971 B and embeds the 1,943 B runtime at offset 28. Its runtime code ends at byte 1,890; `16ee4b79` is in the CBOR trailer, not executable code. The append at r1 `:31` correctly supersedes the earlier wording at `:24`; clarify that `Rv2Token.creation.hex` is a 3,942-B text carrier when discussing file size (`:12,31`; `claims/c2/CR-3.md:18`). |
| r3 principal carrier selectors, hashes, and dispatcher forms | **VERIFIED from retained evidence; scope qualification remains** | C2 re-derivations report the principal 13/13, 11/11, 8/8, and 5/5 families, their decoded hashes/sizes, and the scoped solc GT/EQ or linear-EQ shapes (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:12-24,28-31`; `claims/c2/CR-3.md:20-25`, `CR-4.md:17-18`). Secondary matrix rows are not uniformly adjudicated: `CR-2.md:23` and `RV-7.md:17` mark some matrix-only claims unverified, while `CR-3.md:22` and `EX-5.md:24` report independent set checks. The missing canonical audit must name its primary payloads and resolve this evidence-scope disagreement. |
| r3 CBOR `43000825` / PUSH4 claim | **CORRECTED — append-only correction needed** | Re-parsed the instruction stream up to each probe's metadata boundary. VaultB nopt: code end 3,110; 15 code-region PUSH4 sites, all selector occurrences; `43000825` is only at file byte 3,157. Rv2TokenOpt: code end 925; six code-region sites (five selectors plus panic `4e487b71`); `43000825` is only at byte 972. The current statement at r3 `:26` treats a CBOR pattern as a code PUSH4; distinguish trailer bytes from opcode-boundary instructions (`claims/c2/RV-6.md:24`; `claims/verdicts/CR-6.md:58`). |
| r4 selector sets, decoded identities, and CarrierV dispatch | **VERIFIED for checked artifacts; static only** | Saved evidence reports CarrierV 15/15, Ex09Vault 7/7, StewardToken 22/22, CarrierW 9/9, Smoke 4/4. CarrierV independently rechecked here at 1,562 B and the digest above; its 13 table words target JUMPDESTs and 15 XOR compare sites agree with the saved selector set. Broader decoded hashes and per-carrier paths are in `claims/c2/CR-3.md:26-30`, `EX-12.md:19-29`, and the r4 entry `:12-24`. These are retained-byte checks, not contract execution. |
| Ex09Vault carrier serialization identity | **DECODED RUNTIME VERIFIED; ORIGINAL INPUT IDENTITY UNVERIFIABLE** | Direct hash of `.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/vyper/Ex09Vault.runtime.hex` gives carrier `1,165 B / 05a2953657736eac3ea4fc53023942e917f24f7128dfac249ddc201c349792e4`, decoding to `581 B / 54b14e306bbaf7614d062c06522e88327177aba576309905008e63a90ad199ee`. CR-2/CR-6 report the original probe input was a distinct 1,163-B `/var/tmp` carrier (`aee38762…`) that is not retained; a later witness binds the checked-in carrier to the same decoded runtime and 7/7 set (`claims/c2/CR-2.md:29`, `CR-6.md:60`). This is a serialization/provenance gap, not a decoded-runtime hash mismatch. |
| r4 `CODECOPY` table description | **CORRECTED** | The copy-length operand is 2: only the bucket-selected two-byte word is copied from `0x600 + 2*(selector % 13)` to memory `0x1e`, not the full 13-entry table (`claims/c1/EX-3/evidence/vyper-table-independent.txt:14-23`). |
| r4 creation/initcode claim | **CORRECTED — append-only wording needed** | The runtime is embedded at offset 20 in the 1,637-B CarrierV creation blob; the probe's zero-function result is parsed-and-empty, not byte-level absence. Corresponding direct byte checks also found r1 Rv2Token at offset 28 and r3 VaultB opt200 at offset 34. The actual current false initcode sentence is r4 `:17`; r1 `:24` is historical and corrected by r1 `:31`. **Do not use the r3 `:24` pointer in `EX-9.md:28`, `EX-12.md:31`, or `CR-6.md:56`: r3 `:24` is the Rv2TokenOpt result, not an initcode sentence** (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24`; `claims/verdicts/VZ-3.md:65-66`). |
| Ex09Vault chain-walk discrepancy | **EX-10 diagnostic is DISCREPANT; 7/7 raw dispatch verified** | `.ufo/waves/arc3-loop1-round5/claims/c2/EX-10.md:19` and `.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/analysis/dispatch-structure.txt:12-21,53-68` show two selectors omitted by that chain walker. Independently parsing `.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.bin` (581 B) and following the mismatch branches yields bucket 0 `d0e30db0,2ddbd13a`; bucket 1 `5c975abb`; bucket 2 empty; bucket 3 `8da5cb5b`; bucket 4 `0ff5ce72,191a62d4`; bucket 5 `2bec1547`. All six table targets are JUMPDESTs; the seven unique selectors equal the probe/planted set. The stale diagnostic needs correction; this does not refute the probe's 7/7. |
| Ghidra feature-count erratum | **VERIFIED** | `ls -1 "$HOME/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features" | wc -l` → `34`; the append-only 35→34 correction and linked PROVINCE repair are at `corpus/knowledge/2026-10-13-ghidra-install.md:66-76`, `PROVINCE.md:46`. |
| “No Core promotion” disclaimers | **CROSS-FILE DISCREPANCY; parent adjudication required** | Each arc3 entry says “no Core promotion” (r1 `:33`, r3 `:35`, r4 `:30`), while `PROVINCE.md:91-93` explicitly labels r1/r3 Core but lists the r4 Vyper carrier without an explicit Core tag. The r1/r3 cross-file status needs temporal clarification; that PROVINCE line does not contradict the r4 entry-local disclaimer. Some C2 reports treat the entry text alone as sufficient, while others assert an r4 conflict; preserve the distinction between the current lane label and the dated entry scope (`claims/c2/EX-6.md:21`, `claims/verdicts/VZ-3.md:67`). This does not imply runtime, deployment, or availability claims. |
| Frozen r2/r3 errata inventory | **UNVERIFIABLE / SCOPE AMBIGUITY** | Current dated arc3 EVM entries are r1/r3/r4. The Ghidra correction is a separate older-named entry; there is no standalone dated arc3-r2 entry. The frozen scope at `claims-frozen.md:38-45` does not identify precisely which older r2/r3 errata need rows. Enumerate the intended errata or record this scope gap; do not invent a missing entry (`claims/c2/EX-7.md:7,12`; `RV-6.md:7,27-29`). |

**C2 chain status: PARTIAL; full frozen audit UNVERIFIABLE-with-cause.** The pre-write inventory was 15/16 (EX-9 absent); a post-write live inventory now finds all 16 named C2 reports, including EX-9. The required `claims/c2/audit.md` remains absent. Reports such as CR-3 and EX-9 give broad re-derivations; they do not replace the required one-row-per-load-bearing-claim aggregate or resolve all named contradictions (`claims-frozen.md:47-53`).

## C3 — arc2 carried debt

| Frozen item | Verdict | Evidence |
|---|---|---|
| 1. Mid-leg faithful retest | **STOPPED-with-reason** | Fresh `free -b` sample: `MemFree=970743808 B`, `MemAvailable=19949240320 B`; the ambiguous “free RAM” threshold is not met by this snapshot under either field. No affirmative operator host-cost authorization was found in the inspected instructions/records, so no high-memory retest was launched. This is a stop, not a retest result (`claims-frozen.md:60-66`). |
| 2. r10 five-seat deficit | **DISCHARGED-BY-PRECEDENT, with identity/rationale discrepancy** | Direct set comparison: `expanded_roster=64 reports=59 matched=59 missing_count=5 extras=[]`; current set difference is `CR1,E1,E17,E28,R7`. The R5 freeze explicitly permits recording the interruption precedent at `claims-frozen.md:67-70`; that disposition is not proof of 64/64 delivery. The stored receipt names P1 among the misses although `P1.md` currently exists (`.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1`). The generic lesson says re-dispatch one replacement per unresolved seat for a true shortfall and does not state an interruption exception (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`); therefore “per the counting lesson” is inaccurate. The exact historical missing IDs remain unresolved. |
| 3. Full hyper-vs-Devin census | **CARRIED-forward / PARTIAL** | Eight bounded searches for `dispatch*` and `*.jsonl` under `.ufo/waves/arc2-loop1-round1` through `round4` returned no matches. `.ufo/waves/arc2-loop1-round10/E19.md:212-217` still has `<fill>` cells. Without retained dispatch arrays/cutoff data, report counts cannot establish historical denominators; absence in the checked-in paths does not prove external logs never existed. No new workload was launched. |

The per-item C3 rulings do not close the chain: required `claims/c3/disposition.md` was absent at the final inventory.

## Live inventory, roster arithmetic, and completion boundary

The pre-write enumeration was time-bounded: it found C1 16/16 named reports plus TB-1..TB-4, C2 15/16 with EX-9 absent, C3 16/16, and 8/12 explicitly enumerated verdict IDs before this CR-5. A subsequent post-write inventory found:

```text
C1: 16/16 named reports; extras TB-1,TB-2,TB-3,TB-4
C2: 16/16 named reports; EX-9 now present
C3: 16/16 named reports; no unrostered reports
Verdicts: 11/12 explicitly enumerated IDs; CN-1 absent
Aggregates: sweep-report.md absent; audit.md absent; disposition.md absent
```

This is a live snapshot, not a claim that the fleet inventory cannot change again.

`claims-frozen.md:81-86` says 64 seats and claims 16 names in each of four groups, but its explicit lists total `16 + 16 + 16 + 12 = 60`: C1 16, C2 16, C3 16, and verdicts only VZ-1..4, CN-1..4, CR-5..8. This is unresolved roster arithmetic, not permission to invent four seat IDs or use the unrostered TB reports to fill them. Individual report arrivals also make older peer inventories time-bounded: for example, CR-3 is now present although VZ-3's earlier snapshot lists it missing (`claims/verdicts/VZ-3.md:13`).

No all-chain completion claim is justified until the roster inconsistency is resolved and the three frozen aggregate artifacts exist. This verdict records per-item results; it does not modify corpus, PROVINCE, SCORECARD, LOG, or custody paths.