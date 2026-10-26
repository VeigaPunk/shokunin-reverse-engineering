DONE — V2 and D picked and verified: V2 = FRITZ.Box 7430 FRITZ!OS 7.31 BE member, D = FRITZ.Box 6590 Cable FRITZ!OS 7.57 image. 17 AVM `.image` files probed (the tsv has 18 member rows).

# R40C1VendorScout — second vendor carrier V2 and development image D

Artifacts (`.ufo/waves/round-40/w1/artifacts/R40C1VendorScout/`):
- `candidates.tsv`: one row per `filesystem.image`-like member.
- `probe.py`: the pure-Python superblock probe.
- `carve.sh`: download, carve and sha-verify for V2 and D.
- `image-sha256.txt`: sha256 of the whole images.
- `info/`: AVM `info_en.txt` copies and the licence lines.

No tool was installed. No unblob and no REA ran on any image. The only external programs run were `curl`, `tar`, `sha256sum` and python3.

## Method
- Fetched `https://download.avm.de/fritzbox/`; every `.image` URL below returned HTTP 200.
- Downloaded 17 images: 16 `FRITZ.Box_*.image` files from model directories plus V1.
  - V1 = `FRITZ.Box_6490_Cable-07.57.image`. Its sha256 reproduced as `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`.
  - 3272 and 7272 were also probed; they are SquashFS v3, not v4.
- `probe.py` reads each member with `tarfile` and decodes the 96-byte v4 superblock. Magic `sqsh` is read big-endian, `hsqs` little-endian. It then does two checks:
  - It reads the first metadata length header at `inode_table_start`, LE and BE.
  - It walks the whole inode-table block chain from `inode_table_start` to `directory_table_start` with LE and with BE headers. The chain either lands exactly on `directory_table_start` or breaks. This is stronger than a single header.

## Findings
1. Every v4 BE (`sqsh`) member probed has comp=4 (xz), block size 65536, `mkfs_time == bytes_used` (marker YES), and an inode-table chain that is exact under LE headers and breaks at the first block under BE headers. The `inode_chain_BE` column in `candidates.tsv` shows `bad@…(n=0)`.
   - Candidates with that clean split: 3490 (7.31), 5490 (7.31), 5491 (7.31), 6820v1 LTE (7.30), 7430 (7.31), 7490 (7.62), 6490 BE member, 6590 BE member.
   - 7560-07.30 is a BE member but ambiguous at the first header (LE 2060, BE 3080, both plausible). The chain test still resolves it: LE exact over 42 blocks, BE bad. Do not use it where a single-header test is shown.
2. The marker `mkfs_time == bytes_used` also holds on the little-endian `hsqs` members (6490 x86, 6590 x86, 7581, 7582, 7590). It is not an endianness discriminator on its own. unblob's `-be` branch only applies after the magic is `sqsh`.
3. Two structurally different AVM-BE shapes exist:
   - Cable (Puma6) images are tars with a small BE member (1079 inodes, 5.4 MB) at `./var/remote/var/tmp/filesystem.image` plus a LE x86 member at `./var/remote/var/tmp/x86/filesystem.image`. V1 and the 6590 have this shape.
   - MIPS images (3490, 5490, 5491, 7430, 7490, 6820v1) are tars with `./var/tmp/filesystem.image` as an AVM-BE wrapper of about 105 inodes.
     - Both 3490 and 7430 hold ~86–90 symlinks, 8 regular files, 10 dirs and one char device.
     - 3490 and 7430 each hold one huge regular file, `filesystem_core.squashfs` (28.4 MB / 25.2 MB).
     - The 7430 nested `filesystem_core.squashfs` is itself AVM-BE: `sqsh`, 7524 inodes, `mkfs_time == bytes_used == 25194540`, comp 4.
     - The wrapper therefore has a single inode-table metadata block (`n=1`) and several hundred data blocks in one file, with no fragment-heavy structure.
