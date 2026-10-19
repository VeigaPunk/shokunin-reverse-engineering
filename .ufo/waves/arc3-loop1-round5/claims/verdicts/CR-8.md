# CR-8 — arc3-loop1-round5 verdict and convergence

HEAD at the checks below was `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. Measurements and spot-checks in this report were re-derived from Git objects, the live gates, or committed bytes. Peer reports are used only for convergence comparison unless explicitly identified as peer evidence.

## Rulings

| Scope | Ruling |
|---|---|
| C1 calibration | **REPRODUCED with DISCREPANCIES:** Command A counts and live gates reproduce; supplied commit grouping is wrong for `5be4a26`, frozen custody syntax fails although the subcommand passes, and only 8/9 listed PROVINCE needles are absent. The Vyper identity/selector and dispatcher spot-check is **VERIFIED** as static evidence. Required aggregate `sweep-report.md` is absent. |
| C2 coverage | **UNVERIFIABLE-with-cause (partial evidence present):** a C2 seat report `EX-12.md` has now appeared and includes a substantive audit; its initcode/runtime-byte correction is independently confirmed below. The required aggregate `audit.md` is absent, and I did not independently re-derive every audit row. |
| C3 mid-leg retest | **STOPPED-with-reason:** no affirmative operator host-cost authorization was found; no run was launched. |
| C3 r10 deficit | Current count **REPRODUCED**; **DISCHARGED-BY-PRECEDENT** is permitted by the frozen disposition, but whether missing findings require replacement remains **UNVERIFIABLE** pending the sweep. Historical missing-seat identities and the asserted counting-lesson rationale conflict with current evidence. |
| C3 full census | **CARRIED-forward / partial:** source arrays and cutoff evidence are unavailable in the checked-in paths; the extant table remains unfilled. Required aggregate `disposition.md` is absent. |
| Overall convergence | **UNVERIFIABLE-with-cause:** the three required aggregate artifacts (`sweep-report.md`, `audit.md`, `disposition.md`) are absent. Individual reports do not establish that the full chain deliverables are complete. |

## C1 — calibration

### Command A — REPRODUCED; commit grouping DISCREPANCY

I ran the recipe at `SCORECARD.md:88-124` against the six supplied objects and HEAD. Each row is `revision: mapped/knowledge_files; citation_resolved_rules/rule_blocks`; all rows also had `missing=[]`, `dangling=[]`, `coverage_score=10.0`, and `depth_score=10.0`:

```text
fbbbd45: 82/82; 13/13
28aa7a9: 82/82; 14/14
5be4a26: 83/83; 14/14
c418be0: 83/83; 14/14
40de383: 84/84; 14/14
520341d: 83/83; 14/14
71668cc: 84/84; 14/14
```

The `git show --format='%H%n%P%n%s' --no-patch 5be4a26` result identifies `5be4a265…` as a hygiene commit, parent `c418be0…`, subject `hygiene: drop committed pyc + root-ignore __pycache__`; its diff contains only `.gitignore` and generated `.pyc` removal. It is not an r2 work commit. `520341d` is the parent of `40de383`; the supplied association of measurements to rounds needs correction, not the measurements themselves.

### Landed-tree gates — REPRODUCED, with custody syntax correction

- `TMPDIR=/var/tmp python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`.
- `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- The same citation-drift command with `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- The specified `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 with `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` and `error: the following arguments are required: cmd`. The supported `TMPDIR=/var/tmp python3 .ufo/gates/custody-pair/custody-pair.py selftest` passes: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (scratch stayed under `/dev/shm`). Thus the 28-case result reproduces, but the frozen invocation does not.

### PROVINCE hold and exact needle set — DISCREPANCY (8/9)

