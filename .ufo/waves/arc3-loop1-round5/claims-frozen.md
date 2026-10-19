# arc3-loop1-round5 — frozen claims, 2026-10-19

Wave: 64 seats, `openai-codex/gpt-6-luna-max` — the scheduled R5 correctness sweep.
Roster frozen PRE-DISPATCH; the items array carries exactly the 64 names below.
Roster enumerated mechanically: 16 + 16 + 16 + 16 = 64, every seat name appearing
exactly once. No lane signal from prior rounds — this is the scheduled provider.

Axis set: **calibration (owned; the sweep re-derives prior claims against live
state)**, **coverage (owned; the sweep audits corpus claims for correctness)**,
**freshness (fleet; the arc2 carried-debt disposition is recorded)**.
Lowest-axis rule: owned proxies tied at 10.0; calibration is the declared
lowest-axis candidate under heterogeneous proxies (SCORECARD:12) and this round
works it directly by re-derivation. Claims are causally separable: the sweep
(read/verify + report), the mid-leg retest (a bounded re-run or an honest
stop record), the debt ledger (recording, not new work).

## C1 — calibration (owned): correctness sweep of arc3 rounds 1–4

The round's job: independently re-derive the load-bearing numbers arc3 rounds
1–4 recorded, and flag any that do not reproduce. Scope: (a) command A at each
of the three admitted work commits (fbbbd45, 28aa7a9+5be4a26, c418be0+40de383)
— the mapped/rule counts must reproduce or the discrepancy is named; (b) the
custody-pair selftest (28 cases) re-run on the landed tree; (c) the citation-
drift probe both modes on the landed tree; (d) the census v10 PASS on the
landed tree; (e) the PROVINCE 162-line hold + the nine stale-literal absences
re-checked by grep -F; (f) the Vyper entry's claims spot-checked against its
own evidence (the 15/15 K/K, the runtime sha256, the dispatch shape).

Claim: after the round, a sweep report exists at
`.ufo/waves/arc3-loop1-round5/claims/c1/sweep-report.md` recording every
re-derived number, each marked REPRODUCED / DISCREPANCY / UNCHECKABLE-with-
cause; every DISCREPANCY names the corrected value and its evidence. Zero
re-derivations are skipped silently.

Falsifiable before → after: the sweep report exists and carries ≥ the six
scoped checks; each carries a re-derived value, not a quoted one.

## C2 — coverage (owned): corpus correctness audit (arc3 entries)

Re-read the four arc3 knowledge entries landed so far (r1 solc, r3 optimizer-
shapes, r4 vyper-leg, plus the r2/r3 errata) and audit each load-bearing claim
against its cited evidence: the selector counts, the sha256 identities, the
dispatch-shape claims, the byte counts, the "no Core promotion" disclaimers.
Any claim that cannot be re-derived from its own entry's evidence is named
with the correction.

Claim: a per-entry audit at `.ufo/waves/arc3-loop1-round5/claims/c2/audit.md`
with one row per load-bearing claim, marked VERIFIED / CORRECTED(with fix) /
UNVERIFIABLE; corrections land as append-only errata on the entries (never
rewrites), or are named for the parent if corpus-side.

Falsifiable before → after: the audit table exists; every named correction
carries its evidence pointer.

## C3 — freshness (fleet): arc2 carried-debt disposition (three items recorded)

The arc2 debt ledger names three items; the round dispositions each —
disposition means a recorded ruling, not necessarily new work:

1. **Mid-leg faithful retest** — the r6 mid-leg OOM was a recipe-provenance
   error (the retest added a 9G cap the original never had; the original ran
   uncapped at a measured 18.26 GiB peak). A faithful retest must run uncapped
   or above 18.3G — operator-host-cost gated. Disposition: EITHER run it
   uncapped on this host IF a bounded check shows ≥20G free RAM AND the
   operator's host-cost gate is satisfied (record the gating check), OR record
   the honest stop with the measured gating reason.
2. **r10 5-seat deficit** — recorded per the counting lesson
   (interruption is operator-side; not re-dispatched). Disposition: record
   the deficit as DISCHARGED-BY-PRECEDENT with the pointer, or re-dispatch
   the 5 seats if the round's sweep shows the r10 findings are needed.
3. **Full C3 census** — wave-interrupted in arc2-r10; the samples stand.
   Disposition: complete the census table (the hyper-vs-devin lane delivery
   comparison) from the recorded wave data, or record why it stays partial.

Claim: `.ufo/waves/arc3-loop1-round5/claims/c3/disposition.md` exists with a
ruling per item (DISCHARGED / EXECUTED / STOPPED-with-reason /
CARRIED-forward), each with evidence.

Falsifiable before → after: three rulings recorded; none silently dropped.

## Seat roster (64, one AgentSwarm items array)

c1 chain (the sweep, 16): SC-1..SC-8, EX-1..EX-4, RV-1..RV-4
c2 chain (the corpus audit, 16): EX-5..EX-12, CR-1..CR-4, RV-5..RV-8
c3 chain (debt disposition, 16): EX-13..EX-20, PL-1..PL-4, RV-9..RV-12
verdicts/convergence (16): VZ-1..VZ-4, CN-1..CN-4, CR-5..CR-8
