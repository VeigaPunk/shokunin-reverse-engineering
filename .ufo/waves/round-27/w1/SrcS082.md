# SrcS082 — S082 source row for tinyxxd 1.3.17-1 package provenance

Seat: SrcS082. Wave: round 27, wave 1. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Lane base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0; lane HEAD when read a4f674b343d8564e21f7eb8984630a95089c82d6. The seat was read-only in the lane and wrote this report and nothing else in the lane.

## Behavior

One new SOURCES registry row, S082, whose subject is the package record of the round-27 second carrier: the local pacman database for tinyxxd 1.3.17-1, the pacman sync database entry for the same package, and the upstream Arch package page with its JSON record. The row is kind dataset, tier A, status mined, opened 2026-10-22, recheck on-release, used by corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md and corpus/lessons/round-27.md.

## Gates and observations

Each item names its command, an exact output excerpt, the exit code and the UTC time.

1. Observation — the local mtree digest for the carrier file equals the carrier sha256 in the frozen claims. Command `zcat /var/lib/pacman/local/tinyxxd-1.3.17-1/mtree | grep -F './usr/bin/tinyxxd '`, 2026-10-22T14:59:03Z, exit 0: `./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` — the digest equals the claim sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 and the size 38928 equals the claim size.
2. Observation — ownership and byte identity. Commands `sha256sum /usr/bin/tinyxxd /usr/bin/jq /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat` and `/usr/bin/pacman -Qo /usr/bin/tinyxxd` and `/usr/bin/pacman -Qo /usr/bin/jq`, 2026-10-22T14:59:03Z, exit 0 each: `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65  /usr/bin/tinyxxd`, `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq`, `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat`, `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`, `/usr/bin/tinyxxd is owned by tinyxxd 1.3.17-1`, `/usr/bin/jq is owned by jq 1.8.2-1`. The renamed copies were read only; they were not modified.
3. Observation — the local record's fields. Command `grep -E '%(VERSION|BUILDDATE|PACKAGER|URL)%' -A1 /var/lib/pacman/local/tinyxxd-1.3.17-1/desc`, 2026-10-22T14:59:03Z, exit 0: `1.3.17-1`, `https://github.com/xyproto/tinyxxd`, `1790704346`, `Alexander F. Rødseth <xyproto@archlinux.org>`. Epoch 1790704346 is 2026-09-29T17:52:26Z, matching the upstream page build date.
4. Observation — the upstream page opened by plain HTTP, no bot challenge. Command `curl -sS -L --http1.1 --max-time 45 -A 'Mozilla/5.0' -o arch-tinyxxd.html https://archlinux.org/packages/extra/x86_64/tinyxxd/`, 2026-10-22T11:55Z, HTTP status 200, exit 0. Title `Arch Linux - tinyxxd 1.3.17-1 (x86_64)`; page fields `Build Date: 2026-09-29 17:52 UTC`, `Last Packager: Alexander Rødseth`, `Upstream URL: https://github.com/xyproto/tinyxxd`. A case-insensitive count for `captcha`, `cloudflare`, `challenge`, `cf-browser` and `Just a moment` over the fetched bytes was 0, so the page is an ordinary document and not a challenge.
5. Observation — the upstream JSON record agrees with the local record. Command `curl -sS -L --http1.1 --max-time 45 -A 'Mozilla/5.0' -o arch-tinyxxd.json https://archlinux.org/packages/extra/x86_64/tinyxxd/json/`, 2026-10-22T11:56Z, HTTP status 200, exit 0: `"pkgver": "1.3.17"`, `"pkgrel": "1"`, `"build_date": "2026-09-29T17:52:26Z"`, `"url": "https://github.com/xyproto/tinyxxd"`, `"filename": "tinyxxd-1.3.17-1-x86_64.pkg.tar.zst"`, `"packager": "arodseth"`.
6. Observation — the local sync database member for the same version carries the package file digest. Command: a Python read of the tar member `tinyxxd-1.3.17-1/desc` of /var/lib/pacman/sync/extra.db, 2026-10-22T14:57Z, exit 0: `%SHA256SUM%` `3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce`, `%VERSION%` `1.3.17-1`, `%BUILDDATE%` `1790704346`, `%PACKAGER%` `Alexander F. Rødseth <xyproto@archlinux.org>`.

