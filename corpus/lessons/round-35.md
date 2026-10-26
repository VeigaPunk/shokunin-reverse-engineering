# Round 35 — honest stop after frozen-measure falsification

Base: `aa04633a686d49756763b1feed4be6830d5bb479`. Canonical claims snapshot at `2323d197456f1328459d9420aff025cffbcb3e27`; control receipts `3ecf42981a0b63414de90ade643040d609dbb8a5`. The snapshot was scored only on the unchanged frozen predicates. No post-freeze counter or predicate edit is used to claim a pass.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M35-1 | severability / counter-scope coupling | `.ufo/waves/round-35/w1/R35CriticClaims.md:9-20`: C2 D-1 fails when no post-base `corpus/SOURCES.md` change exists; only C1's S125/S129 append can supply that change. In isolated fixture, all other C2 fields were green but C2 emitted `D1_no_sources_change_after_base`, exit 1. | AXES.md §Working the axes requires causal separability; counter C2 `first_change_time` path and `D1_no_sources_change_after_base` branch were not tested against a C1-stalled/C2-complete control before freeze. | Stop C2 under the frozen kill rule; do not remove or neutralize the dependency after data. Future claim design must freeze independent C2 D1 evidence (or a different independent predicate) and demonstrate a C1-absent / C2-green red-green control before freezing. |
| M35-2 | vacuous structural/receipt predicate | `.ufo/waves/round-35/w1/R35CriticClaims.md:24-37`: D-1 accepts fabricated substring receipt `rows=106 EXIT=0 W04` without exact warning count or validating the frozen input hash; D-3 matches `S106` as a substring, not a token. Sandbox C2 returned `C2_CLEAN`, exit 0 on fake census text. | QUALITY.md #61/66 gate-selftest and #68 pin enforcement were not applied to the new counter's D-1/D-3 paths; only D-2/D-4 junk controls were planned. | Honest stop. Future guard needs typed exact parsing, re-hash the pinned census at the freeze revision, and red cases for counterfeit receipt and `S1060`; never retroactively change this claim. |
| M35-3 | historical table boundary mismatch | `.ufo/waves/round-35/w1/R35CriticClaims.md:39-45`: D-4 fails existing SKILL registries because the round-34 heading includes a qualifier and round-32 contains 4-cell and 7-cell separate tables; closure would rewrite historical layouts to raw 8-cell formatting. | QUALITY.md #65/74 required per-file / table-scope evidence; D-4 section names and counted ranges were not reconciled with actual heading/table layout before freeze. | Honest stop; preserve history. Future measurement must bind to an explicitly scoped, already-current table surface or a new round-authored registry, not require retrofitting archived rows. |
| M35-4 | setup-order / freeze-path error | `.ufo/waves/round-35/freeze-status.md`; first freeze-gate run at `f1ea3a6d` failed because gate discovered an earlier `claims.json` freeze with stale counter digests; subsequent canonical snapshot at `2323d197` is gate-clean. Intermediate drafts/corrections are retained and disclosed, not silently erased. | Freeze-gate path was run before the canonical claims file/path had stabilized. | Retain exact supersession record and final freeze-gate receipt; freeze only after counter bytes/selftests settle, then perform one first-add and verify first-add path. |

## Gate

### Candidate source decisions and first-round opening

