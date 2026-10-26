# R38W2ScribeTrend — draft trend verdicts and SHONEN lines (round 38, attempt 2)

Drafted from committed bytes only. Read at HEAD `e265533e` (wave-2 dispatch; no scored surface
after `0fc61133`), base `77091b49`, first freeze `e059ca93`, controls `efd5c47a`. This is a draft
for the L1 to integrate: it rules on nothing, and it amends no contract, predicate, counter,
carrier or oracle.

Caveat recorded at 04:04: the working tree is **no longer HEAD** — three tracked corpus files (two
knowledge entries and the round-38 lesson) were modified at 04:01:25 by another actor while wave 2
ran. Every verdict below is for the HEAD bytes (`git show`/`git diff`), not for that pending tree.

Axes named: **coverage** — every trend and every SHONEN box below rests on a named committed byte,
and each box has a resolvable pointer or a stated reason it cannot; **calibration** — no author
claim is reused as verified, both new entries' own `recheck:` commands were re-run live, and every
inference carries `[INFERENCE]`.

## 1. Trend verdicts (LEARNING.md definitions)

| trend | verdict | one-line basis |
|---|---|---|
| **expansion** | **improved** (with a disclosed defect) | two new admitted `knowledge/` entries, both citing `mined` SOURCES rows and both mapped in the coverage map; one is on Frontier ground (standard BE v4), which the Core map did not hold. The matrix entry carries one false sentence; scored under quality, see the boundary note |
| **quality** | **harmed at committed HEAD** | the admitted matrix entry states that the staged "42 vendor-attributed entries" was a word count, "not a per-handler attribution count"; 42 of the 97 sections do carry a `Vendor:` field, so the staged claim was right. Unmarked at HEAD; repaired in an uncommitted working-tree edit at 04:01 (not this seat's), which is not a committed marking |
| **discernment** | **improved** (grounded-criterion branch) — the spot-check branch is **unproven** this round | M38-1→QUALITY 79 and M38-2→QUALITY 80, each with a check shown able to fail; but the lesson carries no non-author Gate spot-check, and two mistakes (`captured-by: none`) got no criterion |

### expansion: improved

- Net new admitted entries: `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`
  and `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (both `A` in
  `git diff --name-status 77091b49 HEAD -- corpus/knowledge`).
- Uncovered ground: the BE entry lands on the `PROVINCE.md` Frontier bullet that carried the
  "big-endian/AVM stays here" note (`PROVINCE.md:157`, round-38 note added), and the frozen C1
  score records `province_core_row false` — measured, not promoted. The matrix entry is a second
  source on producer-contract ground the round-36 Core row already holds, so it is depth, not new
  ground; the Frontier entry is what moves expansion.
- Each cites a coverage-map row: 126 knowledge files, 126 stems in `corpus/README.md`, 0 unmapped
  (recount below), both new stems present.
- Each `source:` row is `mined` in `corpus/SOURCES.md`: S112/S113/S114 (BE entry), S116 (matrix
  entry); S110 is the widened existing row.
- Bar check (fails-the-bar test): both entries' own `recheck:` commands were re-run and pass
  (S116 page digest `8f8c29af…bbc5`, 97 `<h2 id=`, 3× "more than 30"; S112 handler digest
  `2d7b901b…9287`, `V4BE_EXECUTABLE = "sasquatch-v4be"` ×1). The BE entry's carrier claims match
  the committed receipts (before: 4/4 `missing-extractor-dependency` [`sasquatch-v4be`], 0 files;
  after: K1 5/5, K2 3/3 + 1 `unpublished-entry` gap, K3 4/4, K4 4/4), and K3/K4 bytes equal the
  tag's LFS oids.
- Boundary: the failing sentence in the matrix entry concerns the assimilation correction, not the
  ground the entry was admitted on, so it is scored under quality and not under expansion's
  "fails the bar" clause. An integrator that reads any false sentence as a bar failure should also
  mark expansion harmed; both readings are recorded, this file takes the narrower one.

### quality: harmed at committed HEAD

- `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (HEAD) says the staged "42
  vendor-attributed entries" "was a count of the word `Vendor` (42 occurrences), not a per-handler
  attribution count". Measured on the page at the entry's own digest `8f8c29af…bbc5`: 97 sections,
  **42 of them carry a `Vendor:` field**, one value the literal `unknown`; total `Vendor`
  occurrences also 42. The staged claim was substantively right; the entry's "correction" is wrong.
- At HEAD this false sentence is unmarked, which is exactly the harm clause. A working-tree edit at
  04:01 (not this seat's) repairs the sentence and adds "M38-5" inline in `## Gate`, but it is
  uncommitted at HEAD `e265533e` and M38-5 has no `## Mistakes` row, so it does not yet mark the
  entry in committed bytes. Verdict flips to **unchanged** once the repair is committed with an
  M38-5 row (and, per LEARNING, a criterion for it).
- The BE entry's big-endian sentences and the round-36/dependency entries' scoping still hold; no
  other existing entry was superseded or re-verified this round.

### discernment: improved (grounded-criterion branch only)

- M38-1 → QUALITY 79 and M38-2 → QUALITY 80, each citing `corpus/lessons/round-38.md`, each with
  a check shown able to fail: `freeze-drift-077e212b.json` verdict `drift` (`79f69347`,
  `f1010f67`) vs `freeze-drift-cb4326b2.json` verdict `clean`; `freeze-drift-gen-controls.json`
  verdict `drift` (`efd5c47a`). All three receipts are committed.
- Unproven this round: LEARNING's per-round outside spot-check (a non-author samples ≥1 admit and
  ≥1 reject and records agree/disagree in the round lesson). `corpus/lessons/round-38.md` has no
  such row; a lane-dispatched seat is still the lane, so wave 1 (40 seats) and the L1 cannot fill
  it.
- Gap: M38-3 and M38-4 carry `captured-by: none`, and no QUALITY criterion was added for them,
  although LEARNING §3 says a mistake no criterion caught becomes one. The nearest existing rows
  (55, 61) are not cited by the lesson.
- Gap in the pending repair: the uncommitted edit names "M38-5" only inline in `## Gate`; the
  working tree's `## Mistakes` table still has four rows, and no criterion was added for it.
- One disagreement was learned, not dropped: S115's reason records that 7-Zip's own format page
  lists SquashFS under unpacking, so "7-Zip cannot read SquashFS" would overstate.

Flip conditions: expansion → an admitted entry fails its own recheck, or the map count falls;
quality → the matrix-entry repair is committed with an M38-5 row (flips harm to unchanged), or an
entry is found stale/false and left unmarked; discernment → a named non-author records the Gate
sample (gains the agree/disagree branch), or a criterion lands without a lesson / a disagreement is
dropped (harmed).

## 2. SHONEN lines (one per box; `SHONEN.md` itself was not touched in round 38)

`git diff --name-only 77091b49 HEAD -- SHONEN.md` → empty, so the file text stays as it is; these
are the lines to paste if the L1 refreshes pointers. `[x]` is unavailable for all four — no named
non-author verifier exists for any box. `[ ]` fits none — each box has a resolvable pointer.

- `[~]` SKILL.md decision tables — unchanged this round (no SKILL.md diff); cited `SKILL.md:81-314`
  resolves (81 = `## Queue-drain craft` heading, 314 = a line end) at `3e99fbd`/HEAD. The
  "17/17 rule blocks have resolvable citations" figure is the lane counter's measure and is not
  re-derived here; the box already says "not a full semantic audit".
- `[~]` End-to-end task executed and logged — pointer refreshed: `LOG.md:3126-3134` (round-38
  entry) + `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` (8 committed receipts) +
  `.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json`. The task ran end to end (REA 6.5.0 /
  unblob 26.6.4 on four BE carriers) and the claim honestly stopped at 3/4; the box asks
  "executed and logged", not "succeeded". Verification is lane-internal.
- `[~]` Executable without oral context — historical pointer `corpus/lessons/2026-10-15-round-1.md`
  resolves; round 38 adds a counter-example to the box's assertion: the frozen after-harness failed
  as frozen (M38-4, `harness-after-mode-failure.txt`), was fixed at `cb4326b2`, and only the
  post-fix run produced a receipt. This box cannot rise above `[~]` on this round's bytes.
- `[~]` PROVINCE accuracy — cited `PROVINCE.md:97-125` resolves; this round's PROVINCE edits land
  at lines 44 and 157 (`git diff -U0`), outside the range; the repaired Core-row pointer
  `.ufo/waves/round-19/evidence/doctor/` resolves (`doctor-6.5.0.txt`, `doctor-6.7.0.txt`); the
  matrix entry sits on the same producer ground as the round-36 Core row, so no absorption. The
  counter that certifies this is C2, whose receipt is **uncommitted** (see the report's F1), so
  even the lane-internal certificate is not cold-clone checkable.

## 3. Recounts this seat ran (read-only; every number above)

```
git diff --name-status 77091b49 HEAD -- corpus/knowledge      -> two A rows (BE entry, matrix entry)
git diff --name-only   77091b49 HEAD -- SKILL.md SHONEN.md    -> empty (both untouched)
python: corpus/knowledge/*.md = 126; stems in corpus/README.md = 136; mapped = 126; unmapped = []
sha256sum corpus/evidence/round-37/c1/K3/carrier.bin -> 9c7c523c…97c0  (= squashfs_v4.bin LFS oid, size 4096)
sha256sum corpus/evidence/round-37/c1/K4/carrier.bin -> a29ddc15…56ed  (= squashfs_v4.nopad.bin LFS oid, size 307)
curl unblob.org/formats/ | sha256sum -> 8f8c29af…bbc5 ; grep -o '<h2 id=' | wc -l -> 97 ;
  grep -c 'more than 30 different' -> 3 ; grep -o 'SquashFS ([^)]*)' -> 10 sections incl. v4-BE, v4-broadcom ;
  python split on '<h2 id=' -> 97 sections, 42 with a 'Vendor:' field, 42 'Vendor' string occurrences,
  1 value 'unknown', per-section status 89 Fully / 8 Partially (90/8 string occurrences: one legend) ;
  'Does not support encrypted ZIP files' -> 1
curl .../26.6.4/python/.../squashfs.py | sha256sum -> 2d7b901b…9287 ;
  grep -c 'V4BE_EXECUTABLE = "sasquatch-v4be"' -> 1
curl .../26.6.4/README.md | sha256sum -> 6544d60f…3716 ; '78+' at lines 5 and 22
corpus/evidence/round-38/c1/K2/after.json normalized_result.extraction_gaps -> 1 kind unpublished-entry
git cat-file -t 0fc61133:.ufo/waves/round-38/l1/scores/c2-final.json -> fatal: does not exist
git status --porcelain -- .ufo/waves/round-38/l1/scores/ -> ?? …/c2-at-0fc61133.json
git status --porcelain (04:04) -> M corpus/knowledge/2026-10-26-unblob-format-matrix.md,
  M corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md, M corpus/lessons/round-38.md
  (all mtime 04:01:25, not this seat's writes; HEAD bytes are what these verdicts judge)
```
