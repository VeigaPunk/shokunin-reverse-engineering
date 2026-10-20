# RevNotesmdMaps — Go runtime map-type descriptors (R18 W1)

Seat: `KaidokuR18.RevNotesmdMaps` (leaf, author-side advisory). Lane read-only: this report is
the only lane file written. No REA, no Ghidra/analyzeHeadless, no carrier execution, no installs.
Scratch parser (outside the lane, not a deliverable): `/tmp/r18-revmaps/typemaps.py`,
sha256 `a392e86f00974894cccb900521d9767ba5503778c54fcfcf35ce1e552e81b987`. Labels:
**[OBS]** = parsed/measured this session; **[INF]** = inference, not measured.

## Verdict: the r17 claim is CONFIRMED exactly

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:155-156,163` says notesmd-cli has
"no map types with method info" and "63 map types"; `.ufo/waves/round-17/w2/CriticAetherUnknown.md:117`
records the same script result as `map types 63 with uncommon 0`.

**[OBS]** `/home/vgpnk/.local/bin/notesmd-cli` (sha256
`412dc532d278b9e4aaf502891ea1f7b5c60e7572fb82935778ebdb728000802d`, go1.25.8, matches
`.ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json:7-8`) carries exactly **63 `kind==Map`
descriptors, 0 with `tflagUncommon`, 0 named**. All 63 are **Swiss layout (0x70)** and all 63 are
unnamed (`tflag == 2`; the name string is the `*map[...]` spelling, which `TFlagExtraStar` strips).
Two independent enumerations agree: the `moduledata.typelinks` view and a validated scan of
`[types, etypes)` both give 63/0, with empty symmetric difference. Because there are zero named map
types, "no map types with method info" cannot be an artifact of the enumeration; it is a property
of that binary. The r17 sentence is confirmed, not merely replicated.

## Method (two views of the same table)

1. Locate `.gopclntab`; find `moduledata` by scanning allocated file-backed sections for a pointer
   to the pclntab header; accept a candidate only if `pcHeader == pclntab`, `pclntable.ptr ==
   pclntab + pclnOffset`, `ftab.len == nfunc + 1`, `typelinks.ptr/len == .typelink` address/entries,
   `text == textStart`, and `types < etypes`. Field order is the 1.20–1.25 layout
   (`runtime/symtab.go:394-442`; `textsectmap` then `typelinks []int32 // offsets from types` at
   `:418-419`). The validation passed on all 14 binaries. [OBS]
2. **View A — typelinks:** each `int32` entry is an offset from `types`; this is the table
   `reflect.typelinks()` sees (`cmd/link/internal/ld/typelink.go:20-23`). [OBS]
3. **View B — validated span scan:** every 8-byte-aligned `_type` in `[types, etypes)` with
   `kind&0x1f == Map` (21), `Size_ == 8`, `PtrBytes == 8`, `Align_/FieldAlign_ == 8`, `Hash != 0`,
   `Str`/`Key`/`Elem`/`Group` inside the span and 8-aligned, `Key`/`Elem` resolving to real type
   records, `TFlag` within 0x1f, and `PtrToThis` (when non-zero) pointing to a Pointer record whose
   `Elem` points back. `_type` offsets follow `internal/abi.Type`
   (`internal/abi/type.go:20-45`): `TFlag` at +20, `Kind_` at +23. [OBS]
4. **Layout from bytes:** Swiss iff `GroupSize == 8*SlotSize + 8`, `ElemOff <= SlotSize`,
   `Flags < 16`; Old iff `KeySize`/`ValueSize` equal the key/elem sizes and `Flags < 32`
   (`internal/abi/map_swiss.go:32-43`, `map_noswiss.go:25-36`). None of the 459 map descriptors
   examined was ambiguous between the two tests. [OBS]
5. **Uncommon location:** `Type.Uncommon` places `UncommonType` after the kind's own descriptor
   struct, not after `Size_` (`internal/abi/type.go:358-363`, Map branch; `UncommonType` at
   `:231-237`; `TFlagUncommon = 1<<0` at `:107`): 0x70 for Swiss, 0x58 for Old. [OBS source]
6. Names were decoded with the GoName scheme (flag byte, LEB128 length, name, optional tag,
   optional `int32` pkgPath NameOff), section-bounded; the same decoder reproduces aether's logged
   EOF pair exactly (calibration below). [OBS]

## Counts

Eight originally assigned carriers (their bytes were unchanged for the whole pass):

