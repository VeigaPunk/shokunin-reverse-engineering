# Round 17 shared implementation contract (L1-authored, 2026-10-20)

All paths absolute. `W` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17`.
All tools: Python 3 stdlib only, `#!/usr/bin/env python3`, runnable as `python3 -I <abs path> ...`,
JSON on stdout (`sort_keys=True, indent=2`), exit 0 emitted/clean, 1 failed/mismatch (only where stated),
2 could-not-evaluate (bad input, unreadable file, subprocess failure). Never execute a carrier binary.
Never write outside the paths a CLI is given. No network. Each tool has `--selftest` that builds its
own temporary fixtures under `tempfile.mkdtemp()`, removes them, prints `SELFTEST: CLEAN cases=N` or
`SELFTEST: FAILED ...`, and exits 0/1. Executors MAY run their own tool's `--selftest` once; never
REA `analyze`/`search`/`decompile`, never Ghidra, never another seat's tool.

## W/tools/pins.py  (R16-PROVENANCE fix)
- `snapshot(paths: list[str]) -> dict`: `{"taken_at_utc": ISO8601 with microseconds, "monotonic_ns": int,
  "entries": {abs_path: {"sha256", "size", "mtime_ns"} or {"error": str}}}`.
- `compare(pre: dict, post: dict) -> dict`: `{"equal": bool, "changed": [paths], "missing": [paths],
  "pre_taken_at_utc", "post_taken_at_utc"}`; `equal` is false if any sha256/size differs or any error.
- CLI: `pins.py snapshot --out FILE PATH...` (exit 0, 2 unreadable out dir); `pins.py compare PRE POST`
  (exit 0 equal, 1 differ, 2 unreadable/invalid). Selftest MUST include a red case: snapshot, mutate a
  temp file, snapshot, compare -> exit 1 naming that path.
- It proves only "same bytes at two instants", never "unchanged throughout"; say so in `--help`.

## W/tools/retain.py  (generic retained execution)
`retain.py --out RECEIPT.json [--pin PATH]... [--cwd DIR] [--timeout S] -- ARGV...`
Imports pins.py by `importlib.util.spec_from_file_location` from `W/tools/pins.py`. Takes pre pins,
runs ARGV (no shell), captures stdout/stderr to `RECEIPT.stdout` / `RECEIPT.stderr` files next to the
receipt, takes post pins, writes receipt `{argv, cwd, started_at_utc, ended_at_utc, exit, stdout_path,
stdout_sha256, stderr_path, stderr_sha256, python: sys.version, orig_argv: sys.orig_argv, pins_pre,
pins_post, pins_compare}`. Exit = 0 if child ran (any child exit recorded) and pins equal; 1 if pins
differ; 2 if child could not start/timeout.

## W/tools/carrier-run.py  (Go carrier analyze with retained Ghidra log)
`carrier-run.py --carrier PATH --label LABEL --out-dir DIR [--rea-version 6.5.0] [--timeout 1800]
[--poll 0.5] [--search NAME]...`
1. pins.snapshot([carrier, + the r16 selection.py, the Go data dir listing file is NOT pinned]) pre.
2. `npx -y rea-agents@V inspect-go-binary CARRIER --format json` -> `DIR/inspect-go.json` (+ stderr, exit).
3. Record the set of existing `/tmp/rea-ghidra-*` dirs; start `npx -y rea-agents@V analyze CARRIER --format json`
   (Popen, stdout/stderr to files). While it runs, every POLL seconds copy `ghidra.log` and `script.log`
   of every NEW `/tmp/rea-ghidra-*` dir into `DIR/logs/<dirname>/` (copy to `.tmp` then `os.replace`),
   counting polls and recording the last successful copy time and byte size. Never touch other dirs' files
   beyond reading. Same for each `--search NAME` step: `npx -y rea-agents@V search CARRIER --pattern NAME
   --kind procedures --format json` (verify exact flags with `rea search --help`; record argv as run).
4. pins.snapshot post; pins.compare.
5. `DIR/receipt.json`: label, carrier {path, sha256 pre/post}, every step {argv, cwd, started/ended utc,
   exit, stdout/stderr path+sha256}, retained logs [{session_dir, files {name: {path, sha256, bytes}},
   polls, last_copy_utc}], analyze `evidence_id` parsed from stdout JSON if present, pins pre/post/compare,
   `python`, `orig_argv`, `log_capture_limit`: "polling copy; lines written after the final poll before
   REA deletes its runtime root can be missing".
Exit 0 all steps ran (REA nonzero exits are recorded, not hidden: exit 2 if analyze exit != 0),
1 pins differ, 2 could-not-evaluate.

## W/tools/log-extract.py
`log-extract.py --log GHIDRA_LOG` -> `{log_path, log_sha256, language_compiler (from "Using
Language/Compiler: X" or null), go_lines: [{line, level, component, message}], untested_versions: [..],
snapshot_labels: [..] (from "Using Go API snapshot for X" and "Using Go API snapshot for version X"),
go_version_logged: [..] ("Go version X"), missing_bootstrap: bool, analyzer_errors: [messages with level
ERROR from Golang*], classification}`. Go lines = component in {GoRttiMapper, GoApiSnapshot,
GolangSymbolAnalyzer, GolangStringAnalyzer, GoTypeManager, GoFunctionFixup, GoFunctionMultiReturn} or
component starting with `Go`/`Golang`. classification: `bootstrap_missing` if missing_bootstrap,
`snapshot_loaded` if any snapshot label and not missing, `no_go_analysis` if no go lines, else `other`.
Line format observed: `YYYY-MM-DD HH:MM:SS LEVEL  (Component) message  ` (trailing spaces).

