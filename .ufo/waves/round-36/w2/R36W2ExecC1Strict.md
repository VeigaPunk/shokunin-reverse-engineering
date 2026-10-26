# R36W2ExecC1Strict — independent strict check of P36-C1 and of the surfaces the claim moves

Seat: leaf executor (wave 2, round 36). Read-only on the lane; the only lane write is this file.
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Measured revision
`ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` (R36-C1 landing), freeze
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`, integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`,
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`. Axes: coverage, calibration.

No subagent, no background job, no tool install, no VCS mutation (only `git show` / `git diff` /
`git rev-parse` / `git cat-file` / `git archive` reads). The checker does not import, exec or even read
`tools/round-36/c1-counter.py`; the frozen counter is cited here only as the claim's own instrument.

---

## 0. Verdict

**The P36-C1 sentence survives.** Every clause about the four carriers, the receipts, the evidence ids
and the Core-row/entry/SOURCES chain reads true at `ffc81341`, and stays true at the tip. I could not
falsify it with checks the frozen counter does not perform (published byte-size equality, per-row match
uniqueness, `published_bytes` arithmetic, run-record pins, oracle `regular_files`/offset cross-check,
and an independent `unsquashfs` re-derivation of the K1/K2 oracle).

**Three of the seat's five extra surface conditions are false.** They are *annotation* conditions, not
predicate clauses: the claim's own frozen wording (`plans/round-36-claims.md` P36-C1) never asks the
Frontier bullet or the README Firmware row to be annotated, so the frozen counter is right to score
`met_target` while these readings fail.

| # | seat condition | reading | verdict |
|---|---|---|---|
| S2a | PROVINCE.md Frontier sasquatch bullet **carries** a dated supersession note that **cites the entry** | note inside the bullet text | **FALSE** — `PROVINCE.md:156-157` is byte-identical to the base; no date, no supersession, no citation |
| S2b | same, loose: a dated note referring to the bullet exists and cites the entry (path or stem) | note anywhere in `PROVINCE.md` | **FALSE** — the note at `PROVINCE.md:374` cites only `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`; neither the r36 entry path nor its stem appears in it |
| S3 | README **Firmware** sasquatch line carries a dated note | line itself or within 2 lines | **FALSE** — `corpus/README.md:44` is unchanged and still present-tense "recursion blocked by missing sasquatch"; line 45 is the next table row |
| S4 | README **Frontier** sasquatch line carries a dated note | line itself or within 2 lines | **TRUE** — `corpus/README.md:232` (historical bullet) + `:233` (dated note, cites the entry stem and the dependency stem) |
| S7 | the entry cites S-rows opened 2026-10-26 whose used-by lists it | exact comma item in the used-by cell | **TRUE** — `corpus/SOURCES.md:113-115` (S107/S108/S109, `opened` 2026-10-26, used-by exactly the entry path) |

`S2a`/`S2b` together mean: the supersession note exists, is dated, and points at the bullet by line
(`PROVINCE.md:156-157`), but it lives 218 lines below the bullet in a different section
(`## Round-36 additions to Core`) and it names the *assimilated dependency* entry, not the coverage
entry. A reader who lands on the Frontier bullet at `PROVINCE.md:156` finds no marker there; a reader
who lands on the note is one hop from the dependency entry, not from the measurement entry — the hop
is only closed indirectly by "as measured above" pointing at the Core row at `:372`, which does cite
the entry. If "the entry" in the seat sentence means the dependency entry, `S2b` passes on citation
grounds but `S2a` still fails because the bullet itself carries nothing.

Mechanical summary at `ffc81341`: `23` conditions true, `3` false —
false set `['S2a_province_bullet_carries_dated_note_citing_entry', 'S2b_province_dated_sasquatch_note_cites_entry', 'S3_readme_firmware_sasquatch_line_carries_dated_note']`.

---

## 1. Instrument

`strict-c1.py` (appendix A) reads **only git objects** (`git show REV:path`) at an explicit revision,
so no working-tree state can leak in. 26 conditions:

* `R1`–`R3` frozen-input provenance: `carriers.json`, `oracle.tsv`, `before.json` bytes at the freeze
  equal the bytes at the measured revision; both receipt siblings present and parseable.
* `R4` every oracle row published by the `after` receipt: identical sha256 **and** identical size
  **and** (`relative_path == rel` or `relative_path` endswith `/rel`). Counted **per oracle row**, so
  the 14 byte-identical rows of K3/K4 stay separate.
* `R16` each oracle row is satisfied by **exactly one** published file and the matched published files
  are distinct — closes the double-count loophole a pure `any()` match leaves open.
* `R5` the `after` receipt has no sasquatch extraction gap anywhere in `normalized_result`.
* `R6` the `before` receipt has a `missing-extractor-dependency` gap whose `dependencies` contains the
  exact token `sasquatch`.
* `R7` the `before` receipt publishes no oracle row.
* `R8` both receipts: subject sha256 == carrier sha256, `operation == extract_firmware`,
  `provider.id == unblob`, `provider.version == 26.6.4`.
* `R9` every before/after receipt's stored `evidence_id` authenticates under the **rea-agents 6.5.0**
  rule, recomputed by that package's own `parseEvidence` (appendix B): it strips `evidence_id`,
  rebuilds the semantic projection and rejects any mismatch (`dist/domain/evidence.js:134-138`).
  Nothing about the id rule is retyped.
* `R10` before and after are different measurements (published sha sets differ).
* `R11` every published file has a non-empty `relative_path` and a 64-hex sha256.
* `R12` receipt bytes at the receipts commit `3310d8fa` and at the integration tip `01a44dbf` equal
  the bytes at the measured revision (no silent re-issue between landing and tip).
* `R13` run records: `before-run.json` has `sasquatch: ""` for all four; `after-run.json` has a
  sasquatch path, a 64-hex sha256, the same sha256 in all four, both exits 0, after utc >= before utc.
* `R14` `published_bytes` equals the sum of the published file sizes (before and after).
* `R15` `oracle-run.json`: `regular_files` == oracle row count, `squashfs_offset` == the receipt's
  `squashfs_v4_le` chunk `root_file_range.offset`, `carrier_sha256` == `carriers.json`.
* `O1` independent oracle reproduction: K1/K2 fixtures are committed, so they are re-extracted with
  the local `/usr/bin/unsquashfs 4.7.5 (2026/03/01)` and compared row for row (path, sha256, size) to
  the frozen `oracle.tsv`. K3/K4 carriers are remote (not committed), so their oracle is not re-derived.
* `S1`–`S7`, `X1` the surface conditions in §0 plus the stated-count calibration.

### 1.1 Calibration (17 controls, `selftest-strict.py`, appendix D)

Each control builds a throwaway git fixture in scratch from
`git archive ffc81341 -- PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/evidence/round-36/c1 <entry>`,
commits it as the freeze, applies one mutation, commits, and runs the checker with
`--rev HEAD --freeze <freeze> --skip-cross-rev`. `git -C $D rev-parse --show-toplevel` was checked
against `$D` before the first commit. Fixtures are removed per case.

`17/17` pass, exit 0:

| # | control | result | unexpected |
|---|---|---|---|
| 1 | green (landing copy) | pass | `—` |
| 2 | drop one published file (K3 after) | pass | `—` |
| 3 | change one published sha256 (K1 after) | pass | `—` |
| 4 | change one published size (K2 after) | pass | `—` |
| 5 | add a sasquatch gap to after (K1) | pass | `—` |
| 6 | remove the before sasquatch gap (K2) | pass | `—` |
| 7 | rename a matched published path (K4) | pass | `—` |
| 8 | forge oracle copy, not re-hashed (K1) | pass | `—` |
| 9 | forge oracle copy, re-hashed with 6.5.0 (K1) | pass | `—` |
| 10 | delete the PROVINCE Core row | pass | `—` |
| 11 | break S107 used-by | pass | `—` |
| 12 | append an oracle row after freeze | pass | `—` |
| 13 | change a carrier sha256 | pass | `—` |
| 14 | break the README coverage stem | pass | `—` |
| 15 | add the entry path to the PROVINCE Frontier note | pass | `—` |
| 16 | make the PROVINCE Frontier bullet carry the note | pass | `—` |
| 17 | add a dated note after the README Firmware row | pass | `—` |

Three of these controls matter for the finding:

* `delete the PROVINCE Core row` → `S1` red: the predicate binding is falsifiable, not a free pass.
* `add the entry path to the PROVINCE Frontier note` → only `S2b` turns green, `S2a` stays red; the
  detector is not stuck false, it is reporting placement plus citation.
* `add a dated note after the README Firmware row` → `S3` green: the missing landing (finding F2) is
  exactly the wave-1 draft text, and the condition would have passed had it been applied.

One control is expected to stay **green**, and is the instrument's own blind spot:

| control | observed |
|---|---|
| `forge oracle copy, not re-hashed (K1)` | `R4` true, `R9` **false** — a receipt edited to publish the oracle without re-sealing is refused |
| `forge oracle copy, re-hashed with 6.5.0 (K1)` | `R4`/`R5`/`R9` **all true** — a fabricated `after` receipt sealed with the 6.5.0 package's own digest code passes |

That second row is the same class the round's lesson records as M36-4 and the wave-1 critic recorded
as its F1. It is stated here as an instrument limit, not as a suspicion about the committed receipts:
the committed pair is corroborated by four independent wave-1 reproductions
(`.ufo/waves/round-36/w1/R36ExecReproK{1,2,3,4}.md`) and by the run records, and **no receipt field
inside the `after` envelope names sasquatch at all** (checked: `raw_result.execution.stdout`/`stderr`
contain no sasquatch string in K1/K3 either mode; the positive evidence is the gap's disappearance
plus `after-run.json`). A strictly receipt-internal checker therefore proves *absence of the recorded
gap*, never *presence of a sasquatch run*.

---

## 2. Receipt evidence, per carrier at `ffc81341`

| carrier | carrier sha256 (carriers.json) | oracle rows (distinct) | after published | oracle rows matched (unique) | before published | before oracle hits | before gap | after sasquatch gap | after `published_bytes` = Σsizes | after `coverage` | stored evidence id (6.5.0 authentic) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | `93802938…a589` | 3 (3) | 3 | 3 (3) | 0 | 0 | 1 × `missing-extractor-dependency` `["sasquatch"]` handler `squashfs_v4_le` | none | 70086 = 70086 | `complete` | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` (after) / `ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3` (before) |
| K2 | `ce5bf60e…084f` | 4 (4) | 4 | 4 (4) | 0 | 0 | 1 × same shape | none (1 `unpublished-entry` symlink remains) | 273971 = 273971 | `partial` | `ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f` / `ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c` |
| K3 | `b644d034…29fb` | 2130 (2116) | 2147 | 2130 (2130) | 2 (carve only) | 0 | 1 × same shape, offset 944632 len 10510336 | none (2 `unpublished-entry`) | 51122564 = 51122564 | `partial` | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` / `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` |
| K4 | `8efcec73…e1c2` | 2130 (2116) | 2147 | 2130 (2130) | 2 (carve only) | 0 | 1 × same shape, offset 936456 len 10420224 | none (2 `unpublished-entry`) | 51792724 = 51792724 | `partial` | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` / `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` |

Cross-checks that also read true:

* `R13`: all four `before-run.json` carry `sasquatch: ""`; all four `after-run.json` carry
  `sasquatch: /home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256
  ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, version
  `unsquashfs version 4.5.1 (2022/03/17)`; exits 0; before `2026-10-26T04:17:49Z` < after
  `2026-10-26T04:22:42Z` (K1/K3; same for K2/K4 records). The installed binary on this host today is
  the same `ad02d27a…4754` (382824 B), i.e. the run-record digest is reproducible, not just asserted.
