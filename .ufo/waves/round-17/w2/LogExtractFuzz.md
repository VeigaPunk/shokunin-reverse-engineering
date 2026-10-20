# LogExtractFuzz — adversarial fixture attack on `tools/log-extract.py` (WAVE 2 / FALSIFY)

Seat: KaidokuR17.LogExtractFuzz (executor leaf; no dispatches, no labrat used).
Target: `.ufo/waves/round-17/tools/log-extract.py`, worktree sha256
`41b2c08068a7c619134c8f6f4abda7fe5e07db4c179f86793a26e84909109429`
(lane rev da64646; file last committed at 2711674, worktree clean).
Attack script: `.ufo/waves/round-17/w2/log-extract-attack.py` (new, this seat).
Ground truth: installed `Base-src.zip` (ghidra_12.1.4_PUBLIC), cited per-finding.
Run: `python3 -B .ufo/waves/round-17/w2/log-extract-attack.py` → 28 fixtures,
exit 0, every case output = its script-pinned expectation (0 unexpected diffs).
Verdicts: 6 CLEAN / 12 WEAK / 10 DEFECT. Fixtures kept under
`/tmp/log-extract-attack-*/`.

All fixture claims below are `[observation]` of parse_log output; emission
claims cite the installed Java source.

## Findings

### D1. Unicode line-separator injection forges whole records — carrier-controlled [observation + Java-verified channel]

`text.splitlines()` (log-extract.py:144) splits on every Unicode line
boundary — `\x0b`, `\x0c`, `\x1c-\x1e`, `\x85`, U+2028, U+2029 — not just
`\r\n`/`\n`. `LINE_RE` (:68-70) then accepts the suffix as a new record.
A Go carrier's file name becomes `program.getName()` and lands verbatim in
`"Reading Go binary info: %s"` (GoRttiMapper.java:106); the carrier's raw
build-info version string lands verbatim in
`"Invalid Go version string [%s]"` (:168). Both are carrier-controlled and
can contain U+2028, letting ONE physical emitted line materialize as TWO
synthetic records.

Observed: fixture `u2028_injection` (name `target<U+2028>`) → a second
`GoRttiMapper` record is produced and `untested_versions=["9.9.9"]`.
Fixture `vtab_injection` → `missing_bootstrap=true`,
`classification="bootstrap_missing"` on a log where no analyzer ever
emitted bootstrap failure. Impact on C2: `compare.py`'s
"observed list contains predicted" would report `match:true` for
fields the analyzer never wrote — a receipt-level false positive.

### D2. `startswith("Go")` component overmatch + un-gated label regexes → forged labels/classification/route-inconsistency [observation]

`_is_go_component` (:97-103) admits ANY component starting `Go`. But
`SNAPSHOT_RE`/`UNTESTED_RE`/`missing_bootstrap` run on every go_line
(:178-191), while route gates on exact `GoApiSnapshot` (:196).
Observed `component_lookalikes`:
`INFO (GoApiSnapshotX) Using Go API snapshot for 9.9.9` +
`INFO (GovernorOfGo) Using Go API snapshot for 7.7.7` →
`snapshot_labels=["9.9.9","7.7.7"]`, `classification="snapshot_loaded"`,
`snapshot_route="none"` — violating the tool's own :76-80 comment that
only GoApiSnapshot discriminates. `untested_injection`: a `GoatAnalyzer`
WARN forges `untested_versions`. Control `NotGoApiSnapshot` correctly
excluded. Emitter universe in installed source confirms the genuine
emitters are exactly {GoApiSnapshot, GoRttiMapper, analyzers} — no
`GoApiSnapshotX`/`GovernorOfGo` exists; a hostile or renamed plugin
component (or a line injected via D1) still matches.

### D3. Route/label/classification divergence on lawful-ish shapes [observation]

- `api_info_version_phrasing`: `INFO (GoApiSnapshot) Using Go API
  snapshot for version 1.23.12` → `snapshot_route="none"`,
  `api_snapshot_info_labels=[]`, yet `snapshot_labels=["1.23.12"]`,
  `classification="snapshot_loaded"`. `API_INFO_RE` (:82) lacks the
  `(?:version )?` guard `SNAPSHOT_RE` (:73) has and requires `\s*$`;
  same fact, three disagreeing fields. (The phrased form is not the
  current emitter text; brittle against any future/lower-level re-emit.)