| carrier | Go | layout (bytes) | typelinks entries | TL maps / uncommon | scan maps / uncommon / named | uncommon map records |
|---|---|---|---|---|---|---|
| s1246-noswiss-methods | 1.24.6 | old | 464 | 11 / 0 | 12 / 1 / 1 | `*main.Counts`, mcount 2, `Keys,String`, true unc @0x58 |
| s1246-noswiss-nomethods | 1.24.6 | old | 463 | 11 / 0 | 11 / 0 / 0 | — |
| s1246-swiss-methods | 1.24.6 | swiss | 464 | 11 / 0 | 12 / 1 / 1 | `*main.Counts`, mcount 2, @0x70; SlotSize 24 |
| s1246-swiss-nomethods | 1.24.6 | swiss | 463 | 11 / 0 | 11 / 0 / 0 | — |
| s1250-noswiss-methods | 1.25.0 | old | 485 | 11 / 0 | 12 / 1 / 1 | `*main.Counts`, mcount 2, @0x58 |
| s1250-noswiss-nomethods | 1.25.0 | old | 484 | 11 / 0 | 11 / 0 / 0 | — |
| s1250-swiss-methods | 1.25.0 | swiss | 485 | 11 / 0 | 12 / 1 / 1 | `*main.Counts`, mcount 2, @0x70; SlotSize 24 |
| s1250-swiss-nomethods | 1.25.0 | swiss | 484 | 11 / 0 | 11 / 0 / 0 | — |

The shared 11 stdlib map types are identical in all eight: `*map[abi.TypeOff]*abi.Type`,
`*map[int32]unsafe.Pointer`, `*map[interface {}]interface {}`, `*map[runtime._typePair]struct {}`,
`*map[string]*unicode.RangeTable`, `*map[string]bool`, `*map[string]int`,
`*map[string]runtime.metricData`, `*map[uint32][]*abi.Type`, `*map[uint64]bool`,
`*map[unsafe.Pointer]int32`. Each `methods` variant adds exactly `*main.Counts`; each `nomethods`
variant adds nothing. **stdlib alone contributes 0 uncommon map types** (all 11 are unnamed,
`tflag == 2`). [OBS]

Four `nethttp` carriers that appeared mid-pass (source `carriers/src/nethttp/main.go:1-4`, recipe
`carriers/build.sh:5-7,19`; see F4):

| carrier | Go | layout | typelinks | TL maps / unc | scan maps / unc / named | uncommon records (SlotSize → misread NameOff) |
|---|---|---|---|---|---|---|
| s1246-noswiss-nethttp | 1.24.6 | old | 988 | 36 / 0 | 38 / 2 / 2 | `*textproto.MIMEHeader` 5 methods, `*url.Values` 6; true unc @0x58 |
| s1246-swiss-nethttp | 1.24.6 | swiss | 996 | 36 / 0 | 38 / 2 / 2 | same two; SlotSize 40 → misread 0x28 |
| s1250-noswiss-nethttp | 1.25.0 | old | 1020 | 36 / 0 | 38 / 2 / 2 | same two; true unc @0x58 |
| s1250-swiss-nethttp | 1.25.0 | swiss | 1029 | 36 / 0 | 38 / 2 / 2 | same two; SlotSize 40 → misread 0x28 |

Calibration binaries: **notesmd-cli** 63 / 0 (1326 typelinks entries), **aether** 152 / 7
(3739 typelinks entries, 145 maps), both Swiss. [OBS]

## Findings

### F1 — `typelinks` is structurally incomplete for exactly the map types that matter
**[OBS]** In every non-dynlink static build examined, the typelinks view misses every *named* map
type, which is precisely the set that can carry `TFlagUncommon`: aether 145 vs 152 (the 7 missing
are the 7 named uncommon maps), each `methods` carrier 11 vs 12 (the missing one is
`main.Counts`), each `nethttp` carrier 36 vs 38 (the two missing are the named stdlib maps).
Symmetric difference is otherwise empty on all 14 binaries. **[OBS source]** The compiler sets
`MakeTypelink` only when `Flag_dynlink`, or for an *unnamed* composite
(`cmd/compile/internal/reflectdata/reflect.go:948-964`, `TMAP` at `:956`), and `extra` (the
uncommon record) is `t.Sym() != nil || len(methods(t)) != 0` (`:754`). For `-buildmode=exe` the
typelinks table therefore cannot contain a named type, and its map-uncommon count is necessarily 0.