* `R15`: `oracle-run.json` offsets 0/0/944632/936456 equal each `after` receipt's `squashfs_v4_le`
  chunk `root_file_range.offset`; `regular_files` 3/4/2130/2130 equal the oracle row counts.
* `O1`: K1 re-extracted from the committed fixture (sha256 `93802938…a589`, equal to
  `carriers.json`) yields exactly the 3 frozen rows; K2 (`ce5bf60e…084f`) exactly the 4 frozen rows;
  zero symmetric difference; `unsquashfs` exit 0. The K2 symlink stays out of the regular-file set.
* `R12`: the eight receipt files at `3310d8fa` and at `01a44dbf` are byte-identical to those at
  `ffc81341`.
* `X1`: the counts the docs state are the counts observed — PROVINCE row "oracle 3, 4, 2,130, 2,130"
  (`PROVINCE.md:372`) and README "K1 3/3, K2 4/4, K3 …, 2130/2130, K4 …, 2130/2130"
  (`corpus/README.md:89`). The entry's own table (`entry:83-88`) matches too, including
  `published 2147 / extras 17` and `coverage` values; extras decompose as 9 `carved.elf` + 8 one-byte
  `.padding` (all sha256 `6e340b9c…01d`, the digest of a single NUL) = 17, as the entry states.

---

## 3. Surface findings, with file:line

### F1 — the PROVINCE Frontier note dropped the entry citation the wave-1 draft had (S2a, S2b)

`PROVINCE.md:156-157` at `ffc81341`, verbatim (2 lines, unchanged from base):

```
- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback
  covers the carved-image path today.
```

The dated note that refers to it is `PROVINCE.md:374`, the last line of the
`## Round-36 additions to Core` section (heading `:368`, table header `:370-371`, data row `:372`):

> Frontier note, 2026-10-26: the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)`
> (`PROVINCE.md:156-157`; `PROVINCE.md:149-150` before this round's 7-line Adjacent addition) is
> superseded for little-endian SquashFS v4 as measured above; its "(AUR-only)" was wrong as a route
> statement — unblob's own README documents the Debian-package install
> (`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`). Big-endian/AVM and vendor-mangled
> images stay Frontier.

Measured: that string contains neither `2026-10-26-r36-sasquatch-squashfs-recursion` nor
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` (checker `S2b.notes[0]`:
`cites_entry_path false`, `cites_entry_stem false`, `cites_dep_entry true`, `in_core_section true`,
`in_frontier_section false`).

Why this is a **landing** gap and not a drafting gap: the wave-1 draft for exactly this note ended
with the entry path. `.ufo/waves/round-36/w1/R36ScribeProvince.md:63`:

> Frontier note, 2026-10-26: … is superseded for the four measured carriers only; big-endian/AVM images
> and vendor-mangled images stay Frontier (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`).

The citation slot was re-filled with the *dependency* entry and the measurement entry was dropped. The
Core row three lines above (`PROVINCE.md:372`) does cite the entry, and the note says "as measured
above", so the chain is recoverable by a careful reader; [INFERENCE] the edit was made to satisfy
M36-1's "Frontier notes cite S110 by entry" line and the entry citation was lost in that rewrite.

### F2 — the README Firmware row carries no dated note; the wave-1 draft row was not landed (S3)

`corpus/README.md:44` at `ffc81341` (unchanged from base; grep of every `sasquatch` line in the
file returns nine: `44, 89, 90, 164, 195, 196, 224, 232, 233`):

```
| Firmware | `2026-10-13-r2-firmware-probe`, `2026-10-13-r4u-01-firmware-deep`, `2026-10-13-r4u-03-unblob-extract` | held (partial) — … AppImage SquashFS carved but recursion blocked by missing sasquatch; … |
```

`corpus/README.md:45` is `| Frontier prerequisites | …` — no note row was inserted. The landing diff
`git diff d2e46ef5 ffc81341 -- corpus/README.md` adds exactly six lines: two `## Coverage map` rows
(`:89`, `:90`), two `## Knowledge` rows (`:195`, `:196`), one `## Lessons` row (`:224`) and one
`## Frontier` bullet (`:233`). No `## Coverage map` row adjacent to the Firmware row, and no dated
annotation on `:44` itself.

The wave-1 draft for this surface was written and is unambiguous —
`.ufo/waves/round-36/w1/R36ScribeReadme.md:49-55` ("Draft B — dated note appended to the Firmware row",
"Insert immediately after current line 44") with the row text starting
`| Firmware (2026-10-26 note) | \`2026-10-26-r36-sasquatch-squashfs-recursion\` | dated supersession of the row above, which is not rewritten: … |`.
It was not applied. My control `add a dated note after the README Firmware row` shows the condition
would have read true with that row in place.

Consequence: the row the claim names as the moved surface (`plans/round-36-claims.md` R36-C1 "Surface
moved") is still present-tense false at the point of the statement. The supersession is recorded in two
other places (`corpus/README.md:89` "Dated supersession of the Firmware row's … (2026-10-13 state, kept
as history)" and `:233`), which is why a whole-file reader is not misled, but a reader of the Firmware
row alone is. This is the M36-1 shape (stale present-tense route/gap prose) one layer down: the round
found the stale premise and did not put the correction on the line it corrected.

### S4 — the README Frontier line does carry its note (true)

`corpus/README.md:232-233` (`## Frontier`, heading `:226`):

```
- sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today.
- sasquatch — 2026-10-26 dated note on the line above (kept as history): LE SquashFS v4 recursion is now
  Core (`2026-10-26-r36-sasquatch-squashfs-recursion`); "AUR" was one route, the producer documents a
  Debian package (`2026-10-26-unblob-sasquatch-dependency`). Still frontier: big-endian/AVM
  (`sasquatch-v4be`) and vendor-mangled images.
```

Note the file's own convention is bare stems, so the entry is cited by stem, not by path; the exact
path appears only in `## Coverage map` (`:89`) and `## Knowledge` (`:195`).

### S1/S5/S6/S7 — predicate bindings (true)

* `PROVINCE.md:372` is a data row of the `## Round-36 additions to Core` table whose first cell is
  `sasquatch squashfs recursion` and whose last cell ends `entry
  \`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md\``.
* `corpus/README.md:89` is a `## Coverage map` (heading `:11`) data row carrying the stem.
* The entry exists (215 lines) with three `source:` lines at `entry:1-3` (S107/S108/S109),
  `verified-at: 2026-10-26` (`:4`), `recheck: 180d` (`:5`).
* `corpus/SOURCES.md:113` (S107), `:114` (S108), `:115` (S109): each row has 11 cells, cell 9
  (`opened`) `2026-10-26`, and cell 11 (`used-by`) is exactly
  `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` — the exact-item test, not a
  substring test, and an `S1070`-style token cannot satisfy it (token boundary regex, exercised by the
  frozen counter's own case and by my `break S107 used-by` control, which leaves S108/S109 valid and
  still turns `S7` red).

### Dated history, not defects

`corpus/README.md:164` (`## Knowledge` index row for the 2026-10-13 entry: "squashfs needs sasquatch
(7z fallback)") and `:44`'s clause are index/historical text about a past state. `:164` is correctly
historical by the file's index convention. `:44` is the row the claim names as moved, which is why F2
treats it as unannotated rather than as history.

---

## 4. Revision sweep (instrument discriminates)

`strict-c1.py --rev <REV> --freeze 790561d4 --json-out …` (all read-only):

| revision | false conditions | reading |
|---|---|---|
| `cab59f22` (base) | all 26 | honest stop: no carriers, no oracle, no receipts, no entry, no Core row |
| `790561d4` (freeze) | 19 | freeze-only inputs: oracle/carriers/before present, after and all surfaces absent; `R6`/`R7`/`R9` (before half) already true |
| `d2e46ef5` (C2 landing) | 9 | receipts landed (`R*` all true), every textual surface absent |
| `3310d8fa` (receipts commit) | 9 | identical to the previous row: the receipt commit adds no prose |
| `ffc81341` (C1 landing) | 3 | `S2a`, `S2b`, `S3` |
| `01a44dbf` (tip) | 3 | unchanged: `git diff ffc81341 01a44dbf -- PROVINCE.md corpus/README.md corpus/SOURCES.md <entry>` is empty |

The same three surface readings are false at the tip, so this is not a mid-round artefact.

---

## 5. Limits of this check

1. **Receipt integrity is not provenance.** A fabricated `after` receipt re-sealed with the 6.5.0
   package's own digest code passes every `R` condition (control 9). The committed receipts are
   corroborated by four independent wave-1 reproductions and the run records; inside the envelopes
   themselves nothing names sasquatch (verified by scanning `normalized_result` and the captured
   stdout/stderr for K1/K3 in both modes).
2. **K3/K4 oracle is not independently re-derived here.** Those carriers are not committed (remote
   neovim release assets); I verified their oracle's internal consistency (`regular_files` == row
   count, offset == receipt chunk offset, carrier digest == `carriers.json`, 2116 distinct digests over
   2130 rows, 14 shared-byte rows) but did not re-run `unsquashfs` on them.
3. **Suffix rule has a latent ambiguity** that this carrier set does not trigger: K3/K4 contain both
   `nvim.desktop` and `usr/share/applications/nvim.desktop`, so the nested path is also a suffix match
   for the root row. Their shas/sizes differ (`b407dc89…` 4169 vs `0b297403…` 4142), so each row is
   satisfied by exactly one published file (`R16` true, `match_counts == [1]`). A future carrier with
   byte-identical files at such a pair would let one published file satisfy two rows.
4. **The README/PROVINCE wording conditions are mine, not the frozen predicate's.** The frozen
   predicate's own bindings are `S1`, `S5`, `S6`, `S7`, and all four are true; the seat's extra
   annotation conditions are what fail. I did not change any frozen predicate, counter, carrier or
   oracle, and I did not repair the lane.
5. A sibling wave-2 reviewer independently flagged placement of the `PROVINCE.md:374` note as drift
   debt (`.ufo/waves/round-36/w2/R36W2ReviewerProvince.md:129`); that is compatible with F1 but is not
   evidence for it — F1 rests on the citation measurement above.

---

## 6. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC1Strict; mkdir -p "$S"; export TMPDIR="$S"
# appendices A, B, C, D written into "$S"
python3 -I -B "$S/strict-c1.py"  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin  --rev ffc813417d3bceeeb7b028b12ce0be8a5dc33d95  --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0  --pkg650 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents  --json-out "$S/strict-at-ffc81341.json"
# -> prints TRUE/FALSE per condition, "all_true: False", exit 1
python3 -I -B "$S/selftest-strict.py"
# -> {"selftest": "strict-c1", "cases": 17, "pass": 17, "failures": []}, exit 0
```

Exit codes observed: strict check `1` (three surface conditions false), selftest `0`, base/freeze/tip
sweep `1` each (correctly not met). Checksums of the instrument as run:

```
c7166510360f57f8822e4a8c196ee76fba831c0f682d3bffb87f504874226b12  strict-c1.py
9c024c96475ca40f9f0e9a624f4faafd28822828a3cddc03c0b7f03abc86b069  evid-650.mjs
46e4d0db8bbd1d295e72f42a7bc25fa0697c2d00a351feb4e0246146c2e43df3  forge-rehash.mjs
b6b03ce8cb1e685b8bc316d8c3b96219b1a296b856cf256447425d8d332045cd  selftest-strict.py
```

Tool installs: none. Scratch removed on exit (`trap 'rm -rf -- "$S"' EXIT`); everything cited here is
copied into this report because scratch paths are not evidence.

---

## 7. Files changed

* `.ufo/waves/round-36/w2/R36W2ExecC1Strict.md` (this report) — only write.
* No lane source, tool, counter, carrier, oracle, receipt, VCS object or `shokuknow` file touched.

### What the L1 has to decide (not repaired by me)

1. Apply the wave-1 Firmware note (`R36ScribeReadme.md:49-55`) after `corpus/README.md:44`, or record a
   reason for leaving the row present-tense; today the claim's named surface is unannotated.
2. Either add the entry citation to `PROVINCE.md:374`, or state that the Core row at `:372` is the
   intended carrier of that citation and that the note deliberately cites only S110.

---

## Appendix A — `strict-c1.py` (verbatim, as run)

```python3
#!/usr/bin/env python3
"""R36W2ExecC1Strict — independent STRICT check of predicate P36-C1 and of the surfaces
the claim says it moves. Does not import, exec or read tools/round-36/c1-counter.py.

Every read is a git object read at an explicit revision (default the R36-C1 landing
ffc813417d3bceeeb7b028b12ce0be8a5dc33d95); nothing is read from the working tree.

Receipt conditions, per frozen carrier K1..K4
  R1  carriers.json bytes at freeze == at rev; ids K1..K4
  R2  oracle.tsv bytes at freeze == at rev and non-empty; oracle rows well formed
  R3  before.json bytes at freeze == at rev; before + after present and parse
  R4  after publishes EVERY oracle row: sha256 identical AND (relative_path == rel or
      relative_path endswith /rel) AND size identical; counted per oracle row, so the
      14 duplicate-byte rows of K3/K4 stay separate
  R5  after carries no sasquatch extraction gap anywhere in normalized_result
  R6  before carries >=1 missing-extractor-dependency gap whose dependencies name sasquatch
  R7  before publishes no oracle row
  R8  subject digest == carrier sha256, operation extract_firmware, provider unblob 26.6.4
  R9  every before/after receipt's stored evidence_id authenticates under the rea-agents
      6.5.0 rule, recomputed by the 6.5.0 package's own parseEvidence (evid-650.mjs)
  R10 before and after are different measurements (published sha sets differ)
  R11 every published file has a non-empty relative_path and a 64-hex sha256
  R12 receipt bytes at 3310d8fa (receipts commit) and at the integration tip equal the bytes at rev
  R13 run records: before sasquatch == "" for all four; after sasquatch path with sha256 equal to
      the installed binary and to S107's deb member; both exits 0; after run utc >= before utc
  R14 published_bytes equals the sum of the published file sizes
  R15 oracle-run.json offsets equal the receipt chunk root_file_range offsets, its regular_files
      equal the oracle row counts, its carrier sha256 equals carriers.json

Surfaces the claim says it moves
  S1  PROVINCE.md `## Round-36 additions to Core` data row naming sasquatch in cell 1 and citing
      the entry path
  S2a PROVINCE.md Frontier `- **sasquatch**` bullet itself carries the dated supersession note
      and that note cites the entry path
  S2b a dated sasquatch supersession note exists anywhere in PROVINCE.md and cites the entry
      (path or stem)  — the looser reading of the same sentence
  S3  corpus/README.md Firmware sasquatch line carries a dated note (line itself or within two lines)
  S4  corpus/README.md Frontier sasquatch line carries a dated note (line itself or within two lines)
  S5  corpus/README.md Coverage map data row holds the entry stem
  S6  entry present, with source: rows
  S7  every entry source id is a SOURCES.md row opened 2026-10-26 whose used-by lists the entry
      as an exact comma-separated item
  X1  the oracle counts stated in the PROVINCE row and the README coverage row equal the observed

Independent oracle reproduction (O1): K1/K2 fixtures are committed, so the frozen oracle is
re-derived with the local /usr/bin/unsquashfs and compared row for row.
Exit 0 only when every condition is true.
"""
import argparse, json, os, re, subprocess, sys, tempfile

CARRIERS = 'corpus/evidence/round-36/c1/carriers.json'
EVDIR = 'corpus/evidence/round-36/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md'
STEM = '2026-10-26-r36-sasquatch-squashfs-recursion'
DEP_ENTRY = 'corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md'
CORE_HEADING = '## Round-36 additions to Core'
FRONTIER_HEADING = '### Round-4 frontier (post-unlock)'
OPENED = '2026-10-26'
HEX64 = re.compile(r'^[0-9a-f]{64}$')
SID = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
TOKEN_SASQ = re.compile(r'(?<![A-Za-z0-9_-])sasquatch(?![A-Za-z0-9_-])')
ISO_DATE = re.compile(r'(?<!\d)(20\d\d-\d\d-\d\d)(?!\d)')
NOTE_MARKERS = re.compile(r'dated note|supersed|kept as history|now Core', re.I)
CODE_SPAN = re.compile(r'`[^`]*`')


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit('git ' + ' '.join(args) + ': ' + p.stderr.decode(errors='replace').strip())
    return p


def show(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}', check=False)
    return p.stdout if p.returncode == 0 else None


def text(root, rev, path):
    b = show(root, rev, path)
    return None if b is None else b.decode()


def oracle_rows(raw):
    rows = []
    if raw is None:
        return rows
    for i, line in enumerate(raw.decode().splitlines(), 1):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 3:
            raise SystemExit(f'oracle row {i} has {len(parts)} fields, not 3: {line!r}')
        rel, sha, size = parts
        if not HEX64.match(sha):
            raise SystemExit(f'oracle row {i} sha256 not 64 lowercase hex: {sha!r}')
        rows.append((rel, sha, int(size)))
    return rows


def published(env):
    nr = (env or {}).get('normalized_result') or {}
    return [(f.get('relative_path') or '', f.get('sha256') or '', f.get('size')) for f in nr.get('files') or []]


def row_match(rows, files):
    """Oracle row -> matching published paths (exact relpath or /relpath suffix, same sha256, same size)."""
    out = {}
    for rel, sha, size in rows:
        out[(rel, sha)] = [fp for fp, fs, fz in files
                           if fs == sha and fz == size and (fp == rel or fp.endswith('/' + rel))]
    return out


def walk_strings(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f'{path}[{i}]')
    else:
        yield path, obj


def sasquatch_mentions(env):
    return [(p, v) for p, v in walk_strings((env or {}).get('normalized_result'))
            if isinstance(v, str) and 'sasquatch' in v.lower()]


def sasquatch_missing_gap(env):
    nr = (env or {}).get('normalized_result') or {}
    out = []
    for g in nr.get('extraction_gaps') or []:
        if g.get('kind') != 'missing-extractor-dependency':
            continue
        if any(isinstance(d, str) and d.strip().lower() == 'sasquatch' for d in (g.get('dependencies') or [])):
            out.append(g)
    return out


def section_lines(lines, heading):
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    j = i + 1
    while j < len(lines) and not lines[j].startswith('## '):
        j += 1
    return i, j


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def header_bullet(lines, head_re):
    for i, line in enumerate(lines):
        if re.match(head_re, line):
            j = i + 1
            while j < len(lines) and lines[j].startswith((' ', '\t')) and lines[j].strip():
                j += 1
            return i, j, '\n'.join(lines[i:j])
    return None


def prose_dates(s):
    """Dates written outside backticked code spans (a knowledge stem's date is not a note date)."""
    return ISO_DATE.findall(CODE_SPAN.sub('', s))


def is_dated_note(s):
    return bool(NOTE_MARKERS.search(s)) and bool(prose_dates(s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', default='ffc813417d3bceeeb7b028b12ce0be8a5dc33d95')
    ap.add_argument('--freeze', default='790561d4e3aca732a434081aa9573ec2fa5fd7d0')
    ap.add_argument('--pkg650', required=True)
    ap.add_argument('--node', default='node')
    ap.add_argument('--unsquashfs', default='/usr/bin/unsquashfs')
    ap.add_argument('--skip-oracle-repro', action='store_true')
    ap.add_argument('--skip-cross-rev', action='store_true')
    ap.add_argument('--json-out')
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    res = {'revision': a.rev, 'freeze': a.freeze, 'predicate': 'P36-C1', 'conditions': {}}
    C = res['conditions']

    def put(cid, val, **ev):
        C[cid] = {'ok': bool(val), **ev}

    git(root, 'cat-file', '-e', f'{a.rev}^{{commit}}')
    git(root, 'cat-file', '-e', f'{a.freeze}^{{commit}}')

    work = tempfile.mkdtemp(prefix='strict-c1.')
    envfiles = {}

    def dump(name, env):
        p = os.path.join(work, name.replace('/', '_') + '.json')
        json.dump({'data': env}, open(p, 'w'))
        envfiles[name] = p
        return p

    # ---------------------------------------------------------------- carriers
    frozen_carriers = show(root, a.freeze, CARRIERS)
    rev_carriers = show(root, a.rev, CARRIERS)
    if frozen_carriers is None:
        raise SystemExit('carriers.json absent at freeze')
    spec = json.loads(frozen_carriers)
    ids = [c['id'] for c in spec['carriers']]
    put('R1_carriers_frozen_unchanged_and_ids', rev_carriers == frozen_carriers and ids == ['K1', 'K2', 'K3', 'K4'],
        carrier_ids=ids, bytes_identical=rev_carriers == frozen_carriers)

    per = {}
    for c in spec['carriers']:
        k = c['id']
        d = {'id': k, 'sha256': c['sha256']}
        o_freeze = show(root, a.freeze, f'{EVDIR}/{k}/oracle.tsv')
        o_rev = show(root, a.rev, f'{EVDIR}/{k}/oracle.tsv')
        rows = oracle_rows(o_freeze)
        d['oracle_frozen'] = o_freeze is not None and o_freeze == o_rev
        d['oracle_rows'] = len(rows)
        d['oracle_distinct_shas'] = len({s for _, s, _ in rows})
        b_freeze = show(root, a.freeze, f'{EVDIR}/{k}/before.json')
        b_rev = show(root, a.rev, f'{EVDIR}/{k}/before.json')
        d['before_frozen'] = b_freeze is not None and b_freeze == b_rev
        raw = {'before': b_rev, 'after': show(root, a.rev, f'{EVDIR}/{k}/after.json')}
        d['present'] = {m: raw[m] is not None for m in raw}
        d['oracle_run'] = json.loads(show(root, a.rev, f'{EVDIR}/{k}/oracle-run.json') or b'{}')
        d['run'] = {m: json.loads(show(root, a.rev, f'{EVDIR}/{k}/{m}-run.json') or b'{}') for m in raw}
        for m in ('before', 'after'):
            try:
                env = json.loads(raw[m]) if raw[m] else None
            except json.JSONDecodeError:
                env = None
            if not isinstance(env, dict):
                d[m] = None
                continue
            dump(f'{k}/{m}', env)
            files = published(env)
            nr = env.get('normalized_result') or {}
            d[m] = {
                'subject_sha256': ((env.get('subject') or {}).get('digest') or {}).get('sha256'),
                'operation': env.get('operation'),
                'provider': env.get('provider'),
                'published': len(files),
                'malformed_published': [f for f in files if not f[0] or not HEX64.match(f[1])],
                'sasquatch_mentions': sasquatch_mentions(env),
                'sasquatch_missing_gaps': sasquatch_missing_gap(env),
                'hits': {f'{rel}\t{sha}': fp for (rel, sha), fp in row_match(rows, files).items() if fp},
                'match_counts': sorted({len(fp) for fp in row_match(rows, files).values()}),
                'distinct_matched_files': len({f for fps in row_match(rows, files).values() for f in fps}),
                'published_shas': sorted({f[1] for f in files}),
                'published_bytes': nr.get('published_bytes'),
                'size_sum': sum(f[2] for f in files if isinstance(f[2], int)),
                'chunks': [{kk: ch.get(kk) for kk in ('handler', 'input_path', 'range', 'root_file_range', 'extraction_failed')}
                           for ch in (nr.get('chunks') or [])],
            }
        per[k] = d
    res['carriers'] = per

    ks = list(per)
    put('R2_oracle_frozen_nonempty', all(per[k]['oracle_frozen'] and per[k]['oracle_rows'] > 0 for k in ks),
        rows={k: per[k]['oracle_rows'] for k in ks}, distinct={k: per[k]['oracle_distinct_shas'] for k in ks})
    put('R3_before_frozen_and_both_present',
        all(per[k]['before_frozen'] and all(per[k]['present'].values()) for k in ks),
        before_frozen={k: per[k]['before_frozen'] for k in ks}, present={k: per[k]['present'] for k in ks})
    put('R4_after_publishes_every_oracle_row',
        all(per[k]['after'] and len(per[k]['after']['hits']) == per[k]['oracle_rows'] for k in ks),
        matched={k: (len(per[k]['after']['hits']) if per[k]['after'] else None) for k in ks},
        rows={k: per[k]['oracle_rows'] for k in ks})
    put('R16_each_oracle_row_matched_by_exactly_one_file',
        all(per[k]['after'] and per[k]['after']['match_counts'] == [1]
            and per[k]['after']['distinct_matched_files'] == per[k]['oracle_rows'] for k in ks),
        match_counts={k: (per[k]['after']['match_counts'] if per[k]['after'] else None) for k in ks},
        distinct_matched={k: (per[k]['after']['distinct_matched_files'] if per[k]['after'] else None) for k in ks},
        rows={k: per[k]['oracle_rows'] for k in ks})
    put('R5_after_no_sasquatch_gap',
        all(per[k]['after'] and not per[k]['after']['sasquatch_missing_gaps'] for k in ks),
        gap_counts={k: (len(per[k]['after']['sasquatch_missing_gaps']) if per[k]['after'] else None) for k in ks},
        sasquatch_mention_paths={k: ([p for p, _ in per[k]['after']['sasquatch_mentions']]
                                     if per[k]['after'] else None) for k in ks})
    put('R6_before_names_missing_sasquatch',
        all(per[k]['before'] and len(per[k]['before']['sasquatch_missing_gaps']) >= 1 for k in ks),
        gap_counts={k: (len(per[k]['before']['sasquatch_missing_gaps']) if per[k]['before'] else None) for k in ks},
        gaps={k: ([{'kind': g.get('kind'), 'dependencies': g.get('dependencies'), 'handler': g.get('handler')}
                   for g in per[k]['before']['sasquatch_missing_gaps']] if per[k]['before'] else None)
              for k in ks})
    put('R7_before_publishes_no_oracle_row',
        all(per[k]['before'] and not per[k]['before']['hits'] for k in ks),
        matched={k: (len(per[k]['before']['hits']) if per[k]['before'] else None) for k in ks})
    pin = lambda m: all(per[k][m] and per[k][m]['subject_sha256'] == per[k]['sha256']
                        and per[k][m]['operation'] == 'extract_firmware'
                        and (per[k][m]['provider'] or {}).get('id') == 'unblob'
                        and (per[k][m]['provider'] or {}).get('version') == '26.6.4' for k in ks)
    put('R8_subject_operation_provider_pin', pin('before') and pin('after'),
        before=pin('before'), after=pin('after'),
        provider={k: (per[k]['after']['provider'] if per[k]['after'] else None) for k in ks})
    put('R10_before_after_differ',
        all(per[k]['before'] and per[k]['after']
            and per[k]['before']['published_shas'] != per[k]['after']['published_shas'] for k in ks),
        before_published={k: (per[k]['before']['published'] if per[k]['before'] else None) for k in ks},
        after_published={k: (per[k]['after']['published'] if per[k]['after'] else None) for k in ks})
    put('R11_no_malformed_published_paths',
        all(per[k][m] is not None and not per[k][m]['malformed_published'] for k in ks for m in ('before', 'after')),
        detail='every published file has a non-empty relative_path and a 64-hex sha256')

    # ---------------------------------------------- 6.5.0 evidence-id recompute
    ev_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evid-650.mjs')
    order = sorted(envfiles)
    p = subprocess.run([a.node, ev_script, '--pkg650', a.pkg650] + [envfiles[k] for k in order],
                       capture_output=True, text=True)
    parsed = {}
    for line in p.stdout.splitlines():
        f = line.split('\t')
        if len(f) >= 3:
            parsed[os.path.basename(f[0]).replace('.json', '')] = (f[1], f[2])
    put('R9_evidence_id_authentic_650',
        p.returncode == 0 and len(parsed) == len(order) and all(v[1] == 'accept' for v in parsed.values()),
        node_exit=p.returncode, node_stderr=p.stderr.strip()[:400],
        receipts={n: {'stored_id': v[0], 'status': v[1]} for n, v in sorted(parsed.items())})

    # ---------------------------------------- receipt bytes stable across commits
    if a.skip_cross_rev:
        put('R12_receipts_stable_at_3310d8fa_and_tip', True, skipped=True)
    else:
        stable = {}
        for rev in ('3310d8fa27bfaa95ad858c4aaad6f6377f853982', '01a44dbf45913a1bdcabbbfb85b7bb9d232cb930'):
            git(root, 'cat-file', '-e', f'{rev}^{{commit}}')
            stable[rev] = all(show(root, rev, f'{EVDIR}/{k}/{m}.json') == show(root, a.rev, f'{EVDIR}/{k}/{m}.json')
                              for k in ks for m in ('before', 'after'))
        put('R12_receipts_stable_at_3310d8fa_and_tip', all(stable.values()), per_rev=stable)

    # ------------------------------------------------------------- run records
    after_sha = per[ks[0]]['run']['after'].get('sasquatch_sha256')
    r13 = {}
    for k in ks:
        b, af = per[k]['run']['before'], per[k]['run']['after']
        r13[k] = {
            'before_sasquatch_empty': b.get('sasquatch') == '',
            'after_sasquatch_set': bool(af.get('sasquatch')) and bool(HEX64.match(af.get('sasquatch_sha256') or '')),
            'after_sha_matches_s107_member': af.get('sasquatch_sha256') == after_sha,
            'exits_zero': b.get('exit') == 0 and af.get('exit') == 0,
            'after_not_before_utc': (af.get('utc') or '') >= (b.get('utc') or ''),
        }
    put('R13_run_records', all(all(v.values()) for v in r13.values()),
        per_carrier=r13, after_sasquatch_sha256=after_sha,
        all_after_sha_same=len({per[k]['run']['after'].get('sasquatch_sha256') for k in ks}) == 1)

    put('R14_published_bytes_arithmetic',
        all(per[k][m] is not None and per[k][m]['published_bytes'] == per[k][m]['size_sum']
            for k in ks for m in ('before', 'after')),
        per_carrier={k: {m: ({'published_bytes': per[k][m]['published_bytes'], 'size_sum': per[k][m]['size_sum']}
                            if per[k][m] else None) for m in ('before', 'after')} for k in ks})

    r15 = {}
    for k in ks:
        orun = per[k]['oracle_run']
        after_chunks = per[k]['after']['chunks'] if per[k]['after'] else []
        sq = [ch for ch in after_chunks if ch.get('handler') == 'squashfs_v4_le']
        offsets = {ch['root_file_range']['offset'] for ch in sq if ch.get('root_file_range')}
        r15[k] = {
            'regular_files_matches_rows': orun.get('regular_files') == per[k]['oracle_rows'],
            'offset_matches_chunk': (orun.get('squashfs_offset') in offsets) if offsets else None,
            'carrier_sha_matches': orun.get('carrier_sha256') == per[k]['sha256'],
            'oracle_offsets': sorted(offsets),
            'oracle_run_offset': orun.get('squashfs_offset'),
        }
    put('R15_oracle_run_cross_check',
        all(v['regular_files_matches_rows'] and v['carrier_sha_matches'] and v['offset_matches_chunk'] is not False
            for v in r15.values()), per_carrier=r15)

    # ------------------------------------- independent oracle reproduction K1/K2
    if a.skip_oracle_repro:
        put('O1_oracle_reproduced_unsquashfs', False, skipped=True)
    else:
        repro = {}
        for k in ('K1', 'K2'):
            fx = next((c['path'] for c in spec['carriers'] if c['id'] == k), None)
            blob = show(root, a.rev, fx) if fx else None
            if blob is None:
                repro[k] = {'ok': False, 'error': 'fixture not committed'}
                continue
            d = os.path.join(work, f'repro-{k}')
            os.makedirs(d, exist_ok=True)
            carrier = os.path.join(d, 'carrier.bin')
            open(carrier, 'wb').write(blob)
            import hashlib
            got_sha = hashlib.sha256(blob).hexdigest()
            out = os.path.join(d, 'out')
            r = subprocess.run([a.unsquashfs, '-no-progress', '-d', out, carrier],
                               capture_output=True, text=True)
            rows = []
            for dirpath, dirnames, filenames in os.walk(out):
                for fn in filenames:
                    fp = os.path.join(dirpath, fn)
                    if os.path.islink(fp) or not os.path.isfile(fp):
                        continue
                    rel = os.path.relpath(fp, out)
                    h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
                    rows.append((rel, h, os.path.getsize(fp)))
            want = [(rel, sha, size) for rel, sha, size in oracle_rows(show(root, a.rev, f'{EVDIR}/{k}/oracle.tsv'))]
            repro[k] = {
                'ok': r.returncode == 0 and sorted(rows) == sorted(want) and got_sha == per[k]['sha256'],
                'fixture': fx, 'fixture_sha256': got_sha, 'expected_fixture_sha256': per[k]['sha256'],
                'unsquashfs_exit': r.returncode, 'rows': len(rows), 'oracle_rows': len(want),
                'diff': sorted(set(rows) ^ set(want))[:5],
                'unsquashfs_stderr_head': r.stderr.strip().splitlines()[:1],
            }
        put('O1_oracle_reproduced_unsquashfs', all(v.get('ok') for v in repro.values()), per_carrier=repro)

    # ------------------------------------------------------------- surfaces
    prov = text(root, a.rev, 'PROVINCE.md')
    plines = prov.splitlines() if prov is not None else []
    sec = section_lines(plines, CORE_HEADING)
    core_rows = [(i + 1, l) for i, l in
                 enumerate(plines[sec[0] + 1:sec[1]], start=sec[0] + 1) if l.lstrip().startswith('|')] if sec else []
    hit_rows = [(n, l) for n, l in core_rows if TOKEN_SASQ.search(cells(l)[0]) and ENTRY in l]
    put('S1_province_core_row', sec is not None and bool(hit_rows),
        heading_line=(sec[0] + 1) if sec else None,
        row_lines=[n for n, _ in hit_rows],
        row_cites_entry_path=bool(hit_rows) and all(ENTRY in l for _, l in hit_rows),
        first_cell=[cells(l)[0] for _, l in hit_rows],
        table_data_rows=len([1 for n, _ in core_rows]))

    fb = header_bullet(plines, r'^- \*\*sasquatch\*\*')
    fsec = section_lines(plines, FRONTIER_HEADING)
    bullet_in_section = bool(fb and fsec and fsec[0] < fb[0] < fsec[1])
    bullet_dated = bool(fb and is_dated_note(fb[2]))
    bullet_cites = bool(fb and ENTRY in fb[2])
    put('S2a_province_bullet_carries_dated_note_citing_entry',
        bullet_in_section and bullet_dated and bullet_cites,
        bullet_line=(fb[0] + 1) if fb else None,
        bullet_span=((fb[0] + 1), fb[1]) if fb else None,
        in_frontier_section=bullet_in_section,
        bullet_is_dated_note=bullet_dated,
        bullet_cites_entry_path=bullet_cites,
        bullet_text=fb[2][:200] if fb else None)

    notes = [(i + 1, l) for i, l in enumerate(plines) if is_dated_note(l) and TOKEN_SASQ.search(l)]
    note_state = [{'line': n, 'cites_entry_path': ENTRY in l, 'cites_entry_stem': STEM in l,
                   'cites_dep_entry': DEP_ENTRY in l,
                   'in_core_section': bool(sec and sec[0] < n - 1 < sec[1]),
                   'in_frontier_section': bool(fsec and fsec[0] < n - 1 < fsec[1])} for n, l in notes]
    put('S2b_province_dated_sasquatch_note_cites_entry',
        any(s['cites_entry_path'] or s['cites_entry_stem'] for s in note_state),
        notes=note_state)

    readme = text(root, a.rev, 'corpus/README.md')
    rlines = readme.splitlines() if readme is not None else []
    fw = [(i + 1, l) for i, l in enumerate(rlines) if l.lstrip().startswith('| Firmware')]
    fw_sasq = [(n, l) for n, l in fw if TOKEN_SASQ.search(l)]
    fw_notes = []
    for n, _l in fw_sasq:
        for idx in range(max(0, n - 3), min(len(rlines), n + 2)):
            if is_dated_note(rlines[idx]) and TOKEN_SASQ.search(rlines[idx]):
                fw_notes.append(idx + 1)
    put('S3_readme_firmware_sasquatch_line_carries_dated_note',
        bool(fw_sasq) and any(n in fw_notes or abs(n - x) <= 2 for n, _ in fw_sasq for x in fw_notes),
        firmware_row=[n for n, _ in fw], firmware_row_mentions_sasquatch=[n for n, _ in fw_sasq],
        firmware_row_still_says_blocked=any('recursion blocked by missing sasquatch' in l for _, l in fw_sasq),
        firmware_row_dated_note_lines=fw_notes)

    fstart = section_lines(rlines, '## Frontier')
    rf = [(i + 1, l) for i, l in enumerate(rlines)
          if (not fstart or fstart[0] < i < fstart[1]) and TOKEN_SASQ.search(l)]
    rf_notes = [(n, l) for n, l in rf if is_dated_note(l)]
    rf_cites = [(n, l) for n, l in rf_notes if STEM in l or ENTRY in l]
    put('S4_readme_frontier_sasquatch_line_carries_dated_note',
        bool(rf_notes) and any(abs(a[0] - b[0]) <= 2 for a in rf for b in rf_notes),
        frontier_section=(fstart[0] + 1, fstart[1]) if fstart else None,
        sasquatch_lines=[n for n, _ in rf],
        dated_note_lines=[n for n, _ in rf_notes],
        dated_note_cites_entry_stem=[n for n, _ in rf_cites],
        exact_path_cited=any(ENTRY in l for _, l in rf_notes),
        excerpts=[{'line': n, 'text': l[:200]} for n, l in rf])

    cm = section_lines(rlines, '## Coverage map')
    cm_rows = [(i + 1, l) for i, l in enumerate(rlines[cm[0] + 1:cm[1]], start=cm[0] + 1)
               if l.lstrip().startswith('|')] if cm else []
    cm_hits = [(n, l) for n, l in cm_rows if STEM in l]
    put('S5_readme_coverage_map_row', bool(cm_hits), row_lines=[n for n, _ in cm_hits],
        is_table_data_row=all(len(cells(l)) >= 2 for _, l in cm_hits))

    ent = text(root, a.rev, ENTRY)
    ent_ids = set()
    if ent:
        for line in ent.splitlines():
            if line.startswith('source:'):
                ent_ids |= set(SID.findall(line))
    put('S6_entry_present_with_sources', ent is not None and bool(ent_ids),
        source_ids=sorted(ent_ids), has_s107='S107' in ent_ids, has_s108='S108' in ent_ids,
        has_s109='S109' in ent_ids, lines=len(ent.splitlines()) if ent else 0)

    reg = text(root, a.rev, 'corpus/SOURCES.md')
    reg_rows = {}
    if reg:
        for i, line in enumerate(reg.splitlines(), 1):
            m = re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|', line)
            if m:
                reg_rows.setdefault(m.group(1), []).append((i, cells(line)))
    tok_state, ok_ids = {}, []
    for sid in sorted(ent_ids):
        states = []
        for n, c in reg_rows.get(sid, []):
            used = [u.strip() for u in c[10].split(',')] if len(c) >= 11 else []
            states.append({'line': n, 'cells': len(c), 'opened': c[8] if len(c) >= 11 else None,
                           'used_by_item_equals_entry': ENTRY in used,
                           'used_by_cell_contains_entry_substring': ENTRY in (c[10] if len(c) >= 11 else '')})
            if len(c) == 11 and c[8] == OPENED and ENTRY in used:
                ok_ids.append((sid, n))
        tok_state[sid] = states
    put('S7_source_rows_opened_today_with_entry_in_used_by',
        bool(ok_ids) and len(ok_ids) == len(ent_ids),
        qualifying_rows=[{'id': s, 'line': n} for s, n in ok_ids], per_token=tok_state)

    # --------------------------------------------- stated counts vs observed
    stated = {}
    prov_row = hit_rows[0][1] if hit_rows else ''
    m = re.search(r'oracle (\d+), (\d+), ([\d,]+), ([\d,]+) regular files', prov_row)
    if m:
        stated['province_row'] = [int(m.group(1)), int(m.group(2)),
                                  int(m.group(3).replace(',', '')), int(m.group(4).replace(',', ''))]
    stated['readme_row'] = [[int(x), int(y), int(z)] for x, y, z in
                            re.findall(r'K(\d) (\d+)/(\d+)', cm_hits[0][1] if cm_hits else '')]
    observed = {k: {'oracle_rows': per[k]['oracle_rows'],
                    'after_matched': len(per[k]['after']['hits']) if per[k]['after'] else None} for k in ks}
    ok_counts = True
    if 'province_row' in stated:
        ok_counts &= stated['province_row'] == [per[k]['oracle_rows'] for k in ('K1', 'K2', 'K3', 'K4')]
    if stated['readme_row']:
        for kid, matched, total in stated['readme_row']:
            k = f'K{kid}'
            ok_counts &= matched == total == len(per[k]['after']['hits']) == per[k]['oracle_rows']
    else:
        ok_counts = False
    put('X1_stated_counts_equal_observed', ok_counts, stated=stated, observed=observed)

    res['all_true'] = all(v['ok'] for v in C.values())
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    for cid in sorted(C):
        v = C[cid]
        print(f"{'TRUE ' if v['ok'] else 'FALSE'}  {cid}")
    print('all_true:', res['all_true'])
    import shutil
    shutil.rmtree(work, ignore_errors=True)
    return 0 if res['all_true'] else 1


if __name__ == '__main__':
    sys.exit(main())
```

## Appendix B — `evid-650.mjs` (verbatim)

```javascript
#!/usr/bin/env node
/**
 * R36W2ExecC1Strict — independent recompute of a receipt's evidence id under the
 * rea-agents 6.5.0 rule.
 *
 * The rule is not retyped here. This script imports the 6.5.0 package's own
 * `parseEvidence` (dist/domain/evidence.js), which strips `evidence_id`, rebuilds
 * the semantic projection and rejects the record when the stored id differs
 * (evidence.js:134-138).
 *
 * Usage: node evid-650.mjs --pkg650 <pkg root> ENVELOPE...
 * Prints: <path>\t<stored id>\taccept|reject:<first issue>
 */
import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import { join } from "node:path";

let pkg = null;
const files = [];
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--pkg650") { pkg = argv[i + 1]; i += 1; }
    else files.push(argv[i]);
}
if (!pkg || files.length === 0) {
    console.error("usage: evid-650.mjs --pkg650 <pkg root> ENVELOPE...");
    process.exit(2);
}
const mod = await import(pathToFileURL(join(pkg, "dist", "domain", "evidence.js")).href);
const parseEvidence = mod.parseEvidence;
if (typeof parseEvidence !== "function") {
    console.error("parseEvidence not exported by the 6.5.0 package");
    process.exit(2);
}
let rejected = 0;
for (const f of files) {
    let record;
    try {
        const raw = JSON.parse(await readFile(f, "utf8"));
        record = raw && typeof raw === "object" && raw.data && typeof raw.data === "object"
            && "evidence_id" in raw.data ? raw.data : raw;
    } catch (error) {
        console.log([f, "(unreadable)", "unreadable:" + error.message].join("\t"));
        rejected += 1;
        continue;
    }
    const stored = record && typeof record.evidence_id === "string" ? record.evidence_id : "(none)";
    let status;
    try {
        parseEvidence(record);
        status = "accept";
    } catch (error) {
        const first = error && Array.isArray(error.issues) && error.issues[0]
            ? `${error.issues[0].code}:${error.issues[0].message}:${(error.issues[0].path || []).join(".")}`
            : String(error && error.message ? error.message : error);
        status = "reject:" + first.replace(/[\t\n]/g, " ");
        rejected += 1;
    }
    console.log([f, stored, status].join("\t"));
}
process.exit(rejected === 0 ? 0 : 1);
```

## Appendix C — `forge-rehash.mjs` (verbatim; the forgery control)

```javascript
#!/usr/bin/env node
/**
 * R36W2ExecC1Strict — forge control. Re-seals an edited receipt under the
 * rea-agents 6.5.0 evidence-id rule so a structure-only reader cannot tell the
 * record was never produced by an extraction run.
 *
 * The projection is transcribed from <pkg>/dist/domain/evidence.js
 * (`const semanticProjection = ...`) and the hash is the package's own
 * digestCanonicalValue. The result is checked by the package's own parseEvidence
 * before it is written, so an inexact transcription fails loudly.
 *
 * Usage: node forge-rehash.mjs --pkg650 <pkg root> ENVELOPE.json
 */
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { join } from "node:path";

const argv = process.argv.slice(2);
let pkg = null;
const files = [];
for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--pkg650") { pkg = argv[i + 1]; i += 1; } else files.push(argv[i]);
}
if (!pkg || files.length !== 1) {
    console.error("usage: forge-rehash.mjs --pkg650 <pkg root> ENVELOPE.json");
    process.exit(2);
}
const { digestCanonicalValue } = await import(
    pathToFileURL(join(pkg, "dist", "domain", "canonicalDigest.js")).href);
const { parseEvidence } = await import(pathToFileURL(join(pkg, "dist", "domain", "evidence.js")).href);

const projection = (evidence) => ({
    subject: evidence.subject === null
        ? null
        : {
            digest: evidence.subject.digest,
            format: evidence.subject.format,
            architecture: evidence.subject.architecture,
        },
    provider: evidence.provider,
    analysis_profile: evidence.analysis_profile,
    predicate_type: evidence.predicate_type,
    operation: evidence.operation,
    parameters: evidence.parameters,
    raw_result: evidence.raw_result,
    normalized_result: evidence.normalized_result,
    confidence: evidence.confidence,
    authority: evidence.authority,
    environment: evidence.environment,
    limitations: evidence.limitations,
    ...(evidence.relationship_coverage === null
        ? {}
        : { relationship_coverage: evidence.relationship_coverage }),
    locations: evidence.locations,
    evidence_links: evidence.evidence_links,
});

const file = files[0];
const raw = JSON.parse(readFileSync(file, "utf8"));
const record = raw && typeof raw === "object" && raw.data ? raw.data : raw;
const { evidence_id: _old, ...withoutId } = record;
const id = `ev_${digestCanonicalValue(projection(withoutId), "Evidence")}`;
const sealed = { ...withoutId, evidence_id: id };
parseEvidence(sealed);
writeFileSync(file, JSON.stringify(raw && raw.data ? { ...raw, data: sealed } : sealed));
console.log(`${file}\t${id}\tsealed-and-accepted`);
```

## Appendix D — `selftest-strict.py` (verbatim)

```python3
#!/usr/bin/env python3
"""R36W2ExecC1Strict — calibration controls for strict-c1.py.

Each case builds a throwaway git fixture from the R36-C1 landing revision
(`git archive ffc81341 -- <paths>` into the fixture), commits that as the freeze,
applies one mutation, commits again, and runs strict-c1.py on the fixture with
`--rev HEAD --freeze <freeze> --skip-cross-rev`. A case passes when every
condition named in `want_false` reads false and every condition named in
`want_true` reads true.

Cases that must turn red prove the checker is not structure-blind; cases that
must turn green (notes added, used-by repaired) prove the surface detectors are
not stuck false. The last case re-seals a fabricated receipt with the 6.5.0
package's own digest code: it is expected to read GREEN, and records the one
blind spot the checker shares with the frozen counter (receipt integrity is not
provenance).
"""
import json, os, shutil, subprocess, sys, tempfile

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC_REV = 'ffc813417d3bceeeb7b028b12ce0be8a5dc33d95'
PKG650 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
CHECKER = os.path.join(SEAT, 'strict-c1.py')
EVDIR = 'corpus/evidence/round-36/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md'
PATHS = ['PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', EVDIR, ENTRY]
GITENV = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
              GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')

S2A = 'S2a_province_bullet_carries_dated_note_citing_entry'
S2B = 'S2b_province_dated_sasquatch_note_cites_entry'
S3 = 'S3_readme_firmware_sasquatch_line_carries_dated_note'
S4 = 'S4_readme_frontier_sasquatch_line_carries_dated_note'
BASE_RED = {S2A, S2B, S3}          # the three false readings the lane shows as landed


def git(d, *args, check=True):
    p = subprocess.run(['git', '-C', d, *args], capture_output=True, text=True, env=GITENV)
    if check and p.returncode != 0:
        raise SystemExit(f'git {" ".join(args)}: {p.stderr.strip()}')
    return p


def build_fixture(dst):
    OS_OK = subprocess.run(['git', '-C', LANE, 'rev-parse', '--show-toplevel'],
                           capture_output=True, text=True)
    if OS_OK.returncode != 0:
        raise SystemExit('lane is not a git repo')
    src = subprocess.run(['git', '-C', LANE, 'archive', SRC_REV, '--'] + PATHS, capture_output=True)
    if src.returncode != 0:
        raise SystemExit('git archive failed: ' + src.stderr.decode(errors='replace'))
    subprocess.run(['tar', '-x', '-C', dst], input=src.stdout, check=True)
    git(dst, 'init', '-q')
    top = git(dst, 'rev-parse', '--show-toplevel').stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dst):
        raise SystemExit('fixture toplevel mismatch')
    git(dst, 'add', '-A')
    git(dst, 'commit', '-qm', 'freeze')
    return git(dst, 'rev-parse', 'HEAD').stdout.strip()


def commit(dst, msg):
    git(dst, 'add', '-A')
    git(dst, 'commit', '-qm', msg, '--allow-empty')
    return git(dst, 'rev-parse', 'HEAD').stdout.strip()


def env_path(dst, k, mode):
    return os.path.join(dst, EVDIR, k, f'{mode}.json')


def load(dst, k, mode):
    return json.load(open(env_path(dst, k, mode)))


def save(dst, k, mode, env, rehash=False):
    p = env_path(dst, k, mode)
    json.dump(env, open(p, 'w'), indent=1)
    if rehash:
        r = subprocess.run(['node', os.path.join(SEAT, 'forge-rehash.mjs'),
                            '--pkg650', PKG650, p], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit('rehash failed: ' + r.stderr.strip())


def text_path(dst, rel):
    return os.path.join(dst, rel)


def mutate_text(dst, rel, fn):
    p = text_path(dst, rel)
    lines = open(p).read().splitlines(keepends=True)
    open(p, 'w').write(''.join(fn(lines)))


# --------------------------------------------------------------- mutations
def m_none(dst):
    return


def m_drop_published(dst):
    e = load(dst, 'K3', 'after')
    rows = [l.split('\t')[0] for l in open(os.path.join(dst, EVDIR, 'K3', 'oracle.tsv')).read().splitlines() if l]
    files = e['normalized_result']['files']
    for i, f in enumerate(files):
        if any(f['relative_path'].endswith('/' + r) for r in rows):
            del files[i]
            break
    else:
        raise SystemExit('K3 after publishes no oracle row')
    save(dst, 'K3', 'after', e)


def m_change_sha(dst):
    e = load(dst, 'K1', 'after')
    e['normalized_result']['files'][0]['sha256'] = '0' * 64
    save(dst, 'K1', 'after', e)


def m_change_size(dst):
    e = load(dst, 'K2', 'after')
    e['normalized_result']['files'][0]['size'] += 1
    save(dst, 'K2', 'after', e)


def m_add_after_gap(dst):
    e = load(dst, 'K1', 'after')
    e['normalized_result']['extraction_gaps'].append({
        'kind': 'missing-extractor-dependency', 'dependencies': ['sasquatch'],
        'handler': 'squashfs_v4_le', 'input_path': '$input'})
    save(dst, 'K1', 'after', e, rehash=True)


def m_remove_before_gap(dst):
    e = load(dst, 'K2', 'before')
    e['normalized_result']['extraction_gaps'] = []
    save(dst, 'K2', 'before', e, rehash=True)


def m_rename_matched_path(dst):
    e = load(dst, 'K4', 'after')
    files = e['normalized_result']['files']
    rel = 'usr/bin/nvim'
    for f in files:
        if f['relative_path'].endswith('/' + rel):
            f['relative_path'] += 'X'
            break
    else:
        raise SystemExit('K4 after has no published usr/bin/nvim')
    save(dst, 'K4', 'after', e, rehash=True)


def m_forge_oracle_copy(dst):
    """Structure-blind forgery without re-hashing: oracle rows as published files."""
    e = load(dst, 'K1', 'after')
    rows = [l.split('\t') for l in open(os.path.join(dst, EVDIR, 'K1', 'oracle.tsv')).read().splitlines() if l]
    nr = e['normalized_result']
    nr['files'] = [{'relative_path': 'firmware.bin_extract/' + r[0], 'sha256': r[1], 'size': int(r[2])}
                   for r in rows]
    nr['extraction_gaps'] = []
    nr['published_bytes'] = sum(int(r[2]) for r in rows)
    save(dst, 'K1', 'after', e)


def m_forge_oracle_copy_rehashed(dst):
    m_forge_oracle_copy(dst)
    e = load(dst, 'K1', 'after')
    save(dst, 'K1', 'after', e, rehash=True)


def m_drop_core_row(dst):
    mutate_text(dst, 'PROVINCE.md', lambda ls: [l for l in ls if not l.startswith('| sasquatch squashfs recursion |')])


def m_break_used_by(dst):
    def fn(ls):
        return [l.replace('| corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |',
                          '| corpus/lessons/round-36.md |') if l.startswith('| S107 |') else l for l in ls]
    mutate_text(dst, 'corpus/SOURCES.md', fn)


def m_append_oracle_row(dst):
    p = os.path.join(dst, EVDIR, 'K1', 'oracle.tsv')
    open(p, 'a').write('extra.txt\t' + '1' * 64 + '\t1\n')


def m_change_carrier_sha(dst):
    p = os.path.join(dst, EVDIR, 'carriers.json')
    spec = json.load(open(p))
    spec['carriers'][0]['sha256'] = '2' * 64
    json.dump(spec, open(p, 'w'), indent=1)


def m_break_coverage_stem(dst):
    mutate_text(dst, 'corpus/README.md',
                lambda ls: [l.replace('2026-10-26-r36-sasquatch-squashfs-recursion', '2026-10-26-r36-other') for l in ls])


def m_note_cites_entry(dst):
    """Add the entry path to the existing PROVINCE dated Frontier note."""
    mutate_text(dst, 'PROVINCE.md',
                lambda ls: [l.replace('(`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`)',
                                      '(`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`; `' + ENTRY + '`)')
                            if l.startswith('Frontier note, 2026-10-26:') else l for l in ls])


def m_bullet_carries_note(dst):
    """Turn the Frontier bullet itself into a dated supersession note citing the entry."""
    def fn(ls):
        out = []
        for l in ls:
            out.append(l)
            if l.startswith('- **sasquatch**'):
                out.append(f"  Superseded 2026-10-26 for LE SquashFS v4 by `{ENTRY}`.\n")
        return out
    mutate_text(dst, 'PROVINCE.md', fn)


def m_firmware_row_note(dst):
    """Insert a dated note directly after the README Firmware row."""
    def fn(ls):
        out = []
        for l in ls:
            out.append(l)
            if l.lstrip().startswith('| Firmware'):
                out.append('| Firmware (updated) | dated note 2026-10-26: sasquatch recursion now Core, see `'
                           + ENTRY + '` | superseded 2026-10-13 state kept as history |\n')
        return out
    mutate_text(dst, 'corpus/README.md', fn)


CASES = [
    ('green (landing copy)', m_none,
     {'want_false': set(BASE_RED), 'want_true': {'R1_carriers_frozen_unchanged_and_ids', 'R4_after_publishes_every_oracle_row',
                                                 'S1_province_core_row', 'S7_source_rows_opened_today_with_entry_in_used_by'}}),
    ('drop one published file (K3 after)', m_drop_published, {'want_false': {'R4_after_publishes_every_oracle_row'}}),
    ('change one published sha256 (K1 after)', m_change_sha, {'want_false': {'R4_after_publishes_every_oracle_row'}}),
    ('change one published size (K2 after)', m_change_size, {'want_false': {'R4_after_publishes_every_oracle_row'}}),
    ('add a sasquatch gap to after (K1)', m_add_after_gap, {'want_false': {'R5_after_no_sasquatch_gap'}}),
    ('remove the before sasquatch gap (K2)', m_remove_before_gap, {'want_false': {'R6_before_names_missing_sasquatch'}}),
    ('rename a matched published path (K4)', m_rename_matched_path, {'want_false': {'R4_after_publishes_every_oracle_row'}}),
    ('forge oracle copy, not re-hashed (K1)', m_forge_oracle_copy,
     {'want_true': {'R4_after_publishes_every_oracle_row'}, 'want_false': {'R9_evidence_id_authentic_650'}}),
    ('forge oracle copy, re-hashed with 6.5.0 (K1)', m_forge_oracle_copy_rehashed,
     {'want_true': {'R4_after_publishes_every_oracle_row', 'R5_after_no_sasquatch_gap', 'R9_evidence_id_authentic_650'}}),
    ('delete the PROVINCE Core row', m_drop_core_row, {'want_false': {'S1_province_core_row'}}),
    ('break S107 used-by', m_break_used_by, {'want_false': {'S7_source_rows_opened_today_with_entry_in_used_by'}}),
    ('append an oracle row after freeze', m_append_oracle_row, {'want_false': {'R2_oracle_frozen_nonempty'}}),
    ('change a carrier sha256', m_change_carrier_sha, {'want_false': {'R1_carriers_frozen_unchanged_and_ids'}}),
    ('break the README coverage stem', m_break_coverage_stem, {'want_false': {'S5_readme_coverage_map_row'}}),
    ('add the entry path to the PROVINCE Frontier note', m_note_cites_entry, {'want_true': {S2B}}),
    ('make the PROVINCE Frontier bullet carry the note', m_bullet_carries_note, {'want_true': {S2A}}),
    ('add a dated note after the README Firmware row', m_firmware_row_note, {'want_true': {S3}}),
]


def run(dst, rev, freeze):
    out = os.path.join(dst, 'receipt.json')
    r = subprocess.run([sys.executable, '-I', '-B', CHECKER, '--root', dst, '--rev', rev,
                        '--freeze', freeze, '--pkg650', PKG650, '--skip-cross-rev',
                        '--json-out', out], capture_output=True, text=True, cwd=SEAT)
    if not os.path.exists(out):
        raise SystemExit('checker produced no receipt:\n' + r.stdout + r.stderr)
    return json.load(open(out))['conditions']


def main():
    sroot = tempfile.mkdtemp(prefix='strict-selftest.')
    fails, results = [], []
    try:
        for name, mut, want in CASES:
            d = os.path.join(sroot, 'fx.' + str(len(results)))
            os.makedirs(d)
            try:
                freeze = build_fixture(d)
                mut(d)
                rev = commit(d, 'mutation: ' + name)
                conds = run(d, rev, freeze)
                bad = [c for c in want.get('want_false', ()) if conds.get(c, {}).get('ok') is not False]
                bad += [c for c in want.get('want_true', ()) if conds.get(c, {}).get('ok') is not True]
                results.append({'case': name, 'pass': not bad, 'unexpected': bad,
                                'false_conditions': sorted(k for k, v in conds.items() if not v['ok']),
                                'detail': {c: conds.get(c) for c in bad}})
                if bad:
                    fails.append(f'{name}: {bad} {json.dumps({c: conds.get(c) for c in bad})[:400]}')
            finally:
                shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(sroot, ignore_errors=True)
    print(json.dumps({'selftest': 'strict-c1', 'cases': len(CASES),
                      'pass': len(CASES) - len(fails), 'failures': fails,
                      'detail': results}, indent=1))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
```

## Appendix E — measured conditions at `ffc81341` (checker `--json-out`, `hits`/`published_shas`
lists elided)

```json
{
 "all_true": false,
 "conditions": {
  "O1_oracle_reproduced_unsquashfs": {
   "ok": true,
   "per_carrier": {
    "K1": {
     "diff": [],
     "expected_fixture_sha256": "93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589",
     "fixture": "corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh",
     "fixture_sha256": "93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589",
     "ok": true,
     "oracle_rows": 3,
     "rows": 3,
     "unsquashfs_exit": 0,
     "unsquashfs_stderr_head": []
    },
    "K2": {
     "diff": [],
     "expected_fixture_sha256": "ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f",
     "fixture": "corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh",
     "fixture_sha256": "ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f",
     "ok": true,
     "oracle_rows": 4,
     "rows": 4,
     "unsquashfs_exit": 0,
     "unsquashfs_stderr_head": []
    }
   }
  },
  "R10_before_after_differ": {
   "after_published": {
    "K1": 3,
    "K2": 4,
    "K3": 2147,
    "K4": 2147
   },
   "before_published": {
    "K1": 0,
    "K2": 0,
    "K3": 2,
    "K4": 2
   },
   "ok": true
  },
  "R11_no_malformed_published_paths": {
   "detail": "every published file has a non-empty relative_path and a 64-hex sha256",
   "ok": true
  },
  "R12_receipts_stable_at_3310d8fa_and_tip": {
   "ok": true,
   "per_rev": {
    "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930": true,
    "3310d8fa27bfaa95ad858c4aaad6f6377f853982": true
   }
  },
  "R13_run_records": {
   "after_sasquatch_sha256": "ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754",
   "all_after_sha_same": true,
   "ok": true,
   "per_carrier": {
    "K1": {
     "after_not_before_utc": true,
     "after_sasquatch_set": true,
     "after_sha_matches_s107_member": true,
     "before_sasquatch_empty": true,
     "exits_zero": true
    },
    "K2": {
     "after_not_before_utc": true,
     "after_sasquatch_set": true,
     "after_sha_matches_s107_member": true,
     "before_sasquatch_empty": true,
     "exits_zero": true
    },
    "K3": {
     "after_not_before_utc": true,
     "after_sasquatch_set": true,
     "after_sha_matches_s107_member": true,
     "before_sasquatch_empty": true,
     "exits_zero": true
    },
    "K4": {
     "after_not_before_utc": true,
     "after_sasquatch_set": true,
     "after_sha_matches_s107_member": true,
     "before_sasquatch_empty": true,
     "exits_zero": true
    }
   }
  },
  "R14_published_bytes_arithmetic": {
   "ok": true,
   "per_carrier": {
    "K1": {
     "after": {
      "published_bytes": 70086,
      "size_sum": 70086
     },
     "before": {
      "published_bytes": 0,
      "size_sum": 0
     }
    },
    "K2": {
     "after": {
      "published_bytes": 273971,
      "size_sum": 273971
     },
     "before": {
      "published_bytes": 0,
      "size_sum": 0
     }
    },
    "K3": {
     "after": {
      "published_bytes": 51122564,
      "size_sum": 51122564
     },
     "before": {
      "published_bytes": 11454968,
      "size_sum": 11454968
     }
    },
    "K4": {
     "after": {
      "published_bytes": 51792724,
      "size_sum": 51792724
     },
     "before": {
      "published_bytes": 11356680,
      "size_sum": 11356680
     }
    }
   }
  },
  "R15_oracle_run_cross_check": {
   "ok": true,
   "per_carrier": {
    "K1": {
     "carrier_sha_matches": true,
     "offset_matches_chunk": true,
     "oracle_offsets": [
      0
     ],
     "oracle_run_offset": 0,
     "regular_files_matches_rows": true
    },
    "K2": {
     "carrier_sha_matches": true,
     "offset_matches_chunk": true,
     "oracle_offsets": [
      0
     ],
     "oracle_run_offset": 0,
     "regular_files_matches_rows": true
    },
    "K3": {
     "carrier_sha_matches": true,
     "offset_matches_chunk": true,
     "oracle_offsets": [
      944632
     ],
     "oracle_run_offset": 944632,
     "regular_files_matches_rows": true
    },
    "K4": {
     "carrier_sha_matches": true,
     "offset_matches_chunk": true,
     "oracle_offsets": [
      936456
     ],
     "oracle_run_offset": 936456,
     "regular_files_matches_rows": true
    }
   }
  },
  "R16_each_oracle_row_matched_by_exactly_one_file": {
   "distinct_matched": {
    "K1": 3,
    "K2": 4,
    "K3": 2130,
    "K4": 2130
   },
   "match_counts": {
    "K1": [
     1
    ],
    "K2": [
     1
    ],
    "K3": [
     1
    ],
    "K4": [
     1
    ]
   },
   "ok": true,
   "rows": {
    "K1": 3,
    "K2": 4,
    "K3": 2130,
    "K4": 2130
   }
  },
  "R1_carriers_frozen_unchanged_and_ids": {
   "bytes_identical": true,
   "carrier_ids": [
    "K1",
    "K2",
    "K3",
    "K4"
   ],
   "ok": true
  },
  "R2_oracle_frozen_nonempty": {
   "distinct": {
    "K1": 3,
    "K2": 4,
    "K3": 2116,
    "K4": 2116
   },
   "ok": true,
   "rows": {
    "K1": 3,
    "K2": 4,
    "K3": 2130,
    "K4": 2130
   }
  },
  "R3_before_frozen_and_both_present": {
   "before_frozen": {
    "K1": true,
    "K2": true,
    "K3": true,
    "K4": true
   },
   "ok": true,
   "present": {
    "K1": {
     "after": true,
     "before": true
    },
    "K2": {
     "after": true,
     "before": true
    },
    "K3": {
     "after": true,
     "before": true
    },
    "K4": {
     "after": true,
     "before": true
    }
   }
  },
  "R4_after_publishes_every_oracle_row": {
   "matched": {
    "K1": 3,
    "K2": 4,
    "K3": 2130,
    "K4": 2130
   },
   "ok": true,
   "rows": {
    "K1": 3,
    "K2": 4,
    "K3": 2130,
    "K4": 2130
   }
  },
  "R5_after_no_sasquatch_gap": {
   "gap_counts": {
    "K1": 0,
    "K2": 0,
    "K3": 0,
    "K4": 0
   },
   "ok": true,
   "sasquatch_mention_paths": {
    "K1": [],
    "K2": [],
    "K3": [],
    "K4": []
   }
  },
  "R6_before_names_missing_sasquatch": {
   "gap_counts": {
    "K1": 1,
    "K2": 1,
    "K3": 1,
    "K4": 1
   },
   "gaps": {
    "K1": [
     {
      "dependencies": [
       "sasquatch"
      ],
      "handler": "squashfs_v4_le",
      "kind": "missing-extractor-dependency"
     }
    ],
    "K2": [
     {
      "dependencies": [
       "sasquatch"
      ],
      "handler": "squashfs_v4_le",
      "kind": "missing-extractor-dependency"
     }
    ],
    "K3": [
     {
      "dependencies": [
       "sasquatch"
      ],
      "handler": "squashfs_v4_le",
      "kind": "missing-extractor-dependency"
     }
    ],
    "K4": [
     {
      "dependencies": [
       "sasquatch"
      ],
      "handler": "squashfs_v4_le",
      "kind": "missing-extractor-dependency"
     }
    ]
   },
   "ok": true
  },
  "R7_before_publishes_no_oracle_row": {
   "matched": {
    "K1": 0,
    "K2": 0,
    "K3": 0,
    "K4": 0
   },
   "ok": true
  },
  "R8_subject_operation_provider_pin": {
   "after": true,
   "before": true,
   "ok": true,
   "provider": {
    "K1": {
     "id": "unblob",
     "name": "Unblob",
     "version": "26.6.4"
    },
    "K2": {
     "id": "unblob",
     "name": "Unblob",
     "version": "26.6.4"
    },
    "K3": {
     "id": "unblob",
     "name": "Unblob",
     "version": "26.6.4"
    },
    "K4": {
     "id": "unblob",
     "name": "Unblob",
     "version": "26.6.4"
    }
   }
  },
  "R9_evidence_id_authentic_650": {
   "node_exit": 0,
   "node_stderr": "",
   "ok": true,
   "receipts": {
    "K1_after": {
     "status": "accept",
     "stored_id": "ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860"
    },
    "K1_before": {
     "status": "accept",
     "stored_id": "ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3"
    },
    "K2_after": {
     "status": "accept",
     "stored_id": "ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f"
    },
    "K2_before": {
     "status": "accept",
     "stored_id": "ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c"
    },
    "K3_after": {
     "status": "accept",
     "stored_id": "ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b"
    },
    "K3_before": {
     "status": "accept",
     "stored_id": "ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a"
    },
    "K4_after": {
     "status": "accept",
     "stored_id": "ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa"
    },
    "K4_before": {
     "status": "accept",
     "stored_id": "ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01"
    }
   }
  },
  "S1_province_core_row": {
   "first_cell": [
    "sasquatch squashfs recursion"
   ],
   "heading_line": 368,
   "ok": true,
   "row_cites_entry_path": true,
   "row_lines": [
    372
   ],
   "table_data_rows": 3
  },
  "S2a_province_bullet_carries_dated_note_citing_entry": {
   "bullet_cites_entry_path": false,
   "bullet_is_dated_note": false,
   "bullet_line": 156,
   "bullet_span": [
    156,
    157
   ],
   "bullet_text": "- **sasquatch** \u2014 unblob's squashfs recursion extractor (AUR-only); 7z fallback\n  covers the carved-image path today.",
   "in_frontier_section": true,
   "ok": false
  },
  "S2b_province_dated_sasquatch_note_cites_entry": {
   "notes": [
    {
     "cites_dep_entry": true,
     "cites_entry_path": false,
     "cites_entry_stem": false,
     "in_core_section": true,
     "in_frontier_section": false,
     "line": 374
    }
   ],
   "ok": false
  },
  "S3_readme_firmware_sasquatch_line_carries_dated_note": {
   "firmware_row": [
    44
   ],
   "firmware_row_dated_note_lines": [],
   "firmware_row_mentions_sasquatch": [
    44
   ],
   "firmware_row_still_says_blocked": true,
   "ok": false
  },
  "S4_readme_frontier_sasquatch_line_carries_dated_note": {
   "dated_note_cites_entry_stem": [
    233
   ],
   "dated_note_lines": [
    233
   ],
   "exact_path_cited": false,
   "excerpts": [
    {
     "line": 232,
     "text": "- sasquatch (AUR) \u2014 unblob squashfs recursion; 7z fallback covers today."
    },
    {
     "line": 233,
     "text": "- sasquatch \u2014 2026-10-26 dated note on the line above (kept as history): LE SquashFS v4 recursion is now Core (`2026-10-26-r36-sasquatch-squashfs-recursion`); \"AUR\" was one route, the producer documen"
    }
   ],
   "frontier_section": [
    226,
    238
   ],
   "ok": true,
   "sasquatch_lines": [
    232,
    233
   ]
  },
  "S5_readme_coverage_map_row": {
   "is_table_data_row": true,
   "ok": true,
   "row_lines": [
    89
   ]
  },
  "S6_entry_present_with_sources": {
   "has_s107": true,
   "has_s108": true,
   "has_s109": true,
   "lines": 215,
   "ok": true,
   "source_ids": [
    "S107",
    "S108",
    "S109"
   ]
  },
  "S7_source_rows_opened_today_with_entry_in_used_by": {
   "ok": true,
   "per_token": {
    "S107": [
     {
      "cells": 11,
      "line": 113,
      "opened": "2026-10-26",
      "used_by_cell_contains_entry_substring": true,
      "used_by_item_equals_entry": true
     }
    ],
    "S108": [
     {
      "cells": 11,
      "line": 114,
      "opened": "2026-10-26",
      "used_by_cell_contains_entry_substring": true,
      "used_by_item_equals_entry": true
     }
    ],
    "S109": [
     {
      "cells": 11,
      "line": 115,
      "opened": "2026-10-26",
      "used_by_cell_contains_entry_substring": true,
      "used_by_item_equals_entry": true
     }
    ]
   },
   "qualifying_rows": [
    {
     "id": "S107",
     "line": 113
    },
    {
     "id": "S108",
     "line": 114
    },
    {
     "id": "S109",
     "line": 115
    }
   ]
  },
  "X1_stated_counts_equal_observed": {
   "observed": {
    "K1": {
     "after_matched": 3,
     "oracle_rows": 3
    },
    "K2": {
     "after_matched": 4,
     "oracle_rows": 4
    },
    "K3": {
     "after_matched": 2130,
     "oracle_rows": 2130
    },
    "K4": {
     "after_matched": 2130,
     "oracle_rows": 2130
    }
   },
   "ok": true,
   "stated": {
    "province_row": [
     3,
     4,
     2130,
     2130
    ],
    "readme_row": [
     [
      1,
      3,
      3
     ],
     [
      2,
      4,
      4
     ]
    ]
   }
  }
 },
 "freeze": "790561d4e3aca732a434081aa9573ec2fa5fd7d0",
 "predicate": "P36-C1",
 "revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95"
}```

## Appendix F — selftest result (verbatim)

```json
{
 "selftest": "strict-c1",
 "cases": 17,
 "pass": 17,
 "failures": [],
 "detail": [
  {
   "case": "green (landing copy)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "drop one published file (K3 after)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R14_published_bytes_arithmetic",
    "R16_each_oracle_row_matched_by_exactly_one_file",
    "R4_after_publishes_every_oracle_row",
    "R9_evidence_id_authentic_650",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "change one published sha256 (K1 after)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R16_each_oracle_row_matched_by_exactly_one_file",
    "R4_after_publishes_every_oracle_row",
    "R9_evidence_id_authentic_650",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note",
    "X1_stated_counts_equal_observed"
   ],
   "detail": {}
  },
  {
   "case": "change one published size (K2 after)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R14_published_bytes_arithmetic",
    "R16_each_oracle_row_matched_by_exactly_one_file",
    "R4_after_publishes_every_oracle_row",
    "R9_evidence_id_authentic_650",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note",
    "X1_stated_counts_equal_observed"
   ],
   "detail": {}
  },
  {
   "case": "add a sasquatch gap to after (K1)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R5_after_no_sasquatch_gap",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "remove the before sasquatch gap (K2)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R3_before_frozen_and_both_present",
    "R6_before_names_missing_sasquatch",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "rename a matched published path (K4)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R16_each_oracle_row_matched_by_exactly_one_file",
    "R4_after_publishes_every_oracle_row",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "forge oracle copy, not re-hashed (K1)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R9_evidence_id_authentic_650",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "forge oracle copy, re-hashed with 6.5.0 (K1)",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "delete the PROVINCE Core row",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S1_province_core_row",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "break S107 used-by",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note",
    "S7_source_rows_opened_today_with_entry_in_used_by"
   ],
   "detail": {}
  },
  {
   "case": "append an oracle row after freeze",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "O1_oracle_reproduced_unsquashfs",
    "R2_oracle_frozen_nonempty",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "change a carrier sha256",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "R1_carriers_frozen_unchanged_and_ids",
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "break the README coverage stem",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note",
    "S5_readme_coverage_map_row",
    "X1_stated_counts_equal_observed"
   ],
   "detail": {}
  },
  {
   "case": "add the entry path to the PROVINCE Frontier note",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "make the PROVINCE Frontier bullet carry the note",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2b_province_dated_sasquatch_note_cites_entry",
    "S3_readme_firmware_sasquatch_line_carries_dated_note"
   ],
   "detail": {}
  },
  {
   "case": "add a dated note after the README Firmware row",
   "pass": true,
   "unexpected": [],
   "false_conditions": [
    "S2a_province_bullet_carries_dated_note_citing_entry",
    "S2b_province_dated_sasquatch_note_cites_entry",
    "X1_stated_counts_equal_observed"
   ],
   "detail": {}
  }
 ]
}
```
