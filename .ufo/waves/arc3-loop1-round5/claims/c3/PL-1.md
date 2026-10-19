# PL-1 — C3 carried-debt re-derivation

Measured against lane `HEAD` `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. I wrote only this seat artifact. I did not run an REA analysis or initiate the resource-intensive retest.

## Rulings

| Debt | Re-derivation | Ruling |
|---|---|---|
| Mid-leg faithful retest | Prior uncapped receipt re-derived as 18.262848 GiB peak tree RSS. Current memory gate is ambiguous/fails under literal `MemFree`; the separate operator host-cost gate is not established. | **STOPPED-with-reason**; retest result remains uncheckable because it was not run. |
| r10 five-seat deficit | Frozen roster parses to 64 unique seats; current report-file set contains 59, with five exact missing IDs. | **DISCHARGED-BY-PRECEDENT**; the reconciliation receipt's missing-ID list is discrepant and corrected below for this audit. |
| Hyper-vs-Devin census | Re-derived report-file counts are available for r1–r4 and r10. Exact r2–r4 dispatch denominators/task outcomes are not preserved in the inspected wave records. | **CARRIED-forward** for a full dispatch-level census; artifact-count comparison below is complete for files presently recorded. |

## 1. Mid-leg faithful retest — STOPPED-with-reason

`.ufo/waves/arc3-loop1-round5/claims-frozen.md:60-66` requires either a faithful uncapped or >18.3G run after both a ≥20G free-RAM check and the operator host-cost gate, or an honest stop. The raw r6 receipt at `.ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt:12-14` records `peak_tree_rss_kb=19149984`; conversion re-run from that file:

```text
peak_tree_rss_kb=19149984
GiB=18.262848
18.3GiB_threshold_kb=19188940.8
raw_peak_exceeds_18.3GiB=False
```

Fresh bounded memory sample (`free -b`; the table and conversions were read in the same command):

```text
               total        used        free      shared  buff/cache   available
Mem:     32483102720 10749702144   471027712  1112997888 22871699456 21733400576
Swap:    36779188224  4192763904 32586424320
MemFree=471027712 bytes (0.439 GiB)
MemAvailable=21733400576 bytes (20.241 GiB)
20GiB_threshold=21474836480 bytes; available_pass=True; free_column_pass=False
```

`MemAvailable` clears 20 GiB, but literal `MemFree` does not; the instruction says “free RAM” without defining which measure. More importantly, no affirmative operator host-cost authorization/result is present in the current instruction or the cited carried-debt record. Both conditions must be established before the expensive run, so I stopped without launching it. No retest outcome is claimed.

## 2. r10 five-seat deficit — DISCHARGED-BY-PRECEDENT

I parsed the pre-dispatch roster in `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:1-4` (including its `SC1-S2` shorthand as SC1/SC2), then compared its unique IDs against top-level seat-report filenames. Reproduction output:

```text
frozen_roster=64 unique=64
r10: report_files=59/64 coverage=92.1875% missing=E1,E17,E28,R7,CR1
```

This independently reproduces the five-file deficit. It also corrects the exact missing-ID record: `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1` names P1, CR1, E1, E17, and an unspecified fifth; P1 is a substantive report (`.ufo/waves/arc2-loop1-round10/P1.md:1-5,11-16`). The current set difference is E1, E17, E28, R7, CR1. I did not edit the historical receipt.

The operator interruption is recorded in `SCORECARD.md:1277-1280`, and the frozen C3 instruction explicitly offers the DISCHARGED-BY-PRECEDENT route, requiring re-dispatch only if this round needs the missing r10 findings (`.ufo/waves/arc3-loop1-round5/claims-frozen.md:67-70`). The report-file census needs no missing seat's content; re-dispatch would not resolve the older rounds' absent dispatch records below. I therefore did not re-dispatch and do not infer terminal task status from an absent file. This is a ruling on the carried reporting deficit, not a claim that the five tasks failed or completed.

## 3. Hyper-vs-Devin C3 census — CARRIED-forward (full dispatch-level result)

Independent count of seat-named top-level Markdown artifacts:

```text
r1: seat_report_files=64
r2: seat_report_files=60
r3: seat_report_files=60
r4: seat_report_files=60
r10: seat_report_files=59
```

| Wave | Recorded lane/provider | Re-derived report files | Scope of conclusion |
|---|---|---:|---|
| r1 | Mixed `opencode-go` / Devin (`.ufo/reports/arc2-loop1-round1/kaidoku.md:3-6`) | 64 | File count only. |
| r2 | Devin (`.ufo/reports/arc2-loop1-round2/kaidoku.md:3-6`) | 60 | File count only; no round-local frozen dispatch roster located. |
| r3 | Devin (`.ufo/reports/arc2-loop1-round3/kaidoku.md:3-7`) | 60 | File count only; no round-local frozen dispatch roster located. |
| r4 | Devin (`.ufo/reports/arc2-loop1-round4/kaidoku.md:3-8`) | 60 | File count only; no round-local frozen dispatch roster located. |
| r10 | Hyper; pre-dispatch roster at `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:1-4` | 59 of 64 (92.1875%) | Exact report-file coverage; five absent IDs listed above. |

This is not a verified comparison of dispatched-item completion rates for r2–r4: their original item arrays and per-seat dispatch/terminal-status receipts are not in the committed records inspected. A bounded filename search for `*dispatch*`, `*items*`, and `*roster*` under `.ufo/waves/arc2-loop1-round{2,3,4}/` returned `No matches found`; content searches for `"items"`, `items\s*:`, `seat_?id`, and `task_?id` in JSON files under each of those wave directories returned `No non-sensitive matches found`. The r2 manifest at `.ufo/waves/arc2-loop1-round2/receipts/MANIFEST.txt:1-8` inventories config/REA evidence digests, not a dispatch payload. The standing counting rule requires the actual items array and distinguishes a missing report from a known failed task (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-28,39-51,61-69`). Therefore the counts above complete the report-artifact census but cannot establish each historical denominator, missing-seat cause, or a full delivery-rate comparison. The interruption and samples do not support a provider-quality conclusion; no new quality/convergence comparison is claimed.
