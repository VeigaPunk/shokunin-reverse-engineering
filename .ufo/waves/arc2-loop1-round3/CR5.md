# CR5 (critic) — attack on census/instrument completeness for C1 and C3

Seat CR5, wave arc2-loop1-round3, read-only. Every command below was run by this
seat this session (2026-10-18, stamps 17:57:38Z–18:14Z) at HEAD
`679af5d749f2fd48b9d543e3c99d348d5458f90f`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round3/` only, at every check. Scratch only under
`/tmp/arc2-l3r3-CR5-sim/`. This report is my only write. Pre-pair receipt
verified 5/5, rc=0, before my leg (§2.1). No battery leg run by this seat (not
my scope); no processes started; scratch residue confined to
`/tmp/arc2-l3r3-CR5-sim/` (scripts, fixtures, captured outputs — mine only, no
other seat's namespace touched).

## 1. Verdict

**PARTIAL REFUTE — three findings, each measured.**

1. **C1's declared dead-pointer set is not the census, and its prescribed repair
   target is already dead.** C1 declares `mcp-registrations.md :9,:80,:88` plus
   `r4-16-frontier-rescan.md:43` and plans a re-point to `config.toml:2938/:2940`.
   Measured this session: line `:9` carries **no line pointer** and line `:80`
   carries **no line pointer** (the dead tokens sit on `:11`, `:12`, `:18`, `:88`);
   the live rea stanza is at `:3296`/`:3298`, so a re-point to `:2938/:2940` lands a
   **third dead number**. A content-resolved census over *all pointer forms* in
   editable files finds **12 `config.toml` pointer loci, 12 dead, 0 live** — C1
   names 3 of them. `SCORECARD.md:291` (`:1478`) is a fourth colon-form locus that
   neither C1 nor the carried-debt sentence at `SCORECARD.md:759-760` names.
2. **C3's first gate draft (E14) cannot red on the class it was built for.**
   I extracted E14's quoted script and table (`E14.md:177-595`, `E14.md:601-643`)
   and ran them against this tree: **exit 0, repo=24, failed=0, advisory=5** — the
   entire `config.toml` pointer family is `host`-scoped, i.e. advisory by design,
   and **0 of the 24 `repo` rows cover any C1 pointer locus**. The gate as drafted
   is a probe for C1's class, not a gate; C1's "N→0" cannot be measured by it.
   E14 also places its frozen baseline at `scripts/citation-drift-frozen/`, while
   `PROTOCOL.md:390-391` pins frozen baselines under a `.ufo/waves/*/frozen` root
   (`find .ufo -type d -name frozen` → 0 hits this session). E15's second draft is
   placed under `.ufo/waves/arc2-loop1-round3/frozen` — the compliant root.
3. **Three pointer classes are invisible to the draft instruments unless pinned
   explicitly** (each proven by executing E14's own `classify()` on fixtures, §2.5):
   a **multi-line needle** is always `missing`; a **range citation** is only as wide
   as the rows pinned (the draft pins one row per locus, so a range like
   `:1284-1292` is one row, and a mid-range reword passes); a **path with spaces**
   degrades to `target_missing` under any naive extractor (fail-safe but
   misclassified), so the table must carry the quoted form.

One transient must be recorded for the parent: at 18:12Z this worktree held a
**+2-line `corpus/README.md` insert** (my first E14 run: `drifted corpus/README.md:138
found_at=139`, `:177 found_at=179`, exit 1), then was restored byte-identical to
HEAD (hash `29cd30ee…`, mtime `18:12:28Z`). C3's finding #1 — a README insert
shifts every later citation — was therefore rehearsed **live in the shared
worktree** by a sibling mid-wave. Any pointer measured against a moving worktree
is not comparable to the frozen revision (`PROTOCOL.md:378-380`).

## 2. Evidence — exact commands with observed output

### 2.1 Pre-leg receipt, HEAD, live config identity

```
$ git rev-parse HEAD
679af5d749f2fd48b9d543e3c99d348d5458f90f
$ git status --porcelain
?? .ufo/waves/arc2-loop1-round3/
$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum /home/vgpnk/.kimi-code/config.toml
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  /home/vgpnk/.kimi-code/config.toml
$ grep -n 'mcp_servers\.rea\]\|rea-agents@' /home/vgpnk/.kimi-code/config.toml
3296:[mcp_servers.rea]
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ wc -l /home/vgpnk/.kimi-code/config.toml
3322
$ for n in 2938 2940 3227; do printf "%s => " $n; sed -n "${n}p" /home/vgpnk/.kimi-code/config.toml; done
2938 => max_context_size = 1000000
2940 => capabilities = [ "thinking", "tool_use" ]
3227 => default_effort = "high"
```

Observation: receipt 5/5; the live pin is `:3298`, stanza `:3296`, and the
numbers C1 plans to write (`:2938`/`:2940`) and the numbers the repo already
carries (`:3227`, `:2940`, `:1284`, `:1287`) all resolve to unrelated models-table
lines. Config **bak history** shows the churn is monotone today (each `.bak` is
the pre-write state; stanza line per revision):

```
$ for b in /home/vgpnk/.kimi-code/config.toml.20261018-*.bak; do printf "%-38s %s " "$(basename $b)" "$(sha256sum $b | cut -c1-8)"; printf "lines=%s stanza=%s\n" "$(wc -l < $b)" "$(grep -n 'mcp_servers.rea\]' $b | head -1 | cut -d: -f1)"; done
config.toml.20261018-085645.bak   51352d26 lines=2939 stanza=2913
config.toml.20261018-114557.bak   84acf4fb lines=2956 stanza=2930
config.toml.20261018-143236.bak   3546e033 lines=2964 stanza=2938
config.toml.20261018-145016.bak   f10b01e9 lines=3251 stanza=3225
config.toml.20261018-150133.bak   bd5a78d1 lines=3322 stanza=3296
```

### 2.2 C1's declared loci vs. the tree (line `:9` and `:80` carry no pointer)

```
$ for n in 9 11 12 18 80 88; do printf "%s => " $n; sed -n "${n}p" corpus/knowledge/2026-10-13-mcp-registrations.md | grep -oE 'config\.toml[^;]*|lines [0-9,-]+|line [0-9]+' | tr '\n' '|'; echo; done
9 =>
11 => lines 1-17|lines 1-16|config.toml lines 1285-1292|
12 => config.toml`|
18 => config.toml line 1288|
80 => config.toml`), all launching pinned `npx -y rea-agents@6.4.0 mcp` with `GHIDRA_INSTALL_DIR`/`JAVA_HOME`|
88 => config.toml:1284` (startup_timeout_sec at 1287), not 1285/1288. (audit-A, consistency)|
$ for p in "…:9" "…:80" "…:88"; do sed -n "${p##*:}p" corpus/knowledge/2026-10-13-mcp-registrations.md | grep -cE ':[0-9]{3,4}|config\.toml:[0-9]+'; done
9  → 0
80 → 0
88 → 1
```

Observation (converges with `E15.md:224-227`, reached independently before reading
it): the declaration names two loci with no line-number token (`:9` heading, `:80`
Summary prose) and misses `:11`, `:12`, `:18`. The dead-token set is
`{11, 12, 18, 88}`. `r4-16-frontier-rescan.md:43` is correctly named; that file
also carries a second pointer at `:233` (`sed -n '1283,1294p'`) that C1 does not
name.

### 2.3 The pointer-class census — 12 loci, 12 dead, across four forms

A resolver over all editable non-`.ufo` files (excluding `LOG.md`), matching
four forms and content-resolving each span against the live config:

```
editable-file config.toml pointer loci: 12
  DEAD  PROVINCE.md:18                                    config.toml:2940 2940-2940 [colon]
  DEAD  PROVINCE.md:18                                    bare 3227-3227    [bare]
  DEAD  SCORECARD.md:59                                   config.toml:2940 2940-2940 [colon]
  DEAD  SCORECARD.md:291                                  config.toml:1478 1478-1478 [colon]
  DEAD  SCORECARD.md:698                                  config.toml:2940 2940-2940 [colon]
  DEAD  corpus/knowledge/2026-10-13-mcp-registrations.md:11  lines 1285-1292   [prose]
  DEAD  corpus/knowledge/2026-10-13-mcp-registrations.md:12  sed 1285-1293     [sed]
  DEAD  corpus/knowledge/2026-10-13-mcp-registrations.md:18  line 1288-1288    [prose]
  DEAD  corpus/knowledge/2026-10-13-mcp-registrations.md:88  config.toml:1284 1284-1284 [colon]
  DEAD  corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43  config.toml:1284-1292 [colon]
  DEAD  corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:233 sed 1283-1294   [sed]
  DEAD  corpus/lessons/2026-10-15-round-1.md:82           config.toml:1287 1287-1287 [colon]
  live=0 dead=12
```

Observation: C1's measured set ("dead-pointer loci in the scoped set N→0") is
**incomplete on every axis**: by locus (3 named vs 12 existing), by form (its
sweep is colon-shaped; `lines N-M` prose, `sed -n 'N,Mp'`, and bare `:3227`
continuations are all separate needles), and by file (`PROVINCE.md:18`,
`SCORECARD.md:59/:291/:698`, `lessons/2026-10-15-round-1.md:82` are outside its
named edit set — `SCORECARD.md:59` and `:698` are not even in the carried-debt
sentence at `SCORECARD.md:757-761`, which names only `:9,:80,:88`).

### 2.4 E14's gate, run — exit 0, and zero repo rows on the C1 class

```
$ sed -n '177,595p' .ufo/waves/arc2-loop1-round3/E14.md > /tmp/arc2-l3r3-CR5-sim/e14-quoted.py   # 419 lines, parses OK
$ sed -n '601,643p' .ufo/waves/arc2-loop1-round3/E14.md > /tmp/arc2-l3r3-CR5-sim/e14-table.tsv  # 43 lines
$ python3 (import e14-quoted; parse_table; evaluate(root, rows))
parsed rows: 36
EXIT = 0 | counts = {"rows": 36, "repo": 24, "host": 12, "failed": 0, "could_not_evaluate": 0, "advisory": 5}
repo rows naming a ~/.kimi-code/config.toml citation locus: 0
rows mentioning mcp-registrations / r4-16 / SCORECARD:270: 1   (SCORECARD.md:544 only)
  ADVISORY /home/vgpnk/.kimi-code/config.toml:2940 -> drifted found_at=3298
  ADVISORY /home/vgpnk/.kimi-code/config.toml:3227 -> drifted found_at=3298
  ADVISORY /home/vgpnk/.kimi-code/config.toml:2938 -> drifted found_at=3296
  ADVISORY /home/vgpnk/.kimi-code/config.toml:1284 -> drifted found_at=3296
  ADVISORY /home/vgpnk/.kimi-code/config.toml:1287 -> drifted found_at=3299
```

Observation: E14's own §5b comment ("every repo locus that cites a
`~/.kimi-code/config.toml` line, as its own host row") is accurate — and that is
exactly the defect for C1's purposes: the class is `host`, host rows "never change
the exit code" (`E14.md:194-196`), so the gate returns **0 clean while all five
pointer rows are drifted**. A round that lands this gate and then claims C1's
"N→0" would be measuring the claim with a probe that cannot fail on it. E14's own
§1 finding 2 states the exit-0 behaviour ("green on repo rows and reports the
pointer family as advisory … 5 hits, exit 0", `E14.md:12-14`) — I confirm it by
execution.

Also measured: **E14's frozen baseline root is non-conformant.** It lands under
`scripts/citation-drift-frozen/` (`E14.md:27`; registry row `E14.md:663`), but
`PROTOCOL.md:390-391` pins "Frozen baseline names resolve under any
`.ufo/waves/*/frozen` root; a bare name matching more than one root fails closed."
`find .ufo -type d -name frozen` → **0** this session; E15's draft uses
`.ufo/waves/arc2-loop1-round3/frozen` (`E15.md:293`), which is the compliant
placement. Landing E14's layout unchanged leaves the two-evidence clause with an
out-of-tree baseline.

### 2.5 The three missed pointer classes, proven by executing E14's `classify()`

Fixtures under `/tmp/arc2-l3r3-CR5-sim/`; E14's own code, unmodified:

```
range-start pinned, file intact -> resolved
3-row range, line 4 deleted -> [(2,'resolved'),(3,'resolved'),(4,'missing')]
1-row form (start only)     -> [(2,'resolved')]          ← the range's tail is unguarded
multi-line needle -> missing                              ← a wrapped needle can never resolve
truncated first-half needle -> resolved                   ← and a truncated one passes after re-point
spaced path, correct -> resolved
naive-extracted basename 'space.md' -> target_missing     ← misclassifies, does not crash
```

```
$ python3 -c "naive re on 'cite: fixture/with space.md:3'"
naive regex extracted: 'space.md' line 3
```

Observation: the table format `path<TAB>line<TAB>needle<TAB>scope` is sound for
single-line, single-row, space-free pointers — and every real C1 pointer is at
least one of the three other kinds: `:11` is a **prose range** (`lines 1285-1292`),
`:12` is a **`sed` range**, `SCORECARD.md:759-760` is a **multi-line needle**
(the token `:1284/:1287` and the word `pointers` sit on different lines — verified:
`sed -n '759p' SCORECARD.md | grep -cE 'config\.toml:[0-9]+'` → 0, while a
multi-line regex matches). The table must therefore carry one row per *line of
the range* (or an explicit range field), quote spaced paths, and never rely on a
needle that wraps.

### 2.6 The multi-line needle class in the round's own text

```
$ sed -n '759p' SCORECARD.md | grep -cE 'config\.toml:[0-9]+'
0                      # line-scoped: no match
$ python3 -c "re.search(r'mcp-registrations\.md:9,:80,:88 \(dead .:1284/:1287.', t, re.S)"
multiline path+bare-colon-list match: True
$ sed -n '759,760p' SCORECARD.md
corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88 (dead `:1284/:1287`
pointers) + r4-16-frontier-rescan.md:43 (stale-pin loci outside C1's declared
```

Observation: the carried-debt sentence's own pointer list is a **comma-list**
(`:9,:80,:88`) whose tail tokens are bare (`:80`, `:88`, `:1284`) and a
**wrapped needle** (`dead \`:1284/:1287\`` / `pointers)`). A naive `path:NNN`
extractor recovers only the first member of the comma list and nothing from the
wrapped one — so any census derived from reading *this sentence* undercounts by
construction.

