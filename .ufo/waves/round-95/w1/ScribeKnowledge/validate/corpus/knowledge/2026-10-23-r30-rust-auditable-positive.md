source: S089 (cargo-auditable `.dep-v0` format, README/PARSING.md/schema at `e2316a67`); S090 (REA 6.5.0 reader code, for the inference in Results); S091 (PyPI release record for uv 0.13.0, the wheel digests behind every carrier)
verified-at: 2026-10-23, round 30 (R30-C1); 16 live `rea-agents@6.5.0` `inspect-rust-binary` calls 2026-10-23T02:59:33+00:00–2026-10-23T03:00:31+00:00 (`corpus/evidence/round-30/c1/runs.tsv`), all after the freeze commit `4ee65c67` (02:35:13Z) and after the control receipts `f39f4530`
recheck: `python3 -I -B tools/round-30/c1-rust-positive.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>` (re-runs REA live on the 16 carriers at `/fast/scratch/hyaku/kaidoku-r30/carriers/`, which must be present: re-extract an absent one by hand from its S091 wheel (`carriers.tsv` names wheel and member); the counter exits 2 on an absent or altered carrier; target `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0)

# `inspect-rust-binary` on cargo-auditable images: REA 6.5.0 reads the full `.dep-v0` dependency graph exactly on ELF, PE and thin Mach-O (16 of 16)

## Claim

R30-C1 is the coverage claim: PROVINCE Core gains the positive input class of REA operation `inspect_rust_binary` (an image that carries a cargo-auditable `.dep-v0` section) on three container formats (ELF x86_64/aarch64/riscv64, PE x86_64/arm64, thin Mach-O x86_64/arm64). At the base the lane holds only null-metadata runs of this verb (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md`: no `.dep-v0` found) and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` names `inspect-rust-binary` 0 times.

## Carriers

The frozen list is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv`. SHA-256 column below is the first 12 hex characters of each frozen member digest; sizes are bytes.

| id | format | arch | wheel | sha256 prefix | size |
|---|---|---|---|---|---:|
| elf-x86_64-uv | elf | x86_64 | uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | `3e801df89243` | 39714040 |
| elf-x86_64-uvx | elf | x86_64 | uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | `2e9105ad9481` | 332008 |
| elf-aarch64-uv | elf | aarch64 | uv-0.13.0-py3-none-manylinux_2_28_aarch64.whl | `a72b2853c84a` | 33697800 |
| elf-aarch64-uvx | elf | aarch64 | uv-0.13.0-py3-none-manylinux_2_28_aarch64.whl | `e3ef59b327cd` | 299768 |
| elf-riscv64-uv | elf | riscv64 | uv-0.13.0-py3-none-manylinux_2_31_riscv64.whl | `63cc77a4904a` | 36309624 |
| elf-riscv64-uvx | elf | riscv64 | uv-0.13.0-py3-none-manylinux_2_31_riscv64.whl | `20ee113ad020` | 297968 |
| pe-x86_64-uv | pe | x86_64 | uv-0.13.0-py3-none-win_amd64.whl | `2bfbe53d3cc9` | 33307440 |
| pe-x86_64-uvx | pe | x86_64 | uv-0.13.0-py3-none-win_amd64.whl | `3489d6931cae` | 347440 |
| pe-x86_64-uvw | pe | x86_64 | uv-0.13.0-py3-none-win_amd64.whl | `a6ea65950009` | 346928 |
| pe-arm64-uv | pe | arm64 | uv-0.13.0-py3-none-win_arm64.whl | `885a370550b1` | 32984368 |
| pe-arm64-uvx | pe | arm64 | uv-0.13.0-py3-none-win_arm64.whl | `15153057351d` | 332592 |
| pe-arm64-uvw | pe | arm64 | uv-0.13.0-py3-none-win_arm64.whl | `af15b1a1c01c` | 332080 |
| macho-x86_64-uv | macho | x86_64 | uv-0.13.0-py3-none-macosx_10_12_x86_64.whl | `f31d4fdce12a` | 41406880 |
| macho-x86_64-uvx | macho | x86_64 | uv-0.13.0-py3-none-macosx_10_12_x86_64.whl | `f25305942412` | 344160 |
| macho-arm64-uv | macho | arm64 | uv-0.13.0-py3-none-macosx_11_0_arm64.whl | `4cd60b63cf32` | 29134784 |
| macho-arm64-uvx | macho | arm64 | uv-0.13.0-py3-none-macosx_11_0_arm64.whl | `360f023f4f53` | 334512 |

