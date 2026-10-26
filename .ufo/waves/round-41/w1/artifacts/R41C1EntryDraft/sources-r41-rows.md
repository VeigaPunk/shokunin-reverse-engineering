corpus/SOURCES.md — R41-C1 landing text (draft; L1 applies it at the freeze)
=======================================================================

One new row. R41-C1 requires the entry to cite a SOURCES row that is ABSENT at the base
(`49096c7e`) and whose `used-by` cell names the entry (binding `sourced` of
`tools/round-41/c1-counter.py`, and `sourced_new` of the supplementary gate). The highest id at the base
is `S126` (`git show 49096c7e:corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort -u | tail -1`), so the new
row is `S127`.

S127 was opened by the round-41 source seat; the numbers below are that seat's measured served bytes
(`.ufo/waves/round-41/w1/artifacts/R41SrcAvm/{avm-http-probe.tsv,identity-crosscheck.tsv}`, listings and
info files fetched 2026-10-26T20:23Z), cross-checked against this wave's V3 fetch
(`.ufo/waves/round-41/w1/artifacts/R41C1VendorV3/fetch-5490.json`). If the source seat lands a different
row text, the L1 must use the source seat's text and keep only the two invariants: `opened` = `2026-10-26`
and `used-by` naming the entry stem.

Append at the end of the `## Registry` table (exactly 11 cells per row; no `|` inside a cell):

| S127 | AVM FRITZ!Box 5490 and 5491 FRITZ!OS 07.31 firmware download directories — https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/; https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/ (files `info_en.txt`, `info_de.txt`, `FRITZ.Box_5490-07.31.image`, `FRITZ.Box_5491-07.31.image`) | dataset | A | The vendor's own published identity for the V3 and V4 carrier images: product, FRITZ!OS version, release date, advertised file sizes, ETags and the licence notice; not the SquashFS layout of any member, not licence permission to redistribute or reverse engineer, not other models or FRITZ!OS versions | opened 2026-10-26T20:23Z: both `fritz.os/` listings HTTP 200, 574 B, sha256 `88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4` (5490) and `badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7` (5491); `info_en.txt` 50 653 B sha256 `e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18` (5490) and 53 166 B sha256 `ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4` (5491), both carrying `Product:` at line 8, `Version: FRITZ!OS 7.31` at line 10 and `Release date: 09/04/2023` at line 14; image HEAD 200 with Content-Length 33 269 760 and ETag `64f592ae-1fba800` (5490), 36 392 960 and ETag `64f5a91e-22b5000` (5491); licence text at lines 665-670 (5490) and 688-693 (5491) restricts redistribution and reverse engineering | Bind the V3 and V4 carrier images to a vendor-published product and version before any layout claim, and read the licence sentence before publishing anything beyond derived metadata | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md |

Notes
-----
- Not drafted: an own-work row for the four fresh carriers. Their provenance is the frozen
  `.ufo/waves/round-41/c1/carriers.json` (pins, fetch chain, oracle paths) plus
  `corpus/evidence/round-41/c1/`, which is what `S126`-style own-work rows would only duplicate; a source
  row exists for opened external sources.
- The 5490 and 5491 info files are CRLF Latin-1 (a strict UTF-8 read fails at 5490 byte 17974), so quote
  them with byte offsets or line numbers, never by re-encoded text.
- The 5491 `info_en.txt` tail signature line `HKR 2021/11/17` predates its own `Release date: 09/04/2023`;
  that is the source's own inconsistency and is not a carrier defect (the 5490 pair agrees on
  `DHA 2023/09/04`).
- `S127` must not be cited anywhere the entry's `source:` lines do not also carry it, and the entry must
  keep at least one `source:` line naming `S127` after any copy-edit: the binding reads only lines whose
  first token is `source`.
