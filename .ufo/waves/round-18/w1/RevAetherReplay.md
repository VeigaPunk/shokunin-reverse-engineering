# RevAetherReplay — independent recomputation of the aether `Unable to read past EOF` chain

Scope: read-only, from `/usr/bin/aether` bytes and the installed Ghidra 12.1.4 sources/snapshot.
No carrier execution, no REA `analyze`/`search`/`decompile`, no Ghidra/analyzeHeadless, no
installs. Carrier pin: sha256 `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e`,
20,694,888 B, ET_EXEC, `go1.25.14` (`.go.buildinfo`). R17 report under test:
`.ufo/waves/round-17/w2/RevAetherEOF.md` (F1/F2). Current-lane log:
`.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log` (sha256
`5e6d8563050dea00507d0b8a75817bc6945cd56b33176ddc71aa48cd51dc2939`); committed r17 log at
`da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log`
(blob sha256 `f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed`, 244 lines) has
the identical line 177. Labels: **OBS** = observed from bytes/tool output; **INFER** = inference.

## Verdict

R17's arithmetic (`index, length`) is correct, but its attribution stops one level short.

- The failing getter is `GoName.getPkgPath` on a **misparsed GoName N0 at 0x954048**, not on a
  genuine name record. N0's `pkgPath` field is `0x00780100`.
- N0 is reached as the `PkgPath` of a **misread `GoUncommonType`** belonging to a **Swiss-map**
  type descriptor. Ghidra reads that uncommon type at `maptype + 88`, because its
  `runtime.maptype` resolves to `internal/abi.OldMapType` (88 B), while the carrier's true type is
  `internal/abi.SwissMapType` (112 B). At `maptype + 88` the true layout has
  `SwissMapType.SlotSize`, not `UncommonType.PkgPath`.
- The map involved is **`http.Header` at vaddr 0xa350a0**, whose true `SlotSize` is `0x28`. That
  makes the misread `PkgPath` `0x28`, resolving to `types + 0x28 = 0x954048`, whose bytes parse as
  N0 with `pkgPath = 0x780100`, resolving to `0x10D4120`, whose flags/LEB then throw
  `17645861, 111938854` (0x10D4125, 111,938,854).
- Field Ghidra misreads: **`internal/abi.UncommonType.PkgPath` (nameOff), read at
  `maptype+88`**, where the true field is `internal/abi.SwissMapType.SlotSize`. Secondary (not
  causal): `OldMapType.KeySize/ValueSize/BucketSize/Flags` at 80–87 are read over `GroupSize`.
- Three map descriptors have `SlotSize=0x28` and reproduce the exact pair if marked:
  0xa1c7a0 `textproto.MIMEHeader`, 0xa229a0 `url.Values`, 0xa350a0 `http.Header`. The logged
  stack shape (exactly two interface-markup frames) matches **only 0xa350a0**.

R17 F2's dismissed candidate (the structurally odd parse at 0x954048) is in fact the real N0.
R17 F2's “the invoking GoName cannot be identified” is therefore corrected, not merely bounded.

## Recomputed chain (each step OBS unless marked)

### 1. Image geometry and module

```
$ readelf -SW /usr/bin/aether | grep -E '\.rodata|\.typelink|\.itablink'
[18] .rodata   PROGBITS 0000000000954000 554000 a60c40
[19] .typelink PROGBITS 00000000013b4c40 fb4c40 003a6c
[20] .itablink PROGBITS 00000000013b86c0 fb86c0 000eb0          exit=0
$ readelf -lW /usr/bin/aether | grep '^  LOAD'
LOAD 0x554000 0x0000000000954000 0x0000000000954000 0xdabea8 0xdabea8 R
LOAD 0x1300d50 0x0000000001700d50 0x0000000001700d50 0x0bae91 0x0ff050 RW   exit=0
```

`runtime.moduledata` at vaddr `0x172E400` (file `0x132E400`, `.noptrdata`) supplies the type
domain (`+0x128 types`, `+0x130 etypes`, `+0x160 typelinks`, `+0x178 itablinks`):

```
types=0x954020 etypes=0x13B4999 typelinks=0x13B4C40 len=0xE9B itablinks=0x13B86C0 len=0x1D6
```

`0xE9B` = 3739 typelinks; `etypes-types = 0xA60979 = 10,882,425`. All vaddr→file mapping is
`vaddr − 0x400000` for these LOADs (`.rodata` file `0x554000` = vaddr `0x954000`).

