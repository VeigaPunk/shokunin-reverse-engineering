# ConnectorCross — round-75 cross-surface scan (sibling scan, milestone r75-w1)

Seat: ConnectorCross (connector, leaf). Date: 2026-11-04. Method: read-only scan of the
lane repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, the fleet root
(`/home/vgpnk/Projects/shokunin/scripts`, sibling `*-shokunin` lanes), and
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/`. No instrument was executed against claim
data; no files outside this findings file were written. Lane HEAD at scan time: `668e545e`
(post-freeze landing commits; only untracked path is `.ufo/waves/round-75/w1/`).

Id note: the frozen assignment text names "S283 admitted / S284 rejected". The tree's
disclosed errata (`.ufo/waves/round-75/claims.json:80-89`) record that S283 (`re.fullmatch`)
was withdrawn as a duplicate of S143; the live round-75 rows are **S277** (proc_pid_cmdline(5),
retrospective round-73 row), **S284** (os.path.commonpath, mined), **S285** (environ(7),
rejected). This report uses the live ids.

## Item 1 — Do the fleet census or another lane already implement round 75's grammars?

Surfaces scanned: `scripts/sources-census.sh` (fleet gate, 806 lines, read in full);
`kumitate-shokunin/scripts/sources-check.mjs`; `tabi-shokunin/scripts/check-sources.mjs`;
`tsukuroi-shokunin/tools/check-source-scope-correction.py`; fleet-wide grep for
`Where searched|census erratum` over `*/tools`, `*/scripts`, `scripts/` (only this lane's
own `tools/round-74/record-audit.py` and `tools/round-75/record-audit.py` match);
fleet-wide grep for `REJECTED:|flip:` (kumitate, tabi, tsukuroi hits above, plus this lane).

The lane's four grammars live in `tools/round-75/record-audit.py`: `PATH_RE` (:74),
`parse_used_by` (:156-181), `parse_search_note` (:184-200), `parse_rejected_row`
(:203-220), `parse_census_erratum` (:223-233), exercised by `GRAMMAR_CASES` red fixtures
(:236-261) and — since disclosed amendment `7edb005e` — applied to live cells by
`atom_grammar_reds` (:363-395): S277's used-by cell, the round-75 search-log note
(`corpus/SOURCES.md:230`), S285's rejected row, and the census erratum in SCORECARD.md's
round-75 section, measured against `census_rows` (:148-149).

### Clause-by-clause comparison

**Clause a — used-by path list.**

- Lane D9' (`record-audit.py:156-181`): every comma token must match
  `^(?:corpus/knowledge|corpus/lessons)/[A-Za-z0-9._-]+\.md$` (:74); tokens prefixed
  `not|no|never` (case-insensitive) are defects; empty / only-`—` cell is a defect;
  status-agnostic. Amended D20 additionally resolves each kept path at the measured
  revision via `git show` (existence bound to the rev, not the worktree).
- Fleet census (`sources-census.sh:544-570`, function spans :561-571 per line grep):
  only rows with `status == mined` (:559); tokens split on comma, trimmed; empty/`—`
  skipped; sole test is disk existence `[ ! -e "$dir/$path" ]` → E11 (:566-567). No path
  shape, no negation handling. Note the existence probe concatenates `$dir/$path`, so an
  absolute token (e.g. `/etc/passwd`) would bypass the lane-root prefix entirely.
- Divergences that would make the two disagree on the same cell:
  1. **Status scope** — census checks only mined rows; D9' applies to any row's cell.
     A queued/rejected row with a malformed used-by is census-silent, lane-red.
  2. **Shape vs existence** — a token that exists on disk but is not a corpus path passes
     E11 and fails D9'. Live precedent: **S275's used-by cell
     (`corpus/SOURCES.md:192`) still contains `.ufo/waves/round-72/w1/ScoutSource.md`** —
     census-clean (the file exists), grammar-red (PATH_RE rejects it). No live atom
     conflict only because amended D20 applies D9' to S277, not S275. Contested scope,
     named below.
  3. **Negation** — a negated token `not corpus/knowledge/x.md` reaches E11 as a missing
     *file* and fails the gate only for mined rows; D9' defects on the negation itself
     for any row. Conversely a file literally named `not …` would pass E11 and fail D9'.
  4. **Empty/`—`** — census W03 "mined but unused" (:673-674) and W01 tier-C/mined
     (:669-670) are warnings that never change a lane's exit; D9' treats an empty cell as
     a defect.
- Verdict: **duplication, divergent**. The fleet gate owns existence/E11; the lane owns
  shape/D9'. Neither can certify the other; the divergences above are the exact seams.

**Clause b — search-note fields.**

- Lane D10' (`record-audit.py:184-200`): exactly one line naming the label; required
  substrings `Question:`, `Where searched:`, `Identified`, `screened`, `included`,
  `excluded`, `Stop:`; integer counts via `(Identified|screened|included|excluded)\s+(\d+)`
  (number must immediately follow the word — `Identified: 4` with a colon fails).
- Fleet census: no search-log concept. kumitate/tabi/tsukuroi scripts: no matches for the
  field set (grep above). Only this lane's round-74 audit touched the same surface with a
  weaker predicate (round 74's D10 atom checked the search log's presence, not the fields).
- Live target parses clean: `corpus/SOURCES.md:230` (round-75 note, counts 4/4/2/2).
- Verdict: **new ground** (lane-owned). No divergence possible with the census gate
  because the gate has no corresponding clause; the only risk is internal strictness
  (the colon form above), not cross-surface disagreement.

**Clause c — rejected row.**

- Lane D11' (`record-audit.py:203-220`): cell 8 (index 7) must be exactly `rejected`;
  teaches cell must match `^REJECTED:\s*(.+?)[;\s]*flip:\s*(.+)$` (IGNORECASE); reason
  ≥ 3 words; flip ≥ 3 words. Red fixtures: `d11-empty-flip-red`, `d11-complete-accepts`.
- Fleet census W02 (`sources-census.sh:671-672`): `status=="rejected" &&
  length(teaches)<8` → warning, exit 0. A teaches of `REJECTED: x` (10 chars, no flip)
  or any 8+ char non-conforming string passes the gate and fails D11'. The gate cannot
  certify D11', and W02 never fails a lane.
- Sibling lanes DO implement this clause:
  - `kumitate-shokunin/scripts/sources-check.mjs:322-327`: `REJECTED_NO_REASON` and
    `REJECTED_NO_FLIP` as **errors**, substring `includes('REJECTED:')` and regex
    `/\bflip:/u` — with an explicit negative selftest (:740-747): `reflip:` does NOT
    satisfy the marker.
  - `tabi-shokunin/scripts/check-sources.mjs:325-326`: `rejected_without_flip` as an
    error, pure substring `includes('REJECTED:') || includes('flip:')`.
- Cross-implementation divergences:
  1. **Anchor** — D11' is start-anchored (`^REJECTED:`); kumitate/tabi are substring
     checks. Teaches `note: REJECTED: reason; flip: condition` (leading junk) passes
     kumitate/tabi, fails D11'.
  2. **`reflip:` edge** — kumitate's `\bflip:` refuses `reflip:` and selftests it; D11's
     `(.+?)[;\s]*flip:` can absorb the `re` into the reason group and accept
     `…; reflip: …` if both sides carry ≥ 3 words. The lane grammar is **looser** than
     kumitate's on this marker; the fleet census is silent. Latent (no live row carries
     `reflip:`); named as contested scope, not absorbed.
  3. **Severity** — census: warning; kumitate/tabi: error; lane: atom defect.
- Live target S285 parses clean (`corpus/SOURCES.md:202`: `REJECTED: defines the C
  environment array, … Flip: the page states the cmdline layout …`).
- Verdict: **duplication with divergences** — kumitate and tabi got here first on the
  REJECTED:/flip: clause (owner lanes for the substring form); the lane's anchored,
  word-counted form is its own instrument; all three disagree with the fleet gate, which
  checks only length.

**Clause d — erratum binding.**

- Lane D12' (`record-audit.py:223-233`): the round's SCORECARD section must contain
  `census erratum`, a 2-4-digit number equal to the measured row count, and `W04`.
  Amended D20 measures with `census_rows(sources)` — line regex `(?m)^\|[ \t]*S[0-9]{3,}[ \t]*\|`
  (:148-149) — over `corpus/SOURCES.md` at the measured revision.
- Fleet census: no erratum concept; it produces the values (rows, W04) but validates no
  record that names them. No sibling lane implements it.
- Divergence (latent) in row counting: census counts rows only inside `## Registry` with
  0-3 leading spaces and skips separator rows (`sources-census.sh:547, 617-630`);
  `census_rows` requires column-zero `|`, counts any section (an E12 out-of-section row
  would count for the lane, not for the census) and rejects 1-3-space indentation (counts
  for the census, not for the lane). Today the two agree (census-end 191; lesson records
  191 at round end, `corpus/lessons/round-75.md:36-37`, and 23 W04 at both censuses,
  `.ufo/waves/round-75/l1/census-start.txt`), so the erratum's value is currently
  consistent with the gate; the counting-rule difference is the seam where they could
  silently split.
