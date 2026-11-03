# ScoutJscRoute — Upstream Reconnaissance for R64-C1 (round 64, w1)

Seat: `ScoutJscRoute` (round 64, wave w1, attempt 1).  
Role: scout.  
Surface: Upstream GitHub repository `xqy2006/jsc2js`, releases API, release assets, raw README at commit `01fc264d`, and local git tree.  
Full details: `.ufo/waves/round-64/w1/ScoutJscRoute/findings.md`.

---

## Verdict & Summary

All five assigned reconnaissance checks were completed. Upstream `main` matches the frozen commit `01fc264d22055865a460b322399a15d84b71f5aa` with zero drift. The three target d8 releases exist with verified tarball digests matching local preserved archives; their difference from `PINS` is confirmed (API provides compressed tarball digests, whereas `PINS` in `jsc-route-matrix.py` pins the extracted `d8` executable binaries). The upstream release count has grown from 677 (claimed in S129) to 679 (7 pages, all 679 tags distinct, +2 upstream releases). The README sentences on matching d8 and the View8 invocation were located with exact line numbers and quoted verbatim. `View8/view8.py` was confirmed present in the git tree at the pinned commit.

---

## Evidence Table

| # | claim | command | observed | verdict |
|---|---|---|---|---|
| 1 | Upstream `main` at `01fc264d` | `git ls-remote https://github.com/xqy2006/jsc2js refs/heads/main` | `01fc264d22055865a460b322399a15d84b71f5aa refs/heads/main` | **match** |
| 2a | Release `14.8.178.14` asset name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.8.178.14` | asset: `d8-14.8.178.14-linux.tar.gz`, size: 13,796,728 B, digest: `sha256:9326e285066c5d06b76f4c8487091be9695888202b823a796b950a22691ee5f6`. Differs from `PINS["D1"]` (`bc70d3c0...`) which pins the extracted `d8` binary. Local tarball absent under `/home/vgpnk/.local/share/kaidoku-jsc` (only unpacked tree exists). Lead scratch tarball sha256 matches API digest byte-for-byte. | **verified** |
| 2b | Release `14.8.178.1` asset name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.8.178.1` | asset: `d8-14.8.178.1-linux.tar.gz`, size: 13,797,051 B, digest: `sha256:87a8afe9869235aeece3d4461335b52e2ec5e8c9d73da9ad5fa261cc4abb6ea3`. Differs from `PINS["D2"]` (`4060ff2e...`). Local tarball absent under `/home/vgpnk/.local/share/kaidoku-jsc`. Lead scratch tarball sha256 matches API digest byte-for-byte. | **verified** |
| 2c | Release `14.7.173` asset name, size, digest vs PINS | `curl -sS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/14.7.173` | asset: `d8-14.7.173-linux.tar.gz`, size: 13,962,025 B, digest: `sha256:fe51888335060dab0a00e741c92539b8cdd72f44d8955180d58b12b8c80738de`. Differs from `PINS["D3"]` (`c240ffae...`). Local tarball absent under `/home/vgpnk/.local/share/kaidoku-jsc`. Lead scratch tarball sha256 matches API digest byte-for-byte. | **verified** |
| 3 | Upstream releases count & distinct tags across pages 1..7 | Paginated API query `.../releases?per_page=100&page={1..7}` | Pages 1–6: 100 releases each; Page 7: 79 releases. Total = 679 releases, distinct tags = 679. S129 claimed 677 (+2 releases published upstream: `15.6.75.25` on 2026-10-30, `15.2.124.45` on 2026-10-28). | **verified drift (+2)** |
| 4a | README sentence on matching d8 (<=25 words) | `https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md` | Line 199: `"- V8 bytecode opcodes, register/slot layouts, and handler table structures vary across versions. Always use a **matching** d8 build."` (18 words) | **verified** |
| 4b | README view8 invocation (<=25 words) | Same raw README at commit `01fc264d` | Line 152: `"python view8.py --disassembled ../xxx.txt ../xxx.js"` (5 words). Also line 44: `"python view8.py --disassembled ../xxx.txt ../xxx.js"`. | **verified** |
| 5 | Confirm View8 path in git tree at `01fc264d` | `git -C /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src ls-tree 01fc264d22055865a460b322399a15d84b71f5aa View8/` | Tree lists `View8/view8.py` (blob `bab4a42d8dcf3d22941b90b3ed079916463b0ae1`, sha256 `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c` matches `PINS["view8.py"]`). | **match** |

---

## Detailed Findings