The carriers are 16 members of seven official uv 0.13.0 PyPI wheels. Host `/home/vgpnk/.local/bin/uv` and `/home/vgpnk/.local/bin/uvx` are byte-identical to the manylinux x86_64 members and are not separate carriers.

## Method

- **Independent oracle:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` decodes the package metadata from each carrier's `.dep-v0` section. It supplies the section offset and compressed size plus the package/dependency tuples used for comparison; it shares the cargo-auditable format specification with REA, not implementation code.
- **REA:** The C1 counter invokes REA 6.5.0 `inspect-rust-binary` live for every frozen carrier and compares its envelope to the oracle. The carriers are read as static bytes only; none is executed. A committed envelope is a record that must agree with the live run, not a substitute for that run.
- **Predicate P1-pass (verbatim from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json`):**

> A carrier passes when its live REA 6.5.0 inspect-rust-binary run exits 0 with an ok envelope whose operation is inspect_rust_binary and whose subject sha256 equals the carrier's frozen sha256, and whose auditable_metadata package list equals, as a multiset of (name, version, source, kind, root, dependency (name, version) set) tuples, the non-empty list that the independent oracle decodes from the carrier's own .dep-v0 section, with REA's file_offset and compressed_bytes equal to the oracle's section offset and size; and its committed envelope, first added after the freeze commit, carries the same evidence_id and package multiset, and the round-30 entry names that evidence_id.

## Results

Observation. Every carrier passed P1: REA's `auditable_metadata.packages` equals the oracle's decoding as a multiset of (name, version, source, kind, root, dependency (name, version) set) tuples, and REA's `file_offset` and `compressed_bytes` equal the oracle's section offset and content size (for PE the content size is `min(VirtualSize, SizeOfRawData)`, not the padded raw size). Every envelope reports `format_version` 1, a single root package `uv 0.13.0`, and `kind` values `null` (absent in the section) or `build`. Counter stdout `carriers=16 pass=16 target=16` (`.ufo/waves/round-30/after/c1-rust-positive-at-24da3459.txt`, `…-at-92b1dd2d.txt`; per-run rows in `corpus/evidence/round-30/c1/runs.tsv`); envelopes `corpus/evidence/round-30/c1/envelopes/<id>.json`, stderr beside each.

| id | evidence_id | packages | edges | file_offset | compressed_bytes | root package | verdict |
|---|---|---:|---:|---:|---:|---|---|
| elf-x86_64-uv | `ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33` | 584 | 3041 | 39701656 | 9870 | uv 0.13.0 | P1-pass |
| elf-x86_64-uvx | `ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e` | 584 | 3041 | 319695 | 9870 | uv 0.13.0 | P1-pass |
| elf-aarch64-uv | `ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e` | 584 | 3042 | 33685332 | 9871 | uv 0.13.0 | P1-pass |
| elf-aarch64-uvx | `ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8` | 584 | 3042 | 287372 | 9871 | uv 0.13.0 | P1-pass |
| elf-riscv64-uv | `ev_6fb2c5354740d93ceb96e5c98b807d84bd02bbace617b93e88498eda90e7a371` | 580 | 3030 | 36297611 | 9737 | uv 0.13.0 | P1-pass |
| elf-riscv64-uvx | `ev_3b6453525097133d138ae225eee86e46af8403b17648dfda4f70abc045ff80bc` | 580 | 3030 | 286025 | 9737 | uv 0.13.0 | P1-pass |
| pe-x86_64-uv | `ev_3cb29ace54adb615cf4cf9495ae753a12fd8240fd6b82b5cdc34e57c85449943` | 596 | 3013 | 33154560 | 9943 | uv 0.13.0 | P1-pass |
| pe-x86_64-uvx | `ev_eaf76ad92d83fa393039570cb113b16120e3369332b6444f39e9f79540351863` | 596 | 3013 | 316416 | 9943 | uv 0.13.0 | P1-pass |
| pe-x86_64-uvw | `ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2` | 596 | 3013 | 315904 | 9943 | uv 0.13.0 | P1-pass |
| pe-arm64-uv | `ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e` | 596 | 3012 | 32826368 | 9938 | uv 0.13.0 | P1-pass |
| pe-arm64-uvx | `ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc` | 596 | 3012 | 301568 | 9938 | uv 0.13.0 | P1-pass |
| pe-arm64-uvw | `ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9` | 596 | 3012 | 301056 | 9938 | uv 0.13.0 | P1-pass |
| macho-x86_64-uv | `ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10` | 573 | 2974 | 40876072 | 9666 | uv 0.13.0 | P1-pass |
| macho-x86_64-uvx | `ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0` | 573 | 2974 | 308048 | 9666 | uv 0.13.0 | P1-pass |
| macho-arm64-uv | `ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d` | 573 | 2975 | 28893720 | 9667 | uv 0.13.0 | P1-pass |
| macho-arm64-uvx | `ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7` | 573 | 2975 | 298304 | 9667 | uv 0.13.0 | P1-pass |

