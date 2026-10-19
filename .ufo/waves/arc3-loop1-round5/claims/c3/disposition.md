# arc3-loop1-round5 — C3 aggregate: arc2 carried-debt disposition

Consolidated from the 16 c3-chain seat artifacts (EX-13..20, PL-1..4,
RV-9..12). Parent-written aggregate; each ruling cites the seats that
re-derived it first-hand. HEAD at disposition close: `71668cc`.

The three arc2 debt items get a recorded ruling each: DISCHARGED / EXECUTED /
STOPPED-with-reason / CARRIED-forward. None silently dropped.

## Item 1 — mid-leg faithful retest → **STOPPED-with-reason**

The debt: arc2-r10's mid-leg re-run was kernel-OOM-killed at a 9G cgroup cap
that the original r6 run never had — the original ran uncapped at a measured
18.26 GiB peak (`arc2-loop1-round6/receipts/mid-rung-meta.txt:12-14`,
`peak_tree_rss_kb=19149984` = 18.262848 GiB — just *under* the 18.3 GiB
threshold). A faithful retest must run uncapped or above 18.3G.

**Gating check (re-derived by EX-13, PL-1, EX-19):**
- `MemAvailable` ≈ 20.2–20.6 GiB → passes a literal "≥20G free RAM" reading
  under `MemAvailable`; fails under literal `MemFree` (~0.4–0.7 GiB). The
  frozen condition says "free RAM" without naming the measure — ambiguous.
- **The operator host-cost gate is not evidenced** in this round's
  instruction or the carried-debt record — and the conjunctive condition
  requires BOTH the RAM check AND that gate.

**Ruling: STOPPED-with-reason.** No seat launched the uncapped retest —
correctly: an unapproved ~20 GiB memory-heavy run is exactly what an honest
stop exists for. This is a permission-gate stop, not a retest result and not a
failed memory check. The debt stays open as *operator-gated*: it discharges
the moment the operator authorizes the host cost (or a future round runs it
with that authorization recorded).

## Item 2 — r10 five-seat deficit → **DISCHARGED-BY-PRECEDENT** (corrected set)

The debt: arc2-r10's wave delivered 59/64 reports under operator interruption.

**Re-derived (EX-13, PL-1, EX-19):** frozen roster parses to 64 unique seats;
the report set has 59 files; the exact missing set is **E1, E17, E28, R7, CR1**
— a corrected list: the older reconciliation receipt named P1 among the
missing, but `P1.md` is a substantive present report, so the corrected set
supersedes it. Interruption is operator-side (`SCORECARD.md:1277-1280`,
`.ufo/reports/arc2-loop1-round10/kaidoku.md:74-75`).

**Ruling: DISCHARGED-BY-PRECEDENT** per the frozen claim's explicit option:
record the interruption disposition, re-dispatch only if the sweep needed the
missing findings. The C1 sweep did not need any missing r10 report as
evidence. **Caveat recorded honestly (VZ-1, EX-19):** the counting lesson
(`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`) limits
replacement to a confirmed true shortfall during the wave and carries no
interruption exception — so the basis is the frozen R5 option, not a general
"interruption needs no backfill" rule. The five tasks' terminal status is not
inferred; the ruling is on the *reporting* deficit only.

## Item 3 — full C3 hyper-vs-devin census → **CARRIED-forward (partial)**

The debt: arc2-r10's lane-delivery comparison was wave-interrupted; samples
stood but the full table was never completed.

**Re-derived (EX-13, PL-1, EX-19):** report-file counts are measurable —
r1:64, r2:60, r3:60, r4:60, r10:59 seat-report files. **But report files are
not dispatch denominators:** no archived wave directory preserves the
serialized `items` array, so `D = len(items)` cannot be freshly re-derived for
the historical comparison. The E19 census table still has `<fill>` cells at
`.ufo/waves/arc2-loop1-round10/E19.md:212-217`.

**Ruling: CARRIED-forward.** The file-level census is complete and recorded
above; the dispatch-denominator census stays partial because the denominator
isn't reconstructible from in-repo artifacts. No provider-quality conclusion is
drawn from an interrupted wave — recorded as such. A future round can close it
only by locating external session/dispatch logs, which are out of repo scope.

## Closing

All three items carry a recorded ruling with evidence: one honest stop
(operator-gated), one precedent discharge (with the counting-lesson caveat
named, not smoothed), one carried-forward partial (with the missing
denominator named). The arc2 carried-debt ledger is discharged of its two
administrative items; the one substantive item (mid-leg retest) stays open as
explicitly operator-gated.
