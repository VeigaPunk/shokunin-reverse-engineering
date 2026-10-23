# R30 wave 2 — ReDerivePeX86 (attack R30-C1 on the pe-x86_64 carriers)

Seat: KaidokuR30.ReDerivePeX86. Scratch: /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDerivePeX86/. Work window 2026-10-23T03:12:04Z to 03:15:30Z.

## Verdict

**holds** for pe-x86_64-uv, pe-x86_64-uvx and pe-x86_64-uvw.

My own reader decoded each carrier's `.dep-v0` section independently. It does not use `tools/round-30/rust_dep_oracle.py` or the counter. Its decoding agrees field by field with both the committed envelope at 24da3459 and a fresh live REA 6.5.0 run, for every package and every edge. Section offset and size agree as well. The live evidence_id equals the committed one for each carrier. I found no counterexample.

## What I attacked and how

1. **Carrier provenance.** I fetched the official wheel and confirmed that its sha256 matches PyPI and carriers.tsv. I then extracted the three members and compared them with the carriers. This matters because pe-x86_64-uvx is one of the four carriers that were rewritten in place during wave 1 (M30-2; mtime 23:44 -03:00 = 02:44Z). carriers.tsv was committed at 0dbabf78 (02:34:24Z), before that rewrite.
2. **Independent extraction with two methods, on copies only:**
   - (a) `pe_dep_reader.py` is my own hand-written parser. It reads `e_lfanew`, the COFF header and the section table (and would resolve `/N` long names through the string table), then selects every section named `.dep-v0`. It uses `min(VirtualSize, SizeOfRawData)` bytes from `PointerToRawData`, inflates them with `zlib.decompressobj`, checking EOF and trailing bytes, and parses the JSON.
   - (b) `llvm-objcopy --dump-section .dep-v0=<out> <copy> <explicit-output-object>`, run on the scratch copy, plus `llvm-readobj --sections` to read the headers.
3. **Comparison done by my reader.** For each package index it compares name, version, source, kind, dependencies and root. A missing `kind` counts as runtime, which matches null. It also compares:
   - the root index;
   - the edge multiset by ((name, version) → (name, version)), against both `dependency_edges` and each package's `dependencies`;
   - the ordered index edge list;
   - `file_offset`, `section_bytes`, `compressed_bytes`, `uncompressed_bytes`, `format_version` and the `file-offset-range` location;
   - `cyclic_dependency_indices`, against my own DFS cycle finder.
4. **Live REA**, once per carrier, with exactly the allowed argv.
5. **Comparator sensitivity.** I planted 16 single defects in scratch copies of the committed uvx envelope, covering version, name, source, kind, root flag, root index, a retargeted edge, a dropped edge, a dropped package dependency, a dropped package, two swapped packages, offset, size, uncompressed size, cyclic list and location end. My reader must reject every one.

## Per-carrier results (observation)

| id | carrier sha256 = tsv = wheel member | .dep-v0 PointerToRawData / VirtualSize / SizeOfRawData (mine; llvm-readobj) | envelope file_offset / section_bytes / compressed_bytes | inflated bytes (mine / env) | packages (json / committed / live) | edges by (name,version) (json / env list / env pkg-deps) | root (json / env) | kind / source / root fields | cycles (mine / env) | committed evidence_id | live evidence_id | equal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pe-x86_64-uv | 2bfbe53d…f162 yes | 33154560 / 9943 / 10240; 0x1F9E600 / 0x26D7 / 10240 | 33154560 / 9943 / 9943 | 56487 / 56487 | 596 / 596 / 596 | 3013 / 3013 / 3013, multisets equal | 455 uv@0.13.0 / 455 | all 596 equal | [] / [] | ev_3cb29ace54adb615cf4cf9495ae753a12fd8240fd6b82b5cdc34e57c85449943 | same | yes |
| pe-x86_64-uvx | 3489d693…c89 yes | 316416 / 9943 / 10240; 0x4D400 / 0x26D7 / 10240 | 316416 / 9943 / 9943 | 56487 / 56487 | 596 / 596 / 596 | 3013 / 3013 / 3013, multisets equal | 455 uv@0.13.0 / 455 | all 596 equal | [] / [] | ev_eaf76ad92d83fa393039570cb113b16120e3369332b6444f39e9f79540351863 | same | yes |
| pe-x86_64-uvw | a6ea6595…d6a yes | 315904 / 9943 / 10240; 0x4D200 / 0x26D7 / 10240 | 315904 / 9943 / 9943 | 56487 / 56487 | 596 / 596 / 596 | 3013 / 3013 / 3013, multisets equal | 455 uv@0.13.0 / 455 | all 596 equal | [] / [] | ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2 | same | yes |

