# R21Attack09 — `objdump_architectures_positive`

**Axes:** calibration; depth.

## Findings

- **No actionable finding for the assigned case.** The frozen contract requires exit `0` when the same Evidence record has `operation: inspect_with_objdump`, `parameters.operation: architectures`, and `subject: null` (`.ufo/waves/round-21/fixture-contract.json:14`). The frozen battery record has those fields and independently also declares exit `0` (`.ufo/waves/round-21/fixtures/battery.json:61-65`). One direct invocation of the R21 successor returned exit `0` and `{"bound": true, "finding": "evidence_bound", "pathless": true}`. This agrees with the contract, including the pathless limit.

## Exact run record

The command used only the frozen case's evidence, verb, and Evidence ID. The inert C2 extractor stub was staged beside the case input in the external temporary directory but was not passed to or executed by the C1 CLI; the contract explicitly separates C1 and C2. The temporary directory was removed after the command.

- Expected exit (contract): `0`
- Expected exit (battery): `0`
- Observed exit: `0`
- `argv`:

```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/tmp/kaidoku-r21-attack09-9vk0f_ze/evidence.json", "--verb", "list-objdump-architectures", "--evidence-id", "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
```

- stdout (exact):

```text
{"bound": true, "finding": "evidence_bound", "pathless": true}
```

- stderr (exact): empty
- External temporary directory: `/tmp/kaidoku-r21-attack09-9vk0f_ze`; observed removed: `true`
- The C2 extractor stub emitted a bounded null observation (`first_failure: null`, `last_line: 0`); it was not exercised in this C1 run.

## Nearby counterexample (unrun)

`objdump_wrong_parameter`, the adjacent frozen negative at `.ufo/waves/round-21/fixtures/battery.json:68-72`, retains the same Evidence ID and top-level operation but sets `parameters.operation` to `disassemble` and places `architectures` only in `notes`. It is expected to exit `1` by the contract (`fixture-contract.json:15`). **Unrun** to honor the one-case execution assignment; it is a useful nearby check that the parameter—not unrelated text—controls binding.

## Basis and limits

The successor source maps this verb to `inspect_with_objdump`, requires the exact ID and operation in one record, then checks `parameters.operation == architectures`; it reports `pathless` when a matching record's subject is null (`tools/verb-coverage.py:85-99`). This is consistent with the observed result but is not a claim of cryptographic Evidence authentication. No analyzed carrier was run and no provider/REA call was made. The result does not assess runtime routing, same-identity rerouting, or saturation claims.

No LSP device was exposed: looking up `xd://lsp` returned “No such tool.” Therefore no LSP status, references, definition, or diagnostics were available; source citations here are contextual, not semantic proof from an LSP server. No production or fixture files were changed, and no tools were installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack09.md`
