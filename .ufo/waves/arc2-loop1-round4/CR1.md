# CR1 (critic) — attack on C1: is rule #11 over-broad?

Seat CR1, wave `arc2-loop1-round4`, 2026-10-18. Read-only on every repo and home
file; **the only repo write is this report**. No git mutation, no config edits,
no installs, no network. Scratch confined to `/tmp/arc2-l4r4-CR1/` (my
namespace). HEAD at my first batch: `158a96611f22afdfa723131f3ec27f39138020e8`;
the parent's commit `1692acbe48ce0eac3b7c87698be59d8a04f46a08` ("rule 11",
19:09:10Z) moved HEAD mid-session — I measured at both and report which is
which. The live 91.6 MB PE analyze was observed only as process presence; never
signalled, reniced, or touched. No battery leg, no MCP session, no REA probe.

## 1. Verdict

**PARTIALLY REFUTED — rule #11 as worded is over-broad, and the boundary is not
"operator-mutable" at all: it is the write-cadence of the *target* file, with a
second, separate sub-class the draft misses entirely.**

Three findings, each measured:

1. **The stated scope is wrong, and the seat line's own example class is empty.**
   `/usr/bin` targets are cited **by digest, never by line** — `git grep` over
   the whole repo finds **0** `/usr/...:NNN` tokens, while the jq digest
   `e8156675…` appears at 62 sites. Conversely, files that *are*
   operator-owned and operator-mutable **do** carry line citations that all
   resolve today and have not drifted: `~/.bashrc:23,:24,:58,:61,:63`,
   `~/.profile:4,:7-12`, `~/.config/devin/mcp_config.json:7`,
   `~/.omp/agent/mcp.json:8`. "Operator-mutable" therefore does not partition
   the citation class: it contains both the churner and members that have been
   stable across all four arc-2 rounds.
2. **The class that actually broke is "target rewritten in place", and there is
   a second class the draft does not name: "path replaced wholesale".** The
   `~/.npm/_npx/<hash>/…` caches cited at 11 repo sites are keyed by content
   hash and get garbage-collected: `9b9809298fe40d2c` (cited at
   `corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:42`) and
   `af752b90495482d7` (cited at 8 sites) **do not exist on disk at my read
   time**. No stanza key, no receipt and no line number survives that class —
   only a content anchor does. A rule that says "anchor by stanza key + receipt"
   is silent on it.
3. **A rule phrased as a blanket ban on "bare line numbers" also condemns the
   churn *record* itself.** Rule #11's own evidence sentence lists
   `:1284 -> :2938 -> :3225 -> :3296`, and the two corpus blocks it cites as the
   "durable repair form" (`mcp-registrations.md:93-101`,
   `r4-16-frontier-rescan.md:941-948`) are themselves dense with bare line
   numbers — 9 and 6 numeric tokens respectively. Those numbers are **data**
   (observed positions at instants), not pointers. A rule that forbids them
   forbids the lane's own drift evidence, and would force editing of records
   under the card's verbatim-preservation convention (`SCORECARD.md:16-17`).

**C1's core move survives the attack and I endorse it**: a citation into a file
whose writer inserts lines above the target is dead on arrival, and
`[mcp_servers.rea]` is the correct anchor for the Kimi pin. What must change is
the *scope clause* ("operator-mutable files") and the addition of the
wholesale-replacement class and the record-exemption.

**Measurability check (both directions).** C1's stated measurable — "rules
10→11, 11/11 resolvable, craft otherwise byte-identical" — is **achievable but
not automatic**: a rule #11 carrying no `corpus/knowledge/*.md` citation scores
`rule_blocks 11, citation_resolved_rules 10, depth_score 9.09` (§3.2). With a
resolving citation it scores `11/11, 10.0`. The draft text in E20 §4.1 and my
boundary-corrected replacement both measure `11/11, depth 10.0` (§3.4).

## 2. Pre-leg receipt check (required before my leg)

`.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt` — **5/5 OK, rc 0**,
checked twice: once at `158a966` and once after HEAD moved to `1692acb`.

