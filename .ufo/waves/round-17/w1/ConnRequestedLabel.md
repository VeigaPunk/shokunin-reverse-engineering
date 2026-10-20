# Conn — "requested label" vs runtime `Using Go API snapshot for 1.23.12`

Scope: read-only. Primary evidence = retained pilot log, installed Ghidra source/data, r16
selection model, round-16/17 text. I ran no REA analyze/search/decompile, no Ghidra, no carrier
binary. One local read-only re-run of r16 `selection.py` (below). No installs/updates.
Labels: **OBS** = observed bytes/output; **INF** = inference from source or control flow.

## 1. Anchors verified

- **OBS** `corpus/lessons/round-16.md:21` is exactly the reject row:
  `| Requested-version label authenticates exact patch data | reject | Source passes original
  requested GoVer to `read` after lower-diff/base fallback; object label is not file identity |`
- **OBS** `pilot/esbuild-0.25.12-log/ghidra.log` (10973 B, sha256
  `f6b6115297915e7eaba5e6dc1165241166fb6c09ae521c7268095aeeda5d89a7`, = `pilot/SHA256SUMS:1`;
  `sha256sum -c` over all six entries exit 0):
  - `:63` `2026-10-20 10:18:20 INFO  (GoApiSnapshot) Using Go API snapshot for 1.23.12  `
  - `:64` `2026-10-20 10:18:21 INFO  (GoRttiMapper) Using Go API snapshot for version 1.23.12  `
  - `:67` `2026-10-20 10:18:21 INFO  (GolangSymbolAnalyzer) Go version 1.23.12  `
- **OBS** no fallback line anywhere: `grep -c 'Falling back'` = 0 in both pilot `ghidra.log`s.
- **OBS** carrier label: `pilot/README.txt:8` esbuild sha256 `bab29b…7014`, build info `go1.23.12`;
  `README.txt:1,6` say this is a pilot, not a measured run, with no pre/post carrier pins.

## 2. What each log line actually is (source law, OBS from `Base-src.zip`)

