# EX-41 — arc3-citation census and dispositions (C3 freshness, arc3-loop1-round3)

Census surface: the non-wave files touched by the four arc3 r1/r2 commits
(`fbbbd45` work r1, `14b1682` records r1, `28aa7a9` work r2, `c07af80` records
r2) — extracted mechanically by `census.py` over the added lines. Scope
boundary: the lane's durable citation surfaces (knowledge entries, SKILL.md,
corpus/README.md, SHONEN.md, SCORECARD.md, LOG.md, the committed instruments,
the custody README). Wave-internal citations are evidence provenance, not lane
citations (the r10 extension precedent keeps the table on durable surfaces);
they are adjudicated as a class in the table's `exempt` ledger.

Every pinnable row is either TABLE-COVERED (new entry id, or the pre-existing
entry that already grades it) or NO-ENTRY with a named cause. Acceptance is
this census, not the entry count.

## A. Line-number citation rows (the drift class)

| # | citing file | token as written | target resolves? | disposition |
|---|---|---|---|---|
| 1 | `.ufo/gates/c1-census-v10.py:7` | `SCORECARD.md:850-852` | yes | TABLE-COVERED `census-cites-sc-e22-debt` |
| 2 | `.ufo/gates/c1-census-v10.py:27` | `SCORECARD.md:856-1336` | yes (481-line scope range) | TABLE-COVERED `census-cites-sc-round4-range` (needle grades the span's start header) |
| 3 | `.ufo/gates/c1-census-v10.py:33` | `SCORECARD.md:908` | yes | TABLE-COVERED `census-cites-sc-laundering-refusal` |
| 4 | `.ufo/reports/arc3-loop1-round1/kaidoku.md` | `corpus/README.md:38` | yes, still accurate at HEAD | NO-ENTRY — append-only round record (exempt row A); a live entry would grade a record's revision |
| 5 | `.ufo/reports/arc3-loop1-round1/kaidoku.md` | `SKILL.md:371` | **no — measured stale** | NO-ENTRY — round record; measured at HEAD: `SKILL.md:371` holds `## Refuses`; the citation-drift row moved to `:389` when round 2 inserted the rule-#14 block above the registry table |
| 6 | `.ufo/reports/arc3-loop1-round2/kaidoku.md` | `SHONEN.md:6` | yes | NO-ENTRY — round record (exempt row A); SHONEN.md:6 itself is TABLE-COVERED by the pre-existing `shonen-skill-range` |
| 7 | `SCORECARD.md:1435` | `SHONEN.md:6` | yes | TABLE-COVERED `sc-arc3r2-cites-shonen` |
| 8 | `SHONEN.md:6` | `SKILL.md:81-255` | yes | TABLE-COVERED by the pre-existing `shonen-skill-range` (the r2 same-commit refresh is that entry's subject) |
| 9 | `SKILL.md:252` | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7` | yes | TABLE-COVERED `skill-rule14-entry-recheck` |
| 10 | `SKILL.md:246` | `.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89` | yes | TABLE-COVERED `skill-rule14-cr2-identity` |
| 11 | `SKILL.md:248` | `.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md:149-153` | yes | TABLE-COVERED `skill-rule14-verdict-identities` |
| 12 | `SKILL.md:254` | `LOG.md:1411-1412` | yes | TABLE-COVERED `skill-rule14-log-fresh-identity` |
| 13 | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:17` | `corpus/knowledge/2026-10-13-r3-evm-interface.md:149-155` | yes | TABLE-COVERED `arc3r1-entry-r3-offsets` |
| 14 | `…arc3-r1-evm-real-solc.md:18` | `…r3-evm-interface.md:59-70` | yes | TABLE-COVERED `arc3r1-entry-r3-stub-mutability` |
| 15 | `…arc3-r1-evm-real-solc.md:21` | `corpus/QUALITY.md:24-25` | yes | TABLE-COVERED `arc3r1-entry-quality-ids` |
| 16 | `…arc3-r1-evm-real-solc.md:24` | `corpus/QUALITY.md:21` | yes | TABLE-COVERED `arc3r1-entry-quality-11` |
| 17 | `…arc3-r1-evm-real-solc.md:25` | `…r3-evm-interface.md:44-45` | yes | TABLE-COVERED `arc3r1-entry-r3-hypothesis` |
| 18 | `…arc3-r1-evm-real-solc.md:26` | `…r3-evm-interface.md:93-96` | yes | TABLE-COVERED `arc3r1-entry-r3-cli-quirk` |

## B. File-level and surface citations (the anchor class)

| # | citation | disposition |
|---|---|---|
| 19 | `corpus/README.md` map row token `2026-10-19-arc3-r1-evm-real-solc` | TABLE-COVERED `readme38-arc3r1-token` (anchored, line deliberately unpinned — the map grows by rows) |
| 20 | the r1 entry's `source:` / `recheck:` provenance roster (wave artifact paths, no numbers) | NO-ENTRY — no stated number means no drift class; the recheck line itself is graded via row 9; wave-internal targets are adjudicated by class (exempt row B) |
| 21 | `SKILL.md` registry rows: citation-drift (arc3 r1) and custody-pair (arc3 r2) | TABLE-COVERED `skill-registry-citation-drift-row`, `skill-registry-custody-pair-row` (anchors; lines unpinned — the lane appends to this file and to this table) |
| 22 | `.ufo/gates/custody-pair/README.md` receipt conventions: v2 field set, rewrite identity, verify precedence, never-`/tmp` | TABLE-COVERED `custody-readme-v2-fieldset`, `-rewrite-identity`, `-precedence`, `-scratch-never-tmp` |
| 23 | README v1-shape examples: `config-pre-pair.txt` (stanza), `EX-26/custody-sha256.txt` (sums), `config-pre-pair-metadata.txt` (pipe) | TABLE-COVERED `custody-readme-v1-stanza-example`, `-sums-example`, `-pipe-example` (file-level anchors on frozen wave receipts) |
| 24 | the five operator paths as written in the custody README | NO-ENTRY — operator-mutable, outside the repo, unresolvable as Git objects; rule #11 forbids pinning them (exempt row C) |
| 25 | arc3 SCORECARD section keys (r1 `:1338`, r2 `:1419`) — the rule-#11-conforming form SKILL.md rule #14 anchors by | TABLE-COVERED `sc-arc3r1-section-key`, `sc-arc3r2-section-key` |
| 26 | current-state count tokens (`82/82`, `13/13`, `15/15`, `31 entries`, `10.0/10.0`) in the arc3 sections and registry rows | NO-ENTRY — measurement tokens, not pointers; a pin buys same-commit churn and no drift detection (exempt row D) |
| 27 | `LOG.md` arc3 entries' file-level evidence rosters | NO-ENTRY — append-only history by rule; no stated numbers (exempt row E) |
| 28 | wave-internal citations (`.ufo/waves/arc3-loop1-round{1,2}/**` artifacts citing one another) | NO-ENTRY as a class — evidence provenance inside one wave; wave targets are graded where a durable surface cites them (rows 10, 11; existing `readme22-r8envelope`) (exempt row B) |

## Counts

- line-number citation rows: 18 (17 in-repo resolvable, 1 measured-stale round record)
- file-level/surface rows: 10 groups
- TABLE-COVERED: 24 new entries + 2 pre-existing (`shonen-skill-range` covering rows 8 and — via the same entry — the r2 refresh)
- NO-ENTRY with named cause: 6 rows/groups, materialized in the table's `exempt` ledger (3 → 8 rows)
- new entries added: 26; table `entries` 31 → 57; `quoted` unchanged (4); `exempt` 3 → 8