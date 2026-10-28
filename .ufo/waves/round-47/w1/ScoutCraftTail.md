# ScoutCraftTail — SKILL.md map at the round-47 freeze

Mapped `SKILL.md` in commit `5017e1f7299c3a812e87e7950148f54313dd279e` (freeze blob), not the worktree. Worktree file is dirty; see drift. No counter CLI was run.

Blob `173d93bbd281577488f17ec45311e3c23f3561e7`. Content sha256 `9bb902a1a1c9f20a31620f4bf8259433ec1fdd4f88ba211394ff9ea44b586f5c`. 299931 bytes, newline-terminated, 1737 lines.

Receipts: `.ufo/waves/round-47/w1/ScoutCraftTail/receipts/`. No tools installed.

## Block 24, as the counter splits it

`tools/round-47/exact.py` at this commit (worktree `exact.py` is not in the diff) splits the craft section on `(?m)^- \*\*` and drops the preamble:

```
30:CRAFT = "## Queue-drain craft "
32:MARKER = "<!-- exactness-table v3 -->"
101:def craft_section(skill):
106:    return skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]
109:def blocks_of(skill):
110:    return re.split(r"(?m)^- \*\*", craft_section(skill))[1:]
191:    receipt.update({"block_is_last": blocks[-1] is block,
194:    if hard and not receipt["block_is_last"]:
196:    if hard and not block.startswith("24. "):
```

The split consumes `- **`, so the source line for block 24 is `- **24. ` plus the title, and it must be the last `^- \*\*` before the next `\n## `. Re-running that split on the freeze blob returns 23 blocks. The last body starts with `23. `. Marker `<!-- exactness-table v3 -->` occurs 0 times.

## Measurement receipts

| measurement | value | exit | utc | stdout sha256 | command |
|---|---|---|---|---|---|
| blob oid | `173d93bbd281577488f17ec45311e3c23f3561e7` | 0 | 2026-10-28T17:50:19Z | `068fb905cae5df30ffa30bcf80180ebd19fa0e31c5598b0d41dcb36eef600237` | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse 5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md` |
| blob size | 299931 | 0 | 2026-10-28T17:50:19Z | `261172bf9f95f1650015b515e95f03dbd9f46eefdcacdfae12610ff69f45265e` | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -s 5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md` |
| line count | 1737 | 0 | 2026-10-28T17:50:19Z | `b80b56085287206d9e50b38891cea9943d6ef81b31af0f2cc547602ef6a7bfc0` | `bash -c 'git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md \| wc -l'` |
| content sha256 | `9bb902a1a1c9f20a31620f4bf8259433ec1fdd4f88ba211394ff9ea44b586f5c` | 0 | 2026-10-28T17:50:19Z | `dbf96d64a1358ff280fa259a834a67ec5fc608de80f41e97e933f2ba2c9591a8` | `bash -c 'git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md \| sha256sum'` |
| craft heading | line 81, one hit | 0 | 2026-10-28T17:50:19Z | `08c4550d66e2f1ddc97b9675f229ff0f6c952ebc5573248c6fa49e89cfc96b22` | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -e '^## Queue-drain craft' 5017e1f7299c3a812e87e7950148f54313dd279e -- SKILL.md` |
| all level-2 headings | next after craft is line 632; Checklists is line 706 | 0 | 2026-10-28T17:50:19Z | `15433fdfd1597fa2c969f3947bf95d39e8d7ce78060e7790369b39dd3dd5d76a` | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -E '^## ' 5017e1f7299c3a812e87e7950148f54313dd279e -- SKILL.md` |
| registry markers | lines 1694 and 1737 only; no exactness-table hit | 0 | 2026-10-28T17:50:19Z | `1f2916e36f9351c433d0b0c5bf42ea621c0924f56ea6ac95b229cb165f528298` | `git grep -n -F` of the two marker strings and `<!-- exactness-table` at the freeze, path `SKILL.md` |
| block map | 31 file-wide dash-bold lines; 23 in the craft section; last craft block 612-631; insert before 632 | 0 | 2026-10-28T17:50:19Z | `808fb075a86173592fcb80aa5d12d8059ffeac9403f790e22fdeaddeefa2336f` | `python3 -I measure_skill.py` (preserved at `receipts/measure_skill.py`; reads `git show` of the freeze blob) |
| exact.py parser lines | 30, 32, 101, 109, 191, 194, 196 | 0 | 2026-10-28T17:51:23Z | `9259aa4200406e474f794953e0ca563fbc6dccaa30963a679897e211aeb76610` | `git show` of freeze `tools/round-47/exact.py` piped to `receipts/parser_lines.py` |
| worktree stat | `SKILL.md` 13 insertions, 0 deletions; `exact.py` absent | 0 | 2026-10-28T17:50:19Z | `5eaed54edac636437740113d75da1d4499c489846d98126c049d7aadaa11a174` | `git diff --stat 5017e1f7299c3a812e87e7950148f54313dd279e -- SKILL.md tools/round-47/exact.py` |
| worktree hunk headers | two hunks; added text not stored | 0 | 2026-10-28T17:51:23Z | `d874b4541481d9d9a86efab207581e4652a05060b80746e8aa969c18f307b8fb` | `git diff -U0` of freeze `SKILL.md`, headers only, via `receipts/hunk_headers.py` |
| full exact.py blob | 23607 bytes | 0 | 2026-10-28T17:50:19Z | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | `git show 5017e1f7299c3a812e87e7950148f54313dd279e:tools/round-47/exact.py` |

