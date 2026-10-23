# ReDerivePeArm — round 30 wave 2: re-derive R30-C1 on the pe-arm64 carriers

Seat: KaidokuR30.ReDerivePeArm (reviewer, attack seat). Window 2026-10-23T03:12:21Z to 03:14:29Z.
Attacked: R30-C1 / P1-pass on `pe-arm64-uv`, `pe-arm64-uvx`, `pe-arm64-uvw`. The question is whether REA 6.5.0's committed and live `inspect_rust_binary` output equals the `.dep-v0` contents, judged by a reader written for this seat. I did not use `tools/round-30/rust_dep_oracle.py` or the counter.

## Verdict: HOLDS (all 3 pe-arm64 carriers)

No counterexample was found. On each carrier, my reading of `.dep-v0` matches both the committed envelope and the live REA envelope. It matches on every package field (name, version, source, kind, root), on the dependency edges compared by (name, version), on the root package index, on the flat edge list, and on file_offset, section_bytes, compressed_bytes and uncompressed_bytes. Each live run returned the same evidence_id as its committed envelope.

## Method (observation)

1. I copied each carrier into `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDerivePeArm/bytes/<id>`. The copies' sha256 values equal the frozen `carriers.tsv` values. The originals are `----i---` (immutable) and were never written. All tools ran on the copies, except the one allowed REA run on each original path.
2. `pe_dep_reader.py` is my own stdlib-only reader (`struct` and `zlib`). It parses MZ, then `e_lfanew`, the COFF header and the section table. It selects the single section named `.dep-v0` and takes `min(VirtualSize, SizeOfRawData)` bytes from `PointerToRawData`. It then runs zlib inflate and checks for stream EOF, unused trailing bytes, nonzero padding, and whether inflating the padded block gives the same result.
3. Cross-check: `llvm-objcopy --dump-section .dep-v0=out/<id>.objcopy.section bytes/<id> out/<id>.objcopy.obj`, always with an explicit output object and run on the copy. I also ran `llvm-readobj --section-headers` on the copy.
4. `compare.py` compares packages. It maps an absent `kind` to null and an absent `root` to false, and uses (name, version) keys and edge sets of (from name, from version, to name, to version). It also checks that the ordered lists are identical. `compare_hdr.py` compares the header fields, `root_package_index`, `dependency_edges` and evidence_id.
5. Live REA, once per carrier: `TMPDIR=.../ReDerivePeArm/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/<id> --format json --full-output`.

## Section extraction (observation)

Command: `timeout 120 python3 -I -B pe_dep_reader.py bytes/<id> out`. Exit 0 for each carrier, 2026-10-23T03:12:45Z.

| id | machine | PointerToRawData | VirtualSize | SizeOfRawData | zlib consumed | inflated | packages |
|---|---|---|---|---|---|---|---|
| pe-arm64-uv | 0xaa64, PE32+ | 32826368 | 9938 | 10240 | 9938 (EOF, 0 unused) | 56487 | 596 |
| pe-arm64-uvx | 0xaa64, PE32+ | 301568 | 9938 | 10240 | 9938 (EOF, 0 unused) | 56487 | 596 |
| pe-arm64-uvw | 0xaa64, PE32+ | 301056 | 9938 | 10240 | 9938 (EOF, 0 unused) | 56487 | 596 |

- On every carrier, the 302 bytes of raw padding are all zero, and inflating the padded block gives the same JSON.
- Excerpt: `"payload_bytes": 9938, "zlib_consumed": 9938, "zlib_eof": true, "unused_after_stream": 0, "padding_nonzero": false`.
- My section bytes and the llvm-objcopy dumps are byte-identical on all three carriers: sha256 `01e34aaa103ff0e6dd4433a23b0d661d5458a0306cd69473497b1cacf54db17a` (objcopy exit 0 each).
- `llvm-readobj` agrees, for example on pe-arm64-uvx: `VirtualSize: 0x26D2`, `RawDataSize: 10240`, `PointerToRawData: 0x49A00`.
- The inflated JSON is identical on all three carriers: sha256 `651b3840…dc76`. Top-level keys are `["format","packages"]`, with `format` 1.
- The JSON contains 38 packages with `kind: "build"` and none with an explicit `"runtime"`. `root: true` appears exactly once, at index 455, `uv 0.13.0`. Sources are `crates.io` and `local` (the `uv-*` workspace crates at 0.0.92 plus `uv` 0.13.0).
- A third, independent source for the size: each image has two `.dep-v0\0` byte hits. One is the section header (file offset 696 in uv, 680 in uvx and uvw). The other is a linker debug record holding RVA, size and name, for example in uv: `\x00\xd0\xf5\x01\xd2&\x00\x00.dep-v0\0`, meaning RVA 0x1F5D000 and size 0x26D2 = 9938. This matches the section header. There is no second `.dep-v0` section (my reader requires exactly one).

