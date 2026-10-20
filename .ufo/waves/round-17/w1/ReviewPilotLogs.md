# W1 review — round-17 pilot logs: observation vs inference

Seat `KaidokuR17.ReviewPilotLogs-3`, author-side advisory. Read-only; no REA `analyze`/`search`/`decompile`,
no Ghidra, no carrier execution (two `rea inspect-go-binary` reads, explicitly permitted by the wave
contract). No installs; no tool upgrades needed.

Paths: `P` = `.ufo/waves/round-17/pilot`, `C` = `.ufo/waves/round-17/contract.md`, `S` = the Ghidra
12.1.4 source archive `Ghidra/Features/Base/lib/Base-src.zip`. Findings are tagged [obs] (observed in
the artifacts or source) or [inf] (inference; basis stated).

## 1. Integrity I re-ran

- `sha256sum -c P/SHA256SUMS` → **all 6 entries OK, exit 0** (`esbuild-0.25.12-log/{ghidra,script}.log`,
  `shfmt-log/{ghidra,script}.log`, `esb.json`, `shfmt.json`). [obs]
- Carrier identity agrees across four channels [obs] — README prose, REA's own `subject.digest.sha256`,
  Ghidra's import-time MD5 recorded in the retained log, and the bytes on disk now:

| carrier | `P/README.txt:7-8` | `subject.digest.sha256` (`esb.json`/`shfmt.json`) | Ghidra import MD5 in log | on disk now |
|---|---|---|---|---|
| shfmt | `58f76563…b459` | same | `caacf2c8…0070` @ `P/shfmt-log/ghidra.log:64` | sha256+md5 same |
| esbuild 0.25.12 | `bab29b2c…7014` | same | `c0601045…1717` @ `P/esbuild-0.25.12-log/ghidra.log:55` | same |

- The imported copy name embeds `sha256[:12]`: `target-58f765638eed.bin` (`P/shfmt-log/ghidra.log:46`),
  `target-bab29b2ca7a9.bin` (`P/esbuild-0.25.12-log/ghidra.log:46`). [obs] This is a usable in-band
  log↔evidence binding (see P8).
- The surviving scratch dir `/tmp/kr17-pilot/logs{,2}/rea-ghidra-*/` is **byte-identical** to the retained
  logs and JSONs (identical sha256), with copy mtimes `10:17:57.12` and `10:19:54.46` — within ~1 s and
  ~1.5 s of the last logged second (`10:17:56`, `10:19:53`). `/tmp/kr17-pilot/before.txt` and `before2.txt`
  are **0 bytes**, created at each run's start (`10:17:27`, `10:18:19`): the pre-pin step left a physical
  trace and recorded nothing. [obs]
- Version strings confirmed by permitted `inspect-go-binary`: shfmt `go1.27.0-X:nodwarf5`,
  esbuild `go1.23.12`; `build_info.settings` is absent in both REA results. [obs]

## 2. Findings, by severity

### P1 [high, calibration] The contract's normalization cannot consume REA's own version string

`C:65-66` tells the implementer to "Normalize exactly as Ghidra's `GoVer.parse`". Applied literally to
REA's `go1.27.0-X:nodwarf5`, `GoVer.parse` yields **INVALID**, not `1.27.0`: its first act is
`s.replaceAll("[^.0-9].*$", "")` (`S:ghidra/app/util/bin/format/golang/GoVer.java:64-65`), which strips
from the leading `g` to end → empty string → `parts.length < 2` → `INVALID` (`GoVer.java:66-68`).

The pilot shows the actual chain: Ghidra strips the `go` prefix first
(`S:…/golang/GoBuildInfo.java:488-490`), then parses, producing exactly `Untested Go version [1.27.0]`
(`P/shfmt-log/ghidra.log:83,87`) and `Using Go API snapshot for version 1.23.12`
(`P/esbuild-0.25.12-log/ghidra.log:64`). [obs]

