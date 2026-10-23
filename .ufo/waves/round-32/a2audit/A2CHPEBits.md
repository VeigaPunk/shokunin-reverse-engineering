# A2CHPEBits — ARM64X/ARM64EC code-map bit tags, range addresses, and oracle.classify scope (round-32 a2audit)

Seat: `KaidokuR32A2.A2CHPEBits` (leaf, no subagents). Observations window: 2026-10-23 06:47:45Z–~06:59Z (host `date -u` anchor 06:47:45Z). All times UTC.
Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CHPEBits`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only). No writes outside scratch + this report. No tools installed or updated (host LLVM 23.1.3 already present; `clang/lld-link/llvm-mc/llvm-readobj` at `/usr/bin` — recorded per tooling directive as "none needed").

## 0. Pins verified (exercised)

- `git show -s --format='%H %cI %s' 9a73680a f382e3b7 283aad7f` → `9a73680af21b002e3b99956c89234b2bbde2a71b 2026-10-23T03:03:46-03:00 (=06:03:46Z) round-32: freeze R32-C1 …`; `f382e3b7978e6091a19ca93277c15a75c0016b43 2026-10-23T03:10:01-03:00 (=06:10:01Z) round-32: freeze R32-C2 v3 …`; `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 2026-10-23T02:44:59-03:00 (=05:44:59Z)`.
- Instruments at 9a73680a: `tools/round-32/arm64x_oracle.py` sha256 `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686` = claims.json pin ✓ (worktree copy byte-equal; `git diff --stat 9a73680a -- tools/round-32/ corpus/evidence/round-32/` shows only later c2-v2/v3/freeze-integrity additions). `c1-arm64x-positive.py` = `7a534be6…` ✓.
- Carriers pinned at `/fast/scratch/hyaku/kaidoku-r32/carriers/`: 12 files, sha256 all equal `corpus/evidence/round-32/c1/carriers.tsv` (spot chain: k01 `2f386dde73a262a6…`, k11 `b5e2af7f2b96fd66…`, k12 `8c852d075fab64ac…` — full list recomputed and matched).

## 1. Independent code-map reconstruction from carrier bytes (exercised)

Method: a purpose-written pure-Python struct parser in scratch (no import of the lane oracle at parse time), reading MZ/PE, COFF machine, PE32+ data directory 10 (load config), `CHPEMetadataPointer` (uint64 at load-config offset 0xC8), metadata `{uint32 Version; uint32 CodeMap_RVA; uint32 CodeMapCount; …}`, and code-map entries as `{uint32 start_with_tag; uint32 length}` at 8-byte stride. The stride/field layout was taken from the pinned instrument's documented format and then re-derived from raw bytes; results were checked against `llvm-readobj --coff-load-config` as an independent witness. Agreement: 12/12 carriers, every entry.

Invariant across all 12 carriers: `machine=0xAA64`, `image_base=0x180000000`, load config RVA `0x4000` size `0x140`, CHPE pointer `0x180005000` (RVA `0x5000`), metadata `Version=2`, `CodeMap RVA=0x415C` (file offset `0x195C`), `CodeMapCount=3`.

Bit tags observed in raw `start` dwords (low 2 bits): `0`=ARM64, `1`=ARM64EC, `2`=X64 (llvm-readobj prints "X64"; the frozen oracle names the same tag "AMD64"). No tag value 3 occurs. The tag is the only type carrier: masking it (`start & ~3`) gives the range RVA.

| id | ARM64 entry (raw start, len) | range RVA–end (VA = +0x180000000) | ARM64EC entry (raw, len) | range RVA–end | X64/AMD64 entry (raw, len) | range RVA–end | section of tag-2 range |
|----|------|------|------|------|------|------|------|
| k01 | 0x1000, 0x10 | 0x1000–0x1010 | 0x2001, 0x5c | 0x2000–0x205C | 0x3002, 0x10 | 0x3000–0x3010 | .hexpthk |
| k02 | 0x1000, 0x20 | 0x1000–0x1020 | 0x2001, 0x70 | 0x2000–0x2070 | 0x3002, 0x20 | 0x3000–0x3020 | .hexpthk |
| k03 | 0x1000, 0x84 | 0x1000–0x1084 | 0x2001, 0xd8 | 0x2000–0x20D8 | 0x3002, 0x30 | 0x3000–0x3030 | .hexpthk |
| k04 | 0x1000, 0x40 | 0x1000–0x1040 | 0x2001, 0x5c | 0x2000–0x205C | 0x3002, 0x10 | 0x3000–0x3010 | .hexpthk |
| k05 | 0x1000, 0x10 | 0x1000–0x1010 | 0x2001, 0x98 | 0x2000–0x2098 | 0x3002, 0x40 | 0x3000–0x3040 | .hexpthk |
| k06 | 0x1000, 0xdc | 0x1000–0x10DC | 0x2001, 0x138 | 0x2000–0x2138 | 0x3002, 0x50 | 0x3000–0x3050 | .hexpthk |
| k07 | 0x1000, 0x60 | 0x1000–0x1060 | 0x2001, 0x70 | 0x2000–0x2070 | 0x3002, 0x20 | 0x3000–0x3020 | .hexpthk |
| k08 | 0x1000, 0x20 | 0x1000–0x1020 | 0x2001, 0xc0 | 0x2000–0x20C0 | 0x3002, 0x60 | 0x3000–0x3060 | .hexpthk |
| k09 | 0x1000, 0x70 | 0x1000–0x1070 | 0x2001, 0x84 | 0x2000–0x2084 | 0x3002, 0x30 | 0x3000–0x3030 | .hexpthk |
| k10 | 0x1000, 0x84 | 0x1000–0x1084 | 0x2001, 0x198 | 0x2000–0x2198 | 0x3002, 0x70 | 0x3000–0x3070 | .hexpthk |
| k11 | 0x1000, 0x80 | 0x1000–0x1080 | 0x2001, 0xe8 | 0x2000–0x20E8 | 0x3002, 0x80 | 0x3000–0x3080 | .hexpthk |
| k12 | 0x1000, 0x10 | 0x1000–0x1010 | 0x2001, 0x70 | 0x2000–0x2070 | 0x3002, 0x20 | 0x3000–0x3020 | .hexpthk |

Structural reading of the ranges (exercised, from section table): tag-0 (ARM64) and tag-1 (ARM64EC) ranges both lie in `.text` (native and EC contributions merged into one section, disjoint address windows); tag-2 (X64) ranges lie in `.hexpthk` and their length equals 0x10 × ec_exports. `x64_code_ranges_to_entry_points` count = 0 in the metadata while llvm-readobj still prints per-thunk entry-point tables (synthesized side structures), so those are not read from `CodeMapCount`. Example witness (`llvm-readobj --coff-load-config k01.dll`, exit 0): `CodeMap [ 0x1000 - 0x1010 ARM64 / 0x2000 - 0x205C ARM64EC / 0x3000 - 0x3010 X64 ]`.

Side observation (exercised): the frozen oracle's `export_names()` on all 12 returns exactly the native `f*`/`n*` names (k01 `['f1']`, k06 5 names, k09 `n1..n7`, k11 8, k12 `['n1']` …), matching `predictions.tsv` `procedure_count` 1,2,3,4,1,5,6,2,7,3,8,1 — the primary export directory holds native-view names only; EC exports are not in it.

## 2. Upstream tag and input provenance (exercised)

- Committed inputs are byte-identical to upstream at tag `llvmorg-23.1.3`: `diff` of `corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s` vs `https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64.s` → no output, exit 0, sha256 `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`; same for `loadconfig-arm64ec.s`, sha256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4`. Both equal `claims.json.frozen_inputs` ✓. (An earlier rendered view had suggested whitespace deltas; the byte diff shows none.)
- The `.s` files declare `__chpe_metadata` but leave `__hybrid_code_map` undefined — lld-link synthesizes the code map at link time from section contributions. Upstream test expectations at the same tag document the semantics: quote (17 words) — "Order of arguments doesn't matter in this case, chunks are sorted by target type anyway." — `lld/test/COFF/arm64ec-codemap.test:48`, tag llvmorg-23.1.3, sha256 `edf6964b69261a5354d90b2fed1689c089b8600393f5a7b63e5047b42c229022`, fetched 2026-10-23. Same test's `CODEMAPX` CHECK lines show the three tags emitted as `ARM64`, `ARM64EC`, `X64`. Note: `lld/test/COFF/arm64x.test` does not exist at llvmorg-23.1.3 (curl 404); the codemap test is the operative upstream witness.
- Microsoft Learn (claim row S099) definition, quote (20 words) — "Arm64X is a new type of binary that can contain both the classic Arm64 code and Arm64EC code together." — https://learn.microsoft.com/en-us/windows/arm/arm64x-pe, `ms.date 2025-11-06`, `git_commit ab16bb917a5a6310749000da77644e7c664759c1`, opened 2026-10-23. The page defines the dual-code intent; it does not specify bit tags — the bytes and the lld test above are the tag authority.

