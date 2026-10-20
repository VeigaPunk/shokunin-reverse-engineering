# Round 14 C2 fixtures — provenance and limits

Owner: `KaidokuR14.QuoteSourceFixtures` (leaf, source-only). Access date: **2026-10-20** (UTC).
No gate run, selftest, test, linter, REA call, or target execution was performed by this seat.
Expected verdicts below are byte-inspection results against the documented gate semantics; L1 owns the frozen run.

## Scope

These fixtures exercise **quote location and contiguity inside captured excerpts**. They do not prove
whole-source authenticity, absence of defects elsewhere in a source, or any semantic claim about the
sources, REA, or a target. Every manifest pins its source bytes; the gate can prove only that the
excerpt and manifest agree with those pins.

No upstream file is redistributed in full. The S018 page is a third-party "all rights reserved"
article; only a bounded derived excerpt is retained here, with omitted ranges labelled. The View8
README is public; its fixture is also a bounded derived excerpt with labelled omissions and no command blocks.

## Source A — S017 View8 README (bounded derived excerpt)

| Field | Value |
|---|---|
| Upstream URL | `https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md` |
| Pinned commit | `ef39099b4f5076042173f9113382ebeb0630a56d` |
| Opened | 2026-10-20, direct HTTPS GET, HTTP 200 |
| Upstream bytes | 13,242 bytes; 283 LF-terminated lines; SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b` |
| Excerpt file | `s017-view8-readme-usage-deterministic.html` |
| Excerpt bytes / SHA-256 | 1,150 bytes / `b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9` |
| Transform | **Derived bounded excerpt.** Selected original lines are copied verbatim (LF preserved): headings 18, 20, 66, 71, 76, 81, 108; the line-40 `--normalize` list item carrying the corrected quote; and the line-82 short paragraph. Omitted ranges are replaced by HTML comments naming their original line spans. No command block (`<pre>`), CSV example, or other list item is retained. |
| Selection mapping | Retained original lines: **18, 20, 40, 66, 71, 76, 81, 82, 108**. Omitted original lines: **19, 21–39, 41–65, 67–70, 72–75, 77–80, 83–107, 109–283**. |

Original heading lines retained verbatim (line numbers from the upstream capture):

| Line | Element |
|---|---|
| 18 | `<h2>Usage</h2>` |
| 20 | `<h3>Command-Line Arguments</h3>` |
| 66 | `<h3>Basic Usage</h3>` |
| 71 | `<h3>Disassembler Path</h3>` |
| 76 | `<h3>Processing Disassembled Files</h3>` |
| 81 | `<h3>Deterministic Function Names and Mapping CSV</h3>` |
| 108 | `<h3>Creating and Processing Serialized Files</h3>` |

Factual byte checks on the excerpt:

- Corrected sentence, original line 40: `Replace address-derived function identifiers with deterministic names based on parse order.` — 11 whitespace words, exactly 1 occurrence in the excerpt. It lies inside the `Command-Line Arguments` section (next heading of same or higher level: `Basic Usage`, line 66).
- Round-13 spliced quote, `Use --normalize to replace address-derived function names with deterministic names based on parse order.` — 14 whitespace words, **0 occurrences** in the whole excerpt and in the whole upstream capture.
- Original line 82 is retained verbatim as a short paragraph (22 whitespace words): `Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers. To preserve the relationship between the original and normalized names, add <code>--normalize-map</code>:`. In raw bytes the `<code>` elements interrupt the plain sentence; no tag-stripped rendering is stored, and the gate's raw-byte quote rule is not probed with this line.

## Source B — S018 Check Point Research article (bounded derived excerpt)

| Field | Value |
|---|---|
| Upstream URL | `https://research.checkpoint.com/2026/breaking-the-seal-static-deobfuscation-of-jsceals-compiled-v8-bytecode/` |
| Opened | 2026-10-20, direct HTTPS GET, HTTP 200, `text/html; charset=UTF-8` |
| Upstream bytes | 355,603 bytes; 4,569 LF terminators; SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e` |
| Prior lane snapshot | Deleted by its owner for custody; its recorded SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e` equals this fresh capture's digest |
| WAF | No WAF interstitial was encountered on the direct GET; the returned title and body are the article. No cookie/header dump is retained. |
| Excerpt file | `s018-checkpoint-introduction-decompiled.html` |
| Excerpt bytes / SHA-256 | 1,674 bytes / `a6cd53dc9dd1f775aa48191b607d0b6b5ced840b4796ec450585f1fdcbfc33bd` |
| Transform | **Derived bounded excerpt.** Selected original lines are copied verbatim (CRLF preserved). Omitted bodies are replaced by HTML comments naming the omitted original line spans. Every heading between the first and last captured heading is retained in order; no heading is dropped or added. |

Retained original lines, verbatim:

| Line | Content |
|---|---|
| 469 | `<h1 class="wp-block-heading">Introduction</h1>` |
| 489 | `<p class="wp-block-paragraph">The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode. ...</p>` (entire original paragraph line) |
| 497 | `<h1 class="wp-block-heading">Distributed payloads</h1>` |
| 565 | `<h1 class="wp-block-heading">Analysis methodology</h1>` |
| 601 | `<h1 class="wp-block-heading">Environment Setup</h1>` |
| 625 | `<h1 class="wp-block-heading">Decompiled output</h1>` |
| 629 | Decompiled-output paragraph beginning `Once we have the correct disassembly, ...` |
| 633 | Decompiled-output paragraph beginning `View8 does not reconstruct the original JavaScript source. ...` |
| 707 | `<h1 class="wp-block-heading">Obfuscation layers</h1>` |