### 2. What Ghidra thinks `runtime.maptype` is

Snapshot selected: `go1.25.0.json` — the run logged
`Falling back from 1.25.14 to 1.25.0 for Go API snapshot` (log:92), i.e. no 1.25.x patch diff
(`patchverdiffs/` has no `go1.25*`), and the base JSON is used unpatched.

- `go1.25.0.json:all.Types["runtime.maptype"] = {Kind:"alias", Target:"internal/abi.OldMapType",
  Position:"$GOROOT/runtime/map_noswiss.go:68:6"}` (single-line JSON; key path cited).
- `internal/abi.SwissMapType` is present in the same snapshot but is **not** the alias target.
- `go1.24.0.json` has the same wrong alias; `go1.23.0.json` maps to `internal/abi.MapType`.

Why the alias does not save it: `GoTypeManager.convertAliasDef` materializes it as a
`TypedefDataType` (`GoTypeManager.java:549-556`), and `DataTypeMapper.getType(name,
Structure.class)` returns it only if it **is** a `Structure`
(`DataTypeMapper.java:282-295`). `GoMapType`'s candidate list is
`{"runtime.maptype","internal/abi.MapType","internal/abi.OldMapType"}`
(`GoMapType.java:32-34`); `runtime.maptype` fails the `Structure` test, `internal/abi.MapType` is
absent in the 1.24/1.25 snapshots, so **`internal/abi.OldMapType` is selected**, and its length is
used by `StructureMappingInfo.getStructureLength()` (`StructureMappingInfo.java:114-119`).

Layout arithmetic (Go source, `internal/abi/type.go`): `Type` = 48 B; `OldMapType`
(`map_noswiss.go:25`) adds Key/Elem/Bucket/Hasher (4×8) + KeySize u8 + ValueSize u8 + BucketSize
u16 + Flags u32 → **88 B**. `SwissMapType` (`map_swiss.go:32`) adds Key/Elem/Group/Hasher +
GroupSize + SlotSize + ElemOff + Flags → **112 B**. The carrier is a Swiss build:
`.go.buildinfo` settings contain no `GOEXPERIMENT` line (only `-buildmode`, `-compiler`,
`-ldflags`, `-tags`, `CGO_*`, `GOARCH/GOOS/GOAMD64`), and Go 1.25's baseline has
`SwissMap: true` (`internal/buildcfg/exp.go:85`). Independently, the bytes at each uncommon map
have the Swiss layout exactly (SlotSize at +88, ElemOff at +96, real uncommon at +112 with a valid
package path/mcount), so this is observed, not assumed.

### 3. The map descriptors

Enumerating all 3739 typelinks gives 145 kind-21 (Map) descriptors, none with TFlagUncommon. A
full-blob scan of structurally valid `abi.Type` records finds **152** map records: the 145 plus 7
**unindexed** named maps with `TFlag=0x07` (Uncommon|ExtraStar|Named). Each is discovered through
the matching `*T` pointer type in `.typelink` (`GoPointerType.discoverGoTypes`,
`GoPointerType.java:61-69`; e.g. `*http.Header` at 0xa2e4e0, kind 22, elem 0xa350a0).

| map descriptor | name (ExtraStar stripped) | TFlag | true GroupSize | true SlotSize | true ElemOff | true uncommon @+112 | mcount |
|---|---|---|---|---|---|---|---|
| 0x9E1880 | `go.shape.map[string]interface{}` | 0x07 | 264 | 32 | 16 | pkg `go.shape` | 0 |
| 0x9E7F80 | `go.shape.map[string][2]int32` | 0x07 | 200 | 24 | 16 | pkg `go.shape` | 0 |
| 0x9E8000 | `go.shape.map[string]int32` | 0x07 | 200 | 24 | 16 | pkg `go.shape` | 0 |
| 0xA15B80 | `dbus.sigSet` | 0x07 | 200 | 24 | 16 | pkg `github.com/godbus/dbus/v5` | 4 |
| **0xA1C7A0** | **`textproto.MIMEHeader`** | 0x07 | 328 | **40 (0x28)** | 16 | pkg `net/textproto` | 5 |
| **0xA229A0** | **`url.Values`** | 0x07 | 328 | **40 (0x28)** | 16 | pkg `net/url` | 6 |
| **0xA350A0** | **`http.Header`** | 0x07 | 328 | **40 (0x28)** | 16 | pkg `net/http` | 13 (xcount 8) |

