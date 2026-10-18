# CR3 — round-7 attack: verdict inflation + smuggled claims; C1 negative-branch pre-acceptance

Seat CR3, wave `arc2-loop1-round7`, 2026-10-18. Observation window
18:47–19:15 -03 (my samples bracket the 19:04:11 seal). HEAD
`995e6a0799c4dad26942de15bd9058fe7acb676d`; tree clean except the untracked
round-7 wave dir. Only repo write: this file. `arc2-r7-pe` observed
read-only, never signalled; no `reset-failed` run by this seat (the unit was
already unloaded at my post-seal check — done by another actor). No custody
path written; no scratch dir needed (all evidence inline).

## 1. Verdict

**INFLATION: NONE FOUND. SMUGGLED CLAIMS: ATTACK SUSTAINED ON THREE, PLUS
ONE STALE POINTER AND ONE HELD-BRANCH OMISSION. C1 NEGATIVE BRANCH STAYED
PRE-ACCEPTED THROUGH SEAL.**

1. **No verdict inflation in the wave artifacts.** The run sealed at
   19:04:11.350 (envelope mtime; same second as the journal `Consumed`
   line). Every seat file asserting a terminal outcome postdates the seal by
   mtime; every pre-seal file asserts no outcome (§2.3). Baseline command A
   mechanically reproduced at HEAD: 80/80, missing [], dangling [], 11/11,
   10.0/10.0 — nothing pre-landed.
2. **Sustained — smuggled causal claim in the dispatched C2 wording.**
   "queue-drain rule #12 — long Ghidra analyze runs are caller-independent
   systemd user services, never --scope (**r4 teardown, r6 holds as
   evidence**)" re-smuggles the story round 6's adjudication refused:
   round 4 died by memcg OOM with its launcher still alive (no
   `Stopping`/`Killing` line exists), and round 6's service self-exited in
   7.554 s under an untouched 9G cap — it evidences nothing about
   caller-independence, which is untested on this host. Landing rule #12
   with this rationale would re-introduce the exact generic-advice +
   false-causal combination CR14 sustained an attack against (§2.4).
3. **Sustained — smuggled mechanical dependency in "Command A 11→12,
   12/12 resolvable, token-free".** Command A's depth regex resolves only
   `corpus/knowledge/*.md:N(-M)` citations and `valid = bool(refs)` fails
   any rule without one (`SCORECARD.md:105-117`). `corpus/lessons/…` — the
   C3 lesson file — does not match the pattern. The claimed 12/12 is
   therefore sequence-coupled to C1's knowledge entry existing at command-A
   time (or requires citing an already-resolvable knowledge file). As
   dispatched it reads as an unconditional property of the rule text (§2.5).
4. **Sustained (hazard, not yet a defect) — stale re-point arithmetic.**
   E52's landing constraints were written at pre-landing HEAD `54bc9dd`;
   its `:165/:166/:167/:177` README pointers are one r6-insert stale at
   HEAD `995e6a0`. The round-7 C3 coupled re-point is `SCORECARD.md:69`
   **178→179**, not 177→178. Following E52 §3.3 literally re-points the
   wrong line — the same stale-pointer class rounds 3–5 chased (§2.6).