Elided original ranges, all labelled in the excerpt: 470–488, 490–496, 498–564, 566–600, 602–624, 626–628, 630–632, 634–706, 708–4569.

Factual byte checks on the full upstream capture (not only the excerpt):

- The quoted sentence is **19 whitespace words**, contiguous, and occurs exactly **1** time in the whole capture, at line 489.
- It lies inside `Introduction` (line 469; next same-level heading `Distributed payloads`, line 497).
- `Decompiled output` spans lines 625–706 (next same-level heading `Obfuscation layers`, line 707). The quoted sentence occurs **0** times in that span.
- Round-13's rendered line numbers (heading 77, quote 87) are not reproducible from these bytes and are **not** used. The section heading plus the capture digest are the locator.

## Manifests and expected verdicts

All paths are relative to this directory. Each manifest pins its source file; `expected.json` pins every
manifest and every source file for `--frozen`. Finding IDs are the gate's sorted
`<class>@<quote-id>` strings.

| Manifest | Source | Section | Quote id | Expected exit | Expected findings |
|---|---|---|---|---|---|
| `manifest-s017-original.json` | S017 | `Deterministic Function Names and Mapping CSV` | `S017-Q1` | 1 | `quote_not_contiguous@S017-Q1` |
| `manifest-s017-red.json` | S017 | `Command-Line Arguments` | `S017-Q1` | 1 | `quote_not_contiguous@S017-Q1` |
| `manifest-s017-fixed.json` | S017 | `Command-Line Arguments` | `S017-Q1` | 0 | none |
| `manifest-s017-location.json` | S017 | `Deterministic Function Names and Mapping CSV` | `S017-Q1` | 1 | `quote_location_mismatch@S017-Q1` |
| `manifest-s018-red.json` | S018 | `Decompiled output` | `S018-Q1` | 1 | `quote_location_mismatch@S018-Q1` |
| `manifest-s018-fixed.json` | S018 | `Introduction` | `S018-Q1` | 0 | none |
| `manifest-corrected.json` | S017 + S018 | corrected locations | `S017-Q1`, `S018-Q1` | 0 | none |

Paired causal deltas (verified by JSON object comparison):

- `manifest-s017-red.json` → `manifest-s017-fixed.json`: only `quotes[0].quote` differs. Same source, section, and quote id. This isolates the splice from location.
- `manifest-s017-fixed.json` → `manifest-s017-location.json`: only `quotes[0].section` differs. Same source and quote. This isolates location.
- `manifest-s018-red.json` → `manifest-s018-fixed.json`: only `quotes[0].section` differs. Same source, quote, and quote id. This isolates the original wrong heading from the quote.

`manifest-corrected.json` is the separate clean multi-quote control (exit 0, no findings).

## Pinned inputs

| File | Bytes | SHA-256 |
|---|---|---|
| `s017-view8-readme-usage-deterministic.html` | 1,150 | `b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9` |
| `s018-checkpoint-introduction-decompiled.html` | 1,674 | `a6cd53dc9dd1f775aa48191b607d0b6b5ced840b4796ec450585f1fdcbfc33bd` |
| `manifest-s017-original.json` | 451 | `7761238844228f21d5595d06d56cdb3f2ba78225a5d72928af511be40a10111f` |
| `manifest-s017-red.json` | 429 | `e7f19e738cdc7282bc678f2dffd8d20b5481fab6cd7e537a2196f0aeddb91e48` |
| `manifest-s017-fixed.json` | 416 | `ab592dbdc84150ec629499bb2be0105b7611cec11a460c0a9c6e0deaae3fda77` |
| `manifest-s017-location.json` | 438 | `cfce915b861e7a5da4bdb5aff7db1da534b7ada57822eddd75513abbf2d84d2a` |
| `manifest-s018-red.json` | 442 | `8b753511b270a20f8f1869576af9b430a7accb6727ab382d8e4495544daa806f` |
| `manifest-s018-fixed.json` | 437 | `5fb9837e9514600c398bab667d24bf2bd3a1b1b00c439a2eb1b1ba5a893329d1` |
| `manifest-corrected.json` | 813 | `7bb4deb5d333cac935237a4d798fe9de11187f9277cecc4a510d07b5972d00b6` |
| `expected.json` | 1,787 | `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf` |

`expected.json` is not self-pinned; L1 should pin its digest outside the run (the gate does not hash the
frozen file itself). Any change to a manifest or source after this file was written will make
`--frozen` report `snapshot_tampered` (exit 2), by design.

## Limits

- S018 is mutable (article metadata: modified 2026-09-24). These bytes are today's capture only; a later
  fetch may differ in digest and content. No claim is made that round 13 read identical bytes.
- The S018 fixture is a **derived** excerpt, not the page. Its elision comments are additions; every
  retained source line and the quote are exact bytes. Absence of the quote from `Decompiled output` is
  asserted for the full capture (line span 625–706), not inferred from the excerpt.
- The View8 fixture is a **derived** excerpt, not the whole README. Its selection comments are
  additions; every retained source line is exact bytes. Claims about text outside the retained lines
  are not encoded in it.
- The gate was not executed here. Verdicts in `expected.json` are the author's byte-level predictions
  under the gate contract; L1's frozen run is the independent check.
