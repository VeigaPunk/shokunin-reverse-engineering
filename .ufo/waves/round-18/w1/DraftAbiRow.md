# DraftAbiRow — go1.25.0 `internal/abi` map descriptors (C3 frontier, draft only)

Author: `KaidokuR18.DraftAbiRow` (leaf, advisory). Lane files not edited. L1 integrates.
ID note: `claims.json` assigns `S033` to C1 (S033 supersedes S032). This draft uses **S034**; L1 confirms the id at integration.

## Draft

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S034 | Go 1.25.0 `internal/abi` map type descriptors — `src/internal/abi/map_swiss.go`, `map_noswiss.go`, `map_select_swiss.go`, `map_select_noswiss.go` (go1.25.0 tarball at `/home/vgpnk/.local/opt/go-1.25.0`; `raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/`) | code | A | The go1.25.0 toolchain's own `SwissMapType` and `OldMapType` descriptor structs and the build-tag alias that selects one; not Ghidra's reader and not Go 1.26 | Official go1.25.0 tree; sha256 `map_swiss.go` `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383`, `map_noswiss.go` `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`, `map_select_swiss.go` `c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718`, `map_select_noswiss.go` `b8a433106c57585b8da857321f48bbeae4cc18050c1c02ee9b0700e2103b974f`; `map_swiss.go:32-43`, `map_noswiss.go:25-36`, `map_select_swiss.go:5,22`, `map_select_noswiss.go:5,10`, `type.go:358-363` | Swiss descriptor is `Type` + Key/Elem/Group pointers, Hasher, GroupSize/SlotSize/ElemOff, `Flags uint32` (112 B amd64, flags at 104); old descriptor is `Type` + Key/Elem/Bucket, Hasher, `KeySize`/`ValueSize` uint8, `BucketSize` uint16, `Flags uint32` (88 B amd64, flags at 84). The build tag `goexperiment.swissmap` picks which struct is `mapType`, so the `Map` uncommon-data offset in `Type.Uncommon()` (`type.go:358-363`) moves by 24 bytes between builds. | mined | 2026-10-20 | on-release | corpus/lessons/round-18.md (draft; L1 adds), corpus/knowledge/2026-10-20-r18-swiss-map-layout.md (draft; L1 adds) |

## Gate quote line (draft)

> `internal/abi` at go1.25.0 declares `type SwissMapType struct {` (`map_swiss.go:32`) and `type OldMapType struct {` (`map_noswiss.go:25`), and aliases `type mapType = SwissMapType` only under `//go:build goexperiment.swissmap` (`map_select_swiss.go:5,22`) and `type mapType = OldMapType` under `//go:build !goexperiment.swissmap` (`map_select_noswiss.go:5,10`); `type.go:358-363` puts uncommon data after `mapType` for `Map`.

## Evidence (path:line and command sources)

Observations (opened and read this round, go1.25.0 local tree, identical to `raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/`; `cmp` returned identical for all five files fetched: `map_swiss.go`, `map_noswiss.go`, `type.go`, `map_select_swiss.go`, `map_select_noswiss.go`):