## jq cross-check (report only, no row proposed)

7. Observation — yes, the jq mtree carries the carrier sha256. Command `zcat /var/lib/pacman/local/jq-1.8.2-1/mtree | grep -F './usr/bin/jq '`, 2026-10-22T14:59:03Z, exit 0: `./usr/bin/jq time=1781975439.0 size=30800 sha256digest=e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` — equal to the claim sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806. The jq local desc gives version 1.8.2-1, packager `Felix Yan <felixonmars@archlinux.org>`, build epoch 1781975439 (2026-06-20T17:10:39Z), upstream `https://jqlang.github.io/jq/`; the sync database member `jq-1.8.2-1/desc` carries `%SHA256SUM%` 35f197700d1e8a1692fd67c644c1e57a72f4969707772ac1f477b02351248e1b. The jq Arch JSON record was fetched too (sha256 711974cdb2f2a025e826a70e1c9864abd7b80fcdc999a0106dfe81dc52ebf994, build_date 2026-06-20T17:10:39Z, packager felixonmars) and is not proposed as a row.

## Drafts, verbatim

SOURCES registry row, 11 columns in the shape of corpus/SOURCES.md:

| S082 | Arch Linux package record for tinyxxd 1.3.17-1 — local pacman database `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc` and `/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree` (gzip), repository database member `tinyxxd-1.3.17-1/desc` of `/var/lib/pacman/sync/extra.db`, and the upstream package page https://archlinux.org/packages/extra/x86_64/tinyxxd/ with its JSON record https://archlinux.org/packages/extra/x86_64/tinyxxd/json/ | dataset | A | The installed bytes of the round-27 carrier `/usr/bin/tinyxxd` as recorded by the local pacman database, and the upstream Arch record of the same package version; not the tool's behaviour, its upstream source tree, or any claim about other versions or other machines | Local `desc`: `%VERSION%` `1.3.17-1`, `%BUILDDATE%` `1790704346`, `%PACKAGER%` `Alexander F. Rødseth <xyproto@archlinux.org>`, `%URL%` `https://github.com/xyproto/tinyxxd`; local `mtree` entry `./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`; sync database `%SHA256SUM%` `3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce` for `tinyxxd-1.3.17-1-x86_64.pkg.tar.zst`; Arch page `Build Date: 2026-09-29 17:52 UTC`; opened 2026-10-22 | The carrier's bytes are the package's own recorded file: the pacman mtree digest for `./usr/bin/tinyxxd` equals the carrier sha256 and the local record's version, packager, build epoch and upstream URL agree with the upstream Arch record, so the second carrier's identity is a named package record rather than a bare file | mined | 2026-10-22 | on-release | corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md, corpus/lessons/round-27.md |

Gate table lines for corpus/lessons/round-27.md, same five columns as the round-26 Gate table:

| S082 | local pacman desc `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc`; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "Alexander F. Rødseth <xyproto@archlinux.org>" | `%PACKAGER%` |
| S082 | same desc file; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "1790704346" | `%BUILDDATE%` |
| S082 | same desc file; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "https://github.com/xyproto/tinyxxd" | `%URL%` |
| S082 | local pacman mtree `/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree`, gzip; opened 2026-10-22 | compressed a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58; decompressed cd9ad639309eccbeadcaa05425a64b19b54c9802feb58cba61a2f80efe2cd36b | "./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65" | mtree entry for `./usr/bin/tinyxxd` |
| S082 | pacman sync database `/var/lib/pacman/sync/extra.db`, member `tinyxxd-1.3.17-1/desc`; opened 2026-10-22 | database file 0b07b40310883996d6313f0980e841757a4832eb1ef0c8785477f5875a95fd63; member bytes a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941 | "3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce" | `%SHA256SUM%` |
| S082 | https://archlinux.org/packages/extra/x86_64/tinyxxd/ ; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Build Date: 2026-09-29 17:52 UTC" | `Build Date` |
| S082 | same package page; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Last Packager: Alexander Rødseth" | `Last Packager` |
| S082 | same package page; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Upstream URL: https://github.com/xyproto/tinyxxd" | `Upstream URL` |
| S082 | https://archlinux.org/packages/extra/x86_64/tinyxxd/json/ ; opened 2026-10-22 | 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb | "\"build_date\":\"2026-09-29T17:52:26Z\"" | `build_date` |

