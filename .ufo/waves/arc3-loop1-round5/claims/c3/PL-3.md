# PL-3 — C3 carried-debt disposition

HEAD checked: `71668cc`. I re-read the source receipts and independently enumerated the wave files; no prior seat report was used to derive the counts below. Only this artifact is written.

## 1. Mid-leg faithful retest — STOPPED-with-reason

**Historical requirement re-derived; no new retest run.** The original mid-rung launch script is a bare timeout around `node … analyze`, with no `systemd-run` or `MemoryMax` (`/var/tmp/arc2-l6r6-E9-mid/run-leg.sh:65-68`). Its receipt records `peak_tree_rss_kb=19149984`, `peak_java_rss_kb=2884192`, `wall_s=2479` (`.ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt:12-14`). The tree-RSS sum converts to 18.263 GiB; the launcher script sums per-process `VmRSS` (`run-leg.sh:36-39`), so this is a tree-RSS measurement, not a direct cgroup charge. The archived r10 mid envelope is typed `cancelled` (`.ufo/waves/arc2-loop1-round10/receipts/r10-mid-kill-envelope.json:1-3,38-39`); a direct read-only text count returned `r10-mid-kill-envelope.json: evidence_id occurrences=0`. Historical journal and current-unit outputs:

```text
$ journalctl --user -u arc2-r10-mid.service --no-pager -o short-iso
2026-10-18T20:57:18-03:00 plazir27 systemd[1539]: arc2-r10-mid.service: The kernel OOM killer killed some processes in this unit.
2026-10-18T20:57:18-03:00 plazir27 systemd[1539]: arc2-r10-mid.service: Main process exited, code=exited, status=1/FAILURE
2026-10-18T20:57:18-03:00 plazir27 systemd[1539]: arc2-r10-mid.service: Failed with result 'oom-kill'.
2026-10-18T20:57:18-03:00 plazir27 systemd[1539]: arc2-r10-mid.service: Consumed 4min 14.200s CPU time over 53.602s wall clock time, 9G memory peak, 1G memory swap peak.
$ systemctl --user show arc2-r10-mid.service -p Result -p ExecMainStatus -p MemoryMax -p MemoryPeak
Result=success
ExecMainStatus=0
MemoryPeak=[not set]
MemoryMax=infinity
```

Memory gate snapshot (`free -b` plus `/proc/meminfo`): `MemAvailable=21575716 kB = 22093533184 bytes = 20.576 GiB`; 20 GiB is 21474836480 bytes. Thus the Linux `MemAvailable` interpretation clears the numeric threshold. The literal `free` bucket in the same `free -b` output was 1085091840 bytes (about 1.010 GiB), so the threshold depends on interpreting “free RAM” as allocatable/available memory rather than only currently unused pages. **No affirmative operator host-cost approval is present in this seat’s instructions or inspected record.** A memory snapshot alone does not satisfy both gates, so I did not start the uncapped workload; the faithful retest remains open.

Caution: a fresh `systemctl --user show arc2-r10-mid.service` returned `Result=success`, `ExecMainStatus=0`, `MemoryPeak=[not set]`, `MemoryMax=infinity`, whereas the historical journal records `oom-kill`. I do not use the current unit properties to infer the prior run’s cap or outcome.

## 2. r10 five-seat deficit — DISCHARGED-BY-PRECEDENT

The frozen roster says `64 seats == len(dispatch items)` and records the 64-seat class ranges (`.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:1-4`). I expanded those ranges and compared them to direct `*.md` report filenames:

```text
R10: reports=59
R10: frozen_roster=64; missing=['CR1', 'E1', 'E17', 'E28', 'R7']; extra=[]
```

The stored one-line reconciliation (`receipts/roster-reconciliation.txt:1`) names P1 as absent, but the current directory contains `P1.md`; its missing-name list is stale. The current set difference above is the fresh count. The operator-interruption classification is recorded at `SCORECARD.md:1277-1281`; the counting lesson requires comparing against the frozen roster and warns against invented shortfalls (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-33`). This C3 recheck needs only the roster/report reconciliation and does not rely on findings from the absent slots. I therefore discharge the re-dispatch action by the recorded operator-interruption precedent; the five missing reports remain a recorded fact, not a claim of 64/64 delivery. No seats were re-dispatched.

## 3. Full C3 census — CARRIED-forward (partial)

I counted direct `*.md` files in each wave directory:

```text
R1: reports=64
R2: reports=60
R3: reports=60
R4: reports=60
R10: reports=59
```

R10's frozen dispatch denominator is independently available in `roster-frozen.txt:1-4`, so its observed delivery is 59/64 (92.1875%), with five reports absent as listed above. For R1-R4, the counts above are report files only, not delivery rates: I checked the archived wave subtrees with read-only `git ls-tree -r --name-only` at their artifact commits, and found no retained path named for a dispatch, roster, or items array:

```text
df31bfb .ufo/waves/arc2-loop1-round1: dispatch/roster/items artifacts=[]
b21c0da .ufo/waves/arc2-loop1-round2: dispatch/roster/items artifacts=[]
dbba2dd .ufo/waves/arc2-loop1-round3: dispatch/roster/items artifacts=[]
fc8e53c .ufo/waves/arc2-loop1-round4: dispatch/roster/items artifacts=[]
```

Thus R2-R4’s dispatch denominators cannot be re-derived from the retained in-repository artifacts checked here; file counts alone do not prove the items-array size. R1 was a recovery/mixed-provider wave, not a clean Devin-only comparison (`SCORECARD.md:647-652`). I leave the hyper-vs-Devin comparison partial rather than repeat unverified historical ratios. This is the permitted “record why it stays partial” disposition for the census debt (`claims-frozen.md:71-79`); no out-of-repository swarm logs were available to this check.
