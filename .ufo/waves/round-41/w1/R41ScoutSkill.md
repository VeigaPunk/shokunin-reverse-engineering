DONE — placement recon for R41 at base `49096c7e6f226af0c750c4b003be58883cb6049f`: every insertion point, the command-A resolution rules (simulated on a sandbox clone, 14 variants), and copyable templates are below. No REA/unblob/extractor was run, nothing installed, no VCS mutation in the lane (the one commit-capable use was a `--shared` sandbox clone under scratch, fixture identity, toplevel asserted).

Artifacts (`.ufo/waves/round-41/w1/artifacts/R41ScoutSkill/`): `command-A-verbose.py` (SCORECARD recipe A verbatim + `bad_rules` list), `sim-block20.py` + `sim-block20.out.json` (the 14-variant simulation), `block-20-template.md` (skeleton with citation slots).

All line numbers are at base; `git rev-parse HEAD` = `49096c7e…`. Observed unless marked [INFERENCE].

## 1. SKILL.md — where rule block 20 goes

| fact | value |
|---|---|
| `## Queue-drain craft (rounds 5-12, distilled in round 13)` heading | `SKILL.md:81` |
| block 18 (table v1) | `:316-346` (prose :316-334, table :336-346) |
| block 19 (table v2) | `:348-374/375`: prose `:348-359`, v2 marker `:361`, actions line `:362`, header `:363`, separator `:364`, rows `:365-375` (last row `clean-empty` `:375`) |
| blank lines | `:376-379` (four blanks), then `## Config custody for live-probe rounds (SOP)` at `:380` |
| craft span used by SCORECARD/SHONEN | `SKILL.md:81-375` (last non-blank line 375) |
| file length | 1405; last heading `### Round-40 instrument registry` at `:1388` |

**Insertion:** gap after line 375: one blank line, then block 20 as a column-0 `- **…` bullet whose continuation lines are indented two spaces (same as 316/348); keep the existing 4 blanks before `:380`. In hashline: `PUT >375:` with body `+` (blank) then `+- **SquashFS `extract-firmware` outcome triage v3 (round 41).** …`. New last non-blank line = 375 + 1 + N (N = lines in block 20); block 20 starts at 377. Re-read SKILL.md for a fresh `#TAG` (the one I saw, `#36C7`, is a partial read).

**Pointer sentence precedent:** block 18 prose says "Superseded for routing by rule block 19 (table v2, round 40); this v1 table stays as the round-39 record" (`:331-334`). Do the same inside block 19's prose (`:357-359`, before the marker at :361): "Superseded for routing by rule block 20 (table v3, round 41); this v2 table stays as the round-40 record". Edit prose only: the round-40 interpreter/counter compare the table block (marker line through last row), not the prose (`tools/round-40/c2-counter.py:449-452`, `table_block` docstring "Marker line through the table's last row"). Keep block 19's `:361-375` byte-identical. If the sentence adds lines it shifts block 19's rows, so add it first, then compute the span.

**Shift effect:** only lines ≥ 376 move (by N+1). Live pointers into SKILL.md at ≥ 376: none. The only ones are two stale historical pointers inside SKILL itself (`SKILL.md:1007` cites `SKILL.md:411-412` and `:894`, already not matching their targets). Pointers that must be re-stated: `SHONEN.md:6` (`SKILL.md:81-375`, "19/19"), `SCORECARD.md:24` observable cell and evidence cell (below). Pointers ≤ 375 (`:316-343`, `:348-375`, `:81-343`) stay valid.

