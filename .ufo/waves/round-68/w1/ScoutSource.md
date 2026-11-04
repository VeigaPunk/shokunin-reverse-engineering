# ScoutSource — r68 w1: the primary source for R68-C2's identity rule

Question assigned: which primary source grounds the identity rule ("a packed executable is restored
by unpacking to its original bytes; packing is reversible and the unpacked file is the original
program, not a reconstruction"), and which candidate must the lane reject.

Deliverables: `ScoutSource/gate.md` (candidate table), `ScoutSource/row.S270.md` (the one registry
row, unlanded), `ScoutSource/fetch/` (nine fetched copies + `SHA256SUMS`). Nothing was appended to
`corpus/SOURCES.md`; nothing tracked was edited.

## Answer

The rule is grounded by **UPX 5.2.0's own manual, format-scoped section** — `doc/upx-doc.txt` at tag
`v5.2.0` (commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`), the section `NOTES FOR LINUX/ELF386`:

> "Packed programs will be byte-identical to the original after uncompression."
> — fetched-bytes lines 441-442, byte offset 18963 (heading line 433; "Linux/elf386 is automatically
> selected for Linux ELF executables." line 439)

- **[observation]** HTTP 200, 37208 bytes, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`;
  a second fetch of the same URL returned the identical sha256. 11 words, contiguous when whitespace
  is flattened (the source wraps before "uncompression").
- **[observation]** The same file documents the switch at lines 74-75 ("All UPX supported file formats
  can be unpacked using the -d switch, eg. `upx -d yourfile.exe` will uncompress the file you've just
  compressed.", byte offset 2707) and bounds the guarantee at lines 101-105: `--exact` requires a
  byte-identical file after `-d` but is "work in progress and is not supported for all formats yet".
- **[observation]** The guarantee is per format, not global: the same sentence appears under
  ATARI/TOS (192), DOS/COM (211), DOS/SYS (253), DJGPP2/COFF (287), LINUX/SH386 (487), LINUX/386
  (530) and PS1/EXE (594); the PS1/EXE one alone adds "until further notice" (line 595). The ELF386
  one carries no qualifier.
- **[observation]** Stability: v5.3.0 (`7c7bea44146c7ad6e17cb2d0bb9566805b44a91a`) carries the same
  sentence at line 484, sha256 `9b980dcab21e1220e9d6e4bb41a36c2b25392891934a998af4fe71cd750d3c35`.
  The pin is v5.2.0 because the installed packer is upx **5.2.0-1** (`pacman -Qo /usr/bin/upx`,
  sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`) — the version the route
  actually runs, not the newest tag.
- **[inference]** "the unpacked file is the original program, not a reconstruction" follows from byte
  identity by definition; the manual never uses "reconstruction". The source grounds *byte equality*,
  which is exactly what the route's `identity_ok` arm measures (unpacked sha256 == carrier pin). The
  `--exact` note makes that an expectation to measure per carrier, not a promise to assume.

## Rejections

- **[observation] a2 — the URL the brief names, https://upx.github.io/upx-doc.html, is gone**: HTTP
  404, 9379 bytes, GitHub Pages `Page not found`, `<title>` at byte offset 254. The project site does
  not serve the manual at all (`upx-doc` 0 occurrences on the front page).
- **[observation] a1 — the front page (https://upx.github.io/, 200, 5056 bytes, sha256 `f07678bd…`)**
  is a landing page: its only related prose is the `safe` bullet, "you can list, test and unpack your
  executables" (offset 3152) and "a checksum of both the compressed and uncompressed file is
  maintained internally" (offset 3221). No `-d`, no `original`, no `byte-identical`. Rejected as a
  rule source, not as a description of the packer.
- **[observation] c — Debian's man page mirror (https://manpages.debian.org/unstable/upx-ucl/upx.1.en.html,
  200, 61251 bytes, sha256 `40e69ca3…`) renders the sentence**, but of `upx-ucl` **4.2.4-2** (page
  header, footer "upx-ucl 4.2.4-2", synopsis "upx 4.2.4"). Quoting it would attribute a 4.2-era
  sentence to the 5.2.0 binary the route runs.
- **[observation] c2 — ManKier (https://www.mankier.com/1/upx, 200, 48794 bytes, sha256 `ba8b23d7…`)**
  renders the same sentence with **no revision pin** (`revision` 0, `commit` 0, `tag ` 0), so the
  quote cannot be tied to 5.2.0 (its text tracks upstream tip, which is 5.3.0's wording).

## The id: S270, and why not S269

- **[observation] Lane tip** `git rev-parse HEAD` = `6ffa9ce1119ec01c953494d8f5b28e419efad646`; highest
  id at that revision (`git show HEAD:corpus/SOURCES.md`) is **S268**. So S269 is free at the tip, as
  the brief assumes.
- **[observation] The working tree is not at the tip for this file.** `corpus/SOURCES.md` is modified
  (` M`), one inserted row, line 186: an **S269** row by a concurrent wave-1 seat covering
  `doc/upx.pod` at `v5.2.0` and quoting the `=head2 NOTES FOR LINUX [general]` passage (pod lines
  459-460, "UPX keeps your original program untouched…"), sha256 `cc93ccea…` — a fetch this seat
  reproduced byte-for-byte. That row is already cited as `S269` by the round-68 entry
  `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` (untracked, line 3).
- **[observation]** The registry census in `CORPUS.md` requires *duplicate ids → must print nothing*.
  Landing a second S269 would be a hard defect, so this row takes **S270** — free at the tip and free
  in the tree.
- **[inference]** S269 and S270 are the same manual family but not the same value: S269's quote is
  the Linux-*general* "keeps your original program untouched" claim, S270's is the *format-scoped*
  linux/elf386 guarantee — the format both R68-C2 carriers are, and the statement the identity arm
  measures. The row's `scope` cell says so, so the pair is auditable. If the L1 wants one row per
  family, fold the ELF386 line into S269's anchor cell and drop S270; no other cell changes.
- **[observation]** The row is 11 columns (13 fields on a `|` split, i.e. the census's `NF==13`), tier
  A, kind `docs`, status `mined`, opened 2026-11-03, recheck 180d, and all three `used-by` paths exist
  in the worktree (`tools/round-68/packed-elf.py`, `plans/round-68-claims.md`,
  `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`).

## Landed under this seat

`ScoutSource/row.S270.md` (the row, one line), `ScoutSource/gate.md` (candidate table), and
`ScoutSource/fetch/`: `upx-github-io.html`, `upx-github-io-upx-doc.html.404`,
`upx-v5.2.0-doc-upx-doc.txt`, `upx-v5.2.0-doc-upx.1`, `upx-v5.2.0-doc-upx.pod`, `upx-v5.2.0-README`,
`upx-v5.3.0-doc-upx-doc.txt`, `reject-debian-upx-ucl-4.2.4-2.html`, `reject-mankier-upx.html`, plus
`SHA256SUMS`. Verify with `sha256sum -c SHA256SUMS` from `ScoutSource/` (the manifest's paths are
`fetch/`-prefixed); every hash there equals the value recorded at fetch time.

Tooling: **nothing installed or upgraded**; `curl`, `git`, `python3` and `pacman -Q*` (read-only) were
sufficient. No pacman transaction was attempted.

## Remaining unknowns

- **[unknown]** Whether `upx.github.io` ever served a rendered manual at `upx-doc.html`; no archive was
  opened, so the 404 is a fact about 2026-11-03 only.
- **[unknown]** Whether a non-UPX packer (or an anti-UPX stub) preserves the identity property; the
  pinned source speaks for UPX only, and the manual's `--exact` note keeps per-format identity a
  measured property.
- **[unknown]** Whether the concurrent S269 row survives landing; if it is reverted, S270 leaves a gap
  at 269 (harmless to the census, which checks duplicates and format, not continuity) and the row can
  be renumbered to S269 by changing one cell.
