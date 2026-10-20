# ReviewR4Observation — R4's Go 1.26 / `Missing Go bootstrap` claims, and what a go1.27 observation is worth

Seat: KaidokuR17.ReviewR4Observation-3. Read-only; baseline `b563c799d97774aae4351276fe43cb897311e349`.
No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution. One allowed
`rea inspect-go-binary /usr/bin/shfmt` was run (cited below). `R4` =
`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`.

Axes named: **calibration** (is the new observation cited at the strength it supports?),
**depth** (does it pin the mechanism, or restate a message?), **retention integrity**
(cited source vs retained source).

## A. What R4 actually claimed

### A1. Measurement, Go 1.26 / 1password-cli
- `R4:19` target table: `1password-cli` 2.34.1-1 → 2.40.0-2, member `usr/bin/op`,
  41,210,040 → 43,475,106 B, sha256 `d24dc5d4…` → `8d029d2c…`, "ELF x86-64 static,
  stripped Go (**go1.25.7 → go1.26.8**)".
- `R4:29` overview: 11,595 procedures / 76,338 strings / 16 segments on 2.40.0 vs
  33,060 / 76,550 / 18 on 2.34.1. `R4:33`: `search "main.main"` → 0 hits on 2.40.0;
  `R4:34`: full inventories 33,060 vs 11,595 rows. `R4:36`: 2.40.0 entry dossier is
  named `entry` at ELF entry `0x491f20`.
- `R4:69-70`: "only 11,595 procedures recovered, 11,588 of them `FUN_*`/`thunk_FUN_*`
  auto-names; the sole real name is `entry`."
- `R4:186-189` summary generalizes: "**a Go toolchain bump silently collapses provider
  symbol recovery** — 99.94% of 2.40.0 procedures are `FUN_*`…".

### A2. The causal sentence and the bootstrap line
- `R4:70-71` (the causal clause): "Ghidra 12.1.4's Go / analyzer cannot parse the Go 1.26
  moduledata/pclntab layout".
- `R4:71-73` (its evidence, the parenthetical): "(transient / `Missing Go bootstrap type
  info, unable to extract Go RTTI info` seen in its / `ghidra.log` during the session —
  dir since deleted, so this is observed-not-cited)." The message is therefore quoted
  *as corroboration* of the moduledata/pclntab parse-failure claim, while being marked
  unretained.
- `R4:116-118` repeats the same coupling in the candidate's `suggested:` line: "the
  toolchain-version link is corroborated by embedded `go1.26.8`/`go1.25.7` strings and a
  transient Ghidra Go-bootstrap log line (session dir since GC'd — flagged honestly)."

### A3. What R4 itself already divides
- `R4:196-211` (Round-14 appendix) supersedes the causal sentence at `R4:70-73`; the
  original cause is **UNKNOWN** (`R4:203`); "Historical numeric outputs and the caution
  against symbol-only pairing are preserved" (`R4:210-211`). `R14` =
  `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, whose own correction at
  `R14:83-90` binds the same lines.
- Net current claim set: the **inventory/naming collapse is retained measurement**; the
  **layout-parse attribution is withdrawn**; the **bootstrap line is retained only as an
  unretained observation, no longer as mechanism evidence**. `R4:116-118`'s coupling of
  that line to the "toolchain-version link" was not separately amended (see F2).

## B. Verdict: correction, confirmation, or different case

**Different case.** It is neither a correction of R4 nor a confirmation of R4's claim.
It *is* an out-of-sample confirmation of the R14/R15 source model (a different
proposition, different scope), and the first **retained** witness of that class.

1. **Not a correction.** The only R4 sentence it bears on (`R4:70-73`) is already
   superseded in place by `R4:196-211`. There is no current R4 text for a new run to
   correct. A draft sentence such as "go1.27 confirms R4" would itself be the defect.
