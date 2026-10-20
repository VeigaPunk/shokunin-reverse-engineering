# Go API snapshot selector: source reconstruction

**Axes:** depth (branch-complete selector and reader model); calibration (source-only claims, no target behavior asserted).

## Evidence chain

Read the shipped Ghidra 12.1.4 `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` and `ghidra/app/util/bin/format/golang/GoVer.java`. No `lsp` device is mounted (`read xd://lsp` reported no such tool); source was read directly, with literal search used only to pin line anchors, not as semantic proof. No target was selected and no program was executed.

`GoApiSnapshot.get` asks `getApiSnapshotJsonFile` for a provider, reads it when non-null, otherwise returns `EMPTY` (GoApiSnapshot.java:104-117). The selector's base lookup is `goVer.withPatch(0)` followed by `getApiSnapshotFile(baseVer, "", "")`; a null base returns immediately, before patch lookup (122-128). The common helper forms `typeinfo/golang/%sgo%s.json%s` (168-176). Thus the selector asks for `goM.m.0.json`; it does not call the separate `getApiFile` helper. That helper has its own `goM.m.json` fallback for patch zero (183-190), but it is not in this call chain.

## Exact lookup truth table

Assume the requested patch `p` is a nonnegative integer. A candidate diff is looked up as `patchverdiffs/goM.m.q.json.diff` for patch `q`.

| Base `goM.m.0.json` resolves? | Requested `p` | Diff lookup outcome | Returned provider / effective patch |
|---|---:|---|---|
| No | Any | Diff search is skipped | `null`; `get()` returns `GoApiSnapshot.EMPTY` (122-128, 114-117). |
| Yes | 0 | Loop guard `patch > 0` is false; no `.diff` is checked | Base provider unchanged; no patch applied (153-156, 129-131). |
| Yes | `p > 0` | Diff at `q = p` resolves | Apply that exact diff to the base and return the derived provider (153-156, 128-145). |
| Yes | `p > 0` | Requested diff is absent; a lower `q` in `1..p-1` resolves | Search decrements one patch at a time; the first resolving diff is the greatest available `q < p`, and that diff is applied to the base (153-156, 128-145). |
| Yes | `p > 0` | No diff resolves for any `q` in `1..p` | Search reaches patch zero and exits without looking for a zero diff; returns the unchanged base provider (153-156, 129-131). |

`getPatchVerDiffFile` only falls back on a null result from the per-patch resource lookup. Once a non-null diff is selected, the caller reads it, constructs `JsonPatchApplier` from the base, applies the patch, and serializes the patched JSON; this path has no source-level retry with an older diff if read/application fails (128-145). `getApiSnapshotFile` converts caught `IOException` during resource resolution to `null` (168-177), so “absent” in the table means “lookup returned null,” not proof that only physical absence can cause it.

The final log branch compares the loop's `patchVer` with the request: equal emits the “Using” info message; unequal emits “Falling back” warning, then returns `patchDiffFile` (158-165). Consequently patch zero logs “Using” while returning no diff; and a positive request with no diffs decrements to zero, logs “Falling back … to …0” even though the returned diff is null and the base remains unpatched. These messages alone do not establish that a patch was applied.

## Reader branch

For a non-null provider, `get` builds this exact order: `GOOS-GOARCH`, `GOOS`, `unix` iff `GOOS` belongs to the hard-coded Unix set (otherwise the empty string), `GOARCH`, `all` (108-111, 180-181). `read` skips JSON architecture entries not in that set (205-222), then rebuilds a `LinkedHashMap` in the supplied order while dropping absent and empty names (228-237). `getFuncdef` returns the first matching function as it traverses that ordered map (514-518). This is priority order, not a claim that every requested key exists.

## Limit / divergence

This reconstructs source control flow and naming only. It does not establish which base/diff files exist for a particular request, whether a target selects this code path, or what any target binary contains. The separate `getApiFile` filename fallback must not be modeled as selector behavior; no target/runtime capability is claimed.