# SimplifyC3Tools — YAGNI review of C3 (swiss-misread + run-carriers)

Seat `KaidokuR18.SimplifyC3Tools`, author-side advisory, leaf. Read-only: this report is the only
file written; all byte work ran in `/tmp`. Baseline `B = 9011581d84527ba34c675f9cf912e54d2e72d470`
(`claims.json:4`). Axes: calibration (does the emulator's number mean what the claim says),
operability (can the runner be rerun and checked), depth (does a second authority add information).

Siblings were landing W18 tools and editing W17 tools while this ran; worktree anchors are as of the
reads below (12:37–12:45). Contract anchors are stable.

## Verdict

1. **Full moduledata parsing: no.** Four of the selected snapshot's 45 `runtime.moduledata` fields are
   load-bearing (`pcHeader`, `types`, `etypes`, `typelinks`). The snapshot JSON already carries every
   struct layout, so a generic JSON layout calculator replaces a hand-written 45-field parser.
2. **`typelinks` + r17 `buildinfo-probe.py`: no — insufficient twice over.**
   (a) The misread only bites map types carrying `TFlagUncommon`. aether has **0** such maps among its
   145 typelink map types and **7** among the types Ghidra *discovers* (152 total; 7 is the r17
   measured count, §2). A typelinks-only tool reports `uncommon_map_types: 0` for aether and fails the
   frozen calibration (`contract.md:119-120`).
   (b) `buildinfo-probe.py` emits Go version but **no `GOEXPERIMENT`** (no settings decode) and no
   addresses; both the Swiss/noswiss discriminator and the typelink base are missing.
3. **The EOF is two name hops from the misread field**, not one: misread `pkgpath` 40 →
   `GoName@types+40` → its `pkgpath` 0x780100 → `GoName@types+0x780100` → length 111,938,854. A
   one-hop emulator returns no EOF and would be "correct" but calibrate red.
4. **`run-carriers.sh`: a thin parameterization of the r17 runner is not viable** without editing a
   hash-pinned historical artifact. The landed standalone W18 script is the right shape; one selftest
   assertion is a no-op (defect below).

## 1. What Ghidra reads (observations from the installed sources)

- `GoType.getUncommonType()` reads `GoUncommonType` at `context.getStructureEnd()`, i.e. after the
  *mapped* structure: `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoType.java:144-147`.
- `GoMapType` binds `{"runtime.maptype","internal/abi.MapType","internal/abi.OldMapType"}`
  (`types/GoMapType.java:32-34`, fields `:37-62`).
- Uncommon is TFlag bit 0: `types/GoBaseType.java:100-101`, `types/GoTypeFlag.java:29`; kind is
  `Kind_ & 0x1f`: `types/GoKind.java:54,69-73`.
- Snapshot alias: `all.Types["runtime.maptype"]` = `{"Kind":"alias","Target":"internal/abi.OldMapType"}`
  in both `go1.24.0.json` and `go1.25.0.json`; `internal/abi.SwissMapType` exists as a separate struct.
  JSON-derived sizes: Type 48, OldMapType 88, SwissMapType 112, UncommonType 16.
- `GoUncommonType.getPkgPath` resolves `pkgpath` via `resolveNameOff` (`types/GoUncommonType.java:58`);
  methods are an artificial slice at `uncommon+moff` (`:73-82`).
- `GoName.readStructure` reads flags, LEB128 name, optional tag, optional `pkgPath`
  (`GoName.java:93-101`); `GoName.getPkgPath` resolves again (`:123-124`); `GoVarlenString` reads the
  LEB128 length then `readNextByteArray` (`GoVarlenString.java:68-71`); the EOF text is
  `MemoryByteProvider.java:311-312`.
- Discovery: `GoTypeManager.init` walks `module.getTypeList()` then `goType.discoverGoTypes`
  (`rtti/GoTypeManager.java:106-144`); base discovery reads uncommon methods and adds each method type
  (`types/GoType.java:328-341`); maps add key/elem/bucket (`types/GoMapType.java:121-138`); func
  params/results start at `getOffsetEndOfFullType()` (`types/GoFuncType.java:97-100`).
- `GoModuledata.getTypeList` maps typelink `int32` offsets onto the `types` base
  (`rtti/GoModuledata.java:398-405`); the module is validated against the `.typelink` section
  (`:246-259`); pcHeader discovery uses the `gopclntab` section name (`rtti/GoRttiMapper.java:203`,
  `:1116-1131`).

## 2. Measured minimal parse (aether; static byte reads only)

```
$ python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py /usr/bin/aether    # exit 0 (summary)
go_version "go1.25.14"; keys: bytes/endian/flags/format/found/header_offset/header_vaddr/
inline/limitations/modinfo_first_line/path/pointer_format/ptr_size/search_space/sha256
(no "settings" key; `grep -n 'settings' buildinfo-probe.py` exit 1, no match)
```

```
$ python3 -I -B /tmp/kr18_probe.py /usr/bin/aether                              # exit 0 (trimmed)
moduledata size 584 pcHeader@0 types@296 etypes@304 typelinks@352
.gopclntab 0x13b9580 3424712 .typelink 0x13b4c40 14956
pcHeader magic=0xfffffff1 minLC=1 ptrSize=8 textStart=0x408ee0
firstmoduledata 0x172e400 types=0x954020 etypes=0x13b4999
typelinks=(0x13b4c40,3739,3739)
typelinks 3739 first 271488 last 400832
Type=48 tflag@20 kind@23 str@40 | OldMapType=88 | SwissMapType=112 | UncommonType=16
map_types 145 uncommon_map_types 0
```

The four offsets come from the snapshot's own `runtime.moduledata` field list (45 fields, 1.25.0
layout), not from hardcoded per-version knowledge:

```
$ python3 -c 'import json; t=json.load(open("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json"))["all"]["Types"]; print(len(t["runtime.moduledata"]["Fields"]), t["runtime.maptype"])'   # exit 0
45 {'Kind': 'alias', 'Target': 'internal/abi.OldMapType', 'Position': '$GOROOT/runtime/map_noswiss.go:68:6'}
```

Culprits are outside typelinks; their parents are inside:

```
$ python3 -I -B /tmp/kr18_membership.py                                        # exit 0
0xa1c7a0 in_typelinks False offset 0xc8780
0xa229a0 in_typelinks False offset 0xce980
0xa350a0 in_typelinks False offset 0xe1080
parent 0x9ba560 in_typelinks True      # func type (params include 0xa1c7a0)
parent 0x9b9040 in_typelinks True
parent 0x9ff5e0 in_typelinks True      # ptr/slice elem edge
parent 0xa2e4e0 in_typelinks True
```

Two-hop chain reproduces the logged pair exactly
(`.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log:177`):

```
$ python3 -I -B /tmp/kr18_chain.py                                             # exit 0 (condensed)
0xa1c7a0: kind 21 tflag 7 SlotSize 40; Ghidra uncommon @0xa1c7f8;
  misread pkgpath 40 -> GoName@0x954048 {flags 0x6e, name_len 0, tag_len 1, pkgpath 0x780100}
  -> GoName@0x10d4120 {flags 0xf6, name_len 111938854} -> eof_read [17645861, 111938854]
same pair for 0xa229a0 and 0xa350a0
```

The 152/7 discovery count is the r17 retained measurement
(`.ufo/waves/round-17/w2/CriticAetherUnknown.md:60-64`); it is consistent with 145 typelink maps + 7
discovered, and with the log's `Found 6115 Go types` vs 3739 typelinks. I re-verified the three named
culprits against bytes, not by re-deriving the full closure (see Limits).

## 3. Answers

### 3.1 Full moduledata: no

- Only `pcHeader` (discovery/validation), `types`, `etypes`, `typelinks` are read. `data`, `ftab`,
  `findfunctab`, `itablinks`, `textsectmap`, `ptab`, `pluginpath`, `typemap`, … are not inputs to the
  map prediction. A hardcoded parser would need all 45 field definitions plus per-version field order
  (1.24.0 and 1.25.0 happen to agree; older majors do not — 1.15 has 35 fields, 1.18 has 41, 1.21 has
  45 in a different order; `GoModuledata.java:46-59` conditions fields on `presentWhen`); the JSON
  removes that entire class of error. Inference: hardcoding buys zero additional predictions.

