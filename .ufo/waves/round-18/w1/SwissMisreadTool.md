# SwissMisreadTool — round 18 W1 (`swiss-misread.py`)

Seat: `KaidokuR18.SwissMisreadTool` (leaf, author-side advisory). Axes: calibration, operability, depth.
Wrote exactly two files: `.ufo/waves/round-18/tools/swiss-misread.py` and this report. No REA, no Ghidra,
no carrier execution. No installs or upgrades (nothing needed; Python 3 stdlib only).

## 1. What the tool is

`python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier PATH --golang-root DIR [--go-version X] [--selftest] [--debug]`

It reads only the carrier bytes, the installed snapshot JSON, and `Base-src.zip`. It emulates, per hypothesis,

* **h1** — Ghidra 12.1.4 binds `runtime.maptype` to `internal/abi.OldMapType` (88 B amd64), so a true Swiss
  descriptor (112 B) gets its UncommonType read 24 B early; and
* **h0** — Ghidra reads the true layout (Swiss for a Swiss build, old for `GOEXPERIMENT=noswissmap`),

then outputs `layout {ghidra_maptype, ghidra_size, true_kind, true_size}`, `map_types`, `uncommon_map_types`,
`misread_map_types`, `predicted_eof_reads_h1/h0`, `predicted_failure_kind_h1/h0`
(`past_eof|invalid_index|none|unknown`), `predicted_invalid_index_reads_h1/h0`, per-map-type
`{name, addr, slot_size, h1/h0 {outcome, eof, index, ghidra_uncommon}}`, a separate full-markup `walk`
channel with `failed`/`first_failure`/`path`, `diagnostic` (h1 vs h0 on the map path), `basis`, `limits`.
Exit 0 emitted, 1 selftest failure, 2 unparseable. `predicted_failure`/`predicted_eof_reads` remain the
h1 aliases required by `contract.md:113-120`.

Truth of the layout is the build setting (`GOEXPERIMENT=noswissmap` or `X:noswissmap` in the version string,
else Go >= 1.24), cross-checked by a byte witness (`map.group[` vs `map.bucket[`).

## 2. Acceptance (exact)

```
$ python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --selftest
SELFTEST: CLEAN cases=15
selftest_exit=0
```

```
$ python3 -I -B .../swiss-misread.py --carrier /usr/bin/aether --golang-root .../typeinfo/golang
aether_exit=0
/usr/bin/aether past_eof [[17645861, 111938854]] [] True
$ python3 -I -B .../swiss-misread.py --carrier /home/vgpnk/.local/bin/notesmd-cli --golang-root .../typeinfo/golang
notesmd_exit=0
/home/vgpnk/.local/bin/notesmd-cli none [] [] False
```

Exact equality holds for aether: `predicted_eof_reads_h1 == [[17645861, 111938854]]` (not "contains").
notesmd-cli: `uncommon_map_types = 0`, `predicted_failure = false` (vacuous negative, recorded as such).
Carrier digests: aether `06c91f55…006e`, notesmd-cli `412dc532…802d`; `sha256sum -c SHA256SUMS` in
`/home/vgpnk/.local/share/kaidoku-r18/carriers` → 12 × OK, exit 0.

Selftest fixtures are synthetic ELFs under `tempfile.mkdtemp()` (removed): Swiss slot 40 with a two-hop
name chain (H1 past_eof, exact pair; H0 silent), Swiss slot 24 (silent both), old layout (`noswissmap`),
and a garbage file that must exit 2. The named red case is slot 40 under H0: the tool must *not* predict
an EOF when the true uncommon is read; the selftest fails if H0 fails.

## 3. Per-carrier summary (12 carriers + 2 calibration)

`h1` is the map-path prediction; `walk` is the separate full-markup channel.

| carrier | Go | true | h1 kind | h1 eof / invalid | h0 kind | maps/uncommon/misread | diag | walk failed |
|---|---|---|---|---|---|---|---|---|
| aether | 1.25.14 | swiss | **past_eof** | `[[17645861,111938854]]` | none | 152/7/7 | true | true |
| notesmd-cli | 1.25.8 | swiss | none | — | none | 63/0/0 | false | true |
| s1246-swiss-methods | 1.24.6 | swiss | none | — | none | 12/1/1 | false | false |
| s1246-swiss-nomethods | 1.24.6 | swiss | none | — | none | 11/0/0 | false | false |
| s1246-swiss-nethttp | 1.24.6 | swiss | **invalid_index** | `[22386945]` | none | 38/2/2 | true | true |
| s1246-noswiss-methods | 1.24.6 | old | none | — | none | 12/1/0 | false | false |
| s1246-noswiss-nomethods | 1.24.6 | old | none | — | none | 11/0/0 | false | false |
| s1246-noswiss-nethttp | 1.24.6 | old | none | — | none | 38/2/0 | false | false |
| s1250-swiss-methods | 1.25.0 | swiss | none | — | none | 12/1/1 | false | false |
| s1250-swiss-nomethods | 1.25.0 | swiss | none | — | none | 11/0/0 | false | false |
| s1250-swiss-nethttp | 1.25.0 | swiss | none | — | none | 38/2/2 | false | false |
| s1250-noswiss-methods | 1.25.0 | old | none | — | none | 12/1/0 | false | false |
| s1250-noswiss-nomethods | 1.25.0 | old | none | — | none | 11/0/0 | false | false |
| s1250-noswiss-nethttp | 1.25.0 | old | none | — | none | 38/2/0 | false | false |

