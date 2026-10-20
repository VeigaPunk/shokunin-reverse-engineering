# Round 15 w1 — SnapshotEntry: installed Go snapshot selection decision record

- Seat: `KaidokuR15.SnapshotEntry` (leaf executor; no subagent dispatch; no live target/provider execution; no build/test/lint/gate run).
- Axes: **depth** (three-layer selection model: file, retained applicability keys, per-type resolution; diagnostic discrimination) and **calibration** (observed source law vs inference vs unknown; S003 and S023 pin scopes kept separate; no historical causality).
- Date: 2026-10-20.
- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Deliverable: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/SnapshotEntry.candidate.md` (provenance trio + source-backed selection decision table; source law only, no inventory numerals, no placeholders).
- This report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/SnapshotEntry.md`.

## Scope and axes moved

C1 asks for a pinned installed snapshot inventory plus a source-selection decision record that discriminates missing base, patch-diff substitution, and OS/architecture applicability without asserting historical target causality. This seat contributes the **decision-record** half only:

- **Depth additions over the r14 entry and the sibling source traces**: an explicit three-decision decomposition (which file, which keys are retained, which type resolves); the request-label/content divergence at `GoApiSnapshot.java:111`; the two distinct invalidities (`GoSnapshot.isInvalid()` vs `GoVer.isInvalid()`) and the divergent log gates they feed; the five diagnostic signals that separate absent base, present-but-empty arches, diff substitution, snapshot IOException, and mapping failure with a valid snapshot; the unreachable `*-cgo` key family; and module-relative data resolution rather than a hard-coded install path.
- **Calibration additions**: S003's pin covers only the source archive (SourceCustody), so installed-data statements cite S023 and its pinned digest; the bootstrap diagnostic is presented as conditional, not as proof; the entry states no counts, no current-target behavior, no decompiler outcome, and no historical cause.

No coverage, operability, freshness, or adjacency claim is made. No new source row was opened or edited; S023 already exists in `corpus/SOURCES.md` with the digest used here.

## Sources and retained evidence

All paths absolute; every command below was run read-only in this seat. No file under `corpus/`, `SKILL.md`, `MANIFEST`, `LOG`, `SCORECARD`, or another seat's paths was modified.

### 1. Pin check (re-derived, not copied from the registry)

```text
$ sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
            /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md \
            /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json
f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804  .../Base-src.zip
c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4  .../ChangeHistory.md
54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252  .../go1.25.0.json
```

Observed: the three digests equal S003, S007, and S023 in `corpus/SOURCES.md`. The S003 pin authenticates the archive only; the installed JSON's identity is S023's pin, and the directory is user-owned (SourceCustody), so no package-manager integrity is implied. `test -d .../data/typeinfo/golang` returned true; no count was taken for the entry.

### 2. Archive member anchors (extracted, then numbered with `awk`)

```text
$ unzip -o -q .../Base-src.zip 'ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java' \
    '.../GoRttiMapper.java' '.../GoTypeManager.java' '.../JsonPatchApplier.java' \
    '.../GoVer.java' '.../GoVerRange.java' '.../GoBuildInfo.java' \
    '.../structmapping/DataTypeMapper.java'
$ wc -l .../GoApiSnapshot.java .../GoRttiMapper.java .../GoTypeManager.java
  534 GoApiSnapshot.java
 1200 GoRttiMapper.java
 1166 GoTypeManager.java
```

Numbered reads used for the entry's anchors:

- `GoApiSnapshot.java`: `get` 102-116 (`archSearchOrder` 108-109, `read(...,goVer)` 111, `EMPTY` 115); `getApiSnapshotJsonFile` 118-146 (base gate 122-126, raw-base bypass 129-131, derived provider 133-145); `getPatchVerDiffFile` 148-166 (loop 153-156, warn 158-160, info 163); `getApiSnapshotFile` 168-178; `IS_GOOS_UNIX` 180-181; `getApiFile` 183-192; `read` 205-240 (skip non-kept 218-221, priority assembly 228-237); `EMPTY` 242; `GoArch` 445-447; `GoTypeDefDeserializer` 450-465 (`default -> null` 463); constructor 494; `getVer` 499; `isInvalid` 503-505; `getFuncdef` 514-520; `getTypeDef` 524-530.
- `GoRttiMapper.java`: `SUPPORTED_VERSIONS` 79; `getSharedGoBinary` 102-128 (Bootstrap catch 114, IOException catch 118, `Failed to read Go info` 121); `getGoBinary` 151-187 (invalid version 165-169, advisory 170-172, snapshot call 176-177, info gate 178-181); `super(program, null)` 331; `new GoTypeManager` 346; `initStructMappings` 351-367 (missing-bootstrap 356-360, other message 364-365); `getType` override 380-395 (catch returns null 391-395).
- `GoTypeManager.java`: `findTypeRec` 402-455; `apiSnapshot.getTypeDef` 449-450; `convertApiTypeDef` 468-480; field type resolution 582.
- `DataTypeMapper.java`: `registerStructure` 172-181; missing-structure throw 180-181.
- `GoVer.java`: `parse` 62-79 (non-version strip 65); `isInvalid` 105-107; `prevPatch` 134-136; `withPatch` 138-140; `toString` 155-159.
- `GoVerRange.java`: `parse` 42-55; `contains` 83-87.
- `GoBuildInfo.java`: GOARCH map 65-73; `getGOOS`/`getGOARCH` and fallbacks 272-327; `go` prefix strip 488-490.
- `Application.java`: `getDataFileInModule` 354-375; single-arg `getModuleDataFile` 954-963.
- `GModule.java`: search roots 47-58; `findModuleFile` 147-155.

