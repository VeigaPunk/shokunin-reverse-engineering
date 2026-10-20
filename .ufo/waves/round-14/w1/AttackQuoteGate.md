# AttackQuoteGate — critic of the C2 quote-location gate interface (round 14, w1)

Seat: KaidokuR14.AttackQuoteGate (critic, leaf). I only read and counted. Access date: 2026-10-20.
I did not run `quote-fidelity.py`, `--selftest`, or any manifest; at the time of writing, `round-14/tools/` and `round-14/fixtures/` did not exist (glob, empty). Every verdict below is a **byte/substring count over the sources**, not gate output.
Tools installed or upgraded: none. `curl` and `python3` were already present.

Axes: **calibration** (does a pass or fail mean what C2 says?), **coverage** (do the S017 and S018 cases test the failure classes they claim to test?). No-harm: every correction below keeps the corrected positive controls green (checked by byte position).

## Sources opened

| Source | Location | Access | Contiguous quote (≤25 words) |
|---|---|---|---|
| View8 README, pinned `ef39099b…` | `raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md` → `/tmp/aqg-view8-README.md` (283 lines, sha256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b`, git blob `2a0c5a6037e236654e60d8b27d226b5c1bb820fb`, matching the r13 reviewer's tree-API `2a0c5a60…` and the peer copy in `w1/ReviewS017-source/`) | curl, 2026-10-20 | line 40: “Replace address-derived function identifiers with deterministic names based on parse order.” |
| Check Point S018 article | snapshot `w1/s018-raw.html` captured by ReviewS018 (sha256 `31b82315…74dd5e`, re-hashed by me); **I did not re-fetch it** | local file, 2026-10-20 | line 489: “The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.” |
| r13 non-author review | `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kaidoku-r13-review.md:96-104` | local | “The printed “quote” is the section prefix combined with the CLI bullet’s tail, swapping names/identifiers; it exists verbatim nowhere.” |
| r13 lesson errata | `corpus/lessons/round-13.md:63-66` | local | “These append-only corrections supersede the S017 quote and S018 location printed in the original Gate table.” |

Limitations: the article is a dynamic WordPress page (raw `<meta>` modified 2026-09-24, per ReviewS018). The snapshot shows only what the page served today. Neither source establishes REA or target behavior.

## Findings (severity order)

### A1 — High: a raw-bytes gate rejects a true quote that the S017 controls never test (false positive)
- **Counterexample:** the verbatim sentence from `Deterministic Function Names and Mapping CSV` (README line 82, as rendered): “Use --normalize to replace address-derived function names with deterministic identifiers.” Raw substring: **False**, because the source has `Use <code>--normalize</code> to`. After stripping tags: **True**.
- The planned positive control (the CLI sentence on line 40) passes under both policies (raw **True**, stripped **True**). It sits after `</code>: `, so the tag never falls inside it. The control therefore cannot distinguish an exact-bytes gate from a rendered-text gate.
- The r13 reviewer audited 20/22 quotes “allowing only stripped markdown backticks/bold” (`kaidoku-r13-review.md:94`). A gate that is stricter than the review it claims to encode will flag real quotes as `quote_not_contiguous`.
- **Smallest correction:** state the match policy in the interface: exact bytes, or text with tags/backticks/entities removed and whitespace collapsed. Then add the line-82 sentence under `### Deterministic Function Names and Mapping CSV` as a **second green control**, so the policy is pinned. Under either policy the S017 splice stays red (stripped: **False**). ReviewS017 §45 confirms this independently.

### A2 — High: “exact Markdown heading” cannot be satisfied by either pinned source; any fixture is a derived rendering
- The View8 README has **0** ATX `#` headings. Every heading is `<h1>`–`<h3>`, e.g. line 20 `<h3>Command-Line Arguments</h3>`. ReviewS017 F3 reports this independently. S018 is raw HTML whose sections are `<h1 class="wp-block-heading">` (Introduction at 469, Decompiled output at 625).
- So a fixture that satisfies the section grammar must be a conversion. Its sha256 then pins the **conversion**, not upstream blob `2a0c5a60…` or snapshot `31b82315…`.
- **Misleading integrity claim:** `source_tampered` only means “the fixture bytes differ from the manifest's sha256”. The fixture producer writes both, so it is a self-consistency check and does not show fidelity to the source. C2's `limits` already says “local captured source excerpts only”. The finding name and the SKILL wording must not read as source authentication.
- **Smallest correction:** either (a) let the gate recognise `<hN>` headings, which keeps raw pinned bytes (README sha256 `191621cd…`) as the fixture; or (b) keep Markdown and have `expected.json` record, per fixture, the upstream raw sha256, the line span, and the conversion rule. Rename or describe the finding as an excerpt-digest mismatch. Option (a) removes the derivation layer entirely.

### A3 — Medium: heading-text exactness gives false `quote_location_mismatch` on real headings
- S018 raw line 431 is `<strong>Key Points</strong>` inside an h1, and line 3581 is `Appendix &#8211; A`. Their rendered text is `Key Points` and `Appendix – A`. Without a stated rule, a manifest that names the rendered heading fails against markup bytes.
- The S017/S018 cases (`Introduction`, `Decompiled output`, `Command-Line Arguments`, `Deterministic Function Names and Mapping CSV`) contain no inline markup or entities, so the controls never exercise this.
- **Correction:** apply the same normalisation to headings as to quote text (A1). This affects only these cases.

### A4 — Medium: the “until next same/higher heading” rule lets a parent heading absorb a mislocation (false negative)
- Under the stated rule, `## Usage` (README line 18, h2) runs to the next h2 at line 133 (`Tree Output`). It therefore contains **both** line 40 (the CLI row) and lines 81–107 (`Deterministic …`).
- Citing `## Usage` admits a quote from either subsection. That is the same class of anchor drift as S018 (a topically adjacent but wrong subsection). The S018 red case only works because its sections are h1 **siblings** (469 vs 625). It would not catch the same mistake one level down.
- **Smallest correction (no harm to the controls):** compare against the **deepest enclosing heading**, i.e. a section ends at the next heading of any level. Both corrected controls stay green: line 40's nearest heading is line 20 `Command-Line Arguments` (next heading is line 66), and line 489's is line 469 `Introduction` (next heading is line 497). If L1 keeps the descendant-inclusive rule, record “parent sections are accepted” as a calibration limit.

### A5 — Medium: elided excerpts manufacture section membership (false negative)
- In S018, `Introduction` (469) is followed by `Distributed payloads` (497), `Analysis methodology` (565) and `Environment Setup` (601) before `Decompiled output` (625). An excerpt that keeps 469 and 625 but drops the headings in between makes `# Introduction` run until 625. A quote from `Analysis methodology` would then pass as “located in Introduction”.
- The gate cannot detect this, because it trusts the excerpt.
- **Correction:** the fixture producer keeps every heading line between the first and last section it includes, and marks any elided span explicitly. This is a fixture rule, not new gate scope.

### A6 — Medium: contiguity after normalisation spans list items (false negative)
- After tags are stripped and whitespace collapsed, “based on parse order. --normalize-map [CSV]: While using --normalize, write a CSV mapping” is contiguous (count: **True**). In the source it spans two `<li>` items, lines 40–42; the raw substring count is **False**.
- This is the cheapest surviving splice shape under the A1 normalisation. It stays inside one section, so location does not catch it either.
- **Correction:** keep block boundaries when normalising (only within-block whitespace collapses), or record the tradeoff as a limit. The S017 red case does not test this. It splices across **sections**, not blocks.

### A7 — Medium: weak expected verdicts
1. **Exit code alone is not enough.** One manifest with both red quotes exits `1` even when one of the two findings is missing or wrong. Pin the full sorted list of `(quote id, finding id)` plus exit, per frozen manifest. Keep the positive controls in a separate manifest that must exit `0`; otherwise an always-fail gate meets every red expectation.
2. **Precedence is unspecified.** The S017 splice is cited under `Deterministic …`, and its first 77 characters (9 words) **are** contiguous in that section. An implementation that checks “in section?” first could emit `quote_location_mismatch` instead of `quote_not_contiguous`. Define the rule: absent from the whole source → `quote_not_contiguous`; present only outside the named section → `quote_location_mismatch`; heading absent from the source → state which ID, and do not let it fall to exit 2.
3. **Any fuzzy matcher admits the splice.** `difflib` ratio splice↔line-82 sentence = **0.85**; splice↔CLI sentence = **0.841**. Any similarity threshold at or below 0.84 turns the S017 red case green. Exact (normalised) substring matching is the only rule that passes, so the interface should forbid similarity matching.
4. **Self-graded expectations.** The fixture producer authors fixtures, manifests and `expected.json`. The red expectations should cite their non-author anchor, `kaidoku-r13-review.md:96-104` (S017 “exists verbatim nowhere”; S018 under `# Introduction`, not `Decompiled output`), rather than the producer's own byte inspection alone.
5. **`--selftest` is not C2 evidence.** It runs the code producer's synthetic fixtures. Only the frozen S017/S018 run with digest-pinned gate, manifest and fixture bytes supports C2's observable. The gate's sha256 check does not cover the manifest itself; L1's pin must.

### A8 — Low: calibration scope of the claim
- Both red cases were already caught by human review (`round-13-verifier-spotcheck.md:13`) and the gate is fitted to them. The gate shows executable regression detection for two known defects, not a detection rate.
- Out-of-sample mislocations exist in fleet reviews: a verbatim quote cited under the wrong section (`kaika-w3/kasegi-review.md:102`), and three location fixes (`kaika-w3/kengaku-review.md:129-131`). These belong to sibling lanes. I list them only as held-out candidates for L1; I made no claim about them and no writes.
- Line numbers are not stable keys. S018's round-13 “line 87 / heading 77” does not match the raw 489/469 (ReviewS018 F3). Keep line numbers out of manifests.

### Not exercised by these sources (scope note)
No duplicate heading texts exist in either the README heading map or the S018 article `<h1>`/`<h2>` list, so duplicate-heading ambiguity is untested by the real fixtures. ReviewQuoteContract owns that question. Path escape (`..`, absolute paths, symlinks) in manifest `path` belongs to GateInputSafety.

## Checks L1 should run after integration (none run by me)
- The frozen S017 manifest: the splice under `Deterministic …` → `quote_not_contiguous`; the CLI sentence under `Command-Line Arguments` → clean; the line-82 sentence under `Deterministic …` → clean (A1); the CLI sentence under `Deterministic …` → `quote_location_mismatch`.
- The frozen S018 manifest: the quote under `Decompiled output` → `quote_location_mismatch`; under `Introduction` → clean. Pin exit + sorted IDs + the gate, manifest and fixture sha256s.
- If A4 is adopted: the CLI sentence under `Usage` → `quote_location_mismatch`.
