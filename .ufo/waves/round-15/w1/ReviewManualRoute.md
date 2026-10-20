# Round 15 w1 — ReviewManualRoute (routed defect 2: manual-only input boundary)

seat: KaidokuR15.ReviewManualRoute (reviewer, leaf, source-only)
repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
baseline: 9719dd232687f5ee78a4ed323b37f8810e833d10
execution: none. No gate, selftest, frozen run, build, test, linter, REA call, or target execution. Non-verdict reads and `sha256sum` only.
tool installs/updates: none.
writes: this file only.

## Verdict

- The routed defect is real and is a calibration defect, not a verdict-logic defect. The tool returns exit 1 "quote absent" for any quote whose exact bytes are not in the pinned excerpt, and it has no input-class handling. A rendered quote that spans markup therefore fails with the same finding as a fabricated quote.
- The proposed docs-only resolution (new QUALITY row superseding #16 + SKILL row wording) is the correct in-scope route for C2. It is a **not-submitted policy**. It does **not** add automatic unsupported detection, and the docs must not say it does.
- The current wording "this local instrument does not grade them" (QUALITY #16) is inaccurate. The instrument does grade them and emits exit 0 or 1. What it lacks is input classification. The replacement text must say this.
- Accept the docs-only route only with the acceptance checks in section 5, and only with the wording constraints in section 4.

## 1. Sources read (absolute, with observed digests where taken)

| ID | Path | Observed |
|---|---|---|
| claims | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/claims.json | C2 = "two routed correction duties, no quote gate implementation change"; manual-only inputs "not be submitted to raw quote machine grading" |
| spec | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/spec.json | context matches claims; reportDir `.ufo/waves/round-15/w1` |
| closure | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:172-174 | routed defect 2 origin: "Clarify that these inputs must not be submitted as machine-gradeable, or align the documented exit behavior and add an appropriate control." |
| criterion | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:26 (row 16); header rule L4-6 | sha256 of file `2754e5257211e1af81ffe17bf7795d8ba00fabcb4764c458e8533d9f4c6030a3`. Header: a criterion is replaced by a new row naming the row it supersedes, never rewritten. |
| SKILL row | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:450 | sha256 `98f4dafaa0cc265bd568135623e90b5759a8a828e722d0ff731c86ad46dfeebc`. Says "1 failed (quote absent/mislocated/too long)" and "Raw UTF-8 substring and Markdown/single-line HTML heading consistency only". |
| tool | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py | sha256 `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8` (matches pin in round-14 measurement-pins.json:4) |
| frozen pins | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json | sha256 `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf` (matches measurement-pins.json:5) |
| measure | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py | sha256 `ee546111cb19e70eae63634f0795325465d58d3f3d0e098cbafc1fdb0c4dd2ab` (matches measurement-pins.json:6); L24 counts `"quote-fidelity" in QUALITY.md` |
| S017 excerpt | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/s017-view8-readme-usage-deterministic.html | sha256 `b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9` (matches PROVENANCE pin) |
| fixture provenance | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/PROVENANCE.md:46-47 | "the gate's raw-byte quote rule is not probed with this line" (S017 line 82 sentence with `<code>`) |
| lesson (r14) | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md:29, 44-45 | "Quotes interrupted by markup remain outside its raw-substring guarantee." |
| author steer | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/QuoteGateCode.md:62, 165 | "A visible sentence interrupted by inline tags is unsupported and must not be quoted (L1 steer ...)" |
| attack | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/AttackQuoteGate.md:22-26 | A1 counterexample: rendered sentence False raw, True after tag strip; L1 later accepted raw-only as a stated limit |
| fixture scope | /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/QuoteSourceFixtures.md:33, 89 | line-82 sentence intentionally not a green quote; "raw-byte quote policy" belongs to the gate contract |

Digests above were taken with `sha256sum` in this seat. Nothing else was executed.

## 2. What the tool does with markup, code, JSON (code-read; observed in source, not executed)

Observed in `quote-fidelity.py`:

- Manifest schema (docstring L16-22; `parse_manifest` L173-209): fields are `sources{path,sha256}` and `quotes[{id,source,section,quote}]`. There is **no kind, type, or raw/rendered field**. Any source path is accepted.
- Quote grading (`grade_quote` L250-268): (a) >25 whitespace words → `quote_too_long`; (b) `quote not in text` on raw UTF-8 → `quote_not_contiguous` with detail "no contiguous occurrence in source" (L256-258); (c) section match on heading selectors; (d) quote must lie in the section body.
- Findings (docstring L38-45): seven IDs. None is an unsupported-input or markup class. `CNE_FINDINGS` (L78) is `{invalid_manifest, source_tampered, snapshot_tampered}`. No code path emits exit 2 for markup-spanning or code/JSON quotes.
- Heading scanner (`scan_headings` L212-236; `MD_HEADING` L75) runs on **every** source regardless of kind. Only fences are excluded.
- Grep of the whole tool for `markup|unsupported|rendered|strip|kind|type` hits only the docstring heading-label text and `type(exc)`. Confirmed: no classification logic.
- Selftest (L566-709, read): the cases I read; none uses a quote containing tags, a rendered-vs-raw pair, a code member, or JSON. The round-14 closure records 28 CLEAN cases; I did not recount them.

Consequence (verified by reading the code path): the gate's verdict is a function of **copy form (raw bytes)**, not of whether the sentence matches the source's visible text.

## 3. Findings (severity order)

### F1 — HIGH (calibration): exit 1 for a rendered quote is indistinguishable from a fabricated quote

- Evidence: `grade_quote` L256-258 emits the same `quote_not_contiguous` for "bytes do not occur" whether the quote is a splice (round-13 S017 case) or a faithful rendered paraphrase. SKILL row L450 documents exit 1 as "quote absent/mislocated/too long". Under that wording a reader cannot tell a fidelity failure from a form mismatch.
- Concrete pair from the pinned excerpt (`.ufo/waves/round-14/fixtures/s017-view8-readme-usage-deterministic.html:14`, raw bytes `<p>Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers. ...</p>`, under `<h3>Deterministic Function Names and Mapping CSV</h3>` at :13):
  - rendered form `Use --normalize to replace address-derived function names with deterministic identifiers.` → predicted exit 1, `quote_not_contiguous@<id>` (INFERENCE from L256; not executed);
  - raw-copied form `Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers.` → predicted exit 0 (raw substring present; section body runs to the next `<h3>` at :16). INFERENCE from L256-268.
- Consequence: the same visible sentence gets opposite verdicts depending on byte form. The docs-only fix must state this explicitly; otherwise "exit 0 = clean" implies visible fidelity that the gate does not establish.

### F2 — HIGH (calibration): QUALITY #16 says "does not grade"; the instrument does grade

- Evidence: QUALITY row 16 (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:26`) ends "...quotations spanning markup require their appropriate manual source check under #1; this local instrument does not grade them." The tool emits `QUOTE_FIDELITY_VERDICT` with exit 0 or 1 for such input (verdict print L416-417; grade L250-268). "Does not grade" is literally false. The accurate statement is "does not classify; its verdict is raw-byte presence only and is not a fidelity result for these inputs."
- Wording correction is required in any superseding row. Do not edit row 16 in place (header rule forbids rewriting).

### F3 — MEDIUM: "quotations spanning markup" is ambiguous for raw-copied quotes

- A quote copied from raw HTML that contains `<code>` (F1 raw form) is also a quotation "spanning markup" in a literal reading. Under the current row 16 text, such a raw copy would need manual check even though the gate returns exit 0 for it.
- The docs-only fix must define the class by **the form submitted**: a manifest quote whose bytes contain tags, entities, or a backtick/bold rendering, and any quote whose visible text differs from its raw bytes. Name both raw-tag-bearing and rendered-only forms as manual-only, or explicitly allow raw-tag-bearing quotes as machine-checked with an explicit disclaimer. Pick one; do not leave it implicit.

### F4 — MEDIUM (inference, not observed): code members, JSON, command output and commit objects have failure modes beyond markup

- Heading scanner runs on every source (L212-236). A code or JSON source containing a line beginning `# ` (MD_HEADING L75 requires `#{1,6}` plus whitespace) is parsed as a Markdown heading and can split a section body or create duplicate-heading `invalid_manifest` (exit 2, L261-263). INFERENCE; not observed.
- JSON quotes copied from a rendered viewer will differ from raw bytes at `\"` and `\n` escapes → exit 1 by F1 mechanism. INFERENCE from L256.
- Commit objects and command output are plain text; the gate would grade them with the same raw rule. Not classified.
- The docs-only row should name these kinds as manual-only and should not claim the gate handles them.

### F5 — MEDIUM (policy enforcement): "not submitted" is discipline only

- The manifest accepts any source file and any quote string (F1, schema L16-22). Nothing in the tool, the SKILL row, or the frozen pins restricts input class.
- Existing "must not" language is about **quoting** (QuoteGateCode.md:62) and is in author artifacts under `.ufo/waves/round-14/w1`, not in the corpus. Round-14 lesson L172 uses "must not be submitted", but that is a closure note, not a rule in QUALITY or SKILL.
- Therefore the rule has no enforcement point. It is a **not-submitted policy**. A future operator who submits a rendered quote gets exit 1 and may misread it as a fabricated quote. Document that consequence explicitly.

### F6 — LOW (no regression risk found): the docs-only route is compatible with pins and frozen controls

- `measurement-pins.json` (round-14) pins only `quote-fidelity.py`, `expected.json`, and `measure.py` (lines 3-7). It does **not** pin `QUALITY.md` or `SKILL.md`. A docs-only edit does not break a pin.
- `measure.py:24` counts `"quote-fidelity" in corpus/QUALITY.md`. The token already appears in row 16, so a new row that repeats the token keeps the count at 1 and does not change the measure.
- The frozen expectations (`expected.json`, 7 manifests) cover only fixture manifests and sources. Docs-only changes do not touch them.

## 4. Two routes and their differences (not-submitted policy vs automatic unsupported detection)

| Route | What catches a rendered/markup/code/JSON input | Verdict for such input | In scope for C2? | Risk |
|---|---|---|---|---|
| A. Not-submitted policy (docs only) | Nothing automatic. Author/operator discipline. | Unchanged: exit 1 "quote_not_contiguous" (F1), exit 0 for raw-copied tag-bearing text. | **Yes.** Matches claims C2 ("no quote gate implementation change"). | Relies on discipline; misreading of exit 1 possible if docs are weak. Mitigated by wording constraints in section 4.1. |
| B. Automatic unsupported detection (gate change) | Would need a manifest kind field, or a heuristic such as "quote absent raw but present after tag-stripping → exit 2". | Could return exit 2 `unsupported` or `markup_spanning` for such input. | **No.** Requires implementation change, new selftest cases, and new frozen pins (changes tool digest and expected.json pin). | Heuristic (B2) can turn a spliced quote that spans markup from exit 1 (absent) into exit 2 (unevaluable), violating QUALITY #16's "an absent or misplaced quote is rejected". Also a quote-character heuristic (`<` in quote) misses rendered quotes with no tags left and false-flags code containing `<`. QuoteGateCode.md:62 and L1 steer already rejected normalization. |

Recommendation: route A only, in this round. Record route B as a candidate for a future round with its own selftest and pins. Do not describe any current behavior as "automatic detection".

### 4.1 Wording constraints for the superseding row and SKILL row

Required for acceptance:

1. New QUALITY row numbered 17, last column `16` (supersedes), appended. Row 16 text unchanged.
2. The row states that the gate grades **raw UTF-8 byte presence** of the quote in a pinned excerpt, plus section location and word count. It states the gate has **no input-class classification** and **never returns exit 2** for rendered, markup-spanning, code, JSON, command-output, or commit inputs.
3. The row states that exit 1 on such an input means "raw bytes absent or located elsewhere", not a fidelity finding about the source. It states that exit 0 on a raw copy containing tags proves byte consistency only.
4. The row defines the excluded class by submitted form (F3) and lists the kinds (F4). It cites `corpus/lessons/round-14-verifier-spotcheck.md:172` and `corpus/lessons/round-14.md:44-45`.
5. SKILL.md:450 exit-1 wording changes from "quote absent" to "quote's raw bytes absent or located outside its section, or too long", and adds a sentence that rendered/markup/code/JSON inputs are manual-only (QUALITY superseding row).
6. No row or SKILL text says "detects", "rejects" or "returns 2" for those inputs. No text says "does not grade" (the phrase in row 16).

Draft row wording (for L1 to integrate; not written by this seat):

> | 17 | Machine-check input class (supersedes 16's grading sentence): `quote-fidelity` tests whether a manifest quote's exact raw UTF-8 bytes occur in a pinned excerpt, inside the named heading's section, at ≤25 words. It performs no input classification: rendered text that spans markup, code members, JSON, command output and commit objects are manual-only and must not be submitted as manifest quotes. For such input exit 1 means the raw bytes are absent or misplaced, not a fidelity finding; exit 2 is never produced for them; exit 0 on a raw copy containing tags proves byte consistency only. Manual source check per #1. | corpus/lessons/round-14-verifier-spotcheck.md:172; corpus/lessons/round-14.md:44-45 | 16 |

(Draft only; L1 may tighten. Must not claim automatic detection.)

## 5. Verifiable acceptance (named checks for L1; none executed by this seat)

Run once after all seats finish. Expected results given.

- **A1 pins unchanged.** `sha256sum` of `tools/quote-fidelity.py`, `fixtures/expected.json`, `measure.py` equals `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`, `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf`, `ee546111cb19e70eae63634f0795325465d58d3f3d0e098cbafc1fdb0c4dd2ab` (paths under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/`).
- **A2 no implementation change.** Diff of `.ufo/waves/round-14/tools/` and `.ufo/waves/round-14/fixtures/` against baseline `9719dd232687f5ee78a4ed323b37f8810e833d10` is empty.
- **A3 criterion append-only.** `corpus/QUALITY.md` diff against baseline adds exactly one table row numbered 17 whose last cell is `16`. Row 16 line is byte-identical to baseline line 26. No other row changed.
- **A4 required terms present.** The new row contains: `raw UTF-8`, `must not be submitted`, `never produced for them` (or equivalent exit-2 negation), `rendered`, `code members`, `JSON`, `command output`, `commit`. `grep -c "does not grade" corpus/QUALITY.md` returns 0 (the row-16 phrase is not reused).
- **A5 no overclaim.** `grep -n -i -E "detect|reject|unsupported|returns 2|exit 2"` on the new row and on SKILL.md:450 returns no sentence asserting automatic detection or exit 2 for markup/code/JSON inputs.
- **A6 SKILL row wording.** SKILL.md:450 exit-1 description no longer reads "quote absent/mislocated/too long" alone. It contains "raw bytes" and "manual-only". Its trailing limit sentence still reads "Raw UTF-8 substring ... only".
- **A7 measure unchanged.** `grep -c quote-fidelity corpus/QUALITY.md` is ≥1, so `C2_grounded_quality_criteria` stays 1.
- **A8 frozen run.** `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-14/fixtures/expected.json` exits 0, with 7 `match` pin lines and `findings=0`. (Expected because no implementation or fixture changed.)
- **A9 selftest unchanged.** `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` exits 0 with 28 CLEAN cases (as recorded in round-14 closure). Optional; not needed if A1 holds.
- **A10 documented-limit control (optional, must be non-committed).** Copy `s017-view8-readme-usage-deterministic.html` (digest A1 `b5942047...`) into a temporary directory under `/var/tmp` with a fresh manifest. Two quotes, section `Deterministic Function Names and Mapping CSV`:
  - `Use --normalize to replace address-derived function names with deterministic identifiers.` → predicted exit 1, `quote_not_contiguous@<id>`.
  - `Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers.` → predicted exit 0.
  Observation confirms F1. If the predictions fail, F1 is wrong and the row wording must be revised. Delete the temporary directory afterwards.

Failure conditions: any row 16 change; any new row claiming exit 2 or automatic detection; any byte change in the tool, expected.json, or measure.py; any pin mismatch in A1.

## 6. Residual risks and gaps

- Nothing was executed. F1 predictions are code-read inferences (A10 is the discriminating check). F4 items are inference from L212-236 and L256-263.
- I read `quote-fidelity.py` at L1-72, L173-298, L212-273, L300-347 (partly elided), L349-436, L555-644, L645-709 (partly elided), and L815-833. Lines 300-347 and 437-555 and 710-812 were covered only by grep and partial reads. The conclusion "no markup classification" rests on the full grep, which is consistent.
- I did not run `git diff` against baseline `9719dd2`; A2 and A3 depend on L1 running it. The current QUALITY.md digest is `2754e52...`; the baseline digest was not computed here.
- The round-14 closure offered "clarify OR align exit behavior and add a control". This review supports only "clarify" for C2, because "align" requires a gate change (route B) that C2 excludes.
- SKILL and QUALITY are not assigned to this seat. Wording in section 4.1 is a proposal for L1 to integrate.
- Tool installs/updates: none.
