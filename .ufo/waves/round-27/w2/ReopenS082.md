# ReopenS082 — re-open of SOURCES row S082 and its round-27 Gate lines

Seat: KaidokuR27.ReopenS082, round 27, wave 2, attempt 1. Leaf reviewer; no subagents or background jobs; no lane writes except this file.
Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Tip examined: 4084d8975b684a8837b1c858eea0008ce9ab49e0 (main). The working corpus/SOURCES.md and corpus/lessons/round-27.md match that HEAD byte for byte.
Claims freeze a4f674b343d8564e21f7eb8984630a95089c82d6: S082 is absent there, and claims.json is unchanged since it.
All times are UTC, 2026-10-22. Run window 15:36:14Z to 15:42:56Z.

## Verdict

- Carrier identity holds. The local pacman mtree digest for ./usr/bin/tinyxxd equals the carrier sha256. The package file's usr/bin/tinyxxd has the same sha256, and the sync record names that package file.
- 11-column shape holds: the registry header, the S082 row and all 82 registry rows have 11 cells.
- Gate lines 31 to 35 hold. Gate lines 36 to 39 fail as worded. Lines 36 to 38 quote text that is not contiguous in the fetched page bytes, and their page sha256 cannot be reproduced. Line 39 is missing a space.
- The facts behind every failing quote hold. The failures are in quote and hash wording.

## Gate lines (corpus/lessons/round-27.md, lines 31 to 39)

| Line | Source | Quote | sha256 cell | Verdict |
|---|---|---|---|---|
| 31 | local desc, %PACKAGER% | `Alexander F. Rødseth <xyproto@archlinux.org>` | a2d70e53… reproduced | holds |
| 32 | local desc, %BUILDDATE% | `1790704346` | same, reproduced | holds |
| 33 | local desc, %URL% | `https://github.com/xyproto/tinyxxd` | same, reproduced | holds |
| 34 | local mtree, ./usr/bin/tinyxxd line | `./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c…` | gz a5e4c9e6… and text cd9ad639… reproduced | holds |
| 35 | sync db member, %SHA256SUM% | `3f84d7de…` | db 0b07b403… and member a8a2df3f… reproduced | holds |
| 36 | Arch page, Build Date | `Build Date: 2026-09-29 17:52 UTC` | 4e5fff12… not reproduced | fails |
| 37 | Arch page, Last Packager | `Last Packager: Alexander Rødseth` | same | fails |
| 38 | Arch page, Upstream URL | `Upstream URL: https://github.com/xyproto/tinyxxd` | same | fails |
| 39 | Arch JSON, build_date | `"build_date":"2026-09-29T17:52:26Z"` | 30e4c410… reproduced | fails |

## Checks (command, output excerpt, exit code, UTC time, verdict)

Script: verify_s082.py (in scratch), run as `python3 verify_s082.py > verify_s082.out`; exit 0 at 15:42:10Z. It ran 49 checks: 44 PASS, 5 FAIL. Excerpts come from verify_s082.out.

