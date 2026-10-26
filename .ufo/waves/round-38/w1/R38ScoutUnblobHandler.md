# R38ScoutUnblobHandler — unblob 26.6.4 squashfs handler (candidate SOURCES row, C1)

Scout only; lane corpus untouched. Copy of fetched file: `.ufo/waves/round-38/w1/artifacts/R38ScoutUnblobHandler/squashfs.py.26.6.4.txt`.

## 1. Brief-URL defect (reported, not repaired)
- `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/unblob/handlers/filesystem/squashfs.py` -> body `404: Not Found` (14 bytes; its sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` is the hash of the 404 text, NOT the handler; fetched 2026-10-26T06:16:41Z).
- `https://github.com/onekey-sec/unblob/tree/26.6.4/unblob/handlers/filesystem` -> HTTP 404.
- At tag 26.6.4 the package sits under `python/`. Real, fetched 200 URLs:
  - raw: `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
  - blob: `https://github.com/onekey-sec/unblob/blob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
  - dir: `https://github.com/onekey-sec/unblob/tree/26.6.4/python/unblob/handlers/filesystem`
- The SOURCES row must use the `python/` path. A row with the brief's path would be a dead URL.

## 2. Access record (candidate row fields)
- Access UTC: 2026-10-26T06:17:04Z (curl -sSL, HTTP 200).
- Tag 26.6.4 = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` (GitHub API `git/ref/tags/26.6.4`, type commit; commit date 2026-06-04T07:39:13Z; release published 2026-06-04T08:52:43Z).
- File: 590 lines, 19842 bytes. sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`. Git blob sha `70fe16974951eabd391995c548b74a052503c8dd` (matches API tree entry; `git hash-object` on the fetched bytes agrees, so the fetched bytes = tag content).
- Companion files fetched same pass (same tag, `python/unblob/`): `file_utils.py` sha256 `87d4dc9a51bc4e92ee410fba77dfcf88fb32266e58e1e6be0ea70bfe44320745`; `extractors/command.py` sha256 `8ae7d2a3980b80b25274d2351a724631be40c79bc8a2da3be14dae2bf09f85af`.
- Dir listing (git tree API, `trees/26.6.4?recursive=1`, truncated=false) of `python/unblob/handlers/filesystem/`: `__init__.py`, `android/{__init__,erofs,sparse}.py`, `btrfs_stream.py`, `cramfs.py`, `extfs.py`, `fat.py`, `iso9660.py`, `jffs2.py`, `minixfs.py`, `ntfs.py`, `romfs.py`, `squashfs.py`, `ubi.py`, `ufs.py`, `yaffs.py`. There is no separate squashfs_v4_be module and no built-in squashfs extractor; `python/unblob/extractors/` holds only `README.md`, `__init__.py`, `command.py`.
- Integration fixtures at tag: `tests/integration/filesystem/squashfs/squashfs_v4_be/__input__/{squashfs_v4.bin,.1kpad.bin,.4kpad.bin,.nopad.bin}` (K3/K4 provenance).

## 3. Dispatch: v4_be vs v4_le (squashfs.py)
Dispatch is by magic pattern, not by endian logic at match time. Each handler has its own `PATTERNS`; the extractor decides endian afterwards.
- L454-466 `SquashFSv4LEHandler` (`NAME = "squashfs_v4_le"`): pattern `68 73 71 73 [24] 04 00` ("hsqs" + version 4 LE at +28).
- L513-525 `SquashFSv4BEHandler(SquashFSv4LEHandler)` (`NAME = "squashfs_v4_be"`): pattern `73 71 73 68 [24] 00 04` ("sqsh" + version 4 BE). Inherits `C_DEFINITIONS`/`HEADER_STRUCT` (`squashfs4_super_block_t`, L468-492) and `calculate_chunk` from `_SquashFSBase` (L77-98; chunk end = bytes_used rounded to 4096/1024 if zero padding follows).
- L527 `SquashFSv4BEHandler.EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` — only v4 handler that passes version 4 with the "sqsh" BE magic.
- `SquashFSv4LEHandler` sets no `EXTRACTOR`; it inherits L75 `_SquashFSBase.EXTRACTOR = SquashFSExtractor(3, 0x73_71_73_68)` (version 3). Harmless: LE magic -> `Endian.LITTLE` -> the `case Endian.LITTLE, _` arm (L53-54), version ignored.
- L548-572 `SquashFSv4BroadcomHandler`: extractor `SquashFSExtractor(4, 0x71_73_68_73)` (L553), two patterns (BE "qshs", LE "shsq").

## 4. External extractors and where invoked
- L24-26 class constants: `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"`.
- L32-66 `SquashFSExtractor.extract`: reads magic via `get_endian` (file_utils.py L350-361: BIG iff 4 magic bytes read big-endian == `big_endian_magic`, else LITTLE), then `match endian, self.version` (L39-54):
  - `Endian.BIG, 4` (L40-50): executable switched to `sasquatch-v4be`; header parsed with `SquashFSv4LEHandler.C_DEFINITIONS` as BIG; `is_avm = header.bytes_used == header.mkfs_time`; `-be` appended only when NOT AVM.
  - `Endian.BIG, _` (L51-52): `-be` with plain `sasquatch`.
  - `Endian.LITTLE, _` (L53-54): `-le` with plain `sasquatch`.
- L56-66 tail args `-no-exit-code -f -d {outdir} {inpath}`; executed as `Command(executable, *commands_args).extract(inpath, outdir)`. `Command.extract` (extractors/command.py L36-85) runs it with `subprocess.run`; non-zero exit -> `ExtractCommandFailedReport`; `FileNotFoundError` -> `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` (command.py L69-77).
- L68-69 `get_dependencies` returns `[EXECUTABLE, V4BE_EXECUTABLE]` = `["sasquatch", "sasquatch-v4be"]` for every squashfs handler (even LE), so a missing-dependency report names both.
- Resulting argv for a standard BE v4 carrier (K1-K4): `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>`. For AVM-BE: same without `-be`.

## 5. Located quotes (each <=25 words; line numbers in the fetched file)
- L25-26: `EXECUTABLE = "sasquatch"` / `V4BE_EXECUTABLE = "sasquatch-v4be"`
- L40-41: `case Endian.BIG, 4:` / `executable = self.V4BE_EXECUTABLE`
- L48-50: `is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm:` / `commands_args.append("-be")`
- L513-514, 522, 527: `class SquashFSv4BEHandler(SquashFSv4LEHandler):` ... `73 71 73 68 [24] 00 04` ... `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)`

## 6. Calibration finding for C1 (report, not repaired) [flag to L1/scribe]
The frozen claim text says the after-receipt is "run with stock unblob 26.6.4; no external extractor dependency" and (L62-65) that "stock unblob handles standard BE v4 ... without any external extractor". The 26.6.4 source shows the opposite wiring: the `squashfs_v4_be` handler always shells out to `sasquatch-v4be` for BE v4 (L40-41, L65-66; standard BE adds `-be`). There is no in-process squashfs reader (section 2). Supported reading: the SOURCES row can back "handler `squashfs_v4_be` is dispatched by magic `sqsh…00 04`" and "extraction invokes `sasquatch-v4be -be`", but it cannot back "no external extractor". Observed host fact: `~/.local/bin/{sasquatch,sasquatch-v4be}` exist (mtime Oct 26 01:22, installed by the L1 per brief), so a measured after-receipt on PATH may have used them. [INFERENCE] The "no external extractor dependency" wording is then true only if it means "no extra install beyond what the harness PATH already has", or if the receipt's run env lacked them and unblob reported something other than extraction via sasquatch; neither is shown by this source. L1 should check the K*/after.json for which binary ran (or for an `ExtractorDependencyNotFoundReport`) before the predicate wording is admitted. REA's own CapabilityInventory text also says "Extraction also requires the selected format's external extractor" (`rea-agents/dist/application/CapabilityInventory.js:323`).

## 7. Candidate SOURCES row (draft for scribe)
- Title: unblob 26.6.4 `python/unblob/handlers/filesystem/squashfs.py` (squashfs v1-v4 handlers + `SquashFSExtractor`)
- URL: https://github.com/onekey-sec/unblob/blob/26.6.4/python/unblob/handlers/filesystem/squashfs.py (raw: raw.githubusercontent.com/.../26.6.4/python/...)
- Opened: 2026-10-26 (fetch 2026-10-26T06:17:04Z); tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089
- Pin: sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287 (590 lines, 19842 B), git blob 70fe169…
- Supports: v4_be/v4_le dispatch by pattern (L454-466, 513-527); sasquatch/-v4be invocation (L24-69); not "no external extractor".

## Tooling / limits
- No installs. Tools used: curl, sha256sum, git hash-object (read-only), python3 stdlib JSON parse. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ScoutUnblobHandler` removed at end. Not exercised: running unblob/sasquatch; K*/after.json contents (not yet landed).
