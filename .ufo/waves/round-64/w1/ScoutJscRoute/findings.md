# ScoutJscRoute — Findings: Upstream Recon for R64-C1

Seat: `ScoutJscRoute`  
Wave: `round-64/w1`  
Date: 2026-11-03  
Target: Upstream reconnaissance for jsc2js / View8 / d8 toolchain underpinning R64-C1.

---

## Findings Table

| claim | command | observed | verdict |
|---|---|---|---|
| 1. Upstream `main` commit equals `01fc264d22055865a460b322399a15d84b71f5aa` | `git ls-remote https://github.com/xqy2006/jsc2js refs/heads/main` | `01fc264d22055865a460b322399a15d84b71f5aa refs/heads/main` | **match** (zero drift on upstream `main`) |
| 2a. Release asset `14.8.178.14`: linux name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.8.178.14` | asset: `d8-14.8.178.14-linux.tar.gz`, size: 13,796,728 B, digest: `sha256:9326e285066c5d06b76f4c8487091be9695888202b823a796b950a22691ee5f6`. Differs from `PINS["D1"]` (`bc70d3c0...`) because PINS holds the unpacked `d8` binary hash, not the tarball digest. Local tarball is absent under `/home/vgpnk/.local/share/kaidoku-jsc` (unpacked directory exists). The preserved tarball in lead scratch (`/fast/scratch/hyaku/kaidoku-r64/lead/d8-14.8.178.14-linux.tar.gz`) has sha256 `9326e285...`, matching the API digest byte-for-byte. | **verified** (API digest matches tarball; PINS pins unpacked binary `d8`) |
| 2b. Release asset `14.8.178.1`: linux name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.8.178.1` | asset: `d8-14.8.178.1-linux.tar.gz`, size: 13,797,051 B, digest: `sha256:87a8afe9869235aeece3d4461335b52e2ec5e8c9d73da9ad5fa261cc4abb6ea3`. Differs from `PINS["D2"]` (`4060ff2e...`, unpacked binary). Local tarball absent under `/home/vgpnk/.local/share/kaidoku-jsc`. Lead scratch copy sha256 matches API digest `87a8afe9...`. | **verified** (API digest matches tarball; PINS pins unpacked binary `d8`) |
| 2c. Release asset `14.7.173`: linux name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.7.173` | asset: `d8-14.7.173-linux.tar.gz`, size: 13,962,025 B, digest: `sha256:fe51888335060dab0a00e741c92539b8cdd72f44d8955180d58b12b8c80738de`. Differs from `PINS["D3"]` (`c240ffae...`, unpacked binary). Local tarball absent under `/home/vgpnk/.local/share/kaidoku-jsc`. Lead scratch copy sha256 matches API digest `fe518883...`. | **verified** (API digest matches tarball; PINS pins unpacked binary `d8`) |
| 3. Upstream release count & distinct tag count across pages N=1..7 (S129 claims 677) | Paginated fetch `https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page={1..7}` | Pages 1..6: 100 releases each. Page 7: 79 releases. Total releases = 679. Distinct tag names = 679. S129 claimed 677 (+2 new releases published upstream: `15.6.75.25` on 2026-10-30 and `15.2.124.45` on 2026-10-28). | **verified drift** (679 releases, all distinct; +2 over S129) |
| 4a. README matching d8 quote (line number, <=25 words) | `curl -sS https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md` | Line 199: `"- V8 bytecode opcodes, register/slot layouts, and handler table structures vary across versions. Always use a **matching** d8 build."` (18 words) | **verified** (exact line & quote located; sha256 `df85060f...`) |
| 4b. README view8 invocation quote (line number, <=25 words) | Same README at `01fc264d` | Line 152 (English section): `"python view8.py --disassembled ../xxx.txt ../xxx.js"` (5 words). Also line 44 (Chinese section): `"python view8.py --disassembled ../xxx.txt ../xxx.js"` (5 words). | **verified** (exact line & quote located) |
| 5. View8 path in repo tree at `01fc264d` | `git -C /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src ls-tree 01fc264d22055865a460b322399a15d84b71f5aa View8/` | Lists `View8/Bin`, `View8/Parser`, `View8/README.md`, `View8/Simplify`, `View8/Translate`, and `100644 blob bab4a42d8dcf3d22941b90b3ed079916463b0ae1 View8/view8.py`. Working tree file and commit blob sha256 is `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c`. | **match** (`view8.py` present at path, matches `PINS["view8.py"]`) |

---

## Detailed Notes

### Upstream Commit
- Upstream `refs/heads/main` at `https://github.com/xqy2006/jsc2js` points to `01fc264d22055865a460b322399a15d84b71f5aa`.
- The local clone at `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src` is checked out detached at this exact commit with a clean working tree.

### Tarball vs Binary Pin Clarification
- The instrument `tools/round-64/jsc-route-matrix.py` checks `d / "d8"` against `PINS["D1"]`, `PINS["D2"]`, and `PINS["D3"]` (`check_pins()` lines 150-157).
- These pins correspond to the unpacked ELF executables:
  - `D1`: `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` (`d8-14.8.178.14/d8`)
  - `D2`: `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` (`d8-14.8.178.1/d8`)
  - `D3`: `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` (`d8-14.7.173/d8`)
- The GitHub Releases API provides SHA-256 digests of the compressed tarballs:
  - Tag `14.8.178.14`: `d8-14.8.178.14-linux.tar.gz` (13,796,728 bytes) -> `sha256:9326e285066c5d06b76f4c8487091be9695888202b823a796b950a22691ee5f6`
  - Tag `14.8.178.1`: `d8-14.8.178.1-linux.tar.gz` (13,797,051 bytes) -> `sha256:87a8afe9869235aeece3d4461335b52e2ec5e8c9d73da9ad5fa261cc4abb6ea3`
  - Tag `14.7.173`: `d8-14.7.173-linux.tar.gz` (13,962,025 bytes) -> `sha256:fe51888335060dab0a00e741c92539b8cdd72f44d8955180d58b12b8c80738de`
- Under `/home/vgpnk/.local/share/kaidoku-jsc/`, only the extracted directories exist; no local tarball files are present.
- The tarball copies preserved in lead scratch (`/fast/scratch/hyaku/kaidoku-r64/lead/`) match the GitHub API digests exactly.

### Upstream Releases Count & Drift
- Paging through GitHub API releases (`per_page=100`, pages 1 to 7):
  - Page 1: 100
  - Page 2: 100
  - Page 3: 100
  - Page 4: 100
  - Page 5: 100
  - Page 6: 100
  - Page 7: 79
  - Total releases: 679 (all 679 tag names distinct).
- Compared to S129 inventory count of 677, upstream added 2 releases:
  - `15.6.75.25` (published 2026-10-30T09:32:59Z)
  - `15.2.124.45` (published 2026-10-28T09:01:59Z)

### README Location & Citations
- Fetched raw `README.md` from GitHub raw URL at commit `01fc264d` (sha256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`, 219 lines).
- Matching d8 sentence at line 199:
  > "- V8 bytecode opcodes, register/slot layouts, and handler table structures vary across versions. Always use a **matching** d8 build."
- Quick Start section also specifies matching d8 at lines 128 & 130:
  > Line 128: `### 1. Get the matching d8`  
  > Line 130: `Go to the Releases page and choose the V8 version that is **identical to** the one that produced your target .jsc. (Open an Issue if the version you need is missing.)`
- View8 reconstruction command at line 152:
  > `python view8.py --disassembled ../xxx.txt ../xxx.js`
  (And in Chinese section at line 44: `python view8.py --disassembled ../xxx.txt ../xxx.js`).
