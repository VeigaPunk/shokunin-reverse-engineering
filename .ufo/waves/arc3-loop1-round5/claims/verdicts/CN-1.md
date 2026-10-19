# CN-1 — independent arc3-loop1-round5 convergence verdict

## Scope and evidence boundary

This verdict re-derives the frozen C1/C2/C3 claims at `claims-frozen.md:17-79` and reconciles the currently available seat and verdict reports. Direct measurements below are from the immutable Git objects, current files, retained bytecode/evidence, read-only probes, and—only for the historical arc2 dispatch census—the host-local parent session record identified below. Static byte inspection is not EVM execution or deployed-contract evidence. No fresh REA target execution, high-memory retest, re-dispatch, or repository-side correction was made.

Current inventory at this verdict write:

| Area | Current files |
|---|---|
| C1 | All 16 explicitly named frozen reports; plus unrostered `TB-1..TB-4` |
| C2 | All 16 explicitly named frozen reports, including `EX-9.md` |
| C3 | All 16 explicitly named frozen reports |
| Verdicts | 11 of the 12 explicitly named IDs; `CN-1.md` was absent before this write |
| Frozen aggregates | `claims/c1/sweep-report.md`, `claims/c2/audit.md`, and `claims/c3/disposition.md` are absent |

Earlier peer inventories saying C2 had no reports, one report, or 15/16 reports (including `CN-2`, `CN-3`, `CN-4`, `CR-7`, `VZ-2`, `VZ-3`, and `VZ-4`) are time-bounded snapshots. They are superseded by the present 16/16 C2 inventory; the missing `audit.md` is not superseded.

There is a frozen-roster arithmetic inconsistency: `claims-frozen.md:3-6` says 64 seats and 16 per group, while its explicit lists at `:81-86` name 16 C1 + 16 C2 + 16 C3 + only 12 convergence IDs (VZ-1..4, CN-1..4, CR-5..8), totaling 60. The four `TB-*` files are not in those frozen lists. Do not infer four missing IDs or count those extras as rostered replacements without an authoritative roster correction.

## C1 — calibration

### Command A — measurements REPRODUCED; grouping discrepancy

I replayed the recipe at `SCORECARD.md:88-124` against the named Git objects and current HEAD. Results are mapped/knowledge files and resolved/rule blocks:

| Revision | Mapped / files | Resolved / rules |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| HEAD `71668cc` | 84/84 | 14/14 |

Every object had empty missing/dangling sets and 10.0/10.0 coverage/depth scores. Git parent/subject inspection shows `5be4a26` is a hygiene child of `c418be0` (generated `.pyc` removal and `.gitignore` change), not an r2 work commit; `520341d` is the parent of `40de383`. The counts stand per hash; the supplied round grouping does not. See the frozen grouping at `claims-frozen.md:20-22` and commit metadata independently captured in `claims/verdicts/CN-2.md:25` and `claims/verdicts/CR-6.md:31`.

### Landed-tree gates — REPRODUCED with one invocation discrepancy

- Census v10 passes: `stale=0 ambiguous=0 undeclared=0 unresolved=0`; `PROVINCE.md` is 162 lines.
- Citation drift default: `reported findings=0 exit=0`; strict: `clean findings=0 exit=0`.
- The frozen custody invocation `python3 -B .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 because the positional `cmd` is required. The supported `python3 -B .ufo/gates/custody-pair/custody-pair.py selftest` passes all 28 cases. Thus the test result reproduces, but the frozen CLI spelling does not (`claims/verdicts/CN-2.md:27-32`).

### PROVINCE literals — DISCREPANCY (8/9 absent)

`PROVINCE.md` is 162 lines. Searching the exact nine needles recorded in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` finds eight absent; `JEB (unprobed)` remains at `PROVINCE.md:88`. The whole-file “all nine cleared” wording at `SCORECARD.md:1603-1606` conflicts with this result and the separate JEB no-change disposition. Some C1 peers' 9/9 searches used different lists that omit JEB; they do not reproduce the frozen vector. Do not remove the current operator-owned JEB status to make the count fit (`claims/verdicts/CN-2.md:39-40`, `claims/verdicts/VZ-3.md:39-42`).

### Vyper spot-check — STATIC EVIDENCE REPRODUCED; prose discrepancy

The retained CarrierV runtime is 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`. The three saved probe envelopes report 15/15 selectors, matching the retained selector evidence; the 13-entry table at `0x600` points to JUMPDESTs. However, the byte prefix's `CODECOPY` length is 2: it copies only the selected two-byte table entry from `0x600 + 2*(selector % 13)` to memory `0x1e`, not the full 26-byte table. This contradicts the r4 entry's memory-copy wording at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21`; the static correction is recorded at `claims/c1/EX-3/evidence/vyper-table-independent.txt:14-23,38-56`. This is a retained-byte check, not a new provider call or execution result.

