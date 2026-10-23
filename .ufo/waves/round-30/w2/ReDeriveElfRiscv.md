# ReDeriveElfRiscv — round 30 wave 2

Seat: KaidokuR30.ReDeriveElfRiscv (reviewer, attack seat). Attacks R30-C1 (P1-pass) on carriers `elf-riscv64-uv` and `elf-riscv64-uvx`.
The question: do REA 6.5.0's committed and live `inspect_rust_binary` outputs equal the `.dep-v0` contents, as read by a parser I wrote myself? I did not use `tools/round-30/rust_dep_oracle.py` or the counter.

## Verdict

**holds** for both elf-riscv64 carriers (observation). I found no counterexample.

## Method

1. I copied each carrier from `/fast/scratch/hyaku/kaidoku-r30/carriers/<id>` to the scratch `<id>.copy`. The sha256 of each copy equals the `carriers.tsv` value. Carriers were still `chattr +i` and had unchanged sha256 after all runs.
2. Extraction method A: `timeout 120 llvm-objcopy --dump-section .dep-v0=<id>.dep-v0.objcopy.bin <id>.copy <id>.objcopy-out.o`. It ran on the copy with an explicit output object, exit 0 for both.
3. Extraction method B is my own parser in `reader.py`. It reads the ELF64 LE header with `struct`, walks the section headers through `e_shstrndx`, finds `.dep-v0` by name, and slices the bytes at `sh_offset` with length `sh_size`. Python `zlib` inflates the slice and `json` parses it. The script maps the raw cargo-auditable fields to the expected REA fields:
   - `kind` absent → null
   - `dependencies` absent → `[]`
   - `root` absent → false
4. Comparison: `reader.py` compares each package by index on name, version, source, kind, dependencies and root, and flags any extra keys. It checks `root_package_index` against the single raw `root: true` package, and compares edges as an index set and as a `(name, version)` → `(name, version)` set. It also compares file offset, section, compressed and uncompressed sizes, and format version.
5. Live run, once per carrier: `TMPDIR=<scratch>/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`.
6. Live versus committed: `reader.py` compares the committed envelope at `corpus/evidence/round-30/c1/envelopes/<id>.json` and the live envelope against the raw model and against each other: `evidence_id`, `auditable_metadata` and the whole `normalized_result`. `extra.out` also compares the whole `data` object.

## Per-carrier results

| carrier | offset (own / readelf / committed / live) | size (own / committed / live) | packages | edges | root | kind/source | evidence_id live = committed |
|---|---|---|---|---|---|---|---|
| elf-riscv64-uv | 36297611 (0x229db8b) all four equal | 9737 (0x2609); uncompressed 55323, all equal | 580 = 580, 0 field mismatches, order equal | 3030 = 3030; index set and (name,version) set equal; missing 0, extra 0 | idx 459 `uv@0.13.0`, ok | 36 `build`, 544 null; 494 `crates.io`, 86 `local`; all equal | yes: `ev_6fb2c5354740d93ceb96e5c98b807d84bd02bbace617b93e88498eda90e7a371` |
| elf-riscv64-uvx | 286025 (0x45d49) all four equal | 9737 (0x2609); uncompressed 55323, all equal | 580 = 580, 0 field mismatches, order equal | 3030 = 3030; index set and (name,version) set equal; missing 0, extra 0 | idx 459 `uv@0.13.0`, ok | same as uv | yes: `ev_3b6453525097133d138ae225eee86e46af8403b17648dfda4f70abc045ff80bc` |

The table is observation, taken from `<id>.reader.out` and `extra.out`.

## Evidence (command, excerpt, exit code, UTC time)

- **llvm-objcopy plus llvm-readelf** (2026-10-23T03:12:20Z, both exit 0):
  - `[29] .dep-v0 PROGBITS 0000000000000000 229db8b 002609` (uv)
  - `[28] .dep-v0 PROGBITS 0000000000000000 045d49 002609` (uvx)
  - The two dumps have the same sha256, `4ff9dcd8e952ad1d324118f125a4d7763eb037dcc974798a4c78329a00983f47`.
- **REA live** (`npx -y rea-agents@6.5.0 inspect-rust-binary ... --format json --full-output`):
  - uv: exit 0, 03:12:55Z–03:12:56Z, stderr empty.
  - uvx: exit 0, 03:12:56Z–03:12:57Z, stderr empty.
