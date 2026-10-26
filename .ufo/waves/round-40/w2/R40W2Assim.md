# R40W2Assim — assimilation Gate spot-check (round 40, wave 2)

**Verdict: DEFECTS FOUND.** The round-40 assimilation *substance* holds — one ADMIT (the
`avm-image-extraction` lead, folded into `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` via
own-work row S126) and the two REJECTS (they still carry falsified sentences) are each correct on bytes
I re-opened — but the Gate **cannot be assembled from the retained drafts as they stand**: the only Gate
draft maps its three new-row ids to three documents that now hold *different* rows (S123/S124/S125), the
entry cites S114 for a sentence S114's recorded scope does not carry, S126 is the registry's only
host-absolute cross-repo `source:` with no repo revision and no located anchor in the entry, and no run of
the id-collision guard is recorded after the freeze consumed S123.

What I attacked: (1) the admit's own-work row and every file it cites; (2) the two rejects' surviving
bytes and the landed entry's statement of the mechanism; (3) CORPUS.md rule 1 for a cross-repo own-work
row; (4) CORPUS rule 4 ("expansion is knowledge, not rows") and rule 2 (append-only) by cell-level diff;
(5) the id-collision guard's record and its ability to fail.

## Axes

| axis | what moves here |
|---|---|
| **coverage** | whether the round may count one admitted entry on AVM ground, and with which three registry rows as its provenance |
| **depth** | the discriminating sentence the corpus now owns: the *marker triggers the `-be` drop*, the *block-length byte order is the format* — and which row is allowed to anchor each half |
| **calibration** | whether each landed row can be spot-checked: a located quote, a resolvable base, an id that names one document, and a gate that can fail |

## Item verdicts

| # | item | verdict |
|---|---|---|
| 1 | admit: `avm-image-extraction` → `2026-10-26-r40-avm-be-squashfs-core.md` via S126 | **ADMISSIBLE**, two corrections (F1, F2) |
| 2 | rejects: `avm-firmware-image-unblob`, `avm-le-variant-reachability` | **CORRECT** — falsified sentences still present, not cited by any landed surface |
| 3 | is an own-work row into another repo admissible under CORPUS rule 1 | **admissible in kind, defective in form** (F1) |
| 4 | did the L1 append only rows the admitted entry cites (rule 4) | **PASS** — three rows added, all cited, two E3-drafted rows dropped |
| 5 | rule 2 (append-only) on the registry edit | **PASS** — only `used-by` changed in place, six rows |
| 6 | was the id-collision guard run | **NO RECORD after the freeze**; outcome clean by my own run (F3) |
| 7 | is the admit load-bearing in any scored binding | **No** — the C1 claim names no `claim_row` (F4) |
| 8 | the landed entry's "measured, not promoted" framing | **CONFIRMED** by carrier bytes; one wording overclaim (F5) |

## Findings

### F1 — S126 is the registry's only host-absolute cross-repo `source:`, and nothing validates it

`corpus/SOURCES.md:132` cites
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv (sha256 f205807d…)`,
kind `own-work`, tier `A`. Under CORPUS.md the `source` cell is "title — canonical URL or DOI (a repo path
or command for `own-work`)", and rule 1 only requires that the source be *opened* in the round that writes
the row and that the Gate record "the URL, the access date, and a ≤25-word quote with its location".
Nothing in rule 1 forbids another repository; `own-work` legitimately covers the lane's own round-11 work,
which is committed in shokuknow (`git ls-files --error-unmatch` succeeds; `git -C … rev-parse` →
`8b94c5c1…`, tip 2026-10-24). So the row is **admissible in kind**.

Its *form* is the defect, on two counts:

1. **No base and no containing-repo revision.** All ten other `own-work` rows in the registry cite
   lane-relative paths (`S039`, `S053`, `S055`, `S057`, `S060`, `S061`, `S063`, `S067`, `S072`, `S115` —
   `awk -F'|' … if(k=="own-work")`). S126 is the only `S###` row whose `source` is a host-absolute path in
   a different repo, and its anchor pins the *files* (image and log sha256) but not the repo state the
   path resolves in. The contract's `anchor` asks for "exact section / heading / page / line plus revision
   (version, commit, or publication date)" — S126 has the rows and the file digests, not the commit.
