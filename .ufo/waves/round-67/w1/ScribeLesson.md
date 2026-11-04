# ScribeLesson — round 67, wave w1 (scribe)

Seat: `ScribeLesson` (scribe; leaf member, no dispatch). Drafted the round lesson prose and the two
QUALITY row drafts at `.ufo/waves/round-67/w1/ScribeLesson/lesson.md`, plus the Gate fetch receipt
`.ufo/waves/round-67/w1/ScribeLesson/gate-fetch.json`. The L1 lands; nothing was landed, and **no
claim verdict is asserted here** — both after-arms belong to the L1's data run and the closure to
the non-author judge.

## Behavior

Read the claim declaration (`plans/round-67-claims.md`), the claims container
(`.ufo/waves/round-67/claims.json`), the five `l1/pre/` receipts, the round-66 lesson and the
round-66 verifier spot-check; then measured what the Gate needed rather than repeating the plan:
one new-source fetch, four row re-opens, the two gap-rule files, the engine's `disposition_check`,
the battery's case names, the mutant artifacts, and the assimilation directories.

## Gate (drafted lesson §Gate)

- **Admit — S268** (drafted id; registry tops at S267, S268 free): Linux kernel SquashFS docs
  §3.2 Inodes. Accessed **2026-11-03**: `https://docs.kernel.org/filesystems/squashfs.html`,
  HTTP 200, 26,045 bytes, sha256 `10767bbf8b5c49e81d7aafadd84b6e06602c19641d7f7ae9b0a0258d81733685`,
  `Last-Modified: Sun, 01 Nov 2026 22:46:23 GMT`, heading `3.2 Inodes` (`<section id="inodes">`
  raw line 401). Located quote, raw lines 412-414, 22 words: "there are different inodes for each
  file type (regular file, directory, device, etc.), the inode contents and length varying with the
  type". Scope: the on-disk inode class per file type — **not** the extraction privilege (S250) and
  **not** a carrier fact (the envelopes).
- **Reject (b)** the same page's §1 inode-size sentence (raw 264-266) as a second row: duplicate
  locator and scope; flip = the row's subject becomes the inode *size* claim.
- **Reject (c)** `Documentation/filesystems/squashfs.rst` on `torvalds/linux.git` plain: HTTP 200,
  14,201 bytes, sha256 `e709573a…3ba5f9`, same three sentences at :184-186, but the locator names no
  revision (default branch) — same text and scope under a weaker pin. Flip = adopt at a tagged tree.
- **Reject (d)** `l1/pre/control-dryrun.json` `per_carrier.g7581.gaps_note_round50` as the ground
  that no extractor record can exist: a receipt demonstrates a red arm, never a rule's ground.
  Flip = never.
- **Re-opened S243 / S244 / S245 / S249** (2026-11-03) and all four pins match: S243 1,153 B
  `e28b3341…84c707`; S244 root listing HTTP 200 and the 6490-cable row
  `FRITZ.Box_6490_Cable-07.57.image 04-Sep-2023 17:07 39741440`; S245 19,842 B
  `2d7b901b…599287`; S249 67,591 B `6c601b34…070a7`. **No new row needed for any**: each scope is
  exactly the subject the re-freeze re-uses, and none states the on-disk device inode class.
- Assimilation: none, measured — `ls merge/kaidoku/` and `ls considerthese` both exit 2.

## Mistakes (drafted lesson §Mistakes)

