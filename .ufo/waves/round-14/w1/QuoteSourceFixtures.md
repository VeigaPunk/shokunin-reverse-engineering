# QuoteSourceFixtures — C2 frozen quote-location fixtures (round 14, w1)

Seat: `KaidokuR14.QuoteSourceFixtures` (leaf executor). Access date: **2026-10-20**. Worktree: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Axes: **calibration** (does a red/green verdict mean what C2 says?) and **coverage** (are the two prior defects testable as isolated controls?). No-harm: source opening, exact extraction, hashing, and JSON authoring only.

I did **not** run `quote-fidelity.py`, `--manifest`, `--frozen`, or `--selftest`, and I ran no tests, builds, linters, or formatters. No tool was installed or upgraded. No code, SKILL, registry, lesson, LOG, SCORECARD, or manifest outside `fixtures/` was edited.

## Files written

All under `.ufo/waves/round-14/fixtures/`:

| File | Bytes | SHA-256 | Role |
|---|---|---|---|
| `s017-view8-readme-usage-deterministic.html` | 1,150 | `b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9` | S017 source: bounded derived excerpt, selected lines verbatim, no command blocks |
| `s018-checkpoint-introduction-decompiled.html` | 1,674 | `a6cd53dc9dd1f775aa48191b607d0b6b5ced840b4796ec450585f1fdcbfc33bd` | S018 source: bounded derived excerpt, selected lines verbatim, omitted bodies labelled |
| `manifest-s017-original.json` | 451 | `7761238844228f21d5595d06d56cdb3f2ba78225a5d72928af511be40a10111f` | red-before: original compound S017 defect (splice + `Deterministic Function Names and Mapping CSV`) |
| `manifest-s017-red.json` | 429 | `e7f19e738cdc7282bc678f2dffd8d20b5481fab6cd7e537a2196f0aeddb91e48` | isolated quote control: same splice under `Command-Line Arguments` |
| `manifest-s017-fixed.json` | 416 | `ab592dbdc84150ec629499bb2be0105b7611cec11a460c0a9c6e0deaae3fda77` | corrected S017 quote |
| `manifest-s017-location.json` | 438 | `cfce915b861e7a5da4bdb5aff7db1da534b7ada57822eddd75513abbf2d84d2a` | negative location control: corrected S017 quote under the wrong heading |
| `manifest-s018-red.json` | 442 | `8b753511b270a20f8f1869576af9b430a7accb6727ab382d8e4495544daa806f` | red-before: exact S018 quote under `Decompiled output` |
| `manifest-s018-fixed.json` | 437 | `5fb9837e9514600c398bab667d24bf2bd3a1b1b00c439a2eb1b1ba5a893329d1` | corrected S018 location |
| `manifest-corrected.json` | 813 | `7bb4deb5d333cac935237a4d798fe9de11187f9277cecc4a510d07b5972d00b6` | separate clean two-quote control |
| `expected.json` | 1,787 | `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf` | `--frozen` pins: every manifest and source, expected exit and sorted IDs |
| `PROVENANCE.md` | 10,705 | not pinned | upstream identities, transforms, line spans, limits |

`expected.json` is not self-pinned; its own digest is printed here and must be pinned outside the frozen run. The gate hashes pinned manifests and sources before evaluation, exactly as its `evaluate_frozen` preflight does.

## Sources reopened

