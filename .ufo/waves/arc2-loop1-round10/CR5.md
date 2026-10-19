# CR5 — round-10 critic: census completeness (which claims might the wave miss?)

Seat: CR5 (critic), arc2-loop1-round10. Read-only over the repo; only this file written.
Scratch: `/var/tmp/arc2-l10r10-CR5-selftest`. Custody pre-pair re-verified 5/5 (see G10).

## (1) Verdict

**Do not land C1 as a two-scale-point id-stability result: only ONE of the two
legs can answer the question, and the second leg's failure is a cap artifact
that will be mis-attributed if it is recorded as an id-instability finding.**

The big leg resolved (ids equal, envelope byte-identical). The mid leg produced
**no evidence id at all** — it was OOM-killed at the unit's 9 GiB memcg limit in
53.6 s. C1's own branch structure has no slot for "leg killed before sealing",
so a naive census will either (a) claim "both legs sealed" (false), or (b)
report the mid failure as evidence about id stability (a false attribution:
r6 ran **uncapped**, receipted peak tree RSS 18.26 GiB, so the r6 hold cannot
reproduce under a 9 GiB cap by construction).

Ten gaps below; G1–G5 are substantive, G6–G10 are census-surface.

## (2) Evidence — commands, output excerpts, resolving pointers

### G1 — the mid leg sealed nothing (C1's "two scale points" is false)

```
$ systemctl --user status arc2-r10-mid --no-pager
   Active: failed (Result: oom-kill) since Sun 2026-10-18 20:57:18 -03; 50s ago
   Duration: 53.178s
   Mem peak: 9G (swap: 1G)
$ head -c 200 /var/tmp/arc2-l10r10-mid/stdout.json
error: Analysis failed
code: cancelled
category: cancelled
message: Analysis was cancelled. Start it again when ready.
...
    failure_kind: cancelled
    failure_message: Ghidra startup was cancelled
```

No `evidence_id` anywhere in the 315,462-byte mid output; the file is not JSON
(see G9). So `ev_8b688ce7…` re-derivation is **unanswered**, and the r6 entry's
last named unknown stays open (`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:7,21`).

### G2 — the mid leg is NOT the r6 recipe: cap mismatch (the crux)

r6 ran with **no cgroup cap** — `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:7`
is a bare `node …rea.mjs analyze …` invocation; the seat command
`.ufo/waves/arc2-loop1-round6/E9.md:77` wraps it in `/usr/bin/timeout -k 60 5400`
and nothing else. Its receipted peak:

```
$ cat .ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt
exit_code=0
peak_tree_rss_kb=19149984      # 18.263 GiB
peak_java_rss_kb=2884192
wall_s=2479
```
`.ufo/waves/arc2-loop1-round6/E9.md:66` — "Peak tree 19,149,984 kB (18.263 GiB)
was the decompiler swarm (10 `decompile` children observed, one ~4.1 GB RSS)".

The r10 mid leg ran under a cap:

```
$ systemctl --user show arc2-r10-mid -p Environment -p MemoryMax -p MemorySwapMax -p Result
MemoryMax=9663676416          # 9 GiB
MemorySwapMax=1073741824      # 1 GiB
Environment=REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G
  TMPDIR=/var/tmp/arc2-l10r10-mid GHIDRA_INSTALL_DIR=… JAVA_HOME=…
Result=oom-kill
```

`REA_GHIDRA_DISABLED_ANALYZERS` is absent (correct: this is the natural leg).
r6 needed 18.26 GiB; the r10 cap is 9 GiB. **The re-derivation is structurally
impossible under the r10 envelope, and the OOM is a cap artifact — not evidence
about id stability, and not evidence that the 17.7 MB rung "walls".** The
recorded mechanism matches r8's, not a new one:

```
$ journalctl -k --since "20:57:10" --until "20:57:30" --no-pager
decompile invoked oom-killer: gfp_mask=0x100cca(GFP_HIGHUSER_MOVABLE), order=0, oom_score_adj=200
 oom_kill_process.cold+0x8/0x91
 mem_cgroup_out_of_memory+0xe1/0xf0
memory: usage 9437184kB, limit 9437184kB, failcnt 206682
Memory cgroup stats for /user.slice/…/arc2-r10-mid.service:
 anon 9567342592
 file 1318912
oom-kill:constraint=CONSTRAINT_MEMCG,…,task=java,pid=622553,uid=1000
```
Task list at the kill: 10 `decompile` children (643360/643448/643454/643566/
643621/643708/643801/643849/643901/644073) + `npm exec rea-ag` + node + java —
the r8 profile ("10-12 decompile workers", `…arc2-r7-pe-wall.md:31-33`), now at
**17.7 MB instead of 91.6 MB**. The OOM was anon-driven (`anon 9.57 GB`,
`file 1.3 MB`) — not page cache, so a TMPDIR/cache explanation is refuted.