## W/tools/predict.py
`predict.py --go-version STR [--goos linux --goarch amd64] --golang-root DIR` where STR is REA
`inspect-go-binary` `normalized_result.build_info.go_version` (e.g. `go1.27.2-X:nodwarf5`, `go1.23.12`, ``).
Normalize exactly as Ghidra's `GoVer.parse`/`fromVersionString` would (read the S003 member
`ghidra/app/util/bin/format/golang/GoVer.java` or wherever GoVer lives in Base-src.zip; cite lines). Then
call r16 `select_snapshot(root, "M.m.p", goos, goarch)` imported from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py`. Output
`{input, normalized, in_declared_range (GoRttiMapper.java:79 "1.15-1.25"), selection (r16 dict),
expected: {untested_version: str|null, snapshot_label: str|null, missing_bootstrap: bool}, basis: [source
anchors]}`. `missing_bootstrap` predicted true iff selection status is `missing_base` (EMPTY snapshot),
`snapshot_label` predicted as the normalized requested label (not selected file) when a base exists.
Empty/unparseable version -> exit 2 with reason, never a guess.

## W/tools/compare.py
`compare.py --prediction P.json --observation O.json` (O = log-extract output) -> per field
`{field, predicted, observed, match}` for untested_version (observed list contains predicted, or
both empty), snapshot_label, missing_bootstrap; exit 0 all match, 1 any mismatch, 2 invalid input.

## W/tools/invocation-audit.py  (R16-INVOCATION counting)
`invocation-audit.py --root LANE --rev REV` reads Git objects only (`git show REV:path`). Registry rows =
SKILL.md table rows whose 2nd cell matches `(probe|gate|tool) / kaidoku`. Command = first backticked
span in the 3rd cell. Receipts = every `verification.json`, `final-recheck.json`, `*receipt*.json`,
`gate-results.json` under `.ufo/` at REV; an exercised argv = any JSON array of strings under a key
named `argv` (or `orig_argv`) — join with spaces. Row classes: `exercised_match` (normalized command,
placeholders `<...>` as wildcards, equals some exercised argv modulo leading `python3`/interpreter path),
`labelled_unexercised` (row text contains `unexercised`), `unlabelled_variant` otherwise. Output
`{rev, rows:[{name, command, class, matched_receipt}], counts}`. Exit 0 reported, 2 could-not-evaluate.

## W/tools/temporal-sweep.py  (R16-PROVENANCE counting)
`temporal-sweep.py --root LANE --rev REV [--extra ABS_FILE]...`. Sites = lines in LOG.md, SCORECARD.md,
corpus/lessons/round-16.md, SKILL.md, `.ufo/waves/round-16/verification.json` at REV matching
`(?i)(unchanged during|remained unchanged during|stable throughout|pins_unchanged_during_run)`.
A site is `corrected` iff some line at REV in LOG.md, SCORECARD.md or corpus/lessons/round-17.md (or an
`--extra` file) contains `R16-PROVENANCE` and the site's repo-relative path. Output sites with
file:line, text, corrected; counts {sites, corrected, unqualified}. Exit 0 reported, 2 could-not-evaluate.

## W/tools/buildinfo-probe.py
`buildinfo-probe.py PATH` -> independent stdlib reader of the Go build-info blob: find
`\xff Go buildinf:` (16-byte aligned search as Go's debug/buildinfo does), decode flags (ptr size,
endianness, inline-string bit 0x2), read varint-prefixed inline version/modinfo strings (Go >= 1.18),
report `{path, sha256, header_offset, flags, ptr_size, inline, go_version, modinfo_first_line,
limitations}`; pointer-format (pre-1.18) -> report `pointer_format` and stop (exit 0, version null);
no magic -> exit 0 with `found:false`. Cite Go source `src/debug/buildinfo/buildinfo.go` lines.

## W/tools/receipt-validate.py
`receipt-validate.py RECEIPT.json...` recomputes every recorded file sha256, re-runs pins.compare on
recorded pre/post, checks required fields; exit 0 valid, 1 invalid (lists findings), 2 unreadable.

## W/tools/carrier-census.py
`carrier-census.py --out FILE PATH...` for each given path: sha256, size, `file`-style ELF check by
magic, `npx -y rea-agents@6.5.0 inspect-go-binary PATH --format json` go_version + evidence_id, and
`pacman -Qo PATH` owner string (read-only query; never any other pacman op). Exit 0.

## W/measure.py and W/controls.py
`measure.py REV` (Git objects only): presence of each tool above, knowledge entry
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, QUALITY row 19, SCORECARD capability row
text `retained REA Ghidra-session log`, SKILL registry rows for new tools, retained run receipts
`W/runs/*/receipt.json` count, SOURCES row count/tier/status histograms, README map tokens vs knowledge
files. `controls.py BEFORE AFTER`: generalize `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/controls.py`
(old LOG prefix retained; all old lessons/knowledge prefixes retained; prior `*-verifier-spotcheck.md`
byte-identical; pre-existing `.ufo/waves/**` and `evidence/**` blobs byte-identical; QUALITY rows 1-18
unchanged), retaining argv/orig_argv and resolved revisions.
