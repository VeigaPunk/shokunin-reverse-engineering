# SC2 — repository census: HEAD, tree state, the r10 pre-pair/roster receipts

Seat: SC2 (scout), arc2-loop1-round10 (first wave on the hyper provider).
Scope: census only — repo read-only, services observed read-only, never
signalled. No repo file edited by this seat; the only write is this report.

## 1. Verdict

**Census is clean and the two pre-dispatch receipts verify 5/5; the round's
in-flight legs are not.** HEAD is `c561f00d9000f5da13719673c6f2c2f79a572d0a`
(main, the `c561f00`-class the round claims cite). Tracked and staged trees are
**byte-clean** (`git diff --exit-code` and `git diff --cached --exit-code` both
0); the worktree is not literally clean only because r10's artifacts are
untracked, which is the expected pre-integration state. The frozen roster is
**64/64 by class arithmetic** and pre-dispatch this round (the r9 wire-it
amendment lands operationally). Custody `config-pre-pair.txt` is **5/5
byte-identical** to the live files by `sha256sum`.

**The material finding is the big leg: `arc2-r10-big` succeeded and sealed,
re-deriving the r7 `evidence_id` byte-identically — so the r7 entry's last
named unknown ("rerun id-stability is UNKNOWN") CLOSES, CONFIRMED at the 91.6MB
scale point** (see §2g). The r10 rerun's `stdout.json` is byte-identical
(`cmp`) to the committed r7 envelope, wall differed (1424.663 s → 1438.082 s),
and the envelope did not — the id is content+params-keyed and
timing-independent.

**The second finding is the mid leg: `arc2-r10-mid` is dead — kernel MEMCG
OOM-kill at the 9G cap after 53.6 s, with no `evidence_id` minted.** So the
**mid**-scale point does **not** close from this attempt (the r6 entry's
unknown stays open, now named debt), and its typed envelope mislabels the cause
(`cancelled` / "Ghidra startup was cancelled") exactly as the r8 erratum warned.

## 2. Evidence — exact commands + observed output

### 2a. HEAD and tree state

```
$ git log --oneline -1 && git rev-parse HEAD && git rev-parse --abbrev-ref HEAD
c561f00 arc2-loop1-round9: records — SCORECARD round section …; round admitted 3/3
c561f00d9000f5da13719673c6f2c2f79a572d0a
main

$ git diff --exit-code; echo diff_exit=$?; git diff --cached --exit-code; echo cached_exit=$?
diff_exit=0
cached_exit=0

$ git status --porcelain --untracked-files=all
?? .ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc
?? .ufo/waves/arc2-loop1-round10/E21.md
?? .ufo/waves/arc2-loop1-round10/E9.md
?? .ufo/waves/arc2-loop1-round10/P2.md
?? .ufo/waves/arc2-loop1-round10/R4.md
?? .ufo/waves/arc2-loop1-round10/V5.md
?? .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt
?? .ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt
```

Zero tracked/staged edits. At census open the untracked set was the two r10
receipts only; sibling seat reports (`E9.md`, `P2.md`, `V5.md`, `R4.md`,
`E21.md`) landed while this seat was running, and
`.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` is the bytecode side
effect of a seat running the census gate. All are integration-pending, not
drift.

### 2b. Custody — pre-pair verifies 5/5

```
$ tail -n +2 .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt > /var/tmp/…/receipt-body.txt
$ for f in /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
      /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile; do
      printf '%s  %s\n' "$(sha256sum "$f" | cut -d' ' -f1)" "$f"; done > /var/tmp/…/custody-live.txt
$ diff /var/tmp/…/custody-live.txt /var/tmp/…/receipt-body.txt && echo CUSTODY_MATCH=5/5
CUSTODY_MATCH=5/5
```

Observed digests (`.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt:2-6`,
timestamp line `:1` = `2026-10-18T23:56:25Z`), all five equal to the live files:
`16f496e6…` Devin `mcp_config.json`, `38d2a1d0…` OMP `mcp.json`, `6ba8a0f9…`
Kimi `config.toml`, `7d2ca28a…` `.bashrc`, `6c6be761…` `.profile`. The same five
values also equal `/var/tmp/arc2-l10r10-C2-custody-expected.txt` (5/5), and the
pre-pair body is **byte-identical** to r9's pre-pair (`.ufo/waves/arc2-loop1-round9/receipts/config-pre-pair.txt`,
`2026-10-18T23:36:53Z`) and r9's post-pair (`…config-post-pair.txt`,
`2026-10-18T23:53:14Z`) — consistent with the config files' mtimes all
predating `23:36Z` (2026-10-14 17:53:20, 2026-10-14 17:53:20, 2026-10-18
20:16:24, 2026-10-16 13:33:16, 2026-10-15 03:12:07). So no config drift across
r9 pre → r9 post → r10 pre.

