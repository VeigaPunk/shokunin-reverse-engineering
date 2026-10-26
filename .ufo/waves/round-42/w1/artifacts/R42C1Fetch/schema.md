# fetch-carrier.py — frozen schema and integration notes (round 42, C1)

Tool: `fetch-carrier.py` (this directory). Destination in the lane: `tools/round-42/fetch-carrier.py`.
Spec destination: `.ufo/waves/round-42/c1/carriers.json` (the tool's `REPO_SPEC` default, so a frozen
run is `fetch-carrier.py --root LANE --rev REV --cache DIR`).

## 1. Schema

```json
{
  "claim": "R42-C1",
  "target": 4,
  "carriers": [
    {
      "id": "TQ",
      "url": "https://<published third-party image>",
      "image_sha256": "<64 hex: digest of the whole downloaded file>",
      "container": {"kind": "tar", "member": "./firmware.bin", "member_sha256": "<64 hex>"},
      "carve": {"offset": 0, "bytes_used": 3014656, "sha256": "<64 hex: the carrier pin>"},
      "kind": "vendor", "product": "...", "publisher": "...",
      "oracle": "corpus/evidence/round-42/c1/TQ/oracle.tsv",
      "nonregular": "corpus/evidence/round-42/c1/TQ/nonregular.tsv"
    },
    {
      "id": "KM",
      "url": "https://archive.openwrt.org/.../openwrt-...-squashfs.img",
      "image_sha256": "<64 hex>",
      "container": {"kind": "range", "offset": 65536, "length": 1900544,
                    "member_sha256": "<64 hex>"},
      "carve": {"offset": 0, "bytes_used": 1900544, "sha256": "<64 hex>"}
    },
    {
      "id": "RAW",
      "url": "https://<raw squashfs file>",
      "image_sha256": "<64 hex>",
      "carve": {"offset": 0, "bytes_used": 1234567, "sha256": "<64 hex>"}
    }
  ]
}
```

Rules the tool enforces (`link` in the receipt names the first broken one, in this order):

| link | step |
|---|---|
| `spec` | structure: url scheme, 64-hex digests, `carve.bytes_used > 0`, `carve.offset >= 0`, **no unknown keys inside `container` or `carve`** |
| `work` | the staging directory (`--work`, else `$TMPDIR`, else platform default) is missing or unwritable |
| `url` | transport error, HTTP status error, or a body shorter than `Content-Length` |
| `image_sha256` | digest of the whole downloaded file |
| `member` | tar member absent / not a regular file / short; range past the end of the image / short |
| `member_sha256` | digest of the container member (mandatory for any `container`) |
| `carve` | `carve.offset + carve.bytes_used` past the end of the member/image |
| `carve_sha256` | digest of the carve window = the carrier pin |
| `cache` | a symlink / non-directory component of `--cache` or `--image-cache`; failure to create/replace the entry |
| `verify` | post-write lstat + re-hash of the entry with `O_NOFOLLOW` |

`CACHE/<carve.sha256>.bin` holds exactly the carved bytes (`bytes_used` bytes starting at
`carve.offset` of the member). Records without a `url` (lane-built carriers with `path`) are
skipped and reported as `skipped: not-external`; they do not affect the exit code, but a spec
with no managed record exits 1.

## 2. Integration notes for the C1 counter port (not this tool's scope)

* The round-41 counter's `carve_ok` compares `external.length == bytes_used == size`
  (`tools/round-41/c1-counter.py:1559-1566`). The round-42 spec has **no `external.length`**:
  the port must read `carve.bytes_used` (and record `carve.offset`) from `carriers.json`, and
  keep the invariant `bytes_used == size` of the cache file — which the fetch tool guarantees,
  because the cache entry *is* the carve window.
* The cache entry name stays `<pin>.bin`, so `--carrier-cache` reading is unchanged.
* `layout_probe` in the counter reads the superblock from offset 0 of the carrier; round-42
  carriers are already carved to the superblock start, so no probe change is needed for the
  magic/major/compression binding — only for the `carve` accounting above.

## 3. Rebuild / re-run

```
S=/fast/scratch/hyaku/kaidoku-r42/R42C1Fetch
mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
python3 -I -B <LANE>/.ufo/waves/round-42/w1/artifacts/R42C1Fetch/fetch-carrier.py --selftest
python3 -I -B <LANE>/.../e2e-real-fixtures.py --tool <LANE>/.../fetch-carrier.py \
        --fixtures <LANE>/.../fixtures --scratch "$S/e2e"
python3 -I -B <LANE>/.../probes.py --tool <LANE>/.../fetch-carrier.py \
        --fixtures <LANE>/.../fixtures --scratch "$S/probes"
```

Fixture provenance (unblob 26.6.4, commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`, MIT LFS
blobs fetched from `https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/`):

| local name | upstream path | bytes |
|---|---|---|
| `squashfs_v3_le.bin` | `squashfs/squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` | 4096 (258 used) |
| `squashfs_v3_be.lzma.bin` | `squashfs/squashfs_v3_adaptive/__input__/squashfs_v3_be.lzma.bin` | 4096 (256 used) |
| `squashfs_v3_le.lzma.bin` | `squashfs/squashfs_v3_adaptive/__input__/squashfs_v3_le.lzma.bin` | 4096 |
| `squashfs_v3.be.nopad.bin` | `squashfs/squashfs_v3/big_endian/__input__/squashfs_v3.be.nopad.bin` | 320 |

`fixtures/SHA256SUMS` pins them. These are development inputs: never a C1 carrier.

## 4. Known limits (unchanged by this tool)

* No ChaCha/`.sha256`/`.asc` beside most vendor images: the chain proves "the bytes fetched at
  freeze time", not "the bytes the vendor produced" (round-41 D6 class). Only the digest pin
  travels.
* A redirect at fetch time is followed but the resolved URL is not recorded; the pin is the
  arbiter if the locator later moves.
* `_check_path` verifies each component of the cache path with `lstat` immediately before the
  `O_EXCL` create; a racer that swaps a component for a symlink between the two calls is a
  theoretical TOCTOU window not closed here (no `openat2(RESOLVE_NO_SYMLINKS)`), [INFERENCE]
  irrelevant to a scratch cache only the run itself writes.