### G3 — concurrency is RULED OUT as the trigger (do not chase it)

Both legs launched the same second (20:56:25) and the big leg was at 6.9 G when
the mid leg died. The kernel line above settles it: `constraint=CONSTRAINT_MEMCG`
with `oom_memcg=…/arc2-r10-mid.service` — the mid unit's **own** 9 GiB limit, not
host pressure. Record this explicitly so the failure is not attributed to the
double launch.

### G4 — the wave's strongest available result is byte-identity, not "ids equal"

```
$ journalctl --user -u arc2-r10-big --no-pager | tail -1
Oct 18 21:20:23 … arc2-r10-big.service: Consumed 42min 43.809s CPU time over
  23min 58.082s wall clock time, 7.8G memory peak, 769.1M memory swap peak.
$ grep -o -E "ev_[0-9a-f]{64}" /var/tmp/arc2-l10r10-big/stdout.json | head -1
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
$ cmp /var/tmp/arc2-l10r10-big/stdout.json \
      .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json \
  && echo BYTE-IDENTICAL
BYTE-IDENTICAL
$ sha256sum /var/tmp/arc2-l10r10-big/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  (5204 B)
```

The r10 rerun is **byte-for-byte the committed r7 receipt** (same 5204 B, same
`a77ebee8…`) despite a different wall (1438.082 s vs 1424.663 s) and peak
(7.8 G vs 7.9 G). Two consequences a census that reports only "ids equal" would
miss: (a) the id is time- and memory-invariant, not merely stable; (b) the r7
entry's `recheck:` cheap check now *reproduces* — yet that line still reads
"A second run was not made; id stability across a rerun is UNKNOWN"
(`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7`), and `:19` still lists
"rerun id-stability" among the honest unknowns. An append-only erratum is owed
(draft in §3).

### G5 — the mid OOM is a second natural control, and the wave's question misses it

r8's control was 91.6 MB at 9 G. The r10 mid leg is 17.7 MB at 9 G, no disables
→ OOM in 53.6 s with the same 10-worker profile. That is a knowledge-worthy
data point (the analyzer-disable's necessity is not size-specific across at
least 17.7 MB → 91.6 MB under a 9 GiB cap) that C1's question — "does the id
re-derive?" — cannot see. It is a *new* observation, not a re-derivation of r6.

### G6 — cap/heap/deadline evidence is unreceipted for r7/r8 and evaporates for r10

r7's receipt dir holds only `config-pre-pair.txt`, `config-post-pair.txt`,
`MANIFEST.txt`, `r7-pe-envelope.json` — **no unit dump**. The "9G memory cap +
1G swap cap" (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13`) and r8's
"identical cap/deadline/heap" (`…:29-33`) are prose; the transient units are
gone and the envelope records no cap/heap/deadline field (full 90-line envelope
read: only subject/provider/analysis_profile/parameters/normalized_result).

The r10 units' evidence was retrievable while running and is now **gone**:

```
$ systemctl --user show arc2-r10-big -p Environment -p MemoryMax -p MemorySwapMax
MemoryMax=infinity
MemorySwapMax=infinity
Environment=
$ systemctl --user status arc2-r10-big --no-pager | head -1
Unit arc2-r10-big.service could not be found.
```
(At 20:59 the same command returned `MemoryMax=9663676416` and the full
`Environment=` block.) **The wave must receipt `systemctl --user show` for both
legs while alive** — otherwise G2's cap comparison is unreproducible, which is
exactly the hole that made this seat dig into r6's seat report.

### G7 — command A cannot see any wave claim

command A (`SCORECARD.md:92-123`) is `git show <rev>:<path>` over
`corpus/knowledge` + the SKILL "Queue-drain craft" section only; it emits
`{mapped, knowledge_files, missing, dangling, citation_resolved_rules,
rule_blocks, coverage_score, depth_score}`. It cannot count: wave artifacts,
knowledge-entry scope bounds, README wall text, SHONEN, or any leg outcome. So
"81/81, 13/13, 10.0/10.0" is silent on C1's closure claim — a disclosed textual
census is required, not a command-A PASS.

### G8 — the roster freezes the count but not the scope/paths; the "64" is self-asserted

