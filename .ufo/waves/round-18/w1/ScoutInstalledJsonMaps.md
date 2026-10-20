# Scout — installed Ghidra Go snapshot: `runtime.maptype`, map-struct layouts, 1.24/1.25 patch diffs, r16 selection

Seat: `KaidokuR18.ScoutInstalledJsonMaps` · Round 18 (hyaku phase 2) · 2026-10-20.
Axes: **calibration** (are the installed bytes being read the way Ghidra reads them?), **operability** (can
the L1 reproduce each number), **depth** (does this settle what a carrier's map type is or is not).

Read-only. No REA/Ghidra run, no carrier execution, no git/jj write, no tool installed (all commands used
pre-installed `jq`, `python3`, `unzip`, `sha256sum`). Only this file was written.

`G` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`
`SRC` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (Ghidra 12.1.4 sources)
`LANE` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

Both snapshot JSONs are a **single line with no trailing newline** (`wc -l` = 0; `grep -n` reports `1:`);
JSON citations below are therefore `file:1 → <JSON pointer>`.

## Answer (all observation)

| Question | Answer |
|---|---|
| `runtime.maptype` alias target, 1.24.0 | `internal/abi.OldMapType`, Position `$GOROOT/runtime/map_noswiss.go:67:6` |
| `runtime.maptype` alias target, 1.25.0 | `internal/abi.OldMapType`, Position `$GOROOT/runtime/map_noswiss.go:68:6` |
| `OldMapType` fields / size | 9 fields, `Type,Key,Elem,Bucket,Hasher,KeySize,ValueSize,BucketSize,Flags`; **88 B (0x58)** on ptr=8, **56 B (0x38)** on ptr=4 |
| `SwissMapType` fields / size | 9 fields, `Type,Key,Elem,Group,Hasher,GroupSize,SlotSize,ElemOff,Flags`; **112 B (0x70)** on ptr=8, **64 B (0x40)** on ptr=4 |
| Patch diffs, 1.24 | `go1.24.1` … `go1.24.6` — exactly 6, nothing for 1.24.0 |
| Patch diffs, 1.25 | **none** — 0 files matching `1.25` in `patchverdiffs/` |
| r16 selection, 1.24.6 | `exact_diff`: base `go1.24.0.json` + `patchverdiffs/go1.24.6.json.diff` (patch 6), exit 0 |
| r16 selection, 1.25.0 | `base_only`: `go1.25.0.json` (patch 0 probes no diff dir), exit 0 |

The alias is the **noswiss** flavour in both snapshots. Both structs carry identical definitions in 1.24.0
and 1.25.0 (canonical-JSON equality, see §2.4); only the alias's `Position` line moved 67→68.

## 1. `runtime.maptype` alias

`G/go1.24.0.json:1 → /all/Types/runtime.maptype` (verbatim):

```json
{"Kind":"alias","Target":"internal/abi.OldMapType","Position":"$GOROOT/runtime/map_noswiss.go:67:6"}
```

`G/go1.25.0.json:1 → /all/Types/runtime.maptype` (verbatim):

```json
{"Kind":"alias","Target":"internal/abi.OldMapType","Position":"$GOROOT/runtime/map_noswiss.go:68:6"}
```

Related observed facts, both files:

- `internal/abi.mapType` is a second alias to the same target:
  `{"Kind":"alias","Target":"internal/abi.OldMapType","Position":"$GOROOT/internal/abi/map_select_noswiss.go:10:6"}`
  in both snapshots.
- **No alias anywhere in either snapshot targets `internal/abi.SwissMapType`.** Enumerating every
  `Kind:"alias"` entry whose `Target` is one of the two structs returns exactly the two rows above
  (1.24.0 and 1.25.0 identical). Keys `runtime.swissmap` / `runtime.swissMap` do not exist.
- `internal/abi.SwissMapType` *is* defined, and `internal/runtime/maps.*` functions take
  `*internal/abi.SwissMapType` in both snapshots; the `runtime.*` map functions take `*runtime.maptype`
  (e.g. `runtime.makemap` params `["*runtime.maptype","int","*runtime.hmap"]`). So the snapshot models the
  noswiss runtime name and the swiss maps package side by side.
- Inference (not encoded in the JSON): `map_noswiss.go` is the `!goexperiment.swissmap` source file, so the
  alias is the opt-out flavour of `runtime.mapType`; a default-swiss carrier's runtime source uses a
  different alias name that this snapshot does not define. The JSON itself only records Kind/Target/Position.

## 2. `internal/abi.OldMapType` and `internal/abi.SwissMapType`

### 2.1 Verbatim definitions (identical in both files)

`G/go1.24.0.json:1 → /all/Types/internal/abi.OldMapType`:

```json
{"Kind":"struct","Fields":[{"Name":"Type","DataType":"internal/abi.Type"},{"Name":"Key","DataType":"*internal/abi.Type"},{"Name":"Elem","DataType":"*internal/abi.Type"},{"Name":"Bucket","DataType":"*internal/abi.Type"},{"Name":"Hasher","DataType":"func(unsafe.Pointer, uintptr) uintptr"},{"Name":"KeySize","DataType":"uint8"},{"Name":"ValueSize","DataType":"uint8"},{"Name":"BucketSize","DataType":"uint16"},{"Name":"Flags","DataType":"uint32"}],"Position":"$GOROOT/internal/abi/map_noswiss.go:25:6"}
```

`G/go1.24.0.json:1 → /all/Types/internal/abi.SwissMapType`:

```json
{"Kind":"struct","Fields":[{"Name":"Type","DataType":"internal/abi.Type"},{"Name":"Key","DataType":"*internal/abi.Type"},{"Name":"Elem","DataType":"*internal/abi.Type"},{"Name":"Group","DataType":"*internal/abi.Type"},{"Name":"Hasher","DataType":"func(unsafe.Pointer, uintptr) uintptr"},{"Name":"GroupSize","DataType":"uintptr"},{"Name":"SlotSize","DataType":"uintptr"},{"Name":"ElemOff","DataType":"uintptr"},{"Name":"Flags","DataType":"uint32"}],"Position":"$GOROOT/internal/abi/map_swiss.go:32:6"}
```

Both are members of the **`all`** bucket only. Presence matrix over all 27 top-level buckets (1.24.0 and
1.25.0 identical): `runtime.maptype`, `internal/abi.OldMapType`, `internal/abi.SwissMapType`,
`internal/abi.mapType`, `internal/abi.Type` → `['all']`; absent from `linux-amd64`, `linux`, `unix`, `amd64`.
Inference: no arch bucket overrides them, so `GoApiSnapshot.getTypeDef`'s first-match-in-search-order rule
(`SRC:…/rtti/GoApiSnapshot.java:524-532`) is unambiguous for these names.

### 2.2 The JSON has no size/offset field — size is computed

Enumerated key set across all 3,706 entries of `/all/Types` in `go1.24.0.json` (counts):
`Fields` 2283, `Kind` 3706, `Params` 305, `Position` 3139, `Results` 305, `Target` 698, `TypeParams` 19.
There is **no** `Size`, `Length`, `Offset` or `Align` key. The Java model matches:
`GoApiSnapshot.GoTypeDef` (`SRC:…/rtti/GoApiSnapshot.java:353-368`) is an empty base whose
`getDataTypeSize` throws, and a grep of that file for `getDataTypeSize` returns exactly **one** declaration
(`:365`, the throwing base — no subtype overrides it), so the sole size path in this build is
`GoTypeManager.getDataTypeLength`. Subclasses: `GoStructDef` is `Fields`+`TypeParams` (`:370-388`);
`GoArch` is `Funcs`+`Types` (`:445-448`); `GoTypeDefDeserializer` maps
`"struct"/"iface"/"basic"/"alias"/"funcdef"` (`:450-466`).

Ghidra therefore computes length/alignment with `GoTypeManager.getDataTypeLength`
(`SRC:…/rtti/GoTypeManager.java:1030-1128`):

- struct: fields in declaration order, each at `getUnsignedAlignedValue(len, field.align)`, `align = max`,
  final length rounded up to `align` — `:1115-1127`;
- `Func` → `ptrSize` — `:1046`; pointer `*T` → `ptrSize` — `:1068`; `map[…]`/`chan …` → `ptrSize` — `:1080`;
- alias → its target — `:1103-1105`; funcdef type → `ptrSize` — `:1107-1109`; iface → `2*ptrSize` — `:1111-1113`;
- `ptrSize = goBinary.getPtrSize()` — `:85` (target-dependent, not fixed by the JSON).

The `Hasher` field resolves because the snapshots also register the signature as a type:
`/all/Types["func(unsafe.Pointer, uintptr) uintptr"]` = `{"Kind":"funcdef","Params":[{"DataType":"unsafe.Pointer"},{"DataType":"uintptr"}],"Results":[{"DataType":"uintptr"}]}`
(no `Position`), reached via `getDataTypeLength(String)` → `getTypeDef` → `GoFuncTypeDef` (`:1087-1094`).

Supporting type: `/all/Types/internal/abi.Type` = `Size_ uintptr, PtrBytes uintptr, Hash uint32,
TFlag internal/abi.TFlag, Align_ uint8, FieldAlign_ uint8, Kind_ internal/abi.Kind, Equal
func(unsafe.Pointer, unsafe.Pointer) bool, GCData *byte, Str internal/abi.NameOff, PtrToThis
internal/abi.TypeOff`, Position `$GOROOT/internal/abi/type.go:20:6`; `TFlag`/`Kind` are aliases of `uint8`
and `NameOff`/`TypeOff` aliases of `int32` (same pointer). → **48 B (0x30)** at ptr=8, 32 B at ptr=4.

### 2.3 Layout (arithmetic shown, ptr=8)

`internal/abi.OldMapType` — 88 B (0x58), align 8:

| off | field | type | size |
|---|---|---|---|
| 0x00 | `Type` | `internal/abi.Type` | 48 |
| 0x30 | `Key` | `*internal/abi.Type` | 8 |
| 0x38 | `Elem` | `*internal/abi.Type` | 8 |
| 0x40 | `Bucket` | `*internal/abi.Type` | 8 |
| 0x48 | `Hasher` | `func(unsafe.Pointer, uintptr) uintptr` | 8 |
| 0x50 | `KeySize` | `uint8` | 1 |
| 0x51 | `ValueSize` | `uint8` | 1 |
| 0x52 | `BucketSize` | `uint16` | 2 |
| 0x54 | `Flags` | `uint32` | 4 |
| 0x58 | *end / size* | | **88** |

`internal/abi.SwissMapType` — 112 B (0x70), align 8:

| off | field | type | size |
|---|---|---|---|
| 0x00 | `Type` | `internal/abi.Type` | 48 |
| 0x30 | `Key` | `*internal/abi.Type` | 8 |
| 0x38 | `Elem` | `*internal/abi.Type` | 8 |
| 0x40 | `Group` | `*internal/abi.Type` | 8 |
| 0x48 | `Hasher` | `func(unsafe.Pointer, uintptr) uintptr` | 8 |
| 0x50 | `GroupSize` | `uintptr` | 8 |
| 0x58 | `SlotSize` | `uintptr` | 8 |
| 0x60 | `ElemOff` | `uintptr` | 8 |
| 0x68 | `Flags` | `uint32` | 4 |
| 0x70 | *end (0x6C rounded to align 8)* | | **112** |

ptr=4 (`386`, `arm`): `internal/abi.Type` 32; `OldMapType` **56 B (0x38)** (`Key` 0x20, `Elem` 0x24,
`Bucket` 0x28, `Hasher` 0x2C, `KeySize` 0x30, `ValueSize` 0x31, `BucketSize` 0x32, `Flags` 0x34);
`SwissMapType` **64 B (0x40)** (`Group` 0x28, `Hasher` 0x2C, `GroupSize` 0x30, `SlotSize` 0x34, `ElemOff`
0x38, `Flags` 0x3C).

These numbers are **derived** (JSON fields + Ghidra's own layout function above), not read from a size key.
No Go toolchain is installed on this host (`which go` empty; `/usr/lib/go/src/internal/abi/*` absent), so a
compile-time `unsafe.Sizeof` cross-check was not run. The arithmetic is fully auditable from §2.3.

### 2.4 Definition stability across the two snapshots

Canonical-JSON (sorted keys, compact) equality of `/all/Types/<name>`:

```
internal/abi.Type          identical=True
internal/abi.OldMapType    identical=True
internal/abi.SwissMapType  identical=True
internal/abi.mapType       identical=True
runtime.maptype            identical=False   (Position 67:6 -> 68:6; Target identical)
```

## 3. Which patch diffs exist for 1.24 / 1.25

`G/patchverdiffs/` holds 123 files total, `go1.15`…`go1.24.6`; the newest entry is `go1.24.6.json.diff`
(`ls … | sort -V | tail`). For the two asked-for lines:

| file | bytes | hunks (`^@ \[`) | sha256 |
|---|---|---|---|
| `go1.24.1.json.diff` | 44137 | 331 | `28be359f82b588100502483d1ebb930d832a93c99dd0d1ba1185f48b69e0506a` |
| `go1.24.2.json.diff` | 54555 | 409 | `549086b4e61f890e1bce9799ab9aed037aff449b1a696f75efa32fb34274e951` |
| `go1.24.3.json.diff` | 90820 | 686 | `4bc5612aa900eb6ca504c2d08491bcd20afe5894ce0a870fd6ad524a36ed52fe` |
| `go1.24.4.json.diff` | 95067 | 716 | `90d4ec82468c7ce68c5685491b78ec78faabda8e6c06875938226e525aef907d` |
| `go1.24.5.json.diff` | 106091 | 800 | `5743f4335615fdc5aa8d7e3c2516a8223a3eb769ffd306b3344b79bef4ea7053` |
| `go1.24.6.json.diff` | 118810 | 897 | `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6` |
| **1.25.x** | — | — | **0 files** |

Format (observed, `G/patchverdiffs/go1.24.6.json.diff:1-3`): `@ <JSON-array path>` followed by context
lines (two-space prefix), `- ` old lines, `+ ` new lines. Paths reach depth 6
(e.g. `["all","Funcs","reflect.rangeNum","Params",0,"Name"]`).

**Cumulative from the 1.24.0 base** (observation): hunk counts rise monotonically 331→897, and the path set
of each diff is a subset of the next (`1.24.1 ⊆ 1.24.2 ⊆ … ⊆ 1.24.6`, all True). 862 of 863 `- ` values in
`go1.24.6.json.diff` equal the base value at that path; the one exception is explained in §3.2. This matches
`GoApiSnapshot.getApiSnapshotJsonFile` (`SRC:…/GoApiSnapshot.java:134-144`), which builds a derived provider
by applying the diff to `go<M.m.0>.json`, and `getPatchVerDiffFile` (`:148-166`), which probes downward from
the requested patch and warns on fallback.

### 3.1 Do the diffs touch the map types? No.

`grep -h -c` summed over all six 1.24 diffs, per pattern:

```
runtime\.maptype      0      OldMapType        0      SwissMapType     0
map_noswiss           0      map_swiss         0      internal/abi\.mapType  0
runtime\.hmap         0
```

Per-file `grep -c '"Types","<name>"'` for `internal/abi.OldMapType`, `internal/abi.SwissMapType`,
`runtime.maptype`, `internal/abi.mapType`, `runtime.hmap`, `internal/abi.Type` → `0` in every one of the six
files (grep exit 1 = no match, expected). Minimum path depth per diff is 3 (`[bucket,"Types"|"Funcs",name]`),
so no diff replaces a whole `["all","Types"]` object either (depth histogram of 1.24.6: `{3:47, 4:839, 5:7,
6:4}`).

**Consequence:** the effective merged snapshot for 1.24.6 (`go1.24.0.json` + `go1.24.6.json.diff`) defines
`runtime.maptype`, `OldMapType`, `SwissMapType` and `internal/abi.Type` exactly as §1/§2 — the diffs perturb
positions and signatures elsewhere, not these structs.

### 3.2 Patch semantics caution (inference, with anchors)

Hunks are an **ordered positional edit script against the partially patched document**, not path-wise
substitution into the base. Evidence: `G/patchverdiffs/go1.24.6.json.diff:1721-1723` inserts
`{"DataType":"*go/types.Var","Name":"origin"}` at `["all","Types","go/types.Var","Fields",1]`; the later hunk
`:1725-1727` reads `- "used"` / `+ "isParam"` at `Fields[4,"Name"]`, but base `go/types.Var` is
`[object, embedded, isField, used, origin]` so base index 4 is `"origin"` — `"used"` is the value at index 4
only *after* the insertion. Applying the hunks in file order reproduces that; applying them by path against
the base does not. (Cross-check: `go1.25.0.json` `go/types.Var` is `[object, origin, kind, embedded]`, a
different layout again, so the 1.25 base is not a usable proxy for the 1.24.6 patch result.)

## 4. r16 selection for 1.24.6 and 1.25.0

`LANE/.ufo/waves/round-16/selection.py` is a source-law preview of the Java above: base is always
`go<M>.<m>.0.json` (`selection.py:211`), diff = greatest present same-minor patch ≤ request
(`:240-261`), status `base_only` when none (`:274-280`); it never merges (`patch_applied` false).

### 4.1 `1.24.6` — command, output, exit

```sh
python3 .ufo/waves/round-16/selection.py \
  --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang \
  --request 1.24.6 --goos linux --goarch amd64
```

```json
{
  "requested": "1.24.6",
  "request_raw": "1.24.6",
  "goos": "linux",
  "goarch": "amd64",
  "status": "exact_diff",
  "base": {
    "path": "go1.24.0.json",
    "size": 10039962,
    "sha256": "aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571"
  },
  "selected_diff": {
    "path": "patchverdiffs/go1.24.6.json.diff",
    "size": 118810,
    "sha256": "e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6"
  },
  "selected_patch": 6,
  "arch_search_order": ["linux-amd64", "linux", "unix", "amd64", "all"],
  "base_matching_buckets": ["linux-amd64", "linux", "unix", "amd64", "all"],
  "base_matching_buckets_source": "unpatched_base_file",
  "patch_applied": false,
  "evidence_class": "source_model"
}
```

**exit 0.** Digests independently confirmed by `sha256sum G/go1.24.0.json` (`aab28c8f…c571`) and
`sha256sum G/patchverdiffs/go1.24.6.json.diff` (`e169e8dd…ded6`).

### 4.2 `1.25.0` — command, output, exit

```sh
python3 .ufo/waves/round-16/selection.py \
  --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang \
  --request 1.25.0 --goos linux --goarch amd64
```

```json
{
  "requested": "1.25.0",
  "request_raw": "1.25.0",
  "goos": "linux",
  "goarch": "amd64",
  "status": "base_only",
  "base": {
    "path": "go1.25.0.json",
    "size": 10081618,
    "sha256": "54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252"
  },
  "selected_diff": null,
  "selected_patch": 0,
  "arch_search_order": ["linux-amd64", "linux", "unix", "amd64", "all"],
  "base_matching_buckets": ["linux-amd64", "linux", "unix", "amd64", "all"],
  "base_matching_buckets_source": "unpatched_base_file",
  "patch_applied": false,
  "evidence_class": "source_model"
}
```

**exit 0.** `sha256sum G/go1.25.0.json` = `54d10162…6252`, matching.

### 4.3 Boundary probes (same script, read-only, exit 0 each)

| request | status | base | selected_diff | selected_patch |
|---|---|---|---|---|
| 1.24.9 | `fallback_diff` | `go1.24.0.json` | `patchverdiffs/go1.24.6.json.diff` | 6 |
| 1.25.3 | `base_only` | `go1.25.0.json` | `null` | 0 |

1.24.9 shows the "nearest present ≤ request" rule; 1.25.3 shows that the absence of any 1.25 diff makes a
later 1.25 patch resolve to the 1.25.0 base with **no diff file**. One divergence to keep straight: the Java
probe (`SRC:…/GoApiSnapshot.java:153-161`) decrements `patchVer` to `.0` and then, because
`patchVer.getPatch() != goVer.getPatch()`, emits the same `Msg.warn("Falling back from 1.25.3 to 1.25.0")`
that a real fallback gets — even though the cause is "no diffs exist", and `getApiSnapshotJsonFile` still ends
up base-only (`:128-131`). `selection.py` reports `base_only` (file selection correct, warning not modelled).

## 5. Calibration for the L1

1. **Base bytes vs merged bytes.** `selection.py` reports digests of the *stored* base file and explicitly
   does not merge (`patch_applied: false`). Java *does* merge for any patch > 0
   (`SRC:…/GoApiSnapshot.java:134-144`). For 1.24.6 the merged document differs from the base in 897 hunks,
   but not in any map-type entry (§3.1), so §2 holds for both.
2. **Size is derived, not stored.** If a row needs "size", cite it as computed by
   `GoTypeManager.getDataTypeLength` (§2.2) at `ptrSize` of the carrier — 88/112 for 64-bit, 56/64 for
   32-bit. A carrier's `ptrSize` (not the JSON) decides which applies.
3. **Alias scope.** `runtime.maptype → internal/abi.OldMapType` is the noswiss alias; the snapshot contains no
   alias to `SwissMapType`. Do not use it to claim what a default (swiss) build names its map type — the JSON
   is silent there. `internal/runtime/maps.*` signatures do reference `*internal/abi.SwissMapType` directly,
   which is the swiss-side evidence the snapshot does carry.
4. **Do not describe the 1.24 diffs as incremental.** Each is cumulative from `go1.24.0.json` (subset chain,
   monotone hunk counts). And do not patch them by path against the base (§3.2).
5. **`base_matching_buckets` is a base-only preview.** The script computes it on the raw base
   (`selection.py:266-272`, `:293-296`); the merged document could in principle add/remove buckets, and the
   script would not show it.

## 6. Commands run and exit codes

| # | command (exact, as run) | exit |
|---|---|---|
| 1 | `ls -la G/patchverdiffs \| grep -Ei '1\.2[45]'` | 0 |
| 2 | `ls G/patchverdiffs \| sort -V \| tail -40`; `… \| wc -l` (123); `… \| grep -c '1\.25'` | 0 / 0 / **1** (0 matches) |
| 3 | `sha256sum G/go1.24.0.json G/go1.25.0.json G/patchverdiffs/go1.24.6.json.diff` and `sha256sum G/patchverdiffs/go1.24.*.json.diff` | 0 |
| 4 | `jq -c '."all".Types["runtime.maptype"] // "ABSENT"' G/go1.24.0.json` (and the two structs, both files) | 0 |
| 5 | `jq -c '."linux-amd64".Types["runtime.maptype"] // "ABSENT"' …` (arch-bucket absence) | 0 |
| 6 | `jq -r '."all".Types[] \| keys[]' G/go1.24.0.json \| sort \| uniq -c` (schema key census) | 0 |
| 7 | `python3` heredoc: presence matrix across all buckets (§2.1) | 0 |
| 8 | `python3` heredoc: canonical-JSON equality of the five entries (§2.4) | 0 |
| 9 | `python3` heredoc: Go-layout computation (§2.3 tables, ptr=8 and ptr=4) | 0 |
| 10 | `python3` heredoc: diff hunk parse — counts, buckets, depth hist, subset chain, base-value match | 0 |
| 11 | `for pat in <7 patterns>; do grep -h -c "$pat" G/patchverdiffs/go1.24.*.json.diff \| awk '{s+=$1} END {print s+0}'; done` | 0 (all sums `0`) |
| 12 | `grep -c '"Types","internal/abi.OldMapType"\|"Types","internal/abi.SwissMapType"\|"Types","runtime.maptype"\|"Types","internal/abi.mapType"\|"Types","runtime.hmap"\|"Types","internal/abi.Type"' G/patchverdiffs/go1.24.*.json.diff` | **1**, printing `0` per file (expected no-match) |
| 13 | `unzip -p SRC '…/rtti/GoTypeManager.java' \| nl -ba \| sed -n '…'` (5 regions) | 0 |
| 14 | `unzip -p SRC '…/rtti/GoApiSnapshot.java' \| nl -ba \| sed -n '95,200p;205,330p;350,370p;443,475p'` | 0 |
| 15 | `unzip -p SRC '…/rtti/types/GoKind.java' \| nl -ba \| sed -n '1,140p'` | 0 |
| 16 | `python3 .ufo/waves/round-16/selection.py --root G --request <v> --goos linux --goarch amd64` for `1.24.6`, `1.25.0`, `1.24.9`, `1.25.3` | 0, 0, 0, 0 |
| 17 | `jq` precise params/results scan for the map-struct names (both files) | 0 |
| 18 | `wc -l G/go1.24.0.json G/go1.25.0.json` | 0, printing `0` `0` `0 total` |
| 19 | `unzip -p SRC '…/rtti/GoApiSnapshot.java' \| nl -ba \| grep -n 'getDataTypeSize'` | 0, one hit (line 365) |
| 20 | `jq -r '[(."all".Types\|length), …Kind histograms…] \| @tsv' G/go1.24.0.json` | 0, prints `3706 3706 2387 698 305 316` |

Reproduce §2 exactly (the script from #9):

```sh
cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang && python3 - <<'PY'
import json
WORD={'uintptr':None,'uint32':(4,4),'uint16':(2,2),'uint8':(1,1),'int32':(4,4),'int64':(8,8),'bool':(1,1)}
def size_of(dt,ptr,t):
    if dt in WORD: return (ptr,ptr) if WORD[dt] is None else WORD[dt]
    if dt.startswith('*') or dt.startswith('func('): return (ptr,ptr)
    if dt.startswith('['):
        n,rest=dt[1:].split(']',1); i,a=size_of(rest,ptr,t); return (int(n)*i,a)
    d=t[dt]
    if d['Kind']=='alias': return size_of(d['Target'],ptr,t)
    if d['Kind']=='struct':
        off=0; al=1
        for f in d['Fields']:
            s,a=size_of(f['DataType'],ptr,t); off+=(-off)%a; off+=s; al=max(al,a)
        return ((off+(-off)%al), al)
    if d['Kind']=='iface': return (2*ptr,ptr)
    if d['Kind']=='funcdef': return (ptr,ptr)
    raise SystemExit(d['Kind'])
for fn in ('go1.24.0.json','go1.25.0.json'):
    t=json.load(open(fn))['all']['Types']
    for ptr in (8,4):
        for n in ('internal/abi.Type','internal/abi.OldMapType','internal/abi.SwissMapType'):
            print(fn, 'ptr=%d'%ptr, n, 'size=%d align=%d'%size_of(n,ptr,t))
PY
```

## Remaining unknowns

- Whether Ghidra 12.1.4 actually emits these structs for a given 1.24.x/1.25.x carrier (import may skip a type
  it cannot resolve): not exercised — the L1's carrier analysis is the only path, and I did not run it.
- The history that produced the 1.24.1→1.24.6 hunks (e.g. why `go/types.Var` gained `isParam` at 1.24.6) is not
  in the installed data; only the edit script is.
- Whether the go-api-parser used a noswiss build of Go to emit these snapshots is not recorded in the JSON; the
  `map_noswiss.go` positions imply it (inference), and no manifest/metadata file in `G` states the build
  flavour.