C1's measurements mostly reproduce with the corrections above, but the frozen aggregate `claims/c1/sweep-report.md` is absent; the chain is not closed at its required artifact level.

## C2 — corpus coverage

All 16 named C2 reports are now present, but the one-row-per-load-bearing-claim aggregate `claims/c2/audit.md` is absent. The frozen scope at `claims-frozen.md:38-53` names the r1/r3/r4 entries and “r2/r3 errata”; the current dated arc3 EVM files are r1, r3, and r4, with no standalone dated arc3-r2 entry. The intended fourth audit unit / errata list therefore remains ambiguous. Individual seat reports do not substitute for the aggregate.

### Independently re-derived byte findings

- **Smoke byte domains:** `Smoke_sol_Smoke.bin` is a 1,370-byte hex-text carrier, SHA-256 `530efc7bb166fd47e42fe9623ee347234b99a65691b0a0ad42d2682702986a5f`. Decoding it yields 685 bytes, SHA-256 `08299f31203e05e5dcdcd2453f9dd5a105a97fd94f2b48194ba18e963c368ebd`. The r1 entry pairs the decoded size with the text-carrier digest at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:15`; keep both representations distinct (`claims/c2/EX-7.md:18`, `claims/verdicts/CN-2.md:58`).
- **Embedded runtimes in creation blobs:** Rv2Token runtime (1,943 B) occurs at offset +28 in 1,971 B creation bytes; VaultB opt200 runtime (1,621 B) at +34 in 1,655 B; CarrierV runtime (1,562 B) at +20 in 1,637 B. A zero-function creation probe means parsed-and-empty, not that the blob lacks runtime bytes or that initcode executes the embedded dispatcher. The old r1 sentence at `:24` is superseded by its append at `:31`; the false r4 wording remains at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`.
- **Mislocated initcode citations:** `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24` is the Rv2TokenOpt result, not an initcode-absence sentence. `claims/c2/EX-12.md:31` and `claims/verdicts/CR-6.md:54-61` misattribute the creation wording to that r3 line; the live false sentence is r4 `:17`. `VZ-1.md:57` additionally says CR-6 later corrects itself at `CR-6.md:66`, but that line is in its C3 retest discussion, not an r3 citation correction. Do not propagate those pointers.
- **r3 CBOR boundary:** opcode-boundary checks put the VaultB nopt code end at byte 3,110 and its `43000825` marker at 3,157; Rv2TokenOpt code ends at byte 925 and its marker is at 972. The marker is trailer metadata, not an executable code-region PUSH4 as r3 `:26` claims. Selector counts are unaffected (`claims/verdicts/CN-2.md:60`, `claims/verdicts/VZ-3.md:63-65`).
- **Ex09Vault dispatch dispute:** independently walking the raw 581-byte runtime's six table heads at `0x239` (`0x18, 0x204, 0x220, 0x1e9, 0xf7, 0x1b8`) and following mismatch edges recovers all seven planted selectors in the correct `%6` buckets. Bucket 0 is `d0e30db0 -> 2ddbd13a`; bucket 1 `5c975abb`; bucket 2 empty; bucket 3 `8da5cb5b`; bucket 4 `0ff5ce72 -> 191a62d4`; bucket 5 `2bec1547`. Thus the 7/7 static dispatch result holds, while `claims/c1/EX-09/analysis/dispatch-structure.txt:53-68` and `claims/c2/EX-10.md:19` incorrectly report two missing selectors. This agrees with `claims/verdicts/VZ-3.md:65-66` and contradicts `claims/verdicts/CR-7.md:28`, which leaves the chain unresolved. It is byte inspection, not execution.
- **Core boundary:** r1 and r3 corpus entries disclaim Core promotion (`r1:33`, `r3:35`), while `PROVINCE.md:91-93` labels the r1/r3 real-solc carriers Core. That cross-file status is unresolved and requires parent adjudication. The r4 Vyper item is named without an explicit Core tag; do not extend the conflict to r4 (`claims/verdicts/CN-2.md:66`, `claims/verdicts/VZ-3.md:67`).
- **Auxiliary matrix limit:** peers report conflicting levels of support for VZ-1's auxiliary matrix rows. Alternate envelopes can support some selector/hash re-derivations, but the exact path-sensitive matrix IDs and `extras_push4` fields are not bound by the primary evidence checked here. Leave those exact fields UNVERIFIABLE rather than asserting all matrix rows verified or absent (`claims/verdicts/CN-2.md:65`, `claims/verdicts/CR-7.md:27`).

C2 is therefore substantively advanced but not a complete frozen audit: the per-entry aggregate is missing, scope remains unclear, and the corrections/status conflicts above need disposition. No corpus edits were made.

## C3 — arc2 carried-debt dispositions

### 1. Faithful mid-leg retest — STOPPED-with-reason

A bounded `free -b` sample recorded `free=1,049,260,032 B` and `available=19,433,107,456 B`; the threshold wording (“20G free RAM”) is ambiguous, but this sample is below 20 GB even on the available field. More importantly, no affirmative operator host-cost authorization is recorded. The frozen conjunction at `claims-frozen.md:60-66` is not met; no high-memory retest was launched. This is a stop, not a retest result.