### 3. `getApiFile` caller scan (whole archive, not a subtree)

```text
$ python3  # zipfile scan of all .java/.py/.txt/.md/.html/.xml/.properties members
members containing b'getApiFile': 1
ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java
```

Observed: only the definition file mentions `getApiFile`. The entry therefore says "no Java member of this archive calls it", not that no extension or downstream fork could.

### 4. S007 anchor

```text
$ grep -n "^# " /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md
564:# Ghidra 12.0 Change History (December 2025)
$ sed -n '585p' .../ChangeHistory.md
* _Analysis_. Added support for Golang 1.24 and 1.25.  Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files. (GP-5470)
```

The entry quotes only the 17-word second sentence and scopes it to the installed release's own history.

### 5. S023 anchor used in the entry

The S023 registry anchor records SHA-256 `54d10162…f16252` and JSON `all.Types.runtime.moduledata.Fields[1]`. L1 observed the raw snippet `"Name":"pcHeader","DataType":"*runtime.pcHeader"`. A targeted query of the pinned file (not a count) was run by this seat:

```text
$ python3 - <<'PY'
import json
p='/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json'
d=json.load(open(p))
names=('runtime.moduledata','runtime.pcHeader')
for k in sorted(d):
    t=d[k].get('Types') or {}
    hit=[n for n in names if n in t]
    if hit: print(k, hit, [t[n].get('Kind') for n in hit])
print('absent-from:', sorted(k for k in d if not any(n in (d[k].get('Types') or {}) for n in names)))
PY
all ['runtime.moduledata', 'runtime.pcHeader'] ['struct', 'struct']
absent-from: ['386', 'amd64', 'arm', 'arm64', 'cgo', 'darwin', 'darwin-amd64', 'darwin-amd64-cgo', 'darwin-arm64', 'darwin-arm64-cgo', 'linux', 'linux-386', 'linux-386-cgo', 'linux-amd64', 'linux-amd64-cgo', 'linux-arm', 'linux-arm-cgo', 'linux-arm64', 'linux-arm64-cgo', 'linux-cgo', 'unix', 'windows', 'windows-386', 'windows-386-cgo', 'windows-amd64', 'windows-amd64-cgo']
```

No other bucket's `Types` map contains either name; the "absent-from" list covered every remaining key, including `amd64`, `linux`, `unix`, and the `-cgo` variants. That is bucket placement for two names, not a general inventory count, and it does not show what those structs contain beyond the S023 anchor and the `Kind` values above. The entry attributes the S023 schema snippet to the registry anchor and this placement query to the pinned file; it does not claim registration or recovery.

## What the entry establishes (and refuses)

Established as source observation, with anchors in the candidate:

1. File selection is base-first and minor-bound; a missing `go<M>.<m>.0.json` returns `EMPTY` before any diff lookup, and no cross-minor fallback exists.
2. Patch diffs are named `patchverdiffs/go<M>.<m>.<p>.json.diff`; selection decrements only the patch; an exact hit logs info, a lower/absent hit logs a warn, and the fallback diff or raw `.0` base is then applied.
3. The snapshot object is stamped with the **requested** version even when lower-patch bytes were used, so `getVer()`, the derived provider name, and the mapper info line are labels, not byte provenance.
4. Applicability is a five-slot priority list (`os-arch`, `os`, `unix` when applicable, `arch`, `all`); only listed keys are parsed and only matching keys are retained in priority order; per-type lookup takes the first definition and does not merge, though each field type resolves independently by name.
5. `GoApiSnapshot.isInvalid()` is `arches.isEmpty()`, while the info-log gate uses `GoVer.isInvalid()`; a present file with no retained key logs the info line yet still reaches the missing-bootstrap branch, whereas an absent base logs neither.
6. The missing-bootstrap message has no `%s`, so it cannot identify a version; the separate `Invalid Go bootstrap struct mapping info` message requires a non-invalid snapshot.
7. `*-cgo` keys are never constructed into the search list; definitions only under those keys are outside the retained set (inference; not measured for need).

