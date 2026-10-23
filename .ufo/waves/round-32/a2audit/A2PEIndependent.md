# A2PEIndependent — independent stdlib PE structural decode of the 12 R32-C1 carriers

Seat: `KaidokuR32A2.A2PEIndependent` (executor leaf). Report written 2026-10-23T07:05Z.
Lane (read-only): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze read: `.ufo/waves/round-32/claims.json` C1 (freeze `9a73680a`), `.ufo/waves/round-32/claims-v3.json` C2 (freeze `f382e3b7`), base `283aad7f`.
Lane HEAD at first read (06:46Z): `f382e3b7`. Lane HEAD at final evidence read (07:04Z): `33393e59` (commits `411f3a80`, `33393e59` landed by L1 integration while this seat ran; this seat made no lane write). Frozen blobs re-checked at both `9a73680a` and `f382e3b7` and are byte-identical to the pinned hashes below.

This seat wrote only `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2PEIndependent/*` and this report. No counter, predicate, target, label, carrier, envelope or lane file was edited; no C1/C2 score is claimed here. No live REA, no Ghidra, no carrier execution, no build, no tool install/update, no git/jj write.

## 1. What was exercised vs inferred

Exercised (bytes read from the immutable carriers and decoded by my own code): COFF machine, ImageBase, data-directory table, section table, primary export directory (names/RVAs/ordinals), load-config CHPE metadata pointer, CHPE metadata v2 code map and counters, `.hexpthk` slot contents, and a structural scan for a second export directory. Compared against the frozen `carriers.tsv` labels and two witnesses (frozen oracle CLI, `llvm-readobj` 23.1.3).

Not exercised / inference: no Windows loader was run, so how the loader consumes the second export directory is not observed. No call graph, relocation application, import resolution, or REA/Ghidra import was performed. The segment rule `max(VirtualSize, SizeOfRawData)` is computed but, on these bytes, is not separable from `SizeOfRawData` (see L2).

## 2. Instruments and frozen inputs (hash-verified)

| file | observed sha256 | pinned sha256 | match |
|---|---|---|---|
| `tools/round-32/arm64x_oracle.py` (witness) | `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686` | claims `instruments`, same | yes |
| `corpus/evidence/round-32/c1/carriers.tsv` | `8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e` | claims `frozen_inputs`, same | yes |
| `corpus/evidence/round-32/c1/predictions.tsv` | `fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b` | claims `frozen_inputs`, same | yes |

Both pinned hashes were re-derived from the git blobs at `9a73680a` and `f382e3b7` (`git show <rev>:<path> | sha256sum`), not only from the working tree. All 12 carrier files are `chattr +i` (`lsattr`: `----i-----------------` on every `k01..k12.dll`); all opens were `"rb"`.

Environment: Python 3.14.8 (`python3 -I -B`), LLVM 23.1.3 (`llvm-readobj` 23.1.3, host toolchain).

## 3. Exact argv, exit status, retained output

Run order matters: the independent decode was produced **before** the oracle witness was captured, so witness output could not inform it.

```
# 06:55Z  independent reader (my code), 12 carriers
cd /fast/scratch/hyaku/kaidoku-r32/a2audit/A2PEIndependent
bash -c 'ulimit -v 4194304; exec timeout 900 python3 -I -B ./pe_indep.py \
  --tsv /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-32/c1/carriers.tsv \
  --json indep.json'
=> exit 0 ; stdout 96,541 B (indep.stdout.txt) ; stderr 0 B (indep.stderr.txt)

# 06:56Z  frozen oracle CLI witness (not imported, not used as input)
bash -c 'ulimit -v 4194304; timeout 900 python3 -I -B \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/arm64x_oracle.py \
  /fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll ... k12.dll'
=> exit 0 ; 12 JSON lines (oracle.stdout.jsonl) ; stderr 0 B (oracle.stderr.txt)

# 06:57Z  third-party dual-view witness
for k in k01 .. k12; do llvm-readobj --file-headers --sections --coff-exports \
  /fast/scratch/hyaku/kaidoku-r32/carriers/$k.dll > readobj-$k.txt 2>&1; done
=> 12/12 exit 0 ; 11,624-12,380 B each

# 07:01Z  comparison of decode vs labels vs both witnesses
bash -c 'ulimit -v 4194304; exec timeout 900 python3 -I -B ./compare.py'
=> exit 0

# 07:03Z  secondary-directory placement/reference evidence
bash -c 'ulimit -v 4194304; exec timeout 900 python3 -I -B ./secondary_evidence.py'
=> exit 0
```

`compare.stdout.txt` (full):

