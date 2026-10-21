# R21Attack39 — t1246-cover retrospective compatibility

## Scope and axes

- **Calibration:** verify the exact retained-log binding and digest before interpreting the comparison.
- **Depth:** exercise the R21 first-failure comparator against only retained R20 label `t1246-cover`, using its frozen prediction and original R20 extractor. This is retrospective evidence, not a fresh forecast.
- Frozen C2 says retained R20 results are to remain matches; this report establishes only this one artifact, not the nineteen-result population or the full C2 claim.

## Exact-artifact result

The R20 binding `.ufo/waves/round-20/runs/t1246-cover/comparison-log-binding.json` names:

- Log: `.ufo/waves/round-20/runs/t1246-cover/logs/rea-ghidra-mFkiDF/ghidra.log`
- Bound SHA-256: `facaced427a73c56cf8dee9de61938331ef3fd0f465bc6ccadc1dcaeb8b8b6de`
- Binding field `verified`: `true`

Actual hash command and output:

```text
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cover/logs/rea-ghidra-mFkiDF/ghidra.log
facaced427a73c56cf8dee9de61938331ef3fd0f465bc6ccadc1dcaeb8b8b6de  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cover/logs/rea-ghidra-mFkiDF/ghidra.log
```

The actual digest matches the binding.

Actual comparison execution (`cwd=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`):

```json
{
  "argv": [
    "python3", "-I", "-B",
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py",
    "--prediction", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-cover.json",
    "--log", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-cover/logs/rea-ghidra-mFkiDF/ghidra.log",
    "--extractor", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py"
  ],
  "exit": 0,
  "stdout": "{\"finding\": \"failure_match\", \"last_line\": 250, \"match\": true, \"observed\": null, \"predicted\": null}\n",
  "stderr": ""
}
```

**Finding:** the assigned `t1246-cover` retrospective comparison matched: frozen prediction `first_failure.h1` is null, and the original extractor reported no qualifying first failure through log line 250. This establishes the comparator's null/null result for this bound artifact only. The comparator's contract explicitly scopes null to bounded observed silence, not successful analysis; unrelated analyzer errors do not establish success and are not evidence of a successful analysis here.

## Residual risk and verification gaps

No other retained R20 labels, malformed-observation controls, or broader C2 battery were exercised under this one-label assignment. No REA or native carrier was run. No production edits or tool installs/updates were made. No `lsp` device was exposed in this session, so no LSP status, references, definition, or diagnostics check was available.

Report: .ufo/waves/round-21/w2/R21Attack39.md