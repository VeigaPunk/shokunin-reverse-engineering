# CR7 (critic) — attack on smuggled exploratory claims and verdict inflation

Seat CR7, wave arc2-loop1-round3, 2026-10-18. Read-only on every repo and home file; **the
only write is this report**. No git mutations, no config edits, no installs, no network, no
battery leg, no MCP session (nothing to close). Scratch confined to
`/tmp/arc2-l3r3-CR7/` and `/tmp/arc2-l3r3-CR7-gate.py` (my namespace). I read — never wrote —
sibling scratch `/tmp/arc2-l3r3-E11/*` for the live C2 leg's outcome (§2). HEAD at every
command: `679af5d749f2fd48b9d543e3c99d348d5458f90f`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round3/` only (one mid-round exception, §1.3).

## 1. Verdict

**PARTIAL REFUTE — each of the three claims carries a verdict that cannot be earned as
written.** The smuggling is not in exploratory claims (the slot is unused, §4.1); it is in
claim *scopes and labels*:

1. **C1 cannot reach "dead-pointer loci in the scoped set N → 0".** The declaration's own
   re-point target `:2938/:2940` is dead in the live file (holds `max_context_size = 1000000`
   and `capabilities = [ "thinking", "tool_use" ]`); landing C1 verbatim mints two fresh dead
   pointers. The declared set also misnames its loci (`:9` and `:80` carry no line pointer at
   all — they carry stale *pin claims*; the dead `:128x` tokens sit on `:11`, `:12`, `:18`,
   `:88`) and omits at least three same-class loci the claim never names (`r4-16:233`,
   `r2-doctor-reverify-r2:46`, `lessons/2026-10-15-round-1.md:82`). Measured class size:
   **10 current-surface loci carrying 12 dead line-tokens across 6 files**, plus 2
   historical-qualified loci. Append-only errata cannot zero raw loci without a metric
   restatement (§1.1, §5 Block 1).
2. **C2 landed INCONCLUSIVE, not the pre-accepted "honest typed refusal/timeout".** The 91.6 MB
   leg died by its own outer cap: `EXIT=124`, wall 30m01s, stdout a `code:"cancelled"` envelope
   with **no `timeout_ms`** — the raised 3600000 ms deadline was never reached. The leg's script
   set a 3600 s internal deadline under `timeout -k 30 1800`; the cap fires first by
   construction, and the round's own P2.md:373 pre-declared that class INCONCLUSIVE. Recording
   this as "not-verified with the pre-accepted negative" would be verdict inflation: the
   negative that landed is a *procedure* negative (wall-clock under-provisioning), not a
   *capability* negative (§1.2, §5 Block 2).
3. **C3's "frozen run" evidence is unenforced by the artifact, and both drafts are tmpfs-bound.**
   E15's `expected.json` carries a `frozen_run` block, but the script contains **zero**
   occurrences of `frozen_run` and reads only `expected["snapshots"]`. Tamper control (mine,
   §3.3): flipping `frozen_run.verdict` → `clean` and its revision → a non-existent hash changes
   nothing — the output is byte-identical to the control (`failed findings=10 exit=1`, `diff`
   empty). The Gate standard's "Two evidences" limb ("so a later hand-edit of that artifact
   contradicts the frozen run", `PROTOCOL.md:375-381`) is therefore prose, not enforcement. Both
   drafts (E14, E15) live only under `/tmp`, which `PROTOCOL.md:341` excludes as evidence, so the
   operability row may record "improved" only if the parent lands the bytes in-repo in the same
   commit (§5 Block 3).

### 1.1 The exact failure of C1's metric (detail)

The claim defines its measurable as "dead-pointer loci in the scoped set N→0 (cited line lacks
cited content)". Three independent defects, each measured this session (§2.2, §2.3):

- **Unreachable target.** The declared repair is "re-point to `:2938/:2940`". Live read:
  `:2938` = `max_context_size = 1000000`, `:2940` = `capabilities = [ "thinking", "tool_use" ]`.
  The stanza is at `:3296`, the pin at `:3298`. A verbatim landing yields N→N+2.
- **Set mis-description.** Of the three named loci in `mcp-registrations.md`, two cannot even be
  evaluated under the claim's own definition (no cited line): `:9` is a heading ("...all pinned
  to `npx -y rea-agents@6.4.0 mcp`...") and `:80` is the Summary paragraph — both carry stale
  *pin statements* (a different class, C2 round-3's Class X), not line pointers. The actual dead
  tokens are on `:11`, `:12`, `:18`, `:88`.
- **Set under-inclusion.** Same-class dead loci outside the declared set, all re-verified by my
  resolver: `r4-16-frontier-rescan.md:233` (cites `:1283` → holds `capabilities = [ "image_in",
  ... ]`), `r2-doctor-reverify-r2.md:46` (cites `:1290` → holds `max_context_size = 500000`),
  `lessons/2026-10-15-round-1.md:82` (cites `:1287` → holds `[models."opencode-go-3/grok-4.7"]`).
  Landing only the declared set leaves the class non-zero by ≥3 loci.
- **Append-only vs raw count.** Already measured by E2.md §7: raw loci 4 → 4 (append-only keeps
  the dead lines); only "unwarned-by-a-later-erratum" reaches 0. That is a metric *redefinition*,
  and it changes the before-number too — the parent must restate both or record N as unchanged.

### 1.2 The exact failure of C2's pre-accepted negative (detail)

The seat line pre-accepts two outcomes: HELD (exit 0 + evidence id) or "honest typed
refusal/timeout → recorded negative". The leg produced neither. It produced the third class the
round itself pre-declared inconclusive (`P2.md:364,373`): `exit 124 + empty/partial stdout ->
outer cap fired; deadline NOT tested; INCONCLUSIVE`. Additional measured context:

- The envelope is REA's *cancellation* path, not its timeout path: `"code":"cancelled"`,
  `"failure_kind":"cancelled"`, `"failure_message":"Ghidra startup was cancelled"`, and
  `timeout_ms` absent (checked programmatically: `'timeout_ms' in json.dumps(d)` → `False`).
  The 6.7.0 cache separates the two mechanically (`dist/application/DirectAnalysis.js:320-321`
  installs `process.on("SIGTERM", cancel)` → `controller.abort()`; the deadline path is
  `dist/cli-runtime/binary-CWVNJhAC.js:9775` "Ghidra did not finish ... within its ${timeoutMs}
  ms startup deadline").
- The "on an idle host" precondition (`PROVINCE.md:141-144`) was not met: loadavg 13.04 at
  start, 12.8–19.7 through the leg, on 32 cores with the fleet live.
- Memory was under pressure at the kill: JVM RSS 8,892,652 kB against `-Xmx8G` (monitor
  18:28:20Z) — so even a longer wall clock might have hit a different wall; that stays unknown.
- No evidence id was sealed; stdout is 87,639 B of envelope. Cleanup was complete (no
  `rea-ghidra-*` session dir remains; no java process left).

### 1.3 One environment observation relevant to the round record

At 18:11:15Z `git status --porcelain` showed ` M corpus/README.md` (+3/−1: two `dummy` rows and
a retry-entry reference; mtime 18:12:28Z), and the worktree census over that text read
`mapped 79 / files 79 / dangling []` only because the dummy tokens match the map regex. By
18:23:35Z the worktree was clean again (187 lines, no `dummy` strings). This is another seat's
mid-round mutate-and-revert (P4.md:31-44 documents the same window); I observed it, wrote
nothing, and record it here because any census the parent runs mid-edit can false-pass or
false-fail on it.

## 2. Evidence — commands run THIS session (2026-10-18, stamps 17:57:55Z–18:30:00Z)

### 2.1 Pre-pair receipt — verified 5/5, five times

```
$ R=.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
$ wc -l < "$R"; grep -cE '^[0-9a-f]{64}  /' "$R"; grep -cE '^[0-9]{4}-' "$R"
6
5
1
$ tail -n +2 "$R" | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum "$R"
3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553
```

Verifications at 17:57:55Z, 18:11:15Z, 18:19:25Z, 18:23:02Z, 18:29:40Z — rc=0 every time;
`sha256sum /home/vgpnk/.kimi-code/config.toml` returned `bd5a78d1a829f480f12735bdfc18f6f8778e
702caac7d766a776eda5597a9f3c` at every one of those checks.

### 2.2 Live config anchors (the C1 target state)

```
$ sha256sum /home/vgpnk/.kimi-code/config.toml ; wc -l /home/vgpnk/.kimi-code/config.toml
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c
3322
$ awk 'NR==2938||NR==2940||NR==3296||NR==3298||NR==3299{printf "%d: %s\n",NR,$0}' ~/.kimi-code/config.toml
2938: max_context_size = 1000000
2940: capabilities = [ "thinking", "tool_use" ]
3296: [mcp_servers.rea]
3298: args = [ "-y", "rea-agents@6.7.0", "mcp" ]
3299: startup_timeout_sec = 30
```

The file's mtime is `2026-10-18 14:50:34.896343019 -0300` (= 17:50:34Z) — the third observed
state of the day after the round-2 drift receipt's `:2938→:3225` (`f10b01e9…`, backed up as
`config.toml.20261018-145016.bak`). I also confirmed the round-2 drift record's own claim:
`config.toml.20261018-143236.bak` carries `:2938` = `[mcp_servers.rea]` and its sha256 is
`3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a` — the receipt value.

### 2.3 The 15-locus resolver — my own script, run this session

Script at `/tmp/arc2-l3r3-CR7/census.py`; it reads each citing line from `HEAD:<file>` (git
object, not worktree), extracts the number with a per-locus regex, and prints what the cited
line holds (repo files from HEAD, `config.toml` from the live file):

```
SCORECARD.md:270  cites :157  holds '| entry | round | gist |'
SCORECARD.md:270  cites :160  holds '| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠pr'
SCORECARD.md:59  cites :2940  holds 'capabilities = [ "thinking", "tool_use" ]'
SCORECARD.md:698  cites :2940  holds 'capabilities = [ "thinking", "tool_use" ]'
PROVINCE.md:18  cites :2940  holds 'capabilities = [ "thinking", "tool_use" ]'
PROVINCE.md:18  cites :3227  holds 'default_effort = "high"'
corpus/knowledge/2026-10-13-mcp-registrations.md:11  cites :1285  holds 'support_efforts = [ "low", "medium", "high", "xhigh" ]'
corpus/knowledge/2026-10-13-mcp-registrations.md:12  cites :1285  holds 'support_efforts = [ "low", "medium", "high", "xhigh" ]'
corpus/knowledge/2026-10-13-mcp-registrations.md:18  cites :1288  holds 'provider = "opencode-go-3"'
corpus/knowledge/2026-10-13-mcp-registrations.md:88  cites :1284  holds 'display_name = "Grok 4.7 (key 2)"'
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43  cites :1284  holds 'display_name = "Grok 4.7 (key 2)"'
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:233  cites :1283  holds 'capabilities = [ "image_in", "always_thinking", "tool_use" ]'
corpus/knowledge/2026-10-13-r2-doctor-reverify-r2.md:46  cites :1290  holds 'max_context_size = 500000'
corpus/lessons/2026-10-15-round-1.md:82  cites :1287  holds '[models."opencode-go-3/grok-4.7"]'
SCORECARD.md:291  cites :1478  holds 'max_output_size = 131072'
```

Classification (mine): **10 current-surface loci / 12 dead line-tokens across 6 files** (the 10
loci above minus the last two rows' qualifiers: `SCORECARD.md:59` is stamp-qualified — its own
text says "per the 16:57:35Z custody receipt" — and `SCORECARD.md:291` is a dated luna-round-2
record); **2 dead README tokens on `SCORECARD.md:270`** (`:157`, `:160`; the bullet it names is
at `corpus/README.md:177`). This independently re-derives V1.md's token count (11 by its
convention) and E15's finding of the `:9/:80` mis-description; the counting convention differs,
the loci do not.

### 2.4 The declared `:9/:80` loci, read at their lines

```
$ sed -n '9p;80p;88p' corpus/knowledge/2026-10-13-mcp-registrations.md
9:  ## Candidate: Exactly three client files register REA — omp, devin, kimi — all pinned to `npx -y rea-agents@6.4.0 mcp` with identical env
80: REA is registered for 3 of 7 surfaces (omp via ...), all launching pinned `npx -y rea-agents@6.4.0 mcp` with `GHIDRA_INSTALL_DIR`/`JAVA_HOME`; ...
88: - kimi stanza header is `config.toml:1284` (startup_timeout_sec at 1287), not 1285/1288. (audit-A, consistency)
```

`:9` and `:80` contain no `config.toml:NNNN` token; they are stale pin statements (Class X in
C2.md's round-3 census, which also lists `:31`, `:52`, `:66` as host-state-drifted content).
The claim's parenthetical "(... carry dead `:1284/:1287` pointers ...)" is false for two of its
three named loci — which matters because the claim's metric is defined over *pointers*, and
these two are not pointer loci at all.

### 2.5 C2 leg outcome — read-only observation of `/tmp/arc2-l3r3-E11/`

```
$ cat /tmp/arc2-l3r3-E11/run-big-console.log
START_UTC=2026-10-18T17:58:20Z loadavg=13.04
WALL real=30m1.228s user=60m38.787s sys=1m8.320s
END_UTC=2026-10-18T18:28:21Z
EXIT=124
STDOUT_BYTES=87639
$ head -c 240 /tmp/arc2-l3r3-E11/analyze-stdout.json
{"error":"Analysis failed","code":"cancelled","category":"cancelled","message":"Analysis was cancelled. Start it again when ready.","retryable":true,...
$ tail -c 120 /tmp/arc2-l3r3-E11/analyze-stdout.json
..."failure_kind":"cancelled","failure_message":"Ghidra startup was cancelled"}}}
$ python3 -c "import json; d=json.load(open('/tmp/arc2-l3r3-E11/analyze-stdout.json')); print(d['details']['operation'], d['details']['cleanup'], 'timeout_ms' in json.dumps(d))"
read_binary_inventory_summary complete False
$ head -6 /tmp/arc2-l3r3-E11/run-big.sh
export TMPDIR=/tmp/arc2-l3r3-E11/tmp
export npm_config_offline=true
export REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000
export GHIDRA_HEADLESS_MAXMEM=8G
time timeout -k 30 1800 npx -y rea-agents@6.7.0 analyze "$PE" --format json
$ grep 'rss=' /tmp/arc2-l3r3-E11/monitor.log | tail -1
2026-10-18T18:28:20Z java pid=2514831 rss=8892652 kB pcpu=154
$ ps -o pid,stat -p 2514831 ; ls -d /tmp/arc2-l3r3-E11/tmp/rea-ghidra-* 2>&1
(no process)
no rea-ghidra session dir (cleanup complete)
```

`PROVINCE.md:141-144` records the plan this leg executed ("raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
to ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host"); `P2.md:354-364` had already
measured that the running leg's 1800 s cap cannot reach the 3600 s deadline and prescribed a
4200 s outer cap for a decisive re-run; `P2.md:373` pre-declared `exit 124 + empty/partial
stdout -> ... INCONCLUSIVE`. The artifact matches that pre-declared class exactly.

### 2.6 Command A at HEAD (for the C2 record)

```
$ python3 <recipe SCORECARD.md:92-123 verbatim> "$(git rev-parse HEAD)"
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "rule_blocks": 10}
```

## 3. C3 — the gate as an artifact: what I reproduced, and the tamper control

### 3.1 E15's gate, reproduced by me (copy at `/tmp/arc2-l3r3-CR7-gate.py`, sha256 `0c5350b1…`)

```
$ python3 gate.py --selftest --expected expected.json | tail -1
CITATION_DRIFT_SELFTEST: CLEAN cases=10 passed=10 failed=0 exit=0
$ python3 gate.py --root . --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f \
    --table pointer-table.json --expected expected.json --snapshot-dir . | tail -1
