# Round 15 w1 — QuoteRawBoundary: gate parse_manifest / evaluate logic and rendered markup boundary

Seat: `KaidokuR15.QuoteRawBoundary` (leaf scout; no subagent dispatch).  
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.  
Subject file: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py`.  
Access date: 2026-10-20.  
Axes: **depth** (line-level code traces across parse, search, and exit-resolution paths) and **calibration** (truthful characterization of gate limits; distinguishing automated failure from unsupported refusal).

---

## 1. Limits, Custody, and Posture

- **Read-Only / No Execution:** This seat executed **no** gate invocations, selftests, frozen runs, tests, builds, linters, formatters, or target executions. All findings derive strictly from static source reading of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py` and repository governance files.
- **Tools Installed / Updated:** None (`none`). Standard environment tools were sufficient.
- **Separation of Evidence:**
  - **Observed:** Verbatim source code, string constants, control flow branches, and regex patterns in `quote-fidelity.py`.
  - **[INFERENCE]:** Trace of variable states when hypothetical rendered markup inputs are passed through the documented functions.
  - **Unknown:** Behavior of future or uncommitted patch versions not present in the repository at HEAD.

---

## 2. Gate Logic Code Trace: `parse_manifest` and `evaluate_manifest`

The gate script `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py` (836 lines, SHA-256 `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`) defines two primary evaluation pipelines: manifest evaluation (`evaluate_manifest`) and frozen suite evaluation (`evaluate_frozen`).

### 2.1 Manifest Parsing: `parse_manifest(data, base_real)` (`:173-209`)

```python
173: def parse_manifest(data, base_real):
174:     if not isinstance(data, dict):
175:         raise ManifestError("manifest must be a JSON object")
176:     sources = data.get("sources")
177:     quotes = data.get("quotes")
178:     if not isinstance(sources, dict) or not sources:
179:         raise ManifestError("sources must be a non-empty object")
180:     if not isinstance(quotes, list) or not quotes:
181:         raise ManifestError("quotes must be a non-empty array")
...
194:     for index, entry in enumerate(quotes):
195:         if not isinstance(entry, dict):
196:             raise ManifestError("quote #%d must be an object" % index)
197:         fields = {}
198:         for key in ("id", "source", "section", "quote"):
199:             value = entry.get(key)
200:             if not isinstance(value, str) or not value.strip():
201:                 raise ManifestError("quote #%d field %r must be a non-empty string" % (index, key))
202:             fields[key] = value
203:         if fields["id"] in seen:
204:             raise ManifestError("duplicate quote id %r" % fields["id"])
205:         seen.add(fields["id"])
206:         if fields["source"] not in pins:
207:             raise ManifestError("quote %s names unknown source %s" % (fields["id"], fields["source"]))
208:         parsed.append(fields)
209:     return pins, parsed
```

**Observed parse properties:**
1. **Pure Structural Schema Check:** `parse_manifest` validates only that:
   - `data` is a JSON dict.
   - `sources` is a non-empty dict mapping source IDs to dicts containing relative paths and 64-hex SHA-256 digests.
   - `quotes` is a non-empty list of dicts.
   - Each quote entry contains non-empty string values for `"id"`, `"source"`, `"section"`, and `"quote"`.
   - Quote IDs are unique within the manifest.
   - Each quote's `"source"` references a declared key in `sources`.
2. **No Content-Type or Markup Inspection:** `parse_manifest` performs **zero** inspection on the characters inside `"quote"` or `"section"`. It does not detect HTML tags, Markdown symbols, stripped tags, HTML entities, or newline layouts.
3. **Parse Outcome on Rendered Markup:** A manifest entry containing a rendered markup quote (e.g., `"quote": "Use raw bytes."` when the underlying source has `Use <em>raw</em> bytes.`) is accepted as valid syntax. `parse_manifest` does **not** raise `ManifestError` and does **not** generate any finding. It returns `(pins, parsed)` normally.

---

### 2.2 Source Ingestion and Verification: `evaluate_manifest(path)` (`:271-297`)

