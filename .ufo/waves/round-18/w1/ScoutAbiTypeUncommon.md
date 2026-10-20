# ScoutAbiTypeUncommon — `abi.Type` / `TFlagUncommon` / `UncommonType` / `Type.Uncommon`

Seat: `KaidokuR18.ScoutAbiTypeUncommon` (leaf, advisory; Git HEAD `9011581d`, lane read-only).
Source: `/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/type.go` (go1.25.0, `go version go1.25.0 linux/amd64`, observed).
Labels: **[OBS]** = read/measured this session; **[INF]** = inference, not measured.

## 1. The answer in one line

**[OBS]** `Type.Uncommon()` returns `&(*u)(unsafe.Pointer(t)).u` where `u` embeds *the kind's own descriptor struct*; the uncommon offset is therefore `align_up(sizeof(kind descriptor), alignof(UncommonType)=4)`, which equals `sizeof(kind descriptor)` for every kind on both measured pointer widths (every descriptor size is a multiple of 4).

## 2. Exact anchors (all `type.go` unless stated)

| item | lines | content |
|---|---|---|
| `type Type struct` | 20–45 | `Size_`, `PtrBytes`, `Hash uint32`, `TFlag`, `Align_`, `FieldAlign_`, `Kind_`, `Equal`, `GCData`, `Str NameOff`, `PtrToThis TypeOff` |
| `TFlag` type | 89 | `type TFlag uint8` (doc 87–88) |
| `TFlagUncommon` const | **107** | `TFlagUncommon TFlag = 1 << 0`, doc block 92–106 ("just beyond the shared-per-type common data"; struct vs interface get *different* offsets) |
| `Kind()` | 193 | `return t.Kind_ & KindMask` — the switch key is masked, so kind bits above `KindMask` (`1<<5 - 1`, line 84) are not compared |
| `type UncommonType struct` | **231–237** | `PkgPath NameOff` (4), `Mcount uint16` (2), `Xcount uint16` (2), `Moff uint32` (4), `_ uint32` (4) |
| `UncommonType.Methods()` | 239–244 | early `nil` when `Mcount == 0`; else `addChecked(t, t.Moff)` → `[:Mcount:Mcount]` |
| `type structTypeUncommon struct` | **306–309** | `StructType` + `u UncommonType` — the only named helper; other kinds declare an anonymous twin inside the switch |
| `func (t *Type) Uncommon()` | **321–377** | `nil` unless `TFlag&TFlagUncommon != 0` (322–324), then `switch t.Kind()` (325) |

Switch branches: `Struct` 326–327, `Pointer` 328–333, `Func` 334–339, `Slice` 340–345, `Array` 346–351, `Chan` 352–357, **`Map` 358–363**, `Interface` 364–369, `default` 370–375.

## 3. The ≤25-word quote

> `func (t *Type) Uncommon()`: uncommon data follows the kind's own descriptor struct — `case Map:` wraps `mapType` (`type.go:321,358-363`).

(17 words. Verbatim tokens: `type.go:321` = `func (t *Type) Uncommon() *UncommonType {`; `type.go:360` = `mapType` inside the `case Map:` struct.)

## 4. Offset table — map kind → which struct

**[OBS]** measured by `unsafe.Offsetof` on anonymous structs whose embedded descriptor is extracted verbatim (regex `^type (\w+) struct` block capture) from `type.go`, `map_swiss.go`, `map_noswiss.go`, compiled and run by the installed go1.25.0 (`GOOS=linux`, `CGO_ENABLED=0`, scratch `mkdtemp`, outside the lane). Probe `exit=0` for amd64 and 386.

| `Kind` | branch | descriptor struct | source | sizeof amd64 | **uncommon off amd64** | sizeof 386 | **off 386** |
|---|---|---|---|---|---|---|---|
| `Struct` | 326–327 | `StructType` | `type.go:560-564` | 88 | **88** | 52 | **52** |
| `Pointer` | 328–333 | `PtrType` | `type.go:545-548` | 56 | **56** | 36 | **36** |
| `Func` | 334–339 | `FuncType` | `type.go:497-501` | 56 | **56** | 36 | **36** |
| `Slice` | 340–345 | `SliceType` | `type.go:481-484` | 56 | **56** | 36 | **36** |
| `Array` | 346–351 | `ArrayType` | `type.go:271-276` | 72 | **72** | 44 | **44** |
| `Chan` | 352–357 | `ChanType` | `type.go:300-304` | 64 | **64** | 40 | **40** |
| **`Map`** | **358–363** | **`mapType`** = build-selected alias | `map_select_swiss.go:22` / `map_select_noswiss.go:10` | **112** (`SwissMapType`) / **88** (`OldMapType`) | **112 / 88** | 64 / 56 | **64 / 56** |
| `Interface` | 364–369 | `InterfaceType` | `type.go:449-453` | 88 | **88** | 52 | **52** |
| `default` (`Bool`…`UnsafePointer`, `String`, unnamed) | 370–375 | bare `Type` | `type.go:20-45` | 48 | **48** | 32 | **32** |