### 2.7 The C1 measurable, corrected — what "N→0" must be measured over

The claim's own measurement can be made unambiguous and cheap:

- **Locus set** (12, all measured dead this session): the 4 colon-form repo loci
  (`PROVINCE.md:18`, `SCORECARD.md:59,:291,:698`), the 5 knowledge/lesson loci
  (`mcp-registrations.md:11,:12,:18,:88`; `lessons/2026-10-15-round-1.md:82`), and
  the 3 secondary forms (`r4-16-frontier-rescan.md:43,:233`; the bare `:3227`
  continuation on `PROVINCE.md:18`).
- **Durable anchor**: the stanza header `[mcp_servers.rea]` and the pin line
  `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`, both byte-identical across all
  five observed config states (bak table §2.1) while the line number moved
  `:2913 → :2930 → :2938 → :3225 → :3296`. Any landed repair that writes a line
  number re-arms the class on the next rewrite; the repair should name the header
  (as `C3.md` §5.3 proposes) or the receipt.
- **Verdict map for the gate**: a `repo` row per config-pointer locus (so the gate
  can red), `host` rows only for the five custody files' content landmarks, and a
  `stamp`-qualified exemption only where the citing text itself names its receipt
  (`SCORECARD.md:59` does: "per the 16:57:35Z custody receipt").
