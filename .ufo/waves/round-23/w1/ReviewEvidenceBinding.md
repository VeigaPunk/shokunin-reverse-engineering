# ReviewEvidenceBinding

Axes: coverage (exact verb/record linkage and refusal handling); calibration (what metadata can and cannot establish).

## Findings

### Medium — refusal ancestry in `meta` is only partially preserved

**Evidence:** `.ufo/waves/round-22/tools/count-c1.py:76-96` checks top-level `ok` and `r21.refused(envelope)`, requires `meta.command == verb`, then applies a recursive dict/list refusal walk to `data`. It subsequently passes only `json.dumps(record)` to `r21.bind`, so metadata refusal context must be handled before that extraction. The metadata check at line 79 delegates to `.ufo/waves/round-21/tools/verb-coverage.py:39-55`; `refused()` returns false for non-dicts (line 41), does not inspect an `ok` field, and recurses only through `raw_result`/`normalized_result` by calling itself on the child. If either child is a list, the recursive call returns false instead of inspecting its members. The robust list + nested `ok` walk at `count-c1.py:84-94` applies only to `data`, not `meta`.

**Observed targeted probe:** I loaded those two reviewed source modules in Python 3.14.8 and invoked `bind_cli` directly in memory with a valid synthetic direct record (`evidence_id=ev_` + 64 `a`s, `operation=identify_flutter_build`) and matching `meta.command`. Return values were: positive direct record `0`; direct `meta.error` refusal `1`; `meta.exit_code=1` refusal `1`; `meta.ok=false` `0`; `meta.raw_result=[{"ok":false,"error":{"code":"execution_failure"}}]` `0`; wrong `meta.command` `1`; outer `ok=false` `1`. Thus the wrapper rejects the tested ordinary metadata refusal forms and exact-command mismatch, but still accepts metadata that declares failure via `ok:false` or a refusal object in a list. These were in-memory synthetic inputs, not evidence that REA emits either metadata shape; no subprocess argv/exit/stderr applies to this direct call.

**Fixture coverage:** `counter-fixtures.py:121-128` puts nested `ok:false` and array refusal under `data`; lines 131-134 cover only direct `meta.error` and `meta.exit_code`. There is no metadata `ok:false` or metadata-array refusal case in the C1 fixture list (lines 82-89). Add those cases and apply the same recursive refusal policy to metadata before slicing it away; otherwise a producer-refusal ancestor recorded in `meta` can coexist with a counted direct data record.

### No finding — direct-record, command, and operation checks are aligned for evidenced cases

`count-c1.py:74-83` requires a successful CLI envelope and a direct `data` dictionary containing both `evidence_id` and `operation`; line 79 compares `meta.command` exactly to the catalog verb; lines 95-96 send only the direct record to the inherited binder. `verb-coverage.py:77-99` matches the requested ID and operation on that record, with hyphen-to-underscore operation conversion. The R22 aliases at `count-c1.py:34-35` correspond to the retained package-source excerpt in `.ufo/waves/round-22/evidence/sources/cli-aliases.json:8-10` (`debug-with-gdb` → `gdb_console`; `debug-with-rizin` → `rizin_debug_command`). Existing C1 fixtures include wrong-command and forged-debug-operation controls (`counter-fixtures.py:119-120,137-138`); the retained prior selftest record reports both passing (`w2/C1Duplicate.json:5-29`). I did not rerun the suite.

Actual retained JSON supports the command-value check for `identify-flutter-build` (`evidence/c1/identify-godot.envelope.json:1`, `meta.command` matches, direct operation is `identify_flutter_build`). A retained `inspect-dart-aot-saber.envelope.json:1` has matching `meta.command` but `ok:false` and `error.code=unsupported_target`; the current top-level gate refuses it. No retained debugger envelope was examined; whether debugger `meta.command` uses the catalog verb is therefore **unknown here**. The source evidence for debugger aliasing establishes operation-name mapping, not the emitted `meta.command` value.

## Residual risk and verification gaps

- The wrapper binds a local JSON assertion, not the original invocation: the counter docstring at `count-c1.py:14-16` explicitly says this is not authentication and does not compare the envelope with `run.stdout`. A matching `meta.command`, Evidence ID, and operation therefore do not prove that the named CLI command produced the file. This is an acknowledged limit, not a separate finding.
- R22's recorded HEAD measurement was 1/6 (not full six-verb saturation); its 6/6 positive control was synthetic (`w2/C1Source.md:13-17`; `w2/C1Duplicate.json:31-37`). No canonical runtime, same-identity rerouting, live debugger, device, or target execution was used or established in this review.
- LSP status could not be obtained: `read xd://lsp` returned “No such tool.” No semantic references/definition/diagnostics checks were available; findings above are grounded in direct source reads and the targeted function call, not grep.
- Target SHA-256: `count-c1.py` `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`; inherited R21 helper `verb-coverage.py` `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`.
- No REA probe, build, full test suite, linter, formatter, or install was run. No production files were changed.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewEvidenceBinding.md` — final SHA-256 is supplied with the handoff to avoid embedding a stale self-hash.

## Installs

None.

## Open risks

Metadata refusal arrays and metadata `ok:false` pass the current `bind_cli` gate in the targeted probe. Debugger `meta.command` emission remains unobserved, and local envelope fields remain unauthenticated by design.