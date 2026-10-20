# LogExtractTool report — log-extract.py (round 17, wave 1)

Seat: KaidokuR17.LogExtractTool-3 (executor leaf, no dispatches).
Deliverable: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/log-extract.py`
(new file, Python 3 stdlib only, `python3 -I` clean, no writes anywhere).

## Contract coverage (contract.md:51-60)

Output object: `{log_path, log_sha256, language_compiler, go_lines,
untested_versions, snapshot_labels, go_version_logged, missing_bootstrap,
analyzer_errors, classification}` — all keys emitted; JSON `sort_keys=True,
indent=2`; exit 0 emitted, 2 unreadable/bad input (verified in selftest).

Implementation choices within the contract (all `[INFERENCE]` where the
contract text is ambiguous, each exercised in selftest):

- `go_lines[].line` = 1-based line number (citeable anchor). A `raw` field
  carrying the verbatim line (trailing spaces kept) is added alongside the
  four contract fields so downstream seats can re-anchor without re-reading.
- `analyzer_errors` read literally: `level == "ERROR"` AND component
  startswith `"Golang"` (contract.md:56 "messages with level ERROR from
  Golang*"). Consequence: `GoRttiMapper` ERRORs — including "Untested Go
  version" — are NOT in `analyzer_errors`; they remain in `go_lines` and
  `untested_versions`. Boundary case `component_boundary` asserts this.
- List fields (`untested_versions`, `snapshot_labels`, `go_version_logged`,
  `analyzer_errors`) are deduplicated preserving first-occurrence order;
  per-event duplicates remain in `go_lines` (e.g. shfmt logs the same
  bootstrap failure twice, lines 82-85 and 86-89). Dedupe chosen so
  `compare.py`'s "observed list contains predicted" never compares
  duplicates.
- `snapshot_labels` regex `^Using Go API snapshot for (?:version )?(\S+)`
  covers both observed phrasings; `GoApiSnapshot.java:160`'s "Falling back
  from %s to %s for Go API snapshot" is a WARN and deliberately not a label.
- `go_version_logged` regex `^Go version (\d\S*)` is message-anchored so
  "Untested Go version [1.27.0]" cannot leak in; `\d` start rejects the
  bracketed form.
- `missing_bootstrap` = substring "Missing Go bootstrap type info" in any
  go_line message (WARN text from `BootstrapInfoException` via
  `GoRttiMapper.java:115`).
- `language_compiler` = first "Using Language/Compiler: X" message, any
  component; else null.

## Grounding in installed Ghidra source (Base-src.zip, 12.1.4)

- `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`: `:106` "Reading
  Go binary info", `:115` warns exception text, `:171` "Untested Go version
  [%s]", `:179-180` "Using Go API snapshot for version %s" (logs the
  *snapshot's* version, `apiSnapshot.getVer()`, not the requested version —
  relevant when patch-fallback occurs), `:358-360` bootstrap-missing text.
- `.../rtti/GoApiSnapshot.java`: `:160` patch-fallback warn, `:163` "Using Go
  API snapshot for %s" (requested `goVer`).
- `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java`: `:135` ERROR
  "Go symbol analyzer error: unable to get GoRttiMapper", `:139` "Go version
  %s".
- `.../GolangStringAnalyzer.java`: `:105` ERROR "Go string analyzer error:
  unable to get GoRttiMapper".

## Verification exercised (author-side, per contract allowance)

`python3 -I log-extract.py --selftest` → `SELFTEST: CLEAN cases=6`, exit 0.
Cases: bootstrap_missing (shfmt-shaped), snapshot_loaded (esbuild-shaped),
no_go_analysis (gcc binary shape), other (go lines, no snapshot, no
missing), component_boundary (PropagateRttiBackgroundCommand excluded —
Go text but non-`Go*` component; GolangDWARFFunctionFixup included;
GoRttiMapper ERROR not in analyzer_errors; 1-based line numbering),
exit-2 on missing file via subprocess.

Pilot log runs (read-only, files not copied):

- `pilot/shfmt-log/ghidra.log` (go1.27.0, out of 1.15-1.25 range):
  `classification=bootstrap_missing`, `untested_versions=["1.27.0"]`,
  `missing_bootstrap=true`, `snapshot_labels=[]`, `go_version_logged=[]`,
  `analyzer_errors`=["Go symbol analyzer error: unable to get GoRttiMapper",
  "Go string analyzer error: unable to get GoRttiMapper"], 8 go_lines
  (log lines 82-89), `language_compiler=x86:LE:64:default:golang`,
  `log_sha256=aaf677ed…45b5255` — matches pilot/SHA256SUMS.
- `pilot/esbuild-0.25.12-log/ghidra.log` (go1.23.12, in range):
  `classification=snapshot_loaded`, `snapshot_labels=["1.23.12"]`,
  `go_version_logged=["1.23.12"]`, `untested_versions=[]`,
  `missing_bootstrap=false`, `analyzer_errors=[]`, 17 go_lines
  (log lines 62-85), `language_compiler=x86:LE:64:default:golang`,
  `log_sha256=f6b61152…da5d89a7` — matches pilot/SHA256SUMS.

## Limits / notes for downstream seats

- Contract-mandated component filter excludes Go-related text logged under
  non-`Go*` components: esbuild pilot lines 80-82 (`PropagateRttiBackgroundCommand`,
  `FixClosureFuncArgsBackgroundCommand`) and line 84
  (`FixGcWriteBarrierFlagBackgroundCommand`) are visible only via `go_lines`
  exclusion, not in the output. `[INFERENCE]` contract intends this.
- The "Untested Go version" ERROR is `GoRttiMapper`, not `Golang*`, so a
  failing-but-bootstrapped carrier could classify `other` with empty
  `analyzer_errors`; check `untested_versions`/`go_lines` for ground truth.
- `snapshot_labels` may hold the *snapshot* version (GoRttiMapper:180) that
  differs from the requested version after patch fallback (`GoApiSnapshot:160`
  warn). compare.py should compare against the deduped list; a two-element
  list would signal that case.
- Line regex requires `LEVEL  (Comp)` with space-padded 5-char level and a
  space before message; a hypothetical Ghidra level >5 chars or unparenthesized
  format would be skipped as non-record. `[INFERENCE]` — only the observed
  format is claimed.
- No installs performed. No carrier binaries executed; no REA/Ghidra invoked.