```console
$ git rev-parse HEAD
1692acbe48ce0eac3b7c87698be59d8a04f46a08
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

The round-4 pre-pair stamp is `2026-10-18T19:03:02Z` (`:1`). My leg ran no REA
probe, so it wrote nothing to any custody path.

**Mid-session HEAD move — recorded, and it matters to C1.** Commit `1692acb`
("rule 11") touched `.ufo/waves/arc2-loop1-round4/E23.md`, `E4.md`,
`receipts/config-pre-pair.txt`, and a repo-root `e16-table.json` — and
**no `SKILL.md`**:

```console
$ git show --name-only --format='' 1692acb
.ufo/waves/arc2-loop1-round4/E23.md
.ufo/waves/arc2-loop1-round4/E4.md
.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
e16-table.json
$ git diff --name-only 158a966 1692acb -- SKILL.md | wc -l
0
$ git rev-parse 158a966:SKILL.md 1692acb:SKILL.md
800acec5ee4d61ea7861cd595e3eb2b0a8eceb1e
800acec5ee4d61ea7861cd595e3eb2b0a8eceb1e
$ git show 1692acb:SKILL.md | sed -n '/## Queue-drain craft/,/^## /p' | grep -c '^- \*\*'
10
```

**Observation.** The commit subject says "rule 11" but the craft section still
holds **10** rule blocks at that commit, and `SKILL.md` is byte-identical
between `158a966` and `1692acb`. C1's depth claim is **not yet landed**; the
commit is a mislabeled artifact landing (three seat reports + the pre-pair
receipt + a stray `e16-table.json`). The parent should either land the rule
under a corrected subject or amend the subject — as things stand, a reader of
`git log` would conclude rule #11 exists when it does not.

## 3. Evidence — commands run THIS session, with observed output

### 3.1 The seat line's example class is empty: `/usr/bin` is cited by digest, never by line

```console
$ git grep -nE '/usr/[A-Za-z0-9_./+@-]+:[0-9]+' -- . ':(exclude).ufo'
(no output)
$ git grep -cE '/usr/[a-z0-9.-]+:[0-9]' | wc -l
0
$ git grep -l 'e8156675' | wc -l
62
$ sha256sum /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
$ stat -c '%y %s' /usr/bin/jq
2026-06-20 14:10:39.000000000 -0300 30800
$ pacman -Qo /usr/bin/jq
/usr/bin/jq is owned by jq 1.8.2-1
```

**Observation.** There is not one line-number citation into `/usr/bin` anywhere
in the repo (including `.ufo`), and the jq binary — the lane's most-cited
native target — is cited by a digest that still matches the live bytes. The
seat line's hypothetical ("some operator files are stable — e.g. /usr/bin
binaries cited by line") names a case that **does not occur**; the *real*
stable-citation pattern is already digest-based, and it is stable for a reason
that is not ownership: a distro binary's path and bytes change only on a
package upgrade, and the digest is the pin.

### 3.2 Operator-owned files that are cited by line and have NOT drifted

```console
$ for n in 23 24 58 61 63; do b=$(sed -n "${n}p" ~/.bashrc.bak.1792084648); \
    l=$(sed -n "${n}p" ~/.bashrc); [ "$b" = "$l" ] && echo ":$n IDENTICAL" || echo ":$n CHANGED"; done
:23 IDENTICAL
:24 IDENTICAL
:58 IDENTICAL
:61 IDENTICAL
:63 IDENTICAL
$ diff ~/.bashrc.bak.1792084648 ~/.bashrc
73a74,79
> 
> 
> # >>> grok installer >>>
> export PATH="$HOME/.grok/bin:$PATH"
> [[ -r "$HOME/.grok/completions/bash/grok.bash" ]] && source "$HOME/.grok/completions/bash/grok.bash"
> # <<< grok installer <<<
$ wc -l ~/.bashrc.bak.1792084648 ~/.bashrc
  73 /home/vgpnk/.bashrc.bak.1792084648
  79 /home/vgpnk/.bashrc