### 1. Upstream Commit Identity
- Command: `git ls-remote https://github.com/xqy2006/jsc2js refs/heads/main`
- Exit: 0
- Output: `01fc264d22055865a460b322399a15d84b71f5aa refs/heads/main`
- Finding: Upstream `main` has not drifted since the round-64 freeze. The local checkout at `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src` is clean and detached at this exact commit.

### 2. Tarball Assets vs PINS
- In `tools/round-64/jsc-route-matrix.py`, `check_pins()` compares `d / "d8"` against `PINS["D1"]`, `PINS["D2"]`, and `PINS["D3"]`:
  - `D1`: `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` (unpacked ELF binary)
  - `D2`: `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` (unpacked ELF binary)
  - `D3`: `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` (unpacked ELF binary)
- The GitHub Releases API provides digests for the compressed `.tar.gz` tarball assets:
  - `14.8.178.14`: `d8-14.8.178.14-linux.tar.gz`, 13,796,728 B, API digest `sha256:9326e285066c5d06b76f4c8487091be9695888202b823a796b950a22691ee5f6`
  - `14.8.178.1`: `d8-14.8.178.1-linux.tar.gz`, 13,797,051 B, API digest `sha256:87a8afe9869235aeece3d4461335b52e2ec5e8c9d73da9ad5fa261cc4abb6ea3`
  - `14.7.173`: `d8-14.7.173-linux.tar.gz`, 13,962,025 B, API digest `sha256:fe51888335060dab0a00e741c92539b8cdd72f44d8955180d58b12b8c80738de`
- Local tarball check under `/home/vgpnk/.local/share/kaidoku-jsc`: No tarball archives exist; only unpacked trees `d8-14.8.178.14/`, `d8-14.8.178.1/`, `d8-14.7.173/` are present. No binaries were downloaded.
- Tarball archives in lead scratch (`/fast/scratch/hyaku/kaidoku-r64/lead/`) match the GitHub API digests byte-for-byte.

### 3. Release Count Inventory & Drift
- Paging through the GitHub Releases API (`https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=N` for N=1..7):
  - Page 1: 100
  - Page 2: 100
  - Page 3: 100
  - Page 4: 100
  - Page 5: 100
  - Page 6: 100
  - Page 7: 79
  - Total releases: 679
  - Distinct tags: 679 (zero duplicate tag names)
- S129 claimed 677 releases. Upstream published 2 new releases since S129 was recorded:
  - `15.6.75.25` (published 2026-10-30T09:32:59Z)
  - `15.2.124.45` (published 2026-10-28T09:01:59Z)

### 4. README Quotes and Line Numbers
- Raw README fetched from `https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md` (sha256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`, 219 lines, identical to local `jsc2js-src/README.md`).
- Matching d8 rule:
  - **Line 199** (under `## Notes`): `"- V8 bytecode opcodes, register/slot layouts, and handler table structures vary across versions. Always use a **matching** d8 build."` (18 words).
  - Also in Quick Start heading **Line 128**: `### 1. Get the matching d8`, and **Line 130**: `"Go to the Releases page and choose the V8 version that is **identical to** the one that produced your target .jsc."` (23 words).
- View8 invocation:
  - **Line 152** (under `### 3. Use the modified View8 to reconstruct JavaScript`): `"python view8.py --disassembled ../xxx.txt ../xxx.js"` (5 words).
  - (Also in Chinese section at **Line 44**: `"python view8.py --disassembled ../xxx.txt ../xxx.js"`).

### 5. View8 Path in Git Tree
- Command: `git -C /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src ls-tree 01fc264d22055865a460b322399a15d84b71f5aa View8/`
- Output:
  ```
  040000 tree 254314fb9358c28de415c187a06e3d93a29292be	View8/Bin
  040000 tree 3f9b4fdf29b18729a0ceee539e6a4be3a5d7013b	View8/Parser
  100644 blob 9769294bfb1a112aa9e48264041fc2575652eaa4	View8/README.md
  040000 tree f4f588f8348617f02af0fa23b056124000c04ea0	View8/Simplify
  040000 tree 030b511091679ce68fa071db185f6261e49fb8cb	View8/Translate
  100644 blob bab4a42d8dcf3d22941b90b3ed079916463b0ae1	View8/view8.py
  ```
- File `View8/view8.py` exists, with object hash `bab4a42d8dcf3d22941b90b3ed079916463b0ae1` and content sha256 `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c`, exactly equal to `PINS["view8.py"]`.

Report: .ufo/waves/round-64/w1/ScoutJscRoute.md
