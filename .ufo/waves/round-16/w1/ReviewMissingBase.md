# ReviewMissingBase — round-16 w1

Scope: "missing base returns no selected diff even if diff exists". Source/data/model evidence only. No candidate `selection.py` exists under `.ufo/waves/round-16/` at review time (checked `ls`; only `claims.json`, `wave1-*.json`, `w1/`, `CorrectionDraft.candidate.md`, `documentation-red.json`, `wave1-registration.json`). The only model under review is the contract text in `wave1-dispatch.json` (`taskCall.context`, "Shared implementation contract"). No builds, tests, or runs were executed.

## Verdict

1. **The proposed failure is not a defect against the source.** Ghidra returns no diff when the base is absent, even when a patch file exists. Expected output for that state: `status=missing_base`, `base=null`, `selected_diff=null`, `selected_patch=null`, `patch_applied=false`, exit 0.
2. **The case is unreachable in shipped data.** Every minor with a patch diff has its `.0` base present, so the "missing base + diff" state exists only in synthetic fixture trees. It must not be cited as installed-data evidence.
3. **Defects to guard against in the model (not yet written):** listed under Defect risks. The most likely silent failures are a model that inspects the diff before the base, a model that falls back to a neighbouring base, and a runner that skips `null` expectations.

## Source anchors (GoApiSnapshot.java, Base-src.zip, `ghidra/app/util/bin/format/golang/rtti/`)

