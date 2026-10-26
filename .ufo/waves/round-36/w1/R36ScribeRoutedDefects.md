# R36ScribeRoutedDefects — drafted appended corrections for the still-open routed defects

Seat: `R36ScribeRoutedDefects` (kaidoku round 36, wave 1). Work is **text only**: no frozen predicate,
counter, carrier, oracle or instrument byte was changed; no VCS mutation; no REA/CLI run; nothing written
outside this file and a removed scratch directory.

Read at: lane `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (`main`), base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`;
fleet repo `/home/vgpnk/Projects/shokunin` HEAD `a7c6d0f1828099828a6ca0e01c2f6eb2b3f8c59c` (read-only).
Sources of the routed list: `corpus/lessons/round-34-verifier-spotcheck.md:130` (D-2), `:135` (D-3);
`corpus/lessons/round-35-verifier-spotcheck.md:107-111` (R35-D1..D5).

## 1. Verification — every fact re-checked, with the command that produced it

All commands run from the lane root unless a `-C`/absolute path says otherwise; read-only git only.

### r34 D-2 (seat accounting 31/32, `AAdjacencyCite` unreported)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | wave-2 seat map has 32 entries (after repair) | `jq 'length' .ufo/waves/round-34/r34b/w2-seat-map.json` | `32` | holds |
| 2 | wave-2 reports on disk = 31 | `ls .ufo/waves/round-34/r34b/w2/*.md \| wc -l` | `31` | holds |
| 3 | the missing seat is `AAdjacencyCite` | `jq -r '.[][0]' …w2-seat-map.json \| sort > seats`; `ls …w2/*.md \| xargs -n1 basename \| sed 's/\.md$//' \| sort > files`; `comm -23 seats files` | `seats`=32, `files`=31, diff = `AAdjacencyCite`, no report without a seat | holds |
| 4 | its prompt is committed; its report does not exist | `git ls-files .ufo/waves/round-34/r34b/w2/prompts/AAdjacencyCite.md` (exit 0, 2848 bytes); `ls .ufo/waves/round-34/r34b/w2/AAdjacencyCite.md` | tracked; `No such file or directory` (exit 2) | holds |
| 5 | its scratch dir was empty and was removed | `grep -n 'AAdjacencyCite' .ufo/waves/round-34/r34b/w2/AWaveAccounting.md` | `:81` "I removed the empty directory `/fast/scratch/hyaku/kaidoku-r34b/w2/AAdjacencyCite`… (it contained zero files)" | holds |
| 6 | wave-1 is 34/34 | `ls .ufo/waves/round-34/r34b/w1/*.md \| wc -l`; `jq 'length' .ufo/waves/round-34/r34b/w1-seat-map.json` | `34`, `34` | holds |
| 7 | the report's final accounting says `… 32/32 reports on disk` | `grep -n '32/32\|66 settled' /home/vgpnk/Projects/shokunin/.ufo/reports/round-34/kaidoku.md` | `:38` "Final accounting: 67 seats, 66 dispatched, 66 settled, 0 dead, 0 refused, 34/34 and 32/32 reports on disk." (file 144 lines, `sha256 61d747e003de02b067551c9ddb8a7765875ecc5d097a9d265b61c0a4ec9f5d88`) | holds |
| 8 | the same wrong count is inside the addendum | `jq '.post_filing_findings[] \| select(.id=="N5")' .ufo/waves/round-34/r34b/claim-stop-addendum.json` | `consequence` = "… 66 settled, 0 dead, 0 refused, 34/34 and 32/32 reports on disk at handoff." | holds |
| 9 | the seat map's 31→32 repair is committed | `git log --oneline -- .ufo/waves/round-34/r34b/w2-seat-map.json`; `git show 35152484 -- …w2-seat-map.json` | `35152484 round-34: … repair the wave-2 seat map to 32 entries`; diff adds `["AAdjacencyCite","critic",…/prompts/AAdjacencyCite.md]` | holds |
| 10 | the 31st report landed after the census | `git show --stat --oneline 2e8a7758` | adds `.ufo/waves/round-34/r34b/w2/AScorecardPlan.md` (133 lines) | holds |