CITATION_DRIFT_VERDICT: failed findings=10 exit=1
```

The live-run findings reproduce E15.md §5.2 verbatim (9 `citation_dead` + 1
`citation_historical_ok`, across `SCORECARD.md:270` ×2, `PROVINCE.md:18`, `SCORECARD.md:698`,
`mcp-registrations.md:11,:12,:18,:88`, `r4-16-frontier-rescan.md:43`). The selftest is real and
green; the gate fails the live tree and (per E15 §5.3) passes a repaired scratch tree.

### 3.2 The enforcement gap — `frozen_run` is never read

```
$ grep -c 'frozen_run' /tmp/arc2-l3r3-E15/citation-drift-gate.py
0
$ python3 - <<'PY'  # keys actually read from expected.json
import re, pathlib
src = pathlib.Path('/tmp/arc2-l3r3-E15/citation-drift-gate.py').read_text()
print(re.findall(r'expected\.get\((".*?")\)', src))
PY
['"snapshots"']
```

`expected.json` (sha256 `6ebada28259262da835c8371b9bfccfcebe4500c22fdd19716933a62fbca1beb`)
carries `frozen_run: {revision: 679af5d…, verdict: "failed", expected_findings: ["citation_dead"]}`
— and no code path reads it.

### 3.3 The tamper control (my decisive experiment)

I built a tampered copy of `expected.json` that flips `frozen_run.verdict` → `"clean"`, sets
`frozen_run.revision` → `"deadbeef"×5`, and leaves the `snapshots` digest untouched
(`/tmp/arc2-l3r3-CR7/expected-tampered-frozenrun.json`, sha256 `157516ed…`), then ran the gate
against both files:

```
$ python3 gate.py --root . --rev 679af5d --table pointer-table.json \
    --expected expected.json            --snapshot-dir .  | tail -1