**Method trap (recorded for C2's probe/pointer table):** the receipt stores
**64-hex (sha256)** digests. Comparing with `md5sum` reports **5/5 mismatches**
on an untouched tree — a silent false-negative. Verified both ways in this
seat.

### 2c. Frozen roster — 64/64 by arithmetic, pre-dispatch

```
$ python3 - <<'PY'   # parse receipts/roster-frozen.txt:3
P1-P4 planners -> 4 ; C1-C4 connectors -> 4 ; E1-E28 executors -> 28 ;
S1-S2 scribes -> 2 ; SC1-S2 scouts -> 2 ; R1-R8 reviewers -> 8 ;
CR1-CR8 critics -> 8 ; V1-V6 verifiers -> 6 ; Z1-Z2 convergence -> 2
TOTAL = 64
PY
```

`.ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt:2` states the roster
is **PRE-DISPATCH** frozen (r9's was retrospective) and that E25-E28 return;
`:4` asserts `len(items) == 64 == roster seats`. Gap confirmed independently:
`find .ufo -maxdepth 3 \( -name "*items*" -o -name "*dispatch*" \)` → empty, so
the assertion's left side is **unverifiable from the repo** at this position
(the roster is frozen; the items array is not committed). That matches E9's
`:232-235` finding and is the r9 wire-it amendment's own artifact gap.

### 2d. Live legs, read-only (observed, never signalled)

```
$ systemctl --user show arc2-r10-mid.service -p ActiveState -p Result -p ExecMainStatus \
    -p ExecMainExitTimestamp -p MemoryMax -p MemorySwapMax -p Environment
ActiveState=failed  SubState=failed  Result=oom-kill  ExecMainStatus=1
ExecMainExitTimestamp=Sun 2026-10-18 20:57:18 -03
MemoryMax=9663676416  MemorySwapMax=1073741824
Environment=REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G \
  TMPDIR=/var/tmp/arc2-l10r10-mid GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC \
  JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

```
$ journalctl --user -u arc2-r10-mid.service --no-pager -n 40
Oct 18 20:57:18 … arc2-r10-mid.service: The kernel OOM killer killed some processes in this unit.
Oct 18 20:57:18 … arc2-r10-mid.service: Failed with result 'oom-kill'.
Oct 18 20:57:18 … arc2-r10-mid.service: Consumed 4min 14.200s CPU time over 53.602s wall clock time,
                  9G memory peak, 1G memory swap peak.

$ journalctl -k --since "2026-10-18 20:55" --until "2026-10-18 21:05" | grep -i oom
Oct 18 20:57:18 plazir27 kernel: decompile invoked oom-killer: gfp_mask=0x100cca(GFP_HIGHUSER_MOVABLE),
  order=0, oom_score_adj=200
Oct 18 20:57:18 plazir27 kernel: oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=user.slice,
  oom_memcg=/user.slice/user-1000.slice/user@1000.service/app.slice/arc2-r10-mid.service,
  task_memcg=…/arc2-r10-mid.service,task=java,pid=622553,uid=1000
Oct 18 20:57:18 plazir27 kernel: Memory cgroup out of memory: Killed process 622553 (java)
  total-vm:10093312kB, anon-rss:2367976kB, file-rss:22132kB, …, oom_score_adj:200
```

The sealed envelope `/var/tmp/arc2-l10r10-mid/stdout.json` (315 462 B) is the
typed `cancelled` wrapper, **no `evidence_id`**:

```
error: Analysis failed / code: cancelled / category: cancelled
details.operation: list_documents   details.cleanup: complete
details.diagnostics.target_sha256: a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786
details.diagnostics.failure_kind: cancelled
details.diagnostics.failure_message: Ghidra startup was cancelled
```

`a6a9a365…` is the r6 mid-rung artifact
(`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:19`), so the leg was
pointed at the right bytes. Its `runtime_root`
(`/var/tmp/arc2-l10r10-mid/rea-ghidra-FSLOSS/`) was **deleted on cleanup**, so
no `ghidra.log` survives for the mid leg — only `stdout.json`.

`arc2-r10-big` sealed at **21:20:23**. While running it showed
`ActiveState=active SubState=running`, pid 622317 → 622423 (`node …/rea`) →
622629 (`java -Xmx6G`), env exactly
`REA_GHIDRA_DISABLED_ANALYZERS="Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis"`
`REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000` `GHIDRA_HEADLESS_MAXMEM=6G`
`TMPDIR=/var/tmp/arc2-l10r10-big` (the r7 recipe), importing
`target-7a2ccd688f6c.exe` = the r7 artifact. `ghidra.log` (280 lines) shows the
pre-script honored at 20:56:31-32 —
`REPORT: Execute script: …/ReaGhidraAnalysisOptions.java 'Call Convention ID,Deco…'`
then `ANALYZING all memory and code` at 20:56:32. Cgroup `MemoryCurrent` =
`MemoryPeak` = 6 080 274 432 B (6.08G) under the 9G cap, CPU 247 s at that
sample.

### 2e. Big leg sealed — the r7 rerun id-stability unknown CLOSES

```
$ systemctl --user show arc2-r10-big.service -p Result -p ExecMainStatus -p ExecMainCode
Result=success  ExecMainStatus=0  ExecMainCode=0
$ journalctl --user -u arc2-r10-big.service --since "2026-10-18 20:56" | tail -1
Oct 18 21:20:23 … arc2-r10-big.service: Consumed 42min 43.809s CPU time over 23min 58.082s
                 wall clock time, 7.8G memory peak, 769.1M memory swap peak.

$ cmp /var/tmp/arc2-l10r10-big/stdout.json \
      .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json && echo BYTE_IDENTICAL=yes
BYTE_IDENTICAL=yes
$ sha256sum /var/tmp/arc2-l10r10-big/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  /var/tmp/arc2-l10r10-big/stdout.json
$ grep -o 'ev_[0-9a-f]\{16,\}' /var/tmp/arc2-l10r10-big/stdout.json | sort -u
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
$ grep -oE '(segment_count|procedure_count|string_count|analyzer_preset)[^,}]*' \
      /var/tmp/arc2-l10r10-big/stdout.json | head -4
analyzer_preset: "ghidra-default+disabled:Call Convention ID
segment_count: 9
procedure_count: 75218
string_count: 137345
```

The rerun's envelope is **byte-identical** to the committed r7 envelope (5204 B,
same sha256 `a77ebee8…` as the committed receipt, §2f) and carries the **same
`evidence_id ev_a4aa9b0d…`** and the **same census** (9 / 75,218 / 137,345,
same `analyzer_preset`) as
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:15-17`. The journal figures
**differ** — wall 1424.663 s (r7) → 1438.082 s (r10), memory peak 7.9G → 7.8G,
swap peak 769.1M — yet the envelope does not, because those live in the
service journal and not in the envelope. So at the 91.6MB scale point the id is
**content+params-keyed and timing-independent**, and the r7 entry's closing
unknown resolves: **CONFIRMED** (`.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json`
reproduced exactly by a second, independent run under the r7 recipe).

### 2f. Bonus integrity check (cheap, passes)

`sha256sum .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json` →
`a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`, 5204 B —
byte-exact to the committed claim at
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7`. (The file is TOON, so
`json.loads` fails on it; the entry's check is the sha256, which passes.) This
is the same digest the r10 rerun reproduced in §2e.

### 2g. Why the mid leg is not a params-identical rerun of r6

The r6 mid leg ran with **no cgroup cap**: `.ufo/waves/arc2-loop1-round6/E9.md:77`
records `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G … TMPDIR=…`
then `node scripts/rea.mjs analyze <path> --format json` with an outer
`timeout -k 60 5400` backstop that "did not fire" — no `systemd-run`, no
`MemoryMax`. The r10 mid leg is the same env **plus** `MemoryMax=9G` /
`MemorySwapMax=1G` under `systemd-run`. So the two runs differ in the memory
envelope, and the r10 attempt died at that envelope's cap in 53.6 s versus r6's
2479 s hold.

## 3. Verbatim-landable text (drafted, not applied)

For the round's records, if the parent wants the leg outcomes stated in the
lane's own voice:

```text
- Live legs (arc2-loop1-round10, observed read-only; never signalled).
  `arc2-r10-big` (91.6MB Godot ARM64, the r7 three-disable recipe, 9G cap)
  SEALED: exit 0, wall 23m58.082s (1438.082s), 7.8G memory peak / 769.1M swap
  peak; stdout.json is BYTE-IDENTICAL (cmp) to the committed r7 envelope
  `receipts/r7-pe-envelope.json` (5204 B, sha256 a77ebee8…), carrying the same
  `evidence_id ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608`
  and the same census (9 segments / 75,218 procedures / 137,345 strings).
  Wall differed from r7 (1424.663s → 1438.082s) while the envelope did not —
  the id is content+params-keyed, not timing-dependent. The r7 entry's closing
  unknown ("rerun id-stability is UNKNOWN") therefore RESOLVES: CONFIRMED at
  the 91.6MB scale point.
  `arc2-r10-mid` (17.7MB agent-browser, no disables, 9G cap) is DEAD: kernel
  MEMCG OOM-kill at the 9G cap after 53.6s wall / 4m14.2s CPU, trigger process
  `decompile` (journal `decompile invoked oom-killer`,
  `constraint=CONSTRAINT_MEMCG`, `task=java,pid=622553`). Its envelope is typed
  `cancelled` with `failure_message: "Ghidra startup was cancelled"` and NO
  `evidence_id` — the r4/r8 mislabel class: the wrapper is not the diagnosis.
  The mid-scale rerun therefore did NOT re-derive `ev_8b688ce7…`; that
  id-stability question stays open as named debt. Note the r6 mid recipe ran
  uncapped (`.ufo/waves/arc2-loop1-round6/E9.md:77`), so r10-mid is not
  params-identical to the run it was meant to re-derive.
```

Candidate pointer-table / lesson row for the mislabel generalization (C2's
axis; offered, not landed):

```text
| mid-leg OOM mislabel | a MEMCG OOM-kill surfaces in the REA envelope as typed `cancelled` / "Ghidra startup was cancelled" with no `evidence_id`; the cause is only in the systemd journal + kernel log | arc2-loop1-round10 `arc2-r10-mid` (17.7MB, 9G cap, 53.6s) generalizes the r8 erratum's "the `cancelled` wrapper is not the OOM diagnosis" from the 91.6MB control to a 17.7MB target | `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json:1-5`; `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37` |
```

Candidate record text for the closure (C1's axis; offered, not landed):

```text
- Rerun id-stability (arc2-loop1-round10): the r7 91.6MB leg was re-run under the
  identical recipe (same three analyzer disables, 7200s startup deadline, 6G heap,
  9G cap). Envelope sealed byte-identical to the r7 receipt (5204 B, sha256
  `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`) with the
  same `evidence_id ev_a4aa9b0d…` and the same census (9 segments / 75,218
  procedures / 137,345 strings) — while wall differed (1424.663s → 1438.082s) and
  peak memory differed (7.9G → 7.8G). The r7 entry's named unknown "rerun
  id-stability is UNKNOWN" (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7`)
  therefore resolves CONFIRMED for `analyze` at this scale: the id is
  content+params-keyed, not timing-dependent. The mid-scale point stays open —
  `arc2-r10-mid` was kernel-OOM-killed at its 9G cap after 53.6s and minted no
  `evidence_id` (named debt).
```

## 4. Observation / inference / unknown

- **Observation.** HEAD `c561f00`; tracked+staged clean; only untracked r10
  artifacts (2 receipts + 5 sibling reports + one gate `__pycache__`). Custody
  pre-pair 5/5 by sha256, byte-identical to r9's pre- and post-pair bodies.
  Roster pre-dispatch, class ranges summing to 64. `arc2-r10-big` `Result=success`
  and its `stdout.json` byte-identical to the committed r7 envelope with the
  same `ev_a4aa9b0d…`. `arc2-r10-mid` `Result=oom-kill` at 9G/1G after 53.602 s
  with a `decompile`-triggered MEMCG kill and a `cancelled` envelope carrying
  no `evidence_id`. The r7 receipt's sha256 matches its committed claim and the
  rerun.
- **Inference.** (a) The r7 entry's rerun id-stability unknown closes as
  CONFIRMED for `analyze` on a 91.6MB PE under the r7 recipe: identical request
  bytes → identical envelope → identical id, with wall time differing by 13.4 s
  and peak memory by 0.1G across the two runs. This is one verb family and one
  scale point; it does not by itself extend to `analyze_function` or to
  path-sensitive verbs (QUALITY.md:29-30 keeps those per-family). (b) The mid
  leg's typed wrapper is a mislabel for a kernel MEMCG OOM — the r8 erratum's
  class, now at 1/5 the target size and ~1/5 the time. (c) The 53.6 s death at
  the cap with the decompile-worker trigger is *consistent with* the kill being
  driven by un-disabled decompile workers rather than by target scale (r6 held
  2479 s uncapped), but this seat did **not** measure worker count for the mid
  leg and the concurrent 91.6MB big leg plus heavy host swap use (18 GiB of
  34 GiB swap in use, 913 MiB free of 30 GiB) is an unexcluded confounder for
  cgroup pressure timing — hypothesis, not claim.
- **Unknown.** Whether the mid leg was *intended* to carry a 9G cap (the seat
  line says "9G cap", yet it calls the run "the r6 mid-rung recipe", and r6 ran
  uncapped — the seat line and the r6 receipt disagree, and this seat did not
  resolve which is authoritative). Whether a params-identical uncapped rerun
  would re-derive `ev_8b688ce7…` — still UNKNOWN, now with a named obstruction.
  Whether the `len(items)==64` assertion was actually evaluated at dispatch —
  no items artifact exists in the repo to check it against. Whether a
  mid-scale hold is reachable at all under a 9G cap with the full analyzer set
  (this run says no at 53.6 s; r6's uncapped hold does not test the cap).