```python
271: def evaluate_manifest(path):
272:     findings = Findings()
273:     try:
274:         base_real = os.path.realpath(os.path.dirname(os.path.abspath(path)))
275:         pins, quotes = parse_manifest(load_json(path, "manifest"), base_real)
276:     except ManifestError as exc:
277:         findings.add("invalid_manifest", "manifest", str(exc))
278:         return findings
279:     texts = {}
280:     for source_id, (source_path, pinned) in pins.items():
...
286:         if sha256(blob) != pinned:
287:             findings.add("source_tampered", source_id, "sha256 differs from manifest pin")
288:             return findings
289:         try:
290:             texts[source_id] = blob.decode("utf-8")
291:         except UnicodeDecodeError:
292:             findings.add("invalid_manifest", source_id, "source is not valid UTF-8")
293:             return findings
294:     for quote in quotes:
295:         findings.quotes += 1
296:         grade_quote(quote, texts[quote["source"]], findings)
297:     return findings
```

**Observed evaluation properties:**
1. Once all source files pass SHA-256 verification and decode as valid UTF-8, each parsed quote is submitted directly to `grade_quote(quote, text, findings)`.
2. There is no pre-filter, classifier, or routing layer before `grade_quote`.

---

### 2.3 Quotation Evaluation: `grade_quote(quote, text, findings)` (`:250-269`)

```python
250: def grade_quote(quote, text, findings):
251:     ident = quote["id"]
252:     if len(quote["quote"].split()) > MAX_WORDS:
253:         findings.add("quote_too_long", ident, "more than %d whitespace words" % MAX_WORDS)
254:         return
255:     lines, heads = scan_headings(text)
256:     if quote["quote"] not in text:
257:         findings.add("quote_not_contiguous", ident, "no contiguous occurrence in source")
258:         return
259:     matches = [position for position, head in enumerate(heads)
260:                if quote["section"] in head[2]]
261:     if len(matches) > 1:
262:         findings.add("invalid_manifest", ident, "duplicate exact heading %r" % quote["section"])
263:         return
264:     if not matches:
265:         findings.add("quote_location_mismatch", ident, "section not found")
266:         return
267:     if quote["quote"] not in section_body(lines, heads, matches[0]):
268:         findings.add("quote_location_mismatch", ident, "quote lies outside the declared section")
```

**Observed grading steps:**
1. **Word Cap Check (`:252-254`):** If whitespace-delimited word count > 25, emits `quote_too_long@<ident>` and returns.
2. **Global Substring Check (`:256-258`):** Executes `if quote["quote"] not in text:`.
   - `text` is the raw decoded UTF-8 string of the source file.
   - `quote["quote"]` is tested as an exact, byte-identical contiguous substring of `text`.
   - No whitespace collapsing, tag stripping, entity translation, or punctuation normalization is applied.
   - If `quote["quote"]` is absent from `text`, emits `quote_not_contiguous@<ident>` with detail `"no contiguous occurrence in source"` and returns.
3. **Heading Resolution (`:259-266`):**
   - Headings are scanned via `scan_headings(text)` (`:212-236`).
   - Markdown headings match `^(#{1,6})[ \t]+(.+?)[ \t]*\Z` outside code fences; selector tuple is `(line.rstrip(),)`.
   - HTML headings match `^<h([1-6])(?:\s[^>]*)?>(.*?)</h\1>[ \t]*\Z` on a single line; selector tuple is `(" ".join(label.split()), line.rstrip())`.
   - If `quote["section"]` does not match any heading selector, emits `quote_location_mismatch@<ident>` (`"section not found"`).
   - If `quote["section"]` matches multiple headings, emits `invalid_manifest@<ident>` (`"duplicate exact heading ..."`).
4. **Section Body Substring Check (`:267-268`):**
   - `section_body(lines, heads, matches[0])` extracts raw source lines from the heading to the next heading of equal or higher level (`:239-247`).
   - If `quote["quote"] not in section_body(...)`: emits `quote_location_mismatch@<ident>` (`"quote lies outside the declared section"`).

---

### 2.4 Verdict and Exit Code Resolution (`:86-101`, `:415-418`)

```python
72:  CLEAN, FAILED, CNE = 0, 1, 2
78:  CNE_FINDINGS = frozenset({"invalid_manifest", "source_tampered", "snapshot_tampered"})
...
97:  def exit_code(self):
98:      if any(finding in CNE_FINDINGS for finding, _, _ in self.rows):
99:          return CNE
100:     return FAILED if self.rows else CLEAN
```

**Observed exit mapping:**
- **`0` (`CLEAN`):** Zero findings in `self.rows`.
- **`1` (`FAILED`):** `self.rows` contains one or more findings, and none belongs to `CNE_FINDINGS`.
- **`2` (`CNE` / could-not-evaluate):** `self.rows` contains at least one finding in `CNE_FINDINGS` (`invalid_manifest`, `source_tampered`, `snapshot_tampered`).

