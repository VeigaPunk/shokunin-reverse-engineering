# R38W2Simplifier — minimality review of the attempt-2 landing

**VERDICT: DEFECTS FOUND** — the landed text carries one duplicated gate (a second implementation of
QUALITY 55's post-freeze drift check, built because the round's own instrument map is not in the
container that gate accepts), one duplicated registry authority (S112 restates S108), ~18 restatements
that survive only as padding, and four pieces of text whose cited artefacts do not say what the text
says (`c2-final.json` absent; the C1 control receipt is the v3 re-score, not "at the freeze";
`PROVINCE.md:372` and `corpus/README.md:238` still call standard BE v4 unmeasured; `HOST-CONTRACT.md`
does not exist).

Everything below is read from git objects, never the working tree (the tree currently carries other
seats' uncommitted edits and untracked receipts — `git status --porcelain` = 13 entries at start and at
end of this seat, of which my only write is this report). No lane file was edited; no VCS mutation.

Range reviewed: `git -C <lane> diff 077e212b81015f985febc12261ecac4fec71683a
0fc6113376a156fddc3ec385386d71c3a4a9f690 -- PROVINCE.md corpus/README.md corpus/SOURCES.md
corpus/QUALITY.md corpus/knowledge SCORECARD.md LOG.md corpus/lessons tools/round-38/freeze-drift.py`
(304 insertions, 4 deletions across 10 files).

Deletion-candidate proofs: **no `lsp` device is mounted in this seat**, so the semantic-caller step
(`references`) is unavailable; recorded here as the literal fallback the role permits. Caller sets were
taken with `grep -rn` over the lane for `freeze-drift` and `S112`.

---

## 1. Removable content (one line each; nothing edited)

