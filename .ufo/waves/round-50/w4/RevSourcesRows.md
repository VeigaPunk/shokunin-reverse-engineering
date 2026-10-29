# RevSourcesRows — wave 4 (falsify) re-open of SOURCES rows S243/S244/S245/S249

**Verdict: PASS — all four rows held under attack. No STOP finding.**
Every anchored element re-located byte-contiguously in freshly served bytes
(2026-10-29T21:28-21:31Z); every sha256/byte-size in the row anchors reproduces;
all four rows carry `status mined`, `opened 2026-10-28`,
`used-by corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, and the
knowledge entry cites all four back. The S243 Freetz-NG byte-identity side claim
also verifies (at the correct Freetz-NG repo path).

Seat dir: `.ufo/waves/round-50/w4/RevSourcesRows/` (receipts incl. served bodies).
No lane/fleet files touched; lane tree read-only. Scratch removed after receipts
copied. No tools installed this seat.

## Findings table

Fetch receipt: `receipts/fetch.tsv` (columns: id, t0, t1, curl_exit, http, size_download, body_bytes, body_sha256). All 8 fetches: curl exit 0, HTTP 200.

| Row | URL | cmd (fetch) | exit / http | bytes (row anchor) | sha256 served = anchor? | quote locate | row metadata |
|---|---|---|---|---|---|---|---|
| S243 | raw.githubusercontent.com/Freetz/freetz/master/.../101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch | `curl -sS -o s243.patch -w '%{http_code}\|%{size_download}' <url>` (21:28:32Z) | 0 / 200 | 1,153 = `1,153 B` | `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` = `e28b3341…4c707` ✓ | `:7` `+#define AVM_LE 2` ✓; `:17` condition names `SQUASHFS4_LE \|\| AVM_LE` ✓, `:18` `#define TARGET_FORMAT_BYTE_ORDER __LITTLE_ENDIAN` ✓ | mined / 2026-10-28 / used-by ✓ |
| S244 root | download.avm.de/fritzbox/ | same pattern (21:28:32Z) | 0 / 200 | 8,990 (lessons: root 8,990 B) ✓ | `75e886e2…0764` byte-identical to w3 same-day receipt ✓ | lists `fritzbox-7581/`, `fritzbox-7582/`, `fritzbox-6490-cable/`, `fritzbox-6430-cable/` ✓ | mined / 2026-10-28 / used-by ✓ |
| S244 7581 | download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/ | same (21:28:33Z) | 0 / 200 | 574 = `574 B` ✓ | `c1dd76d6…8589` ✓ | `FRITZ.Box_7581-07.18.image` `19-Aug-2024 12:33` `32010240` ✓ | — |
| S244 7582 | download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/ | same (21:28:33Z) | 0 / 200 | 574 = `574 B` ✓ | `18ccf345…d70d` ✓ | `FRITZ.Box_7582-07.18.image` `19-Aug-2024 12:36` `32256000` ✓ | — |
| S244 6490 | download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/ | same (21:28:34Z) | 0 / 200 | 604 = `604 B` ✓ | `4de20237…beb7` ✓ | `FRITZ.Box_6490_Cable-07.57.image` `04-Sep-2023 17:07` `39741440` ✓ | — |
| S244 6430 | download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/ | same (21:28:35Z) | 0 / 200 | 604 = `604 B` ✓ | `ab4da28c…aabf` ✓ | `FRITZ.Box_6430_Cable-07.30.image` `05-Sep-2023 09:10` `35911680` ✓ | — |
| S245 | raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | same (21:28:36Z) | 0 / 200 | 19,842 = `19,842 B` ✓ | `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` = `2d7b901b…599287` ✓ | `:53` `case Endian.LITTLE, _:` ✓, `:54` `commands_args.append("-le")` ✓, `:455` `NAME = "squashfs_v4_le"` ✓ (entry extras `:48` `is_avm = header.bytes_used == header.mkfs_time` ✓ inside `:40` `case Endian.BIG, 4:` ✓; LE pattern `68 73 71 73 [24] 04 00` at `:463` ✓) | mined / 2026-10-28 / used-by ✓ |
| S249 | download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt | same (21:28:36Z) | 0 / 200 | 67,591 = `67,591 B` ✓ | `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7` = `6c601b34…070a7` ✓ | `:850` "The licensee may create only one copy of the software, which may be used exclusively for backup use." — 18 words ≤ 25, contiguous in line 850 ✓ | mined / 2026-10-28 / used-by ✓ |

Quote check receipt: `receipts/quote-check-receipt.txt` — cmd `python3 -I -B quote-check.py`, exit 0, `QUOTE_CHECK located=18 missing=0`, stdout sha256 `dfc80456fc66b25bb906c8cab6121fa2778f178cacf812241b5623923dfb9a33`.
Metadata check receipt: `receipts/row-metadata.txt` — exit 0, all four rows `mined / 2026-10-28 / used-by corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`; knowledge entry lines 5-8 cite S243/S244/S245/S249.

## Side-claim verification (S243 Freetz-NG byte-identity)

Row anchor: "byte-identical at Freetz-NG `9a723692`". Verified: commit resolves to
`9a7236926bffaa6af16f84b3db27017cb5f02724` (2026-10-26, "juis: automatic update").
The blob lives at the Freetz-NG path `make/host-tools/squashfs4-be-host/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch`
(repo `Freetz-NG/freetz-ng`; note `squashfs4-be-host`, not Freetz's `squashfs4-host-be`).
`cmp` of the two 1,153 B blobs: **BYTE-IDENTICAL** (sha256 `e28b3341…4c707` both).
Receipt: `receipts/freetzng-byte-identity.txt` + `receipts/freetzng-101-at-9a723692.patch` + `receipts/freetzng-commit-9a723692.json`.

## Residual risk / gaps

- All eight served bodies are byte-identical to the w3 wave's same-day receipts
  (`.ufo/waves/round-50/w3/ScribeRowsSources/receipts/receipts.tsv`), i.e. the
  sources were stable across two independent fetches today. S243 tracks a moving
  branch (Freetz `master`); S244/S249 are live AVM listings. Both rows carry sane
  recheck gates (180d / 90d); content matched at both today's fetches.
- S244's anchor pins dates+sizes, not a body hash (the listing HTML is live);
  the row says so. All four (date,size) pairs reproduced exactly.
- Rows abbreviate sha256 as prefix…suffix; full digests reproduced above and in
  `receipts/SHA256SUMS`. No mismatch.
- Nothing re-run beyond my seat's remit: no REA, no counter reruns; offline fetches only.
