# C1SrcAvmIndex — round 50 wave 1: AVM source re-open and carrier provenance

**Verdict: DONE, with two plan defects to fold in before the freeze.** D1 (must fix): the plan's carrier table names `./var/tmp/filesystem.image` for all four carriers, but for the two cable carriers (c6490, c6430) that path is absent at the top level; their LE AVM-marker member is `./var/remote/var/tmp/x86/filesystem.image`. D2 (labelling): the plan's sizes are tar-member sizes, not the image files AVM lists. Everything else in the plan's provenance re-derives: the 7530 image hash matches the plan, all four LE members are `hsqs` v4.0 compression 4 with `mkfs_time == bytes_used`, and the publisher and image licence text forbid redistribution. Nothing was committed, staged or run against data. The draft S151 row and `## Gate` text are in the seat dir for the L1 to apply.

Timestamps are UTC from `date -u` and the HTTP `date` header. Every request returned HTTP 200 or 206 except the one 404 in F9.

## Defects for the L1

- **D1 (wrong carrier member path, c6490 and c6430; must fix).** The plan's table and chain say `tar member ./var/tmp/filesystem.image` for every carrier. Measured: in the 6490 and 6430 images that path does not exist at the top level. The LE `hsqs` member is `./var/remote/var/tmp/x86/filesystem.image`; the BE `sqsh` rootfs is `./var/remote/var/tmp/filesystem.image`. As written, the chain fails the dev arm for a reason the claim owns, and the plan's own recovery clause would turn a plan error into a recorded negative. Corrected pins: `tools/round-50/carriers-draft.json`.
- **D2 (sizes mislabelled).** The plan's "34 MB / 35.8 MB / 28 MB / 23.9 MB" are the tar member sizes (34,005,000; 35,835,912; 28,200,968; 23,863,304 B). The image files AVM lists are 41,850,880; 42,393,600; 39,741,440; 35,911,680 B. Label the members as members.

## Findings table

Commands are abridged to the operative call. Receipts are under `receipts/` with `SHA256SUMS`.