---

## 3. Exact Rendered Markup Input Outcome

When an analyst or automated process copies rendered text (e.g. from a browser display, HTML view, or rendered Markdown viewer) where formatting tags have been stripped, collapsed, or interpreted, the gate produces deterministic outcomes based strictly on raw UTF-8 substring comparisons.

### Case A: Quotation spanning markup tags / formatting
- **Source excerpt (raw bytes):**
  ```html
  ## Introduction
  Use <em>raw</em> bytes for verification.
  ```
- **Submitted rendered quote:**
  `"Use raw bytes for verification."`
- **Execution trace in `grade_quote`:**
  1. `len("Use raw bytes for verification.".split())` = 5 $\le$ 25. Passes.
  2. `quote["quote"] in text`:
     `"Use raw bytes for verification." in "## Introduction\nUse <em>raw</em> bytes for verification.\n"` evaluates to **`False`**.
  3. `findings.add("quote_not_contiguous", ident, "no contiguous occurrence in source")` is called.
  4. Function returns immediately.
- **Exit code resolution:**
  - Finding is `quote_not_contiguous`.
  - Is `quote_not_contiguous` in `CNE_FINDINGS`? **No.**
  - `exit_code()` evaluates: `FAILED if self.rows else CLEAN` $\rightarrow$ **`1`**.
- **Exact Outcome:** **Exit 1 (`FAILED`)** with finding `quote_not_contiguous@<ident>`.

### Case B: Rendered quote occurs contiguously elsewhere, but section heading is rendered or styled
- **Source excerpt (raw bytes):**
  ```html
  <h1 class="entry-title">Overview</h1>
  <p>Some words.</p>
  <div class="header">Details</div>
  <p>Target phrase appears here.</p>
  ```
- **Submitted quote & section:**
  `"section": "Details"`, `"quote": "Target phrase appears here."`
- **Execution trace in `grade_quote`:**
  1. `quote["quote"] in text` evaluates to `True`.
  2. `scan_headings` extracts only `<h1 class="entry-title">Overview</h1>`. The `<div class="header">Details</div>` is not matched by `HTML_HEADING` (`^<h([1-6]) ...`).
  3. `matches = [pos for pos, head in enumerate(heads) if quote["section"] in head[2]]` is empty (`[]`).
  4. `findings.add("quote_location_mismatch", ident, "section not found")` is called.
- **Exit code resolution:**
  - Finding is `quote_location_mismatch`.
  - Is `quote_location_mismatch` in `CNE_FINDINGS`? **No.**
  - `exit_code()` returns **`1`**.
- **Exact Outcome:** **Exit 1 (`FAILED`)** with finding `quote_location_mismatch@<ident>`.

### Case C: Rendered quote occurs in section, but differs by whitespace or entities
- **Source excerpt (raw bytes):**
  `AT&amp;T announced&nbsp;updates.`
- **Submitted rendered quote:**
  `"AT&T announced updates."`
- **Exact Outcome:** **Exit 1 (`FAILED`)** with finding `quote_not_contiguous@<ident>`.

---

## 4. Complete Absence of Unsupported Classification

A critical calibration finding from static review of `quote-fidelity.py`:

1. **Zero Occurrences of Unsupported Vocabulary:**
   - Literal token search: `grep -i -E 'unsupported|manual|rendered' quote-fidelity.py` yields **0** matches.
   - There is no finding code such as `unsupported_input`, `unsupported_representation`, `unsupported_format`, or `rendered_quote_not_supported`.
2. **Exhaustive Finding Inventory:**
   The codebase recognizes exactly seven finding identifiers:
   | Finding ID | Classification | Exit Code | Trigger Condition |
   |---|---|:---:|---|
   | `quote_too_long` | Quote failure | 1 | Word count > 25 |
   | `quote_not_contiguous` | Quote failure | 1 | Substring not in full source text |
   | `quote_location_mismatch` | Location failure | 1 | Heading not found, or substring not in section body |
   | `expected_verdict_mismatch` | Frozen suite failure | 1 | Actual exit/findings differ from frozen pin |
   | `invalid_manifest` | Could-not-evaluate (CNE) | 2 | Malformed JSON, schema violation, duplicate heading, non-UTF8 source |
   | `source_tampered` | Could-not-evaluate (CNE) | 2 | Source SHA-256 does not match manifest pin |
   | `snapshot_tampered` | Could-not-evaluate (CNE) | 2 | Frozen input file missing, unreadable, or digest mismatch |