Search-log sentence for the corpus/SOURCES.md search log:

- 2026-10-22 UTC, round 27 — Question: which package record ties the round-27 second carrier's bytes to a named upstream package? Where searched: the local pacman database `/var/lib/pacman/local/tinyxxd-1.3.17-1/{desc,mtree}`, the pacman sync database `/var/lib/pacman/sync/extra.db` member `tinyxxd-1.3.17-1/desc`, and the upstream Arch package page plus its JSON endpoint, all opened by plain HTTP fetch with no browser; identified 3 source families, screened 3, included 1 (row S082), excluded 0; the jq cross-check used the same three families for a report-only reading and added no row.

## Touched surfaces and out of scope

- Lane: read only. This seat created no file in the lane except this report. No git or jj command was run against the lane or the fleet root. No package was installed or upgraded.
- No SOURCES.md, lesson, knowledge, SCORECARD, LOG, SKILL, PROVINCE, SHONEN, QUALITY or corpus file was edited; the row, Gate lines and search-log sentence are drafts for the L1 to integrate.
- The renamed copies under /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/ were read, never modified. No REA call was made by this seat.

## Findings and limits

- Observation: the mtree digest check passes for both carriers; the jq question is answered yes.
- Observation: the upstream Arch page and JSON endpoint are plain documents, not a bot challenge, so no source is recorded as unopened.
- Finding: a first `curl` without `--http1.1` failed with `curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading` and HTTP status 000 at 2026-10-22T11:55Z; the retry with `--http1.1` returned HTTP 200. The plain-reader tool also failed with `ECONNRESET`, so the page was opened by curl only.
- Limit: the Arch package page and its JSON endpoint do not publish the package file digest, so the `%SHA256SUM%` value comes from the local sync database snapshot dated 2026-10-17 22:37, not from the upstream page.
- Limit: that sync database is a snapshot; the row rests on the installed local database and the upstream page agreeing on version, build epoch, packager and upstream URL, plus the mtree digest matching the carrier bytes.
- Unknown: the upstream project tree at https://github.com/xyproto/tinyxxd was not opened; the row claims only the package record.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/SrcS082/)

- draft.md sha256 e52d0609b83ac4278a88901c4848e630b7a6432e5b739d90c53eb9699b6ac714 (the drafts above)
- tinyxxd-mtree.txt sha256 cd9ad639309eccbeadcaa05425a64b19b54c9802feb58cba61a2f80efe2cd36b (decompressed mtree)
- jq-mtree.txt sha256 f7f25cc362c326e585f20fa357207d8d618d7459838f515031e0fabe25a8684d (decompressed mtree)
- arch-tinyxxd.html sha256 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89
- arch-tinyxxd.json sha256 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb
- arch-jq.json sha256 711974cdb2f2a025e826a70e1c9864abd7b80fcdc999a0106dfe81dc52ebf994
- extra-db-tinyxxd-desc.txt sha256 a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941
- extra-db-jq-desc.txt sha256 c2b7f289617328432eb22a78c58dc27c037820577330250d6a8c1447443c09d4

## Tooling

No install or upgrade was needed. Tools used: curl 8.23.0 and Python 3.14.8 as already installed.
