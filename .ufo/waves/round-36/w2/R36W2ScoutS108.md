# R36W2ScoutS108 — S108 re-open (unblob squashfs.py @ 26.6.4)

Row under test: `corpus/SOURCES.md:114` at lane HEAD 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930. Scratch (own dir under /fast/scratch/hyaku/kaidoku-r36/) removed. No tools installed; no lane writes except this file.

## Per-value verdicts (all AGREE)

| Value in row | My observation | Verdict |
|---|---|---|
| URL `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | `curl` → HTTP 200, 19842 bytes | AGREE |
| tag 26.6.4 = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` | `git ls-remote https://github.com/onekey-sec/unblob.git 'refs/tags/26.6.4*' 'refs/tags/v26.6.4*'` → single line `1fcc7a0a…089 refs/tags/26.6.4` (lightweight tag, no `^{}` peel; no `v26.6.4` tag, which matches the knowledge file's "tag 26.6.4 (not v26.6.4)"). Fetching the same path at the full commit SHA gives the identical sha256. | AGREE |
| 590 lines | `wc -l` = 590; no CR bytes (`grep -c $'\r'` = 0); file ends `)\n` | AGREE |
| sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` | `sha256sum` of tag download = `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (full 64 hex, equal to row, lesson prefix `2d7b901b…599287`, knowledge file) | AGREE |
| byte-identical to installed uv-tool copy | `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`: same sha256, 590 lines, `cmp` identical; `~/.local/bin/unblob --version` → `26.6.4` | AGREE |
| lines 24-26 "EXECUTABLE and V4BE_EXECUTABLE" | 24 `class SquashFSExtractor(Extractor):`, 25 `    EXECUTABLE = "sasquatch"`, 26 `    V4BE_EXECUTABLE = "sasquatch-v4be"` | AGREE |
| lines 48-50 "AVM test" | 48 `is_avm = header.bytes_used == header.mkfs_time`, 49 `if not is_avm:`, 50 `commands_args.append("-be")`. Range covers the test and its consequence; the explanatory comment (AVM-BE-format.txt URL) is line 47, just outside | AGREE (see note 1) |
| lines 58-62 argv tail `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` | 58 `"-no-exit-code",` 59 `"-f",` 60 `"-d",` 61 `"{outdir}",` 62 `"{inpath}",` — exact, in that order, inside `commands_args.extend([...])` (56-64) | AGREE |
| lines 68-69 get_dependencies | 68 `def get_dependencies(self) -> list[str]:`, 69 `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]` | AGREE |

## Downstream claims that cite S108 (spot-checked against the same file)

- Lesson line 28 quote `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` (lines 58-62): exact.
- Knowledge file 144-147: LE command line `-le -no-exit-code -f -d {outdir} {inpath}` = line 54 `-le` (case `Endian.LITTLE, _`) + 58-62; get_dependencies returns both names: confirmed.
- Knowledge file 180-182: BE v4 selects `sasquatch-v4be` (line 41), appends `-be` unless `bytes_used == mkfs_time` (48-50): confirmed.
- Knowledge file 183-184: Broadcom `qshs` magic handlers exist in the same file (`BIG_ENDIAN_MAGIC = 0x71_73_68_73` at 366 and 551; `qshs` in comment at 381): confirmed.
- SCORECARD.md:3396 "S108 lines 40-50" for the BE-v4 path: lines 40-50 are `case Endian.BIG, 4:` through the `-be` append: confirmed.

## Notes (not disagreements)

1. Row's "48-50 AVM test" is slightly loose: only line 48 is the AVM predicate; 49-50 are its branch. The row's scope sentence ("the AVM test only") is fine.
2. The "LE/BE argv" scope claim relies on lines outside the four cited ranges (52, 54: `-be`/`-le` flags; 39-41 executable selection); they exist and are correct (lines 40-41, 51-54 as observed), merely uncited in col 6.
3. Row cites the raw URL; knowledge file line 2 uses the `github.com/.../blob/26.6.4/...` form — different URL, same path/tag; not a conflict.

## Result

No disagreement found on any S108 value (commit, line count, sha256, ranges 24-26, 48-50, 58-62, 68-69, and their content).
