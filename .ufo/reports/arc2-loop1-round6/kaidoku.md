# kaidoku arc2-loop1-round6 — coverage (mid-rung HELD) / operability / freshness

Date: 2026-10-18. Wave: 128 seats on `xai-oauth/grok-4.7-fast` — the arc's
first 128/128 (roster frozen per the r5 lesson). Work commits: `045c1b8`
(C2), `596df1c` (C1+C3), `b910a33` (wave artifacts). Two contained user
services ran as round infrastructure (caller-independent per the round-4
--scope lifetime lesson).

**Round admitted: all three claims verify.**

## Work performed

Claims (3, distinct axes):

1. **C1 — coverage** (owned): the scale-wall decisive retry, two legs. The
   91.6MB big leg (service `arc2-r6-pe`, 9G cap, disabled-analyzers set)
   sealed a typed refusal in 7.554s — the guessed analyzer name doesn't
   exist in Ghidra's registry and REA aborts before disabling any name
   (CR9's costume-retry attack, verified from the envelope). The 17.7MB
   mid-rung (service `arc2-r6-mid`, same cap, no mitigation in force) HELD:
   exit 0, `ev_8b688ce7…`, 11 segments / 19,012 procedures in 2479s.
2. **C2 — operability**: probe `--rev` preflight (dead/absent revision →
   exit 2 could-not-evaluate per the registry row's declared map).
3. **C3 — freshness**: the r5-deferred README lessons-index row + SCORECARD
   re-point, landed as a Z2-measured coupled pair.

Work items (pointers): the service watches (E1-E5, SC1: memory profiles,
ghidra.log analyzer verification, cgroup decomposition); the name-registry
research (E3/E4: `Call Convention ID` is the registered class name); the
mid-rung legs (E9-E11, E38, E61: run, independent verification, census
extraction); the entry + token forms (E6, E10, E11, E42: line-neutral map
append re-derived for 80/80); the probe fix (E12-E16, P3, V4: defect
reproduction, convergent fix drafts, 11-case selftest, byte-stability); the
README pair (E17-E20: row text, shift math, re-point, full simulation); the
host-pressure and custody watches (E28, E33, E44, E56); the adversarial
record (CR1-CR16, including CR9's costume attack and CR10's OOM-by-design
challenge — answered by the refusal envelope's OOMKills=0).

## Landed changes

- `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md` — the mid-rung entry
  (envelope census, segment table, ladder placement, explicit not-examined
  list). LOG: this entry; commit `596df1c`.
- `corpus/README.md` — map token joined to the r4-12 row's list (same line;
  187→188 via the lessons row). Commit `596df1c`.
- `SCORECARD.md` — `corpus/README.md:177`→`:178` re-point (same commit as
  the insert). Commit `596df1c`.
- `.ufo/gates/citation-drift/` — probe preflight + expected case. Commit
  `045c1b8`.
- Receipts: mid-rung envelope + meta, big-leg refusal envelope, post-pair.
  Wave reports at `b910a33`. Records: this commit.

## Before → after measurements

- **C1** — command A at `b910a33`: knowledge_files 79 → **80**, mapped 79 →
  **80**, missing [], dangling [], 11/11 rules, coverage 10.0 / depth 10.0.
  The mid-rung envelope: exit 0, `ev_8b688ce7…`, sha256 `2f39ab66…` (5660 B),
  wall 2479s. The big-leg envelope: `execution_failure`, no evidence_id,
  sha256 `4a3ebb82…` (16692 B), wall 7.554s, OOMKills=0.
- **C2** — selftest: `CLEAN cases=11 passed=11` incl.
  `case=rev_unresolvable exit=2`; `--rev deadbeef` → one
  `revision_unresolvable` row, exit 2; `--rev HEAD` → findings=0 exit 0.
- **C3** — probe findings=0 and census v10 PASS post-landing; the coupled
  pair verified by Z2's simulation (insert-without-re-point = findings=1).
- Custody: pre/post 5/5 on own baselines; services touched no custody path
  (fd scans); containment corroborated (zero host OOM, E44/SC1).

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists: 11 rules + custody SOP +
  2-row registry (the probe's declared map now matches its behavior);
  command A 11/11 at `b910a33`; no outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task: the mid-rung analyze (sealed envelope) + both
  contained service runs; receipts + this LOG entry; no outside verifier
  (`SHONEN.md:7-8`).
- [~] Executable without oral context: the entry's recheck line, the probe
  registry rows, and the service-launch pattern (caller-independent units)
  replay from the record (`corpus/lessons` candidate drafted at E52/E53);
  documentation-level only (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: host/process surfaces observed read-only;
  operator configs untouched (5/5 custody throughout); no complete outside
  audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

Stale-lane duty: both services terminal at close (one success, one typed
refusal — neither in-flight); all seat processes closed; custody pair
captured at both ends.

## Verdicts

- coverage: **improved** — 80/80 at `b910a33`; the ladder has two live
  points and the wall has two named classes.
- operability: **improved** — the probe now matches its own registry row.
- freshness: **improved** — the coupled pair landed with zero regressions.
- depth / calibration: **unchanged**.

Stagnation window 6/10. Regimen continues to round 7 — 16-32 seats on
`zai-coding-plan/glm-5.3-flash`.
