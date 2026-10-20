# ReviewPatchHonesty — kaidoku-r16-w1

Scope: `base_matching_buckets` honesty under explicit "unpatched" vs "patched content unknown" labelling, checked against shipped source S003 and installed data. No candidate `selection.py` existed at review time (globs over `kaidoku-shokunin/` and `Projects/shokunin/` returned none), so this is a source-contract and proposed-failure review. Nothing was executed; no checks, fixtures, or builds were run. Tool installs: none.

Source anchors (`Base-src.zip`, `ghidra/app/util/bin/format/golang/...`):
- `rtti/GoApiSnapshot.java`: `get` L102–116 (search order L108–109, EMPTY on null base L115); `getApiSnapshotJsonFile` L118–146 (base = `withPatch(0)` L122, null base returns before any diff check L123–125, base returned unpatched when no diff L127–128, derived bytes named `"go%s.json".formatted(goVer)` L135); `getPatchVerDiffFile` L148–166 (nearest-lower loop L153–155, fallback `Msg.warn` L158–160); `getApiSnapshotFile` L168; `IS_GOOS_UNIX` L180; legacy `getApiFile` L183 (filename fallback, prohibited by spec); `read` L205, empty-name skip L229–230, priority-ordered map L229–235.
- `rtti/JsonPatch.java` L63 (`read`), L135 (`PatchSection`), L162/L188 (format checks).
- `rtti/JsonPatchApplier.java` L62 (`apply`), L87–88 (REMOVE), L118 (unsupported section), L122–151 (`findParent` throws when an intermediate key is missing).
- `GoVer.java`: `prevPatch` L134, `withPatch` L138, `toString` L155–157 (`M.m.p`, which is the filename component).

## Corpus facts (installed data, read-only)

- 11 base files `go1.15.0.json`…`go1.25.0.json`; 123 patch diffs (`patchverdiffs/go1.15.1`…`go1.24.6`). Zero diffs exist for any go1.25.x.
- Patch-section shape, all 123 files: zero length-1 sections (no top-level bucket add/remove). Zero length-2 sections. Every section's second key is `Funcs` or `Types`, so no whole-container replacement. The grep counts for these are 0, 0, and 82,579 section lines at depth ≥3.
- Bucket-key containment: for each minor, the distinct first keys of its diffs were compared by hand against that minor's base key set. Every diff key is present in its own base, so no diff references a missing bucket (which `findParent` would throw on). This is a manual set comparison, not an automated proof.
- Base top-level bucket sets are not constant across minors:
  - go1.15.0 has no `cgo`, `darwin-arm64`, or `darwin-arm64-cgo`.
  - go1.16.0 through go1.18.0 have no `cgo`.
  - go1.19.0 has `cgo`, `darwin-cgo`, and `windows-cgo`.
  - go1.20.0 has `cgo` and `windows-cgo` but no `darwin-cgo`.
  - go1.21.0 through go1.25.0 have `cgo` but no `darwin-cgo` or `windows-cgo`.
  - `linux-amd64`, `linux`, `unix`, `amd64`, and `all` are present in all 11 bases.
  - `cgo`, `darwin-cgo`, and `windows-cgo` are never produced by `arch_search_order` for a plain goos/goarch request, so they are unreachable from this selector. The only search-order-reachable absence is `darwin-arm64` at go1.15.0.

## Findings

**F1 — High (label): `base_matching_buckets` reads as the selected snapshot's bucket set.**
Under `exact_diff` or `fallback_diff`, `base_matching_buckets` is computed from the unpatched base (`wave1-spec.json:3`, `patch_applied:false`). Corpus evidence supports that top-level bucket *presence* is unchanged by every diff (F-corpus above). Bucket *contents* (`Funcs`/`Types` entries, `Position`, `Params`) are changed by diffs and are unknown without applying them. The key name alone does not say this. Required: add an explicit basis field, for example `bucket_basis: "unpatched_base_key_presence"`, and `patched_content: "unknown"`. Do not emit any `Funcs`/`Types` presence or count as a patched claim. If the implementation claims patched bucket presence equals base presence, label it as a source-scan invariant, not a computed patched result.

