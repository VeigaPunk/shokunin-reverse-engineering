# R44CritC1 — attack of the R44-C1 draft

**Verdict: FIXABLE DEFECTS FOUND.** The standard v1/v2 carriers are readable by both `unsquashfs` 4.7.5 and 7-Zip 26.04, and the inherited unblob carve rule is knowable. But the claim's compression evidence is internally contradicted by its own cited `file` probe; the stated oracle-independence is overstated; and the actual `tools/round-44/c1-counter.py` draft is absent, so its probe/bindings and do-nothing behavior cannot yet be accepted. The four-carrier limitation is honestly disclosed and does not itself invalidate this narrowly scoped claim.

## Attacks and evidence

### 1. The `file` compression probe is a counterexample, not confirmation

`plans/round-44-claims.md:56-57` says the v1/v2 superblock probe (including compression) is verified against `file`; lines 85-87 then treat `file`'s v2-BE “uncompressed” report as a carrier property. That does not survive independent checks:

- `file` on the committed `v1-be--squashfs_v1.0_be.bin` reports **uncompressed**; on `v2-be--squashfs_v2.0_be.bin` it also reports **uncompressed**. Yet `tools/round-42/fixtures.json` records `compression: gzip` for both, and `unsquashfs -s` on both says “Inodes are compressed” and “Data is compressed.”
- The LE fixtures also report compressed in `file`; BE/LE behavior is therefore not a reliable compression classification. `file` additionally reports v1-BE blocksize `-32768`, while `unsquashfs -s` reports the valid 32768 block size.
- A byte scan of the four committed carriers found zlib-header candidates at offsets 73 (both v1 images), 63/90/138 (v2-LE), and 63/90/140 (v2-BE). This corroborates the fixture pins and `unsquashfs`, not `file`'s BE label.

**Smallest safe correction:** do not claim that compression is a v1/v2 superblock field or use `file` as its witness. The unblob v1/v2 definitions at `.../unblob/handlers/filesystem/squashfs.py:123-137` contain only magic, inode count, `bytes_used`, UID/GID starts, inode/directory table starts, and major/minor — no compression ID. Bind the family/version/endian from the actual superblock; if a compression assertion is retained, derive it from documented metadata-block decoding and corroborate with the oracle/tool output. Correct the v2-BE statement at claims lines 85-87 and note the v1-BE `file` counterexample too.

### 2. Oracle producer independence is weaker than the draft says; a better counterexample tool is available

Claims lines 82-85 call `unsquashfs` a different producer from sasquatch and call unblob `__output__` a second cross-checking oracle. There are two distinct issues:

- The four `__output__` trees are unblob integration expected outputs; the pinned `fixtures.json` identifies sasquatch as unblob's extractor dependency (and this round's claim explicitly measures REA/unblob with sasquatch). They are valuable committed regression expectations, but are not independent of the producer under test.
- `/usr/bin/unsquashfs` 4.7.5 is a distinct upstream binary from sasquatch 4.5.1, but the two share squashfs-tools code lineage. Calling the binary different is grounded; treating shared parser/extractor lineage as proof of fully independent correctness is not.

A stronger local counterexample is already available: `/usr/bin/7z` 26.04 lists and extracts all four standard v1/v2 carriers, including BE. I ran `7z e` on both v2 LE and BE and both v1 LE and BE; extracted file SHA-256 values matched across endian variants and matched the `unsquashfs` extraction values (e.g. v2 `apple1.txt` `6181259c…`, v1 `apple.txt` `303980bc…`). Conversely, both `unsquashfs` and 7z refuse the `sqlz` v2-nonstandard fixtures, consistent with the frontier decision at claims lines 54-55.

**Smallest safe correction:** describe `__output__` as a pinned regression/cross-check dataset, not an independent oracle; qualify `unsquashfs` as a separate implementation/version with shared lineage; and add 7-Zip 26.04 extracted-member digests (or at minimum its listing and sizes) as the genuinely distinct reader corroboration. Keep the v2-nonstandard scope Frontier; the refusal behavior was reproduced.

### 3. The v1/v2 superblock and carve rules are specific; a v3-layout port is unsafe unless replaced completely