Supporting measurements **[OBS]**: `sizeof(Type)` 48/32, `sizeof(UncommonType)` 16 (**ptrSize-independent**, align 4, `Moff` at +8); `SwissMapType` field offsets amd64 `Key=48 Elem=56 Group=64 Hasher=72 GroupSize=80 SlotSize=88 ElemOff=96 Flags=104`; `OldMapType` `Key=48 Bucket=64 Hasher=72 KeySize=80 BucketSize=82 Flags=84`.

Independent cross-check **[OBS]**: the linker-facing formulas in `internal/abi/compiletype.go:15` `CommonSize(ptrSize) = 4*ptrSize + 8 + 8` → 48 / 32, matching the probe, and `:20-22` `UncommonSize() = 4+2+2+4+4` = 16; `cmd/compile/internal/rttype/rttype.go:78-86` asserts `CommonSize`, `StructFieldSize`, `UncommonSize` and `TFlagOff` (= `2*ptrSize+4` → 20 / 12, i.e. `TFlag` at byte 20 on amd64) against reflection-derived sizes. **The compiler never re-derives the uncommon offset by hand**: it builds each descriptor from `reflect.TypeOf(abi.X{})` (`rttype.go:24-40,60-67`), so padding is automatic there.

### Two consequences worth carrying

1. **[OBS] `Func` offset is 56, not 52.** `FuncType` is 48 + `uint16` + `uint16` = 52 declared bytes, padded to alignment 8 → 56 on amd64 (386 has no pad: 36). A reader that sums declared field widths lands 4 bytes early for func kinds only. This is the same *class* of bug as the map one, at 1/6 the magnitude.
2. **[OBS] `Map` is the only kind whose offset is build-configuration dependent** — through the alias `type mapType = SwissMapType` under `//go:build goexperiment.swissmap` (`map_select_swiss.go:5,22`) vs `= OldMapType` under `!goexperiment.swissmap` (`map_select_noswiss.go:5,10`). The upstream comment is explicit about the hazard: "mapType *must not be used by any functions called in the compiler to build a target program* because the compiler must use the map type determined by run-time GOEXPERIMENT, not the build tags" (`map_select_swiss.go:12-15`), and it names `Type.Uncommon` as one of the functions that "depend on the layout of type + uncommon objects in the binary" (`:17-21`). **[INF]** Therefore an offline analyzer must resolve swiss-vs-old from the *target* binary (Go version ≥ 1.24 and `GOEXPERIMENT` lacking `noswissmap`), never from its own build tags; `internal/buildcfg/exp.go:85` defaults `SwissMap: true`.

## 5. Registry coverage — do **not** draft a new row