Stale-but-true-when-written: `AWaveAccounting.md:50` "`w2-seat-map.json` has 31 entries" is the pre-`35152484`
state; `:66` already states "31/32 w2 reports at census".

### r34 D-3 (provenance trio on `2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | entry opens `author/status/sources/revisions`, no trio | `sed -n '1,6p' corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | exactly those four fields (73 lines total) | holds |
| 2 | trio counts are zero | `grep -c '^source:'` / `'^verified-at:'` / `'^recheck:'` | `0` / `0` / `0` | holds |
| 3 | it is the only recent entry without it | loop over `git ls-files corpus/knowledge \| sort \| tail -17` printing the three counts | 16 markdown entries all `1/1/1`; `.gitkeep` `0/0/0`; this entry `0/0/0` | holds |
| 4 | S106 exists and its `used-by` names the entry | `awk -F'\|' '/^\| S106 /…' corpus/SOURCES.md` | row at `corpus/SOURCES.md:112`: kind `code`, tier `A`, status `mined`, opened `2026-10-25`, recheck `on-release`, used-by `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | holds |
| 5 | the cited corpus rule | `grep -n 'provenance trio\|verified-at:.*recheck:' /home/vgpnk/Projects/shokunin/CORPUS.md` | `:18` (Layout) and `:163-165` ("A new knowledge entry opens with its provenance trio … come first") | **citation corrected** — no section named "Additional corpus rules" exists in CORPUS.md (184 lines, headings listed) |

### R35-D1 (self-graded `quality: improved`)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | the grade | `grep -n 'quality:' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md` | `:46` "**quality: improved** — the round surfaced and durably recorded specific counter/record-quality defects …" | holds |
| 2 | the definition it must satisfy | `sed -n '28,38p' /home/vgpnk/Projects/shokunin/LEARNING.md` | `:34` `improved` when "a weaker entry is superseded by a stronger one, or stale entries re-verify, with no admitted entry failing its re-check" | holds |
| 3 | no entry or criterion moved | `git diff --name-status aa04633a cab59f22 -- corpus/` ; `git diff --stat … -- corpus/QUALITY.md` ; `git diff --name-only … -- corpus/knowledge/ \| wc -l` ; `… corpus/SOURCES.md \| wc -l` | only `M corpus/claim-freezes.tsv`, `A corpus/lessons/round-35.md`, `A corpus/lessons/round-35-verifier-spotcheck.md`; QUALITY diff empty; knowledge `0`; SOURCES `0` | holds |
| 4 | no correction landed | `git log --oneline -- /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md` | single commit `33be25b8`; current `sha256 4071d18706d846a7f70ebac096e053c8ddba8b56505a069df1a08308c36c8aed`, 56 lines | holds (still open) |

### R35-D2 (seat accounting derivable from committed bytes)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | round-35 wave tree is committed | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files .ufo/waves/round-35 \| wc -l` | `90` | holds |
| 2 | results: 64 entries, every seat `output` null | `jq -c '[.results[]\|select(.output==null)]\|length' .ufo/waves/round-35/w1-results.json` | `64` (and `64` at `3b1ab3c9`; entries themselves are not null) | holds, with wording correction |
| 3 | reports on disk = 64, all non-empty, all tracked | `ls .ufo/waves/round-35/w1/*.md \| wc -l`; `git ls-files '.ufo/waves/round-35/w1/*.md' \| wc -l`; `find … -size 0 \| wc -l` | `64`, `64`, `0` | holds |
| 4 | settle receipt is malformed | `cat .ufo/waves/round-35/w1-settle.json`; `od -c …`; duplicate-key scan with `object_pairs_hook` | bytes `{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}`; duplicate top-level key `['spawned']`; 54 bytes | holds (still malformed at HEAD) |
| 5 | it is now tracked (was untracked at r35 closure) | `git ls-files --error-unmatch .ufo/waves/round-35/w1-settle.json`; `git show --stat --oneline cab59f22` | tracked, exit 0; `cab59f22` adds 14 files (12 seat reports + `claims-canonical-note.md` + `w1-settle.json`) | **partially closed** by `cab59f22` |
| 6 | the derived-count gap the settle file leaves | `jq '.items\|length' .ufo/waves/round-35/w1-spec.json` | `64` spec items and 64 reports on disk vs the settle file's `spawned=2, settled=2, dead=0` — no derived count is consistent with the settle bytes | holds |