## 3. Exactly what `oracle.classify` proves (source-verified, hash-pinned)

Pinned source (9a73680a, sha256 verified above), docstring quote (22 words): "COFF machine 0xAA64, a non-zero CHPE metadata pointer, and a code map holding at least one ARM64 and one ARM64EC range." — `tools/round-32/arm64x_oracle.py:15-17`.

Exercised behavior of the frozen copy (imported from a hash-verified scratch copy; `oracle_copy.py` sha256 = `17eea1f9…`): `classify` consumes exactly
1. `MZ` + `PE\0\0` signatures; PE32+ magic 0x20B;
2. COFF machine field == 0xAA64 (probe B3: flipping it to 0x8664 → `arm64x:false` with map intact);
3. data directory 10 RVA non-zero and load-config `Size >= 0xD0`;
4. `CHPEMetadataPointer` (uint64 @ LC+0xC8) non-zero (probe B4: zeroing → `arm64x:false`, map empty);
5. metadata words at +4/+8 (`CodeMap RVA`, `CodeMapCount`) and each entry's low-2 tag bits — nothing else. Metadata `Version` is read but never checked. Probe B1: retagging the EC entry 1→0 → `arm64x:false`; probe B2: retagging the `.hexpthk` X64 thunk range 2→1 → `arm64x:true` with map `{ARM64@0x1000, ARM64EC@0x2000, ARM64EC@0x3000}`; llvm-readobj prints the relabeled range as `0x3000 - 0x3010 ARM64EC`, i.e. the independent reader also trusts the tag bits alone.