## Per-carrier agreement (observation)

Commands:
- `compare.py <id> out/<id>.json <lane>/corpus/evidence/round-30/c1/envelopes/<id>.json out/<id>.live.json` at 03:13:17Z, exit 0.
- `compare_hdr.py …` at 03:13:40Z, exit 0.

The committed envelopes in the worktree are byte-identical to `git show 24da3459:…` (`cmp` was silent).

| id | packages mine / committed / live | edges by (name, version) | root | kind/source attributes | file_offset | section and compressed bytes | uncompressed | flat `dependency_edges` |
|---|---|---|---|---|---|---|---|---|
| pe-arm64-uv | 596 / 596 / 596, ordered-identical | 3012 = 3012 = 3012, no edges on only one side | 455 `uv 0.13.0` = 455 | 0 mismatches | 32826368 = 32826368 | 9938 = 9938 | 56487 = 56487 | 3012, equal |
| pe-arm64-uvx | 596 / 596 / 596, ordered-identical | 3012 = 3012 = 3012 | 455 = 455 | 0 mismatches | 301568 = 301568 | 9938 = 9938 | 56487 = 56487 | 3012, equal |
| pe-arm64-uvw | 596 / 596 / 596, ordered-identical | 3012 = 3012 = 3012 | 455 = 455 | 0 mismatches | 301056 = 301056 | 9938 = 9938 | 56487 = 56487 | 3012, equal |

Excerpt for each id: `"mine_vs_committed": {... "attr_mismatch": [], "edge_count": [3012, 3012], "edges_only_left": [], "edges_only_right": [], "ordered_identical": true, "equal": true}`, and the same for `mine_vs_live`. (name, version) is unique in all three lists (`"nv_unique": [true, true]`). That makes the comparison by (name, version) equivalent to the multiset in P1.

## Live and committed evidence_id (observation)

Live runs: uv 03:12:52Z to 03:12:53Z, uvx 03:12:53Z to 03:12:54Z, uvw 03:12:54Z to 03:12:55Z. Live stderr was empty (sha256 `e3b0c442…b855`) and every envelope has `"ok": true` and `operation: inspect_rust_binary`. The live subject sha256 equals the frozen sha256 for each carrier.

| id | committed evidence_id | live evidence_id | equal | `data` keys that differ |
|---|---|---|---|---|
| pe-arm64-uv | ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e | the same | true | [] (`normalized_result` equal) |
| pe-arm64-uvx | ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc | the same | true | [] |
| pe-arm64-uvw | ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9 | the same | true | [] |

Only `meta.duration` differs: 479/412/360 ms committed against 150/65/64 ms live.

Other P1 clauses, checked read-only at 03:14:23Z:
- Each envelope was first added in 24da3459a5b4…, which descends from the freeze commit 4ee65c67 (`git merge-base --is-ancestor` succeeded) and is not the freeze commit.
- Each evidence_id is named in `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` (found by `git grep` at HEAD).
- `claims.json` and `carriers.tsv` are unchanged between 4ee65c67 and HEAD (`git diff --quiet` succeeded).
- `runs.tsv` records exit 0 for all three committed runs (03:00:04Z to 03:00:15Z, `P1-pass packages=596 edges=3012`).

Extra check, outside P1: REA's `rustc_commit` (`b940084d7eb6a299eb4bfeb8e34901bc051e7ac4`, evidence_kind `inferred`) is confirmed by my scan of the copies. `/rustc/b940084d…/` sits exactly at the offsets REA reports: 28200952 in uv, 221240 in uvx, 220688 in uvw. It is the only 40-hex rustc hash in each image (93, 41 and 41 occurrences respectively).

## Verification gaps and residual risk

