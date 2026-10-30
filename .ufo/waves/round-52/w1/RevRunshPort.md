# RevRunshPort — settled static port checklist

Verdict: checklist complete; recommendation only, not admission of an R52 implementation.

Deliverable: `.ufo/waves/round-52/w1/RevRunshPort/checklist.md` covers every requested MUST-preserve and MUST-change item with baseline file:line references and R52 claims anchors; additionally inventories environment controls, receipt fields, failure receipts, CLI options and exit semantics.

## Findings by severity

- **Medium / freeze completeness:** `plans/round-52-claims.md:71-75,154-161` names the harness and procedure but leaves detailed pins/guards/PATH/oracle grammar/schema implicit. The checklist supplies the missing port acceptance surface; this is a declaration risk, not an observed faulty R52 diff.
- **Medium / retry boundary:** baseline `tools/round-50/c1-run.sh:733-737` retries only provider_timeout, with configurable `C1_REA_ATTEMPTS`, and `:834` records aggregate attempts. Claims `:105-114` adds bounded ENOENT retry and failing diagnostics to the **counter projection**; do not infer that promise already exists in the harness or silently broaden harness retries.
- **Low / depth visibility boundary:** baseline `tools/round-50/c1-run.sh:772` omits input_path/continuation_id from its first-20 gap summary; claims `:59-62,97-98` requires them in the **counter receipt**. Full after.json remains present (`:755,791`); satisfy F8 there rather than treating the harness summary as sufficient.

## Residual risk / verification gaps

Static baseline-to-contract inspection only. No R52 harness draft comparison, tests, REA, controls, runtime, download or oracle invocation. Integration owner should compare the integrated harness against the checklist, including all three schema/claim constructors (`:334,622,804`) and preserve the independent oracle's two-direction comparisons. No admission or claim scoring performed.

`xd://lsp` is not mounted (read returned `No such tool`), so semantic status/references/definition/diagnostics were unavailable. Findings use direct literal source inspection, not semantic proof. Source identity command, exit 0, exact stdout SHA256 and UTC are in `RevRunshPort/inspection.json`. No scratch needed or created; no tool installs; no lane source changes or git mutations.

Self-evaluation: accuracy 4 (static evidence only; cannot establish runtime behavior), completeness 5 (all named acceptance surfaces and omitted knobs inventoried), clarity 4 (long checklist required by field-level contract), actionability 5 (line-indexed checkboxes), conciseness 4 (receipt schema necessarily dense); overall 4.4. Improvements: integration owner applies the checklist to actual port bytes; distinguish counter-specific enhancements from inherited harness behavior.
