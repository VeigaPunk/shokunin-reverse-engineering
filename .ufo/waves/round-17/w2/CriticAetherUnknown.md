# CriticAetherUnknown — round 17 wave 2 (FALSIFY)

Target: how round 17 handles the unpredicted aether `GolangSymbolAnalyzer` failure
(`runs/pro-aether/`), at lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`.
Axes: calibration, depth. Method: static reading only. I read the retained log, the
Ghidra 12.1.4 `Base-src.zip` source, the installed Go typeinfo JSON, and the carrier
bytes of `/usr/bin/aether` (Python `-B`, read-only). I did not run REA or Ghidra, and I
did not execute any carrier. Installs: none. Scratch scripts are in `/tmp/kr17-cau/`
(`probe.py`, `probe2.py`, `fullscan.py`, `maps.py`, `maps2.py`).

## Verdict

Writing UNKNOWN was honest (nothing in the round was false). It is also
**under-calibrated**. The retained evidence supports one source-consistent mechanism. I
found exactly one such mechanism, and it does not involve the 1.25.14→1.25.0 patch
fallback.

Ghidra 12.1.4 binds Go map types to the **pre-Swiss `internal/abi.OldMapType`** layout,
which is 0x58 bytes. aether (go1.25.14) uses the Swiss layout, which is 0x70 bytes. For
`map[string][]string` named types, Ghidra therefore reads the UncommonType at +0x58. The
"pkgPath nameOff" it reads there is really `SlotSize` = 40 (0x28). Each later link was
recovered from the file bytes and ends at the logged `EOFException` values exactly.

This is static evidence plus source. It is not a Ghidra replay, so it should be labelled
**INFERENCE (strong)**, not OBSERVATION.

## Premise correction (applies to the assignment, not to the artifacts)

- `17645861, 111938854` are **index and length**, not two offsets.
  `MemoryByteProvider.ensureBounds` formats the message as
  `"Unable to read past EOF: %s, %d".formatted(index, length)`
  (`Base-src.zip:ghidra/app/util/bin/MemoryByteProvider.java:309-313`).
- File size does not set the bound. The Go mapper's provider is
  `new MemoryByteProvider(program.getMemory(), imageBase.getAddressSpace())`
  (`structmapping/DataTypeMapper.java:511-513`). Its base is `ram:0`, so the index is a
  virtual address, and `maxOffset` is the highest mapped `ram` address, 0x18006ef. That
  is the end of the `EXTERNAL` block in `runs/pro-aether/analyze.json` `segments`.
  - Measured: index 0x10d4125 lies in `.rodata` (0x954000–0x13b4c40).
  - The remaining bytes are 7,521,739. The requested length is 111,938,854.
  - The file size is 20,694,888, which is irrelevant here.
- aether is **not PIE**. `readelf -h /usr/bin/aether` shows `Type: EXEC`,
  `Entry point address: 0x408df0`. It is dynamically linked: there is an `INTERP` header
  and `go version -m` reports `CGO_ENABLED=1` and `-buildmode=exe`. Neither fact plays a
  part in the mechanism. No round artifact claims PIE (`grep -i '\bPIE\b'` over the
  knowledge entry, the lesson and the w1 drafts finds nothing).
- Carrier identity: `sha256sum /usr/bin/aether` gives
  `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e`. This equals
  `analyze.json` `subject.digest`. `pacman -Qo` reports `aether 4.32.0-2`.

## The reconstructed chain (each link checked against bytes or source)

The full stack is in `runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log:97-198`
(sha256 `f39c3293…f0b4ed`, which matches `observation.json` `log_sha256`).

| # | Link | Evidence |
|---|---|---|
| 0 | Interface method → func type → param/result list | Stack: `GoInterfaceType.additionalMarkup` → `GoSlice.markupArrayElements` → getter (non-collection) → getter (collection, `log:113` = `MarkupSession.java:105` Collection branch) → getter → getter → field MarkupReference. Only `GoIMethod.getType` → `GoFuncType.getParamTypes` (`types/GoFuncType.java:106-111`) fits the collection hop. The full `@Markup` getter list is from `grep -rn -A2 '@Markup$'`. |
| 1 | S2 = map type → `GoType.getUncommonType()` reads at `getStructureEnd()` | `types/GoType.java:143-149`. `GoMapType` maps `{"runtime.maptype","internal/abi.MapType","internal/abi.OldMapType"}` (`types/GoMapType.java:27-29`). It has no SwissMapType name. |
| 2 | Bootstrap binds `runtime.maptype` to OldMapType (88 B = 0x58) | `typeinfo/golang/go1.25.0.json` `all.Types["runtime.maptype"]` = `{"Kind":"alias","Target":"internal/abi.OldMapType","Position":"$GOROOT/runtime/map_noswiss.go:68:6"}`. go1.24.0 is the same (`map_noswiss.go:67`). Bootstrap succeeded with 6115 types. `GoMapType` has non-optional fields `bucket`/`keysize`/`ValueSize`/`bucketsize`, which only the old layout has. A missing field throws (`structmapping/StructureMappingInfo.java:316-322`). |
| 3 | aether uses the **Swiss** layout (0x70) | `python -B /tmp/kr17-cau/maps.py`: 152 map types, 7 with uncommon. For each, the u32 at +0x70 resolves to the correct package: `net/textproto`, `net/url`, `net/http`, `github.com/godbus/dbus/v5`, `go.shape`. +0x58 is `SlotSize`. The file has 97 `internal/runtime/maps.` strings. |
| 4 | Misread nameOff = 0x28 for exactly 3 types | `*textproto.MIMEHeader`@0xa1c7a0, `*url.Values`@0xa229a0, `*http.Header`@0xa350a0: `SlotSize 40 u32@+0x58 0x28`. All three are `map[string][]string` (16+24). |
| 5 | S4 = GoName at types+0x28 = 0x954048 | moduledata@0x172e400: `types`=0x954020, `etypes`=0x13b4999. 0x954048 is the **last byte** of the real name `00 01 6e` ("n") at 0x954046. Read as a GoName it gives flags 0x6e (HAS_TAG\|HAS_PKGPATH\|EMBEDDED + junk bits), name length 0, tag "a", and pkgPath bytes `00 01 78 00` = nameOff **0x780100**. |
| 6 | S5 = GoName at 0x954020+0x780100 = 0x10d4120 | flags 0xf6, followed by a 4-byte LEB128 that decodes to **111938854** (0x6ac0d26). The string bytes start at 0x10d4125 = **17645861**. `GoName.java:95` is the name read (not the tag), and `GoVarlenString.java:71` is `readNextByteArray`. |
| 7 | 0x10d4120 is inside an embedded JPEG | A Go string header at 0x13982b8 = {0x10b91e0, 2289954}. Magic `ffd8ffe0`. The target is 110,400 bytes into the blob, and the blob ends at 0x12e8302 (`gofunc` = 0x12e8308). Entropy is about 7.7–7.8 bits/byte. |

Uniqueness checks (exhaustive over `[types, etypes)`, using Ghidra's parse rules:
flags byte, LEB128 name, optional tag, u32 pkgPath):

- `python -B /tmp/kr17-cau/fullscan.py 0x780100` finds only 2 GoName starts whose
  pkgPath field holds 0x780100: 0x954048 and 0xde7c83.
- `python -B /tmp/kr17-cau/fullscan.py 0x28 0x493c63` gives 149 candidates. Only 3 have
  any pointer referrer, and each referrer is a real type's slice-data pointer at
  type+0x38. No file pointer or typeOff reaches type+8, so those 3 are not on any
  realisable path.
- No 8-byte value 0x954048 or 0xde7c83 exists in any `LOAD` segment, so S4 can only be
  reached through a nameOff.
- Among all 7 uncommon map types, the misread nameOffs are only 0x20, 0x18 and 0x28.

The only realisable path is therefore S3 = `GoUncommonType` read 0x18 bytes early, on
one of the three `map[string][]string` types. Which of the three, and through which
interface method, is not determinable statically. `http.ResponseWriter.Header() Header`
is a plausible route (INFERENCE).

## Findings

### F1 — `Cause: UNKNOWN` is under-resolved (calibration + depth) — MEDIUM
- Where: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:84-91` (`:90`
  "Cause: **UNKNOWN**.").
