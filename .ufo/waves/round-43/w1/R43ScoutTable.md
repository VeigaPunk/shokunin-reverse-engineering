DONE — v4 table region pinned and byte-identical at base `6b9e64fe` and round-42 freeze `d1681696`; safe insertion points, byte ranges and every landing-edit format given below; one draft-text inconsistency flagged for the L1 (C2 copy destination).

All line numbers are 1-indexed in `git show <rev>:<path>` (LF endings; base SKILL.md = 1568 lines, corpus/README.md = 285 lines, SCORECARD.md = 3487 lines). Region bytes and contexts staged under `.ufo/waves/round-43/w1/artifacts/R43ScoutTable/`.

## (1) v4 table region — exact placement and hashes

Definition per draft P43-C1: "from the line containing `<!-- sqfs-triage-table v4 -->` through the end of the first markdown table after it".

| rev | marker line | table lines (header→last row) | region lines | sha256 | bytes |
|---|---|---|---|---|---|
| `6b9e64fe7e0de202d9383baad5792fbfe039a743` | **521** | 523–539 (header 523, `|---|` 524, 15 data rows 525–539) | **521–539** | `99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da` | 13 857 |
| `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` | **521** | 523–539 | **521–539** | `99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da` | 13 857 |

- **Byte-identical: YES.** Identical sha256 over the identical line range.
- Region = marker (521), `sqfs-triage-actions` comment (522), header (523), separator (524), rows 525–539 (`container-depth-limited` … `clean-empty`). Byte range `[54685, 68542)` in the blob.
- Including the three trailing blank lines (540–542) gives sha256 `b967a30dd4db7f3c88f50190f6499b280266b24cd7ddeb098574987a3ac4ccbd` (13 860 B) — same hash both revs.
- Whole-file `diff base frozen` shows exactly one changed line, **457** (inside block-21 prose, before the marker): base carries the citation ``(`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md:1-14`)``; `d1681696` does not. Outside the region — the freeze claim still holds — but note any prose hash of block 21 differs between revs.
- Verification: `git show <rev>:SKILL.md | sed -n '521,539p' | sha256sum` on both revs → `99cd54d7…`; diff of the two full blobs → single line 457.
- Frozen tools (also proven unchanged): `tools/round-42/sqfs-triage-v4.py`, `indep-eval-v4.py`, `fixtures.json` — `git diff --name-only d1681696 6b9e64fe -- <those paths>` is empty and per-file sha256 at both revs equal. `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` likewise untouched.

## (2) Insertion points for a one-line status sentence (region bytes preserved)

Rule first: the sentence must be **indented continuation prose** (`  <text>`, two spaces) inside the owning `- **` list item — never a new `- **` bullet (would raise command A's `rule_blocks` 21 → 22), never a `## ` heading (would break command A's `\n## ` section split).

**v4 block (block 21, item spans lines 455–542):**
- *Before the marker:* insert a new line at **521** (between the blank line 520 and the marker). Marker and table shift to 522–540; region bytes unchanged (counter finds marker by content).
- *After the table:* insert a new line at **540** (between last row 539 and the first blank). Row 539 stays the table's end; blanks move to 541–543.
- Either keeps `sed -n` byte extraction of "marker → end of first table" identical to `d1681696`. Post-table (540) is the least disruptive — it preserves the marker's own line number for citations that pin `:521`.

**v3 block (block 20, item spans lines 387–454):**
- v3 marker at **438**; table lines 440–453 (header 440, `|---|` 441, 12 data rows 442–453); blank 454; next `- **` item (v4 prose) at 455.
- *Before the marker:* new line at **438** (between blank 437 and marker).
- *After the table:* new line at **454** (between last row 453 and the blank) — becomes part of block 20's item text.

## (3) v3 (round-41) block — exact byte range and command-A context

- Command A (SCORECARD `## Measurement recipes`, lines 92–124) computes `rules = re.split(r'(?m)^- \*\*', craft)[1:]` over `SKILL.md` split on `'## Queue-drain craft '` (note the trailing space — heading `## Queue-drain craft (rounds 5-12, distilled in round 13)` at line 81 must keep that form). At the base there are exactly **21** `- **` items in the craft section (items at lines 86, 108, 118, 137, 151, 162, 170, 175, 187, 196, 207, 219, 233, 240, 256, 279, 293, 316, 351, 387, 455) → `rule_blocks 21`.
- Block 20 (v3 item): lines **387–454** — `- **SquashFS \`extract-firmware\` outcome triage v3 (round 41).**` prose 387–437, v3 table region **438–453**.
- v3 table region: lines 438–453, bytes `[39373, 49033)` in the blob, sha256 `5ecae76fdac1d11755d6a3ab5b25c77b12a9ed8e3faf8cc38454a4af3cc5f7f1` (9 660 B) — identical at `d1681696` (whole-file diff is line 457 only).
- Other table blocks for reference: v1 marker 339, table 340–349 (region bytes `[24224,27311)`, `73559503…`); v2 marker 371, actions comment 372, table 373–385 (region `[29004,35608)`, `b81edab9…`).
- A status line added per §(2) keeps `rule_blocks` = 21 and every `citation_resolved_rules` ref intact (the refs live in prose, untouched).

## (4) corpus/README.md — coverage-map row and `## Frontier` tail

