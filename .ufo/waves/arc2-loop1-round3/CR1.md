# CR1 (critic) — attack on C1: are the "dead pointers" actually dead?

Seat CR1, wave arc2-loop1-round3, 2026-10-18, read-only. HEAD `679af5d749f2fd48b9d543e3c99d348d5458f90f`
(`git rev-parse HEAD`); `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only. My only
write is this file. Every command below was run by this seat this session (stamps 17:58:31Z–18:06:10Z);
every `path:line` was resolved by a command, none from memory. No battery leg, no MCP session, no
`/tmp` scratch used (all commands inline).

## 1. Verdict

**SPLIT — and C1's own repair values are already dead.** Content-based checking confirms the
`~/.kimi-code/config.toml:NNNN` pointer class is dead at HEAD for every corpus locus, but
(1) the strongest NO-CHANGE steelman holds for the repo-internal `SCORECARD.md:270` `:157`
locus under the card's own baseline-revision convention (`SCORECARD.md:16-17`) — its cited
content lived at the cited line at the revision that reading names; and (2) **the re-point
target C1 prescribes (`:2938/:2940`) no longer holds the cited content either**: at HEAD
`:2938` = `max_context_size = 1000000` and `:2940` = `capabilities = [ "thinking", "tool_use" ]`,
while the stanza is at `:3296`. Landing C1 verbatim writes **fresh dead pointers**, and the
claim's measurable ("dead-pointer loci in the scoped set N→0") would then report a **false
N→0** under any honest content check. C1's enumeration is also wrong on two of its named
lines: `mcp-registrations.md:9,:80` carry **no** `config.toml:NNNN` pointer at all (they carry
the stale *pin*); the file's actual dead-pointer lines are `:11`, `:18` and `:88` — of which
C1 names only `:88`.

## 2. Receipt check (required before my leg)

```
$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```
**5/5 OK, rc 0** — the pre-pair (`2026-10-18T17:55:49Z`, `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt:1-6`)
matches the live files at my check time. The config.toml line is
`bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c`, which is also the live hash
I read independently (`sha256sum /home/vgpnk/.kimi-code/config.toml`).

## 3. Evidence — the pointer family at HEAD, content-checked

### 3.1 Live stanza position vs every corpus claim

```
$ for n in 1284 1287 1288 1292 1478 2938 2940 3225 3296 3298 3299; do printf '%s => ' "$n"; \
    sed -n "${n}p" /home/vgpnk/.kimi-code/config.toml; done