Every one of these is the peer-predicted outcome (`ConnC3Prediction.md`, `RevNotesmdMaps.md`,
`RevAetherReplay.md`, `SimplifyC3Tools.md`): aether past_eof pair; s1246-swiss-nethttp
`Invalid index: 22386945`; s1250-swiss-nethttp none; methods/nomethods none; noswiss none.

## 4. Aether per-type map-path evidence (h1 vs h0)

`types = 0x954020`, `etypes = 0x13B4999`; 7 uncommon map types (`map_types = 152`, matching
`CriticC3.md:30-43`). H1 reads the UncommonType at `T+0x58` (low 32 of `SlotSize` = `PkgPath`,
high 32 = `Mcount = 0`):

| named map type | SlotSize | H1 pkgpath/mcount | H1 outcome | H0 pkgpath/mcount | H0 outcome |
|---|---|---|---|---|---|
| `*textproto.MIMEHeader` | 40 | 40 / 0 | **past_eof `[17645861, 111938854]`** | 55036 / 5 | silent |
| `*url.Values` | 40 | 40 / 0 | **past_eof same pair** | 16493 / 6 | silent |
| `*http.Header` | 40 | 40 / 0 | **past_eof same pair** | 20987 / 13 | silent |
| `*go.shape.map[string]interface {}` | 32 | 32 / 0 | silent | 18547 / 0 | silent |
| `*go.shape.map[string][2]int32` | 24 | 24 / 0 | silent | 18547 / 0 | silent |
| `*go.shape.map[string]int32` | 24 | 24 / 0 | silent | 18547 / 0 | silent |
| `*dbus.sigSet` | 24 | 24 / 0 | silent | 119968 / 4 | silent |

The chain is exactly the r17 mechanism: nameOff 40 → `types+0x28`; that GoName has flags `0x6e`, zero-length
name, tag `a`, pkgPath `0x780100`. The emitted `per_type[].h1.ghidra_uncommon` for the three failing maps is `{pkg_path: 40, mcount: 0, moff: 16}`; H0 emits `{55036, 5}`, `{16493, 6}`, `{20987, 13}`.
`types+0x780100` = `0x10D4120`, whose LEB128 name length is 111,938,854
starting at `0x10D4125` = 17,645,861. The full-markup walk independently reaches the same pair through
`struct.field → interface.imethod.typ → func.param → interface.imethod.typ → func.param` (path retained in
`walk.h1.path`), which reconciles `RevGhidraMapTypeRead.md`'s "no map frame" observation: the same bad GoName
is reachable from interfaces as well as from the three slot-40 maps.

`s1246-swiss-nethttp` is the held-out **loud** case: SlotSize 40 at `types+0x28` lands on a GoName whose
pkgPath is out of range, so `MemoryByteProvider.ensureBounds` throws `Invalid index: 22386945`
(`MemoryByteProvider.java:302`), not past-EOF. H0 reads the true uncommon and stays silent. That is a
map-path diagnostic (h1 != h0 on the logged field) on a 1.24.6 carrier.
`s1246-swiss-methods` `*main.Counts` is the held-out **silent** case: SlotSize 24 → flags `0x01`, no
pkgPath, so H1 is silent while H1's tuple (`pkgpath 24, mcount 0`) differs from H0's (`576, 2`).
This is the "misread but silent" program-DB effect `CriticC3.md:46-52` describes; it is not a log field,
so `diagnostic` is false for it.

## 5. Reconciliation with peers

- **Agree** with `CriticC3.md`: trigger is a named Swiss map type × SlotSize, not "methods"; 3 eof + 4 silent
  on aether; notesmd 0 uncommon; s1246/s1250 methods `main.Counts` silent; exact aether pair.
- **Agree** with `RevGhidraMapTypeRead.md` §1.1/§3/§5: binding table, 88/112 sizes, `T+0x58` read, LEB128
  then bytes, `Invalid index` vs past-EOF split. The tool's `basis` cites the same members.
- **Agree** with `ScoutGhidraGoStructMapping.md`: no Swiss class, no map version switch, alias→`OldMapType`.
- **Reconcile** `RevGhidraMapTypeRead.md`'s stack observation (struct→interface→imethod, no map frame):
  the retained stack is the *actual* call site; the map path is a second, numerically identical route to the
  same GoName. The tool reports both channels, so neither observation is discarded.
