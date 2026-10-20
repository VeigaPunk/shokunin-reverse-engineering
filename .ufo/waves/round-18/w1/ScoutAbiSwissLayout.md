# ScoutAbiSwissLayout — Go 1.24/1.25 amd64 map descriptor layouts

Author: `KaidokuR18.ScoutAbiSwissLayout` (leaf, author-side advisory). Lane files not edited; only this report written. L1 integrates.

Scope: the `internal/abi` map type definitions in the official go1.24.6 and go1.25.0 trees, their upstream raw bytes, field lists, and **compiled amd64** struct sizes/offsets. Not Ghidra's reader (C3's `swiss-misread.py` owns that), not Go 1.26, not 32-bit, no carrier execution, no REA.

Path shorthands used below (each expands to an absolute path):
`A124` = `/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi`; `A125` = `/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi`;
`R124` = `/home/vgpnk/.local/opt/go-1.24.6/src/cmd/compile/internal/reflectdata`; `R125` = `/home/vgpnk/.local/opt/go-1.25.0/src/cmd/compile/internal/reflectdata`;
`RT125` = `/home/vgpnk/.local/opt/go-1.25.0/src/runtime`.

## Verdict (all OBSERVED unless marked)

| struct | amd64 size | align | trailing pad | `Flags` offset |
|---|---|---|---|---|
| `abi.Type` (embedded header) | 48 | 8 | 0 | — |
| `abi.SwissMapType` | **112** | 8 | 4 bytes (108–111) | **104** |
| `abi.OldMapType` | **88** | 8 | 0 | **84** |

Both toolchains produce the same numbers, and the two map source files are **byte-identical** between 1.24.6 and 1.25.0. So the 1.24→1.25 version step is not what selects a map descriptor layout; the build experiment `buildcfg.Experiment.SwissMap` is (§5).

## 1. Provenance (OBSERVED)

- Toolchain identity: `go version go1.24.6 linux/amd64` and `go version go1.25.0 linux/amd64` (exit 0); `VERSION` files say `go1.24.6` / `time 2025-08-01T19:18:26Z` and `go1.25.0` / `time 2025-08-08T19:33:32Z`.
- Local file sha256 (exit 0):
  - `A124/map_swiss.go` and `A125/map_swiss.go` = `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383`
  - `A124/map_noswiss.go` and `A125/map_noswiss.go` = `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`
  - `A124/type.go` = `44ee183a5a3567f6c1e3cc7ca813cbaabcb3834516442ce447ecb5631aa5a2a9`; `A125/type.go` = `6f3e3d720b4ba23750593d77dcc8e844fdfa18581a17e045e21b68c7f6cc603c`
- `cmp -s` across tags for `map_swiss.go` and `map_noswiss.go`: exit 0 and exit 0 (identical bytes).
- Upstream raw equality (OBSERVED, `curl` http=200, exit 0, `local_match=yes` for all four):
  - `https://raw.githubusercontent.com/golang/go/go1.24.6/src/internal/abi/map_swiss.go` → `0e2fed…c383`
  - `https://raw.githubusercontent.com/golang/go/go1.24.6/src/internal/abi/map_noswiss.go` → `03db5a…7291`
  - `https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/map_swiss.go` → `0e2fed…c383`
  - `https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/map_noswiss.go` → `03db5a…7291`
  - `type.go` at both tags also matched local (`go1.24.6` `44ee18…a2a9`, `go1.25.0` `6f3e3d…603c`; http=200, match=yes). The local trees are the release bytes for these files.

## 2. Field lists with anchors (OBSERVED)

`map_swiss.go` and `map_noswiss.go` carry **no build tags** (grep for `//go:build`/`// +build` returned no lines, exit 1), so both struct declarations are present in every build of the package. Line numbers are identical in 1.24.6 and 1.25.0 (files are byte-identical).

`SwissMapType` — `A124/map_swiss.go:32-43` / `A125/map_swiss.go:32-43`:
- `:32` `type SwissMapType struct {`; `:33` embedded `Type`
- `:34` `Key *Type`; `:35` `Elem *Type`; `:36` `Group *Type`
- `:38` `Hasher func(unsafe.Pointer, uintptr) uintptr`
- `:39` `GroupSize uintptr`; `:40` `SlotSize uintptr`; `:41` `ElemOff uintptr`
- `:42` `Flags uint32`; `:43` `}`