- `get()` L105-115: `getApiSnapshotJsonFile` returns null → `return GoApiSnapshot.EMPTY` (L115). The patch path is never reached. Missing base is a value, not an exception.
- `getApiSnapshotJsonFile()` L118-146:
  - L122 `GoVer baseVer = goVer.withPatch(0);` → the base is always `go<M.m>.0.json`, never the requested filename.
  - L123-126 base lookup; `null` → `return null`, **before** L128 `getPatchVerDiffFile(goVer)`. This is the source law for the target case.
  - L128-130: no diff → raw base provider (unpatched; the contract's `base_only`).
- `getApiSnapshotFile()` L168-178: any `IOException` → `null`. Missing base is therefore indistinguishable from "lookup failed".
- `getPatchVerDiffFile()` L148-166: runs only when the base exists. Loop L153-156 steps `prevPatch()` down to patch 0; L158-164 logs warn/info (no log is emitted on the missing-base path).
- `getApiFile()` L183-192: legacy `go%d.%d.json` fallback when patch==0. The contract forbids it; a model using it would find a different base name.
- `isInvalid()` L503-505 (`arches.isEmpty()`) and `EMPTY` L242 confirm the missing-base state is an empty snapshot.

## Supporting source anchors

- `GoVer.java` (Generic-src/Base-src, `ghidra/app/util/bin/format/golang/GoVer.java`): L134-136 `prevPatch()` floors at 0 and never changes minor → no cross-minor diff fallback. L138 `withPatch`. L155-158 `toString()` gives `M.m.p`, so the file names `go1.20.0.json` / `patchverdiffs/go1.20.5.json.diff` follow directly.
- `Application.java` (Generic-src.zip, `ghidra/framework/Application.java`): L954-963 `getModuleDataFile` → L354-375 `getDataFileInModule` throws `FileNotFoundException` when the file is absent (L364-368) **or a directory** (L369-372). A directory named `go1.20.0.json` is therefore "missing", not "present".
- `ResourceFile.java` (Utility-src.zip, `generic/jar/ResourceFile.java`): L247-252 `getFile(true)` → `resource.getResourceAsFile(this)`.
- `JsonPatchApplier.java` L122-144 `findParent`: a patch whose intermediate path element is absent throws `IOException`. The whole patch fails; there is no partial fallback. (Ghidra then raises from `get()`; it does not return `EMPTY`.)
- `JsonPatch.java`: `PatchSection.path` is a JSON array; `readPatchSection` requires `path` and `elements`.

## Installed data facts (read-only listing; `Ghidra/Features/Base/data/typeinfo/golang`)

- Bases present: `go1.15.0` … `go1.25.0` (11 files). `go1.25.x` has no diffs.
- Diffs (`patchverdiffs/`): minors 1.15 (1-15), 1.16 (1-15), 1.17 (1-13), 1.18 (1-10), 1.19 (1-13), 1.20 (1-14), 1.21 (1-13), 1.22 (1-12), 1.23 (1-12), 1.24 (1-6). Patch numbering is gap-free in every minor. 123 diff files in total.
- Every diff minor has its `.0` base present (computed set difference: empty). Missing-base-with-diff is therefore unreachable from installed data.
- Diff section paths: every path begins `@ ["<bucket>", ...` with length ≥2 (grep `^@ \["[^"]*"\]$`-style single-element paths: 0 matches). Top-level buckets seen: all, amd64, arm, cgo, darwin, darwin-amd64(-cgo), darwin-arm64(-cgo), linux, linux-386(-cgo), linux-amd64(-cgo), linux-arm(-cgo), linux-arm64(-cgo), unix, windows, windows-386(-cgo), windows-amd64(-cgo).
- Not verified: whether each diff's bucket exists in its base (requires parsing the 4-10 MB base JSON). A missing intermediate bucket would make the Ghidra patch fail (see `findParent`), which a source-model preview cannot see.

## Expected behavior for the target case (source-derived)

Fixture shape: `patchverdiffs/go1.20.5.json.diff` present; `go1.20.0.json` absent; request `1.20.5`.
- `status: missing_base`, `base: null`, `selected_diff: null`, `selected_patch: null`, `patch_applied: false`, `evidence_class: source_model`.
- `arch_search_order` for linux/amd64: `["linux-amd64","linux","unix","amd64","all"]` (computed from request, independent of base; `unix` included because `linux ∈ IS_GOOS_UNIX` at L180-181).
- Exit 0 (valid emission; no Ghidra exception on this path). Contract currently says "exit2 invalid/unreadable" — see ambiguity A2.

## Defect risks (what a wrong model would do; check in code review)

- D1 (base name): checking the requested file `go1.20.5.json` as base. Source uses `go1.20.0.json` (L122). A model that finds an exact-named file would report a base that Ghidra would never load.
- D2 (neighbour fallback): using `go1.19.13`/`go1.20.x` or any other minor's base when `go1.20.0.json` is missing. Contract forbids it; GoVer `prevPatch` (L134-136) does not cross minors.
- D3 (legacy lookup): `getApiFile`-style `go1.20.json` fallback. Forbidden by contract; source L183-190 exists but is not on the snapshot path.
- D4 (ordering): computing the diff/selected_patch before the base check. Source order L123-128 means diff must never be reported when base is absent.
- D5 (directory as file): a directory named `go1.20.0.json` treated as present. Ghidra throws (`Application.java:369-372`).
- D6 (exit code): mapping absent base to exit 2. Ghidra treats absent base as an empty snapshot (`get()` L115), not an error. Exit 0 with `missing_base` is the source-faithful mapping.
- D7 (root vs base conflation): absent `--root` directory should be exit 2 ("unreadable"), while absent base file is status `missing_base`. Ghidra cannot distinguish these (both → EMPTY); this split is a CLI design choice. [INFERENCE]
- D8 (runner null handling): the selfcheck subset comparison must treat `expected: null` as a required equality. A subset comparator that skips `None` expectations would pass a model that returns a non-null `selected_diff` for a missing-base fixture. This is the highest-risk gap for this exact target. Cross-check with the SelectorRunner reviewer.

## Contract ambiguities (recommend explicit text before implementation)

- A1: `selected_diff (same or null)` — "same" as `base` (object `{path,size,sha256}`) or a plain path string? The runner text says "path basename normalization … when expected string", which implies strings for some fixtures. Schema mismatch between contract and runner.
- A2: Exit code for absent base is not stated. "exit2 invalid/unreadable" could be read to cover absence. Source supports exit 0.
- A3: `base_matching_buckets` for `missing_base` is unspecified (`[]` vs `null`). Source has no buckets when the base is absent (`EMPTY`, `arches` empty).
- A4: `base_only` for a patch-0 request is not an "unpatched preview" — the base is the exact requested version. The contract only requires the preview label "when diff selected", so the status name should not imply preview for patch 0. [INFERENCE on intent]
- A5: `base_matching_buckets` reflects the base alone. Ghidra's runtime bucket set is post-patch; shipped diffs add no top-level buckets (0 single-element paths), but this is not proven for every diff. State the limit in `patch_applied:false` output or the report.

## Limits

- No Ghidra runtime, no build, no tests were executed (contract prohibits it). Behaviour above is source control flow, `evidence_class: source_model`.
- Source files read: `GoApiSnapshot.java`, `JsonPatch.java`, `JsonPatchApplier.java`, `GoVer.java` (Base-src.zip); `Application.java` (Generic-src.zip); `ResourceFile.java` (Utility-src.zip). Java `getResourceAsFile` implementation not read; its null/throw behaviour for unreadable (permission-denied) base files is unverified.
- No Ghidra log on the missing-base path (silent `null`). The `missing_base` label is inferred from control flow, not observed.
- No candidate `selection.py` existed; review is against the contract and source only.
- Installs: none. Host files not opened (`swarm-registry.json` in `w1/` was not read; mode 600).
