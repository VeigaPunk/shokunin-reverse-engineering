# AttackCausality — round 15 critic (depth, calibration)

Seat: `KaidokuR15.AttackCausality` (leaf critic; no dispatch, no edits outside this file).
Access date: 2026-10-20. Method: source reading of S003, a non-verdict inventory of installed
data, a constant-pool string check of the compiled `Base.jar`, and one read of an S004 member.
No Ghidra, REA, target, gate, test, build, or linter was executed. Tool installs/updates: none.

Target inferences attacked:

- **(I1)** The absence of installed `go1.26.0.json` proves why the historical `op` 2.40.0 run failed.
- **(I2)** Adding a snapshot repairs Go 1.26 support.

Verdict: **both rejected.** I1 is also *overdetermined*. Under the installed 12.1.4 classes,
source reading predicts the analyzer-level outcome fails with or without the base JSON. The
JSON's absence selects *which message* appears, not *whether* recovery fails.

## Strongest counterexample (rejects I2 and weakens I1 to message selection)

Added: upstream `go1.26.0.json` at S004 commit `385e8cd923d09f10b1a7874108e71748875fa174`.
Read with installed 12.1.4 struct-mapping classes. These are source predictions, not executions.

| Required binding in 12.1.4 | Installed source/bytes | `go1.25.0.json` (installed) | `go1.26.0.json` (S004 member) |
|---|---|---|---|
| `GoMapType` structure names `runtime.maptype`, `internal/abi.MapType`, `internal/abi.OldMapType`; non-optional, ungated `@FieldMapping` `bucket`, `keysize`, `elemsize`/`ValueSize`, `bucketsize` | `rtti/types/GoMapType.java:32-63` (Base-src.zip); `Base.jar` `GoMapType.class` contains `bucket` (3 hits) and no `-1.25`, `1.26-`, or `group` | `runtime.maptype` is an alias to `internal/abi.OldMapType` with fields `Bucket, KeySize, ValueSize, BucketSize`. Binds. | No `runtime.maptype` and no `OldMapType`. `internal/abi.MapType` fields are `Type, Key, Elem, Group, Hasher, GroupSize, SlotSize, ElemOff, Flags`. **4 required fields missing.** |
| `GoPcHeader.textStart`, `presentWhen = "1.18+"` | `rtti/GoPcHeader.java:180-182`; `Base.jar` `GoPcHeader.class` has `1.18+` and lacks `1.18-1.25` | `runtime.pcHeader` contains `textStart`. Binds. | The `runtime.pcHeader` slot is named `_`. **Missing.** |

Derived control flow (S003 anchors):

1. Field binding is eager at registration. The `StructureMappingInfo` constructor calls
   `readFieldInfo` (`StructureMappingInfo.java:~83, 268-285`).
2. A missing, non-optional, present-when-true field throws `IllegalArgumentException`
   `Missing structure field` (`:315-323`).
3. `DataTypeMapper.java:190-196` rewraps that exception as `IOException`.
4. The snapshot is now valid, so `initStructMappings` throws
   `IOException("Invalid Go bootstrap struct mapping info: …")` (`GoRttiMapper.java:363-365`).
5. `getSharedGoBinary` catches it at `:118-123` (`Failed to read Go info`) and returns null (`:125`).
6. `GolangSymbolAnalyzer.java:133-137` logs `unable to get GoRttiMapper` and returns false.

This is the same terminal state that the EMPTY-snapshot branch reaches
(`GoRttiMapper.java:356-360`, then `:114-117`).

Corroboration that upstream needed these code changes: the S004 diff gates `GoMapType.bucket`,
`keysize`, `elemsize`, and `bucketsize` as `-1.25`. It adds `group` as `1.26-`, changes
`GoPcHeader.textStart` to `1.18-1.25`, and also changes `GoModuledata.getFirstModuledata`
(`go.module` section), `GoTypeFlag`, and `GoBuildId`.

Calibration control: the same static census reports **no** missing required field for
`go1.25.0.json` at 1.25.7. That matches the retained historical success on `op` 2.34.1 (33,060
procedures; `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:66-68`).

Limits:

- The census reads only declared fields in each class file, not superclass fields. It can
  under-report missing fields, not invent them. Its one false positive (`GoString` →
  primitive `string`) appears identically in the 1.25 control.
