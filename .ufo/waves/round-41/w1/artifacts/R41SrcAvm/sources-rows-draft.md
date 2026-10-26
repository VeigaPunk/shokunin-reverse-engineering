# R41SrcAvm — draft SOURCES rows for the round-41 freeze (S127, S128)

Seat: `R41SrcAvm`. Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Nothing here is committed.
Schema source: `git show 49096c7:corpus/SOURCES.md` header (11 columns) and rows S124-S126.
Paste the two lines below immediately after row S126, one row per line, no blank line between them.
They contain no literal `|` inside any cell, so the lane's 11-column row regex
(`tools/round-35/c1-coverage-counter.py:ROW_RE`) parses them; `check-rows.py` in this directory proves it.

```
| S127 | AVM FRITZ!Box 5490 FRITZ!OS 07.31 download directory and info_en.txt — https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/ (files info_en.txt, info_de.txt, FRITZ.Box_5490-07.31.image) | dataset | A | The vendor's own published identity (product, FRITZ!OS version, release date, the directory's single image name, its size and mtime) for the V3 carrier image; not the SquashFS layout, superblock or member contents of that image, not a build number, not licence permission to redistribute or reverse engineer, not other FRITZ!OS versions or models | opened 2026-10-26T20:21:50Z, HTTP 200 for the listing (574 B, sha256 88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4), info_en.txt (50653 B, sha256 e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18, Last-Modified 2024-11-18 14:01:57 GMT) and info_de.txt (56125 B, sha256 519e5038d4e28935f6c356333d0d48062e770125b11f2092600486b6b174a5c9) each fetched twice with identical digests, plus a HEAD of the image (200, 33269760 B, ETag 64f592ae-1fba800 = mtime+size, Last-Modified 2023-09-04 08:17:50 GMT; body not fetched); both info files are CRLF and Latin-1, not UTF-8 (strict UTF-8 fails at info_en.txt byte 17974); info_en.txt lines 8-14 "Product: FRITZ!Box 5490 / Version: FRITZ!OS 7.31 / Release date: 09/04/2023", line 29 "# Further Improvements of FRITZ!OS 7.31", line 672 "DHA 2023/09/04", lines 663-670 the AVM licence notice | The listing, info_en.txt, info_de.txt (Release-Datum 04.09.2023), the image Last-Modified and the trailing signature line all agree on FRITZ!Box 5490 and 2023-09-04, so V3 may be cited as FRITZ!OS 07.31 for that model; info_en.txt names only the template FRITZ.Box_5490-xx.xx.image (line 1), so the filename-to-version binding rests on the directory's single image entry; the file carries no Build number, so build identity must come from the image's own var/content; the licence notice forbids reverse engineering and redistribution, so cite the image by sha256 and keep it out of the lane | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md |
| S128 | AVM FRITZ!Box 5491 FRITZ!OS 07.31 download directory and info_en.txt — https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/ (files info_en.txt, info_de.txt, FRITZ.Box_5491-07.31.image) | dataset | A | The vendor's own published identity (product, FRITZ!OS version, release date, the directory's single image name, its size and mtime) for the V4 carrier image; not the SquashFS layout, superblock, nested member or filesystem_core contents of that image, not a build number, not licence permission to redistribute or reverse engineer, not other FRITZ!OS versions or models | opened 2026-10-26T20:21:52Z, HTTP 200 for the listing (574 B, sha256 badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7), info_en.txt (53166 B, sha256 ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4, Last-Modified 2024-11-18 14:01:04 GMT) and info_de.txt (47098 B, sha256 dc663791cbb0499e69d0be097a844ed105772c2c7ad8e33d6e9b8397292c745e) each fetched twice with identical digests, plus a HEAD of the image (200, 36392960 B, ETag 64f5a91e-22b5000 = mtime+size, Last-Modified 2023-09-04 09:53:34 GMT; body not fetched); both info files are CRLF and Latin-1, not UTF-8; info_en.txt lines 8-14 "Product: FRITZ!Box 5491 / Version: FRITZ!OS 7.31 / Release date: 09/04/2023", line 30 "# Further Improvements of FRITZ!OS 7.31", line 695 "HKR 2021/11/17", lines 686-693 the AVM licence notice | The listing, info_en.txt, info_de.txt (Release-Datum 04.09.2023) and the image Last-Modified agree on FRITZ!Box 5491 and 2023-09-04, so V4 may be cited as FRITZ!OS 07.31 for that model; the trailing signature line is stale (info_en.txt 695 and info_de.txt 584 read 2021/11/17, two years before the stated release date), so never date this carrier from the file tail; info_en.txt carries no Build number, so build identity must come from the image's own var/content; the licence notice forbids reverse engineering and redistribution, so cite the image by sha256 and keep it out of the lane | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md |
```

## Why these two rows, and what they deliberately do not say

- The frozen C1 predicate needs the vendor carriers' identity to be citable without holding vendor bytes
  (AVM licence, `info_en.txt` lines 663-670 / 686-693: no redistribution, no "opened" reverse engineering).
  These rows are the identity half of that chain; the image -> member -> carrier sha256 chain stays with the
  V3/V4 seats and the round-41 provenance artifacts.
- Tier `A`: the vendor's own distribution page, opened live this round.
- Kind `dataset`: the rows describe published dataset identity (names, sizes, dates), not a document's rules.
- Used-by is the round-41 knowledge entry named by the draft predicate. That file does not exist at the base
  or in the worktree yet; the entry seat owns it.
- Recheck `180d` (not `on-release`): the v2 instruction for this item allows only an ISO date or `NNd`, and
  this is a static archive directory (fritz.os body unchanged since 2023-09-04, listing last touched
  2024-11-18, both proven by 304 responses on If-None-Match and If-Modified-Since at 2026-10-26T20:22:28Z
  and 20:22:31Z). A vendor re-release would move the ETag, which the anchor records.

## Verification performed on these rows

- `python3 check-rows.py sources-rows.txt` (this directory) parses both rows with the round-35 row regex and
  asserts: exactly 11 columns each, no stray `|`, single physical line each, ids absent from the base
  registry (S127/S128 are the next free ids after S126), status `mined`, opened `2026-10-26`,
  recheck `180d`, used-by the round-41 entry path.
- Every hash, size, HTTP status, ETag, Last-Modified and access instant quoted in the cells is reproduced in
  `avm-http-probe.tsv`; the quoted lines are reproduced verbatim in `quote-excerpts.txt`.
