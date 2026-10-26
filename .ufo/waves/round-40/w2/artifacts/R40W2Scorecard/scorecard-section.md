Draft for L1 integration (seat `R40W2Scorecard`, round 40 wave 2). Every number below is measured
from Git objects at the revision it names — `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` for the owned
axes, `42c10a58cb2cae3a4a0122af35a0cf95ac718043` for the two claim rows (the measured revision the
frozen counters scored). Nothing here is written into `SCORECARD.md`. Command A is the recipe at
`SCORECARD.md:92-124`, run unmodified with `REV` set; its raw output is
`artifacts/R40W2Scorecard/cmdA.txt`.

---

## Round 40 — genuine AVM-layout big-endian SquashFS v4 measured but not promoted on a counter suffix false negative; a triage table with a scored action column reaches 26/26 on a freeze-seeded held-out set

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`
(`plans/round-40-claims.md`, every round-40 tool, the four C1 carriers with their oracles and the gap
rule, the SKILL triage v2 block 19 and its entry, S123, the C2 controls, wave-1 evidence); controls
`45e89864e967d7501110b529cb8517b26b92c7ef`; C2 held-out data
`2d1ac5bcd08f6828dbfdee9054bbeec0ea211b33`; C1 after-receipts
`73c7bf9c73bd7b4891c4e46c93d1d29c287e4541`; landing `42c10a58cb2cae3a4a0122af35a0cf95ac718043`;
scores `c17565bc772dd296deeaf1699fbe737c6afbea3c`; honest-stop record with the Core row demoted
`4d62ee5a86b4692a13f682b29ed7975e8d7e5326`; wave-2 dispatch
`0b15c8b2c593b7954efda92249ef3fa895c79f99`. Wave 1: 42 seats building and
attacking the draft, 42 non-empty outputs (`.ufo/waves/round-40/w1/`). Wave 2: 38 seats attacking the
landing after data (`.ufo/waves/round-40/w2/`).

Both claims carry the round-39 freeze-integrity rule. The C1 score reports `frozen_path_changed []` and
the C2 score `frozen_paths_changed []` at `42c10a58`, and every score receipt records the scorer's exit
code (routed R39-CL6): C1 exit 1, C1-extra exit 0, C2 exit 0.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R40-C1 | coverage — genuine AVM-layout big-endian SquashFS v4 Frontier → Core: `PROVINCE.md` row naming the AVM layout, round-40 frontier note, entry `2026-10-26-r40-avm-be-squashfs-core`, `corpus/README.md` coverage-map row, S124–S126 | at the freeze the counter exits 1, `carriers_matched 0`, `target 4`, and every documentation binding false (`province_core_section`, `province_core_row`, `entry_present`, `coverage_map_row`, `frontier_note`, `sourced`), while its frozen inputs validate (`carriers_spec_ok`, `frozen_tables_valid`, `gap_rule_ok` true) (`.ufo/waves/round-40/controls/c1/ctl-c1-0-do-nothing.json`) | `carriers_matched 3` of `target 4`, `met_target false`, exit 1; all document bindings true; V1 697/697, V2 8/8, L1 7/7 oracle regular files published (paths and sha256), L2 6/6 published but `nonregular_unpublished_ok false`; supplementary gate `c1-extra.py` met, exit 0 (`.ufo/waves/round-40/l1/scores/c1-extra-at-42c10a58.json`) | `python3 -I -B tools/round-40/c1-counter.py --root <LANE> --rev 42c10a58 --freeze 7fce3086 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache <CACHE> --json-out <OUT>`; `python3 -I -B tools/round-40/c1-extra.py … --base fa6a8a3f …` | `42c10a58` (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`, exit 1; `c1-extra-at-42c10a58.json`, exit 0) | **NOT MET** — honest stop; Core row demoted to a measured-not-promoted record at `4d62ee5a` |
| R40-C2 | depth — SKILL `## Queue-drain craft` rule block 19 after `<!-- sqfs-triage-table v2 -->` (`SKILL.md:361-375`, 11 labels, columns `operation` and `provider` first), interpreter `tools/round-40/sqfs-triage-v2.py`, held-out set seeded by the freeze | at the freeze the counter exits 2 `no_manifest_at_rev` (`.ufo/waves/round-40/controls/c2-counter-at-freeze.json`); the frozen v2 interpreter on the base `SKILL.md` exits 2, `marker '<!-- sqfs-triage-table v2 -->' absent from the craft section`; the best pre-data control reaches 24/26 (`CTL-C2-4`, `CTL-C2-5`, `CTL-C2-6`, `.ufo/waves/round-40/controls/c2-dev-scores.json`) | `matched 26` of `n 26`, `bindings_false []`, `frozen_paths_changed []`, `met_target_consistent true`, exit 0; 13 classes × 2, 12 distinct (label, action) pairs, the out-of-domain envelope labelled `unclassified` with action `none`; v1 table 3086 B and v2 table 6603 B identical at the freeze and at the measured revision; manifest first added `2d1ac5bc` with `seed == freeze` | `python3 -I -B tools/round-40/c2-counter.py --root <LANE> --rev 42c10a58 --freeze 7fce3086 --json-out <OUT>` | `42c10a58` (`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`, exit 0) | **MET** |