- Counterexample: the chain above. The cause can be bounded statically without a
  replay.
- Smallest fix: keep the OBSERVATION bullet and add one INFERENCE bullet, for example:
  > INFERENCE (static, source + file bytes; not replayed): Ghidra 12.1.4 binds
  > `runtime.maptype` to `internal/abi.OldMapType` (`go1.25.0.json`, alias from
  > `map_noswiss.go:68`; `GoMapType.java:27-29` has no Swiss name). aether's Swiss map
  > types (0x70 B) therefore get their UncommonType read at +0x58 = `SlotSize`. For
  > `http.Header`/`url.Values`/`textproto.MIMEHeader` that value is 40, and nameOff 0x28
  > lands mid-name (types+0x28 = 0x954048, flags 0x6e). Its pkgPath 0x780100 points into
  > an embedded JPEG (0x10d4120), where a LEB128 length 111,938,854 at index 17,645,861
  > overruns memory end 0x18006ef. One chain survives an exhaustive scan.
  > Exact map type and interface method: UNKNOWN.

### F2 — the lesson's reject rationale is wrong in kind, though the verdict stands — MEDIUM
- Where: `corpus/lessons/round-17.md:33`, "no control separates fallback data from
  carrier layout; recorded UNKNOWN".
- Counterexample 1 (separation exists at the data level): the misbinding sits in the
  **base** `go1.25.0.json`, which every 1.25.x carrier uses, and the same alias is in
  go1.24.0. Patch fallback cannot reach it. No `go1.25.*.json.diff` is installed. Across
  all 123 installed diffs (1.15.1–1.24.6), the bootstrap RTTI types are changed only at
  `Position`:
  `grep -h -E '^@ \["[^"]*","Types","(internal/abi\.(Name|Imethod|InterfaceType|StructField|Type|UncommonType|Method|NameOff|TypeOff|TextOff)|runtime\.(moduledata|_type|imethod|interfacetype|structfield|name|uncommontype|pcHeader|textsect|functab|_func))"' patchverdiffs/* | sort | uniq -c`
  printed only `…,"Position"]` paths.
  The failing GoName decode is hand-coded (`GoName.java:93-103`) and does not depend on
  the snapshot.
