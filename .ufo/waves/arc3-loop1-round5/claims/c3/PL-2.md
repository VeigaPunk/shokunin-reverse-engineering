# PL-2 — arc3-loop1-round5 C3 debt disposition

Scope: independently disposition the three arc2 debts from `claims-frozen.md:55-79`. No REA retest was launched. This seat wrote only this artifact; historical numbers below were re-derived from source measurements or a fresh file enumeration, not copied from prior-seat totals.

## 1. Mid-leg faithful retest — STOPPED-with-reason

**Historical peak: REPRODUCED. Retest: STOPPED-with-reason.** The raw r6 sampler record `/var/tmp/arc2-l6r6-E9-mid/meta.txt:12` reads `peak_tree_rss_kb=19149984`. Recalculation: `19149984 / 1024 / 1024 = 18.262848 GiB` (command output: `peak_tree_rss_kb=19149984; GiB=18.262848`). This independently confirms the historical footprint relevant to the frozen retest condition (`claims-frozen.md:60-66`).

Bounded host check, captured at `2026-10-19T11:49:18-03:00`:

```text
$ free -b
               total        used         free      shared   buff/cache    available
Mem:     32483102720 10392260608  1796304896  1108201472 21882290176 22090842112
Swap:    36779188224  3958517760 32820670464
```

`MemAvailable=22,090,842,112` bytes exceeds 20 GiB (`21,474,836,480` bytes). However, the independent operator host-cost gate is not affirmatively satisfied in the task/context. Since both conditions are required, I did not run the resource-intensive retest. The result remains an honest stop, not a failed reproduction.

## 2. r10 five-seat deficit — DISCHARGED-BY-PRECEDENT (VERIFIED)

I expanded the frozen roster role ranges from `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:3` and intersected the expected IDs with direct wave-root Markdown filenames:

```text
$ python3 -c 'from pathlib import Path; base=Path(".ufo/waves/arc2-loop1-round10"); ranges={"P":4,"C":4,"E":28,"S":2,"SC":2,"R":8,"CR":8,"V":6,"Z":2}; expected={f"{p}{i}" for p,n in ranges.items() for i in range(1,n+1)}; files={p.stem for p in base.glob("*.md")}; present=expected & files; print(f"roster={len(expected)}; direct-seat-reports={len(present)}; deficit={len(expected-present)}"); print("missing="+",".join(sorted(expected-present)))'
roster=64; direct-seat-reports=59; deficit=5
missing=CR1,E1,E17,E28,R7
```

The independent count verifies the five-seat shortfall. Ruling: **DISCHARGED-BY-PRECEDENT**, not “full delivery.” `SCORECARD.md:1277-1280` records operator interruption and no backfill; `SCORECARD.md:1330-1332` carries the deficit forward under that operator decision. This arc3 sweep is scoped to arc3 rounds 1–4 and does not require the missing r10 findings, so the frozen claim's re-dispatch condition is not triggered. The measured shortfall remains explicit.

## 3. Full C3 census — CARRIED-forward (UNVERIFIABLE-with-cause)

The r10 delivery side is independently established above (64 frozen seats, 59 reports, five missing). That does not complete the hyper-vs-Devin census. The wave-local draft still has `<fill>` entries in the hyper cells for delivery, sizes, convergence, and defects (`.ufo/waves/arc2-loop1-round10/E19.md:212-217`); its fill recipe asks for the parent dispatch wire line at `:219-234`. The quality/convergence records are explicitly samples, not a complete per-seat comparison (`.ufo/waves/arc2-loop1-round10/E10.md:299-307`; `.ufo/waves/arc2-loop1-round10/E11.md:441-448`).

The round report says only “C3 — census recorded in this section's round records” (`.ufo/reports/arc2-loop1-round10/kaidoku.md:54`); inspection of its full 1–89 lines found no census table. Thus `SCORECARD.md:1309` (“the full census rides in the round report”) is not borne out by that report, while `SCORECARD.md:1332` correctly leaves the full table as debt. The local historical wave receipts inspected contain no dispatch-named artifact; I cannot first-hand re-derive the Devin comparator's dispatch-array denominators from the evidence available here, and will not substitute prior-round totals for that evidence.

**Ruling: CARRIED-forward.** Reason: the complete cross-lane table is absent from the landing report, the wave draft remains unfilled, and sample evidence does not support upgrading it to a full census. Preserve the samples; record only the independently verified r10 delivery result until the primary comparator data and completed table are available.