```
carriers=12 checks=372 passed=372 failed=0
  classify_arm64x                            pass=12 fail=0
  code_map_arm64_and_arm64ec                 pass=12 fail=0
  hexpthk_slots_are_x64_thunks               pass=12 fail=0
  label_bytes                                pass=12 fail=0
  label_ec_exports                           pass=12 fail=0
  label_ec_via_entry_point_count             pass=12 fail=0
  label_ec_via_hexpthk                       pass=12 fail=0
  label_ec_via_redirection_count             pass=12 fail=0
  label_native_exports                       pass=12 fail=0
  label_sha256                               pass=12 fail=0
  machine_0xaa64                             pass=12 fail=0
  oracle_arm64x_flag                         pass=12 fail=0
  oracle_code_map                            pass=12 fail=0
  oracle_document                            pass=12 fail=0
  oracle_format_arch                         pass=12 fail=0
  oracle_image_base                          pass=12 fail=0
  oracle_machine                             pass=12 fail=0
  oracle_native_export_names                 pass=12 fail=0
  oracle_procedure_count                     pass=12 fail=0
  oracle_segment_count                       pass=12 fail=0
  oracle_segments                            pass=12 fail=0
  oracle_sha256                              pass=12 fail=0
  readobj_format                             pass=12 fail=0
  readobj_hybrid_export_names                pass=12 fail=0
  readobj_hybrid_export_table_rva            pass=12 fail=0
  readobj_hybrid_format                      pass=12 fail=0
  readobj_image_base                         pass=12 fail=0
  readobj_machine_is_synthesized             pass=12 fail=0
  readobj_primary_export_names               pass=12 fail=0
  readobj_section_count                      pass=12 fail=0
  readobj_section_names                      pass=12 fail=0
```

`secondary-evidence.stdout.txt` (full; column 4 = 4-byte occurrences of the EC-directory RVA with containing section):

```
k01 adjacent=True named_by_dd=False u32=[('0x2236', '.reloc')] u64=[]
k02 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k03 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k04 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k05 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k06 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k07 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k08 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k09 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k10 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k11 adjacent=True named_by_dd=False u32=[('0x2436', '.reloc')] u64=[]
k12 adjacent=True named_by_dd=False u32=[('0x2236', '.reloc')] u64=[]
```

## 4. Independent decode vs frozen labels vs witnesses

All 12 files: `e_lfanew=0x78`, PE32+ (`0x020b`), COFF characteristics `0x2022`, Subsystem 2, `SizeOfHeaders=0x400`, `SizeOfImage=0x9000`, `NumberOfRvaAndSizes=16`, non-zero data directories only `export`, `exception`, `basereloc`, `debug`, `load_config`, seven sections `.text/.hexpthk/.rdata/.data/.pdata/.a64xrm/.reloc` in that order, `ImageBase=0x180000000`.

| id | file sha256 == label | machine | ImageBase | secs | segs | DD0 names (label native) | EC dir RVA | EC dir names (label EC) | .hexpthk slots | entry-pt count | redir count | code-map kinds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| k01 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 1 (1) | 0x4385 | 1 (1) | 1 (1) | 1 (1) | 1 (1) | ARM64/ARM64EC/AMD64 |
| k02 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 2 (2) | 0x43a2 | 2 (2) | 2 (2) | 2 (2) | 2 (2) | ARM64/ARM64EC/AMD64 |
| k03 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 3 (3) | 0x43b7 | 3 (3) | 3 (3) | 3 (3) | 3 (3) | ARM64/ARM64EC/AMD64 |
| k04 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 4 (4) | 0x43ac | 1 (1) | 1 (1) | 1 (1) | 1 (1) | ARM64/ARM64EC/AMD64 |
| k05 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 1 (1) | 0x43ad | 4 (4) | 4 (4) | 4 (4) | 4 (4) | ARM64/ARM64EC/AMD64 |
| k06 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 5 (5) | 0x43e9 | 5 (5) | 5 (5) | 5 (5) | 5 (5) | ARM64/ARM64EC/AMD64 |
| k07 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 6 (6) | 0x43d6 | 2 (2) | 2 (2) | 2 (2) | 2 (2) | ARM64/ARM64EC/AMD64 |
| k08 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 2 (2) | 0x43d2 | 6 (6) | 6 (6) | 6 (6) | 6 (6) | ARM64/ARM64EC/AMD64 |
| k09 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 7 (7) | 0x43eb | 3 (3) | 3 (3) | 3 (3) | 3 (3) | ARM64/ARM64EC/AMD64 |
| k10 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 3 (3) | 0x43e7 | 7 (7) | 7 (7) | 7 (7) | 7 (7) | ARM64/ARM64EC/AMD64 |
| k11 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 8 (8) | 0x4438 | 8 (8) | 8 (8) | 8 (8) | 8 (8) | ARM64/ARM64EC/AMD64 |
| k12 | yes | 0xaa64 | 0x180000000 | 7 | 8 | 1 (1) | 0x4395 | 2 (2) | 2 (2) | 2 (2) | 2 (2) | ARM64/ARM64EC/AMD64 |