| Source | Location | Access | Contiguous quotation (≤25 whitespace words) | Limit |
|---|---|---|---|---|
| S017 pinned View8 README | `https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md`; upstream line 40, `Usage` → `Command-Line Arguments` → `--normalize` row | 2026-10-20, HTTP 200; 13,242 bytes; SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b` | `Replace address-derived function identifiers with deterministic names based on parse order.` | This is study provenance, not proof of View8 behavior or V8 14.8 compatibility. |
| S017 deterministic section, raw bytes | Same capture, line 82 under `<h3>Deterministic Function Names and Mapping CSV</h3>` | Same | `Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers.` | The `<code>` elements interrupt this sentence; it is not the corrected CLI sentence and is not used as a green quote. |
| S018 Check Point Research article | `https://research.checkpoint.com/2026/breaking-the-seal-static-deobfuscation-of-jsceals-compiled-v8-bytecode/`; `Introduction`, raw line 489; heading line 469 | 2026-10-20, HTTP 200, `text/html`; 355,603 bytes; SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e` | `The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.` | 19 words; exact quote does not prove the described pipeline works. |
| S018 wrong anchor | Same capture; `Decompiled output` heading line 625, section span 625–706, next heading `Obfuscation layers` line 707 | Same | Heading: `Decompiled output` | The quoted sentence occurs **0** times in that span and once at line 489. |
| Round-13 errata | `corpus/lessons/round-13.md:63` | Local, 2026-10-20 | `These append-only corrections supersede the S017 quote and S018 location printed in the original Gate table.` | Prior author record; not independent evidence. |
| Round-13 outside review | `corpus/lessons/round-13-verifier-spotcheck.md:13` | Local, 2026-10-20 | `Review found S017's spliced quotation and S018's mislocated exact quote.` | Names the defects; does not itself locate the quotes. |
| C2 claim text | `.ufo/waves/round-14/claims.json:24-25` | Local, 2026-10-20 | `quote-location fidelity gate plus grounded QUALITY criterion rejecting S017 splice and S018 mislocation while admitting corrected contiguous located quotes` | Scoped to local captured excerpts; no whole-registry or semantic claim. |
| Gate implementation read (not run) | `.ufo/waves/round-14/tools/quote-fidelity.py:254,265`; SHA-256 `f8d66742703c5503c6e502fbb93c26790a7e772c8ccbef8ab74f5bf116f93968` | Local, 2026-10-20 | `if quote["quote"] not in text:` / `if quote["quote"] not in section_body(lines, heads, matches[0]):` | Code was read only; this seat did not execute it. Its hash is not in `expected.json`. |

The direct S018 GET returned the article itself, with no WAF interstitial. Its digest equals the prior lane snapshot's recorded digest (`31b82315…74dd5e`); no cookie, header, or WAF dump is retained. The page is mutable (metadata modified 2026-09-24), so these bytes are today's only.

## Fixture construction

- **S017** — bounded derived excerpt, 1,150 bytes. Selected original lines are copied verbatim with LF preserved: headings 18 (`Usage`), 20 (`Command-Line Arguments`), 66 (`Basic Usage`), 71 (`Disassembler Path`), 76 (`Processing Disassembled Files`), 81 (`Deterministic Function Names and Mapping CSV`), and 108 (`Creating and Processing Serialized Files`); the line-40 `--normalize` list item carrying the corrected quote; and the line-82 short paragraph. Omitted ranges are replaced by HTML comments naming their original spans. No command block, CSV example, or other list item is retained. Line 71 is retained even though the requested heading list named only 18/20/66/76/81/108: it is an intervening h3, and dropping it would widen `Basic Usage` and break heading hierarchy.
- **S018** — bounded derived excerpt, 1,674 bytes. Original lines 469, 489, 497, 565, 601, 625, 629, 633, and 707 are copied verbatim with CRLF preserved. Omitted ranges 470–488, 490–496, 498–564, 566–600, 602–624, 626–628, 630–632, 634–706, and 708–4569 are replaced by HTML comments naming the span. Every heading between `Introduction` and `Obfuscation layers` is retained in order; none is dropped or added. The absence claim for the wrong section is based on the **full capture** (span 625–706), not on the excerpt.
- Scratch full copies were deleted after hashing/extraction. Only the bounded excerpts remain in the repository.

## Expected verdicts (byte-derived; gate not run)

`expected.json` uses the gate's frozen shape: `manifests[] {path, sha256, exit, findings}` and `sources[] {path, sha256}`, with paths relative to `expected.json`. Findings are sorted `class@quote-id`.

| Manifest | Section | Quote | Exit | Expected IDs |
|---|---|---|---|---|
| `manifest-s017-original.json` | `Deterministic Function Names and Mapping CSV` | original splice, 14 words | 1 | `quote_not_contiguous@S017-Q1` |
| `manifest-s017-red.json` | `Command-Line Arguments` | original splice, 14 words | 1 | `quote_not_contiguous@S017-Q1` |
| `manifest-s017-fixed.json` | `Command-Line Arguments` | corrected sentence, 11 words | 0 | none |
| `manifest-s017-location.json` | `Deterministic Function Names and Mapping CSV` | corrected sentence, 11 words | 1 | `quote_location_mismatch@S017-Q1` |
| `manifest-s018-red.json` | `Decompiled output` | exact S018 sentence, 19 words | 1 | `quote_location_mismatch@S018-Q1` |
| `manifest-s018-fixed.json` | `Introduction` | exact S018 sentence, 19 words | 0 | none |
| `manifest-corrected.json` | corrected S017 + S018 locations | both corrected sentences | 0 | none |

