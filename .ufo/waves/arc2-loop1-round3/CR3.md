# CR3 (critic) — C2 claim-structure attack: what accrues vs the r4-12 record, and is this a re-run dressed as a move?

Seat CR3, wave arc2-loop1-round3, read-only on the repo and home. Every command
below was run by this seat this session (2026-10-18; stamps I recorded lie in
[18:04:46Z, 18:30:02Z]; the receipt read and command A ran earlier in the same
session). HEAD at every command: `679af5d749f2fd48b9d543e3c99d348d5458f90f`;
`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only. This report
is my only write. I ran no REA probe and no battery leg (no session of mine to
close); I sampled the live leg's `/proc` and scratch **read-only** (that leg is
seat E11's). Scratch `/tmp/arc2-l3r3-CR3` was created for one local `timeout`
mechanics test and deleted; zero residue (`ls -d /tmp/arc2-l3r3-CR3` → absent).

## 1. Verdict

**PARTIAL REFUTE of the claim as a *move*, full confirmation of the leg as a
*genuine new execution*. The 91.6 MB leg did not hold and did not produce REA's
typed timeout — it died at its own 30-min outer cap (exit 124) with a typed
`cancelled` envelope and no evidence id, an outcome class the claim text did
not pre-register. Against the r4-12 record the leg accrues four new
observations (a lower bound on the wall, a resource-envelope datum, a
clean-cancellation datum, and a decisive cap-chain arithmetic point) but **no
capability, no counts, no falsification, and no coverage movement**. It is not
"a re-run dressed as a move" — it is the record's own prescribed next step,
executed honestly — but the claim's stated measurable (`command A 79→80`) is
bookkeeping that even the HELD branch could not have turned into axis movement
(the proxy is saturated by construction, `E20.md:83-85`), and on the actual
outcome nothing moves at all.**

Four load-bearing findings:

1. **The executed outcome is the third branch, not the pre-accepted second.**
   The claim pre-accepted "honest typed refusal/timeout → recorded negative".
   What happened is neither: `timeout -k 30 1800` fired at 30m01.2s, and REA
   translated the SIGTERM into `{"code":"cancelled", …}` — a cancellation, not
   a refusal and not `provider_timeout`. The round's own plan predicted this
   class and typed it **INCONCLUSIVE, "the deadline was NOT tested"**
   (`P2.md:367-374`; `C4.md:231-263`). Landing it as the claim's "recorded
   negative" would overstate it: the 3600 s deadline never got a chance to
   fire. **Refinement to the round's prediction:** both P2 and C4 expected an
   *untyped* kill with empty/partial stdout; the observed envelope is **typed**
   (`code/category: cancelled`, `cleanup: complete`, 87,639 B valid JSON).
   That does not change the taxonomy verdict — `cancelled` is not
   `provider_timeout` and carries no `evidence_id`/`timeout_ms` — but the
   round record should not say "no envelope" or "untyped": REA's SIGTERM path
   is graceful and self-documenting.
2. **Even a HELD outcome could not have moved the coverage *axis*.** Command A
   at HEAD returns `knowledge_files 79, mapped 79, coverage_score 10.0` (run
   this session). The claim's measurable is a denominator change; the score is
   `10*79/79 = 10*80/80 = 10.0` either way, and `SCORECARD.md:23` defines
   coverage as "index integrity only, **not** fraction of the REA domain
   held". So "79→80" is an expansion side-effect, exactly as luna-round-8
   recorded its own entry (`SCORECARD.md:550`: "unchanged (the entry is the
   round's expansion side-effect, recorded)").
3. **The retry moved three variables at once (deadline, heap, REA version), so
   no outcome could be attributed to the deadline knob alone.** r4-12 ran
   `rea-agents@6.4.0` (`r4-12:6`) with default `-Xmx2G` (`:74-78`); the retry
   ran 6.7.0 (E11 leg) with `-Xmx8G`. The heap change is not neutral: the live
   JVM's `VmHWM` reached **8,754,888 kB (8.35 GiB)** — 3.7× r4-12's 2.36 GB
   peak, and *above its own 8 GiB heap cap in RSS* (off-heap). The version
   delta is named by no round-3 seat as an attribution threat for this leg
   (grep for a 6.4.0↔6.7.0 pairing in that sense returns nothing).
4. **The cap chain was inconsistent by r4-12's own arithmetic.** Executed cap
   1800 s < declared deadline 3600 s < r4-12's own estimate "plausibly needs
   30–90 min" (`r4-12:148-150`, i.e. up to 5400 s). A 30-minute cap cannot
   falsify a 30–90-minute estimate. P2's "decisive" recipe uses a 4200 s cap
   (`P2.md:354-365`) — still below the estimate's upper bound; a decisive
   re-run needs > 5400 s. No round-3 seat cites the 30–90 min estimate against
   the cap (grep for `30–90|30-90|plausibly needs` in `.ufo/waves/arc2-loop1-round3/*.md` → empty).

## 2. Evidence — commands run this session, with observed output

### 2.1 Pre-pair receipt and target identity

```
$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -    (at 18:17:54Z)
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553   (6 lines)
$ sha256sum /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
$ stat -c '%s %n mtime=%y' <target>
91662336 … mtime=2026-10-11 16:17:46.129033608 -0300
$ file <target>  → PE32+ executable for MS Windows 6.00 (GUI), ARM64, 8 sections
```

Observation: 5/5 OK rc=0; the target is byte-identical to r4-12's recorded
carrier (`r4-12:16-19`). The retry is on the same bytes — that part of the
claim is exact.

### 2.2 Command A at HEAD (the claim's own measurable, before-state)

```
$ python3 - "HEAD" <<'PY' …  (SCORECARD.md:88-124 recipe, body verbatim) … PY
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [],
 "revision": "HEAD", "rule_blocks": 10}
```

Observation: 79/79, 10/10, 10.0/10.0 — matches the round's declared baseline
(`E20.md:75-85`). A new file **plus** a map token is required for 80/80; a
file without a token *lowers* coverage (9.88, `P2.md:250-271`).

### 2.3 The live leg — configuration, first-hand

```
$ ps -eo pid,ppid,etimes,rss,args   (18:04:46Z)
2514443 2514440  timeout -k 30 1800 npx -y rea-agents@6.7.0 analyze <91.6MB PE> --format json
2514444 2514443  npm exec rea-agents@6.7.0 analyze <PE>
2514465 2514444  node …/.bin/rea analyze <PE>
2514831 2514465  java … -Xmx8G … AnalyzeHeadless … -import target-7a2ccd688f6c.exe -readOnly -deleteProject
$ tr '\0' '\n' < /proc/2514831/environ | grep -E '^(REA_|GHIDRA_|TMPDIR|JAVA_HOME)'
REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000
GHIDRA_HEADLESS_MAXMEM=8G
REA_PACKAGE_VERSION=6.7.0
TMPDIR=/tmp/arc2-l3r3-E11/tmp/rea-ghidra-QzJOuD/tmp
$ grep -n 'GHIDRA\|STARTUP_TIMEOUT\|timeout -k\|TMPDIR' /tmp/arc2-l3r3-E11/run-big.sh
3:export TMPDIR=/tmp/arc2-l3r3-E11/tmp
5:export REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000
6:export GHIDRA_HEADLESS_MAXMEM=8G
11:time timeout -k 30 1800 npx -y rea-agents@6.7.0 analyze "$PE" --format json > "$S/analyze-stdout.json" 2> "$S/analyze-stderr.log"
```

Observation: the knobs the claim names are live on the process (3.6M ms
deadline, 8G heap, 6.7.0 pin), and the executed outer cap is 1800 s — half the
declared deadline. **1800 s cap < 3600 s deadline.**

### 2.4 The leg's resource trajectory and analyzer progress (my own sampling)

```
18:07:05 etimes=523s VmRSS=7345552kB VmHWM=7345552kB load=14.68
18:07:20 etimes=538s VmRSS=7418224kB VmHWM=7418224kB
18:07:35 etimes=553s VmRSS=2984508kB VmHWM=7516512kB     ← GC dip
18:07:50 etimes=568s VmRSS=1711296kB VmHWM=7516512kB
18:14:41 etimes=980s VmRSS=6819036kB VmHWM=8754888kB     ← peak, first observed
… VmHWM stayed 8754888 kB through 18:22:41Z …
$ awk '/VmHWM/{print}' /proc/2514831/status   →  VmHWM: 8754888 kB   (8.35 GiB)
```

```
$ grep -nE 'IMPORTING|ANALYZING|PngDataType|ApplyDataArchive|FidAnalyzer' /tmp/arc2-l3r3-E11/tmp/rea-ghidra-QzJOuD/ghidra.log
46:  14:58:22 INFO  (HeadlessAnalyzer) IMPORTING: file:///…/target-7a2ccd688f6c.exe
275: 14:58:26 INFO  (HeadlessAnalyzer) IMPORTING: Loaded 0 additional files
276: 14:58:27 INFO  (HeadlessAnalyzer) ANALYZING all memory and code: …/target-7a2ccd688f6c.exe
278: 14:59:02 ERROR (PngDataType) Invalid PNG data at 144c76470
372: 15:05:29 ERROR (VarnodeContext) VarnodeContext: out of address spaces at @142cc5074 …   (137 by 18:23:53Z)
471: 15:17:49 DEBUG (FidAnalyzer) No FID Libraries apply for language AARCH64:LE:64:v8A
479: 15:17:50 INFO  (ApplyDataArchiveAnalyzer) Applied data type archive: windows_vs12_64
480: 15:17:50 INFO  (ApplyDataArchiveAnalyzer) Applied data type archive: rust-common
```

Observation: the same analyzer-phase sequence r4-12 recorded (`r4-12:64-73`)
recurs on 6.7.0 with the same bytes — PngDataType at +48 s (r4-12: +48 s),
VarnodeContext from +11 min (r4-12: +8 min), ApplyDataArchive/FidAnalyzer at
+19m35s (r4-12: +12m47s). The milestone arrives at ~1.53× r4-12's wall clock
while the cap gave 2.0× the wall — i.e. the extra deadline bought less progress
than the ratio suggests, consistent with E9's contention estimate
(`E9.md:101`: "~19.4 min to reach where r4-12 was at ~12.4 min").

### 2.5 The outcome — captured by this seat at 18:29:19Z (first-hand)

```
$ tail -6 /tmp/arc2-l3r3-E11/run-big-console.log
START_UTC=2026-10-18T17:58:20Z loadavg=13.04
WALL real=30m1.228s user=60m38.787s sys=1m8.320s
END_UTC=2026-10-18T18:28:21Z
EXIT=124
STDOUT_BYTES=87639
$ sha256sum /tmp/arc2-l3r3-E11/analyze-stdout.json
41768a3f139690995051eae8ef96360437c4091c24c23d43bc14f5b0a24aea22   (87,639 B, valid JSON)
$ head -c 520 analyze-stdout.json
{"error":"Analysis failed","code":"cancelled","category":"cancelled","message":"Analysis was cancelled. Start it again when ready.","retryable":true,"remediation":{…},"details":{"operation":"read_binary_inventory_summary","cleanup":"complete","diagnostics":{"target_path":"…/windows_release_arm64.exe","target_sha256":"7a2ccd68…","transport":"uni…
$ grep -c evidence_id analyze-stdout.json   → 0
$ grep -c timeout_ms  analyze-stdout.json   → 0
$ python3 -c "…json.load…"   → details keys: operation, cleanup, diagnostics;
                               diagnostics tail: "failure_kind":"cancelled","failure_message":"Ghidra startup was cancelled"
$ ls -d /tmp/arc2-l3r3-E11/tmp/rea-ghidra-*   → no rea-ghidra dir (self-cleaned)
```

Observation: exit **124** at the outer cap; stdout is a *typed* envelope
(`code: cancelled`, `category: cancelled`, `cleanup: complete`,
`failure_message: "Ghidra startup was cancelled"`), **no `evidence_id`, no
`timeout_ms`**; the session dir self-cleaned. Note also the in-flight
`operation` label differs from r4-12's (`read_binary_inventory_summary` here
vs `list_documents` in r4-12's envelope, `r4-12:38-39`) — both labels exist in
the 6.7.0 dist (`dist/application/CapabilityInventory.js:490`,
`dist/application/AnalysisDocument.js:21`), so this is a different in-flight
operation, not a rename; recorded, not over-interpreted.

### 2.6 The knobs are real, but only one is schema-validated (read this session)

```
$ grep -rn "REA_GHIDRA_STARTUP_TIMEOUT_MS" <6.7.0>/dist/config/environment.js
:39   REA_GHIDRA_STARTUP_TIMEOUT_MS: providerStartupTimeoutSchema.default(DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS)
$ sed -n '1,20p' <6.7.0>/dist/config/providerStartupTimeout.js
:3  DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS = 330_000
:10 MAX_TIMER_DELAY_MS = 2_147_483_647
$ grep -rln "GHIDRA_HEADLESS_MAXMEM" <6.7.0>/dist/config/     → rc=1 (absent)
$ sed -n '114p' <6.7.0>/dist/ghidra/GhidraJavaLaunch.js
const configuredMaxHeap = environment.GHIDRA_HEADLESS_MAXMEM || environment.GHIDRA_MAXMEM || "2G";
$ grep -n ParallelGCThreads <6.4.0>/dist/ghidra/GhidraJavaLaunch.js <6.7.0>/dist/ghidra/GhidraJavaLaunch.js
6.4.0:54 "-XX:ParallelGCThreads=2"   6.7.0:142 "-XX:ParallelGCThreads=2"
```

Observation: `REA_GHIDRA_STARTUP_TIMEOUT_MS` is schema-wired with default
330 s; `GHIDRA_HEADLESS_MAXMEM` bypasses the schema and reaches the JVM from
the raw environment. Both the 2-thread GC and CICompiler caps are injected by
REA on every pin — a self-imposed serialization that is part of the wall's
context, unchanged between r4-12 and the retry.

### 2.7 The bounded mid-size leg (E10) — what it does and does not add

```
$ cat /tmp/arc2-l3r3-E10/target-decompile-exe.meta.txt     (first-hand)
target_sha256=ea42e06df2a64f95188a12422a35a36cd48fd4a6f621e62b001e82f1bbbe923b
exit_code=0  wall_s=44.117  peak_java_rss_kb=1707552
env: REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000 GHIDRA_HEADLESS_MAXMEM=6G
```

Observation: the 2.5 MB PE completes in 44.1 s with `ev_92dea347…`
(`E10.md:13-24,94-113`) — a new size-vs-time datum, far from the wall, on
**6.5.0** (the E11 leg is 6.7.0, r4-12 was 6.4.0 — three pins across the
comparison set; `R5.md:413-414` flags the two battery legs as not mutually
comparable, but the pin spread against r4-12 is unnamed).

## 3. What actually accrues vs the r4-12 record — the ledger

| # | Datum | New vs r4-12? | Why |
|---|---|---|---|
| 1 | Same bytes survived 1800 s (2× the r4-12 kill point) still in auto-analysis, no OOM | **Yes — new lower bound** | r4-12 died at real 15m01.8s (`:125`); the wall is now known to be >1800 s under 8G/3.6M on this host. r4-12's "pure deadline, not capability" (`:94-95`) was an *inference*; this is a live measurement in the same direction. |
| 2 | JVM peak `VmHWM` 8,754,888 kB (8.35 GiB), above its own `-Xmx8G` in RSS | **Yes — new envelope** | r4-12's peak was ~2.36 GB under `-Xmx2G` (`:76-78`); the raised-heap run is a different resource regime, so "not OOM" no longer describes the retry. |
| 3 | SIGTERM → typed `cancelled` + `cleanup: complete` + zero residue | **Yes — operability datum** | Not in r4-12 (its kill was REA's own deadline, not an external SIGTERM). |
| 4 | Cap chain 1800 < 3600 < 5400 s | **Yes — arithmetic point** | Unnamed by any round-3 seat; fixes the size of a decisive re-run's cap. |
| 5 | Same analyzer phases recur on 6.7.0 at ~1.53× r4-12's wall | **Yes, with confound** | Confirms the analyzer chain is not version-broken, but version + contention + heap all differ. |
| 6 | Completion, counts, evidence id | **No** | Absent by construction — the session died before `list_documents`/inventory returned (r4-12's `:86-88` construction repeats). |
| 7 | Falsification of the 3600 s deadline hypothesis | **No** | The cap fired first; per `P2.md:369-374` the deadline was NOT tested. |
| 8 | Coverage movement | **No** | No entry lands on this outcome (`E8.md:275`: "NOT-VERIFIED — no new knowledge entry, no map row, command A unchanged"); and even on HELD the score stays 10.0 (`E20.md:83-85`). |

**Answer to the seat's question.** It is *not* a re-run dressed as a move: the
leg is the record's own prescribed next step (`r4-12:91-95`, `PROVINCE.md:139-144`),
executed with the declared knobs on the identical artifact — a genuine new
execution, not a repetition of r4-12's 900 s run. But the *claim structure*
carries the re-run risk in two concrete places: (a) its measurable ("command A
79→80") is a denominator change that cannot move the coverage axis in either
branch, so it cannot distinguish a move from a bookkeeping increment; (b) its
pre-accepted negative ("honest typed refusal/timeout") does not name the
outcome that actually occurred (cap-kill → `cancelled`, INCONCLUSIVE by the
round's own taxonomy). If the parent lands a knowledge entry for this leg, the
round *will* have dressed an inconclusive re-run as a move — because the entry
would move the coverage denominator (79→80) while the frontier does not move.
The honest landing is the no-entry branch.

## 4. Text for the parent to land VERBATIM

**4a — C2 disposition line for the round record / LOG:**

```text
C2 (arc2-loop1-round3): NOT-VERIFIED / INCONCLUSIVE — the 91.6 MB Godot ARM64
PE leg (seat E11, rea-agents@6.7.0, REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000,
GHIDRA_HEADLESS_MAXMEM=8G, target sha256 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
= r4-12's recorded carrier) died at its own outer cap, not at REA's deadline:
`timeout -k 30 1800` fired at wall 30m1.228s (EXIT=124, END_UTC 2026-10-18T18:28:21Z);
stdout 87,639 B (sha256 41768a3f139690995051eae8ef96360437c4091c24c23d43bc14f5b0a24aea22)
is a typed `cancelled` envelope — {"code":"cancelled","category":"cancelled",
"details":{"operation":"read_binary_inventory_summary","cleanup":"complete", …,
"failure_kind":"cancelled","failure_message":"Ghidra startup was cancelled"}} —
with NO evidence_id and NO timeout_ms; session dir self-cleaned. Per the round's
own taxonomy (P2.md:369-374) this is the third branch: the 3600000 ms deadline
was NOT tested → INCONCLUSIVE, not a falsification and not the claim's
pre-accepted "typed refusal/timeout". No knowledge entry, no map row; command A
stays 79/79, 10.0/10.0; coverage row: unchanged. New observations recorded
(append-only, freshness-class): (i) lower bound — the same bytes under the
raised knobs survived 1800 s (2× r4-12's 900 s kill) still in auto-analysis;
(ii) resource envelope — JVM VmHWM 8,754,888 kB (8.35 GiB), 3.7× r4-12's ~2.36 GB
peak and above its own -Xmx8G cap in RSS, so the retry ran in a different memory
regime and no outcome could be attributed to the deadline knob alone (deadline,
heap, and REA pin 6.4.0→6.7.0 all moved together); (iii) REA's SIGTERM path is
typed and clean (cancelled + cleanup:complete + zero residue); (iv) the executed
cap chain 1800 s < 3600 s deadline < r4-12's own 30–90 min estimate
(corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:148-150) means the leg as
launched could not test the hypothesis; a decisive re-run needs an outer cap
> 5400 s, not the 4200 s P2.md:354-365 proposes.
```

**4b — if the parent prefers an append-only observation note inside the
existing r4-12 entry instead of the round record** (this keeps command A at
79/79 — appending cannot stale a cited range, and no new file/map token
appears):

```text
Recheck note (2026-10-18, arc2-loop1-round3): the prescribed raised-knob retry
(REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000, GHIDRA_HEADLESS_MAXMEM=8G,
rea-agents@6.7.0) ran the identical bytes and survived this entry's 900 s kill
point, still in auto-analysis, killed by its own 30-min outer cap (exit 124,
typed `cancelled`, no evidence id). Lower bound moved: wall >1800 s. Resource
regime differed (JVM peak RSS 8.35 GiB vs this entry's ~2.36 GB). The built-in
startup default is 330_000 ms; the "~900 s internal deadline" wording in
PROVINCE.md:139-144 and corpus/README.md:22/:117 was this entry's configured
value, not an internal constant. A decisive re-run needs an outer cap > 5400 s
(this entry's own 30–90 min estimate).
```

## 5. Conclusions, labeled

**OBSERVATIONS (ran/read this session):**

- Pre-pair receipt 5/5 OK rc=0 at 18:17:54Z; self-hash `3cba32fb…`; target
  sha256 `7a2ccd68…`, 91,662,336 B, mtime 2026-10-11.
- Command A at HEAD: 79/79, 10/10, 10.0/10.0, `missing []`, `dangling []`.
- Live leg at 18:04:46Z: `timeout -k 30 1800` wrapper (pid 2514443), JVM
  `-Xmx8G`; environ carries `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000`,
  `GHIDRA_HEADLESS_MAXMEM=8G`, `REA_PACKAGE_VERSION=6.7.0`; `run-big.sh:11`
  is the 1800 s cap.
- My own samples: JVM `VmHWM` reached and held 8,754,888 kB from ~18:14Z to
  the kill; RSS sawtoothed 1.71–7.42 GB in the early window (GC cycle).
- Ghidra log phases (E11's leg): ANALYZING at 14:58:27 local, PngDataType at
  14:59:02, VarnodeContext from 15:05:29 (137 by 18:23:53Z), FidAnalyzer +
  ApplyDataArchive at 15:17:49-50 — same sequence as r4-12's `:64-73`.
- Outcome (18:29:19Z): `WALL real=30m1.228s`, `EXIT=124`, `STDOUT_BYTES=87639`;
  stdout valid JSON, `code/category: cancelled`, `cleanup: complete`,
  `failure_message: "Ghidra startup was cancelled"`, 0 `evidence_id`, 0
  `timeout_ms`; session dir self-cleaned.
- 6.7.0 dist: `DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS = 330_000` (`:3`),
  `MAX_TIMER_DELAY_MS = 2_147_483_647` (`:10`), schema wiring at
  `dist/config/environment.js:39`; `GHIDRA_HEADLESS_MAXMEM` absent from
  `dist/config/` and read at `GhidraJavaLaunch.js:114`; `ParallelGCThreads=2`
  injected on 6.4.0:54 / 6.7.0:142.
- E10's meta (first-hand): exit 0, 44.117 s, `ev_92dea347…`, 6G heap, 6.5.0.
- Novelty greps over `.ufo/waves/arc2-loop1-round3/*.md`: no seat pairs
  6.4.0↔6.7.0 as an attribution threat for this leg; no seat cites r4-12's
  30–90 min estimate against the cap; E21 (18:29:59Z) captured the outcome
  independently.
- `GHIDRA_HEADLESS_MAXMEM` appears in the repo's non-round-3 files only as a
  *suggestion* (PROVINCE.md:143, corpus/README.md:172) — no prior execution
  recorded; all corpus `-Xmx` mentions are `2G`.

**INFERENCES:**

1. The retry is a genuine next-step execution, not a repeat of r4-12, but its
   claim as stated cannot certify a move: the measurable is bookkeeping, and
   the pre-accepted negative does not match the outcome class that occurred.
2. The single genuinely new frontier datum is the lower bound (wall > 1800 s
   for these bytes under 8G/3.6M on this host); everything else new is
   envelope/operability/arithmetic context.
3. Because deadline, heap, and REA pin all moved, a future HELD outcome would
   still not isolate the deadline knob — the confound is structural, not
   incidental.
4. The progress-rate comparison (~1.53× wall to reach r4-12's phase vs 2.0×
   available wall) suggests contention cost ~1.3–2×, consistent with E9's
   estimate; the retry under load cannot be treated as an idle-host test
   (r4-12's own precondition, `:154`).
5. Landing an entry for this leg would move the coverage denominator without
   moving the frontier — the re-run-dressed-as-a-move failure mode is a real
   landing hazard, not a rhetorical one.

**UNKNOWNS:**

1. Where the wall actually is: >1800 s, upper bound unmeasured; r4-12's
   30–90 min estimate remains the only bracket.
2. Whether the leg would have completed under a >5400 s cap on an idle host —
   untested; the confound (heap/version/contention) means even that outcome
   would need care in attribution.
3. Whether E11's own report (not yet present in the wave directory at my write
   time, 18:30:02Z) will classify the outcome as INCONCLUSIVE per P2's
   taxonomy; E21 (`:272-273`) has captured the same outcome independently.
4. Whether the parent chooses the round-record form (§4a) or the append-only
   note (§4b) — both keep command A at 79/79; the choice is the parent's.

## 6. Scope compliance

- Only repo write: this report. `git status --porcelain` at close:
  `?? .ufo/waves/arc2-loop1-round3/` only; HEAD unchanged at `679af5d…`.
- No config edits, no installs, no network fetches, no git mutations, no REA
  probe launched by me. The live leg is seat E11's; I sampled its `/proc` and
  its scratch read-only and killed nothing.
- Scratch: `/tmp/arc2-l3r3-CR3` (one `timeout` mechanics test) — removed; no
  residue (`ls -d` → absent); no runaway processes of mine (`pgrep gktest` →
  none).
- All five custody paths were read as sha256 digests only; config contents
  never opened; `.bashrc`/`.profile` never opened.
- Artifacts the parent should copy out of tmpfs before they are lost:
  `/tmp/arc2-l3r3-E11/analyze-stdout.json` (sha256 `41768a3f…`),
  `/tmp/arc2-l3r3-E11/run-big-console.log`, `/tmp/arc2-l3r3-E11/monitor.log`
  (E11's namespace — its seat owns the copy; I did not write into it).
