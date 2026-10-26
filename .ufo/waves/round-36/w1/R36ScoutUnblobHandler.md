# R36ScoutUnblobHandler — unblob SquashFS handler at 26.6.4 (round 36, wave 1)

Advisory scout. No lane file other than this report was written. Date of observation: 2026-10-26.

## Verdict

- Installed unblob is **26.6.4** (`~/.local/bin/unblob --version` → `26.6.4`; uv tool, `uv-receipt.toml` requirement `unblob`; `unblob-26.6.4.dist-info`).
- Matching upstream tag **`26.6.4`** → commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` (GitHub API `tags` list and `git/ref/tags/26.6.4`, object type `commit`).
- **Tag source == installed source, byte-identical.** Fetched
  `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
  (HTTP 200) and the installed
  `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`:
  both 590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`; `diff` exit 0, no output.
- Line numbers below are the same in both copies.

## Located facts (file `squashfs.py`, line numbers 1-based)

| fact | lines | observed |
|---|---|---|
| executables | 24-26 | `class SquashFSExtractor(Extractor)`; `EXECUTABLE = "sasquatch"`; `V4BE_EXECUTABLE = "sasquatch-v4be"` |
| endian + branch | 32-55 | `extract` reads endian with `get_endian(file, self.big_endian_magic)`, then `match endian, self.version`: `BIG, 4` → executable `sasquatch-v4be`; `BIG, _` → `-be`; `LITTLE, _` → `-le` |
| v4 BE / AVM | 40-50 | `case Endian.BIG, 4:` switches to `sasquatch-v4be`, parses the LE v4 header struct with `Endian.BIG`; comment cites Freetz `AVM-BE-format.txt`; `is_avm = header.bytes_used == header.mkfs_time` (line 48); `-be` is appended only `if not is_avm` (lines 49-50), so AVM images run `sasquatch-v4be` with no endian flag |
| argv tail | 56-64 | `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` appended after the endian flag; `Command(executable, *commands_args)` at line 65 |
| resulting argv, LE | 36-66 | `sasquatch -le -no-exit-code -f -d <outdir> <inpath>` (this is what K1-K4, all little-endian v4, run) |
| resulting argv, BE v4 non-AVM | 40-66 | `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>` |
| resulting argv, BE v4 AVM | 40-66 | `sasquatch-v4be -no-exit-code -f -d <outdir> <inpath>` |
| handler-level dependencies | 68-69 | `def get_dependencies(self)` → `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]` (both names) |
| v4 LE handler | 454-465 | `SquashFSv4LEHandler`, `NAME = "squashfs_v4_le"`, pattern `68 73 71 73 [24] 04 00`; defines no `EXTRACTOR`, so it inherits line 75 `SquashFSExtractor(3, 0x73_71_73_68)` — its LE magic `hsqs` ≠ big-endian magic, so `get_endian` → LITTLE → `-le` branch |
| v4 BE handler | 513-527 | `SquashFSv4BEHandler(SquashFSv4LEHandler)`, `NAME = "squashfs_v4_be"`, pattern `73 71 73 68 [24] 00 04`, `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` |
| Broadcom v4 | 548-553 | `BIG_ENDIAN_MAGIC = 0x71_73_68_73`; `SquashFSExtractor(4, 0x71_73_68_73)` (also goes down the `BIG, 4` branch when magic matches) |

Companion code (installed copy, not tag-diffed; same package version):

- `unblob/dependencies.py:18-31` — `get_dependencies(handlers, dir_handlers)` unions `handler.get_dependencies()` and checks `shutil.which(command)`; this feeds `--show-external-dependencies`. Observed on this host: `sasquatch ✓`, `sasquatch-v4be ✓` (both in `~/.local/bin`, installed by L1).
- `unblob/extractors/command.py:36-` `Command.extract`: `subprocess.run(...)`; on `FileNotFoundError` it builds `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` where `Command.get_dependencies` (line 101) is `return [self._executable]` — the **one executable actually spawned**, not the handler's two-name list. Non-zero exit → `ExtractCommandFailedReport`. (`-no-exit-code` is why sasquatch returns 0 on partial failures.)

### Consequences for R36-C1 (observation vs inference)

- Observed: committed `K1/before.json` records `extraction_reports[0].dependencies = ["sasquatch"]` and `extraction_gaps[0].kind = "missing-extractor-dependency"`, `dependencies ["sasquatch"]` — consistent with `Command.get_dependencies` returning only the spawned executable, and NOT with the handler-level two-name list.
- [INFERENCE] For all four frozen carriers (LE v4) only `sasquatch` is ever spawned; `sasquatch-v4be` is irrelevant to C1's predicate. The claims' "Not claimed: big-endian / AVM SquashFS" matches the code: only the `BIG, 4` branch needs `sasquatch-v4be`, and that branch is not exercised.
- [INFERENCE] `c1-run.sh` before mode strips every PATH directory holding an executable `sasquatch` (lines 71-72); since `sasquatch-v4be` sits in the same directory (`~/.local/bin`), it is also removed — harmless, as it is never spawned for LE.
- Caveat: `--show-external-dependencies` would list `sasquatch-v4be` as a second missing dependency even though a LE extraction reports only `sasquatch`; do not cite the two-name list as what an extraction gap reports.

## Quote (≤25 words, located)

`"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"` — squashfs.py lines 58-62, tag 26.6.4 = installed (sha256 above).

(Alternative single-line quote, `squashfs.py:69`: `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]`.)

## Draft SOURCES row S108 (11 columns; registry file is `corpus/SOURCES.md`, whose head today is S106 — S107 is not yet present, so S107 must be taken by another row or S108 will leave a gap; L1 to decide)

Capture path below is a suggestion only; the lane must retain a copy at that path for the anchor to resolve (sha256 identifies it independently).

```
| S108 | unblob SquashFS handler, tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | The sasquatch invocation, handler-level dependency list and v4 big-endian/AVM branch of unblob 26.6.4 only; not sasquatch itself, not extraction output, not other unblob handlers | tag `26.6.4` = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`; `python/unblob/handlers/filesystem/squashfs.py` 590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, byte-identical to installed uv-tool copy (diff exit 0); lines 24-26, 32-66, 68-69, 513-527; companion `extractors/command.py:101` | LE v4 runs `sasquatch -le -no-exit-code -f -d OUT IN` and an absent executable is reported as only the spawned name (`sasquatch`); only the BE-v4 branch needs `sasquatch-v4be` and the AVM test is `bytes_used == mkfs_time`; `get_dependencies` lists both names | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Validation of the row (split on ` | `, 11 cells, no stray pipes, `opened` = 2026-10-26, used-by = exactly the entry path): python3 split check on the row printed `11` cells; cells 8-11 = `mined`, `2026-10-26`, `on-release`, `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`.

## Commands and results

1. `curl -sSfL -o $S/tag.py -w '%{http_code}\n' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` → `200`.
2. `sha256sum` of tag copy and installed copy → both `2d7b901b…599287`; `wc -l` 590 / 590; `diff` → exit 0.
3. `curl -sS https://api.github.com/repos/onekey-sec/unblob/git/ref/tags/26.6.4` → object sha `1fcc7a0a584a70a96c31f5a276c20944d199a089`, type `commit`.
4. `~/.local/bin/unblob --show-external-dependencies | grep sasq` → `sasquatch ✓`, `sasquatch-v4be ✓`; `sasquatch -version` → `unsquashfs version 4.5.1 (2022/03/17)`.
5. `grep -n sasquatch` on `corpus/SOURCES.md` neighbours: registry rows S104-S106 are the last; no existing unblob row (`grep -n unblob corpus/SOURCES.md` empty).

## Tooling

No tool installed or upgraded by this seat (RULES.md read; nothing needed). Used curl, diff, sha256sum, python3 (stdlib) only. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScoutUnblobHandler` removed at the end.

## Limits

- Only `squashfs.py` was tag-diffed; `command.py`/`dependencies.py`/`file_utils.py` were read from the installed copy only (same package version, not byte-compared with the tag).
- No extraction was run by this seat; BE/AVM argv above is derived from source, not executed.
