# ScribeC2Block — R94-C2 draft seat (round 94, wave 1)

Seat: `.ufo/waves/round-94/w1/ScribeC2Block/`
Item: DRAFT the R94-C2 candidate text (craft block 33, QUALITY rows 189-190), then verify the
draft in a scratch clone at the declaration commit `dd4524916a0332bb65f83525532da1c1b8d709de`.
Lane files were NOT edited. All drafts are candidates for the L1 to integrate; the L1 re-measures
at the landing commit.

## Behavior

Three drafts delivered in the seat directory:

1. **`block33.md`** — the exact markdown to APPEND as craft rule block 33 at the end of the
   `## Queue-drain craft` section of `SKILL.md` (after block 32's Refs line, before
   `## Config custody`). It begins with the bullet `- **33. ...**` and carries the marker comment
   `<!-- receipt-path-json-safe v1 -->` on that same bullet line; follows with a one-paragraph
   statement of the failure class (round-93 M93-e; the honest-case `TypeError: Object of type
   bytes is not JSON serializable` raised by `json.dump` on the bytes in `fresh_cells[*].output`;
   the truncated receipt; and the helper-only selftest that missed the public path); then the
   decision table with header `| observed failure class | signature | guard | criterion |` and a
   separator, with exactly three single-line body rows whose first cells are exactly
   `honest-case receipt crashes`, `truncated receipt read as a pass`, and
   `helper-only selftest misses the public path`; and ends with the required two-space-indented
   `Refs:` line naming `corpus/knowledge/2026-11-05-r94-receipt-path-json.md:1-12`, QUALITY rows
   189-190 at base `dd4524916a0332bb65f83525532da1c1b8d709de`, and the v4/v3 batteries.
   Criterion cells: `QUALITY 189`, `QUALITY 189`, `QUALITY 190` — exactly one `QUALITY N`
   citation per cell. Guard cells state, in the row's own order: serialize every non-JSON value
   to a length and a sha256 before the write; write through a temporary file renamed only after
   the serializer returns; the public command with the receipt flag is the proof of the honest
   case. Signature cells cite the round-93 receipts by path (e.g.
   `.ufo/waves/round-93/l1/scores/c1-pos-json-stderr-at-ca5aa6a2.txt`,
   `.ufo/waves/round-93/l1/scores/c1-F3-json-at-ca5aa6a2.json`,
   `.ufo/waves/round-93/l1/scores/c2-selftest-at-ca5aa6a2.txt`) and the base receipts at
   `.ufo/waves/round-94/pre/c1-base-v3-pos.stderr` and `.ufo/waves/round-94/pre/c1-base-v3-F3.json`.

2. **`quality-189-190.md`** — the exact rows to APPEND at the end of `corpus/QUALITY.md` (base
   ends at Row 188), each a single-line bullet `- **Row N (short title).** statement.`
   Row 189 title "a receipt writer is complete JSON or absent"; Row 190 title "a frozen counter
   is proven only through its public command". Each row states the rule itself (not a pointer),
   cites evidence paths, and no cell or sentence contains a `|`. Required literal phrases all
   present: `bytes become a length and a sha256`, `temporary file`, `complete JSON or absent`
   (Row 189); `through its public command`, `re-read by a JSON parser` (Row 190).

3. **`verify.txt`** — every command with its exit code and last line (details below).

## Gates (all exercised, none assumed)

Scratch `S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r94/ScribeC2Block`; clone
`git clone --shared -q <lane> "$S/clone"` checked out at `dd4524916a0332bb65f83525532da1c1b8d709de`
(`git -C "$S/clone" rev-parse --show-toplevel` = `/fast/scratch/hyaku/kaidoku-r94/ScribeC2Block/clone`).
`TMPDIR="$S/tmp"` exported for every command.