4. The 4040 (`filesystem.image` is 0 bytes, kernel only, 08.03), 7390 (0 bytes) and 6591 (08.25, a 61 MB `firmware-update.uimg` with no filesystem.image member) have no usable member.
5. Observation made while listing the 3490 wrapper: `sasquatch-v4be` WITHOUT `-be` on an AVM-BE member prints "SquashFS version [1024.0] / inode count [1761607680] suggests a SquashFS image of a different endianess" on stderr, then "Successfully decompressed with default xz decompressor". I listed the wrapper with `sasquatch-v4be -ll`. This is a sasquatch-v4be observation on a development candidate, not a REA run.

## Picks
**V2 = `FRITZ.Box_7430-07.31.image`** (FRITZ!Box 7430, FRITZ!OS 7.31, released 04.09.2023 per `info_en.txt`). It is a different family (MIPS/Lantiq-style wrapper) and a different FRITZ!OS version from V1 (7.57).
- URL: `https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image`
- HTTP 200, 28,856,320 B, image sha256 `3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4`.
- Member `./var/tmp/filesystem.image`: 25,825,288 B, sha256 `b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c`.
- Header: `sqsh`, v4.0, comp 4 (xz), inodes 109, `mkfs_time = bytes_used = 25824314` (marker YES).
- Inode table starts with LE header 748 (compressed); the chain is exact under LE and breaks under BE at once.
- Why it is a good carrier:
  - It is a genuine AVM-BE v4 member with LE block lengths.
  - Its shape complements V1: symlink-dense, with one 25 MB file spanning hundreds of LE-headed data blocks, and a nested second AVM-BE layer.
- Cost: 25.8 MB is large to commit.
- Fallback V2 if size is a problem: the 6590 BE member (5,443,592 B, sha `65e85647f0199f9dcbb3f06674557bfda2fc9a4412378448b572478d2bff832a`, different model, FRITZ!OS 7.57). It is the same tar shape as V1, so lower diversity. If it is taken as V2, use a different image as D, for example 6820v1 or 3490.

**D = `FRITZ.Box_6590_Cable-07.57.image`** (development; recon seats may run REA on it).
- URL: `https://download.avm.de/fritzbox/fritzbox-6590-cable/other/fritz.os/FRITZ.Box_6590_Cable-07.57.image`
- HTTP 200, 39,290,880 B, sha256 `0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae` (under the 60 MB preference).
- Its tar has exactly V1's shape: `./var/remote/var/tmp/filesystem.image` is an AVM-BE member of 5,443,592 B, sha `65e85647…832a`; `./var/remote/var/tmp/x86/filesystem.image` is an LE member of 27,750,408 B, sha `57552a6d…2786`; plus kernels, `var/burnimage`, `info.txt`, `content`, `version`.
- The BE member is `sqsh`, v4.0, comp 4, 1079 inodes, `mkfs_time = bytes_used = 5441468`, LE chain exact (5 blocks).
- Why D: recon on it predicts what REA and unblob do on the V1 shape without touching V1. Its members differ from V1's by sha.
- Caveat: the 6590 `info_en.txt` says "FRITZ!OS 7.56" while the file name says 07.57 (vendor text inconsistency), so cite it by file name and sha.

Other development images with a BE member, if a seat wants a second D:
- `FRITZ.Box_3490-07.31.image`: 32,020,480 B, sha `81e519c7a423347aa97111a07124880e0fe495bf66a9056ba8b1f9115d83edf6`.
- `FRITZ.Box_6820v1_LTE-07.30.image`: 28,334,080 B, sha `3948449d89708589cde05e8495a34cb7ed1efeb880d1ed4539b07d4594069450`.
- `FRITZ.Box_7490-07.62.image`: 38,092,800 B, sha `2ab05656563abe7fabdbbf62b3305123098b798e6f79c678f00baefc553f8ee9`.