The R42 source is explicitly a v3 counter: `tools/round-42/c1-counter.py:1174-1190` and `:1214-1221` read v3's 64-bit `bytes_used` at offset 63 and enforce a v3-sized superblock. That logic cannot be reused for these carriers. The installed unblob 26.6.4 source provides a direct layout witness at `squashfs.py:123-137`: the v1/v2 header has `uint32 bytes_used` at offset 8, and `uint16 s_major`/`s_minor` at offsets 28/30 in detected endianness. The committed hexdumps agree: `bytes_used` is 176, 177, 196, and 201 respectively for v1LE, v1BE, v2LE, v2BE; `unsquashfs -s` reports matching filesystem sizes and versions. There is no compression field in that header.

Carving is **not** just `bytes_used`: unblob's shared `_SquashFSBase.calculate_chunk` at `squashfs.py:77-98` reads `bytes_used` as the end-of-data offset, then accepts zero padding to 4096 or 1024 bytes (in that order), else ends at the unpadded byte count. All four fixtures have zero tails and therefore carve to 4096, despite their sub-202-byte `bytes_used`. A port that uses the R42 v3 offset/size or that compares the REA chunk length directly to `bytes_used` will reject valid receipts or misbind the chunk.

**Smallest safe correction:** in the R44 counter require exact v1/v2 layout parsing (`magic` + endian, u32@8 `bytes_used`, major/minor@28/30), and reproduce the unblob pad selection/zero-prefix rule exactly. Add a selftest for each endian/version using the committed bytes and assert `bytes_used` and `chunk_end` above. Treat compression as a separate decoded property, not a superblock member.

### 4. Exact handler binding: the inherited source is good, but the R44 counter remains unreviewable

The draft correctly requires per-carrier exact `squashfs_v1`/`squashfs_v2` equality (claims lines 43-52, 62-75) and specifically forbids a v3/v4 substitution (lines 39-41, 98-100). In the inherited R42 source, `handler_ok` checks equality against the frozen carrier handler (`tools/round-42/c1-counter.py:2443-2444`); the receipt freshness check uses `first_add` plus strict ancestry (`:1947-1957`, applied at `:2418-2420`). This is the right pattern: suffix/prefix-family matches are not enough, and an old receipt copied post-freeze is still caught by the frozen subject/superblock/handler/rerun bindings, not by freshness alone.

However, `tools/round-44/c1-counter.py` does **not exist** in the lane at review time (nor does `tools/round-44/`); the only available implementation is the R42 v3 counter. Thus no claim can be made here that the R44 probe uses exact equality, rejects stale paths, or makes CTL-C1-0 fail. The R42 pattern is evidence for what the port should preserve, not evidence that it has done so.

**Smallest safe correction:** do not freeze or score C1 until the actual R44 counter exists and its selftests cover (a) each v1/v2 exact binding, (b) wrong-version and v3/v4 handler receipts, (c) an old receipt copied into the R44 path after freeze, and (d) no R44 receipt with the stale round-42 receipt tree present. CTL-C1-0 must use only the exact R44 carrier IDs/paths and report zero matches plus false docs bindings; the strict first-add-descendant rule should be retained.

### 5. Four thin fixtures are an honest limit, not a hidden counterexample

Claims lines 110-117 explicitly disclose the four 4-KiB carriers, their few regular files, the unavailable published-image probes, and the excluded v2ns/v3/vendor/nested families. `fixtures.json` confirms the four standard fixtures are all 4096 bytes and list 3/3/4/4 expected files. `unsquashfs -lls` and 7z extraction reproduced those populations. This is thin evidence for broad real-world v1/v2 prevalence, but the claim is explicitly limited to these frozen carriers and the handler family “through REA on the frozen carriers”; it should not be widened. No correction needed beyond keeping the limitation adjacent to the target.

## Verification boundary

I ran only the review probes described above: `file`, hexdumps, `unsquashfs -s/-lls` and extraction on the four committed fixture carriers; 7z list/extract on those carriers and refusal probes on v2ns; and read-only source inspection of unblob 26.6.4 and the committed R42 counter. I did **not** run `tools/round-44/c1-run.sh` or any after-side REA C1 data procedure. No tools were installed/updated. I did not find or inspect a R44 counter draft because no `tools/round-44/` directory exists yet.