Consequence: an implementation that follows `C:65-66` literally returns INVALID for **every** carrier and
must take `predict.py`'s "unparseable → exit 2" path — the wave's central prediction is never emitted.
The contract must name the prefix strip (`GoBuildInfo.java:488-490`) before the `GoVer.parse` regex.

Secondary, same finding: the `1.15-1.25` range is a **log-only** gate (`GoRttiMapper.java:170-172`; it
emits `Msg.error` and continues). The observed failure cause is different in kind: `GoApiSnapshot.get`
derives the base name `go1.27.0.json` then `go1.27.json`, finds neither, returns `EMPTY`
(`S:…/rtti/GoApiSnapshot.java:105-115, 122-126, 183-189`; the data dir has `go1.15.0.json` …
`go1.25.0.json` and no 1.27 entry), and the mapper then throws because
`apiSnapshot.isInvalid()` (`GoRttiMapper.java:356-360`). `C:71-72` already keys `missing_bootstrap` on
selection status — correct — but `claims.json` C2's prose ("out-of-range go1.27.x") frames the range as
causal. It is not; the causal premise is snapshot-file availability.

### P2 [high, calibration] `analyzer_errors` drops the cause; `go_version_logged` gains a phantom

- `C:55-56` defines `analyzer_errors` as ERRORs "from `Golang*`". The pilot's decisive ERRORs are from
  **`GoRttiMapper`** (`P/shfmt-log/ghidra.log:83,87`). Under the literal prefix they are excluded, leaving
  only the two downstream symptoms `Go symbol analyzer error: unable to get GoRttiMapper` (`:85`) and
  `Go string analyzer error: …` (`:89`). The field named "analyzer errors" would omit the version-gate
  error and keep its consequences. Recommend reusing the `go_lines` component rule verbatim, or an explicit
  set including `GoRttiMapper`/`GoTypeManager`.
- `C:55` defines `go_version_logged` as `("Go version X")`. In the failing carrier the only occurrences of
  that substring are inside `Untested Go version [1.27.0]` (`:83`, `:87`). A literal regex/substring
  implementation yields `["[1.27.0]", "[1.27.0]"]` instead of `[]`. The genuine line
  (`GolangSymbolAnalyzer.java:139`) exists only on success — `P/esbuild-0.25.12-log/ghidra.log:67`. Anchor
  extraction to level INFO **and** component `GolangSymbolAnalyzer`.

### P3 [high, depth] The component allowlist discards exactly the deepest Go outcomes

`C:56-58` keeps components in `{GoRttiMapper, GoApiSnapshot, GolangSymbolAnalyzer, GolangStringAnalyzer,
GoTypeManager, GoFunctionFixup, GoFunctionMultiReturn}` or starting `Go`/`Golang`. In the successful
carrier the log attributes four Go-analysis outcomes to `*BackgroundCommand` classes, so all four are
dropped: [obs]

| line | component | message |
|---|---|---|
| `P/esbuild…/ghidra.log:80` | `PropagateRttiBackgroundCommand` | `Go RTTI callsite fixup info (total/updated/skipped): 9908/9798/2` |
| `:81` | `FixClosureFuncArgsBackgroundCommand` | `Go closure/method wrapper types found: 174/14` |
| `:82` | `FixClosureFuncArgsBackgroundCommand` | `Go closure/method wrapper funcs fixed: 214/16` |
| `:84` | `FixGcWriteBarrierFlagBackgroundCommand` | `runtime.writeBarrier flag candidates: {…}` |

These are emitted by `GolangSymbolAnalyzer` code (`S:…/GolangSymbolAnalyzer.java:779, 882, 884, 1110`) but
logged under the background-command class. They are the only quantitative Go outcomes beyond counts, i.e.
the evidence C2 is buying. Additionally, the `AutoAnalysisManager` table is the *only* record that the
deferred duffzero/duffcopy fixup ran — `P/esbuild…/ghidra.log:106` — and the contract ignores the table
entirely. As written, `log-extract.py` would under-deliver C2's "extract the Go analyzer diagnostics".