```
$ cat -n .ufo/waves/arc2-loop1-round10/receipts/roster-frozen.txt
2  # 64 seats == len(dispatch items). E25-E28 return (the IDs rounds 2-4 never dispatched).
3  P1-P4 planners | C1-C4 connectors | E1-E28 executors | S1-S2 scribes | SC1-S2 scouts | R1-R8 reviewers | CR1-CR8 critics | V1-V6 verifiers | Z1-Z2 convergence
4  # assertion enforced at dispatch: len(items) == 64 == roster seats.
```
Rule #2 requires "One row per logical seat with its scope and expected report
path" (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:25-26`); `:3` is one
line of ID ranges with neither scope nor report path. And the `len(items)==64`
assertion lives in the same file that asserts it (`:2,:4`) — self-referential.
Prior item counts varied per wave: r6 **128** (`LOG.md:1222`), r7 **24**
(`:1253`), r8 **20** (`:1295`), r9 **24** (`:1331`). The count must come from
the dispatch items array, not from the roster's own claim.

### G9 — the envelopes are YAML, not JSON

`file` reports both `r7-pe-envelope.json` and the legs' `stdout.json` as
"assembler source, ASCII text" (the REA envelope's YAML rendering);
`json.load` fails on all three. A census that parses these as JSON silently
reads nothing. Also: a *successful* r10-big leaves no Result line in the
journal (only the "Consumed …" line) — success is visible only via
`systemctl show -p Result`.

### G10 (custody, in scope for the 5/5 check)

Pre-pair re-verified 5/5 by sha256 against
`.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt:2-6`:
`16f496e6…` devin/mcp_config.json, `38d2a1d0…` omp/mcp.json, `6ba8a0f9…`
kimi config.toml, `7d2ca28a…` .bashrc, `6c6be761…` .profile — all match.
Point-in-time only; no post-pair exists at this cut. (Note: r8 recorded in-window
config.toml drift, `.ufo/waves/arc2-loop1-round8/receipts/drift-config-toml-round8.txt`;
r10 has no drift receipt yet.)

### C3 census gap — the devin baseline is a *defective count*

Rounds 2–5 recorded "64 dispatched, 60 delivered, 4 non-completions"; the r5
audit proved **each dispatched exactly 60 and completed 60**
(`corpus/lessons/2026-10-18-wave-dispatch-counting.md:3-16`). A naive
devin-vs-hyper delivery comparison therefore pits a defective count (60/64)
against a corrected one. C3 must use the audit-corrected baseline (60/60) and
record the pre-dispatch roster freeze (landed r9/r10) as a **co-variate** —
otherwise the provider is credited with the counting repair. Lane record:
devin rounds are 1–5 (`LOG.md:1074,1120`); r6 xai-oauth/grok-4.7-fast (`:1222`),
r7/r8 zai/glm-5.3-flash (`:1253,1295`), r9 openai-codex/gpt-6-luna-max (`:1331`),
r10 hyper/deepseek-v4.1-flash. The comparison is non-adjacent (three other
providers in between) though the deepseek family is held.

### C2 census note (baseline verified, extension unlanded)

```
$ TMPDIR=/var/tmp/arc2-l10r10-CR5-selftest python3 \
    .ufo/gates/citation-drift/citation-drift-probe.py --selftest
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0
$ TMPDIR=/var/tmp/arc2-l10r10-CR5-selftest python3 \
    .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
$ grep -c "arc2-r7-pe-wall" .ufo/gates/citation-drift/pointer-table.json
0
```
Selftest and HEAD run both clean (11/11, 0 findings). The pointer table still
holds 13 entries / 4 quoted / 3 exempt with **zero** r7/r8 references, so C2's
extension is unlanded at this cut. When it lands, `expected.json`'s
`frozen_run.revision` pin (`679af5d7…`) describes a different measurement and
must be re-pinned or explicitly scoped.

## (3) Verbatim-landable text

**(a) C1 census clause — replace any "both legs sealed / two scale points" wording:**

```text
C1 id-stability, arc2-loop1-round10 (measured, 1/2 legs):
- BIG leg (91.6MB Godot ARM64, r7 recipe verbatim): SEALED. `ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608`
  re-derived, and the 5204-byte envelope is byte-identical to the committed r7
  receipt (sha256 `a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a`;
  `cmp` clean) at wall 1438.082s / 7.8G peak vs r7's 1424.663s / 7.9G peak —
  so the id is time- and memory-invariant, not merely equal. r7's "rerun
  id-stability" unknown closes.
- MID leg (17.7MB agent-browser, no disables): NOT SEALED — no id produced.
  Unit `Result=oom-kill`, memcg OOM at the unit's own 9 GiB limit in 53.178s
  (`anon 9567342592`, `failcnt 206682`, 10 `decompile` children; envelope typed
  `cancelled`, `failure_message: Ghidra startup was cancelled`). The leg is NOT
  a rerun of r6: r6 ran UNCAPPED with a receipted peak tree RSS of 19,149,984 kB
  (18.263 GiB), so re-derivation is impossible under a 9 GiB cap. `ev_8b688ce7…`
  re-derivation is a NAMED DEBT (an uncapped rerun needs >18 GiB, above this
  round's envelope budget), NOT an id-instability finding.
- Third branch, to be carried forward: a leg killed before sealing yields NO id
  — neither "equal" nor "different". C1's branch structure needs this slot.
```

**(b) Required receipt (add to the wave's receipts before the units are unloaded):**

```text
systemctl --user show <unit> -p Environment -p MemoryMax -p MemorySwapMax \
  -p RuntimeMaxUSec -p Result  >  receipts/<unit>-unit.txt
# + one decompile-worker sample (ps -ef | grep -c '[d]ecompile') and the live
# java argv. Reason: transient units are garbage-collected at exit — at 21:58
# `systemctl --user show arc2-r10-big -p MemoryMax` returned `infinity` and
# `Environment=` empty, and the unit file was gone. r7/r8 have no unit dump
# either, so their caps are prose-only (`…arc2-r7-pe-wall.md:13,29-33`).
```

**(c) Append-only erratum for the r7 entry (do not edit `:7`/`:19` in place):**

```markdown
## Erratum (arc2-loop1-round10 rerun, 2026-10-18, append-only)

- The named unknown "rerun id-stability" (`:19`) resolves: user service
  `arc2-r10-big` re-ran the same target under the same recipe (9 GiB cap +
  1 GiB swap, `GHIDRA_HEADLESS_MAXMEM=6G`, 7200s deadline, the three
  `REA_GHIDRA_DISABLED_ANALYZERS` names, zero decompile workers at the watch
  sample) and re-derived `ev_a4aa9b0d…` with a **byte-identical** 5204-byte
  envelope (sha256 `a77ebee8…`, `cmp` clean) at wall 1438.082s / 7.8G peak.
  The `:7` recheck line's cheap integrity check is thereby reproduced. The id
  is time- and memory-invariant. (arc2-loop1-round10)
```

**(d) C3 baseline clause:**

```text
C3 baseline: use the r5-audit-CORRECTED devin figures (rounds 2–5 each
dispatched exactly 60 items and completed 60/60; the recorded "60/64" was a
parent counting defect, `corpus/lessons/2026-10-18-wave-dispatch-counting.md:3-16`).
Record the pre-dispatch roster freeze (landed r9/r10) as a co-variate; otherwise
the hyper-lane delivery comparison credits the provider with the counting repair.
```

## (4) Observation / inference / unknown

- **Observation** — mid leg `Result=oom-kill` at its own 9 GiB memcg limit,
  53.178s, 10 `decompile` children, anon-driven, `CONSTRAINT_MEMCG`; no
  evidence_id, envelope typed `cancelled`. Big leg sealed, id re-derived, envelope
  byte-identical to the committed r7 receipt at a different wall/peak. r6's
  receipted peak tree RSS is 19,149,984 kB with no cap in its command. Custody
  pre-pair 5/5. Citation-drift selftest 11/11, HEAD run 0 findings, table has no
  r7/r8 rows. r10-big's unit env/caps are no longer retrievable.
- **Inference** — the mid leg's failure is caused by the 9 GiB cap, not by id
  nondeterminism and not by concurrency; the r6 hold is cap-conditional and the
  r6 entry never names a cap, so its `recheck:` line is not reproducible as
  written. The r7/r8 caps are unreceipted, so their "identical cap" comparison
  rests on prose. The devin baseline for C3 is a defective count unless the r5
  audit correction is applied.
- **Unknown** — whether the wave's dispatch items array actually holds 64 (the
  roster asserts it; prior waves were 128/24/20/24); whether the r10 mid leg's
  heap was in fact 6G (its `GHIDRA_HEADLESS_MAXMEM=6G` is visible in the unit
  env, but the dead JVM's argv was not captured — the unit is gone); whether an
  uncapped mid rerun is within the round's budget (>18 GiB needed); whether the
  mid OOM's 10 workers all belong to the same analysis phase as r6's 10; and
  whether C2/C3's edits land before the wave closes.
- **Scope** — textual + read-only probes only; no service signalled, no repo
  file modified, no network; only this report written.