2. **Nothing catches a dangling source.** `scripts/sources-census.sh` checks path existence only for
   `used-by` (`E11`, line 567: `printf '%s\tE11\t%s missing used-by %s\n'`). A reorganised shokuknow would
   leave S126 dangling and the registry would still validate clean — measured: `validate --file
   corpus/SOURCES.md --today 2026-10-26` → exit 0 (only `W04` duplicate-URL warnings), artifact
   `census-validate.txt`.

Smallest safe correction (no in-place anchor edit — rule 2): the Gate records the base
`/home/vgpnk/Projects/shokuknow` and its commit `8b94c5c1…` beside the S126 quote; the next contract
version should take `<repo>:<repo-relative path>` for own-work rows outside the lane.

The row's own honesty holds: its `teaches` cell states "while the retained log carries no exit status and
an earlier attempt in the same directory failed to run its extractor". I verified the log has neither an
exit status nor a version banner (`unblob.log`, 2153 B, sha256 `352e0d79…`, ends at the 12:01 extraction's
`Processing file` lines).

### F2 — the entry cites S114 outside the row's recorded scope; the block-length sentence has no row

The entry's `source:` line 6 reads "S114 — … — line 8, block length little-endian; lines 13-14, the
marker". S114's recorded cells are: scope "AVM-BE **marker** semantics (mkfs_time == bytes_used) that
unblob's handler branches on; not the v4be binary", anchor "opening line …; `mkfs_time` field holds the
same value as `bytes_used`", teaches "Keep AVM-BE distinct from standard BE v4 when reading handler argv
decisions". Tier B is scoped to that marker claim; **the block-length bullet is not in it**, and two
wave-1 seats said so independently:

- `w1/R40SrcFreetz.md` §"Defect in the current S114 anchor": "it does not carry the block-length sentence.
  It does not need it for its current use-by (the r38 entry), but the R40 AVM claim needs it", and it
  proposed extending S114's anchor with lines 8-9 — which SOURCES rule 2 forbids in place.
- `w1/artifacts/R40AssimE3/gate.md`, heading "Why **S125 is a second row for a document the lane already
  holds as S114**": "it does not carry the block-length bullet, and CORPUS rule 2 forbids editing an
  anchor in place."

The landed state did neither: S114 was left byte-identical except `used-by` (cell diff below) and no row
anchors lines 8-9, yet the entry cites S114 for them. The claim's layout half is still supported by S124
(code, tier A, scope "which field is read little-endian", anchor `patch line 35 /* block length in AVM-BE
format is stored in LE order */`) and by the lane's own identity test — so this is a calibration defect,
not a false claim. Smallest safe correction: land E3's dropped format-doc row under a fresh id (S127) with
the lines 8-9 quote and used-by the entry — duplicate URL across scopes is a `W04` warning, and the
registry already carries that pattern (`S083`/`S090`/`S092`/`S123` on one tarball) — **or** drop the
"line 8" clause from the entry's S114 line. `corpus/SOURCES.md` is not a frozen C1 path, so either edit
is admissible at closure.

### F3 — the id-collision guard was not re-run after the freeze, and its retained output is now wrong

- The guard *was* run once, pre-freeze, by `R40AssimE3`: 122 registry ids vs 132 staged ids, 17 collisions
  (S106–S122), "next free lane id = S123"; independently `R40RevCensus` reports "next free id is **S123**"
  (`w1/R40RevCensus.md:3,69`).
