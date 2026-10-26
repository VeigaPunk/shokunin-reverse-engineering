# id-collision table — kaidoku round 38 (registry vs shokuknow staged append)

Registry `corpus/SOURCES.md`: 111 rows, S001–S111 contiguous. Staged `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md`: 132 rows, S106–S237 contiguous.
Collision count: **6** (S106–S111). "Occupant" = the row that holds the number in the registry; "same document" = a registry row whose URL/note names the staged document.

| id | staged document | staged URL | registry occupant at that id | same document already in registry | final registry id |
|---|---|---|---|---|---|
| S106 | unblob upstream README | <https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md> | GNU binutils readelf version-needs reader | registry S110 notes "staged as package S106, renumbered by document" | `S110` |
| S107 | sasquatch upstream README | <https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md> | onekey-sec/sasquatch release sasquatch-v4.5.1-6 | identical URL at registry S111; registry S111 notes "staged as package S107, renumbered by document" | `S111` |
| S108 | Linux core(5) manual page | <https://man7.org/linux/man-pages/man5/core.5.html> | unblob SquashFS handler at tag 26.6.4 | none (distinct document) | `fresh id at append (S112+ in adoption order; never S108)` |
| S109 | Binwalk v3 upstream README | <https://raw.githubusercontent.com/ReFirmLabs/binwalk/HEAD/README.md> | neovim v0.12.6 release | none (distinct document) | `fresh id at append (S112+ in adoption order; never S109)` |
| S110 | dncil upstream README (Mandiant FLARE) | <https://raw.githubusercontent.com/mandiant/dncil/main/README.md> | unblob README at tag 26.6.4 | none (distinct document) | `fresh id at append (S112+ in adoption order; never S110)` |
| S111 | jadx upstream README | <https://raw.githubusercontent.com/skylot/jadx/HEAD/README.md> | devttys0 sasquatch README | none (distinct document) | `fresh id at append (S112+ in adoption order; never S111)` |