| # | file:line (at `0fc61133`) | removable text | one-line reason | convention-backed? |
|---|---|---|---|---|
| R1 | `tools/round-38/freeze-drift.py:2-11` | the ten-line M38-1 narrative in the docstring | the mistake story is already QUALITY 79's row plus lesson M38-1; the tool's contract is argv + exit codes | no — 3 of 5 surfaces state it |
| R2 | `tools/round-38/freeze-drift.py` (whole file, 80 lines) | the tool | `tools/round-31/freeze-integrity.py` (the gate QUALITY 55 names) already prints `commits_after_freeze=N` per pinned input and exits 1 on any commit after the freeze — the identical mechanic, with a 25-case selftest this file lacks | no; see §2A for the reason it was written |
| R3 | `PROVINCE.md:157` | "big-endian/AVM stays here." (the clause) | the next sentence in the same bracket says the same thing about BE and adds the date; one statement of "still Frontier" is enough | no |
| R4 | `PROVINCE.md:157` | "K2's in-tree symlink leaves an `unpublished-entry` gap" | mechanism, not state: `corpus/README.md:91`, `:239` and the entry's §Symlinks carry it; PROVINCE needs "not promoted — honest stop" only | no |
| R5 | `PROVINCE.md:372` | "(`sasquatch-v4be` is its big-endian sibling, unmeasured)" | now false — the same round measures it (entry + `:157`) — so PROVINCE holds two authorities on one fact and they disagree; update or delete the aside | no (stale, not historical) |
| R6 | `corpus/README.md:238` | trailing "Still frontier: big-endian/AVM (`sasquatch-v4be`) and vendor-mangled images." | duplicates `:239`'s enumeration three lines below, and its BE half is refuted by `:239`; keep the dated LE-history clause | partly — the LE clause is history, the enumeration is not |
| R7 | `corpus/README.md:92` | "its meta description's "more than 30" conflicts with the README's "78+";" | the count dispute is the entry's §"The count conflict" and S116's scope cell; a coverage-map row needs the claim, not the quarrel | no |
| R8 | `corpus/SOURCES.md:118` (S112) | the whole row | same URL **and** same sha256 (`2d7b901b…9287`) as S108, whose scope already names `sasquatch-v4be`, the LE/BE argv and `get_dependencies` (S108 anchor: "lines 24-26 … 58-62 … 68-69"); one document, two rows | partly — census class W04 admits per-scope rows; see §2B |
| R9 | `corpus/SOURCES.md:122` (S116 anchor) | "(staged as package S122, renumbered by document)" | the renumber is recorded three more times (entry source line, entry body `:10-11`, lesson `:34`); the lesson's old→new line is the one to keep | no |
| R10 | `corpus/QUALITY.md:87` | relation cell "executes 55" | the only row in the file with that verb; row 55's gate is `tools/round-31/freeze-integrity.py` while row 79 names a different tool — the cell asserts inheritance without saying which gate is canonical (row 80 uses "sharpens") | no |
| R11 | `SCORECARD.md:3401` | "The v2/v3 counters are not the rule; their score is reported for information only." | restated inside the same section at `:3405` ("the v3 counter, which is not the rule, gives 4/4…"); one disclaimer | no |
| R12 | `SCORECARD.md:3408` | "one measured-not-promoted entry and one assimilated entry, both mapped" | `:23` already says "two entries added and mapped"; the Owned-scores line only needs the numbers | "Owned scores:" is per-section convention; the parenthetical is not |
| R13 | `SCORECARD.md:3411` | "retired: none. Saturation line and stagnation window unchanged; last capability entry round 36." | byte-identical to `:3398` (round-37 section): a standing fact re-issued per section | per-section convention (2 occurrences) → optional |
| R14 | `SCORECARD.md:3405` | "exit 1 at the freeze" (the attribution, not the cell) | the cited receipt is the v3 re-score (`--rev f1010f67 --freeze f1010f67`), so nothing in the landed tree holds a first-freeze C1 control receipt — see F1 | no |
| R15 | `LOG.md:3132` | "staged S122 → S116, staged S106 → S110 by document" | duplicated by lesson `:34` (registry cell changes) and by S116's anchor; LOG needs admission/refusal counts only | no |
| R16 | `corpus/lessons/round-38.md:5-7` | attempt-1 seat id, launch/death instants, "re-verifies the inherited bytes and lands this round" | `LOG.md:3128` already carries the death narrative; `:7` adds no fact, and the verdicts two lines below state the outcome | no |
| R17 | `corpus/lessons/round-38.md:28` | the S112 row of the Gate table | repeats S108's URL, tag and digest inside the same file that already records S108 at `:61`; goes with R8 | no |
| R18 | `corpus/lessons/round-38.md:74-81` | the five per-row quarantine bullets | campaign register bookkeeping the lane did not act on (`:81` itself says none is appended); the register and the wave-1 hand-check are the citation | section is convention (round-36 lesson has it) → keep the heading, cut the rows to a pointer |
| R19 | `corpus/lessons/round-38.md:80` | "`HOST-CONTRACT.md` line 41" | that file exists at no revision of this repo, in no commit, and nowhere in the read-only package — see F5 | no |
| R20 | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:43-46` | the "**Status.** This is not a Core promotion." framing | the title already says "(measured, not promoted)" and `corpus/README.md:91` repeats it; only the `carriers_matched 3` reason sentence is new information | no |
| R21 | `…r38-sasquatch-be-squashfs-recursion.md:22` | "that refusal is recorded as a rejected row (S115), not as a source." | S115's status cell says exactly this; the entry needs no pointer to its own rejection | no |
| R22 | `corpus/knowledge/2026-10-26-unblob-format-matrix.md:1` | "(staged as package S122, renumbered by document)" | the body (`:9-11`) states the same renumber with both ids and both targets | no |
| R23 | `corpus/knowledge/2026-10-26-unblob-format-matrix.md:6` | the title's "97 handlers … 'more than 30'" | both numbers are stated with their provenance in `:24-27`; a title that repeats the body's two counts is not a label | house style elsewhere does put the claim in the title → optional |

Not reported as removable (checked, kept): every `M38-1..M38-4` row's evidence cell (each carries a
distinct artifact), QUALITY 79's and 80's rule sentences, the `squashfs_v4_be` table in the entry, the
`## Round 38` table's before/after columns, LOG `:3134` ("No tools installed…"), the SOURCES S115
rejected row (required by R37-CL3), the S110 old→new cell change (required by QUALITY 74), and the
`corpus/README.md:89` round-36 row's "big-endian/AVM … not measured" clause, which is dated to round 36
and is historical provenance.

---

## 2. Structural deletion candidates

### 2A. `tools/round-38/freeze-drift.py` duplicates the accepted freeze gate — and the reason is a container defect

- QUALITY 55 assigns the rule to a gate: "…checked at the measured revision against the digest in the
  claims file at the freeze commit **and for any commit touching it after the freeze** … Gate:
  `tools/round-31/freeze-integrity.py`."
