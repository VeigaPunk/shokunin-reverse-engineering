# ReviewLowerDiff — nearest lower (not first glob/lexicographic) patch-diff selection

Seat: KaidokuR16.ReviewLowerDiff (reviewer, leaf). Axes named for this lane: **depth**, **calibration**.
Evidence class: source + installed data only. No target, no compiled provider, no execution of selection.py, builds, or tests.

## Artifacts reviewed

- Source S003: `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (installed at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`).
  - `get` L102-115; `getApiSnapshotJsonFile` L118-146 (base L122, `getPatchVerDiffFile` call L128, `JsonPatch.read`/`jpa.apply` L136-140); `getPatchVerDiffFile` L148-165 (walk loop L153-155, fallback warning L157-161); `getApiSnapshotFile` L168; `getApiFile` L183 (legacy `go%d.%d.json` fallback, excluded by contract); `read` L205 (keeps only `archNames`, L218).
- `GoVer.java` (`Base-src.zip:ghidra/app/util/bin/format/golang/GoVer.java`): `prevPatch` L134 (`patch > 0 ? patch-1 : 0`), `withPatch` L138, `toString` L155 (`M.m.p`, or `M.m` when patch is -1).
- `JsonPatch.java` L172-198 (`lineFromJson`, context lines skipped); `JsonPatchApplier.java` L33 (docstring: no context hints, "should only be used against the exact original value"), L75-110 (`applySection`; REMOVE for object keys is unconditional, the old value is never compared).
- Data: `.../typeinfo/golang/` base files `go1.15.0.json` through `go1.25.0.json` (all 11 present); `patchverdiffs/` holds 123 `.diff` files.
- No `selection.py` exists anywhere on the local filesystem at review time (`find /` for `selection.py` / `select_snapshot*` outside site-packages returned nothing). The review is therefore a contract review plus a data-level simulation; no candidate CLI output was inspected.

## Patch coverage (from `ls`)

Contiguous from patch 1 with no interior gaps in every minor:

| minor | diffs present | minor | diffs present |
|---|---|---|---|
| 1.15 | 1-15 | 1.20 | 1-14 |
| 1.16 | 1-15 | 1.21 | 1-13 |
| 1.17 | 1-13 | 1.22 | 1-12 |
| 1.18 | 1-10 | 1.23 | 1-12 |
| 1.19 | 1-13 | 1.24 | 1-6 |
| | | 1.25 | **none** (base only) |

Consequences: no `go1.14.*` base, no `go1.26.*` base, and no `go1.14.*` diffs, so these resolve to `missing_base`. For 1.24.7 and above the walk lands on 1.24.6.

## Findings

### F1 (depth, high if the CLI is implemented as glob-sorted): a lexicographic selector returns the wrong diff

Source contract: `getPatchVerDiffFile` (L153-155) decrements the patch number numerically via `prevPatch()`. Any selector that sorts filenames as strings is wrong. Each row below was computed from the actual `patchverdiffs/` listing.

| request | Java-equivalent numeric walk (correct) | lexicographic "max name <= target" | lexicographic "first glob" |
|---|---|---|---|
| 1.24.7 | 1.24.6 | 1.24.6 | 1.24.1 |
| 1.24.10 | **1.24.6** | **1.24.1** (wrong) | 1.24.1 (wrong) |
| 1.19.14 | 1.19.13 | 1.19.13 | 1.19.1 (wrong) |
| 1.19.20 | **1.19.13** | **1.19.2** (wrong) | 1.19.1 (wrong) |
| 1.19.10 (exact) | 1.19.10 | 1.19.10 | 1.19.1 (wrong) |

Cause: `"go1.24.1.json.diff" < "go1.24.10.json.diff"` because `.` (0x2E) sorts before `0` (0x30), so the string max among names not exceeding the target is `1.24.1`. Fixture rows for 1.24.10 and 1.19.20 would discriminate this selector from the correct walk; 1.19.14 and 1.24.7 would not.

Required fixture cases: `1.24.10 -> fallback_diff, selected_patch 6`; `1.19.20 -> fallback_diff, selected_patch 13`; `1.19.10 -> exact_diff, selected_patch 10`.

### F2 (calibration, medium): `base_only` conflates two different states

Status set `base_only` covers:
- (a) requested `M.m.0`: no walk happens, `getPatchVerDiffFile` returns null (L118-128), and the base is the exact, unpatched snapshot for that version;
- (b) requested `M.m.p`, p>0, no diff at any level down to 1: the walk ends at patch 0 (L153-155, warning L157-161 says "Falling back from M.m.p to M.m.0"), and the loaded snapshot is the unpatched base, a preview of M.m.p.

The contract says base-only matching "must be labelled so when diff selected". That wording is ambiguous: it does not say what to emit when no diff is selected. Case (b) is only correct as a preview if labelled, and the status enum alone does not carry that. Example: 1.25.3 and 1.25.0 both emit `base_only` with `selected_diff: null`, `selected_patch: null`, so a consumer cannot tell exact from preview.

Recommendation: state explicitly in the contract either a separate status (e.g. `base_only_unpatched_preview`) or a `preview: true` flag set iff requested patch > 0 and selected_diff is null. Fixture: `1.25.3 -> base_only, preview true`; `1.25.0 -> base_only, preview false`.

### F3 (depth, medium): the walk must not stop at a base-only or missing-base boundary early