### 4. Ghidra's misread of the uncommon type

`GoMapType` extends `GoType`; `hasUncommonType()` reads `TFlagUncommon` from the correct Type
prefix (`GoBaseType.java:100-102`). `GoType.getUncommonType()` then reads `GoUncommonType` at
`context.getStructureEnd()` (`GoType.java:143-150`), and `StructureContext.getStructureEnd()` is
`structureStart + structureDataType.getLength()` (`StructureContext.java:190-204`) — 88 for the
selected `OldMapType`. So for `http.Header`:

```
maptype         = 0xA350A0
OldMapType end  = 0xA350A0 + 88 = 0xA350F8
PkgPath read    = u32 @ 0xA350F8 = 0x00000028        (<- true SwissMapType.SlotSize)
Mcount @+4      = 0x0000   Xcount @+6 = 0x0000   Moff @+8 = 0x10
```

`GoUncommonType.getPkgPath()` calls `resolveNameOff(context.getStructureStart(), pkgpath_nameOff)`
(`GoUncommonType.java:38-41,56-59`), and `resolveNameOff` computes
`nameStart = module.getTypesOffset() + off` (`GoRttiMapper.java:1053-1064`):

```
types + 0x28 = 0x954020 + 0x28 = 0x954048
```

### 5. N0 at 0x954048 — the misparsed GoName

`GoName.readStructure` (`GoName.java:92-102`) parses bytes at 0x954048 as
`flags=0x6E`, name-length `0x00`, tag-length `0x01`, tag `'a'`, then a 4-byte `pkgPath`:

```
0x954048: 6e 00 01 61 00 01 78 00 01 79 ...
          ^flags=0x6E (EXPORTED|HAS_TAG|HAS_PKGPATH|EMBEDDED, plus bits 5-6 = 0x60)
             ^name="", ^tag len 1/tag 'a', ^pkgPath = 00 01 78 00 = 0x00780100
```

This is not a genuine record: the real 3-byte name records in that table are `d u n a x y ...`
(e.g. `n` at 0x954046, `a` at 0x954049, `x` at 0x95404C); 0x954048 is the `n` character byte, and
the value read as `pkgPath` is the genuine `x` record's `00 01 78` plus the next record's `00`.
R17 F2 found this candidate and rejected it as “not genuine” — correct that it is not genuine, but
it is exactly the record the map misread resolves to.

### 6. The EOF

`GoName.getPkgPath` (`GoName.java:122-125`) calls `resolveNameOff(0x954048, 0x780100)`:
`0x954020 + 0x780100 = 0x10D4120` (in range: `0x780100 < 0xA60979`). Reading a GoName there:

```
0x10D4120: f6 | a6 9a b0 35 | 1e 34 f6 41 ...
flags=0xF6 (bits 4-7 set, impossible for a genuine name)
name-length LEB at 0x10D4121 = a6 9a b0 35 = 111,938,854 (0x6AC0D26)
name bytes start at 0x10D4125
```

`GoVarlenString.readFrom` (`GoVarlenString.java:65-71`) does the LEB then
`readNextByteArray(111938854)`. `MemoryByteProvider.ensureBounds` (`MemoryByteProvider.java:289-313`)
is built over the default address space with base = space min = 0, max inclusive = last mapped byte
(`0x1700D50 + 0xFF050 - 1 = 0x17FFD9F`), so **index == program address**:

```
index       = 0x10D4125 = 17,645,861
maxOffset   = 0x17FFD9F
remaining   = 0x17FFD9F - 0x10D4125 = 7,519,354
available   = remaining + 1 = 7,519,355
length - 1  = 111,938,853 > remaining  -> throw
"Unable to read past EOF: %s, %d" (index, length)
```

That is exactly `Unable to read past EOF: 17645861, 111938854` (log:177). R17's “remaining bytes =
7,519,355” is the true available-byte count; the provider's `remaining` variable is one less by
design (`MemoryByteProvider.java:305-310`). No correction of substance.

## Which descriptor fired (depth)

