# SC1 (scout) — custody corroboration + config pin census

Seat scope: verify the pre-pair custody receipt 5/5; census the config pins; answer
"any churn since r9's post-pair?". Read-only everywhere outside this repo; no repo
file edited by this seat; no service signaled.

## 1. Verdict

**Custody: CORROBORATED 5/5, and zero config churn since r9's post-pair.** All five
declared hashes recompute byte-identical, and they equal r9's post-pair receipt exactly
— so the r10 pre-pair surface is the same surface r9 closed on.

**Config pin census: CLEAN.** Command A at HEAD `c561f00` reproduces 81/81 mapped,
13/13 citation-resolvable rules, 10.0/10.0. Census v10 `VERDICT: PASS (stale=0
ambiguous=0 undeclared=0 unresolved=0)`. The three client pins re-derive to
`devin=6.5.0 / omp=6.5.0 / kimi=6.7.0` and are independently grep-confirmed in the
configs, not taken from the instrument.

**`arc2-r10-big` SEALED, and `ev_a4aa9b0d…` RE-DERIVES EXACTLY.** The leg completed
`Result=success` at `2026-10-18T21:20:23-03` (23min 58.082s wall, 7.8G peak, 769.1M swap)
and its envelope is **byte-identical** to r7's committed envelope — same sha256
`a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`, same 5204 bytes,
`cmp` clean, same `evidence_id`
`ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608`. The r7 wall
entry's last named unknown — rerun id-stability — therefore **CLOSES at the 91.6MB scale
point**: analyze ids are content+params-keyed and stable across a rerun.

