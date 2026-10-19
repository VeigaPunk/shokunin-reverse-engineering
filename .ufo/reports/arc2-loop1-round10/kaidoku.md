# kaidoku arc2-loop1-round10 — calibration / freshness / adjacency (the rerun round)

Date: 2026-10-18. Wave: 64 seats on `hyper/deepseek-v4.1-flash` (operator
substitution), roster frozen pre-dispatch (the r9 gate's first run); ~59/64
delivered under operator interruption. Work commits: `dbae324` (the coupled
C1+C2 landing), `02c45d5` (probe-needle fix), `af51e91` (wave artifacts).

**Round admitted: all three claims verify** — C1 as the pre-accepted split.

## Work performed

Claims (3, distinct axes):

1. **C1 — calibration** (owned): rerun id-stability, two legs. The big leg
   re-ran the exact r7 request and sealed a byte-identical envelope — the
   r7 entry's last named unknown closes. The mid leg died on a
   recipe-provenance error (a cap the original never had) — named debt with
   the containment requirement measured.
2. **C2 — freshness**: the citation-drift probe table extends to the r7/r8
   citations + SHONEN pointers (31 entries), advisory semantics preserved.
3. **C3 — adjacency**: the hyper-lane substitution census, recorded
   operator-facing.

Work items (pointers): the big-leg seal (P2/E2/V6 + Z1: 23m58.082s wall,
7.8G peak, zero OOM; envelope byte-identity `cmp`-verified by the parent);
the mid-leg kill (P2: 53.602s, cgroup anon 8.96G, `decompile invoked
oom-killer`; the r6 uncapped 18.26 GiB peak from `mid-rung-meta.txt:14`); the
id domain measured from source (Z1 §2.3: RFC 8785 canonical JSON);
the C2 variants adjudicated (Z1 §1.4: E8's 31-entry draft over R2's minimal,
CR2's constraints applied); the coupling (Z1 §1.5: the r7:7 correction rides
the table commit); the C3 samples (E10/E11); the roster gate (E26/V5).

## Landed changes

- `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` — rerun erratum +
  recheck-line correction (id STABLE; id domain measured). Commit `dbae324`.
- `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md` — NOT-resolved erratum
  (containment requirement named). Commit `dbae324`.
- `.ufo/gates/citation-drift/pointer-table.json` — 13 → 31 entries +
  `corpus/README.md:175` re-point (same commit, Z1's coupling); the needle
  fix `02c45d5`.
- Receipts (both envelopes, post-pair, roster reconciliation, MANIFEST) at
  `dbae324`; wave reports at `af51e91`. Records: this commit.
- **Operator-authorized push executed after this commit** (see LOG).

## Before → after measurements

- **C1** — big leg: envelope byte-identical (cmp rc 0), same
  `ev_a4aa9b0d…`, wall 1424.663s → 1438.082s with zero envelope change.
  Mid leg: `Result=oom-kill`, 53.602s, no evidence_id. R7 unknown: CLOSED.
  R6 unknown: named debt (retest needs >18.3G or no cap).
- **C2** — table 13 → 31 entries; probe selftest 11/11; findings=1 → 0
  after the needle fix (the extension's first live catch, in-round).
- **C3** — census recorded in this section's round records (operator-facing).
- Side-harm check — command A: 81/81, 13/13, 10.0/10.0; census v10 PASS.

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists: 13 rules + custody SOP +
  registry + capabilities + the 31-entry probe table; command A 13/13; no
  outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task: the two sealed service reruns (one hold, one
  contained kill) + receipts + this LOG entry; no outside verifier
  (`SHONEN.md:7-8`).
- [~] Executable without oral context: the id-domain derivation (Z1 §2.3)
  and the faithful-retest requirement replay from the entries;
  documentation-level only (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: the hyper census is recorded, not absorbed;
  operator surfaces untouched; no complete outside audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

Stale-lane duty: both services terminal at close (one success, one contained
kill); the wave interrupted by the operator — the deficit is recorded, not
hidden; custody pair captured at both ends.

## Verdicts

- calibration: **improved** — one scale point closed by byte-identical
  re-derivation; the other honestly named debt.
- freshness: **improved** — the table doubles and catches its first live
  drift.
- adjacency: **improved** — the operator's substitution gets its evidence
  record without absorption.
- coverage / depth: **unchanged**.

Stagnation window 10/10 complete (no nudge — capabilities entered in-window).
Regimen continues to round 11 — 32-64 seats on `devin/glm-5-3-flash-max`.