**Interpreter hazards for block 20's prose (from `tools/round-40/sqfs-triage-v2.py:380-413` / `parse_actions_line`):** the parser takes the FIRST line in the craft span containing the marker, then the first line starting with `|` after it, then requires the `<!-- sqfs-triage-actions: … -->` line immediately above that table (skipping blanks). So in block 20: never write the literal marker string `<!-- sqfs-triage-table v3 -->` in prose before the real marker line; no line starting `|` before the real table; vocabulary line directly above the header, tokens lowercase-dashed, unique. Block 19's literal v2 marker is only at :361 (prose :348-359 does not quote it) so adding v3 does not disturb the v2 parse. Columns v2 = 12 fixed (`HEADER`, `sqfs-triage-v2.py:~130`); v3 needs its own interpreter (the draft's "no contains-operator" control implies a new set-contains cell form).

## 2. SCORECARD command A — what counts and what resolves

Recipe at `SCORECARD.md:88-124` (`## Measurement recipes` A). Mechanics, verified by running it at base (`command-A-verbose.py HEAD`): `knowledge_files 130, mapped 130, missing [], dangling [], rule_blocks 19, citation_resolved_rules 19, coverage 10.0, depth 10.0`.

- **rule block** = a chunk of the craft section (text between `## Queue-drain craft ` and the first `\n## `) split on `(?m)^- \*\*` — i.e. any column-0 `- **`. Table rows (indented) and the table never split. Craft chars at base 27847.
- **resolved** = block has ≥ 1 match of `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?` AND for every match the file exists at REV (`git show REV:corpus/knowledge/<name>`) AND `1 <= first <= last <= len(file.splitlines())` (a bare `.md` with no range is checked as line 1). All matches must be valid, not just one.
- **coverage** = stems of every `corpus/knowledge/*.md` at REV vs `2026-10-\d{2}-[a-z0-9-]+` matches inside README `## Coverage map` (section = after `## Coverage map\n` to the next `\n## `, i.e. README lines 11-96). `missing` = file with no mention; `dangling` = mentioned stem with no file.

Simulation (`sim-block20.py`, sandbox clone, base + candidate block + stub entries, each variant its own commit; output `sim-block20.out.json`):

| variant | files/mapped | rules / resolved | result |
|---|---|---|---|
| P0 base | 130/130 | 19/19 | green |
| P1 block 20 citing a committed `r41-sqfs-triage-v3.md` (60 lines) at `:11-18`,`:19-26` + README row | 131/131 | 20/20 | green |
| N1 entry committed, no README row | 131/130, missing `[r41-sqfs-triage-v3]` | 20/20 | coverage breaks |
| N2 range `:11-40` on a 30-line entry | 131/131 | 20/19, bad=[20] | depth breaks |
| N3 reversed range `:26-19` | — | 20/19 | depth breaks |
| N4 entry file not in the commit but README/cite present | 130/130, dangling `[stem]` | 20/19 | both break |
| N5 block with no `corpus/knowledge/…` citation | — | 20/19 | depth breaks |
| N6 a second col-0 `- **` bullet inside the block | — | 21/20 | it counts as a 21st block (uncited → unresolved) |
| N7 a `## ` line inside the block | — | 20/20 | silently truncates craft there: everything after it (incl. later citations and the real `## Config custody` boundary logic) leaves the measurement — green but vacuous |
| N8 citation path wrapped across a newline | — | 20/19 | not matched |
| N9 uppercase in cited name | — | 20/19 | `[a-z0-9-]` truncates the match, file missing |
| N10 README maps `2026-10-26-r41-avm-be-squashfs-core` with no file | dangling | 20/20 | coverage breaks |
| N11 table-cell style `knowledge 2026-…md :11-18` (how block 19's table rows cite) | — | 20/19 | not counted (only the prose cites count) |
| P2 block citing only the older `r40-sqfs-triage-v2.md:11-18`, v3 entry absent | 131/131 | 20/20 | green — command A does NOT prove block 20 cites the v3 entry; the C2 predicate/counter must check that itself |

Rules for block 20 so it resolves: every citation is `corpus/knowledge/<lowercase-name>.md:<a>-<b>` on ONE line, cite only entries committed at or before REV, ranges within the entry's final line count (cite after the entry is final; the v3 entry's line count at the freeze is what the freeze-time command A sees), no col-0 `- **` and no `## ` inside the block. Keep the table-cell style `S112 :44-50` for the table's source column (not counted, harmless).

**Expected counts after R41 (two entries per the draft: `r41-avm-be-squashfs-core`, `r41-sqfs-triage-v3`):** coverage `132/132`, rule blocks `20/20`. The freeze itself reads 131/131 if only the C2 entry lands there (as in round 39: 127/127 at freeze).

**Calendar hazard:** the map regex is `2026-10-\d{2}-…`. Entries dated 2026-11-xx are invisible to the mapped set (permanent `missing`). Today is 2026-10-26, so keep the `2026-10-NN` stems; flag if the round crosses 2026-10-31 [INFERENCE from the regex; not run with a November stem].

## 3. PROVINCE.md — Round-41 additions and frontier note

`PROVINCE.md` has 394 lines (ends with a newline). `:386` `## Round-40 measured, not promoted (R40-C1 honest stop)`, `:388` intro, `:390-392` table, `:394` Round-40 frontier note (last line). Round-39 pattern (`:378-384`): heading, blank, 4-col table (`Surface | Ports / keys | Probe | Verified evidence`), blank, "Round-39 frontier note, 2026-10-26: …" paragraph. Append with `PUT >394:`:

```
(blank)
## Round-41 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`, AVM layout: big-endian fields, little-endian metadata/data block-length headers, `mkfs_time == bytes_used`) | no new REA key — unblob 26.6.4 runs `sasquatch-v4be` without `-be` when the AVM marker holds; `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1; `extract-firmware --max-depth 1` | `extract-firmware` (rea-agents 6.5.0) on four frozen carriers — V3 <FRITZ!Box 5490 07.31 member>, V4 <5491 07.31 …>, L3/L4 lane-built xz/gzip with nested-name collisions (vendor bytes fetched by `tools/round-41/fetch-vendor.py`, never committed) | every oracle regular file published at its exact extract-root path (<n>, <n>, <n>, <n>), <gap summary>, no failed chunk; receipts `corpus/evidence/round-41/c1/`; counter `tools/round-41/c1-counter.py` (exact-path matching, rerun binding); entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` |

