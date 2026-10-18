# CR1 — attack C1: third attempt at the same wall — sunk cost or sound frontier economics?

Observed 2026-10-18T21:47–21:49Z. HEAD `995e6a0`. Read-only except this file.
Scratch: none needed beyond live-service observation (watch-only; never signaled).
Custody pre-pair re-verified mid-window 5/5 (see §2.6); this seat wrote no custody path.

## 1. Verdict

**ATTACK REFUTED — sound frontier economics, not sunk cost — with one boundary
condition recorded for the wave.** The framing "third attempt at the same wall"
miscounts the wall: the r6 engagement never attempted the wall (it died in the
pre-script in 7.554 s before auto-analysis started — `.ufo/waves/arc2-loop1-round6/CR9.md:3`
"not a plain retry either: r3/r4 entered auto-analysis; this run died in the
pre-script"; `.ufo/waves/arc2-loop1-round6/Z1.md:151` "not a retry"). The actual
analysis attempts are r3 (outer 1800 s cap — time class), r4 (memcg self-kill at
its own 7G cap in 4m42s — memory class), and r7 (running). Between attempts, each
failure named a mechanism and the next attempt changed exactly that mechanism:
time → memory containment (r3→r4), memory → validated-name analyzer disable under
larger headroom (r4→r7), with r6 as a near-zero-cost diagnostic (7.554 s, 2.2G
peak, cap untouched) that converted a guessed knob into a registry-validated one
(`E4.md` javap `ldc` strings; absence sweep 0 hits for the wrong name).

Sunk-cost test, four criteria — all resolve for frontier economics:

1. **New falsifiable hypothesis per attempt.** Mechanism chain: time cap →
   memory cap → name validation → analyzer load + headroom. No hypothesis was
   re-run; each was derived from the prior failure's named cause
   (SCORECARD.md:800-808 r3; :894-901 r4; :1043-1052 r6).
2. **Pre-committed branches; failure cannot be spun.** HELD → knowledge entry +
   line-neutral map token (80→81, Z1 §5d form, Z1.md:161-163); typed
   refusal/kill → honest-negative taxonomy sentence; in-flight at close → "not
   verified for C1" — the round does not depend on this leg. The discipline has
   teeth on record: r3's CR3 refusal of "a re-run dressed as a move"
   (SCORECARD.md:806-808) and r6 landing NO big-leg knowledge while the leg was
   unresolved (denominator stayed 79 until the mid-rung sealed HELD on its own
   evidence, SCORECARD.md:1034-1043).
3. **Bounded, measured cost.** One transient user service: 9G cap, 7200 s
   deadline, disk TMPDIR, `OOMKills=0`; r4 precedent — one in-scope victim, zero
   bystanders (SCORECARD.md:895-898). No custody path touched (§2.6).
4. **Failure pre-classified honest-negative**, and the taxonomy branch gives
   every terminal class a landing (three wall classes already named:
   SCORECARD.md:1049-1051).

Marginal-value check: coverage is the owned axis and the only live frontier
move (depth/calibration saturated); the 91.6MB retry is the round's named
carried debt (SCORECARD.md:1090-1092, "the renamed-analyzer retry … with
validated names — E4's registry work"). No cheaper rung exists in the family:
the nearest intermediate binary is 75,679,864 B (`linux_release.x86_32`, §2.5) —
83% of the wall's size — so an intermediate rung would cost near-wall cost to
answer a question the frontier did not name. Executing the named debt at bounded
cost is the efficient move.

**Boundary condition (where this attack WOULD bite):** the mechanism list is
near-exhausted — time, memory, names, analyzer-load+headroom. REA's env schema
has no worker-count knob (CR9.md:50-52; E4.md:37 — no per-analyzer or worker
flag in headless), so the remaining knobs (deadline ↑, cap ↑) interpolate
already-failed mechanisms at rising cost. **If r7 ends in a kill or timeout, a
fifth engagement without a NEW mechanism is sunk cost; retire the retry and hold
the honest-negative taxonomy.** The wave should write that stop into the round
record now, while it is cheap.

## 2. Evidence

### 2.1 The wall history is four mechanisms, not one wall tried thrice

- r3: 91.6MB leg died at its own outer 1800 s cap, typed `cancelled`, no
  evidence; raised deadline never reached — SCORECARD.md:800-808.
- r4: contained scope 7G/1G-swap, OOM at own cap in 4m42s, `CONSTRAINT_MEMCG`,
  one in-scope victim, zero bystanders; "the wall is memory … not time" —
  SCORECARD.md:894-901.
- r6: service `arc2-r6-pe` exit 1 in 7.554 s, `MemoryPeak=2208227328` of
  `MemoryMax=9663676416`, `Unknown Ghidra analyzer for this program: Decompiler
  Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22`; "whether
  a renamed list would pass is unknown — not a retry" — Z1.md:151;
  E52.md:130-134; CR9.md:21-28.
- r7: this round; see §2.3. Carried-debt line authorizing it: SCORECARD.md:1090-1092.

### 2.2 The validated names are prior-round knowledge, not a guess

`.ufo/waves/arc2-loop1-round6/E4.md:19-35` — `javap -c -p -l` constructor
`ldc` strings: `Decompiler Parameter ID` (DecompilerFunctionAnalyzer),
`Decompiler Switch Analysis` (DecompilerSwitchAnalyzer), `Call Convention ID`
(DecompilerCallConventionAnalyzer); absence sweep: the wrong token = 0 hits in
the install. E4.md:66 verbatim-landable list is byte-identical to the running
service's env (§2.3).

### 2.3 Live service watch (read-only; never signaled)

```
$ systemctl --user show arc2-r7-pe -p ActiveState -p Result -p ExecMainStatus \
    -p MemoryMax -p MemoryPeak -p OOMKills -p Environment
ActiveState=active
Result=success
ExecMainStatus=0
MemoryPeak=8130965504
OOMKills=0
MemoryMax=9663676416
Environment="REA_GHIDRA_DISABLED_ANALYZERS=Call Convention ID,Decompiler Parameter ID,Decompiler Switch Analysis" REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G TMPDIR=/var/tmp/arc2-l7r7-pe GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

`systemctl --user status arc2-r7-pe --no-pager`: active since Sun 2026-10-18
18:40:26 -03; the headless child runs `-Xmx6G` and
`-preScript …ReaGhidraAnalysisOptions.java "Call Convention ID,Decompiler
Parameter ID,Decompiler Switch Analysis"`. First-sample process memory:
`/proc/3224474/status` → `VmRSS: 4376732 kB`, `VmHWM: 6792572 kB`.

**Key live fact:** `MemoryPeak=8130965504` (7.57G) **exceeds r4's 7G kill point
with `OOMKills=0` and the unit still active ~7 minutes after start** — the run
has already outlived the r4 wall and is in territory no prior attempt reached.
The retry is therefore not treading water; it is producing a result the record
does not yet contain (attribution open — see §4).

### 2.4 The r6 evidence priced the retry correctly

CR9 verified the failure class from the envelope before any claim: embedded
script argv proves the knob was forwarded; the `Unknown Ghidra analyzer` line
names the offender; `Processing aborted as a result of pre-script` proves
auto-analysis never started (CR9.md:9-14). Z1 §6 sealed it honest-negative with
no knowledge file and no token (Z1.md:151). The wave already refused to pay
sunk cost in landed knowledge for r6 — the denominator did not move on the big
leg (SCORECARD.md:1051-1052). CR9.md:52 names exactly the unknown r7 resolves:
"whether `Call Convention ID` plus `Decompiler Switch Analysis` (Parameter ID
already default-off) would move the r4 memcg wall."

### 2.5 No cheaper rung exists between the held mid-rung and the wall

```
$ ls -l /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/ | sort -k5 -n | tail
75679864 linux_release.x86_32
91662336 windows_release_arm64.exe   <- the wall (stat -c %s confirms 91662336)
98958848 windows_debug_arm64.exe
...
```

The held rungs are 2.5MB/44s and 17.7MB/2479s (SCORECARD.md:1035-1039,
:1050-1051). The next-smallest candidate in the family is 75.7MB — 83% of the
wall's cost for an unnamed question. Skipping to the named debt is the
economically correct move.

### 2.6 Custody (C1-adjacent, verified anyway)

`.ufo/waves/arc2-loop1-round7/receipts/config-pre-pair.txt` (6 lines, stamp
2026-10-18T21:40:26Z) lists 5 hashes. Mid-window re-hash of all five paths
returned all five digests byte-identical (devin mcp_config.json `16f496e6…`,
omp mcp.json `38d2a1d0…`, kimi config.toml `e0634d8c…`, .bashrc `7d2ca28a…`,
.profile `6c6be761…`) — 5/5.

### 2.7 Token discipline for the landing text

Per `.ufo/waves/arc2-loop1-round4/E21.md:225` (a bare version token in an
undeclared append → census FAIL; token-free → PASS) and Z1.md:186-195 (census
SCOPE ends at SCORECARD `:854`; version literals in appends are undeclared
loci), the landable block below is pin-free: no version literals, no bare
`:NNNN` tokens, no config.toml line references.

## 3. Verbatim-landable

```markdown
## CR1 — the 91.6MB retry is frontier economics, not sunk cost; stop rule recorded

The big leg has had three analysis attempts, not four: the r6 engagement never
reached analysis (typed pre-script name-mismatch refusal in seconds, sealed
honest-negative, no knowledge landed), so the scale hypothesis was untested
since r4. Each attempt changed exactly the mechanism the previous failure named:
time cap → memory containment → registry-validated analyzer disable under larger
headroom. The retry is the round's named carried debt, runs as a contained
caller-independent user service with a typed-envelope contract (HELD → entry +
same-line map token; refusal/kill → honest-negative taxonomy sentence; in-flight
at close → not verified), and its live unit has already exceeded the round-4
memory-kill point with zero OOM kills — evidence no prior attempt produced. An
intermediate rung would cost near-wall cost for an unnamed question; the named
debt is the efficient move. Stop rule for the wave: if this attempt ends in a
kill or timeout, the mechanism list is exhausted (no worker-count knob exists in
the analyze harness) — a fifth engagement without a new mechanism would be sunk
cost; retire the retry and hold the three-class honest-negative taxonomy.
```

## 4. Labels

- **Observation:** live show/status values and env string (§2.3); MemoryPeak
  8130965504 > 7G with OOMKills=0 and unit active; VmRSS/VmHWM first sample;
  target size 91662336 B; pre-pair 5/5 mid-window re-hash; all CR9/Z1/E4/E52
  quotes at the cited lines; the scorecard wall history r3/r4/r6 at the cited
  sections; export_templates size listing.
- **Inference:** the engagement sequence is mechanism-iterating frontier work
  by the four-criterion sunk-cost test; the run is past the r4 wall; "no cheaper
  rung" from the size listing; the landable block's stop-rule sentence follows
  from the mechanism list being near-exhausted plus no worker knob in the
  harness env schema.
- **Unknown:** the r7 terminal class (in-flight at this stamp; deadline
  7200 s from 21:40:26Z); whether survival past 7G is attributable to the
  disabled analyzers reducing concurrent load or simply to the larger cap —
  not separable from this watch; whether the run completes inside 7200 s
  (superlinear scaling from 17.7MB/2479s leaves timeout plausible; the disabled
  analyzers change the constant, direction unknown); whether MemoryPeak is a
  running max that could still approach the 9G cap.