### R35-D3 (C2 design: coupling, substring, heading/table shape)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | D-1 is coupled to C1 | `sed -n '55,80p' tools/round-35/c2-calibration-counter.py`; `grep -n 'first_change_time\|D1_no_sources_change_after_base' …` | D-1 needs a `corpus/SOURCES.md` change after the base (failure id `D1_no_sources_change_after_base`) | holds |
| 2 | no SOURCES change exists in the round | `git log --oneline aa04633a..HEAD -- corpus/SOURCES.md`; `git diff --name-only aa04633a cab59f22 -- corpus/SOURCES.md \| wc -l` | empty; `0` | holds — C2 was green only if C1 landed |
| 3 | D-3 is a substring test | `sed -n '126p' tools/round-35/c2-calibration-counter.py` | `if not re.search(r"(?m)^source\s*:.*S106", body):` | holds (`S1060` would pass) |
| 4 | D-4 demands 8 cells; historical tables are 4/5 cells | `sed -n '20,24p' tools/round-35/c2-calibration-counter.py`; `awk` cell count over `SKILL.md:1064-1085,1209-1230` | constants name `### Round-32 instrument registry`, `### Round-34 run-6 instrument registry`; round-32 primary table = 8 cells but its residual-witness table = 4 cells (`SKILL.md:1081-1084`); run-6 table = 5 cells (`SKILL.md:1213-1219`) | holds |
| 5 | the run-6 section string does not even match its heading | control receipt `.ufo/waves/round-35/controls/c2-do-nothing.json` | `failing` contains `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4` and `D4_section_missing:### Round-34 run-6 instrument registry` (heading at `SKILL.md:1209` carries the long title) | holds — new precision |
| 6 | D-2 sums a file that does not exist | `sed -n '26,31p' …c2-calibration-counter.py`; `ls .ufo/waves/round-35/w2-settle.json` | `SETTLE_FILES` = `w1-settle.json` + `w2-settle.json`; second path `No such file or directory` | holds — new precision |
| 7 | no post-freeze C2 measurement was run | `grep -n 'No post-freeze claim measurement' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md` | `:32` states it explicitly | holds |

### R35-D4 (C1 package staged, unadopted)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | S125/S129 absent | `grep -o '^\| S[0-9]\+' corpus/SOURCES.md \| tail -5`; `grep -c '^\| S' corpus/SOURCES.md` | highest id `S106`; `106` rows | holds |
| 2 | entries absent | `ls corpus/knowledge \| grep r35` | exit 1, no match | holds |
| 3 | frontier row open | `grep -n 'jsc' PROVINCE.md` | `:147` "- **`.jsc` → source mapping** — Ignition disassembly held; a View8/jsc2js-style …" | holds |
| 4 | coverage-map gap open | `grep -n 'jsc' corpus/README.md` | `:224` "- `.jsc` → source mapping — … mapper is next for typora's real app." | holds |
| 5 | the package is only prep/claims/controls/reports | `git ls-files '.ufo/waves/round-35/**' \| grep -i 'source\|row\|entry'`; `ls .ufo/waves/round-35/prep/jsc-sources/` | `jsc2js-readme.md`, `releases-page1.json`, `releases-page7.json`, `R35ReconJscRows.md`; no staged entry or registry row | holds |