Round-41 frontier note, 2026-10-26: AVM-layout BE SquashFS v4 is **Core** for the layout and carriers above, superseding `## Round-40 measured, not promoted (R40-C1 honest stop)` (the round-40 row's "measured, not promoted") and the AVM sentence of the round-39 frontier note ("AVM-BE bodies … stay Frontier") (`2026-10-26-r41-avm-be-squashfs-core`). Still Frontier: LE AVM members (`hsqs`), AVM kernels, nested `filesystem_core` images below depth 1 (<edit to match the measured result>), other vendor-mangled images.
```

Pointer sites to touch (round 39 did the same, `LOG.md` round-39 final-commit note): `:157` (the bracketed history on the `- **sasquatch**` bullet; append "Round 41: AVM-layout BE v4 is Core — see `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); …"; in-place extension of an existing line, no line shift), `:384` (round-39 note's last sentence "AVM-BE bodies and vendor-mangled images stay Frontier" — append "Round 41: AVM-layout BE superseded by `## Round-41 additions to Core` below."), and `:394` (round-40 note's last sentence — same pointer). The round-38 note at `:376` is the precedent for this wording ("Round 39: superseded … by `## Round-39 additions to Core` below (`…`)"). The draft's `## Round-41 additions to Core` + frontier-note names are a `PROVINCE.md` string check; keep the exact heading text and the words "Round-41 frontier note". The Core table at `:44-62` is not rewritten (rounds 30/31/32/36/39 all append). `## Frontier` (`:73-95`) has no sasquatch line; nothing to edit there.

## 4. corpus/README.md and the root README

Root `README.md` (24 lines) has no coverage map or frontier — nothing to edit. `corpus/README.md` (273 lines):

