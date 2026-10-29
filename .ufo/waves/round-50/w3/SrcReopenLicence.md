# SrcReopenLicence — S249 AVM licence info_en.txt re-open (R50 attempt-2, wave 3, 2026-10-29)

## Verdict

**UNCHANGED — S249 re-open confirmed, anchor holds.** Fresh fetch of `https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt` on 2026-10-29T20:33Z returned HTTP 200, 67,591 B, sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7` — **byte-identical to attempt-1** (2026-10-28). The attempt-1 quote locates verbatim on **line 850** exactly as the attempt-2 plan and `land_c1.py` pin (`anchor :850`). Row cells re-affirmed: **kind docs, tier A, scope "AVM firmware licence restricts redistribution"**. The L1 can land the S249 row with this receipt; nothing in the source moved.

## Findings

| # | Check | Exact command (cwd = scratch) | Exit | Result |
|---|---|---|---|---|
| F1 | Fetch + status + size | `curl -sS -D headers-raw.txt -o info_en.txt -w '%{http_code} %{size_download} %{url_effective}' --max-time 60 https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt` | 0 | stdout `200 67591 https://…/info_en.txt` at 2026-10-29T20:33:15Z→20:33:16Z; headers: HTTP/1.1 200 OK, Server nginx, Last-Modified `Mon, 04 Sep 2023 17:07:50 GMT`, ETag `"64f60ee6-10807"`, Content-Length 67591, Accept-Ranges bytes; no Set-Cookie in response |
| F2 | Bytes + sha256 vs attempt-1 | `sha256sum info_en.txt`, `wc -c info_en.txt` (via Python hashlib/os.stat on the fetched file) | 0 | 67,591 B; sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7` = attempt-1 value in `w1/C1SrcAvmIndex.md` F12 and `l1/land_c1.py:86`. **Identical.** |
| F3 | Attempt-1 quote locates | Python line scan of the served bytes for `create only one copy of the software` + verbatim match of the full sentence on the numbered line | 0 | Sentence "The licensee may create only one copy of the software, which may be used exclusively for backup use." is on **line 850**, 18 words, contiguous in the served bytes; line 850 reads: `AVM grants the non-exclusive right to use this AVM firmware package, which is supplied exclusively in object code format. The licensee may create only one copy of the software, which may be used exclusively for backup use.` |
| F4 | Neighbouring clause (gate rows) | Same line scan for `Without previous approval in writing` | 0 | Intro of the forbidden list on **line 851**: "…Without previous approval in writing, and except for in cases permitted by law, it is particularly forbidden for this AVM firmware packet to be"; items on 852 (`- copied, propagated, or in any other manner made publicly accessible, or`) and **853** (`- processed, disassembled, reverse engineered, translated, decompiled or in any other manner "opened" and subsequently copied, propagated or made publicly accessible in any other manner.`) — line 853 is the reverse-engineering prohibition the planned S249 scope cell leans on |
| F5 | File shape | Python `data.split(b"\n")`, endswith check | 0 | CRLF line endings; 854 newline-terminated lines + final line 855 `HKR 2023-07-13.` with **no trailing newline**; 67,591 B includes the `\r` bytes |
| F6 | Server metadata self-consistency | ETag hex decode: `0x64f60ee6` = 1693847270 epoch; `0x10807` = 67591 | 0 | ETag decodes to 2023-09-04 17:07:50 UTC and to exactly the served length — self-consistent. **Discrepancy note:** the old round-42 record (S125 census receipt) says "Last-Modified 2023-09-04 17:08:03 GMT"; today's header and the ETag both say **17:07:50**. Bytes are identical, so this is a transcription slip in the old receipt, not a source change. No claim is affected. |
| F7 | Attempt-1 line-number reconciliation | Read of `l1/land_c1.py:86` (`:850`) vs `w1/C1SrcAvmIndex.md` F12 ("clause at line 851") | 0 | Both receipts are right about their own quotes: the **backup-copy sentence is line 850** (the plan's anchor), the **forbidden-list intro is line 851** (what F12 pointed at). No off-by-one in the plan; F12's wording was loose. Gate rows should cite :850 for the backup-copy quote and :851-853 for the prohibition context. |

## Row cells I would give S249

- **kind:** `docs`
- **tier:** `A` (publisher's own served text, fetched first-hand)
- **scope:** `AVM firmware licence restricts redistribution` — the licence wording that limits copying of the firmware package (one personal backup copy, line 850; copying/propagation and reverse-engineering prohibitions, lines 851-853); not a statement about SquashFS layout, extraction or any member
- **anchor:** `:850` (18-word quote, contiguous); supporting context `:851-853`
- This matches the plan's cells in `l1/land_sources.py:122-129` and the w3 dispatch brief verbatim; the fresh receipt is the only update needed (`verified-at 2026-10-29`).

## Artifacts (this seat dir)

- `SrcReopenLicence/info_en.txt` — served body, byte-exact (sha256 `6c601b34…070a7`; AVM licence text, not firmware bytes; saving it here is this seat's named deliverable)
- `SrcReopenLicence/headers.txt` — response headers, Set-Cookie stripped (none present anyway)
- `SrcReopenLicence/receipt.md` — exact command, exit code, stdout sha256, UTC times, quote location

## Not run / out of scope

- The 7530/7590/6430 directories' `info_en.txt` were **not re-fetched** — this seat's task names only the 6490 URL; attempt-1 F12 hashes for the other three remain the standing record.
- No REA runs, no fixture repos, no tool installs (none needed; curl/Python stdlib only). Disk-guard checked before fetch: `/fast/scratch/hyaku` 39% used, 497.2 G free.

## Scratch

`/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenLicence` removed after artifact copy (receipts above are the surviving record).
