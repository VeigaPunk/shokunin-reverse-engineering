# R36W2ReviewerRoutedCorrections — wave-2 falsification of the routed-defect corrections

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`,
tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`, freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`.
Scope: the appended corrections landed in the integration tip — `corpus/lessons/round-34.md` (D-2, D-3),
the r34b entry trio (`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`),
`corpus/lessons/round-35.md` (R35-D1..D5). Every fact below was re-derived with a read-only command at
the revision the correction itself names; nothing was repaired, nothing written outside this report.
Note: lane HEAD has since moved to `6f2ba761`; all revision-sensitive facts were pinned with
`git show <rev>:<path>`, and the working tree is byte-identical to the tip for all three correction
files (`git diff 01a44dbf -- <3 files>` empty).

## Landed and append-only (binding check)

`git diff --stat cab59f22 01a44dbf -- <3 files>` = `79 insertions(+)`, `0 deletions`. Per-file deleted-line
count via `git diff … | grep -c '^-[^-]'`: round-34.md `0` (added 24), round-35.md `0` (added 45), entry `0`
(added 4). Each hunk appends at EOF (`@@ -106,3 +106,29 @@`, `@@ -32,3 +32,50 @@`, `@@ -71,3 +71,9 @@`).
In `cab59f22..01a44dbf` exactly one commit touches the three files: `01a44dbf` ("… routed-defect corrections
(r34 D-2/D-3, R35-D1..D5) …"). **Append-only: PASS.**

## r34 D-2 (seat accounting, `corpus/lessons/round-34.md`)

| Correction claim | Re-derivation | Result |
|---|---|---|
| `jq 'length' .ufo/waves/round-34/r34b/w2-seat-map.json` = 32 | `jq 'length'` → `32` | OK |
| map repaired by `35152484` | `git show --stat 35152484`: `w2-seat-map.json | 5 ++`; subject "repair the wave-2 seat map to 32 entries" | OK |
| `ls .ufo/waves/round-34/r34b/w2/*.md \| wc -l` = 31 | → `31` | OK |
| set difference is `AAdjacencyCite` | `jq -r '.[][0]' map` vs report basenames: map-only `{AAdjacencyCite}`, report-only `{}` | OK |
| prompt `w2/prompts/AAdjacencyCite.md` committed, 2848 bytes, from `66b84027` | `git cat-file -s 66b84027:<path>` → `2848`; `stat` → `2848 bytes`; `git log --follow` oldest touch = `66b84027` | OK |
| no `w2/AAdjacencyCite.md` exists | `test -e` → NO; tracked at tip → 0 | OK |
| `w2/AWaveAccounting.md:81` records its scratch dir empty and removed | line 81: "I removed the empty directory `/fast/scratch/hyaku/kaidoku-r34b/w2/AAdjacencyCite` … (it contained zero files; no content lost)" | OK |
| wave 1 = 34/34 (`ls w1/*.md \| wc -l` = 34; `w1-seat-map.json` = 34) | → `34`, `jq 'length'` → `34` | OK |
| fleet `.ufo/reports/round-34/kaidoku.md:38` (sha256 `61d747e0…`) says "34/34 and 32/32 reports on disk" | `sha256sum` (fleet root path) → `61d747e003de02b0…f5d88`; line 38 ends "… 34/34 and 32/32 reports on disk." | OK |
| addendum `post_filing_findings[id=N5].consequence` carries "66 settled, 0 dead, 0 refused, 34/34 and 32/32 reports on disk at handoff" | N5 consequence: "Round total 67 seats: 66 dispatched, 66 settled, 0 dead, 0 refused; 34/34 and 32/32 reports on disk at handoff." | OK (quote-fidelity nit, F3) |
| `:66` already stated 31/32 | line 66 contains "31/32 w2 reports at census" | OK (timestamp gloss imprecise, F2) |
| `:50`'s "31 entries" describes the pre-`35152484` map | line 50: "`w2-seat-map.json` has 31 entries; `w2-spec.json` has 32 items; `set(diff) = {'AAdjacencyCite'}`" | OK |
| corrected accounting 67 planned / 66 dispatched / 34-34 w1 / 31-32 w2 / `AAdjacencyCite` unreported / 0 dead / 0 refused | 34+32+1=67 planned; 66 seats dispatched; 34/34 and 31/32 on disk; all consistent with `:66` and the counts above | OK |
| QUALITY 76 and M34-15/M34-16 unchanged | M34-15/M34-16 at `round-34.md:62-63`; QUALITY Row 76 bytes intact (moved `:126`→`:128` at tip because rows 77-78 insert above) | OK |
| **"The repair trail is addendum item N6 (appended, not an edit of N5)"** | `jq -r '.post_filing_findings[].id'` → `Y1 Y2 Y3 Y4 Y5 N1 N2 N3 N4 N5`; `grep -c '"N6"'` → 0 (whole file, tree and tip); addendum untouched in `cab59f22..01a44dbf` (`git log` empty, `git diff 01a44dbf` empty) | **FAIL — no N6 exists** (F1) |

## r34 D-3 (provenance trio, r34b knowledge entry)

| Correction claim | Re-derivation | Result |
|---|---|---|
| at `d2e46ef5` the entry is 73 lines and counts `^source:`/`^verified-at:`/`^recheck:` = 0/0/0 | `git show d2e46ef5:<entry> \| wc -l` → 73; three greps → 0, 0, 0 | OK |
| only entry among the lane's last 17 knowledge files without the trio; other 16 each 1/1/1 | `git log d2e46ef5 --name-only -- corpus/knowledge/` dedup head -17; per-file greps at `d2e46ef5`: this entry 0/0/0, the other 16 all 1/1/1 | OK |
| round 36 appends the trio at the entry's end | tip counts 1/1/1; entry 79 lines = 73+6; hunk appends after `## Rejected` | OK |
| trio cites S106 (`corpus/SOURCES.md:112`, mined, opened 2026-10-25, recheck on-release, used-by this entry) | `grep -n '^| S106 '` → `112:`; row columns: status `mined`, opened `2026-10-25`, recheck `on-release`, used-by `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | OK |
| capture sha256 `7e81eedf19b2…ddeeff` | `git cat-file blob d2e46ef5:.ufo/waves/round-34/prep/R34ElfReader-files/readelf.c-binutils-2_47 \| sha256sum` → `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff` | OK |
| trio's URL/commit matches the S106 row | both carry `hb=6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32` | OK |
| `corpus/QUALITY.md:126` row 76 (as re-read at `d2e46ef5`) | `git show d2e46ef5:corpus/QUALITY.md \| sed -n '126p'` = "- **Row 76 added after the round (seat accounting).** …" | OK (tip drift noted, F5) |
| receipts exist: `claim-stop.json`, `claim-stop-addendum.json`, `w2/AWaveAccounting.md`; lesson M34-15/M34-16; QUALITY rows 67-74 | all tracked at `d2e46ef5`; M34-15/16 at lesson lines 62-63; QUALITY table rows `| 67 |`…`| 74 |` present; entry body line 5 cites "rows 67-74" | OK |
| `CORPUS.md:163` requires the trio to "come first" | fleet-root `CORPUS.md:163`: "**A new knowledge entry opens with its provenance trio.** `source:`, …" — an append cannot satisfy "opens with" | OK (fleet-root path, F6) |
| standing check `grep -n '^| S106 ' corpus/SOURCES.md` keeps the entry in used-by | returns line 112; used-by cell lists the entry (round-36 lesson: "S106's used-by is unchanged") | OK |

## R35-D1..D5 (`corpus/lessons/round-35.md`)

- **D1** — report `:46` "`quality: improved`" OK; fleet `LEARNING.md:34` defines quality as "a weaker entry is
  superseded by a stronger one, or stale entries re-verify, with no admitted entry failing its re-check" OK;
  `git diff --name-only aa04633a cab59f22 -- corpus/knowledge/` → 0 files OK; `git diff --stat … -- corpus/QUALITY.md`
  → empty OK; `corpus/SOURCES.md` → 0 files OK; `round-35-verifier-spotcheck.md:102` already ruled
  "**quality: unchanged.** The report self-grades `improved` …" OK. Superseded grade justified.
- **D2** — `3ca5a80f` landed `w1-{results,dispatch,spec}.json` OK; `cab59f22` added exactly 14 files (12 seat
  reports + `claims-canonical-note.md` + `w1-settle.json`) and its message labels it "in-flight snapshot
  committed by the orchestrator (not a landing)" OK; at `d2e46ef5` 64 tracked `w1/*.md` reports, none zero-byte
  (per-file `git cat-file -s`) OK; `w1-results.json` `.results` = 64 entries, non-null `output` = 0, all 64
  notes start "orchestrator kernel restarted mid-wave; seat output … not retained — read the seat report file in
  the wave dir" OK; identical blob `b812d37a` at `3b1ab3c9` OK; `w1-settle.json` bytes exactly
  `{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}` (duplicate `spawned`, totals match no 64-seat wave) OK;
  report `:14` "settled/dead seat counts … **not yet verified**" OK.
- **D3** — `tools/round-35/c2-calibration-counter.py:63-77` requires a post-base `corpus/SOURCES.md` change
  (`first_change_time(root, base, rev, "corpus/SOURCES.md")`, else `D1_no_sources_change_after_base`) OK, and no
  such change exists in `aa04633a..cab59f22` OK; `:126` is literally
  `re.search(r"(?m)^source\s*:.*S106", body)` (substring; `S1060` passes) OK; `:20-24` `EIGHT_CELL_SECTIONS` =
  round-32 + run-6 headings OK; `SKILL.md:1081-1084` round-32 residual-witness table is 4-cell OK;
  `SKILL.md:1209` heading is "### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped
  capability)" ≠ the bare constant OK, and the run-6 table `:1213-1219` is 5-cell OK; runtime proof
  `.ufo/waves/round-35/controls/c2-do-nothing.json:15` records
  `"D4_section_missing:### Round-34 run-6 instrument registry"` OK; `:26-29` sums `w1-settle.json` +
  `w2-settle.json` while `w2-settle.json` does not exist (ls-tree at `d2e46ef5` and tree both empty) OK;
  report `:32` says "No post-freeze claim measurement was run" — supports the "never run" statement with a
  wording nit (F4).
- **D4** — at `d2e46ef5`: SOURCES = 106 rows, highest id S106, `grep -c 'S125\|S129'` → 0 OK; no
  `2026-10-25-r35-jsc2js-*` in `corpus/knowledge/` OK; `PROVINCE.md:147` = "`**.jsc` → source mapping** —
  Ignition disassembly held; a View8/jsc2js-style …" frontier bullet OK; `corpus/README.md:224` = the open-gap
  line OK; `.ufo/waves/round-35/prep/jsc-sources` tracked OK.
- **D5** — `.ufo/reports/round-35/kaidoku.md` has exactly one fleet commit `33be25b8` ("round-35: kaidoku
  report", 2026-10-25 16:20:58 -03) OK; mtime `2026-10-25 16:20:46 -0300` OK; sha256 `4071d18706d846a7…` OK;
  `3ca5a80f` 16:43:52 -0300 and `cab59f22` 2026-10-25 23:16:39 -0300 both land after it OK; report `:14`
  declares its own accounting unverified OK.

## Findings

- **F1 (medium — factual error inside a landed correction).** `corpus/lessons/round-34.md`, D-2 block:
  "The repair trail is addendum item N6 (appended, not an edit of N5)." No item N6 exists anywhere in
  `.ufo/waves/round-34/r34b/claim-stop-addendum.json` — ids are `Y1-Y5, N1-N5`; `grep -c '"N6"'` = 0 at the
  tree and at tip; the addendum is untouched in `cab59f22..01a44dbf`. The actual repair trail is commit
  `35152484`, which appended N5 and repaired `w2-seat-map.json` in the same commit, with the repair recorded
  inside N5's own D2 clause ("repaired in this addendum's commit to 32"). Every other fact in the D-2 block
  verified true; only this pointer is wrong. Recommend a one-line erratum appended to the D-2 block by whoever
  owns corrections next round (I did not repair the lane).
- **F2 (low, calibration).** D-2: "`w2/AWaveAccounting.md:66` already stated 31/32 at its 07:44Z census."
  Line 66 does state "31/32 w2 reports at census", but without a timestamp, and the file's own 07:44Z census
  lines (`:36` "27/32 reports as of 07:44Z", `:84` "27/32 w2 at census, 28/32 with this report") show the
  07:44Z census counted 27/32. The "07:44Z" attachment to the 31/32 figure is the correction's gloss; the
  substantive point (31/32 was already stated in the record) holds.
- **F3 (info, quote fidelity).** The D-2 quote of N5's consequence elides "66 dispatched," without ellipsis and
  renders the source semicolon as a comma ("… 66 settled, 0 dead, 0 refused, 34/34 …" vs source "… 66
  dispatched, 66 settled, 0 dead, 0 refused; 34/34 …"). Meaning preserved.
- **F4 (info, wording).** R35-D3 cites report `:32` for "No post-freeze C2 measurement was ever run"; the line
  (the C1 bullet) reads "No post-freeze **claim** measurement was run". Supported, paraphrased narrower.
- **F5 (info).** The trio pins `corpus/QUALITY.md:126` to its stated re-read rev `d2e46ef5`, where it is exact;
  at tip `01a44dbf` Row 76 sits at `:128` (rows 77-78 insert above). Honest as scoped; future readers at tip
  following `:126` land on Row 75.
- **F6 (info).** D-2's `.ufo/reports/round-34/kaidoku.md` (and R35's round-35 report paths) resolve only from
  the fleet root `/home/vgpnk/Projects/shokunin`, not the lane (lane `.ufo/reports/` has no `round-34/`).
  Internally consistent with D5's "fleet commit" phrasing, but unqualified in D-2.

## Residual risk / verification gaps

- The sourceware URL in the trio's `source:` field was not fetched; the S106 pin was verified against lane
  bytes only (SOURCES row 112 + tracked capture sha256). Remote liveness/content drift is outside this seat.
- "66 settled" inside N5 (and the corrected accounting) rests on the r34b records; I verified the arithmetic
  (34+32+1 = 67 planned; 66 seats dispatched; 34+31 seat reports on disk; 65+L1 = 66/67 returned at handoff)
  and every on-disk count, not the orchestrator's internal settle bookkeeping.
- C2/C1 counter verdicts, receipts and controls are other seats' lanes; not re-scored here.

## Tooling / bounds record

No tools installed or updated; no pacman transactions; no VCS mutation (read-only `git show/log/diff/ls-tree/
ls-files/cat-file/rev-parse` only); no subagents, no background jobs. Scratch
`/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerRoutedCorrections` created and removed; `/tmp` intermediates
(<50 MB) removed.
