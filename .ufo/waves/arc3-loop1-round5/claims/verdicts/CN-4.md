# CN-4 — arc3-loop1-round5 convergence reconciliation

## Scope and evidence boundary

This verdict reconciles the frozen C1/C2/C3 claims (`claims-frozen.md:17-79`) with the peer artifacts available at this inspection. The frozen roster names 16 seats per chain and 16 convergence seats (`claims-frozen.md:81-86`); the dispatch plan says reports belong under `claims/<chain>/<SEAT>/` (`dispatch-plan.md:4-6`). HEAD for the direct command checks was `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. I wrote only this artifact. Git was not mutated; existing `M .ufo/waves/arc2-loop1-round10/C3.md` was left untouched.

The findings below separate first-hand command output from peer-reported evidence. No high-memory retest, seat re-dispatch, REA target execution, external lookup, or source/corpus correction was performed.

## C1 — calibration: core checks reproduce; literal-sweep discrepancy remains

### Command A and commit attribution — REPRODUCED, with corrected hash mapping

I reran the recipe in `SCORECARD.md:88-124` on the immutable Git trees (Python stdlib plus `git show`/`git ls-tree`; `PYTHONDONTWRITEBYTECODE=1 python3 -B`). Results (`mapped/files`, `resolved/rules`; all `missing=[]`, `dangling=[]`, coverage/depth `10.0/10.0`):

| Revision | Mapped/files | Resolved/rules |
|---|---:|---:|
| `fbbbd45` | 82/82 | 13/13 |
| `28aa7a9` | 82/82 | 14/14 |
| `5be4a26` | 83/83 | 14/14 |
| `c418be0` | 83/83 | 14/14 |
| `015e1ba` | 83/83 | 14/14 |
| `520341d` | 83/83 | 14/14 |
| `40de383` | 84/84 | 14/14 |
| `71668cc` (HEAD) | 84/84 | 14/14 |

`git show -s --format='%h parent=%p %s'` confirms `5be4a26` is a hygiene child of `c418be0`, not an R2 work commit; `520341d` is parent of `40de383`, and `40de383` adds the Vyper entry (also recorded at `SC-3.md:7-19`, `EX-1.md:9-23`, `VZ-4.md:15-29`). Associate measurements with hashes, not the frozen shorthand grouping.

### Landed-tree gates — REPRODUCED; custody invocation spelling is wrong

Fresh commands at HEAD:

- `PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; `PROVINCE.md=162` lines, `SCORECARD.md=1631`, `SKILL.md=390`.
- Citation drift default and `--strict` → respectively `reported findings=0 exit=0` and `clean findings=0 exit=0`.
- `custody-pair.py --selftest` exits 2 with argparse usage because this CLI requires the positional `selftest` subcommand. Corrected, read-only-safe command `TMPDIR=/dev/shm PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/gates/custody-pair/custody-pair.py selftest` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. This agrees with C1 reports (`SC-3.md:21-27`, `EX-1.md:25-33`, `VZ-4.md:31-36`). The test used `/dev/shm` scratch.

### PROVINCE literals — DISCREPANCY (8/9 absent, not 9/9)

The exact nine-item test vector is `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-10`; the frozen claim asks for those literal absences (`claims-frozen.md:23-27`). Current `PROVINCE.md` remains 162 lines, but the exact needle `JEB (unprobed)` is still present at `PROVINCE.md:87-88`. Correct whole-file result: **8/9 absent**. The other eight needles are absent.

This is a literal-result discrepancy, even though `SCORECARD.md:1605-1606` separately adjudicates JEB `NO-CHANGE-with-cause` (the verb was probed; no JEB install exists). The same SCORECARD section says “all nine stale literals cleared” at `:1603-1604`, so the two statements cannot both describe the literal sweep. `SC-3.md:31-38`, `SC-1.md:46-61`, `TB-2.md:67-83`, `RV-1.md:28-45`, and `VZ-4.md:38-46` identify the same 8/9 result. By contrast, `SC-4.md:56-70` and `EX-4.md:31-32` report nine matches absent but use different needles (including the old config/asar strings and omitting JEB); those searches do not falsify the frozen exact-set result. No PROVINCE edit is proposed from this seat.

