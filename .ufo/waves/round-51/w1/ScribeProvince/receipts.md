# R51-C1 ScribeProvince — receipts (every command run by this seat)

Host: `vgpnk` / Linux 7.2.11-arch1-1. Lane:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base revision
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

No REA run, no `--data-run`, no network, no download, no mutation of the lane tree or the
fleet repo: every command below is read-only (`grep`/`awk`/`git log`/`git show`/`sed -n`/
`python3` on committed files). The only writes this seat made are inside
`.ufo/waves/round-51/w1/ScribeProvince/` and the scratch
`/fast/scratch/hyaku/kaidoku-r51/w1-ScribeProvince` (removed after the receipts were copied in).

---

## R1 — per-class device census from the committed oracle tables

Command (run from the lane root):

```
awk -F'\t' 'NF>=2{print $2}' tools/round-50/oracle/<id>.nonregular.tsv | sort | uniq -c
for f in c6430 c6490 g7581 g7582; do
  printf "%s\t" "$f";
  awk -F'\t' 'NF>=2 && $2=="char-device"{printf "%s(%s) ", $1, $3}' tools/round-50/oracle/$f.nonregular.tsv;
  echo;
done
```

Exit code: `0`. UTC: `2026-10-30T05:03:18Z`.
stdout sha256: `8cb919a0bda50e73cf104b83a12ff92b908f81a70fcb7c5ea5d5121ce923e691`
(stdout saved as `census.txt`, 7 lines, in this seat directory).

Input digests (sha256, committed oracle tables):

```
cb691b4420cb2232eee6018af2776b59376a1116482066fc2d9834f85ed77594  tools/round-50/oracle/c6430.nonregular.tsv
74f171744d1ce28bd3e4cfc85dd07b30a9ba1604d8c4eef6dc8feef4c50b345c  tools/round-50/oracle/c6490.nonregular.tsv
e8706799c39f470903c06596631c5b6dfb9a6ec4866e74bfaa305c26a5c58b92  tools/round-50/oracle/g7581.nonregular.tsv
eff3f15ec9107159f9ba9e6067ebbfd959bc05828d0729f23356f7e0f6ae0306  tools/round-50/oracle/g7582.nonregular.tsv
```

Result (this is the per-class census the round-51 rule is derived from):

| carrier | class | symlink | dir | char-device | total non-regular |
|---|---|---|---|---|---|
| `c6430` | Cable | 568 | 255 | 1 (`dev/led` 247:0) | 824 |
| `c6490` | Cable | 613 | 300 | 1 (`dev/led` 247:0) | 914 |
| `g7581` | FRITZ!Box | 639 | 349 | 13 | 1001 |
| `g7582` | FRITZ!Box | 639 | 349 | 13 | 1001 |

The char-device rows of the FRITZ!Box class: `dev/led` 247:0; `dev/pts/0-7` 136:0-7;
`dev/tiatm` 230:0; `dev/ttyp0-2` 3:0-2. No `fifo`, `socket` or `block-device` row occurs in any of
the four tables (the kinds present are `symlink`, `dir`, `char-device` only). The per-carrier
non-regular totals 824 / 914 / 1001 / 1001 agree with the round-50 entry's Results table
(`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, "Results" table: 1 001 / 1 001 /
914 / 824 non-regular entries).

## R2 — exact old-line capture for the frontier-note patch

Command: `awk 'NR==394||NR==402||…||NR==448 {print …}' PROVINCE.md` plus a Python line-dump of
lines 156, 157, 394, 402-406, 408, 416, 430, 438, 442, 448.

Exit code: `0`. sha256 of the captured file `old-lines.txt`:
`4d79f155a350f265afe3ac23e037f846aeac02b18d5bb10c796154d99cbabf6e`.
The quoted OLD strings in `frontier-note-edits.md` are verbatim from this capture.

## R3 — binding self-check (offline) on the drafted section

Command:

```
python3 -I -B binding-selfcheck.py --province candidate-province.md --json-out binding-selfcheck.json
```

Exit code: `0`. Result: `province_core_section true`, `province_core_row true`,
`frontier_note true`, `all_bindings_true true`.
`candidate-province.md` is `province-r51-section.md` verbatim (the drafted section alone).

The harness `binding-selfcheck.py` is a port of the round-50 counter's three documentation-binding
predicates (`tools/round-50/c1-counter.py:2443-2492`, constants at :375-397 and :426-434) with the
round-51 constants named in `plans/round-51-claims.md` (`core_heading`
`## Round-51 additions to Core`, entry stem `2026-10-30-r51-avm-le-squashfs-core`, `frontier_mark`
`Round-51 frontier note`). It reads a candidate PROVINCE.md text file; it does not run REA.