- **Disagree (declared)** with `CriticC3.md:43,103` on two internal counts: my discovery index is 5924 vs the
  peer's 5927, and my gap scan adds 0 unindexed vs the peer/log's 188. I added a `Str` in
  `[0, etypes-types)` filter (not in Ghidra's `isValid`) to reject three misaligned bogus refs; that filter
  is the likely source of the 3-type delta. The gap scan's `getEndOfTypeInfo` ranges in my emulator cover the
  closure gaps, so it finds nothing. Neither delta changes the map-path predictions (all peer numbers match);
  I report them as calibration gaps, not as agreement.

## 6. Anchors (Base-src.zip members; read in this session)

- `rtti/types/GoMapType.java:32-34,39-62` — binding names, eight unconditional fields.
- `rtti/types/GoType.java:137-149` — `getUncommonType()` at `context.getStructureEnd()`.
- `rtti/types/GoUncommonType.java:41-104` — PkgPath/Mcount/Xcount/Moff, method slice, end.
- `rtti/GoName.java:79-100,123-126` — eager name/tag/pkgPath reads; recursive pkgPath.
- `rtti/GoVarlenString.java:65-74` — LEB128 length then `readNextByteArray`.
- `rtti/GoRttiMapper.java:1053-1075` — `resolveNameOff = types + off`, no range check.
- `rtti/GoTypeManager.java:96-209,263-269` — discovery, gap scan, `allTypes()` VA-sorted.
- `structmapping/MemoryByteProvider.java:289-313` — past-EOF (312) vs invalid-index (302) messages.
- `structmapping/StructureContext.java:171-204` — field location and structure end.
- `structmapping/StructureMappingInfo.java:170-175` — `isValid()` throws "Invalid data".
- `structmapping/MarkupSession.java:105,324-356` — recursive markup / array elements.
- `rtti/types/GoStructType.java:90-95,176-184`; `GoInterfaceType.java:70-78,173-184`;
  `GoFuncType.java:89-119`; `GoStructField.java:35-47`; `GoIMethod.java:36-48`.
- `rtti/GoApiSnapshot.java:102-168` — base `go<M.m.0>.json` + nearest earlier patch diff.
- JSON `go1.24.0.json` / `go1.25.0.json`: `runtime.maptype → internal/abi.OldMapType`; `SwissMapType` 112 B
  (`GroupSize` 80, `SlotSize` 88, `ElemOff` 96, `Flags` 104), `OldMapType` 88 B, `UncommonType` 16 B.

## 7. Limits, risks, blockers

- The full-markup `walk` produces false positives on notesmd-cli and on aether-h0 (`unmapped at 0x8` /
  `0x2eeb`-style low addresses) from refs this emulator follows but Ghidra's discovery/alignment filters
  evidently do not. It is reported separately and never folded into `predicted_failure`; do not read
  `walk.failed` as a prediction.
- Index 5924 vs 5927 and gap scan 0 vs 188 (above). The gap scan also clamps a non-advancing
  `getEndOfTypeInfo` to `addr + ptr` to avoid an infinite loop; that path was not exercised on these
  carriers.
- `snapshot_diff` is selected by the r16 law but not applied; no 1.24/1.25 `patchverdiffs` file edits
  `internal/abi.{OldMapType,SwissMapType,UncommonType,Type,Method}`, so the layouts used are the base bytes.
- Method `mtyp`/`ifn`/`tfn` targets are resolved as types only (no deep recursive markup) and struct
  field/param loops cap at 4096 entries; a misread huge slice could hide a later failure.
- Only 64-bit little-endian ELF carriers were exercised; the sizer has a 32-bit path but it is untested.
- No claim about Go 1.26/1.27, no upstream fix, no REA/Ghidra run. Predictions are not frozen here; the L1
  freezes them in Git.

## 8. Commands and exits (all run in this session)

| command | exit |
|---|---|
| `python3 -I -B …/swiss-misread.py --selftest` → `SELFTEST: CLEAN cases=15` | 0 |
| `… --carrier /usr/bin/aether --golang-root …` → past_eof `[[17645861,111938854]]` | 0 |
| `… --carrier ~/.local/bin/notesmd-cli --golang-root …` → none, `predicted_failure false` | 0 |
| loop over 12 carriers + aether + notesmd (`timeout 120` each) | 0 ×14 |
| `sha256sum -c SHA256SUMS` (12 carriers) | 0 (12 OK) |
| `sha256sum /usr/bin/aether ~/.local/bin/notesmd-cli` | 0 |
| `unzip -p Base-src.zip <members>` / `grep` reads cited above | 0 |
| scratch phase profiler (aether discovery/gap/markup) | 0 (2.96 s wall) |

Report: .ufo/waves/round-18/w1/SwissMisreadTool.md