### Vyper spot-check — VERIFIED as static evidence only

C1 peers re-derived the retained CarrierV evidence: runtime `1,562` bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, selector set 15/15, and the modulo-13 table/XOR-chain shape (`EX-1.md:52-60`, `SC-1.md:62-76`, `RV-4.md:85-111`). The cited byte-level dispatcher checker reports `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and equal probe/leg-chain sets. This verifies the saved bytes/evidence, not runtime contract behavior, deployment identity, or chain state.

### C1 artifact coverage — INCOMPLETE

The C1 frozen roster is SC-1..SC-8, EX-1..EX-4, RV-1..RV-4 (`claims-frozen.md:83-84`). A read-only Python enumeration of `claims/c1/*.md`, compared with those 16 names, returned `roster=16 top_level_md=19 missing_expected=['EX-3']`; the four extra, unrostered names are TB-1..TB-4. The required consolidated `.ufo/waves/arc3-loop1-round5/claims/c1/sweep-report.md` was absent on the latest exact-path Glob check. Thus the individual reports substantiate most checks, but the frozen C1 deliverable is not complete.

**C1 verdict:** substantive checks largely reproduce; record the custody invocation correction, hash-attribution correction, strict 8/9 literal discrepancy, and missing consolidated report / EX-3 artifact. Do not call the C1 chain fully closed.

## C2 — coverage: UNVERIFIABLE-with-cause at chain level

At the current snapshot, `Glob .ufo/waves/arc3-loop1-round5/claims/c2/**/*.md` returns only `EX-12.md`; the required `claims/c2/audit.md` is absent. Of the 16 frozen C2 seats, only EX-12 has a Markdown report; raw JSON and `CR-2`/`CR-3` re-derivation evidence do not replace the per-entry audit table required by `claims-frozen.md:38-53`.

EX-12 reports VERIFIED selector counts, decoded byte identities, dispatch results, and scope disclaimers for the r1/r3/r4 entries (`EX-12.md:7-29,35`). It also reports a real initcode wording correction: runtime bytes occur inside the saved creation blobs at offsets 28 (r1 Rv2Token), 34 (r3 VaultB opt200), and 20 (r4 CarrierV), although the probe reports zero functions on those initcode inputs (`EX-12.md:31`). I independently reran the byte-substring check; output was `r1-Rv2Token creation_bytes=1971 runtime_bytes=1943 runtime_offset=28`, `r3-VaultB-opt200 creation_bytes=1655 runtime_bytes=1621 runtime_offset=34`, `r4-CarrierV creation_bytes=1637 runtime_bytes=1562 runtime_offset=20`. The accurate distinction is probe “parsed-and-empty” versus runtime bytes embedded in initcode; embedding does not mean initcode executes the runtime dispatcher.

Two qualifications remain:

1. The r4 statement is present at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17` and is contradicted by the retained bytes; no append-only r4 erratum was present in this inspection. The r1 entry also retains the old sentence at `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`, but its append-only correction at `:31` explicitly supersedes it.
2. EX-12 cites r3 `:24` as “Creation blobs carry no runtime dispatch table” (`EX-12.md:31`), but the current `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:24` is the Rv2TokenOpt selector observation, not that statement. A corpus-wide literal search finds the cited wording at r1 `:24` and r4 `:17`, not at the alleged r3 location. Do not append a correction against that wrong pointer without identifying the intended source line.

**C2 verdict:** `UNVERIFIABLE-with-cause` for the frozen chain deliverable. EX-12 contributes useful, partly rechecked findings and an erratum candidate, but it is not the required `audit.md`, is only 1/16 seat reports, and contains a miscited r3 target.