- `fallback_only_truncated` / `fallback_warn_only_noecho`: a log cut
  between `GoApiSnapshot.java:160` (WARN emit) and `GoRttiMapper.java:180`
  (echo emit) — a window `carrier-run.py`'s `log_capture_limit` text
  admits is real (poll gap / CancelledException at :183-185) — yields
  `snapshot_route="fallback"`, `snapshot_labels=[]`,
  `classification="other"`. A provably-loaded snapshot classifies as
  "other", and `compare.py` mismatches the predicted requested label on a
  truthful retained log. Even in the complete log, `snapshot_labels`
  records the *requested* `1.25.8`; the authoritative selected `1.25.0`
  lives only in `snapshot_fallbacks[].to`.

### D4. `no_go_analysis` misclassification is reachable in-lane [observation]

- `empty_file` → `classification="no_go_analysis"`, identical to a
  genuine non-Go run; no emptiness/truncation signal exists.
- `pilot_truncated_pre_go`: REAL retained pilot log
  (`pilot/shfmt-log/ghidra.log`) truncated at line 81, one line before
  the first GoRttiMapper record (:82) → `no_go_analysis` with
  `language_compiler="x86:LE:64:default:golang"`. A retained copy that
  lost its tail (poll race) reports "no Go analysis ever ran" for a
  go1.27 bootstrap-failure carrier — false headline on the exact
  evidence this lane retains.

### D5. `.search` over every record forges provenance fields [observation]

`LOG_FILE_RE`/`IMPORT_RE` run `.search` on every parsed message with no
component/anchor gate (:156-163). `log_file_injection`: an unrelated
component's message mentioning the phrases sets
`log_file_line="/tmp/attacker.log"`, `import_target="/etc/passwd"`.
Also observed on the pilot log: `log_file_line` reports the *original
deleted* `/tmp/rea-ghidra-*/ghidra.log` path, not the retained copy —
semantics worth a caveat wherever it is consumed.

### WEAK (brittleness/absorption, silent; no defect flag anywhere)

- `LINE_RE` literal-shape assumptions (`:68-70`): tab after LEVEL
  (record dropped; surviving lines mask as `other`), tab after
  `(Component)` (record dropped → `no_go_analysis`), millisecond
  timestamp `10:47:46.123` (ALL records dropped → `no_go_analysis` on a
  complete log), `)` inside component name, UTF-8 BOM (first record
  dropped → `language_compiler=null`).
- `level_spoof`: level never checked by `FALLBACK_RE`/`API_INFO_RE`
  (:196-202): WARN "Using Go API snapshot…" enters
  `api_snapshot_info_labels`; INFO "Falling back…" enters
  `snapshot_fallbacks` → `route="conflict"` on level-contradicting text.
- `warn_extra_text` vs `api_info_version_phrasing`: FALLBACK accepts
  unanchored trailing text into route; INFO with trailing text is
  dropped from route but still labeled — asymmetric, unflagged.
- `info_warn_conflict`: two legitimate same-log events (two programs /
  sessions: INFO for A, WARN fallback for B) collapse to `conflict`;
  no per-attempt scoping (:222-229).
- `bootstrap_plus_snapshot`: any bootstrap text anywhere overrides to
  `bootstrap_missing` (:212-219) even with snapshot evidence present.
- `bootstrap_substring`: unanchored substring at :190, no level/emitter
  check (real emitter is WARN via GoRttiMapper.java:115 relaying :359).
- `language_compiler_first_wins`: first match anywhere wins
  (:152-155); multi-program log reports gcc though Go lines exist.
- `non_utf8`: `errors="replace"` (:127) folds invalid bytes to U+FFFD
  silently into `untested_versions`.

### CLEAN confirmations (held under attack)

CRLF endings identical to LF; stack-trace continuations dropped (incl.
a `Caused by: … Missing Go bootstrap type info` continuation correctly
NOT setting `missing_bootstrap` — record-only detection); version
suffixes (`1.25rc1`, `1.25.0-beta.1`, `devel go1.26-abc +dirty`,
`1.27.0-X:nodwarf5`) pass through verbatim; 1MB+ message line parses
fine; CLI exit 0; `NotGoApiSnapshot` excluded; fallback `from/to`
captured correctly.

## Bottom line for C2 calibration

The extractor is correct on the three shapes the lane exercised, but its
fields are not source-faithful under four pressures that matter here:
(1) carrier-controlled Unicode line boundaries forge records (D1) —
the only finding a real analyzed binary can trigger end-to-end;
(2) label/classification fields do not share route's emitter gate (D2/D3);
(3) truncation = `no_go_analysis` (D4), an admitted poll-race shape;
(4) un-gated `.search` fields are freely forgeable (D5). Any
compare.py-driven match on untested/snapshot fields should be read as
"message text matched", not "the named analyzer emitted it".