`wc -l PROVINCE.md` returned `162 PROVINCE.md`. I checked the exact nine needles in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-11` against the current file. Eight are absent: `Reserve: 91MB Godot ARM64 template`; `all 3 organic cores`; `real solc/vyper-compiled bytecode untested`; `Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS`; `probe-refused since r2`; `pacman pairs beyond expac unexercised`; `absent: 7z`; and `35 features incl. PyGhidra/BSim`. The remaining needle is present at `PROVINCE.md:88`:

```text
JEB (unprobed). Engine installs are operator-owned.
```

Therefore the whole-file “all nine stale literals cleared” statement at `SCORECARD.md:1603-1606` conflicts with the exact scan and its JEB NO-CHANGE ruling: the measured result is 8/9 absent. This is a reporting discrepancy, not a reason to remove the current JEB status.

### Vyper CarrierV spot-check — VERIFIED, static only

The runtime hash is `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0` (`1562` bytes). I ran `rea-agents@6.4.0 inspect-evm-interface` on `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex` with `--format json`, and compared its decoded result to `EX-04/evidence/planted-K.json`: evidence ID `ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f`, 15 functions, all `dispatch="abi"`, selector set equal to planted K, `missing=[]`, `extra=[]`, decoded size/hash matching the runtime.

The local `EX-04/evidence/dispatch-census.py` check independently reports a jump table at `0x600` (13 two-byte buckets), 15/15 bodies reached, 15/15 offset agreement, and probe selector set equal to the leg-chain set. The prefix is `5f3560e01c6002600d820660011b61060001601e395f5156`. These are byte/interface and static-dispatch checks; they do not demonstrate EVM execution or deployed-contract behavior.

## C2 — partial seat evidence; aggregate still missing

The fresh claims scan now includes `.ufo/waves/arc3-loop1-round5/claims/c2/EX-12.md`; consequently, earlier statements in `CN-2.md` and `VZ-4.md` that no C2 Markdown report existed are stale snapshots. `EX-12.md:31` reports that several initcode blobs embed the complete runtime byte sequence and corrects wording that treated a zero-function probe as proof of byte-level absence.

I independently tested the three cited binary pairs by reading and comparing the bytes:

```text
r1 Rv2Token: runtime_bytes=1943 creation_bytes=1971 runtime_embedded_offsets=[28]
r3 VaultB.opt200: runtime_bytes=1621 creation_bytes=1655 runtime_embedded_offsets=[34]
r4 CarrierV: runtime_bytes=1562 creation_bytes=1637 runtime_embedded_offsets=[20]
```

The byte-copy correction is confirmed; it does not imply the initcode itself executes the runtime dispatcher. However, `.ufo/waves/arc3-loop1-round5/claims/c2/audit.md` is absent. EX-12 is a single seat report, and this convergence check has not independently recreated all its selector/hash/dispatch rows, so the full four-entry-plus-erratum audit remains **UNVERIFIABLE-with-cause**, not “no C2 evidence.”

## C3 — carried debt

### Mid-leg retest — STOPPED-with-reason

The frozen condition requires both a bounded check showing at least 20 GB free RAM and operator host-cost authorization (`claims-frozen.md:60-66`). I found no affirmative authorization in the inspected instructions or records and did not launch the uncapped retest. C3 reports PL-4, EX-13–20, PL-2/3, and RV-9/11/12 likewise record a stop rather than a run. This does not claim the RAM condition alone was decisive.

### r10 five-seat deficit — count REPRODUCED; discharge rationale qualified

I expanded `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:3` and enumerated current top-level Markdown reports in the round-10 directory:

```text
expanded_roster=64; reports=59; absent=5; unrostered_reports=
absent_names=CR1,E1,E17,E28,R7
```

The old `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1` instead names P1, CR1, E1, E17, and an unspecified fifth; P1 is present now. Thus the deficit count reproduces, but the historical missing-seat identities do not reconcile.

`claims-frozen.md:67-70` permits recording DISCHARGED-BY-PRECEDENT, subject to the possibility that the sweep shows findings are needed. Separately, `corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51` says a confirmed shortfall gets one replacement per unresolved seat; it does not state an operator-interruption/no-backfill exception. Do not treat `SCORECARD.md:1330-1332`'s attribution of that exception to the lesson as supported by the lesson text. The frozen disposition makes a precedent ruling available, but whether the absent findings are needed remains unverified while the required C2 audit is incomplete.

### Full C3 census — CARRIED-forward / partial

The full hyper-vs-Devin census cannot be completed from the checked-in evidence: searches for dispatch captures and JSONL arrays under arc2 rounds 1–4 returned no matches, and `.ufo/waves/arc2-loop1-round10/E19.md:212-217` still has `<fill>` cells. This establishes missing retained local evidence, not that external session logs never existed. The aggregate `.ufo/waves/arc3-loop1-round5/claims/c3/disposition.md` is absent.

## Peer reconciliation and convergence limits

- C1 reports broadly agree with the Command A values, live gates, custody subcommand correction, and 8/9 literal result. I also read the subsequently visible `SC-3.md` and `RV-4.md`; their measurements support those same corrections. `SC-4.md` and `EX-4.md` assert nine absences using lists that omit `JEB (unprobed)` and substitute other strings, so those assertions are not results over the canonical nine-needle vector.
- C3 reports PL-4, EX-13–20, PL-2/3, and RV-9/11/12 converge on no retest without authorization, a 64/59/5 current count, and a partial census. The roster identities and counting-lesson rationale remain material caveats as described above.
- `VZ-4.md` independently records the same C1 corrections and C3 limitations, but its “no C2 audit/report” snapshot predates `EX-12.md`. `CN-2.md` likewise says no C2 Markdown existed at its inspection; that statement is now stale. EX-12 adds substantive and partly independently confirmed C2 evidence, but it does not replace the absent required aggregate audit.
- No `.ufo/waves/arc3-loop1-round5/claims/c1/sweep-report.md`, `claims/c2/audit.md`, or `claims/c3/disposition.md` was present at the final pre-write scan. Accordingly, do not declare whole-wave convergence complete.

Only this CR-8 artifact was written by this seat. The pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` was left untouched; scratch and temporary data stayed under `/var/tmp` or `/dev/shm`.
