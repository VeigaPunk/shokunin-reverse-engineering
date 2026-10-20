# Candidate QUALITY admission criterion — `quote-fidelity` (round 14, C2)

Seat: KaidokuR14.QuoteCriterionDraft · 2026-10-20 · proposal only.
Status: **not integrated**. `corpus/QUALITY.md`, `SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md` and `corpus/lessons/` are untouched by this seat; L1 owns the append and the gate registration.

Evidence base: prior non-author review at the out-of-lane path `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kaidoku-r13-review.md` (DEFECT-1 S017 splice, DEFECT-2 S018 mislocation), summarized lane-side in `corpus/lessons/round-13-verifier-spotcheck.md`; append-only corrections in `corpus/lessons/round-13.md`; the round-14 lesson is **planned** at `corpus/lessons/round-14.md` and does not exist at draft time (0 files match `round-14` in `corpus/lessons/`).

## Proposed row (append to `corpus/QUALITY.md` → Admission criteria)

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 16 | A source quote offered as Gate evidence (a `corpus/SOURCES.md` row's lesson Gate entry or a lesson `## Gate` table) from a heading-structured document — Markdown, or HTML captured as a disclosed Markdown excerpt — is admitted only when the registered `quote-fidelity` gate reports no finding for that quote's entry in a frozen manifest: the quote's exact bytes must occur contiguously in a SHA-256-pinned local excerpt, inside the span of exactly one section whose heading line matches the manifest byte-for-byte, at ≤25 whitespace words, with no inserted ellipsis, bracket, splice, tag-stripping, case-folding, or whitespace/Unicode normalization. A clean run exits 0. Findings reject the entry: `quote_not_contiguous` (bytes absent from the excerpt), `quote_location_mismatch` (bytes occur only outside the named section), `quote_too_long`. Exit 2 (`source_tampered`, `invalid_manifest`) is could-not-evaluate for every entry, never clean. Gate quotes from code members, commit objects, JSON records or command output — where no document section exists — and all knowledge-entry quotes are outside this criterion and remain under #1 and their evidence rules; the gate neither admits nor rejects them. The pass is excerpt-bounded: it never certifies the excerpt's completeness, upstream byte identity, currency, or that the passage supports `teaches`; rendered line numbers are never a locator. | r13 non-author review defects (S017 splice, S018 `Decompiled output` mislocation) as recorded in `corpus/lessons/round-13-verifier-spotcheck.md` and corrected in `corpus/lessons/round-13.md`; the review itself is `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kaidoku-r13-review.md`; r14 lesson (planned, `corpus/lessons/round-14.md`) records the gate and its frozen run | sharpens 1 |

The literal token `quote-fidelity` is required in the pasted row: `.ufo/waves/round-14/measure.py` computes `C2_grounded_quality_criteria` as `int("quote-fidelity" in get("corpus/QUALITY.md"))`.

## What the pass certifies — and what it must not

Admitted by exit 0:

- The claim is a source quote offered as Gate evidence (a `corpus/SOURCES.md` row's lesson Gate entry or a lesson `## Gate` table) from a heading-structured document. Gate quotes from code members, commit objects, JSON records and command output, plus all knowledge-entry quotes, are outside this criterion; the gate neither admits nor rejects them and #1 continues to govern them.
- The quoted bytes exist as one contiguous substring of the pinned excerpt.
- The substring lies inside the span that starts at the named heading line and ends before the next heading of the same or higher level.
- The named heading line occurs exactly once in the excerpt.
- The quote is at most 25 whitespace-separated words.

**Not** admitted by exit 0, and not to be written into a lesson or registry row as if it were:

- That the excerpt is the complete upstream document, or that its bytes equal the upstream bytes, or that it is current. A converted excerpt (for example HTML-to-Markdown) is a different byte object; the digest pins the converted excerpt only.
- That the source is correct, or that the passage semantically supports `teaches`. The gate locates bytes; it does not adjudicate meaning, and it does not detect a real quote used to support a claim it does not support.
- That any other entry is clean. Admission is per entry: a finding on a sibling entry neither launders nor poisons this one, and a clean run over this entry says nothing about the registry as a whole.
- That a line number is a location. Rendered line numbers shift with capture and conversion; the heading is the key.

Exit 2 is a refusal to grade: a digest mismatch (`source_tampered`) or a malformed manifest (`invalid_manifest`) must never be reported as clean.

## Red-before and green cases

Expected verdicts below are derived from exact-byte inspection of the pinned objects, using the C2 interface's finding codes. They are **not gate output**: `quote-fidelity.py` was absent at draft time (`.ufo/waves/round-14/tools/` did not exist), and this seat ran no gate, no selftest and no fixture.

| case | pinned excerpt | quote | section | expected |
|---|---|---|---|---|
| `S017-R13-SPLICE` (red-before) | View8 pinned README, 13,242 bytes, SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b` | r13 Gate sentence, 14 words: “Use --normalize to replace address-derived function names with deterministic names based on parse order.” | `### Deterministic Function Names and Mapping CSV` | exit 1, `quote_not_contiguous` — occurrence count in the excerpt is 0 |
| `S017-CORR-WRONG-SECTION` (red) | same | corrected sentence, 11 words: “Replace address-derived function identifiers with deterministic names based on parse order.” | `### Deterministic Function Names and Mapping CSV` | exit 1, `quote_location_mismatch` — present once at raw line 40, outside that span |
| `S017-CORR-LOCATED` (green) | converted Markdown excerpt of the same README (disclosed conversion, digest pins converted bytes) | same 11-word sentence | `### Command-Line Arguments` | exit 0 clean |
| `S018-R13-MISLOCATION` (red-before) | Check Point capture, 355,603 bytes, SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e` | “The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.”, 19 words | `# Decompiled output` | exit 1, `quote_location_mismatch` — absent from lines 625–706; present once at line 489 |
| `S018-CORR-LOCATED` (green) | converted Markdown excerpt of the same capture | same 19-word sentence | `# Introduction` | exit 0 clean |
| `DIGEST-DRIFT` (could-not-evaluate) | any excerpt whose bytes differ from its manifest SHA-256 | any | any | exit 2, `source_tampered`, never clean |

Notes that keep these cases honest:

- The pinned View8 README has **zero** Markdown `#` headings (all headings are `<h1>`–`<h3>`); the Check Point capture is HTML. Both green cases therefore need a disclosed, digest-pinned Markdown excerpt produced by the fixture owner. A green case must not be claimed against the raw bytes under a Markdown-heading contract.
- In the View8 excerpt the corrected sentence sits at raw line 40 inside `<h3>Command-Line Arguments</h3>` (line 20) and before `<h3>Basic Usage</h3>` (line 66). The r13 Gate cited the `Deterministic Function Names and Mapping CSV` section (line 81), whose own sentence reads (tag-stripped) “Use --normalize to replace address-derived function names with deterministic identifiers.” — the splice's first half.
- In the Check Point capture the quote occurs once, at line 489, inside `<h1>Introduction</h1>` (line 469; next `<h1>` `Distributed payloads` at line 497). The `Decompiled output` heading is at line 625; the quote does not occur in that section.
- The r13 errata's “line 87 (heading at line 77)” is not reproducible from the captured bytes (heading line 469, quote line 489; offset 20, not 10). This is why the criterion bans line numbers as locators rather than pinning a rendering.

## Why this is a new criterion, not a restatement

- `CORPUS.md` rule 1 already requires “a ≤25-word quote with its location grounding `teaches`”, and QUALITY #1 requires a resolvable source. Both are prose: they state the obligation but supply no executable test, so the r13 splice and mislocation passed author-side and were caught only on non-author re-open.
- The r13 lesson records exactly that gap: its errata says the existing CORPUS/SOURCES rule caught both defects and “no extra QUALITY criterion was added.” C2 adds the missing mechanical test, so the obligation becomes falsifiable at author time.
- It does not replace #1 (any resolvable source remains admissible under #1); it sharpens #1 for Gate-evidence quotes only. No existing row is superseded.
- It deliberately does not bind quotes outside the Gate-evidence surface (knowledge entries) or from sources without document sections (code members, commit objects, JSON records, command output). Binding by locator alone would still have collided with C1's knowledge-entry GoReSym quote at `Version Support`; binding only Gate-evidence quotes from heading-structured documents leaves C1 and similar entries under #1, where they already sit.

## Integration notes for L1

1. Append one row numbered 16; keep the token `quote-fidelity` (measurement dependency above). Do not rewrite rows 1–15.
2. Register the gate in the SKILL “Local round-evidence gate registry” with the 0 clean / 1 failed / 2 could-not-evaluate map, the `--selftest` entry, and an `expected.json` that pins every excerpt digest plus expected exit and stable finding ID per case. The registry row must state that `source_tampered` and `invalid_manifest` are refusals, not findings.
3. Freeze the manifests for the two original defects, the S017 wrong-section case and the two corrected quotes, with their digests; then run the gate once after integration and record the actual output. The expected table above is a hypothesis until that run; do not present it as measured.
4. Record in the r14 lesson that a green `S017`/`S018` case depends on a disclosed converted excerpt, and that the raw upstream bytes are not the gate input. The registry rows for S017/S018 need no superseder for this criterion; whether S018's anchor gains `Introduction` is a separate registry decision.
5. Do not extend the claim to whole-registry fidelity or semantic truth. The C2 limit is stated in `claims.json`: local captured excerpts only.

## Residual limits

- A contiguous, correctly located quote can still misrepresent its source; that stays a non-author semantic judgment (QUALITY #2 and the non-author review).
- A heading that repeats in an excerpt makes the locator ambiguous; such an excerpt is inadmissible until the heading or excerpt is disambiguated. The gate's verdict mapping for duplicates is unverified here.
- A quote equal to a heading line, or a very short common phrase, can pass the locator test. The criterion adds no arbitrary minimum length; semantic sufficiency remains outside the gate.
- Attribution is assumed. Per-entry admission needs the finding to carry the quote's manifest `id`. If a run reports only a global failure, the entry cannot be called clean and is inadmissible until the gate names it; no pass is inferred from a run-level exit alone.
- Conversion provenance (tool, version, command) is not authenticated by the digest; it must be disclosed in the fixture report. The digest authenticates the excerpt artifact, not the pipeline that produced it.
