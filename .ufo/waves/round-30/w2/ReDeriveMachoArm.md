# R30 wave 2 — ReDeriveMachoArm (attack R30-C1 on the macho-arm64 carriers)

Seat: `KaidokuR30.ReDeriveMachoArm`. Attacked: R30-C1 / predicate P1 on carriers `macho-arm64-uv` and `macho-arm64-uvx`. I used my own reader, not `tools/round-30/rust_dep_oracle.py` or the counter.

**Verdict: holds.** For both carriers I found no counterexample. Packages, edges, root, kind, source, offset, size and evidence_id all agree exactly between the section bytes I extracted myself, the committed envelope (measured revision 92b1dd2d), and a fresh live REA 6.5.0 run.

## Method

- The carriers (mode 0444, `chattr +i`, verified by `lsattr`) were copied with `cp` into `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveMachoArm/<id>.bin`. The sha256 of each copy equals carriers.tsv: `4cd60b63…d240` for uv and `360f023f…223b` for uvx (observation, 2026-10-23T03:12:18Z).
- First extraction method: my own stdlib Mach-O parser, `rederive.py`. It reads the `mach_header_64`, walks the `LC_SEGMENT_64` commands and their `section_64` records, finds `.dep-v0`, and takes bytes `[offset, offset+size)` from the copy, which is opened read-only. It then runs `zlib.decompressobj`, `json.loads`, and builds an index-preserving package model: an omitted kind becomes null, an omitted root becomes false, and omitted dependencies become `[]`. It recomputes the edges from each package's dependency list, finds cycles with an iterative DFS, and looks for `/rustc/<40hex>/` strings.
- Second extraction method: `timeout 120 llvm-objcopy --dump-section __DATA,.dep-v0=<id>.objcopy.section.bin <id>.bin <id>.objcopy-out.o`, always on the copy and always with an explicit output object. Both methods exited 0, and `cmp` reported the two sections identical for both ids. The carrier sha256 values were unchanged afterwards (observation, 03:13:22Z).
- `llvm-otool -l` cross-check on uvx: `sectname .dep-v0 / segname __DATA / size 0x00000000000025c3 / offset 298304` (observation).
- Live REA, one run per carrier, both started 2026-10-23T03:12:23Z: `TMPDIR=<seat>/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`. Both runs exited 0 with empty stderr.
- Comparator command: `timeout 300 python3 -I -B rederive.py <id>.bin <committed envelope> live-<id>.json <id>`. Both runs exited 0 at 03:13:09Z. Full results are in `<id>.result.json`.

## Per-carrier results (all observations; source: `<id>.result.json`)

| check | macho-arm64-uv | macho-arm64-uvx |
|---|---|---|
| Mach-O header | magic feedfacf, cputype 0x100000c (arm64), filetype 2, ncmds 22 | same magic/cputype/filetype, ncmds 16 |
| `.dep-v0` sections found | 1 (`__DATA,.dep-v0`) | 1 (`__DATA,.dep-v0`) |
| my offset / size | 28893720 / 9667 | 298304 / 9667 |
| REA file_offset / section_bytes / compressed_bytes (committed = live) | 28893720 / 9667 / 9667 | 298304 / 9667 / 9667 |
| `locations` file-offset-range | start 28893720, end 28903387: agree | start 298304, end 307971: agree |
| section sha256 (both extraction methods) | `8dc0a262…7cc3` | `8dc0a262…7cc3` |
| zlib header / trailing bytes after the stream | 789c / 0 | 789c / 0 |
| inflated bytes (mine = REA uncompressed_bytes) | 54678 = 54678 | 54678 = 54678 |
| JSON top-level keys, format | `format, packages`, format 1 = REA format_version 1 | same |
| packages (mine / committed / live) | 573 / 573 / 573 | 573 / 573 / 573 |
| packages exactly equal, ordered, every field (name, version, source, kind, root, dependency index list) | true (committed), true (live), 0 field diffs | true, true, 0 field diffs |
| duplicate (name, version) pairs | 0, so (name, version) edges are unambiguous | 0 |
| edges (mine / committed / live) | 2975 / 2975 / 2975 | 2975 / 2975 / 2975 |
| edges equal, ordered (from, to) | true / true | true / true |
| edges equal as (name, version) → (name, version) | true / true | true / true |
| edge index out of range | 0 | 0 |
| root | my roots [458] = REA root_package_index 458 = `uv 0.13.0`, source `local` | same |
| kind | 537 omitted (REA null), 36 `build`, exact per package | same |
| source | 487 `crates.io`, 86 `local`, exact per package | same |
| cycles (my DFS / REA cyclic_dependency_indices) | [] / [] | [] / [] |
| subject sha256 = carriers.tsv sha256 | true | true |
| envelope `ok`, operation | true, `inspect_rust_binary` | true, `inspect_rust_binary` |
| evidence_id committed | `ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d` | `ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7` |
| evidence_id live | identical | identical |
| live `data` vs committed `data` | deep-equal; no differing key | deep-equal; no differing key |

The live and committed files differ only in `meta.duration`: uv 147ms live vs 400ms committed, uvx 78ms live vs 407ms committed. That field is outside `data`, so the file sha256 values differ but `data` is equal.

## The other P1 clauses (observation; read-only git in the lane, 03:13:37Z)

