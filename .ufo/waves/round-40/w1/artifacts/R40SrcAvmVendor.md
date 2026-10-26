# R40SrcAvmVendor — SOURCES candidate for vendor carrier V1

**Verdict: DONE.** One 11-column row drafted (`artifacts/R40SrcAvmVendor/row.md`); no existing download.avm.de / AVM row in `corpus/SOURCES.md`; the candidate is mineable. Mismatch with the assignment: `./var/info.txt` inside the image is only the AVM licence notice and names no product or version; the product/version quote comes from `info_en.txt` and the image's `./var/content`.

## Registry check
`grep -n "download.avm.de" corpus/SOURCES.md` and `grep -n "avm"` → no hits (exit 1). Last registry id is S122 (rows S120-S122 read). Row id S123 is provisional; the L1 assigns the real id. Kind `dataset` (vendor published record; closest existing kind: S015/S037), recheck `on-release` (the file is a 2023 release frozen by hash).

## Fetches (curl, no auth; access UTC from `date -u` before each fetch)
| URL (under https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/) | UTC | HTTP | bytes | sha256 |
|---|---|---|---|---|
| (directory listing) | 2026-10-26T18:18:06Z | 200 | 592 | 063ec39af00bd45e668519cc2ce95debf41cf5d56ed9dcde37223b57f6d8f7bc |
| info_en.txt | 2026-10-26T18:18:13Z | 200 | 67591 | 6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7 |
| info_de.txt | 2026-10-26T18:18:17Z | 200 | 111698 | 3becce798a914683a366e838aab015d31d5c361a4eb32ab401ee77f40cdc5a1e |
| FRITZ.Box_6490_Cable-07.57.image | 2026-10-26T18:18:19Z | 200 | 39741440 | f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d (equals the assignment's V1 hash) |

Listing is only three files (image, info_de.txt, info_en.txt, all Last-Modified 04-Sep-2023 17:08); there is no separate release-notes file beyond info_*.txt. Header files are saved next to the copies.

## Image-internal text members (tar extraction of three small text members only; `tar tvf` listing; no REA/unblob/sasquatch run on any member, no carrier read)
Tar listing includes `./var/remote/var/tmp/filesystem.image` 5443592 B, `./var/remote/var/tmp/x86/filesystem.image` 28200968 B (sizes as in the assignment/tar header), `kernel.image` 1932808 / x86 3552264.
- `./var/info.txt` 2807 B sha256 b0360d8820be53c70365dc0adfc19a665efb19dc510dd75126466f82ae07e39b — bilingual AVM licence notice ("© AVM GmbH 2006 …", forbids copying, distributing, reverse engineering/decompiling "in whole or in part"). Names no product/version.
- `./var/content` 346 B sha256 ab238b0ed62419a4f3f32454e81bb14ef4bbce7ce462f7631f9555a38eca9557: `Product=Fritz_Box_HW213a (FRITZ!Box 6490 Cable)`, `Type=Release`, `Releasecycle=MOVE21NL1`, `Version=07.57`, `Build=107830`.
- `./var/version` 47 B sha256 288451feb464cffe24faccd236a49e6bf97a24b4687753eb875fdd95958fbdb3: `FIRMWAREVERSION=141.07.57,,107830,120308002013`.

## Located quotes (<=25 words)
- info_en.txt lines 8-14: "Product: FRITZ!Box 6490 Cable … Version: FRITZ!OS 7.57 … Release date: 04.09.2023" (16 words).
- `./var/content`: "Product=Fritz_Box_HW213a (FRITZ!Box 6490 Cable)" … "Version=07.57" … "Build=107830".
- info_en.txt "Further Improvements of FRITZ!OS 7.57": "Fixed stability and security increased" (no layout information).

## Caveats
- The licence notice (`var/info.txt`, `license.txt` link) forbids redistribution and reverse engineering; the 39.7 MB image was therefore NOT copied into artifacts (sha256 + URL cited; rebuild: `curl -O <image URL>` and check sha256) and its text members are copied only as 3 small files for the identity quote [INFERENCE: quoting short notice text for identification is low risk; the L1 may prefer to drop `image-members/info.txt`].
- The source teaches product/version identity only. It says nothing about AVM-BE SquashFS layout; that claim needs the pure-Python oracle / sasquatch-v4be evidence and S121.
- Scratch was /fast/scratch/hyaku/kaidoku-r40/R40SrcAvmVendor; removed at end.

## Artifacts (`.ufo/waves/round-40/w1/artifacts/R40SrcAvmVendor/`)
row.md, fetched.sha256, listing.html/.hdr, info_en.txt(+.hdr), info_de.txt(+.hdr), FRITZ.Box_6490_Cable-07.57.image.hdr, image-members/{info.txt,version,content}.

Tools: none installed. Commands: curl -sS -D hdr -o file URL; sha256sum; `tar xf image ./var/info.txt ./var/version ./var/content`.
