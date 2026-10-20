# ReviewNoDiff — base-only patch0 vs requested nonzero metadata (round-16 w1)

Scope: source/data/model review only. No selector run, no build/test, no patch application, no target. Tool installs: none.

## Inputs read
- Source S003: `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` — `get()`, `getApiSnapshotJsonFile()`, `getPatchVerDiffFile()`, `getApiSnapshotFile()`, `read()`, `getFuncdef()`. Line numbers from the tool window `:104-245`; ±2 unverified. Round-15 lesson cites `:111` for the `read(...)` call, which matches my count within one line.
- `Base-src.zip:.../golang/GoVer.java` — `parse`, `prevPatch`, `withPatch`, `toString`.
- `Base-src.zip:.../rtti/JsonPatch.java`, `JsonPatchApplier.java` — diff section format and applier.
- Installed data `Ghidra/Features/Base/data/typeinfo/golang/`: 11 bases `go1.15.0.json`…`go1.25.0.json`; 123 `patchverdiffs/go*.json.diff`.
- Candidate artifact: **none available.** No `selection.py` or fixtures exist under `kaidoku-shokunin` at review time (glob), and `.ufo/waves/round-16/w1/` holds only `swarm-registry.json`. Findings below are against the contract text and the Java/data.

## Verified source and data facts
1. `getPatchVerDiffFile` only decrements patch (`prevPatch`, `GoVer.java`), never minor. Patch-0 requests skip the loop, return `null`, and log `Msg.info` ("Using …"). Nonzero requests with no diff log `Msg.warn` ("Falling back …"). Base is always `goVer.withPatch(0)`.
2. `getApiSnapshotJsonFile` returns `null` when the base is missing, even when diffs exist. `get()` then returns `EMPTY` (`ver = INVALID`).
3. When a diff is found, the base bytes are patched via `JsonPatchApplier` into a derived provider. When none is found, the unpatched base is returned.
4. `read(is, archSearchOrder, goVer)` stores the **requested** `goVer` as the object's version. Its bytes may come from `go1.X.0` or a lower patch diff.
5. `archSearchOrder` for `goOS+goArch` is `[goOS-goArch, goOS, unix-or-"", goArch, "all"]`. For non-unix GOOS (e.g. windows) the third element is the empty string `""`. `read()` skips `""`.
6. `isInvalid()` is true only when no search-order bucket is present. `all` is present in 11/11 installed bases, so that path is unreachable with the installed data.
7. Histogram (123 diffs): 1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14, 1.21:13, 1.22:12, 1.23:12, 1.24:6. Each minor's patch numbers are contiguous from 1 to its max. There are **no diffs for any 1.25.x**, no base for 1.14 or 1.26, and no `.0` diff.
8. JsonPatch diff sections are `@ <path>` lines. Every one of the 123 files parses. Top-level bucket names touched by the diffs: all bucket names are present in the corresponding base's top-level key set (0 missing). No section has a length-1 path, so no top-level bucket is added or removed by any diff. Section counts across all diffs for the buckets that matter to linux/amd64: `linux-amd64` 848, `linux` 3254, `unix` 1655, `amd64` 88, `all` 58666. Bucket applicability is therefore invariant under the listed diffs at top level; content is not.
9. Every base contains `linux-amd64`, `linux`, `unix`, `amd64`, `all`. For linux/amd64, `base_matching_buckets` is the full 5-element list for every base. Example non-linux difference: go1.15.0 lacks `darwin-arm64`.
10. `GoVer.parse("go1.25.1")` returns INVALID. `replaceAll("[^.0-9].*$","")` strips everything from the leading `g`. The selector must not accept a `go` prefix silently.

## Boundary table (linux/amd64, derived from source + data; not executed)
| request | Java path | status (contract) | base | selected_patch | selected_diff |
|---|---|---|---|---|---|
| 1.15.0 | patch 0, base exact | base_only | go1.15.0.json | 0 | null |
| 1.15.1 | exact diff | exact_diff | go1.15.0.json | 1 | go1.15.1.json.diff |
| 1.15.16 | no diff, falls to 15 | fallback_diff | go1.15.0.json | 15 | go1.15.15.json.diff |
| 1.22.13 | falls to 12 | fallback_diff | go1.22.0.json | 12 | go1.22.12.json.diff |
| 1.24.7 | falls to 6 | fallback_diff | go1.24.0.json | 6 | go1.24.6.json.diff |
| 1.25.0 | patch 0, base exact | base_only | go1.25.0.json | 0 | null |
| 1.25.7 | no diff, no lower in minor | base_only (**preview**) | go1.25.0.json | 0 | null — must **not** be go1.24.6 |
| 1.14.5 | base missing | missing_base | null | null | null |
| 1.26.0 | base missing | missing_base | null | null | null |

