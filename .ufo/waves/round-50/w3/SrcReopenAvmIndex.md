# SrcReopenAvmIndex — R50 attempt-2 w3 — S244 source re-open (AVM download index)

Seat: SrcReopenAvmIndex (leaf scout, no subagents). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
All writes confined to this report + `.ufo/waves/round-50/w3/SrcReopenAvmIndex/` + scratch `/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex` (removed after receipt copy). No REA invoked. No image bodies downloaded.

## Verdict

**PASS — zero drift; chain fetchable.** All four frozen `http_last_modified` + `http_etag` pins from `tools/round-50/carriers.json` match the live HTTP HEAD responses byte-for-byte (UTC 2026-10-29T20:35:17–20Z, curl 8.23.0). All five index bodies fetched HTTP 200 with complete listings; every pinned image row is present with date and size in three-way agreement (listing size = HEAD Content-Length = ETag size-hex). Attempt-1's located quote `FRITZ.Box_7581-07.18.image 19-Aug-2024 12:33 32010240` is intact. Source side is clean for the L1 data run.

## Findings

### 1. Index fetches (5 bodies, UTC 2026-10-29, redirects=0, final URL == request URL)

| name | URL | ts (UTC) | status | bytes | sha256 |
|---|---|---|---|---|---|
| base | https://download.avm.de/fritzbox/ | 20:35:17Z | 200 | 8990 | `75e886e28f104038649196da4f5509cab8536c5046479184c835e7f06fc40764` |
| fritzbox-7581 | …/fritzbox-7581/other/fritz.os/ | 20:35:18Z | 200 | 574 | `c1dd76d62a6a2ac9964a9844be8d69c6dc902cb00ef16bcb04a2a39176248589` |
| fritzbox-7582 | …/fritzbox-7582/other/fritz.os/ | 20:35:19Z | 200 | 574 | `18ccf34526bb95f675679820e3ace0ddd9c56b6b5e6d76472c364d101453d70d` |
| fritzbox-6490-cable | …/fritzbox-6490-cable/deutschland/fritz.os/ | 20:35:20Z | 200 | 604 | `4de2023728137eefc887853dded6b354e9c602929b35450576baa21533b2beb7` |
| fritzbox-6430-cable | …/fritzbox-6430-cable/deutschland/fritz.os/ | 20:35:21Z | 200 | 604 | `ab4da28c400a7b8493e6bae56f68f1aa98fb104e64865336380e31aa7dfeaabf` |

curl rc=0 for all five; bodies archived under `SrcReopenAvmIndex/idx/` (body + response headers + curl -w receipt each).

### 2. Carrier HEAD pins vs carriers.json frozen pins — 4/4 MATCH

| carrier | Last-Modified (live) | pin | ETag (live) | pin | Content-Length | verdict |
|---|---|---|---|---|---|---|
| g7581 | Mon, 19 Aug 2024 12:33:29 GMT | = | `"66c33b99-1e87000"` | = | 32010240 | MATCH |
| g7582 | Mon, 19 Aug 2024 12:36:33 GMT | = | `"66c33c51-1ec3000"` | = | 32256000 | MATCH |
| c6490 | Mon, 04 Sep 2023 17:07:51 GMT | = | `"64f60ee7-25e6800"` | = | 39741440 | MATCH |
| c6430 | Tue, 05 Sep 2023 09:10:35 GMT | = | `"64f6f08b-223f800"` | = | 35911680 | MATCH |

All HEADs: rc=0, HTTP 200, Content-Type application/octet-stream, Accept-Ranges bytes (range fetch possible). Headers archived under `SrcReopenAvmIndex/head/`.

### 3. Pinned listing rows (tag-stripped from the fetched index bodies)

| model dir | row (name / date / size) |
|---|---|
| fritzbox-7581/other/fritz.os/ | `FRITZ.Box_7581-07.18.image` / 19-Aug-2024 12:33 / 32010240 |
| fritzbox-7582/other/fritz.os/ | `FRITZ.Box_7582-07.18.image` / 19-Aug-2024 12:36 / 32256000 |
| fritzbox-6490-cable/deutschland/fritz.os/ | `FRITZ.Box_6490_Cable-07.57.image` / 04-Sep-2023 17:07 / 39741440 |
| fritzbox-6430-cable/deutschland/fritz.os/ | `FRITZ.Box_6430_Cable-07.30.image` / 05-Sep-2023 09:10 / 35911680 |

