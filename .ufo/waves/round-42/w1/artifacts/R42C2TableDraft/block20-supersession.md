Supersession sentence for block 20 (append to the end of block 20's bullet, i.e. after `stale second text behind.` on `SKILL.md:414`, before the blank line and the `**Layout pre-check …**` paragraph). Exactly one sentence, 2-space continuation indent:

```
 Superseded for routing and for the action column by rule block 21 (table v4,
  round 42): v4's handler cells cover the seven v1–v3 handler names this table's
  `squashfs_v4_*` cells cannot match, so a legacy chunk is labelled instead of falling to
  `unclassified`, and v4 adds the `legacy-body-failure` row, whose action is a cross-read
  rather than the `-be` wrapper.
```

Kept as one sentence on purpose (the dispatch says one sentence). It names only two changes,
both measured this wave: v3's four `squashfs_v4_*`/`squashfs_v4_be` handler cells cannot
match a v1–v3 chunk (measured: both dev-arm legacy envelopes are `unclassified` under the
frozen v3 interpreter), and `legacy-body-failure` does not exist in v3 (12 rows vs 13).

Wording note for the L1: block 20's bullet already ends with the no-embedded-copy sentence,
so this appends after that and does not disturb the table, the marker or the action line.
The v3 interpreter takes the first table after `<!-- sqfs-triage-table v3 -->`, which is
block 20's own table; block 21's marker sits below it, so v3 keeps reading v3.
