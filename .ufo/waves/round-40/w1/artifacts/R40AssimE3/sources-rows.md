# SOURCES rows this seat proposes to append (normalized, 11 columns, no pipe inside a cell)

Proposed ids continue the lane registry: `grep -cE '^ {0,3}\| S[0-9]{3}' corpus/SOURCES.md` = 122,
next free **S123**. The id is bookkeeping; the **document** is the evidence — see
`collision/renumber-map.tsv`. If the L1's append order differs, renumber from that map by document,
never by arithmetic.

Entry these rows point at: `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S123 | A real AVM-BE image built by the lane and extracted by unblob — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv (sha256 f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0) | own-work | A | the end-to-end extraction observation on the retained 4 096-byte genuine AVM-BE image, and that image's own superblock fields — never an inference from a detector, and nothing about vendor firmware or about the layout test the round-40 entry adds | file rows `image_path`, `image_magic`, `image_compression_id`, `image_mkfs_time`, `image_bytes_used`, `image_is_avm`, `unblob_handler`, `unblob_be_flag`, `extracted_files`; image `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs` 4 096 bytes sha256 c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32; run log `unblob.log` sha256 352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7 (re-opened 2026-10-26) | that a genuine AVM-BE image extracts through unblob 26.6.4 with no `-be` on the argv, publishing four files with their exact contents, while the retained log carries no exit status and an earlier attempt in the same directory failed to run its extractor | mined | 2026-10-26 | 180d — `sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs` -> c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32 (ran 2026-10-26) | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S124 | The upstream release the AVM toolchain pins, its md5 and its download path — /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/freetz-squashfs4-host-be.mk (sha256 48fb043d8fb2e9b1ea916abb06316bb99a3c3d2232d8694e6f6f651a0393a3d5) | own-work | A | the source tarball the AVM recipe pins and the path it is served from — the artefact whose absence blocked rounds 9 and 10, and not a statement about any image | file lines 1-4: `SQUASHFS4_HOST_BE_VERSION:=4.3`, `SQUASHFS4_HOST_BE_SOURCE:=squashfs$(SQUASHFS4_HOST_BE_VERSION).tar.gz`, `SQUASHFS4_HOST_BE_SOURCE_MD5:=d92ab59aabf5173f2a59089531e30dbf`, `SQUASHFS4_HOST_BE_SITE:=@SF/squashfs`; the working URL and the `-DTARGET_FORMAT=AVM_BE` build line are recorded in the same file (re-opened 2026-10-26) | that Freetz pins squashfs4.3.tar.gz by md5 and that the tarball is served, so a reader can rebuild the AVM-BE mksquashfs the retained image came from instead of trusting the image alone | mined | 2026-10-26 | 180d — `grep -c -F 'd92ab59aabf5173f2a59089531e30dbf' /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/freetz-squashfs4-host-be.mk` -> 1 (ran 2026-10-26) | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S125 | Freetz AVM-BE format description, read for its layout bullet — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt | docs | A | what makes an image the AVM layout rather than standard big-endian v4: the block-length field's byte order, and the marker bullet — not the marker alone, and not any image's outcome | file `AVM-BE-format.txt` at `tools/make/squashfs4-host-be/` in Freetz master, HTTP 200, 1 496 B, sha256 c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5; line 5 the big-endian layout, line 8 the little-endian block length, lines 13-14 the `mkfs_time` bullet; a second row for the document S114 already holds, whose anchor quotes only the opening line and the marker | that the only little-endian data field in AVM-BE is the block length at the start of each block, and that `mkfs_time` holding the value of `bytes_used` is a separate super-block property, so the marker cannot stand in for the layout | mined | 2026-10-26 | 180d — `curl -fsSL -o avm-be-format.txt https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt && grep -c -F 'the only data field stored in the little-endian format is the block length value' avm-be-format.txt` -> 1 (ran 2026-10-26) | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |

## Existing rows whose `used-by` this entry extends (append-only in-place change, logged old→new)

| id | old used-by | new used-by |
|---|---|---|
| S107 | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S108 | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |
| S121 | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md |

No other cell of S107, S108 or S121 changes; no row is deleted; nothing else in the registry is touched.

## Rows deliberately not appended

- The 132-row package is **not** bulk-appended (CORPUS rule 4). This seat adopts three rows; every
  other package row stays staged.
- No row was minted for the handler digest, the sasquatch release or the `-be` semantics: S107, S108
  and S121 already hold those scopes and are cited instead.
- S114 is **not** superseded: it is not wrong, only narrower than S125. No reversal is recorded,
  because none happened.
