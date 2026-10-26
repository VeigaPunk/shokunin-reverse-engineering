# Native magic support, measured 2026-10-26

Probe: `--probe --no-normalize-magic` on the `nopad` fixture of each family
(same result for the `1kpad`/`4kpad` twins) with the shipped binaries:
`unsquashfs` 4.7.5, 7-Zip 26.04, `unsquashfs-backhand` 0.25.5 (L1 build,
sha256 `88cf3ba5db572a43ef70553416be104b1de70058cb63f1d6f532615cf007972f`).

| superblock magic | byte order | unblob handler family | backhand 0.25.5 | unsquashfs 4.7.5 | 7-Zip 26.04 |
|---|---|---|---|---|---|
| `hsqs` | little | `squashfs_v3` (and the v3.0 canonical of `_ddwrt`) | reads | reads | reads |
| `sqsh` | big | `squashfs_v3` (and `_broadcom`/`_nonstandard` BE canonicals) | reads | reads | reads |
| `shsq` | little | `squashfs_v3_broadcom` | **reject** (rc 1) | **reject** (`Can't find a valid SQUASHFS superblock`) | reads |
| `qshs` | big | `squashfs_v3_broadcom` | **reject** | **reject** | reads |
| `hsqt` | little | `squashfs_v3_ddwrt` | **reject** | **reject** | **reject** |
| `tqsh` | big | `squashfs_v3_ddwrt` | **reject** | **reject** | **reject** |
| `zlqs` | little | `squashfs_v3_nonstandard` | **reject** | **reject** | **reject** |
| `sqlz` | big | `squashfs_v3_nonstandard` | **reject** | **reject** | **reject** |

Backhand was probed both with `-k le_v3_0` / `-k le_v3_0_lzma` and with no `-k`
(its own auto-detect, which prints `Failed <kind>:` for all thirteen kinds);
all vendor magics fail every way, and the same bytes with the four magic bytes
standardised read fine (`shsq -> hsqs`, `zlqs -> hsqs`, `tqsh -> sqsh` all
verified). 7-Zip 26.04 agrees from the inside: `7z i` declares its SquashFS
signature set as

    SquashFS squashfs      h s q s  ||  s q s h  ||  s h s q  ||  q s h s

i.e. `hsqs`, `sqsh`, `shsq`, `qshs` only.

Consequence: a multi-producer oracle can only cover the whole v3 handler family
if it normalises the magic; the tool copies the image and rewrites those four
bytes (`hsqt`/`zlqs`/`shsq` -> `hsqs`, `tqsh`/`sqlz`/`qshs` -> `sqsh`), recording
`original_magic`, `normalized_magic` and the normalised sha256 in
`oracle-run.json`.  The original image sha256 and magic stay the carrier pin.
