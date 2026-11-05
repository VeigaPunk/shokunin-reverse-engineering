# ScribeC2Block — R95-C2 draft seat (round 95, wave 1)

Seat: `.ufo/waves/round-95/w1/ScribeC2Block/`
Item: DRAFT the R95-C2 candidate (craft block 34, corpus/QUALITY.md rows 191-192) and
verify the draft in a scratch clone at the frozen declaration commit
`4bda1d1dd3788973f10e61212b70df18b3b14ea0` (base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`).
Lane files were NOT edited: the three drafts and the receipts are candidates for the L1
to integrate, and the L1 re-measures at the landing commit.

## Behavior — three drafts delivered in the seat directory

1. **`block34.md`** — the exact markdown to APPEND as craft rule block 34 at the end of the
   `## Queue-drain craft` section of `SKILL.md` (after block 33's `Refs:` line, before
   `## Config custody for live-probe rounds (SOP)`). One bullet,
   `- **34. A receipt that exits 0 is bound to the world it claims: its label, its own
   counts, the measured tree and the pinned bytes, and it is written through a name no
   planted symlink can occupy.**`, carrying the marker comment
   `<!-- receipt-world-binding v1 -->` on the same line, then a one-paragraph statement of
   the failure class (a receipt, its stdout and its rc that agree with each other while
   none of them is bound to the world they describe) naming the round-94 history with
   pointers into `.ufo/waves/round-94` and `.ufo/waves/round-95`:
   M94-e (the pinned `tools/round-94/c1-receipt-agreement.py` admits a consistently
   rewritten label pair and a wholly fabricated triple; evidence
   `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json`), M94-f (the base
   receipts' short `--rev`, unvalidated; evidence `.ufo/waves/round-94/pre/c1-base-v3-pos.json`),
   and SentinelWrite F1 (the v4 writer's `open(<json-out>.tmp, "w")` follows a planted
   symlink; evidence `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`, `victim_intact
   false`, verdict `followed-symlink`). It then states the three round-95 answers
   (`tools/round-95/c1-agreement-v2.py`, `tools/round-95/stop-boundary-repair-battery-v5.py`,
   `tools/round-95/symlink-probe.py`; evidence
   `.ufo/waves/round-95/l1/scores/c1-symlink-v5-at-4bda1d1d….json`, `victim_intact true`).

   The decision table has the header `| observed failure class | signature | guard | criterion |`,
   the separator `|---|---|---|---|`, and EXACTLY four body rows of four cells each, whose
   first cells are exactly `consistent label rewrite`, `counts that do not recompute the
   label`, `revision field not the measured tree` and `temp-file symlink escape`:

   | first cell | signature | guard | criterion |
   |---|---|---|---|
   | `consistent label rewrite` | a receipt pair whose label is rewritten consistently in both files passes the round-94 agreement counter, because the counter compares the receipt with its stdout and its rc but never with the world (`.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json`: valid 4, agree 4, predicted 4, met true; `.ufo/waves/round-95/forgery/forge-pos.json`) | bind the label to the frozen expect label when met_target is true and recompute it from the receipt's own counts, so a rewritten label is refused with `label-not-frozen` | `QUALITY 191` |
   | `counts that do not recompute the label` | the label claims `repaired 12 of 12` while the receipt's own counts record 10, so the label is consistent with its stdout and its rc but outruns the counts it carries (`.ufo/waves/round-95/forgery/forge-F1.json`) | recompute the label from the receipt's own counts before the receipt may exit 0, so a label that outruns its counts is refused with `label-not-recomputed` | `QUALITY 191` |
   | `revision field not the measured tree` | a short `--rev` is written into the receipt unvalidated, so the receipt names a tree that was never measured (`.ufo/waves/round-94/pre/c1-base-v3-pos.json`, M94-f; `.ufo/waves/round-95/forgery/forge-F2.json`) | bind the receipt revision to the full measured revision resolved by git rev-parse, so a short or wrong revision is refused with `revision-not-bound` | `QUALITY 192` |
   | `temp-file symlink escape` | a planted `<json-out>.tmp` symlink is written through, so the writer's receipt lands on the link's target and the file the writer believes it produced is somewhere else (`.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`: `victim_intact false`, verdict `followed-symlink`) | write through a unique temporary name from mkstemp in the receipt's own directory, so the planted name is never opened and never followed | `QUALITY 192` |

   Each criterion cell cites exactly one `QUALITY N` form (re-derived: `['191']`, `['191']`,
   `['192']`, `['192']`). The block ends with the two-space-indented `  Refs:` line naming
   `corpus/QUALITY.md` rows 191-192 (base `4bda1d1dd3788973f10e61212b70df18b3b14ea0`),
   `tools/round-95/c1-agreement-v2.py`, `tools/round-95/stop-boundary-repair-battery-v5.py`,
   `tools/round-95/symlink-probe.py` and
   `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`.

2. **`quality-rows.md`** — the exact two rows to APPEND at the end of `corpus/QUALITY.md`
   (the base ends at Row 190), each a single-line bullet `- **Row N (short title).** text`:
   Row 191 "(a receipt that exits 0 is bound to the label, the counts, the revision and the
   pins it claims)", Row 192 "(a receipt names the full measured revision and is written
   through a unique temporary name no planted symlink can occupy)". Each row states the rule
   (row 191: when `met_target` is true the label must be bound to the frozen expect label and
   must recompute the label from its own counts, and the same receipt must carry the
   revision of the tree it measured and the sha256 of the pinned counter bytes; row 192: the
   revision recorded is the full measured revision resolved by git rev-parse, and the bytes
   are written through a unique temporary name created with mkstemp in the receipt's own
   directory, so the predictable `<json-out>.tmp` name is never opened and a planted symlink
   standing at it is neither read nor followed), names the round-95 evidence paths, and states
   its own limit before the data. Required phrases present verbatim: `bound to the frozen
   expect label`, `when met_target is true`, `recompute the label from its own counts` (row
   191); `full measured revision`, `git rev-parse`, `unique temporary name`, `planted`
   (row 192). Forbidden phrases absent: `complete JSON or absent` and `helper-only selftest`
   (grep count 0 each).