- **`python3 -I -B reader.py <id>.copy <id>.dep-v0.objcopy.bin <committed> <live>`** (03:13:01Z–03:13:02Z, exit 0 for both). Excerpts for each carrier:
  - `objcopy_dump_equal=True`
  - `committed.offset_ok=True size_ok=True uncompressed_ok=True format_ok=True`
  - `committed.packages=580 count_ok=True field_mismatches=0`
  - `committed.root_package_index=459 root=uv@0.13.0 root_ok=True`
  - `committed.edges=3030 edge_set=3030 index_edges_ok=True`
  - `committed.name_version_edges_ok=True missing=0 extra=0`
  - The same lines appear with the `live.` prefix.
  - `evidence_id_equal=True`, `auditable_metadata_equal=True`, `normalized_result_equal=True`
- **Extra probes in `extra.out`** (03:13:16Z, exit 0), for both carriers:
  - `zlib_header 789c eof True unused_data 0`: there are no trailing bytes after the zlib stream inside the section.
  - `duplicate_key_objects 0`
  - `data_equal True`: the whole `data` object matches between live and committed. Only `meta.duration` differs: committed 408ms/350ms, live 163ms/74ms.
- **Read-only git** (03:13:16Z): `git show 24da3459:<envelope>` and `git show HEAD:<envelope>` give the same sha256 as the working file:
  - uv: `1a61dbed…db5f`
  - uvx: `c1e49365…098d`

  `runs.tsv` rows record exit 0, `P1-pass`, `packages=580 edges=3030` for both.

## Findings

No actionable defect for these two carriers.

## Residual risk and verification gaps

- **Inference: the two riscv64 carriers are not independent content evidence.** Their `.dep-v0` payloads are byte-identical and have the same root, `uv@0.13.0`; only the file offset differs. For this payload, the pair tests REA's section location on two ELF layouts, not two different dependency graphs. This is plausibly because `uvx` is a second binary target of the `uv` package, but I did not check that against uv's source (unknown). I did not check the other 14 carriers for the same duplication; that is out of scope.
- **Not exercised by these carriers.** Neither carrier has git or registry sources, `cyclic_dependency_indices` is empty, and the section is not compressed (`sh_flags=0x0`). REA's handling of those cases is untested here.
- **Shared toolchain.** My parser shares Python's `zlib` and `json` with any Python oracle. I only cross-checked ELF section location independently, with llvm-readelf and llvm-objcopy against my own header walk.
- **Not done.** I ran no counter and no mutants, as required for this seat.

## Installs

None.

## Scratch artifacts

All in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveElfRiscv/`, with their sha256:

| file | sha256 |
|---|---|
| reader.py | 61f13f6fae048c098507807424672b4cfaef588a146ac63a2573511c515b5860 |
| elf-riscv64-uv.copy | 63cc77a4904a9e6ba424959f81f7d6648ddabfb071f713fe391be3bc2505efdc |
| elf-riscv64-uvx.copy | 20ee113ad020d7ff6dc3e9afc62985d4684f0dee566d92532e8884f92ea82b9d |
| elf-riscv64-uv.dep-v0.objcopy.bin | 4ff9dcd8e952ad1d324118f125a4d7763eb037dcc974798a4c78329a00983f47 |
| elf-riscv64-uvx.dep-v0.objcopy.bin | 4ff9dcd8e952ad1d324118f125a4d7763eb037dcc974798a4c78329a00983f47 |
| elf-riscv64-uv.objcopy-out.o | bf03b6948e7ca8f023d2350484a626912a7aeb3d9cc913d912467d8b01455c7d |
| elf-riscv64-uvx.objcopy-out.o | 52749e523cfd10a4201619dba36bd577980262895808e5426fc7d317dd54a673 |
| elf-riscv64-uv.live.json | 01770e539310a9838d52e4d1f6bddb41091659f00860a9d8c5f5bc627319e926 |
| elf-riscv64-uvx.live.json | 7fdb7521a78ddfae81b3d8de42bd42816c70191682d5af31bcfd579dcd4f3682 |
| elf-riscv64-uv.live.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| elf-riscv64-uvx.live.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| elf-riscv64-uv.reader.out | 994e6b06bf456ffe6af2958a1f27d408fdfee84b3cf0105b1899dba031326370 |
| elf-riscv64-uvx.reader.out | ff8398659b7bae2b8104717ea7be8e1befe407394eb0a5128fb1dfceca0b4d70 |
| extra.out | 305de380386fed47aa0c4a2722d1e368a8335a9f88b7e993fc5e8d0ccf4a2d2c |

Processes: every REA run had exited; `pgrep -fa rea-agents` returned nothing at 03:13:24Z.