The logged stack has exactly **two** `GoInterfaceType.additionalMarkup` frames (log:124,138) and
**one** `GoStructType.additionalMarkup` (log:147), with `markupGoTypes` at log:154. Mapping
`MarkupSession` line numbers (`MarkupSession.java:324,327,339,349`; `FieldMappingInfo.java:285-304`)
gives the shape:

`container type's @Markup getter -> struct X -> field type interface I1 -> method func F1 ->
param interface I2 -> method func F2 -> param map M -> GoType.getUncommonType -> GoUncommonType
-> GoName N0 -> EOF`

(`@MarkupReference` only invokes the getter and adds a reference; it does **not** mark the returned
object — `FieldMappingInfo.java:285-304`. That is why no `GoMapType`/`GoUncommonType` frame is
visible: those getters return before the nested markup that throws, and `GoUncommonType` has only a
class-level `@Markup` `getPkgPath`, matching the `createMarkupFuncFromGetter` frame at log:105.)

Graph search over the type closure from typelinks (5927 types, which is exactly
`6115 − 188` unindexed types from log:94-95) for that pattern yields **only** the `http.Header`
chain:

```
*options.App 0x9857C0 (typelink seed, kind 22)
  -> options.App 0xA515C0, field #15 "AssetsHandler" = 0x9CBA40 http.Handler
     -> ServeHTTP 0x9A98C0 func(http.ResponseWriter, *http.Request)
        -> param 0: http.ResponseWriter 0x9DAF00
           -> method "Header" typeOff 0x49400 -> 0x99D420 func() http.Header
              -> out 0: http.Header 0xA350A0
                 -> GoUncommonType at 0xA350F8 (misread)
```

Verified named signatures: `http.Handler` has one method `ServeHTTP` -> 0x9A98C0; 0x9A98C0 has
in-params `[http.ResponseWriter 0x9DAF00, *http.Request 0xA47500]`; `http.ResponseWriter` has
`Header`->0x99D420, `Write`->0x9B5F60, `WriteHeader`->0x99B360; 0x99D420 is
`func() http.Header` with out-param 0xA350A0.

First-reach check: no type with address below 0x9857C0 has a markup edge to `http.Header`, to the
five candidate structs, or to `options.App` (inbound scan of all 5927 types). Each candidate
struct's only inbound edge is its pointer type: `*options.App` 0x9857C0, `*assetserver.Options`
0x9BD6A0, `*assetHandler` 0x9F0F80, `*requestFinalizer` 0xA12A20, `*AssetServer` 0xA2F140 — the
lowest is `*options.App`. `*options.App` is a typelink seed and is not referenced by any earlier
type, so it is marked at its own turn, and `options.App`'s field #15 is the first chain into the
map. **OBS** for addresses/edges; **INFER** that the enclosing struct in the elided 73 frames is
`options.App` (the log cannot name it), and **INFER (high)** that 0xA350A0 rather than the other
two 0x28-slot maps fired, because only it matches the two-interface stack shape.

## Corrections to `RevAetherEOF.md`

1. **F1 mechanism/arithmetic: confirmed.** (index, length) ordering, LEB `a6 9a b0 35`, vaddr
   `0x10D4125`, file `0xCD4125`, and `resolveNameOff = types + off` all recompute exactly.
2. **F1 attribution: incomplete.** The failing `GoName.getPkgPath` is not on a genuine name; it is
   the misread uncommon `PkgPath` of a Swiss map. R17 never identified the map and did not consider
   unindexed map types.
3. **F2: corrected.** The invoking GoName is identified: N0 = 0x954048, reached via
   `GoUncommonType` of `http.Header` at 0xA350F8 (read) / true uncommon 0xA35110.
4. **F1's “no structurally valid record has HAS_PKGPATH with value 0x780100”** remains true for
   *genuine* records; the record used is the mid-record parse at 0x954048, which r17 correctly
   called non-genuine but wrongly treated as non-causal.
5. **Provider max:** inclusive max is 0x17FFD9F, not 0x17FFDA0; r17's 7,519,355 is the available
   byte count (remaining+1), so its conclusion stands.
6. **F4 (`compare.json` hides the abort): unaffected/confirmed** by log:97 + log:238.

## Command transcript (all exit 0 unless stated)

