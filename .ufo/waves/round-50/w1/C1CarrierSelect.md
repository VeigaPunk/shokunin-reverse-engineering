# R50 wave 1 — C1CarrierSelect (carrier chain pinning)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Seat dir:
`.ufo/waves/round-50/w1/C1CarrierSelect/` (deliverable `carriers-chain.json`,
instrument `tools/round-50/probe-carrier.py`, receipts `receipts/`). Scratch
`/fast/scratch/hyaku/kaidoku-r50/C1CarrierSelect` removed after receipt copy.
UTC run window: 2026-10-28.

## Verdict

**GREEN — recommend keeping the four planned carriers unchanged** (a7530, a7590,
c6490, c6430). All four chains pin and materialise through
`tools/round-41/fetch-vendor.py` (exit 0, four pins byte-verified); the three
backups materialise too (exit 0, live HTTP fetch through the tool itself). Every
carrier's member is a genuine AVM-marker LE SquashFS v4: `hsqs`, 4.0, xz
(compression id 4), `mkfs_time == bytes_used`, member longer than `bytes_used`.
Three distinct SoC lines across the four (IPQ40xx ARM / GRX350 / Puma 6 x86) —
the ≥2-families preference is met.

**Two pre-freeze corrections the L1 must fold into the plan and the counter
port** (details in "Defects & risks for the L1"):

1. **Cable member path.** `./var/tmp/filesystem.image` does not exist in any
   cable tar (c6490, c6430, and backup b6590). The LE member the plan's size
   column points at (28 MB / 23.9 MB) is
   **`./var/remote/var/tmp/x86/filesystem.image`**. `carriers-chain.json` pins
   that exact name; the plan table and `tools/round-50/carriers.json` must
   carry it per carrier (fetch-vendor uses `external.member` literally).
2. **BE sibling chunk in cable images.** Each cable tar also carries
   `./var/remote/var/tmp/filesystem.image` — a **`sqsh` big-endian** v4 xz
   AVM-marker filesystem (~5.4 MB). An REA `extract-firmware` run over the
   whole `.image` will surface both chunks; the predicate's "names the
   `squashfs_v4_le` handler for the carrier's chunk with no failed chunk"
   needs the oracle scoped to the x86-LE chunk and the BE sibling disposed by
   the frozen gap/removal rule (and a dev-arm check that the BE sibling does
   not count as a failed chunk — **not run here**, dev-arm decision).

## Chain pins (the deliverable)

`carriers-chain.json` uses the round-41 shape: top-level `carriers` (what
fetch-vendor materialises) plus `backups` in the same entry shape. Carrier
bytes = tar member carved to its superblock `bytes_used` (`external.length ==
bytes_used == mkfs_time`; superblock clause should read the **carve**, not the
padded member).