2. **Not a confirmation of R4.** Every identity dimension differs: carrier
   `/usr/bin/shfmt` 3,601,168 B sha256 `58f7656…` vs `op` 43,475,106 B (`R4:19`);
   `go1.27.0-X:nodwarf5` vs `go1.26.8`; REA 6.5.0 vs 6.4.0 (`R4:6`); retained logs vs a
   deleted one (`R4:73`). R4's distinguishing measurement is a procedure-name inventory
   (11,588/11,595 `FUN_*`); the pilot retains **no name inventory** — `procedure_count
   2581` (`pilot/shfmt.json` normalized_result) is not a naming statistic. Even the
   coarse measurement is not replicated.
3. **Same mechanism class, third instance.** With installed data bases 1.15–1.25
   (`ls …/data/typeinfo/golang/`: `go1.15.0.json` … `go1.25.0.json`; `R15:63-64,68`),
   go1.27.0 has no base (`w1/selection-1.27.0.json`: `status: missing_base`). R4's
   go1.26.8 side also has no base (`R15:68`; no 1.26/1.27 patch diffs, `R15:64`). So the
   pilot is a *same installed-data class* instance as `op` 2.40.0 — with the log R4
   lacked — not a new mechanism.
4. **What it does confirm.** The R14/R15 predicted chain for an out-of-range carrier:
   `GoRttiMapper.java:79` range 1.15–1.25 → advisory `Msg.error` only at `:170-172`
   (no throw) → `GoApiSnapshot.java:122-126` base gate returns null, `get` yields
   `EMPTY` at `:115` → constructor `:348` → `initStructMappings` `:351-361` throws
   "Missing Go bootstrap type info…" → `GolangSymbolAnalyzer.java:133-137` logs
   "unable to get GoRttiMapper" and returns false. The pilot log is that sequence
   verbatim: `pilot/shfmt-log/ghidra.log:82-85` (and again `:86-89` for the string
   analyzer). This is confirmation of the model at `R14:31-50` and `R15:17-19`, not of
   `R4:70-73`.

**Citation rule for the R17 entry (recommended wording):** "A retained go1.27.0 shfmt
session reproduces the predicted invalid-snapshot bootstrap sequence. It is a new
carrier instance of the diagnostic class recorded (unretained) at R4:71-73 and modelled
at R14:31-50/R15:17-19; it does not re-establish the historical `op` 2.40.0 cause, which
remains UNKNOWN (R4:196-211)."

## C. Findings by severity

**F1 — HIGH, calibration/depth: the bootstrap message is non-diagnostic for a
layout-parse failure, and the pilot demonstrates the shape.** `initStructMappings` is
called from the mapper constructor (`GoRttiMapper.java:348`) and throws at `:356-361`
*before* `GolangSymbolAnalyzer` reaches `getFirstModule` (`:148`) or `markupGoFunctions`
(`:155`); the analyzer has already aborted at `:133-137`. The shfmt log shows exactly
that order — `Untested` → `Missing Go bootstrap` → `unable to get GoRttiMapper`
(`pilot/shfmt-log/ghidra.log:83-85`) — and contains no `Go version 1.27.0` line (emitted
only after mapper success, `GolangSymbolAnalyzer.java:139`) and no `Go strings found:`
line (present on the in-range esbuild run, `esbuild-0.25.12-log/ghidra.log:83`). So a
run can emit the message with **zero** moduledata/pclntab work. This does not prove what
R4's run did; it proves the message cannot support `R4:70-73` either way. *Observation*
(log) + *inference from installed source* (ordering).

**F2 — MEDIUM, calibration of surviving text: `R4:116-118` still couples the bootstrap
line to the version link.** Under `R14:39-50` the line marks failed struct registration
with an invalid snapshot; it corroborates version→snapshot-coverage correlation, not a
parse refusal. Only `R4:70-73` is marked superseded (`R4:196-211`); the `suggested:`
clause at `R4:116-118` is not. If L1 wants it corrected, it needs a new named append —
do not silently re-read it.