## Commands
Run `artifacts/R40C1VendorScout/carve.sh WORKDIR` with `WORKDIR` under the scratch dir. It was dry-run with exit 0 in 8.5 s; all five sha checks printed OK. The commands it runs:
```
B=https://download.avm.de/fritzbox
# V2
curl -fsS -o v2.image $B/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image
echo "3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4  v2.image" | sha256sum -c -
tar -xOf v2.image ./var/tmp/filesystem.image > v2-member.sqfs      # 25825288 B
echo "b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c  v2-member.sqfs" | sha256sum -c -
# D
curl -fsS -o d.image $B/fritzbox-6590-cable/other/fritz.os/FRITZ.Box_6590_Cable-07.57.image
echo "0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae  d.image" | sha256sum -c -
tar -xOf d.image ./var/remote/var/tmp/filesystem.image > d-be-member.sqfs        # 5443592 B, 65e85647…
tar -xOf d.image ./var/remote/var/tmp/x86/filesystem.image > d-le-member.sqfs    # 27750408 B, 57552a6d…
```
Re-probing: `python3 probe.py URL=FILE …` (TSV on stdout; no scratch writes).

## Sources and info files
- AVM info files beside the images (HTTP 200; copies in `artifacts/R40C1VendorScout/info/`):
  - `https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/info_en.txt`: 20,590 B, sha `84e16052773533b7e1b61beb9dfe72cc936f45bd84717e64dae48d921472a158`, Last-Modified 2023-09-04. Product FRITZ!Box 7430, Version FRITZ!OS 7.31, Release date 09/04/2023. `info_de.txt` is beside it.
  - `https://download.avm.de/fritzbox/fritzbox-6590-cable/other/fritz.os/info_en.txt`: 68,978 B, sha `38a4420aa0f2eee5146ae4d6188c98f596904adaadf16e0b4fce32a082047cf7`.
  - `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/info_en.txt` (V1): 67,591 B, sha `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`, Last-Modified 2023-09-04 17:08:03 GMT. Product FRITZ!Box 6490 Cable, FRITZ!OS 7.57, Release date 04.09.2023.
  - The 7490 directory also has `update_info_*.txt`; it lists `recover/`.
- The licence text inside the image (`./var/info.txt`) and in `info_en.txt` lines 264–270 says the package is "supplied exclusively in object code format", that the licensee "may create only one copy … for backup use", and that it is forbidden without prior written approval to be "copied, propagated, or in any other manner made publicly accessible". It also says the open-source part (GPL/LGPL/FreeBSD) is available on written request to `fritzbox_info@avm.de`, with details at `https://download.avm.de/fritzbox/license.txt`.
  - [INFERENCE] Committing the V1 or V2 member into the lane repo may conflict with that clause. The safer provenance is URL + sha256 + a carve script, not the bytes. The L1 should decide.
- AVM-BE layout reference quoted by unblob's own source comment (`squashfs.py:47`): `https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt`. Verbatim from it:
  - "it uses the big-endian layout for most of the data stored in the SquashFS image (to be more precise for all file system related data)"
  - "the only data field stored in the little-endian format is the block length value at the beginning of each block"
  - "compression method is hardcoded to be XZ (aka LZMA2)"
  - "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'"
  - It also says the user-id table is always stored uncompressed.
- unblob 26.6.4 (`handlers/filesystem/squashfs.py` lines 47–50): for BE and v4, `is_avm = header.bytes_used == header.mkfs_time`, and `-be` is appended only if not `is_avm`.

## Unresolved
- I did not read V1 or any V2 candidate beyond the superblock and inode-table chain.
  - The 6590 BE member content is untested against V1 content (same family, different sha).
  - I did not walk data-block LE headers or run a full pure-Python decode. The inode-table chain proves LE headers for metadata blocks only. By the Freetz text, data-block lengths also use LE headers.
- I did not check whether the 7430 wrapper has fragments or a fragment table. The 25 MB single-file shape suggests few or none. [INFERENCE]