- **SCORECARD.md:270 reword**: measured same-line-count candidate (74 chars → 74
  chars, so no landed citation shifts):
  `` `:157` pointer (at `:177` in HEAD, per seat C7) is recorded as named debt, ``

Blast radius if the reword is *not* same-line-count: **9 pointers into
`SCORECARD.md` at line >270** (`LOG.md:939,:940,:964,:1061`; `SCORECARD.md:681,:682,:761`;
`SKILL.md:199,:213`) shift on any insert above them.

## 3. Verbatim block for the parent (land as-is if used)

```text
C1 census definition (frozen for this round) — corrected, with the instrument fix:

Scope: "dead pointer" means a line-number citation whose cited line no longer
holds the content the citing sentence claims. Measured at HEAD 679af5d against the
live ~/.kimi-code/config.toml (sha256 bd5a78d1…, stanza :3296, pin :3298):
12 such loci in editable files, 12 dead, 0 live.

The loci (this is the census; C1's declaration names 3 of them):
  colon form  PROVINCE.md:18 (`:2940`), SCORECARD.md:59 (`:2940`, stamp-qualified),
              SCORECARD.md:291 (`:1478`), SCORECARD.md:698 (`:2940`),
              corpus/knowledge/2026-10-13-mcp-registrations.md:88 (`:1284`),
              corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43 (`:1284-1292`),
              corpus/lessons/2026-10-15-round-1.md:82 (`:1287`)
  prose form  corpus/knowledge/2026-10-13-mcp-registrations.md:11 (`lines 1285-1292`),
              :18 (`line 1288`)
  sed form    corpus/knowledge/2026-10-13-mcp-registrations.md:12 (`sed -n '1285,1293p'`),
              corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:233 (`sed -n '1283,1294p'`)
  bare form   PROVINCE.md:18 (`:3227`, continuation)
Lines mcp-registrations.md:9 and :80 carry NO line-number token — they are not
pointer loci. mcp-registrations.md:11,:12,:18 are loci the declaration misses.

Do NOT re-point to :2938/:2940 — the stanza is at :3296/:3298 and the number has
already moved five times today (:2913→:2930→:2938→:3225→:3296). The durable anchor
is the header `[mcp_servers.rea]` (pin line byte-identical in all five states) or
the receipt. A landed repair that writes a literal line number re-arms the class.

Gate requirement (C3): the draft gate's config-pointer rows are `host`-scoped and
therefore advisory — the gate returns exit 0 while every pointer row is drifted.
For C1's measurable to be gate-measurable, each config-pointer locus above must
be a `repo` row, with one row per line of a range (a single row at the range's
start leaves the tail unguarded — measured), quoted paths for any path containing
a space, and no needle that wraps a line (a multi-line needle is always `missing`;
a truncated half-needle passes after the referent is re-pointed). Frozen baseline
root must be `.ufo/waves/*/frozen` (PROTOCOL.md:390-391); E14's
`scripts/citation-drift-frozen/` is non-conformant, E15's
`.ufo/waves/arc2-loop1-round3/frozen` is conformant.

SCORECARD.md:270 same-line-count reword (74→74 chars; 9 landed pointers into
SCORECARD.md above :270 stay put):
`:157` pointer (at `:177` in HEAD, per seat C7) is recorded as named debt,
```

## 4. Conclusions, labeled

**Observations** (ran/read this session): receipt 5/5 rc=0 and HEAD unchanged
throughout; live config hash `bd5a78d1…` with stanza `:3296`/pin `:3298`; the
five-`.bak` line/stanza progression; the 12-locus/12-dead census across four
pointer forms; `:9`/`:80` carrying no line token; E14's script+table extracted and
executed (exit 0, 0 repo rows on the C1 class, 5 advisory drifts); E14's frozen
root at `scripts/` with zero `.ufo/**/frozen` dirs in the tree; the three
`classify()` fixture behaviours (multi-line → missing; range tail unguarded;
spaced-path basename extraction); the multi-line needle at `SCORECARD.md:759-760`
(line-scoped rc=1, multi-line match true); the 9-pointer blast radius above
`:270`; the 74→74 reword; the transient README +2 state at 18:12Z followed by
byte-identical restore (`29cd30ee…`, mtime `18:12:28Z`).

**Inferences:** (1) C1's claim as declared is not measurable as written — it names
one locus class, one pointer form, and a repair target that is already dead;
(2) the E14 gate, if landed unchanged, would certify C1's class as clean while it
is 12/12 dead, because the class lives in advisory rows; (3) E15's draft is the
stronger of the two on the C1 class (its `extracted` entry kind reads the number
*out of* the citing line and checks the target, and its frozen root is compliant),
but its inlined table is a scratch-path artifact (`/tmp/arc2-l3r3-E15/`) that the
parent must copy at land time; (4) any repair that writes a line number into the
repo re-arms the class on the next operator rewrite — the header/receipt anchor is
the only durable form; (5) the README +2 transient shows sibling rehearsals mutate
the shared worktree mid-wave, so every pointer measurement in every report needs
its revision named (PROTOCOL.md:378-380).

**Unknowns:** (1) whether the parent freezes C1's N over the 12-locus set, the
3-file set, or the round declaration's 5 named loci — this choice, not the sweep,
decides the claim; (2) whether `SCORECARD.md:59`'s stamp-qualification counts as
resolved (it is accurate at its stamp; the gate draft would record it
`citation_historical_ok`, E14's table treats it as advisory); (3) whether the
parent lands E14, E15, or a merge — I ran only E14's quoted bytes; E15's script
was not inlined and I did not reconstruct it; (4) which seat produced the 18:12Z
README transient (the bytes were restored, so no evidence survives in the
worktree); (5) the post-battery closing state of the five custody paths — my
captures are mid-wave.

## 5. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
sha256sum /home/vgpnk/.kimi-code/config.toml; grep -n 'mcp_servers\.rea\]\|rea-agents@' /home/vgpnk/.kimi-code/config.toml
for b in /home/vgpnk/.kimi-code/config.toml.20261018-*.bak; do printf "%s lines=%s stanza=%s\n" "$(basename $b)" "$(wc -l <$b)" "$(grep -n 'mcp_servers.rea\]' $b|head -1|cut -d: -f1)"; done
for n in 9 11 12 18 80 88; do printf "%s => " $n; sed -n "${n}p" corpus/knowledge/2026-10-13-mcp-registrations.md | grep -oE 'config\.toml[^;]*|lines [0-9,-]+|line [0-9]+' | tr '\n' '|'; echo; done
sed -n '177,595p' .ufo/waves/arc2-loop1-round3/E14.md > /tmp/arc2-l3r3-CR5-sim/e14-quoted.py
sed -n '601,643p' .ufo/waves/arc2-loop1-round3/E14.md > /tmp/arc2-l3r3-CR5-sim/e14-table.tsv
python3 -c "import importlib.util as u; s=u.spec_from_file_location('g','/tmp/arc2-l3r3-CR5-sim/e14-quoted.py'); m=u.module_from_spec(s); s.loader.exec_module(m); r=m.parse_table(open('/tmp/arc2-l3r3-CR5-sim/e14-table.tsv').read()); import json; print(json.dumps(m.evaluate('.',r)['counts']))"
find .ufo -type d -name frozen    # 0 hits
sed -n '759p' SCORECARD.md | grep -cE 'config\.toml:[0-9]+'    # 0
awk 'NR==270{print length($0)}' SCORECARD.md                   # 74
```