**F2 — High (contract ambiguity, likely inverted): "Base-only matching is unpatched preview and must be labelled so when diff selected."**
`wave1-spec.json:3` reads two ways: (a) label `base_only` status as an unpatched preview; (b) label `base_matching_buckets` as unpatched whenever a diff is selected. The phrase "when diff selected" contradicts `base_only`, which by definition has no diff. Propose an explicit rule instead:
- `base_only` with requested patch 0: the exact release base. It is not a preview and must not be labelled as one.
- `base_only` with requested patch p>0 and no diff ≤ p: `unpatched_preview` of `go M.m.0`. The Java path serves base bytes silently, apart from a `Msg.warn` (`GoApiSnapshot.java:158–160`). Fixture: `go1.25.1` → `base_only` plus preview label, because zero 1.25.x diffs exist. `go1.25.0` → `base_only` exact.
- `exact_diff` and `fallback_diff`: `base_matching_buckets` must carry the F1 label.

**F3 — Medium (edge semantics): `missing_base` with a diff present.**
Java returns before any diff lookup (`GoApiSnapshot.java:122–125`). A fixture with a diff file but no base must yield `status: missing_base`, `selected_diff: null`, `selected_patch: null`. The spec does not say whether `base_matching_buckets` is `null` or `[]` in this case. Decide, and encode it in the fixture schema. The `expected` subset form cannot distinguish the two unless the fixture says so.

**F4 — Medium (data dependence): expected buckets must come from the real base, not assumed.**
Because bucket sets vary by minor (see corpus facts), a `darwin/arm64` request at go1.15.x yields `[darwin, unix, arm64, all]` (no `darwin-arm64`), while the same request at go1.16+ includes `darwin-arm64`. Expected values in synthetic fixtures should be stated per case, with the base key set used, rather than inferred from linux/amd64, which is stable.

**F5 — Medium (order and empties): `arch_search_order` and bucket lists.**
Java inserts `""` for non-unix goos (`GoApiSnapshot.java:108–110`) and skips it on read (`L229–230`). Specify whether `arch_search_order` omits `""`. `base_matching_buckets` must follow priority order (`LinkedHashMap` built in `archNames` order, `L229–235`), not base-file or sorted order. Make list-order part of the fixture expectation, since a subset comparison will otherwise pass a reordered list.

**F6 — Medium (base-file identity): base must be `go M.m.0`, never the fallback diff's own version.**
For `fallback_diff`, the base stays `go1.M.0.json` and the diff is the lower-patch file. Fixture `go1.24.7` → `fallback_diff`, `selected_diff` `go1.24.6.json.diff`, `selected_patch` 6, base path `go1.24.0.json`. Do not let a `go1.24.6.json` base or a `go1.24.7` filename label leak into `base`.

**F7 — Medium (silent relabelling, Java precedent not to copy): derived bytes are named by requested version.**
`GoApiSnapshot.java:135` names fallback-derived bytes `go<requested>.json` (for example `go1.22.13`), which hides that the content is `go1.22.12`. The Python output must report the actual `selected_patch` (12) and the actual diff, never the requested label. Fixture: `go1.22.13` → `fallback_diff`, `selected_patch` 12.

**F8 — Low (request validation divergence): Java `GoVer.parse` is looser than the spec.**
`GoVer.parse` defaults a missing patch to 0 and strips trailing text (`GoVer.java:` parse helper; the "1.22.8 X:rangefunc" example). The spec requires `M.m.p`. Decide whether `1.21` is rejected (exit 2) or treated as `1.21.0`, and state it. Do not silently accept it.

**F9 — Low (no legacy fallback): `getApiFile` must stay unused.**
`GoApiSnapshot.java:183–193` falls back to `go%d.%d.json`, which is the filename fallback the spec forbids. A `go1.26.0` request must return `missing_base`, not the nearest older minor.

**F10 — Low (path portability): `base.path` and `selected_diff` should be root-relative.**
Absolute host paths in committed fixtures would be non-portable. The spec says "path"; specify relative to `--root`.

## Claims I could not verify

- No candidate `selection.py` or fixture exists at review time, so no output was checked.
- Bucket-level invariance under diffs rests on the static section scan and a manual per-minor key comparison, not an automated run. It says nothing about `Funcs`/`Types` contents or whether each bucket has the `Funcs` key that `findParent` needs (`JsonPatchApplier.java:122–151`).
- Installed data is assumed to match `Base-src.zip` S003 (same Ghidra 12.1.4 tree). The version was not checked against the jar.

## Recommended verification for the main agent (not run here)

Fixture cases to cover: `1.21.13` exact; `1.24.7` fallback to 6; `1.22.13` fallback to 12; `1.25.0` and `1.25.1` base_only with the F2 labels; `darwin/arm64` at `1.15.0` (absent `darwin-arm64`) and `1.16.0` (present); `missing_base` with a diff present; `windows` (empty entry omitted from `arch_search_order`); `go1.26.0` missing_base.