### P4 [high, provenance] The retained logs are provably tail-truncated, not merely at risk

Both files stop mid-sequence, at points whose successors are known from source: [obs]

- shfmt, last line `P/shfmt-log/ghidra.log:125` = `ANALYZING changes made by post scripts: …`
  (`HeadlessAnalyzer.java:1122`). The next terminal record, `REPORT: Post-analysis succeeded for file:`
  (`HeadlessAnalyzer.java:1130`), plus the save records (`:1223`, `:1619`), are absent.
- esbuild, last line `P/esbuild-0.25.12-log/ghidra.log:123` = `SCRIPT: …ReaGhidraBridge.java`
  (`HeadlessAnalyzer.java:581`). The bridge script's own execution, post-analysis (`:1122`/`:1130`) and
  save are all absent — this session lost more than shfmt's.

Neither retained log contains a session-completion marker, so the logs do **not** show that either session
closed cleanly; the only completion evidence is the unpinned 7-byte exit files (P6). `C:46`'s
`log_capture_limit` is therefore a deterministic loss of the terminal phase at close, not a rare race.
The exact loss is unknowable from the pilot (only that lines after the final copy are gone). [inf, from
source ordering + copy mtimes]

### P5 [medium, calibration] Duplicate emissions are structural; `compare.py` semantics are underspecified

Two independent mapper reads per analysis (`P/shfmt-log/ghidra.log:82-85` and `:86-89`; the same
`Reading Go binary info` twice) mean both list fields are 2-element in both carriers: `untested_versions`
= `["1.27.0","1.27.0"]`, `snapshot_labels` = `["1.23.12","1.23.12"]` (the latter from
`GoApiSnapshot.java:163` and `GoRttiMapper.java:179-180`, which word the line differently — `C:54` already
anticipates both forms). [obs]

`C:77-78` grants "contains" semantics only to `untested_version`; `snapshot_label` match semantics are
unspecified. A naive equality check fails on the **successful** carrier. Specify contains/dedupe for both.

Deeper: the label cannot identify the snapshot *file*. `GoApiSnapshot.get` passes the **requested** `goVer`
into `read` (`S:…/rtti/GoApiSnapshot.java:111`) and `read` stores it as `ver` (`:494-500`), so `getVer()` —
the value printed at `GoRttiMapper.java:179-180` — always equals the requested version, even when the data
came from a lower base JSON because no patch diff existed (`:128-131`, warned only at `:158-161`). The
esbuild carrier happens to have an exact `go1.23.12.json.diff`, so exact and fallback are indistinguishable
in this pilot. If the wave wants to distinguish "exact snapshot" from "base fallback",
`log-extract.py` must capture the `Falling back from X to Y` WARN as its own field; otherwise every in-range
carrier looks identical to the model.

### P6 [medium, provenance] `SHA256SUMS` omits the claims and the exit records

6 of 12 files covered. Not covered: `README.txt` (all prose claims: argv, carrier ids, polling design,
"no keep knob"), `SHA256SUMS` (cannot self-cover), and all four `esb.err`/`esb.exit`/`shfmt.err`/
`shfmt.exit`. Those four are the only evidence of exit 0, and the two exit files are byte-identical
(`19eaf438…`), so even pinned they identify a run only by filename. [obs] Recommendation: pin `README.txt`
and fold the child exit into the JSON receipt (the contract already does this in `carrier-run.py`) rather
than relying on sidecar files.

### P7 [medium, calibration] Evidence carries no toolchain identity or timestamp — but the run pair is configuration-identical

