# Round 30 wave 2 — ReviewEntryC1

Seat: `KaidokuR30.ReviewEntryC1` (reviewer). Attacks: `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` (the R30-C1 entry). The entry was last changed in `24da3459` and is unchanged at HEAD `3502b94c` (`git diff --quiet 92b1dd2d HEAD -- <entry>` printed `entry_unchanged_since_92b1dd2d`). Checks ran 2026-10-23T03:12:17Z–03:15:51Z.

**Verdict: fails, on two claims.** Every identifier and number in the Carriers and Results tables, the evidence IDs, the timing, the provenance and the P1 quote is backed by committed bytes: 32 table rows, 0 mismatches. Two claims are false:

- The "5 distinct package documents" claim. The carriers hold 7 distinct documents.
- The "five architectures" claim. The carriers cover 3 instruction-set architectures, or 7 format×architecture pairs; neither count is 5.

There are also smaller defects: a wrong pointer for the collection stdout, S090 missing from the `source:` line, and a Limits section that does not meet QUALITY row 7.

No REA run, carrier execution, lane write or git write was made. The carriers were copied to scratch and read as bytes only.

## Method (commands)

- **Independent decoder.** `timeout 300 python3 -I -B depdecode.py` ran in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewEntryC1` on scratch copies of the 16 carriers. All 16 copies pass `sha256sum -c` against `carriers.tsv`. The script parses ELF section headers, the PE section table (VirtualSize and SizeOfRawData) and Mach-O LC_SEGMENT_64 sections itself, without importing the lane oracle. It zlib-inflates `.dep-v0`, then compares the result with each committed envelope. Exit 0, 03:13:21Z.
- **Table check.** An inline python script parses both markdown tables and compares them with `carriers.tsv` and the envelopes. It also checks that `dependency_edges` equals the per-package `dependencies` and looks for duplicate name/version pairs. Exit 0, output `tablecheck.out`.
- **jq tabulation** of all 16 envelopes, run at 03:12:17Z.
- **Read-only git:** `git log`, `git show d210fb8:PROVINCE.md`, `git diff 24da3459~1 24da3459`.
- **Text checks:** `cmp` of P1 from `claims.json` against P1 in the entry, and `grep` of `SOURCES.md`, the counter, the oracle, the wave-1 reports and the REA 6.5.0 npx dist.

## Claim-by-claim table

| # | Entry claim (location) | Evidence (command → excerpt) | Label | Verdict |
|---|---|---|---|---|
| 1 | Carriers table: format, arch, wheel, sha256 prefix and size for 16 ids | table check → `carrier rows 16 result rows 16 mismatches 0`; the envelopes' `subject.digest.sha256` and `artifact.bytes` also equal `carriers.tsv` | observation | holds |
| 2 | "16 members of seven official uv 0.13.0 PyPI wheels" | `carriers.tsv` names 7 distinct wheel digests. All 7 appear in the committed `pypi-uv-0.13.0.json` (`comm -23` printed nothing). That file's SHA-256 is `2eaed6c87b93…` = the served SHA in the S091 row | observation | holds |
| 3 | Host `~/.local/bin/uv` and `uvx` are byte-identical to the manylinux x86_64 members | `sha256sum` → `3e801df89243…` and `2e9105ad9481…`, equal to elf-x86_64-uv and elf-x86_64-uvx; `uv 0.13.0 (x86_64-unknown-linux-gnu)`. Host state, not committed bytes | observation | holds (unlabeled in the entry) |
| 4 | Results: evidence_id, packages, edges, file_offset, compressed_bytes and root for each of the 16 rows | table check: every cell equals the envelope's `data.evidence_id`, `len(packages)`, `len(dependency_edges)`, `file_offset`, `compressed_bytes` and `packages[root_package_index]` | observation | holds |
| 5 | REA packages equal the oracle's decoding as a tuple multiset; offset and size equal | independent decoder → all 16 rows `multiset_equal True`, `offset_equal True`, `size_equal True`, `uncompressed_equal True` | observation | holds |
| 6 | PE: "content size is `min(VirtualSize, SizeOfRawData)`, not the padded raw size" | decoder → PE VirtualSize 9943 (x86_64) and 9938 (arm64), SizeOfRawData 10240, and REA `compressed_bytes` = VirtualSize. Caveat: the oracle (`tools/round-30/rust_dep_oracle.py:71`) uses `rawsize if vsize == 0 else min(vsize, rawsize)`, and so does the REA dist container parser (`cli.js:4457`, `virtualSize === 0 ? size : Math.min(virtualSize, size)`; that this parser feeds `RustBinaryImage.js` is an inference). The entry leaves out the VirtualSize = 0 case. Neither the VirtualSize = 0 case nor VirtualSize > SizeOfRawData occurs in the carriers | observation and inference | holds for the data; the stated rule is incomplete |
| 7 | "`kind` values `null` (absent in the section) or `build`" | decoder: the section `kind` key is absent on 537–558 packages and `build` on 36–38 per carrier, and REA emits `null` exactly where it is absent. REA's own limitation text: "An omitted package kind is left null. … that default was not stored in the section." No `dev` and no explicit `runtime` value occurs anywhere | observation | holds |
| 8 | `format_version` 1, a single root `uv 0.13.0` | jq → `format_version` 1 on 16/16, exactly one `root:true`, and `root_package_index` 463/459/458/455 equal to the oracle-side root position | observation | holds |
| 9 | "16 carriers hold 5 distinct package documents" (Limits) | decoder → `distinct doc_sha256: 7` (aarch64, riscv64 and x86_64 ELF; arm64 and x86_64 Mach-O; arm64 and x86_64 PE) and `distinct list_sha256: 7` (the P1 tuple multiset, including the dependency set). Only the (name, version, source) multiset gives 5 (`distinct nv_sha256: 5`). Example of the difference (`pairdiff.out`): elf-aarch64 has edges `cpufeatures 0.2.17→libc`, `cpufeatures 0.3.0→libc` and `ring→libc` that elf-x86_64 lacks, while elf-x86_64 has `blake3→cpufeatures` and `chacha20→cpufeatures` | observation | **fails** |
| 10 | "the 16 carriers hold 5 distinct package lists (573-596 packages)" | true only if a "package list" means (name, version, source). Under P1's own tuple (with the dependency set) the count is 7. The 573–596 range holds | observation | ambiguous; false under P1's tuple |
| 11 | "uv and uvx of one wheel carry the same dependency document" | decoder: the members of each wheel share a document SHA, and for PE uvw shares it too. The entry leaves uvw out | observation | holds (incomplete) |
| 12 | "three containers and five architectures" (What this adds to Core) | REA `normalized_result.architecture` takes the values `amd64`, `arm64` and `riscv`: 3 ISAs. aarch64 and arm64 are one ISA (REA reports `arm64` for both elf-aarch64 carriers). Format×arch pairs number 7 | observation | **fails** |
| 13 | "about 3,000 edges per carrier"; the edge list and root index preserved | edges range from 2974 to 3042. The table check prints no `EDGE ARRAY != deps` line, so REA `dependency_edges` equals the per-package `dependencies` in all 16 envelopes. The root index matches the oracle (row 8). The counter compares neither `dependency_edges` nor `root_package_index`: it compares the dependency (name, version) set per package and the `root` flag | observation | holds by this seat's check; not counter-scored |
| 14 | `rustc_commit` reported with `evidence_kind: inferred`; "the counter does not score it" | jq → `inferred` on 16/16; `grep rustc_commit tools/round-30/c1-rust-positive.py` → no match | observation | holds |
| 15 | "Collection run stdout: `carriers=16 pass=16 target=16` (`corpus/evidence/round-30/c1/runs.tsv`)" | `runs.tsv` has only per-carrier rows (id, utc, exit, argv, …, `P1-pass`, `packages=… edges=…`). `grep -rn 'carriers=16'` matches only `.ufo/waves/round-30/after/c1-rust-positive-at-24da3459.txt:17` and `…-at-92b1dd2d.txt:17` (`carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)`). No committed collection-run stdout exists | observation | **fails** (wrong pointer; the line is backed by the after receipts) |
| 16 | `verified-at`: 16 live calls from 02:59:33 to 03:00:31 +00:00, after freeze `4ee65c67` (02:35:13Z) and after `f39f4530` | `runs.tsv` first start `2026-10-23T02:59:33+00:00`, last end `03:00:31+00:00`, all exit 0 with `pkg_version 6.5.0`. `4ee65c67` committed `2026-10-22T23:35:13-03:00` (= 02:35:13Z); `f39f4530` committed `23:59:22-03:00` (= 02:59:22Z, 11 s before the first run) | observation | holds |
| 17 | Committed envelopes first added after the freeze | `git log --diff-filter=A -- …/c1/envelopes` → only `24da3459 2026-10-23T00:04:20-03:00`; all 16 stderr files are 0 bytes | observation | holds |
| 18 | P1 quoted "verbatim" from `claims.json` | `cmp p1-claims.txt p1-entry.txt` → `P1_IDENTICAL` (685 bytes each) | observation | holds |
| 19 | The oracle "shares the format specification with REA, not implementation code" | oracle imports only `json`, `struct` and `zlib` (lines 17–19). Absence of copied logic cannot be proven from imports | inference | holds as far as checked |
| 20 | Inference paragraph: REA's limitation quote "Embedded dependency metadata is file content. …" | the exact string is present in 16/16 envelopes (`grep -c` → 16 files) | observation | holds |
| 21 | Inference: agreement shows REA does not "drop, deduplicate, reorder-lose or mis-index packages" | multiset equality rules out dropped and duplicated packages. No document has duplicate (name, version) pairs or duplicate dependency indices (`dup_nv 0`, `dup_dep_idx_pkgs 0` on 16/16). So collapsing duplicates, and confusing two packages that share a name and version, were never exercised | inference | holds only in part (the class is not exercised) |
| 22 | Claim: at the base the lane held only null-metadata runs; PROVINCE names `inspect-rust-binary` 0 times | `git show d210fb8:PROVINCE.md \| grep -c inspect-rust-binary` → `0`. l7-02 records two 6.5.0 RESULTs with `auditable_metadata` null and the quote "No `.dep-v0` section was found". arc3-r10 is REA 6.7.0 with `auditable_metadata:null` (line 22) | observation | holds |
| 23 | Supersedes only the clause "Untested: non-ELF inputs" of `l7-02:10`; that entry is not rewritten (pointer appended) | `grep -n Untested` → line 10. `git diff 24da3459~1 24da3459` on l7-02 → 4 insertions, 0 deletions. The pointer at line 14 cites the clause "Untested: non-ELF inputs, missing-metadata/rejected-input behavior" for both R30 entries, which is consistent with C1 taking the non-ELF half | observation | holds |
| 24 | Pre-data controls scored `pass` 0 or 1 of 16, exit 1 (`controls/receipts.tsv`) | `receipts.tsv`: the 5 R30-C1 rows have `counter_exit 1` and `met_target no`, but no pass counts. The counts come from `receipts-detail.tsv`: `pass=0` four times and `pass=1` for the id shortcut | observation | holds (counts sit in `receipts-detail.tsv`, not the file cited) |
| 25 | Counter limits from wave 1 (committed-record clause not checking subject, operation or range; `entry_ok`/`province_ok` as token checks; `GIT_DIR`) | `CriticTargetsControls.md:34` "Committed operation, subject digest, offset, and size are not checked". `RevSelftestLookalikes.md:141,187` (entry_ok/province_ok). `SentinelNoExec.md:12` (`GIT_DIR`/`GIT_WORK_TREE` redirection) | observation | holds |
| 26 | `source:` line: S089 (README/PARSING.md/schema at `e2316a67`) and S091 | `SOURCES.md:95` S089 pins `e2316a672fc0…` for the three files. `SOURCES.md:97` S091 has the served SHA `2eaed6c8…` and the 7 wheel digests. **But the body cites S090** ("REA 6.5.0 inflates and parses the section itself (S090)") and the `source:` line leaves S090 out | observation | **fails** (source line incomplete) |
| 27 | Title: REA reads the graph "exactly" on ELF, PE and thin Mach-O | the decoder confirms the Mach-O magic `0xFEEDFACF` (thin, 64-bit) on all 4. `bits`/`byte_order` are `64 little` on 16/16 | observation | holds for the frozen set |

## QUALITY rows 4–7 (`corpus/QUALITY.md:14-17`)

| Row | Criterion (short) | Finding | Verdict |
|---|---|---|---|
| 4 | Names the artifact by absolute path plus a stable identity (SHA-256) | The entry body gives each carrier as an id with a 12-hex (48-bit) prefix. The full SHA-256 and the absolute path appear only by reference, through the committed `carriers.tsv` and the `recheck` directory `/fast/scratch/hyaku/kaidoku-r30/carriers/`. That is a scratch location, rebuilt from the wheels if absent; the wheel digests are pinned by S091 | partly met (identity delegated to a committed file) |
| 5 | Every conclusion labeled observation, inference or unknown | Results has "Observation." and "Inference." labels. These parts carry no label: the title ("exactly"), the Claim paragraph, the host byte-identity sentence (Carriers), the Method statement about the oracle sharing only the spec, the "What this adds to Core" paragraph (which contains the false "five architectures"), and every Limits line ("one producer" is an inference). No "Unknown" label appears anywhere | partly met |
| 6 | REA claims cite an Evidence ID or the exact reproducing call | All 16 evidence_ids match the envelopes exactly (row 4 above). The exact argv `npx -y rea-agents@6.5.0 inspect-rust-binary <path> --format json --full-output` is in `runs.tsv` | met |
| 7 | Names what was NOT examined | Named: one producer, one REA pin, one host, and the counter limits. **Not named:** (a) the detail level: runs used `--full-output`, which appears only in the `runs.tsv` argv; (b) the effective sample is 7 distinct documents, mis-stated as 5; (c) all 16 are 64-bit little-endian: no 32-bit, big-endian or fat/universal Mach-O; (d) `kind` only absent or `build`, with no `dev` or explicit `runtime`; (e) `source` only `crates.io` or `local`, with no git or other registry; (f) no duplicate name/version and no duplicate dependency indices, so the claimed protection against deduplication and mis-indexing is unexercised; (g) PE only with VirtualSize < SizeOfRawData, so the VirtualSize = 0 branch and VirtualSize > SizeOfRawData (zero-fill) are untested; (h) the counter does not compare `dependency_edges`, `root_package_index`, `section_bytes`, `uncompressed_bytes` or `format_version`, yet the entry asserts the edge list and root index are preserved (true per this seat, not counter-scored) | not met |

## Defects (by severity)

1. **High: wrong distinct-document count.** Limits line 72 says "16 carriers hold 5 distinct package documents". Observation: there are 7 distinct inflated `.dep-v0` documents and 7 distinct P1-tuple multisets (`decode.out`: `distinct doc_sha256: 7`, `distinct list_sha256: 7`). Only the (name, version, source) projection gives 5. The sentence also repeats itself ("…5 distinct package documents; … the 16 carriers hold 5 distinct package lists"). Fix: say 7 distinct documents and P1 package lists; 5 if dependency edges are ignored.
2. **High: wrong architecture count.** Line 67 says "three containers and five architectures". Observation: the envelopes report 3 ISAs (`amd64`, `arm64`, `riscv`), and the carriers form 7 format×arch pairs. aarch64 and arm64 are the same ISA.
3. **Medium: wrong pointer for the collection stdout.** Results (line 46) cites `runs.tsv` for `carriers=16 pass=16 target=16`. Observation: that line is not in `runs.tsv`. It is backed by `.ufo/waves/round-30/after/c1-rust-positive-at-24da3459.txt:17` and `…-at-92b1dd2d.txt:17` (a measurement, not the collection run). No collection-run stdout is committed.
4. **Medium: S090 missing from the source line.** The body cites S090 for REA's inflate-and-parse behaviour, but the `source:` header lists only S089 and S091 (QUALITY row 1 concerns resolvable sources; the header is the entry's source list).
5. **Medium: QUALITY row 7 limits incomplete.** Items (a) and (c)–(h) in the row 7 finding above are unexamined parts of the input class or the counter, and the entry does not name them.
6. **Low: QUALITY row 5 labels incomplete.** Several conclusions are unlabeled, including the false "five architectures" sentence; no Unknown label is used.
7. **Low: PE rule stated without its VirtualSize = 0 case.** The oracle (line 71) and the REA container parser (`cli.js:4457`) both fall back to SizeOfRawData when VirtualSize is 0. The case is not exercised.
8. **Low: control pass counts cited to the wrong file.** The "pass 0 or 1 of 16" numbers come from `controls/receipts-detail.tsv`, not the cited `receipts.tsv`, which only carries exit and met_target.
9. **Low: uvw left out.** "uv and uvx of one wheel carry the same dependency document" omits uvw, which shares the document in both PE wheels.

## Residual risk and verification gaps

- This seat ran no live REA call; the live-run agreement is ReRunC1's lane. The agreement findings here compare committed envelopes with this seat's own decoding of the carrier bytes.
- My decoder handles only what these carriers contain: thin little-endian Mach-O 64-bit, ELF section headers, and the PE section table. It is not a general oracle.
- The claim that REA's `cli.js:4457` container parser is the one behind `RustBinaryImage.js` is an inference from grep; the full call path was not traced.
- QUALITY rows 4 and 5 are judgments about how far the entry complies, not mechanical checks.
- Installs: none.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewEntryC1/`)