- That gate already does this half. `tools/round-34/freeze-integrity.py` (strict-schema successor of
  round-31/32/33) prints `ok\t<path>\tsha=…\tcommits_after_freeze=<N>` per pin and exits 1 on history
  (`"freeze-integrity: FAIL pins=1 changed=1"`), with a 25-case selftest including "restore commit must
  still fail".
- It cannot run on round 38, and this is the actual defect the new tool papers over:
  - `python3 -I -B tools/round-34/freeze-integrity.py --root <lane> --round 38` → **exit 2**,
    `freeze-integrity: ERROR no commit adds .ufo/waves/round-38/claims.json at HEAD`;
  - the round's freeze does ship a map, `.ufo/waves/round-38/instruments.json`, but its values are
    **paths, not digests**, so the accepted gate rejects it:
    `--claims .ufo/waves/round-38/instruments.json --rev 0fc61133` → **exit 3**,
    `ERROR schema code=pin_digest_format claims=… where=instruments:c1_carriers`;
  - the same frozen file carries an unsubstituted `"frozen_at_commit": "{{FREEZE}}"` (identical at
    `e059ca93` and at `0fc61133`; `git diff e059ca93 0fc61133 -- .ufo/waves/round-38/instruments.json`
    is empty) — i.e. the map never names its own freeze commit. *This file is outside the reviewed
    diff; it is reported because it is the cause of R2.*
- Consequence, stated as the deletion candidate: pin the kill-rule paths as digests in the container
  QUALITY 66/68 accept, and run the round-31/34 gate. That removes R2 entirely, closes the
  `{{FREEZE}}` placeholder, and restores the green+red selftest that QUALITY 61 requires of a new gate
  and freeze-drift.py does not have (`grep -c selftest tools/round-38/freeze-drift.py` → 0).
- Peer calibration: `R38W2ConnSiblingGates` (fleet-wide) judged the tool "extends" and found no
  sibling duplicate; that scan did not include the in-lane round-31..34 family's `commits_after_freeze`
  output. The two findings agree on the fleet axis and differ on the in-lane axis.
- Tradeoff: freeze-drift.py adds `--json-out` and takes an arbitrary path set (repo-relative or
  pathspec), which the family gate does not; that convenience is why the receptionist-sized fix lost
  to a new instrument. If the map is repinned, keep only that.

### 2B. SOURCES S112 restates S108

`S108` (round 36): URL `…/26.6.4/python/unblob/handlers/filesystem/squashfs.py`, sha256 `2d7b901b…9287`,
scope "How unblob 26.6.4 names and invokes its SquashFS extractors (sasquatch, **sasquatch-v4be**), the
LE/BE argv and the AVM test only", anchor "lines 24-26 … 48-50 … 58-62 … 68-69 get_dependencies".
`S112` (round 38): same URL, same digest, scope "v4 BE extractor dependency and argv", anchor
"`SquashFSExtractor` lines 24-70: … executable = self.V4BE_EXECUTABLE … get_dependencies() returns
sasquatch + sasquatch-v4be". Nothing in S112 is outside S108.

Caller set for S112 (grep over the lane): entry source line + README knowledge row + lesson Gate row +
the lesson's registry-change line. Of these only the lesson row is an argument *for* the row (it
records the Gate decision).

Tradeoff for removing it: the first-freeze predicate required the C1 entry to cite "a `SOURCES.md` row
**opened 2026-10-26**", and the counter's selftest has a red case "source opened earlier"; S112 exists to
satisfy that clause. The claim stopped, so the clause binds nothing now — but a future BE-v4 claim
would need the row or a re-dated S108. Recommend: drop S112, cite S108, and if a later claim needs a
same-round row, record that as a *re-opened* date on S108 rather than a second row for one document.

---

## 3. Falsifications (text that its own cited artefact does not support)

