# Gate id remap — E3's draft ids vs the landed rows (closure must use the right column)

Measured 2026-10-26 from `corpus/SOURCES.md` at `0b15c8b2` (read-only) and
`.ufo/waves/round-40/w1/artifacts/R40AssimE3/{gate.md,collision/renumber-map.tsv}`.

| id | E3 `gate.md` / `renumber-map.tsv` says | `corpus/SOURCES.md` says at the tip | agreement |
|---|---|---|---|
| S123 | round-11 `lead1-avm-image.tsv` (own-work) | rea-agents 6.5.0 `operation`/provider row, added in the freeze `7fce3086` (author `w1/R40SrcReaOps.md`) | **collision of meaning** |
| S124 | `round11/work/freetz-squashfs4-host-be.mk` (own-work, tarball md5) | Freetz-NG `350-unsquashfs__AVM_BE.patch` (code, commit-pinned) — the row `w1/R40SrcFreetz.md` drafted as "S123" | **different document** |
| S125 | `AVM-BE-format.txt` lines 5/8-9/13-14 (docs) | AVM 6490 Cable FRITZ!OS 07.57 download directory (dataset) — the row `w1/R40SrcAvmVendor.md` drafted as "S123" | **different document** |
| S126 | — (E3 never wrote it) | the round-11 `lead1-avm-image.tsv` (own-work) = E3's proposed S123 | only id that moved to a fresh number |

Two rows E3 drafted were **not** landed: the `freetz-squashfs4-host-be.mk` own-work row and the
second `AVM-BE-format.txt` row. The entry cites neither; `S114` (kept, unchanged) is cited instead
for the block-length sentence, which its recorded anchor/scope does not carry.

Consequence: pasting E3's "New-row Gate records" table into `corpus/lessons/round-40.md` would pair
three ids with three documents that are not those rows. Use this remap.

Gate-ready quotes per landed row (each already in a wave-1 report or row anchor):

| landed id | source | opened | located quote (≤25 words) | where recorded |
|---|---|---|---|---|
| S124 | `https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a723692…/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch` | 2026-10-26T18:25Z, HTTP 200, 2217 B | "/* block length in AVM-BE format is stored in LE order */" — patch line 35 | `corpus/SOURCES.md` S124 anchor (landed) |
| S125 | `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` | 2026-10-26T18:18Z, HTTP 200 | "Product: FRITZ!Box 6490 Cable … Version: FRITZ!OS 7.57 … Release date: 04.09.2023" — `info_en.txt` lines 8-14 | `w1/R40SrcAvmVendor.md` "Located quotes" |
| S126 | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv` (sha256 `f205807d…9eb0`) | 2026-10-26 | "absent - the AVM branch passes no -be" — TSV row `unblob_be_flag` (9 words) | `w1/artifacts/R40AssimE3/gate.md` |