Heading grep stdout:

```
5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md:81:## Queue-drain craft (rounds 5-12, distilled in round 13)
```

Registry grep stdout:

```
5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md:1694:<!-- instrument-registry v2 -->
5017e1f7299c3a812e87e7950148f54313dd279e:SKILL.md:1737:<!-- /instrument-registry -->
```

Not run: `python3 -I tools/round-47/exact.py`. Not run: `python3 -I tools/round-47/record.py`.

## Heading, last block, insertion

| item | freeze line | text |
|---|---|---|
| craft heading | 81 | `## Queue-drain craft (rounds 5-12, distilled in round 13)` |
| last craft block | 612-631 inclusive | starts `- **23. Freeze-integrity evidence is only evidence when its ` |
| closing blank of that block | 631 | empty |
| next `## ` heading | 632 | `## Config custody for live-probe rounds (SOP)` |
| following line | 633 | empty |

Insertion point: before line 632, after line 631. Neighbouring lines:

```
631|
632|## Config custody for live-probe rounds (SOP)
```

Line 630 is the last non-empty line of block 23 (the Refs paragraph). A new `^- \*\*` on lines 613-631 would split block 23. The gap that keeps block 23 whole and makes the new block last is between 631 and 632.

The landed source line must be `- **24. …` so the stripped body starts with `24. `.

## Craft-section dash-bold starts (23)

First 60 characters are Python `str` slices from `receipt-measure.stdout`. Inclusive end for blocks 1-22 is next start minus 1 (derived). Block 23 inclusive end is receipt field `LAST_BLOCK_RANGE=612-631`. The receipt's `end=` column for blocks 1-22 is the next block's start, not an inclusive end.

