# Round 15 w1 — ReviewPatchCases: Go snapshot edge cases vs source

seat: KaidokuR15.ReviewPatchCases (leaf reviewer, read-only)
axes: depth, calibration
scope: patch 0, nonzero patch with diff present / absent, absent minor, missing diff, OS/arch applicability in the Go API snapshot selector
repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
verification run by this seat: none (source reading and non-verdict inventory only; no build, test, lint, gate, or target execution)
tool installs/updates: none

## Sources and anchors

- S003 installed archive: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`. Line numbers below were taken with `unzip -p <zip> <member> | cat -n`. The `read` tool on archive members returns text without numbers, so I did not rely on it for anchors.
- Members read: `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (whole file), `.../rtti/GoRttiMapper.java` (lines 78-79, 165-185, 347-367), `.../rtti/JsonPatch.java`, `.../golang/GoVer.java`, `.../golang/GoVerRange.java:42-87`, `.../golang/GoBuildInfo.java:237-239`, `.../structmapping/DataTypeMapper.java:172-181`, `.../rtti/GoTypeManager.java:402-455`.
- Installed data: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`. This is a directory listing and JSON key inventory. The JSON was parsed only to list top-level keys and sample `Position` values.
- Prior entry checked: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (decision table, "Correction and limits").

## Selector logic, as source

`GoApiSnapshot.get` (`GoApiSnapshot.java:102-116`) calls `getApiSnapshotJsonFile` (`:118-146`), then `read(..., goVer)` (`:111`). The selector works like this:

1. `baseVer = goVer.withPatch(0)`; `jsonFile = getApiSnapshotFile(baseVer)` (`:122-123`). If null, return null and `get` returns `EMPTY` (`:124-126`, `:115`). Nothing else is consulted, including patch diffs.
2. `patchDiffFile = getPatchVerDiffFile(goVer)` (`:128`, `:148-166`). The loop `:153-156` runs only while `patch > 0`, decrementing with `prevPatch()` until a diff exists or patch reaches 0. It stays inside the same major.minor. The last assignment inside the condition is the one that decides the result, so when the loop exits at patch 0 with no hit, `patchDiffFile` is null (no stale value).
3. If `patchDiffFile == null`, the raw base bytes are returned (`:129-131`). Otherwise the single diff is applied to the base (`:133-144`). The derived provider is named `go<goVer>.json` (`:135`), but the content comes from `patchVer`, the diff that was found.
4. `read(..., goVer)` stamps the snapshot with the requested `goVer` (`:111`), not the version whose diff was applied.
5. `read` keeps only arches named in `[goOS-goArch, goOS, unix(if unix GOOS), goArch, "all"]` (`:108-109`, `:228-237`). `isInvalid()` is `arches.isEmpty()` (`:503-505`).

Caller: `GoRttiMapper.getGoBinary` (`GoRttiMapper.java:165-181`). Out-of-range versions only log `Msg.error` (`:170-172`) and continue. Any snapshot with `getVer()` valid logs `Using Go API snapshot for version <getVer()>` (`:178-180`). For EMPTY, `getVer()` is INVALID, so that log is skipped.

Bootstrap message: `initStructMappings` (`:351-367`). Only when `registerStructures` throws `IOException` does `apiSnapshot.isInvalid()` select `Missing Go bootstrap type info…` (`:356-360`). Otherwise it throws `Invalid Go bootstrap struct mapping info` (`:364-365`). `DataTypeMapper.registerStructure` throws the `IOException` when the Ghidra struct is not found (`DataTypeMapper.java:176-181`). With EMPTY, `GoTypeManager.findTypeRec` finds no `apiSnapshot.getTypeDef` hit (`GoTypeManager.java:449`, `GoApiSnapshot.getTypeDef` iterates an empty map at `:524-531`). So for EMPTY the missing-bootstrap message follows by control flow. This is source reasoning, not an execution.

Range check: `GoVerRange.parse("1.15-1.25")` makes minor-granular bounds (`GoVerRange.java:47-52` uses `parseWildcardPatch`, so patch = -1). `contains` (`:83-87`) compares with `compareTo`, which treats patch -1 as equal to any patch (`GoVer.java` compareTo). So every 1.15.N through 1.25.N is in range, and 1.14.x and 1.26.x are out. Version parse: `GoBuildInfo.getGoVer` uses `GoVer.parse` (`GoBuildInfo.java:238`), which defaults a missing patch to 0 and strips anything after the first non `[.0-9]` character (`GoVer.java` parse, `replaceAll("[^.0-9].*$","")`). Wildcard patch -1 therefore does not reach `GoApiSnapshot.get` from this path.

## Installed data inventory (non-verdict)

- Base files (`go<X.Y>.0.json`): exactly 11, for 1.15.0 through 1.25.0. There is no go1.14.x base and no go1.26.x base.
- Patch diffs (`patchverdiffs/go<X.Y.N>.json.diff`): 123 files. Per minor, N runs contiguously from 1 with no gaps:
  - 1.15: 1-15 (15); 1.16: 1-15 (15); 1.17: 1-13 (13); 1.18: 1-10 (10); 1.19: 1-13 (13); 1.20: 1-14 (14); 1.21: 1-13 (13); 1.22: 1-12 (12); 1.23: 1-12 (12); 1.24: 1-6 (6); 1.25: none.
  - No `.0` diff exists for any minor.
- Every base file has the keys `all`, `unix`, and `linux-amd64`, plus `linux` and `amd64`. `darwin-arm64` is absent in go1.15.0 only. Each base holds 26-29 top-level keys.
- Diff format: jd native text. Sections start `@ ["all","Funcs",…]` followed by `-`/`+` lines. The diff carries no version header, so content cannot self-identify its version.
- Base-relativity spot check (one entry only): `crypto/tls.buildRetryConfigList` Position is `ech.go:621:6` in go1.24.0 base, and the go1.24.6 diff removes exactly `ech.go:621:6` and adds `:641:6`. This is consistent with each diff being relative to its minor's `.0` base. It is one entry, not a full replay.
- Note: `go1.25.0` base shows that entry at `ech.go:652:6`. That value is not evidence about any 1.25.x binary.

## Truth table

Columns: case, input, base, diff chosen, bytes applied, `ver` label, `isInvalid`, log emitted, installed instances, anchors. "Installed" means a row reachable with the 11 base files and 123 diffs above.

| # | Case | Input | Base | Diff chosen | Bytes applied | `ver` label | isInvalid | Log | Installed instances | Anchors |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | patch 0, base present | 1.N.0 (N=15..25) | go1.N.0.json | none (`patchDiffFile==null`) | base raw | 1.N.0 | false (has `all`) | Info "Using Go API snapshot for 1.N.0" | 1.15.0 … 1.25.0 (11) | `GoApiSnapshot:122-131,162-164,111`; `GoRttiMapper:178-180` |
| R2 | patch k≥1, diff k present | 1.N.k | go1.N.0 | go1.N.k diff | base + diff k | 1.N.k | false | Info | 1.15.1–15.15, 1.16.1–16.15, 1.17.1–17.13, 1.18.1–18.10, 1.19.1–19.13, 1.20.1–20.14, 1.21.1–21.13, 1.22.1–22.12, 1.23.1–23.12, 1.24.1–24.6 (123) | `GoApiSnapshot:128-145,153-165` |
| R3 | patch k, diff k absent, some diff j (1≤j<k) present in minor | 1.N.k | go1.N.0 | nearest lower j | base + diff j | **1.N.k (requested)** | false | Warn "Falling back from 1.N.k to 1.N.j" then Info-free; GoRttiMapper Info still says "version 1.N.k" | None installed (no gaps); 1.24.7+ would hit this with 1.24.6 | `GoApiSnapshot:153-161,135,111` |
| R4 | patch k, no diff for any 1..k in minor | 1.N.k | go1.N.0 | none (loop reaches 0, `patchDiffFile` null) | **base raw (N.0 content)** | **1.N.k (requested)** | false | Warn "Falling back from 1.N.k to 1.N.0"; then `GoRttiMapper` Info "Using Go API snapshot for version 1.N.k" | **1.25.1 onward** (no 1.25.x diffs installed); also any 1.24.k beyond the highest diff | `GoApiSnapshot:153-156,158-161,165,111`; `GoRttiMapper:178-180` |
| R5 | base absent, any patch | 1.N.k where go1.N.0.json missing | none | never consulted (returns at `:124-126`) | none → `EMPTY` | INVALID (`EMPTY`, `:242`) | true | none from selector; then bootstrap message if struct mapping throws | 1.26.x (any patch); 1.14.x and below (also out of range) | `GoApiSnapshot:122-126,115,242`; `GoRttiMapper:356-360`; `DataTypeMapper:176-181` |
| R6 | base absent, diff present for same minor | hypothetical | none | not consulted | none → EMPTY | INVALID | true | as R5 | none installed | `GoApiSnapshot:122-126` |
| R7 | absent minor, diffs present in another minor | 1.26.k | none | not consulted (no minor fallback; `withPatch(0)` keeps minor) | none → EMPTY | INVALID | true | as R5 | 1.26.x against installed 1.24.1–6 diffs; no cross-minor use | `GoApiSnapshot:122,155,158-161` (loop bounded by `prevPatch`, same minor) |
| R8 | base present, requested OS/arch key absent, `all` and/or `unix` present | any | go1.N.0 | per R1–R4 | partial arch set | as R1–R4 | **false** (`all` retained at `:108-109`, `:228-237`) | as R1–R4 | darwin-arm64 for go1.15.0 (`unix`/`all` present) | `GoApiSnapshot:108-109,228-237,503-505` |
| R9 | base present, JSON lacks every search key incl. `all` | hypothetical | present | per R1–R4 | empty arches | INVALID-like (`arches.isEmpty()`) | true | as R5 | none (all 11 bases have `all`) | `GoApiSnapshot:503-505` |
| R10 | out-of-range version | 1.14.x, 1.26.x | as R1–R5 | as R1–R5 | as R1–R5 | as R1–R5 | as R1–R5 | `Msg.error "Untested Go version"` (advisory; no selection change) | 1.26.x, ≤1.14 | `GoRttiMapper:79,170-172`; `GoVerRange:47-52,83-87` |
| R11 | rc/suffix string | e.g. "1.25rc1" | go1.25.0 | per R1 (patch parses to 0) | base raw | 1.25.0 | false | Info | Not observed; inference that real GOVERSION text reaches this form | `GoVer.parse`; `GoBuildInfo:238` |

Note for R3/R4: the `Msg.warn` is the only signal that the content is not the requested patch. The `ver` label, the `GoRttiMapper` "Using … version" log, and `isInvalid()` all report success. No bootstrap diagnostic fires.

## Findings

1. **[HIGH, calibration] Silent base substitution for nonzero patch with no diff in the minor (R4).** The selector returns the `.0` base bytes but stamps the snapshot with the requested `goVer` (`GoApiSnapshot.java:111`). The only difference is a `Msg.warn` (`:158-161`). `GoRttiMapper` then logs `Using Go API snapshot for version 1.25.N` (`GoRttiMapper.java:178-180`). Installed consequence: no 1.25.x diffs exist (verified by listing), so any go1.25.N (N≥1) target gets go1.25.0 content labeled 1.25.N and is not flagged as invalid. The r14 entry's decision table (`2026-10-20-r14-go-version-diagnosis.md`, table rows) lists "Missing base JSON" as the only absent-file row and does not cover missing patch diffs. A future decision record must not treat "valid snapshot" as "patch-exact snapshot".

2. **[HIGH, calibration] Diff-substitution mislabels content (R3).** When diff j<k is used for requested k, bytes are base + diff j (`:135-144`) but the label is k. Installed inventory has no such case, but 1.24.7+ would hit it. Same mechanism and same silence as Finding 1.

3. **[MEDIUM, calibration of prior entry] OS/arch exclusion cannot reach `isInvalid()` with the installed inventory.** The r14 entry says "A present file without applicable records can therefore reach the same invalid-snapshot branch" (`GoApiSnapshot.java:205-239`, `:503-505`), and its decision table pairs `Missing Go bootstrap type info` with "distinguish absent base file from OS/architecture exclusion." In source, `archSearchOrder` always contains `"all"` (`:108-109`). With every installed base containing `all` (inventory), `arches` is never empty for a present base. So OS/arch exclusion yields a non-invalid partial snapshot (R8). It can then fail later in struct mapping, which gives `Invalid Go bootstrap struct mapping info` (`GoRttiMapper:364-365`), not the missing-bootstrap message. The mapping-failure branch is [INFERENCE]: I did not trace `registerStructures` on a partial snapshot. The claim in the r14 entry is true only for a hypothetical JSON lacking `all` (R9). Treat it as unreachable with installed data.

4. **[LOW, hazard] Unused `getApiFile` (`GoApiSnapshot.java:183-192`).** Its patch-0 fallback to `go%d.%d.json` is not reachable on the live path: the only call site in S003 is the definition. The live path (`getApiSnapshotFile`, `:168-178`) tries only `go<X.Y.0>.json`. Do not cite `getApiFile` as evidence of a fallback that happens at runtime.

5. **[LOW, message accuracy] `GoRttiMapper.java:359` calls `.formatted(goVer)` on a string with no `%s`.** The bootstrap message omits the version. No behavior change, but a future decision record must not expect the version in that message.

6. **[LOW, depth] Range is minor-granular.** `SUPPORTED_VERSIONS` (`GoRttiMapper.java:79`) with patch -1 bounds (`GoVerRange.java:47-52`) means every patch of 1.15 and 1.25 is "tested". The advisory warning therefore never distinguishes patch levels. Consistent with the r14 entry's "advisory range" framing, which I confirm.

7. **[POSITIVE, verified by reading] `getPatchVerDiffFile` has no stale-assignment bug.** `patchDiffFile` can be non-null only when the loop exits on a hit (`:153-156`). At patch 0 it is null. R1 and R4 are therefore correctly null-returning.

8. **[POSITIVE] Missing base is cleanly EMPTY (R5/R7).** The base check precedes diff lookup (`:122-126`), so a diff without a base cannot be applied. No cross-minor fallback exists (`withPatch(0)` at `:122`; `prevPatch` stays in-minor).

## Truth table: the decision-record consequence

- Missing base (`1.26.x`, `≤1.14`): EMPTY → bootstrap message path. Supported by source and inventory.
- Patch 0 with base: exact. Supported.
- Nonzero patch with diff: exact to requested patch (R2). Supported, but labeled by requested version without a content check; the diff carries no version header (inventory).
- Nonzero patch with no diff in minor (1.25.N, N≥1): base content, valid, silent apart from one warn. Must be recorded as a distinct decision row, not as "exact" or "missing base".
- OS/arch exclusion: non-invalid partial snapshot. The missing-bootstrap message cannot be the discriminator on installed data.

## Limits

- Source is S003 (Ghidra 12.1.4 Base-src.zip) only. Not checked: `JsonPatchApplier.java` and `Application.getModuleDataFile` resolution order. The installed data directory is assumed to be what the running Ghidra loads.
- The base-relativity of diffs was spot-checked on one entry (`crypto/tls.buildRetryConfigList`), not replayed.
- `registerStructures` behavior on a partial (non-invalid, wrong-arch) snapshot was not traced; Finding 3's downstream message is [INFERENCE].
- No real go1.25.N target was inspected. Whether real go1.25.N binaries actually fail or produce wrong symbols is not established here; the finding is about what the selector does, not about any historical run.
- Whether GOVERSION strings with rc suffixes reach `GoVer.parse` in that form (R11) is not observed.
- Line numbers are from `cat -n` on the S003 members in this session; they are not re-derived from the registry digest beyond the digest already recorded in SOURCES.md.

## Proposed L1 checks (not executed by this seat)

1. Digest: `sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` equals `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (SOURCES.md S003).
2. Re-run the inventory: count `typeinfo/golang/go1.*.json` = 11; count `patchverdiffs/*.diff` = 123; `ls patchverdiffs | grep -c '^go1.25\.'` = 0; `'all' in` each base's top-level keys.
3. Line anchors: `unzip -p <zip> ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java | cat -n` must show `get` at 102-116, selector 118-166, `getApiFile` 183-192, `isInvalid` 503-505; GoRttiMapper 79, 170-172, 176-181, 351-367 as cited above.
4. In the new decision record, add rows for R4 (patch with no diff, silent base substitution) and for OS/arch exclusion as non-invalid. Confirm the r14 entry's OS/arch sentence is qualified, not repeated.
5. Do not cite `getApiFile` as runtime behavior.