## R4 — binding mutants (offline)

Seven mutants of the drafted section, each run through the same harness:

| mutant | change | exit | `province_core_section` | `province_core_row` | `frontier_note` |
|---|---|---|---|---|---|
| M1 | Core heading → `## Round-51 measured, not promoted (R51-C1 honest stop)` | 1 | false | false | true |
| M2 | first cell names `squashfs_v4_be` instead of `squashfs_v4_le` | 1 | true | false | true |
| M3 | "AVM-marker" dropped from the first cell only | 0 | true | true | true |
| M4 | row cites the round-50 entry path | 1 | true | false | true |
| M5 | the `Round-51 frontier note` paragraph removed | 1 | true | true | false |
| M6 | frontier note without an LE-AVM token | 1 | true | true | false |
| M7 | every "AVM marker"/"AVM-marker" phrase removed from the row | 1 | true | false | true |

M3 is green because the round-50 predicate searches the AVM-marker in the **whole row** (with the
entry path removed), and the row's second cell independently contains "the AVM marker test exists
only in the BE branch, :48" — the same phrase the round-50 row carries. M7 (the marker absent from
the row entirely) is red, so the binding does discriminate. The drafted row names `AVM-marker` in
its **first cell** as well, so it satisfies the intended reading; the finding for the L1 is that
the round-51 counter should bind the marker to the first cell (as `HANDLER_RE` already is).

## R5 — final artifact digests (seat directory)

```
11b3cea863a0b0fa9133173527b4a0036d80d2fce72d570d3c2cebc8f8ff44d8  province-r51-section.md
a8b98937e6584926001cfeb49cbd8200c408321159813e921cefa3ad90ee7469  binding-selfcheck.py
8cb919a0bda50e73cf104b83a12ff92b908f81a70fcb7c5ea5d5121ce923e691  census.txt
```

The final re-run of the self-check against the shipped `province-r51-section.md` (after the
frontier-note counts were turned into `<<4>>` / `<<0>>` placeholders) exits **0** with
`province_core_section true`, `province_core_row true`, `frontier_note true`
(`binding-selfcheck.json` in this directory).

## R6 — lane read-only inspection commands

All exit `0`; no writes:

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --oneline -3
git -C … log --oneline -12 -- PROVINCE.md
git -C … show 042b8769 -- PROVINCE.md      # round-41 landing shape
git -C … show eb8215ac -- PROVINCE.md      # round-42 landing shape
git -C … show 3847f393 -- PROVINCE.md      # round-49 landing shape
git -C … show b98fd2d0 -- PROVINCE.md      # round-50 falsify corrections (in-place dated bracket)
git -C … ls-tree -r --name-only f04b51dd… corpus/knowledge | grep -c '\.md$'   # -> 140
sha256sum tools/round-50/oracle/*.nonregular.tsv
python3 -c "import json; …" .ufo/waves/round-50/l1/scores/c1-after-attempt2.json
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
```

The round-50 miss receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` reports
`carriers_matched 2`, `target 4`, `met_target false`, `exit_code 1`, `frozen_path_changed []`,
`failing ["g7581:gaps_ok", "g7581:projection_ok", "g7582:gaps_ok"]`, and the bindings
`province_core_section false`, `province_core_row false` — the two Core-promotion bindings were
false precisely because the round-50 landing wrote a *measured-not-promoted* block instead of a
`## Round-50 additions to Core` section. This is the fact the round-51 draft must fix, and the
self-check in R3/R4 is what proves it does.

## R7 — disk guard

`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit `0`;
`/fast/scratch/hyaku/kaidoku-r51` shows 8.6M, idle=0. No heavy pass was run by this seat (no REA,
no image extraction), so no capacity reservation was needed.

## Not run (stated, not claimed)

- **REA / `extract-firmware`**: not run by this seat (the L1 alone runs the data run).
- **The four-carrier data run**: not run; every receipt-dependent cell in the draft is a
  `<<PLACEHOLDER>>`.
- **The round-51 counter itself**: not written by this seat (a different port seat owns
  `tools/round-51/c1-counter.py`); the harness used here is an offline port of the round-50
  binding predicates, in this seat's scratch, offered to the L1 as a cross-check — it is not a
  lane instrument and is not registered.
- **`tools/round-51/gap-rule.json`**: not written by this seat; the census in R1 is the input the
  rule derivation seat needs.
