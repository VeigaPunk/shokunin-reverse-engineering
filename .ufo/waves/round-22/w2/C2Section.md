# R22-C2 section parser attack review

**Axes:** coverage (spoofed/prefix and duplicate headings; empty reason); calibration (positive control and fail-closed cases).

**Target snapshot:** `.ufo/waves/round-22/tools/count-c2.py`, SHA-256 `0a5f2a41a9801e2ac421fd61766ec926cc69f7f96d66be8a18b7ced780b8f7a0`. Tests used a private scratch clone at `/tmp/r22-c2-attack`, based on lane revision `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, and an identical counter snapshot at `/tmp/count-c2-review-snapshot.py`. No production file was changed. Complete exact argv/stdout/stderr for every counter invocation is in the same-name JSON attachment, `C2Section.json` (including byte counts and stdout SHA-256).

## Finding — Low / conditional: format-only reason passes the non-empty guard

At `count-c2.py:74-79`, table cells are normalized with Python `str.strip()`, then `check` tests only `if not row["reason"]` at lines 101-105. A reason consisting solely of U+200B ZERO WIDTH SPACE survives `.strip()` and is truthy. In the scratch clone, replacing the `inspect-packet-fields` reason with only `\u200b` produced `accounted_count: 14`, `mismatched: []`, `finding: "dispositions_complete"`, and exit **0**. The exact stdout contains the row reason as `"\\u200b"`; the full output, argv, empty stderr, and stdout digest are in `C2Section.json`.

This is a concrete bypass of a *human-visible non-empty reason* check. Calibration: the counter's explicit limit at `count-c2.py:170-173` says reason semantics require manual review, so this does **not** establish a false receipt match or violate a promise of semantic reason validation; treat it as residual risk unless the intended invariant is that a reason must be visibly present. Narrow fix if that invariant is required: reject reason text after removing whitespace and Unicode format/control-only characters (e.g. `unicodedata.category` `Cf`/`Cc`) and add the format-only row as a red fixture. Do not infer semantic quality from non-empty text; the declared manual-review boundary remains.

## Attacked controls and results

- **Positive control:** baseline lane revision, all genuine dispositions intact — exit **0**, `accounted_count: 14`, `finding: "dispositions_complete"`, stderr empty.
- **Heading-prefix spoof:** changed only the canonical line to `### Round-22 catalog dispositions (draft mirror)`. The parser's exact `line == HEADING` comparison does not select it; all verbs are `unaccounted`, exit **1**. No false clean result.
- **Two exact headings:** duplicated the exact heading with an empty first section before the real table. `section_rows` raises `ambiguous_disposition_sections`; stdout is exactly `{"finding": "unevaluable", "error": "ambiguous_disposition_sections"}\n`, exit **2**, stderr empty. This is fail-closed.
- **Truly empty reason:** set the first row reason to `""`. It is reported `missing_reason`; 13/14 accounted, exit **1**. The literal empty-reason attack is rejected.
- **Format-only reason:** U+200B-only reason passes as described in the finding, exit **0**.

The `C2Section.json` attachment preserves complete stdout for the 14/14 positive control and each mutation, not merely these summaries.

## Residual risk and verification gaps

- Exact heading selection and duplicate-section detection are effective for the tested prefix and duplicate-heading cases. The earlier content is not silently substituted for a second exact section.
- The reason-text edge is bounded by the counter's explicit manual-review limit; the counter alone does not certify the reason's semantic content.
- No LSP device/server route is exposed in this assignment's tool set, so no LSP status/references/definition/diagnostics query was available. I did not use text search as semantic proof; findings cite the direct source read and observed CLI outputs. No installs or other runtime/device probes were performed.