Further observations, all from my reader's output:

- Each PE image has exactly one section whose name resolves to `.dep-v0`, and no other section name contains "dep". The section list is `.text .rdata .data .pdata .dep-v0 .fptable .rsrc .reloc`.
- Machine is 0x8664 and the optional header magic is 0x20b. REA reports architecture `amd64`, format `pe`, 64-bit, little-endian.
- The zlib stream ends with EOF and 0 unused bytes. The 297 padding bytes after VirtualSize are all zero.
- The JSON top-level keys are `format` (=1) and `packages`. Sources are crates.io 509 and local 87. `kind` is absent on 558 packages and "build" on 38; the explicit value "runtime" never appears, so mapping a missing kind to null is the only normalisation in play. Exactly one package has `root: true` (index 455). No (name, version) pair occurs twice, so matching by (name, version) is unambiguous. No dependency index is out of range, no package depends on itself, and there are no cycles.
- The three carriers' `.dep-v0` blobs are byte-identical: blob sha256 54a55231946c5541218392e3aec33fceeb5c9d5f3dc2b6e296bb5f420376016c for both my reader and llvm-objcopy, and inflated sha256 666784faeb60defa0744ef9ae4f2a2fa0c40687abbeb64f7ea78844bac66f6f1. Only the offsets differ.
- Live and committed envelopes have identical `data` objects (Python `==` on the whole `data` dict: True). The only difference is `meta.duration`: uv 381ms committed vs 91ms live, uvx 444ms vs 59ms, uvw 355ms vs 64ms. `ok` is true in both. Operation is `inspect_rust_binary`, and the subject sha256 equals the frozen tsv value.
- Each committed envelope was first added in 24da3459 (2026-10-23T03:04:20Z), and the freeze commit 4ee65c67 (02:35:13Z) is its ancestor. Rows 17–19 of `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` at 92b1dd2d name these three evidence_ids, with 596 packages, 3013 edges, the same file_offset, 9943 compressed bytes and root uv 0.13.0. All of that matches my values.

Sensitivity (observation): `planted=16 caught=16`, exit 0. Fifteen defects were flagged DISAGREE. The dropped-package defect made my reader exit 1 with `IndexError: list index out of range`, which is fail-closed: an edge points at the removed index.

## Evidence (commands, excerpts, exit codes, UTC)

- 03:12:44Z: `cp --no-preserve=all /fast/scratch/hyaku/kaidoku-r30/carriers/$id <scratch>/$id.bin; sha256sum …` (exit 0). Each copy and carrier hashes to its tsv sha256, for example `3489d6931caef4947b338a1d90b3f450915b56ec190e56c13ae33e55da4acc89  …/pe-x86_64-uvx`. `lsattr` on the carriers shows `----i-----`.
- 03:13:06Z: `timeout 300 curl -sS -o uv-0.13.0-py3-none-win_amd64.whl -w '%{http_code} %{size_download}\n' <URL>` printed `200 15819247` (exit 0). The wheel sha256 is `0367b4e0ae4dcef32da4aa2ad2f3853b6ad81d50c187abe50d343d892b8fea21`. The members are `uv.exe 33307440 2bfbe53d…f162`, `uvx.exe 347440 3489d693…c89` and `uvw.exe 346928 a6ea6595…d6a`, each equal to its carrier.
- 03:13:47Z, for each id:
  - `git -C <lane> show 24da3459:…/envelopes/$id.json > committed-$id.json`, which is cmp-equal to both the worktree and HEAD 3502b94c.
  - `timeout 120 python3 -I -B pe_dep_reader.py $id.bin committed-$id.json` returned `reader rc=0`, `"mismatches": []` and `"verdict": "AGREE"` for all three.
  - `timeout 120 llvm-objcopy --dump-section .dep-v0=objcopy-$id.dep-v0 $id.bin objcopy-out-$id.bin` exited `objcopy rc=0` and produced 9943 bytes with sha256 54a55231…016c. Afterwards the carriers' sha256 was unchanged.