- **Unknown:** the process exit code of my three live REA runs. My wrapper's `exit=$?` was expanded after a `$(date …)` substitution in the same `echo`, so it recorded `date`'s status. I did not rerun, because the assignment allows one live run per carrier. Inference: REA exited 0, since each envelope is `ok: true`, stderr is empty, and the committed `runs.tsv` rows record exit 0. The live exit-0 clause of P1 is therefore inferred, not observed, by this seat.
- **Observation, a coverage note rather than a defect:** all three pe-arm64 carriers embed byte-identical `.dep-v0` payloads, rooted at `uv 0.13.0`. Inference: `uvx.exe` and `uvw.exe` are bin targets of the `uv` package. So the three carriers test three distinct section offsets and image layouts, but only one package graph. Agreement on uvx and uvw is not independent evidence about package decoding beyond what uv gives.
- My reader only handles PE with a short (8-byte) section name, which is the only case these carriers exercise. The ELF and Mach-O carriers are out of scope for this seat.
- The P1 clause "the round-30 entry names that evidence_id" was checked by literal `git grep`, not by parsing the entry.
- No LSP applies here: these are binary artifacts and JSON, with no source changes under review.

## Tooling and installs

None. I used preinstalled `/usr/bin/llvm-objcopy`, `/usr/bin/llvm-readobj`, Python 3.14.8, and `npx -y rea-agents@6.5.0`, which runs through npx's cache and installs nothing. No lane files were written except this report. No processes were left running (`pgrep` empty at 03:14:29Z), and the carrier sha256 values were unchanged after the REA runs.

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDerivePeArm/`)

| path | sha256 |
|---|---|
| pe_dep_reader.py | 2ace8850817b710852a7392514b8429c198f73826c2a4f298fc7b3e2c15a1f34 |
| compare.py | 836e99fbfc7ead165f4032e6ea9416659cc863c06b63e3d932ea34c685a9505a |
| compare_hdr.py | ad1910551f318a44954e1bbccdb884aebf211ab9b2c804d2353928630420c3da |
| out/reader.txt | 9c6d0b3feb45bf3a81420ef3bca6e8c37152c9354119c15c949c3caaf069db63 |
| out/objcopy.txt | 38ce929b523e86cc31eb2d6d895c639b87a40f33ee788c66f299e564ce1a8a1b |
| out/compare.txt | a074cec7f917ee14253ca3bc73a728a11d341d972a83e9954d6824a24f8afc75 |
| out/compare_hdr.txt | 62909e275f03e48477624d5ea3813ae63a3f9f0a37149afdf9ba5188e3056dcd |
| out/live-runs.txt | 3c77b04f1adcfe6faff223b5dbefea7c03fd48ec482594ac1952a972bba5ce24 |
| out/pe-arm64-{uv,uvx,uvw}.section and .objcopy.section | 01e34aaa103ff0e6dd4433a23b0d661d5458a0306cd69473497b1cacf54db17a |
| out/pe-arm64-{uv,uvx,uvw}.json (inflated) | 651b3840a6591c80a098eda914ae06ba6cf5b82e993857b0f82446faea79dc76 |
| out/pe-arm64-uv.live.json | 73f81da78a875cd4db8372c194d2b49ea93e8742d6d481549af626e43e42b465 |
| out/pe-arm64-uvx.live.json | adbb4dee8978bd6d4699a827643c691972b1776007b9194a366a046de49d358c |
| out/pe-arm64-uvw.live.json | 8168d3262bc1dda29c218dae9a37f6d3f010743d139b4cd091ed2a3eedba694f |
| out/pe-arm64-{uv,uvx,uvw}.live.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| out/pe-arm64-uv.objcopy.obj | b5c96678a89bd5ee6aac04d28e9a5dcc463222c95b9edb776f2dfa45bee809dc |
| out/pe-arm64-uvx.objcopy.obj | 9938c60618abbf1afad249d9774a4db75fab6591b7d6e55e81572d3a81ee3959 |
| out/pe-arm64-uvw.objcopy.obj | b92e1f0f264e7d0484dfbe7846e4cba3fd52efe6162bc2323f2a5f6f11c3f23a |
| bytes/pe-arm64-{uv,uvx,uvw} (copies) | equal to the frozen carrier sha256 values |
