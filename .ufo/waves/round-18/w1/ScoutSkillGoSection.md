# ScoutSkillGoSection — C3 Swiss-map replay: exact update sites

Seat: `KaidokuR18.ScoutSkillGoSection` (leaf, read-only). Revision:
`9011581d84527ba34c675f9cf912e54d2e72d470` (`git rev-parse refs/heads/main`, exit 0).
No REA `analyze`/`search`/`decompile`, no Ghidra/analyzeHeadless, no carrier execution,
no installs (nothing installed or upgraded). Files read unmodified; anchors are the
`grep` tool's line numbers, cross-checked with raw `read` ranges.

## Commands (all exit codes literal)

```text
$ ls -la .ufo/waves/round-18 .ufo/waves/round-18/w1
  w1/ holds only swarm-registry.json; carriers/ holds build.sh + src/{methods,nomethods}
  no predictions/, no tools/, no runs/ yet                                  EXIT:0
$ wc -l SKILL.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
  546 SKILL.md
  198 corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
                                                                            EXIT:0
$ sha256sum SKILL.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
  bf68da135a9da6abb74ea774f1b7f19fdebf09331d2544730e0efb8d78be49b4  SKILL.md
  acd8dffd7662836b34bdd8f7f79be39eb11027b692a2d8a3fa2798a2a954ab55  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
                                                                            EXIT:0
$ git rev-parse refs/heads/main
  9011581d84527ba34c675f9cf912e54d2e72d470                                  EXIT:0
```

## Outcome gates the wording must respect