- **Committed after the freeze:** `git log --diff-filter=A` shows both envelopes first added in `24da3459` ("round-30: data (16 C1 and 19 C2 live REA 6.5.0 envelopes and runs)…"). Freeze `4ee65c67` is an ancestor of `24da3459`, and the two commits are distinct.
- **Envelope unchanged at the measured revision:** `git show 92b1dd2d:<envelope> | sha256sum` equals the working-tree sha256 (uv `f70877a4…0597`, uvx `be90ed53…b0f`). The last change to both envelopes is `24da3459`.
- **The entry names the evidence ids:** `git grep` at 92b1dd2d finds `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:64` = `| macho-arm64-uv | \`ev_7f9ac67a…b35d\` | 573 | 2975 | 28893720 | 9667 | uv 0.13.0 | P1-pass |`. Line 65 is the same row for uvx with `ev_6fcab3d4…87f7` and offset 298304. Every number in both rows matches my own reading.
- The committed `.stderr` files for both carriers are 0 bytes.

## Counterexamples to P1

None.

## Informational findings outside P1 (observation; not counterexamples)

1. **`rustc_commit.hashes[].file_offset` marks the start of the `/rustc/` path, not the 40-hex hash.**
   - uvx: committed `{'hash': 'b940084d…c4', 'file_offset': 244531}`. The bytes at 244531 are `b'/rustc/b940084d7eb6a299eb4bfeb8e34901bc051e7ac4/'`, so the hash itself starts at 244538 (+7).
   - uv: file_offset 27145545, and the hash starts at 27145552.
   - The hash value does match the bytes. REA reports only the first of 47 (uvx) or 105 (uv) occurrences.
   - This is consistent with the limitation text, which says the commit is "inferred from a /rustc/<40-hex>/ path". Whether "offset of the path" is the intended meaning is unknown, and P1 does not cover `rustc_commit`.
2. **The two carriers are not independent in content.** Both macho-arm64 carriers embed byte-identical `.dep-v0` sections (sha256 `8dc0a262…7cc3`), and both have root `uv 0.13.0`; uvx does not get its own `uvx` root. As tests, they differ only in the containing image and section offset (inference: uvx is a second bin target of the same `uv` package, so it inherits the same audit data). This narrows how much variety the 16/16 count covers, but it does not falsify P1.

## Residual risk and verification gaps

- My reader and REA both follow the same cargo-auditable JSON shape (`format`, `packages[]` with index-based `dependencies`). A shared misreading of the format spec would not be caught. Mitigation: the inflated JSON is parsed raw, and the edges are cross-checked by (name, version).
- I checked only `LC_SEGMENT_64` in a thin image. There are no fat or multi-arch macho-arm64 carriers in the frozen list, so fat-binary handling is unexercised here.
- I did not run the C1 counter. That is not my seat, and the comparison above is independent of it.
- REA ran on the immutable shared carrier paths, as the assignment allows, which are read-only. My own parsing and llvm-objcopy ran only on the copies.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDeriveMachoArm/`)

| file | sha256 |
|---|---|
| rederive.py | b07c1028d7caab6cdf0b1b439174dabdb7b6be10647d07578793f2c8247a34ec |
| macho-arm64-uv.bin (copy) | 4cd60b63cf3221572ccb0e171cfc3404cede505ce8f701b6520439476bc1d240 |
| macho-arm64-uvx.bin (copy) | 360f023f4f5354b35e5240d081b7c40fc6b489692e7b178cad697380d753223b |
| macho-arm64-uv.section.bin | 8dc0a26277878dc80305fa1f7c5d0387f14527f6323746dd9da1e0f1daf57cc3 |
| macho-arm64-uvx.section.bin | 8dc0a26277878dc80305fa1f7c5d0387f14527f6323746dd9da1e0f1daf57cc3 |
| macho-arm64-uv.objcopy.section.bin | 8dc0a26277878dc80305fa1f7c5d0387f14527f6323746dd9da1e0f1daf57cc3 |
| macho-arm64-uvx.objcopy.section.bin | 8dc0a26277878dc80305fa1f7c5d0387f14527f6323746dd9da1e0f1daf57cc3 |
| macho-arm64-uv.objcopy-out.o | 17798721cd0d776e4de06a936fc998e93879e76914336051b5cfcb6b49cf84b6 |
| macho-arm64-uvx.objcopy-out.o | 75660bc4e4780914187f15058e8a414d8ff94a9202b0dbda5f6796cd9a1ea1c8 |
| macho-arm64-uv.inflated.json | 41bdcbf2db8232445ed4e291d16c00dffc913e89c237cf77be16f83e7e718489 |
| macho-arm64-uvx.inflated.json | 41bdcbf2db8232445ed4e291d16c00dffc913e89c237cf77be16f83e7e718489 |
| macho-arm64-uv.result.json | 35d4dcd00ec8db87ef965b35485bb1560c806f398120c890e12295cafa646d72 |
| macho-arm64-uvx.result.json | fcb756b424b82f9528f9d9d39a1f8c94bebdf0805b27bfb1bd4034ad23237e0c |
| macho-arm64-uv.stdout | e5a2f1de6f9e14cf4fb99885756731edf88dea134add9feb950a9f5011b9ff6c |
| macho-arm64-uvx.stdout | e06133e64098e1ff805f8f31d4bbaeb194bd2d8f2753fed4eb5443b88626e55a |
| live-macho-arm64-uv.json | 3f807c786c6ff602627d6ea04af6cac36f06105a8c2c6fe5e0fe72212fdb7f98 |
| live-macho-arm64-uvx.json | dec04c070aabd1b7b66075d5f0e5cdd36121e12eea579b3378999bda23e92eea |
| live-macho-arm64-uv.stderr / live-macho-arm64-uvx.stderr (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

Installs: none. Processes: every command ran under `timeout`, and `pgrep -af rea-agents` at the end returned "no rea processes". No lane, fleet, or Git/jj writes were made; this report is the only file written in the lane.