- `map_swiss.go:32-43`: `SwissMapType` fields in order: embedded `Type`; `Key *Type`; `Elem *Type`; `Group *Type`; `Hasher func(unsafe.Pointer, uintptr) uintptr`; `GroupSize uintptr`; `SlotSize uintptr`; `ElemOff uintptr`; `Flags uint32`.
- `map_swiss.go:45-51`: flags `SwissMapNeedKeyUpdate`, `SwissMapHashMightPanic`, `SwissMapIndirectKey`, `SwissMapIndirectElem` via `1 << iota`.
- `map_swiss.go:22-23`: `SwissMapMaxKeyBytes = 128`, `SwissMapMaxElemBytes = 128`.
- `map_noswiss.go:25-36`: `OldMapType` fields in order: embedded `Type`; `Key`; `Elem`; `Bucket *Type`; `Hasher`; `KeySize uint8`; `ValueSize uint8`; `BucketSize uint16`; `Flags uint32`.
- `map_noswiss.go:38-54`: old flags are literal bits: `IndirectKey` `Flags&1`, `IndirectElem` `&2`, `ReflexiveKey` `&4`, `NeedKeyUpdate` `&8`, `HashMightPanic` `&16`; comment at `:38-39` says these must match `cmd/compile/internal/reflectdata/reflect.go:writeType`.
- `map_select_swiss.go:5` `//go:build goexperiment.swissmap`; `:22` `type mapType = SwissMapType`.
- `map_select_noswiss.go:5` `//go:build !goexperiment.swissmap`; `:10` `type mapType = OldMapType`.
- `type.go:20-45`: `Type` header: `Size_`, `PtrBytes`, `Hash uint32`, `TFlag`, `Align_`, `FieldAlign_`, `Kind_`, `Equal`, `GCData`, `Str NameOff`, `PtrToThis TypeOff`.
- `type.go:320-326`: `Uncommon()` returns nil unless `TFlagUncommon`.
- `type.go:358-363`: `case Map:` wraps `struct { mapType; u UncommonType }` and returns `&...u`, so uncommon data follows the build-selected map struct.
- `type.go:387-390`, `:475-476`: `Elem()` and `Key()` for `Map` cast through `mapType`.
- `cmd/compile/internal/reflectdata/reflect.go:775-779`: type-descriptor size chosen by `buildcfg.Experiment.SwissMap` (`rttype.SwissMapType` vs `rttype.OldMapType`).
- `cmd/compile/internal/reflectdata/reflect.go:879-883`: writer dispatch on the same flag.
- `cmd/compile/internal/reflectdata/map_swiss.go:264-309`: Swiss writer fills `Key`, `Elem`, `Group`, `Hasher`, `GroupSize`, `SlotSize`, `ElemOff`, `Flags`, and an `R_KEEP` reloc for named maps; `elemOff` is asserted to be 8 for `AMEM64` keys and 16 for `ASTRING` keys (`:274-279`).
- `cmd/compile/internal/reflectdata/map_noswiss.go:259-301`: old writer sets `KeySize`/`ValueSize` to `PtrSize` with flag 1/2 when a slot exceeds 128 bytes; `BucketSize` is `uint16(OldMapBucketType(t).Size())`; flags 4/8/16 for reflexive, need-update, hash-might-panic.
- `runtime/type.go:607-611`: `typesEqual` for `abi.Map` chooses `abi.SwissMapType` or `abi.OldMapType` on `goexperiment.SwissMap`.
- `internal/buildcfg/exp.go:85`: baseline `SwissMap: true`; `go env GOEXPERIMENT` (go1.25.0) printed empty, i.e. default flags.

Measurement (command source): `/home/vgpnk/.local/opt/go-1.25.0/bin/go run main.go` in `/tmp/r18abi/probe/` (throwaway, outside the lane; `GOFLAGS=-mod=mod`), then `GOARCH=386 ... go run main.go`. The probe mirrors the `abi` field order because `internal/` cannot be imported:

- amd64: `Type` 48 (align 8); `SwissMapType` 112 (Key 48, Elem 56, Group 64, Hasher 72, GroupSize 80, SlotSize 88, ElemOff 96, Flags 104); `OldMapType` 88 (Key 48, Elem 56, Bucket 64, Hasher 72, KeySize 80, ValueSize 81, BucketSize 82, Flags 84).
- 386: `Type` 32; `SwissMapType` 64 (Flags 60); `OldMapType` 56 (Flags 52).

Inference (not observed in this round): the 24-byte amd64 difference (112 vs 88) is the shift that makes a reader using the wrong map layout read uncommon and method data from the wrong offset. The contract's C3 pair tests that inference on carriers; this draft does not test it.

## Limits

- Ghidra 12.1.4 was not opened or run; its `GoMapType` layout is not described here (C3's `swiss-misread.py` owns that comparison).
- `/tmp/r18abi/probe/main.go` is a mirror, so the measured sizes check arithmetic of the declared fields, not the compiler's `rttype` output. The compiler-emitted layout would need a built carrier, which is out of this leaf's scope.
- Go 1.24 and Go 1.26 were not opened.
- The `## Gate` line quotes the source; it does not claim any carrier outcome.

## Tools / installs

- No installs or updates. Used the existing go1.25.0 toolchain only as a runner for the probe (`go version go1.25.0 linux/amd64`).
- Network: `curl -sfL` to `raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/` for `map_swiss.go`, `map_noswiss.go`, `type.go`, `map_select_swiss.go`, `map_select_noswiss.go`; all identical to local.
- Lane: read-only (`read`, `grep`, `glob`). Only this report written; no `jj`, no git writes, no REA, no carrier execution.
