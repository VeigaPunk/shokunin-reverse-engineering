# C1CarrierPins — carrier custody

**Verdict: pins agree. No content-hash mismatch on the four R49-C1 carriers.**

At base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` (HEAD, worktree clean on these paths) each committed fixture is 4096 bytes, not a Git LFS pointer, and its sha256 equals the draft `carriers.json` pin, `oracle.image.sha256`, `tools/round-44/carriers.json`, `tools/round-42/fixtures.json`, and the unblob 26.6.4 `__input__` bytes from `media.githubusercontent.com`. Superblocks match the frozen endian and `s_major`/`s_minor`. `c1-run.py` `resolve_fixture` binds each id to that round-42 path via the `path` field, and the digest equals the pin.

Axes: coverage (four ids × every pin source × upstream), depth (git blob vs worktree, superblock, resolver, LFS pointer vs media), calibration (v2.1 copies and the `raw.githubusercontent.com` pointer are not scored-pin failures).

No tools installed.

## Findings

| id | committed file (mode 100644) | sha256 (git blob = worktree = both carrier tables = fixtures.json = media body) | magic | s_major.s_minor | upstream `__input__` name |
|---|---|---|---|---|---|
| v1le | `corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin` blob `4001fddaf33e4b42bb23e47281a736297a6503ec` | `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71` | `hsqs` le | 1.0 | `squashfs_v1/little_endian/__input__/squashfs_v1.0_le.bin` |
| v1be | `corpus/evidence/round-42/c2/fixtures/v1-be--squashfs_v1.0_be.bin` blob `1cd1e5ce178c2204ecce091ae1b8592c08a98e25` | `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6` | `sqsh` be | 1.0 | `squashfs_v1/big_endian/__input__/squashfs_v1.0_be.bin` |
| v2le | `corpus/evidence/round-42/c2/fixtures/v2-le--squashfs_v2.0_le.bin` blob `0cd7729c99356530e0aa2a8e2e953655b0e12da5` | `7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124` | `hsqs` le | 2.0 | `squashfs_v2/little_endian/__input__/squashfs_v2.0_le.bin` |
| v2be | `corpus/evidence/round-42/c2/fixtures/v2-be--squashfs_v2.0_be.bin` blob `617e7906f43ab6961836be986d0e8a18ad28c292` | `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0` | `sqsh` be | 2.0 | `squashfs_v2/big_endian/__input__/squashfs_v2.0_be.bin` |

`fixtures.json` `file` is the upstream basename (`squashfs_v1.0_le.bin`, …). The committed name adds the id prefix (`v1-le--`, …). `source_pin` joins on `fixtures[].id` (`v1-le`, `v1-be`, `v2-le`, `v2-be`). Hashes are equal; the names are a prefix, not a second pin.

`tools/round-42/fixtures.json` `pinned.commit` is `1fcc7a0a584a70a96c31f5a276c20944d199a089`. The tag API object sha is the same commit. Those four pins are absent from `tools/round-42/prior-pins.json` (`pins[]` of rounds 38–41).

### `corpus/evidence/round-44/carriers/` is the v2.1 pair, not a second copy of the four

`git ls-tree` at the base lists only:

| file | sha256 | superblock | upstream |
|---|---|---|---|
| `squashfs_v2.1_le.bin` blob `54e1341f11ba886e0a3a3bbf48667f872ce446f6` | `6b6cd2fd63e17a499861d2d89d617bd836b169601e46cb2f5a5c66bea8ef253a` | `hsqs` 2.1 | `squashfs_v2/little_endian/__input__/squashfs_v2.1_le.bin` media HTTP 200, 4096 bytes, `cmp` exit 0 |
| `squashfs_v2.1_be.bin` blob `3f1fe68e01fee0d681237741d03b6f7f3c4a2846` | `c0140bac22d92df7d6c63fdf6de2d3e75a8fad6b30e6f9eeeb9ef533134f35db` | `sqsh` 2.1 | `squashfs_v2/big_endian/__input__/squashfs_v2.1_be.bin` media HTTP 200, 4096 bytes, `cmp` exit 0 |

Neither hash equals any of the four pins. The plan already excludes v2.1. The draft runner's `FIXTURE_DIRS` includes this directory only as a fallback; with `path` set, resolution does not use it (receipt below).

### `raw.githubusercontent.com` is the LFS pointer; the media URL is the image

For v1le, three URL forms:

| URL | HTTP | body | vs committed image |
|---|---|---|---|
| `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` | `HTTP/2 200` (0 redirects, 200962 bytes, sha256 `cc1425139dd60b071e55f9a30184206c57125fb66dcb381fc0bb055b98e3bc16`) | HTML shell | `rg` for `squashfs_v1.0_le.bin` / `squashfs_v2.0_le.bin` exit 1 (names not in the HTML) |
| `https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v1/little_endian/__input__/squashfs_v1.0_le.bin` | `HTTP/2 200`, 4096 bytes | sha256 `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71` | `cmp` exit 0. Same for v1be, v2le, v2be (`cmp` exit 0 each) |
| `https://github.com/onekey-sec/unblob/raw/26.6.4/.../squashfs_v1.0_le.bin` | `HTTP/2 302` then `HTTP/2 200` at the media URL, 4096 bytes | same sha256 | `cmp` exit 0 |
| `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/.../squashfs_v1.0_le.bin` | `HTTP/2 200`, 129 bytes, body sha256 `292220d6fa8cb2db4f354ac05f54a2feedd6c67cb4622636fe3713ee993a4b87` | Git LFS pointer whose `oid sha256:` is `b45925fa…e23e71` and `size 4096` | `cmp` exit 1 (differ at byte 1). The pointer is not the image; the oid is the pin |

