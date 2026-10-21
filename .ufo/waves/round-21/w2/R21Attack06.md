# R21Attack06 — C1 `execution_failure`

## Scoped finding

No actionable defect observed in this one case. The frozen `fixture-contract.json` independently assigns `execution_failure` exit **1** because the matching record carries typed `execution_failure` error. The frozen battery record supplies exact matching `evidence_id` and `operation` together with `"error":{"code":"execution_failure"}`. The C1 successor is `tools/verb-coverage.py`; its structural refusal path returns `evidence_refused` for a matching but refused record.

Executed only this case through the actual successor CLI. The evidence JSON was staged in `/tmp/R21Attack06-vpzz2c7z/evidence.json`; the temporary directory was checked absent after cleanup.

- `argv`: `["/usr/bin/python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/R21Attack06-vpzz2c7z/evidence.json", "--verb", "inspect-wasm-artifact", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]`
- Expected exit (fixture contract): **1**
- Observed exit: **1**
- stdout: `{"bound": false, "finding": "evidence_refused"}\n`
- stderr: empty
- External temp directory: absent after cleanup

This establishes the expected result for this record only; it is not a claim that the whole C1 fixture set passes.

## Nearby counterexample — unrun

`[UNRUN]` Keep the same exact matching id and operation but put the literal `execution_failure` only in a prose field, e.g. `{"evidence_id":"ev_…","operation":"inspect_wasm_artifact","notes":"execution_failure"}`. Expected exit **0**: the contract requires a typed refusal, and the successor documents that arbitrary prose is not a refusal field. This is a nearby check that distinguishes structural refusal from token matching.

## Residual risk and verification gaps

- The requested case belongs to C1 and its actual CLI (`verb-coverage.py`) has no extractor argument or extractor execution path. No C2 comparator case was run and no C2 extractor stub was created; doing so would test a different case despite the `ONLY R21-C1 execution_failure` scope.
- No LSP device is mounted (`read xd://lsp` returned “No such tool”), so status/references/definition/diagnostics were unavailable. No grep was used.
- No build, suite, formatter, or unrelated case was run. No production or fixture file was changed. No tool was installed or updated.
