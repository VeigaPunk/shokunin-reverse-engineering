# Draft registry edit for S138 / S139 (`corpus/SOURCES.md`; NOT applied to the lane)

Only the `used-by` cell of each row changes. `status` (`mined`), `opened` (`2026-10-28`, equal to the counter's `OPENED`), `recheck` and every other cell stay byte-identical.

| row | cell | old | new |
|---|---|---|---|
| S138 | used-by (column 11 of 11) | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |
| S139 | used-by (column 11 of 11) | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |

Separator is `, ` (the census splits on `[,;]`; existing multi-path cells such as S001 use the same form).

Landing constraint: this edit must land in the same commit as `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`. Landed alone, the census's mined-path check prints `missing: corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` twice (`census-run.txt`, V1).

Full edited rows: `registry-rows-S138-S139.edited.md` (sha256 `1b5eac5d42775856a13d035019ff868b5a505815c57076fd77285a342198fbf4`). Diff: `registry-S138-S139.diff`.

Open decision for L1 (not applied): the `used-by` definition is "knowledge entries or lessons citing the row", and `corpus/lessons/round-44.md`, `corpus/lessons/round-44-verifier-spotcheck.md` and `corpus/lessons/round-45.md` already cite S138 and/or S139 without being listed. Adding a round-49 lesson path would follow the definition, but the existing cells already omit the lessons, so the convention is unsettled.