1284 => display_name = "Grok 4.7 (key 2)"
1287 => [models."opencode-go-3/grok-4.7"]
1288 => provider = "opencode-go-3"
1292 => capabilities = [ "image_in", "always_thinking", "tool_use" ]
1478 => max_output_size = 131072
2938 => max_context_size = 1000000
2940 => capabilities = [ "thinking", "tool_use" ]
3225 => display_name = "K3-256k"
3296 => [mcp_servers.rea]
3298 => args = [ "-y", "rea-agents@6.7.0", "mcp" ]
3299 => startup_timeout_sec = 30
$ wc -l /home/vgpnk/.kimi-code/config.toml
3322 /home/vgpnk/.kimi-code/config.toml
```

**Observation:** the only stanza is `:3296`–`:3302` (`[mcp_servers.rea]` :3296, `args` :3298,
`startup_timeout_sec` :3299, `[mcp_servers.rea.env]` :3301; `grep -n '^\[mcp_servers'` returns
exactly 3296 and 3301). **Every** `config.toml:NNNN` value in the repo is content-dead at HEAD.

### 3.2 The pointer family repo-wide (non-`.ufo`)

```
$ git grep -nE 'config\.toml:[0-9]+' -- . ':(exclude).ufo'
LOG.md:1005:  `PROVINCE.md:10,:18` claim Kimi `rea-agents@6.4.0` at `config.toml:1478`,
LOG.md:1018:  Kimi pin (only `rea-agents@6.7.0` at `config.toml:2940`; `:1478` =
PROVINCE.md:18:`rea-agents@6.7.0` (`~/.kimi-code/config.toml:2940` at the 16:57:35Z receipt; a 17:32Z rewrite relocated it to :3227, value unchanged). Cache/catalog
SCORECARD.md:59:  (arc2-loop1-round2): Kimi pin is `rea-agents@6.7.0` at `config.toml:2940` per the
SCORECARD.md:291:  `~/.kimi-code/config.toml:1478` → 6.4.0 (170 / 127 / 25802f6d… / expects
SCORECARD.md:698:(live config now pins `rea-agents@6.7.0` at `config.toml:2940`, SC2-refuted);
corpus/knowledge/2026-10-13-mcp-registrations.md:88:- kimi stanza header is `config.toml:1284` (startup_timeout_sec at 1287), not 1285/1288. (audit-A, consistency)
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43:  `~/.kimi-code/config.toml:1284-1292` (`[mcp_servers.rea]`, npx
corpus/lessons/2026-10-15-round-1.md:82:`~/.kimi-code/config.toml:1287` still pins 6.4.0. Installed shared skill
```
Plus the range-form pointers C1 did **not** name:
```
$ grep -nE 'config\.toml[ :]+(line|lines|[0-9])' corpus/knowledge/2026-10-13-mcp-registrations.md
11:- source: … ~/.kimi-code/config.toml lines 1285-1292
18:- source: … ~/.kimi-code/config.toml line 1288
```
**Observation:** ten dead `config.toml` pointers across six files at HEAD, of which C1's scoped
set names three (`mcp-registrations:88`, `r4-16:43`, and the `SCORECARD:270` `:157`). **C1
misses `mcp-registrations:11` and `:18`** (the two range-form pointer lines) and **mis-attributes
`:9`/`:80`** — those lines carry the stale *pin* `rea-agents@6.4.0`, not a line pointer. The
same mis-attribution is already recorded in the carried-debt line at `SCORECARD.md:758-759`
("mcp-registrations.md:9,:80,:88 (dead `:1284/:1287` pointers)").

### 3.3 The relocation history — why line numbers cannot be drained

```
$ for f in ~/.kimi-code/config.toml.20261018-085645.bak ~/.kimi-code/config.toml.20261018-114557.bak \
           ~/.kimi-code/config.toml.20261018-143236.bak ~/.kimi-code/config.toml.20261018-145016.bak; do
    printf '%s: ' "$f"; grep -n 'mcp_servers.rea' "$f" | head -1; done
…config.toml.20261018-085645.bak: 2913:[mcp_servers.rea]
…config.toml.20261018-114557.bak: 2930:[mcp_servers.rea]
…config.toml.20261018-143236.bak: 2938:[mcp_servers.rea]
…config.toml.20261018-145016.bak: 3225:[mcp_servers.rea]
```
Cross-checked against the parent's own round-2 drift record, read verbatim this session
(`.ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt`):
"`[mcp_servers.rea]` relocated :2938 -> :3225; the pin line is byte-identical
(`rea-agents@6.7.0`)" and "post-window `config.toml` rewrite at 17:32:20Z detected and recorded
verbatim … not repaired, per SOP — operator-owned surface" (`SCORECARD.md:729-730`).

**Observation:** the stanza has been observed at `:2913`, `:2930`, `:2938`, `:3225` and now
`:3296`. The live file's mtime is `2026-10-18 14:50:34 -0300` (= 17:50:34Z) — **after** the
round-2 drift record's own reading (17:32:20Z) and **before** the round-2 records commit
`679af5d` (14:54:52 -0300 = 17:54:52Z) by ~4 minutes. So the `:3225` position the drift record
characterized was already superseded when the round-2 records landed, and the `:3296` position
is what the 17:55:49Z round-3 receipt froze (sha `bd5a78d1…`). The `:2938/:2940` pair C1
prescribes corresponds to the stanza state captured in `config.toml.20261018-143236.bak`; by the
next reachable snapshot it was `:3225`, and by the live file `:3296`.

**Unknown (flagged):** the two 14:32 backups' mtimes are inverted relative to their contents
(`…143236.bak` mtime 14:32:36 holds `:2938`; `…145016.bak` mtime 14:32:20 holds `:3225`). I
did not resolve the intra-day ordering of those two writes; it does not affect the conclusion,
which rests on the live file plus the parent's own 17:32:20Z receipt.

## 4. Locus-by-locus: dead, or defensible?

### Locus A — `SCORECARD.md:270` (`:157` parenthetical)

Text at HEAD (`SCORECARD.md:269-271`): "the stale-summaries bullet's `:157` pointer (at `:160`
in HEAD, per seat C7) is recorded as named debt, not silently fixed."

Content check at HEAD: `corpus/README.md:157` = `| entry | round | gist |` — a table header,
not a frontier bullet. `corpus/README.md:160` = the round-2 Lessons row with the safety-scope
parenthetical. The frontier bullet is at `:177`.

**Steelman (strong).** The sentence sits inside `## luna-round-1 — coverage map completion,
2026-10-16` (`SCORECARD.md:237`; next section `:273`) — a round-dated section, not the living
surface. The card's own convention (`SCORECARD.md:16-17`) is that line citations refer to the
**baseline revision** unless marked current. I resolved both readings:
```
$ git show 6645585873c4e66372b15687c47000abf8d91978:corpus/README.md | awk 'NR==157 {print}'
- Runtime-obs extended: process-capture, managed `verify`/`project` ops, native call-target resolution (per r4-16 rescan: ~26 self-provisionable).
$ git show a79945c4:corpus/README.md | awk 'NR==160 {print}'
- Runtime-obs extended: process-capture, managed `verify`/`project` ops, native call-target resolution (per r4-16 rescan: ~26 self-provisionable).
```
So **`:157` is exactly correct at `6645585`** (the 2026-10-15 card baseline) and **`:160` is
exactly correct at `a79945c4`** (the luna-round-1 baseline) — the sentence records *both*
readings, each true at the revision it belongs to. The only imprecision is the words "in HEAD":
at the revision where the sentence landed (`a4bd355`), README `:160` = "adb device surface"
and the bullet was at `:162` — so "in HEAD" was loose, while `:160` was right for the section's
declared baseline. This is the same shape the parent already adjudicated as NO-CHANGE once:
`SCORECARD.md:672-676` — the `SCORECARD.md:79` `PROVINCE.md:107-109` token ruled
"baseline-revision-correct under the card's own convention (:16-17) … byte-identical".

**Ruling:** the cited content *does* live at the cited line under a defensible reading —
**NO-CHANGE has a real case**. The debt the sentence names was also independently discharged
(`SCORECARD.md:68-72`), so the sentence now reads as a dated record of a superseded debt, which
is what a round-dated section is for. If the parent edits it, the honest edit names the
baseline revision; re-pointing to `:177` would rewrite a dated record to assert something
round-1 did not say. Note the tension: the measurable "cited line lacks cited content" is
**convention-dependent** here — it fails under a literal HEAD reading and passes under the
card's own baseline convention.

### Locus B — `corpus/knowledge/2026-10-13-mcp-registrations.md`

- `:9`, `:80` — carry the pin `rea-agents@6.4.0` in the heading and Summary. At HEAD the live
  pin is `rea-agents@6.7.0` (`:3298`). Stale as a *current-surface* claim; **not** pointer lines.
- `:11` (`config.toml lines 1285-1292`), `:18` (`config.toml line 1288`), `:88`
  (`config.toml:1284`, `startup_timeout_sec at 1287`) — all dead at HEAD (§3.1).
- The other two cited ranges on `:11` — `~/.omp/agent/mcp.json lines 1-17` and
  `~/.config/devin/mcp_config.json lines 1-16` — **resolve to the cited content**:
  ```
  $ wc -l ~/.omp/agent/mcp.json ~/.config/devin/mcp_config.json
   18 /home/vgpnk/.omp/agent/mcp.json
   17 /home/vgpnk/.config/devin/mcp_config.json
  $ sed -n '1,17p' ~/.omp/agent/mcp.json | grep -c rea     → 2
  $ sed -n '1,16p' ~/.config/devin/mcp_config.json | grep -c rea → 2
  ```
  (Both ranges end one line short of the file's closing brace — a nit, not a dead pointer.)

**Steelman for NO-CHANGE.** The entry is a dated evidence record — header "corpus entry —
kaidoku-shokunin round 1 (2026-10-13)" (`:1`) with `verified-at: 2026-10-13` on every candidate
(e.g. `:13`, `:20`, `:27`). Under a snapshot semantics, a pointer is a reference to the file
state *at verification time*, not a live pointer; the pin claim is bounded by its own
`verified-at`. The file's own governance is append-only (`## Errata (round 2)` at `:82`), and
`corpus/QUALITY.md:4-5` states the corpus convention: "A criterion is replaced by a new row
naming the row it supersedes, never rewritten." So the right mechanism is an append, which is
what C1 proposes — the attack lands on the *values*, not the mechanism.

**Write-time correctness is unknown.** I cannot verify that `:1284/:1287` (or `:1285-1292`,
`:1288`) ever held the stanza: the earliest snapshot reachable is
`config.toml.20261018-085645.bak` (Oct 18 08:56, stanza `:2913`), and nothing in this repo
pins a 2026-10-13 config.toml. The erratum at `:88` asserts a round-2 correction
("not 1285/1288"), which implies a 2026-10-13 check I cannot reproduce. **Honest status:
dead at HEAD (observation); dead-or-alive at write (unknown).**

### Locus C — `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43`

```
$ awk 'NR==43 {print}' corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
  `~/.kimi-code/config.toml:1284-1292` (`[mcp_servers.rea]`, npx
```
Content check: `:1284` = `display_name = "Grok 4.7 (key 2)"`, `:1292` = a `capabilities` line.
**Dead at HEAD, content-confirmed.**

**Steelman (weakest of the three).** The sentence is a record of a *verification act* performed
`2026-10-13T16:46Z` (`:46`, `:50`), inside a dated entry, and the file already carries an
append-only errata tail (`## Errata (round 9 freshness, 2026-10-16, append-only)` at `:927`)
that cross-references `:751-752` — so appending is the established form. But unlike Locus A
there is no repo-internal baseline convention covering an *external operator file*: the target
is mutable, operator-owned, and rewritten at least four times on 2026-10-18 alone. The dated-act
defense preserves the *observation*, not the pointer. **Ruling: genuinely dead; append-only
errata is the right repair — with content anchors, not new line numbers.**

### Locus D — the same class landed by round 2 itself

`PROVINCE.md:18` (landed at `b3cd790`, 14:53:09 -0300) reads: "…`config.toml:2940` at the
16:57:35Z receipt; a 17:32Z rewrite relocated it to :3227, value unchanged". Live `:3227` =
`default_effort = "high"`. **Round 2 landed a pointer that was dead within the hour**, because
the config was rewritten again at 14:50:34 -0300 (17:50:34Z). The parent's own round-2 record
already discloses the drift
(`.ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt`), but the
"relocated to :3227" clause written *from* that receipt was stale before the round's records
commit. `SCORECARD.md:59`, `SCORECARD.md:698` and `LOG.md:1018` all cite `:2940` — same class.

**Inference:** the C1 values `:2938/:2940` most plausibly came from the round-2 drift receipt's
"relocated :2938 -> :3225" sentence (which names `:2938` as the *old* location) rather than
from a live read; a live read at drafting time would have given `:3296`. Labeled inference —
the parent knows its own drafting path.

## 5. What this does to C1's measurable

C1's acceptance test is "dead-pointer loci in the scoped set N→0 (cited line lacks cited
content)". Three ways it can be run, with different outcomes:

1. **Content check against the live config at landing** — landing `:2938/:2940` leaves both
   loci dead (`:2938` = `max_context_size`, `:2940` = a `capabilities` line) → claim reports
   **not-verified**.
2. **Content check against the 14:32-era file** — passes, but that file no longer exists on
   this host and is not the current surface; the pass would not be reproducible.
3. **Check only that a number changed** — passes, and is exactly the false-PASS mode round-1's
   CR5 proved for the sibling census (`CR5.md` round-1 §2.5). Not acceptable.

There is no run of the test as written under which landing C1 verbatim both (a) puts the cited
content at the cited line and (b) is verifiable after the fact. That is the core refutation.

## 6. Text the parent may land VERBATIM

Append to `corpus/knowledge/2026-10-13-mcp-registrations.md` (append-only, after `:88`):

```text
## Errata (round 3, 2026-10-18, append-only)

- **External-pointer staleness (arc2-loop1-round3, CR1).** The `~/.kimi-code/config.toml`
  line numbers above are dead at HEAD `679af5d`: `:11`'s `lines 1285-1292`, `:18`'s `line 1288`
  and `:88`'s `:1284`/`:1287` no longer hold the stanza. At HEAD `:1284` is
  `display_name = "Grok 4.7 (key 2)"`, `:1287` is `[models."opencode-go-3/grok-4.7"]`, `:1288` is
  `provider = "opencode-go-3"`, `:1292` is a `capabilities` line. The file is operator-owned and
  was rewritten repeatedly on 2026-10-18; the stanza has been observed at `:2913`, `:2930`,
  `:2938`, `:3225` and, at the 17:55:49Z custody receipt, `:3296` (file 3322 lines, sha256
  `bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c`). The durable citation is
  the content anchor, not the line number: `[mcp_servers.rea]`, `args = [ "-y",
  "rea-agents@6.7.0", "mcp" ]`, `startup_timeout_sec = 30`. The pin claims at `:9`/`:80` are
  historical as of 2026-10-13 (`verified-at`); the live pin is `rea-agents@6.7.0`. No line
  number is re-pointed here, because any such number is expected to die at the next config write.
```

Append to `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` (append-only, after `:936`):

```text
## Errata (round 3, 2026-10-18, append-only)

- **`:43` config.toml pointer dead at HEAD (CR1, arc2-loop1-round3).** The cited
  `~/.kimi-code/config.toml:1284-1292` does not hold `[mcp_servers.rea]` at HEAD `679af5d`;
  the stanza is at `:3296` in the 3322-line file (sha256 `bd5a78d1…`, custody receipt
  2026-10-18T17:55:49Z). The 2026-10-13 hand verification this entry records stands as a dated
  act; the line-number form does not survive operator config rewrites. Content anchor:
  `[mcp_servers.rea]` with `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`.
```

For `SCORECARD.md:270` the defensible disposition is **NO-CHANGE with the reason stated**, not
a re-point: the parenthetical is baseline-revision-correct at `6645585` (`:157`) and at
`a79945c4` (`:160`), sits in a round-dated section (`:237`-`:272`), and the debt it names was
discharged at `:68-72`. If the parent prefers an edit, the honest form names the revision
("as of the 2026-10-15 baseline `6645585`"), it does not re-point to `:177`.

Also for the parent's own bookkeeping (outside my write scope): `PROVINCE.md:18`'s
"relocated it to :3227" is now dead (live `:3227` = `default_effort = "high"`), as are
`SCORECARD.md:59`, `SCORECARD.md:698` and `LOG.md:1018` (`:2940`). Per `AGENTS.md` the
integration must append the LOG.md entry for whatever it lands — this seat may not write there.

## 7. Conclusions, labeled

**Observations (run/read this session):** the 5/5 rc-0 receipt check; live stanza at
`:3296`/`:3298`/`:3299` and file 3322 lines sha `bd5a78d1…`; every cited `config.toml` line's
actual content (`:1284,:1287,:1288,:1292,:1478,:2938,:2940,:3225,:3227`); the ten-locus
pointer family from `git grep`; the two unnamed range-form pointers at `mcp-registrations:11,18`;
the four `.bak` stanza positions; the round-2 drift receipt text; `README:157`/`:160` contents
at HEAD and at `6645585`/`a79945c4`/`a4bd355`; the omp/devin range resolutions; the round-1
NO-CHANGE precedent at `SCORECARD.md:672-676`.

**Inferences:** (1) landing C1 verbatim writes fresh dead pointers, so its measurable cannot
honestly reach N→0; (2) the `:2938/:2940` values were taken from the round-2 drift receipt's
"old location" rather than a live read; (3) the pointer class is not drainable by re-pointing
because the target is operator-owned and was rewritten at least four times in one day; (4) the
`SCORECARD.md:270` locus is the one where NO-CHANGE genuinely survives, on the card's own
revision convention plus the `:79` precedent.

**Unknowns:** (1) whether `:1284/:1287`/`:1285-1292`/`:1288` ever held the stanza on
2026-10-13 — no snapshot of that date is reachable from here, so write-time correctness is
unverifiable; (2) the exact intra-day ordering of the two 14:32 backups (mtimes are inverted
relative to content); (3) whether the parent intends the measurable to be read literally at
HEAD (C1 fails) or under the card's baseline convention (the `:157` locus passes).

## 8. Reproduction commands

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD; git status --porcelain
tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -   # 5/5 OK, rc 0
for n in 1284 1287 1288 1292 1478 2938 2940 3225 3296 3298 3299; do printf '%s => ' $n; sed -n "${n}p" ~/.kimi-code/config.toml; done
grep -n '^\[mcp_servers' ~/.kimi-code/config.toml; wc -l ~/.kimi-code/config.toml
git grep -nE 'config\.toml:[0-9]+' -- . ':(exclude).ufo'
grep -nE 'config\.toml[ :]+(line|lines|[0-9])' corpus/knowledge/2026-10-13-mcp-registrations.md
for f in ~/.kimi-code/config.toml.2026*.bak; do printf '%s: ' "$f"; grep -n 'mcp_servers.rea' "$f" | head -1; done
git show 6645585873c4e66372b15687c47000abf8d91978:corpus/README.md | awk 'NR==157'
git show a79945c4:corpus/README.md | awk 'NR==160'
awk 'NR==270' SCORECARD.md; awk 'NR==18' PROVINCE.md
```