What this adds to Core: before this round every lane run of the verb returned `auditable_metadata: null` (no section). Inference: the positive class is now held on three containers and three ISAs (x86-64, AArch64/ARM64, RISC-V 64) in seven format×architecture pairs, with the edge list (about 3,000 edges per carrier), the root index and the build/runtime kind preserved. REA also reports a `rustc_commit` object (`evidence_kind: inferred`) from compiler path strings; the counter does not score it.

Inference. Because REA 6.5.0 inflates and parses the section itself (S090) and the oracle does the same with Python's zlib and json, agreement shows REA does not drop, deduplicate, reorder-lose or mis-index packages on these inputs; it does not show that the embedded list is true (REA's own limitation: "Embedded dependency metadata is file content. It does not authenticate package names, versions, sources, or the compiler that produced the binary.").

## Limits

- Width: one producer (astral's uv 0.13.0 release build), so 16 carriers hold 5 distinct package lists (name, version, source, kind) and 7 distinct dependency documents, one per wheel, whose edges differ between architectures (wave 2 `ReDeriveElfX86.md`, `ReviewProvince.md`); uv, uvx and uvw of one wheel carry the same dependency document; the 16 carriers hold 5 distinct package lists (573-596 packages). The oracle shares the format spec (S089) with REA, not code. One REA pin (6.5.0), one host (Linux).

## Supersedes / pointers

This positive-class entry is complementary to, not a replacement for, the two earlier entries: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md` records two REA 6.5.0 typed RESULTs with null `auditable_metadata`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md` is a separate REA 6.7.0 Evidence-ID study whose measured Rust input also had null `auditable_metadata`. Those earlier observations remain scoped to their tested inputs; this claim concerns the frozen positive `.dep-v0` class.

- Pre-data controls (`.ufo/waves/round-30/controls/receipts.tsv`, committed before the data): do-nothing, junk-row, all-false, no-reader and id-keyed shortcut all scored `pass` 0 or 1 of 16 under the frozen counter, exit 1.
- Counter limits found by the wave (`.ufo/waves/round-30/w1/CriticTargetsControls.md`, `RevSelftestLookalikes.md`, `SentinelNoExec.md`): the committed-record clause compares evidence_id and packages but not subject, operation or range; `entry_ok`/`province_ok` are token checks; `GIT_DIR` in the caller's environment can redirect the counter's git reads (runs here unset it).
- Supersedes only the clause "Untested: non-ELF inputs" of `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10` for the positive class; that entry is not rewritten (pointer appended there).
- Not examined (wave 2 `ReviewEntryC1.md`): detail level is `--full-output` only; all 16 carriers are 64-bit little-endian; `source` values are only `crates.io` and `local`; no document has duplicate (name, version) pairs or duplicate dependency indices, so deduplication and mis-indexing are not stressed; PE sections with `VirtualSize` 0 or larger than `SizeOfRawData` are not exercised; the counter compares packages, offset and size but not `dependency_edges` or `root_package_index` (both were checked equal by wave-2 seats). Control pass counts are in `.ufo/waves/round-30/controls/receipts-detail.tsv`.
