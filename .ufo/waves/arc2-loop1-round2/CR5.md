# CR5 (critic) — attack on C1 census completeness

Seat CR5, wave arc2-loop1-round2, read-only. Every command below was run by
this seat this session (2026-10-18, stamps 17:00:23Z–17:07:13Z) at HEAD
`165057e36f558c95eb02bf24de4a874d559d6950`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round2/` only. This report is my only write. I ran
no MCP session and no battery leg (not my scope); no session to close.

## 1. Verdict

**PARTIAL REFUTE — the census as drafted is complete for the three declared
files but NOT complete for the claim's natural reading, and three instrument
holes make "N → 0" unmeasurable as written.**

1. **Three-file scope (PROVINCE.md / SKILL.md / SCORECARD.md): the sweep's
   coverage is sound but its count is scope-load-bearing.** I re-derived the
   current-surface set independently: **10 stale Kimi-pin statement groups**
   (PROVINCE.md ×8, SKILL.md ×1, SCORECARD.md ×1) — see §3 ledger. Round-2
   seats name 8 of the 10 groups; the two unnamed are inside already-named
   lines' *continuations* (`PROVINCE.md:11`, `:21-22` are named only by
   `R1.md`), and one policy locus (`:67`) is disputed across four seats. So
   with the declared scope and per-locus decisions, N → 0 is achievable and
   the sweep misses nothing *in those files*.
2. **Outside the declared files, four files carry current-surface-looking
   Kimi-pin statements that NO round-2 seat names** (I grepped every round-2
   report for each): `corpus/lessons/2026-10-15-round-1.md:82` (present-tense
   "still pins 6.4.0"), `corpus/knowledge/2026-10-13-mcp-registrations.md:9,`
   `:80` (pin claim in heading + Summary) and `:88` (an *erratum* whose
   corrected pointer `config.toml:1284`/`1287` no longer resolves — the
   stanza moved to `:2938`/`:2940`), and
   `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43` (same pointer
   class). `MINT.md:10` and `corpus/QUALITY.md:18` are named by `R1.md:30,100`
   but by no executor's edit set. **Repo-level stale Kimi-pin loci N stays
   ≥ 7 after the three-file sweep unless these get one decision each.**
3. **Three instrument holes, each proven by execution** (§5): a line-scoped
   client+version grep returns rc=1 on the real `SKILL.md:19-20` pair
   (client on :19, pin on :20) and on `corpus/lessons/...:82` (lowercase
   "kimi"); an unanchored `6\.[0-9]+\.[0-9]+` sweep false-positives on
   non-REA tools (`26.6.4` unblob at `PROVINCE.md:123`, `SKILL.md:57`);
   and three stale claims carry **no version token at all** on their own
   lines (`PROVINCE.md:11`, `:21`, `:22` — digest/cache-path forms), so any
   version-token-only sweep silently false-passes on them.
4. **The pointer family is a separate needle class with its own count.**
   Seven `config.toml:NNNN` pointers exist repo-wide (non-`.ufo`); at HEAD,
   `:1284`, `:1287`, `:1288`, `:1292`, `:1478` resolve to unrelated
   models-table lines and the live stanza is `:2938`/`:2940`. Version edits
   that do not also repair or scope the pointers leave a second non-zero
   family — and round-1's own claim text did not count pointers at all.

The frozen/editable partition with one decision per locus is §3; the
verbatim block the parent can land is §6.

## 2. Evidence — exact commands with observed output

### 2.1 Live pin re-verified (this seat, not quoted from siblings)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-18T17:00:23Z
$ grep -n 'rea-agents' /home/vgpnk/.kimi-code/config.toml \
    /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json
/home/vgpnk/.kimi-code/config.toml:2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
/home/vgpnk/.config/devin/mcp_config.json:7:        "rea-agents@6.5.0",
/home/vgpnk/.omp/agent/mcp.json:8:        "rea-agents@6.5.0",
$ sed -n '1478p' /home/vgpnk/.kimi-code/config.toml
model = "kimi-k3"
$ sed -n '2936,2946p' /home/vgpnk/.kimi-code/config.toml
[mcp_servers.rea]            # :2938
command = "npx"
args = [ "-y", "rea-agents@6.7.0", "mcp" ]   # :2940
startup_timeout_sec = 30
[mcp_servers.rea.env]        # :2943
GHIDRA_INSTALL_DIR = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC"
JAVA_HOME = "/usr/lib/jvm/java-21-openjdk"
$ for n in 1284 1287 1288 1292; do printf "%s => " $n; sed -n "${n}p" /home/vgpnk/.kimi-code/config.toml; done
1284 => capabilities = [ "image_in", "always_thinking", "tool_use" ]
1287 => 
1288 => [models."opencode-go-4/grok-4.7"]
1292 => max_output_size = 500000
$ wc -l /home/vgpnk/.kimi-code/config.toml
2964 /home/vgpnk/.kimi-code/config.toml
```

