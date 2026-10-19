# RV-9 — C3 carried-debt dispositions

Independent read-only re-derivation for arc3-loop1-round5. No REA retest or wave re-dispatch was launched. Three rulings follow; the full provider comparison is explicitly left partial where primary dispatch evidence is absent.

## 1. Mid-leg faithful retest — STOPPED-with-reason

The raw r6 sampler reports `peak_tree_rss_kb=19149984` (`.ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt:7-14`); direct conversion gives **18.262848 GiB**. The run recipe at `/var/tmp/arc2-l6r6-E9-mid/run-leg.sh:65-68` is a direct `timeout ... node ... analyze` invocation, without a cgroup wrapper. This supports the ledger's faithful-retest constraint (uncapped or cap above 18.3G), rather than another constrained run.

Read-only terminal capture, re-run first-hand:

```text
$ journalctl --user -u arc2-r10-mid.service --no-pager -o short-iso -n 5
2026-10-18T20:56:25-03:00 ... Started [systemd-run] ... agent-browser-win32-x64.exe.
2026-10-18T20:57:18-03:00 ... The kernel OOM killer killed some processes in this unit.
2026-10-18T20:57:18-03:00 ... Main process exited, code=exited, status=1/FAILURE
2026-10-18T20:57:18-03:00 ... Failed with result 'oom-kill'.
2026-10-18T20:57:18-03:00 ... 53.602s wall clock time, 9G memory peak, 1G memory swap peak.
```

The bounded host check output was:

```text
$ date -Ins; free -b; awk '/^MemAvailable:/ {print}' /proc/meminfo
2026-10-19T11:54:05,853576726-03:00
Mem: 32483102720 10403528704 933552128 1112829952 22738669568 22079574016
Swap: 36779188224 4197380096 32581808128
MemAvailable: 21562084 kB
```

`MemAvailable` was above 20 GiB, but the literal `free` column was only 933552128 bytes. More importantly, the assignment/inspected records contain no operator host-cost authorization. Because the cost gate is an independent required condition, I STOPPED and did not launch the high-memory retest. This is an honest gate stop, not a retest result.

## 2. r10 five-seat deficit — DISCHARGED-BY-PRECEDENT (aggregate count reproduced)

The pre-dispatch roster groups in `.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:1-4` enumerate 64 IDs. I counted current report files against those IDs independently:

```text
round10: frozen_ids=64; direct_md_reports=59; matched_ids=59; missing=['CR1', 'E1', 'E17', 'E28', 'R7']; unexpected=[]
round10: artifact_delivery_percent=92.1875
```

The aggregate 5-report gap reproduces. The reason is recorded as operator interruption in `.ufo/waves/arc2-loop1-round10/receipts/roster-reconciliation.txt:1` and `.ufo/reports/arc2-loop1-round10/kaidoku.md:3-6`; the counting rule separates delivery accounting from claim verdicts (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:39-51`). Per the frozen instruction, I record the interruption as operator-side and do not re-dispatch these seats or infer a provider-quality result.

Name-level caveat: the receipt says its missing list begins `P1, CR1, E1, E17 + 1`, while a fresh report-file/roster diff finds `CR1, E1, E17, E28, R7` and finds `P1.md` present. Thus the total deficit matches, but the receipt's named set does not match the current files; exact identities at the interruption cutoff remain unresolved. This mismatch is disclosed, not silently reconciled.

## 3. Full hyper-vs-Devin delivery census — CARRIED-FORWARD (partial)

Read-only report-file census, derived from the wave directories:

| Lane / round | Direct `.md` report files | Frozen dispatch denominator independently available here? |
|---|---:|---|
| Devin r2 | 60 | No roster/item-array receipt found in that round's `receipts/` tree |
| Devin r3 | 60 | No roster/item-array receipt found in that round's `receipts/` tree |
| Devin r4 | 60 | No roster/item-array receipt found in that round's `receipts/` tree |
| Hyper r10 | 59 of 64 frozen IDs | Yes; current missing set is `CR1, E1, E17, E28, R7`, subject to the receipt mismatch above |

The direct output was:

```text
round2: direct_md_reports=60; roster_receipt_files=[]
round3: direct_md_reports=60; roster_receipt_files=[]
round4: direct_md_reports=60; roster_receipt_files=[]
round10: frozen_ids=64; direct_md_reports=59; matched_ids=59; missing=['CR1', 'E1', 'E17', 'E28', 'R7']; unexpected=[]
```

The Devin lane identities are recorded in `.ufo/reports/arc2-loop1-round2/kaidoku.md:3-6`, `round3/kaidoku.md:3-7`, and `round4/kaidoku.md:3-6`; however, a count of landed report files does not prove the dispatch denominator or per-task terminal states. The counting lesson requires checking the items array and not inferring task completion from report-file presence (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-27,39-51`). With no such per-round roster/array receipts in the inspected directories, and the r10 cutoff/name mismatch above, I cannot independently complete a dispatch-level hyper-vs-Devin census. Keep this comparison partial; retain only the existing quality/convergence samples and draw no provider-quality conclusion from the interrupted wave.

Reproduction command for the file counts and r10 ID diff:

```sh
python3 - <<'PY'
from pathlib import Path
root = Path('.ufo/waves')
for n in (2, 3, 4):
    d = root / f'arc2-loop1-round{n}'
    reports = {p.stem for p in d.glob('*.md')}
    receipts = sorted(p.name for p in (d / 'receipts').glob('*roster*')) if (d / 'receipts').exists() else []
    print(f'round{n}: direct_md_reports={len(reports)}; roster_receipt_files={receipts}')
expected = ({f'P{i}' for i in range(1,5)} | {f'C{i}' for i in range(1,5)} |
            {f'E{i}' for i in range(1,29)} | {f'S{i}' for i in range(1,3)} |
            {f'SC{i}' for i in range(1,3)} | {f'R{i}' for i in range(1,9)} |
            {f'CR{i}' for i in range(1,9)} | {f'V{i}' for i in range(1,7)} |
            {f'Z{i}' for i in range(1,3)})
d = root / 'arc2-loop1-round10'
reports = {p.stem for p in d.glob('*.md')}
actual = reports & expected
print(f'round10: frozen_ids={len(expected)}; direct_md_reports={len(reports)}; matched_ids={len(actual)}; missing={sorted(expected-actual)}; unexpected={sorted(reports-expected)}')
print(f'round10: artifact_delivery_percent={100*len(actual)/len(expected):.4f}')
PY
```