1. Local desc hash. `sha256sum` of /var/lib/pacman/local/tinyxxd-1.3.17-1/desc gives a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456. Exit 0, 15:36:14Z. Holds.
2. Local mtree hash. `gzip -t` and `gzip -dc` exit 0. Compressed a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58; decompressed cd9ad639309eccbeadcaa05425a64b19b54c9802feb58cba61a2f80efe2cd36b. Exit 0, 15:37:35Z. Holds.
3. Mtree line. Script: "PASS | R34 quote is one exact mtree line | ./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c…ae65". Exit 0, 15:42:10Z. Holds.
4. Mtree digest against carrier. `sha256sum /usr/bin/tinyxxd` gives 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65. Script: "PASS | mtree sha256digest equals carrier sha256"; size 38928 and mtime 1790704346 also PASS. Exit 0, 15:36:49Z and 15:42:10Z. Holds.
5. Installed-file integrity. `pacman -Qkk tinyxxd`: "tinyxxd: 12 total files, 0 altered files". Exit 0, 15:42:56Z. Holds (query only).
6. Sync db file and member. `sha256sum /var/lib/pacman/sync/extra.db` gives 0b07b40310883996d6313f0980e841757a4832eb1ef0c8785477f5875a95fd63. `bsdtar -xOf` of member tinyxxd-1.3.17-1/desc gives a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941 (1246 bytes). Exit 0, 15:37:35Z. Holds.
7. Package file behind the sync record (extra check). `curl -sS -L` to the archlinux.org download link: "http=200 bytes=28521". `sha256sum` gives 3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce, equal to %SHA256SUM%. `zstd -t` passes. Exit 0, 15:39:06Z. Holds.
8. Package payload and metadata (extra check). `bsdtar -xOf` gives usr/bin/tinyxxd with sha 7b1e5d0c…ae65 (equal to the carrier), .PKGINFO 5406009934062f4a5a8ec7743a824b8aac31c4bf68d8e2199e7353198cb022c9 and .BUILDINFO 24fb383f27f1a0d8cd8b255056e68da2e6ea0bfd8e1ea72789f2d2ffff3711aa. The local mtree digests for .PKGINFO and .BUILDINFO equal these. Exit 0, 15:39:08Z and 15:42:10Z. Holds.
9. Arch JSON bytes. `curl -sS -L` to the json/ endpoint: "http=200 bytes=685 type=application/json". sha 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb, equal to line 39's sha cell. Exit 0, 15:37:35Z. Holds.
10. JSON content. Script: build_date epoch equals %BUILDDATE% (1790704346); pkgver-pkgrel 1.3.17-1 equals %VERSION%; url equals %URL%. All PASS. Exit 0, 15:42:10Z. Holds.
11. Line 39 quote. Script: "FAIL | R39 quote verbatim in JSON bytes | "build_date":"2026-09-29T17:52:26Z"" and "INFO | R39 spaced variant present in JSON bytes | True". Exit 0, 15:42:10Z. Fails.
12. Arch page sha. `curl` three times with the default user agent (15:39:06Z), and once with the wave-1 command `--http1.1 -A 'Mozilla/5.0'` (15:40:44Z; first try exit 35, "TLS connect error ... unexpected eof"; retry exit 0). Raw sha256 values: 13a43c9c…ce, 533408b2…12, f334c684…09, 5ded5ddd…75. None is 4e5fff12…. With nonce attributes removed, all four give 6b033af362d20dcfb85b3fa5032c81a6e74bb50030b697d1f5914c06c0d57beb. Fails (not reproducible).
13. Arch page quotes (lines 36 to 38). Script: "FAIL | R36 quote contiguous in page bytes", the same FAIL for R37 and R38; "PASS | … present in rendered text (tags to spaces)" and "PASS | … label and value sit in separate markup cells" for all three. Exit 0, 15:42:10Z. Fails as worded; holds as rendered text.
14. Registry shape. Script: "PASS | SOURCES registry header has 11 columns"; "PASS | S082 registry row has 11 cells | 11"; "PASS | every registry row has 11 cells | rows=82". Exit 0, 15:42:10Z. Holds.
15. Registry status and used-by. Script: "mined", "2026-10-22" and "on-release" PASS; both used-by paths exist. Exit 0, 15:42:10Z. Holds.
16. Gate shape. Script: "PASS | Gate S082 row count is 9 | 9"; "PASS | Gate S082 rows have 5 cells". Exit 0, 15:42:10Z. Holds.
17. Lane HEAD and working files. `git rev-parse HEAD` gives 4084d8975b684a8837b1c858eea0008ce9ab49e0. `git show HEAD:<file> | cmp - <file>` exit 0 for both files. Exit 0, 15:37:35Z. Holds.
18. Freeze comparison. `git show a4f674b3…:corpus/SOURCES.md | cmp -` exit 1, first difference at line 87. The lessons file is "not in a4f674b3". `git diff --stat a4f674b3 HEAD` gives 2 files, 96 insertions. claims.json `cmp` exit 0. Script PASS: "S082 row absent at claim-freeze commit". Exit codes as shown, 15:40:18Z to 15:42:10Z. Observation: S082 was added after the freeze.

## Findings (failures, with counterexamples)