**F1 — the C1 control receipt is the v3 re-score, not "at the freeze".**
`SCORECARD.md:3405` "before" cell: "`carriers_matched 0`, exit 1 **at the freeze**
(`.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json`)". At `0fc61133` that file's argv reads
`--rev f1010f677a53ecf0e671952ce1bf4f44d51e151b --freeze f1010f677a53ecf0e671952ce1bf4f44d51e151b`
and its `output.revision` is `f1010f67…`. The receipt that actually ran at the freeze is the
`efd5c47a` version of the same path (`--rev e059ca93 --freeze e059ca93`), which the landing
overwrote twice: `git log --oneline e059ca93..0fc61133 -- .ufo/waves/round-38/controls/` →
`077e212b` (c1-0 under v3), `3b0da5dd` (all three c1 controls under v2), `efd5c47a` (seven controls).
So `SCORECARD.md:3401`, `LOG.md:3128`-adjacent, and `lessons/round-38.md:5` ("receipts `efd5c47a…`
(7 controls…)") all point at a receipt set the landed tree no longer holds for C1. The C2 controls
still carry the `efd5c47a` bytes (checked: c2-0 `--rev 77091b49`, mismatches 1, unresolved
`[prov_core:REA MCP server, evidence/doctor/]` — consistent with `SCORECARD.md:3406`).
*Not a verdict change:* all seven still exit 1; the text's attribution is what fails.

**F2 — `c2-final.json` is cited as committed and exists at no revision.** Three citations:
`SCORECARD.md:3406` ("exit 0 (`.ufo/waves/round-38/l1/scores/c2-final.json`, revision in its `revision`
field)"), `corpus/lessons/round-38.md:11`, `LOG.md:3130` (directory form), plus the lesson's R37-CL1
bullet `:85-86` ("every receipt this round cites is committed: … `.ufo/waves/round-38/l1/scores/` …").
`git cat-file -e 0fc61133:.ufo/waves/round-38/l1/scores/c2-final.json` → absent; the directory holds
only `c1-v1-at-3b960fe5.json` and `c1-v3-at-3b960fe5-NOT-THE-RULE.json`. Independent re-run (this
seat) at the same revision: **exit 0, `mismatches 0`, `guards_ok true`, `knowledge_files 126`,
`mapped 126`** — the C2 verdict stands, the citation does not; R37-CL1's sentence is false as written.
Already established independently by `R38W2C2Rederive` and `R38W2C2Rescore`; recorded here because the
same absent path is the one deletion R14 depends on.

**F3 — two statements still call standard BE v4 unmeasured.** `PROVINCE.md:372` ("`sasquatch-v4be` is
its big-endian sibling, unmeasured") and `corpus/README.md:238` ("Still frontier: big-endian/AVM
(`sasquatch-v4be`) …"). Both are contradicted by the round's own landed entry and by
`PROVINCE.md:157`/`README.md:239`. The first-freeze predicate named `PROVINCE.md:372` as a surface C1
would move; the stop left it untouched, so the lane now has two PROVINCE statements about one fact in
opposite states. C2's frozen counter does not catch this: it checks pointer resolution and the four
stated counts, not the truth of prose (`mismatches 0` while `:372` is false).

**F4 — the frozen instrument map is not a pin map** (see §2A): paths instead of digests, rejected by
the accepted gate (exit 3), plus `{{FREEZE}}` never substituted. Outside the reviewed diff, inside the
reviewed round's freeze.

**F5 — `HOST-CONTRACT.md` does not exist.** `corpus/lessons/round-38.md:80` cites "`HOST-CONTRACT.md`
line 41". `git log --all -- HOST-CONTRACT.md` → empty; `find` over the lane, its history, the fleet
root at depth 3, and all of `/home/vgpnk/Projects/shokuknow` → nothing. Dangling citation in a lesson
the round cites for its quarantine slice.

---

## 4. Preserved contract (do not delete these while removing the above)

- R38-C1's honest stop as an **outcome**: `carriers_matched 3`, `met_target false`, K2's in-tree
  symlink as the single `unpublished-entry` gap, no Core row. Stated once as state (PROVINCE Frontier),
  once as score (SCORECARD `## Round 38`), once as evidence (the entry's table) — the restatements listed
  in §1 are padding, the three are not.
- Every receipt the landing actually holds: `c1-v1-at-3b960fe5.json` (re-derived by this seat's run of
  the frozen tool chain: `freeze-drift` at `3b960fe5` → exit 1, drift `f1010f67` + `79f69347`, matching
  M38-1), `c1-v3-…-NOT-THE-RULE.json`, both do-nothing controls, the three `freeze-drift-*.json`, the
  `corpus/evidence/round-38/c1/K*/{before,after}.json` set (8 files: four carriers × both arms, all present).
- The 126/126 coverage figure: verified, not assumed — `c2-counter.py` at `0fc61133` reports
  `knowledge_files 126, mapped 126`; the directory holds 126 `.md` files.
- QUALITY 79's and 80's **rules** (first freeze is the rule; controls land inside the freeze). The
  criterion text is the round's durable product; only the gate pointer (R2/R10) is in question.
- The dated historical lines: `PROVINCE.md:157`'s LE-supersession clause, `README.md:238`'s LE-history
  clause, `README.md:89`'s round-36 limitation clause. Explicitly historical → not removable.
- S115's rejected row (R37-CL3), the S110 old→new cell change (QUALITY 74), the `## Round 38` table's
  before/after columns, and the `## Gate`/`## Routed defects` headings (round-36 precedent).

---

## 5. Checks run (read-only; nothing in §1 was applied)

| check | command | result |
|---|---|---|
| diff under review | `git diff --stat 077e212b 0fc61133 -- <10 paths>` | 304 insertions, 4 deletions, 10 files |
| C1 measured revision, drift | `python3 -I -B tools/round-38/freeze-drift.py --root <lane> --freeze e059ca93… --rev 3b960fe5… --json-out <scratch>` | **exit 1**, drift = `f1010f67` (`tools/round-38/c1-counter.py`), `79f69347` (claims + counter) |
| cited C1 score receipt | `git show 0fc61133:.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` | `carriers_matched 3`, `met_target false`, `province_core_row false`, `province_core_section false` |
| cited control receipts | all seven under `.ufo/waves/round-38/controls/` | all `exit 1`; c1-0 carries `--freeze f1010f67` (F1); c2-0 carries base rev, `mismatches 1` |
| C2 re-derivation | `python3 -I -B tools/round-38/c2-counter.py --root <lane> --rev 0fc61133… --base 77091b49… --json-out <scratch>` | **exit 0**, `mismatches 0`, `guards_ok true`, `knowledge_files 126/mapped 126`, `base_pointers 48`, `unresolved [['prov_core:REA MCP server','evidence/doctor']]` repaired |
| accepted gate on this round | `python3 -I -B tools/round-34/freeze-integrity.py --root <lane> --round 38` | **exit 2** `no commit adds .ufo/waves/round-38/claims.json` |
| accepted gate on the round's map | same, `--claims .ufo/waves/round-38/instruments.json --rev 0fc61133…` | **exit 3** `schema code=pin_digest_format … instruments:c1_carriers` |
| instrument map frozen? | `git diff e059ca93 0fc61133 -- .ufo/waves/round-38/instruments.json` | empty (`{{FREEZE}}` present at both) |
| control rewrites after the freeze | `git log --oneline e059ca93..0fc61133 -- .ufo/waves/round-38/controls/` | `077e212b`, `3b0da5dd`, `efd5c47a` |
| artefacts cited by the diff | `git cat-file -e REV:<path>` over 26 cited paths | 24 present; absent: `l1/scores/c2-final.json` (F2) — the second "miss" was my own wrong path guess for `w1/artifacts/R38CrossToolK4/7z-refusal.txt`, which **is** present |
| `HOST-CONTRACT.md` | `git log --all -- HOST-CONTRACT.md`; `find` over lane, fleet root, `shokuknow` | absent everywhere (F5) |
| caller sets | `grep -rn "freeze-drift"`; `grep -rln "S112"` over the lane | freeze-drift: QUALITY 87-88, lesson 17/18/98, README 229, LOG 3133, SCORECARD 3401/3410, tool itself, wave-2 artifacts; S112: 2 entries, lesson, README, SOURCES |

No install or upgrade was needed for this seat (`python3`, `git` only). Scratch
`/fast/scratch/hyaku/kaidoku-r38/R38W2Simplifier` removed before this report was written.

## 6. Limits

- Prose truth was checked only where the text names a commit, a file, a count or a receipt. I did not
  re-open S112–S116 upstream; S113's LFS oid, S114's Freetz line and S116's HTTP body are taken as
  cited (their re-check is another seat's lane).
- The quarantine slice's five campaign rows were checked for *existence of the cited lane file* only;
  `HOST-CONTRACT.md` is the one that fails.
- "Removable" in §1 means removable without weakening a claim the round scores; the ranking in §2 is
  where the real weight is. `[INFERENCE]` marks: that the round-31/34 gate would have reported M38-1
  had the map been digest-valued (from its docstring and selftest strings, not from a run — it cannot
  run on this freeze at all).
