# QuoteCriterionDraft — C2 QUALITY criterion proposal (round 14, w1)

Seat: KaidokuR14.QuoteCriterionDraft (executor, leaf) · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Access window (source opens): 2026-10-20T05:14Z–05:19Z. Status: author-side draft, **not integrated, not gate output, no tests run**.
This seat is author-side and cannot supply non-author admission; L1 owns integration and the post-integration run.

## Sources opened

| id | location | exact quote and location | access | limit |
|---|---|---|---|---|
| L1 | `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kaidoku-r13-review.md` | “The printed “quote” is the section prefix combined with the CLI bullet’s tail, swapping names/identifiers” — DEFECT-1, line 101. Also “appears once, at page line 87 under `# Introduction` (heading L77).” — DEFECT-2, line 104. | 2026-10-20 | Non-author review of round 13; read-only; its line numbers refer to its own rendering. |
| L2 | `corpus/lessons/round-13.md` | “Replace address-derived function identifiers with deterministic names based on parse order.” — `Post-review citation-fidelity errata`, S017 bullet. Also “line 87 (heading at line 77), not `Decompiled output`.” — S018 bullet; “no extra QUALITY criterion was added.” — final errata paragraph. | 2026-10-20 | Append-only lesson record, not the source itself; the S018 line numbers are not reproducible from the captured bytes (see F3). |
| L3 | `corpus/lessons/round-13-verifier-spotcheck.md` | “Review found S017's spliced quotation and S018's mislocated exact quote.” — `## Gate`, line 13. | 2026-10-20 | Adjudication summary; it samples two decisions, not the whole registry. |
| L4 | `/home/vgpnk/Projects/shokunin/CORPUS.md` | “A quote names its location.” — line 42; “a ≤25-word quote with its location grounding `teaches`” — Contract v1 rule 1. | 2026-10-20 | Fleet-level contract; kaidoku-local admission remains `corpus/QUALITY.md`. |
| L5 | `corpus/QUALITY.md` | “every criterion cites the lesson that produced it.” — line 4; the append-only row rule is “A criterion is replaced by a new row” immediately before it. | 2026-10-20 | Rows 1–15 only; `grep -c quote-fidelity corpus/QUALITY.md` = 0 at draft time. |
| L6 | `SKILL.md` | “Local round-evidence gate registry” — section heading, line 438; “0 clean, 1 failed, 2 could-not-evaluate” — registry entry format. | 2026-10-20 | Format reference only; no quote gate is registered yet. |
| L7 | `.ufo/waves/round-14/claims.json` | “quote-location fidelity gate plus grounded QUALITY criterion rejecting S017 splice and S018 mislocation while admitting corrected contiguous located quotes” — C2 `observable` (19 words); “local captured source excerpts only; no whole-registry or semantic truth assertion” — C2 `limits` (11 words). | 2026-10-20 | Plan, not a measured result. |
| L8 | `.ufo/waves/round-14/measure.py` | `C2_grounded_quality_criteria` is computed as `int("quote-fidelity" in get("corpus/QUALITY.md"))` — verified source line. | 2026-10-20 | Counts a literal token and the tool path; it does not verify gate semantics. |
| E1 | `.ufo/waves/round-14/w1/s018-raw.html` (local capture; a fresh `/tmp` copy was byte-identical and was removed after hashing) | “The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.” — line 489, 19 words, inside `Introduction` (`<h1>` line 469; next `<h1>` line 497). | 2026-10-20 | 355,603 bytes, SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e`; fresh HTTP 200 fetch today is byte-identical. Authenticates today's capture only, not round 13's bytes. |
| E2 | `https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md` | “Replace address-derived function identifiers with deterministic names based on parse order.” — raw line 40, 11 words, inside `<h3>Command-Line Arguments</h3>` (line 20). | 2026-10-20 | 13,242 bytes, SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b`; HTTP 200. File has **zero** Markdown `#` headings; all headings are HTML `<h1>`–`<h3>`. |

Peer drafts `w1/ReviewS017.md`, `w1/ReviewS018.md` and `w1/ReviewS017-source/` were read as data. Their S017 byte claim (same SHA-256) and S018 heading/line claims agree with my independent re-derivation below; nothing in this report rests on them alone.

## Findings

**F1 — The two r13 defects are different verdict classes; the criterion must keep them distinct.**
The S017 splice is absent as contiguous bytes from the whole pinned README (occurrence count 0). The S018 sentence is present exactly once (line 489) but outside the section the r13 Gate named. Collapsing both into one code would erase the distinction the non-author review drew: spliced text versus real text at the wrong location. The proposal therefore requires `quote_not_contiguous` for absence and `quote_location_mismatch` for “present only elsewhere”, matching the C2 interface's two distinct exit-1 codes. If the eventual gate only searches the named section, both cases return the same code and the criterion's location claim is false; L1 must confirm the whole-excerpt search with the frozen red cases.