$ date -u -d @1792084648
Thu Oct 15 05:17:28 PM UTC 2026
```

Every cited `~/.bashrc` line resolves identically today and in the 2026-10-15
snapshot, despite the file having been written since (Oct-16 mtime). The one
write was an **EOF-only append** — which is exactly the shape under which line
citations are safe. And the `.profile` side is frozen outright:

```console
$ stat -c '%y %n' ~/.profile ~/.bashrc
2026-10-15 03:12:07.440808802 -0300 /home/vgpnk/.profile
2026-10-16 13:33:16.272618342 -0300 /home/vgpnk/.bashrc
$ for n in 4 7 8 9 10 11 12; do printf ':%s [%s]\n' "$n" "$(sed -n "${n}p" ~/.profile)"; done
:4 [export JAVA_HOME=/usr/lib/jvm/java-21-openjdk]
:7 [export REA_PWNTOOLS_PYTHON="$HOME/.local/share/kaidoku-pwnenv/bin/python"]
:8 [export REA_BINWALK_COMMAND=/usr/bin/binwalk]
:9 [export REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob"]
:10 [export REA_APKTOOL_COMMAND=/usr/bin/apktool]
:11 [export REA_ADB_PATH=/usr/bin/adb]
:12 [export REA_JADX_MCP_JAR="$HOME/.local/opt/jadx-headless-mcp/jadx-headless-mcp-0.7.1-all.jar"]
```

The registration pins are likewise line-stable across all four arc-2 rounds:

```console
$ for r in 1 2 3 4; do f=.ufo/waves/arc2-loop1-round$r/receipts/config-pre-pair.txt; \
    printf 'r%s %s ' "$r" "$(head -1 $f)"; for n in 2 3 4 5 6; do \
    sed -n "${n}p" "$f" 2>/dev/null | cut -c1-8 | tr '\n' ' '; done; echo; done
r1 2026-10-18T14:49:13Z 16f496e6 38d2a1d0 3546e033
r2 2026-10-18T16:57:35Z 16f496e6 38d2a1d0 3546e033 7d2ca28a 6c6be761
r3 2026-10-18T17:55:49Z 16f496e6 38d2a1d0 bd5a78d1 7d2ca28a 6c6be761
r4 2026-10-18T19:03:02Z 16f496e6 38d2a1d0 bd5a78d1 7d2ca28a 6c6be761
$ sed -n '7p' ~/.config/devin/mcp_config.json | grep -c '6.5.0'   → 1
$ sed -n '8p' ~/.omp/agent/mcp.json | grep -c '6.5.0'             → 1
```

**Observation.** Across four rounds spanning 4h14m, exactly **one** of the five
custody paths changed (`config.toml`: `3546e033…` → `bd5a78d1…`); devin, omp,
`.bashrc` and `.profile` are byte-identical in all four receipts, and their
cited line numbers resolve. **The churner is a single file, not a class.** A
rule scoped to "operator-mutable files" therefore imposes the content-anchor
discipline on 27 `.bashrc` sites, 7 `.profile` sites, 5 devin sites and 5 omp
sites that have never drifted — which is cost without a defect.

### 3.3 The two classes that DO break — both measured today

**(a) Target rewritten in place.** The config stanza, from the operator's own
backups plus the live file (my run):

```console
$ for b in ~/.kimi-code/config.toml.20261018-*.bak ~/.kimi-code/config.toml; do \
    printf '%-52s lines=%-5s stanza=%s\n' "$(basename $b)" "$(wc -l < $b)" \
    "$(grep -n '^\[mcp_servers\.rea\]$' $b | cut -d: -f1)"; done
config.toml.20261018-085645.bak                      lines=2939  stanza=2913
config.toml.20261018-114557.bak                      lines=2956  stanza=2930
config.toml.20261018-143236.bak                      lines=2964  stanza=2938
config.toml.20261018-145016.bak                      lines=3251  stanza=3225
config.toml.20261018-150133.bak                      lines=3322  stanza=3296
config.toml                                          lines=3322  stanza=3296
$ printf 'config.toml:1478 now: '; sed -n '1478p' ~/.kimi-code/config.toml
config.toml:1478 now: max_output_size = 131072
$ printf 'config.toml:1287 now: '; sed -n '1287p' ~/.kimi-code/config.toml
config.toml:1287 now: [models."opencode-go-3/grok-4.7"]
$ printf 'config.toml:2940 now: '; sed -n '2940p' ~/.kimi-code/config.toml
config.toml:2940 now: capabilities = [ "thinking", "tool_use" ]
```

Six positions in one day; every historical pointer is content-dead. This is the
class rule #11 correctly targets.

The same in-place class hits a **non-operator, tool-owned** file, which matters
for scoping:

```console
$ sed -n '48p' ~/.agents/skills/reverse-engineer-anything/SKILL.md
   that provider: static JavaScript inspection needs neither Hopper nor Ghidra,
$ sed -n '48p' ~/.agents/skills/reverse-engineer-anything/SKILL.md.rea.backup
- ASAR or extracted JavaScript/Electron tree:
$ grep -n 'ASAR or extracted JavaScript/Electron tree' ~/.agents/skills/reverse-engineer-anything/SKILL.md
91:- ASAR or extracted JavaScript/Electron tree:
$ wc -l ~/.agents/skills/reverse-engineer-anything/SKILL.md.rea.backup \
        ~/.agents/skills/reverse-engineer-anything/SKILL.md
  221 .../SKILL.md.rea.backup
  342 .../SKILL.md
```

`corpus/knowledge/2026-10-13-asar-surface.md:57` cites
`~/.agents/skills/reverse-engineer-anything/SKILL.md:48` for the routing
statement; at my read time the statement is at `:91` and `:48` holds unrelated
text. The REA skill file is written by the **REA package installer**, not the
operator — so "operator-mutable" under-includes the class. The invariant is
*whether the writer inserts above the target*, not who the writer is.

**(b) Path replaced wholesale — the class the draft does not name.**

```console
$ for c in 9b9809298fe40d2c af752b90495482d7 dea9475797100b20 a1722018f28f9df2 ad9a3fdbcad992c6; do \
    printf '%-18s %s\n' "$c" "$([ -d ~/.npm/_npx/$c ] && echo EXISTS || echo GONE)"; done
9b9809298fe40d2c   GONE
af752b90495482d7   GONE
dea9475797100b20   EXISTS
a1722018f28f9df2   EXISTS
ad9a3fdbcad992c6   EXISTS
$ ls -ldt ~/.npm/_npx/*/
a1722018f28f9df2 (Oct 18 16:05)  ad9a3fdbcad992c6 (16:03)  dea9475797100b20 (14:42)
c8ab89660c602c20 (Oct 16 23:52)  ceb651102292ad92 (19:06)   94207acffe67148d (13:34)
```

Both vanished caches are **cited in the repo**:

```console
$ git grep -ohE '_npx/[0-9a-f]{16}' -- . ':(exclude).ufo' | sed 's|_npx/||' \
    | sort | uniq -c | while read n h; do printf '%2s sites  %s  %s\n' "$n" "$h" \
    "$([ -d ~/.npm/_npx/$h ] && echo EXISTS || echo GONE)"; done
 3 sites  9b9809298fe40d2c  GONE
 1 sites  a1722018f28f9df2  EXISTS
 1 sites  ad9a3fdbcad992c6  EXISTS
 8 sites  af752b90495482d7  GONE
13 sites  dea9475797100b20  EXISTS
```

11 cited sites point into caches that no longer exist — including the
`source:` line of a corpus entry:

```console
$ sed -n '40,44p' corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md
- source:
  `~/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/dist/javascript/recovery/WakaruCommand.js:43,60-79`
  (limiter resolution + spawn args + env),
```

The cache directory is content-addressed by npm and garbage-collected on cache
eviction. **Neither a stanza key nor a receipt can rescue this class** — the
whole path is gone. The only durable anchor is content (the file's own text or
digest), which the draft's "anchor by stanza key + receipt" does not cover.
Note the surviving `dea9475797100b20` cache *does* still carry the cited file
and its line 43 — so this class fails by whole-path deletion, not by drift.

### 3.4 The measurable: rule #11 must carry a corpus citation, or depth drops

Command A (the verbatim recipe at `SCORECARD.md:92-123`) run in a throwaway
mini-repo (`/tmp/arc2-l4r4-CR1/mini`, built from `git archive 158a966` of
`corpus/knowledge`, `corpus/README.md`, `SKILL.md`), baseline first:

```console
$ python3 runA.py        # baseline, 10 rules
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [],
 "rule_blocks": 10, "revision": "c08f5db41de3b5e4a200a043c6f124885a839fbb"}

$ python3 runA.py        # variant A: rule #11 with NO corpus/knowledge citation
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [],
 "depth_score": 9.09, "knowledge_files": 79, "mapped": 79, "missing": [],
 "rule_blocks": 11}

$ python3 runA.py        # variant B: rule #11 WITH one resolving corpus citation
{"citation_resolved_rules": 11, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [],
 "rule_blocks": 11}
```

**Observation.** A rule #11 written as pure prose about external files — no
`corpus/knowledge/*.md` reference — is **unresolvable** by command A's regex and
lowers the headline proxy from 10.0 to **9.09**. C1's measurable ("rules 10→11,
11/11 resolvable") is achievable **only if the rule cites at least one corpus
entry inside its 1..N line bounds**. Both E20's §4.1 draft and my replacement do;
a naive draft of the same rule does not. This is a real trap for the landing,
not a formality.

### 3.5 E20's §4.1 draft text — tested verbatim, resolves 11/11

The draft text (read this session at `.ufo/waves/arc2-loop1-round4/E20.md:371-386`),
committed verbatim into my mini-repo:

```console
--- E20 draft §4.1 VERBATIM ---
rule 10: RESOLVED :: ['2026-10-16-l8-01-6p4-symmetry-battery.md:15-15 n=17 ok']
rule 11: RESOLVED :: ['2026-10-13-mcp-registrations.md:93-101 n=111 ok',
                      '2026-10-13-r4-16-frontier-rescan.md:941-948 n=975 ok']
{"citation_resolved_rules": 11, "coverage_score": 10.0, "depth_score": 10.0,
 "rule_blocks": 11}
```

Both cited blocks exist and contain the referenced content (verified by
`sed -n '93,101p'` and `sed -n '941,948p'`). **The draft's citation targets are
sound.** My attack is on its *scope clause*, not its citations.

### 3.6 The "durable repair form" the draft cites is itself full of bare line numbers

```console
$ sed -n '93,101p' corpus/knowledge/2026-10-13-mcp-registrations.md \
    | grep -oE 'config\.toml[: ]*[0-9]+(-[0-9]+)?|:[0-9]{4}(-[0-9]{4})?' | sort | uniq -c
      1 :1284
      1 :2938
      2 :3225
      2 :3296
      1 :3298
      1 :3299
      1 :3301
      1 config.toml:3296-3303
$ sed -n '941,948p' corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md \
    | grep -oE 'config\.toml[: ]*[0-9]+(-[0-9]+)?|:[0-9]{4}' | sort | uniq -c
      1 :2913
      1 :2930
      1 :2938
      1 :3225
      1 :3296
      1 config.toml:1284-1292
$ git grep -nE 'config\.toml[:` ]*[0-9]+' -- . ':(exclude).ufo' | wc -l
11
```

**Observation.** The very blocks rule #11 names as the durable repair form hold
15 bare numeric tokens, and 11 repo sites carry bare `config.toml:NNN` tokens.
Two readings are possible and the rule must pick one:

- **Pointer reading** (what the draft implies): those numbers are dead pointers
  and should be content-anchored. But they are *records of observed positions at
  instants* — the round-3 errata deliberately keep them as the drift history
  ("`:1284→:2938→:3225→:3296`, so any line number into it drifts"). Deleting or
  rewriting them destroys the evidence that motivates the rule.
- **Record reading** (what I recommend): a churn record that *lists* observed
  numbers is a datum, not a pointer, and must be left verbatim. The rule should
  say so explicitly, or a future seat will "repair" the history.

Under the card's own convention (`SCORECARD.md:16-17`: "Line citations to
pre-existing lane files refer to the baseline revision unless explicitly marked
current"), rewriting historical numbers would be a convention violation in
addition to evidence destruction.

### 3.7 The card's baseline convention covers in-repo files, not external ones

```console
$ sed -n '16,17p' SCORECARD.md
Line citations to pre-existing lane files refer to the baseline revision unless
explicitly marked current; the added lesson-index row shifts later README lines.
$ sed -n '270p' SCORECARD.md
`:157` pointer (at `:160` in HEAD, per seat C7) is recorded as named debt,
```

**Observation.** The convention is explicitly scoped to *lane files*
(baseline-revision reading). It gives no cover to external-file citations, and
none to the churn records. So rule #11 is **not** redundant with the card
convention — it addresses a genuinely uncovered class — but its scope must be
written so that it does not collide with the convention on lane files. A rule
phrased "never bare line numbers" would collide.

## 4. The boundary, stated precisely

**A line-number citation is safe if and only if the citing file's target
location is write-stable in the direction that matters — i.e. the writer of the
target file does not insert or delete lines at or above the cited line.** Three
sub-classes, with the measured discriminator for each:

| Sub-class | Measured discriminator | Anchor that survives | Examples (measured this session) |
|---|---|---|---|
| **Insert-stable** — writer appends only, or path/bytes are frozen | cited line resolves in two snapshots ≥1 write apart; or target is digest-pinned | line number **is** safe; keep it | `~/.bashrc:23,:24,:58,:61,:63` (identical in Oct-15 bak and live, one EOF-only append); `~/.profile:4,:7-12` (no write since Oct-15); `~/.config/devin/mcp_config.json:7`, `~/.omp/agent/mcp.json:8` (byte-identical across 4 receipts); `/usr/bin` targets (cited by digest, `e8156675…`) |
| **In-place rewrite** — writer inserts/deletes above the target | target's line moves across snapshots | **section key** (`[mcp_servers.rea]`) + round receipt fixing the instant | `~/.kimi-code/config.toml` (stanza `:2913→:2930→:2938→:3225→:3296` in one day); `~/.agents/skills/reverse-engineer-anything/SKILL.md` (installer-written: cited `:48` now holds unrelated text, statement at `:91`) |
| **Wholesale replacement** — the path itself is replaced/deleted | `test -e` on the cited path fails at a later read | **content only** (quote the text, or cite a digest of the file) — no key or line survives | `~/.npm/_npx/9b9809298fe40d2c/…` (cited `r4u-05:42`) and `~/.npm/_npx/af752b90495482d7/…` (cited at 8 sites) — both GONE |

**Ownership is not the discriminator** (operator-owned `.bashrc`/`.profile` are
insert-stable; tool-installer-owned REA skill is in-place-rewrite). **Repo
boundary is not the discriminator** either (lane files get the card's baseline
convention, external files get this rule). **The discriminator is write-cadence
of the target**, and it is *observable* — every row above was decided by running
`diff`/`test -e`/`grep -n` against two snapshots, not by reasoning about who
owns the file.

**The rule must also carry a record-exemption**: a line that *records* observed
positions at an instant (`:1284→…→:3296`, the round-3 errata lists) is data and
stays verbatim. Otherwise the rule eats its own evidence.

## 5. Text the parent should land VERBATIM (fenced)

I recommend this replacement for E20 §4.1. It is tested: committed into the
mini-repo it yields `rule_blocks 11, citation_resolved_rules 11, depth_score
10.0` (§3.4). Land it **after `SKILL.md:206`** (the line
`  is not a same-round zero-drift observation.`), before `## Config custody` at
`:208` — the anchor E20 already specifies.

```markdown
- **Line-number citations survive only where the writer cannot insert above
  them.** A line number into a file that is rewritten in place dies the
  moment its writer inserts above it — the Kimi rea stanza walked
  `config.toml:1284 -> :2938 -> :3225 -> :3296` in one day
  (`corpus/knowledge/2026-10-13-mcp-registrations.md:93-101`) — so cite the
  stanza key (`[mcp_servers.rea]`) plus the receipt that fixes the instant,
  never a bare number. Ownership is not the test: operator-owned `.bashrc`
  and `.profile` lines stayed put from their 2026-10-15 snapshot through an
  EOF-only append (`~/.bashrc:23-63`), `~/.config/devin/mcp_config.json:7`
  and `~/.omp/agent/mcp.json:8` are byte-stable across four rounds, and
  `/usr/bin` targets are cited by digest (`e8156675…`), not by line. The
  third case is a path that can be replaced wholesale, where neither key nor
  line survives: the `~/.npm/_npx/<hash>/…` caches cited at
  `corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:42` are
  garbage-collected, so anchor those by content. A churn record that lists
  observed numbers is a datum, not a pointer — leave it verbatim. The
  durable repair form and its limits are recorded at
  `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:941-948`.
```

Tested text sha256 (my run, `/tmp/arc2-l4r4-CR1/rule11-final.txt`, 1267 B):
`eee87b88ac8d1a313660fcb92c398a7ce6502a769dda88b4476daeff1cb5dd1e`.

If the parent prefers to keep E20's §4.1 text unchanged (it also measures
`11/11, depth 10.0`), the **minimum** correction is to soften the scope clause
from "operator-mutable files" to "files rewritten in place" and to add one
sentence exempting churn records. Everything else in the draft stands.

## 6. Conclusions, labeled

- **OBSERVATION** — `/usr/bin` targets carry **0** line-number citations in this
  repo (including `.ufo`); jq is cited by digest `e8156675…` at 62 sites and the
  digest matches live bytes (§3.1). The seat line's example class is empty.
- **OBSERVATION** — `~/.bashrc:23,:24,:58,:61,:63` and `~/.profile:4,:7-12`
  resolve identically in the 2026-10-15 backup and the live file; `.bashrc`'s
  only intervening write was an EOF-only 6-line append; `.profile` has no write
  since Oct-15. devin/omp pin lines are byte-stable across all four arc-2
  receipts (§3.2). "Operator-mutable" therefore does not partition the class.
- **OBSERVATION** — the `[mcp_servers.rea]` stanza occupied six line numbers in
  one day (`:2913, :2930, :2938, :3225, :3296` across five `.bak` files plus the
  live file); `:1478`, `:1287`, `:2940` all hold unrelated content now (§3.3a).
- **OBSERVATION** — `corpus/knowledge/2026-10-13-asar-surface.md:57` cites
  `~/.agents/skills/reverse-engineer-anything/SKILL.md:48`, which now holds
  unrelated text; the cited statement is at `:91`. That file is written by the
  REA installer, not the operator (§3.3a). A tool-owned file shows the same
  drift, so the class is not owner-defined.
- **OBSERVATION** — two cited npx caches (`9b9809298fe40d2c` at 3 sites,
  `af752b90495482d7` at 8 sites) no longer exist on disk; the surviving
  `dea9475797100b20` still carries its cited file at the cited line (§3.3b).
- **OBSERVATION** — a rule #11 without a corpus citation scores
  `rule_blocks 11, citation_resolved_rules 10, depth_score 9.09`; with one it
  scores `11/11, 10.0` (§3.4).
- **OBSERVATION** — E20's §4.1 draft text measures `11/11, depth 10.0` verbatim,
  and its two cited blocks exist with the referenced content (§3.5).
- **OBSERVATION** — commit `1692acb` ("rule 11") contains no `SKILL.md` change;
  craft holds 10 rules at that commit and at `158a966` (§2).
- **INFERENCE** — the rule's correct scope is write-cadence of the target, in
  three sub-classes (insert-stable / in-place-rewrite /
  wholesale-replacement), with a churn-record exemption. This is what my §5
  text encodes and it is what makes the rule correct without over-reaching.
- **INFERENCE** — the existing digest-citation practice for `/usr/bin` is the
  lane's own precedent for the wholesale-replacement class; the rule should
  generalize it rather than invent a new form.
- **UNKNOWN** — whether the two vanished caches were evicted by npm's cache GC,
  by an operator `npm cache clean`, or by disk pressure; I did not observe the
  deletion. The class is demonstrated (path absent, citations present); the
  mechanism is not.
- **UNKNOWN** — whether the parent intends `1692acb`'s subject to be corrected;
  I do not edit. Flagged in §2.
- **UNKNOWN** — whether any citation into `~/.npm/_npx/…` targets a cache that
  still exists at a *different* hash (the same file under a new cache key). I
  checked existence only; I did not search the surviving caches for the cited
  file contents.

## 7. Scope compliance

- Only repo write: this file. No git mutation by me; the `1692acb` commit is the
  parent's.
- No config edits, no installs, no network fetches, no REA probe, no MCP session.
- The live PE analyze was observed only through `ps`/`git log` output quoted from
  sibling reports; I never signalled, reniced, or touched it.
- All five custody paths were read as digests only; config contents were read
  only at the landmark lines already published in the repo, and no token, key or
  secret value appears in this report.
- Scratch confined to `/tmp/arc2-l4r4-CR1/` (mini-repo, `runA.py`, `classify.py`,
  `rule11-final.txt`). A `git clone` attempt into `/tmp` failed on tmpfs quota
  (80% full, 3.1 GiB free) and was abandoned in favour of the `git archive`
  mini-repo; the partial clone directory was removed.