The rationale follows the gate's stated order: the splice is absent from the whole source, so it is `quote_not_contiguous`; the S018 sentence is present in the source but outside the declared section, so it is `quote_location_mismatch`; the corrected pairs satisfy the section span. `manifest-s017-original.json` reproduces the compound round-13 shape (splice plus the original `Deterministic Function Names and Mapping CSV` heading); because the gate tests whole-source contiguity before section membership, the declared heading cannot change that verdict. The isolated pair then attributes the failure to the quote text alone.

## Causal pairing (verified by JSON object comparison)

- `manifest-s017-red.json` → `manifest-s017-fixed.json`: **only `quotes[0].quote` differs**. Source, section, quote id, and source pin are identical. This isolates the splice from location.
- `manifest-s017-fixed.json` → `manifest-s017-location.json`: **only `quotes[0].section` differs**. This isolates location from quote text.
- `manifest-s018-red.json` → `manifest-s018-fixed.json`: **only `quotes[0].section` differs**. This isolates the original wrong heading from the quote.

`manifest-corrected.json` is a separate clean control, so a combined green cannot hide a red pair. All pair deltas were computed over parsed JSON, not eyeballed.

## Verification actually performed

- Re-hashed both upstream captures before extraction: S017 `191621cd…619b`; S018 `31b82315…dd5e`.
- Confirmed the S017 excerpt retains selected upstream lines verbatim, including every heading 18–108 and no command block; the corrected sentence occurs once (line 40), and the splice occurs zero times in the whole upstream capture.
- Confirmed the S018 sentence occurs once in the full capture (line 489), is inside `Introduction` (469–496), and occurs zero times in `Decompiled output` (625–706).
- Confirmed every selected S018 line is byte-present in the upstream capture, all headings between the captured endpoints are retained, and the stored excerpt hashes match `expected.json`.
- Confirmed every manifest parses as JSON, every source pin matches its file, and each quote's whitespace-word count is ≤25 (14, 14, 11, 11, 19, 19, 11, 19).
- Confirmed pair deltas as above.

These are byte and JSON facts. They do **not** constitute a gate run, and I do not claim any gate exit was observed.

## Risks and limits

- **Frozen-file trust:** `expected.json` pins the manifests and sources but not itself or the gate script. L1 should pin `expected.json` and `tools/quote-fidelity.py` outside the run, as `GateInputSafety` F4 recommends. The gate script hash at report time was `f8d66742…f93968`; it now enforces that every manifest-referenced source is also pinned in `expected.json.sources`, which this set satisfies. If the code changes again before integration, expected IDs may need re-derivation.
- **Derived excerpts (both sources):** omission markers are additions. The fixtures prove quote-location logic, not that the retained excerpts equal the full pages; every retained source line and quote is exact bytes. Absence of the S018 quote from `Decompiled output` is evidenced against the full capture and recorded in `PROVENANCE.md`.
- **Mutable source:** a later fetch of S018 may differ in bytes or content. The pinned digest identifies today's capture only; round 13's rendering line numbers (heading 77, quote 87) are not reproducible here and are not used.
- **Raw-byte quote policy:** all fixture quotes are tag-free raw-byte substrings. The line-82 sentence is intentionally not a green quote because `<code>` interrupts it; a text-normalizing gate would treat that sentence differently. That policy question belongs to the gate contract, not to this fixture set.
- **Selector form:** manifests use visible HTML heading labels (`Command-Line Arguments`, `Introduction`, `Deterministic Function Names and Mapping CSV`, `Decompiled output`), matching the gate's raw-HTML heading support. A gate restricted to Markdown `#` selectors would not admit these sources.
- **Scope:** an exit-0 pair shows that the excerpt and manifest agree and the quote lies in the named section. It does not prove source authenticity, absence of other source defects, or any REA/target behavior.
- This seat is author-side and cannot provide non-author admission.

## Handoff checks for L1 (not run here)

1. Pin `expected.json`, the seven manifests, the two excerpts, and `tools/quote-fidelity.py` by SHA-256 outside the gate.
2. Run `python3 -I tools/quote-fidelity.py --frozen fixtures/expected.json` once, after freezing; expect overall exit 0 with seven matching manifest rows.
3. Run each manifest separately if causal evidence is needed in the log; the red pairs must show exactly the single finding listed above and the green pairs must show `findings=0`.
4. Do not regenerate or reformat the fixtures after pinning; any byte change yields `snapshot_tampered` (exit 2) by design.