| id | image file | http | image sha256 | member | member B | member sha256 | bytes_used (=mkfs_time) | carrier pin (sha256 of carve) |
|---|---|---|---|---|---|---|---|---|
| a7530 | `FRITZ.Box_7530-08.25.image` | 200 | `b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c` | `./var/tmp/filesystem.image` | 34,005,000 | `df6c22ddd009870404375aff606853c9d5171580437b6aae193114d2040c6e56` | 34,003,969 | `e822655ac51cad32842e02e3eb31ff93d0b7e0d5620f88a9c86c07a7deda199e` |
| a7590 | `FRITZ.Box_7590-08.25.image` | 200 | `267ef427337d2141736ad6ed5d9389722a6a1234dd590bb7d4ebf11a00616c0d` | `./var/tmp/filesystem.image` | 35,835,912 | `05ba6ac992f77076cd72d97ed98ab7612f3cc6969f6bbf736515537a9373c3dc` | 35,834,769 | `c902f70beba12f7c0fb604fdfb89025f5c6988332482a7a2510911fd4436ba4f` |
| c6490 | `FRITZ.Box_6490_Cable-07.57.image` | 200 | `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d` | `./var/remote/var/tmp/x86/filesystem.image` | 28,200,968 | `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419` | 28,200,029 | `880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7` |
| c6430 | `FRITZ.Box_6430_Cable-07.30.image` | 200 | `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815` | `./var/remote/var/tmp/x86/filesystem.image` | 23,863,304 | `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c` | 23,861,507 | `da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f` |
| b7520 (backup) | `FRITZ.Box_7520-08.25.image` | 200 | `2929eb6e4a69739f0d86830f5ba2f8aef8637d64f256eded72ab2e1c793c818c` | `./var/tmp/filesystem.image` | 34,013,192 | `6e2f4a0b420378764ea5461fd83b1620caf54c3bc7eed3824a9a3a433f8629a2` | 34,009,089 | `107f83432575f884364028a71287003ec21a3652967966a3914f2fbf4207cde6` |
| b6590 (backup) | `FRITZ.Box_6590_Cable-07.57.image` | 200 | `0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae` | `./var/remote/var/tmp/x86/filesystem.image` | 27,750,408 | `57552a6dd81b6a43032b761bfbd10090442dbbcce88609bdb731af1242932786` | 27,748,075 | `09b48e2cdfe2db0eec2d225bdfcc21b4573d1c885ab7417fc5baac6adc72bcee` |
| b6850 (backup) | `FRITZ.Box_6850_5G-08.25.image` | 200 | `5e034fb396eeae5fc7e41896fd35ae524fa2dc207dea165d6d8e18812cf82773` | `./var/tmp/filesystem.image` | 32,526,344 | `3fc0825b533bbe7adb817cdc62230cd52473f325b50ecffab7a73fab327102c8` | 32,525,731 | `899854145eb9c497a25c7045db04f56513360bcd7daee96b9ff9937b528c013a` |

All superblocks: `hsqs`, `s_major.s_minor = 4.0`, compression id 4 (xz),
block_size 65,536, `avm_marker` (mkfs_time == bytes_used) **true**, member
length > bytes_used **true**. a7530's image sha256 equals the L1 scan pin
(`scan-output.txt`), independent confirmation.

Product/version: `./var/info.txt` is licence text only; the product/version
line lives in `./var/version`: `FIRMWAREVERSION=164.08.25` (a7530),
`154.08.25` (a7590), `141.07.57` (c6490), `159.07.30` (c6430), `175.08.25`
(b7520), `148.07.57` (b6590), `258.08.25` (b6850) — receipts/probes.

## Fetch-vendor exercises (the two RUNs)

Commands, from `S=/fast/scratch/hyaku/kaidoku-r50/C1CarrierSelect`:

1. Main spec (deliverable, four planned; image cache seeded from the curl
   downloads keyed by image sha256):
   `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/fetch-vendor.py --spec $SEAT/carriers-chain.json --cache $S/cache --image-cache $S/img --json-out $S/fetch-main.json`
   → **exit 0**; records: a7530/a7590/c6490/c6430 all `ok: true`, `fetch:
   cache`, `bytes` = bytes_used, pins as in the table; cache files re-hashed
   after the run — all four `pin_match True`.
2. Backups, live network through the tool itself (empty image cache):
   `python3 -I .../tools/round-41/fetch-vendor.py --spec $S/spec-backups.json --cache $S/cache-backups --image-cache $S/img-net --json-out $S/fetch-backups.json`
   → **exit 0**; b7520/b6590/b6850 all `ok: true`, `fetch: http 200`, pins
   re-hashed `pin_match True`.

Receipts: `receipts/fetch-main.json`, `receipts/fetch-backups.json`,
`receipts/spec-backups.json`.

## Download metadata (7 × HTTP 200; no cookies recorded)

| id | Content-Length | Last-Modified | ETag |
|---|---|---|---|
| a7530 | 41,850,880 | Wed, 22 Apr 2026 10:03:15 GMT | `"69e89ce3-27e9800"` |
| a7590 | 42,393,600 | Thu, 26 Mar 2026 13:44:31 GMT | `"69c5383f-286e000"` |
| c6490 | 39,741,440 | Mon, 04 Sep 2023 17:07:51 GMT | `"64f60ee7-25e6800"` |
| c6430 | 35,911,680 | Tue, 05 Sep 2023 09:10:35 GMT | `"64f6f08b-223f800"` |
| b7520 | 41,861,120 | Thu, 21 May 2026 10:13:45 GMT | `"6a0edad9-27ec000"` |
| b6590 | 39,290,880 | Mon, 04 Sep 2023 13:20:25 GMT | `"64f5d999-2578800"` |
| b6850 | 188,272,640 | Thu, 09 Jul 2026 11:02:29 GMT | `"6a4f7fc5-b38d000"` |

