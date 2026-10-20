# Installed Go snapshot/diff schema reconstruction

**Axes:** depth, calibration.

## Reconstructed contract

- **Base `.json` is the snapshot.** S003 `GoApiSnapshot.getApiSnapshotJsonFile` first constructs the patch-zero version and requests `typeinfo/golang/go<major>.<minor>.0.json` (`GoApiSnapshot.java:122–126, 169–178`). The reader consumes a JSON root object keyed by architecture/platform buckets; each retained bucket deserializes as `GoArch { Funcs, Types }` (`GoApiSnapshot.java:187–208, 400+`). The installed `go1.25.0.json` confirms bucket values have `Funcs` and `Types`; its root contains buckets such as `all`, `linux-amd64`, and `amd64`.
- **`.json.diff` is a delta, not another snapshot JSON.** S003 `JsonPatch` documents the supported input as jd-native text diff; `readPatchSection` reads `@ <JSON-array-path>` sections followed by `-`/`+` value lines, and `PatchSection`/`PatchLine` model path plus operations. Installed `go1.24.6.json.diff:1–3` shows the form directly (`@ ["all","Funcs",...,"Position"]`, then removed/added JSON strings); lines 187–204 show a whole function value replacement. It cannot be read as the base bucket schema.
- **Selection is base-first and chooses at most one diff.** `getApiSnapshotJsonFile` returns null when the same-minor patch-zero base is absent; if the base exists but no diff is found, it returns the base provider unchanged. `getPatchVerDiffFile` searches the requested patch downward within that minor and returns the first present diff (`GoApiSnapshot.java:122–145, 148–166`). It does not accumulate intermediate diffs. The normal `get` path supplies bucket search order `[goos-goarch, goos, unix-if-goos-is-unix, goarch, all]` (`:108–109`); for linux/amd64 this is `[linux-amd64, linux, unix, amd64, all]`.

## Divergence to preserve in the assigned selector

The installed Java path **does apply** a selected diff: it constructs `JsonPatchApplier` from the base, applies the patch, and emits derived JSON (`GoApiSnapshot.java:128–145`; `JsonPatchApplier.apply/applySection`). The applier warns in source that it uses no context hints and requires the exact original base (`JsonPatchApplier` class comment). This assignment is only a read-only source model: report the selected base and optional diff, set `patch_applied:false`, and label a base-only result as an unpatched preview. Do not claim that preview is the requested patch's bytes or validate the diff's effect. A missing base remains `missing_base` even if a diff file exists; do not use the separate `getApiFile` filename fallback.

## Evidence limits

Source was read from registered source S003 and corroborated with the installed base JSON and diff text. No Ghidra code, patch applier, or target was run; no patch was applied. No `lsp` route is mounted (`xd://lsp` reported no such tool), so these findings come from direct source-member reads, not LSP results or grep inference. Confidence: high for the stated source selection/schema behavior; no claim about execution against a target or semantic correctness of installed patches.
