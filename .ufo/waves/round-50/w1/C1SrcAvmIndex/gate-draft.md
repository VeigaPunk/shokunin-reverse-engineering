# Draft `## Gate` text for the round-50 lesson (C1SrcAvmIndex; NOT applied; L1 applies)

## Gate

Sources opened this round (2026-10-28, UTC; each located quote is from the served body after tag removal and whitespace collapse; the receipts are under `.ufo/waves/round-50/w1/C1SrcAvmIndex/receipts/`; the licence texts are recorded by sha256 and are not copied into the lane tree).

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S151 | https://download.avm.de/fritzbox/fritzbox-7530/deutschland/fritz.os/ (index; `receipts/index-fritzbox-7530_deutschland_fritz.os.html`) | 2026-10-28T23:32:31Z, HTTP 200, 586 B, sha256 b178e7b060379f65ab29a85f2ac562969abb5ea5bb0b69db0419ddfa5f6825d9 | listing row `FRITZ.Box_7530-08.25.image` `22-Apr-2026 10:03` `41850880` (the whole image file) | **admit** (tier A, `mined`), scoped to which firmware images AVM publishes and their sizes; the 7590, 6490-cable and 6430-cable directory listings are the same discipline (receipts) |
| S152 (L1 decision) | https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt (sha256 6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7) | 2026-10-28T23:32:52Z, HTTP 200, 67591 B | "Without previous approval in writing, and except for in cases permitted by law, it is particularly forbidden for this AVM firmware packet to be" (24 words; line 851) | **admit if cited** (tier A, `mined`): the licence wording that makes the four carriers chain-pinned and never committed. The 7530 text differs: line 1680 "Licensee shall be entitled to make a copy exclusively reserved for personal backup purposes (backup copy)." (16 words); both are listed in the row |
| S152 (image-internal) | `./var/info.txt` inside https://download.avm.de/fritzbox/fritzbox-7530/deutschland/fritz.os/FRITZ.Box_7530-08.25.image (member at data offset 2048, 2807 B, sha256 b0360d8820be53c70365dc0adfc19a665efb19dc510dd75126466f82ae07e39b; identical in the 7590 and 6490 images) | 2026-10-28T23:35:56Z, HTTP 206 (Range) | "shall not be copied, distributed or otherwise made publicly available" (11 words; English list in the member) | corroborates the publisher text; the member is not copied into the lane tree |

- **Round-40 agreement, verified.** `./var/content` of the 6490 image (346 B, sha256 ab238b0ed62419a4f3f32454e81bb14ef4bbce7ce462f7631f9555a38eca9557) and `./var/info.txt` (sha256 b0360d88…) equal the round-40 receipt `.ufo/waves/round-40/w1/R40SrcAvmVendor.md`.
- **Same bytes at two 6490 paths: an inference.** The 6490 image at `deutschland/` hashes to `f518ce6b…`, the value the round-40 receipt pins for the `other/` path (S125). The `other/` bytes were not re-fetched this round, so "the same bytes" is an [INFERENCE] from the matching pin.
- **Plan defect D1 (must fix before the freeze).** The round-50 carrier table names `./var/tmp/filesystem.image` for c6490 and c6430. For those two images that member is absent at the top level; the LE AVM-marker member is `./var/remote/var/tmp/x86/filesystem.image` (28200968 B and 23863304 B).
- **Plan defect D2 (labelling).** The sizes in the table are tar-member sizes, not image-file sizes (listed image files 41850880, 42393600, 39741440 and 35911680 B).
- **Not a registry change in this round.** The row is a draft; the L1 applies it after the freeze decision and assigns S151 (and S152 if the licence is cited).
- **Assimilation: none in this seat.** No merge/kaidoku staging was read; the seat touched only the AVM public bytes listed above.