## Which images are latest / likely replaced

Every model directory publishes exactly one `.image` (in-place replacement), so
each download is the latest of its model. The four 08.25-line images (7530,
7590, 7520, 6850) are the current generation and **will be replaced** when AVM
ships the next line (7530 replaced as recently as Apr 2026). The three cable
07.x images are EOL/final (mtimes Sep 2023) — effectively immutable. The pins +
`--carrier-cache` mechanism covers a replaced image exactly as the plan's
disclosed limit (2) states.

## Recommendation & backup ranking

- Keep the four planned. SoC spread: a7530 (IPQ40xx ARM line), a7590 (GRX350
  line), c6490 + c6430 (Puma 6 x86 cable, two firmware lines) — three families.
- Backup order: **b7520** first (like-for-like ARM swap for a7530, 08.25 line);
  **b6850** second (ARM/5G variant; 188 MB image — download cost only);
  **b6590** last (its x86 kernel sha256 `bd922b7d…7164` is **identical** to
  c6490's, so it adds no SoC diversity and duplicates the BE-sibling risk).

## Defects & risks for the L1 (fold before the freeze)

1. **Plan table member column** — for c6490/c6430 the frozen
   `tools/round-50/carriers.json` must pin
   `./var/remote/var/tmp/x86/filesystem.image`; `./var/tmp/filesystem.image`
   is absent from cable tars (probe exits 2 for that member: observed during
   the first probe pass; receipts/probes hold the corrected runs).
2. **BE sibling chunk** — c6490/c6430 tars also carry
   `./var/remote/var/tmp/filesystem.image` = `sqsh` BE 4.0 xz, marker true
   (member sha256 `334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4`
   / `7d3677e679ad5d07d9d49b4c1567f7f2f82dac28795b946875a62eeb949c9251`).
   Scope the oracle to the LE chunk's extract root; route the BE sibling
   through the round-41 `gaps_ok` disposition; verify at the dev arm that REA
   does not count it as a failed chunk (sasquatch-v4be exists on PATH, but the
   receipt behaviour is **not verified here**).
3. **Pin convention** — carrier bytes are the carve to `bytes_used`; the
   counter's superblock clause must read the carved carrier (`length ==
   bytes_used`), matching `external.length` semantics of fetch-vendor.
4. **info.txt vs var/version** — any doc binding quoting product/version
   should quote `./var/version` (`FIRMWAREVERSION=…`), not `./var/info.txt`
   (licence text).
5. **SoC evidence honesty** — `kernel.image` blobs carry no readable banner or
   arch strings in any of the seven (08.x kernels opaque; c6490/b6590/c6430
   arch evidence is the `x86/` member path itself). Header word@0x24 is not a
   zImage magic anywhere (a7530/b7520/b6850 share `00008039`; a7590
   `c09288c8`). SoC attribution (IPQ4018 / GRX350 / Puma 6) rests on the
   plan's table, not on in-image proof — record as such in the entry.

## Commands & exit codes (summary)

- Listing probe: `curl -sS -o listings/<model>.html https://download.avm.de/fritzbox/<model>/fritz.os/` × 7 → all `200`.
- Downloads: `curl -sS --fail -o img-dl/<file> -D headers/<id>.hdr <url>` × 7 → all `200`, sha256 as tabled.
- Probe: `python3 -I tools/round-50/probe-carrier.py --image <img> [--member <m>] --out probes/<id>.json --file-cmd` × 10 (7 carriers + 3 cable `-remote` siblings) → all rc=0.
- fetch-vendor main + backups runs → rc=0 (records above).
- Cache re-hash verification → all pins verified True.

## Tooling authorization record

No tools installed or upgraded (curl, tar, python3, file, sha256sum already
present; versions unaffected). No pacman transaction; no host service touched.
No vendor firmware bytes copied into the lane tree — receipts are hashes,
listings, header metadata (Set-Cookie lines stripped defensively) and JSON
records only.