Refused in the entry:

- No file counts, per-minor diff ranges, or coverage ratios. Those are the companion inventory seat's observations and L1's to pin.
- No claim that any current target is Go 1.25.N, that bootstrap succeeds, or that a specific installed diff fails to apply.
- No claim that the selector explains the r14 historical run; its cause remains UNKNOWN.
- No claim that S003 source equals executing `Base.jar` bytecode.
- No claim that OS/arch exclusion yields `isInvalid()` on installed data; the entry explicitly qualifies r14 `:51-54` and table row `:77`.

## Comparison with the integrated record (read-only)

After this draft was written, L1 created `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` from direct source and JSON opens. It is not edited here. Against the pinned archive, its cited anchors and claims check out, including `GoApiSnapshot.java:111,115,122-126,128-145,148-166,205-239,503-505`, the mapper info line `:178-181`, and the virtual-dispatch chain `DataTypeMapper.java:176,310-313` → `GoRttiMapper.java:379-396` → `GoTypeManager.java:355-358,402-455`. I found no substantive factual error to report.

Two wording items are worth a final read rather than a correction:

1. The table row "Missing bootstrap definition during registration … Snapshot validity only chooses error text" understates the branch. `GoRttiMapper.java:356-365` selects a `BootstrapInfoException` for an invalid snapshot and a distinct `IOException` for a valid one; both abort mapper construction, but by different routes (`:114-122`) and with different severity. "Also selects which exception route aborts construction" would match the source.
2. Its recheck line already names `.ufo/waves/round-15/snapshot-inventory.py` and `inventory.json`; those must exist with pinned output before commit, per L1's addendum plan. No check was run here.

Parts of this draft that the integrated record does not currently state, and that L1 may fold if useful (not a request to widen scope):

- The log discriminator between absent base and present-but-empty arches: `EMPTY` has an invalid `GoVer`, so the mapper info line is skipped (`GoRttiMapper.java:178-181`), while a present file with no retained key has a valid requested `GoVer` and does print it (`GoApiSnapshot.java:111,239`). Both can then reach the same bootstrap text.
- The separate `Failed to read Go info` route for a snapshot-path `IOException`, including a patch parse/apply failure (`GoRttiMapper.java:118-122`; `JsonPatchApplier.java:118,151,158`).
- The exact `isInvalid()` split: `arches.isEmpty()` versus `major==0 && minor==0` (`GoApiSnapshot.java:503-505`; `GoVer.java:105-107`).
- The missing-bootstrap literal has no `%s`, so `.formatted(goVer)` emits no version (`GoRttiMapper.java:359-360`).
- `*-cgo` keys never enter the constructed search list (`GoApiSnapshot.java:51-81,108-109`).
- `getApiFile`'s two-segment fallback is uncalled and is not the live path (`GoApiSnapshot.java:183-192`; archive-wide scan below).
- Module-relative data resolution with `build/` and shadow-module roots (`Application.java:354-375,954-963`; `GModule.java:47-58,147-155`).
- The `GoArch.Funcs`/`Types` null guard gap and `Kind` deserializer null return (`GoApiSnapshot.java:445-447,450-465`).

Overlap note for the depth judgment: base-first ordering, the patch-decrement loop, and the five-slot key order are re-statements needed to make the decision table self-contained; they are not claimed as new depth. The added distinctions are the label/content split, the three-layer selection model, the diagnostic matrix, the two-invalidity split, cgo exclusion, and the dead-helper caveat.

## Cross-seat observations for L1 adjudication

These are discrepancies I observed while aligning the candidate; none is a verdict on another seat.

