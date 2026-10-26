# R41C2EntryReview — evidence record

All byte reads at base `49096c7e6f226af0c750c4b003be58883cb6049f`. Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41C2EntryReview` removed at finish; this directory holds
everything cited by `../../../R41C2EntryReview.md` (report path relative to the lane root).

## Commands

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
  -> 49096c7e6f226af0c750c4b003be58883cb6049f   (== the base; working tree clean for tracked files:
     git status --porcelain shows only untracked .ufo/waves/round-41/ and plans/round-41-claims.md)
git -C <lane> show 49096c7e…:SKILL.md                                > $S/at-commit/SKILL.md
git -C <lane> show 49096c7e…:tools/round-40/sqfs-triage-v2.py        > $S/at-commit/tools-round-40/…
git -C <lane> show 49096c7e…:tools/round-39/sqfs-triage.py           (hashed in place via the working tree)
git -C <lane> show 49096c7e…:corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md > $S/at-commit/corpus-knowledge/…
python3 -I -B celldiff.py        # cell-by-cell diff, v2 and v1 tables vs embedded copies
python3 -I -B celldiff.py > celldiff-output.txt   # re-run from the artifacts copy, exit 0
```

## sha256 (working tree == at-commit copies for every file cited)

| file | sha256 |
|---|---|
| `SKILL.md` | `926dac301cf0281e2b35b6736b6f6ee869a0a1b415fd5207f9de3959c4ca0054` |
| `tools/round-40/sqfs-triage-v2.py` | `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617` |
| `tools/round-39/sqfs-triage.py` | `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` |
| `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` | `b160af3fa613d8264660a7d005adb0635fec3dffa51ba57f9b8ddeac481b195c` (at-commit copy and working-tree file hash equal, measured) |

## celldiff.py results (full output in `celldiff-output.txt`)

- v2: `SKILL.md:363-375` vs `TABLE_BLOCK` (`sqfs-triage-v2.py:171-187`) — headers equal (12 cells);
  divergence in exactly 2 cells of row `avm-marker-be-dropped` (`cause`, `source`); all other 10 rows
  byte-identical.
- v1: `SKILL.md:337-346` vs round-39 `TABLE_BLOCK` (`sqfs-triage.py:131-141`) — headers equal (9 cells);
  5 decision-cell divergences: handler `squashfs_v4_be` (embedded) vs `squashfs_v4_*` (SKILL) on
  clean/escaping/in-tree; published files `0` (embedded) vs `*` (SKILL) on dep-missing-be/dep-missing-le.
- escaping row decision cells (SKILL:372): `['escaping-symlink-removed', '`extract_firmware`',
  '`unblob`', '`squashfs_v4_*`', '`*`', '`*`', '`*`', '`yes`', '`*`']` — gap-kinds cell is `*`.
- `_skel(TABLE_BLOCK)` uses: 19 in the v2 selftest region (region from `:720`; 45 `@case`, 41 `_skel(`
  calls, 22 `TABLE_BLOCK` refs); 16 in the v1 selftest.
- contains operator in the v2 interpreter: absent (`match_set` = `any`/`none`/`frozenset(values) == payload`,
  `:604-605`; `rule_matches` `:608-633`; `classify` first-match-wins `:636-640`).

## Anchor checks (read-only)

- `w1/R40C1MarkerBoundary.md` H1 `:111-127` + matrix rows `d2`/`m1s`/`m2s` `:95,:102,:104` — marker-stripped
  genuine AVM body: unblob appends `-be`, 0 files, `extractor-failure`, P=0; `sasquatch-v4be` noflag extracts.
- `w1/R40MistakeHunt.md:65` MH-6 — the TableReview's M2 quote ("The marker-stripped shape is exactly the
  frozen `body-extractor-failure` tuple …") is verbatim present in the MH-6 row.
- `w1/R40C2ActionReview.md` findings 4–7 (`:62-72`) and D5b/D7 (`:55-61`) — anchors exist as cited.
- `w1/R40C2Shortcuts.md` D2 `:156-163`; one-authority correction `:223-227` (unadopted by the round-40 freeze).
- `SCORECARD.md:3443` — the R40-C2 row already carries AxisFit F1's partition sentence.
- Installed unblob 26.6.4 `…/site-packages/unblob/extractor.py:67-72` — empty-target symlink branch removes
  with no `MaliciousSymlinkRemoved` report (L6's mechanism, my own read).

## Tooling record

Nothing installed, upgraded or removed; no pacman transaction. System `python3` (stdlib only), read-only
`git`, `read`/`grep`/`write` tools. No vendor bytes copied; no carrier built; no REA/unblob run.