### 3.2 typelinks + buildinfo-probe: no

- Observation: typelinks has 145 map-kind entries and **zero** with `TFlagUncommon`; the misread is
  unreachable from that set.
- Observation: the three aether culprits are discovered one edge beyond typelinks, through func
  parameter lists and element pointers. Ghidra's closure is not optional for this claim.
- Observation: `buildinfo-probe.py` decodes the module blob but returns only `modinfo_first_line`
  (`buildinfo-probe.py:417`); `GOEXPERIMENT` is in the bytes
  (`.ufo/waves/round-18/evidence/carrier-buildinfo.json`) but not in its output. The probe also
  exposes no address/type information.
- Therefore a tool built as "typelinks + buildinfo-probe" would emit `uncommon_map_types: 0` and
  `predicted_failure: false` for aether — a calibration failure that is *not* a size-arithmetic bug.

### 3.3 Minimal sufficient design (inference)

- ELF VMA→file + block extents: reuse `buildinfo-probe`'s `elf_parse`, `elf_data_reader`,
  `file_offset_of_vaddr` by file-path import (the pattern `predict.py:94-103` uses for `selection.py`);
  do not edit the pinned r17 file.
- Build info: version from the probe's output; `GOEXPERIMENT` by re-decoding the module blob with the
  probe's `decode_string` helpers (~15 lines), since the probe discards it.
- Bootstrap: `.gopclntab` section start → pcHeader; scan writable data for a qword equal to the
  pcHeader address; validate `typelinks.array == .typelink start` and `len == cap` (Ghidra's own check,
  `GoModuledata.java:246-259`); `len == section size/4` is available as a second, independent check.
- Read `types/etypes/typelinks` via JSON field offsets; seed the discovery queue with typelink
  addresses; expand with Ghidra's edges (map key/elem/group, ptr/slice/array/chan elem, func in/out,
  struct field types, interface method types, uncommon method `mtyp`), de-duplicating by address.
- Layouts: Ghidra bound = snapshot `runtime.maptype` alias → OldMapType (88); truth = SwissMapType
  (112) iff Go ≥ 1.24 and the `GOEXPERIMENT` setting lacks `noswissmap`, else OldMapType (88).
- For each discovered map with `TFlagUncommon`: `e = start + 88`; `pkgpath=int32@e`,
  `mcount=uint16@e+4`, `moff=uint32@e+8`; then recurse through `GoName` (flags, LEB128 name, optional
  tag, optional pkgpath → resolve) and stop at the first read whose `index+length` exceeds the
  containing block. Record `[index,length]`; `predicted_failure = any`.
- Markup order and the analyzer's abort point need not be modeled: the calibration asks containment
  (`contract.md:119`).
- Counts: report `map_types`/`uncommon_map_types` over the discovered set (aether 152/7), not
  typelinks (145/0); `misread_map_types` = maps whose Ghidra bound differs from the true layout *and*
  which carry uncommon (7 for aether, 0 for any noswiss carrier).

## 4. run-carriers: parameterize or copy?

### 4.1 The r17 script is pinned history

- 39 lines; `W` hardcoded at `round-17/run-carriers.sh:9`; tools resolved relative to cwd at
  `:25,33,34`; the prediction path is absolute at `:26` and cwd-relative at `:34`; the `pro-op` env
  special case at `:23`.
- `round-17/verification.json:1891-1895` pins it at
  `sha256 acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b`, size 2155. The current
  file matches:

```
$ sha256sum .ufo/waves/round-17/run-carriers.sh                                # exit 0
acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b
```

- The r17 knowledge's recheck recipe (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`)
  tells a reader to rerun exactly this path. Editing it would make a retained verification record and
  a documented rerun describe different bytes. That is a provenance/operability cost, not a style
  preference.

