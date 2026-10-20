# ConnChousaMethod — SOURCES rows must stay a registry, not a method

author: KaidokuR17.ConnChousaMethod-3 (connector); 2026-10-20
scope: read-only method-boundary analysis for round-17 new SOURCES rows (S024+). No REA
analysis, no Ghidra, no carrier execution, no installs.

## Axes named

| axis | what this lane touches |
|---|---|
| calibration | C2 says its warrant "rests on new SOURCES rows opened this round" (`.ufo/waves/round-17/claims.json:23`). A row that states a procedure or an admission rule would let a curation state be read as claim support — the second-method failure rule 3 forbids. |
| depth | The Go 1.27 prediction-vs-observation comparison is only attributable if each row's `anchor` is the exact line/section that states the version/suffix proposition, not a page. A page-level anchor makes a mismatch unexplainable. |

## What the chousa method is, operation by operation

Observation — `chousa-shokunin/SKILL.md` separates four operations, each with its own
output and its own failure row:

| operation | anchor | output | failure row |
|---|---|---|---|
| question framing | `SKILL.md:17` | record with a declared question | starting from a search box |
| source hierarchy | `SKILL.md:18` | hierarchy row per source | aggregator quoted as primary (`:42`) |
| citation chain | `SKILL.md:19` | every hop's anchor verified or unresolved | dead link (`:43`); altered hop when a qualifier drops (`:45`) |
| claim-vs-source check | `SKILL.md:20` | verified / contradicted / unresolved | restatement accepted as source |
| per-claim admission | `SKILL.md:22` | tier-for-this-scope + suitability reason | source label treated as authority for every claim |
| support reporting | `SKILL.md:23` | opens · on-topic · states at a named anchor · true; `verified` needs state 3 | `verified` from access or relevance alone |

Observation — chousa itself says its ladder is "this lane's own construction", a
`proposal` until anchored (`SKILL.md:25-33`). So "the method stays chousa's" does **not**
mean kaidoku inherits the primary>secondary ladder as authority; it means kaidoku must
not mint a *second* ranking or admission rule.

## What rule 3 forbids — and what it does not

Observation — `CORPUS.md:119-122`: claim admission stays in `corpus/QUALITY.md`; the
research method stays chousa's (question → source hierarchy → citation chain →
claim-vs-source check); `SOURCES.md` duplicates neither; `QUALITY.md` points to SOURCES
for tier definitions. Kaidoku already honours both pointers: `corpus/QUALITY.md:41`
("claim admission still follows this QUALITY bar") and `SKILL.md:452` (tier/anchor
maintenance is delegated to SOURCES).

Observation — the frozen contract itself puts method-shaped matter inside SOURCES:
`## Paths` is "ordered study sequences" (`CORPUS.md:81`) and `## Search log` is
PRISMA-inspired (`CORPUS.md:82`, rule 5 at `:126-128`). Therefore the line rule 3 draws
is not "no procedure words in SOURCES". It is:

- **Permitted plane**: this lane's concrete study *order* (`## Paths`), per-search
  *receipts* (search log), scoped A/B/C tiers (`CORPUS.md:93-97`), and what the opened
  artifact states (`teaches`, `:101`).
- **Forbidden plane**: a reusable rule for *ranking*, *admitting*, or *verifying*
  sources that a claim could cite instead of chousa's four operations. That, and only
  that, is the second method.

## Concrete hazards for the round-17 rows