OBSERVATION from `claims.json` C3: the status move and the prediction score are two
separate axes (`falsifiable_before_after` reports compare exit per carrier "match or
not", and separately moves the mechanism status). The documents should therefore gate
on the **discriminating pattern**, not on 8/8:

- **CONFIRMED** — the two `s*-swiss-methods` carriers abort symbol markup after
  bootstrap with the predicted `Unable to read past EOF` read, and their `noswissmap`
  twins plus all four nomethods carriers do not. Compare exit 0 is corroboration, not
  the definition.
- **REFUTED** — the layout does not discriminate: swiss+methods does not abort, or
  noswiss+methods aborts the same way. (A prediction miss on a non-discriminating
  carrier does not by itself refute.)
- **NEITHER** (guard) — unbound/missing logs, no emulator output, compare exit 2, or a
  bare `Go analysis failure` without the predicted EOF pair. That is
  "replay attempted, inconclusive"; `not replayed` in SKILL.md:528 is stale either way.

## A. Must change in both outcomes

### A1. `SKILL.md:528` — `Bootstrap OK …` row, **Limit** cell (primary site)

Current (verbatim):

```text
INFERENCE, not replayed: Swiss maps read with the `OldMapType` layout from `go1.25.0.json` (S032 lead), not the patch fallback
```

CONFIRMED replacement cell:

```text
OBSERVATION, replayed on the round-18 eight-carrier pair: Swiss maps with method info read under the `OldMapType` layout abort symbol markup; `noswissmap` twins and nomethods carriers do not. Synthetic {1.24.6,1.25.0}, x86-64 ELF, calibrated on aether; not every carrier, and aether's exact invoking record stays inferred. Not the patch fallback
```

REFUTED replacement cell:

```text
INFERENCE, replayed-refuted on the round-18 pair: the `OldMapType` binding did not separate swiss from `noswissmap` carriers, so it is not the demonstrated cause of this failure. The `go1.25.0.json` binding stands; its causal link does not. Not the patch fallback
```

If the run lands in NEITHER: `INFERENCE, replay attempted but inconclusive (W18/runs; unbound log or no emulator output)`. A compare exit 1 with a clear discriminating pattern is not NEITHER: the pattern sets the status, and the mismatch is reported separately.

OBSERVATION: this is the only `SKILL.md` line mentioning aether, `Swiss` or
`OldMapType`; the only other hit for `grep 'aether|Swiss|OldMapType|INFERENCE|S032'`
is the S032 source list at `:512`.

### A2. `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:145-160` — `INFERENCE, aether cause`

Current block asserts the mechanism and ends `:158-160` with "These are seat byte traces
(…), not a Ghidra replay with instrumentation. The exact invoking record is unresolved."

Both outcomes make `not a Ghidra replay`/`not replayed` stale. The entry is **append-only**
under QUALITY #19 (`corpus/QUALITY.md:29`: an overstatement is corrected "by a named
append-only line carrying the exact `file:line`, never by rewriting filed bytes"), and
the r14 precedent is an appended correction plus qualified summaries
(`corpus/lessons/round-14-verifier-spotcheck.md:106`). Append a section; do not rewrite
:145-160.

CONFIRMED append:

```text
## Erratum — aether cause status (round 18, append-only)

- R18-REPLAY: the `INFERENCE, aether cause` block at :145-160 is replayed-confirmed on
  the round-18 eight-carrier pair {go1.24.6, go1.25.0} x {swiss, noswissmap} x
  {methods, none}: both swiss+methods carriers abort `GolangSymbolAnalyzer` symbol
  markup with the predicted `Unable to read past EOF` pair; the noswissmap twins and
  all four nomethods carriers do not. Evidence: `W18/runs/<label>/{receipt,compare}.json`
  (compare exit 0), predictions frozen at <REV> before the runs. Limits: synthetic
  carriers, x86-64 ELF, Ghidra 12.1.4; aether's exact invoking record (:149-152) remains
  a byte-trace inference, and the in-memory size-field reads are emulated from bytes and
  installed source, not observed inside Ghidra.
- The status clause at :158-160 ("not a Ghidra replay with instrumentation") is
  superseded as a status, not as a fact: the round-18 replay is log-bound and
  uninstrumented, and the exact aether record remains unresolved.
```

REFUTED append:

```text
## Erratum — aether cause status (round 18, append-only)

- R18-REPLAY: the `INFERENCE, aether cause` block at :145-160 is replayed-refuted on
  the round-18 eight-carrier pair {go1.24.6, go1.25.0} x {swiss, noswissmap} x
  {methods, none}: <observed pattern — swiss+methods did not abort, or
  noswissmap+methods aborted identically>. The OldMapType binding is therefore not the
  demonstrated cause of aether's EOF; the cause returns to UNKNOWN. The source fact at
  :146-148 (go1.25.0.json binds runtime.maptype to internal/abi.OldMapType) stands; the
  causal claim at :148-152 and the corollary at :161-164 are withdrawn. S032 remains a
  lead only. Evidence: `W18/runs/<label>/{receipt,compare}.json`; predictions frozen at
  <REV> before the runs.
- The status clause at :158-160 is superseded in scope: the round-18 replay is
  uninstrumented and did not reproduce the mechanism; the exact aether record remains
  unresolved.
```

### A2b. `…diagnostics.md:155-157` — the notesmd-cli contrast

Current: "notesmd-cli has no map types with method info, so it does not reach this path;
the 1.25.14→1.25.0 patch fallback is not the cause." This sentence is load-bearing in
both outcomes and must be narrowed explicitly (do not let the A2 erratum's
"cause withdrawn" language silently cover it).

CONFIRMED:

```text
- The notesmd-cli contrast at :155-157 is corroborated in kind: the round-18 nomethods
  controls do not abort, so method-carrying map types remain the exposure condition, and
  s1250-swiss-methods (built by exactly go1.25.0, so no fallback WARN is expected) isolates
  the layout from the patch fallback without notesmd-cli. notesmd-cli itself was not
  re-run; its 63 map types remain unexamined for a silent layout difference.
```

REFUTED:

```text
- The notesmd-cli contrast at :155-157 is narrowed to what the pair showed: <swiss+methods
  did not abort => method presence alone is not sufficient; noswissmap+methods aborted
  identically => method presence, not the Swiss layout, is the discriminator>. Either way
  the Swiss-layout reading of that contrast is withdrawn; the fallback is still not shown
  to be the cause, and notesmd-cli itself was not re-run.
```

### A3. `…diagnostics.md:161-164` — the corollary

Current: "the same binding would silently misread the size fields of every Swiss map
type in any 1.24/1.25 carrier (notesmd-cli has 63 map types) without a log line. 'No
error' in the table therefore does not mean that map types were laid out correctly."

CONFIRMED qualification (the silent half stays inference):

```text
- The corollary at :161-164 is replayed-confirmed only for failure-exposed Swiss map
  types: the swiss+methods carriers take the misread path. No log line exists for the
  nomethods carriers, so "silently misread every Swiss map type" remains an inference
  from the same binding, not an observation. "No error" still does not establish
  correct map-type layout.
```

REFUTED qualification (withdraw the mechanism, keep the caution):

```text
- The corollary at :161-164 is withdrawn on the round-18 pair: the binding did not
  produce the predicted misread, so map-type size fields must not be said to be misread
  on this mechanism. "No error" still does not establish correct layout, but that
  caution now rests on the absence of any map-type layout line, not on Swiss/OldMapType.
```

### A4. `…diagnostics.md:181-198` — `## Not examined` gains one bullet

Must be added in both outcomes; only the tail differs. Insert before the final bullet
(`:197-198`).

CONFIRMED:

```text
- The round-18 Swiss replay covers eight synthetic carriers plus the aether/notesmd-cli
  calibration only: it observes log-line outcomes, not the in-memory size-field reads
  (emulated from bytes and installed source), and it does not identify aether's
  invoking record.
```

REFUTED:

```text
- The round-18 Swiss replay covers eight synthetic carriers plus the aether/notesmd-cli
  calibration only; the negative result does not exclude another 1.24/1.25 layout
  condition or a carrier-specific cause, and aether's invoking record remains
  unidentified.
```

## B. Optional qualification (confirmed only; skipping harms no axis)

### B1. `SKILL.md:528` — **Means** cell

Current `Symbol markup aborted after bootstrap (aether 1.25.14; strings still recovered)`.
CONFIRMED may append `; replayed on the round-18 pair`. REFUTED: leave unchanged — the
observed abort is unaffected.

### B2. `SKILL.md:516-519` — closing guidance

Current: "Use it before attributing Go symbol loss to a layout change."
CONFIRMED may append: `Round 18 replays one 1.24/1.25 case on a synthetic pair: Swiss map types under the OldMapType layout, silent unless symbol markup fails.`
REFUTED may append: `Round 18 did not reproduce the 1.24/1.25 Swiss-map case; the caution still covers unobserved 1.26/1.27 layouts only.`
Neither edit is required: the sentence remains true in both outcomes.

### B3. `…diagnostics.md:134` — decision-table row (`Bootstrap OK …`)

Current Limit: `That the snapshot fallback caused it`. Add nothing in place; the A2
erratum may add one line: CONFIRMED `- Decision-table row :134 is corroborated: the fallback did not cause the abort; the layout did.` REFUTED: no change (the Limit stands, cause unresolved).

## C. Explicitly no edit

- `…diagnostics.md:108-115` (aether EOF observation) — an observation of the r17 run;
  the erratum may reference it, never rewrite it. No contradictory wording exists here.
- `…diagnostics.md:71` (`pro-aether` observations-table row) — "symbol markup then
  fails" is outcome-independent.
- `…diagnostics.md:1-3` (`source:`, `verified-at:`, `recheck:`) — provenance of the r17
  two-pass runs; a replay is a new entry, not a recheck of these fields.
- `…diagnostics.md:183-198` existing bullets — unchanged; A4 only inserts.
- `SKILL.md:511-512` source list — S032 stays a cited row in both outcomes.
- `SKILL.md:523-527` (INFO/WARN/Untested/Invalid/no-build-info rows) — unaffected: the
  replay exercises no new snapshot route.
- `SKILL.md:530-533` capture/binding recipe — unchanged; W18 reuses it.
- `SKILL.md:537-546` registry rows — C3 adds `swiss-misread.py`, W18 `run-carriers.sh`
  and new `log-extract.py` fields regardless of outcome. That is an outcome-independent
  registry addition, not a conditional update; do not let it wash out the status edit
  at :528.

## D. Cross-claim / propagation list (outside my two files; not mine to edit)

- `SCORECARD.md:2363` (r17 row) says `aether's post-bootstrap EOF is a labelled
  INFERENCE, not replayed`. SCORECARD is old-prefix under `contract.md:142-143`; do not
  rewrite. A new round-18 row must carry `replayed-confirmed` or `replayed-refuted`;
  otherwise the two rows contradict.
- `SCORECARD.md:2422-2424` `Planned:` names this replay as option (a). It is delivered
  (either outcome); point the new row at it, leave the old line as filed.
- `corpus/README.md:35` "aether's post-bootstrap symbol-markup EOF was unpredicted" —
  still true of the r17 run; MAY add the replay pointer.
- `corpus/SOURCES.md:38` S032 (`tier B`) and `:44` route chain — INFERENCE: C1 adds an
  S033 row that "supersedes S032" (`claims.json` C1 `sourced`; routed defect
  R17-S032-DIGEST requires a `supersedes S032 —` teaches cell with a `fetch-time`
  anchor). If S033 is the surviving row when C3 lands, the A2 erratum and `SKILL:528`
  should cite S033 (noting S032 superseded), or the section will point at a superseded
  source. Verify against C1's SOURCES diff; do not assume S033's content.
- `LOG.md` — new round-18 account only; no r17 edit. `PROVINCE.md` has no
  aether/Swiss/OldMapType text (`grep`, no matches), so nothing to qualify there.

## Calibration notes and remaining unknowns

- The corollary is `:161-164`, not `:161-166` as the ticket states: `:165` begins
  `- INFERENCE, version strings:`. Wording must not swallow that bullet.
- Confirmation confirms a **failure path**, not the silent corollary: no Ghidra log
  line reports map-type layout, so A3's "silent" half stays INFERENCE even on success.
- Depth note for the confirmed wording: `s1250-swiss-methods` is built by go1.25.0, so
  no `Falling back` WARN is expected; a failure there isolates the layout from the patch
  fallback more cleanly than aether (which did fall back) or notesmd-cli (unreplayed).
- Refutation falsifies the **causal link**, not the source fact: `go1.25.0.json`
  binding `runtime.maptype` to `internal/abi.OldMapType` is a filed source read
  (`:146-148`); keep it.
- aether's "exact invoking record is unresolved" (`:159-160`) survives confirmation;
  a synthetic carrier's log cannot identify aether's record.
- Append-only placement: r17 knowledge = appended erratum naming exact `file:line`
  (QUALITY #19); SKILL.md = live index, in-place cell edit with deleted lines listed
  (`contract.md:142-145`).
- UNKNOWN: round-18 `predictions/carriers.tsv`, `tools/` and `runs/` do not exist yet,
  so the actual carrier labels/JSON selection could not be checked; whether 1.24.6
  selects a patch diff or base affects the fallback narrative but not the layout
  controls. No REA or Go toolchain inspection was run, per lane contract.

Report: `.ufo/waves/round-18/w1/ScoutSkillGoSection.md`