**F3 — MEDIUM, drafting guard: overview `string_count` is not Go-string recovery.**
`pilot/shfmt.json` reports 7,813 strings while `GolangStringAnalyzer` aborted
(`pilot/shfmt-log/ghidra.log:89`; analyzer time 0.002 s at `:106`) and no
`Go strings found:` line exists. Esbuild, in range, does log `Go strings found: 6264`
(`esbuild-0.25.12-log/ghidra.log:83`) alongside `Go version 1.23.12` (`:67`). The same
caution applies to R4's 76,550→76,338 overview strings (`R4:29`): they are REA-defined
strings, not Go-analyzer output.

**F4 — MEDIUM, verification gap: the pilot does not establish name recovery on
go1.27.** `procedure_count 2581` says nothing about `FUN_*` share. The R17 run must add
a `search ".*" --kind procedures` step (contract `W/tools/carrier-run.py` `--search`) or
state "analyzer refused; recovery unmeasured". Inferring all-`FUN_*` is source-consistent
(`shfmt` has no `.symtab`; `file` reports "stripped") but is *inference*, not the
measurement R4:113-114 prescribes.

**F5 — LOW-MEDIUM, carrier comparability: shfmt is not a like-for-like `op` analogue.**
`inspect-go-binary` (`ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`)
gives `-buildmode=pie`, `CGO_ENABLED=1`, `-linkmode=external -compressdwarf=false`;
3.6 MB vs 41–43 MB; `.gnu_debuglink` → `shfmt.debug` (log `:79`) which is absent, so
DWARF analysis is skipped (`:81`). If the distro debug file is ever installed, DWARF
function names could mask Go-analyzer failure — record this profile with the run.

**F6 — LOW, positive: the observed label validates the `GoVer.parse` normalization.**
`GoVer.java:62-65` strips from the first character outside `[.0-9]`
(`replaceAll("[^.0-9].*$", "")`, comment "1.22.8 X:rangefunc"), so
`go1.27.0-X:nodwarf5` parses to `1.27.0`; the log proves it (`Untested Go version
[1.27.0]`, `pilot/shfmt-log/ghidra.log:83`). `predict.py` must implement this regex plus
the `<3 parts` → `missingPatchValue` rule (`:66-75`), not an ad-hoc suffix strip.

**F7 — LOW, wording: "transient" (`R4:72`) is a poor word.** The message recurs twice in
one session, once per mapper instantiation (`pilot/shfmt-log/ghidra.log:84,88`). If it
meant "not retained", say that; if it meant "one-off/flaky", the retained logs show the
opposite within a session.

## D. Residual risk and verification gaps

- R4's historical log is gone; no new observation can recover which branch the
  `op` 2.40.0 run hit. `R4:203`'s UNKNOWN stands and must not be upgraded by the pilot.
- The pilot ran REA 6.5.0 (R4 used 6.4.0) and recorded no pre/post carrier pins
  (`pilot/README.txt`). I verified all six pilot artifacts against `pilot/SHA256SUMS`
  (all OK) — that binds the files as shipped, not the run.
- The installed-data constraint is today's inventory; it is not proof that R4's runtime
  used identical data. The 12.1.4 install is the same package, so a differing data dir
  is possible but unrecorded.
- No runtime, rerouting, or saturation surface exists in this scope; nothing to verify
  there.
- Tool installs/updates: **none**. Commands used: `file`, `readelf`, `sha256sum`,
  `pacman -Qo` (read-only), `unzip`/`zipfile` on `Base-src.zip`, and one
  `npx -y rea-agents@6.5.0 inspect-go-binary` (explicitly allowed).
- Cross-citation check: no file in `corpus/` or `.ufo/waves/round-17/` currently cites
  the pilot as confirming R4; `w1/DraftReport.md:45` correctly says "Consistent with the
  C2 prediction", not "confirms R4". Keep it that way.

Report: .ufo/waves/round-17/w1/ReviewR4Observation.md
