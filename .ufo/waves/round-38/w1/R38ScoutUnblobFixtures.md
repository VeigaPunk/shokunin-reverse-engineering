# R38ScoutUnblobFixtures — provenance row for K3/K4 fixture bytes (R37-CL2)

Access UTC: 2026-10-26T06:16Z–06:20Z (`date -u` at first call 2026-10-26T06:16:46Z). No lane corpus edited; scratch removed.

## Observed facts

Upstream: https://github.com/onekey-sec/unblob, tag `26.6.4` → commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` (`api.github.com/repos/onekey-sec/unblob/git/ref/tags/26.6.4`, type commit; tree sha same as listed by `git/trees/26.6.4?recursive=1`, `truncated:false`). License: MIT (GitHub licence API, `spdx_id`).

Fixture dir (handler name = dir name): `tests/integration/filesystem/squashfs/squashfs_v4_be/` (tree `35a3577a2e9bb02a553ae3367ace87ae0aea042e`), with `__input__/` (tree `973ed190…`) and `__output__/` (tree `2f17d4fb…`).

Storage caveat: `.gitattributes` at 26.6.4 has `tests/integration/** filter=lfs …`, so the git blobs are 128/129-byte Git-LFS pointers, not the bytes. Real bytes come from `https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/<path>` (HTTP 200, exit 0). Anyone checking by `git clone` without LFS sees only pointers.

### Inputs (`__input__/`)
| upstream file | LFS oid (sha256) = pointer size | downloaded size / sha256 | lane carrier |
|---|---|---|---|
| `squashfs_v4.bin` | `9c7c523c…97c0`, 4096 | 4096 B, `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` | **K3** `K3/carrier.bin` (4096 B, same sha256) |
| `squashfs_v4.4kpad.bin` | identical oid to `squashfs_v4.bin` (same blob `88ef7cc6…`) | — | also K3 bytes (K3 carriers.json says "4kpad") |
| `squashfs_v4.nopad.bin` | `a29ddc15…56ed`, 307 | 307 B, `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` | **K4** `K4/carrier.bin` (307 B, same sha256) |
| `squashfs_v4.1kpad.bin` | `d0bd6f90…fa42`, 1024 | not fetched | not a carrier |

Lane sha256 (sha256sum) of K3/K4 `carrier.bin` equal the upstream LFS oids and downloaded bytes exactly.

### Expected output (`__output__/squashfs_v4{,.nopad}.bin_extract/apple1..4.txt`; also `.4kpad`, `.1kpad`)
All 16 blobs are LFS pointers with oids identical per apple across all four `_extract` dirs. Downloaded from media for `squashfs_v4.bin_extract` and `squashfs_v4.nopad.bin_extract`: each 7 B; `cmp` equal between the two dirs and byte-equal to the lane `K3/appleN.txt` and `K4/appleN.txt` for N=1..4. sha256 equal `K3/oracle.tsv` and `K4/oracle.tsv`:
- apple1 `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30`
- apple2 `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff`
- apple3 `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6`
- apple4 `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d`
Content of apple1 = `apple1\n`-style 7 B (shown `apple1`).

### Located quote (≤25 words; raw `__input__/squashfs_v4.nopad.bin` pointer at tag 26.6.4)
> "oid sha256:a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed / size 307"

(and `.gitattributes`: "tests/integration/** filter=lfs diff=lfs merge=lfs -text").

## Commands (reproduce)
```
curl -s "https://api.github.com/repos/onekey-sec/unblob/git/trees/26.6.4?recursive=1" | jq -r '.tree[]|select(.path|test("^tests/integration/filesystem/squashfs/squashfs_v4_be/"))|"\(.type) \(.sha) \(.size // "-") \(.path)"'
curl -s https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be/__input__/squashfs_v4.nopad.bin   # LFS pointer
curl -sf -o f https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be/__input__/squashfs_v4.nopad.bin; sha256sum f
```
All exit 0.

## Notes for the SOURCES row / calibration
- Provenance is now closed for the bytes: K3 = `squashfs_v4_be/__input__/squashfs_v4.bin` (≡ `.4kpad.bin`), K4 = `…/squashfs_v4.nopad.bin`; sources are MIT, public, tag-pinned.
- Oracle independence: the K3/K4 "oracle" is unblob's own expected `__output__` apples (written by the unblob project, same repo as the extractor under test); independent of the REA run, but not independent of unblob. The `sasquatch-v4be -be` cross-tool leg in c1-run.sh is the independent check. [INFERENCE: `__output__` produced by unblob/sasquatch at fixture creation; not read from a commit message.]
- The lane's K3 carriers.json note says "(4kpad)" while the upstream fixture of that name is `squashfs_v4.4kpad.bin` AND `squashfs_v4.bin` (same bytes); both names legitimate.
- A "git clone" fetch of the fixture returns pointers; cite the media path or LFS oid, not the git blob sha (`88ef7cc6…`/`9f2fc996…` are pointer blobs, not carrier bytes).
- Tools installed: none.