**[INF] Operability consequence for C3:** a `swiss-misread.py`-style counter that enumerates map
descriptors through `moduledata.typelinks` alone will report `map_types` 145/0 on aether (not
152/7) and 11/0 or 36/0 on every synthetic carrier, i.e. it will fail the "aether →
`predicted_eof_reads` contains `[17645861, 111938854]`" calibration and the "methods variants have
≥1 uncommon map type" expectation for a reason unrelated to layout. The span scan with the
`PtrToThis`/name validation above is required; typelinks is a cross-check only. No
`swiss-misread.py` exists yet (`.ufo/waves/round-18/tools/` at 12:43 holds `head-rev-lint.py`,
`jj-red-before.py`, `revpin.py`, `routed-defects.py`), so this is a pre-freeze warning.

### F2 — `TFlagUncommon` means "uncommon record", not "has methods"
**[OBS]** aether's three `go.shape.map[...]` descriptors carry `tflag == 7`
(uncommon|extra-star|named) with `Mcount == 0` and no methods; `dbus.sigSet` has 4,
`textproto.MIMEHeader` 5, `url.Values` 6, `http.Header` 13. **[INF]** A C3 counter that equates
uncommon with method-carrying will report 4 instead of 7 on aether (and miss named-without-methods
map types generally). On the 12 carriers the two counts coincide (Counts=2, nethttp=5/6), so the
frozen expectation is unaffected there, but the emulator's output fields should stay separate
(`uncommon_map_types` vs `map_types_with_methods`).

### F3 — the aether EOF pair is not reproducible on the carriers' bytes
The r17 mechanism (Ghidra binds `runtime.maptype` to the 0x58-byte `OldMapType`) takes
`GoUncommonType.PkgPath` from the low 32 bits of the Swiss `SlotSize`, then decodes a GoName at
`types + NameOff`. **[OBS]** For aether the chain is exactly the r17 trace: `SlotSize 40 →
NameOff 0x28 → record 0x954048` (flags `0x6e`, len 0, tag "a", pkgPath `0x780100`) → record
`0x10d4120` (flags `0xf6`, LEB128 length 111938854) → name bytes at `0x10d4125` = 17645861, past the
section end → logged pair `[17645861, 111938854]`.

**[OBS]** The synthetic carriers do not reproduce that pair; the read destination differs with each
carrier's own `types` blob. Actual misread record for each swiss carrier:

| carrier / uncommon map | misread NameOff | GoName at `types + off` | result |
|---|---|---|---|
| s1246-swiss-methods `Counts` (SlotSize 24) | 0x18 | 0x495018: flags 0x01, len 116, binary name bytes in-file, no tag/pkgPath | no overrun, no second hop |
| s1250-swiss-methods `Counts` (SlotSize 24) | 0x18 | 0x49b018: flags 0x01, len 115, in-file, no tag/pkgPath | no overrun |
| s1246-swiss-nethttp `MIMEHeader`/`Values` (SlotSize 40) | 0x28 | 0x553028: flags 0x6d, len 0, no tag, pkgPath 0x1006901 → `0x1559901` **unmapped** | no overrun; target outside every section |
| s1250-swiss-nethttp `MIMEHeader`/`Values` (SlotSize 40) | 0x28 | 0x552028: flags 0x62, len 0, tag "m", no pkgPath bit | no overrun |
| s1246/s1250-noswiss-* (control) | true uncommon at 0x58 | pkgPath resolves to `main` / `net/textproto` / `net/url` | correct read; no misread |

**[INF]** The `methods` carriers meet the precondition (one uncommon map type) but the misread
destination is a benign in-file GoName. The `nethttp` carriers hit the same 0x28 offset as aether's
three `map[string][]string` types but different bytes (unmapped pkgPath, or a tag-only record).
A frozen prediction that any synthetic carrier emits `[17645861, 111938854]` is not supported by
these bytes: the emulator must decode each carrier's own `types + SlotSize` record rather than
carry aether's pair over. Ghidra's behaviour on an unmapped pkgPath target is not modelled here;
"no EOF" is **[INF]**, the addresses/bytes are **[OBS]**.

