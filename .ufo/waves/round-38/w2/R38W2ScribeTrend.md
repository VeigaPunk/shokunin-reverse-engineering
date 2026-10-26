# R38W2ScribeTrend — trend verdicts and SHONEN lines for round 38

**DEFECTS FOUND** — in the self-assessment support a trend/SHONEN ruling would rest on, and in one
admitted entry: the round's calibration certificate (R38-C2) is uncommitted and both documents cite
a receipt path that exists nowhere; the lesson carries no non-author Gate spot-check; two mined
mistakes got no QUALITY criterion; and at committed HEAD the admitted `unblob-format-matrix` entry
states a false correction (measured: 42 of 97 sections do carry a `Vendor:` field, so the staged
claim it "corrected" was right). Draft deliverable:
`.ufo/waves/round-38/w2/artifacts/R38W2ScribeTrend/trend-shonen.md`.

Seat `R38W2ScribeTrend` (scribe, leaf; wave 2). Attack target: the round-38 trend verdicts
(expansion / quality / discernment) and the four SHONEN lines, as they would be drafted from
committed bytes. Read at HEAD `e265533e` (wave-2 dispatch; no scored surface after `0fc61133`),
base `77091b49`, first freeze `e059ca93`, controls `efd5c47a`. No predicate, counter, carrier,
oracle or frozen byte was changed; no counter was re-run (a trend ruling does not need one, and
re-running is not the scribe's job).

Working-tree caveat: at 04:04 `git status --porcelain` showed three tracked corpus files modified
at 04:01:25 (`corpus/knowledge/2026-10-26-unblob-format-matrix.md`,
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`,
`corpus/lessons/round-38.md`) — not written by this seat. All verdicts below are for HEAD bytes
(`git show`/`git diff`), not for that pending tree; §3 F5 describes what the pending edit changes.

## 1. Trend verdicts (deliverable, LEARNING.md definitions)

| trend | verdict | basis |
|---|---|---|
| expansion | **improved** (defect disclosed) | two new admitted `knowledge/` entries (`2026-10-26-r38-sasquatch-be-squashfs-recursion`, `2026-10-26-unblob-format-matrix`), both citing `mined` SOURCES rows and both mapped (126/126); the BE entry is on Frontier ground the Core map did not hold, and the frozen C1 score records `province_core_row false` (measured, not promoted). The matrix entry's false sentence is scored under quality (boundary stated in F5) |
| quality | **harmed at committed HEAD** | the admitted matrix entry misstates the page it cites: 42 of 97 sections carry a `Vendor:` field, so the staged "42 vendor-attributed entries" was per-handler, not a word count; the false sentence is unmarked at HEAD. BE-entry and round-36/dependency scoping still hold |
| discernment | **improved, grounded-criterion branch only** | M38-1 → QUALITY 79, M38-2 → QUALITY 80, each with a check shown able to fail (committed `freeze-drift` receipts: drift at `077e212b`, clean at `cb4326b2`, generator drift at `efd5c47a`). The agree/disagree branch is **unproven**: no non-author spot-check of this round's Gate |

Flip conditions are stated in the artifact §1. The SCORECARD's `coverage 10 → 10` is not in
conflict with `expansion: improved`: the owned-axis score tracks the Core surface (no Core row, C1
stopped), while LEARNING's expansion observable is admitted entries on uncovered ground. Do not
read the score as the trend.

## 2. SHONEN state (four boxes; `SHONEN.md` untouched this round)

`git diff --name-only 77091b49 HEAD -- SHONEN.md` → empty. All four boxes stay `[~]`; none can be
`[x]` (no named non-author verifier — wave seats are the lane, per LEARNING), and `[ ]` fits none
(every box has a resolving pointer).

| box | state | round-38 evidence |
|---|---|---|
| SKILL.md decision tables | `[~]` | SKILL.md untouched; `SKILL.md:81-314` resolves; the 17/17 figure is the lane counter's measure, not re-derived here and already qualified in the box |
| End-to-end task executed and logged | `[~]` | fresher pointer available: `LOG.md:3126-3134`, 8 committed receipts `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json`, C1 score; executed end-to-end and honestly stopped at 3/4 — the box asks executed+logged, not succeeded |
| Executable without oral context | `[~]` | counter-example now on record: the frozen after-harness failed as frozen (M38-4), needed `cb4326b2`, and only the post-fix run produced a receipt |
| PROVINCE accuracy | `[~]` | cited range `97-125` resolves; round-38 edits land at lines 44 and 157, outside it; repaired pointer `.ufo/waves/round-19/evidence/doctor/` resolves; no absorption |

## 3. Findings

**F1 — the R38-C2 certificate is uncommitted and its cited path does not exist (DEFECT).**
- `git cat-file -t 0fc61133:.ufo/waves/round-38/l1/scores/c2-final.json` → `fatal: does not exist`;
  same at `HEAD`.
- `git status --porcelain -- .ufo/waves/round-38/l1/scores/` →
  `?? .ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`.
- `git ls-tree -r --name-only HEAD .ufo/waves/round-38/l1/scores/` → only the two C1 files.
- The receipt that exists on disk (`c2-at-0fc61133.json`) records `revision 0fc61133`,
  `mismatches 0`, `guards_ok true`, `met_target true`, `knowledge_files 126`, `mapped 126` — the
  values SCORECARD states — but it is in no commit.
- Both the SCORECARD R38-C2 row (`SCORECARD.md:3406`) and the lesson
  (`corpus/lessons/round-38.md:11`) cite `…/c2-final.json`. The C2 predicate's counted surface is
  the SCORECARD owned-axes/capabilities rows, SHONEN boxes and PROVINCE Core/Frontier rows
  (`plans/round-38-claims.md` at the freeze), so the claim table's own citation sits in the
  predicate's blind spot: the counter's `met_target` is not evidence against this defect.
- Impact: a cold clone cannot check the round's calibration verdict; this is the R37-CL1 class
  (cite only committed receipts) recurring inside the claim that repairs self-assessment.
  Corroborated independently by peer `R38W2C2Rescore.md` (verdict `DEFECTS FOUND`, reproduced the
  receipt field-for-field); my observations above are my own.

**F2 — the round's Gate has no non-author spot-check (DEFECT against LEARNING).**
- `corpus/lessons/round-38.md` has a `## Gate` with source rows, assimilation and the quarantine
  slice, and no spot-check row; `grep -in 'spot-check'` over it returns only unrelated lines.
- LEARNING requires each round a non-author to sample ≥1 admit and ≥1 reject with agree/disagree
  and a reason. The Gate's decisions this round: admits S112/S113/S114/S116 plus the matrix entry,
  rejects S115 plus two staged assimilation refusals. None is sampled from outside the lane.
- The round-37 closure lesson (`corpus/lessons/round-37-verifier-spotcheck.md`, non-author
  `@m_opus`) was filed in this round and did agree with the 7-Zip refusal that this round
  registered as S115 — a carried decision, not a sample of round-38 admits. It cannot stand in for
  the missing sample.

**F3 — two mined mistakes have no criterion (DEFECT against LEARNING §3).**
- `corpus/lessons/round-38.md` M38-3 and M38-4 both carry `captured-by: none`, and the round added
  only QUALITY 79 and 80 (for M38-1 and M38-2). LEARNING: a mistake no criterion caught becomes a
  QUALITY criterion citing that lesson. Nearest existing rows are 55 (frozen input checked) and 61
  (gate self-invocation); the lesson cites neither.

**F4 — minor: the BE entry's "Independent check" has no pointer (LOW).**
- `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` says "`sasquatch-v4be -be`
  run directly reproduces 16/16 oracle regular files" with no path. The claim is supported by
  committed wave-1 reports (`R38CrossToolK1..K4.md`, `artifacts/R38CrossToolK1/…`), so the fact
  holds; only the entry's pointer is missing.

**F5 — the admitted matrix entry states a false correction (DEFECT at HEAD; repair uncommitted).**
- HEAD text (`corpus/knowledge/2026-10-26-unblob-format-matrix.md`): the staged "42
  vendor-attributed entries" "was a count of the word `Vendor` (42 occurrences), not a per-handler
  attribution count".
- Measured on the same page at the entry's own digest `8f8c29af…bbc5` (re-fetched):
  `split('<h2 id=')` → 97 sections; **42 of them contain a `Vendor:` field**; 42 `Vendor` string
  occurrences too (one field per section); one value is the literal `unknown`; per-section status
  89 "Fully supported" / 8 "Partially supported" (90/8 as raw string occurrences — one extra sits
  outside the section split). The staged claim was therefore substantively right, and the entry's
  "correction" is wrong.
- At HEAD this is unmarked → the quality harm clause. A working-tree edit at 04:01:25 (not this
  seat's) repairs the sentence, adds the per-section counts and credits wave-2 seat
  `R38W2SrcS116` — but it is uncommitted at `e265533e`, so it marks nothing in committed bytes.
- Boundary used for my verdicts: the defect sits in the assimilation-correction sentence, not in
  the ground the entry was admitted on (producer coverage matrix, `SquashFS (v4-BE)`), so I score
  it under quality and keep expansion `improved`. A reader who treats any false sentence as a
  failed admission bar should also mark expansion harmed; both readings are in the artifact.
- The same edit changes the BE entry (symlink sentence now scoped to "every run in which
  `sasquatch-v4be` extracts the image") — that clarifies, and the receipts support both readings
  (before-arms carry only the dependency gap).

**F6 — the pending repair is itself incomplete (DEFECT, uncommitted tree).**
- `git diff corpus/lessons/round-38.md` (working tree) adds "M38-5" only inline in `## Gate`; the
  `## Mistakes` table still has four rows and `corpus/QUALITY.md` is unchanged. LEARNING requires a
  `## Mistakes` row per mistake and a criterion when none caught it, so as it stands the repair
  fixes the entry text without recording the mistake the way the corpus contract asks.

## 4. Checks run (all read-only; exact results)

| check | command | observed |
|---|---|---|
| new entries | `git diff --name-status 77091b49 HEAD -- corpus/knowledge` | two `A` rows: BE entry, matrix entry |
| untouched surfaces | `git diff --name-only 77091b49 HEAD -- SKILL.md SHONEN.md` | empty |
| coverage map | python over `corpus/knowledge/*.md` vs stems in `corpus/README.md` | 126 files, 136 stems, 126 mapped, 0 unmapped; both new stems mapped |
| BE carrier provenance | `sha256sum corpus/evidence/round-37/c1/K{3,4}/carrier.bin` vs tag LFS oids | K3 `9c7c523c…97c0` (4096), K4 `a29ddc15…56ed` (307) — exact |
| BE before/after receipts | `normalized_result` of 8 receipts | before: 4/4 `missing-extractor-dependency` [`sasquatch-v4be`], `files []`; after: K1 5 files/0 gaps, K2 3 files/1 `unpublished-entry` gap, K3/K4 4 files/0 gaps (`coverage complete`) |
| matrix entry recheck | `curl -fsSL https://unblob.org/formats/ \| sha256sum`; split on `<h2 id=`; `grep -c 'more than 30 different'` | `8f8c29af…bbc5` (matches entry); 97 sections; 3× "more than 30 different"; 10 SquashFS sections incl. `v4-BE`, `v4-broadcom` (spelled as the entry corrects it); ZIP note ×1; **42 of 97 sections carry a `Vendor:` field** (42 string occurrences, one value `unknown`), per-section 89 Fully / 8 Partially — this is what makes the HEAD entry's "word count, not per-handler" sentence false (F5) |
| dependency source | `curl … 26.6.4/README.md \| sha256sum`; `grep -n '78+'` | `6544d60f…3716` (= S110 digest); `78+` at lines 5 and 22 |
| BE handler source | `curl …/squashfs.py \| sha256sum`; grep | `2d7b901b…9287`; `V4BE_EXECUTABLE = "sasquatch-v4be"` ×1 (recheck passes) |
| C1 score receipt | `.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` | `carriers_matched 3`, `met_target false`, `revision 3b960fe5…`, `bindings` `entry_present`/`coverage_map_row`/`frontier_note` true, `province_core_row false` |
| freeze-drift receipts | `cat .ufo/waves/round-38/l1/freeze-drift-{077e212b,cb4326b2,gen-controls}.json` | `drift` (`f1010f67`, `79f69347`), `clean`, `drift` (`efd5c47a`) — all committed |
| C2 receipt custody | `git cat-file -t` / `git status --porcelain` / `git ls-tree` | F1 above |
| working-tree drift | `git status --porcelain` at 04:04 | three `M` corpus files (two knowledge entries, the lesson) at mtime 04:01:25 plus untracked `paths_raw.txt`, `c2-at-0fc61133.json`; not this seat's writes — F5/F6 describe the pending edit, verdicts judge HEAD |
| r36 entry scope | `grep -n -i 'endian\|not measured' corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` | lines 180-182 scope BE out explicitly ("All four carriers are LE v4… nothing here exercises it") — not stale |

## 5. Bounds and limits

- Wrote only `.ufo/waves/round-38/w2/R38W2ScribeTrend.md` and
  `.ufo/waves/round-38/w2/artifacts/R38W2ScribeTrend/trend-shonen.md`. Nothing under `corpus/`,
  `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md` or `tools/` was touched; no VCS mutation; no
  subagents; no `agent://all`; no campaign tool in `/home/vgpnk/Projects/shokuknow`.
- No tools installed or upgraded. Downloads for the two rechecks were 216 KB / 14 KB / 7 KB.
- **Bounds deviation (self-reported):** I did not create the mandated `S=/fast/scratch/...`; the
  three downloads went to `/tmp` and `/dev/shm` instead (all under the 50 MB `/tmp` rule, `/dev/shm`
  not sanctioned) and were deleted before this report. Nothing from those paths is cited as
  evidence; only digests and counts are reproduced above.
- `[INFERENCE]` The two `c2-final.json` citations are a naming slip for the receipt the L1
  actually wrote (`c2-at-0fc61133.json`); the peer reached the same reading independently.
- `[INFERENCE]` Whether QUALITY 61 (gate self-invocation) already covers M38-4's class is arguable;
  the lesson itself records `captured-by: none`, which is the basis for F3, not my reading.
- F5 discovery note: my first reads of both entries matched HEAD (before 04:01:25); the re-read
  after the edit showed changed text. F5 rests on the live page measurement, not on either text.
  Per-section "89 Fully / 8 Partially" agrees with my own per-section count; I did not chase the one
  extra `Fully supported` string that sits outside the section split.
- Not done, by bounds: no re-derivation of the C1/C2 counters, no entry edits, no Gate sampling
  (a lane seat could not supply F2's missing non-author sample anyway).
