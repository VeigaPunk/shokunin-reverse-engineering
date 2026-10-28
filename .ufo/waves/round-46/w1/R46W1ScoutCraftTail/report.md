# R46W1ScoutCraftTail — SKILL.md tail at the round-46 freeze

Source is the freeze blob, not the worktree. `HEAD` at read time was `8757865679e62dac1f50efb33f583de0be884bf3`, which is not the freeze. Every line number below is from `31820472784284727546808acc31b3ea1e73919b:SKILL.md`.

No lsp device is mounted on this seat. The bullet census is a literal column-zero prefix match (`line.startswith("- **")`) on that blob. These are markdown list items, not symbols.

No tools installed.

## Receipt

| field | value |
|---|---|
| command | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 31820472784284727546808acc31b3ea1e73919b:SKILL.md` |
| exit | 0 |
| stdout sha256 | `36a396ce12f666e1ec1d3449209b866691c927fde377e23bbc4057fda8fe8b1a` |
| git blob | `e0f4823eb1939da827d9f5056682b6b0d39181d4` (mode 100644, 261107 bytes) |
| UTC | 2026-10-28T16:56:11Z |
| line count | 1661 (`splitlines`; file ends with a single newline; last line is not blank) |

## Total lines

1661.

## `## Queue-drain craft ` heading

Line 81, 57 characters, and it does have the trailing space after `craft` that R46-C1's kill rule names:

```
## Queue-drain craft (rounds 5-12, distilled in round 13)
```

Prefix `## Queue-drain craft ` is present; the next character is `(`.

The section runs from line 81 through line 611. The next `## ` heading is line 612.

## Craft rule blocks (the 22 inside the section)

`plans/round-46-claims.md:39` says this section holds 22 rule blocks. The freeze blob matches: 22 lines in `[82, 611]` start with `- **`. None of those 22 is a column-zero `- **` nested inside block 22's body (547–610). A file-wide count is 30; the extra 8 are the Config-custody SOP bullets below line 612 and are not craft rule blocks.

Range = first `- **` line through the last non-blank line before the next `- **` or `## `. First 60 characters are Unicode code points, cut mid-word where the line is longer.

| # | lines | first 60 characters |
|---|---|---|
| 1 | 86–107 | `- **Evidence ids are content-addressed per verb family — nev` |
| 2 | 108–117 | `- **Raw file vaddrs must be pre-shifted +0x100000 into Ghidr` |
| 3 | 118–136 | `- **Refusal families and cost classes.** `VALIDATION_ERROR` ` |
| 4 | 137–150 | `- **Four authority grades — cite a conclusion at the grade i` |
| 5 | 151–161 | `- **Input contracts are shape-gated.** Ledger/coverage verbs` |
| 6 | 162–169 | `- **Module attribution is caller-attested, not proven.** `an` |
| 7 | 170–174 | `- **Tool acceptance ≠ correctness.** `trace-web-source-locat` |
| 8 | 175–186 | `- **Census rows can be defects — check holdings before exerc` |
| 9 | 187–195 | `- **Provisioning hints can be wrong — verify the gate, not t` |
| 10 | 196–206 | `- **Citations into an operator-mutable file anchor by stanza` |
| 11 | 207–217 | `- **Config custody is a pre/post-pair — a zero-drift claim w` |
| 12 | 219–232 | `- **Long Ghidra analyze runs are transient user services, no` |
| 13 | 233–239 | `- **A mitigation claim carries its natural control: same tar` |
| 14 | 240–255 | `- **An artifact that records its own byte-identity must re-d` |
| 15 | 256–278 | `- **A parsed-and-empty result is a statement about the parse` |
| 16 | 279–292 | `- **Co-land every truth dependency.** Before repairing a sta` |
| 17 | 293–314 | `- **Evidence-id field sensitivity is projection-local — meas` |
| 18 | 316–349 | `- **SquashFS `extract-firmware` outcome triage (round 39).**` |
| 19 | 351–385 | `- **SquashFS `extract-firmware` outcome triage v2 (round 40)` |
| 20 | 387–455 | `- **SquashFS `extract-firmware` outcome triage v3 (round 41)` |
| 21 | 457–543 | `- **SquashFS `extract-firmware` outcome triage v4 (round 42)` |
| 22 | 547–610 | `- **22. Freeze integrity is an instrument, and every arm has` |