1. **Stale diff count.** `ArchLookup.md` §1 says "11 base JSON files, 89 patch diffs"; `InstalledLayout.md`, `PatchLookup.md`, `BaseLookup.md`, and `ReviewPatchCases.md` say 123. `InstalledLayout.md` already flags the 89 figure as an earlier incomplete census. L1's inventory must own the number; the candidate avoids it.
2. **`EMPTY` anchor.** `BaseLookup.md` cites `GoApiSnapshot.java:249`; the archive line is 242 (`grep` verified). The candidate uses 242.
3. **Line drift in sibling anchors.** `ArchLookup.md` cites `IS_GOOS_UNIX` at `:173-174` (actual 180-181), `getTypeDef` at `:519-525` (actual 524-530), and `read` spans that end at 244 (actual 240). `PatchLookup.md` cites the mapper info log at `:137-140` (actual 178-181), `getSharedGoBinary` at `:99-102` (actual 102), and gives `JsonPatchApplier.java` as 152 lines (actual 162) and `JsonPatch.java` as 215 (actual 217). Their reasoning is consistent with the source; only the coordinates need re-derivation before folding.
4. **Overstated fidelity language.** `PatchLookup.md` labels exact-patch cases "Full fidelity" and fallback cases "Type drift / fatal abort". Source supports file-level substitution and per-name lookup; it does not support measured decompiler fidelity or a guaranteed abort. The candidate uses "bytes returned / label / log" and keeps outcomes conditional.
5. **Conditional bootstrap claim.** `BaseLookup.md` §4 says the source chain "proves" Ghidra 12.1.4 fails on Go 1.26 binaries. The message selection is source law, but it fires only if `registerStructures` throws; this candidate keeps that condition visible and does not assert failure for any target.
6. **`GoRttiMapper.java:359` formatting.** Confirmed: the literal has no placeholder, so `.formatted(goVer)` is a no-op. This affects log reading, not selection.
7. **S023 scope.** S023 pins one installed base file, not the installed set. The candidate states that limit explicitly and leaves the set to the inventory record.
8. **Parent-supplied patch-case depth.** Confirmed at source: `read(..., goVer)` stamps the requested patch while A4/A5 may supply lower-patch bytes. The candidate makes this its Decision-1 headline rather than a footnote.

## Limits of this seat's work

- Read-only source inspection; no Ghidra headless run, no REA provider call, no Go binary inspection, no analyzer log replay.
- The installed JSON was hashed and queried only for the bucket placement of `runtime.moduledata` and `runtime.pcHeader`; no full parse, key census, or diff application was performed here. S023's schema snippet and the `Fields[1]` detail are cited from the registry anchor.
- Diff files were not replayed; the non-cumulative, base-relative property is taken from `JsonPatchApplier` construction plus the sibling inventory's spot check, and the entry only claims the loader applies one diff to the base.
- `.gdt` coexistence was not re-examined; the entry relies on `super(program, null)` and S007 only for the JSON path, and makes no GDT capability claim.
- Source companion vs compiled classes was not checked by this seat; the range constant's bytecode match is `InstalledLayout.md`'s observation.
- No LSP route was exposed for archive members (not a loaded Java project); symbol relationships were established by extraction plus `grep`/`read`, and no LSP result is claimed.
- Line numbers are from this seat's extracted copies numbered with `awk`; they match the anchors in `ReviewPatchCases.md` where both cite the same regions, except where noted above.
- Tool installs/updates: none.

## Proposed L1 checks (named, not executed)

1. **Pins:** `sha256sum` on S003, S007, S023; compare to the three values above and to `corpus/SOURCES.md`.
2. **Anchors:** `unzip -p <Base-src.zip> <member> | cat -n` for `GoApiSnapshot.java` 102-116, 118-146, 148-166, 168-178, 183-192, 205-240, 242, 445-447, 450-465, 494-505, 514-530; `GoRttiMapper.java` 79, 102-128, 165-172, 176-181, 331, 346-367, 380-395; `GoTypeManager.java` 402-455, 582; `DataTypeMapper.java` 172-181; `GoVer.java` 62-79, 105-107, 138-159; `GoVerRange.java` 42-55, 83-87; `GoBuildInfo.java` 65-73, 272-327, 488-490; `Application.java` 354-375, 954-963; `GModule.java` 47-58, 147-155.
3. **Dead-helper check:** archive-wide scan for `getApiFile` must return only `GoApiSnapshot.java`; confirm the candidate does not present it as runtime behavior.
4. **Inventory (L1-owned):** count base JSONs and `patchverdiffs/*.diff`; confirm the 1.25 diff count and the absent next-minor base per the inventory record; verify `go1.25.0.json` digest and `jq` path `.all.Types.runtime.moduledata`.
5. **Integration shape:** fold the candidate into `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` (the file S023's used-by cell names) rather than committing two competing entries; keep one provenance trio and one decision table; update `corpus/README.md` coverage mapping and S023's used-by if the final stem differs.
6. **Text gates:** confirm the entry contains no inventory counts or placeholders; no "bootstrap succeeds", "current target", or causal claim about the r14 run; the r14 qualification cites `:51-54` and `:77`; the S007 quotation is exact, contiguous, and ≤25 whitespace words; `getApiFile` is not cited as live behavior.
7. **Canonical validators (not run here):** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`; the lane's ordinary citation/coverage checks if the manifest names them.
8. **Consistency:** re-read `ReviewPatchCases.md` rows R3/R4 against candidate rows A4/A5; both must describe requested-label vs applied-bytes identically.

## Files changed

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/SnapshotEntry.candidate.md` (new; entry draft).
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/SnapshotEntry.md` (this report).

No other repository file was written; probe extractions were confined to `/tmp`.