| file | sha256 |
|---|---|
| `depdecode.py` | `8f201b7b45ccb1304193ad8081265f9729b6e63cb31a4c24b2a0eba15bf2cafe` |
| `decode.out` | `cf3114d09cc00fcca80434009779a87011ed72bb4a9045d3dd6218afafd397fc` |
| `pairdiff.out` | `3d91c523b79e8b2978f149dbe02b06d1bed1d1318c28378593ed097915dc3a4c` |
| `tablecheck.out` | `90ddfc4a41b82c7346940ffa2130a1ab462895ec4f39c856566ea92c38fe1fd3` |
| `p1-claims.txt` | `1e2315e332711878e8ebcc8dd1ce3184bec29a094246a651dd1b0da5b2752c05` |
| `p1-entry.txt` | `1e2315e332711878e8ebcc8dd1ce3184bec29a094246a651dd1b0da5b2752c05` |
| `sources-95-97.txt` | `504e52f40e583bf4a517d9f89df8401c4c505c317cac100ec5e0f28a37efbc3a` |
| `carriers.sha256` | `bf42bc08e00af1966f78b8bab37c7c2d3fad38c92e3a1faec1d7de8f43e32ac5` |
| `carriers/` | scratch copies of the 16 carriers (digests in `carriers.sha256`) |