### R35-D5 (report filed before the final lane commit)

| # | Fact | Command | Observed | Verdict |
|---|---|---|---|---|
| 1 | report mtime | `stat -c '%y' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md` | `2026-10-25 16:20:46.780684728 -0300` | holds |
| 2 | two lane commits follow it | `git log -8 --format='%h %cI %s'` | `3ca5a80f 2026-10-25T16:43:52` (w1 results/dispatch/spec + 2 reports), `cab59f22 2026-10-25T23:16:39` (14 files) | holds |
| 3 | the report says so itself | `sed -n '14p' …/round-35/kaidoku.md` | "At report cutoff, the orchestrator had not yet delivered `w1-results.json` / `WAVE-DONE`, so settled/dead seat counts … are **not yet verified**" | holds |
| 4 | no erratum exists | `git log --oneline -- …/round-35/kaidoku.md` | one commit (`33be25b8`) | holds — open |
| 5 | the r34 attempt-1 content is recoverable as claimed | `git cat-file -t 27322359`; `git show 27322359:.ufo/reports/round-34/kaidoku.md \| wc -l`; `… \| sha256sum` | commit; `120` lines; `de33f4c6321f2edc326fab932b1101aacf79ef4a0e970a5ed5f966ff1fb82021` | holds |

## 2. Closure status by already-landed commit (asked explicitly)

| Defect | Fully closed at `d2e46ef5`? | What a landed commit did close | What remains |
|---|---|---|---|
| r34 D-2 | **No** | `35152484` repaired `w2-seat-map.json` 31→32 (adds `AAdjacencyCite`) and landed `AWaveAccounting.md`, QUALITY 76, M34-15/M34-16; `2e8a7758` landed `AScorecardPlan.md` (the 31st wave-2 report). | The authoritative counts still say 32/32 (fleet report `:38`, addendum `N5.consequence`); no committed byte states the **final** 31/32 with `AAdjacencyCite` unreported. |
| r34 D-3 | **No** | Nothing landed. | Entry still `0/0/0`; the routed fix (appended trio block) was never applied. |
| R35-D1 | **No** | Nothing landed; report has one commit. | `quality: improved` stands uncorrected. |
| R35-D2 | **Partially** | `3ca5a80f` landed results/dispatch/spec + 2 reports; `cab59f22` landed the 14 files the defect asked for (seat reports + settle; labelled an in-flight snapshot, not a landing). | `w1-settle.json` still duplicate-keyed and arithmetically impossible; no correction names the supersession of the report's "not yet verified" accounting. |
| R35-D3 | **No (superseded, not repaired)** | Round 36 froze a *different* C2 at `790561d4`; the r35 counter bytes are untouched (correctly frozen). | Every named mechanism still present in `tools/round-35/c2-calibration-counter.py`; the record of them is what the append below supplies. |
| R35-D4 | **No** | Nothing landed. | S125/S129, both entries, PROVINCE `:147` and README `:224` all unchanged; the package is still staged-only. |
| R35-D5 | **No** | The late artifacts did land (`3ca5a80f`, `cab59f22`). | No erratum was appended; the report still stands as filed. |

No routed defect is fully closed by a correction commit. Only sub-facts of D-2 and R35-D2 are.

## 3. Draft appended corrections (text only)

Append-only: each block is a new tail section or a new array item. None rewrites an existing line, and no
frozen counter, predicate, carrier or oracle byte is touched.

### 3.1 `corpus/lessons/round-34.md` — append at end (covers D-2 and points at 3.2/3.3)