Member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`:

| line | code | meaning |
|---|---|---|
| 128 | `File patchDiffFile = getPatchVerDiffFile(goVer);` | selection begins; `goVer` is the *requested* version |
| 153-156 | `while (patchVer.getPatch() > 0 && (patchDiffFile = getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")) == null) patchVer = patchVer.prevPatch();` | first probe is the exact requested patch; only a miss decrements |
| 158-160 | `Msg.warn(..., "Falling back from %s to %s for Go API snapshot")` | emitted iff the loop moved |
| 163 | `Msg.info(GoApiSnapshot.class, "Using Go API snapshot for %s".formatted(goVer))` | emitted iff the loop did **not** move — the `:63` emitter |
| 136-140 | `JsonPatch.read(patchDiffFile)` / `JsonPatchApplier` / `monitor.initialize(..., "Patching Go API snapshot %s -> %s")` | patch read+apply happens **later**, lazily inside the derived `ByteProvider`; `monitor.*` is progress, not a log record |
| 111, 239 | `read(is, archSearchOrder, goVer)` → `new GoApiSnapshot(ver, results)` | the snapshot object stores the requested `goVer` as its label |
| 242 | `EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of())` | missing base ⇒ invalid label, mapper line suppressed |

`GoRttiMapper.java`: `:165` `GoVer goVer = buildInfo.getGoVer();`; `:170-172` out-of-range
`Untested Go version [%s]` is an ERROR that **does not return**; `:176-181`
`GoApiSnapshot.get(goVer,…)` then `Msg.info(…"for version %s".formatted(apiSnapshot.getVer()))`
(the `:64` emitter, gated on `!getVer().isInvalid()`); `:187,337,422` the mapper stores/returns the
same `goVer` that `GolangSymbolAnalyzer.java:139` prints at `:67`. `GoVer.java:155-158` renders a
numeric triple only (suffixes/missing patch collapse).
A scan of every `.java` member of `Base-src.zip` finds **exactly two** emitters of the literal:
`GoApiSnapshot.java:163` and `GoRttiMapper.java:180`.

## 3. What the runtime evidence now supports

1. **Exact-patch filename resolution ran for this carrier (OBS branch + INF).** `:63` is the
   `:163` INFO with a patch-12 label and no fallback WARN exists. By the `:158-164` condition, the
   *first* `patchverdiffs/go1.23.12.json.diff` probe succeeded. This rules out
   lower-diff fallback and base-only for this run.
   Tail-truncation does not weaken this: the WARN and the INFO are mutually exclusive emissions of
   the same call at the same instant, so a fallback would have replaced `:63`, not followed it.
2. **Source-model and runtime agree.** `w1/selection-1.23.12.json` (`status: exact_diff`,
   `selected_patch: 12`, diff `111215 B` sha256 `e1fdbc7e…b7a99c53`, base `go1.23.0.json`
   `9368866 B` sha256 `3b1d795f…f63692`). My independent re-run of the r16 argv
   (`python3 -I …/round-16/selection.py --root …/typeinfo/golang --request 1.23.12 --goos linux
   --goarch amd64`) printed identical fields. **OBS** installed tree contains exactly one
   `go1.23.12.json.diff`, at `Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/`.
3. **The three log lines are one label, not three witnesses (OBS source, INF value identity).**
   `:63` prints the requested `goVer`; `:64` prints `apiSnapshot.getVer()`, which `read():239`
   stored from that same requested `goVer` (`:111`); `:67` prints the mapper's build-info `goVer`.
   r16's third-column mechanism ("passes original requested GoVer to `read` … object label is not
   file identity") is therefore confirmed at the runtime surface.
4. **The snapshot object was non-empty and `read` completed (INF from control flow).**
   `:64` is suppressed for `EMPTY` (`:178` + `:242`); it appears, and no
   `Failed to read Go info`/IOException path is logged. This supports "base + selected diff stream
   was produced and parsed", but no log statement says the patch applied cleanly.
5. **The label is not even a byte-faithful echo of build info (OBS).** shfmt's build info is
   `go1.27.0-X:nodwarf5` (`README.txt:7`) while the GoVer label is the triple `1.27.0`
   (`GoVer.java:155-158`; `shfmt-log/ghidra.log:83` prints `[1.27.0]`). "Label" means normalized
   requested version, never file identity.

## 4. What remains unknown — including "which diff file was actually read"

- **U1 — identity.** The log names no path, module, size, or digest. **INF only** that
  `Base/data/typeinfo/golang/patchverdiffs/go1.23.12.json.diff` was the resolved *name*; two
  installations with different bytes under that name are indistinguishable in this log.
- **U2 — bytes actually consumed.** `Application.getModuleDataFile` + `ResourceFile.getFile(true)`
  resolution/cache is outside the log (r16 already lists "unmodeled cache/module resolution",
  `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` §Limits). The single installed copy
  narrows but does not authenticate what Ghidra opened.
- **U3 — application.** The `:63` line is emitted during `getPatchVerDiffFile` (call at `:128`,
  message at `:163`), *before* `get()` opens the derived stream at `:107` and its lambda executes
  `JsonPatch.read`/`apply` at `:136-140`. It strictly says "found", not "read/applied".
  The `Patching Go API snapshot X -> Y` text is a monitor message, absent from `ghidra.log`; no
  section count and no patched-content digest exist in the retained bytes.
- **U4 — effective content.** No derived-provider digest; no evidence the patched snapshot equals
  the real Go 1.23.12 API. Arch buckets (`linux-amd64/linux/unix/amd64/all`) are never logged;
  `Found 4881 Go types` (`:66`) is a count, not bucket identity. r16:20's reject is also untouched.
- **U5 — fallback observability.** Round 17's extractor cannot see a fallback (next section).

## 5. Contradiction at the round-17 contract surface

`contract.md:54` merges both emitters into one `snapshot_labels` field; `:58` classifies
`snapshot_loaded` on any label; `:72` predicts the normalized requested label "not selected file";
`claims.json:21` says predictions are compared field by field. But the two emitters are **not
equivalent**: `GoApiSnapshot:163` is exact-hit-only, while `GoRttiMapper:180` is also emitted on a
fallback because the object still stores the requested `goVer` (`:111`/`:239`). So a hypothetical
fallback run would produce the same `snapshot_labels` and the same `snapshot_loaded` as this exact
run, and `compare.py` would report a match. Round 17's C2 comparison is therefore **selection-blind**
— it tests the label echo the r16 reject already called non-authenticating, not the selection.
This is a contract-level gap, stated as a contradiction rather than smoothed over: r16:21 is right
about bytes, but the round-17 instrument as specified would also fail to notice when the label is
"right" for the wrong file.

## 6. Proposed move (one bounded synthesis)

**Make the selection branch a compared field, without changing r16:21.**

- `log-extract.py` (contract.md:51-60): add `snapshot_fallbacks: [{line, level, from, to}]` from
  `Falling back from (\S+) to (\S+) for Go API snapshot`, and
  `snapshot_selection ∈ {exact, fallback, base, none}`:
  `fallback` if a fallback record exists; else `base` if the `GoApiSnapshot`-component INFO label
  has patch 0; else `exact` if that label has patch > 0; else `none`. The `GoRttiMapper`
  "for version" line must **not** feed this field.
- `predict.py`: add `expected.snapshot_selection` from the r16 status:
  `exact_diff→exact`, `fallback_diff→fallback`, `missing_base→none`, and
  `base_only→base` **only when the requested patch is 0**; a nonzero request with
  `base_only` is `fallback`, because Java warns `Falling back from X to M.m.0` when the loop
  reaches patch 0 (`GoApiSnapshot.java:153-160`). This split is itself a gain: r16's single
  `base_only` status merges two runtime-distinct cases
  (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:40`, "`base_only` covers both an
  exact patch-0 request and a higher requested patch falling back to base").
- `compare.py`: compare it; a mutated observation (`exact`→`fallback`) must exit 1.
- Append-only r17 note for L1: `GoApiSnapshot` INFO = filename-selection witness;
  `GoRttiMapper` "for version" = label echo also emitted on fallback; neither is byte identity.
  Do not touch `round-16.md:21`.

Axes: **calibration** — the r16 reject keeps its exact scope while the wave gains a field that can
disagree; **depth** — the esbuild run becomes a compiled-provider check, surviving in retained
bytes, that r16's exact branch executed (the earlier r4-10 observation was not retained,
`claims.json:20`), not merely that a label was printed. No harm to
existing fields/exits, no byte/capability/outside-verification claim.

Risks: contract is L1-owned and executors may be mid-flight (make it additive only); the WARN
grammar is source-derived with **no retained fallback log**, so its positive case is fixture-only
and must be labelled unobserved; component names are REA-log-shim dependent (pin the observed
`GoApiSnapshot`/`GoRttiMapper` strings in the fixture); name the value `exact_filename` in help text
so nobody reads `exact` as content identity.

Verification: `log-extract` on the esbuild pilot log → `exact`, label `1.23.12`, `fallbacks: []`;
on the shfmt log → `none` + `missing_bootstrap: true`; selftest synthetic patch-0 INFO → `base`,
WARN → `fallback`, mapper-only → `none`; `compare` match on predicted `exact` vs observed `exact`,
exit 1 on predicted `exact` vs observed `fallback`; re-run on the final measured receipts, not the
pilot.

## 7. Limits

Pilot is explicitly not a measured run and has no pre/post carrier pins (`README.txt:1,6`), so this
is not C2 runtime evidence for the capability row. Log bytes are pinned only by `SHA256SUMS:1`.
I did not execute REA/Ghidra/carriers; the only execution was the read-only selection-model re-run
whose output is reproduced by the assigned `w1/selection-1.23.12.json`. No tools installed.
