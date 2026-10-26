# Draft SOURCES row (provisional id S130) — unblob 26.6.4 SquashFS fixtures

Lane schema at base c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c (`corpus/SOURCES.md`, header after line 3):
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by` (11 columns).
Next free id: S130 (no S130 row exists at base; last row is S129). No literal `|` appears in any cell.

| S130 | unblob 26.6.4 SquashFS integration fixtures — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (LFS payload base https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/) | dataset | A | MIT-licensed Git-LFS fixture bytes and expected member trees for the unblob 26.6.4 SquashFS handler family (v1, v2, v2-nonstandard, v3, v3-adaptive-LZMA, v3-Broadcom, v3-DDWRT, v3-nonstandard, v4 LE, v4 BE, v4-Broadcom), the bytes a round-42 C2 generator may pin; not the handler code, not extractor behaviour, not a C1 carrier and not a vendor image | commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; tree API `?recursive=1` HTTP 200 at 2026-10-26T21:50:43Z, 1522052 B, sha256 adb692a25b66718f9ed1dc237d87d72b4b6440a9a2f2ddbbb49e925df38b3ef2, truncated=false, 380 entries, 58 `__input__` blobs in 11 directories, pointer blobs 128-129 B, payloads 307-4096 B; magic patterns put major and minor at offset 28, so v3 fixtures read 3.0 (9 files) or 3.1 (24 files); example `squashfs_v3/little_endian/__input__/squashfs_v3_le.bin` pointer 129 B sha256 079d7c61dd030a5e8837fdf23a3527710e5a9be64669196ee74940865d82f1a2, oid sha256 0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7, payload 4096 B; `.gitattributes:1` `tests/integration/** filter=lfs diff=lfs merge=lfs -text`; repo LICENSE lines 1 and 12-13 MIT with notice retention | Pin exact fixture bytes and the expected member list by URL plus LFS oid before generating C2 combos; a fixture path is not a handler label, since two of the 58 sit under a DD-WRT or Broadcom directory but carry plain-v3 magic and unblob detects them as `squashfs_v3` | mined | 2026-10-26 | 180d | .ufo/waves/round-42/w1/R42SrcUnblob.md (provisional; L1 re-points after integration) |

Validation performed on the row text above: 11 cells when split on `|` with the leading and trailing
empty fields removed; no cell contains `|`; id S130 absent at base; `opened` follows the date-only
convention of S127-S129 while the exact UTC open time lives in the `anchor` cell.

Two edits the L1 may want instead of the literal cell text:
1. `used-by` should name the frozen consumer once it exists (the round-42 C2 knowledge entry), as
   S127-S129 name `corpus/knowledge/...` files.
2. If the lane prefers a shorter `anchor`, the minimum pinning set is the commit, the tree-API sha256,
   the LFS pointer/oid mechanism and the `.gitattributes:1` rule; the 58-file inventory is reproduced
   in `fixtures-58.tsv` next to this file.