**F2 — S017 splice verified against pinned bytes.**
The r13 Gate sentence (14 words) occurs 0 times in the 13,242-byte pinned README. Its opening “to replace address-derived function names with deterministic” occurs at line 82 in the `Deterministic Function Names and Mapping CSV` section, after the `--normalize` code span; its tail “names based on parse order.” occurs at line 40 in the `Command-Line Arguments` row. The splice joins the middle of one sentence to the tail of another, swapping the section's “identifiers” for the CLI row's “names”. The corrected 11-word sentence occurs once, at line 40, inside `<h3>Command-Line Arguments</h3>`; it does **not** occur in the section the r13 Gate named (lines 81–107). So the red-before case is `quote_not_contiguous`, the corrected-but-wrong-section case is `quote_location_mismatch`, and the corrected green case needs the `Command-Line Arguments` heading.

**F3 — S018 mislocation verified, and the line-number locator fails.**
The 19-word sentence occurs once, line 489, inside `Introduction` (heading line 469; next `<h1>` at 497). The `Decompiled output` heading is at line 625 and the section spans 625–706; the sentence does not occur there. The r13 errata's “line 87 (heading at line 77)” is not reproducible from the captured bytes (offset 20, not 10), so a rendered line number cannot be the key. The heading is the stable locator. Today's fresh fetch is byte-identical to the local capture, which strengthens this session's evidence but does not retroactively authenticate the round-13 capture.

**F4 — Excerpt capture is not source authenticity.**
Both named sources defeat a naive “pin the upstream file” reading: the View8 README is HTML-in-`.md` with no Markdown headings, and the Check Point article is HTML. A gate whose section grammar is “exact Markdown heading including `#`” therefore cannot admit either green case against raw bytes. The honest unit is a locally captured, disclosed conversion whose SHA-256 pins the converted excerpt. That is what the proposed criterion certifies, and it explicitly refuses to certify upstream byte identity, completeness or currency. This is the central calibration boundary of C2, not a footnote.

**F5 — Criterion drafted.**
`.ufo/waves/round-14/w1/QuoteCriterionDraft.candidate.md` contains one ready-to-paste row (number 16, `sharpens 1`), the exact pass/refusal semantics, six expected cases (five quote cases, one refusal case), integration notes and residual limits. It names the registered `quote-fidelity` gate, includes the literal token the round-14 measurement reads, and is scoped to Gate-evidence quotes from heading-structured documents; other quotes are explicitly outside it. It does not supersede any existing row; rows 1–15 are untouched.

**F6 — Measurement coupling, not measurement.**
`before.json` records `C2_grounded_quality_criteria: 0` and `C2_quote_gate_instruments: 0`. `measure.py` will flip the first on the literal token `quote-fidelity` in `corpus/QUALITY.md` and the second on the tool path; neither checks that the gate distinguishes the two defects. The criterion supplies the missing semantic bar, but only L1's post-integration run can produce a measured C2 result. Nothing here claims that run.

**F7 — Why a new criterion is warranted, and why its scope must be the Gate surface.**
CORPUS rule 1 and QUALITY #1 already require a located, ≤25-word quote, but both are prose. The r13 errata records the consequence: “no extra QUALITY criterion was added.” The two defects passed author-side and were caught only on non-author re-open. Making the same obligation mechanically checkable at author time is the new, falsifiable element; #1 remains broader. The scope needs two bounds: the Gate-evidence surface (so C1's knowledge-entry quotes, including its GoReSym sentence at `Version Support`, stay under #1) and heading-structured sources (so Gate quotes from S003's Java members, S015's JSON fields or commit objects, which have no document section, are not forced into a section gate). Bounded that way, the criterion covers exactly the surface where the r13 defects lived.

**F8 — Peer attack incorporated before hand-off.**
`KaidokuR14.AttackNoHarm` flagged two defects in the first draft, both confirmed against the files and fixed: (a) the row's why-cell cited `.ufo/waves/kaika-w3/kaidoku-r13-review.md`, which does not resolve in-lane; it now cites lane-resident `corpus/lessons/round-13-verifier-spotcheck.md` and `corpus/lessons/round-13.md`, with the absolute out-of-lane review path stated separately; (b) the unconditional “quote-bearing claim” scope would have made C1's quotes inadmissible under C2's own row; the row is now bounded by surface (Gate evidence) and source type (heading-structured document), which leaves C1's knowledge entry and the code/JSON Gate quotes untouched. The S017/S018 red-before and green expectations are unchanged by both fixes. The critic's `corpus/QUALITY.md:26` append line-safety note is passed to L1 as the critic's claim, not re-verified here.

## Expected red/green mapping — derived from bytes, not gate output

`quote-fidelity.py` did not exist at draft time (`.ufo/waves/round-14/tools/` absent), and this seat ran no gate, no `--selftest`, no fixture and no build.

