# R36ScoutPrebuiltInventory — sasquatch-prebuilt-package-inventory.md re-check (2026-10-26)

Candidate: /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/sasquatch-prebuilt-package-inventory.md (read-only; not edited).
Method: `curl -sS -D h.txt 'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100'` -> HTTP/2 200, `jq length` = 8 (single page, no Link header). Plus the .deb of the newest tag downloaded and unpacked with `ar`/`tar` (dpkg-deb absent). No installs; scratch removed. No tool installed/updated.

## Observed facts (API, 2026-10-26)
| tag | published_at | draft/prerelease | assets |
|---|---|---|---|
| sasquatch-v4.5.1-6 | 2026-01-27T11:57:51Z | false/false | 6 |
| -5 | 2025-02-10T14:54:38Z | | 6 |
| -4 | 2023-06-06T19:02:28Z | | 6 |
| -3 | 2023-04-07T09:59:24Z | | 6 |
| -2 | 2023-03-09T17:43:19Z | | 6 |
| -1 | 2023-03-02T10:01:02Z | | 6 |
| sasquatch-v1.0.1 | 2022-12-03T10:18:00Z | | 6 |
| sasquatch-v1.0 | 2022-02-26T23:10:04Z | | **2** (only `sasquatch_1.0_amd64.deb`, `sasquatch-dbgsym_1.0_amd64.deb`) |

Newest tag assets (sizes B): sasquatch_1.0_amd64.deb 187244; _arm64 170080; _armhf 164428; sasquatch-dbgsym_1.0_amd64 323896; _arm64 327784; _armhf 319048.
Deb control (v4.5.1-6 amd64): `Package: sasquatch`, `Version: 1.0`, `Architecture: amd64`; payload `./usr/bin/sasquatch`, `./usr/bin/sasquatch-v4be`. Installed `~/.local/bin/sasquatch -version` -> `unsquashfs version 4.5.1 (2022/03/17)`.
Release body v4.5.1-6 (verbatim): `* unsquashfs: fix prototypes for C23 by @whispersofthedawn in https://github.com/onekey-sec/sasquatch/pull/32` (also `CI: fix build-nix`, `fix: remove unnecessary magic checks`). Bodies of -4,-3,-2,v1.0.1,v1.0 empty; -1 body: `Rebased on top of squashfs-tools 4.5.1`; -5: Renovate, symlink dir-loop fix, rename IoT Inspector->ONEKEY.
Recheck command: `curl -fsSL .../releases | grep -c 'sasquatch-v4.5.1-6'` -> 12 (reproduced; `grep -o | wc -l` also 12; HTML page `github.com/onekey-sec/sasquatch/releases` title `Releases · onekey-sec/sasquatch · GitHub`).

## Verdict per claim
1. "publishes 8 releases" — **supported** (jq length 8; both are non-draft, non-prerelease).
2. newest `sasquatch-v4.5.1-6`, published 2026-01-27 — **supported** (published_at 2026-01-27T11:57:51Z; still newest on 2026-10-26).
3. "each carrying a Debian package per architecture: amd64/arm64/armhf plus matching dbgsym" — **wrong as universally stated ("each")**: v1.0 (2022-02-26) has amd64 only (2 assets). True for the other 7 releases, and for the newest tag. Fix wording: "7 of 8; v1.0 amd64-only" or "the newest and six others".
4. Asset matrix `sasquatch_1.0_{amd64,arm64,armhf}.deb` + `sasquatch-dbgsym_1.0_*` — **supported** for v4.5.1-6 (six assets as above).
5. "release body shows the packaged upstream version (4.5.1) against the package version (1.0)" — **wrong as sourced**: the v4.5.1-6 body does not contain "4.5.1" or "1.0"; 4.5.1 appears only in the tag name (and the -1 body "Rebased on top of squashfs-tools 4.5.1"); 1.0 only in asset filenames/deb control. The fact itself (upstream 4.5.1 vs package 1.0) is true and I confirmed it from deb control + `-version`, so cite those, not the "release body".
6. body records "unsquashfs: fix prototypes for C23" — **supported** (verbatim quote above, from the v4.5.1-6 body).
7. recheck line `grep -c ... -> 12` — **supported** (reproduced 12) but weak: it counts text lines mentioning the tag, proving neither 8 releases nor the asset matrix. Suggest `jq length` and per-tag asset counts.
8. Caveat paragraph (not the REA-pinned Unblob 26.6.x compatible; "Very beta" from S107; CANNOT-ANSWER.md) — **not checked here** (not API-derivable); [INFERENCE] the sasquatch 4.5.1 binary is installed by L1 and R36 sibling seats test Unblob compat, so the "stays an operator action" statement may already be stale for this lane.
9. Title claim "AUR was never the only route" / F1 framing — supported by existence of the debs; [INFERENCE] arm/deb packaging is irrelevant on this Arch host, so the practical route is the extracted binary (as L1 did) — not stated in the entry.

## Recommendation
**Admit only after correction** (refuse as written): fix claim 3 ("each" -> all but v1.0, which is amd64-only) and claim 5 (attribute 4.5.1/1.0 to tag name, deb control and binary version, not the release body); strengthen the recheck command. Counts, newest tag/date, asset matrix and the C23 quote are accurate and fresh (checked 2026-10-26, 3 days after the entry's 2026-10-23 stamp).