5. **HELD-branch omission.** The dispatched HELD branch lists "knowledge
   entry + map token" only. A 91.6MB HELD additionally requires: (a)
   same-line rewording of the live frontier recommendation at
   `corpus/README.md:173` ("hits the ~900s internal session deadline; raise
   ≈3.6M + 6-8G, or bisect 2-5MB") — the `held, not frontier` move
   (`SCORECARD.md:69` precedent), which is now falsified advice; (b) the
   map-token stem appended on the **same physical line** of the coverage-map
   row `corpus/README.md:22` (Z1 §5d form), leaving the row's historical
   "dies at the ~900s" gist as history with the supersession carried by the
   new entry; (c) the entry must state the hold is **mitigated** — envelope
   `analyzer_preset: "ghidra-default+disabled:Call Convention ID…"` vs the
   r6 mid-rung's plain `ghidra-default` natural hold
   (`SCORECARD.md:1046-1048`). E2's verdict cell (`E2.md:160-163`) covers
   none of (a)/(b).
6. **C1 negative branch: pre-acceptance held.** The dispatch's branch table
   pre-registers all three outcomes; Z1's round-6 admission rule stands
   (`Z1.md:86` "Do not admit 3/3 on an in-flight mid-rung", `:152` "do not
   invent a class"); E5 pre-wrote every negative form behind "land only if
   the observed terminal state matches" guards and asserted no terminal
   state (`E5.md:24-25`); at my pre-seal samples the run was in-flight
   (active/running, 0-byte stdout.json) and no HELD artifact existed
   anywhere in tree or wave dir. The branch is moot now (seal = HELD), but
   it was genuinely available and honestly pre-accepted. **Confirmed.**

## 2. Evidence

### 2.1 Baseline + custody

```text
$ git rev-parse HEAD && git status --short
995e6a0799c4dad26942de15bd9058fe7acb676d
?? .ufo/waves/arc2-loop1-round7/
$ # command A verbatim from SCORECARD.md:92-123, REV=HEAD:
{"citation_resolved_rules": 11, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 80, "mapped": 80, "missing": [],
 "revision": "995e6a0799c4dad26942de15bd9058fe7acb676d", "rule_blocks": 11}
$ sha256sum <the five custody paths>
16f496e6…  devin/mcp_config.json     38d2a1d0…  omp/agent/mcp.json
e0634d8c…  kimi-code/config.toml     7d2ca28a…  .bashrc
6c6be761…  .profile   — all five byte-identical to
.ufo/waves/arc2-loop1-round7/receipts/config-pre-pair.txt:2-6 (5/5, read-only)
```

Pre-pair stamp `2026-10-18T21:40:26Z` == service start second
(`ExecMainStartTimestamp=Sun 2026-10-18 18:40:26 -03`): custody-before-launch
sequencing held.

### 2.2 The seal (journal + envelope, direct reads; not via E2)

```text
$ journalctl --user -u arc2-r7-pe.service --no-pager -o short-iso
2026-10-18T18:40:26-03 systemd[1539]: Started [systemd-run] … npx -y
  rea-agents@6.5.0 analyze …/windows_release_arm64.exe.
2026-10-18T19:04:11-03 arc2-r7-pe.service: Consumed 42min 35.706s CPU time
  over 23min 44.663s wall clock time, 7.9G memory peak, 53.1M memory swap peak.
# no oom-kill, no Stopping/Killing, no failure line
$ stat -c '%s %y' /var/tmp/arc2-l7r7-pe/std*json /var/tmp/arc2-l7r7-pe/stderr.log
5204  2026-10-18 19:04:11.350258132 -0300   stdout.json
0     2026-10-18 18:40:…                    stderr.log
$ sha256sum /var/tmp/arc2-l7r7-pe/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a
$ grep -o 'ev_[a-f0-9]*' stdout.json | head -1        # count: 1 occurrence
ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
$ grep -o 'analyzer_preset: "[^,]*' stdout.json
analyzer_preset: "ghidra-default+disabled:Call Convention ID …
$ grep -c 'provider_timeout\|execution_failure' stdout.json
0
$ # envelope also carries: subject.digest.sha256 7a2ccd68… (the 91.6MB target),
$ # segment_count: 9, procedure_count: 75218, string_count: 137345, 90 lines
$ systemctl --user show arc2-r7-pe.service -p LoadState -p Result -p OOMKills
LoadState=not-found
Result=success
OOMKills=18446744073709551615   # uint64 max = property unset (post-unload
# residue) — NOT an OOM count; do not cite (E2.md:63-64 concurs)
```

Corroboration of E2's seal reading (`E2.md:147,:172`): id and sha256 match my
direct reads exactly. Precision note: this envelope has **no explicit success
`code:` field** (my `grep -nE 'code|success|completed|exit'` matches only
`pcode`/`decoded-return` body text). The HELD is certified by `evidence_id`
presence (Z1 §5d gate), zero failure-class strings, the clean journal
deactivation, and 0-byte stderr — not by an envelope literal. If the parent
writes "envelope `code: completed`" into records, it cites a field that is
not there; cite the four evidence classes instead.

### 2.3 No pre-written HELD (mtime timeline, `stat -c '%y %n'`)

```text
19:04:11.350  /var/tmp/arc2-l7r7-pe/stdout.json          <- the seal
-- pre-seal seat writes (assert no outcome) --
18:52:13 V1.md   18:53:35 SC1.md   18:57:34 E1.md   19:00:37 R3.md
19:03:37 R1.md   19:03:39 CR1.md
-- post-seal seat writes --
19:04:56 R2.md   19:06:09 P2.md   19:10:12 E3.md   19:10:34 E5.md
19:11:51 E2.md
```

Grep for `HELD|held|oom|OOM|evidence_id|execution_failure|provider_timeout`
across `.ufo/waves/arc2-loop1-round7/` hits only `E2.md` and `E5.md`.
`E5.md:24-25`: "Run state at last sample: **in-flight, not sealed — nothing
here asserts a terminal state**" (its samples were 21:57Z/22:02Z =
18:57/19:02 -03; it filed post-seal without claiming the outcome). No
knowledge entry, no map token, no verdict cell existed pre-seal anywhere
(tree clean; wave dir held only `receipts/` at 18:47).

### 2.4 The adjudicated causal record the C2 wording contradicts

- `CR14.md:3` — "ATTACK SUSTAINED. Do not land the dispatched lesson" (the
  caller-independent-services slogan); `CR14.md:36` — "No 'Stopping scope' /
  session-teardown line. … E53's 'scope teardown' premise is not in that
  journal."
- `CR14.md:62-64` — r6's exit was the analyzer-name abort class, "not a
  lifetime event"; unknown: "whether killing the caller on this host stops a
  scope and spares a service (not run)". `CR14.md:75` — "Unit type is an
  untested lifetime hypothesis"; dropping the measured `MemoryMax` containment
  reopens the bystander-OOM class round 3 measured.
- `E52.md:19-21` — "Do not land 'round 4's scope died with its launcher' or
  'the `--scope` lifetime trap killed the 91.6MB PE run.'"
- `E52.md:111-112` — "**Unknown.** This seat did not kill a caller to test
  survival. Do not upgrade the man-page mechanism to 'proven on this host by
  a kill test.'"
- The compliant forms already exist: E52 §3.1 (arc-anchored lesson draft,
  causal story refused) and E52 §3.2 (token-free SCORECARD sentence: "The
  round-4 contained PE leg died by its own memory cap while its launcher was
  still alive — do not record that death as a caller teardown… service mode
  is not a held analysis").
- Bar: `corpus/QUALITY.md:13` — "Domain-specific — no generic agent advice"
  (verified verbatim this session). An absolute "never --scope" would also
  contradict E52's own rule 1, which is conditional ("Long run, short
  dispatcher") and keeps the scope+`MemoryMax` recipe for contained runs.

### 2.5 Command A's citation contract (why "12/12 resolvable" is not free)

```python
# SCORECARD.md:105  (command A, verbatim)
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
# :108-109  per rule:
refs = re.findall(pattern, rule); valid = bool(refs)
# :110-116  each ref must exist and 1 <= start <= end <= line-count
```

`corpus/lessons/2026-10-18-caller-independent-services.md` never matches the
pattern → a rule #12 citing only it is **unresolved**, command A reads 11/12,
depth drops to 9.17 — a regression the claims block does not announce. Both
C1 branches offer a resolvable target: the r6 mid-rung ladder line
`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:19` (21-line file,
verified) resolves today; an r7 HELD entry resolves only after C1 lands.
The 12/12 claim must name its citation source and its measurement order.

### 2.6 Stale-pointer arithmetic at HEAD

```text
corpus/README.md current: :165 counting-lesson row; :166 admission-correction
row (table ends here); :168 "## Frontier"; :173 ">90MB PE scale — …hits the
~900s internal session deadline; raise REA_GHIDRA_STARTUP_TIMEOUT_MS≈3.6M +
GHIDRA_HEADLESS_MAXMEM=6-8G, or bisect 2-5MB."; :178 the "held, not
frontier" Runtime-obs bullet.
SCORECARD.md:69 reads "`corpus/README.md:178`" — TRUE at HEAD.
E52.md:181-186 ("table ends at :165", ":166 blank", ":167 Frontier", ":177
bullet") — one r6-insert stale; true at 54bc9dd, false at 995e6a0.
```

Any round-7 lessons-table insert (C3's caller-independent-services row)
shifts every line ≥167 by +1 → the SCORECARD-cited bullet moves to **179**
and `SCORECARD.md:69` must be re-pointed `178`→`179` in the same commit. The
HELD map-token append (`:22`, same physical line) and the `:173` same-line
rewording add no shift.

### 2.7 Pin-free discipline for the round-7 records section

`c1-census-v10.py:86-108`: SCORECARD declared SCOPE rows end at
`768, 854` (arc2-loop1-round3). Rounds 4–7 sections are undeclared territory;
a `rea-agents@X.Y.Z` or bare `X.Y.Z` literal there measured `undeclared=1`
FAIL (`Z1.md:82`). The r6 section landed pin-free and census PASS at
`b910a33` — the working form. Do not restate the ExecStart package pin.

## 3. Verbatim-landable (parent lands; this seat does not edit corpus)

### 3.1 Rule #12 — corrected form (E52-adjudicated; command-A-resolvable)

```markdown
- **A long analyze that must outlive its dispatcher runs as a named transient
  user service with its memory caps, not a caller-blocking scope — and unit
  type is form, not result.** The round-4 scope leg died by its own memcg cap
  while its launcher was still alive (no `Stopping`/`Killing` line; the
  launcher's `exit.txt` landed in that same second), and the round-6 service
  exited on its own main process in 7.554 s under an untouched 9G cap:
  neither death is a caller teardown, neither is a held analysis, and service
  mode raises no cap and validates no analyzer name
  (`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:19`). Keep
  `MemoryMax`/`MemorySwapMax` and a disk `TMPDIR` in either unit form; record
  effective `KillUserProcesses` and `Linger` with the recipe; survival past
  an actual caller kill is untested on this host — do not write "proven".
```

Citation resolves in both C1 branches. Reject any wording containing
"r4 teardown", "died with its launcher", "r6 holds", or an absolute
"never --scope". Full account lives in the C3 lesson file (E52 §3.1 form);
the knowledge citation above is what makes command A read 12/12.

### 3.2 C3 re-point (same commit as the lessons-table insert)

```markdown
  frontier bullet now reads "held, not frontier" (`corpus/README.md:179`;
```

i.e. `SCORECARD.md:69` `178`→`179`. Recompute if any other line is inserted
above `## Frontier` in the same commit.

### 3.3 HELD-branch completions (beyond "knowledge entry + map token")

```markdown
- Frontier bullet `corpus/README.md:173`, same-line rewording, no line shift:
  `- >90MB PE scale — held, not frontier: 91.6MB Godot ARM64 completed in
  23m44.7s wall at 6G heap under a 9G cap with the three heavy decompile
  analyzers disabled and the 7200s deadline unused; the earlier boundary was
  the 900s session deadline at 2G default heap
  (corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md).`
- Map token: append the new stem to the existing `## Coverage map` row at
  `corpus/README.md:22` on that same physical line (Z1 §5d form, no new row);
  the row's historical "dies at the ~900s" gist stays as history; the new
  knowledge entry carries the supersession and states the hold is MITIGATED
  (`analyzer_preset: "ghidra-default+disabled:…"`, vs the r6 mid-rung's plain
  `ghidra-default` natural hold, `SCORECARD.md:1046-1048`).
- Certify the HELD by evidence class, not by an envelope `code:` field: this
  envelope carries `evidence_id ev_a4aa9b0d…de608`, zero failure-class
  strings, journal deactivation with no failure line, and 0-byte stderr — it
  has no success-side `code:` literal.
```

### 3.4 Records hygiene (pin-free + measurement order)

```markdown
The round-7 SCORECARD section is undeclared census territory (SCOPE ends at
`SCORECARD.md:854`, `c1-census-v10.py:86-108`): no `rea-agents@X.Y.Z`, no
bare `X.Y.Z`, no `config.toml:N` in the new section unless SCOPE is re-keyed
in the same commit (unmeasured; the pin-free append is the measured-green
form, `Z1.md:82`). Landing order: land C1's knowledge entry before any
command-A run expected to read 81/81 and 12/12 — C2's 12/12 is not
measurable until its rule's `corpus/knowledge` citation target exists.
```

## 4. Labels

**Observations:** HEAD `995e6a0…`, clean tree except the untracked wave dir;
custody 5/5 byte-identical (read-only re-hash), pre-pair stamp == launch
second; pre-seal unit active/running (started 18:40:26 -03,
`MemoryMax=9663676416`, peak 7.77G→8.0G of 9G, `OOMKills=0`, stdout 0 bytes)
under validated analyzer names, 7200000 ms deadline, 6G heap, 9G cap + 1G
swap, disk `TMPDIR` (transient fragment read directly); journal: Started
18:40:26, `Consumed 42min 35.706s CPU … 23min 44.663s wall … 7.9G memory
peak` 19:04:11, no failure/OOM/Stopping line; envelope 5204 B sha256
`a77ebee8…`, `evidence_id` ×1 `ev_a4aa9b0d…`, `analyzer_preset
"ghidra-default+disabled:…"` (mitigated), zero failure-class strings, 9
segments / 75,218 procedures / 137,345 strings, no success `code:` field;
post-seal `LoadState=not-found`, `OOMKills=18446744073709551615` (unset —
do not cite); seat mtime timeline (§2.3) with terminal assertions only
post-seal; command A JSON 80/80 11/11 10.0/10.0 at HEAD; command A regex
`SCORECARD.md:105-117`; census SCOPE `c1-census-v10.py:86-108` ending at
`:854`; README lines `:165/:166/:168/:173/:178` and `SCORECARD.md:69`=178
(currently true).

**Inferences:** no verdict inflation — every terminal-state assertion
postdates the 19:04:11 seal and pre-seal seats assert none; the C2 claim's
parenthetical evidence ("r4 teardown, r6 holds") contradicts the adjudicated
record and would violate `corpus/QUALITY.md:13` if landed as dispatched;
"12/12 resolvable" is sequence-coupled to a resolvable `corpus/knowledge`
citation; the C3 re-point must be 178→179 (E52's 177→178 is one commit
stale); the HELD branch additionally requires the `:173` frontier rewording,
the `:22` same-line token, and the mitigated-hold statement; the C1 negative
branch was genuinely pre-accepted and stayed so through seal (now moot).

**Unknowns:** who unloaded/reset the unit post-seal (not this seat); the
parent's final rule-#12 wording, C3 sequencing, and knowledge-entry stem;
whether SCOPE is re-keyed (unmeasured); whether the sealing seats adopt the
"no envelope `code:` literal" certification phrasing; terminal-class naming
is now settled by the seal itself (HELD, mitigated) — no class was
manufactured pre-seal.