GitHub contents API `HTTP/2 200` lists `squashfs_v1` and `squashfs_v2`. Nested `__input__` listings (`HTTP 200`) name `squashfs_v1.0_{le,be}.bin` (one file each) and, under v2, both `squashfs_v2.0_*` and `squashfs_v2.1_*`. API `size` is 129 (the pointer blob). The media download is the 4096-byte image.

## Commands

Worktree and those paths were clean. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` printed `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. `git status --porcelain` on the fixture dirs, `fixtures.json`, and `tools/round-44/carriers.json` printed nothing. Receipt `receipts/git-status.out` sha256 `1ccdabdb048d70a033410eab2429bfca1043f672d90f20b76a3b7c22f76f03a1`, UTC `2026-10-28T21:06:58Z`, exit 0.

`sha256sum` of the four fixtures and the two round-44 carrier files, UTC `2026-10-28T21:09:31Z`, exit 0. Stdout file `receipts/sha256sum-worktree.out` sha256 `2588d5f86309de80b9cde513287b4df149d17b4abe63039bc9672f739e6d651c`.

`git -C <lane> cat-file blob e4f2cfa5…:<path> | sha256sum` for the same six paths, same UTC, pipe exit 0, stdout file `receipts/sha256sum-gitblob.out` sha256 `7e0087e09a0f6be1cee0d480faf4d730762954d67cb2d844deb36f20e72c1331`. Git blobs are 4096 bytes and do not start with the LFS pointer prefix.

`git ls-tree -r e4f2cfa5… -- <four fixtures> corpus/evidence/round-44/carriers`, UTC `2026-10-28T21:10:35Z`, exit 0, stdout sha256 `9f0d700955de17bebd0e847513ead61b97d47534e91154ceb425af2ba9882349` (`receipts/ls-tree-carriers.out`).

`cmp` of each media body against the committed fixture, UTC `2026-10-28T21:09:31Z`: v1le, v1be, v2le, v2be, and the github-raw follow all exit 0 (`receipts/cmp-upstream.out` sha256 `b974ce4d37cc7c87181768ed91441c1890273b58b957bd8462deeccfb16cf887`). `cmp` of the `raw.githubusercontent.com` body, UTC `2026-10-28T21:09:53Z`, exit 1.

Fetcher: `curl -sS -L --max-time 45` starting UTC `2026-10-28T21:07:23Z`, each curl exit 0. Per-URL status is in `receipts/*.meta` and `receipts/*.hdr`. v2.1 media fetches UTC `2026-10-28T21:10:03Z`, curl exit 0, `cmp` exit 0.

Draft resolver (import of `.ufo/waves/round-49/draft/tools/round-49/c1-run.py`, `load_carriers` + `resolve_fixture` + `carrier_pin`), UTC `2026-10-28T21:09:53Z`, exit 0, stdout file sha256 `a0209e9e306343e497a702ef3f99c5412f249584a9c61f82209e103ee63f750f`:

```
v1le  how=entry field 'path'  sha256=b45925fa…e23e71  eq=True
v1be  how=entry field 'path'  sha256=529e1077…d631e6  eq=True
v2le  how=entry field 'path'  sha256=7c62dbe3…24f124  eq=True
v2be  how=entry field 'path'  sha256=79c0f388…2dfcc0  eq=True
```

Data run: not run (`c1-run.sh --data-run` is reserved for the L1).

Receipts and the fetched bodies used above are under `.ufo/waves/round-49/w1/C1CarrierPins/`. The 200962-byte tree HTML was not copied; its sha256 and the empty `rg` are in `receipts/tree.meta` and `receipts/tree-name-rg.out`.