```
$ sha256sum /usr/bin/aether
06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e  /usr/bin/aether   exit=0
$ stat -c '%s' /usr/bin/aether
20694888                                                                                  exit=0
$ git cat-file -p da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log | sha256sum
f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed  -                     exit=0
$ readelf -SW /usr/bin/aether | grep -E '\.rodata|\.typelink|\.itablink'
  [18] .rodata   ... 0000000000954000 554000 a60c40
  [19] .typelink ... 00000000013b4c40 fb4c40 003a6c
  [20] .itablink ... 00000000013b86c0 fb86c0 000eb0                                      exit=0
$ python3 -B -c "
d=open('/usr/bin/aether','rb').read(); B=0x400000
idx=0x10d4125; print('index',idx,'hex',hex(idx),'fileoff',hex(idx-B))
print('len bytes at 0x10d4121:',d[0x10d4121-B:0x10d4125-B].hex(' '))
v=0;s=0
for b in d[0x10d4121-B:0x10d4125-B]: v|=(b&0x7f)<<s; s+=7
print('leb',v,hex(v))
mx=0x17ffd9f; print('maxOffset',hex(mx),'remaining',mx-idx,'available',mx-idx+1,'length-1',v-1,'gt_remaining',(v-1)>(mx-idx))
"
index 17645861 hex 0x10d4125 fileoff 0xcd4125
len bytes at 0x10d4121: a6 9a b0 35
leb 111938854 0x6ac0d26
maxOffset 0x17ffd9f remaining 7519354 available 7519355 length-1 111938853 gt_remaining True
                                                                                          exit=0
$ grep -nE 'Unable to read past EOF|GoName\.getPkgPath|GoInterfaceType\.additionalMarkup|GoStructType\.additionalMarkup|GoTypeManager\.markupGoTypes|GoVarlenString\.readFrom|getGoName|resolveNameOff|addRefToFieldWithGetter|Found 6115|Discovered 188|Falling back from' ghidra.log
92: Falling back from 1.25.14 to 1.25.0
94: Discovered 188 unindexed Go types
95: Found 6115 Go types
100: FieldMappingInfo.addRefToFieldWithGetter(FieldMappingInfo.java:296)
124,138: GoInterfaceType.additionalMarkup(GoInterfaceType.java:77)
147: GoStructType.additionalMarkup(GoStructType.java:94)
154: GoTypeManager.markupGoTypes(GoTypeManager.java:153)
177: Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854
182: GoVarlenString.readFrom(GoVarlenString.java:71)
194: GoRttiMapper.getGoName(GoRttiMapper.java:1074)
195: GoRttiMapper.resolveNameOff(GoRttiMapper.java:1063)
196: GoName.getPkgPath(GoName.java:124)                                                     exit=0
$ python3 -B <map descriptor scan>
0xa1c7a0 *textproto.MIMEHeader tflag 0x7 slot 40 misread_pkgpath 0x28 true_pkg_off 0xd6fc mcount 5
0xa229a0 *url.Values          tflag 0x7 slot 40 misread_pkgpath 0x28 true_pkg_off 0x406d mcount 6
0xa350a0 *http.Header         tflag 0x7 slot 40 misread_pkgpath 0x28 true_pkg_off 0x51fb mcount 13
                                                                                          exit=0
$ python3 -B <N0 parse>
N0 bytes 6e 00 01 61 00 01 78 00 01 79
flags 0x6e name_len_byte 0x0 tag_len 0x1 tag a pkgPath 0x780100
target bytes f6 a6 9a b0 35 1e 34 f6 flags 0xf6                                           exit=0
$ ls .../typeinfo/golang/patchverdiffs | grep -E '^go1\.25'
(no output)                                                                               exit=1
```

No installs were performed.

## Confidence and limits

- Byte/address/field claims: **high** (all recomputed from `/usr/bin/aether`; committed and re-run
  logs agree line-for-line).
- “http.Header is the descriptor that fired”: **high**, from the two-interface stack shape plus
  the byte-exact EOF pair; `url.Values` and `textproto.MIMEHeader` are structurally capable but do
  not match the logged shape.
- “The enclosing struct is `options.App`”: **inference (medium-high)**; the log elides the 73
  frames that would name it.
- Ghidra snapshot selection is `go1.25.0.json` unpatched (log:92 + no `patchverdiffs/go1.25*`);
  a hypothetical patch diff for 1.25.14 would invalidate only that specific step, not the
  carrier-byte chain.
- No Ghidra/REA execution; the emulation is static, so it cannot observe analyzer ordering beyond
  the logged stack.