## 6. Convergence note

- **Corroborated (not novel here):** the `:3296`/`:3298` relocation and the death
  of C1's `:2938/:2940` plan are independently named by `E14.md:7-9`, `E15.md:5-9`,
  and `C3.md:17-23` (all read this session); the `:9`/`:80`-carry-no-pointer
  finding is `E15.md:224-227`; the README-insert shift is `C3.md:17-20`. My run of
  E14's own table reproduces its §3 result and its §1 finding 2 by execution.
- **Unique to this seat:** the four-form, content-resolved **12-locus/12-dead**
  census (§2.3) with `SCORECARD.md:291` and `PROVINCE.md:18`'s bare `:3227` as
  named loci outside every other seat's list; the **executed** E14 evaluation
  showing **0 repo rows on the C1 class** and exit 0 with 5 drifted advisory rows
  (§2.4); the frozen-root conformance gap (`scripts/` vs `.ufo/waves/*/frozen`,
  §2.4); the three `classify()` fixture behaviours (§2.5); the multi-line/comma-list
  needle proof on `SCORECARD.md:759-760` (§2.6); the 9-pointer blast radius and the
  74→74 same-line reword for `:270` (§2.7); the 18:12Z README transient (§1).
- **Repo state at my final check:** HEAD `679af5d` unchanged; `git status
  --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only; no round-3 edit had
  landed; 32 sibling reports present. Cross-seat line pointers were re-verified at
  my read time; treat them as movable.