Base index also still lists all four model dirs: `fritzbox-7581/` 11-Oct-2017 09:06, `fritzbox-7582/` 12-Nov-2018 15:13, `fritzbox-6490-cable/` 23-Sep-2020 10:06, `fritzbox-6430-cable/` 22-Nov-2017 15:18.

### 4. Attempt-1 located quote — CONFIRMED

7581 listing row `FRITZ.Box_7581-07.18.image` with `19-Aug-2024 12:33` and `32010240` all present (script assertion `QUOTE_CONFIRMED`, verify.out).

### 5. Crosschecks

- ETag size-hex → decimal equals Content-Length equals listing size for all four: 0x1e87000=32010240, 0x1ec3000=32256000, 0x25e6800=39741440, 0x223f800=35911680.
- Listing mtimes agree with HEAD Last-Modified to the displayed minute (12:33↔12:33:29, 12:36↔12:36:33, 17:07↔17:07:51, 09:10↔09:10:35).

### 6. Observations / residual risk for the L1

- Each model's `fritz.os/` dir currently lists ONLY the pinned version (+ info_de.txt/info_en.txt): AVM prunes superseded images from these paths, and no newer entry exists for any of the four models today. The pinned files are the live heads of their URLs — no urgency signal for the quiet-window run.
- HEAD/metadata cannot verify the frozen `image_sha256` values (body downloads out of scope). Residual risk: a same-second server-side rebuild keeping mtime+size would evade pins; the L1's post-download sha256 gate stays the definitive check.
- Cosmetic: header casing differs (lower-case header names for g7581/g7582/c6490 responses, canonical for c6430).
- No `Set-Cookie`/`Cookie` headers in any archived response header (grep-checked before archiving; receipts contain no secrets).

## Exact commands and exit codes

| step | command | exit |
|---|---|---|
| dirs | `rm -rf "$S"; mkdir -p "$S/idx" "$S/head" "$A"` (S=/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex, A=<lane>/.ufo/waves/round-50/w3/SrcReopenAvmIndex) | 0 |
| guard | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → /fast/scratch/hyaku 39% used, 497.4 GiB free (status table printed; wrapper hit its 30 s cap during the top-consumers phase — status data itself was produced) | 0 (timed out after table) |
| indexes | `bash /fast/…/w3-SrcReopenAvmIndex/fetch-indexes.sh` (5× `curl -sS --max-time 30 -A kaidoku-r50-S244-reopen/1.0 -H 'Accept-Encoding: identity' -o body -D hdr -w '…' URL`; UA fallback to a browser UA only on 403/406/error — never triggered) | 0 |
| heads | `bash /fast/…/w3-SrcReopenAvmIndex/head-images.sh` (4× `curl -sSI --max-time 25 -A kaidoku-r50-S244-reopen/1.0 -D hdr -o /dev/null URL`; ranged-GET fallback never triggered) | 0 |
| verify | `bash /fast/…/w3-SrcReopenAvmIndex/verify.sh` (pin compare, hex crosscheck, quote assertion, row/base-row extraction, listing-vs-CL equality) | 0 |
| archive | cp scripts+bodies+headers into seat dir with Set-Cookie strip; `verify.sh > verify.out`; sha256 manifest | 0 |
| cleanup | `rm -rf /fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex` (after receipt copy) | run at yield |

Scripts (fetch-indexes.sh, head-images.sh, verify.sh) and all raw receipts are archived in `SrcReopenAvmIndex/`; `MANIFEST.sha256` covers 32 files.

## Tooling / host notes

- No tool installs or upgrades were needed (curl 8.23.0 already present). Operator tooling authorization: unused; no pacman touched.
- No git commands run; nothing written outside the two seat paths + scratch.
- Not run (out of scope for this seat): image body sha256 verification, any REA invocation, C1/C3 controls.