| # | command (cwd = `"$S/clone"`) | exit | last line |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root "$S/clone" --manifest .ufo/waves/round-94/manifests/block33-after.json --block 33 --rev worktree --json-out <seat>/c2-draft-block33.json` | 0 | `ok exit 0` |
| 2 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root "$S/clone" --worktree --expect-blocks 33` | 1 | `blocks 33 resolved 32 expect 33 unresolved 1 met=False exit=1` |
| 3 | `python3 -I -B tools/round-91/depth-blocks-v3.py --root "$S/clone" --worktree --expect-blocks 33 --shape-from 33` | 1 | `blocks 33, resolved 32, required-shaped 1/1 expect 33 shaped_required 1/1 unresolved 0 met=False exit=1` |

Receipts: `<seat>/c2-draft-block33.json` (command 1) — atoms `block_present`/`marker`/`shape`
all true, `checked` shows cited 189 / 189 / 190 with `missing_keywords: []` for all three rows,
`failing: []`, `ok: true`.

**Cause of the two exit-1s, stated exactly:** the only unresolved block is block 33 and its only
problem is `absent:2026-11-05-r94-receipt-path-json.md:absent in worktree:
corpus/knowledge/2026-11-05-r94-receipt-path-json.md` — ScribeKnowledge's knowledge entry was
absent both in the lane and in this clone at run time (`ls` -> "No such file or directory";
`find .ufo/waves/round-94 -name "*r94-receipt-path*"` -> no hit). Blocks 1-32 resolve 32 of 32.
Nothing was copied into the lane to work around it. Command 1 does not read `corpus/knowledge/`
and is therefore unaffected (exit 0).

**Diagnostic isolating that cause** (scratch throwaway `"$S/clone2"`, a copy of the clone plus a
14-line STAND-IN knowledge file — a scratch fixture only, not a lane file, not a candidate
deliverable): command 1 exit 0 (`ok exit 0`), command 2 exit 0 (`blocks 33 resolved 33 expect 33
unresolved 0 met=True exit=0`), command 3 exit 0 (`blocks 33, resolved 33, required-shaped 1/1
expect 33 shaped_required 1/1 unresolved 0 met=True exit=0`). So the block-33 draft is
shape- and citation-correct and turns green on both depth counters as soon as the real knowledge
entry exists at the cited path with >= 12 lines.

**Base control** (scratch clone at base `8a40ceb6516bb38c19c37bcbff2bb3332f31c832`): depth v2
exit 1 (`blocks 32 resolved 32 expect 33 unresolved 0 met=False exit=1`); depth v3 exit 1
(`blocks 32, resolved 32, required-shaped 0/0 expect 33 shaped_required 0/0 unresolved 0
met=False exit=1`) — matching the committed base receipts
`.ufo/waves/round-94/pre/c2-base-depth-v2.txt` and `.ufo/waves/round-94/pre/c2-base-depth-v3.txt`
byte for byte in substance. craft-citation-semantic cannot be run at base from the base clone
because `.ufo/waves/round-94/manifests/block33-after.json` does not exist at the base revision
(FileNotFoundError, exit 1); the committed receipt
`.ufo/waves/round-94/pre/c2-base-block33-after-manifest.json` already records that base run
(exit 1, "block 33 missing (craft has 32 blocks)").

**Pin check** (sha256sum on the clone bytes at the declaration commit): all nine match the pins
in `.ufo/waves/round-94/claims.json` — v4 `c41d54d7…6272`, agreement `dc384a44…36c9`, v3
`60026511…d4e3`, round-92 battery `63e9df43…38bc`, round-92 v2 `f6ddb48b…74`, checker
`34cf6579…5340`, depth v2 `359f15e1…dcf18f`, depth v3 `bcf6c4ea…b052f`, manifest `9d72f995…40ae`.

**Draft shape checks:** `grep -c -- "- **" block33.md` -> 1 (only the block-33 header bullet; no
stray bullet inside the table); `grep -c "^|" block33.md` -> 5 (header + separator + 3 body
rows); `grep -n "|" quality-189-190.md` -> no match (no pipe in either row); all five required
literal phrases present in the right rows.

## Touched surfaces

Written (seat directory only, plus the scratch clone):
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/block33.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/quality-189-190.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/verify.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/ScribeC2Block.md` (this file)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/c2-draft-block33.json` (command-1 receipt)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block.md` (wave-level copy of this
  report, the path named in the seat's `Report:` trailer; the lane convention from round 93 keeps
  both `<Seat>.md` and `<Seat>/<Seat>.md`)

Scratch (deleted before yield): `"/fast/scratch/hyaku/kaidoku-r94/ScribeC2Block"` with `clone`,
`clone2`, `clone-base`, `tmp`, `work`.

In the scratch clone only (`SKILL.md`, `corpus/QUALITY.md` modified) — the lane was not touched:
`git -C "$S/clone" status --porcelain` -> ` M SKILL.md`, ` M corpus/QUALITY.md` (nothing else).

## Out of scope (not done by this seat)

- The knowledge entry `corpus/knowledge/2026-11-05-r94-receipt-path-json.md` is ScribeKnowledge's
  deliverable. This seat did not write it, did not copy it into the lane, and did not edit any
  lane file. Its absence is the sole reason the two depth counters exit 1 in the clone.
- The L1 lands block 33, QUALITY 189-190 and the knowledge entry; the L1 re-measures at the
  landing commit. Nothing here is a landed claim.
- R94-C1 (calibration, the v4 receipt writer) is a different seat's item; this seat only cites
  the v4/v3 tools and their receipts as evidence in the drafts.

## Findings

1. **The block-33 draft clears the semantic counter at the declaration commit** (`craft-citation-semantic.py`
   exit 0, `ok: true`): marker present, table shape satisfied, and all three manifest rows resolve
   their cited QUALITY row with zero missing keywords — the criterion cells carry the frozen
   keyword atoms in the right rows (189 for the two receipt-path rows, 190 for the selftest row).
2. **Both depth counters turn on one artifact this seat does not own.** depth-v2/v3 resolve
   `corpus/knowledge/*.md` citations per block; block 33 cites
   `corpus/knowledge/2026-11-05-r94-receipt-path-json.md:1-12` (as the frozen Refs line
   prescribes), and that file does not exist yet. With a stand-in present, both go green at
   33/33 and 1/1. So the draft's shape, its table, its citation and its criterion cells are all
   correct; only the sibling knowledge entry is missing.
3. **The Refs line is what couples the block to the knowledge entry**, so the depth counters
   cannot be green before ScribeKnowledge lands. The L1 should land the knowledge entry
   (>= 12 lines at that exact path) in the same wave as block 33, or the frozen depth commands
   will report `resolved 32 of 33`.
4. **The base control reproduces the frozen before-state exactly** (32 blocks, expect 33, exit 1
   on both depth counters), so the drafts do not disturb blocks 1-32 and the pre-state is
   unchanged.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/block33.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/quality-189-190.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/verify.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/c2-draft-block33.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ScribeC2Block/ScribeC2Block.md`
