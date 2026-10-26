# gap-rule.json — derivation, key vocabulary, and structural allowances

Companion to `gap-rule.json` (the file the counter binds; report §12). Fixed from **development runs
only**: 7490 07.62 AVM-BE member (sha256 `58d73b2f…`), 7430 07.31 AVM-BE member (`b919a6a2…`), and the
lane-built standard-BE carriers `t1` / `t2` / `t2b`. No frozen carrier was opened. Evidence:
`feature-table.tsv`, `env-*.json.gz`, `oracle-*-inspect.json`, `member-link-map.tsv`,
`sq-v4be-noflag-ll.txt`.

## Key vocabulary (matches the frozen reader: `dir|symlink|char-device|block-device|fifo|socket`)

SquashFS v4 inode type ids (`fs/squashfs/squashfs_fs.h`, the table the reader's `BASIC_TYPE` mirrors):
`1 dir, 2 reg, 3 symlink, 4 blkdev, 5 chrdev, 6 fifo, 7 socket` and the extended `8 ldir, 9 lreg,
10 lsymlink, 11 lblkdev, 12 lchrdev, 13 lfifo, 14 lsocket`. So `char-device` = type 5 and
`block-device` = type 4; the earlier `device` key was a shorthand and is replaced (not kept) so the table
and this file cannot disagree.

## Per-kind derivation

| key | measured source | measurement | encoding |
|---|---|---|---|
| `symlink` | 7490: 86 links (7 absolute); 7430: 90; t1: 5; t2: 4; t2b: 5 | every **retained** link yields exactly one `unpublished-entry` (86/86, 90/90); escaping links yield `MaliciousSymlinkRemoved` and no gap (t1 4 gaps + 1 MSR, t2 3 + 1, t2b 3 + 2) | `["unpublished-entry"]`, `required: true` |
| `char-device` | both members carry `dev/led` (`crw-rw-rw-`, 247,0; oracle `special_files: 1`) | **no gap, no unpublished entry, no diagnostic, no log line** — `sasquatch-v4be` as non-root leaves `dev/` empty, REA inventories only materialised entries; `"led"` occurs 0 times in the member envelope | `[]`, `required: false` |
| `block-device` | none present in any measured member | not measured; a block node cannot be created unprivileged either, so the expected behaviour equals `char-device` | `[]`, `required: false` `[INFERENCE]` |
| `fifo` | none present | not measured. If one materialises it appears in `unpublished_entries` with kind `special`, and REA emits the gap with kind **`unpublished-entry`** for every unpublished entry (`FirmwarePublication.js:301-307`: `unpublished.map(entry => ({ kind: "unpublished-entry", relative_path: entry.relative_path … }))`). So the gap kind is source-grounded, not a guess; the *entry* kind stays `special`. | `["unpublished-entry"]`, `required: false` |
| `socket` | none present | same branch as `fifo`, same source line. | `["unpublished-entry"]`, `required: false` |
| `dir` | 10 dirs in each member; 933 in the 7590 LE member; 7 / 9 in t1 / t2 | directories never enter REA's entry list — `inventoryFirmwareOutput` traverses them and counts them against the entry budget but only pushes non-directory entries (`FirmwareFiles.js:121-160`) — so no gap can ever map to a directory | `[]`, `required: false` |

`required` is stated explicitly for every key so the counter's default (`true` when `allowed` is non-empty)
never overrules the measured device case. The device is the counterexample to "no gap ⇒ it was published":
it is **not** materialised (empty `dev/`) and still has no gap.

## Structural allowances (`relative_path: null` gaps)

| kind | per-carrier measurement | allowance |
|---|---|---|
| `unknown-chunk-handler` | one 8-byte handler-less chunk on both members (the `round_up(bytes_used,4096)` residual: 35 012 608 vs file 35 012 616; 25 825 280 vs 25 825 288); also 1 in the whole-`.image` depth-2 receipt; **0** on `t1`/`t2`/`t2b` because their `file_size` equals the chunk end | 1 |
| `depth-limited` | exactly 1 at `--max-depth 1` (the chunk's carve dir is the task at `task.depth >= max_depth`); 0 at the default depth 3 for carriers with no nested container; 1 in the whole-`.image` depth-2 receipt | 1 |

Allowances are maxima, so the measured 0 on lane-built carriers and 1 on vendor members are both inside
them. A carrier form outside these two (deeper nesting, two residuals) needs a re-frozen rule, not a
looser one.

## Residual honesty (do not guess a mapping)

- `fifo`/`socket` are the only branches not measured on real carrier bytes; they are encoded so both
  outcomes pass today (`allowed` non-empty, `required: false`). If a frozen carrier ever shows a
  materialised special file whose gap kind is not `unpublished-entry`, that is an honest red and the
  freeze should re-derive from that carrier's development twin.
- `missing-extractor-dependency` and `encrypted-chunk` are not in `structural` and not in any `allowed`:
  neither was produced, and both must fail if they appear.
