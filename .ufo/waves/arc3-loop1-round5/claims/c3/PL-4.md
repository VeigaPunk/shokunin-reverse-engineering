# PL-4 — arc3-loop1-round5 C3 debt disposition

Scope: the three arc2 carried-debt items named in `SCORECARD.md:1329-1332`. This report records only this seat’s checks and rulings; no other path was written.

## 1. Mid-leg faithful retest — STOPPED-with-reason

No retest was launched. The bounded host check was:

```text
$ free -b
               total        used        free      shared  buff/cache   available
Mem:     32483102720 10295726080  1997930496  1106124800 21775114240 22187376640
Swap:    36779188224  3958599680 32820588544
```

`MemAvailable` was 22,187,376,640 bytes (above 20 GiB), while the literal `free` column was 1,997,930,496 bytes. The instruction does not specify which measure defines “free RAM,” and no affirmative operator host-cost authorization/gate result is present in the material available to this seat. Since both conditions were required, I stopped before the resource-intensive run. No retest result is claimed. The rule and stop option are in `claims-frozen.md:60-66`.

## 2. r10 five-seat deficit — DISCHARGED-BY-PRECEDENT

I expanded the frozen roster groups at `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:3` and counted current report files directly:

```text
$ python3 -c 'from pathlib import Path; w=Path(".ufo/waves/arc2-loop1-round10"); groups=[("P",4),("C",4),("E",28),("S",2),("SC",2),("R",8),("CR",8),("V",6),("Z",2)]; roster={f"{p}{i}" for p,n in groups for i in range(1,n+1)}; reports={p.stem for p in w.glob("*.md")}; print(f"expanded_roster={len(roster)}; reports={len(reports)}; absent={len(roster-reports)}"); print("absent_names="+",".join(sorted(roster-reports))); print("unrostered_reports="+",".join(sorted(reports-roster)))'
expanded_roster=64; reports=59; absent=5
absent_names=CR1,E1,E17,E28,R7
unrostered_reports=
```

Thus the current on-disk roster/report difference is five; the historical deficit is retained, not erased. The itemized names in `receipts/roster-reconciliation.txt:1` do not match the current directory (it names P1 absent, but P1.md is present); I use the direct enumeration above for the present set. Per the frozen disposition rule at `claims-frozen.md:67-70`, this seat found no specific r10 finding that requires re-dispatch, so the re-dispatch debt is discharged by the operator-interruption precedent. The counting lesson’s comparison rule is `corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-28`.

## 3. Full C3 hyper-vs-devin census — CARRIED-forward

I did not fill the full comparison table. Independent reconstruction of the historical dispatch denominator requires the actual `items` arrays, not declared intent or a guessed roster (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-24`). The local r1-r4 wave archive search returned:

```text
Glob .ufo/waves/arc2-loop1-round{1,2,3,4}/**/dispatch*  -> No matches found
Glob .ufo/waves/arc2-loop1-round{1,2,3,4}/**/*.jsonl      -> No matches found
```

This establishes only that the checked-in wave directories do not provide those dispatch captures; it does not assert that no external session log exists. Without those primary records I cannot first-hand reproduce the historical denominator, and will not substitute prior seat/round figures. The debt stays partial pending the original r1-r4 dispatch artifacts. The outstanding census is identified at `SCORECARD.md:1332`.