3. **No Exit 2 for Semantic or Representation Limits:**
   - Exit 2 is reserved strictly for `CNE_FINDINGS` (`invalid_manifest`, `source_tampered`, `snapshot_tampered`).
   - A rendered markup quotation is valid JSON, references a valid pinned file, and parses cleanly; hence, it never triggers `invalid_manifest`.
   - The gate **cannot** and **does not** return exit 2 for rendered markup inputs.
4. **No Fallback or Diagnostic Classifier:**
   - The gate possesses no heuristics to distinguish a faithful quotation of rendered browser text from a hallucinated string, an intentional splice, or an altered quote.
   - Both categories fail identically at line 256 with `quote_not_contiguous` (exit 1).

---

## 5. Contract and Governance Calibration (QUALITY #16 vs #17)

### 5.1 The Ambiguity in QUALITY #16
In Round 14, `corpus/QUALITY.md` row 16 included the sentence:
> *"Code members, commit objects, JSON, command output, and quotations spanning markup require their appropriate manual source check under #1; this local instrument does not grade them."*

As documented in `corpus/lessons/round-14-verifier-spotcheck.md:172` (Routed Defect 2):
- The phrase *"this local instrument does not grade them"* was ambiguous: it could be misread as implying that `quote-fidelity.py` detects these substrates and refuses evaluation (e.g. exit 2), or that submitting them is blocked.
- In reality, the instrument **does** evaluate them if submitted: it applies literal raw UTF-8 substring checks, resulting in a machine verdict of **exit 1 (`quote_not_contiguous`)**.

### 5.2 Resolution in QUALITY #17 / Round 15 Claim C2
The calibrated resolution (superseding row 17 in `corpus/QUALITY.md` and C2 claim in `claims.json:8-11`):
1. **Existing Gate Behavior Retained:** No changes are made to `quote-fidelity.py`'s evaluation logic. It remains an exact raw UTF-8 substring instrument.
2. **Normative Submission Prohibition:** Rather than asserting that the gate "does not grade" rendered markup, the standard explicitly specifies:
   - Only captured, heading-structured raw UTF-8 substrings may be submitted as machine-gradeable.
   - Code members, commit objects, JSON, command output, and rendered quotations spanning markup **must not be submitted to raw quote machine grading**.
   - These non-raw substrates must be evaluated via manual source inspection under QUALITY #1.
3. **Documented Machine Limit:** A submitted rendered quote returns machine exit 1 (`quote_not_contiguous`), not exit 2. Exit 2 denotes malformed/tampered manifests/sources, never an unsupported-representation classifier.

---

## 6. Proposed Verification Checks for L1 (Integrator)

*Note: Per contract, this seat ran zero verification commands. L1 should run these exact checks once all seats land:*

1. **Frozen Regression Suite Conformance:**
   Confirm that all existing round-14 regression cases continue to pass without gate modification:
   ```sh
   python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
       --frozen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json
   ```
   *Expected:* Exit 0, 7 manifests matched, 0 findings.

2. **Gate Self-Test Execution:**
   Confirm internal CLI self-test passes:
   ```sh
   python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --selftest
   ```
   *Expected:* Exit 0, all cases CLEAN.

3. **Absence of "Unsupported" Tokens Check:**
   Confirm that no unsupported-classification tokens or dead handlers were introduced:
   ```sh
   grep -E 'unsupported|manual_only|rendered' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py
   ```
   *Expected:* Exit 1 (no matches found).

4. **Synthetic Boundary Fixtures Verification (Sibling Seat `BoundaryFixtures`):**
   Evaluate the paired synthetic raw vs. rendered manifests once landed:
   - Raw markup quote manifest:
     ```sh
     python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
         --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/manifest-raw.json
     ```
     *Expected:* Exit 0 (`CLEAN`), 0 findings.
   - Rendered quote manifest:
     ```sh
     python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
         --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/manifest-rendered.json
     ```
     *Expected:* Exit 1 (`FAILED`), finding `quote_not_contiguous@<ident>`.

5. **QUALITY Admission Table Check:**
   Verify that QUALITY row 17 is appended, supersedes 16, and contains the required tokens:
   ```sh
   grep -q "quote-fidelity" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md
   grep -q "must not be submitted" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md
   ```
   *Expected:* Both exit 0.

---

## 7. Tool Record

- **Installs / Updates:** None.
- **Environment:** Arch Linux, Python 3.14.7 stdlib, Git. Read-only static examination.