`classify` never reads instruction bytes, never checks that a range lies inside a section, checks no overlap/ordering/count-sanity, no checksum, no certificate. Therefore classify proves **declared-metadata self-consistency only**: "this image declares an ARM64-view and an ARM64EC-view code range in a v2-style CHPE metadata it points to". It does not prove that any ARM64EC (or x64) code exists, nor that range bytes decode as the tagged ISA.

## 4. Falsification probe: pure ARM64 file + forged metadata (exercised — passes)

Fixture built entirely in scratch from aarch64-only inputs, host LLVM 23.1.3 (exit 0 throughout):

```
llvm-mc -filetype=obj -triple=aarch64-windows forged-loadconfig.s -o forged-lc.obj
clang --target=aarch64-pc-windows-msvc -O1 -c forged-native.c -o forged-native.obj
lld-link -machine:arm64 -dll -noentry -nodefaultlib -Brepro forged-native.obj forged-lc.obj -out:forged-pure-arm64.dll
```

`forged-loadconfig.s` is a hand-written load config (size 0x140, CHPEMetadataPointer → my `__chpe_metadata`, `Version=2`, `CodeMapCount=2`) plus a hand-written code map: `{0x1000|tag0, len 0x20} (ARM64)`, `{0x1010|tag1, len 0x10} (ARM64EC)`. `forged-native.c` is two exported leaf functions. No ARM64EC object, no x86_64 object, no EC source exists anywhere in the build.

Result: `forged-pure-arm64.dll` sha256 `1542e5102fbb42e7c951d3e1ee27373824c3fd8e80ee6adf2174dac24efbc7f9`, 3072 bytes, machine 0xAA64, sections `.text/.rdata/.data/.reloc` only (no `.hexpthk`, no aux IAT). Full `.text` disassembly (`llvm-objdump -d`, exit 0): two aarch64 leaf functions only — `180001000: add w0, w1, w0; ret` and `180001008: sub w0, w0, w1; ret`; the "ARM64EC"-tagged window 0x1010–0x1020 contains those ARM64 encodings plus zero padding. Frozen oracle on it: `classify → {"arm64x": true, "machine": "0xaa64", "code_map": [{ARM64,0x1000,32},{ARM64EC,0x1010,16}]}`; `expected → {"format":"pe","architecture":"arm64","procedure_count":2,"segment_count":5,…}`.

**Answer to the assignment question: yes — a pure ARM64 file with forged metadata passes `oracle.classify`.** First-line falsified finding (reported, not repaired): any reading of `oracle.classify` (or of the R32-C1 `arm64x` term it feeds) as proof that a binary *contains* ARM64EC code is falsified by construction; classify is a check on declared metadata, forgeable in 8 bytes of map entries. [INFERENCE, bounded]: the frozen P1 predicate's remaining gates (live REA 6.5.0 inspect envelope equality, committed envelope, predictions) compare reader outputs over the same declared structures, so this finding concerns the class "ARM64X evidence = load-config declaration"; whether Ghidra/REA also never validates range bytes was not exercised here — no REA run was in this seat's scope.

## 5. Bounds, cleanup, confidence

- Carrier binaries were only byte-parsed/read (readobj, objdump, python struct); never executed. REA never launched. No counter/predicate file touched. No git/jj writes anywhere; only `git show`/`rev-parse`/`diff` reads against the lane.
- Fixture writes: forged dll 3,072 B; probes 9,216 B each (k01 copies); objects few KB — all far under 1 MiB. No marker/log files created. Build/test commands completed synchronously (seconds, well under the 900 s / 4 GiB caps); `ps` check at end: 0 matching `lld-link|llvm-mc|clang` processes — nothing left running.
- Probe hashes: B1 `0f35665572173c33…`, B2 `70b79f1ca4688835…`, B3 `bf68c13d1bdf480b…`, B4 `c6e23a69015fc658…` (full sha256 in scratch `sha256sum` output above).
- Confidence: §0–§4 statements marked "exercised" are byte/command-observed (exit codes 0, outputs quoted). The lld-synthesizer role of `__hybrid_code_map` is observed via the undefined symbol in the committed input + upstream test expectations + resulting carriers' maps; the lld source itself was not read. Tag-2 naming differs between witnesses (readobj "X64", oracle "AMD64") — same bit value 2 in all observations.

Trailer: `.ufo/waves/round-32/a2audit/A2CHPEBits.md`