- **S125 admit (bounded to jsc2js tool contract, not universal `.jsc` recovery).** URL `https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md`, accessed 2026-10-25. Capture `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md`, SHA-256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`. Located § “Quick Start” / captured lines 128-157: “choose the V8 version that is identical to the one that produced your target `.jsc`” (14 words). This supports a version-matched d8 prerequisite, not output correctness or original-source recovery. A second bounded quote in the same README warns reconstruction cannot be 100% faithful (see `.ufo/waves/round-35/w1/R35ScribeJscGate.md:43-51`); it limits rather than expands claims.
- **S129 admit (published release inventory, not correctness for a particular target).** URL `https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=1` and same endpoint `page=7`, accessed 2026-10-25. Captures `.ufo/waves/round-35/prep/jsc-sources/releases-page1.json` SHA-256 `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c`; `releases-page7.json` SHA-256 `499e2b227a6eb2c3053a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc`. Located release-body quote from page 1, first release `15.6.75.19`: “Patched d8 for V8 15.6.75.19 (includes d8 + snapshot_blob.bin).” (10 words). Live independent audit reports 7 pages (100×6+77), 677 unique releases, no page-boundary duplicates and page 8 empty (`.ufo/waves/round-35/w1/R35Audit02.md:40-48`; `R35Audit18.md:15-22`). The committed page 1/page 7 captures alone establish representative endpoints, not the complete middle-page listing; complete-count assertion is based on the independent live audit, not on only two stored pages.
- **Rejected S150 (payload-absent) and quarantine hand-check.** URL `https://zenn.dev/yasu01/articles/7370bd5d414ec4`, accessed 2026-10-25; live HTTP 200, HTML 174,088 bytes. The registered heading `シンボルがない場合のヒント` occurs 0 times; the actual relevant H2 is `パターン認識のコツ`, and body line 69 provides a different real sentence (`.ufo/waves/round-35/w1/R35Audit26.md:13-18`). This row is refused until re-anchored to a real contiguous quote; the absent heading is fabrication-class, not merely unreachable.
- **S113 reachable-now, not fabrication.** URL `https://developer.android.com/tools/adb?hl=en`, accessed 2026-10-25; HTTP 200, 368,063 bytes; 17 `hreflang` locales plus x-default and the Japanese alternate link; evidence in `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` and live `/tmp/adb.html` capture. Quarantine class was unreachable at campaign time, not fabricated; it remains unadopted because no admitted entry cites it.
- **S117 unverifiable, not fabrication.** DOI `https://doi.org/10.1109/SP46214.2022.9833799`, fetched 2026-10-25, returned HTTP 202 with empty body; no quote could be checked (`quarantine-verdicts.md`).
- **S136 locatable own-work.** `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`, exact prior claim “2 of 24 verbs are” occurs once; register had no locator, now verified against source (`quarantine-verdicts.md`).
- **S147 locatable local contract.** `/home/vgpnk/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`, 3,386 bytes; `rea-agents@6.7.0`, skill v42 and 207 tools are at lines 18/41/53. The prior no-locator defect is now locatable (`quarantine-verdicts.md`).

No source row is appended by this lesson itself. The C1 adoption rows and entries were not authored because the frozen C1 counter has an unbounded semantic scope check (filename stems are accepted anywhere in PROVINCE/README), and the round has not completed the required wave. No SOURCES status/recheck/used-by cell changed in this lesson.

### ID-collision guard proof and current collision

The 0–3-leading-space extractor was tested on a scratch fixture whose registry contains `  | S002 |` and staged IDs contain `S002`; `comm -12` produced nonempty `collisions` with exactly `S002`. Evidence: `.ufo/waves/round-35/assimilation/id-guard-proof/{fixture-registry.md,reg-ids,staged-ids,collisions,run-proof.log}`. On the real package, registry IDs 106, staged rows 132, collision count 1: `S106` (`assimilation/{reg-ids,staged-ids,collisions}`). It is the prior r34 source row and stays unchanged; adopted rows S125/S129 do not collide. The package IDs 106-237 are not copied wholesale; no row append occurs this round.

## Gate result / spot-check handoff

One explicit admit (S125/S129 theme; two bounded sources), at least one explicit reject (S150), and the quarantine dispositions are recorded for outside review. C1/C2 claim scoring remains stopped; no admission is asserted. A fresh non-author closure is required to reopen any source for adoption and to rule on claim findings.

## Corrections appended — round 36

- **R35-D1 (trend grade): `quality: improved` is withdrawn.** `.ufo/reports/round-35/kaidoku.md:46` grades
  `quality: improved`. `LEARNING.md:34` defines the quality observable as a weaker entry superseded by a
  stronger one, or stale entries re-verified with none failing; round 35 changed no knowledge entry
  (`git diff --name-only aa04633a cab59f22 -- corpus/knowledge/` = 0 files), `corpus/QUALITY.md` is
  byte-identical across the round (`git diff --stat aa04633a cab59f22 -- corpus/QUALITY.md` empty) and
  `corpus/SOURCES.md` is unchanged (0 files). Superseded grade: **quality: unchanged**, as the round-35
  verifier spot-check already ruled (`corpus/lessons/round-35-verifier-spotcheck.md:102`). M35-1..M35-4 are
  mined mistakes, which the round requires and which do not move this observable.