| section | lines | append point | format |
|---|---|---|---|
| `## Coverage map` (3-col `section | entries | state`) | 11-96 | after `:96` (the round-40 AVM row) | `| <title> (round 41) | \`2026-10-26-r41-avm-be-squashfs-core\` | **Core** — … |` |
| `## Knowledge` index (4-col `entry | what | sources | date`) | 98-208 | after `:208` | `| \`2026-10-26-r41-avm-be-squashfs-core\` | … | S12x…; receipts \`corpus/evidence/round-41/c1/\` | 2026-10-26 |` |
| `## Lessons` (3-col `lesson | round | summary`) | 210-239 | after `:239` (`round-40` row) | `| \`round-41\` | 41 | … ; QUALITY 84 |` |
| `## Frontier` bullets | 241-255 | after `:251` (the round-40 `sasquatch-v4be` line), before `:252 - adb device surface …` | see below |

Coverage-map rows (exact prefix format of `:95-96`):
```
| Genuine AVM-layout big-endian SquashFS v4 through REA (round 41) | `2026-10-26-r41-avm-be-squashfs-core` | **Core** — `extract-firmware --max-depth 1` publishes every oracle regular file at its exact extract-root path on four fresh frozen carriers (V3 FRITZ!Box 5490 07.31 member, V4 <…>, L3 xz, L4 gzip with nested-name collisions in both directions); gaps only as the frozen rule allows; supersedes the round-40 "measured, not promoted" state; LE AVM members and AVM kernels stay Frontier |
| SquashFS `extract-firmware` outcome triage v3 (round 41) | `2026-10-26-r41-sqfs-triage-v3` | held as SKILL rule block 20: table v3 labels combined gap sets (partial failure + symlinks, depth-limited + symlinks) and adds `depth-limited-nested`; scored on a freeze-seeded held-out set against labels from a frozen independent evaluator |
```
Both stems must be spelled exactly once as `2026-10-26-…` (no `.md`) inside `:11-96`, and both files committed at or before REV, or command A reports `missing`/`dangling` (N1/N10).

Frontier line (format of `:249-251`; round-40 line is `:251`):
```
- sasquatch-v4be — 2026-10-26 round 41: genuine AVM-layout BE v4 is **Core** (`2026-10-26-r41-avm-be-squashfs-core`), superseding the round-40 line above (measured, not promoted). Still frontier: LE AVM members (`hsqs`), AVM kernels, nested `filesystem_core` images below depth 1, other vendor-mangled images.
```
The older bullet `:247` (`- sasquatch (AUR) …`) and `:248` are kept as history (dated-note-on-the-line-above idiom); do not rewrite them.

## 5. SCORECARD.md — capability row, owned-axes cells, round section

