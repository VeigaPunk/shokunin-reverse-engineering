# R44C1FixtureAudit — C1 carrier fixture audit (round 44 wave 1)

Seat: R44C1FixtureAudit-2 · lane HEAD at audit: `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717` (the assignment names base c29360e3; HEAD differs — the fixture blobs are unchanged since their only commit `d1681696`, 2026-10-26, and `git diff HEAD -- fixtures` is empty).
Commands: `sha256sum`, `file`, `unsquashfs -s/-lls` (4.7.5, 2026/03/01), `xxd -l 64`, `curl` re-fetch to `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1FixtureAudit/` (4 × HTTP 200, 4096 B each). All exit 0 except the final `find` that has no match (not a defect).

## Result table

| carrier | sha256_match | file_verdict | licence |
|---|---|---|---|
| V1LE `v1-le--squashfs_v1.0_le.bin` | **yes** — `b45925fa…ce23e71` = fixtures.json pin; = re-fetch from unblob 26.6.4 media URL (byte-identical, 4096 B) | `Squashfs filesystem, little endian, version 1.0, compressed, 176 bytes, 4 inodes`; magic `hsqs`; `unsquashfs -s`: valid little endian SQUASHFS 1:0, inodes+data compressed | MIT (S135) |
| V1BE `v1-be--squashfs_v1.0_be.bin` | **yes** — `529e1077…d631e6` = pin; = re-fetch | `Squashfs filesystem, big endian, version 1.0, uncompressed [file misparse, see N1], 177 bytes, 4 inodes`; magic `sqsh`; `unsquashfs -s`: valid big endian SQUASHFS 1:0, "Inodes are compressed / Data is compressed" | MIT (S135) |
| V2LE `v2-le--squashfs_v2.0_le.bin` | **yes** — `7c62dbe3…afd924f124` = pin; = re-fetch | `Squashfs filesystem, little endian, version 2.0, compressed, 196 bytes, 5 inodes, blocksize: 65536`; `unsquashfs -s`: valid little endian SQUASHFS 2:0, inodes/data/fragments compressed | MIT (S135) |
| V2BE `v2-be--squashfs_v2.0_be.bin` | **yes** — `79c0f388…2dfcc0` = pin; = re-fetch | `Squashfs filesystem, big endian, version 2.0, uncompressed [file misparse, see N1], 201 bytes, 5 inodes, blocksize: 65536`; `unsquashfs -s`: valid big endian SQUASHFS 2:0, all compressed | MIT (S135) |

All four are in the lane git index at HEAD (blobs 1cd1e5ce / 4001fdda / 617e7906 / 0cd7729c), clean worktree, committed once in `d1681696` — i.e. they are the committed round-42 copies, and the independent re-fetch from the pinned unblob 26.6.4 LFS media path (`tools/round-42/fixtures.json` `url`) matches byte for byte: no drift.

Pin sources: `tools/round-42/fixtures.json` (ids v1-be/v1-le/v2-be/v2-le, handlers `squashfs_v1`/`squashfs_v2`, size 4096, compression field `gzip`) — all 4 sha256 equal the recomputed values. `tools/round-44/carriers.json` **does not exist yet** (`tools/round-44/` is empty at audit time; L1 installs it after the freeze), so that second pin could not be compared: **pending, not a pass**. The claims table in `plans/round-44-claims.md` lists exactly these four paths; the L1 must re-run `sha256sum` against `carriers.json` once installed (expected values above).

## Notes for the counter port
- N1 `file(1)` mislabels both **big-endian** images "uncompressed" (and prints blocksize `-32768` for v1). `unsquashfs -s` says "Inodes are compressed / Data is compressed" for all four, and fixtures.json says gzip. The counter's superblock probe must read the flags/compression itself (zlib is the only v1/v2 compressor) and must not take compression from `file` text for BE. Endianness/version tokens from `file` agree with the unsquashfs verdicts for all four.
- N2 Raw header magic: LE images start `hsqs` (`6873 7173`), BE images `sqsh` (`7371 7368`) (xxd -l 64). Major version is taken from `unsquashfs -s` (1:0 / 2:0) and `file`, both agreeing; I did not independently decode the s_major field offset.
- N3 `unsquashfs -lls` oracle census: v1 = 3 regular files (apple.txt 6 B, banana.txt 7 B, cherry.txt 7 B); v2 = apple1..4.txt 7 B each (+ root dir); matches `expected_files` 3 / 4 in fixtures.json.

## v2ns exclusion
`v2ns-le--squashfs_v2.0_le.bin` (sha256 `f25cf3ea…9e24a`) and `v2ns-be--squashfs_v2.0_be.bin` (`6560be64…df6a7b`) exist in the same fixtures dir, handler `squashfs_v2_nonstandard` in fixtures.json; `file` reports `data` for both (no standard magic) — not v1/v2 carriers. They are **not** among the four frozen C1 carriers in the claims table (`plans/round-44-claims.md` §R44-C1 lines ~50–56 keep them Frontier: `unsquashfs` 4.7.5 refuses them). Caution: they share the file basename `squashfs_v2.0_{le,be}.bin` and the `v2-` prefix family — a counter matching by suffix/glob `*squashfs_v2.0_*` would wrongly admit them; match by exact path (per-carrier EXACT equality) as the contract requires. Carriers.json check on exclusion: pending (file absent).

## Licence (S135)
`corpus/SOURCES.md` row S135 = unblob 26.6.4 LICENSE (MIT; "the fixture bytes may be committed and regenerated in the lane evidence tree"; HTTP 200, 1068 B, sha256 `67303bbd…922e`). Independent re-hash of the installed distribution licence `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob-26.6.4.dist-info/licenses/LICENSE` = `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e` — equal to S135. Fixtures.json `pinned.license` = MIT. Honoured: fixtures are committed, attributed to onekey-sec/unblob 26.6.4 in fixtures.json (project, version, commit, url). Gap (minor, not a blocker): no per-directory LICENSE/NOTICE file sits beside the fixtures (`corpus/evidence/round-42/c2/fixtures/` has none); attribution lives in `tools/round-42/fixtures.json` and S135 only. MIT requires the notice accompany "copies or substantial portions" — 4 KiB data fixtures with the notice in the lane registry is the lane's existing practice (rounds 42/43); flagged for the L1 to decide, not changed here.

Verdict: **PASS on bytes (4/4 pin match, 4/4 re-fetch identical), PASS on file/unsquashfs identity (with N1 caveat), PASS on v2ns exclusion by claims; carriers.json comparison PENDING (file not yet installed).**