Only block 22 carries a numeric title prefix (`22. `). Blocks 18–21 are the ones later prose calls rule blocks 18–21; their titles are not numbered.

Blank lines 544–546 sit between block 21 and block 22. Block 11 ends at 217 and block 12 starts at 219 (one blank at 218). Block 17 ends at 314 and block 18 starts at 316 (one blank at 315).

## Last craft block

- Range: **547–610** (content). Line 611 is blank and is not part of the block.
- Start (line 547): `- **22. Freeze integrity is an instrument, and every arm has a red case.** A freeze is`
- Last line (line 610): `  pathspec that must be passed explicitly.`
- Marker inside the block: `<!-- freeze-integrity-table v1 -->` at line 583.
- Next `## ` heading after it: line **612**, `## Config custody for live-probe rounds (SOP)`.

## Where a new craft rule block begins

**Not block 24.** The freeze has 22 craft blocks, the last titled `22. `. `plans/round-46-claims.md:48-50` and `:64-65` require the landed block's title to begin `23. `, marker `<!-- freeze-integrity-table v2 -->` exactly once, and that block to be the **last** craft block. There is no block 23 in the frozen file, so a block 24 has no start line yet. Putting a `24. ` title into the only tail gap would miss the landed-surface clause.

The only insertion slot for the next (last) craft block is between these two neighbours. The new block's first line is inserted here and becomes the new line 612; the heading shifts down.

- Line 611: *(empty)*
- Line 612: `## Config custody for live-probe rounds (SOP)`

After block 23 has landed and is the last craft block, a later block 24 would occupy that same structural gap: after the then-last craft block, immediately before `## Config custody for live-probe rounds (SOP)`. Its line number depends on block 23's length, which is not in the freeze blob. Not computed; not invented.

File-wide reading, recorded so it is not confused with the craft slot: the 24th column-zero `- **` in the whole file already exists at line 636 (`- **Why the shell files are in scope.** `PROVINCE.md:15-26` `). It is inside `## Config custody`, not a new craft block, and not an insertion point. The file-wide last `- **` is line 681 (`- **Commit both receipts tracked.** The pair is the durable `), range 681–684, last line `  not a re-run of the hash.`, next `## ` heading line 686 `## Checklists`.

## Registry sections

| heading | line |
|---|---|
| `### Round-40 instrument registry` | 1620 |
| `### Round-44/45 instrument registry` | 1639 |

Round-40: prose 1622, table header 1624, separator 1625, rows 1626–1637, blank 1638, then the Round-44/45 heading.

Round-44/45 (the last registry section in the file): prose 1641–1648, blank 1649, table header 1650, separator 1651, six data rows 1652–1657, blank 1658. What follows that table, through EOF:

- 1659: `Limit: `c2-counter.py` checks that a row names the path, not that the tool exists at`
- 1660: `` `--rev` (routed R45-CL2). The scope is these six instruments only; rounds 41–43 tools stay ``
- 1661: `unregistered until a round censuses them (R45-CL3).`

No further heading. No `### Round-46` section. The file ends at line 1661.

## Confidence

High on line numbers, prefixes, and the 22-block count: they are a direct read of blob `e0f4823eb1939da827d9f5056682b6b0d39181d4` / raw sha256 `36a396ce…`. High that the next craft title is `23. `, not `24. `: that is `plans/round-46-claims.md:39-50`, which agrees with the frozen block count. Unresolved: the landed length of block 23, so no line number for a subsequent block 24.