- Verdict: **new ground** (lane-owned), bound to the census gate's output values by
  convention, not by a shared parser.

### Item 1 summary

| Clause | Fleet census | Sibling lanes | Verdict |
|---|---|---|---|
| used-by path list | E11 existence, mined-only, no shape | none | duplication, divergent (4 named seams) |
| search-note fields | none | none | new ground |
| rejected row | W02 length<8, warning only | kumitate (anchored? no — substring +\bflip:, error), tabi (substring, error) | duplication, divergent (anchor, reflip:, severity) |
| erratum binding | none | none | new ground, census-value-bound |

## Item 2 — sole_detector overlap with existing instruments

- Definition this round (`tools/round-75/probe-mutation.py:263-265` in `score_text`):
  per mutant, `sole = (verdict == "killed" and failed == [expect_case])` — the mutant's
  failure list must be EXACTLY its one declared case. Emitted as `sole_detector` map +
  `multi_detected` list (:335-337), asserted via `--expect-sole` (:328, :438), and
  independently recomputed in `validate()` (:374-383) so a self-declared map cannot
  certify itself.
- Round-74 battery (`tools/round-74/probe-mutation.py`): same `classify` membership
  semantics (:172-178, `killed`/`killed_wrong_case`) but rows carry only
  name/expect_case/rc/failed/cases/verdict (:218-221) — **no `sole` field, no
  `sole_detector` map, no `--expect-sole`**. The round-74 cross-binding (canary-field
  deletion also failing `a12-kernel-multiple-samples`) was exactly the absence of this
  concept. New in round 75.