- The `Base.jar` check is string presence only, not bytecode equivalence with the source.
- Nothing after registration (moduledata location, type-flag validation) was evaluated.
  Those steps are **UNKNOWN**, and do not need to be known to reject I2.

## Further evidence against I1

1. **Unretained, contested attribution.** The only link from the historical run to the
   bootstrap branch is a transient `ghidra.log` line whose directory was deleted
   (`2026-10-13-r4-10-real-version-pair.md:71-73`). That round ran under fleet load with
   "16+ parallel Ghidra jobs" (`:156-157`). Whether the log was per-process is UNKNOWN, so
   attributing the line to the 2.40.0 import is unverified.
   Without that line, other source branches give the same `FUN_*` outcome with different or no
   messages:
   - `GoBuildInfo` null → no message at `getGoBinary:160-162`.
   - Invalid version → `Invalid Go version string` (`:166-168`).
   - Post-registration `init` failure → `Failed to read Go info` (`:110`, `:444-466`, `:1133-1135`).
2. **Install identity is supported, not proved.**
   - Install root birth is `2026-10-12 09:50:47 -0300`. `go1.25.0.json` and `Base.jar` have
     birth and ctime on `2026-10-12`, before the 2026-10-13 run. No metadata change has
     occurred since.
   - `application.properties`: version `12.1.4`, revision `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`.
   - `Base.jar` sha256 `5ce4a06970f6d0a5c1458d627443a4e474742e06208e8f9c001679bd17f0b7bf`.
   - The historical entry names "Ghidra 12.1.4 headless" (`:8`). Which install path REA used
     was not retained. [INFERENCE] It is probably the same install, but that is not proved.
3. **The 2.34.1 → 2.40.0 contrast is not a one-variable experiment.** The binaries differ in
   Go minor version (1.25.7 → 1.26.8), map ABI (swiss-only `abi.MapType` in the 1.26
   snapshot), pcHeader layout, and size. Snapshot presence is one of several co-varying factors.

## Explicit rejected candidates

| # | Candidate | Decision | Evidence |
|---|---|---|---|
| X1 | "Installed `go1.26.0.json` absence proves the historical `op` 2.40.0 failure cause." | reject | Overdetermined under the 12.1.4 classes (table above). The message evidence was unretained and its attribution is contested. The historical cause remains **UNKNOWN**. |
| X2 | "Adding `go1.26.0.json` to the installed 12.1.4 repairs Go 1.26 support." | reject | Source-predicted `Missing structure field` on `GoMapType` (4 fields) and on `GoPcHeader.textStart`. The analyzer still returns false through the IOException branch. |
| X3 | "A snapshot plus the range edit `1.15-1.26` repairs support." | reject | The range is advisory (`GoRttiMapper.java:170-172`: log only, no throw/return). It does not affect field binding. |
| X4 | "Set the analyzer's `fallbackGoVer` to 1.25 to reuse `go1.25.0.json`." | reject | The fallback applies only when `buildInfo` is null or its version is invalid (`GoRttiMapper.java:153-159`; set at `GolangSymbolAnalyzer.java:129-131`). A validly parsed 1.26.8 never reaches it. |
| X5 | "Missing patch diffs (1.25.x, or 1.26.1-8) cause failure." | reject | `getPatchVerDiffFile` falls back to base with a warning (`GoApiSnapshot.java:148-166`). Installed and upstream-at-S004 both have 123 diffs, the highest being 1.24.6, with no 1.25.x or 1.26.x diffs. Historical 1.25.7 succeeded on base content. The real hazard is calibration, not failure: the result is labelled with the requested version (`:111`, `:239`; `GoRttiMapper.java:178-180`). |
| X6 | "OS/arch exclusion is a live alternative cause of an invalid snapshot on this installation." | reject (installed data) | `"all"` is always in the search order (`GoApiSnapshot.java:108-109`). All 11 installed bases contain a non-empty `all` (types 2,421-3,741) and `linux-amd64`/`linux`/`unix`/`amd64`. The upstream 1.26 file also has all five. Exclusion is source-possible only for hypothetical files; on installed data, applicability changes shadowing and never sets `isInvalid()`. |
| X7 | "S004 proves upstream support works on `op` 2.40.0." | reject | Not executed. S004 also adds no 1.26 patch diffs, so 1.26.8 would load 1.26.0 content labelled 1.26.8. |
| X8 | "Today's inventory equals what the historical process read." | admit only as bounded [INFERENCE] | Birth and ctime support it (item 2 above); provider path selection was unretained. |