## Findings (ordered by severity)

**F1 — medium, calibration: `base_only` conflates exact patch-0 bytes with unpatched preview.**
Contract line (wave1-spec.json:3): "Base-only matching is unpatched preview and must be labelled so when diff selected." For requested patch 0 the base is the exact requested bytes (Java `getPatchVerDiffFile` returns `null` with `Msg.info`). For nonzero requests with no diff, the base is a preview (`Msg.warn`). The status set has no `exact_base`. In installed data, nonzero base_only occurs **only** for 1.25.x, since every minor 15–24 has a patch-1 diff. A status-only label would mislabel every `1.X.0` request as preview. Fix: a distinct status, or a `preview` boolean computed as `requested.patch != 0` and `status == base_only`.

**F2 — medium, depth: requested label is not byte identity.**
Java stores the requested version as the object version (`read(..., goVer)`), so `getVer()` reports the label even for go1.25.0 or go1.24.6 bytes. The contract's `requested` key is correct, but nothing in the JSON separates label from bytes. Fix: emit `label_version` (= requested) and `byte_source_version` (= base patch or selected diff patch), and state that `selected_patch` refers to the bytes, not the label.

**F3 — medium, boundary hazard: cross-minor fallback.**
Java never crosses minor versions. A naive "nearest lower diff" search by semver would select `go1.24.6.json.diff` for a 1.25.7 request and apply it to the `go1.25.0` base. That is wrong: the diff is computed against 1.24.0. Fixture required: 1.25.7 → `base_only`, `selected_diff: null`, `selected_patch: 0`. The contract's "nearest-lower-diff" wording (wave1-spec.json:3) does not state the same-minor restriction.

**F4 — medium, calibration: `patch_applied:false` and `exact_diff` wording.**
Java applies the diff (`getApiSnapshotJsonFile` derived provider). The selector does not apply it, so `patch_applied:false` is accurate about the selector but reads as "the patched bytes are established" under `exact_diff`. The status names should say the diff is selected/would apply, not exact content. Suggest `diff_selected` (or `diff_would_apply`) and keep `patch_applied:false`.

**F5 — low-medium, depth: `base_matching_buckets` under diff statuses.**
The field is computed from the unpatched base. Verified above: top-level bucket applicability is invariant under all 123 diffs, but content is not (see fact 8). The contract should say "bucket keys present in the unpatched base that match `arch_search_order`; invariant to listed diffs at top level; content not verified." Without that, `base_matching_buckets` can be read as patched-content applicability.

**F6 — low, contract: `arch_search_order` contains `""` for non-unix GOOS.**
Example for windows/amd64: `["windows-amd64","windows","","amd64","all"]`. Java's `read()` skips `""`. The selector must exclude `""` from `base_matching_buckets` and should state how `""` appears in `arch_search_order`. Fixtures for windows and darwin-arm64 (absent from go1.15.0) are the cases that exercise this.

**F7 — low, contract: undefined fields.**
- `selected_diff (same or null)`: "same" is undefined. C1 requires byte identities, so the diff entry needs `{path,size,sha256}` like `base`.
- `selected_patch` for `base_only`: 0 or null is unstated. Java selects `withPatch(0)`, so 0 with `base` set is the faithful choice.
- `missing_base`: Java returns `EMPTY` (not an error). The contract's "exit0 emission or exit2 invalid/unreadable" leaves it open. Recommend exit 0 with `base: null` for missing base.
- Unknown GOOS/GOARCH: Java does not validate; the contract does not say whether to exit 2 or emit with reduced buckets.

**F8 — low, contract: request format.**
Java's `GoVer.parse` strips the `go` prefix only by returning INVALID; the selector should reject `go1.25.1` and non-`M.m.p` strings with exit 2. The contract says `--request M.m.p` but does not state the rejection for the `go` prefix.

## Verification gaps
- No selector or fixture exists at review time; F1–F8 are contract/source-level, not measured against an implementation.
- No patched-output digest was computed; F4/F5 remain source-model claims.
- Line numbers for GoApiSnapshot.java are from a tool window and not independently re-verified beyond ±2.
- Not checked: Ghidra `Application.getModuleDataFile` search order across extension data dirs (the selector models only `--root`), and `ResourceFile.getFile(true)` extraction behavior.

## Handoff
Checks for L1 after integration (not run by this reviewer): fixture rows for 1.15.0, 1.15.1, 1.15.16, 1.22.13, 1.24.7, 1.25.0, 1.25.7, 1.14.5, 1.26.0 on linux/amd64, plus windows/amd64 for F6.