- `timeout 60 llvm-readobj --sections $id.bin` (LLVM 23.1.3) reported, for example, `Name: .dep-v0 (2E 64 65 70 2D 76 30 00)`, `VirtualSize: 0x26D7`, `RawDataSize: 10240` and `PointerToRawData: 0x4D400` (uvx). Exit 0.
- 03:14:02Z–03:14:05Z: `TMPDIR=<scratch>/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/$id --format json --full-output` printed `pe-x86_64-uv start=2026-10-23T03:14:02Z end=03:14:03Z rc=0`, `pe-x86_64-uvx … 03:14:03Z–03:14:04Z rc=0` and `pe-x86_64-uvw … 03:14:04Z–03:14:05Z rc=0`. Stderr was 0 bytes each time, and the carriers' sha256 was unchanged afterwards.
- 03:14:0xZ: the live-vs-committed compare printed `evidence_id equal True`, `packages equal True edges equal True` and `data equal True ok True True` for all three. `pe_dep_reader.py $id.bin live-$id.json` returned `rc=0 AGREE []` for all three.
- 03:14:48Z: `timeout 300 python3 -I -B sensitivity.py pe-x86_64-uvx.bin committed-pe-x86_64-uvx.json sens` printed `planted=16 caught=16` (exit 0).

## Out-of-scope side observation

The envelope's `rustc_commit.hashes[].file_offset` points at the leading `/` of `/rustc/<hash>/`, not at the hash itself. For uvx at offset 222904 the bytes are `b'/rustc/'` followed by `b940084d7eb6a299eb4bfeb8e34901bc051e7ac4`. The field is labelled `evidence_kind: inferred`, and P1 does not cover it. This is an observation only, not a defect against R30-C1.

## Residual risk and verification gaps

- **Inference:** the three PE x86_64 carriers carry one identical `.dep-v0` blob. They therefore test REA's section location three times (three different offsets) but its JSON decoding only once. A decoding bug that only shows up in other dependency trees cannot be exposed by this subset.
- **Inference:** the blob lists the full 596-package dependency tree of the `uv` package even inside 347 KB launcher binaries (uvx.exe, uvw.exe). cargo-auditable records the dependency tree of the package being built, not what was actually linked. P1 checks fidelity to the section, not truth about the linked code. That is consistent with REA's own limitation text: "It does not authenticate package names, versions, sources, or the compiler that produced the binary."
- My reader trusts that `min(VirtualSize, SizeOfRawData)` is the content length. This holds here (VirtualSize 9943 < SizeOfRawData 10240, and the zlib stream ends exactly at 9943 with no unused bytes). A PE image with VirtualSize 0, or with VirtualSize larger than the raw size, was not exercised.
- Not checked: the other 13 carriers (assigned to other seats); the C1 counter itself (seat ReRunC1); `province_ok`. I did not run the C2 counter or touch any mutant.

## Source opened

- https://files.pythonhosted.org/packages/b2/00/73abae6cafcdb868d42b2c71bf12c9c2eb06a8d229a09569760c41b7948d/uv-0.13.0-py3-none-win_amd64.whl, accessed 2026-10-23 at 03:13:06Z. The sha256 of the bytes read is 0367b4e0ae4dcef32da4aa2ad2f3853b6ad81d50c187abe50d343d892b8fea21. Quote from the archive member `uv-0.13.0.dist-info/RECORD`, line 7: "uv-0.13.0.data/scripts/uvx.exe,sha256=NInWkxyu9JR7M4odkLP0UJFbVuwZDlbBOuM-VdpKzIk,347440". The served bytes are a ZIP, so this line comes from the inflated member, not from raw served bytes.