## Peer-artifact defects found (routed to L1; I did not edit them)

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/EvidenceChain.md:23`
  says "98 patch diff files". **Observed: 123** (15+15+13+10+13+14+13+12+12+6). This agrees
  with `ReviewPatchCases.md:36-37`. Do not integrate 98.
- `EvidenceChain.md:148` "Barrier C: OS/arch keys unrepresented" is vacuous on installed data (X6).
- `EvidenceChain.md:151` says 12.1.4 "cannot succeed on Go 1.26 … without a snapshot". That
  states a necessary condition, but integrated text must add "and is not predicted to succeed
  with the snapshot alone (X2)". Otherwise it implies sufficiency.
- `ArchLookup.md:146-153` calls the two invalid-snapshot pathways "mutually exclusive causes"
  and anchors Pathway B at `:242`. Pathway B is actually constructed at `GoApiSnapshot.java:239`;
  `:242` is the `EMPTY` definition. Also, Pathway B is unreachable for installed files (X6).
- `SnapshotIntent.md:18`, "a JSON file may exist but still produce an invalid snapshot", is true
  only for hypothetical files. Qualify it with X6.

## Smallest safe correction (impacted axes: depth, calibration)

The C1 decision record or knowledge entry should add these rows without rewriting prior text:

1. **Base JSON added, 12.1.4 classes unchanged.** Snapshot lookup becomes valid. Do not
   conclude that support is repaired. Next evidence: compare each required `@FieldMapping`
   against the snapshot struct (`GoMapType` and `GoPcHeader` above). In source, the predicted
   branch is `Invalid Go bootstrap struct mapping info`.
2. **Missing base JSON.** This is a necessary-condition explanation for *message selection* only.
   On 12.1.4 the outcome is overdetermined. Historical cause: UNKNOWN.
3. **OS/arch applicability on installed data.** Shadowing only, never invalidation, because
   `"all"` is present in all 11 bases.
4. **Patch diff absent.** Base substitution is labelled with the requested patch version; the
   log does not prove a patch-exact snapshot.

Cite the upstream file as an S004 member (`Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json`
at `385e8cd9…`, sha256 `66af006eb4183d817c9ce9f9064507f716572a0c469db45686d9a36cc79e672d`,
10,556,117 bytes). It is in the already-registered S004 commit, so no new source row is needed.
None of this changes C2, and no gate change is implied.

## Proposed L1 checks (not run by this seat)

```sh
G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base
Z=$G/lib/Base-src.zip
sha256sum $Z $G/lib/Base.jar   # f00d29c2… / 5ce4a069…
ls $G/data/typeinfo/golang/go1.*.0.json | wc -l          # 11
ls $G/data/typeinfo/golang/patchverdiffs | wc -l         # 123
ls $G/data/typeinfo/golang/patchverdiffs | grep -c '^go1\.2[56]\.'   # 0
unzip -p $Z ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java | sed -n '32,63p'
unzip -p $Z ghidra/app/util/bin/format/golang/rtti/GoPcHeader.java | sed -n '170,202p'
unzip -p $Z ghidra/app/util/bin/format/golang/structmapping/StructureMappingInfo.java | sed -n '268,323p'
unzip -p $Z ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | sed -n '102,129p;151,188p;351,367p'
curl -sSL -o /var/tmp/go1.26.0.json https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/385e8cd923d09f10b1a7874108e71748875fa174/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json && sha256sum /var/tmp/go1.26.0.json
python3 -c "import json;d=json.load(open('/var/tmp/go1.26.0.json'))['all']['Types'];print([f['Name'] for f in d['internal/abi.MapType']['Fields']],[f['Name'] for f in d['runtime.pcHeader']['Fields']],'runtime.maptype' in d)"
python3 -c "import json;d=json.load(open('$G/data/typeinfo/golang/go1.25.0.json'))['all']['Types'];print(d['runtime.maptype'],[f['Name'] for f in d['internal/abi.OldMapType']['Fields']])"
stat -c '%n %w %z' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC $G/lib/Base.jar
```

Expected results are stated in the sections above. Scratch extraction under `/tmp/acaus` was
removed after writing this report. No repo, corpus, SOURCES, QUALITY, or SKILL file was touched.