### 4.2 The landed W18 script is a specialization, not a copy of the r17 runner

- 181 lines (`run-carriers.sh`), `bash -n` exit 0. Env knobs `:20-23`, preflight `:132-138`, loop
  `:146-180`, explicit pins `:167`, selftest `:26-123`.
- The four knobs (`TOOLS_DIR`, `PREDICTIONS_DIR`, `SWISS_MISREAD`, `SELECTION_PY`) exist for the
  required dry-check against a fake tools dir (header `:7-11`; RunCarriers18 prompt). They cannot be
  defaults inside the r17 script without editing it.
- The duplicated part is the loop body (22 lines in r17 `:17-38`, 33 in W18 `:148-180`). A "thin
  parameterization" would need (a) `W`, `TOOLS`, `PRED` env knobs, (b) an extra-pin hook for
  `swiss-misread.py`, and (c) the selftest, all inside the r17 file or a third shared file: two
  artifacts touched to save the shared lines, plus the r17 pin breaks. **Keep the standalone.**

### 4.3 Defect in the landed runner (calibration)

`run-carriers.sh:106-108` asserts the mixed-run exit as:

```
"${envbase[@]}" bash "$0" > ... && fail "mixed-run exit (expected 1)"
[ $? = 1 ] || true
```

`[ $? = 1 ] || true` can never fail. If the child exits 2 (setup error), the `&&` does not fire,
`[ 2 = 1 ]` is false, and `|| true` swallows it; the case does not fail on the exit code and, if the
later per-run assertions hold, the selftest prints `CLEAN` despite the wrong wave exit. Fix: `rc=$?` on
the line after the invocation, then `[ "$rc" = 1 ] || fail "mixed-run exit $rc"`.
(Source observation; I did not execute the selftest — it belongs to the owner.)

Minor, not a defect: `run-carriers.sh:167` explicitly pins the carrier realpath and
`SELECTION_PY` (comment `:162-164`), but `carrier-run.py` already pins `[carrier(realpath), R16_SELECTION]` by default and
de-duplicates (`carrier-run.py:290,319-321`), so those two `--pin`s are exact duplicates and do not
change the receipt's pin set. Keep as documentation or drop both plus the `SELECTION_PY` knob; no
correctness impact. The script depends on `jq`; on this host `jq --version` reports `jaq 3.1.1`
(inherited from r17's `:30`), so do not assume a specific jq implementation.

## 5. Kept moves (deliberately not deleted)

- `W17/tools/log-extract.py` `eof_reads` (`:106` regex, `:162-171` extraction, `:282` output,
  `:472-497` selftest) and `W17/tools/compare.py` `analyzer_errors_empty`/`eof_reads` (`:197-211`) are
  the contract's in-place additive fixes; the W18 runner calls them under `W17/tools`, so there is no
  per-wave fork. `git status --porcelain` shows both modified (concurrent owner).
- The W18 runner's env knobs and selftest are called by its dry-check and the contract's selftest rule;
  keep.
- Carrier list: the 12 synthetic + 2 calibration rows match the wave-1 amendment
  (`contract.md:150-151`) and `/home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS` (12 lines);
  the tsv additionally carries `real-kimi-webbridge`, which is not in that amendment.

## 6. Limits

- All byte claims are static file reads; no REA, no Ghidra, no carrier execution. Scratch scripts were
  `/tmp/kr18_probe.py` (ELF + snapshot layout + bootstrap) and `/tmp/kr18_chain.py` (two-hop name
  chain); both are ephemeral and not deliverables.
- The 152/7 count is the r17 retained measurement (`CriticAetherUnknown.md:60-64`), corroborated here
  by 145/0 typelinks, the non-membership of the three named culprits, and the exact pair. A full
  closure re-count was attempted and discarded (my seed filter accepted false addresses); do not cite
  it as a measurement.
- Concurrent siblings were writing W18 tools and editing W17 tools during this review; worktree
  anchors can move, contract/B anchors cannot.
- No tool installs or upgrades were made.
