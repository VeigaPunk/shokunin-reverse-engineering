# CriticC2 — R94-C2 falsification report (lane kaidoku, round 94, wave 1)

Canonical copy: `.ufo/waves/round-94/w1/CriticC2/CriticC2.md` (seat directory). This file is the
prompt-trailer-named copy of the same report.

Seat: CriticC2 (critic). Item: falsify R94-C2 — "craft block 33 is a decision table for the
receipt-path failure class whose criteria (QUALITY 189/190) state the rules their rows assert,
checked by the frozen keyword atoms." All work in a shared scratch clone at the frozen
declaration commit `dd4524916a0332bb65f83525532da1c1b8d709de` plus fixture copies; the lane
was not modified (only seat-directory writes below). Scratch dir deleted before yield.

## Pins re-derived (kill-rule inputs)

`sha256sum` on clone bytes at dd45249:

| file | sha256 | claim pin |
|---|---|---|
| `tools/round-93/craft-citation-semantic.py` | `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340` | match |
| `tools/round-91/depth-blocks-v3.py` | `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f` | match |
| `tools/round-89/depth-blocks-v2.py` | `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f` | match |
| `.ufo/waves/round-94/manifests/block33-after.json` | `9d72f9951d7aadf12a335b2e2177bcb7a7300c5c8c4f481640f9c721751f40ae` | match |

The frozen manifest was used unmodified (passed by its absolute lane path) in every attack.

## Before-state reproduced (do-nothing control)

Clean clone, `git status` porcelain empty, `git rev-parse HEAD` = `dd45249…`:

```
python3 -I -B tools/round-93/craft-citation-semantic.py --root $C --manifest <frozen manifest> --block 33 --worktree   → rc 1, "block 33 missing (craft has 32 blocks)"
python3 -I -B tools/round-91/depth-blocks-v3.py --root $C --worktree --expect-blocks 33 --shape-from 33                → rc 1, "blocks 32, resolved 32 … expect 33 met=False"
python3 -I -B tools/round-89/depth-blocks-v2.py --root $C --worktree --expect-blocks 33                                → rc 1, "blocks 32 resolved 32 expect 33 met=False"
```

Receipts: `receipts/base-{craft,v3,v2}.{json,stdout,stderr}`. Matches the claim's before row and
the committed pre receipts.

## Attack 1 — keyword stuffing: BROKEN (the frozen predicate passes a stuffed fixture); confirms the claim's named limit

Fixture `fx-stuff` (base clone + three edits): block 33 appended before the unique anchor
`## Config custody for live-probe rounds (SOP)` — marker `receipt-path-json-safe v1`, 4-column
decision table, 3 body rows of 4 cells with the exact manifest row snippets, criteria citing
QUALITY 189/189/190; `corpus/QUALITY.md` gains Rows 189/190 that are one-line keyword carriers
stating no rule (`bytes become a length and a sha256 temporary file complete JSON or absent.` /
`through its public command re-read by a JSON parser.`); `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`
(12 lines) added; block 33 cites it `:2-9`.

```
craft-citation-semantic --root fx-stuff --manifest <frozen> --block 33 --worktree → rc 0 "ok"
depth-blocks-v3 --root fx-stuff --worktree --expect-blocks 33 --shape-from 33     → rc 0 "blocks 33, resolved 33, required-shaped 1/1 … met=True"
depth-blocks-v2 --root fx-stuff --worktree --expect-blocks 33                     → rc 0 "blocks 33 resolved 33 expect 33"
```

`receipts/fx-stuff-craft.json` records `checked[*].missing_keywords == [[], [], []]` — every
frozen keyword found in the meaningless rows.

**Verdict: the claim's own named limit is confirmed, not refuted.** The exact residual: the
keyword atom is substring presence of the pinned phrases in the cited row's text; it verifies the
citation's vocabulary, not its truth. A criterion that merely repeats the phrases passes all three
counters. R94-C2 therefore cannot be read as proving "the criteria state the rules their rows
assert" — only that they carry the frozen phrases in the cited rows, which is exactly what the
claim's named limit and QUALITY 188 already concede. No counter regression; the claim text does
not overclaim relative to its limit, but the depth gained is a vocabulary check.

## Attack 2 — prose block: HELD (v3 shape clause fires; v2 false-green re-measured)

Fixture `fx-prose`: block 33 = marker + resolving prose (knowledge `:2-9`, ≥25 words, ≥2
backticked spans), no table, same QUALITY/knowledge fixtures.