"README rows" in prior landing commits means **`corpus/README.md`** — the lane-root `README.md` (24 lines) holds no coverage map (verified: `git show eb8215ac -- corpus/README.md` added the round-42 row; root README unchanged).

**Coverage map** — `## Coverage map` at line 11; header `| section | entries | state |` (line 13); rows end at line **101** (`| SquashFS v3 through REA (round 42) | \`2026-10-26-r42-squashfs-v3-core\` | **Core** — … |`); blank 102; `## Knowledge` 103.
- Row format: `| <surface title incl. (round NN)> | \`<entry-id>\` | **Core** — <scope sentence; ends with what stays Frontier> |`.
- **New round-43 row: insert at line 102** (after line 101, before the blank). If a second row is added (e.g., triage v4 scored), it follows the same column layout.

**Knowledge registry** — `## Knowledge` at 103; header `| entry | topic | source | verified-at |`; last row at **218** (`\`2026-10-26-r42-squashfs-v3-core\``); blank 219; `## Lessons` 220.
- Row format: `| \`2026-10-27-r43-<slug>\` | <topic sentence> | S<id>[, …]; receipts \`<dir>\`[; counter \`tools/…\`] | 2026-10-27 |`.
- **New row: insert at line 219** (after line 218, before the blank).

**Frontier tail** — `## Frontier` at 251; bullets 255–267. Per-round sasquatch bullets are appended newest-last in the sasquatch cluster: round-42 bullet at **263** (`- sasquatch — 2026-10-26 round 42: SquashFS v3 … Still frontier: v1/v2, …`); unrelated `adb` bullet at 264.
- Format: `- sasquatch — <date> round NN: <what moved/status> (\`<entry-id>\`). Still frontier: <list>.`
- **New round-43 bullet: insert at line 264** (between 263 and the `adb device surface` bullet), keeping the sasquatch cluster contiguous.

## (5) SCORECARD `## Round 42` section format + SHONEN asserted-line format

**SCORECARD** — `## Round 42 — <one-line outcome summary>` at 3469 (last section; file ends 3487). Structure:
- line 3471: `Base \`<full hash>\`; freeze \`<full hash>\` (\`plans/round-42-claims.md\`); controls \`<h>\`; data \`<h>\`; C1 landing and measured revision \`<h>\`; scores \`<h>\`. Wave 1: 43 seats (\`.ufo/waves/round-42/w1/\`). Lesson \`corpus/lessons/round-42.md\`.`
- lines 3473–3476: claims table, header `| claim | axis / surface | before | after | counting command | measured at | verdict (author) |`, one `| R42-Cx | … | **met** / **not met — honest stop** |` row per claim.
- line 3478: `Owned scores: coverage 10 → 10 (map proxy …); depth …; calibration …`.
- line 3480: `### Capability addition (demonstrated before this row)` + table `| Capability | What it can now do | Evidence pointer | First-working round |` (3482–3484).
- line 3486: `- **planned (round 43, after a steer):** <plan>`; line 3487: `- **retired:** none.` — **EOF**.
- **Round-43 section appends after line 3487** (new `## Round 43 — …` + same skeleton; the round-42 `planned` bullet is then history, matching prior rounds' pattern).

**SHONEN asserted lines** — under each `- [~]` checklist item (items at lines 5, 7, 9, 11…), a continuation line `  asserted: <newest sentence first>; earlier: <chain of prior evidence>` (two-space indent). Round-43 edits prepend the new round's sentence to the relevant asserted lines (pattern seen at lines 6, 8, 10, 12: "round 42 …; earlier: … round 41 …"). Never a new top-level bullet; the `[~]` status stays until adjudication.

## Flagged inconsistency (for the L1)

Draft `plans/round-43-claims.md` **P43-C2 predicate, Separabilities and Frozen paths** all pin `corpus/evidence/round-42/local-sources/` (+ preserved S126 under `corpus/evidence/round-41/s126/`) as the copy destination — matching the prepared pack `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/local-sources.json`, whose 18 source keys map to `copy: corpus/evidence/round-42/local-sources/<ROW>/…`. The draft's own "Surface moved" paragraph and my seat brief say `corpus/evidence/round-43/local-sources/`. If copies land under round-43 while the map pins round-42, the gate stays red. [INFERENCE] the brief/summary round-43 path is stale; predicate + map are authoritative — L1 to reconcile before landing.

## Commands run (reproduce)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
for rev in 6b9e64fe… d1681696…; do git show $rev:SKILL.md | sed -n '521,539p' | sha256sum; done
git show 6b9e64fe:SKILL.md > base.SKILL.md; git show d1681696:SKILL.md > frozen.SKILL.md
diff base.SKILL.md frozen.SKILL.md          # → 457c457 only
git diff --name-only d1681696 6b9e64fe -- tools/round-42/sqfs-triage-v4.py tools/round-42/indep-eval-v4.py tools/round-42/fixtures.json   # empty
```

Artifacts: `.ufo/waves/round-43/w1/artifacts/R43ScoutTable/{v4-table-region.sha256-src,v3-table-region.sha256-src,v4-region-context.txt,v3-region-context.txt,base-vs-d1681696.diff}`.

Tool installs: none (existing git/coreutils/python3 sufficed).