- Counterexample 2 (the implied control would be invalid): `pro-notesmd-cli` (go1.25.8,
  the same fallback base) logged no analyzer error. However,
  `python -B /tmp/kr17-cau/maps2.py ~/.local/bin/notesmd-cli` reports
  `map types 63 with uncommon 0`, so it never exercises this path. Its silence neither
  supports nor refutes the fallback.
- Smallest fix: change the rationale to: "Rejected on source and data. The failing
  binding is the base go1.25.0.json alias `runtime.maptype → OldMapType`, which fallback
  does not touch. notesmd-cli has no uncommon map types and is not a control."

### F3 — "during interface-type markup" names the outer frame, not the defect — LOW
- Where: knowledge `:89`.
- Evidence: links 0–6 above. The failing getter is `GoName.getPkgPath` (`log:196`),
  reached through `GoMapType` → `GoUncommonType` (`GoType.java:143-149`,
  `GoUncommonType.java:55-58`).
- Fix: append "(map-type UncommonType → GoName.pkgPath)".

### F4 — "no error" does not mean the map types were marked up correctly — LOW (generalization)
- Where: decision table, knowledge `:107`, and implicitly every 1.24/1.25 row (`:54`).
- Evidence: in aether, the other 4 uncommon map types (`go.shape.map[string]interface {}`,
  `go.shape.map[string][2]int32`, `go.shape.map[string]int32`, `*dbus.sigSet`) are misread
  **silently**. They get nameOff 0x20 or 0x18, which gives pkgpath "d" or junk with no
  HAS_PKGPATH bit, so no exception is raised (`maps2.py` output).
- INFERENCE: `GoMapType`'s `keysize`/`elemsize`/`bucketsize`/`flags` fields are misread
  for every Swiss map type, including notesmd-cli's 63, without any log line.
- Fix: add a "Does not mean" cell: "that map types were laid out correctly (1.24+/1.25
  Swiss maps are bound to OldMapType)".
- Prediction this enables (falsifiable in a later round, needs a run): any 1.24.x/1.25.x
  carrier whose uncommon Swiss map type has `SlotSize` N, where types+N decodes to a name
  with the HAS_PKGPATH bit and an out-of-range pkgPath, will abort `GolangSymbolAnalyzer`
  the same way. Same-bytes reruns of aether should reproduce `17645861, 111938854`
  exactly.

## Bounded no-findings (checked, no defect)
- The knowledge bullet does not claim fallback causation (`:91` "does not show that the
  1.25.0 fallback data caused it"). It is consistent with the lesson's reject.
- The compare fields do not include analyzer errors. `compare.json` `all_match: true`
  sits alongside `observation.json:2-4`, and the knowledge entry labels the failure
  "unpredicted", so it is not counted as predicted. `corpus/README.md:35` says "routes
  matched", which is accurate.
- `observation.json` `log_sha256` equals `sha256sum` of the retained `ghidra.log`. The
  carrier digest equals the analyze subject digest.
- `Go strings found: 7200` (`log:207`) is consistent with symbol markup aborting
  independently of string analysis.

## Impacted axes
Calibration: an UNKNOWN can be replaced by a bounded, labelled INFERENCE. Depth: the
mechanism is now traced to a named Ghidra binding defect. Generalization: affects every
1.24/1.25 Swiss-map carrier. No harm to the round's admitted route claims.