`get` (L108-115) checks the base file first (L122-124). If the base is missing, `getApiSnapshotJsonFile` returns null and `get` returns EMPTY, even if diffs exist for that minor. The data has no such case (no diff exists without its base), so it cannot fire on current data. Fixture needed: a synthetic tree with `patchverdiffs/go1.X.Y.json.diff` but no `go1.X.0.json` must yield `missing_base`, not `fallback_diff`.

### F4 (depth, low): arch search order includes an empty bucket for non-unix GOOS

L108 builds `[goOS-goArch, goOS, IS_GOOS_UNIX ? "unix" : "", goArch, "all"]`. For `windows`/`amd64` that is `["windows-amd64","windows","","amd64","all"]`; the empty string is skipped inside `read` (L218-219 area, `archName == null || isEmpty -> continue`). The contract asks for `arch_search_order` as a JSON key. Decide whether the empty entry is emitted or omitted and document it; the Java behaviour is to skip it on lookup. Linux is in `IS_GOOS_UNIX` so `linux/amd64` gives `["linux-amd64","linux","unix","amd64","all"]`.

### F5 (depth, low, limit): `--root` cannot reproduce `Application.getModuleDataFile`

`getApiSnapshotFile` (L168) resolves through `Application.getModuleDataFile`, which searches all module data directories. The CLI reads only `--root`. A user or extension data directory could shadow or add files that Ghidra would use. Record as an explicit limit; do not claim equivalence with the running tool. Existence test in Python should be `isfile()` (a directory is not a file), matching the `rfile.getFile(true)` null path.

### F6 (depth, positive verification): the diffs are cumulative from base, so fallback to a lower patch is valid

`JsonPatchApplier` applies every diff to the base `go1.X.0.json` (L136-140), not chained. Therefore a fallback diff yields the state of its own patch level only if each diff is cumulative from base. Checks I ran (read-only, Python stdlib, scratch files `/tmp/r16_lower_diff_probe.py`, `/tmp/r16_seq_probe.py`, outputs in `/tmp/*.out`):

- Discriminator example: `ProcessEnv Position`. Base `go1.15.0.json` value is `child.go:358:6`. `go1.15.1`, `go1.15.2`, `go1.15.3`, `go1.15.4` all carry `-` `358` / `+` `377`. A chained (incremental) diff would show `377` on the `-` side for 1.15.2+. It does not, so the diffs are cumulative from base.
- Sequential application of each diff to its base, checking each scalar `-` old value against the state at the point it is applied: **74,743 scalar replacements, 0 mismatches** across all 123 diffs.
- A naive non-sequential check (old value vs base only) shows mismatches in 1.16.10+ and 1.17.3+ and 1.18.8+ and 1.24.2+, all on list-index paths (`Fields`, index 7 / 27 / 4). These disappear under sequential application, so they are within-diff index shifts, not a broken base. Do not cite the naive count as evidence of inconsistency.

Limit: the applier does not verify `-` values (`applySection` L87-99 removes keys unconditionally, `JsonPatchApplier` L33 says so). A wrong-base application would be silent. The check above is a data-consistency check, not ground truth for any target's snapshot.

### F7 (calibration, low): identical-content adjacent patch diffs

Seven pairs of adjacent diffs have byte-identical content: `1.15.4=1.15.5`, `1.20.8=1.20.9`, `1.21.12=1.21.13`, `1.22.8=1.22.9`, `1.22.11=1.22.12`, `1.23.5=1.23.6`, `1.23.8=1.23.9`. The selection record must label `selected_patch` by filename version (the walk), never by content hash or content identity. A consumer that compares diff bytes to infer "exact" would wrongly treat 1.15.5 as 1.15.4's content-equal copy. Recommend emitting `selected_diff` sha256 alongside the name, with the status computed from the version numbers only.

### F8 (depth, positive): the walk semantics match the contract's described order

Walk: start at requested `M.m.p`, test `patchverdiffs/go{M.m.p}.json.diff`, then `prevPatch()` until patch 0 or a hit. Verified by hand against the listing:
- 1.15.1 -> exact_diff 1; 1.15.99 -> fallback_diff 15; 1.24.9 -> fallback_diff 6; 1.25.3 -> base_only (F2); 1.25.0 -> base_only exact (F2); 1.18.11 -> fallback_diff 10; 1.22.12 -> exact_diff 12.

## Boundary fixture candidates (for the runner; not executed here)

| request | goos/goarch | expected status | selected_patch | note |
|---|---|---|---|---|
| 1.15.1 | linux/amd64 | exact_diff | 1 | first patch |
| 1.15.99 | linux/amd64 | fallback_diff | 15 | beyond last |
| 1.24.10 | linux/amd64 | fallback_diff | 6 | F1 discriminator |
| 1.19.20 | linux/amd64 | fallback_diff | 13 | F1 discriminator |
| 1.25.0 | linux/amd64 | base_only | null | exact base |
| 1.25.3 | linux/amd64 | base_only, preview | null | F2 |
| 1.14.9 | windows/amd64 | missing_base | null | no base |
| 1.26.0 | linux/arm64 | missing_base | null | no base |

## Verification gaps

- No selection.py exists; no CLI output, fixture, or runner was observed. F1-F5 are contract findings only.
- F6 checks old-value consistency, not that any patched output equals the real Go snapshot.
- Module-data shadowing (F5) is untested.

## Tooling record

No installs or updates by this seat. Scratch files written only under `/tmp` (`r16_lower_diff_probe.py`, `r16_lower_diff_probe.out`, `r16_seq_probe.py`, `r16_seq_probe.out`); nothing written in the repository beyond this report.
