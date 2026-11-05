source: S265 — https://github.com/xqy2006/jsc2js/releases — tag 14.8.178.14 release body, opened 2026-11-03
verified-at: 2026-11-03
recheck: 90d

# jsc2js releases are a version index, not a compatibility guarantee

Assimilated from `merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-release-inventory.md` (staged S129, renumbered by URL to S265).

The release body for tag 14.8.178.14 reads: "Patched d8 for V8 14.8.178.14 (includes d8 + snapshot_blob.bin)."

The L1 fetched API pages 1–7 with `per_page=100` on 2026-11-03 and counted 679 distinct tags. Majors were 5:12, 6:18, 7:54, 8:79, 9:66, 10:55, 11:83, 12:78, 13:92, 14:90, 15:52. This corrects the staged entry's 677 and its incomplete major-version list; these are dated observations, not a promise of exhaustive future inventory. Independent source checking: `.ufo/waves/round-64/w1/ScoutJscRoute/` and `.ufo/waves/round-64/w1/ScribeSources/`.

Recheck: fetch `https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=N` for successive N until an empty array; save each response separately; parse each JSON array and count distinct `tag_name` values. Never count only the default first page.

A published tag establishes a downloadable build, not that it loads a particular cache. The round-64 matrix measured failures on the shipped Typora cache despite a matching V8 version. No general source-recovery capability follows.