`OldMapType` — `A124/map_noswiss.go:25-36` / `A125/map_noswiss.go:25-36`:
- `:25` `type OldMapType struct {`; `:26` embedded `Type`
- `:27` `Key *Type`; `:28` `Elem *Type`; `:29` `Bucket *Type`
- `:31` `Hasher func(unsafe.Pointer, uintptr) uintptr`
- `:32` `KeySize uint8`; `:33` `ValueSize uint8`; `:34` `BucketSize uint16`
- `:35` `Flags uint32`; `:36` `}`

`Type` header — `A124/type.go:20-45` / `A125/type.go:20-45` (field block identical in both trees):
`Size_ uintptr` 21, `PtrBytes uintptr` 22, `Hash uint32` 23, `TFlag` 24, `Align_ uint8` 25, `FieldAlign_ uint8` 26, `Kind_ Kind` 27, `Equal func(...)` 30, `GCData *byte` 42, `Str NameOff` 43, `PtrToThis TypeOff` 44. Widths: `Kind uint8` (`type.go:49`), `TFlag uint8` (`:89`), `NameOff int32` (`:131`), `TypeOff int32` (`:134`).

## 3. Layout table (OBSERVED by compiling the real files)

Measured with each version's own toolchain on the copied real source files (method and receipts in §8), amd64:

`SwissMapType` (112 bytes): `Type` 0, `Key` 48, `Elem` 56, `Group` 64, `Hasher` 72, `GroupSize` 80, `SlotSize` 88, `ElemOff` 96, `Flags` 104 (+4 pad).
`OldMapType` (88 bytes): `Type` 0, `Key` 48, `Elem` 56, `Bucket` 64, `Hasher` 72, `KeySize` 80, `ValueSize` 81, `BucketSize` 82, `Flags` 84.
`Type` = 48, align 8; individual `Type` member offsets (0, 8, 16, 20, 21, 22, 23, 24, 32, 40, 44) are **derived** from the source widths at `A125/type.go:20-45`, not separately measured.

`Hasher` occupies 8 bytes (a func value is one pointer), which is why `GroupSize` starts at 80 in both structs.

## 4. Cross-version difference (OBSERVED)

`diff A124/type.go A125/type.go` exits 1 with exactly two hunks, neither in the `Type` field list:
- `190,194c190`: `TypeOf[T]` implementation rewritten to `return (*PtrType)(unsafe.Pointer(TypeOf((*T)(nil)))).Elem` (1.25.0), replacing the 1.24.6 nil/interface fallback.
- `490c486`: comment `// funcType represents…` → `// FuncType represents…`.

`map_swiss.go` / `map_noswiss.go` have zero differences. Therefore "Go 1.25 changed the map type layout" is false for 1.24.6→1.25.0; any layout split observed in carriers must come from the experiment gate (§5), not the version.

## 5. Which descriptor a carrier actually carries (OBSERVED anchors)

- Baseline experiment: `SwissMap: true` at `/home/vgpnk/.local/opt/go-1.24.6/src/internal/buildcfg/exp.go:81` and `/home/vgpnk/.local/opt/go-1.25.0/src/internal/buildcfg/exp.go:85`; flag doc `SwissMap bool` at `/home/vgpnk/.local/opt/go-1.24.6/src/internal/goexperiment/flags.go:120` and `/home/vgpnk/.local/opt/go-1.25.0/src/internal/goexperiment/flags.go:116`, described as "SwissMap enables the SwissTable-based map implementation."
- `go env GOEXPERIMENT` prints empty for both toolchains (exit 0), i.e. default flags, so `SwissMap` is on unless `noswissmap` is passed at build time.
- Compiler descriptor choice: `R124/reflect.go:772-776` and `R125/reflect.go:776-780` — `if buildcfg.Experiment.SwissMap { rt = rttype.SwissMapType } else { rt = rttype.OldMapType }` (assignment lines 773/775 and 777/779).
- Writer dispatch: `R124/reflect.go:876-880` (`writeSwissMapType` at `:877`, `writeOldMapType` at `:879`); `R125/reflect.go:880-884` (`:881`, `:883`).
- Compiler layout source: `/home/vgpnk/.local/opt/go-1.25.0/src/cmd/compile/internal/rttype/rttype.go:58-59` builds `rttype.OldMapType`/`rttype.SwissMapType` from `reflect.TypeOf(abi.OldMapType{})` / `reflect.TypeOf(abi.SwissMapType{})`, i.e. the compiler sizes the emitted descriptor from these exact structs.
- Runtime alias: `RT125/map_swiss.go:5` `//go:build goexperiment.swissmap`, `:22` `type maptype = abi.SwissMapType`; `RT125/map_noswiss.go:5` `//go:build !goexperiment.swissmap`; the mirror aliases inside the ABI package are `A125/map_select_swiss.go:5,22` (`type mapType = SwissMapType`) and `A125/map_select_noswiss.go:5,10` (`type mapType = OldMapType`). `RT125/type.go:609-614` selects `(*abi.SwissMapType)` vs `(*abi.OldMapType)` on the same gate.
- Flag semantics differ between the two structs (OBSERVED): Swiss constants are `1 << iota` in the order `NeedKeyUpdate=1, HashMightPanic=2, IndirectKey=4, IndirectElem=8` (`A125/map_swiss.go:47-50`; accessors `:54,57,60,63`). Old accessors are literal `Flags&1` indirect key, `&2` indirect elem, `&4` reflexive key, `&8` need key update, `&16` hash might panic (`A125/map_noswiss.go:41,44,47,50,53`). The same bit position means different things in the two layouts (e.g. bit 3: Swiss = indirect elem, Old = need key update).