| # | Finding | Command (abridged) | Exit | Evidence | Status |
|---|---|---|---|---|---|
| F1 | AVM download index for the root and the four model `fritz.os/` directories | `curl -sS -D hdr -o body -w` on `https://download.avm.de/fritzbox/` and the four `deutschland/fritz.os/` directories | 0 each | root 8990 B sha256 `75e886e28f104038649196da4f5509cab8536c5046479184c835e7f06fc40764` (23:32:30Z, 200, 70 `fritzbox-*` entries incl. the four); 7530 586 B sha256 `b178e7b060379f65ab29a85f2ac562969abb5ea5bb0b69db0419ddfa5f6825d9` (23:32:31Z, 200); 7590 832 B sha256 `f87556d41a5ee659817a6a4e739dd522fc117b908cc9eb0644386a6badf94221` (23:32:32Z, 200); 6490-cable 604 B sha256 `4de2023728137eefc887853dded6b354e9c602929b35450576baa21533b2beb7` (23:32:33Z, 200); 6430-cable 604 B sha256 `ab4da28c400a7b8493e6bae56f68f1aa98fb104e64865336380e31aa7dfeaabf` (23:32:34Z, 200) | confirmed |
| F2 | Listing rows (names, sizes, dates) of the four directories | read of `receipts/index-*.html` | 0 | `FRITZ.Box_7530-08.25.image` 22-Apr-2026 10:03 41850880 B; `FRITZ.Box_7590-08.25.image` 26-Mar-2026 13:44 42393600 B; `FRITZ.Box_6490_Cable-07.57.image` 04-Sep-2023 17:07 39741440 B; `FRITZ.Box_6430_Cable-07.30.image` 05-Sep-2023 09:10 35911680 B | confirmed; D2 |
| F3 | Image HEAD (no body) for the four carriers | `curl -sS -I` | 0 | Content-Length and Last-Modified equal the listing rows (F2); 6490 ETag `64f60ee7-25e6800` (hex size = 39741440) | confirmed |
| F4 | Full image bytes of the four carriers, hashed in scratch (then deleted) | `curl -sS -D hdr -o image`; `sha256sum` | 0 each | a7530 `b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c` (41850880 B; equals the plan's pin); a7590 `267ef427337d2141736ad6ed5d9389722a6a1234dd590bb7d4ebf11a00616c0d` (42393600 B); c6490 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d` (39741440 B); c6430 `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815` (35911680 B). Bytes not copied (`receipts/vendor-image-sha256.txt`) | confirmed (7530 matches the plan; the other three are new pins) |
| F5 | Tar members and LE superblocks of each carrier | `tarfile` member walk; `struct` read of the 96-byte superblock (`hsqs` = LE, `sqsh` = BE) | 0 | a7530 `./var/tmp/filesystem.image` 34005000 B, sha256 `df6c22ddd009870404375aff606853c9d5171580437b6aae193114d2040c6e56`, LE v4.0 comp 4, mkfs 34003969 = bytes_used; a7590 `./var/tmp/filesystem.image` 35835912 B, sha256 `05ba6ac992f77076cd72d97ed98ab7612f3cc6969f6bbf736515537a9373c3dc`, LE v4.0 comp 4, mkfs 35834769 = bytes_used; c6490 `./var/remote/var/tmp/x86/filesystem.image` 28200968 B, sha256 `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419`, LE v4.0 comp 4, mkfs 28200029 = bytes_used; c6430 `./var/remote/var/tmp/x86/filesystem.image` 23863304 B, sha256 `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c`, LE v4.0 comp 4, mkfs 23861507 = bytes_used | confirmed for the LE layout; D1 for c6490 and c6430 |
| F6 | Range walk of the same tar headers, without a full download | `python3 -I -B tools/round-50/avm-member-walk.py <four paths>` (seat tool, stdlib only) | 0 | six superblock members compared against the earlier walk: 0 mismatches; output `receipts/walk-seat-tool.json` sha256 `0fff29eb466425507e50fb78626ca1839f5c1434d9e346549c6f355b4bc30821` (fields differ from the earlier run only by the UTC stamp) | confirmed; the instrument reproduces |
| F7 | The four LE members: `hsqs`, v4.0, compression 4, `mkfs_time == bytes_used` | from F5 | 0 | 4 of 4 | confirmed (the plan's marker clause) |
| F8 | The BE rootfs in the same cable images also satisfies the marker, so the marker alone does not select LE | walk of c6490 and c6430 `./var/remote/var/tmp/filesystem.image` | 0 | 6490 BE 5443592 B, sha256 `334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4`, mkfs 5442392 = bytes_used; 6430 BE 5984264 B, sha256 `7d3677e679ad5d07d9d49b4c1567f7f2f82dac28795b946875a62eeb949c9251`, mkfs 5981012 = bytes_used | confirmed; the endian and layout clause separates LE from BE, not the marker. CTL-C1-1 (BE receipts) is red only through the layout clause, which the plan already names |
| F9 | `other/` path for the carriers (HEAD only; not downloaded) | `curl -sS -I` on `…/fritzbox-6490-cable/other/…` and `…/fritzbox-6430-cable/other/…` | 0 (6490); 0 with HTTP 404 (6430) | 6490 `other/` 200, Content-Length 39741440, ETag `64f60ef3-25e6800` (differs from the deutschland ETag `64f60ee7-25e6800`); 6430 `other/` 404 (146 B) | confirmed: the 6490 `other/` bytes were not re-fetched; only the deutschland 6430 path exists |
| F10 | The 6490 deutschland image matches the round-40 pin for `other/` | `sha256sum` of the deutschland image (F4) vs `corpus/evidence/round-40/c1/V1/provenance.json` `chain.image_sha256` (pinned for the `other/` URL) | 0 | both `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`; the round-40 `member_sha256` `334e56df…` equals F8's BE member. [INFERENCE] the two paths serve the same bytes, from the matching pin; the `other/` bytes were not re-fetched | confirmed for the deutschland bytes; the `other/` equality is an inference |
| F11 | Image-internal licence notice (`./var/info.txt`) identical across three images | Range read at member data offset (7530 @2048; 7590 @2048; 6490 @39404544), 2807 B | 0 | sha256 `b0360d8820be53c70365dc0adfc19a665efb19dc510dd75126466f82ae07e39b` in all three (= round-40 receipt) | confirmed |
| F12 | Publisher licence text per directory (`info_en.txt`) | `curl -sS -D hdr -o info_en.txt` on each of the four; then a case-insensitive search for licence, copy, distribute and reverse-engineer wording | 0 | 6490 sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`, clause at line 851; 6430 sha256 `3a1fd9b52bb20b559a2115da8a528e49cfcdb1a566886d6b54d2abf0c7a75932`, line 341; 7530 sha256 `19148a074910d9709cabe0855e706ed0d8d0cd1bcaa46f4bdeaa1d5cc1b08be4`, line 1680; 7590 sha256 `e21206aae2999cfe0c84088d588fd5beeac72b7d71ef8168da0a4ac31b40ca98`, licence clause near line 1825 (bodies not copied) | confirmed |
| F13 | Root `license.txt` (German text) | `curl -sS -D hdr -o license.txt https://download.avm.de/fritzbox/license.txt` | 0 | 91057 B, 23:33:00Z, sha256 `12b824ca32c74c41902c31f5870a6660992af6904ff21b55e0ae7f1c9bedda63` (body not copied) | confirmed; not used for a quote |
| F14 | Product identity per image (`./var/content`, Range read) | `Range` read at offset 1024 (7530, 7590, 6490) and 4608 (6430) | 0 | 7530 HW236, 08.25, Build 131719 (sha256 `796e20680559ce4230a990fd3425571647d47cae369473f8339254905a2d342d`); 7590 HW226, 08.25, Build 130856 (`eac29b6ee9c976d3df78a489c87552a7de65cf98a1293877c1254f64ea040160`); 6490 HW213a, 07.57, Build 107830 (`ab238b0ed62419a4f3f32454e81bb14ef4bbce7ce462f7631f9555a38eca9557` = round-40 pin); 6430 HW231a, 07.30, Build 107861 (`e150c62a8de2dd9cfb69796f99f29a26119e33bc4414eee0ae11a1ccd3596fed`) | confirmed |
| F15 | The round-40 table with a 27,750,408 B member does not describe V1 | `grep -rl '27 750 408' .ufo/waves/round-40` | 0 | the only hit is `.ufo/waves/round-40/w1/R40C1ReconWrap.md`, which has the image at 39 290 880 B (sha256 `0c539499…`) and a separate `dev6590` probe; V1 is 39 741 440 B. The wrap file's own table is for that other image | resolved: not a V1 inconsistency; I did not trace the origin of the 39 290 880 B image beyond that file |
| F16 | Round-41 member pins | `grep -rhoE './var/[^ ]*filesystem.image' tools/round-41 .ufo/waves/round-41` | 0 | 134 hits for `./var/tmp/filesystem.image` and 1 for `./var/remote/var/tmp/filesystem.image`; the round-41 carrier chain file is not under `tools/round-41/` | not determined: which round-41 BE carrier used which member is not traced; CTL-C1-1 copies those receipts verbatim, so the L1 should record the member path in the control README before freezing |
| F17 | Registry: S151 free; no AVM row for these deutschland directories | `grep -c '^| S151 ' corpus/SOURCES.md`; `grep -n` for the `fritzbox-7530` and `fritzbox-7590` download paths | 1 (count 0; no match) | last rows S148 and S149; the only AVM directory row for these models is S125 at `fritzbox-6490-cable/other/fritz.os/` (a different path from the carrier pins) | S151 free; S125 must not be cited for the deutschland bytes |
| F18 | Round-40 V1 receipt values | `grep -c ab238b0ed…` in `.ufo/waves/round-40/w1/R40SrcAvmVendor.md` | 0 | 1 hit | confirmed |

## Draft artifacts (not applied; the L1 applies after review)

- `row-S151.md`: the S151 row (dataset, tier A, scope limited to the listing), plus an optional S152 licence row, which the L1 adopts only if the entry cites the licence.
- `gate-draft.md`: the `## Gate` table text: S151 admit; S152 admit-if-cited; located quotes (≤25 words); the D1 and D2 defects recorded in the gate.
- `tools/round-50/carriers-draft.json`: corrected carrier pins (image sha256, member path and member sha256, superblock fields, product line), with the `other/` and BE-sibling notes.
- `tools/round-50/avm-member-walk.py`: stdlib draft walker over HTTP Range reads (F6).

### Located quotes (≤25 words; checked against the bodies)

- 6490 `info_en.txt` line 851: "Without previous approval in writing, and except for in cases permitted by law, it is particularly forbidden for this AVM firmware packet to be" (24 words).
- 7530 `info_en.txt` line 1680: "Licensee shall be entitled to make a copy exclusively reserved for personal backup purposes (backup copy)." (16 words).
- Image `./var/info.txt` (sha256 `b0360d88…`, English list): "shall not be copied, distributed or otherwise made publicly available" (11 words).

## Calibration and limits (not run or not claimed)

- Not run: REA `extract-firmware`, unblob, `sasquatch`, `unsquashfs`, the oracle, and any counter. Those belong to the carrier-select and dev-arm seats; this seat measured identity and layout only.
- The four full images were downloaded only to scratch, hashed and read, then deleted. No vendor bytes are in the lane tree.
- The 6490 `other/` bytes were not re-fetched; the equality with `deutschland/` is an inference from the matching round-40 pin (F10).
- The round-41 `./var/tmp/filesystem.image` pins (F16) are not traced to a specific carrier; check before freezing CTL-C1-1.
- The 7530 `ARM (IPQ4018) LE` architecture note in the plan was not checked; only the superblock endianness was measured.
- The S151 and S152 rows and the `## Gate` text are drafts; the registry was not edited.

## Tools and installs

- No tool installed, upgraded or removed. Used: `curl`, `sha256sum`, Python 3 standard library (`tarfile`, `struct`, `urllib`), `grep`, `sed`, `awk`. Channel: system. Reason: fetch, hash and read only.
- `scripts/hyaku/disk-guard.sh status` exit 0 at 23:32Z before the downloads.

## Receipts and paths

- Seat dir: `.ufo/waves/round-50/w1/C1SrcAvmIndex/` (`receipts/` with `SHA256SUMS` listing every receipt file; `tools/round-50/`; `row-S151.md`; `gate-draft.md`).
- Secret scan of `receipts/` for `Set-Cookie`, `Authorization` and `session=`: no matches (exit 1). `Set-Cookie` lines were stripped from every saved header.
- Scratch `/fast/scratch/hyaku/kaidoku-r50/C1SrcAvmIndex` removed after the receipts were copied.
- No commit, push, stage or stash. No write to the lane's `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, or the fleet repo.
