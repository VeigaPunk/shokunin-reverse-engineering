# R38ScoutFreetzAvm — Freetz AVM-BE SquashFS note: provenance, fidelity, SOURCES verdict

Seat: scout (leaf, advisory). Lane corpus untouched. Scratch removed (`/fast/scratch/hyaku/kaidoku-r38/R38ScoutFreetzAvm`, `/tmp/r38freetz_keep` gone). No tools installed.

## Path correction (observed)
The assignment names `.ufo/waves/round-38/probes/avm.txt`; that path does not exist (`.ufo/waves/round-38/` has no `probes/`). The committed copy is `.ufo/waves/round-37/probes/avm.txt` (1496 bytes, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`), committed in base `77091b492cc53f8743bd0701b1e7d5e66123dd84` (`git log`, 2026-10-26 02:33 -0300). This is the file the R37-CL2 lesson and the round-38 claims line 107 refer to. Any SOURCES row must name the round-37 path.

## Upstream (observed)
- Primary page: Freetz-NG docs wiki, "SquashFS 4 (BE)".
  - Blob URL: https://github.com/Freetz-NG/freetz-ng/blob/master/docs/wiki/60_Development/squashfs4-be.en.md
  - Raw URL fetched: https://raw.githubusercontent.com/Freetz-NG/freetz-ng/master/docs/wiki/60_Development/squashfs4-be.en.md (HTTP 200, 1514 bytes, sha256 `100948f38ea0ff7258eee00a420e67b090fd9a1e7e191361d03b9a9604875fc9`)
  - Git blob sha (GitHub contents API): `9c4d82d23e1dec01dc3016efb81abf4a8c1ed7c2`
  - Last commit touching the path: `f9157c387a116d6b8d6a8c99e2626c10495ed71f`, 2021-02-15T16:20:26Z, "host tools: move description to docs"
  - master HEAD at access: `eb0540c021690e6178e9d2d8a27d731f19f62126` (2026-10-25T22:53:08Z)
  - Access UTC: **2026-10-26T06:17:20Z** (fetch window 06:17:20–06:17:21Z; API checks to 06:17:39Z).
- Sibling upstream version (same format, different wording): https://raw.githubusercontent.com/dnicolodi/squashfs-avm-tools/master/README-AVM-BE (`main` identical; HTTP 200, 1408 bytes, sha256 `74108564e0a997772803aa48f8de847bcc6317d0a088cfe2f67da497e47555ca`; last commit `dfffa9db3d31985af5989d08efc4adbdcfd21770`, 2020-10-10T08:24:42Z). It is NOT what avm.txt copies.
- Not found: `squashfs4-be.de.md` / `.md` (404). The older freetz.org trac page was not located; not needed.

## Fidelity verdict: avm.txt is a faithful copy — YES (one-line delta)
`diff squashfs4-be.en.md avm.txt` → only `1d0 < # SquashFS 4 (BE)`: avm.txt omits the Markdown heading line. `diff <(tail -n +2 squashfs4-be.en.md) avm.txt` → empty (rc 0): body byte-identical (1514 − 18 heading bytes = 1496). So copy = upstream body minus its H1 title; modification is a stripped title only. Provenance line must say "heading `# SquashFS 4 (BE)` removed". It is not a copy of the dnicolodi README (diff shows full rewording).

## Claim verification
Located quotes (≤25 words, from the upstream page, present verbatim in avm.txt lines 8–9 and 15–16):
- Block length: "the only data field stored in the little-endian format is the block length value at the beginning of each block" (21 words).
- mkfs_time: "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'" (21 words).

1. Block-length field little-endian — **as stated by the note: confirmed present** (also in the dnicolodi README: "the only data field stored in the little-endian format is the block length value at the beginning of each block"). Independent byte-level confirmation on a real AVM image: **not available** in the lane (no AVM firmware carrier).
2. mkfs_time == bytes_used — **as stated by the note: confirmed present** (both upstream texts). Same: no real AVM image to check.
3. Cross-check on the committed fixtures `be-squashfs_v4.bin` (4096 B) and `be-squashfs_v4.nopad.bin` (307 B), parsed big-endian (python `struct`, superblock):
   - magic `sqsh`, version 4.0, comp id 1 (gzip), flags 0xc0, inodes 5, mkfs_time 1646222857, bytes_used 307 → **mkfs_time ≠ bytes_used**.
   - inode-table metadata header at offset 121: bytes `00 3a`; BE value 0x3a = 58 = dir_table(181) − inode_table(121) − 2, i.e. the block length is **big-endian** (LE read would give 0x3a00).
   - Both properties contradict AVM-BE (comp is gzip not XZ; block length BE not LE; mkfs_time real). [INFERENCE-free, observed] The fixtures are plain big-endian SquashFS v4, not AVM-BE. This reinforces the round-37 verdict "AVM-BE stays Frontier": the note supports the claim that the plain `-be` path cannot decode AVM-BE, but no carrier in the lane is AVM-BE, so the note supports no promotion.

## SOURCES verdict for the C1 Gate: ADMIT (class: format description, tier B/secondary; scope-limited)
Reason: R37-CL2 requires every third-party text the claims lean on to have a row; the lesson table (round-37-verifier-spotcheck.md line 70) already cites avm.txt for the AVM-BE Frontier reject. The page is the primary maintainer statement of the format (Freetz developers, credited analysis by PeterPawn), small, stable (last edit 2021-02-15), byte-pinned (sha256 above), and its two checkable claims are matched by the independent dnicolodi README.
Scope to state in the row: supports only "AVM-BE = SquashFS4 with BE fs data, LE block-length, XZ hardcoded, mkfs_time == bytes_used, COMP_OPT unset in seen images, uid table uncompressed (author TODO)"; not any carrier property, not unblob's behaviour (S108 covers that), not that sasquatch-v4be extracts it, not that `be-squashfs_v4*.bin` are AVM-BE (they are not, see above).
Limits: community reverse-engineered note; "so far known"; own TODO on uid table; no firmware sample bytes.
Flip condition → reject/downgrade: (a) a real AVM-BE image shows block length BE, or mkfs_time ≠ bytes_used, or non-XZ compression; (b) upstream path removed/reworded so the quote no longer matches the pinned sha256; (c) no claim in round 38 actually leans on it — if C1 never cites avm.txt, the row is housekeeping only and could be omitted without harm (then R37-CL2 closes by removing the file reference instead). Promotion flip for AVM-BE capability itself: only with a real AVM-BE carrier whose oracle matches the note's two properties.
Suggested row fields: URL = blob URL above; access 2026-10-26T06:17:20Z; upstream blob sha `9c4d82d…`; commit `f9157c38…`; local copy path `.ufo/waves/round-37/probes/avm.txt` sha256 `c1c43f6f…`, upstream raw sha256 `100948f3…`, delta = H1 line removed.

## Commands (key)
`curl -sS -m 30 -o F -w '%{http_code}' <raw url>`; `diff`/`sha256sum`; `curl https://api.github.com/repos/Freetz-NG/freetz-ng/{commits?path=…,contents/…}`; python3 `struct` parse of the two fixtures (exit 0). Limit: GitHub unauthenticated API; browser rendering of the blob page not used (raw + API sufficed).
