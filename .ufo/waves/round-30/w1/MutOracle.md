# MutOracle — independent oracle mutation probe

## Verdict

- **[OBSERVATION] Three mutants killed, four survived, zero inconclusive**, using all 16 frozen real carriers for every pristine, mutated and restored run.
- **[OBSERVATION] Every oracle offset agrees with LLVM.** All 10 ELF/Mach-O sizes agree directly with LLVM `Size`; all six PE sizes agree with LLVM `VirtualSize` (which is smaller than `RawDataSize`). Thus content-range agreement holds on 16/16; literal agreement with PE raw/padded extent does not.
- **[OBSERVATION] Package counts never change under any of the seven mutants.** Counting packages alone would miss all seven; normalized package/dependency tuples expose two of the mutants.
- **[INFERENCE]** PE raw-size selection, defaulting absent kind to `runtime`, and retaining dependency indices instead of names affect fields used by C1 equality. They would fail equality against REA output having the pristine values. The other four changes are invisible on this carrier set. **[UNKNOWN] Live REA agreement was not measured by this seat.**

Axes: mutation sensitivity, independent layout agreement, real-carrier coverage, exact-byte restoration.

## Scope and carrier incident

Only isolated files under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/` were mutated. No carrier, shared mutant, lane source, Git/JJ state, or sibling file was written. This report is the only lane write. No REA, C1 measure counter, C2 counter, carrier execution, installation or update was invoked.

L1 reported four carriers had been altered by an unidentified writer at 02:42:35Z, restored at approximately 02:46Z, and made immutable. **This seat was not that writer.** This seat had not run a detector or counter before that notice, so there is **no PIN-blocked run to report**. Preliminary section-format inspections are not used as measurement evidence. The complete measured run below began at 2026-10-23T02:47:07.759019Z, after the reported restoration. Every detector invocation checked the SHA-256 and length of all 16 carriers against the frozen manifest and encountered zero identity errors. This is a fresh post-restoration measurement, not a claimed rerun of a nonexistent failed run.

One preliminary copy command failed because `cp` interpreted a proposed destination as a second source (`cannot stat .../pristine.py`, exit 1); exact-byte copies were then made successfully before any detector ran. This was setup failure, not a mutant kill or PIN result.

## Producing commands and detector

Driver command, exit **0**, recorded interval **2026-10-23T02:47:07.759019Z–02:47:16.610614Z**:

```text
timeout 600 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe.py
```

The **identical bounded detector command** ran 21 times: pristine, mutated, restored for each of seven mutants:

```text
timeout 90 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/detect.py --oracle /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/rust_dep_oracle.py --reference /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/pristine.py --manifest /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/carriers.tsv --llvm-dir /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm
```

Expected detector: nonzero for changed normalized tuples, changed offset/size, oracle errors, or LLVM content-range disagreement; zero for unchanged real-carrier output with matching ranges. A failed pristine/restored baseline would be inconclusive, not killed. The detector invokes `read_file()` and `normalize()` on each real carrier for both the tested module and the immutable pristine reference. It compares package counts, full normalized values, documents and section dictionaries; records first tuple differences; and independently parses LLVM section listings. It does not fabricate REA envelopes or score a live REA claim.

LLVM sections were collected once after restoration and reused unchanged by all 21 detector invocations. Exact commands, UTC start/end, exit, full stdout and stderr are retained in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm-commands.json`. All 16 commands exited **0**, with empty stderr, during **02:47:07.775985Z–02:47:07.810384Z**:

```text
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-aarch64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-aarch64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-riscv64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/elf-riscv64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uvw
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uvw
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/macho-x86_64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/macho-x86_64-uvx
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/macho-arm64-uv
timeout 30 llvm-readobj --sections /fast/scratch/hyaku/kaidoku-r30/carriers/macho-arm64-uvx
```