```markdown
## Corrections appended — round 36

- **D-2 (seat accounting): the final wave-2 count is 31/32, not 32/32.** Re-measured at lane
  `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (2026-10-26): `jq 'length'
  .ufo/waves/round-34/r34b/w2-seat-map.json` = 32 (the map was repaired by `35152484`), `ls
  .ufo/waves/round-34/r34b/w2/*.md | wc -l` = 31, and the set difference is `AAdjacencyCite` — its prompt
  `.ufo/waves/round-34/r34b/w2/prompts/AAdjacencyCite.md` is committed (2848 bytes, from `66b84027`), no
  `.ufo/waves/round-34/r34b/w2/AAdjacencyCite.md` exists, and `w2/AWaveAccounting.md:81` records its scratch
  directory as empty and removed. Wave 1 is 34/34 (`ls .ufo/waves/round-34/r34b/w1/*.md | wc -l` = 34;
  `w1-seat-map.json` = 34). Two authoritative records still carry the wrong number and are **superseded**:
  `.ufo/reports/round-34/kaidoku.md:38` (`sha256 61d747e0…`) "… 34/34 and 32/32 reports on disk", and this
  addendum's `post_filing_findings[id=N5].consequence` "66 settled, 0 dead, 0 refused, 34/34 and 32/32
  reports on disk at handoff". Corrected accounting: **67 planned, 66 dispatched, 34/34 wave-1 and 31/32
  wave-2 reports on disk, `AAdjacencyCite` unreported (not settled), 0 dead, 0 refused.** The repair trail is
  addendum item N6 (appended, not an edit of N5); `w2/AWaveAccounting.md:66` already stated 31/32 at its
  07:44Z census and `:50`'s "31 entries" describes the pre-`35152484` map. QUALITY 76 and M34-15/M34-16 are
  unchanged; no measurement, clause or score moves.
- **D-3 (provenance trio): appended to the entry, never rewritten.** At `d2e46ef5`,
  `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` (73 lines) still counts
  `grep -c '^source:'` = 0, `^verified-at:` = 0, `^recheck:` = 0, and it is the only markdown entry among
  the lane's last 17 knowledge files without the trio (the other 16 each count 1/1/1). Round 36 appends the
  trio block at the entry's end, citing S106 (`corpus/SOURCES.md:112`, status `mined`, opened 2026-10-25,
  recheck `on-release`, used-by that entry) and the round-34 stop receipts. Residual, recorded not hidden:
  `CORPUS.md:163` requires the trio to "come first", which an append cannot satisfy; the appended fields
  exist so freshness sweeps and counters read them.
```

### 3.2 `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` — append at end

(Plain lines, no bullet, so both the historical sweep `grep -rlE '^[-* ]*recheck *:'` and the r35-style
counter regex `^source\s*:` read them.)

```markdown
## Provenance trio (appended round 36 — the header above is not rewritten)

