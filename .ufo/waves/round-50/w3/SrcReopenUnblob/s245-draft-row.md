# Draft S245 row (L1 input — review/rewrite freely)

Same URL as S108/S112, different scope (LE branch). Census impact verified: W04 warning only, validate exit stays 0 (receipts R2/R3). Insertion point used in the fixture: directly after the S248 row, Registry table kept contiguous.

```
| S245 | unblob SquashFS handler at tag 26.6.4, LE branch — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | the LE decision surface of unblob 26.6.4's SquashFS extractor only: the `SquashFSv4LEHandler` name and the little-endian argv branch; not the BE/AVM branch (S108, S112), not other versions, not any carrier | tag 26.6.4 = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`; re-opened 2026-10-29T20:34:12Z HTTP 200, 19,842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (byte-identical to attempt-1 and to S108's pinned hash); line 455 `NAME = "squashfs_v4_le"`; lines 53-54 `case Endian.LITTLE, _:` then `commands_args.append("-le")`; `is_avm` appears only at lines 48-49, inside `case Endian.BIG, 4:` | A little-endian v4 chunk runs plain `sasquatch -le` with no AVM marker test — the `is_avm` probe exists only in the `Endian.BIG, 4` branch — so an AVM-marked LE member is handled as ordinary LE v4 by this extractor | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md |
```

Notes for L1:
- used-by points at the two existing entries that already cite the LE branch of this file (`2026-10-28-r44-squashfs-v1v2-core.md` `:48-54`, `2026-10-28-r49-squashfs-v1v2-core.md` `:53-54` with receipt `s112-argv`), so E11 passes at landing time; append the R50-C1 entry to used-by when it lands.
- opened 2026-10-28 follows the attempt-2 claims wording ("opened 2026-10-28, re-opened 2026-10-29 this attempt"); recheck `on-release` matches S108 (same tag-pinned bytes); switch to `180d` to match S112 if preferred — both pass E09.
- Id gap check: S245 absent from the registry at base `f890bbea` (grep: no matches); S150–S242 intentionally skipped per `plans/round-50-claims.md:259-261`.
