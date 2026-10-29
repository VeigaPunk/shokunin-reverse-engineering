# AssimGuard — id-collision guard for `merge/kaidoku/` (R50 wave 1)

**Verdict: the staged package CANNOT be appended as-is. The round-prompt guard yields 44 collisions (S106–S149, every id in the overlap), with 0 identical rows — each id names a different source in the registry vs the staged file. The guard itself is proven (it catches an indented row the column-zero pattern misses). Quarantine slice: 5 rows, all carry an S-id. Staged ids cited by the two AVM-LE notes (S206/S207/S212/S213/S214) are collision-free and absent from quarantine.** Nothing was run in `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`; sources were only read.

Time of runs: 2026-10-28T23:32Z–23:40Z. Receipts: `.ufo/waves/round-50/w1/AssimGuard/assimilation/` (`SHA256SUMS` there). Scratch `/fast/scratch/hyaku/kaidoku-r50/AssimGuard` removed at the end.

## Findings

| # | Check | Exact command | rc | Result | sha256 of output |
|---|---|---|---|---|---|
| 1a | registry ids | `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md \| grep -oE 'S[0-9]+' \| sort > reg-ids` | 0 | 149 ids, S001–S149, no duplicates | `041ff3de…a1b` (reg-ids) |
| 1b | staged ids | same on `merge/kaidoku/SOURCES.append.md` -> `staged-ids` | 0 | 132 ids, S106–S237 contiguous (no dups; 0 indented rows in the staged file) | `93841167…89b` |
| 1c | collisions | `comm -12 reg-ids staged-ids > collisions` | 0 | **44** = S106…S149 contiguous; first 10: S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 | `a884f408…09010` |
| 1d | are collisions the same row? | python: compare registry vs staged source column per id | 0 | **0 of 44 identical**. e.g. S106 reg = GNU binutils readelf, staged = unblob README; S108 reg = unblob SquashFS handler, staged = Linux core(5); S110 reg = unblob README @26.6.4, staged = dncil README | (inline; not saved) |
| 2 | guard proof | fixture `guard-proof/SOURCES.indent.md` = registry with all col-0..3 `S###` rows removed + one row `  \| S106 \| indented fixture row \| docs \| A \|` (line 108); guard run on it, then column-zero-only `grep -oE '^\|[[:space:]]*S[0-9]{3,}'` | 0 / 0 | guard `reg-ids` = `S106`, `collisions` = **S106 (non-empty)**; column-zero-only: 0 ids, **0 collisions (miss)** | proof/collisions `68f990a0…206b`; col0 `e3b0c442…b855` (empty file) |
| 3 | quarantine slice | `awk -F'\|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' …/corpus-expansion-1/absent-defect-register.md > quarantine-slice` | 0 | **5 rows**, `grep -cvE 'S[0-9]+'` = 0 (every line has an S-id): S150 (`payload-absent`), S113, S117, S136, S147 | `7383a90e…8e6a` |
| 4 | note citations | `grep -n '^source' knowledge/corpus/knowledge/avm-le-*.md` | 0 | see below | — |

Check 4 detail (path: `merge/kaidoku/knowledge/corpus/knowledge/`):
- `avm-le-variant-reachability.md`: S206, S207. `avm-le-image-genuine-marker.md`: S212, S213, S214.
- Each is staged (1×), not in the registry (0×), not in the quarantine slice (0×). None collides.

## Defects / risks for the L1
1. **Real collision, not a false positive**: appending `SOURCES.append.md` verbatim gives 44 duplicate S-ids with different meanings (S106–S149). The note `source:` lines then resolve to the wrong registry row for any of them. Across all `source:` lines in the package's knowledge notes: 130 distinct ids; **42 of them collide with registry ids** (S106–S113, S116–S149 — set in `knowl-ids`; `comm -12 knowl-ids reg-ids`). The AVM-LE notes are safe only because their ids are ≥S206. Remedy needed before append: renumber the staged rows S106–S149 (S150+ appear unused in the registry; first free id is S150, but S150–S237 are staged ids too, so a renumber has to be a shift of the whole staged block, with note `source:` lines rewritten to match) or append only S206/S207/S212/S213/S214 and leave the rest. I did not perform either.
2. **Quarantine ids are in the staged id space, not the registry's.** The slice's S113/S117/S136/S147 collide with registry rows of the same number (different sources). If those are applied by id against the lane registry they quarantine the wrong rows. If a renumber is done, the slice must be renumbered the same way. Also the register itself has a stray backtick (`S113\``, `S117\``, `S136\``, `S147\``) in the second table; the awk pattern tolerates it (`$4 ~ /S[0-9]+/`) but any exact-match join must strip it. S150's row comes from the first (class) table and has a different column layout (`$5` = class, not reason).
3. Guard weakness (proved in check 2): the column-zero-only pattern misses an indented row; the `^ {0,3}` form catches it. 4+ space indent (markdown code block) is not matched by design; the staged file has none (0 rows matching `^\s{4,}\|`); the registry has none indented at all.
4. Check 2 fixture removed every other registry row so the single collision is attributable to the indented row; it proves detection, not a particular real-registry state.

## Not run
No campaign tool in `merge/kaidoku`; no append; no renumbering; no content check of staged S206–S214 against their upstream URLs.

Tooling installed: none.