source: S106 — GNU binutils `readelf` version-needs reader, https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32 (tracked capture `.ufo/waves/round-34/prep/R34ElfReader-files/readelf.c-binutils-2_47`, sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`); corpus/QUALITY.md rows 67-74 as cited above.
verified-at: 2026-10-26 — re-read at lane `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`: `corpus/SOURCES.md:112` (S106, mined, opened 2026-10-25, recheck `on-release`, used-by this entry); stop record `.ufo/waves/round-34/r34b/claim-stop.json`; addendum `.ufo/waves/round-34/r34b/claim-stop-addendum.json`; seat report `.ufo/waves/round-34/r34b/w2/AWaveAccounting.md`; lesson `corpus/lessons/round-34.md` (M34-15, M34-16); `corpus/QUALITY.md:126` row 76.
recheck: on-release — reopen S106 at the next binutils tag and re-read the claim-stop record; the standing check `grep -n '^| S106 ' corpus/SOURCES.md` must keep this entry in `used-by`.
```

### 3.3 `.ufo/waves/round-34/r34b/claim-stop-addendum.json` — append one item to `post_filing_findings`

Appended because the addendum's own `status` is "append-only addendum; the stop record is not edited" and the
wrong number sits inside `N5.consequence`, which must not be rewritten.

```json
{
  "consequence": "supersedes N5.consequence's totals: 67 planned, 66 dispatched, 34/34 wave-1 and 31/32 wave-2 reports on disk, AAdjacencyCite unreported (not settled), 0 dead, 0 refused. Appended; N5 is not edited, and no measurement, clause, score or frozen byte changes.",
  "evidence": "jq 'length' .ufo/waves/round-34/r34b/w2-seat-map.json = 32 (repaired by 35152484); ls .ufo/waves/round-34/r34b/w2/*.md | wc -l = 31; comm of seat-map names against report stems = {AAdjacencyCite}; ls .ufo/waves/round-34/r34b/w1/*.md | wc -l = 34; w2/AWaveAccounting.md:66 states 31/32 at the 07:44Z census and :81 records the seat's empty, removed scratch dir",
  "id": "N6",
  "severity": "medium",
  "what": "N5's account of the wave-2 total is wrong. It states '66 settled ... 34/34 and 32/32 reports on disk'. At lane d2e46ef5 the wave-2 seat map holds 32 entries but only 31 reports exist on disk; the missing seat is AAdjacencyCite (prompt committed since 66b84027, report never written). The same wrong number stands in the fleet report .ufo/reports/round-34/kaidoku.md:38."
}
```

### 3.4 `corpus/lessons/round-35.md` — append at end (covers R35-D1..D5)

```markdown
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
```

### 3.5 Fleet report errata — **not landable from this lane** (write scope)

Both contract reports live in the fleet repo (`/home/vgpnk/Projects/shokunin/.ufo/reports/…`), outside this
lane's write scope. Queued text for L1/operator, to be filed as an erratum in a later report commit or a
round-36 "corrections to prior records" section:

- `.ufo/reports/round-34/kaidoku.md:38` — replace `Final accounting: 67 seats, 66 dispatched, 66 settled, 0
  dead, 0 refused, 34/34 and 32/32 reports on disk.` with: **"Final accounting: 67 planned, 66 dispatched,
  34/34 wave-1 and 31/32 wave-2 reports on disk; the wave-2 seat `AAdjacencyCite` is **unreported**, not
  settled; 0 dead, 0 refused. Corrected in round 36 (lane `corpus/lessons/round-34.md`, addendum N6); the
  r34 report's original sentence is superseded, not rewritten."**
- `.ufo/reports/round-35/kaidoku.md:46` — replace the `quality: improved` clause with: **"quality:
  unchanged — the round's durable records moved no knowledge entry, no `QUALITY.md` criterion and no SOURCES
  row; improvement under `LEARNING.md:34` requires a weaker entry superseded or stale entries re-verified, and
  neither occurred (round-35 verifier spot-check `:102`)."**
- `.ufo/reports/round-35/kaidoku.md:14` — append: **"Post-filing: the wave landed 64/64 reports
  (`cab59f22`, an in-flight snapshot commit, plus `3ca5a80f`); `w1-settle.json` is duplicate-keyed and is not
  a source for settled/dead totals (`corpus/lessons/round-35.md`, corrections appended round 36)."**

## 4. Findings beyond the routed list (reported, not repaired)

1. **Wrong section citation in the routed D-3 text.** `round-34-verifier-spotcheck.md:137` cites "CORPUS.md
   §Additional corpus rules"; no such heading exists. The rule is `/home/vgpnk/Projects/shokunin/CORPUS.md:18`
   (Layout) and `:163-165` (kaidoku-campaign rules). The correction draft quotes the right lines.
2. **The r35 control receipts carry no exit status.** `.ufo/waves/round-35/controls/c1-do-nothing.json` and
   `c2-do-nothing.json` record `instrument/predicate/revision/freeze/checks/failing/pass` and `base`, but
   `grep -c '"exit"'` = 0 in both (`pass: false`). The report's "C1 exit 1", "C2 exit 1" and "green=0 red=1"
   (`.ufo/reports/round-35/kaidoku.md:7-8`) are therefore not derivable from those receipts — the same
   record-observability class as R35-D2, but not among R35-D1..D5.
3. **The r35 C2 D-4 constant cannot match its section** (mechanism detail behind "heading/table shape"): the
   counter compares the full stripped line, so the long heading at `SKILL.md:1209` never equals
   `### Round-34 run-6 instrument registry`; the control receipt records the resulting
   `D4_section_missing` alongside the 4-cell failure at `SKILL.md:1081`.
4. **`w2-settle.json` was never created** in round 35, yet the frozen C2 predicate sums it — a frozen
   predicate that cannot be satisfied by any record state (an unprovability, not a data miss).
5. **`w1-settle.json` remains malformed at HEAD** after `cab59f22`: duplicate top-level `spawned` key and
   `spawned=2, settled=2, dead=0` against 64 seats. Whatever later check reads it inherits the ambiguity
   (`json.loads` silently keeps the last `spawned`).
6. **R36-C2's coverage number is coupled to R36-C1 in practice.** `SCORECARD.md:23` states `122/122 knowledge
   files mapped at cab59f22` and `git ls-files corpus/knowledge/*.md | wc -l` = 122 today; C1's entry
   `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` does not exist yet, so landing it makes
   the observable 123/123 and forces a post-data row edit. `plans/round-36-claims.md` (Separability) discloses
   this restatement, and C2 is measured at its own landing commit `d2e46ef5` first — so it is disclosed, not
   hidden. [INFERENCE] The final-tip pass is still measured on an author-edited surface; that is a fairness
   caveat for the judge, not a counter defect.
7. **r34 attempt-1 recoverability holds exactly as D-5 states.** `27322359` is a fleet *commit* (2026-10-23
   08:22:06 -03), not a blob; its report blob is 120 lines, `sha256 de33f4c6…`, while the current file is 144
   lines, `sha256 61d747e0…`. Anyone re-checking D-5 should treat `27322359` as a commit.

## 5. Out of scope / not done

- No edit to any frozen counter, predicate, carrier, oracle, instrument, `SCORECARD.md`, `SHONEN.md`,
  `SKILL.md`, `PROVINCE.md`, `corpus/README.md` or knowledge entry — the blocks in §3 are drafts.
- No VCS mutation of any kind; no `git add/commit/checkout/reset/stash/pull/push`, no jj write. Lane and
  fleet repos were only read (`show`, `log`, `diff`, `ls-files`, `cat-file`, `rev-parse`).
- No REA CLI run, no sasquatch/unblob run, no carrier work, no network fetch. Nothing installed or upgraded
  (tooling line: none; `sasquatch` untouched).
- No frozen counter re-run: every fact above is a property of committed bytes plus `ls`/`jq`/`grep`, so a
  re-run would have added no evidence (and the checks are the L1/exec seats' assignments, not this seat's).
- Fleet report bytes were not modified (§3.5 is queued text only).

## 6. Limits

- "Last 17 knowledge files" is `git ls-files corpus/knowledge | sort | tail -17`, which is lexicographic by
  path (the lane names entries by ISO date, so this is chronological); 16 markdown entries + `.gitkeep`.
- The r34 wave-2 count is "reports on disk at `d2e46ef5`" (`ls`), which is the same observable the routed
  defect specifies; it says nothing about work performed by the unreported seat.
- The r35 wave-1 report count is a file count of tracked `.md` reports (64), not an independent read of each
  report's content; the `output: null` note in `w1-results.json` is the round's own explanation for why the
  session outputs were not retained.
- `[INFERENCE]` marks: only the fairness caveat in §4 item 6. Everything else is a pasted command result.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScribeRoutedDefects` (two sort files, `seats.txt`/`files.txt`)
  was removed before this report was finalised; nothing cited here lives under `/tmp` or scratch.