## 6. Derived misread arithmetic (INFERENCE — for C3, not observed in Ghidra)

Starting from the measured offsets only:

- Descriptor size delta: 112 − 88 = **24 bytes**. `reflectdata/reflect.go` computes `B := rt.Size()` and places the uncommon record at `B` when `extra` is true (`R125/reflect.go:789-793`; `extra := t.Sym() != nil || len(methods(t)) != 0` at `R125/reflect.go:754`; same shape at `R124/reflect.go:785-789,750`). A reader that assumes the 88-byte Old size on a Swiss descriptor therefore locates uncommon/method data 24 bytes early — at `SlotSize`, inside the descriptor tail.
- Field overlay if Old names are applied to a Swiss descriptor: `Key`/`Elem`/`Hasher` line up (48/56/72); `Bucket` at 64 would read the Swiss `Group` pointer; `KeySize` 80 / `ValueSize` 81 / `BucketSize` 82 would read bytes of `GroupSize`; `Flags` at 84 would read the high 4 bytes of `GroupSize`, not the real flags at 104 (a 20-byte miss). All of that is arithmetic from §3, not a Ghidra observation.
- Even at the correct offset 104, applying the Old bit meanings (§5) would invert several flags: indirect-key is bit 2 in Swiss vs bit 0 in Old; need-key-update is bit 0 in Swiss vs bit 3 in Old.

The C3 carrier pair decides whether this mechanism is what aether's log records; this report does not claim any carrier outcome.

## 7. SOURCES row draft (code kind)

ID note: two w1 drafts already claim `S034` — `DraftAbiRow.md` (go1.25.0 `internal/abi`, provisional S034) and `DraftGoNotesRow.md` (Go 1.24 release notes, provisional S034). They collide. Recommendation for the L1: register the release-notes row as `S034`, register **one** map-layout row as `S035`, and let this row subsume `DraftAbiRow.md` (same artifacts, but here covering both tags, upstream-verified, compiled from the real files, with the emit gate). Do not register both map rows. The id below is provisional.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S035 (provisional) | Go 1.24.6 and Go 1.25.0 `internal/abi` map type descriptors — `/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/` and `/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/` files `map_swiss.go`, `map_noswiss.go`, `map_select_swiss.go`, `map_select_noswiss.go`, `type.go`; raw `https://raw.githubusercontent.com/golang/go/go1.24.6/src/internal/abi/` and `https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/` | code | A | The go1.24.6 and go1.25.0 `SwissMapType` and `OldMapType` struct definitions and their compiled amd64 layout, plus the build-experiment alias that selects one; not Ghidra's reader, not Go 1.26, not 32-bit targets, not carrier behavior | Both tags: `map_swiss.go` sha256 `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383` and `map_noswiss.go` `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`, byte-identical across tags (`cmp` exit 0) and equal to the raw tag bytes (`curl` http=200); `type.go` 1.24.6 `44ee183a5a3567f6c1e3cc7ca813cbaabcb3834516442ce447ecb5631aa5a2a9`, 1.25.0 `6f3e3d720b4ba23750593d77dcc8e844fdfa18581a17e045e21b68c7f6cc603c`; `map_swiss.go:32-43`, `map_noswiss.go:25-36`, `type.go:20-45`; compiled amd64 `Type` 48, `SwissMapType` 112 with `Flags` at 104, `OldMapType` 88 with `Flags` at 84 | Gives the amd64 byte layout and size of both map descriptors from the release source: Swiss is 112 bytes with `Flags` at 104, Old is 88 with `Flags` at 84, and the map files are byte-identical across 1.24.6 and 1.25.0, so which descriptor a binary carries follows the `SwissMap` build experiment rather than the 1.24 to 1.25 version step. | mined | 2026-10-20 | on-release | none yet; C3 `W18/tools/swiss-misread.py` and the round-18 knowledge entry cite it on integration |