## Installs

None.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReDerivePeX86/; full list in SHA256SUMS there)

| file | sha256 |
|---|---|
| pe_dep_reader.py | a6fae880792ed5001a16c52da1d93f53804aa2b5f03992080034bfe66dc21449 |
| sensitivity.py | 8b4e2a0ec0b998d16930eb4065e68893e41e7a3fc5b142516818bf63e219ae8d |
| sensitivity-out.txt | c8f22dc11149fdf2368044578e532a85e9c729f042c073fec2647736119bf8d5 |
| uv-0.13.0-py3-none-win_amd64.whl | 0367b4e0ae4dcef32da4aa2ad2f3853b6ad81d50c187abe50d343d892b8fea21 |
| pe-x86_64-uv.bin (copy) | 2bfbe53d3cc95799e98fa08323b04844fc01d4f8c87dd5c00089e43f6554f162 |
| pe-x86_64-uvx.bin (copy) | 3489d6931caef4947b338a1d90b3f450915b56ec190e56c13ae33e55da4acc89 |
| pe-x86_64-uvw.bin (copy) | a6ea65950009f259a08d95410254326f913dbf9f7f966e743c4d36d69bce9d6a |
| committed-pe-x86_64-uv.json | c0e1aa9114e611f77dfa0f84042756c23da574cdaccb5a51b5f3658c95563c03 |
| committed-pe-x86_64-uvx.json | 1d557589b4771431fdcc4eed481d2bbe41c41667ead0130c2ad45c46175bb0e5 |
| committed-pe-x86_64-uvw.json | 31b5ef7128c2d8e916da0ba2703852872b3923c15fc31594e485d551843006d9 |
| live-pe-x86_64-uv.json | 3cb6d35fa56d7a24e720fd4a02033582cb7ee9090fa0209cf4c8f9f306bb7803 |
| live-pe-x86_64-uvx.json | b34957d273c7880891e325b6495bb1caae8aef05ae25834e39eeacf1ce9e3348 |
| live-pe-x86_64-uvw.json | c3a81fbbd7e66e401727732b6fb8bb95aea8ddbcdbf4e7cf1179189359e621dc |
| live-*.stderr (each, empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| mine-vs-committed-pe-x86_64-uv.json (= mine-vs-live) | e4ddfad9872efffc7590ba8291d64933463ae52b9682133f7d78f50a38e91047 |
| mine-vs-committed-pe-x86_64-uvx.json (= mine-vs-live) | 0c0f1c8598fe7e186b9f6778dbae279a909fda51e76c2fa89d3fb3f630709b04 |
| mine-vs-committed-pe-x86_64-uvw.json (= mine-vs-live) | 0f12944c1366b8b1bf38ba54fa99b2ae31cc893d0d900c921dd53131af704d45 |
| objcopy-pe-x86_64-{uv,uvx,uvw}.dep-v0 (each) | 54a55231946c5541218392e3aec33fceeb5c9d5f3dc2b6e296bb5f420376016c |
| objcopy-out-pe-x86_64-uv.bin | f34dcdeb93f31f7df1d95007b56743a8abed72389db2560492c60882097a0086 |
| objcopy-out-pe-x86_64-uvx.bin | bde137ebe9de5570449c2322694cc7713b14d7f5a394dfb4292759b94a6daa27 |
| objcopy-out-pe-x86_64-uvw.bin | 902cedfc1805ba214b3796e196637a5a4f5b0377d241ee4728d6ef952dfecd3d |
| sens/sens-m_*.json (16 planted envelopes) | listed in SHA256SUMS |

No processes are left running. Nothing was written inside the lane except this report.
