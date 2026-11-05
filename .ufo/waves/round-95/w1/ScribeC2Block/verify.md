# ScribeC2Block — verification receipts (R95-C2 draft)

Scratch: `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r95/ScribeC2Block`
(`/fast/scratch/hyaku/kaidoku-r95/ScribeC2Block`).
Clone: `git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"`
then `git -C "$S/clone" checkout -q 4bda1d1dd3788973f10e61212b70df18b3b14ea0`.
`git -C "$S/clone" rev-parse --show-toplevel` = `/fast/scratch/hyaku/kaidoku-r95/ScribeC2Block/clone`
(verified before the scratch commit). `TMPDIR="$S/tmp"` exported for every command.
All counters run with cwd = `"$S/clone"`.

The clone received exactly three edits (all inside the scratch clone; no lane file was
touched): `SKILL.md` (block 34 spliced after block 33's `Refs:` line, before
`## Config custody for live-probe rounds (SOP)`), `corpus/QUALITY.md` (rows 191-192
appended after row 190), and a new `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`
copied from the sibling seat draft `.ufo/waves/round-95/w1/ScribeKnowledge/knowledge.md`
(the depth counters resolve block 34's `corpus/knowledge/...` citation, so the file must
exist for the draft to be measurable). The clone was then committed locally as
`51f54f25ebad9c593d97309ce257a4fa3104a074` (scratch only; nothing was pushed and no lane
ref moved) so the same draft could be measured both `--worktree` and `--rev`.

The spliced block 34 is byte-identical to the seat file `block34.md`
(verified by re-extracting the block from the spliced `SKILL.md` and comparing).

## Frozen counting commands (after)

| # | command | exit | first line of output |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --worktree --work "$S/work" --json-out <seat>/c2-draft-after.json` | 0 | `ok exit 0` |
| 2 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-95/manifests/block34-junk.json --block 34 --worktree --work "$S/work" --json-out <seat>/c2-draft-junk.json` | 1 | `failing exit 1` then `  - row 'consistent label rewrite': QUALITY 191 lacks ['str() fallback']`, `  - row 'revision field not the measured tree': QUALITY 192 lacks ['complete JSON or absent']`, `  - row 'temp-file symlink escape': QUALITY 192 lacks ['helper-only selftest']` |
| 3 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root "$S/clone" --worktree --expect-blocks 34 --json-out <seat>/c2-draft-depth-v2.json` | 0 | `blocks 34 resolved 34 expect 34 unresolved 0 met=True exit=0` |
| 4 | `python3 -I -B tools/round-91/depth-blocks-v3.py --root "$S/clone" --worktree --expect-blocks 34 --shape-from 34 --json-out <seat>/c2-draft-depth-v3.json` | 0 | `blocks 34, resolved 34, required-shaped 1/1 expect 34 shaped_required 1/1 unresolved 0 met=True exit=0` |
| 3b | `python3 -I -B tools/round-89/depth-blocks-v2.py --root "$S/clone" --rev 51f54f25ebad9c593d97309ce257a4fa3104a074 --expect-blocks 34 --json-out <seat>/c2-draft-depth-v2-at-rev.json` | 0 | `blocks 34 resolved 34 expect 34 unresolved 0 met=True exit=0` |
| 4b | `python3 -I -B tools/round-91/depth-blocks-v3.py --root "$S/clone" --rev 51f54f25ebad9c593d97309ce257a4fa3104a074 --expect-blocks 34 --shape-from 34 --json-out <seat>/c2-draft-depth-v3-at-rev.json` | 0 | `blocks 34, resolved 34, required-shaped 1/1 expect 34 shaped_required 1/1 unresolved 0 met=True exit=0` |

The seat spec wrote commands 3 and 4 without `--rev`/`--worktree`; the counters then print
`could-not-evaluate: --rev (or --worktree) is required` and exit 2 (measured, both
counters). Both forms were re-run with `--worktree` (reading the spliced clone worktree)
and with `--rev 51f54f25…` (reading the scratch commit); both agree with the table above.
`--worktree` is the form the L1 will need while the draft is unlanded; the `--rev` form
is the frozen form.

## Before (do-nothing control), same clone, base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`