3. **`verify.md`** — every command with its exit code, its first output lines, the row-shape
   re-derivation, the keyword grep counts, the five-mutation self-attack and the pin check.

   Receipts written by the counters into this seat directory:
   `c2-draft-after.json`, `c2-draft-junk.json`, `c2-draft-depth-v2.json`,
   `c2-draft-depth-v3.json`, `c2-draft-depth-v2-at-rev.json`, `c2-draft-depth-v3-at-rev.json`,
   `c2-draft-before-base.json`.

## Gates (all exercised, none assumed)

Scratch `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r95/ScribeC2Block`; clone
`git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"` checked out
at `4bda1d1dd3788973f10e61212b70df18b3b14ea0`; `git -C "$S/clone" rev-parse --show-toplevel`
= `/fast/scratch/hyaku/kaidoku-r95/ScribeC2Block/clone`. `TMPDIR="$S/tmp"` exported for every
command. cwd = `"$S/clone"` for all counters.

| # | command | exit | first line |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --worktree --work "$S/work" --json-out <seat>/c2-draft-after.json` | **0** | `ok exit 0` |
| 2 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-95/manifests/block34-junk.json --block 34 --worktree --work "$S/work" --json-out <seat>/c2-draft-junk.json` | **1** | `failing exit 1` (three `lacks [...]` lines: `str() fallback`, `complete JSON or absent`, `helper-only selftest`) |
| 3 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root "$S/clone" --worktree --expect-blocks 34 --json-out <seat>/c2-draft-depth-v2.json` | **0** | `blocks 34 resolved 34 expect 34 unresolved 0 met=True exit=0` |
| 4 | `python3 -I -B tools/round-91/depth-blocks-v3.py --root "$S/clone" --worktree --expect-blocks 34 --shape-from 34 --json-out <seat>/c2-draft-depth-v3.json` | **0** | `blocks 34, resolved 34, required-shaped 1/1 expect 34 shaped_required 1/1 unresolved 0 met=True exit=0` |
| 3b | same as 3 with `--rev 51f54f25ebad9c593d97309ce257a4fa3104a074` (the scratch commit of the splice) | **0** | `blocks 34 resolved 34 expect 34 unresolved 0 met=True exit=0` |
| 4b | same as 4 with `--rev 51f54f25ebad9c593d97309ce257a4fa3104a074` | **0** | `blocks 34, resolved 34, required-shaped 1/1 expect 34 shaped_required 1/1 unresolved 0 met=True exit=0` |

The seat spec wrote commands 3 and 4 without `--rev`/`--worktree`; measured, both counters
then print `could-not-evaluate: --rev (or --worktree) is required` and exit **2**. Both were
re-run in the two forms the tools accept (`--worktree` and `--rev`) and both are green. The
`--worktree` form is the one the L1 needs while the draft is unlanded.

