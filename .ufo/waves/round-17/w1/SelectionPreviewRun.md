# SelectionPreviewRun — r17 w1 (KaidokuR17.SelectionPreviewRun-3)

Scope: ran r16 `selection.py` for R ∈ {1.27.0, 1.27.2, 1.23.12, 1.20.12} against the installed
Ghidra 12.1.4 Go typeinfo root, saved stdout, interpreted the pilot log's snapshot line.
No installs (python3 stdlib only); no REA analyze/search, no Ghidra run, no carrier execution.

## Runs (all `python3 -I .../round-16/selection.py --root .../typeinfo/golang --goos linux --goarch amd64`, exit 0)

| request | file (`.ufo/waves/round-17/w1/`) | status | base | selected_diff | selected_patch |
|---|---|---|---|---|---|
| 1.27.0  | `selection-1.27.0.json`  | `missing_base` | null | null | null |
| 1.27.2  | `selection-1.27.2.json`  | `missing_base` | null | null | null |
| 1.23.12 | `selection-1.23.12.json` | `exact_diff` | `go1.23.0.json` (9368866 B, sha256 `3b1d795f…f63692`) | `patchverdiffs/go1.23.12.json.diff` (111215 B, sha256 `e1fdbc7e…a99c53`) | 12 |
| 1.20.12 | `selection-1.20.12.json` | `exact_diff` | `go1.20.0.json` (8875175 B, sha256 `6def3499…6d0a32`) | `patchverdiffs/go1.20.12.json.diff` (164688 B, sha256 `148352d3…105e82b`) | 12 |

Output-file sha256: 1.27.0 `1e4c313f…39352cd`; 1.27.2 `f5fc9a73…3d537`; 1.23.12 `6caf43e5…e471b`; 1.20.12 `6ca8cb18…6570e`.
All four: `arch_search_order` = `[linux-amd64, linux, unix, amd64, all]`, `patch_applied: false`,
`evidence_class: source_model`. The two `exact_diff` runs list all five buckets present in the
unpatched base (`base_matching_buckets_source: "unpatched_base_file"`).

Observation (data dir listing): bases exist only for `go1.15.0`–`go1.25.0` (no `go1.26`/`go1.27`
base, hence `missing_base`); `patchverdiffs/` holds 123 diffs including `go1.20.1`–`go1.20.14`
and `go1.23.1`–`go1.23.12`, so both in-range requests hit exact diffs rather than fallbacks.
Consistent with `GoRttiMapper.SUPPORTED_VERSIONS = "1.15-1.25"` (Base-src.zip
`ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79`).

## What `Using Go API snapshot for 1.23.12` (pilot ghidra.log:63) tells about the selected diff

Emission site: `GoApiSnapshot.getPatchVerDiffFile` `Msg.info` at
`…/rtti/GoApiSnapshot.java:163`, reached only via `getApiSnapshotJsonFile:128`, which is itself
reached only after the base file lookup succeeded (`:122-126`; absent base → `null` →
`GoApiSnapshot.EMPTY`, and this line never prints).

It **does** tell:
- The base `go1.23.0.json` was found on the module data path (else `getPatchVerDiffFile` is
  never called) — inference from `:123-128`.
- The resolved `patchVer.getPatch()` equals the requested patch (`:158-163` else-branch). For a
  patch>0 request the `while` loop at `:153-155` only decrements `patchVer` when the probed diff
  file is missing, so equality on the info branch means `patchverdiffs/go1.23.12.json.diff`
  existed at first probe — i.e. an exact diff was selected, matching `selection-1.23.12.json`
  status `exact_diff` / `selected_patch` 12. Inference, source-derived.
- No fallback occurred: the warn `Falling back from %s to %s` (`:159-160`) is mutually exclusive
  with this info line and is absent from retained log lines 60-67.

It **does not** tell:
- Which file or directory was read: the `%s` at `:163` prints the **requested** `goVer`, never a
  filename — the label cannot by itself prove the bytes came from `go1.23.12.json.diff`
  (the exact-diff conclusion above rests on the else-branch invariant, not the string).
- Whether the diff actually applied or the patched JSON parsed: patching runs lazily inside the
  derived ByteProvider at `:133-144`, i.e. *after* this line. Downstream success is only
  evidenced by the next line `Using Go API snapshot for version 1.23.12` (ghidra.log:64),
  emitted at `GoRttiMapper.java:179-181` only when `apiSnapshot.getVer()` is valid — `EMPTY`
  carries `GoVer.INVALID` (`GoApiSnapshot.java:242`), so line 64 proves a non-empty snapshot was
  constructed, which in turn implies the patch pipeline ran.
- Whether any goos/goarch bucket matched: `read()` silently builds a possibly-empty map
  (`:228-239`); the line is unconditional on bucket hits.
- Where the version came from (real build info vs `GoBuildInfo.fromFallbackInfo`,
  `GoRttiMapper.java:154-159`), or whether it is in `SUPPORTED_VERSIONS` — that is the separate
  `Untested Go version` error at `GoRttiMapper.java:171`.
- Generality caveat: for a patch==0 request the same info line prints with *no* diff file (loop
  skipped, `patchVer == goVer`), so the line alone cannot distinguish `exact_diff` from
  `base_only` in general. For 1.23.12 (patch 12 > 0) that ambiguity does not apply.

## Limits
- All outputs are `source_model` previews: `patch_applied` is always false; the patched document
  is never constructed, and `base_matching_buckets` is computed on the unpatched base.
- `missing_base` predicts EMPTY snapshot + no snapshot log lines for the 1.27.x carriers
  (and the `Untested Go version` error at `GoRttiMapper.java:171` for 1.27.x); observed-log
  confirmation belongs to the carrier-run lane, not this one.
- Java-source line numbers refer to extracted
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` members;
  extraction was to /tmp scratch only, no repo writes outside `w1/`.