Observation: `:1478` is a models-table line; the **only** pin is `:2940` =
6.7.0; all five corpus/ledger pointers into the `1284–1292`/`1478` region are
dead at HEAD (the stanza moved ~+1654 lines). Reproduced SC2's refutation
independently.

### 2.2 The declared three-file surface — full version-token sweep

```
$ git grep -nE '\b6\.[0-9]+\.[0-9]+' -- PROVINCE.md SKILL.md SCORECARD.md | wc -l
38
$ # minus 2 proven FPs (26.6.4 unblob at PROVINCE.md:123, SKILL.md:57)
$ git grep -nE 'rea-agents@|\b6\.[457]\.0\b' -- PROVINCE.md SKILL.md SCORECARD.md | wc -l
36
$ git grep -nE 'rea-agents@' -- PROVINCE.md SKILL.md SCORECARD.md
PROVINCE.md:9,:10,:16,:17,:18,:45   (6 lines)
SCORECARD.md:698                      (1 line)
SKILL.md:12,:19,:20                   (3 lines)
```

Observation: the union instrument finds 36 distinct lines in the three
files; 24 of them (listed in §2.5 comm output) are found by the value-token
instrument but **not** by the `rea-agents@` pin-token instrument — including
`SCORECARD.md:58` and `PROVINCE.md:44`, the two living-card loci. A
pin-token-only sweep is therefore insufficient even inside the declared set.

### 2.3 Current-surface vs round-dated sections

```
$ grep -n '^## \|^### ' SCORECARD.md
3:## Current assessment … 19:## Owned axes  33:## Reconciled current state
51:## Open gaps — deliberately not closed by this move
86:## Measurement recipes  144:## Verdicts, planned, retired
158:## Interactive round-1 recovery … 237:## luna-round-1 …
273:## luna-round-2 … 327:## luna-round-3 … 374:## luna-round-4 …
417:## luna-round-5 … 467:## luna-round-6 … 503:## luna-round-7 …
534:## luna-round-8 … 561:## luna-round-9 … 615:## Capabilities
625:## Saturation  635:## arc2-loop1-round1 …
$ sed -n '16,17p;266,267p' SCORECARD.md
Line citations to pre-existing lane files refer to the baseline revision unless
explicitly marked current; the added lesson-index row shifts later README lines.
forward; retired: none. The 2026-10-15 reconciliation table above stays
frozen; its "current map is 70/72" row is superseded on that point by this
$ git log -S'closed by luna-round-2' --oneline -- SCORECARD.md
a9580eb luna-round-2: records (LOG + SCORECARD + report; calibration measured at work commit 75af886a)
```

Observation: `SCORECARD.md:58-59` sits in `## Open gaps` (:51-84), which is
the card's **living** section (the round-1 record corrected the "frozen
table" wording: the frozen block is :39-49 only — `SCORECARD.md:674-675`,
read this session). `:291`, `:302-304`, `:530`, `:534`, `:537`, `:620` all
sit inside round-dated luna sections → historical by construction.
`SCORECARD.md:698` already carries the round-1 carried-debt sentence with the
correct live values.

### 2.4 Loci outside the declared files (the four no-seat files)