- **Capabilities** table `:615-630` (header `:617` `| Capability | What it can now do | Evidence pointer | First-working round |`; last row `:630` = executable triage v2; `:631` blank; `:632` "Rows entered through rounds…"). Append with `PUT >630:`. Row shape (4 cells; round-40 row's last cell is `40`, round-36's `round-36`):
```
| executable SquashFS `extract-firmware` outcome triage v3 (combined gap sets, independent labels) | a frozen interpreter (`tools/round-41/sqfs-triage-v3.py`) reads one machine-readable SKILL table (rule block 20) and returns the (label, action) pair for an REA envelope including combined gap sets and `depth-limited`; scored against labels from a frozen independent evaluator | `python3 -I -B tools/round-41/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>` → <n>/<n>, exit 0 (`.ufo/waves/round-41/l1/scores/c2-at-<REV8>.json`) | 41 |
| AVM-layout big-endian SquashFS v4 recursion (`squashfs_v4_be`, AVM layout) | `extract-firmware --max-depth 1` publishes every regular file of an independent oracle at its exact extract-root path on genuine AVM-layout BE v4 images (marker `mkfs_time == bytes_used`, little-endian block lengths), with one `unpublished-entry` gap per in-tree symlink and a `depth-limited` gap; LE AVM members, AVM kernels and extracted programs not claimed | `PROVINCE.md` `## Round-41 additions to Core`; entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`; `python3 -I -B tools/round-41/c1-counter.py …` → 4/4, exit 0 | 41 |
```
(only enter the AVM row if R41-C1 is met — round 40 entered none because it stopped, `SCORECARD.md:3445`.)
- **Owned axes** `:23` coverage and `:24` depth: prepend the round-41 clause to the observable cell (existing style: "130/130 knowledge files mapped after the round-40 landing (two entries added and mapped: `corpus/knowledge/…`, …; command A at `<rev>`, `missing []`, `dangling []`, …)"); depth: "20/20 queue-drain rule blocks … (round 41, command A, new block 20 at `SKILL.md:377-<end>` with table v3; …)". Last cell "count refreshed rounds 25, 26, 31, 36, 38, 39 and 40" (`:23` end) and "…25, 26, 39 and 40" (`:24` end) → add 41.
- **Stale cell found (calibration):** `SCORECARD.md:24` evidence column still reads "craft section `SKILL.md:81-343` (heading line 81, last non-blank line 343 at `52b0eb29` … ); command A; measured `52b0eb29…` (round 39 …)" although round 40 moved the span to 375 (`SHONEN.md:6` and `:24`'s observable cell say 375). Round 41 should re-state it to `SKILL.md:81-<new end>` at the measured rev.
- **Round section:** append at EOF `:3452` (`- **retired:** none.` at `:3452`; file ends with `\n`), heading `## Round 41 — <title>`, opening line `Base \`49096c7e…\`; freeze \`<…>\` (…)`, then the 7-col table `| claim | axis / surface | before | after | counting command | measured at | verdict (author) |` with `R41-C1` / `R41-C2` rows (copy the `:3440-3443` shape: "before" = the freeze-time exit codes of the counters, "after" = the scored receipts with paths under `.ufo/waves/round-41/l1/scores/`), an `Owned scores:` paragraph (coverage `130/130 → 132/132`, depth `19/19 → 20/20`, command A at the landing rev), `### Wave-2 falsification record`, and `- **planned (round 42):** …` / `- **retired:** none.` bullets. The existing `planned (round 41, after a steer)` bullet at `:3451` is discharged by naming it in the new section (round-39/40 precedent), not edited.

## 6. LOG.md entry format