### F4 — the carrier set changed mid-pass; the `nethttp` cell is the right shape
**[OBS]** At this pass's first listing the carrier directory held the 8 files + `SHA256SUMS`
(carrier file mtimes 12:15). At 12:36–12:37 four `*nethttp` carriers and `src/nethttp/main.go`
appeared and `SHA256SUMS` gained four rows (all 12 verify, exit 0). `carriers/build.sh:5-7` records that they
were added "after CriticC3: the methods/nomethods pair is predicted non-diagnostic". The eight
originally assigned carriers are byte-identical to the start of this pass. The nethttp source
imports `net/http`, `net/textproto`, `net/url`; only `MIMEHeader` and `url.Values` appear as Map
descriptors — `http.Header` is absent from all four nethttp binaries (zero in the validated map
inventory). **[INF]** That is reachability pruning, so the aether-like set is 2 of 3, not 3.

### F5 — notesmd-cli detail
**[OBS]** 63 descriptors at 63 distinct addresses, 60 distinct stripped names; the three duplicate
names are `map[string]yaml.fieldInfo`, `map[reflect.Type]*yaml.structInfo`,
`map[string]yaml.resolveMapItem`; each pair shares one name string but has distinct elem-type
records (e.g. elem VAs `0x64ffc0` vs `0x6502c0` for the fieldInfo pair). [OBS] The binary carries
both `gopkg.in/yaml.v2` and `gopkg.in/yaml.v3`, so the pair is the two modules' same-named types.
[INF] Counting descriptors (the runtime objects) gives 63; counting printed names gives 60. All
`tflag == 2`, all Swiss (`GroupSize = 8*SlotSize+8` matched 63/63).
Span-scan candidates rejected as non-types: 752 (random `kind` nibbles failing
size/ptrdata/align or field-pointer checks); no rejected candidate had a map-like name.

## Calibration chain
- **[OBS]** aether `moduledata@0x172e400`, `types=0x954020`, `etypes=0x13b4999`, `typelinks` ptr
  `0x13b4c40` len 3739 — identical to `.ufo/waves/round-17/w2/RevAetherEOF.md:52`.
- **[OBS]** aether 152 maps / 7 uncommon and the exact 7 names match `CriticAetherUnknown.md:60`;
  notesmd-cli 63/0 matches `:117`. The decoder also reproduces the exact EOF pair through the
  independent chain in the same file's links 4–6.