- **R35-D2 (seat accounting): artifacts landed; the settle receipt is still malformed.** `3ca5a80f` landed
  `w1-results.json`/`w1-dispatch.json`/`w1-spec.json`; `cab59f22` committed the 14 outstanding files (12 seat
  reports + `claims-canonical-note.md` + `w1-settle.json`) — the commit is labelled an in-flight
  orchestration snapshot, not a landing. At `d2e46ef5`: 64/64 wave-1 reports are tracked and none is
  zero-byte; `w1-results.json` holds 64 entries whose `output` is `null` for all 64, each carrying the note
  "orchestrator kernel restarted mid-wave; seat output … not retained — read the seat report file in the wave
  dir" (the verifier's "all-null" means these outputs, not the entries; the same is true at `3b1ab3c9`).
  `w1-settle.json` is tracked but its bytes are `{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}` — a
  duplicate `spawned` key and totals that match no wave of 64 seats. Corrected accounting: **64 wave-1 seats,
  64/64 reports on disk, 0 dead, 0 refused; the settle receipt is not a source for those totals.** The
  report's "settled/dead … not yet verified" (`.ufo/reports/round-35/kaidoku.md:14`) is superseded by the
  committed reports, not by the settle file.
- **R35-D3 (C2 design): the named defects stand in frozen bytes; the attempt is superseded, not repaired.**
  In `tools/round-35/c2-calibration-counter.py`: (a) D-1 needs a `corpus/SOURCES.md` change after the base
  (`:63-77`, failure `D1_no_sources_change_after_base`) and no such change exists across `aa04633a..cab59f22`,
  so C2 could only be green if C1 landed — the severability breach; (b) D-3 accepts any `source:` line
  containing `S106` (`:126`, `re.search(r"(?m)^source\s*:.*S106", body)`), a substring test that `S1060`
  would pass — the token-exactness breach; (c) D-4 demands eight cells for `### Round-32 instrument registry`
  and `### Round-34 run-6 instrument registry` (`:20-24`), while the round-32 section contains a 4-cell
  residual-witness table (`SKILL.md:1081-1084`), the run-6 table is 5 cells (`SKILL.md:1213-1219`), and the
  second constant does not equal the heading at `SKILL.md:1209` (the control receipt records
  `D4_section_missing:### Round-34 run-6 instrument registry`); (d) D-2 sums `w1-settle.json` +
  `w2-settle.json` (`:26-29`) although `.ufo/waves/round-35/w2-settle.json` does not exist. No post-freeze C2
  measurement was ever run (`.ufo/reports/round-35/kaidoku.md:32`). Round 36's C2 is a different, severable
  predicate (freeze `790561d4`) and does not reuse these bytes; the counter is not edited and the defects stay
  recorded here.
- **R35-D4 (C1 package): still staged, still unadopted.** At `d2e46ef5`, `corpus/SOURCES.md` holds 106 rows
  with `S106` as the highest id, so S125/S129 are absent; `corpus/knowledge/` holds no
  `2026-10-25-r35-jsc2js-*` entry; `PROVINCE.md:147` still carries the `.jsc` → source mapping as a frontier
  bullet and `corpus/README.md:224` as the open gap. The package exists only as prep captures
  (`.ufo/waves/round-35/prep/jsc-sources/`), claims/controls and seat reports.
- **R35-D5 (report before final commit): confirmed; this block is the erratum.** `.ufo/reports/round-35/kaidoku.md`
  is one fleet commit (`33be25b8`), mtime `2026-10-25 16:20:46 -03`, `sha256 4071d187…`; `3ca5a80f` (16:43:52)
  and `cab59f22` (23:16:39) land after it. The report's `:14` already declares its own accounting unverified,
  so the bytes are not dishonest — they are superseded by the two later commits and by this block. The fleet
  report is not rewritten.