1. **A row is not support.** `status: mined` means only "cited by ≥1 path in used-by"
   (`CORPUS.md:103-104`); it says nothing about the claim's truth. If a new row's
   `teaches` is phrased as the C2 claim, the knowledge entry's claim-vs-source check
   collapses to "the row says so" — chousa state 3 (`SKILL.md:23`) is skipped.
   *Observation*: 16 of 22 non-rejected `teaches` cells currently open in imperative mood
   (`corpus/SOURCES.md:9,10,12,13,15,16,19,20,21,22,23,24,25,27` plus `:7,8`); 6 are
   third-person. *Inference*: the imperatives stay compliant because 15 of the 16 carry a
   scope-bound limiter ("not proof", "does not establish", "within the authors'
   evaluation"). Two cells already lean toward the forbidden plane: S015
   (`corpus/SOURCES.md:21`) is a field-divergence comparison rule, and S011 (`:17`) states
   a general evidential rule ("group evidence by origin rather than count multiple readers
   …") whose only bound is attribution to the paper. Neither is a violation — both are
   scoped — but they are the genre the new rows must not extend into a Go-version rule
   ("compare the release page with the binary's build info when they diverge").

2. **A "Ghidra upstream status" row would duplicate S004.** S004's scope already says
   "not the installed 12.1.4 release" (`corpus/SOURCES.md:10`). Rule 2 (`CORPUS.md:116-118`)
   allows in-place change of only status/recheck/used-by, logged old→new; a correction is
   a *new* row whose `teaches` opens `supersedes S0NN —`. So: extend S004's `used-by` and
   log the delta in the lesson, or open a new row for a genuinely new artifact (a different
   commit or the release-notes page) — never a second row restating S004.

3. **Quotes do not live in the row.** Rule 1 (`CORPUS.md:112-115`) puts the URL, access
   date and ≤25-word contiguous quote in the round lesson's `## Gate`; round-16 is the
   worked example (`corpus/lessons/round-16.md:28-34`). The row carries `source`, `anchor`,
   `teaches` only. A draft that moves the quote into SOURCES duplicates rule 1's location
   and is the first step toward a second record format.

4. **Anchor must state the proposition.** Chousa state 3 requires "states the claim at a
   named anchor" (`SKILL.md:23`). For the Go rows the anchor must name the line/function
   that fixes the semantics — e.g. the version-extraction site in
   `src/debug/buildinfo/buildinfo.go`, the go1.27 section of `go.dev/doc/devel/release`
   with its fetch date, the `internal/buildcfg/exp.go` registry entry for `-X:nodwarf5`.
   *Inference, flagged*: the exact line numbers were not verified here because no Go
   source is installed on this host (`go version` empty; `/usr/lib/go` absent); the
   scout that opens the source must cite what it opened, and a page-level anchor must be
   rejected at Gate time.

5. **Negative claims carry their sweep.** Any "no official doc states X" (e.g. the
   experiment suffix) needs the query and stop rationale in the search log
   (`CORPUS.md:39-41`, `:126-128`; chousa checklist `SKILL.md:62`). Without the sweep the
   row states a method-shaped negative claim — absence asserted, nothing searched.

6. **Rejections are kept.** A refused new source needs `REJECTED: <reason>; flip: …`
   (`CORPUS.md:101-102`; chousa `SKILL.md:64`), as S022 already shows
   (`corpus/SOURCES.md:28`). Deleting a rejected candidate removes the lane's taste record.

7. **Do not build a row-verifier.** The tempting round-17 move — a kaidoku script that
   grades row quotes — would duplicate chousa's citation-chain/claim-support machinery.
   The structural census already exists and is contract-owned (`CORPUS.md:131-148`), and
   the round's `measure.py` is defined as row/tier/status *histograms* only
   (`.ufo/waves/round-17/contract.md`, `W/measure.py`). Keep it representational: a
   verdict on row quality would itself be the second method.

## Proposed move (one, bounded)

Add a three-clause drafting rule for S024+ that is enforced only at Gate review — no new
tool, no new file, no retro-edit of existing rows:

1. `teaches` = third-person "the source states X; it does not establish Y", where Y is the
   nearest overclaim this round could make (e.g. the release page does not establish that
   a given 1.27 binary was built from that release; `debug/buildinfo` does not establish
   compiler identity).
2. The load-bearing claim text and the ≤25-word quotes stay in the knowledge entry and the
   lesson `## Gate`; the row carries only source/anchor/scope/teaches.
3. Any new `## Paths` bullet states sequence plus a "these sources do not establish …"
   limit, as the existing bullets do (`corpus/SOURCES.md:33-39`); it must not state a
   ranking rule ("trust A over B").

*Red test*: delete the "does not establish / not proof / within" clause from a candidate
`teaches`; if what remains is a rule that would apply to a different source, the row is a
second-method candidate and must be rewritten. The test is advisory at Gate, not a gate:
on existing rows it flags S015 and S011 for review (each leaves a general rule once
attribution/limiter is stripped) and clears the third-person descriptive rows (S008, S014,
S018, S020, S023). S011 shows the test errs toward flagging a legitimate knowledge
proposition, which is exactly why it stays a human Gate check and not a lane-local script.

*Affected axes*: calibration (removes the admission shortcut; keeps `mined` a curation
state) and depth (forces line-level anchors, so a prediction/observation mismatch is
attributable to a source proposition). No axis is harmed: the rule adds no execution, no
file, and no change to `QUALITY.md` or `SOURCES.md` structure.

## Contradictions stated, not smoothed

- `CORPUS.md:119-122` assigns the source hierarchy to chousa, but chousa declares that
  ladder its own unproven construction (`chousa-shokunin/SKILL.md:25-33`). Resolution used
  here: kaidoku's A/B/C are the frozen contract's curation vocabulary, not a rival ladder;
  a row that writes a *general* preference rule would be the rival ladder and is
  forbidden. The two statements are compatible only under this reading.
- Rule 4 (`CORPUS.md:123-125`) counts expansion by knowledge entries citing a `mined` row,
  while rule 1 writes rows only after opening. A row that is `queued` with `used-by: —`
  but already cited by the draft knowledge entry would be invisible to the expansion
  count. Resolution: L1 flips the row to `mined` in the same commit that lands the
  knowledge entry, logging old→new (rule 2); the census then finds the path
  (`CORPUS.md:146-148`).
- `teaches` as "learner benefit" (`CORPUS.md:101`) is grammatical, not procedural; the
  proposed third-person form stays inside that field definition while removing the
  imperative residue.

## Verification (for L1, after integration)

- Census at the round revision, from the lane root: row count, malformed = 0, duplicate
  ids none, enum/tier-inflation none, missing `used-by` paths none (`CORPUS.md:131-148`).
- Draft-level check: the clause-deletion test above is the primary screen and is shown
  able to fire (S015, S011). Secondary `grep -nE 'must|should|prefer|authoritative for
  every|verified'` over the new rows must return nothing outside quoted source text; note
  this grep does not fire on S015 (no banned token), so it supplements, never replaces,
  the clause test.
- Gate table in `corpus/lessons/round-17.md` lists URL, access date and a ≤25-word
  contiguous quote for every new row, matching `corpus/lessons/round-16.md:28-34`.
- No new source id below S024, no reused id (`CORPUS.md:88`), and `community` never tier A
  (`CORPUS.md:97`).