### 2. R10 five-seat deficit — DISCHARGED-BY-PRECEDENT, not delivery completion

Expanding the current R10 roster and comparing top-level report files yields 64 roster slots, 59 reports, and five current absences: `CR1,E1,E17,E28,R7`; no unrostered reports. The old `receipts/roster-reconciliation.txt:1` instead names P1 among the missing reports, although `P1.md` exists; the range notation in the frozen roster also needs care. The deficit count reproduces, but the historical interruption-time identities do not. The R5 freeze expressly allows a `DISCHARGED-BY-PRECEDENT` ruling unless the sweep shows the missing findings are needed (`claims-frozen.md:67-70`). The generic lesson at `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51` instead requires replacement dispatch for a true shortfall and supplies no interruption exception; it is not the authority for discharge. Record the specific frozen option, do not claim 64/64 delivery, and reopen if the missing findings prove necessary.

### 3. Full hyper-vs-Devin census — CARRIED-FORWARD / PARTIAL, with recovered dispatch data

Unlike peers limited to checked-in round directories, I parsed the host-local parent session record at `/home/vgpnk/.kimi-code/sessions/wd_kaidoku-shokunin_149e98cdb2ff/session_452a340b-3646-4fa2-87f8-9f88fb955cd5/agents/main/wire.jsonl`. It is uncommitted host evidence, not a checked-in wave artifact. Its dispatch/result records yield:

- R1: initial 64 items, 18 completed / 46 aborted; Devin recovery dispatched exactly the 46 initial unfinished seats and completed all 46, giving 64 unique seats across the two attempts (`wire.jsonl:168,400,445,639`).
- R2, R3, R4: 60 items dispatched and 60 completed in each round (`:880,1142`; `:1696,1965`; `:2237,2511`).
- Hyper R10: 64 dispatched, 44 completed / 20 aborted (`:4893,5164`). The archive has 59 report files; 15 of the 20 aborted tasks nevertheless have reports, leaving current report absences `CR1,E1,E17,E28,R7`.

I also compared the archived Markdown reports (R10 Git tree `af51e91`) and independently re-applied the structural scan logic embedded in `arc2-loop1-round10/E11.md:241-389`:

| Round | Reports | Total bytes | Median bytes | Min–max bytes | E11 fingerprint slots / misattributions |
|---|---:|---:|---:|---:|---:|
| R1 | 64 | 846,743 | 12,770 | 5,091–26,067 | 0 / 0 |
| R2 | 60 | 1,262,236 | 19,453 | 10,196–39,596 | 0 / 0 |
| R3 | 60 | 1,561,084 | 23,853 | 12,116–53,763 | 4 / 0 |
| R4 | 60 | 1,618,367 | 26,772 | 12,858–55,158 | 4 / 0 |
| R10 | 59 | 1,144,105 | 19,688 | 6,428–30,691 | 16 / 0 |

This materially repairs the earlier “no dispatch arrays available” picture: the host-local record establishes delivery counts, and the archive supports report-size and structural-census comparisons. It does not fill the entire E19 table at `arc2-loop1-round10/E19.md:212-217`: the table also calls for convergence/claims-admitted and defect counts. E11 measures structural fingerprints, not semantic correctness; E10 is only a six-report quality sample (`E10.md:12-44,208-212,305-307`). Accordingly, do not turn these figures into a full-population semantic-quality ranking or causal provider comparison. Keep C3 item 3 partial until the remaining table cells are supported by primary records. The checked-in E19 draft still has `<fill>` cells at `:214-217`.

## Peer reconciliation and overall ruling

- C1 peers converge on the Command A values, corrected custody invocation, exact 8/9 literal result, and Vyper copy-length correction. Searches omitting JEB do not rebut the frozen vector.
- C2 inventory statements in early verdicts are stale, but the aggregate remains absent. The Ex09Vault parser claim is resolved by raw-byte traversal; CR-7's unresolved conclusion is not supported. The r3 `:24` initcode pointer and VZ-1's claim that CR-6 later repaired it are also inaccurate. Preserve the Core-status, matrix-binding, and r2/r3 scope uncertainties.
- C3 peer findings correctly identify the missing historical roster identities and counting-lesson mismatch. Their checked-in-directory searches missed the host-local parent wire record; that record improves delivery counts but does not establish semantic provider quality or fill E19's convergence/defect cells.
- No all-chain completion claim is justified. C1 measurements reproduce with explicit discrepancies; C2 remains **UNVERIFIABLE-with-cause** at the required aggregate level; C3 has a stopped retest, a precedent disposition (not 64/64 delivery), and a partially reconstructed census. The three frozen aggregate artifacts and the roster arithmetic remain open.

This seat created only `claims/verdicts/CN-1.md`. The pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` was not touched.