F1. Line 39, JSON quote, fails verbatim. Counterexample: the Gate cell has no space after the colon, but the JSON bytes read "build_date": "2026-09-29T17:52:26Z" (checks 9 and 11). Likely a transcription loss (inference: the wave-1 report SrcS082.md item 5 has the spaced form). Fix: quote the spaced form, or the contiguous fragment 2026-09-29T17:52:26Z.
F2. Lines 36 to 38, page quotes, fail "contiguous". Counterexample: the string "Build Date: 2026-09-29 17:52 UTC" does not occur in the bytes. The bytes hold `<th>Build Date:</th>`, whitespace, then `<td>2026-09-29 17:52 UTC</td>`. Lines 37 and 38 likewise join a label cell with an anchor's text (check 13). Fix: quote the contiguous value (2026-09-29 17:52 UTC, Alexander Rødseth, https://github.com/xyproto/tinyxxd) and put the label in the section column, or state that the quotes are rendered-text composites. The registry row (SOURCES.md line 88) repeats the composed Build Date string, so the same fix applies there.
F3. Lines 36 to 38, page sha256 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89, does not reproduce (check 12). Each fetch carries a new CSP nonce in a script tag (nonce values 7ix5zuu1Hp+QNesdzh4/1g==, CgJew7KDrOLdqrK4FK9ZNw==, SjlXqSLgnrXoGc4fcYXs1w==). Inference: the wave-1 bytes carried another nonce, so that hash cannot be re-derived. Fix: record a nonce-normalised hash, or mark the page hash as not reproducible with its fetch time.

## Holds (observations)

O1. The mtree digest equals the carrier sha256; size and mtime equal the file's stat (check 4).
O2. The chain holds end to end: sync %SHA256SUM% equals the package file sha; the package's usr/bin/tinyxxd equals the carrier; the package's .PKGINFO and .BUILDINFO equal the local mtree (checks 6 to 8).
O3. The JSON agrees with the local desc on version, URL and build epoch 1790704346 = 2026-09-29T17:52:26Z (check 10). The page's Last Packager link points to packager=arodseth, the person named in the local desc (observed in page markup).
O4. "11-column shape" refers to the registry table, as the wave-1 draft wrote it. The mtree is not a column table; its tinyxxd line has four whitespace tokens (check 14).
O5. S082 post-dates the claim freeze (check 18).

## Residual risk and gaps

- Unknown: the package's PGP signature (sync %PGPSIG%) was not checked; no gpg run.
- The package came through the archlinux.org redirect to the third-party mirror mirror.accum.se. Trust rests on the hash chain to the sync record, not on the mirror.
- Unknown: the wave-1 page bytes behind 4e5fff12… cannot be recovered; only nonce-normalised content was compared.
- The read tool's reader fetch failed (ECONNRESET) and was not used.
- One machine, one version (1.3.17-1). No claim about other machines or versions.
- Not checked: rows S079 and S081 (out of scope).

## Scratch artifacts (sha256)

Directory /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReopenS082/:

verify_s082.py 3e9b786c90dad608c3da83619569740b3193adffef0ef443bb6e0cc5feadfa84
verify_s082.out 7d90d8b6a976c2f2826a49be8f8b7a18e8e14efe7a9ed119ca5bdf700595db4d
local-desc a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456
local-mtree.gz a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58
local-mtree.txt cd9ad639309eccbeadcaa05425a64b19b54c9802feb58cba61a2f80efe2cd36b
sync-tinyxxd-1.3.17-1-desc a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941
arch-page.html 13a43c9c986bf4507f1954eeafffafc6b2ab0ce7aca4b5805b1ad8078f5fe5ce
arch-page-2.html 533408b27e6ae9a9f45ed0c516b4b67bb38675075445ce64c73e61e15ed97d12
arch-page-3.html f334c684ed0404e4549c0e9daf85132bc852b297a547bd16e939b4cfa935a409
arch-page-w1cmd-5.html 5ded5dddfb94d3932109b773353d04b9c5831cd862431cfc2e0303f9b422b75c
arch-page-2.headers 445670d79367d664af90c03e318cf07cda3e332a62f99ad0959ab6bc90b29a7d
arch-page-3.headers adbf91dcb1d1c74fc385f79b32c36016a2b3b1d9bacf1d6ec6a13155fac2c378
arch-json.json 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb
tinyxxd-1.3.17-1-x86_64.pkg.tar.zst 3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce
pkg-usr-bin-tinyxxd 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65
pkg-PKGINFO 5406009934062f4a5a8ec7743a824b8aac31c4bf68d8e2199e7353198cb022c9
pkg-BUILDINFO 24fb383f27f1a0d8cd8b255056e68da2e6ea0bfd8e1ea72789f2d2ffff3711aa

## Tooling

No installs or upgrades. Used existing curl, zstd, bsdtar, gzip, Python 3.14.8 (standard library), and pacman in query mode only (-Qo, -Qi, -Ql, -Qkk, -Si). No pacman transaction ran. Lane files were not changed.