For PE, `llvm_content_size` explicitly means `RawDataSize` when `VirtualSize == 0`, otherwise `min(VirtualSize, RawDataSize)`. The independent corroboration is LLVM's parsed header fields, **not** a claim that LLVM itself labels this formula a compressed-stream length. Both original LLVM size fields remain recorded, so the PE qualification cannot be hidden by this comparison.

Full stdout/stderr, exact command, UTC timestamps, exit codes, per-carrier results, first differing tuples and before/during/after hashes for every detector run are preserved in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe-receipts.json`.

## Mutants, outputs and verdicts

All times in the following table are UTC on **2026-10-23**. Each row uses the exact detector command above. Exit triples are **pristine / mutated / restored**. Every pristine and restored run reported 16 carriers, zero errors, zero output changes, 16 offset matches and 16 content-size matches.

| Mutant | Smallest behavior-bearing change | Mutated start UTC | Exit triple | Changed carriers | Result / expected equality detector |
|---|---|---|---|---:|---|
| m01-pe-raw-size | Line 71: choose `size = rawsize` unconditionally | 02:47:08.265008 | 0 / 1 / 0 | 6/16 | **Killed**: all six PE sizes change; compressed-size equality detects it |
| m02-macho-any-segment | Line 93: remove the `seg == b"__DATA"` condition | 02:47:09.415024 | 0 / 0 / 0 | 0/16 | **Survived**: every Mach-O `.dep-v0` is already in `__DATA` |
| m03-elf32-offset-size-swap | ELF32-only line 43: return `size, off` instead of `off, size` | 02:47:10.681153 | 0 / 0 / 0 | 0/16 | **Survived**: all six ELF carriers have class 2 (ELF64); the changed path is not entered |
| m04-first-hit | Line 108: reject only empty hits rather than `len(hits) != 1` | 02:47:11.953665 | 0 / 0 / 0 | 0/16 | **Survived**: LLVM finds exactly one named `.dep-v0` in each of the 16 carriers |
| m05-default-runtime | Line 126: `p.get("kind", "runtime")` instead of `p.get("kind")` | 02:47:13.154295 | 0 / 1 / 0 | 16/16 | **Killed**: full normalized tuple equality detects absent-kind replacement; counts do not |
| m06-dependency-indices | Line 125: retain sorted integer dependency indices instead of resolving `(name, version)` | 02:47:14.344520 | 0 / 1 / 0 | 16/16 | **Killed**: dependency tuple equality detects indices in place of named dependencies; counts do not |
| m07-require-no-zlib-trailing | Insert rejection when `d.unused_data` is nonempty | 02:47:15.716141 | 0 / 0 / 0 | 0/16 | **Survived**: every pristine section has a complete zlib stream with zero unused bytes |

**Important direction of m07:** the actual pristine oracle already ignores zlib trailing bytes; it checks `d.eof` but not `d.unused_data`. Therefore the non-no-op mutation tests the opposite policy—require no trailing data—rather than pretending to remove a check that does not exist. This carrier set distinguishes neither policy.

Exact driver stdout excerpts (the driver command above produced these lines):

```text
m01-pe-raw-size phase=mutated utc=2026-10-23T02:47:08.265008+00:00 exit=1 c1_fields_changed=6 carriers=16 errors=0 llvm_content_size_matches=10 llvm_offset_matches=16 llvm_raw_size_matches=16 normalized_changes=0 offset_changes=0 outputs_changed=6 package_count_changes=0 size_changes=6
m02-macho-any-segment phase=mutated utc=2026-10-23T02:47:09.415024+00:00 exit=0 c1_fields_changed=0 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=0 offset_changes=0 outputs_changed=0 package_count_changes=0 size_changes=0
m03-elf32-offset-size-swap phase=mutated utc=2026-10-23T02:47:10.681153+00:00 exit=0 c1_fields_changed=0 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=0 offset_changes=0 outputs_changed=0 package_count_changes=0 size_changes=0
m04-first-hit phase=mutated utc=2026-10-23T02:47:11.953665+00:00 exit=0 c1_fields_changed=0 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=0 offset_changes=0 outputs_changed=0 package_count_changes=0 size_changes=0
m05-default-runtime phase=mutated utc=2026-10-23T02:47:13.154295+00:00 exit=1 c1_fields_changed=16 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=16 offset_changes=0 outputs_changed=16 package_count_changes=0 size_changes=0
m06-dependency-indices phase=mutated utc=2026-10-23T02:47:14.344520+00:00 exit=1 c1_fields_changed=16 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=16 offset_changes=0 outputs_changed=16 package_count_changes=0 size_changes=0
m07-require-no-zlib-trailing phase=mutated utc=2026-10-23T02:47:15.716141+00:00 exit=0 c1_fields_changed=0 carriers=16 errors=0 llvm_content_size_matches=16 llvm_offset_matches=16 llvm_raw_size_matches=10 normalized_changes=0 offset_changes=0 outputs_changed=0 package_count_changes=0 size_changes=0
TOTAL killed=3 survived=4 inconclusive=0 source_unchanged=1 active_restored=1
```

Concrete counterexamples, observed in detector stdout recorded in the receipt:

- **m01:** `pe-x86_64-uv` retains offset `33154560` but size changes `9943 -> 10240`; the other x86-64 PE members also gain 297 bytes. The three ARM64 PE members change `9938 -> 10240` (+302 bytes). All package counts and normalized tuples remain unchanged.
- **m05:** on `elf-x86_64-uv`, the first normalized tuple changes from `["adler2", "2.0.1", "crates.io", null, false, []]` to `["adler2", "2.0.1", "crates.io", "runtime", false, []]`. All carriers contain packages omitting kind: 548 for x86-64/AArch64 ELF, 544 for RISC-V ELF, 558 for PE and 537 for Mach-O.
- **m06:** on `elf-x86_64-uv`, `aes 0.8.4` dependencies change from `[["cfg-if", "1.0.4"], ["cipher", "0.4.4"], ["cpufeatures", "0.2.17"]]` to `[64, 68, 89]`. Every carrier has nonempty dependency edges, so all 16 normalized results differ.

**[INFERENCE] Coverage finding:** the surviving mutants expose missing discrimination for alternate Mach-O segments, the ELF32 path, duplicate named sections and zlib trailers. Survival on these positive carriers does not prove those behaviors correct and is not permission to change the frozen contract. No synthetic carriers or out-of-scope probes were added.

## Layout and package-count comparison: all 16 carriers

The following is the exact table printed by the driver and saved at `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/layout.tsv`. Numbers are decimal. `None` means the PE-only field is inapplicable. Edges are the sum of normalized dependency-list lengths; missing-kind and zlib-unused values are measured on the pristine section.

```text
id	oracle_offset	oracle_size	llvm_offset	llvm_content_size	llvm_raw_size	llvm_virtual_size	packages	edges	missing_kind	zlib_unused
elf-x86_64-uv	39701656	9870	39701656	9870	9870	None	584	3041	548	0
elf-x86_64-uvx	319695	9870	319695	9870	9870	None	584	3041	548	0
elf-aarch64-uv	33685332	9871	33685332	9871	9871	None	584	3042	548	0
elf-aarch64-uvx	287372	9871	287372	9871	9871	None	584	3042	548	0
elf-riscv64-uv	36297611	9737	36297611	9737	9737	None	580	3030	544	0
elf-riscv64-uvx	286025	9737	286025	9737	9737	None	580	3030	544	0
pe-x86_64-uv	33154560	9943	33154560	9943	10240	9943	596	3013	558	0
pe-x86_64-uvx	316416	9943	316416	9943	10240	9943	596	3013	558	0
pe-x86_64-uvw	315904	9943	315904	9943	10240	9943	596	3013	558	0
pe-arm64-uv	32826368	9938	32826368	9938	10240	9938	596	3012	558	0
pe-arm64-uvx	301568	9938	301568	9938	10240	9938	596	3012	558	0
pe-arm64-uvw	301056	9938	301056	9938	10240	9938	596	3012	558	0
macho-x86_64-uv	40876072	9666	40876072	9666	9666	None	573	2974	537	0
macho-x86_64-uvx	308048	9666	308048	9666	9666	None	573	2974	537	0
macho-arm64-uv	28893720	9667	28893720	9667	9667	None	573	2975	537	0
macho-arm64-uvx	298304	9667	298304	9667	9667	None	573	2975	537	0
```

**Layout verdict: holds with the explicit content-size qualification above; fails if rephrased as equality with PE `RawDataSize`.** No real-carrier range disagreement was observed under the oracle's documented content-byte convention.

## Restoration evidence

The following common hash is the SHA-256 of the lane oracle before/after, pristine reference, and active scratch oracle before/after **each** of the seven probes:

```text
f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d
```

Each during-mutation active hash equalled the corresponding mutant specimen hash listed below. Every case recorded `exact_restoration: true`, `restored_stdout_equal: true`, and restored exit 0; all seven pristine exits were also 0. Mutation bytes were activated/restored by bounded `cp` commands, with restoration in `finally`. Retained specimens in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/` are intentionally labeled evidence, not active source. Full per-case before/during/after hashes are in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe-receipts.json`.

All started child commands completed and were reaped; none timed out, and no service/process tree was left running. No installation occurred. Existing tool observations: `timeout 20 llvm-readobj --version`, exit 0 at 2026-10-23T02:47:07.762037Z, stdout `LLVM version 23.1.3`; executable `/usr/bin/llvm-readobj`, SHA-256 `c1d5d7261aa2b25ba5ec4060dd873a6a9808d2912221f97aaf3478f00f3af743`. `timeout 20 python3 --version`, exit 0 at 02:47:07.771623Z, stdout `Python 3.14.8`.

## Source ledger

All source access dates: **2026-10-23**. Only ordinary local reads were used; no web fetch, browser, challenge bypass or target execution. Text-source quotes below are contiguous and at most 25 words each. Carrier binary identities are the 16 frozen SHA-256 values in the manifest and are repeated per detector run in the receipt; no artificial textual line citation is asserted for binary bytes.

| Source URL | SHA-256 | Located quote |
|---|---|---|
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py | f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d | Line 71: `size = rawsize if vsize == 0 else min(vsize, rawsize)` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py | e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a | Line 120: `if meta.get("compressed_bytes") != oracle_sec["size"]:` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv | c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b | Line 1: `wheel_sha256` |

The following generated LLVM text sources are also the inventory of all **16 LLVM stdout artifacts**. Each quote is the contiguous literal `Name: .dep-v0` at the stated line; full numeric fields and exact producing commands are retained in the linked bytes and command receipt.

| Source URL / artifact | SHA-256 | Quote line |
|---|---|---:|
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-x86_64-uv.sections.txt | e4a1e5005848b4a57001aba37e111dfda373ee3c1ce471bd9e648aecf1ce5298 | 512 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-x86_64-uvx.sections.txt | 990255c087819556e7832374f902860db823cfb918959bd9cf9b66c28c01afc6 | 495 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-aarch64-uv.sections.txt | 28fbf7a6469419deb35cce03184a369245d161ac67a686afeac0220dd5e550c5 | 527 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-aarch64-uvx.sections.txt | 08514cd7da6cbd6f985f50de55506cd06ae616aee83493bd822b96d857b541df | 510 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-riscv64-uv.sections.txt | acc2c54a75c440269a2fe8f601672f15b888b22e18ecd3184615b2555e1fbde0 | 460 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/elf-riscv64-uvx.sections.txt | d016515c6efaff9ea1f32f9ecba6c60586450e7378ff2d73d46b5e5b4ef3aa99 | 443 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-x86_64-uv.sections.txt | 62539717c6404d2930dfff9579d1291721f0ecd69e1bfe723104cb3804d5b35b | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-x86_64-uvx.sections.txt | 75f2391a3082b6fecbdf93f230e5be55a2fd50521db7334bca781cb117fb2e72 | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-x86_64-uvw.sections.txt | 05408ff71874c3260a9bf1054175e41e50e4d65a26cd422f5b3b590e4638e026 | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-arm64-uv.sections.txt | 587c4b2b406c73bd6c3b52c44f5a883422cfda9817de1800dcc55377970c2400 | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-arm64-uvx.sections.txt | 4678dd572bfdfd17868f19f686cee23e3bf433b4fc4d2cdfdd6f4ce150641833 | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/pe-arm64-uvw.sections.txt | 4fb29df8f0f3bf20b4771c66c9f0ce41c50e3e3df8dc0703bf4a249defe62e9d | 75 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/macho-x86_64-uv.sections.txt | d73106aa2bdc10a611a8452c2be6405453d564420ffffec5a46a0b7b7a736fc0 | 289 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/macho-x86_64-uvx.sections.txt | 1baefd42715ccd2edc360d25286bf217fb267d5aaf3b17ff808f3992c4742c65 | 255 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/macho-arm64-uv.sections.txt | add7d5aa631134a099bcbb3ee13a3e8893bf9495d63680e38a664daa886a2e81 | 272 |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm/macho-arm64-uvx.sections.txt | 06e9a1272563cb311774391c186be1feaf6fcdf4b5f4de7c15397bcd3994ccbe | 255 |

## Remaining artifact inventory

These **17 artifacts plus the 16 LLVM stdout artifacts above** are every produced file retained in the isolated seat directory. Hashes were produced at **2026-10-23T02:48:11.701807Z–02:48:11.705789Z**, exit **0**, by `timeout 20 sha256sum` with the 33 absolute artifact paths as arguments. No evidence files were modified afterward.

```text
a6ef3a96329cddcf59727fd12b0881d6235b6f90777a32bf88c0c16143b2d83f  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutations.diff
d6001b1673347308a3258bc83b05e2abc708fc4a226386270258b1b4c96577bd  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe-summary.txt
22aaed5061baadb7fcc16594557426e1d583390eb564cbfe3a8608921cfd9b9f  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe-receipts.json
c08697b2d6aab0a3f747ca3c9ba91e5ba82028f64b11e02e1c47144aaa9f6451  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/layout.tsv
f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/rust_dep_oracle.py
b02918d589d825113b0087143bde44d1c3512a16f9f8fa637e19ca7143ecdeb6  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/llvm-commands.json
c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/carriers.tsv
c6d03346ec262be5b032222ed90b194aa84409c83fb2d39e1e9381aafd634651  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/probe.py
d9b644e2cc9db3cc960313718c8a5e019a19240d42f4cb88cc04ce76eba97a21  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/detect.py
f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/pristine.py
0f950b7171a6ecb518a135dbbc3b2c3f64e9acaa18b1c8e6d4c40d4f5ba0f481  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m01-pe-raw-size.py
896d1d48ccd38f8dbcc42b454c9773074f2da14879bc2e68af830b1587c04b2e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m02-macho-any-segment.py
1183af2a473156505728267f1035d5c01d955030f11d55ee06c8dda2bbd1d80d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m03-elf32-offset-size-swap.py
4290844ee9543d6a75ca3e2ca40435a5cac8634e17ab8b7086f91246d0ab326c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m04-first-hit.py
177fdd1cb8decdb32d27b3325f8cf44978ad556fbaf532b9becc025f55994c5e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m05-default-runtime.py
100b17a12cf132e0fc35cf54244cdcc154513bdc193455d277c3b8ef3116fa83  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m06-dependency-indices.py
12f064b1750d090b50f1eb81dae7c89a29b19e22dbd9052f7a48d5a03cba2cb3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutOracle/mutants/m07-require-no-zlib-trailing.py
```

Report: .ufo/waves/round-30/w1/MutOracle.md