- **[OBS]** aether's seven uncommon maps yield Old-reader NameOffs `{0x18, 0x20, 0x28}`
  (SlotSizes 24/32/40), matching `CriticAetherUnknown.md:77` ("misread nameOffs are only 0x20,
  0x18 and 0x28").
- **[OBS]** layout split from bytes matches `GOEXPERIMENT` from `go version -m` on 12/12 carriers
  (`noswissmap` → old on all four noswiss; default → swiss on all four swiss).
- **[OBS]** control pkgPaths resolve through the Old-layout 0x58 read: `main` (Counts),
  `net/textproto` (MIMEHeader), `net/url` (Values).

## Limits
- Counts are descriptor counts, not logical-type counts (F5); `go.shape.*` types are included.
- `moduledata` offsets are the Go 1.20–1.25 layout; for notesmd-cli 1.25.8 and aether 1.25.14 this
  is **[INF]** from the 1.25.0 source, but the field values validate (pclntable pointer, ftab
  length, typelinks identity), which would fail on a shifted layout.
- The span scan assumes type descriptors live in `[types, etypes)` and are 8-byte aligned; that is
  the runtime contract, not separately proven here.
- No Ghidra replay, no REA, no carrier execution: every Ghidra-facing statement is INFERENCE from
  bytes plus the r17-reported binding (`runtime.maptype → OldMapType`, 0x58).
- A /tmp scratch parser was created; no lane file other than this report was written; no tools
  installed or upgraded.

## Commands (read-only; exit codes as observed)

```
$ cd /home/vgpnk/.local/share/kaidoku-r18/carriers && sha256sum -c SHA256SUMS
s1246-noswiss-methods: OK
s1246-noswiss-nethttp: OK
s1246-noswiss-nomethods: OK
s1246-swiss-methods: OK
s1246-swiss-nethttp: OK
s1246-swiss-nomethods: OK
s1250-noswiss-methods: OK
s1250-noswiss-nethttp: OK
s1250-noswiss-nomethods: OK
s1250-swiss-methods: OK
s1250-swiss-nethttp: OK
s1250-swiss-nomethods: OK
exit 0

$ for f in /home/vgpnk/.local/share/kaidoku-r18/carriers/s1* /home/vgpnk/.local/bin/notesmd-cli /usr/bin/aether; do /home/vgpnk/.local/opt/go-1.25.0/bin/go version -m "$f" | head -1; done
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-methods: go1.24.6 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-nethttp: go1.24.6 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-nomethods: go1.24.6 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-methods: go1.24.6
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp: go1.24.6
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nomethods: go1.24.6
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-noswiss-methods: go1.25.0 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-noswiss-nethttp: go1.25.0 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-noswiss-nomethods: go1.25.0 X:noswissmap
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-methods: go1.25.0
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nethttp: go1.25.0
/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nomethods: go1.25.0
/home/vgpnk/.local/bin/notesmd-cli: go1.25.8
/usr/bin/aether: go1.25.14
exit 0

$ cd /tmp/r18-revmaps && for f in /home/vgpnk/.local/share/kaidoku-r18/carriers/s1* /home/vgpnk/.local/bin/notesmd-cli /usr/bin/aether; do python3 -I -B typemaps.py --carrier "$f" --compact >/dev/null || echo "FAIL $f"; done; echo "matrix-exit=$?"
matrix-exit=0

$ for f in /home/vgpnk/.local/share/kaidoku-r18/carriers/s1*; do python3 -I -B typemaps.py --carrier "$f" | python3 -c '
import json,sys
d=json.load(sys.stdin); c=d["carrier"]["path"].split("/")[-1]
tl=d["typelinks_view"]; sc=d["span_scan_view"]
u=[m for m in d["map_types"] if m["uncommon"]]
extra=";".join("%s slot=%d oldread=0x%x"%(m["name"],m["descriptor_tail"]["u64_88"],m["old_reader_uncommon_at_0x58"]["pkgpath_u32"]) for m in u)
print("%-22s %-8s %-5s scan=%2d unc=%d named=%d tl(%2dmap/%dunc) %s" % (c,d["carrier"]["buildinfo_version_scan"],",".join(sc["layout_counts"]),sc["kind_map"],sc["kind_map_uncommon"],sc["kind_map_named"],tl["kind_map"],tl["kind_map_uncommon"],extra))
'; done
s1246-noswiss-methods  go1.24.6 old   scan=12 unc=1 named=1 tl(11map/0unc) *main.Counts slot=562958543356483 oldread=0x243
s1246-noswiss-nethttp  go1.24.6 old   scan=38 unc=2 named=2 tl(36map/0unc) *textproto.MIMEHeader slot=1407396358410622 oldread=0x517e;*url.Values slot=1688875630074893 oldread=0x1c0d
s1246-noswiss-nomethods go1.24.6 old  scan=11 unc=0 named=0 tl(11map/0unc)
s1246-swiss-methods    go1.24.6 swiss scan=12 unc=1 named=1 tl(11map/0unc) *main.Counts slot=24 oldread=0x18
s1246-swiss-nethttp    go1.24.6 swiss scan=38 unc=2 named=2 tl(36map/0unc) *textproto.MIMEHeader slot=40 oldread=0x28;*url.Values slot=40 oldread=0x28
s1246-swiss-nomethods  go1.24.6 swiss scan=11 unc=0 named=0 tl(11map/0unc)
s1250-noswiss-methods  go1.25.0 old   scan=12 unc=1 named=1 tl(11map/0unc) *main.Counts slot=562958543356465 oldread=0x231
s1250-noswiss-nethttp  go1.25.0 old   scan=38 unc=2 named=2 tl(36map/0unc) *textproto.MIMEHeader slot=1407396358410745 oldread=0x51f9;*url.Values slot=1688875630075039 oldread=0x1c9f
s1250-noswiss-nomethods go1.25.0 old  scan=11 unc=0 named=0 tl(11map/0unc)
s1250-swiss-methods    go1.25.0 swiss scan=12 unc=1 named=1 tl(11map/0unc) *main.Counts slot=24 oldread=0x18
s1250-swiss-nethttp    go1.25.0 swiss scan=38 unc=2 named=2 tl(36map/0unc) *textproto.MIMEHeader slot=40 oldread=0x28;*url.Values slot=40 oldread=0x28
s1250-swiss-nomethods  go1.25.0 swiss scan=11 unc=0 named=0 tl(11map/0unc)
exit 0
```
(`oldread` is `u32@+0x58`: the true uncommon pkgPath on old-layout carriers, and the
Swiss-misread nameOff on swiss-layout carriers. The `slot=` column is only meaningful on swiss
carriers; on old carriers it reads into the uncommon record.)
```

$ cd /tmp/r18-revmaps
$ python3 -I -B typemaps.py --carrier /usr/bin/aether --name-chain 0x28 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["types"],d["eof_pair"]); [print(h) for h in d["name_chain"]]'
0x954020 [17645861, 111938854]
{'flags': '0x6e', 'len': 0, 'name': '', 'name_bytes_at': '0x95404a', 'name_bytes_status': 'ok', 'offset': 40, 'pkgpath': 7864576, 'pkgpath_va': '0x10d4120', 'record_va': '0x954048', 'tag': 'a', 'tag_len': 1, 'tag_status': 'ok'}
{'flags': '0xf6', 'len': 111938854, 'name_bytes_at': '0x10d4125', 'name_bytes_status': 'eof', 'offset': 7864576, 'record_va': '0x10d4120'}
exit 0

$ for f in s1246-swiss-methods s1250-swiss-methods; do echo "== $f"; python3 -I -B typemaps.py --carrier /home/vgpnk/.local/share/kaidoku-r18/carriers/$f --name-chain 0x18 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(" eof",d["eof_pair"]); [print("  hop",h) for h in d["name_chain"]]'; done
== s1246-swiss-methods
 eof None
  hop {'flags': '0x1', 'len': 116, 'name_bytes_at': '0x49501a', 'name_bytes_status': 'ok', 'offset': 24, 'record_va': '0x495018'}
== s1250-swiss-methods
 eof None
  hop {'flags': '0x1', 'len': 115, 'name_bytes_at': '0x49b01a', 'name_bytes_status': 'ok', 'offset': 24, 'record_va': '0x49b018'}
exit 0

$ python3 -I -B typemaps.py --carrier /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp --name-chain 0x28
{"eof_pair": null}  (hop 0x553028 flags 0x6d len 0 pkgPath 0x1006901 → 0x1559901 unmapped)
exit 0

$ python3 -I -B typemaps.py --carrier /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nethttp --name-chain 0x28
{"eof_pair": null}  (hop 0x552028 flags 0x62 len 0 tag "m", no pkgPath bit)
exit 0

$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && grep -n "412dc532\|06c91f55" .ufo/waves/round-17/runs/pro-*/receipt.json
.ufo/waves/round-17/runs/pro-aether/receipt.json:7: "sha256_post": "06c91f55…06e"
.ufo/waves/round-17/runs/pro-aether/receipt.json:8: "sha256_pre": "06c91f55…06e"
.ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json:7: "sha256_post": "412dc532…02d"
.ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json:8: "sha256_pre": "412dc532…02d"
(8 matches in 2 files; the other four hits are nested subject digests)
exit 0

$ grep -n "63 map types\|no map types" corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
155:  - The base JSON is identical for notesmd-cli. notesmd-cli has no map types
163:    (notesmd-cli has 63 map types) without a log line. "No error" in the
exit 0

$ grep -n "keep := base.Ctxt.Flag_dynlink\|if !keep && t.Sym() == nil\|case types.TPTR, types.TARRAY, types.TCHAN, types.TFUNC, types.TMAP, types.TSLICE, types.TSTRUCT\|lsym.Set(obj.AttrMakeTypelink, keep)\|extra := t.Sym() != nil" /home/vgpnk/.local/opt/go-1.25.0/src/cmd/compile/internal/reflectdata/reflect.go
754:	extra := t.Sym() != nil || len(methods(t)) != 0
948:	keep := base.Ctxt.Flag_dynlink
949:	if !keep && t.Sym() == nil {
956:		case types.TPTR, types.TARRAY, types.TCHAN, types.TFUNC, types.TMAP, types.TSLICE, types.TSTRUCT:
964:	lsym.Set(obj.AttrMakeTypelink, keep)
exit 0

$ python3 -I -B typemaps.py --carrier /home/vgpnk/.local/bin/notesmd-cli | python3 -c '
import json,sys,collections
d=json.load(sys.stdin); ms=d["map_types"]
print("count",len(ms),"tflag",dict(collections.Counter(m["tflag"] for m in ms)),"layouts",d["span_scan_view"]["layout_counts"])
print("names unique",len({m["name_stripped"] for m in ms}),"dup",[k for k,v in collections.Counter(m["name_stripped"] for m in ms).items() if v>1])
print("named",sum(m["named"] for m in ms),"uncommon",sum(m["uncommon"] for m in ms))
'
count 63 tflag {2: 63} layouts {'swiss': 63}
names unique 60 dup ['map[string]yaml.fieldInfo', 'map[reflect.Type]*yaml.structInfo', 'map[string]yaml.resolveMapItem']
named 0 uncommon 0
exit 0
```

Report: `.ufo/waves/round-18/w1/RevNotesmdMaps.md`
