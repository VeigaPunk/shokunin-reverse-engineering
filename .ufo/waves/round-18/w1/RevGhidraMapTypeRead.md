# RevGhidraMapTypeRead — Ghidra 12.1.4 Go map-type descriptor / uncommon read path

Seat: `KaidokuR18.RevGhidraMapTypeRead` (author-side advisory, leaf; no subagents, no REA, no Ghidra run,
no carrier execution). Axes worked: **calibration** (exact anchors, observed vs inferred), **operability**
(the offset formula + pasteable commands), **depth** (full read path including the snapshot-JSON size law
and the EOF condition).

Artifact under test: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
sha256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`.
All `path:line` anchors below are zip members; I extracted them to a throwaway `/tmp` dir and the line
numbers reproduce the retained 12.1.4 stack frames exactly (see §6), so the anchors are calibrated to the
shipped bytes, not to a guess.

---

## 1. Direct answers

### 1.1 The uncommon/method offset formula Ghidra uses

```
U = T + L_json(M)                    (read site: GoType.getUncommonType)
L_json(M) = mappingInfo.getStructureLength() = structureDataType.getLength()
```

- `T` = start VA of the type descriptor (`runtime._type` / `internal/abi.Type`), captured as
  `StructureContext.structureStart = reader.getPointerIndex()` at context construction
  (`Base-src.zip!ghidra/app/util/bin/format/golang/structmapping/StructureContext.java:76-84`).
- `L_json(M)` = length of the Ghidra `Structure` bound to the class by `@StructureMapping`, which is built
  from the installed snapshot JSON, not from the binary
  (`StructureMappingInfo.java:114-119`, `StructureContext.java:190-193,200-205`).
- Read site: `Base-src.zip!.../rtti/types/GoType.java:144-149`

```java
public GoUncommonType getUncommonType() throws IOException {
    if (uncommonType == null && typ.hasUncommonType()) {
        uncommonType =
            programContext.readStructure(GoUncommonType.class, context.getStructureEnd());
    }
    return uncommonType;
}
```

`hasUncommonType()` is tflag bit 0 (`GoBaseType.java:100-102`, `GoTypeFlag.java:28`); tflag is read at
`internal/abi.Type` offset 20 (`JSON`-derived component offsets, §3).

**Which struct binds for a map type.** `GoMapType` declares the name list
`{"runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType"}`
(`.../rtti/types/GoMapType.java:31-34`). `DataTypeMapper.getType(List, clazz)` tries them in order
(`structmapping/DataTypeMapper.java:310-320`); the dispatch lands in `GoRttiMapper.getType(String, Class)`,
which accepts only a `Structure` instance (`Clazz.isInstance(result)`, `.../rtti/GoRttiMapper.java:380-391`).

- `runtime.maptype` in the installed go1.24.0/go1.25.0 JSON is an **alias** to `internal/abi.OldMapType`
  (positions `$GOROOT/runtime/map_noswiss.go:67:6` and `:68:6`). `convertAliasDef` returns a
  `TypedefDataType` (`GoTypeManager.java:549-557`), which is **not** a `Structure` and is rejected.
- `internal/abi.MapType` is **absent** from both JSON files (observed, all arch maps).
- Therefore **`internal/abi.OldMapType` binds**, and `L_json = 88` on amd64 (56 on 386).

The true runtime layout for Go ≥1.24 default (Swiss) builds is `internal/abi.SwissMapType` = **112 bytes**
(64 on 386). So the uncommon struct is read at `T+88` while it really begins at `T+112`: **−24 bytes** on
amd64, **−8 bytes** on 386.

Concrete field consequences of reading the uncommon at `T+88` in a true Swiss descriptor:

| Ghidra `GoUncommonType` field | Read at | Actually reads (Swiss) |
|---|---|---|
| `pkgpath_nameOff` (4 bytes) | `T+88` | low 32 bits of `SlotSize` (uintptr) |
| `mcount` (2 bytes) | `T+92`(*) | bits 32-47 of `SlotSize` (normally 0) |
| `xcount` (2 bytes) | `T+94`(*) | bits 48-63 of `SlotSize` (normally 0) |
| `moff` (4 bytes) | `T+96` | low 32 bits of `ElemOff` |

(*) The struct-built offsets come from the JSON; `internal/abi.UncommonType` is
`PkgPath`@0, `Mcount`@4, `Xcount`@6, `Moff`@8, `_`@12, length 16 — so relative to `U=T+88` the reads are
`T+88`, `T+92`, `T+94`, `T+96`. The real `Flags` at `T+104` is never read. (Observation: code + JSON;
arithmetic is mine.)

### 1.2 Which `BinaryReader` call raises `Unable to read past EOF: A, B`

Not `BinaryReader` itself — the message is formatted by the `ByteProvider` that backs the reader.
For the Go analyzer the reader is built from program memory:

- `DataTypeMapper.createProgramReader()` → `new MemoryByteProvider(program.getMemory(),
  program.getImageBase().getAddressSpace())` (`structmapping/DataTypeMapper.java:510-514`). The
  AddressSpace ctor delegates to the base-address ctor with `space.getMinAddress()`
  (`ghidra/app/util/bin/MemoryByteProvider.java:117-136`), i.e. index space starts at 0.
- Throw site: `MemoryByteProvider.ensureBounds`, line 312:
  `"Unable to read past EOF: %s, %d".formatted(Long.toUnsignedString(index), length)`
  (`MemoryByteProvider.java:289-313`).
- Call chain for a Go name: `BinaryReader.readNextByteArray(int)` (`BinaryReader.java:703-708`) →
  `BinaryReader.readByteArray(long,int)` (`BinaryReader.java:1169-1176`) →
  `ByteProvider.readBytes(index,length)` → `ensureBounds` (`MemoryByteProvider.java:264-270`).

**A and B** (the two numbers in the message):

- **A = `index`**, printed unsigned (`Long.toUnsignedString`): the provider index of the first requested
  byte. Because this provider's base is the default address space minimum (0), A is the **absolute
  program address/VA** of the first byte requested. (For `FileByteProvider.java:275` the same field is a
  file offset; for `ByteProviderWrapper.java:129`/`RangeMappedByteProvider.java:227` it is that wrapper's
  index. Same formatting, provider-relative meaning.)
- **B = `length`**, printed with `%d`: the requested byte count (signed long). The guard is
  `length != 0 && unsigned(length - 1) > (maxOffset - index)`, where `maxOffset` is the highest address of
  the address space minus the base (inclusive) (`MemoryByteProvider.java:41,155-162,289-313`).

For a `GoVarlenString` (Go name text), B is exactly the LEB128 `strlen` value decoded at
`GoVarlenString.java:65-74`, and A is the reader position immediately **after** that LEB128.

---

## 2. The algorithm, numbered

1. **Analyzer entry.** `GolangSymbolAnalyzer.added` builds a `GoRttiMapper`, then calls
   `goTypes.markupGoTypes(...)` (`Base-src.zip!ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:146`);
   any `IOException` is logged as `Go analysis failure` (`:182`).
2. **Bootstrap/type census.** `GoTypeManager.init` walks each `GoModuledata` type list and reads every
   type (`GoTypeManager.java:96-123`). `GoRttiMapper` created `goTypes` and registered the structure
   mappings in its ctor (`GoRttiMapper.java:331` `super(program, null)`; `:346`; `:353`
   `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`; list at `:294-301`).
3. **Kind detection.** `GoType.getSpecializedTypeClass` reads a `GoTypeDetector` at the type VA — a stub
   that binds only the `kind`/`Kind_` field of `internal/abi.Type` (`GoType.java:56-70`,
   `types/GoTypeDetector.java:29-33`) — then maps `GoKind.Map` (ordinal 21, `GoKind.java:47`, masked by
   `parseByte` `:69-74`) to `GoMapType` (`GoType.java:37-46`).
4. **Descriptor read.** `DataTypeMapper.readStructure(class, position)` clones the program reader, sets the
   pointer index to `T`, and reads the mapped fields (`DataTypeMapper.java:448-450,472-476`). Each Java
   field is read from its `DataTypeComponent.getOffset()` within the bound Structure
   (`StructureContext.java:232-236,245-251`; `FieldMappingInfo.java:44-52`), so the read offsets are the
   JSON-derived component offsets, **not** sequential field order.
5. **Map-specific fields** are read at the JSON offsets (`GoMapType.java:39-62`): `key`@48, `elem`@56,
   `bucket`@64, `hasher`@72, `keysize`@80, `elemsize`@81, `bucketsize`@82, `flags`@84 (OldMapType binding).
6. **Uncommon flag.** `GoBaseType` reads `tflag`@20 and exposes bit 0 (`GoBaseType.java:47-66,100-102`).
7. **Uncommon read.** Only when the flag is set: `readStructure(GoUncommonType.class, T + L_json)`
   (`GoType.java:144-149`). `L_json` is the bound Structure's length (§1.1, §3).
8. **Uncommon layout.** `runtime.uncommontype` is an alias (Typedef, rejected by the same
   `Structure`-instance filter), so `internal/abi.UncommonType` binds: `PkgPath`@0 (4), `Mcount`@4 (2),
   `Xcount`@6 (2), `Moff`@8 (4), `_`@12 (4), length 16
   (`GoUncommonType.java:29-33`, JSON; `types/GoUncommonType.java:41-50`).
9. **Package path.** `getPkgPath()` → `GoRttiMapper.resolveNameOff(uncommonStart, pkgpath_nameOff)`
   (`GoUncommonType.java:57-60`) → `module.getTypesOffset() + off` → `getGoName` →
   `readStructure(GoName.class, nameStart)` (`GoRttiMapper.java:1053-1068,1073-1075`).
10. **Name read.** `GoName.readStructure`: 1 flags byte; `GoVarlenString` name (LEB128 length then bytes)
    (`GoName.java:79-100`); optional tag when flag 0x02; optional `int32` pkgPath when flag 0x04
    (`GoName.java:86-90`). LEB128 is used for Go ≥1.17 (`GoVarlenString.java:39,65-74`) and the value is
    narrowed to `int` before `readNextByteArray`.
11. **Recursive pkgpath resolution.** `GoName.pkgPath` is marked `@MarkupReference("getPkgPath")`
    (`GoName.java:89-90`); markup calls the getter (`FieldMappingInfo.java:288-300`), which resolves
    another `GoName` (`GoName.java:123-126`). This is a recursive name chain; each level can point anywhere
    the 32-bit NameOff allows.
12. **Method slice.** `getMethodsSlice()` = `new GoSlice(context.getFieldLocation(moff), mcount, mcount,
    programContext)` (`GoUncommonType.java:73-75`), i.e. array VA = `U + moff`, len = cap = `mcount`.
    `getMethods()` validates `array + len*sizeof(GoMethod) <= memory` and otherwise warns
    `Bad uncommon method list` and returns empty (`GoUncommonType.java:81-89`; `GoSlice.java:118-140,
    349-358`). `GoMethod` binds `internal/abi.Method` = 16 bytes (`types/GoMethod.java:30,41-53`).
13. **End of type info.** `getEndOfTypeInfo()` = `U + moff + mcount*16` when mcount != 0, else `U+16`
    (`GoUncommonType.java:95-104`); `GoType.getEndOfTypeInfo` delegates to it when the uncommon flag is set
    (`GoType.java:137-141`), else returns `T + L_json`.
14. **Markup.** `GoType.additionalMarkup` marks the method array and labels the uncommon struct
    (`GoType.java:225-238`); `markupGoTypes` drives it (`GoTypeManager.java:148-155`). Getters invoked by
    markup are where name/pkgpath I/O actually happens, so malformed offsets surface here rather than in
    the census.

---

## 3. Structure-size computation from the snapshot JSON

Selection law (observation, code):

- `GoRttiMapper.get` picks the snapshot from `GoVer`, `GOARCH`, `GOOS`
  (`GoRttiMapper.java:171-187`).
- `GoApiSnapshot.get` searches `[goOS-goArch, goOS, unix?, goArch, all]`
  (`GoApiSnapshot.java:102-115`); the file is `go<major>.<minor>.<patch>.json`, falling back to
  `go<major>.<minor>.0.json` plus the nearest earlier `patchverdiffs/*.diff`
  (`GoApiSnapshot.java:117-168`). The retained log shows exactly this fallback for aether:
  `Falling back from 1.25.14 to 1.25.0 for Go API snapshot` (log:92), and the installed
  `patchverdiffs/` contains **0** files matching `1.25`.
- `GoApiSnapshot.read` keeps the requested arch maps in a `LinkedHashMap` in search order
  (`:205-240`); `getTypeDef` returns the first arch map containing the name (`:523-532`).
- Note: the snapshot object's `ver` is the requested version, so the log's
  `Using Go API snapshot for version 1.25.14` (log:93) does **not** mean 1.25.14 bytes were used.

Size law (observation, code), `GoTypeManager.getDataTypeLength`:

```
size(T) / align(T):
  primitives per getTypeLength: bool/int8/uint8 (1,1), int16/uint16 (2,2), int32/uint32 (4,4),
    int64/uint64/float64 (8,8), float32 (4,4), complex64 (8,8), complex128 (16,16),
    int/uint/uintptr -> (ptrSize, ptrSize), string -> (2*ptrSize, ptrSize),
    func -> (ptrSize, ptrSize), pointer/unsafe.Pointer -> (ptrSize, ptrSize)
  []E -> (3*ptrSize, ptrSize); [N]E -> (N*size(E), align(E)); map[...]/chan ... -> (ptrSize, ptrSize)
  alias -> size(Target)                      # recursive
  struct S:  len = 0; A = 1
             for f in S.Fields: len = align_up(len, align(f)); len += size(f); A = max(A, align(f))
             return (align_up(len, A), A)
  funcdef -> (ptrSize, ptrSize); iface -> (2*ptrSize, ptrSize)
```

`getTypeLength` `GoTypeManager.java:1034-1051`; string/pointer/slice/array branch `:1059-1096`;
struct branch `:1115-1127`; `align` is `dtm.getDataOrganization().getSizeAlignment` (`:1055-1057`).
`convertStructDef` then builds `StructureDataType(len)`, sets alignment, re-adds the fields with default
packing, **requires the packed length to equal the computed length** (else
`Go type struct definition changed size when packing`), and `replaceWith`s it
(`GoTypeManager.java:559-597`). `StructureMappingInfo` stores that Structure and reports
`getStructureLength()` = `structureDataType.getLength()` (`:114-119`).

Results of my independent re-implementation of that algorithm over the installed JSON (stdout exit 0,
§8 command 5):

| JSON (all) | `internal/abi.Type` | `OldMapType` | `SwissMapType` | `UncommonType` | `Method` |
|---|---|---|---|---|---|
| go1.24.0 / go1.25.0, ptr 8 | 48 | **88** | 112 | 16 | 16 |
| same fields, ptr 4 | 32 | **56** | 64 | 16 | 16 |

`internal/abi.Type` field offsets (both versions): `Size_`0, `PtrBytes`8, `Hash`16, `TFlag`20, `Align_`21,
`FieldAlign_`22, `Kind_`23, `Equal`24, `GCData`32, `Str`40, `PtrToThis`44, size 48.
`OldMapType`: `Type`0, `Key`48, `Elem`56, `Bucket`64, `Hasher`72, `KeySize`80, `ValueSize`81,
`BucketSize`82, `Flags`84, size 88.
`SwissMapType`: `Type`0, `Key`48, `Elem`56, `Group`64, `Hasher`72, `GroupSize`80, `SlotSize`88,
`ElemOff`96, `Flags`104, size 112.

JSON provenance (observation, `Position` fields):
`runtime.maptype` → `internal/abi.OldMapType` at `$GOROOT/runtime/map_noswiss.go:67:6` (1.24.0) /
`:68:6` (1.25.0); `internal/abi.OldMapType` at `$GOROOT/internal/abi/map_noswiss.go:25:6`;
`internal/abi.SwissMapType` at `$GOROOT/internal/abi/map_swiss.go:32:6`; `internal/abi.UncommonType`
at `$GOROOT/internal/abi/type.go:235:6` (1.24.0) / `:231:6` (1.25.0).
Go ground truth (observation, installed toolchains): `runtime/map_swiss.go:22` `type maptype =
abi.SwissMapType`; `runtime/map_noswiss.go:68` `type maptype = abi.OldMapType`; struct bodies at
`internal/abi/map_swiss.go:32-43` and `internal/abi/map_noswiss.go:25-34` (identical field lists in
go1.24.6 and go1.25.0).

For go1.22.0/go1.23.0 the JSON instead has `runtime.maptype` → `internal/abi.MapType` (a struct, 88
bytes); that is the last-known-good invariant: the same 88-byte layout the binaries actually use. The
divergence starts with the 1.24 snapshot, which records only the `map_noswiss.go` alias and drops
`internal/abi.MapType` entirely. No `@StructureMapping` in the package names `internal/abi.SwissMapType`
(observed: the only hit for any of these names is `GoMapType.java:33`).

---

## 4. What the −24 shift does and does not change

- **Silent, not loud.** `GoMapType.isValid()` only checks `typ.getSize() == ptrSize`
  (`GoMapType.java:156-159`); `recoverDataType` only compares the map's size to a pointer and warns
  `Size mismatch between map type and recovered type` (`GoMapType.java:102-116`). Nothing validates the
  uncommon offset, so no exception is raised at registration time.
- **No missing-field error.** All eight Java fields resolve against `OldMapType` components
  (case-insensitive lookup, `StructureMappingInfo.java:406-415`; `keysize`→`KeySize`,
  `elemsize`→`ValueSize` fallback at `GoMapType.java:56`, `bucketsize`→`BucketSize`). If Ghidra had
  instead bound `SwissMapType`, `keysize`/`elemsize`/`bucketsize` would have had no component and
  registration would have thrown `Missing structure field` (`StructureMappingInfo.java:306-323`) — i.e.
  the shipped binding fails soft, which is why it survived.
- **Scalar fields are mostly inert.** `bucket`@64 reads `Group` (a valid `*Type`, so `discoverGoTypes`
  discovers an extra type); `keysize`/`elemsize`/`bucketsize` read bytes of `GroupSize`; `flags`@84 reads
  the high dword of `GroupSize` (normally 0). In 12.1.4 these values only feed `toString`/prototype
  strings, so the observable defect is the uncommon placement.
- **Only method-carrying map types are affected.** If tflag bit 0 is clear, `getUncommonType()` is never
  taken and `getEndOfTypeInfo()` returns `T+L_json` (`GoType.java:137-149`), so a plain map descriptor is
  read correctly. A named map type with methods is the trigger.

**Inference on remediation (not proposed as work here):** binding the snapshot's `internal/abi.SwissMapType`
for Swiss builds would move `L_json` to 112 and require new Java fields (`group`, `groupSize`, `slotSize`,
`elemOff`); the current field-name set cannot bind that struct. This is an inference from the code paths
above, not an upstream claim.

---

## 5. EOF semantics on real numbers

`GoVarlenString.readFrom` (`GoVarlenString.java:65-74`):

```java
long startPos = reader.getPointerIndex();
int strLen = useLEB128() ? reader.readNextUnsignedVarIntExact(LEB128::unsigned)
                         : reader.readNextUnsignedShort(BigEndianDataConverter.INSTANCE);
this.strlenLen = (int)(reader.getPointerIndex() - startPos);
this.bytes = reader.readNextByteArray(strLen);      // <-- provider read, may throw
```

So for a name at VA `P`:

```
A = P + 1 + lebLen        (the position after flags byte and LEB128 length)
B = LEB128(P+1 .. P+lebLen)
throw iff B != 0 and unsigned(B-1) > maxOffset - A
```

The narrowing to `int` matters: a LEB128 value > `Integer.MAX_VALUE` becomes negative and
`readByteArray` throws `Invalid number of elements specified: ...` instead
(`BinaryReader.java:1169-1176`); a value that fits `int` but exceeds the remaining bytes reaches the
provider and produces the `Unable to read past EOF` message.

---

## 6. Calibration against the retained aether log

**Observation 1 — exact throw.** `runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log:177`
`Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`, with the provider frame
`MemoryByteProvider.ensureBounds(MemoryByteProvider.java:312)` and reader frames
`readBytes:265`, `readByteArray:1173`, `readNextByteArray:704`, `GoVarlenString.readFrom:71`,
`GoName.readStructure:95`, `StructureMappingInfo.readStructure:156`, `StructureContext.readNewInstance:98`,
`DataTypeMapper.readStructure:434/413/449`, `GoRttiMapper.getGoName:1074`, `resolveNameOff:1063`,
`GoName.getPkgPath:124`. Every one of those line numbers matches my extraction of the 12.1.4 zip
(§8 commands 2-4), which is the anchor calibration for this report.

**Observation 2 — A/B meaning proven from bytes, without executing the carrier.** aether is `ET_EXEC`
with first `LOAD` vaddr `0x400000` (`readelf -lW`, §8 command 7), so the program-reader index equals the
VA. `A = 17645861 = 0x10D4125` → file offset `0xCD4125`; I read the 8 bytes around it:

```
file 0xCD411D..0xCD412D = e3 20 10 f6 a6 9a b0 35 | 1e 34 f6 41 46 2a 78 b0
                                 ^  ^^^^^^^^^^^  ^
                               A-5   A-4..A-1    A
```

`f6` at `A-5` is the `GoName.flags` byte; `a6 9a b0 35` at `A-4..A-1` is LEB128 for **111 938 854** —
exactly B; the reader then asked for that many bytes starting at `A`. So the failing nested `GoName`
starts at `0x10D4120`, advertises `HAS_TAG|HAS_PKGPATH` (0x02|0x04) and a 106 MB name, and the request
overruns `maxOffset` (address-space max ≈ `0x1800DA0`, from `LOAD` memsz; remaining ≈ 7.2 MB).

**Observation 3 — the retained stack does not route through a map type.** The outer frames are
`GolangSymbolAnalyzer:146` → `GoTypeManager.markupGoTypes:153` → `GoStructType.additionalMarkup:94`
(field-array elements) → `GoInterfaceType.additionalMarkup:77` (method-array elements) →
`GoIMethod` name `@MarkupReference` (`types/GoIMethod.java:40-49`) → `GoName` markup →
`GoName.pkgPath` `@MarkupReference` → `resolveNameOff` → the failing nested `GoName`. There is **no**
`GoMapType` / `GoUncommonType` frame in the retained trace.

**Inference (labelled):** the map-layout defect in §1-§4 is real and source-confirmed, and it can produce
the same `Unable to read past EOF: A, B` signature when a method-carrying named map type's mislocated
uncommon points `pkgpath` into unrelated data. But the retained aether trace is **not direct evidence**
that aether's failure was caused by that defect: its visible chain is a struct field → interface type →
interface method name → `pkgPath` resolution, i.e. a general name-offset misread of the same *class* as
the r17 PR-#9348 finding, not the map-specific shift. C3's minimal pair is exactly the right instrument:
only the `methods` carriers can exercise step 7-12, and the prediction should assert that the mislocated
`pkgpath`/`mcount`/`moff` are what the emulator predicts, not merely that "an EOF occurs".

Calibration facts for that item (observation): aether reports `go_version: go1.25.14`
(`runs/pro-aether/inspect-go.json`), sha256 `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e`,
and the snapshot actually used is `go1.25.0.json` (log:92-93; no 1.25 patch diffs installed). The log's
init succeeded (`Found 6115 Go types`, log:95) and the failure occurred during markup (log:97) — consistent
with step 14 being the first place name/pkgpath getters are called for nested structures.

---

## 7. Limits of this report

- Source-level reversal + data inspection only. No Ghidra run, no REA, no carrier execution; the aether
  byte read is a plain `read()` of the installed ELF at the offset implied by A.
- I did not locate aether's actual map-type descriptors or moduledata `typesOffset`, so
  `typesOffset + off = 0x10D4120` is decomposed no further, and the first (outer) `GoName` of the chain is
  unidentified. That is deliberate: carrier analysis belongs to the C3 owner after predictions freeze.
- The true Swiss size 112 (64) is derived by applying the same documented Go ABI field walk to the
  installed Go struct bodies; I did not compile a probe. Labelled inference-by-ABI, with the field lists
  quoted from `internal/abi/map_*.go`.
- No claim about Go 1.26/1.27, about recovery quality, or about upstream fixes.

---

## 8. Commands run (all read-only) and exit codes

1. `unzip -q Base-src.zip 'ghidra/app/util/bin/format/golang/*'` into `mktemp -d /tmp/ghsrc.XXXXXX`;
   `unzip -q Base-src.zip ghidra/app/util/bin/BinaryReader.java` into `/tmp/bsrc` — **exit 0** (85 golang
   `.java` members extracted).
2. `cd /tmp/bsrc && grep -rn "Unable to read past EOF" .` (full-zip extraction) — **exit 0**; hits at
   `ByteProviderWrapper.java:129`, `FileByteProvider.java:275`, `MemoryByteProvider.java:312`,
   `RangeMappedByteProvider.java:227`.
3. `grep -n "public GoName resolveNameOff\|public GoName getGoName" GoRttiMapper.java` — **exit 0**
   (`1053`, `1073`); `grep -c "" .../GoMapType.java` — **exit 0** (160 lines).
4. `grep` of the retained log for the EOF string — **exit 0** (1 match at `ghidra.log:177`).
5. Python 3 re-implementation of `GoTypeManager.getDataTypeLength` over
   `go1.22.0/1.23.0/1.24.0/1.25.0.json` for ptrSize 8 and 4 — **exit 0**; output reproduced in §3.
6. Python 3 JSON provenance query (`runtime.maptype`/`OldMapType`/`SwissMapType`/`UncommonType`
   `Kind`/`Target`/`Position`, plus `internal/abi.MapType` presence) — **exit 0**.
7. `readelf -lW /usr/bin/aether` — **exit 0**; 4 LOADs, first at vaddr `0x400000`, last memsz ends
   `0x1800DA0`.
8. Python 3 LEB128 check: `A=17645861`, `B=111938854`, bytes `py[A-0x400000-4:A-0x400000]` =
   `a6 9a b0 35`, decoded = `111938854 == B` — **exit 0**; flags byte at `A-5` = `0xf6`.
9. `sha256sum Base-src.zip` — **exit 0**
   (`f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`); `sha256sum /usr/bin/aether` —
   **exit 0** (`06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e`).
10. `ls patchverdiffs | grep '1\.25' | wc -l` — **exit 0**, output `0` (so the 1.25.14→1.25.0 fallback in
    log:92 is forced); the same grep without `wc` exits 1 for “no match”, which is the no-diff observation.

## 9. Tools installed/updated

None. Everything used was already present (`unzip`, `readelf`, Python 3 stdlib, `grep`). No network.

Report: .ufo/waves/round-18/w1/RevGhidraMapTypeRead.md