## C3 — per-item dispositions converge, with qualifications

1. **Mid-leg faithful retest — STOPPED-with-reason.** The frozen gate requires both the bounded RAM threshold and operator host-cost authorization (`claims-frozen.md:60-66`). Peer samples generally show `MemAvailable` above 20 GiB but literal `MemFree` below it; the threshold wording is ambiguous. No affirmative operator cost authorization is evidenced, so the conjunctive gate is not satisfied and no expensive retest was launched (`EX-13.md:5-22`, `RV-11.md:7-21`, `PL-4.md:5-16`). This is a stop, not a retest result.
2. **R10 five-seat deficit — DISCHARGED-BY-PRECEDENT, with identity/rationale discrepancy.** C3 peers independently reproduce 64 frozen roster slots versus 59 current report files, with current set difference `CR1,E1,E17,E28,R7` (`EX-13.md:24-47`, `EX-17.md:27-51`, `EX-20.md:35-54`). The stored reconciliation receipt instead says `P1, CR1, E1, E17 + 1` (`.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1`); P1 is present in the current tree. `EX-15.md:47-53` notes the wave `C3.md` was modified after that receipt, so current membership does not by itself recover the historical interruption-time set. The specific R5 frozen instruction permits recording the interruption without re-dispatch unless C1 finds the missing reports necessary (`claims-frozen.md:67-70`), and SCORECARD records the prior no-backfill decision (`:1330-1333`). However, the generic true-shortfall lesson says to re-dispatch one replacement per unresolved slot (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`) and states no interruption exception. Keep the discharge conditional on no forthcoming C1 finding requiring those reports; the policy attribution and exact historical identities remain unresolved. No re-dispatch was performed.
3. **Full hyper-vs-Devin census — CARRIED-forward (partial).** Reports agree that file counts are not dispatch denominators: R2-R4 have 60 report files each, but the preserved arrays/rosters needed to derive their denominators are absent; R10 has 59 reports against a frozen 64-slot roster. The E19 table still has `<fill>` cells for delivery, convergence, and defects (`E19.md:212-217`); the promised round report does not carry the full table (`SCORECARD.md:1304-1310`; `EX-13.md:49-53`, `EX-17.md:71-99`, `EX-19.md:52-81`). No full-wave provider-quality or convergence conclusion is supported.

The current C3 peer set contains 15 of 16 expected reports; `PL-1.md` is absent. The required `.ufo/waves/arc3-loop1-round5/claims/c3/disposition.md` was absent on the latest exact-path Glob check. The per-item dispositions converge, but the chain-level artifact remains incomplete.

## Prior verdict snapshots and current convergence result

`CN-2.md:5-7,34-38` correctly recorded that no peer reports were visible at its earlier inspection; that availability result is now superseded by the C1/C3 reports and C2 `EX-12.md`. `VZ-4.md:69-73,89-95` similarly saw no C2 Markdown at its last check; EX-12 now exists, although the required audit remains absent. Treat both as time-bounded snapshots, not current inventories.

Current read-only inventory against the frozen roster:

- C1: 16 expected, 19 Markdown artifacts; EX-3 missing and TB-1..TB-4 unrostered; no `sweep-report.md`.
- C2: 16 expected, one Markdown artifact (EX-12); no `audit.md`.
- C3: 16 expected, 15 Markdown artifacts; PL-1 missing and no `disposition.md`.

**CN-4 ruling:** C1’s checked evidence is substantially reproducible but has explicit discrepancies and an incomplete frozen deliverable; C2 is `UNVERIFIABLE-with-cause` at chain level despite EX-12’s partial findings; C3’s three requested statuses are STOPPED-with-reason / DISCHARGED-BY-PRECEDENT / CARRIED-forward, with the stated roster and policy caveats. Cross-chain completion is **not established**. This report does not claim that the wave or all 64 seat artifacts are complete.
