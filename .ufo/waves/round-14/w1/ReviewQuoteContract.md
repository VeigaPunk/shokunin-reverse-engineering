# ReviewQuoteContract — C2 quote-location gate interface review (round 14, w1)

Seat: KaidokuR14.ReviewQuoteContract (leaf, source-only). Access date: 2026-10-20.
Scope: review the C2 interface text (manifest shape, verdict IDs, exit codes, tamper handling) for ambiguity, absent sections, substring boundaries, location-vs-contiguous distinction, and tamper handling. Inspect round-13 quote failures. No code or test edits. No REA, no target execution, no builds, tests, or linters.
Tools: none installed or upgraded. Read-only Python used only for substring, count, and heading checks on captured bytes.

## Inputs and limits

- The candidate `tools/quote-fidelity.py` is **absent** at review time (`.ufo/waves/round-14/tools/` does not exist). This review covers the interface as written in the assignment text only. Nothing here verifies gate code.
- Sources opened, with location:
  - `.ufo/waves/round-14/claims.json` (C2 observable and limits).
  - `corpus/lessons/round-13.md#ECC4` rows S017 and S018 and the post-review errata (lines 61–67).
  - `corpus/lessons/round-13-verifier-spotcheck.md#99C6`.
  - `corpus/SOURCES.md#E27D` rows S017 (line 23) and S018 (line 24).
  - `.ufo/waves/round-14/w1/ReviewS018.md` (sibling capture report; not independently trusted, cross-checked below).
  - `.ufo/waves/round-14/w1/s018-raw.html`, sha256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e`, 4,569 lines.
  - `.ufo/waves/round-14/w1/ReviewS017-source/View8-README-ef39099b4f5076042173f9113382ebeb0630a56d.md`, sha256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b`, 283 lines.
  - `~/.omp/agent/RULES.md#6A50` (tool policy, no tools needed).
- Quotes from those captures (each ≤25 words, contiguous):
  - S017 capture line 40: "Replace address-derived function identifiers with deterministic names based on parse order." (11 words, location: `<h2>Usage</h2>` line 18 → `<h3>Command-Line Arguments</h3>` line 20 → `--normalize` list item; next heading `<h3>Basic Usage</h3>` line 66.)
  - S018 raw line 489: "The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode." (19 words; `<h1>Introduction</h1>` line 469, next `<h1>Distributed payloads</h1>` line 497.)
  - Original round-13 S017 Gate quote (absent from capture): "Use --normalize to replace address-derived function names with deterministic names based on parse order." (14 words.)
- Access date for the captures is 2026-10-20 per ReviewS018. The S018 article modified date (2026-09-24, per ReviewS018) is later than the round-13 open; no claim that round 13 read identical bytes.

## Facts checked (source-only)

| Check | Result |
|---|---|
| S017 original splice present in capture | No (`in` = False) |
| S017 corrected quote present in capture | Yes, exactly once, line 40, 11 words |
| S017 corrected quote heading chain | `Usage` (h2) → `Command-Line Arguments` (h3); the section ends at the next h3 `Basic Usage` (line 66) |
| S017 heading texts duplicated | None (17 headings, no duplicate text) |
| S017 substring hazard | Heading text `Usage` matches within `Basic Usage` (line 66) under a naive substring match |
| S018 quote present in raw capture | Yes, exactly once, line 489, 19 whitespace tokens (em dash counted) |
| S018 `Introduction` h1 count | 1 (line 469) |
| S018 `Decompiled output` h1 count | 1 (line 625); the quote is not in that span (625–706) |
| S018 duplicate heading texts | None (56 headings) |
| Captures' byte form | Both are **HTML** (`<h1 class="wp-block-heading">`, `<h3>`, `<li>`, `<code>`), not Markdown. Neither contains a `#`-prefixed heading. |
| CR / BOM in S017 capture | 0 CR bytes, no BOM |

## Findings (severity order)

### QR-1 (high) — Verdict boundary between quote_not_contiguous and quote_location_mismatch is not defined

The interface says the quote "must be contiguous inside that section" and names two failure IDs. Read literally, any quote outside the declared section would be "not contiguous inside that section", which makes `quote_location_mismatch` unreachable.

Round-13 evidence separates the two cases:
- S017 original splice: absent from the entire source (checked, False). It must map to `quote_not_contiguous`.
- S018 `Decompiled output` anchor: the quote exists in the source (line 489) but outside the declared section. It must map to `quote_location_mismatch`.