**Scout finding (new, outside the seat's two named legs).** `arc2-r10-mid` is **not
in flight — it is dead.** It was kernel-OOM-killed at its own 9G cap in 53.602s, and
its tool envelope is typed `cancelled` with no `evidence_id`, so `ev_8b688ce7…` did
**not** re-derive; the r6 mid-rung unknown stays **OPEN**. Separately, the dispatched
"r6 mid-rung recipe (… 9G cap)" is a **recipe-provenance error**: the r6 mid leg ran
with **no cgroup memory cap at all**; the `MemoryMax=9663676416` of round 6 belonged to
`arc2-r6-pe.service`, the 91.6MB big leg. The mid leg as dispatched cannot seal, and a
faithful rerun of the same 9G-capped unit is expected to die again.

So the pair splits cleanly: **one leg sealed with a byte-identical envelope, one leg
died at its own cap.** The r7/r6 entries' shared unknown resolves for r7 and not for r6.

## 2. Evidence

### 2a. Custody — recomputed vs declared vs r9 post-pair

```text
$ sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
    /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
6ba8a0f95b8508229fe7137613819597b4da3ea92a873340f2d82b3cf36a73ac  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile
```

These five lines are byte-identical to
`.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt:2-6` (its header timestamp
is `2026-10-18T23:56:25Z`). They are also byte-identical to
`.ufo/waves/arc2-loop1-round9/receipts/config-post-pair.txt:2-6`:

```text
$ diff <(grep -E '^[0-9a-f]{64}' .ufo/waves/arc2-loop1-round9/receipts/config-post-pair.txt) \
       <(grep -E '^[0-9a-f]{64}' .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt)
IDENTICAL: zero churn
```

r9's own pre-pair (`config-pre-pair.txt:2-6`, header `2026-10-18T23:36:53Z`) carries the
same five values, so the whole r9 window was churn-free too. A cross-check of the same
five values in the round's own expected file
(`/var/tmp/arc2-l10r10-C2-custody-expected.txt`, 480 B) matched as well — this seat read
it; it was not authored by this seat.

**5/5 corroborated. Churn since r9 post-pair: none.**

### 2b. Config pin census — command A and census v10

```text
$ REV=c561f00d9000f5da13719673c6f2c2f79a572d0a   # SCORECARD.md:92-123 recipe, unmodified
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 81, "mapped": 81, "missing": [], "rule_blocks": 13,
 "revision": "c561f00d9000f5da13719673c6f2c2f79a572d0a"}
```

81/81, 13/13, 10.0/10.0 — matches the round's stated baseline exactly. The recipe is at
`SCORECARD.md:92-123`; `rule_blocks: 13` is consistent with queue-drain rules #11–#13
(`SCORECARD.md:1122,1237`).

```text
$ python3 .ufo/gates/c1-census-v10.py --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1268 loci=9
SKILL.md       lines=371  loci=2

SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Independent grep corroboration of the same three pins (so the census anchors are not
merely self-consistent):

```text
$ grep -oE '@[0-9]+\.[0-9]+\.[0-9]+' /home/vgpnk/.config/devin/mcp_config.json   -> @6.5.0
$ grep -oE '@[0-9]+\.[0-9]+\.[0-9]+' /home/vgpnk/.omp/agent/mcp.json            -> @6.5.0
$ grep -nE 'version|@[0-9]' /home/vgpnk/.kimi-code/config.toml                   -> 6.7.0 pin present
```

The census loci counts (PROVINCE 6, SCORECARD 9, SKILL 2) are re-derived each run, so a
file that grew without new loci cannot silently shrink the census (`c1-census-v10.py`
L1/L3 header, `:1-60`).

Fleet claim C2's probe instrument was corroborated from this seat rather than assumed:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
SELFTEST_CASE: CLEAN ... (11 cases)
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0
```

### 2c. Scout finding — `arc2-r10-mid` died; the dispatched "r6 recipe" misstates the cap

```text
$ systemctl --user show arc2-r10-mid -p ActiveState,SubState,Result,MemoryPeak,MemorySwapMax
ActiveState=failed
SubState=failed
Result=oom-kill
MemoryPeak=9663676416        # == MemoryMax exactly: the cap-saturated kill signature
MemorySwapMax=1073741824

$ journalctl --user -u arc2-r10-mid --no-pager -o short-iso
2026-10-18T20:56:25-03:00 ... Started [systemd-run] ... npx -y rea-agents@6.5.0 analyze .../agent-browser-win32-x64.exe.
2026-10-18T20:57:18-03:00 ... arc2-r10-mid.service: The kernel OOM killer killed some processes in this unit.
2026-10-18T20:57:18-03:00 ... Failed with result 'oom-kill'.
2026-10-18T20:57:18-03:00 ... Consumed 4min 14.200s CPU time over 53.602s wall clock time, 9G memory peak, 1G memory swap peak.
```

The unit's own environment and cap:

```text
$ systemctl --user show arc2-r10-mid -p Environment -p MemoryMax -p MemorySwapMax
MemoryMax=9663676416
MemorySwapMax=1073741824
Environment=REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G
            TMPDIR=/var/tmp/arc2-l10r10-mid GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
            JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

No `REA_GHIDRA_DISABLED_ANALYZERS` — the "no disables" half of the recipe is faithful.
The target identity is right: the error envelope's `diagnostics.target_sha256` is
`a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786` (the r6 mid-rung
artifact, `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:9`) and
`provider_version: 12.1.4`.

The envelope itself (`.ufo/waves/arc2-l10r10-mid/stdout.json`, 315462 B, sha256
`56e87061869d8928c84a4c0926c5cd5e17c1ce56a0c0166f48ddafa9e4bb0981`, mtime
`2026-10-18 20:57:18.810 -0300`):

```text
error: Analysis failed
code: cancelled
category: cancelled
message: Analysis was cancelled. Start it again when ready.
retryable: true
details:
  operation: list_documents
  ...
    failure_kind: cancelled
    failure_message: Ghidra startup was cancelled
```

**No `evidence_id` anywhere in the 315 KB.** `ev_8b688ce7b54ef1d08823734fda2f062fd19dfa2ca9f4023c329cbae22f726986`
(`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:3,7`) did **not** re-derive.

That `cancelled` wrapper is the r4 mislabel class, and it is now reproduced at a second
target and a second scale. The r8 natural control's envelope is the *same* shape — same
`code: cancelled`, same `details.operation: list_documents`, zero `evidence_id`
(`.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json:1-9`), while its journal
says `oom-kill`. So the wrapper is not an OOM diagnosis in either case; only the systemd
resource record is. (r9 already recorded this limit: `SCORECARD.md:1232-1235`, R1's
"receipt's `cancelled` wrapper is not itself the OOM diagnosis".)

The recipe-provenance error. The r6 mid leg's recorded invocation is a **bare shell
command with an outer `timeout` backstop — no cgroup memory cap**
(`.ufo/waves/arc2-loop1-round6/E9.md:27-38`):

```text
REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 \
GHIDRA_HEADLESS_MAXMEM=6G \
GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC \
TMPDIR=/var/tmp/arc2-l6r6-E9-mid/tmp \
  /usr/bin/timeout -k 60 5400 \
  node .../rea-agents/scripts/rea.mjs analyze <bin> --format json
```

with `REA_GHIDRA_DISABLED_ANALYZERS` unset, and it exited 0 after 2479 s
(`.ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt`: `exit_code=0`, `wall_s=2479`,
`peak_tree_rss_kb=19149984`, `peak_java_rss_kb=2884192`). No `systemd-run` appears in
that leg's record; the only `systemd-run` in round 6's reports is the big leg
(`.ufo/waves/arc2-loop1-round6/C6.md:1,21-34`), whose unit carries

```text
Id=arc2-r6-pe.service
MemoryMax=9663676416
FragmentPath=/run/user/1000/systemd/transient/arc2-r6-pe.service
```

So the 9G cap in round 6 belongs to `arc2-r6-pe` — the **91.6MB big leg** — not to the
17.7MB mid leg. The round-10 dispatch brief's phrase "the r6 mid-rung recipe (no
disables; 3600s; 9G cap)" merges two legs' recipes.

### 2d. `arc2-r10-big` — SEALED, envelope byte-identical to r7

```text
$ systemctl --user show arc2-r10-big -p Environment -p MemoryMax -p MemorySwapMax
MemoryMax=9663676416
MemorySwapMax=1073741824
Environment="REA_GHIDRA_DISABLED_ANALYZERS=Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis"
            REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G
            TMPDIR=/var/tmp/arc2-l10r10-big GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
            JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

That is the r7 recipe (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:9-13`: disable
list, 7200s, 6G heap, 9G/1G caps) modulo `TMPDIR`. The live Ghidra session honored it —
the pre-script ran with exactly those three names, then analysis started:

```text
/var/tmp/arc2-l10r10-big/rea-ghidra-JpFr4i/ghidra.log:276  REPORT: Execute script: .../ReaGhidraAnalysisOptions.java 'Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis'
/var/tmp/arc2-l10r10-big/rea-ghidra-JpFr4i/ghidra.log:278  ANALYZING all memory and code: file:///var/tmp/arc2-l10r10-big/rea-ghidra-JpFr4i/target-7a2ccd688f6c.exe
```

(`:276`/`:278` are the same line numbers r7's E3 cited for its own log — same recipe,
same wire.) Target is the 91.6MB artifact (`target-7a2ccd688f6c`, matching
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:11`'s `7a2ccd688f6c…`), live JVM
`-Xmx6G`. Progress at `2026-10-18T20:59:49-03`: `MemoryCurrent=6793424896`,
`MemoryPeak=6793424896`, ~3.4 min elapsed, one Ghidra JVM (pid 622629) — on the r7
trajectory, with no `decompile` worker processes at the samples (the mitigated
zero-worker profile).

**Terminal record (sealed).**

```text
$ journalctl --user -u arc2-r10-big --no-pager -o short-iso | tail -2
2026-10-18T20:56:25-03:00 ... Started [systemd-run] ... npx -y rea-agents@6.5.0 analyze .../windows_release_arm64.exe.
2026-10-18T21:20:23-03:00 ... arc2-r10-big.service: Consumed 42min 43.809s CPU time over 23min 58.082s wall clock time, 7.8G memory peak, 769.1M memory swap peak.

$ systemctl --user show arc2-r10-big -p ActiveState,SubState,Result
ActiveState=inactive
SubState=dead
Result=success
```

**The id re-derivation — byte-identity, not field agreement.**

```text
$ sha256sum /var/tmp/arc2-l10r10-big/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  /var/tmp/arc2-l10r10-big/stdout.json   (5204 bytes, mtime 2026-10-18 21:20:23.388 -0300)

$ sha256sum .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json   (5204 bytes)

$ cmp /var/tmp/arc2-l10r10-big/stdout.json .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json
BYTE-IDENTICAL
```

The sha256 `a77ebee8…` is exactly the "cheap integrity check" r7's own entry nominated
(`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7`), so the check resolves against the
live rerun. The envelope is YAML, not JSON (`json.load` fails at line 1 column 1 — a
trap for anyone parsing it as JSON); the identity is established by `cmp`, which is
stronger than comparing fields. Grepped from the live file:

```text
$ grep -oE 'ev_[0-9a-f]{16,}' /var/tmp/arc2-l10r10-big/stdout.json | sort -u
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
```

with the same census inside it: `segments[9]` (line 71), `procedure_count: 75218`
(line 82), `string_count: 137345` (line 83), `analyzer_preset:
"ghidra-default+disabled:Call Convention ID,Decompiler Parameter ID,Decompiler Switch
Analysis"` (line 58) — the r7 numbers (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:15`).

**The resource profile differed while the output did not.** Same recipe, same target,
same envelope — but a different wall, CPU and swap footprint:

| | r7 `arc2-r7-pe` | r10 `arc2-r10-big` |
|---|---|---|
| envelope sha256 / bytes | `a77ebee8…` / 5204 | `a77ebee8…` / 5204 (identical) |
| `evidence_id` | `ev_a4aa9b0d…` | `ev_a4aa9b0d…` (identical) |
| wall | 23min 44.663s (1424.663s) | 23min 58.082s (1438.082s) |
| CPU | 42min 35.706s | 42min 43.809s |
| memory peak | 7.9G | 7.8G |
| swap peak | 53.1M | 769.1M |
| procedures / strings / segments | 75218 / 137345 / 9 | 75218 / 137345 / 9 |

r7's row is `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13,15` and
`.ufo/waves/arc2-loop1-round7/E2.md:53`. The envelope is deterministic; the runtime
footprint is not. That is the observation that makes the id a property of
content+params rather than of the run's resource history — and it is why the sealed
envelope, not the wall clock, is the claim source.

### 2e. Repo state at the moment of this report

```text
$ git rev-parse HEAD
c561f00d9000f5da13719673c6f2c2f79a572d0a
$ git status --porcelain=v1 --untracked-files=all
?? .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt
?? .ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt
$ git diff --stat ; git diff --cached --stat
(no output)
```

No tracked or staged edit exists. HEAD is the r9 records commit. At this seat's first
census `.ufo/waves/arc2-loop1-round10/` held only `receipts/`; by close, peer seat
reports had landed alongside this file (`C3 E3 E4 E5 E6 E9 E15 E21 E23 E26 P2 R4 SC2 V5`
and rising) — all untracked, so the "no tracked/staged edit" result is unchanged. The
frozen roster
(`receipts/roster-frozen.txt`) states 64 seats, pre-dispatch, with the
`len(items) == roster seats` assertion — the r9 C3 wire-it amendment landing as
promised (`SCORECARD.md:1243-1245`). This seat counts its roster line as 64/64
satisfied by construction; it did not observe the dispatch command itself.

One stray untracked artifact appeared in the tree during the window:
`.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` (23796 B, mtime 20:59). It is
**not** from this seat: a direct `python3 .ufo/gates/c1-census-v10.py` run does not
emit a `__pycache__` (verified in `/var/tmp/arc2-l10r10-SC1-pycache-test/` — the copy
ran clean and produced no `__pycache__`), so it came from a peer importing the
instrument. Flagged for the parent; this seat did not remove it (its only write is
this file).

### 2f. Cross-seat corroboration of the mid-leg finding

Peer seat `E5` reached the same conclusion independently, from its own observation:
`.ufo/waves/arc2-loop1-round10/E5.md:24-32` — "**The mid leg cannot take either
branch — it produced no id.** `arc2-r10-mid` was kernel-OOM-killed at its own 9G cap
53.178 s in, envelope typed `cancelled`, zero evidence ids … the r6 mid leg ran with
**no memory cap** (bare `timeout(1)` wrapper … = 18.26 GiB — twice the 9G cap this wave
added. So 'the r6 mid-rung recipe' …". Two seats, two independent reads of the same
systemd/receipt record, same conclusion. The only discrepancy is the wall figure:
E5 records `53.178 s`, this seat read systemd's `over 53.602s wall clock time`
(`journalctl --user -u arc2-r10-mid`). Both are sub-minute; the difference is a
measurement-origin difference, not a disagreement, and the parent should quote one
origin explicitly rather than blending them.

Round-9's landed freshness text is confirmed present in the current surface:
`corpus/README.md:22` now reads "wall-fell — r7: … HELD with three validated
analyzers disabled; r8: … OOM-killed at 9G", and `:175` reads ">90MB PE scale —
CLOSED, not frontier". `:117` still carries the dated r4 synopsis, correctly
historical. That matches r9's claimed 2→0 (`SCORECARD.md:1236`).

## 3. Verbatim-landable text

Draft for the round's records — a named-debt line plus the scout correction. Nothing
below was landed by this seat.

```text
- C1 calibration (owned) — rerun id-stability. The 91.6MB leg (`arc2-r10-big`) SEALED
  with the r7 recipe byte-for-byte (env + the three validated disabled analyzer names +
  9G/1G caps + 7200s): `Result=success` at 2026-10-18T21:20:23-03, 23min 58.082s wall,
  7.8G peak, 769.1M swap. Its envelope is BYTE-IDENTICAL to r7's committed envelope —
  sha256 `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`, 5204 B,
  `cmp` clean, `evidence_id ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608`
  re-derived exactly (9 segments / 75218 procedures / 137345 strings, same preset).
  The r7 entry's last named unknown therefore CLOSES: analyze ids are content+params-keyed
  and stable across a rerun at the 91.6MB scale point. Note the envelope is deterministic
  while the runtime footprint is not (r7 1424.663s / 7.9G / 53.1M swap vs r10 1438.082s /
  7.8G / 769.1M) — the sealed envelope, not the wall clock, is the claim source.
  The 17.7MB leg (`arc2-r10-mid`) did NOT seal: kernel-OOM-killed at its own 9G cap
  in 53.602s (MemoryPeak byte-equal MemoryMax; 4m14.2s CPU), envelope typed
  `cancelled` with no evidence_id — the r4 mislabel class reproduced at a second
  target and second scale. `ev_8b688ce7…` therefore did not re-derive; the r6 mid-rung
  unknown stays OPEN. Named debt, and one correction: the dispatched brief described the
  mid leg as "the r6 mid-rung recipe (… 9G cap)", but the r6 mid leg ran with NO cgroup
  memory cap (bare shell + `timeout -k 60 5400`; E9.md:27-38) — the 9G `MemoryMax` of
  round 6 belonged to `arc2-r6-pe.service`, the big leg (C6.md:21-34). A rerun under the
  same 9G-capped unit is expected to die again; a faithful r6 id-stability test needs the
  cap removed (r6's own uncapped tree peaked 18.263 GiB summed RSS, meta.txt
  `peak_tree_rss_kb=19149984`).
```

If the round prefers a one-line form for a table cell:

```text
| calibration — C1 | 91.6MB leg sealed with the r7 recipe and re-derived `ev_a4aa9b0d…` byte-identically (r7 rerun id-stability unknown CLOSES; envelope sha256 `a77ebee8…` on both); 17.7MB leg OOM-killed at its own 9G cap in 53.6s (envelope `cancelled`, no evidence_id) so r6 id-stability stays OPEN, and the dispatched "r6 recipe" 9G cap is a provenance error (r6's mid leg ran uncapped) | calibration improved + named debt |
```

## 4. Observation / inference / unknown

- **Observation.** The five pre-pair hashes recompute exactly and equal r9's post-pair:
  no config churn. Command A gives 81/81, 13/13, 10.0/10.0 at `c561f00`; census v10
  PASSes with the three pins re-derived and grep-confirmed; the citation-drift probe
  selftest is 11/11. `arc2-r10-mid` is `failed`/`oom-kill`, 9G peak byte-equal the cap,
  53.602s; its 315462 B envelope is a `cancelled` wrapper with no `evidence_id`, and its
  `target_sha256` is the r6 mid-rung artifact. `arc2-r10-big` finished `inactive/dead`
  with `Result=success` at 21:20:23-03 after 23min 58.082s (7.8G peak, 769.1M swap), and
  its 5204 B stdout is byte-identical to r7's committed envelope — same sha256
  `a77ebee8…`, same `evidence_id ev_a4aa9b0d…`, same 9/75218/137345 census, same preset.
  HEAD is `c561f00`; no tracked/staged edits; the wave dir holds only untracked seat
  reports and the two pre-dispatch receipts.
- **Inference.** (i) **The r7 rerun id-stability unknown closes**: an identical request
  (same target, same params, same recipe) produced a byte-identical envelope, so analyze
  ids are content+params-keyed and stable at the 91.6MB scale point. (ii) Because the
  envelope is byte-stable while wall/CPU/swap are not, the id carries no resource
  history — it is a property of content+params, which is the mechanism the round was
  testing. (iii) The r6 mid-rung "natural hold" is not reproducible under a 9G cap; the
  mid rung's undisabled profile is cap-bound at 9G, which *extends* the r8
  natural-control lesson from the 91.6MB leg to the 17.7MB leg. (iv) Because the mid
  leg's envelope is byte-shaped like r8-ctl's, the `cancelled` wrapper is a stable
  wrapper for a memcg kill across at least two targets — a usable, cheap diagnostic
  rule. (v) The round-10 dispatch brief's mid-leg cap is a transcription from the wrong
  leg, so the mid leg's failure is a recipe defect, not a target wall — it should not be
  counted as evidence about the 17.7MB artifact. (vi) The pair's net result is a clean
  split: r7's unknown closes, r6's stays open for a reason that is now named and
  actionable.
- **Unknown / limitation.** (1) The mid leg's failure *cause* is inferred from the
  systemd resource record plus the r6 receipt's invocation; this seat ran no controlled
  experiment and cannot separate "9G cap binding" from possible host-level memory
  pressure (the host was at 11G/30G used, with unrelated lanes active). (2) The exact
  byte-identity of the mid leg's *request parameters* versus r6's is not established —
  the mid leg used `npx -y rea-agents@6.5.0` where r6 used a direct `node rea.mjs` from
  the same npx cache; if params feed the id, that is a second, independent reason the id
  could differ. (3) The big leg's byte-identity was observed at **one** rerun; two
  identical envelopes at two scale-adjacent recipes is stability evidence, not a proof
  that no parameter combination can perturb the id. (4) This seat did not observe the
  dispatch command, so the 64/64 roster assertion is taken from
  `receipts/roster-frozen.txt`, not independently measured. (5) The untracked pre-pair
  receipt's capture provenance is not independently authenticated; this seat verified
  only that the five declared values match the five live files. (6) The mid-leg finding
  is corroborated by peer seat `E5` (`E5.md:24-32`) but both seats read the same two
  records — systemd's resource line and the `cancelled` envelope — so this is two
  independent *readings*, not two independent *measurements*; no seat re-ran the mid leg,
  and this seat did not (correctly) touch it. (7) The sealed big-leg envelope lives only
  at `/var/tmp/arc2-l10r10-big/stdout.json`; until a seat copies it into a committed
  receipt, the byte-identity claim rests on an ephemeral path. **This seat did not copy
  it** (its only write is this file) — the parent should land it under
  `.ufo/waves/arc2-loop1-round10/receipts/` before `/var/tmp` is reclaimed.