CITATION_DRIFT_VERDICT: failed findings=10 exit=1        (control)
$ python3 gate.py --root . --rev 679af5d --table pointer-table.json \
    --expected expected-tampered-frozenrun.json --snapshot-dir .  | tail -1
CITATION_DRIFT_VERDICT: failed findings=10 exit=1        (tampered)
$ diff out-control.txt out-tampered.txt
(no output — IDENTICAL)
```

**The committed expected verdict is inert.** The Gate standard's Two-evidences clause exists
precisely so that "a later hand-edit of that artifact contradicts the frozen run"
(`PROTOCOL.md:375-377`); with this draft it does not. (E17.md:356 flags the sibling issue — the
snapshot itself is still in tmpfs — but the not-read defect is separate and, to my check,
unnamed.)

### 3.4 The two drafts are not convergent

- E14's gate (`/tmp/arc2-l3r3-E14/citation-drift.py`, sha256 `2e4f30e5…`; table
  `/tmp/arc2-l3r3-E14/table.tsv`, sha256 `fabe46cb71981ba35411d9869f0f2e2a4ee03f4766170a252c26e7d05da9332`)
  is a needle-at-line check. I ran it in its own simroot: `CLEAN finding=clean rows=36 repo=24
  host=12 failed=0 could_not_evaluate=0 advisory=5 revision=92534f50…+dirty`, rc=0; `--frozen`
  → `CLEAN finding=reproduces rows=24 verdict_exit=0`. Its table contains **no row for
  `SCORECARD.md:270`** (`grep -n '270' table.tsv` → only `SCORECARD.md 544`), so by design it
  cannot catch the very locus C1 is about. Its `host` rows (the `config.toml` pointer family)
  are advisory and never change the exit code — i.e. it deliberately does not gate the class
  C1 wants drained.
- E15's gate is the `extracted`-number resolver (13 entries; 12 `extracted` + 1 `exact`), which
  *does* catch `SCORECARD.md:270`, and whose repaired-tree run goes green. The two are different
  designs with different scopes; the parent must not merge them as "two independent drafts that
  converge".
- Both drafts, and E15's redacted snapshot and E14's frozen dir, live under `/tmp` only.
  `PROTOCOL.md:341`: "paths under `tmpfs` (`/tmp`, `/dev/shm`) ... are not evidence — commit
  the artifact or cite a reproducible command." The round cannot cite `/tmp/arc2-l3r3-E15/...`
  hashes as the capability's evidence pointer.

## 4. The smuggled-claim audit (the seat's question)

### 4.1 Exploratory slot — clean

`grep -rn -iE 'exploratory|unprovable' .ufo/waves/arc2-loop1-round3/*.md` returns only C4.md's
own adjudication (:122-123, :377-378: "Zero exploratory claims declared; the ≤1 exploratory slot
is unused"). My sweep agrees: no claim in the round is typed exploratory, so no
`unprovable-but-better` verdict is smuggled through the slot. (C4's sweep is the primary
evidence; mine is corroboration.)

### 4.2 Where the smuggling actually sits

- **C1 — scope smuggling.** The headline verb is "drain the pointer-drift class"; the metric is
  "dead-pointer loci in the scoped set". The class ⊃ the scoped set, measured: ≥3 same-class
  loci outside the set (§2.3). A verdict of "improved" on the metric is defensible only if the
  record *also* states the class count before and after and the set's boundaries. As written,
  the reader would infer the class is drained when only a subset can be.
- **C1 — metric smuggling.** The claim's remedy is append-only errata, which by construction
  cannot change "cited line lacks cited content" for the raw loci (E2.md §7 measured 4 → 4).
  Reaching 0 requires redefining the metric (e.g. "unwarned by a later erratum") — a scope
  change that must be stated, not silently substituted.
- **C2 — label smuggling.** "The claim then reports as not-verified (honest stop on the axis —
  pre-accepted)" is pre-accepted only for a *typed refusal/timeout*. What landed is the
  round's own INCONCLUSIVE class (`P2.md:364,373`). The record must not paste the pre-accepted
  label onto an inconclusive kill; the honest text is "deadline not tested; the wall-clock
  under-provisioning is the proximate cause; capability status unchanged from r4-12".
- **C2 — basis mis-citation.** The seat line calls C2 "frontier move per the stagnation nudge".
  C4.md:106-119 measured the nudge inactive: `AXES.md:66-70` requires *no capability entered
  within the window*, but the custody capability entered at arc2-loop1-round2
  (`SCORECARD.md:621`, first-working round) inside the window reset at luna-round-10
  (`SCORECARD.md:630-633`). I verified both cells read as stated. C2 remains a legitimate
  owned-axis move (the three-way 10.0 tie, most-falsifiable precedent, `SCORECARD.md:275-277`);
  the nudge phrase must not land in the round record (Z2.md:227,240 and E18.md:386 still carry
  it).
- **C3 — state smuggling.** "Gate v1 committed" is aspirational: at HEAD nothing is committed
  (no `scripts/` dir exists; `ls scripts` → No such file or directory). "Capability acquisition"
  rows enter only "through a round that demonstrates the capability running" (`AXES.md:59-63`);
  a tmpfs-bound rehearsal does not satisfy that as the row's evidence pointer. The row is
  legitimate only after in-repo landing, in the same commit that measures it.

### 4.3 Verdict-inflation ledger (what the round record must not say)

| Tempting sentence | Why it is inflation | Honest form |
|---|---|---|
| "C2: not-verified, the pre-accepted honest negative recorded" | the negative is inconclusive (cap-fired), not typed; the deadline was never tested | "C2: INCONCLUSIVE — outer cap fired at 30m01s (exit 124); raised deadline untested; capability status unchanged" |
| "C1: dead-pointer loci N → 0" | declared set is under-inclusive and its re-point target is dead; raw loci can't zero under append-only | "C1: declared-set tokens repaired by anchor citations; class count 12 → N' with the set boundaries stated" |
| "C3: citation-drift gate committed (E15/E14 convergent)" | not committed; drafts differ in design and scope; frozen-run unenforced | "C3: gate landed at <path> with frozen-run enforcement wired/waived; drafts E14/E15 differ (§3.4)" |
| "zero drift across the battery window" | the in-window 5/5 held for the *custody paths* (verified by me 5×), but the round's own mid-round mutate-and-revert (§1.3) and the config's 18:01Z transient (E19/E14; not observed by me) are part of the window's story | scope the claim to the five named paths, as round 2 already did |

## 5. Text for the parent to land VERBATIM (if used)

### Block 1 — C1 restated (metric + measured before-state)

```text
C1 (freshness) — restated before landing (CR7, arc2-loop1-round3):
Scope: "dead pointer" = a committed citation token (`path:NNNN`, or a range) whose cited
line/range does not hold the content the citing sentence claims; resolved against the live
operator surface for citations into ~/.kimi-code/config.toml and against the committed
revision for repo files.
Measured before (HEAD 679af5d, live config sha256 bd5a78d1…, stanza :3296, pin :3298):
- 10 current-surface loci carrying 12 dead config.toml line-tokens across 6 files:
  PROVINCE.md:18 (:2940, :3227), SCORECARD.md:698 (:2940),
  corpus/knowledge/2026-10-13-mcp-registrations.md:11 (:1285), :12 (:1285), :18 (:1288),
  :88 (:1284, :1287), corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43 (:1284),
  :233 (:1283), corpus/knowledge/2026-10-13-r2-doctor-reverify-r2.md:46 (:1290),
  corpus/lessons/2026-10-15-round-1.md:82 (:1287).
- 2 dead README tokens on SCORECARD.md:270 (:157, :160; the bullet it names is at
  corpus/README.md:177 and now reads "held, not frontier" — the debt it describes is
  discharged, so the honest repair marks the parenthetical historical, it does not re-point
  to a discharged referent).
- 2 historical-qualified tokens, recorded not repaired: SCORECARD.md:59 (:2940; its own text
  says "per the 16:57:35Z custody receipt"), SCORECARD.md:291 (:1478; dated luna-round-2
  record).
Repair form that can reach zero: anchor citations (name the TOML key or the content), never a
fresh bare line number into ~/.kimi-code/config.toml — the stanza has walked :2913 → :2930 →
:2938 → :3225 → :3296 in one day. Append-only files get an append-only erratum whose own
citation is an anchor; the raw dead lines stay by construction (E2.md §7).
Do NOT land the declaration's ":2938/:2940" re-point verbatim: in the live file :2938 =
`max_context_size = 1000000`, :2940 = `capabilities = [ "thinking", "tool_use" ]`.
```

### Block 2 — C2 disposition

```text
C2 (coverage) — disposition (CR7, arc2-loop1-round3):
Verdict: INCONCLUSIVE — the raised deadline was never tested. The 91.6 MB leg ran
17:58:20Z–18:28:21Z and died by its own outer cap: `WALL real=30m1.228s … EXIT=124`,
stdout 87,639 B = {"code":"cancelled", "details":{"operation":"read_binary_inventory_summary",
"cleanup":"complete"}, "failure_kind":"cancelled", "failure_message":"Ghidra startup was
cancelled"} with no `timeout_ms` anywhere. The script exported REA_GHIDRA_STARTUP_TIMEOUT_MS=
3600000 under `timeout -k 30 1800`; the 1800 s cap cannot reach the 3600 s deadline
(P2.md:354-364), so this is the class P2.md:373 pre-declared INCONCLUSIVE — NOT the
pre-accepted typed refusal/timeout. JVM RSS was 8,892,652 kB at the last sample against
-Xmx8G; loadavg 13.0-19.7 throughout (the "idle host" precondition of PROVINCE.md:141-144
was not met). No evidence id was sealed; cleanup complete; no process or session dir residue.
Consequences: the claim reports NOT-VERIFIED and the record must say "deadline not tested",
not "honest typed negative"; no knowledge entry lands; denominator stays 79; command A stays
79/79, 10/10, 10.0/10.0 (measured at HEAD this session). A decisive re-run needs an outer cap
greater than 3600000 ms (P2.md:362 prescribes 4200); until then the scale wall's status is
unchanged from r4-12.
```

### Block 3 — C3 landing condition

```text
C3 (operability) — landing condition (CR7, arc2-loop1-round3):
The operability row may record "improved" only if, in the same commit that measures it, the
gate's own bytes land in-repo: script + pinned pointer table + frozen snapshot with digests +
the SKILL.md registry row. Two independent drafts exist and are NOT convergent (E14:
needle-at-line, 43-row table sha256 fabe46cb…, no row for SCORECARD.md:270, host rows
advisory-only; E15: extracted-number resolver, 13 entries, table sha256 d7bf0eb3…, script
sha256 0c5350b1…). Both live only under /tmp, which PROTOCOL.md:341 excludes as evidence.
If E15's draft is landed, wire the frozen-run comparison into the script or drop the clause
from the registry row: the script reads only expected["snapshots"] (0 occurrences of
`frozen_run`), and a hand-edit flipping frozen_run.verdict to "clean" and its revision to a
non-existent hash changes nothing — my tamper control's output was byte-identical to the
control (failed findings=10 exit=1, diff empty). The Two-evidences limb of the Gate standard
(PROTOCOL.md:375-381) is then prose, not enforcement.
```

## 6. Conclusions, labeled

**OBSERVATION** (ran or read this session):

- Pre-pair receipt verifies 5/5 rc=0, shape 6/5/1, self-hash `3cba32fb…`, at five stamps
  17:57:55Z–18:29:40Z; live `config.toml` sha256 `bd5a78d1…` (3322 lines) at every check.
- The live config's rea stanza is `:3296`/`:3298`; `:2938`, `:2940`, `:1284`, `:1287`, `:1288`,
  `:1290`, `:1291`, `:1478`, `:3227` all hold unrelated lines (each read at its line).
- My 15-locus resolver output (verbatim in §2.3); 12 dead tokens on 10 current-surface loci
  across 6 files, 2 dead README tokens on `SCORECARD.md:270`, 2 historical-qualified.
- The E11 leg's outcome: `EXIT=124`, wall 30m01.228s, `cancelled` envelope, `timeout_ms`
  absent, `failure_kind:"cancelled"`, JVM RSS 8.89 GB, cleanup complete, no residue.
- E15's gate: my selftest 10/10 exit 0; my live run `failed findings=10 exit=1`; the script
  contains 0 `frozen_run` references and reads only `expected["snapshots"]`; the tamper control
  (frozen_run flipped) produced byte-identical output.
- E14's gate: my live run in its simroot `CLEAN … revision=92534f50…+dirty` rc=0; `--frozen`
  reproduces exit 0; its table has no `SCORECARD.md:270` row.
- Command A at HEAD: 79/79, 10/10, 10.0/10.0, `missing []`, `dangling []`.
- The worktree `corpus/README.md` was mid-edit by another actor at 18:11-18:12Z (+3/−1, two
  `dummy` rows) and clean again by 18:23:35Z (187 lines, no `dummy`).
- `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only; HEAD unchanged
  throughout at `679af5d749f2fd48b9d543e3c99d348d5458f90f`.

**INFERENCE**:

- C1 as written is unearnable: the declared repair target is dead, the set misnames its loci
  and omits ≥3, and append-only cannot zero the raw metric. "Improved" is defensible only on a
  restated metric with a measured before-count (Block 1).
- C2's only honest verdict is INCONCLUSIVE; the pre-accepted "honest negative" belongs to a
  typed refusal/timeout that did not occur. A decisive re-run is cheap (one knob change: outer
  cap > 3.6M ms) and is the natural carried debt.
- C3's capability row is legitimate only after in-repo landing; as drafted, the frozen-run
  clause is unenforced and the evidence pointers would be tmpfs paths.
- No exploratory claim was smuggled; the smuggling is scope/label-level, as itemized in §4.2.

**UNKNOWN**:

- Whether the parent lands C3 at all, and which draft; whether it wires the frozen-run check.
- Whether the 18:01Z config transient (`9ac8023b…`, 3336 lines, stanza `:3310` per E19/E14) was
  a settled state or a mutate-and-revert; I never observed it — all five of my reads saw
  `bd5a78d1…` only. (E19.md:27-40 and E14.md:120-128 describe it; C3.md:65-75 calls it an
  observed transient.)
- Whether REA's `cancelled` envelope lacks `timeout_ms` on all versions or only 6.7.0.
- What a >3.6M ms run would do (the deadline was never tested, so both HELD and
  provider_timeout remain open).

## 7. Reproduction (all commands run by this seat, in order)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
wc -l < "$R"; grep -cE '^[0-9a-f]{64}  /' "$R"; tail -n +2 "$R" | sha256sum -c -; sha256sum "$R"
sha256sum ~/.kimi-code/config.toml; awk 'NR==2938||NR==2940||NR==3296||NR==3298{printf "%d: %s\n",NR,$0}' ~/.kimi-code/config.toml
python3 /tmp/arc2-l3r3-CR7/census.py                     # the 15-locus resolver, §2.3
cat /tmp/arc2-l3r3-E11/run-big-console.log; head -c 240 /tmp/arc2-l3r3-E11/analyze-stdout.json; head -6 /tmp/arc2-l3r3-E11/run-big.sh
python3 /tmp/arc2-l3r3-CR7-gate.py --selftest --expected /tmp/arc2-l3r3-E15/expected.json | tail -1
python3 /tmp/arc2-l3r3-CR7-gate.py --root . --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f \
  --table /tmp/arc2-l3r3-E15/pointer-table.json --expected /tmp/arc2-l3r3-E15/expected.json --snapshot-dir /tmp/arc2-l3r3-E15 | tail -1
python3 /tmp/arc2-l3r3-CR7-gate.py --root . --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f \
  --table /tmp/arc2-l3r3-E15/pointer-table.json --expected /tmp/arc2-l3r3-CR7/expected-tampered-frozenrun.json --snapshot-dir /tmp/arc2-l3r3-E15 | tail -1
grep -c frozen_run /tmp/arc2-l3r3-E15/citation-drift-gate.py        # → 0
cd /tmp/arc2-l3r3-E14/simroot && python3 /tmp/arc2-l3r3-E14/citation-drift.py --root . | tail -1
python3 /tmp/arc2-l3r3-E14/citation-drift.py --root . --frozen | tail -1
```

## 8. Pointers used (all resolved by this seat this session)

Repo: `SCORECARD.md:16-17, :23, :59, :68-72, :270, :291, :544, :621, :630-633, :698, :705`;
`PROVINCE.md:18, :141-144`; `corpus/knowledge/2026-10-13-mcp-registrations.md:9, :11, :12, :18,
:80, :88`; `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43, :233`;
`corpus/knowledge/2026-10-13-r2-doctor-reverify-r2.md:46`;
`corpus/lessons/2026-10-15-round-1.md:82`; `corpus/README.md:138, :157, :160, :177`;
`SKILL.md:327-336`. Fleet: `/home/vgpnk/Projects/shokunin/PROTOCOL.md:341, :360-408`;
`/home/vgpnk/Projects/shokunin/AXES.md:33-34, :47-48, :59-63, :66-72`. Wave:
`.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt:1-6`;
`.ufo/waves/arc2-loop1-round3/E15.md:5-6, :13-26, :116-160, :212-235, :296-341, :407-420`;
`.ufo/waves/arc2-loop1-round3/E14.md:14-77, :115-135, :200-213, :712`;
`.ufo/waves/arc2-loop1-round3/E17.md:356`; `.ufo/waves/arc2-loop1-round3/P2.md:43, :354-373`;
`.ufo/waves/arc2-loop1-round3/C4.md:106-119, :373-378`; `.ufo/waves/arc2-loop1-round3/C2.md:109-110,
:158-166`; `.ufo/waves/arc2-loop1-round3/E2.md §1, §7`;
`.ufo/waves/arc2-loop1-round3/V1.md:16, §2.1`; `.ufo/waves/arc2-loop1-round3/E19.md:18-48`;
`.ufo/waves/arc2-loop1-round3/Z2.md:227, :240`; `.ufo/waves/arc2-loop1-round3/P4.md:31-44`.
Home (read-only): `~/.kimi-code/config.toml` (sha256 `bd5a78d1…`),
`~/.kimi-code/config.toml.20261018-143236.bak` (sha256 `3546e033…`),
`~/.kimi-code/config.toml.20261018-145016.bak` (sha256 `f10b01e9…`). Scratch (mine):
`/tmp/arc2-l3r3-CR7/` (`census.py`, `expected-tampered-frozenrun.json`, `out-control.txt`,
`out-tampered.txt`), `/tmp/arc2-l3r3-CR7-gate.py`; sibling scratch read, never written:
`/tmp/arc2-l3r3-E11/*`, `/tmp/arc2-l3r3-E14/*`, `/tmp/arc2-l3r3-E15/*`.

## 9. Scope compliance and residue

- Only repo write: this report. No git mutations; HEAD `679af5d` before and after every check.
- No config edits, no installs, no network, no MCP session, no battery leg; no process
  launched by this seat (so no runaway to kill; the E11 leg was another seat's and exited on
  its own cap at 18:28:21Z).
- Five custody paths read as sha256 digests only; no config contents were copied out except
  the already-published line numbers and values quoted in this report.
- Residue: `/tmp/arc2-l3r3-CR7/` (4 files, cited as the tamper-control evidence) and
  `/tmp/arc2-l3r3-CR7-gate.py` (the reproduced E15 gate copy). Nothing else.