Minimal correction: state the order explicitly. (a) Not a byte substring of the whole source → `quote_not_contiguous`. (b) Present in source but zero occurrences inside the declared section span → `quote_location_mismatch`. (c) Pass requires at least one occurrence inside the declared span. Add one selftest fixture per branch, pinned by exit and finding ID.

### QR-2 (high) — Absent sections and same-text headings are unspecified; substring matching would mis-bind

- Absent heading: the interface gives no verdict. Recommend `quote_location_mismatch` (exit 1). The citation points at a location the source does not have. Treating it as tamper or manifest error would overstate what is known.
- Ambiguous heading (same exact key occurring more than once): the manifest cannot name one location. Recommend `invalid_manifest` (exit 2), reason `section_ambiguous`, evaluated before any quote verdict. Current captures have no duplicate texts, so this is a guard, not a present defect.
- Substring boundary: a heading key must match a whole heading line (level marker, one space, exact text, trailing whitespace stripped). Evidence: in the S017 capture, `Usage` appears as a substring of `Basic Usage` (line 66). A substring-based section lookup would bind a `Usage` key to the wrong section. A fixture should pin this case.

### QR-3 (high) — Section span needs explicit heading-level and code-fence rules

"Until next same/higher heading" needs two rules the interface omits:
- Level is the count of leading `#` (or `<hN>`-equivalent if HTML is ever accepted), and the span ends at the next heading with level less than or equal to the key's level. Deeper headings stay inside the span.
- Lines inside fenced code blocks are not headings. A naive `#`-line scan would end a span early or create false headings. The captures contain 0 fence markers but 22 and 109 `<pre>` blocks respectively, so HTML-side fence handling is also undefined.

Minimal correction: fence-aware heading scan; add one fixture with a `# comment` line inside a fence that must not end a span.

### QR-4 (high) — The interface assumes Markdown excerpts; both available captures are HTML

The interface says "Source UTF-8 Markdown excerpt exact bytes; section is exact Markdown heading text including #". The available captures do not match that form:
- The S017 capture contains `<h3>Command-Line Arguments</h3>`, not `### Command-Line Arguments`. A manifest with the Markdown key would fail as `quote_location_mismatch` even though the quote is correctly located. A false failure against the corrected quote.
- The S018 capture contains `<h1 class="wp-block-heading">Introduction</h1>`, not `# Introduction`. Same false failure for the corrected S018 location.
- The round-13 line numbers (heading 77, quote 87) come from a different rendering. ReviewS018 F3 reproduces offset 20 in the raw bytes (469 / 489), not offset 10. Line numbers must not be gate keys.

Consequence for calibration: C2 can be green only on a Markdown excerpt whose conversion is itself unverified. The gate proves consistency of that excerpt with its manifest, not fidelity to the live page. The claim-level limit "local captured source excerpts only" should say the excerpt must be a pinned Markdown conversion, with its conversion recorded, and that the source's native byte form is HTML.

Minimal correction: the fixture producer pins a Markdown excerpt (sha256 in the manifest) and records how it was produced. Line numbers are informational only. The gate does not parse HTML.

### QR-5 (medium) — Substring and token rules are unstated

- Normalization: the interface implies exact bytes. State it: no whitespace, quote, or Unicode normalization. An em dash (U+2014) in the S018 quote must match byte-for-byte.
- Word boundary: a truncated token (for example `pseudocod` inside `pseudocode`) would pass a bare substring check. Recommend: if the quote's first character is a word character, the preceding character must be a non-word character or start-of-section; the same at the end. The S018 and S017-corrected quotes both satisfy this.
- Word count: "≤25 whitespace words" must be `len(quote.split())`. Under that rule the S018 quote counts as 19 because the standalone em dash is a token. State it, so an implementation that strips punctuation does not change verdicts.
- Empty quote, leading or trailing whitespace in the quote, or a quote containing a line break: `invalid_manifest`.
- Multiple occurrences inside the span: pass, recording the count. Say so; do not leave it to the implementer.

### QR-6 (medium) — Tamper and could-not-evaluate paths have gaps