| case | excerpt | quote | section | expected |
|---|---|---|---|---|
| S017 splice | E2 raw or converted | r13 14-word splice | `### Deterministic Function Names and Mapping CSV` | exit 1 `quote_not_contiguous` |
| S017 corrected, wrong section | E2 | corrected 11-word sentence | `### Deterministic Function Names and Mapping CSV` | exit 1 `quote_location_mismatch` |
| S017 corrected, located | E2 converted (disclosed) | corrected 11-word sentence | `### Command-Line Arguments` | exit 0 clean |
| S018 original anchor | E1 converted (disclosed) | 19-word sentence | `# Decompiled output` | exit 1 `quote_location_mismatch` |
| S018 corrected | E1 converted (disclosed) | 19-word sentence | `# Introduction` | exit 0 clean |
| digest drift | any | any | any | exit 2 `source_tampered`, never clean |

The green cases are conditional on a converted excerpt; the red cases are stable under HTML-tag stripping because the splice still lacks “names based on parse order.” S018's red case is stable because the sentence is absent from the claimed span regardless of conversion.

## Risks

- **Quote-mining survives.** A real, contiguous, correctly located sentence can still be used to support more than it says; the gate does not read meaning. Non-author semantic review remains necessary.
- **Duplicate headings.** If the manifest's heading line occurs twice, the locator names two spans. The proposal makes such an excerpt inadmissible until disambiguated; the gate's verdict mapping for that case is unverified.
- **Conversion reproducibility.** The digest authenticates the excerpt artifact, not the converter or its version. A future re-conversion may differ; the fixture report must name the route.
- **Implementation mismatch.** The gate could classify absence and mislocation identically, or match sections by bare heading text. Either would satisfy a naive reading of the interface but fail F1/F4. The frozen red cases are the check.
- **Attribution assumption.** Per-entry admission needs the finding to carry the quote's manifest `id`; a run-level-only failure leaves the entry unevaluable and inadmissible, not clean. The interface's `quotes[].id` suggests attribution is available, but the implementation is unverified.
- **Upstream drift.** Today's S018 fetch returned 200 and matched; a future WAF or edit is unavailability or a different version, never disproof of the r13 finding.

## Blockers / decisions for L1

1. **Heading grammar vs converted excerpt.** The contract's Markdown-`#` section rule cannot address the raw View8 README or raw article. Decide: disclose a converted Markdown fixture (digest pins converted bytes, recommended by the proposed criterion) or extend the gate to HTML headings. The green S017/S018 cases are blocked until this is decided.
2. **Keep the literal `quote-fidelity` token** in the pasted QUALITY row; otherwise `measure.py` reports no C2 criterion even if the row exists.
3. **Freeze manifests + `expected.json`** with every excerpt digest and per-case expected exit/finding ID, register the gate in the SKILL registry with `--selftest`, then run once post-integration. The expected table here is a hypothesis, not a measured verdict.
4. **Registry anchors** for S017/S018 need no superseder for this criterion; whether S018 gains `Introduction` is a separate registry decision (ReviewS018 F4), outside this seat.
5. **Preserve both scope clauses and stage the row inside the Admission criteria table.** Dropping "Gate evidence" pulls knowledge-entry quotes (C1's GoReSym `Version Support` sentence) into a gate they have no manifest for; dropping "heading-structured document" pulls code/JSON Gate quotes (S003's `GoRttiMapper.java:79`, S015's fields) into a section gate they cannot satisfy. Peer critic `KaidokuR14.AttackNoHarm` reports an append at `corpus/QUALITY.md:26` is line-safe; that line-safety claim is theirs, not re-verified here.
6. **Land row 16, `corpus/lessons/round-14.md`, the gate and its SKILL registry row together.** The why-cell cites the lesson by path; a row committed before the lesson exists is a dangling citation, not a promise. The critic's re-read confirms this is the only remaining integration dependency.

## Files written

- `.ufo/waves/round-14/w1/QuoteCriterionDraft.candidate.md` — proposed row + cases + limits.
- `.ufo/waves/round-14/w1/QuoteCriterionDraft.md` — this report.

No shared file, registry, lesson, SKILL, LOG, SCORECARD, MANIFEST or sibling file was edited. No live artifact or target was touched.

## Tooling

No installs or upgrades. Used pre-existing `curl` (two source fetches), `python3` (byte checks, SHA-256, section spans), `sha256sum`, `grep`, `date`. Gate code was neither present nor run; no client config or REA session was used.

## Retained evidence

- E2 SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b` (13,242 bytes); splice count 0, corrected sentence count 1 at line 40.
- E1 SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e` (355,603 bytes); quote count 1 at line 489; `Introduction` 469–496 contains it, `Decompiled output` 625–706 does not.
- Word counts: splice 14, corrected S017 11, S018 19 — all within the 25-word cap, so the cap is not the detector; contiguity and location are.
- Baseline: `before.json` `C2_grounded_quality_criteria=0`, `C2_quote_gate_instruments=0`, `sources_rows=22`.