```
depth-blocks-v3 --root fx-prose --worktree --expect-blocks 33 --shape-from 33 → rc 1 "blocks 33, resolved 32, required-shaped 0/1 … met=False"
craft-citation-semantic … --block 33 --worktree                               → rc 1 "table shape violated (header 0 cells, body rows 0)" + 3× "row not found: …"
depth-blocks-v2 --root fx-prose --worktree --expect-blocks 33                 → rc 0 met=True
```

The `--shape-from 33` clause kills a fully resolving prose block, as Row 180 requires. `v2`
accepts the prose block — the known shape-blindness (Rows 175/180); v2 is not the shape
authority in the frozen command set, but any depth-only reading of C2 would false-green here.

## Attack 3 — missing manifest row: HELD

Fixture `fx-drop`: the middle body row (`truncated receipt read as a pass`) deleted; the frozen
manifest (unmodified) still names three rows.

```
craft-citation-semantic … → rc 1: "block 33 table shape violated (header 4 cells, body rows 2)", "row not found: 'truncated receipt read as a pass'"
depth-blocks-v3 …          → rc 1 (2 body rows < 3 → required-shaped 0/1)
depth-blocks-v2 …          → rc 0 (no table clause — blind, as attack 2)
```

## Attack 4 — mis-citation to QUALITY 188: HELD by the semantic counter only; both depth counters blind

Fixture `fx-miscite`: row 1's criterion cell `QUALITY 189` → `QUALITY 188` (row exists at base;
contains none of the five phrases — grep-verified, counts 0).

```
craft-citation-semantic … → rc 1: "row 'honest-case receipt crashes': QUALITY 188 lacks ['bytes become a length and a sha256', 'temporary file']"
depth-blocks-v3 …          → rc 0 met=True
depth-blocks-v2 …          → rc 0 met=True
```

The depth counters resolve only `corpus/knowledge/` citations and table shape; a QUALITY
miscite is invisible to them. The mis-citation guard lives solely in
`craft-citation-semantic.py`, which the frozen command set includes — no claim gap, but the
asymmetry means a v2/v3-only measurement would pass the miscite.

## Attack 5 — manifest keywords vs base QUALITY: HELD (manifest not vacuously green at base)

`grep -c` of each frozen phrase in base `corpus/QUALITY.md` at dd45249 — all 0:
`bytes become a length and a sha256` 0, `temporary file` 0, `complete JSON or absent` 0,
`through its public command` 0, `re-read by a JSON parser` 0 (also 0 inside Row 188's text).
The candidate must add text carrying the phrases; the before-state cannot pass the atom.

## Falsification verdict on R94-C2

- **Not killed.** The three frozen commands behave as claimed: a good-faith block 33 passes all
  three (structure, citations, keywords), the base do-nothing fails all three with the declared
  messages, the prose block is killed by the v3 shape clause, a dropped manifest row and a
  miscited criterion fail the semantic counter, and the manifest keywords are absent from base
  QUALITY.
- **The predicate's enforceable content is exactly the vocabulary check the claim names**
  (attack 1): C2 must not be read as proving the criteria state the rules; that residual stays as
  declared (QUALITY 188, round-93 limit). Smallest safe correction: none to the frozen
  declaration — the L1 should score the landed block as a keyword/vocabulary land; any semantic
  strengthening is a new declaration, not R94-C2.

## Files written (all inside the seat directory, plus this trailer-named copy)

- `.ufo/waves/round-94/w1/CriticC2/CriticC2.md` — canonical report.
- `.ufo/waves/round-94/w1/CriticC2.md` — this file.
- `.ufo/waves/round-94/w1/CriticC2/receipts/` — 45 files:
  `{base,fx-stuff,fx-prose,fx-drop,fx-miscite} × {craft,v3,v2} × {json,stdout,stderr}`; all 15
  JSON receipts parse.
- `.ufo/waves/round-94/w1/CriticC2/fixtures/{stuffed-block33.md, stuffed-rows-189-190.md,
  prose-block33.md, knowledge-fixture.md}` — verbatim fixture texts for re-derivation (fx-drop =
  stuffed block minus the middle row line; fx-miscite = stuffed block with row 1's criterion cell
  `189`→`188`).

## Environment

No tools installed (none needed; no pacman transactions). Scratch
`/fast/scratch/hyaku/kaidoku-r94/CriticC2` (shared clone at dd45249 + 4 fixture copies) deleted
before yield. No host state touched; no lane mutations outside the seat paths above.