- Missing source file: no verdict defined. Recommend `invalid_manifest` (exit 2) with reason `source_missing`. Do not reuse `source_tampered`, since absence is not proven modification.
- Undecodable bytes (not strict UTF-8): undefined. Recommend `invalid_manifest` (exit 2), decided before digest comparison only if the digest is computed on raw bytes. Keep the digest over raw bytes so CRLF or BOM changes show up as `source_tampered`, not silently normalized.
- Path handling: absolute paths and `..` escapes (including symlinks resolving outside the manifest directory) are not rejected. Recommend `invalid_manifest`. The gate is read-only, but a manifest should not read arbitrary files.
- Digest format: a non-64-char or non-lowercase-hex digest is `invalid_manifest`, not `source_tampered`.
- Trust anchor: the manifest's own digests are self-asserted. A rewritten source plus a rewritten manifest passes. The gate can only prove self-consistency; the independent anchor is L1's frozen expected verdict with digest pins, plus the registry. State this in the SKILL pointer so no one reads a green run as source authenticity. This is the same limit `claims.json` already states; keep it visible at the interface.
- Precedence: any exit-2 condition (`source_tampered` or `invalid_manifest`) must take precedence over exit-1 quote failures. Pin it: exit 2, and no quote verdict reported as clean.

### QR-7 (medium) — Registry anchors still point at the S017 splice section

`corpus/SOURCES.md` S017 row names the anchors `Requirements`, `Deterministic Function Names and Mapping CSV`, and the pickle warning. The corrected quote sits under `Usage` → `Command-Line Arguments`, which the row does not name. The gate does not read registry anchors, so it cannot flag this. This is the same class as ReviewS018 F4 for S018 (whose row omits `Introduction`).

Recommendation for L1 (not edited here): decide whether registry anchors are in gate scope. If not, state that the gate checks only manifest-declared locations. If yes, add a registry-to-manifest consistency check as a separate claim, not folded into C2.

### QR-8 (low) — Finding structure and precedence are unpinned

The interface does not say whether a quote yields one finding or several, in what order, or which check runs first when several apply. Recommend:
- one finding per quote, first failing check only, in this order: `quote_too_long` (count > 25) → `quote_not_contiguous` → `quote_location_mismatch`;
- output sorted by quote ID;
- duplicate source IDs, duplicate quote IDs, and unknown `source` references are `invalid_manifest`.

Note for QR-8 ordering: the 25-word cap does not catch the round-13 splice. The original S017 quote is 14 words and passes the cap. Only the whole-source substring check (QR-1 branch a) catches it. The selftest must include the splice as a case.

## Proposed minimal correction (interface text, not code)

1. Per-quote check order: (E1) source digest over raw bytes; mismatch → exit 2 `source_tampered`. (E2) manifest validity: bad path, escaping path, missing source, non-UTF-8, bad digest format, unknown or duplicate IDs, empty or padded quote, ambiguous heading → exit 2 `invalid_manifest`. (E3) `len(quote.split()) > 25` → exit 1 `quote_too_long`. (E4) quote not a byte substring of whole source → exit 1 `quote_not_contiguous`. (E5) no occurrence inside declared span (absent heading included) → exit 1 `quote_location_mismatch`. Otherwise pass.
2. Heading key: whole-line match of `#`-prefixed Markdown heading (level + one space + exact text, trailing whitespace stripped), outside fenced code. Span ends before the next heading of level ≤ key level.
3. Matching: byte-exact substring; word-boundary check at each end when the quote's end character is a word character.
4. Exit precedence: any exit-2 finding → exit 2; else any exit-1 → exit 1; else 0.
5. Selftest minimum, one fixture per branch, pinned exit and finding ID: S017 splice (E4), S018 mislocated quote (E5), corrected S017 quote in `Command-Line Arguments` (pass), truncated-token quote (E4), `Usage` vs `Basic Usage` substring key (E5 with exact-match rule; must not pass), duplicate heading (E2), `# comment` inside a fence (span not ended), missing source (E2), digest mismatch (E1), `../` path (E2).

## Verification gaps

- No gate code exists at review time; no finding here is verified against an implementation.
- No selftest or gate run was performed; none is claimed.
- Source fidelity: the S017 and S018 excerpts were checked only against the two local captures. Live pages were not reopened. The S018 capture was fetched on 2026-10-20 by a sibling seat (ReviewS018, which reports no WAF interstitial); the S017 capture's fetch provenance is not documented in this lane beyond its path and hash.
- The round-13 line numbers (77, 87) could not be reproduced from any available bytes.
- This review does not assert that either quote is semantically true of the source's pipeline or of any held REA behavior.
