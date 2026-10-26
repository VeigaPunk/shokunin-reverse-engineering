# R41W2SrcReopen — S127/S128 reopened live: rows hold, the entry's licence-line citation does not

**Verdict: CONFIRMED (both rows) — DONE, nothing falsified.** S127 and S128 re-derived true on 89/89
machine checks against bytes fetched independently today; the registry shape, novelty and used-by cells
are correct. One real **citation defect** sits one hop away, in the round-41 entry the rows point at
(F1: it attributes S128's licence lines to S127, which has no such lines), plus three calibration nits.

What I attacked: every factual assertion in both rows' 11 cells, re-fetched rather than re-read —
HTTP status, body bytes and sha256, sizes, `HEAD` metadata and its `ETag = mtime+size` arithmetic,
CRLF/Latin-1 encoding with the row's stated UTF-8 failure offset, every quoted line at its stated line
number, the non-claims ("no build number", "not the SquashFS layout", "not licence permission"), the
registry parse (11 cells / 12 pipes / id novelty / duplicate scan), the used-by target, and — beyond what
the rows claim — whether the identity page actually describes the bytes C1 pinned.

## 1. Method and exit codes

Lane `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`; row text read with read-only git (`git show`). Re-open
window 2026-10-26, first AVM server `Date: Mon, 26 Oct 2026 21:19:10 GMT`. Exact commands:
`artifacts/R41W2SrcReopen/commands.sh` (steps 1-8). Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41W2SrcReopen`,
removed at the end; every byte the checker reads is re-creatable with step 2-4 of that script.

| step | command | exit | observed |
|---|---|---|---|
| rows | `git -C "$L" show e9a24d07…:corpus/SOURCES.md` | 0 | 230 lines, rows at 133/134 |
| S127 GET listing / info_en / info_de | `curl -sS -D hdr -o body -w '%{http_code} %{size_download}'` | 0 | `200 574` / `200 50653` / `200 56125` |
| S127 image | `curl -sSI … FRITZ.Box_5490-07.31.image` | 0 | `HEAD 200` |
| S128 GET listing / info_en / info_de | same | 0 | `200 574` / `200 53166` / `200 47098` |
| S128 image | same | 0 | `HEAD 200` |
| second fetch (stability) | `curl -o *.2.*` for all four GET bodies | 0 | byte-identical to first fetch, 8/8 |
| validator | `curl -H 'If-None-Match: "<etag>"'` on both info_en | 0 | `304` / `304` |
| image bodies | `curl -o img-<model>.bin` then `sha256sum`, `rm` | 0 | 33 269 760 B and 36 392 960 B, digests below |
| re-derive row claims | `python3 -I -B check-reopen.py --sources … --dir … --carriers …` | **0** | **89 PASS, 0 FAIL** (`check-reopen-output.txt`) |
| shape / novelty / used-by | `awk`+`git show`/`cat-file -e`/`diff` | 0 | `row-shape.txt` |

One non-zero exit in the whole seat, and it is not a failure: `grep -c "build"` printed `0` and therefore
exited 1 (no matches) — that zero is the "no Build number" evidence.

## 2. Per-row verdict

### S127 — AVM FRITZ!Box 5490 FRITZ!OS 07.31 directory + info_en.txt — **CONFIRMED**

| row claim | re-observed 2026-10-26 | verdict |
|---|---|---|
| listing HTTP 200, 574 B, sha256 `88c8d648…8c4a19f4` (row: `88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4`) | `200`, 574 B, identical digest, identical on second fetch | true |
| `info_en.txt` 50 653 B, sha256 `e3100cda…7360d18`, Last-Modified 2024-11-18 14:01:57 GMT | `200`, 50 653 B, identical digest, `Last-Modified: Mon, 18 Nov 2024 14:01:57 GMT`, `ETag "673b48d5-c5dd"`, 304 on revalidation | true |
| `info_de.txt` 56 125 B, sha256 `519e5038…174a5c9` | `200`, 56 125 B, identical digest, same Last-Modified | true |
| both info files "each fetched twice with identical digests" | my two fetches + wave-1's two = four observations, all equal | true |
| image `HEAD` 200, 33 269 760 B, `ETag 64f592ae-1fba800 = mtime+size`, Last-Modified 2023-09-04 08:17:50 GMT, body not fetched | `200`, `content-length: 33269760`, `etag: "64f592ae-1fba800"`; `0x1fba800 = 33269760` exactly and `0x64f592ae` = `Mon, 04 Sep 2023 08:17:50 GMT` exactly | true |
| directory's single image name | listing `<a href>` set is `../`, `FRITZ.Box_5490-07.31.image`, `info_de.txt`, `info_en.txt` — exactly one `.image` | true |
| its size and mtime in the listing | `04-Sep-2023 08:17 33269760` — agrees with `HEAD` | true |
| info files are CRLF and Latin-1, not UTF-8; strict UTF-8 fails at info_en byte 17974 | 671 CRLF / 0 bare LF; strict UTF-8 fails at **byte 17974** on the `0xE4` of "Telegärtner"; info_de fails at byte 44 | true |
| quote, lines 8-14: `Product: FRITZ!Box 5490 / Version: FRITZ!OS 7.31 / Release date: 09/04/2023` | L8 `Product:\tFRITZ!Box 5490`, L10 `Version:        FRITZ!OS 7.31`, L14 `Release date:   09/04/2023` | true (11 words; see F5 on formatting) |
| line 29 `# Further Improvements of FRITZ!OS 7.31` | present at L29 | true |
| line 672 `DHA 2023/09/04` | present at L672 | true |
| lines 663-670 licence notice | L663 ©, L665 licence text, L667 grant, L669-670 the two prohibitions | true |
| info_en names only the template `FRITZ.Box_5490-xx.xx.image` (line 1) | L1 verbatim | true |
| "carries no Build number" | case-insensitive `build` count in both info files = **0** | true |
| "not the SquashFS layout, superblock or member contents" | `squash` = 0, `filesystem` = 0 in both info files | true |
| licence forbids reverse engineering and redistribution | L669-670: "copied, propagated … made publicly accessible" / "processed, disassembled, reverse engineered …" | true |
| listing, both info files, image mtime and trailing signature all agree on 5490 / 2023-09-04 | `Product: FRITZ!Box 5490`; `Release-Datum: 04.09.2023` (info_de L14); image mtime 2023-09-04; `DHA 2023/09/04` | true |

### S128 — AVM FRITZ!Box 5491 FRITZ!OS 07.31 directory + info_en.txt — **CONFIRMED** (one rounding nit F2)

| row claim | re-observed 2026-10-26 | verdict |
|---|---|---|
| listing 200, 574 B, sha256 `badbb744…583af6f7` | `200`, 574 B, identical digest, identical on second fetch | true |
| `info_en.txt` 53 166 B, sha256 `ec2528eb…51970b4`, Last-Modified 2024-11-18 14:01:04 GMT | `200`, 53 166 B, identical digest, `Last-Modified` as recorded, `ETag "673b48a0-cfae"`, 304 | true |
| `info_de.txt` 47 098 B, sha256 `dc663791…292c745e` | `200`, 47 098 B, identical digest | true |
| image `HEAD` 200, 36 392 960 B, `ETag 64f5a91e-22b5000 = mtime+size`, Last-Modified 2023-09-04 09:53:34 GMT | `0x22b5000 = 36392960` exactly; `0x64f5a91e` = `Mon, 04 Sep 2023 09:53:34 GMT` exactly | true |
| single image name | href set `../`, `FRITZ.Box_5491-07.31.image`, `info_de.txt`, `info_en.txt` | true |
| CRLF + Latin-1, not UTF-8 (no byte offset claimed) | 694 CRLF / 0 bare LF in info_en (583/0 in info_de); strict UTF-8 fails at byte 18 256 (info_de: 50) | true |
| quote, lines 8-14 identity | L8/L10/L14 as quoted | true (11 words) |
| line 30 `# Further Improvements of FRITZ!OS 7.31` | present at L30 | true |
| line 695 `HKR 2021/11/17` | `HKR 2021/11/17.` at L695 (trailing period omitted in the quote) | true |
| info_de line 584 also reads 2021/11/17 | `HKR 2021/11/17.` at L584 | true |
| lines 686-693 licence notice | L686 ©, L688 text, L690 grant, L691-693 prohibitions | true |
| trailing signature is stale, "two years before the stated release date" | 2021-11-17 → 2023-09-04 = 656 d = **1.80 years** | true in substance, **rounded up** (F2) |
| "never date this carrier from the file tail" | inference the stale line supports; the © line also reads `2004?2021` (mojibake for an en dash) | sound |
| no Build number / not the SquashFS layout / licence restrictions | same measurements as S127: `build` = 0, `squash` = 0, `filesystem` = 0; L691-693 prohibitions present | true |

## 3. Registry shape, novelty, used-by

- Both rows parse as **11 cells with 12 pipes**; lengths 2111 and 2086 chars (equal to the wave-1 lint's
  numbers), cells trimmed, no embedded pipe.
- Base revision `49096c7e…` tops out at **S126**, so S127/S128 are novel; at the frozen revision the ids
  run S124, S125, S126, S127, S128 with **no duplicate ids**.
- `kind=dataset`, `tier=A`, `status=mined`, `recheck=180d` for both; `180d` is the registry's normal
  interval for a mutable vendor page (dozens of rows use it) and **S125**, the sibling AVM vendor-image
  row, is `dataset`/`A`/`mined` too — convention consistent.
- Used-by cell is exactly `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, which **exists at
  the same revision** (`git cat-file -e`), and the committed rows are **byte-identical** to
  `w1/artifacts/R41SrcAvm/sources-rows.txt` — the landing did not silently edit the wave-1 rows.
- Located quotes are 11 / 6 / 4 words — inside the 25-word rule.

## 4. Beyond the rows: the identity page binds to the pinned carrier bytes

The rows only claim a `HEAD`, so a same-named file could in principle differ. I fetched both bodies to
scratch, hashed them, and deleted them (no vendor bytes kept; licence respected):

| carrier | downloaded size | sha256 | equals `carriers.json` `external.image_sha256` |
|---|---|---|---|
| V3 (5490) | 33 269 760 B | `770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7` | **yes** |
| V4 (5491) | 36 392 960 B | `a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661` | **yes** |

Both sizes equal the listing sizes and the `HEAD` `Content-Length`. So the vendor identity page each row
cites is the identity of the exact bytes the C1 carriers pin — the row's phrase "for the V3/V4 carrier
image" is byte-level true, and `Accept-Ranges: bytes` is served on both images.

## 5. Findings

- **F1 (defect, minor, landing doc).** `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md:128` reads
  `[S127 licence lines 665-670 / 688-693 restrict …]`. S127's `info_en.txt` has 672 lines, so 688-693
  cannot be S127's; they are S128's. Wave 1's own crosscheck
  (`w1/artifacts/R41SrcAvm/identity-crosscheck.tsv:18`) shows the intended pairing (5490 L665-670,
  5491 L688-693). Both ranges also skip the notice's © line (S127 L663 / S128 L686), which the rows
  themselves include. Repair: `[S127 licence lines 663-670 / S128 686-693 …]`. The rows are not at fault;
  this is the only place where a reader following the citation lands on nothing.
- **F2 (calibration nit).** S128 "two years before the stated release date" is 1.80 years (656 days).
  The staleness and the "never date from the tail" inference stand.
- **F3 (calibration nit).** `corpus/lessons/round-41.md:44-45`: the "located quote (≤25 words)" column
  holds a *description* with a pointer, not a quote, for S127/S128 — unlike S129 on line 46. The rows
  themselves carry compliant quotes.
- **F4 (coverage note).** S127/S128 record no image sha256 (HEAD only) while sibling row S125 records its
  image digest; the digests exist in `carriers.json` and are reproducible (proved here). Adding
  `image_sha256` to the two rows would make the registry self-binding. Not an overclaim: their scope cell
  promises only "size and mtime".
- **F5 (note).** The anchor-cell quote joins three labels with ` / ` and normalises tab runs; each fragment
  is verbatim at its line (checked), and verbatim text is retained in `w1/…/quote-excerpts.txt` and in
  `check-reopen-output.txt`. Same convention as S125, so consistent, not a defect.
- **F6 (limit).** The rows' `opened` timestamps (20:21:50Z / 20:21:52Z) match `w1/R41SrcAvm.md` and the
  w1 probe TSV's later pass, but are not independently re-observable; my earliest observation is the
  21:19:10Z server `Date`. [INFERENCE] consistent with the wave-1 artifacts, not proof of the instant.

## 6. Limits / not attacked

- Only the two registry rows and the citations they feed were re-opened; extraction behaviour, the C1/C2
  counters, receipts, controls and the V3/V4/L3/L4 carrier surgery belong to other seats and were not run.
- AVM could change a page between this re-open and any later read; the 180d recheck is the registry's own
  answer to that. `info_en.txt` mtimes are 2024-11-18 and the images 2023-09-04, so drift risk is low but
  not zero.
- The licence notice was quoted, not interpreted: the two image bodies were downloaded only to be hashed
  and were deleted; no vendor bytes are in the lane or in these artifacts.
- No tool install or upgrade was needed (system `curl`, `python3`, `awk`, `sha256sum`); nothing was
  installed. No VCS mutation: only `git show`, `cat-file -e`, `rev-parse`, `diff` were used. Scratch
  removed.

## 7. Artifacts

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-41/w2/artifacts/R41W2SrcReopen/`
(digests in `SHA256SUMS` there):

| file | what |
|---|---|
| `check-reopen.py` | independent re-derivation of every row claim from the fetched bytes; exit 0 iff all pass |
| `check-reopen-output.txt` | its run: **89 PASS, 0 FAIL**, exit 0, including the carrier-pin checks |
| `commands.sh` | exact commands, scratch paths, the image hash-and-delete step |
| `row-shape.txt` | 11 cells / 12 pipes, base max id S126, duplicate scan, used-by existence, byte-identity with the wave-1 draft, quote word counts, S125 convention |
| `live-http-headers.txt` | response headers for all eight requests (statuses, Last-Modified, ETag, Content-Length) |
| `live-5490-fritz.os-listing.html`, `live-5491-fritz.os-listing.html` | the 574 B listings; digests equal the rows' `88c8d648…` and `badbb744…` |
| `vendor-image-digests.txt` | the two image sha256 + sizes proven equal to the `carriers.json` pins (bytes deleted) |
| `findings.md` | F1-F6 with exact quotes and line numbers |
