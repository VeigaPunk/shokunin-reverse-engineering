# R40W2C1AxisFit — probes (seat R40W2C1AxisFit, round 40 wave 2)

All commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless noted; read-only.
No REA, unblob or sasquatch run; no vendor bytes fetched; nothing written outside this artifact dir.

## P1 — does any site at 4d62ee5a still assert AVM-BE is Core?

```
git grep -n "r40-avm-be-squashfs-core\|r40-avm-be" 4d62ee5a -- ':!.ufo'
```

Hits (13 sites, all non-.ufo):

| # | site | what it says | Core assertion? |
|---|---|---|---|
| 1 | `PROVINCE.md:386` | heading `## Round-40 measured, not promoted (R40-C1 honest stop)` | no |
| 2 | `PROVINCE.md:392` | the table row (probe/evidence cells) | no — under the demoted heading; row text carries no "Core" word |
| 3 | `PROVINCE.md:394` | `Round-40 frontier note … AVM-BE is **measured, not promoted** … AVM-BE bodies (this measurement included) … Still Frontier` | no |
| 4 | `corpus/README.md:96` | index row `**measured, not promoted** (R40-C1 honest stop, 3/4 on a counter false negative)` | no |
| 5 | `corpus/README.md:208` | knowledge row `measured (not promoted: R40-C1 stopped 3/4)` | no |
| 6 | `corpus/README.md:250` | frontier bullet `**measured, not promoted** … Still frontier: AVM-BE promotion, …` | no |
| 7-12 | `corpus/SOURCES.md:118,120,127,130,131,132` (S112, S114, S121, S124, S125, S126) | `used-by` cells naming the entry | no (registry rows make no status claim) |
| 13 | `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:41` | round-40 correction note | no |

Also checked: `SCORECARD.md` has no round-40 record yet (`grep -n -i "round 40\|AVM" ` → only the
round-39 capability rows 627-629 and the round-40 `planned` line 3432); `corpus/QUALITY.md` has no
AVM/SquashFS line; `SHONEN.md` has no round-40 AVM line. `grep -n "Round-40 additions to Core"` over
the whole tree at 4d62ee5a returns only `.ufo/` wave evidence (dispatch/spec/wave-1 reports), never a
tracked curriculum file.

Residual: the **entry stem** is `2026-10-26-r40-avm-be-squashfs-core`, and `-core` is this corpus's
recent promotion marker (round-39 entry `…-r39-be-squashfs-v4-core.md` is Core; the round-38
measured-not-promoted entry `…-r38-sasquatch-be-squashfs-recursion.md` has no suffix; only two entries
in `corpus/knowledge/` end in `-core.md`). The stem is hard-coded in both frozen counters, so the
demotion cannot rename it without changing a frozen path:

```
grep -n "ENTRY = \|STEM = " tools/round-40/c1-counter.py tools/round-40/c1-extra.py
tools/round-40/c1-counter.py:191:ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
tools/round-40/c1-counter.py:192:STEM = '2026-10-26-r40-avm-be-squashfs-core'
tools/round-40/c1-extra.py:36:ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
tools/round-40/c1-extra.py:37:STEM = '2026-10-26-r40-avm-be-squashfs-core'
```

## P2 — frozen predicate vs counter clause list (the miss's cause)

```
git show 7fce3086:plans/round-40-claims.md | md5sum        # predicate bytes at the freeze
git show 4d62ee5a:plans/round-40-claims.md | cmp - <(git show 7fce3086:plans/round-40-claims.md)
```
`cmp` exit 0: the claims file is byte-identical freeze→tip (predicate never edited).

Frozen predicate P40-C1 (bytes at 7fce3086, `plans/round-40-claims.md:38-51`) names, per carrier:
handler + no failed chunk; every oracle regular file published (suffix, sha256); gaps only as the gap
rule allows; subject digest = pin; evidence id recomputes; carrier pin + AVM marker + LE metadata
lengths; fresh REA rerun with the same `plus-extractor` projection; frozen reader reproduces the
oracle/non-regular tables; and five doc bindings (PROVINCE Core row + frontier note, entry cites a new
SOURCES row, README maps the stem); plus no frozen C1 path changed.

Counter per-carrier clauses (`tools/round-40/c1-counter.py:227-231`): 17 clauses. Mapping to the
predicate sentence:

| clause | stated in P40-C1? |
|---|---|
| carrier_present, carrier_pin_ok | yes ("carrier bytes hash to the pin") |
| layout_ok | yes ("AVM marker with little-endian metadata block lengths") |
| oracle_ok, nonregular_ok | implied ("the frozen reader … reproduces its frozen oracle and non-regular tables") |
| receipt_present, receipt_fresh | yes ("first added in a commit that descends from the freeze") |
| subject_pin_ok, evidence_id_ok | yes |
| operation_ok, handler_ok, chunks_ok | yes |
| oracle_hits_ok, gaps_ok | yes |
| projection_ok | yes ("fresh REA run … same `plus-extractor` projection") |
| **nonregular_unpublished_ok** | **no — absent from the predicate sentence** |
| **run_provenance_ok** | **no — absent from the predicate sentence** |

L2 clause dump at the score receipt (`c1-score-at-42c10a58.json` → `carriers.L2`): every clause true
except `nonregular_unpublished_ok`. `run_provenance_ok` is true on all four carriers, so the **only**
cause of `carriers_matched 3 < target 4`, `met_target false`, `exit_code 1` is the one clause the
frozen predicate never states. Read as written, the predicate is met on all four carriers
(`carrier_pin_ok`, `layout_ok`, `oracle_hits_ok` 6/6, `gaps_ok`, `subject_pin_ok`, `evidence_id_ok`,
`projection_ok` all true for L2).

## P3 — the clause's implementation: "equals" in the docstring, suffix test in code

```
sed -n '54,56p' tools/round-40/c1-counter.py     # docstring: "no published regular file path equals …"
grep -n "def same_rel" -A 2 tools/round-40/c1-counter.py
tools/round-40/c1-counter.py:606:def same_rel(candidate, rel):
tools/round-40/c1-counter.py:607:    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))
```

Blast radius across all four receipts (script: strip nothing, apply the counter's own suffix test):

| carrier | published files | non-regular entries | suffix hits | exact hits (root stripped) |
|---|---|---|---|---|
| V1 | 697 | 380 | 0 | 0 |
| V2 | 8 | 94 | 0 | 0 |
| L1 | 7 | 12 | 0 | 0 |
| L2 | 6 | 9 | 1 — `firmware.bin_extract/usr/bin/busy` vs symlink `bin/busy` | 0 |

L2's one hit is the symlink's own in-tree target: `nonregular.tsv` row `bin/busy  symlink  ../usr/bin/busy`
and `oracle.tsv` row `usr/bin/busy  e28f81fc…  40000`. The receipt publishes no path for either
symlink (`bin/busy`, `usr/bin/ls` are `unpublished_entries`, each with an `unpublished-entry` gap), so
the clause is flagging a legitimate publication. The clause is layout-lucky on V1/V2/L1, not safe.

## P4 — S126 lineage re-derivation (read-only; no vendor bytes)

```
sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/{lead1-avm-image.tsv,avm-be.squashfs}
f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0  lead1-avm-image.tsv
c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32  avm-be.squashfs
```

Superblock parse of the retained 4096-byte image (big-endian fields; stdlib only):

```
inodes 5  mkfs_time 365  block_size 65536  compression 4 (xz)  major 4 minor 0
root_inode 0x80  bytes_used 365  id_table_start 357  xattr_id_table_start 0xffffffffffffffff
inode_table_start 121  directory_table_start 239
header at 121: 74 00  -> little-endian 116 (masked 0x7fff); big-endian decode 29696 fails
121 + 2 + 116 = 239 == directory_table_start   (True)
```

`unblob.log` (round 11) verbatim argv line:
`sasquatch-v4be -no-exit-code -f -d /tmp/r11-avm3/avm-be.squashfs_extract …/avm-be.squashfs`
— no `-be`; then four `Processing file` lines (`apple1.txt` … `apple4.txt`) and no failure line.
Neither `unblob.log` nor `avm-final.log` carries an unblob exit code (`avm-final.log` has only
`make exit=0`); `avm-final.log` also records an earlier **failed** attempt (`Can't run extract
command`, `dependencies=['sasquatch-v4be']`), i.e. the successful run is the `unblob.log` one.

Lineage scope: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md:76,78,79` show the lead
ran r9 (`sasquatch-unblob-avm-branch`), r10 (`avm-image-build-blocker`), r11 (`avm-image-extraction`)
— "the lane's rounds 9-11 lead" matches.

## P5 — demotion touched no frozen path

```
grep -n "FROZEN_PATHS" -A 12 tools/round-40/c1-counter.py
git show --stat 4d62ee5a        # PROVINCE.md, corpus/README.md, the entry — none of the frozen list
```
The score receipt at 42c10a58 records `frozen_path_changed: []`, `carriers_unchanged: true`,
`gap_rule_unchanged: true`, `exit_code 1`, `carriers_matched 3`, `target 4`, `met_target false`.