`LOG.md` has 3162 lines; last section `## 2026-10-26 — round 40: genuine AVM-layout BE SquashFS measured but not promoted (R40-C1 honest stop, 3/4); SKILL triage table v2 met 26/26 (R40-C2)` at `:3153`, bullets to `:3162`, file ends with a newline. Append (`PUT >$`), one blank line before the heading:
```
## 2026-10-26 — round 41: <C1 result in one clause>; <C2 result in one clause>

- **Claims** (`plans/round-41-claims.md`, frozen `<7 hex>`): R41-C1 coverage — genuine AVM-layout big-endian SquashFS v4 Frontier → Core on four fresh carriers (V3/V4 vendor, L3/L4 lane-built with nested-name collisions) under a counter with exact extract-root path tests (routed R40-CL1) and a bound `member_sha256` (R40-CL6); R41-C2 depth — SKILL rule block 20, triage table v3, scored against a frozen independent evaluator (routed R40-CL5, closure D3).
- **Motivating evidence:** `corpus/lessons/round-40-verifier-spotcheck.md` §5 and `corpus/lessons/round-40.md` `## Routed defects into round 41`.
- **Controls before data** (`<rev>`): …
- **Data:** …
- **Scores at `<rev>`** (`.ufo/waves/round-41/l1/scores/`): …
- **Re-verification (freshness):** …
- **Wave 2** (<n> seats): …
- **Frontier step:** SOURCES 126 → <n> (S127…); QUALITY 84; SKILL `### Round-41 instrument registry`.
```
Round-40's bullet labels are exactly `Claims`, `Motivating evidence`, `Controls before data`, `Data`, `Scores at …`, `Re-verification (freshness)`, `Wave 2`, `Frontier step`; round 39 adds `Surfaces`, `Sources`, `Assimilation`, `Tool installs` bullets (close the entry with a "No tools installed or updated" or a `Tool installs:` line, as rounds 35/36/38/39 did).

## 7. Other round-41 touch points found while mapping

- SKILL tail: append `### Round-41 instrument registry` after `:1405` (format = `:1388-1405`: one intro paragraph, then the table `| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |`; r40's prose names the freeze rev and `score-receipt.sh`).
- SKILL `:1334` ("Big-endian and AVM SquashFS … not claimed", round-36 limits) is historical; round 39/40 left it; add a dated pointer only if the L1 wants the section self-consistent.
- SHONEN `:6`: restate `SKILL.md:81-<end>` and `20/20` (the only SHONEN count-bearing cell; `:7-11` carry the other boxes).
- SOURCES: last rows S123-S126 at `corpus/SOURCES.md:129-132` (11 columns: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`); the next id is S127 if no sibling takes it first (collision check is the L1's; I did not read the staged lead ids).
- The knowledge-index rows and the LOG/SCORECARD texts all require the entries to exist at REV before command A runs (N4).

## 8. Draft attack notes from the placement angle (calibration: unverified beyond the reading below)

1. The draft's rule 7 names a new label `depth-limited-nested` but no action token. Table v2's closed vocabulary (`SKILL.md:362`) has none for it: the v3 vocabulary line needs a new token, and the draft's claim (C2 "(label, action)") should name it before the freeze (otherwise the evaluator and the table choose independently).
2. v2 gap-set cells are EXACT set equality (`_parse_set_cell`: `a+b` = exactly {a,b}; `*` any; `none` empty — `sqfs-triage-v2.py:245-258`). The combined classes need either one row per exact combination or a new contains operator; the draft's "no contains-operator" control presupposes the latter, so the v3 interpreter is a new grammar and block 19's table cannot be transcribed unchanged.
3. Precedence 3 (`missing-extractor-dependency` ∈ G) is silent when D names neither or both extractors, and precedence 5 reads the singular "handler `squashfs_v4_be`" while H is a set — the independent evaluator needs those spelled out or it will diverge from the generator for reasons unrelated to the table.
4. Command A cannot prove block 20 cites the v3 entry (P2); and `SCORECARD.md:24` already carries a stale span (§5).
5. Block 20 must not contain the literal v3 marker in prose, nor a column-0 `- **` (N6) nor a `## ` line (N7); the C2 counter's "table bytes equal freeze bytes" is on the marker-to-last-row block, so prose-only repairs (R40-CL5 M1–M3, L1–L6) do not trip it.

## Commands and limits

- Recipe A run: `python3 command-A-verbose.py HEAD` (cwd lane) → the JSON quoted in §2, exit 0. Simulation: `python3 -I -B sim-block20.py "$D/lane"` (D = `mktemp -d` under `$S`, `git clone --shared`, toplevel asserted) → `sim-block20.out.json`, exit 0 (one expected `fatal: path … does not exist` line from N4 on stderr).
- Limits: the block-20 variants use stub entries and placeholder blocks — they test command A's mechanics, not a real table; the sandbox did not run the round-40 interpreter or counters. Line numbers hold only until a sibling commits to these files; re-read before editing. The November-stem hazard is read from the regex, not run. [INFERENCE] markers: expected counts 132/132 and 20/20 assume both draft entries land; PROVINCE pointer wording follows round-38/39 precedent.
- No tools installed or updated; no REA, unblob or extractor run; no reserved carrier read; scratch `/fast/scratch/hyaku/kaidoku-r41/R41ScoutSkill` removed at exit.
