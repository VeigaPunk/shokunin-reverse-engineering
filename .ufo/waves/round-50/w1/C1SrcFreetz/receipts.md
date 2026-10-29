# C1SrcFreetz receipts (round 50, wave 1). All times UTC, 2026-10-28.

Commands run (scratch `/fast/scratch/hyaku/kaidoku-r50/C1SrcFreetz`, no lane tree write):

| # | command (abridged) | exit | evidence |
|---|---|---|---|
| R1 | `curl -sS -D <f>.hdr -o <f> -w "%{http_code} %{size_download}" <raw URL>` for `tools/make/squashfs4-host-be/AVM-BE-format.txt` and `patches/101-…symbols_only.patch` | 0 / 0 | `200 1496` (AVM-BE-format.txt, Date 23:31:51Z, etag daa140…); `200 1153` (101 patch, Date 23:31:54Z, etag 76cf03…). Headers saved with no Set-Cookie (grep: none). |
| R2 | `sha256sum` of R1 files | 0 | `sha256-receipts.txt` lines 1–2 |
| R3 | `curl` GitHub contents API `repos/Freetz/freetz/contents/tools/make/squashfs4-host-be/patches?ref=master` (JSON listing, 25 entries) | 0 | `sources/patches-index.txt` sha256 `78b9a231311436a65aa37b6f2a124c04268b95824b964b9e74e0b47b7f926ad6`; HTTP 200 |
| R4 | `curl` raw `patches/100-TARGET_FORMAT.patch`, `250-mksquashfs__AVM_BE.patch`, `350-unsquashfs__AVM_BE.patch`, `squashfs4-host-be.mk`, `550-mkfs_time__AVM_BE_AVM_LE.patch` | 0 | all HTTP 200; 550 Date 23:32:41Z, 1,080 B; mk 2,482 B; sha256 in `sha256-receipts.txt` |
| R5 | `curl` raw for all 25 patches listed in R3 into scratch, `sha256sum` each, grep `AVM` / `mkfs_time` / `bytes_used` | 0 | `sources/allpatches-sha.json`; `AVM_LE` occurs only in 101 (`:7`, `:17`, `:24`) and 550 (`:7`, `:24`); `AVM_BE`-conditional only in 250, 350; `mkfs_time` write only in 550 (`:8`) and reads in 100/240/400 unrelated to AVM |
| R6 | `python3 -I -B tools/round-50/quote-check.py` (seat tool, located-substring test over stated line ranges) | 0 | `QUOTE_CHECK located=12 missing=0`; output `tools/round-50/quote-check.out.txt`, sha256 `d6d95cb01a5c05ade26539f6e277baf505c89103e70ee33cf5aec4a1bde7fbdf` (scratch copy) |
| R7 | `git grep -c S150 7c678ae6d97aedb969fd253b52b3d2882ef1e186 -- corpus` (read-only; output truncated by the tool at 10 lines) | 0 | at least 10 lesson files cite S150 (`round-35.md`, `round-35-verifier-spotcheck.md`, `round-36.md`, `round-38.md`, `round-38-verifier-spotcheck.md`, `round-39.md`, `round-40.md`, `round-43.md`, `round-44.md`, `round-45-verifier-spotcheck.md`); S150 occurs 239 times repo-wide (`grep -rhoE`); `corpus/SOURCES.md` has no S150 at base |
| R8 | `grep -rhoE '\bS[0-9]{3}\b' --exclude-dir=.git .` at lane root, first id ≥S150 not present | 0 | first uncited id `S243` |
| R9 | `find . -name CORPUS.md -not -path './.git/*'` at lane root | 0 (empty output) | no CORPUS.md in the lane; `corpus/QUALITY.md:110` points tier definitions to `corpus/SOURCES.md`, whose header carries no tier-letter definitions |
| R10 | `curl` `api.github.com/...squashfs4-host-be` directory listing | 0 | 3 entries: AVM-BE-format.txt, patches, squashfs4-host-be.mk |

Checks NOT run: no unblob, sasquatch, or REA run (out of seat scope); no data run; no git mutation anywhere; no lane file written.

Tool installs/updates in this seat: none.