| command | exit | first line of output |
|---|---|---|
| `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --json-out <seat>/c2-draft-before-base.json` | 1 | `failing exit 1` then `  - block 34 missing (craft has 33 blocks)` |
| `python3 -I -B tools/round-89/depth-blocks-v2.py --root "$S/clone" --rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --expect-blocks 34` | 1 | `blocks 33 resolved 33 expect 34 unresolved 0 met=False exit=1` |
| `python3 -I -B tools/round-91/depth-blocks-v3.py --root "$S/clone" --rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --expect-blocks 34 --shape-from 34` | 1 | `blocks 33, resolved 33, required-shaped 0/0 expect 34 shaped_required 0/0 unresolved 0 met=False exit=1` |

The before-side is met: block 34 is absent at base and the craft section carries 33 blocks.

## Row shape (re-derived from the spliced `SKILL.md`)

Header `| observed failure class | signature | guard | criterion |` (4 cells), separator
`|---|---|---|---|`, exactly four body rows, each with exactly four cells and exactly one
`QUALITY N` form in its criterion cell:

| first cell | criterion cell | QUALITY citations in that cell |
|---|---|---|
| `consistent label rewrite` | `QUALITY 191` | `['191']` |
| `counts that do not recompute the label` | `QUALITY 191` | `['191']` |
| `revision field not the measured tree` | `QUALITY 192` | `['192']` |
| `temp-file symlink escape` | `QUALITY 192` | `['192']` |

Marker `receipt-world-binding v1` present in block 34 (the semantic counter's
`atoms.marker` is `true`; see `c2-draft-after.json`).

## Keyword atoms (draft `quality-rows.md`)

Present verbatim (grep counts over the seat file):
`bound to the frozen expect label` 1, `when met_target is true` 1,
`recompute the label from its own counts` 1, `full measured revision` 1,
`git rev-parse` 1, `unique temporary name` 1, `planted` 1.
Absent (as required): `complete JSON or absent` 0, `helper-only selftest` 0.

## Self-attack (the gates are load-bearing, not rubber stamps)

Each mutation was applied to a copy of the clone at `"$S/attack"` and reverted with
`git -C "$S/attack" checkout -q -- <file>` afterwards.

| mutation | counter | exit | output |
|---|---|---|---|
| M1 marker comment removed from block 34 | `craft-citation-semantic.py` (after-manifest) | 1 | `marker 'receipt-world-binding v1' absent from block 34` |
| M2 the three QUALITY 191 keyword phrases deleted from row 191 | `craft-citation-semantic.py` (after-manifest) | 1 | `QUALITY 191 lacks ['bound to the frozen expect label', 'when met_target is true']`; `QUALITY 191 lacks ['recompute the label from its own counts']` |
| M3 the four-row decision table deleted from block 34 | `depth-blocks-v3.py --shape-from 34` | 1 | `blocks 33, resolved 33, required-shaped 0/0 expect 34 shaped_required 0/0 unresolved 0 met=False exit=1` |
| M4 block 34's `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` citation removed | `depth-blocks-v2.py` | 1 | `blocks 34 resolved 33 expect 34 unresolved 1 met=False exit=1` |
| M5 a criterion cell changed to `QUALITY 192 and QUALITY 191` | `craft-citation-semantic.py` (after-manifest) | 1 | `row 'temp-file symlink escape': criterion cell 'QUALITY 192 and QUALITY 191' names 2 QUALITY citations, expected 1` |

Restored control after all five reverts: `ok exit 0`.

## Pin check (read-only, lane)

`sha256sum` over the pinned paths at the declaration commit matched
`.ufo/waves/round-95/pins.sha256` for every pin this seat depends on:
`tools/round-93/craft-citation-semantic.py` `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`,
`tools/round-89/depth-blocks-v2.py` `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`,
`tools/round-91/depth-blocks-v3.py` `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f`,
`.ufo/waves/round-95/manifests/block34-after.json` `cf5f265f7500d1315f7b141332fff1dd9c60c74f189c53bdad1b1ac91fd03ba8`,
`.ufo/waves/round-95/manifests/block34-junk.json` `abcf7bda5c38eb54791a46d642c71a90a63a657ff374a380dbd853a74db5a321`.
The manifests were read, never edited.
