# C1 list-objdump-architectures alias review

## Axes and scope

- **C1 calibration** (tied-lowest finite proxy): review the alias/parameter binding and preserve the legitimate pathless positive.
- **C2 depth**: not evaluated here; the first-failure comparator/extractor do not implement this C1 evidence-binding predicate.

Read-only scope: the named R20 tools, retained objdump architecture evidence, frozen R21 C1 contract/fixture, and the current R21 binder source. No checks or runtimes were executed.

## Finding — one R20 false-accept defect

**Severity: medium, baseline predicate defect; not evidence that the retained R20 result itself is false.** In `.ufo/waves/round-20/tools/verb-coverage.py:120-123`, the alias `list-objdump-architectures` is mapped to the file-wide tokens `inspect_with_objdump` and `"architectures"`. `bound_evidence()` finds a cited ID in an existing cited evidence blob, then accepts if those tokens occur anywhere in that blob and no refusal token occurs (`:136-165`, especially `:149-164`). It does not parse a record or associate the ID, operation, and operation parameter within one record.

The frozen negative is a concrete counterexample: same cited ID and top-level `operation: inspect_with_objdump`, but `parameters.operation: disassemble` and unrelated `notes: architectures` (`.ufo/waves/round-21/fixtures/battery.json:68-72`). The raw blob contains both R20 token strings, so the R20 predicate can count this wrong-parameter evidence as exercised. This is one record-association defect, not separate alias and null-subject defects. It does not establish that the actual retained R20 architecture observation was miscounted.

## Null-subject boundary — correct positive, not a defect

The retained architecture output has `subject: null`, top-level `operation: inspect_with_objdump`, and `parameters.operation: architectures` (`.ufo/waves/round-20/evidence/c2/objdump/architectures-json/stdout.json:1`); its receipt records the `list-objdump-architectures --format json` invocation and exit 0 (`.../receipt.json:2,15,19`). The R20 knowledge entry explicitly describes the null/pathless boundary (`corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md:9,16,27-28`). Do not require or invent an artifact digest for this operation. The positive must remain accepted and identified as pathless.

## Independent positive/negative fixture and expected result

Reuse the frozen, pre-measurement pair in `.ufo/waves/round-21/fixture-contract.json:14-15` and `fixtures/battery.json:61-73`; do not add it again to the denominator:

1. **Positive `objdump_architectures_positive`:** one JSON record with the cited `evidence_id`, `operation: inspect_with_objdump`, `parameters.operation: architectures`, and `subject: null`. Contract expectation: exit **0**. **[INFERENCE from current R21 source, not executed]** `tools/verb-coverage.py:85-99` should report `finding: evidence_bound`, `bound: true`, `pathless: true`.
2. **Negative `objdump_wrong_parameter`:** same ID and top-level operation, `parameters.operation: disassemble`, with only unrelated `notes: architectures`. Contract expectation: exit **1**. **[INFERENCE from current R21 source, not executed]** `:87-96` should report `finding: evidence_unbound`, `bound: false`; note prose cannot satisfy the parameter check.

The current R21 alias branch maps the verb to `inspect_with_objdump`, requires that exact ID and operation in one parsed record, then requires `parameters.operation == architectures` (`tools/verb-coverage.py:77-99`). It reports `pathless` from `subject is None` rather than rejecting null. Source review indicates the assigned pair is addressed; no runtime pass is claimed.

## Other named tools, residual risk, and verification gaps

No `list-objdump-architectures`, `architectures`, or `subject` token was found by literal search in R20 `compare-first-failure.py` or `first-failure-extract.py`. That scan is only a locator, not semantic proof; these are outside the alias-binding finding. I attempted LSP discovery first (`read xd://lsp`); the tool registry reported no such device, so no LSP status/references/definition/diagnostics were available.

Parent should run the changed-path C1 battery against the two frozen cases and assert both exit and finding; run the stable changed-path smoke/final suite once after all changes land. I ran no tests, builds, lint, formatter, runtime, or REA producer. No tools were installed or updated.

Report: `.ufo/waves/round-21/w1/C1ObjdumpAlias.md`