**[OBS]** `corpus/SOURCES.md` registry has 32 rows, `S001`–`S032` (`S032` at line 38). Nothing in `corpus/` mentions `UncommonType`, `TFlagUncommon`, or `internal/abi/type.go` (grep, exit 0; only `S032`'s PR row matched anything abi-adjacent).

**[OBS]** A sibling w1 draft already registers this source: `.ufo/waves/round-18/w1/DraftAbiRow.md:10` drafts **S034** for `map_swiss.go` / `map_noswiss.go` / `map_select_*.go`, and its gate quote already cites `type.go:358-363`. Its evidence list covers `type.go:20-45`, `:320-326`, `:358-363`, `:387-390`, `:475-476`. It does **not** cover `TFlagUncommon` (`:107`), the `UncommonType` field layout (`:231-237`), `structTypeUncommon` (`:306-309`), the branch-by-branch switch, or any measured offset.

Disposition: **covered for source registration by S034; not covered for the offset law.** Recommended action for L1 (no new row; two rows would duplicate one source):
- append one clause to `S034`'s `teaches` cell: `Type.Uncommon type.go:321-377 places UncommonType (16 bytes, ptrSize-independent) after the kind descriptor: Struct 88, Pointer/Func/Slice 56, Array 72, Chan 64, Interface 88, Map 112 (swiss) / 88 (old), default 48 on amd64`;
- extend S034's `anchor` cell with `type.go` sha256 (my probe hash of the extracted definitions is not a file digest, so L1 should take `sha256sum` at integration);
- optionally add the quote in §3 to S034's gate line.

**[OBS] ID collision to resolve:** `.ufo/waves/round-18/w1/DraftGoNotesRow.md:7` *also* proposes `S034` for the Go 1.24 release-notes row, while `claims.json:14` reserves `S033` for C1. Two drafts claim the same provisional id; L1 must assign distinct ids (next free after `S032` is `S033`, then `S034`).

## 6. Consumer cross-reference (observed, read-only; owner is `RevGhidraMapTypeRead`)

`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoType.java` reads the uncommon structure at the *modelled* descriptor end:
`getOffsetEndOfFullType()` = `context.getStructureEnd() + GoUncommonType length` (`:124-128`), `getEndOfTypeInfo()` (`:137-141`), and `getUncommonType()` = `readStructure(GoUncommonType.class, context.getStructureEnd())` (`:144-150`). So Ghidra's uncommon offset is exactly `sizeof(its GoMapType)`, which makes the §4 map numbers the operand the revenger needs. I did **not** determine Ghidra's `GoMapType` size or JSON selection (that is the revenger's item).

**[INF] (hypothesis, explicitly not established by this source)** If a reader uses the `OldMapType` end (88) on an amd64 Swiss descriptor, byte 88 is the low half of `SlotSize` and byte 96 is `ElemOff`. Then `PkgPath = low32(SlotSize)`, `Mcount/Xcount = high32(SlotSize)` ≈ 0 for any realistic slot size (≤ 8×128), and `Moff = low32(ElemOff)`. That predicts **silently-zero methods** (`Methods()` returns `nil` at `type.go:240-242`), not a bogus `Moff` advance. Any aether EOF (`Unable to read past EOF: 17645861, 111938854`) therefore has to be attributed to another field/consumer; asserting it from the map-layout shift alone would be unfounded. On 386 the shift is 8 bytes and byte 56 is `ElemOff`, so the same reader lands at a different field — the failure mode is arch-dependent.

## 7. Limits

- 32-bit numbers come from a cross-*compiled and executed* 386 binary on this amd64 host; `GOARCH=arm64` was attempted and failed with `exec format error` (exit 1) — arm64 sizes are **not** measured (word size 8 like amd64, so **[INF]** identical).
- The probe mirrors the `abi` field order/extracted blocks because `internal/abi` cannot be imported outside the standard library; the sizes are therefore a check of the declared layout plus Go's padding rules, not a read of a compiled carrier's `moduledata`.
- No carrier binary, REA, Ghidra or `analyzeHeadless` was executed; no network used.
- `go1.24.6` and `go1.27.3` trees were not opened here; `go1.27.3` may differ (`S026` covers it).

## 8. Commands run (exit codes)

| # | command | exit |
|---|---|---|
| 1 | `grep -n "TFlagUncommon\|UncommonType\|func (t \*Type) Uncommon\|type Type struct" /home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/type.go` | 0 |
| 2 | `grep -n -E "^(type (PtrType\|FuncType\|SliceType\|ArrayType\|ChanType\|mapType\|InterfaceType\|StructType\|IfaceType) struct)\|…" $f` (symbol anchors) | 0 |
| 3 | `sed -n`/`awk` numbered spans over `type.go:20-45,92-108,226-250,265-320,306-390,399-440` | 0 |
| 4 | `cat -n map_select_swiss.go map_select_noswiss.go` + `sed -n '1,60p' map_swiss.go map_noswiss.go` | 0 |
| 5 | `go run <mkdtemp>/main.go` (verbatim-extracted structs; `GOOS=linux GOARCH=amd64`, `CGO_ENABLED=0`) → size row | 0 |
| 6 | same probe with `GOARCH=386` → 386 row | 0 |
| 7 | same probe with `GOARCH=arm64` | **1** (`exec format error`, cross-binary cannot run) |
| 8 | `go run` probe #2 (`unsafe.Offsetof` per switch branch, amd64 + 386) | 0 / 0 |
| 9 | `go run` probe #3 (per-field offsets in `SwissMapType`/`OldMapType`, amd64 + 386) | 0 / 0 |
| 10 | `grep -n "Uncommon" cmd/compile/internal/rttype/rttype.go`; `awk 60-90`; `awk 14-30 internal/abi/compiletype.go` | 0 |
| 11 | `unzip -p Base-src.zip .../rtti/types/GoType.java \| grep -nE "getUncommonType\|uncommon"`; `awk 120-152` on the same member | 0 |
| 12 | `grep -rn "UncommonType\|TFlagUncommon" corpus/ .ufo/waves/round-18/` | 0 |
| 13 | `grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md \| sort -u \| tail -5` (max `S032`) | 0 |

Probe hygiene: every scratch program was written under `tempfile.mkdtemp()` and hashed (`extracted-defs-sha256 22a457e6240d5413`, first probe); no file inside the lane was created except this report.

## 9. Tools / installs

No installs, no upgrades, no network. Used the pre-existing `/home/vgpnk/.local/opt/go-1.25.0` toolchain as a runner only.