| id | class | captured-by | fix |
|---|---|---|---|
| M67-1 | scope / over-generalisation from one carrier family (round 50) — the over-wide `required.char-device` | `none` until #107 (M50-7 filed with none; #94 lacks the contrast) | class rule `gap-rule-v2.json` + `gaps_ok_round50 2` vs `gaps_ok_round67 4` in one receipt + 3 red fixtures |
| M67-2 | accounting / witness (this round's own, pre-freeze) — the class rule drops `removed.silent.char-device: ["247:0"]`, so c6430/c6490 read `1 silent` → `0 silent` | `none` (no criterion requires a dropped per-row admission to be re-expressed) | disclosed, not repaired; the predicate does not read the silent count |
| M67-3 | receipt / witness (round 66) — C1 receipts name no measured revision | the round-66 closure, routed | every r67 receipt carries `rev` (three pre receipts verified) |

## Findings for the L1

1. **The C1 padding is not yet present.** `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md`
   does not exist at this reading (`ls corpus/knowledge/ | grep -c 2026-11-03-r67` → 0), and claims
   atom **A8** requires it to cite the new SOURCES row. The entry, its `source:` line and the
   coverage-map row are still owed by the landing.
2. **The r66 routed defect 1's correction entry is not in LOG.md.** The round-66 closure routed "the
   record `02d4880b` cites a LOG entry that does not exist"; the r67 carry-in (`LOG.md:4083`) says it
   is "repaired this round as an appended correction entry". At this reading the only round-67
   heading is the carry-in (`grep -n '^## 2026-11-03 — round 67' LOG.md` → 4083 only). The repair is
   still owed.
3. **The class rule's silent-accounting delta (M67-2).** `gap-rule-v2.json` drops
   `removed.silent.char-device: ["247:0"]`, so the Cable carriers' one observed silent char-device
   removal stops being counted (`1 silent` → `0 silent` in `l1/pre/control-dryrun.json`). The
   `class_disposition` block accounts for the class by the re-derived oracle table and the
   `nonregular_unpublished` check, neither of which records a *missing* record. This is disclosed in
   the lesson, not repaired; no predicate clause reads the silent count, so no verdict moves.
4. **The control's scope guarantee rests on the second fixture.** `junk_rule_would_pass true` in the
   receipt means a waiver that also covered symlinks would pass the first red fixture; only
   `round67_rule_still_fails` (one removed symlink gap) keeps the waiver scoped. Worth stating as a
   limit in the report rather than as a defect — the receipt already discloses it.
5. **The r50 control note names 8 of the 13 char devices per FRITZ!Box carrier.** The note
   (`dev/pts/0`…`dev/pts/7`) reports the first failing subset; the class's extent is the carrier's
   oracle table, not the note. Recorded so no reader takes the note as the class census.
6. **The C1 counter was corrected after the freeze, and the dispatch's pin is superseded.**
   `tools/round-67/avm-le-counter.py` now hashes `55decb51…` (dispatch said `f78ed365…`; commit
   `1e7fe7b7` changed the patched gap-rule name to lane-relative because the engine reads its rule
   through `git show <rev>:<path>` and the absolute name made `measure()` exit 2). `6dcc447e` records
   the supersession in `claims.json` `instrument_supersessions` and the before record was re-taken
   with the same numbers (`gaps_ok_round50 2`, `gaps_ok_round67 4`, `control_ok true`,
   `rev a7a4ce69…`). The rule (`e66ba022…`), the battery (`cabc0a0b…`) and the engine (`9820811b…`)
   are unchanged. Anyone reading the dispatch's "frozen inputs" list must use the claims file.
7. **The data run is live in this wave.** The L1 has committed four
   `corpus/evidence/round-67/c1/<id>/run.json` (`a4c1d0fc`, whose parent chain descends from the
   freeze `3663e6b2`, verified with `git merge-base --is-ancestor` rc 0), and the four `after.json`
   are untracked in the working tree (mtime 21:54–21:56). `l1/scores/` holds only
   `c1-data-stage.json`; no C1 or C2 `--score` after-arm exists at this reading. This seat wrote and
   read none of the carrier evidence and asserts no verdict on it; the lesson now states that state
   instead of the (then true, now false) "no after.json exists".

## Touched surfaces

- Written: `.ufo/waves/round-67/w1/ScribeLesson/lesson.md` (14,789 B, prose draft),
  `.ufo/waves/round-67/w1/ScribeLesson/gate-fetch.json` (fetch + re-open receipt),
  `.ufo/waves/round-67/w1/ScribeLesson.md` (this report).
- Read-only: `plans/round-67-claims.md`, `.ufo/waves/round-67/claims.json`,
  `.ufo/waves/round-67/l1/pre/{control-dryrun.json,control-dryrun-c2.json,score-dryrun-at-base.json,selftest-c2.json,selftest-r50.txt}`,
  `corpus/lessons/round-66.md`, `corpus/lessons/round-66-verifier-spotcheck.md`,
  `corpus/lessons/round-50.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/knowledge/` (listing),
  `corpus/README.md`/`SCORECARD.md`/`LOG.md` (greps), `tools/round-50/{gap-rule.json,c1-counter.py}`,
  `tools/round-67/{gap-rule-v2.json,avm-le-counter.py}`, `tools/round-67/mutation-battery.py`,
  `.ufo/waves/round-66/w1/MutClosure/mutants.md`, `.ufo/waves/round-66/w1/MutCoverage/mutants/M2/`.
- Nothing was written under `tools/`, `corpus/`, `corpus/evidence/`, `PROVINCE.md`, `SCORECARD.md`,
  `LOG.md`, `SKILL.md`, the fleet repo, or any sibling lane. No git/jj write; no `agent://all`; no
  subagent. Scratch `/fast/scratch/hyaku/kaidoku-r67/ScribeLesson` deleted before yield. No tool
  install or upgrade.

## Out of scope / not run

- The two `--score` after-arms, the four carrier data runs (`tools/round-67/c1-run.sh`), the
  landing (lesson, knowledge entry, SOURCES row, census, SCORECARD rows), the freeze-ledger rows and
  the non-author closure are all the L1's or the judge's. The carrier evidence that appeared during
  this seat's drafting (`corpus/evidence/round-67/c1/<id>/run.json` committed at `a4c1d0fc`, four
  untracked `after.json`) was written by the L1's run; this seat neither wrote nor read it.
- No instrument was executed by this seat: the receipts reported here are the committed
  `l1/pre/` files, and the engine/battery pins were read, not re-run.