| n | start | inclusive end | first 60 characters |
|---|---|---|---|
| 1 | 86 | 107 | `- **Evidence ids are content-addressed per verb family — nev` |
| 2 | 108 | 117 | `- **Raw file vaddrs must be pre-shifted +0x100000 into Ghidr` |
| 3 | 118 | 136 | `- **Refusal families and cost classes.** `VALIDATION_ERROR` ` |
| 4 | 137 | 150 | `- **Four authority grades — cite a conclusion at the grade i` |
| 5 | 151 | 161 | `- **Input contracts are shape-gated.** Ledger/coverage verbs` |
| 6 | 162 | 169 | `- **Module attribution is caller-attested, not proven.** `an` |
| 7 | 170 | 174 | `- **Tool acceptance ≠ correctness.** `trace-web-source-locat` |
| 8 | 175 | 186 | `- **Census rows can be defects — check holdings before exerc` |
| 9 | 187 | 195 | `- **Provisioning hints can be wrong — verify the gate, not t` |
| 10 | 196 | 206 | `- **Citations into an operator-mutable file anchor by stanza` |
| 11 | 207 | 218 | `- **Config custody is a pre/post-pair — a zero-drift claim w` |
| 12 | 219 | 232 | `- **Long Ghidra analyze runs are transient user services, no` |
| 13 | 233 | 239 | `- **A mitigation claim carries its natural control: same tar` |
| 14 | 240 | 255 | `- **An artifact that records its own byte-identity must re-d` |
| 15 | 256 | 278 | `- **A parsed-and-empty result is a statement about the parse` |
| 16 | 279 | 292 | `- **Co-land every truth dependency.** Before repairing a sta` |
| 17 | 293 | 315 | `- **Evidence-id field sensitivity is projection-local — meas` |
| 18 | 316 | 350 | `- **SquashFS `extract-firmware` outcome triage (round 39).**` |
| 19 | 351 | 386 | `- **SquashFS `extract-firmware` outcome triage v2 (round 40)` |
| 20 | 387 | 456 | `- **SquashFS `extract-firmware` outcome triage v3 (round 41)` |
| 21 | 457 | 546 | `- **SquashFS `extract-firmware` outcome triage v4 (round 42)` |
| 22 | 547 | 611 | `- **22. Freeze integrity is an instrument, and every arm has` |
| 23 | 612 | 631 | `- **23. Freeze-integrity evidence is only evidence when its ` |

Only blocks 22 and 23 have an `N. ` title. Blocks 1-21 still count. Block 24 is the 24th craft-section dash-bold item.

## Dash-bold lines outside the craft section (8)

After line 632, before `## Checklists` at 706. Not counted by `blocks_of`. Not the block-24 insertion point.

| line | first 60 characters |
|---|---|
| 641 | `- **Freeze the pre-pair before the round's first probe — no ` |
| 656 | `- **Why the shell files are in scope.** `PROVINCE.md:15-26` ` |
| 668 | `- **Read-only, always — the pair never edits a config.** The` |
| 673 | `- **Take the post-pair after the last leg exits and every se` |
| 681 | `- **`tail -n3` is not a config selector on a five-hash recei` |
| 687 | `- **Compare same-round only.** The pair brackets this round'` |
| 694 | `- **Drift disposes the claim, not the config.** Content drif` |
| 701 | `- **Commit both receipts tracked.** The pair is the durable ` |

File-wide count 31 = 23 + 8. No dash-bold line after 701.

## Registry markers

| marker | line | text |
|---|---|---|
| open | 1694 | `<!-- instrument-registry v2 -->` |
| close | 1737 | `<!-- /instrument-registry -->` |

`<!-- exactness-table v3 -->` count is 0. Line 1735 contains the substring `instrument-registry` inside the `tools/round-46/registry.py` row. That is not a marker. The measure script records it as `MARK 1735`; the fixed-string grep does not.

## Worktree drift (not used for line numbers)

Stat: `SKILL.md | 13 +++++++++++++`. `exact.py` unchanged, so the parser quote is the freeze bytes.

Hunk headers only:

```
@@ -631,0 +632,11 @@ bullet is bounded by the lines it cites.
@@ -1736,0 +1748,2 @@ each of 0, 1 and 2 to its meaning. `tools/round-46/registry.py` scores it and
```

An uncommitted insertion already sits at the freeze gap after line 631 (11 lines) and near the registry close (2 lines). Those lines were not scored. Freeze line numbers do not apply to the dirty worktree.

## Failed commands (not measurements)

| name | exit | utc | stdout sha256 | note |
|---|---|---|---|---|
| exact-blocks-fn | 1 | 2026-10-28T17:50:19Z | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | SyntaxError from a quoted `python -c`. stderr: `receipt-exact-blocks-fn.stderr`. |
| parser-lines, first try | 2 | 2026-10-28T17:51:23Z | in `receipts.json` only | Bash syntax error. On-disk `receipt-parser-lines.stdout` is the later success (sha `9259aa42…`), which overwrote the failed stdout. |

## Confidence

High on the freeze line map. `wc -l`, `splitlines()`, and the content sha256 agree. High that the block-24 gap is before line 632: that is the `craft_section` boundary, and block 23 already occupies 612-631.

Counter exit codes: not run.
