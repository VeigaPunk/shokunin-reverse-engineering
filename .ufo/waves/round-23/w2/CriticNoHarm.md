# W2 CriticNoHarm — R23-C1 final-producer no-harm read set

Seat `KaidokuR23.CriticNoHarm`, source review only. Candidate
C=`2838351450ff1ee4baa620c962a1153450d53311`, B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`,
measured V=`6615aeae642aec36959180e7ea940b2794c7f1cb`. Every candidate byte below was read
with `git show <rev>:PATH` or `git diff`. I ran no tests, builds, counters, producers or REA.

Axes attacked: immutable prior knowledge/source rows; append-only SKILL/PROVINCE/LOG/SCORECARD;
R22 C1=1/6 and C2=14/14 "at final"; inherited pointer drift; whether the producer's read set
is bound to the committed revision.

## Findings

### F1 — MEDIUM, fixable: the source census reads the live tree but is labelled with the committed revision (false provenance)
- Observed: `C:.ufo/waves/round-23/verify.py:110` runs
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`.
  This runs **outside** the `with tempfile.TemporaryDirectory` clone block (lines 53–109), with
  a hard-coded absolute root. `record()` (lines 38–50) stamps it `source_rev: rev`.
- Observed: the retained `C:.ufo/waves/round-23/verify/initial/source-census.json` stdout ends with
  `kaidoku\tok\t/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. The census
  therefore validated the moving working-tree file, and E11 (`used-by` path on disk) was resolved
  against the live tree. The record still says `"source_rev": "6615aeae…"`.
- Observed: the census is not git-aware. Its header (`scripts/sources-census.sh:6-7`) says it
  "reads corpus/SOURCES.md". Line 501 derives the lane directory from `dirname(file)/..`.
- Counterexample (inferred, not run): with an uncommitted edit to `corpus/SOURCES.md` or a deleted
  `used-by` file in the worktree, `verify.py --rev <clean C>` reports the census against the dirty
  tree but credits C. The reverse also holds: a committed E-finding is masked if the live tree is
  repaired. Running with `--root` set to another worktree still checks the main checkout.
- Bounded negative (observed): no actual divergence at V. `corpus/lessons/round-23.md` exists at V,
  `SOURCES.md` is byte-identical from V to C, and `git status --porcelain -- corpus SKILL.md
  PROVINCE.md LOG.md SCORECARD.md` is empty now. The defect is latent, not shown to have changed a
  verdict.
- Axes affected: provenance of "source census exit0" (no_harm item 6); the identity binding of
  the final producer.
- Smallest safe correction: move the census call inside the clone block and pass the clone as an
  explicit lane directory, e.g.
  `record('source-census',[census,'validate',str(clone)],0)` or
  `[census,'validate','--file',str(clone/'corpus/SOURCES.md')]`. Line 501 then resolves `used-by`
  inside the snapshot.

### F2 — MEDIUM, disclosure: no producer run exists at C, so "R22 C1=1/6 and C2=14/14 at final" is inferred, not exercised
- Observed: the only committed producer output is `verify/initial`, at V. The `verify-initial-producer.json`
  argv has `--rev 6615aeae…`, and `git show V:.ufo/waves/round-23/verify/initial/summary.json`
  fails because the records were committed later, in C.
- Observed: `git diff --stat V C` shows 18 files, all additions. They are the verify records,
  `LOG.md` +19, `SCORECARD.md` +29 and `corpus/lessons/round-23.md` +25.
- Inferred: the R22 counter inputs do not overlap that delta. R22 C1 reads `corpus/knowledge`,
  `corpus/SOURCES.md`, R22 evidence and the R20/R21 verb-coverage tools
  (`C:.ufo/waves/round-22/tools/count-c1.py:33-56,116-123`). R22 C2 reads the `PROVINCE.md` R22
  section and R22 receipts (`count-c2.py:4,39,193`). None of these changed from V to C, so 1/6
  and 14/14 should hold at C. The same reasoning covers `controls.py`, because LOG and SCORECARD
  are append-only from V to C. **Unexercised.**
- Observed: the C text labels these "initial" measurements at V (`SCORECARD.md` "Round-23 initial
  committed measurements", `LOG.md` "exercised initial verification"). It is honest, but the
  claims.json wording "at final" is not yet met by any run.
- Correction: the designated Run seat, or L1, runs `verify.py --rev 2838351…` once into a new
  `--out`. Until then, report the C values as inherited from V by input disjointness.

### F3 — LOW–MEDIUM, producer read-set gap: no-harm checks cover a narrower set than claims.json and LOG imply
`controls.py` (`C:.ufo/waves/round-21/controls.py:80`) byte-checks only
`.ufo/waves/round-20/`, `corpus/knowledge/` and `corpus/lessons/` (1138 files), plus LOG and
SCORECARD prefixes and QUALITY rows. `verify.py:94-105` adds the `| S` rows of `SOURCES.md` and the
SKILL/PROVINCE prefixes. None of the following is byte-checked by the producer:
- `.ufo/waves/round-21/**` and `.ufo/waves/round-22/**`, including the R22 C1 witnesses in the
  claim's `read_set`, and `round-22/frozen/*`. The R22 counters only detect changes that move their
  count. Observed clean anyway: `git diff --name-only B C -- .ufo/waves/round-2{0,1,2}
  corpus/knowledge corpus/QUALITY.md` lists 0 files.
- Non-row content of `SOURCES.md`: the Paths section, older search-log entries and Leads. The
  `| S`-row filter at `verify.py:94-95` ignores them. Observed clean anyway: numstat 6/0, with the
  R23 search-log entry inserted after the last prior entry (old line 110).
- `corpus/README.md` outside the coverage-map stem set. `controls.py:62-63` checks only that stems
  appear in `## Coverage map`. Counterexample (inferred): rewriting an old coverage-map state cell
  from "held narrowly" to "held", or editing an old Knowledge/Frontier row, passes
  `controls_clean`. Observed: at C, README's only deletions are 3 blank lines; every non-blank
  line at B is preserved.
- Axes affected: "All pre-round knowledge and source rows unchanged", "Historical R22 witnesses
  preserved" and "map integrity". These are true at C by direct diff, not by the producer.
- Correction: add one byte-preservation check in `verify.py`, for example
  `git diff --name-only --diff-filter=MDR B rev` restricted to everything outside
  `.ufo/waves/round-23/` and the five append files. Assert it is empty, and assert that README's
  non-blank lines at B appear in order at rev.

### F4 — LOW, inherited pointer drift is neither caused nor disclosed by R23
- Observed: `SCORECARD.md:69` (identical at B and C) says the frontier bullet "now reads 'held, not
  frontier' (`corpus/README.md:180`)". `README.md:180` is the `.jsc → source mapping` frontier
  bullet at both B and C. The "held, not frontier" bullet is at `README.md:186` at both.
  `SCORECARD.md:2077` still states the constraint that the index "cannot grow above `## Frontier`
  while `SCORECARD.md:69` pins `corpus/README.md:180`".
- Observed: W1 already found this. `C:.ufo/waves/round-23/w1/ConnectFrontier.md:99` records
  `sc69-readme-177 … MISMATCH (… that bullet is now README:186)`.
- Observed: R23's LOG says only that "README rows consume existing separator lines so older
  downstream numbered pointers are not shifted wholesale" (`C:LOG.md:2622-2623`). The R23 SCORECARD,
  LOG and lesson never mention the existing `SCORECARD.md:69` mismatch, and no no-harm check
  covers SCORECARD→README pointers. "citations17/17" counts only SKILL craft rules
  (`controls.py:64-74`). Nothing calls this pointer clean explicitly. Read beside the
  "not shifted" sentence, though, an omission leaves a reader free to assume it is clean.
- Observed: R23's own shifts are confined to `README.md` lines 72–73, 159–160 and 176–177. The
  `## Knowledge`, `## Lessons` and `## Frontier` headings each move down one line; all other line
  numbers in the 196-line file are content-stable. No active-document pointer (SKILL, SCORECARD,
  LOG, PROVINCE, corpus, R21–R23 reports) targets those six lines. `SOURCES.md` lines 64–121 shift
  by +4 or +6. The only pointers into that range are W1/R17 reports. R23's
  `SOURCES.md:64-66` now resolves to S058–S060 as intended, and R17
  `ReopenS029.md:110` was already historical.
- Correction: one append-only LOG/SCORECARD sentence naming the inherited
  `SCORECARD.md:69 → README.md:180` mismatch, which actually lives at :186, as carried and unrepaired.
  Do not rewrite `SCORECARD.md:69`, which is in the immutable prefix.

### F5 — LOW, convention identity: a merged Knowledge-index row
- Observed: the C `corpus/README.md` Knowledge table now has one row listing two entries
  (`2026-10-21-r23-offline-signal-envelopes`, `2026-10-21-r23-dart-legacy-layout-boundary`). It is
  the only multi-entry row in that table, so the table no longer has one row per entry. The merge
  lets a single row consume the single blank separator.
- Observed: no fleet script parses `## Knowledge` or `verified-at`
  (Grep of `/home/vgpnk/Projects/shokunin/scripts`: 0 files). `controls.py` uses only the coverage
  map. There is no measured harm.
- Disclosure: LOG states that separator lines were consumed. It does not state the two-entry merge.
  This is a tradeoff, not a defect; an append-only note is enough.

### Clean (observed, not inferred)
- Prior knowledge and source rows: `git diff --name-status B C` outside `.ufo/waves/round-23/` lists
  exactly 9 paths. There are 6 modifications (LOG, PROVINCE, SCORECARD, SKILL, corpus/README,
  corpus/SOURCES) and 3 additions (two R23 knowledge entries and `corpus/lessons/round-23.md`).
  No `corpus/knowledge` or `corpus/lessons` file from B is modified.
- Append-only files: numstat deletions are 0 for `LOG.md` (+78), `SCORECARD.md` (+46), `SKILL.md`
  (+37), `PROVINCE.md` (+24) and `corpus/SOURCES.md` (+6). `corpus/README.md` is +3/−3, with all
  three deletions blank lines. S001–S057 are identical and S058–S061 follow S057. The retained
  `source-prefixes.json` reports 57→61, `old_rows_unchanged`, `skill_prefix` and
  `province_prefix` all true.
- Producer identity: sha256 of `verify.py` at V and at C is
  `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a`, which equals the recorded
  `producer_source_sha256`.
- Retained no-harm at V (`verify/initial/no-harm.json`): exit 0, `controls_clean`, 1138 prior files
  with 0 changed, QUALITY 32→32 identical, map 104→106 with nothing missing, rules 17/17.

## Produced files and hashes
- `.ufo/waves/round-23/w2/CriticNoHarm.md`: this file. Its sha256 is reported in the seat's
  final message, because a file cannot contain its own hash.

## Installs
None.

## Open risks
- F1 stays latent until the census is bound to the clone. Every future census "exit0" record from
  this producer inherits the live-tree read.
- F2: "at final" for R22 C1/C2, no-harm and census at C is unexercised. Only V has a run.
- I did not review count-c1 semantics, the evidence envelopes, or the correctness of the source
  rows. Those belong to sibling seats.
- R22's 102 reportless seats are outside this seat's read set and were not re-evaluated.