```
$ grep -n 'mcp-registrations\|r4-16\|frontier-rescan' .ufo/waves/arc2-loop1-round2/*.md
(only E9.md:108 — about corpus/README.md:160's content discharge, not the pointer)
$ grep -nE 'lessons/2026-10-15-round-1\.md:82|:1287' .ufo/waves/arc2-loop1-round2/*.md
(no matches — NO round-2 seat names the lessons :82 locus or any :128x pointer)
$ sed -n '80,84p' corpus/lessons/2026-10-15-round-1.md
Read-only registration observations: `~/.omp/agent/mcp.json:8` and
`~/.config/devin/mcp_config.json:7` pin 6.5.0;
`~/.kimi-code/config.toml:1287` still pins 6.4.0. Installed shared skill
metadata is version 42 / tool_count 207. Province's 6.4.0/170/127/v37 values
are historical and are not claimed aligned today.
$ sed -n '9,11p;79,80p;88p' corpus/knowledge/2026-10-13-mcp-registrations.md
## Candidate: Exactly three client files register REA — omp, devin, kimi — all pinned to `npx -y rea-agents@6.4.0 mcp` with identical env
- claim: … each define a server named `rea` launching `npx` with args `["-y","rea-agents@6.4.0","mcp"]` …
- source: … ~/.kimi-code/config.toml lines 1285-1292
## Summary
REA is registered for 3 of 7 surfaces … all launching pinned `npx -y rea-agents@6.4.0 mcp` …
- kimi stanza header is `config.toml:1284` (startup_timeout_sec at 1287), not 1285/1288. (audit-A, consistency)
$ sed -n '41,45p' corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
  doctor's SupportedClients registry; its live registration at
  `~/.kimi-code/config.toml:1284-1292` (`[mcp_servers.rea]`, npx
  `rea-agents@6.4.0 mcp`, same env pair) verified intact by hand — 3/7 surfaces
  (devin/omp/kimi) still registered.
$ sed -n '10p' MINT.md
`rea` MCP server (`npx -y rea-agents@6.4.0 mcp`, registered for Devin in
$ sed -n '18p' corpus/QUALITY.md
| 8 | Capability claims pin tool/provider versions (rea-agents@6.4.0, Ghidra 12.1.4, JDK 21) and the claim source … | — |
```

Observation: seven loci in four files, each carrying a 6.4.0 statement
outside C1's declared scope; none of the four files appears in any round-2
executor's edit set (E18.md:95-110 and E19.md:107-114 enumerate the
three-file set plus MINT/QUALITY as "out-of-scope discovery"). The
`mcp-registrations:88` erratum is the sharpest case: it is a **correction
record** whose corrected pointer is itself dead at HEAD.

### 2.5 Frozen/immutable loci — the census must not reach them

```
$ git grep -n '6\.7\.0' -- . ':(exclude).ufo'
LOG.md:1006:  but the file's only `rea-agents` occurrence is `6.7.0` at `:2940`
SCORECARD.md:698:(live config now pins `rea-agents@6.7.0` at `config.toml:2940`, SC2-refuted);
$ git grep -nE '6\.[0-9]+\.[0-9]+' -- LOG.md | wc -l
19
$ grep -rnE 'rea-agents|6\.4\.0|6\.5\.0|6\.7\.0' evidence/ | head -20
(no output — evidence/ carries zero version tokens)
$ git grep -nE '\b6\.[457]\.0\b' -- . ':(exclude).ufo' | cut -d: -f1 | sort | uniq -c
 19 LOG.md, 1 MINT.md, 13 PROVINCE.md, 20 SCORECARD.md, 1 SHONEN.md, 3 SKILL.md,
 1 corpus/QUALITY.md, 45 corpus/README.md, + per-entry knowledge counts
```