- The freeze `7fce3086` then consumed S123 for the rea-agents `operation`/provider row
  (`w1/R40SrcReaOps.md`), and the landing `42c10a58` appended S124–S126 for three other documents.
- No run after the freeze is recorded. Searched: every file under `.ufo/waves/round-40/` for
  `collision|next free|S127|duplicate id` (only E3's and the census seat's pre-freeze artifacts, plus
  dummy rows in the census mirror fixtures), and the L1 transcript `history://KaidokuR40` (0 lines each
  for `collision`, `S124`, `S125`, `S126`, `used-by`; 1 for `sources-census`). Observation cutoff:
  2026-10-26, tip `0b15c8b2`.
- The counter cannot stand in for the guard: `tools/round-40/c1-extra.py:101` builds `sids()` as a
  `{id: line}` dict, so a duplicate id would silently keep the last row and `sourced_new` would still
  return true.
- **Outcome is clean — measured by me, not by a recorded run.** `scripts/sources-census.sh validate
  --file corpus/SOURCES.md --today 2026-10-26` → exit 0, no `E02`/`E03`/`E05`–`E11`; rows 122 → 126;
  tallies `mined` 117→121, tier `A` 114→118, `code` 36→38, `dataset` 14→15, `own-work` 10→11 — exactly
  the four new rows, no swap (QUALITY #74's tally half satisfied).
- **The retained guard output is now dangerous.** `w1/artifacts/R40AssimE3/collision/renumber-map.tsv`
  and `gate.md` map S123→the round-11 TSV, S124→`freetz-squashfs4-host-be.mk`, S125→`AVM-BE-format.txt`;
  the registry at the tip holds different rows in all three (`artifacts/gate-id-remap.md` in this seat's
  directory has the table). E3's table is the only Gate draft in the lane — pasted unchanged into
  `corpus/lessons/round-40.md` it would assert false provenance for three rows.

Smallest safe correction: the Gate uses the landed ids (remap file), and the Gate's "spot-check result"
line records the census run above with its exit code and the tally deltas.

### F4 — the admit is not load-bearing in any binding, so the Gate is the only record of it

`plans/round-40-claims.md` (blob `04a39b3d…` at both `7fce3086` and tip — verified with `git rev-parse`)
asks that the entry "cites a SOURCES row absent at the base whose used-by lists it" and names no
`claim_row`. `c1-counter.py:1150-1170` accepts *any* cited id with `opened == 2026-10-26` and the entry in
`used-by`; `c1-extra.py:106-115` returns the whole *set* of qualifying new ids. A landing that cited only
S124 would score identically — so nothing scores the assimilation decision itself. (The QUALITY #45
consequence is already routed by `w2/R40W2ConnRouted.md`; the assimilation-specific consequence is that
the closure Gate must state the admit explicitly, and a future round must name `claim_row` if it wants the
admit graded.)

### F5 — one wording overclaim; the Limits paragraph corrects it

The entry's Lineage sentence — "That observation was re-opened this round and is now reproduced on vendor
images with lane receipts" — reads as if the receipts witness the *no-`-be` argv*. They do not: `grep -o
"sasquatch[^\"]*"` over `corpus/evidence/round-40/c1/{L1,L2,V1}/after.json` returns **no match**, so the
receipts carry no extractor command, and the only `unblob -v` argv logs under `.ufo/waves/round-40/` are
for development members and marker controls (`R40C1ReconGaps/unblob-{7490,7430}-member-evidence.txt`,
`R40C1MarkerBoundary/logs/unblob/*.log`), not the four carriers. The entry's own **Limits** paragraph
says exactly this ("REA records no extractor argv on success, so 'no `-be`' rests on the handler source
and direct `unblob -v` logs, not on the receipt"), so the smallest correction is to qualify the Lineage
sentence or let the Gate cite the Limits as the corrective.

## What reproduces (positives, with the command)

- **The cited round-11 files are real and unchanged**: `sha256sum` gives TSV `f205807d…9eb0`, image
  `c7f74691…d32`, log `352e0d79…d5d7` at `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/` —
  equal to the row, the entry and E3's quotes (`artifacts/sha256-inputs.txt`).
- **The lineage image is an AVM-layout body**: `python3 -I -B tools/round-40/sqfs-list.py --layout auto
  --inspect --files … avm-be.squashfs` → `avm_marker: true`, `block_length_signal: "exact"`, compression
  `xz`, and the oracle side lists exactly the four `apple*.txt` files the TSV and the log name
  (`artifacts/inspect-r11-lineage.json`).
- **The committed L carriers carry the layout the entry claims**: same command on
  `corpus/evidence/round-40/c1/{L1,L2}/carrier.sqsh` → `avm_marker: true`, `block_length_signal:
  "exact"`, xz/gzip respectively; the entry's own identity test is not marker-only
  (`artifacts/inspect-{L1,L2}.json`).
- **The honest-stop sentence is exactly what the carrier holds**: `c1/L2/nonregular.tsv` has
  `bin/busy	symlink	/usr/bin/busy` and the published regular file is `usr/bin/busy` (oracle row 4), so
  "its path-suffix test reads the published regular file `usr/bin/busy` as the symlink `bin/busy`" is
  literally the collision the counter hits. L2's oracle has 6 rows; the entry's table says 6.
- **The "no failed chunk" binding is report-based, not exit-code-based** (`c1-counter.py:624`:
  `chunk_failed` reads `extraction_failed`), which is the shape `w1/R40AssimReject.md` §2 demanded, so the
  entry's "one `squashfs_v4_be`, not failed" does not rest on the exit code.

## Rejects — why they are right, and one conflict the Gate must settle

- `avm-firmware-image-unblob.md:16` and `:75-79` still say the handler "never notices the AVM marker at
  all" / "The AVM marker is **invisible to unblob**". The pinned handler does the opposite
  (`S112:44-50`), which the new entry states correctly. **REJECT is correct**; flip unchanged.
- `avm-le-variant-reachability.md` still opens "The second AVM variant is not reachable as an AVM image
  through the recipe the lane holds", overturned by the retained `avm-le-{genuine,plain550}.squashfs`
  byte identity (`18d3ad05…`). **REJECT is correct**; the entry covers no LE ground ("LE AVM members
  (`hsqs`) … not covered").
- `avm-le-image-genuine-marker.md` is where the two wave-1 seats **disagree on status**: `R40AssimE3`
  refuses it as off-surface (LE, while C1 is BE) with the flip "a round whose claim is the LE AVM
  variant"; `R40AssimReject` returns **ADMIT-AFTER-REWRITE** with three defects (`:30` generalises the LE
  observation, `:55-56` denies a mechanism that exists, no exit-code caveat). Both agree it must not land
  unchanged. The Gate must record *one* verdict plus the rewrite conditions, or a future round will read
  "ADMIT" and admit it as written.
- Neither rejected entry, nor `avm-image-build-blocker` / `sasquatch-unblob-avm-branch`, is cited by any
  landed surface: `grep -rn` over `corpus/ PROVINCE.md SKILL.md` hits only round-38/39 **lessons**.
- The rejection of the *mechanism* did not leak into the entry: the entry's first paragraph states the
  marker-triggers-`-be` branch and the block-length-as-format split.

## Registry discipline (rule 2 / rule 4), measured

Cell-level diff across the landing (`42c10a58^` → `42c10a58`, `artifacts/rowdiff.txt`):

```
base 123 land 126
added ['S124', 'S125', 'S126']   removed []
S112 S114 S118 S119 S120 S121 changed only column 11 (used-by)
```

So: append-only holds, no row was rewritten, and `S107`/`S108` — which E3 proposed extending — were
correctly **not** extended, because the landed entry does not cite them. Rule 4 ("expansion is knowledge,
not rows; no row quota") passes: each of the three new rows is on the entry's `source:` line and each is
used by a distinct claim (the reader patch, the carrier's vendor identity, the lineage), and two rows E3
had drafted were dropped rather than padded in. Each new row's `used-by` names an entry that cites it back
(S123 → the C2 entry, `:7` there; S124/S125/S126 → the C1 entry), which is the converse check the census
does not run.

## Gate material the closure can use (and must not copy from E3 verbatim)

- Candidates: the six AVM-ground entries in `merge/kaidoku/knowledge/corpus/knowledge/`
  (`avm-image-extraction`, `avm-firmware-image-unblob`, `avm-image-build-blocker`,
  `avm-le-image-genuine-marker`, `avm-le-variant-reachability`, `sasquatch-unblob-avm-branch`) — the same
  set E3 enumerated; I found no seventh AVM entry there.
- Admit: `avm-image-extraction` → the round-40 entry, via **S126** (not E3's "S123"), with F1's base+commit
  and F2's separate block-length row.
- Rejects: five, with E3's reasons plus the `avm-le-image-genuine-marker` status conflict above.
- Id remap and Gate-ready quotes: `artifacts/gate-id-remap.md` in this seat's directory.
- `corpus/lessons/round-40.md` is **absent at the tip** (`ls corpus/lessons/ | tail` ends at
  `round-39.md`), so CORPUS rule 1's Gate obligation for S123–S126 is still open and is the closure's to
  discharge; it must carry the ids as landed, or it will record provenance for rows that do not exist.

## Limits of this check

- **No vendor bytes fetched and no REA/unblob run made**, so V1/V2's layout and the four `after.json`
  receipts are taken from committed evidence and the C1 score, not re-derived. The AVM licence forbids
  redistribution; nothing vendor-derived was copied into the lane.
- The L1's own landing steps are inferred from commit order, the cell diff and the absence of any record;
  `history://KaidokuR40` may not retain the landing session — I report what it contains at the cutoff, not
  an absence proof.
- `[INFERENCE]` the two dropped E3 rows were dropped deliberately (they are the ones the landed entry
  does not cite); the commit message names only "S124-S126".
- I did not open the other five staged entries in full — only enough to confirm none is cited by a landed
  surface and that `avm-firmware-image-unblob`/`avm-le-variant-reachability` keep their falsified sentences.

## Adjacent observation — an uncommitted `SKILL.md` change at my cutoff

At 2026-10-26T19:33Z `git status --porcelain` in the lane shows ` M SKILL.md`, **not mine** (this seat
wrote only its report and artifacts). The diff is a single hunk, `@@ -1384,3 +1384,22 @@`, appending a
19-line "Round-40 instrument registry" section at EOF; the frozen C2 surface is untouched — the v2 table
marker is at `SKILL.md:361` and no hunk covers it, so "the v2 table bytes equal the freeze bytes" is
unaffected. Flagged for the closure only: an uncommitted edit to a tracked repo file must be committed
deliberately or reverted before the round lands, and the wave-2 bounds do not authorise writing `SKILL.md`.

## Bounds and ledger

- Written: this report, `artifacts/R40W2Assim/{rowdiff.txt,census-validate.txt,inspect-L1.json,
  inspect-L2.json,inspect-r11-lineage.json,sha256-inputs.txt,gate-id-remap.md}`. Nothing else in the lane;
  nothing in shokuknow (read-only: `git rev-parse`, `git log`, `git ls-files`, `sha256sum`, `sed`, `ls`).
- Read-only git only; no add/commit/checkout/reset/stash/pull/push, no jj, no fixture clone needed.
- No tool installed, upgraded or removed; no pacman transaction; `unblob`, `sasquatch`, `sasquatch-v4be`
  untouched; no REA device or CLI call.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2Assim` removed at exit; every cited output copied into
  the artifacts directory above.