## 8. Method and receipts (commands with exit codes)

Positive route: compile the **real** package sources as a non-internal copy (identical field declarations, no transcription), under each version's own toolchain, default and `noswissmap`:

```
$ for G in /home/vgpnk/.local/opt/go-1.24.6 /home/vgpnk/.local/opt/go-1.25.0; do
    d=$(mktemp -d); mkdir -p "$d/abi" "$d/internal/goarch"
    cp "$G"/src/internal/abi/*.go "$d/abi/"; rm -f "$d/abi"/*_test.go "$d/abi"/funcpc.go "$d/abi"/funcpc_gccgo.go
    cp "$G"/src/internal/goarch/*.go "$d/internal/goarch/"; rm -f "$d/internal/goarch"/*_test.go
    sed -i 's#"internal/goarch"#"probe/internal/goarch"#g' "$d/abi"/*.go "$d/internal/goarch"/*.go
    printf 'module probe\n\ngo 1.21\n' > "$d/go.mod"
    # main.go imports probe/abi and prints unsafe.Sizeof/Offsetof for Type, SwissMapType, OldMapType
    (cd "$d" && GOTOOLCHAIN=local "$G/bin/go" run .)
    (cd "$d" && GOTOOLCHAIN=local GOEXPERIMENT=noswissmap "$G/bin/go" run .)
  done
```
Output (all four runs identical, exit 0 each):
`Type=48 Swiss=112 align=8 Flags=104 Old=88 align=8 OldFlags=84`
`Swiss offs Key=48 Elem=56 Group=64 Hasher=72 GroupSize=80 SlotSize=88 ElemOff=96`
`Old offs Key=48 Elem=56 Bucket=64 Hasher=72 KeySize=80 ValueSize=81 BucketSize=82`

Literal receipts (all run from `/home/vgpnk/.local/opt` unless noted):