C1's miss is one binding, and it is a counter false positive on a path suffix, observable inside the
frozen evidence rather than argued: L2's receipt records two `unpublished-entry` gaps, at
`firmware.bin_extract/bin/busy` and `firmware.bin_extract/usr/bin/ls` (both symlinks of
`corpus/evidence/round-40/c1/L2/nonregular.tsv`), while the same counter's `nonregular_published` lists
`firmware.bin_extract/usr/bin/busy` — the *regular* file `usr/bin/busy` in `oracle.tsv`, whose path ends
with the symlink path `bin/busy` (`same_rel` is `candidate == rel or candidate.endswith('/' + rel)`,
`tools/round-40/c1-counter.py:606-607`). The extraction published no symlink path, and the two clauses
contradict each other in one score file. The round-39 AVM sentence in `PROVINCE.md` therefore stands:
the AVM measurement is recorded, not promoted.

The AVM layout itself was measured as stated before data: `sqsh` major 4 minor 0 with the marker
`mkfs_time == bytes_used` on all four carriers (V1 5442392, V2 26013550, L1 230884, L2 241390) and
little-endian metadata block lengths where the field is decidable (V1 `meta_len_le 1380` vs `meta_len_be
25605`; V2 704 vs 16386; L2 `identity`; L1 `plausibility`, 932 vs 9347). Compression ids 4/4/4/1
(xz/xz/xz/gzip) are all covered, and every carrier's gaps are within the frozen rule (V1 264 = 263
`unpublished-entry` + 1 `depth-limited` on 381 non-regular entries with the char device invisible; V2 86
= 85 + 1 on 95; L1 3 = 2 + 1 on 13; L2 3 = 2 + 1 on 10).

Owned scores: coverage 10 → 10 (map proxy 128/128 → 130/130: both round-40 entries added and both mapped,
`missing []`, `dangling []`; measured with command A at `4d62ee5a`, and 129/129 at the freeze, where only
the triage entry exists); depth 10 → 10 (queue-drain rule blocks 18/18 → 19/19 with every block's
citations resolving, `citation_resolved_rules 19`, craft section `SKILL.md:81-375` — heading `:81`, last
non-blank line `:375`, next heading `:380`, v2 marker `:361`; command A at `4d62ee5a`); calibration
10 → 10 (no calibration claim this round; the r1 rubric value 9/9 stands, and the move is the defect
below). Saturation line and stagnation window unchanged; a perfect finite proxy retires no axis.
Capabilities row entered: **SquashFS `extract-firmware` outcome triage v2 (label and action)** — a frozen
interpreter reads one machine-readable SKILL table with an `operation`/`provider` domain guard and a
closed 11-token action column, and returns the (label, action) pair for all 26 freeze-seeded held-out
envelopes, labelling an out-of-set envelope `unclassified` with action `none` (evidence
`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`; entry
`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`). **No capability row for AVM-BE recursion**: the C1
claim stopped, and a measured-not-promoted record is not a capability.

Paste-ready row for the `## Capabilities` table:

```
| SquashFS `extract-firmware` outcome triage v2 (label + action) | reads only the SKILL v2 triage table (block 19, `SKILL.md:361-375`): an `operation`/`provider` domain guard, rows for mixed symlinks, partial body failure, clean-empty trees and a no-match `unclassified` case, and a closed 11-token action column; scores 26/26 on 13 freeze-seeded held-out classes × 2 with 12 distinct (label, action) pairs | `.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`; `corpus/evidence/round-40/c2/heldout/`; entry `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` | round 40 |
```

### Wave-2 falsification record (after the landing)

*Draft-state note for L1 (this seat, `R40W2Scorecard`, is one of the 38 wave-2 seats; no wave-2 seat
finding is adjudicated here).* Two facts a scorecard can record now:

1. **The 3/4 is a `42c10a58` measurement, and the record says so.** The demotion at `4d62ee5a` renamed
   the heading to `## Round-40 measured, not promoted (R40-C1 honest stop)`, so at the tip
   `province_core_section` and `province_core_row` (frozen constant `CORE_HEADING`,
   `tools/round-40/c1-counter.py:193`) are false, and `c1-extra.py`'s `frontier_content` — which requires
   a `Round-40 frontier note` line naming the heading, the entry stem and `supersede` — is false too;
   evaluated by applying the frozen conditions to the two revisions' `PROVINCE.md` bytes, not by
   re-running the counters. `carriers_matched` cannot move with the demotion: `git diff --stat 42c10a58
   4d62ee5a` touches only `PROVINCE.md`, `corpus/README.md`, the C1 entry and the score receipts, so the
   carrier, oracle and receipt bytes are identical. The honest stop is thus self-consistent at the tip —
   no revision in the round reads `met_target true` — and every C1 row must bind its numbers to
   `42c10a58`.
2. **The lane worktree carried an uncommitted `SKILL.md` edit at measurement time** (`+19` lines, a
   `### Round-40 instrument registry` section appended after `:1383`; `git status --porcelain` at
   `0b15c8b2` shows `M SKILL.md`). It does not touch the craft section or the v2 table, so command A and
   the C2 table bindings at `4d62ee5a` are unaffected (both read Git objects). It is not this seat's
   edit; L1 decides whether it is committed or dropped before this section lands.

- **planned (round 41):** coverage on the same AVM surface with a counter whose non-regular clause
  compares the published set element-wise (or by receipt `files[]` kind) instead of by path suffix, so
  L2's two `unpublished-entry` gaps and a published regular file cannot collide; the round-40
  measurement stands as its input and the honest stop needs no re-freeze. Calibration second: the
  routed defect that both `c1-extra.py` bindings and the `CORE_HEADING` document bindings are
  revision-fragile — a score receipt should re-assert its own document clauses at the tip, or the claim
  should decline to be scored after a demotion.
- **retired:** none. Coverage, depth and calibration stay tied at 10; both proxies are perfect finite
  counts and retire no axis.