Before-side (same clone, base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`):
`craft-citation-semantic.py --block 34` → exit 1, `block 34 missing (craft has 33 blocks)`;
`depth-blocks-v2.py --expect-blocks 34` → exit 1, `blocks 33 resolved 33 expect 34 … met=False`;
`depth-blocks-v3.py --expect-blocks 34 --shape-from 34` → exit 1, `blocks 33, resolved 33,
required-shaped 0/0 … met=False`.

## Self-attack (the gates are load-bearing, not rubber stamps)

Applied to a copy of the clone at `"$S/attack"`, each reverted with `git -C "$S/attack"
checkout -q -- <file>` afterwards. All five killed, exit 1:

| mutation | counter | named failure |
|---|---|---|
| M1 marker comment removed | `craft-citation-semantic.py` (after) | `marker 'receipt-world-binding v1' absent from block 34` |
| M2 QUALITY 191's three keyword phrases deleted | `craft-citation-semantic.py` (after) | `QUALITY 191 lacks ['bound to the frozen expect label', 'when met_target is true']`; `… lacks ['recompute the label from its own counts']` |
| M3 the four-row decision table deleted | `depth-blocks-v3.py --shape-from 34` | `blocks 33 … met=False exit=1` (shape floor) |
| M4 block 34's `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` citation removed | `depth-blocks-v2.py` | `blocks 34 resolved 33 expect 34 unresolved 1 met=False exit=1` (resolve floor) |
| M5 a criterion cell changed to `QUALITY 192 and QUALITY 191` | `craft-citation-semantic.py` (after) | `names 2 QUALITY citations, expected 1` |

Restored control after all reverts: `ok exit 0`.

## Touched surfaces

- Wrote (lane, seat directory only; this seat created no file outside it. The lane's `git status` also lists untracked files from other seats and the L1 that this seat did not create):
  `.ufo/waves/round-95/w1/ScribeC2Block/block34.md`,
  `.ufo/waves/round-95/w1/ScribeC2Block/quality-rows.md`,
  `.ufo/waves/round-95/w1/ScribeC2Block/verify.md`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-after.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-junk.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-depth-v2.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-depth-v3.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-depth-v2-at-rev.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-depth-v3-at-rev.json`,
  `.ufo/waves/round-95/w1/ScribeC2Block/c2-draft-before-base.json`,
  and this report `.ufo/waves/round-95/w1/ScribeC2Block.md`.
- Scratch clone (deleted before yield): `SKILL.md` block 34 spliced, `corpus/QUALITY.md`
  rows 191-192 appended, `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` copied
  from the sibling seat draft `.ufo/waves/round-95/w1/ScribeKnowledge/knowledge.md`; locally
  committed as `51f54f25ebad9c593d97309ce257a4fa3104a074` inside the scratch clone only.
- No lane file was edited, created or deleted outside the seat directory. No `git add`,
  `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push`, `worktree`, `tag` or
  mutating `jj` command was run against the lane. No tool was installed or upgraded
  (nothing in this seat's item needed one), so the operator tooling directive has no entry.
  No host state was mutated.

## Out of scope / not done by this seat

- R95-C1 (the calibration claim) is not this seat's item; it was read only as the source of
  the signatures the block's rows cite. No round-95 counter was re-measured here.
- The landing itself (writing `SKILL.md`, `corpus/QUALITY.md` and the knowledge entry into
  the lane, and the `corpus/lessons/round-95.md` `## Gate` record for S320) is the L1's.
- The knowledge entry `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` was taken
  from the sibling seat's draft for the clone measurement only. The L1 must land a knowledge
  file under that exact name, or block 34's `corpus/knowledge/…` citation will not resolve
  and `depth-blocks-v2.py` / `depth-blocks-v3.py` will report block 34 unresolved (measured:
  mutation M4 above reproduces exactly that failure).

## Findings

- **F1 (draft-content, no action needed).** The seat spec's two depth-counter commands omit
  `--rev`/`--worktree`; measured, both exit 2 with `could-not-evaluate`. The frozen commands
  in `plans/round-95-claims.md` use `--rev <landing>`, so the L1 should run the depth counters
  with `--rev <landing>` after landing and `--worktree` before it.
- **F2 (landing dependency, load-bearing).** Block 34's depth resolution depends on the
  existence of `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` at the landing
  revision. Without it the block is unresolved and both depth counters exit 1. The sibling
  seat `ScribeKnowledge` has the draft; the L1 must land it under that exact filename.
- **F3 (naming, informational).** The knowledge draft's own body names the round-95 craft
  rows as "`corpus/QUALITY.md` row 191 (label bindings) and row 192 (revision and temp-file
  bindings)" and describes the four bindings as `label-not-frozen`, `label-not-recomputed`,
  `revision-not-bound`, `pins-not-bound`. The draft block 34 and rows 191-192 use the same
  names and the same row split, so the two artifacts agree; the `pins-not-bound` binding has
  no row of its own in the four-row table because the frozen manifest pins exactly four row
  snippets, and `pins-not-bound` is stated in row 191's prose and in the knowledge entry
  rather than as a fifth table row.
- **F4 (residual, stated not fixed).** The keyword atom remains a vocabulary check, as the
  round-95 claim itself names (QUALITY 188 residual): M2 shows the counter detects a
  criterion whose phrases were deleted, but a criterion that carries the phrases while
  mis-stating the rule would still pass. The junk-manifest control (exit 1, measured) is what
  rules out a checker that passes everything.