```
$ for v in 1.24.6 1.25.0; do for f in map_swiss.go map_noswiss.go type.go; do p=go-$v/src/internal/abi/$f; printf '%s  %s\n' "$(sha256sum "$p" | cut -d' ' -f1)" "$p"; done; done
  (six hashes as in §1)                                          exit=0
$ cmp -s go-1.24.6/src/internal/abi/map_swiss.go go-1.25.0/src/internal/abi/map_swiss.go; echo $?
  0
$ cmp -s go-1.24.6/src/internal/abi/map_noswiss.go go-1.25.0/src/internal/abi/map_noswiss.go; echo $?
  0
$ for v in 1.24.6 1.25.0; do for f in map_swiss.go map_noswiss.go; do
    url="https://raw.githubusercontent.com/golang/go/go$v/src/internal/abi/$f"
    code=$(curl -sS --max-time 25 -o "/tmp/$v-$f" -w '%{http_code}' "$url"); rc=$?
    printf '%s http=%s exit=%s sha=%s local_match=%s\n' "$url" "$code" "$rc" \
      "$(sha256sum /tmp/$v-$f | cut -d' ' -f1)" \
      "$([ "$(sha256sum /tmp/$v-$f | cut -d' ' -f1)" = "$(sha256sum go-$v/src/internal/abi/$f | cut -d' ' -f1)" ] && echo yes || echo no)"
  done; done
  (four lines; http=200 exit=0 local_match=yes)                  exit=0
$ for v in 1.24.6 1.25.0; do url="https://raw.githubusercontent.com/golang/go/go$v/src/internal/abi/type.go"; code=$(curl -sS --max-time 25 -o "/tmp/t-$v" -w '%{http_code}' "$url"); rc=$?; local=$(sha256sum "go-$v/src/internal/abi/type.go" | cut -d' ' -f1); remote=$(sha256sum "/tmp/t-$v" | cut -d' ' -f1); printf '%s http=%s curl_exit=%s match=%s\n' "$url" "$code" "$rc" "$([ "$local" = "$remote" ] && echo yes || echo no)"; done
  (two lines; http=200 curl_exit=0 match=yes)                    exit=0
$ grep -n '//go:build\|// +build' go-1.24.6/src/internal/abi/map_swiss.go go-1.24.6/src/internal/abi/map_noswiss.go go-1.25.0/src/internal/abi/map_swiss.go go-1.25.0/src/internal/abi/map_noswiss.go; echo $?
  (no output)                                                    exit=1
$ /home/vgpnk/.local/opt/go-1.24.6/bin/go version; /home/vgpnk/.local/opt/go-1.25.0/bin/go version
  go version go1.24.6 linux/amd64 ; go version go1.25.0 linux/amd64   exit=0, exit=0
$ /home/vgpnk/.local/opt/go-1.24.6/bin/go env GOEXPERIMENT; echo $?     (empty line) exit=0
$ /home/vgpnk/.local/opt/go-1.25.0/bin/go env GOEXPERIMENT; echo $?     (empty line) exit=0
$ diff go-1.24.6/src/internal/abi/type.go go-1.25.0/src/internal/abi/type.go | head -40; echo ${PIPESTATUS[0]}
  (hunks 190,194c190 and 490c486 only)                           exit=1
$ grep -n 'SwissMap' go-1.24.6/src/internal/buildcfg/exp.go go-1.25.0/src/internal/buildcfg/exp.go; echo $?
  go-1.24.6/.../exp.go:81:		SwissMap:         true,
  go-1.25.0/.../exp.go:85:		SwissMap:        true,        exit=0
$ grep -n 'SwissMapType\|OldMapType' go-1.25.0/src/cmd/compile/internal/reflectdata/reflect.go; echo $?
  777,779,881,883 (as quoted in §5)                              exit=0
$ grep -n 'Flags&' go-1.25.0/src/internal/abi/map_swiss.go go-1.25.0/src/internal/abi/map_noswiss.go; echo $?
  54,57,60,63 / 41,44,47,50,53                                   exit=0
$ grep -n 'type mapType\|go:build' go-1.25.0/src/internal/abi/map_select_swiss.go go-1.25.0/src/internal/abi/map_select_noswiss.go; echo $?
  :5 :22 / :5 :10                                                exit=0
$ readelf -S /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile | grep -c '\.debug_info'
  0 (grep exit 1: no match)
```

Negative routes (recorded so the method is auditable):
- `go run` importing `internal/abi` from a module: **exit 1**, `use of internal package internal/abi not allowed`. A direct authoritative import is unavailable outside GOROOT.
- `go test -overlay=… -run TestSizeProbe internal/abi` (overlay adding a `_test.go` inside the std package, no GOROOT write): **exit 1**, `imports testing from zz_probe_test.go / imports internal/race from testing.go / imports internal/abi from norace.go: import cycle not allowed in test`. `internal/abi` cannot host a `testing`-based test.
- Toolchain DWARF route: `readelf -S /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile | grep -c '\.debug_info'` → `0`; same for `bin/go` → `0` (`.symtab` count 1); `llvm-dwarfdump --name=SwissMapType compile` returned no DIE. Official toolchain binaries are DWARF-stripped, so no DWARF corroboration was possible.

## 9. Limits and remaining unknowns

- The amd64 numbers are compiled from the release source by the release toolchains; the copy step renames the package (`probe/abi`) and rewrites only `internal/goarch`. Layout does not depend on the import path, and the field lists are the real files byte-for-byte (hashes above).
- `Type` member offsets in §3 are derived from declared widths, not individually measured; only `Type` size/align, and every `SwissMapType`/`OldMapType` offset, are measured.
- Not established here: Ghidra 12.1.4's `GoMapType` size/offset assumptions (sibling scout and C3 own that), any carrier's actual descriptor kind, 32-bit or arm64 layouts (the sibling `DraftAbiRow` reports 386 sizes; I did not reproduce them), Go 1.26/1.27 behavior, and patch releases other than 1.24.6/1.25.0.
- The §6 overlay arithmetic is a prediction for C3's emulator, not an observation of a misparse.

## 10. Tools / installs

No installs or upgrades; no `pacman`, `uv`, `npm`, or `cargo` invocation. Used existing go1.24.6/go1.25.0 toolchains only as compilers of the probe copies under `/tmp` (removed), existing `curl`, `sha256sum`, `cmp`, `diff`, `readelf`, `llvm-dwarfdump`, `grep`, `sed`. Network: only the six `raw.githubusercontent.com/golang/go/<tag>/…` fetches named in §1. Lane: read-only; this file is the only write.