Export names observed (my decode, byte-derived): primary `f1..fN` (k01-k08, k11) or `n1..nN` (k09, k10, k12); second directory `f1..fN` (k01-k03, k06, k11), `g1..gM` (k04, k05, k07, k08), `e1..eM` (k09, k10, k12). This is exactly the builder prefix/count spec (`tools/round-32/build-arm64x-carriers.sh` SPEC rows) for both views.

Comparison result: 372/372 checks pass. The label checks are 12/12 each for file sha256, file bytes, native-export count vs DD0 name count, EC-export count vs second-directory name count, EC count vs `.hexpthk` slot count, EC count vs CHPE `CodeRangesToEntryPointsCount` (+0x30) and vs `RedirectionMetadataCount` (+0x34). The oracle witness checks are 12/12 each for sha256, machine, `arm64x` flag, code map triples, ImageBase, segment count, procedure count, full segment list, document name, format/architecture, and native export-name list. The `llvm-readobj` witness checks are 12/12 each for `Format: COFF-ARM64X`, ImageBase, section count/names, primary export names, HybridObject export names, HybridObject `ExportTableRVA`, and HybridObject `Format: COFF-ARM64EC`.

## 5. Bounded findings

1. **Raw COFF machine is `0xAA64` on all 12.** The bytes at `e_lfanew+4` are `64 aa` for every carrier; my reader, the frozen oracle (`class.machine == "0xaa64"`) and the claim predicate agree.
2. **`procedure_count` = primary export-directory name count is corroborated at byte level.** DataDirectory[0] name counts `1,2,3,4,1,5,6,2,7,3,8,1` equal `carriers.tsv.native_exports` and the oracle's `expected.procedure_count` on all 12.
3. **The frozen `ec_exports` label is not a DataDirectory[0] count.** On all 12 it equals the name count of a second structurally valid `IMAGE_EXPORT_DIRECTORY` (own DLL-name string, Base, function/name tables, names, RVAs). That directory begins at the first byte after the primary export bloc in all 12 (`primary_bloc_end_rva == secondary_rva`), is named by no data-directory entry in all 12, has a 4-byte self-RVA occurrence only inside `.reloc` (12/12; `0x2236` for k01/k12, `0x2436` otherwise), and no 8-byte `ImageBase+RVA` occurrence anywhere (12/12).
4. **Two further independent structures reproduce the EC label 12/12:** `.hexpthk` `VirtualSize/16` slots (every slot begins `48 8b c4`; x64 thunk bodies) and the CHPE metadata v2 counters at +0x30/+0x34.
5. **CHPE metadata:** load-config `Size` is `0x140` and `CHPEMetadataPointer` at +0xC8 is non-zero for all 12; metadata `Version=2`; `CodeMap` at +4 with `CodeMapCount=3`; every code map is exactly three ranges in order ARM64, ARM64EC, AMD64 (e.g. k05: `(ARM64,0x1000,16) (ARM64EC,0x2000,152) (AMD64,0x3000,64)`), equal to the oracle's `class.code_map` 12/12.
6. **Segment projection:** `Headers` (`ImageBase .. ImageBase+0x400`) plus the seven sections in table order = 8 segments; equal to the oracle's `expected.segments` field-for-field (start/end/length/image_base/address_space) 12/12.
7. **Witness quirk (recorded, not repaired):** `llvm-readobj` 23.1.3 prints `Machine: IMAGE_FILE_MACHINE_ARM64X (0xA64E)` for the file and `HybridObject { Format: COFF-ARM64EC; Machine: IMAGE_FILE_MACHINE_ARM64EC (0xA641) }`. Neither `0xA641` nor `0xA64E` occurs anywhere in the 12 files' bytes (`u16` search: zero hits); the on-disk COFF field is `0xAA64`. Both machine values are synthesized view labels. Its HybridObject view does independently corroborate the second export directory: `ExportTableRVA` equals my scanned secondary RVA and its export names equal mine, 12/12.
8. **Builder-limit corroboration:** every section in all 12 files has `SizeOfRawData >= VirtualSize` (so the frozen `max(VirtualSize,SizeOfRawData)` rule degenerates to `SizeOfRawData` here, matching the claim's stated limit). All functions being exported leaves is a build property this seat cannot observe from bytes.

## 6. Limits of this evidence

- L1: Carriers are author-built by one host LLVM 23.1.3 `lld-link -machine:arm64x` build from published lld test inputs; no published third-party ARM64X binary was decoded.
- L2: Because every section has `SizeOfRawData >= VirtualSize`, the segment-length rule `max(VirtualSize,SizeOfRawData)` is not separated from `SizeOfRawData` by these bytes. No carrier has a VirtualSize-exceeds-raw section, an internal function, or a call-reached function; those cases are untested here.
- L3: The reader (`pe_indep.py`, written from the PE/COFF format) covers DOS/COFF/optional headers, the 16-entry data-directory table, 8-byte section names, the primary and scanned export directories, and load-config/CHPE v2. It does not parse imports, resources, relocations, forwarded exports (function RVA inside the export directory range), exceptions, debug data, or `/N` long section names, and it verifies no checksum or signature. It requires the export DLL name to end `.dll` when scanning for the second directory; candidates that fail any resolution test are dropped, not repaired.
- L4: The second export directory's location is obtained by a byte-structural scan of file-backed sections, then confirmed by adjacency; that the Windows loader uses the same rule, or any particular loader rule, is **not** exercised (no carrier was executed, no Windows host).
- L5: The `llvm-readobj` text parser used in `compare.py` is mine; an earlier run undercounted primary exports on 3 carriers because uppercase-hex RVA digits were not matched. That defect was fixed before the retained run, and the retained `compare.stdout.txt`/`compare.json` are from the exit-0 372/372 run. The oracle JSON parser and the labels table had no such defect.
- L6: No live REA 6.5.0 and no Ghidra import was run, so this report cannot speak to the REA envelope fields; it independently corroborates the structural inputs the frozen oracle projects into `expected`. The oracle and `llvm-readobj` are witnesses only and were not used as decode inputs.
- L7: This seat did not run, edit or score any counter/predicate/target; no C1/C2 target line is claimed. No tool was installed or updated.

## 7. Retained artifacts (scratch, hashes at 07:04Z)

Directory `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2PEIndependent/` (532 KB total):

| file | sha256 | role |
|---|---|---|
| `pe_indep.py` | `42418a1736c21b054e76b902f0c04130946c645c9c4b4a148b5bddbea973a4f0` | independent reader (stdlib only) |
| `compare.py` | `b955f90849192ceeeee26b2849f2ec8dc1d4032e9fd05bf02e9e039cf9ed4209` | label/oracle/readobj comparison |
| `secondary_evidence.py` | `9aed4a5d46b44aae573ad97ed6b1277ace48648c0f56084aac2c506db72d83d7` | placement/reference checks |
| `indep.json` | `f79b51db2e51b93c1ac0b16b499d22507f4c5c1d1fb0d74607370a1bbfcf44f2` | full independent decode (12 records) |
| `indep.stdout.txt` / `indep.stderr.txt` | 96,541 B / 0 B | reader stdout (full JSON) / stderr |
| `oracle.stdout.jsonl` | `e71a55bafd860fd6efcb9e65dda41459e593e6b860b121d23f7360c15298ef5a` | oracle CLI witness stdout (12 lines) |
| `oracle.stderr.txt` | 0 B | witness stderr |
| `readobj-k01.txt` .. `readobj-k12.txt` | e.g. k01 `aa1ee360c73aba18e525b478f7b75361eb2f6e6b1a48a09d03daf6289203436b` | `llvm-readobj` witness, one per carrier |
| `compare.json` | `4b65110c115b75e78f631b067f2fd444fd2d1ce43eace649405eaa9299e0ae5b` | per-check results (372) |
| `compare.stdout.txt` | `8561cd88c78fa6f65465266f5450a45ede6beb642b0d7ee6787c2ba68619670f` | comparison stdout (exit 0) |
| `secondary-evidence.json` | `b7e7c9d8693febd09779b44af951d80e0cb76ef5becd8fa4b465697023a791a8` | per-carrier placement/reference evidence |
| `secondary-evidence.stdout.txt` | `d48d9a01a8da35fb0526a1a7a8d7dcebf198dab191fab8ac0b997da3c579157c` | its stdout (12 lines) |
| `probe-readobj-k05.txt` | 11,760 B | first `llvm-readobj` probe (read-only) |

No sandbox git clone revision is reported because this seat performed no git write and needed no clone; the immutable carriers under `/fast/scratch/hyaku/kaidoku-r32/carriers/` were the decoded inputs, pinned by the hashes above.
