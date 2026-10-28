# ScoutCraftBlocks measurements

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`. Subject blob `SKILL.md` = `173d93bbd281577488f17ec45311e3c23f3561e7`, sha256 `9bb902a1a1c9f20a31620f4bf8259433ec1fdd4f88ba211394ff9ea44b586f5c`.

No package was installed. Every command below was read-only on the lane except writes under this seat directory and `/fast/scratch/hyaku/kaidoku-r47/ScoutCraftBlocks` (removed after these receipts were copied here).

Findings: `../ScoutCraftBlocks.md` (this file's parent is the seat dir; the Report path is the sibling `ScoutCraftBlocks.md`).

Canonical enumeration is **M5**. M1 is kept because its command-A column is wrong and must not be quoted.

## Ledger

| id | UTC | exit | stdout sha256 | command | result |
|---|---|---:|---|---|---|
| M1 | 2026-10-28T17:52:03Z | 0 | `abe80d5de958a6e56609c0b4d92da6976dcf9c2f63099acc5568b0b031b1b88a` | `python3 -I -B enumerate_craft.py` (first script bytes, sha256 `59909d76892b0260a4d89e620ae193ae93f9540e7de0435762fe6ba2df7883f4`; receipt `stdout-m1.txt`) | **Superseded.** 23 craft blocks, v3 marker count 0, Config custody at line 632. Command A was implemented with `git cat-file -t` and required a blob, so block 22's two `tools/round-45/` trees were reported as command-A failures. That is not `gate.show`. |
| M2 | 2026-10-28T17:53:04Z | 0 | `f7357b0ce5a2696a48084d85fc59811769eed3df4d31806e4e047d8620d2ce6a` (`followup.txt`) | `git -C "$ROOT" rev-parse --show-toplevel`; `rev-parse HEAD`; `status --porcelain -- SKILL.md`; `show "$REV:tools/round-45/"`; `show "$REV:tools/round-45"`; `diff --stat "$REV" HEAD -- SKILL.md`; `log --oneline "$REV"..HEAD -- SKILL.md` | toplevel matched the lane. HEAD at that instant `2e4ae43463aabdae707f8c8a4daa41441ad67a71` (not the freeze; HEAD was moving). `git show` of the directory **exit 0**. Listing sha256 `a83a452ddf3016807bae38b39f924e322bf13c9cef4d46d22ccd59a6c9a39864` (`tree-show.out`, 136 bytes). No-slash variant exit 0, sha256 `99f6a6b2360c9a9ed2c4e92a28010aeee8273e06c34913df3723bcb87ee7f701`. `SKILL.md` status empty. diff stat `13 insertions`. |
| M3 | UTC not captured on the command itself | 0 | `6e65b2543b3a57343cc2032957fa133f008f52eb50f1d6407b49898c73273124` (`skill-diff.txt`) | `git -C "$ROOT" diff -U3 "$REV" HEAD -- SKILL.md` | Insertion of craft block 24 immediately before `## Config custody`, plus two instrument-registry rows outside the craft section. 0 deletions in the stat from M2. Not a freeze measurement. |
| M4 | 2026-10-28T17:54:28Z | 0 | `2145c13cffa535bec01aa2c5e4fda85faf1cb3d3b28029524c14023cf17f1e10` (`grep-freeze.txt`) | `git diff --stat "$REV" HEAD -- tools/round-47/exact.py tools/round-47/record.py plans/round-47-claims.md`; `git grep -n -E '^- \*\*' "$REV" -- SKILL.md`; `git grep -n -E '^## (Queue-drain craft\|Config custody)' "$REV" -- SKILL.md` | `exact.py` not in the diff stat (unchanged at HEAD `1e2c3102952dc636650095643c1963c833859019` then). Craft `- **` lines 86, 108, 118, 137, 151, 162, 170, 175, 187, 196, 207, 219, 233, 240, 256, 279, 293, 316, 351, 387, 457, 547, 612, then SOP bullets 641, 656, 668, 673, 681, 687, 694, 701. Headings: craft line 81, Config custody line 632. |
| M5 | 2026-10-28T17:55:43Z | 0 | `2071bffcb7c913e2fe08162d7a2b62f37aa22ff7bea7b1f6981c9ba43366fc47` (`stdout2.txt`, 234 lines) | `python3 -I -B enumerate_craft.py` script sha256 `13cbbc7e4abbbb5cfea3aa21846bcf649a881fd214ded0c133f03b84cda67d77`; JSON receipt sha256 `3fb84f40e4dc1ef741b3a6a1bbcb76cc3c46f096f443e5ae02b9e6c5648adb1f` (`blocks.json`) | **Canonical.** 23 blocks. Scout citations all resolve (23/23). Command A via `git show` 23/23. v3 marker occurrences in the file: 0. Config custody line 632. Append-before-heading simulation: `block_is_last` true, followers empty. Insert-before-ordinal-23: `block_is_last` false, follower is block 23 only. Citation rows are stdout lines 81–206 (126 citations: 104 in-range selectors, 20 bare blobs, 2 trees). |
| M6 | 2026-10-28T17:56:15Z | 0 | `71686af517479fe869ea65e6fd921c67b064464708725fe05db6b3825cce4524` (`exact-lines.txt`) | `git rev-parse "$REV:tools/round-47/exact.py"`; `git grep -n -F 'exactness-table v3' "$REV" -- SKILL.md`; `git grep -n -F '## Queue-drain craft ' "$REV" -- SKILL.md`; `git show "$REV:tools/round-47/exact.py"` piped to `awk` for lines 101–111 and 188–197 | exact.py blob `fb21a16686633fc3b2d0f6d82910bf9e5eb8b0ac`. Marker grep **exit 1** (no match) — that inner exit is the absence result; the outer script exit is 0. Craft prefix grep exit 0, one line (81). `blocks_of` is the `^- \*\*` split (lines 109–110). `block_is_last` is `blocks[-1] is block` (line 191); the fail string is line 195. Title `startswith("24. ")` is line 196, a different clause. |
| M7 | 2026-10-28T17:56:55Z | 0 | `736c981b2f9a9bfe4f06072199a9496b923ebbb52290fa52d47cab500eb34fc8` (`trail-nl.txt`) | `python3 -I -B` comparing freeze `SKILL.md` block 23 with the worktree file after `rev-parse --show-toplevel` | toplevel exit 0 and equal to the lane. Freeze `git show` exit 0, 299931 bytes. Counts 23 vs 24. Block 23 unequal only by one trailing newline: `work_is_freeze_plus_newline True` (lens 4340 vs 4341). Not a wording change. |

`blocks.json` `freeze.craft_prefix_occurrences` is 1, `intro_markers` is `[]`, `v3_marker_occurrences_file` is 0. That read of the JSON was a follow-on of M6's shell and is not a separate hashed stdout; the same fields are in M5's `blocks.json`.

## Resolver the M5 script applies

Path token, optional `:N` or `:N-M`, prefixes `corpus/`, `plans/`, `tools/`, `.ufo/`, or root `SCORECARD.md` / `LOG.md` / `PROVINCE.md` / `SKILL.md`. Resolves when `git cat-file -t` is `blob` or `tree`; a selector must fall inside a blob's `splitlines()` count. Command-A comparison uses `git show` and defaults a missing selector to line 1, which is why a directory listing of `tools/round-45/` (M2) satisfies command A.

## Not run

`tools/round-47/exact.py --profile v3` against the freeze was not run. The claims file already states the before-cell (`block_present 0`, `rule_blocks 23`). This seat re-derived the block list and the citations; it did not re-score the counter.