[obs] `environment` is `null` in both JSONs, there is no `taken_at` field, and the substring `6.5.0` appears
in neither — the rea-agents version exists only in `P/README.txt:2-3` and the npx path
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/…` (identical in both logs, so the same cached instance served
both). Ghidra 12.1.4 *is* recorded in `analysis_profile…upstream_analysis_profile.provider.version`.

Positive and worth preserving: the two evidence records share byte-identical `analysis_profile.digest`
`254cb0a0…` and parameters digest `9c7f6b24…`, and both declare `language_id: auto-from-header` /
`analyzer_preset: ghidra-default`. The differing Go outcome is therefore attributable to the carrier, not
to a profile difference — the strongest same-identity check the pilot offers.

Gap that survives into the final runs: `C:34` pins the carrier and the r16 `selection.py` only. The Ghidra
install, the rea-agents package, and the Go data dir (explicitly "NOT pinned") are unpinned, yet the
deciding input for the 1.27 outcome is precisely the absence of a `go1.27.*` entry from that data dir.

### P8 [medium, calibration] Capture is not bound to the child session; the logs supply cheap binding tokens

`P/README.txt:4` and `C:37-38` copy from "every NEW `/tmp/rea-ghidra-*` dir". In the pilot the two sessions
were sequential and disjoint (roots `LuPZRm` 10:17:28–10:17:56, `r9xmGu` 10:18:19–10:19:53; 23 s apart), so
no mixing occurred — but the collision case was never exercised, so the procedure's safety is untested. A
concurrent sibling run would let a poll attribute another session's log to this carrier. [obs + inf]

Cheap in-band checks the pilot proves available: `target-<sha256[:12]>.bin`
(`P/shfmt-log/ghidra.log:46,64`; `P/esbuild…/ghidra.log:46,55`) and the log's self-path
`Using log file: /tmp/rea-ghidra-<root>/ghidra.log` (`:2` in both). `receipt-validate.py` should require
the former in the retained log and the latter to match the recorded `session_dir`.

### P9 [medium, depth — inference] A hardlink would close the polling gap

The log path is fixed at launch (`GhidraLauncher.js:448-450`, `ghidraLogPath =
join(runtimeRoot,"ghidra.log")`) and log4j writes it with a plain `RollingFile` whose only policy is a
50 000 KB size trigger (`Ghidra/Framework/Generic/lib/Generic.jar!log4j-appender-rolling-file.xml`); these
logs are ~11 KB, so no rollover occurs. A hardlink to `ghidra.log` taken at first sight would survive
REA's removal of the runtime *directory name* and keep receiving appends, yielding a byte-complete tail
with no polling gap. [inf, unexecuted] Falsifier: a capture that still lacks
`HeadlessAnalyzer.java:1130` and the save lines. Caveat: a >50 MB log rolls and renames, so the rolled
name must be linked too.

### P10 [low] `script.log` carries no information the `ghidra.log` lacks

In both runs `script.log` is one line whose message text is identical to the `GhidraScript` line in
`ghidra.log` (`P/shfmt-log/ghidra.log:122`, `P/esbuild-0.25.12-log/ghidra.log:121`). The bridge script
starts *after* it (`P/shfmt-log/ghidra.log:124`, `P/esbuild-0.25.12-log/ghidra.log:122`), so the pilot
cannot distinguish "bridge prints nothing" from "bridge output lost in the gap". Keep it as a loss
detector only; do not count it as independent evidence.

## 3. Observation vs inference, per claim

- [obs] Both ELFs were imported with language/compiler `x86:LE:64:default:golang`
  (`P/shfmt-log/ghidra.log:48`, `P/esbuild-0.25.12-log/ghidra.log:48`). This is the **only** artifact
  recording the resolved language — the evidence profile says `auto-from-header` — so the retained log
  carries information the pinned JSON does not.
- [obs] The pinned JSONs are `operation: binary_overview` only (`procedure_count`/`string_count`/segments),
  with 10 generic limitations and `environment: null`. They cannot corroborate any analyzer outcome; the
  retained log is the sole record of the analysis *process*.
- [obs] go1.27.0: `Untested Go version [1.27.0]` ×2, `Missing Go bootstrap type info` ×2, symbol+string
  analyzer ERRORs, **zero** snapshot labels.
- [obs] go1.23.12: both snapshot lines, `Go version 1.23.12`, `188 unindexed`/`4881` types, three subtype
  WARNs, `61` NoReturn, `2248` snapshot signatures, `2055` method signatures, `6264` strings, RTTI
  `9908/9798/2`, `19` missing type names.
- [obs] The failing carrier's Go analyzers still appear in the timing table with nonzero times
  (`P/shfmt-log/ghidra.log:106-107`), despite doing nothing. Timing-table presence is not evidence of
  analysis — a trap for any reader that summarises the table instead of the component lines.
- [inf] The go1.27 failure cause is the absent base snapshot (source chain in P1), not the range check;
  the log itself says only `Missing Go bootstrap type info`.
- [inf] The analyzed bytes are REA's ephemeral copy (`import_mode: ephemeral-source-immutable`), so
  path→content binding rests on REA's own read; there is no independent pre/post pin.

## 4. What the pilot cannot show

1. **Repeatability.** n=1 per carrier, no rerun of the same binary, and no third carrier: C2 also names a
   go1.20.12 build; the pilot has only 1.23.12. Timings, counts and log shape are single observations, and
   the two carriers differ in version *and* size, so no cell is replicated.
2. **Extraction branches.** No non-Go binary (`no_go_analysis` unexercised); no case where the base JSON
   exists but the patch diff does not, so the `Falling back from X to Y for Go API snapshot` WARN
   (`GoApiSnapshot.java:158-161`) is unexercised; and only one of the two bootstrap failures is seen —
   `Missing … type info` (`GoRttiMapper.java:358-360`), never `Invalid … struct mapping info` (`:364-365`).
3. **Polling.** No poll count or last-copy timestamp is recorded anywhere in the lane; the "1 s" cadence is
   prose, corroborated only by `/tmp` mtimes, and the number of lost lines is unknown.
4. **Pins.** No pre/post snapshot (`P/README.txt:6` says so; the empty `before*.txt` files confirm it).
   Content identity is *not* zero — REA's sha256 and Ghidra's MD5 both agree with the present bytes — but
   nothing shows stability *during* the run, and nothing is independent of REA.
5. **argv.** The esbuild path is elided in `P/README.txt:3` and no `argv` array exists, so the run cannot be
   replayed from a receipt or matched by `invocation-audit.py`.
6. **Clean completion.** No save/close records; the exit files are unpinned, unlabelled, and mutually
   identical.

## 5. Residual risk and my own verification gaps

- I did not run REA `analyze`/`search`/`decompile`, Ghidra, or any carrier; the session narrative is read
  from logs plus source.
- "1 s polling" and `cp -f` are README claims; I verified only their footprints (byte-identical copies at
  `10:17:57.12` / `10:19:54.46`), not the loop itself.
- I did not verify REA's runtime-root deletion code path; I only observed that no `/tmp/rea-ghidra-*`
  exists now while `/tmp/kr17-pilot` does.
- P9 is an unexecuted design inference, not a demonstrated capability.
- Residual risk: if the L1 treats the retained logs as the session transcript (rather than as a prefix),
  it will over-claim completion and under-count Go analysis on the failing carrier (P3, P4).

## 6. Searched, no finding

- No torn final line: both logs end on a well-formed record with the documented trailing spaces.
- No cross-session interleaving: the two runtime roots and their time intervals are disjoint.
- No stderr: `esb.err` and `shfmt.err` are 0 bytes.
- No divergence between the `/tmp` scratch copies and the retained pilot copies (all six sha256 equal).
- `P/README.txt:5`'s env-knob list is exactly right for the cached package: the only `REA_GHIDRA_*` names in
  the whole `rea-agents` 6.5.0 tree are the six it lists; no retain/keep knob exists. The conclusion "the
  log cannot be kept via env" is therefore sound for 6.5.0.
- The npx-cached package reports `rea-agents 6.5.0` (`package.json`), matching the argv string.