- `tools/round-{69,70,72,73}/mutation-check.py`: same membership classify
  (`expect_case in result["failed"]`), no sole semantics.
- `tools/round-67/mutation-battery.py:45-53`: closest ancestor — `EXPECTED_CASES` = "the
  EXACT failed-case set each mutant must produce; containment is not enough"
  (e.g. `equiv-doctored-bound` + `equiv-doctored-diffs` for one mutant). Overlapping
  family (exact-set kill verification vs containment), different granularity: round 67
  declares a per-mutant SET (size ≥ 1) as the oracle; round 75's `sole` is the strict
  single-element case `failed == [expect_case]` derived from the mutant's declared case,
  and feeds a detector-uniqueness claim rather than a kill claim. No conflicting
  semantics — round 75 narrows round 67's exact-set rule to one case and names it.
- Name collisions only, no semantic overlap: `truth_sole_consistent` /
  `openchain_sole_unfiltered*` in `tools/round-25/a2/resolve-selectors.py`,
  `round-28/c1-heldout-naming.py`, `round-29/c1-fresh-naming.py` ("the only consistent
  candidate" in 4byte/openchain selector resolution); "sole pass condition" comment in
  `round-34/version-needs-counter.py:107`.
- Bound as a criterion: `corpus/QUALITY.md` row 133 ("a mutant has one declared detector
  … The battery records `sole: failed == [expect_case]` per mutant").
- Verdict: **new ground** for this lane's battery lineage; closest prior art is round 67's
  exact-set rule (superset semantics, no conflict). Selftest gap to note (not a defect
  against the frozen claim): the battery `selftest()` cases cover patch/classify/pin but
  no `sole` case — sole is only re-derived in `validate()` and exercised end-to-end by
  the two battery arms in the pre receipts.

## Item 3 — QUALITY.md criterion for "token presence instead of shape"

The criterion already exists, committed at `bfdf03dd` ("round-75: the lesson, the sourced
entry, the registry rows and the two criteria"), as two rows:

- **Row 133** (`corpus/QUALITY.md:210`): "A case that feeds a value merely equal-ish to
  the sensitive one — … — cannot see the mutation it is supposed to kill; and a case
  whose field another case also reads is not a sole detector, whatever its row claims.
  The battery records `sole: failed == [expect_case]` per mutant and a claim that names
  a sole detector requires it." — the R75-C1 face.
- **Row 134** (`corpus/QUALITY.md:211`): "A record check that tests for a token's
  presence accepts a cell that negates the token it names, a line that carries the field
  names without the counts, a pair of values in the wrong order, or a rejection with no
  flip. The atom parses the cell with an exact grammar … and the audit's own selftest
  carries one red fixture per grammar …" — the R75-C2 face, citing `GRAMMAR_CASES` and
  the four `parse_*` functions.
- The same class statement is in `corpus/lessons/round-75.md:14` ("A predicate that
  tests for a token's presence, not for the shape the token must have", faces (a) and (b)).
- Nearest earlier rows: 25/26 (token/path predicate over Evidence records), 54 ("token
  co-occurrence alone is insufficient"), 78 (`fullmatch` vs `search`). None covers the
  grammar-shape class; none is superseded by 133/134 (different scopes).
- Verdict: **no new row needed; no supersession**. Rows 133/134 ARE the mined mistake
  class, cited to the round-74 spot-check §6 items 3-4 and the round-75 instruments. If a
  future round repairs the `reflip:` looseness found in Item 1c, the lane's own
  convention (rows are replaced by new rows naming what they supersede) applies — out of
  this round's scope.

## Item 4 — considerthese/ and shokuknow merge/kaidoku/ (assimilation line)

- `considerthese/`: **absent in this lane** (glob of the fleet root: 17 sibling lanes
  carry `considerthese/`; `kaidoku-shokunin` is not among them). The claims doc's
  "considerthese/ is absent in this lane (no directory)" is confirmed against the tree.
  Sibling lanes' directories are their own surfaces and serve nothing in this round's
  claims.
- `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`: exists; a staged corpus-expansion
  package (`MERGE-REPORT.md`): 132 proposed rows (ids from S106), 77 knowledge entries
  from rounds 1-16, subject matter adb / REA / unblob / AVM firmware; "Nothing was
  written into the lane repo." Grep for `round-?75|seam-probe|canary|sole` hits only
  ordinary prose ("selected solely by the superblock equality",
  `SOURCES.append.md:91`; "appear solely as 24 `adb-provider` entries",
  `rea-adb-operation-vocabulary.md:21`). No A12/seam-probe material, no record-grammar
  material, no round-75 source rows. The package predates rounds 72-75's subjects.
- Verdict: **neither serves this round's claims** — `Assimilation: none` stands, exactly
  as the frozen frontier step states. The merge package remains a rounds-1-16 backlog
  with an adopt checklist; it does not intersect R75-C1/R75-C2 surfaces.

## Contested scope (named, not absorbed)

1. **S275 used-by vs the lane's own D9' grammar** — the registry cell carries
   `.ufo/waves/round-72/w1/ScoutSource.md`, which PATH_RE rejects but census E11 accepts.
   Amended D20 scopes D9' to S277, so nothing fails; but the registry and the lane
   grammar disagree on a live cell. Fixing the cell (scribe/registry owner) vs widening
   PATH_RE (instrument owner) is a decision for the L1 — this seat changes neither.
2. **`reflip:` marker looseness** — D11's regex can accept a `reflip:` marker that
   kumitate's checker explicitly refuses and selftests. Latent; needs a lane decision
   only if the fleet ever unifies rejected-row checks.
3. **Row-counting rules** — `census_rows` (column-zero, any section) vs census
   `rows++` (Registry-section, 0-3-space indent). Equal today (191/191, 23/23 W04);
   the erratum's measured value is the seam if a future edit adds an indented or
   out-of-section row.
4. **Frozen-text id drift** — the assignment paragraph's S283/S284 vs the tree's
   disclosed errata (S283 withdrawn as S143 duplicate; live rows S277/S284/S285).
   Disclosed in `claims.json` `errata`; recorded here so validators comparing against
   the frozen paragraph are not confused.
5. Hygiene note (not contested scope): `tools/round-75/__pycache__/record-audit.cpython-314.pyc`
   exists in the tree (gitignored byproduct of a non-`-B` run). Left untouched; the
   frozen counting command is `python3 -I -B`.

## Verification of this scan

- Fleet census read in full; line numbers cited from grep -n output.
- Lane instruments read at the cited ranges; sibling scripts read at the cited lines.
- Fleet-wide greps: `Where searched|census erratum` over `*/tools */scripts scripts`
  (2 hits, both this lane's record-audits); `REJECTED:|flip:` over the same scope
  (kumitate, tabi, tsukuroi, this lane).
- `git status --porcelain` at scan time: only `?? .ufo/waves/round-75/w1/` — the claims
  amendments and instrument supersessions cited above are committed landing work with
  disclosed `instrument_supersessions`/`errata` in `claims.json:55-89`, conforming to
  QUALITY rows 33/130.
- Read-only throughout; no claim-data instrument was executed.