Observation: `LOG.md` holds 19 version loci — all frozen append-only history
(incl. :1005-1006 which *records* the refutation). `.ufo/reports/*` and
`.ufo/waves/*` hold the prior-round records (`.ufo` is outside the claim by
protocol; `.ufo/reports/arc2-loop1-round1/kaidoku.md:72` already names the
6.7.0 refutation). `evidence/round-1-2026-10-15/*` has zero version tokens —
not a target (confirms round-1 CR5's finding, re-run this session).

### 2.6 Round-2 receipts and wave state (context for the parent's measurement)

```
$ tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
… 5× OK; rc=0
$ wc -l .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
6
```

Observation: the 5-path pre-pair (`2026-10-18T16:57:35Z`) self-checks
rc=0, 5/5. Wave dir holds 20 sibling reports at my write time.

## 3. Frozen vs editable — one decision per locus

**EDITABLE — current-surface (C1 edit set; 10 statement groups):**

| # | Locus | Decision |
|---|---|---|
| 1 | `PROVINCE.md:10` | EDIT: Kimi `rea-agents@6.4.0` → resolved 6.7.0 value + receipt |
| 2 | `PROVINCE.md:11` | EDIT: "Both versions have separate npx cache installs" now undercounts (three caches) + `25802f6d…` digest continuation — no version token on the line (instrument hole) |
| 3 | `PROVINCE.md:18` | EDIT: pin + stale pointer `config.toml:1478` → `:2940` |
| 4 | `PROVINCE.md:21` | EDIT: 6.4.0 cache-path line; add 6.7.0 cache `a1722018f28f9df2` (SC1 confirms complete/offline-resolvable) or mark per-surface |
| 5 | `PROVINCE.md:22` | EDIT: 6.4.0 digest continuation (no version token) |
| 6 | `PROVINCE.md:44` | EDIT: Core row "(Devin/OMP 6.5.0, Kimi 6.4.0; see surface summary)" |
| 7 | `PROVINCE.md:45` | SPLIT: "127 commands" current-surface count (153 on 6.5.0/6.7.0) + probe cell `--version → 6.4.0` is a dated 2026-10-13 receipt → mark historical |
| 8 | `PROVINCE.md:67` | ADJUDICATE: routing sentence "a version drift past 6.4.0" — ceiling false; rephrase (S1.md:134) or NO-CHANGE-with-cause (R1.md:93). One call |
| 9 | `SKILL.md:19-20` | EDIT: current inventory pair; Kimi → 6.7.0. (`SKILL.md:12` is self-labeled "historical, verified 2026-10-13" → NO-CHANGE, compliant) |
| 10 | `SCORECARD.md:58-59` | EDIT or SUPERSEDE: living `## Open gaps` bullet in the maintained section (:51-84, not the frozen :39-49 block); one-token fix or a superseded marker |

**EDITABLE — outside declared scope (4 files, 7 loci; one decision each):**

| Locus | Decision |
|---|---|
| `MINT.md:10` | EDIT pin + wrong-client pairing ("registered for Devin" after 6.4.0) or mark the mint record historical. Mint record edited once since seed (`e0b821e`, 2026-10-13); no freeze marker found |
| `corpus/QUALITY.md:18` | EDIT criterion #8's parenthetical to a version-agnostic example, or NO-CHANGE-with-cause (the parenthetical illustrates *what* to pin, not the current value) |
| `corpus/lessons/2026-10-15-round-1.md:82` | APPEND-ONLY NOTE (round-1 precedent: the :152 correction note at EOF) or NO-CHANGE-with-cause under the baseline-revision convention (:7). Claim "still pins 6.4.0" + dead pointer `:1287`. Not named by any round-2 seat |
| `corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80` | APPEND-ONLY ERRATA (precedent: `## Errata (round 2)` tail already exists at :82) or NO-CHANGE (dated entry) |
| `corpus/knowledge/2026-10-13-mcp-registrations.md:88` | APPEND-ONLY ERRATA: the erratum's corrected pointer `config.toml:1284`/`1287` is dead at HEAD (stanza :2938/:2940). A stale pointer *inside a correction record* is the worst form — it claims to be the fix |
| `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43` | APPEND-ONLY ERRATA or NO-CHANGE: pointer `:1284-1292` dead at HEAD; entry is dated 2026-10-13 |

**FROZEN — NO-CHANGE (must not be edited; scope-out sentence required):**

- `LOG.md` — all 19 version loci, incl. `:21`-class historical claims and
  `:1005-1006` (the refutation record). Append-only history.
- `SCORECARD.md:291, :302-304, :530, :534, :537, :620` — round-dated luna
  sections, historical by construction. `SCORECARD.md:39-49` frozen table
  (`:266-267`). The `:698` carried-debt sentence already states the live
  value and needs no edit.
- `corpus/knowledge/*` dated evidence cells generally (e.g.
  `2026-10-16-l8-01-6p4-symmetry-battery.md:1,5,7,11,13` — round-dated
  battery entry; `corpus/README.md`'s 32 `REA 6.4.0` provenance cells and
  `:74`/`:153` pin rows) — historical evidence cells stay byte-identical per
  the claim's own limb; they need the **scope-out sentence**, not edits.
- `SHONEN.md:12` — names 6.5.0/207/v42 as a *contestation record*, not a pin
  statement. NO-CHANGE.
- `.ufo/waves/*`, `.ufo/reports/*` — prior-round read-only records.
- `evidence/round-1-2026-10-15/*` — zero version tokens (verified above).
- Root `README.md`, `AGENTS.md`, `EXAMPLE.kama.md` — zero version hits.

**Special case:** `corpus/README.md:46-68` (32 `REA 6.4.0` cells) — these are
per-entry provenance ("REA 6.4.0 (warm cache)"), dated 2026-10-13/14. They
are historical evidence cells; the round-1 precedent is that the *claim*
states its scope and the cells stay byte-identical. They must appear in the
scope-out, or the repo-level count silently fails.

## 4. Answer to the seat's question — which version statements could the sweep miss

**Miss class A — files outside the enumerated set.** `MINT.md:10`;
`corpus/QUALITY.md:18`; `corpus/lessons/2026-10-15-round-1.md:82`;
`corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88`;
`corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43`. Round-1's LOG
record named only PROVINCE/SKILL/SCORECARD for correction; the round-2
executor drafts (E18/E19) keep that scope. If the claim means "every
current-surface version/pin statement in the repo", these are counterexamples;
if it means the three files, the claim text must say so (as round-1's C1 had
to, per `CR5.md` round-1 §4-§6).

**Miss class B — no-version-token statements.** `PROVINCE.md:11` (cache-count
"Both versions"), `:21` (cache path), `:22` (digest), `:24` (skill v37
continuation), and count-only forms ("127 commands" at `:45`, "170/127" at
`SCORECARD.md:58`). A `6\.[457]\.0` sweep misses every one; only a
multi-needle sweep (digest prefixes, cache dir names, counts) or a read
passes.

**Miss class C — continuation lines / wrapped paragraphs.** The client token
and the value token can be on different lines: `SKILL.md:19` ("…; Kimi") +
`:20` ("`rea-agents@6.4.0` …"); `PROVINCE.md:17-18`; `SCORECARD.md:290-291`.
Proven below.

**Miss class D — pointer-class loci (no version token at the pointer).**
Seven `config.toml:NNNN` pointers; five dead at HEAD (`:1284,:1287,:1288,
:1292,:1478`). A version census that ignores pointers leaves a stale family
counted at zero.

**Miss class E — frozen loci that *assert* rather than record.** `LOG.md:21`'s
class (round-1 finding) plus `LOG.md:458,:463,:522,:656-672` etc. — all
frozen. The census needs an explicit scope-out, not silence; round-1's LOG
record did exactly this (`LOG.md:1010-1014`).

## 5. Instrument holes — each proven by execution

**(i) Line-scoped client+version grep misses continuation lines.**

```
$ git grep -nE 'Kimi.*6\.4\.0|6\.4\.0.*Kimi' -- SKILL.md
rc=1                      # ← the real stale pair SKILL.md:19-20 NOT matched
$ sed -n '18,20p' SKILL.md
Current REA package inventory by configured client (2026-10-16): Devin/OMP
`rea-agents@6.5.0` (207 MCP tools / 153 CLI commands); Kimi
`rea-agents@6.4.0` (170 MCP tools / 127 CLI commands).
```

**(ii) Case sensitivity.** `corpus/lessons/2026-10-15-round-1.md:82` reads
"`~/.kimi-code/config.toml:1287` still pins 6.4.0" — lowercase `kimi`:

```
$ git grep -nE 'Kimi.*6\.4\.0|6\.4\.0.*Kimi' -- corpus/lessons/2026-10-15-round-1.md
rc=1
$ git grep -niE 'kimi.*6\.4\.0|6\.4\.0.*kimi' -- corpus/lessons/2026-10-15-round-1.md
corpus/lessons/2026-10-15-round-1.md:82:`~/.kimi-code/config.toml:1287` still pins 6.4.0. …
```

**(iii) Unanchored `6\.x\.y` false-positives.**

```
$ git grep -nE '6\.[0-9]+\.[0-9]+' -- PROVINCE.md SKILL.md | grep -E '26\.6\.4'
PROVINCE.md:123: … REA_UNBLOB_COMMAND=~/.local/bin/unblob (26.6.4) …
SKILL.md:57:| Firmware blob | `inspect-firmware-regions` (binwalk 3.1.0), `extract-firmware` (unblob 26.6.4) | …
$ git grep -nE '\b6\.[0-9]+\.[0-9]+' -- PROVINCE.md SKILL.md | grep -E '26\.6\.4'
rc=1                      # ← \b anchor eliminates the class
```

The 38-line raw count is 36 real after removing these two FPs. Any landed
census must anchor (`\b6\.[0-7]\.0\b`) or it over-counts by 2.

**(iv) The `rea-agents@`-only instrument under-counts by 26 lines.**

```
$ comm -13 <(git grep -nE 'rea-agents@' -- PROVINCE.md SKILL.md SCORECARD.md | cut -d: -f1,2 | sort) \
           <(git grep -nE '\b6\.[457]\.0\b' -- PROVINCE.md SKILL.md SCORECARD.md | cut -d: -f1,2 | sort)
PROVINCE.md:19,:20,:24,:26,:44,:67,:125; SCORECARD.md:58,:59,:289,:291,:302,:303,:304,
:463,:467,:471,:496,:500,:503,:530,:534,:537,:549,:619,:620
```

Including `SCORECARD.md:58` and `PROVINCE.md:44` — two of the ten
current-surface loci. Neither the pure pin-token nor the pure value-token
instrument alone yields the correct count; the union (with `\b`, `-i`,
continuation-aware classification) does.

**(v) The sweep must be re-run *after* the edits.** Round-1's r3 census
command (S2's) was proven to have a false-PASS mode when the drafter's
wording changed (`CR5.md` round-1 §2.5, variants A/B/H/I). The same trap
applies here: an edit that writes "Kimi 6.7.0" on `:10` while leaving the
digest continuation `:11` untouched still yields a stale claim invisible to
the token sweep. The verification command must assert **both** the version
tokens AND the digest/cache-path needles, or state that it is a guard only.

## 6. Verbatim block for the parent (land as-is if used)

```text
C1 census definition (frozen for this round) — three-file scope, stated:

Scope: "stale Kimi-pin statements" means current-surface version/pin
statements in PROVINCE.md, SKILL.md, and SCORECARD.md's living sections
(:1-234 and :615-710; round-dated `## luna-round-*` sections and the frozen
2026-10-15 table :39-49 are historical by construction). Measured
independently by CR5 at HEAD 165057e: 10 statement groups
(PROVINCE.md:10, :11, :18, :21, :22, :44, :45, :67; SKILL.md:19-20;
SCORECARD.md:58-59). SKILL.md:12 is already marked "historical, verified
2026-10-13" → compliant, no change.

Scope-outs (named, not counted, not edited):
- LOG.md — append-only history (19 version loci incl. :1005-1006, which
  records the 6.7.0 refutation). Non-endorsement/correction only via new
  append-only entries.
- SCORECARD.md:291,:302-304,:530,:534,:537,:620 — round-dated luna sections;
  :39-49 frozen table. :698 already states the live value.
- corpus/README.md's dated provenance cells (32 `REA 6.4.0` rows incl.
  :74,:153) and corpus/knowledge/* dated evidence cells
  (e.g. 2026-10-16-l8-01-6p4-symmetry-battery.md:1,5,7,11,13) — historical
  evidence cells stay byte-identical.
- SHONEN.md:12 — names 6.5.0/207/v42 as a contestation record, not a pin.
- .ufo/waves/* and .ufo/reports/* — prior-round read-only records.
- evidence/round-1-2026-10-15/* — zero version tokens (verified).

Outside-scope loci (one decision each; repo-level N is NOT zero without
them): MINT.md:10 (stale pin + wrong-client pairing); corpus/QUALITY.md:18
(criterion #8 parenthetical); corpus/lessons/2026-10-15-round-1.md:82
("still pins 6.4.0" + dead pointer :1287 — append-only note precedent:
round-1's EOF note); corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80
(pin claims) and :88 (erratum whose corrected pointer :1284/:1287 is dead —
stanza now :2938/:2940); corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43
(dead pointer :1284-1292).

Pointer family (separate needle, separate count): seven `config.toml:NNNN`
pointers repo-wide; five dead at HEAD (:1284,:1287,:1288,:1292,:1478;
stanza :2938/:2940). Repair or scope each.

Sweep instrument (fix before landing):
  git grep -niE '\b6\.[0-7]\.0\b|rea-agents@|25802f6d|805433f1|af39310c|dea9475797100b20|ad9a3fdbcad992c6|a1722018f28f9df2|config\.toml:[0-9]+' -- <scope>
- \b anchor: without it, unblob 26.6.4 (PROVINCE.md:123, SKILL.md:57) is a
  false positive (proven).
- -i and multi-needle: PROVINCE.md:11,:21,:22 carry the stale claim with no
  version token; lessons:82 uses lowercase "kimi".
- line-scoped client+version greps MISS the real SKILL.md:19-20 pair
  (rc=1 proven) and PROVINCE.md:17-18 — classify by reading, not by regex
  adjacency.
- Post-edit assertion: the digest/cache needles must ALSO return zero stale
  hits, or a partially-edited paragraph false-passes.
```

## 7. Conclusions, labeled

**Observations** (ran/read this session): the live pin `:2940` = 6.7.0 and
dead pointers at `:1478`/`:128x`; the 38/36-line three-file sweep counts and
the 26-line comm gap; SCORECARD section boundaries and the living-vs-frozen
`:51-84`/`:39-49` split; the seven outside-scope loci read at their lines;
the zero-hit scans of `evidence/`, root `README.md`, `AGENTS.md`,
`EXAMPLE.kama.md`; all five instrument demonstrations (rc=1 on line-scoped
greps ×2, FP + `\b` elimination, comm under-count, receipt self-check rc=0);
the absence of every one of the four outside-scope files from every round-2
seat report (three greps returning empty).

**Inferences:** (1) with the declared three-file scope the census is
completable (10 groups, each with a named edit); (2) the claim's natural
reading leaves repo-level N ≥ 7 unless the four outside-scope files get
decisions or a scope-out; (3) the sweep as drafted under-counts without the
digest/cache/pointer needle families and over-counts without `\b`; (4) the
`mcp-registrations:88` erratum and `lessons:82` are the two loci where a
"historical by construction" defence is weakest — both read present-tense and
neither is named by any round-2 seat.

**Unknowns:** (1) whether the parent freezes N over the three files or the
repo — this choice, not the sweep, decides the claim; (2) whether MINT.md
and corpus/QUALITY.md are treated as living (editable) or as dated records;
(3) whether `PROVINCE.md:67` is a policy sentence (NO-CHANGE) or a stale
statement (S1:134 vs R1:93 disagree; both positions are evidenced);
(4) the post-battery closing state of the five custody paths — my captures
are mid-battery, not the parent's closing capture.

## 8. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
grep -n 'rea-agents' /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json
sed -n '1478p;2938,2943p' /home/vgpnk/.kimi-code/config.toml; wc -l /home/vgpnk/.kimi-code/config.toml
git grep -nE 'rea-agents@|\b6\.[457]\.0\b' -- PROVINCE.md SKILL.md SCORECARD.md
git grep -nE 'Kimi.*6\.4\.0|6\.4\.0.*Kimi' -- SKILL.md corpus/lessons/2026-10-15-round-1.md   # rc=1
git grep -niE 'kimi.*6\.4\.0|6\.4\.0.*kimi' -- corpus/lessons/2026-10-15-round-1.md
git grep -nE '6\.[0-9]+\.[0-9]+' -- PROVINCE.md SKILL.md | grep -E '26\.6\.4'   # FP without \b
git grep -nE 'config\.toml:[0-9]+' -- . ':(exclude).ufo'
grep -nE 'mcp-registrations|r4-16|:1287' .ufo/waves/arc2-loop1-round2/*.md      # empty / E9-only
grep -rnE 'rea-agents|6\.[457]\.0' evidence/                                    # empty
tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
```

## 9. Convergence note

- **Corroborated by other round-2 seats (not novel here):** the ten-file
  current-surface classification overlaps `E17.md:39`, `E18.md:95-110`,
  `E19.md:107-114`, `E2.md:167-171`, `E7.md:216-226`; `R1.md:25,30,100`
  independently names `MINT.md:10`, `corpus/QUALITY.md:18`, and the
  `PROVINCE.md:11,:21,:22` no-token class.
- **Unique to this seat (verified absent from every round-2 report by grep):**
  the `corpus/lessons/2026-10-15-round-1.md:82` locus;
  `corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88` and
  `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43`; the five
  instrument proofs (§5) with their exact outputs; the living-vs-frozen
  section-boundary evidence for `SCORECARD.md:58`; the pointer-family count
  (seven, five dead).
- **Repo state at my final check:** HEAD `165057e` unchanged;
  `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/` only; no
  round-2 edit had landed when I finished, so every before-state above still
  describes HEAD. Cross-seat line pointers were re-verified at my read time;
  treat them as movable.
