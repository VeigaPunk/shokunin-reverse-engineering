# R38ScribeSOURCES — SOURCES.md append block for the rows opened in round 38

Seat: scribe (leaf, no subagents, no background jobs, advisory only). Assignment: draft the
`corpus/SOURCES.md` append block for the rows opened this round, 11-column fleet schema, and the
7-Zip rejection candidate; do not touch `corpus/SOURCES.md`.

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base
`77091b492cc53f8743bd0701b1e7d5e66123dd84`, freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`.
Inputs read: `plans/round-38-claims.md`, `corpus/lessons/round-37-verifier-spotcheck.md`,
`.ufo/waves/round-38/w1/R38Scout{UnblobHandler,UnblobFixtures,FreetzAvm,SasquatchReadme}.md`,
`corpus/SOURCES.md` (tail and S105-S111), `.ufo/waves/round-38/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}`,
`.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/{7z-refusal.txt,tool-versions.txt,carrier-pins.txt,unsquashfs-refusal.txt}`,
`tools/round-38/c1-counter.py` (row-binding code, lines 218-235), `tools/round-37/gen-squashfs.py`,
read-only `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` (staged ids only).

## 1. ID accounting (collision check)

Observed, not inferred:

| set | content | source |
|---|---|---|
| registered ids | S001-S111 (111 rows); table header at `corpus/SOURCES.md:5-6`, rows 7-117 | `grep -nE '^\| S[0-9]{3,}' corpus/SOURCES.md` |
| staged ids | S106-S237 | `.ufo/waves/round-38/assimilation/staged-ids` (from `merge/kaidoku/SOURCES.append.md`) |
| collisions | S106-S111 (registered **and** staged) | `.ufo/waves/round-38/assimilation/collisions` |
| ids taken by me | S112, S113, S114, S115, S116 | next unused after S111; none present in `reg-ids` |

Consequence stated for the L1: S112-S116 do **not** collide with the registered set, but the staged
merge bundle already uses S112+ for unrelated documents (S112 Apktool, S113 adb, S122 unblob
formats matrix, S183 unblob `SquashFSExtractor`, S192 Freetz `AVM-BE-format.txt`, ...). Under the
renumber-by-document rule this lane already applied twice (S110 note "staged as package S106,
renumbered by document"; S111 "staged as package S107, renumbered by document"), the staged ids are
not binding: the URL/anchor is the identity. The nearest staged neighbours are **different
documents** — staged S183 is `raw.githubusercontent.com/.../main/python/.../squashfs.py` (branch
main, unpinned) and staged S192 is `Freetz/freetz` `AVM-BE-format.txt` (not the Freetz-NG wiki page
of S114) — so no row here duplicates an admitted source; if the merge later lands either, it must
renumber against S108/S112 and S114 respectively.

## 2. Append block (table rows only)

```markdown
| S112 | unblob 26.6.4 `squashfs_v4_be` magic-pattern dispatch — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | The `squashfs_v4_be` and `squashfs_v4_le` magic PATTERNS and the `SquashFSv4BEHandler` EXTRACTOR binding, i.e. the dispatch that routes a standard big-endian v4 image to the BE handler; S108 over the same file already scopes the extractor names, the `-le`/`-be` argv and the AVM test, and this row adds only pattern-level dispatch; the selected handler still shells out to `sasquatch-v4be`, so a pattern match is not evidence of in-process extraction; not unblob traversal, not REA gap wording, not any carrier | tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; 590 lines, sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287, refetched 2026-10-26; line 454 `class SquashFSv4LEHandler`, 455 `NAME = "squashfs_v4_le"`, 463 LE pattern `68 73 71 73 [24] 04 00`, 513 `class SquashFSv4BEHandler(SquashFSv4LEHandler)`, 514 `NAME = "squashfs_v4_be"`, 522 BE pattern `73 71 73 68 [24] 00 04`, 527 `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` | Line 514 'NAME = "squashfs_v4_be"' and line 522 pattern '73 71 73 68 [24] 00 04': the sqsh plus big-endian version 4 magic is what routes a BE v4 image to this handler. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
| S113 | unblob 26.6.4 big-endian SquashFS v4 integration fixtures (`squashfs_v4_be`) — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be | dataset | A | Byte provenance of C1 carriers K3 and K4 only: the `__input__` images at tag 26.6.4, their Git-LFS pointer rule, and the `__output__` apple1..4 files as unblob's own expected output; not the extraction result, not sasquatch behaviour, not any AVM claim | tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; `__input__/squashfs_v4.bin` and `__input__/squashfs_v4.4kpad.bin` are one LFS object, oid sha256 9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0 size 4096, equal to K3 `carrier.bin`; `__input__/squashfs_v4.nopad.bin` oid sha256 a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed size 307, equal to K4 `carrier.bin`; raw.githubusercontent serves the pointer, media.githubusercontent serves the bytes; `.gitattributes` carries `tests/integration/** filter=lfs` | Pointer lines "oid sha256:a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed" and "size 307": a plain git clone yields LFS pointers, so carrier bytes must come from the media path or match the LFS oid. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
| S114 | Freetz-NG wiki, SquashFS 4 (BE) — https://github.com/Freetz-NG/freetz-ng/blob/master/docs/wiki/60_Development/squashfs4-be.en.md | docs | B | The Freetz maintainers AVM-BE format note — big-endian filesystem data, a little-endian block-length field, XZ hardcoded, COMP_OPT unset, mkfs_time equal to bytes_used — plus the registration of the round-37 local copy `.ufo/waves/round-37/probes/avm.txt`; not any carrier, not unblob behaviour, not that the committed BE fixtures are AVM-BE | raw master fetched 2026-10-26T06:17:20Z, 1514 bytes, sha256 100948f38ea0ff7258eee00a420e67b090fd9a1e7e191361d03b9a9604875fc9; last commit touching the path f9157c387a116d6b8d6a8c99e2626c10495ed71f, 2021-02-15; local copy `.ufo/waves/round-37/probes/avm.txt` 1496 bytes sha256 c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5 is the upstream body minus its H1 line | "the only data field stored in the little-endian format is the block length value at the beginning of each block": the plain -be path cannot decode AVM-BE, so the note supports keeping AVM-BE at the frontier, not promoting it. | mined | 2026-10-26 | 365d | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
| S115 | 7-Zip 26.04 supported-format list and the BE-v4 refusal probe — https://www.7-zip.org/ | tool | A | The vendor's own unpacking-format list plus the observed refusal of the installed 7-Zip 26.04 on the four frozen BE v4 carriers; not a SquashFS reader, not an oracle, not evidence about any image content | site fetched 2026-10-26, 6789 bytes, sha256 0676196757aec8d305d14bf97ab4234828ad019c3a0c2fd0431923b361ddcafc, line 111 under "Unpacking only:"; probe 7-Zip 26.04 (x64) 2026-10-05 on K1-K4 exit 2 "Cannot open the file as archive", recorded in `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt` | REJECTED as a BE-v4 oracle: the vendor lists "RPM, SquashFS, UDF, UEFI, VDI, VHD, VHDX, VMDK, XAR and Z." under unpacking yet 7-Zip 26.04 refuses all four frozen BE v4 carriers; flip: a release that opens one BE v4 image and publishes members matching the oracle. | rejected | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
| S116 | kaidoku lane synthetic SquashFS v4 writer — `tools/round-37/gen-squashfs.py` | own-work | A | Provenance of C1 carriers K1 and K2 only: the lane's own deterministic v4 writer that emits the standard big-endian gzip images from the committed source trees; not vendor bytes, not an independent extractor, not an AVM witness | `tools/round-37/gen-squashfs.py`, 216 lines, sha256 1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5, present at base 77091b492cc53f8743bd0701b1e7d5e66123dd84; line 7 MAGIC map, line 173 `mkfs = bytes_used if e == 'avm' else MKFS_TIME`, lines 213-214 the `--endian le/be/avm` and `--comp gzip/xz` axes | Line 7 "MAGIC = {'le': b'hsqs', 'be': b'sqsh', 'avm': b'sqsh'}": K1 and K2 are lane-synthesized standard BE v4 gzip images, so their oracle is the committed source tree, not vendor output. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
```

Artifact: `.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md` (5926 bytes).

Self-checks run on the block as written (each proved by re-parsing my own artifact):

- 11 cells and exactly 12 raw `|` per row (5/5 rows), no literal `|` and no newline inside any cell;
- ids unique in the block and absent from `corpus/SOURCES.md`;
- `status` in {mined, rejected}; `opened` = `2026-10-26` on all five; `recheck` = `on-release` (4) and
  `365d` (1, the Freetz wiki page whose last edit is 2021-02-15);
- `used-by` = exactly `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` on all
  five (the S115 rejected row carries the entry path too, per the seat brief; the gate accepts `—`
  as well);
- every mined row's `teaches` cell carries a located quote of at most 25 words (word counts measured:
  S112 3+6, S113 2+2, S114 20, S115 11, S116 8+9).

## 3. Row decisions and why

| id | document | status | why this row exists | quote anchor |
|---|---|---|---|---|
| S112 | unblob 26.6.4 `python/unblob/handlers/filesystem/squashfs.py`, pattern-level dispatch | mined | the only row the C1 entry can bind to: it is opened 2026-10-26 and its `used-by` lists the entry; its first cell names `squashfs_v4_be` | lines 514, 522 |
| S113 | unblob 26.6.4 `tests/integration/filesystem/squashfs/squashfs_v4_be` | mined | closes the K3/K4 half of R37-CL2 (fixture provenance was committed without a row) | `__input__/squashfs_v4.nopad.bin` LFS pointer |
| S114 | Freetz-NG wiki `60_Development/squashfs4-be.en.md` | mined | closes the `avm.txt` half of R37-CL2; the round-37 local copy is upstream minus its H1 line | "the only data field stored in the little-endian format..." |
| S115 | 7-Zip 26.04 (vendor format list + observed refusal) | rejected | R37-CL3 requires the 7-Zip rejection filed with reason and flip | "RPM, SquashFS, UDF, ... and Z." |
| S116 | `tools/round-37/gen-squashfs.py` | mined | K1/K2 are lane-synthesized bytes; the entry states their provenance and no row covered it | line 7 `MAGIC = ...` |

Scope separation: S112 shares its URL with mined S108 but not its scope — S108 scopes the extractor
names, the `-le`/`-be` argv and the AVM test; S112 scopes the `PATTERNS`/`EXTRACTOR` binding that
performs the dispatch. S112 carries **no** `supersedes` claim because S108 remains accurate (the
census mirror-gate rule tolerates URL reuse across distinct scopes as a W04 warning).

Deliberately **not** written: an `avm` row for `.ufo/waves/round-37/probes/avm.txt` itself, since
S114 registers it as a local copy inside the same source family; and a row for
`onekey-sec/sasquatch` `debian/rules` (see F5).

## 4. Gateway evidence (what I exercised)

| command | observed | exit |
|---|---|---|
| `curl -sSL https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | HTTP 200, 19842 B, 590 lines, sha256 `2d7b901b...5599287` (equals S108's pin) | 0 |
| `grep -n` on that file for `NAME = "squashfs_v4_be"`, `73 71 73 68 [24] 00 04`, `EXTRACTOR = SquashFSExtractor(4`, `case Endian.BIG, 4:`, `executable = self.V4BE_EXECUTABLE`, `is_avm =`, `get_dependencies` | lines 25, 26, 40, 41, 48, 50, 52, 69, 454, 455, 463, 513, 514, 522, 527, 553 | 0 |
| `curl -sSL .../tests/integration/filesystem/squashfs/squashfs_v4_be/__input__/{squashfs_v4.bin,squashfs_v4.nopad.bin,squashfs_v4.4kpad.bin}` | LFS pointers: `squashfs_v4.bin` oid `9c7c523c...69397c0` size 4096; `.nopad.bin` oid `a29ddc15...dfe956ed` size 307; `.4kpad.bin` identical oid to `squashfs_v4.bin` | 0 |
| `sha256sum corpus/evidence/round-37/c1/K{1..4}/carrier.*` (already recorded by R38CrossToolK4, re-read) | K3 `9c7c523c...` = the LFS oid, K4 `a29ddc15...` = the LFS oid | 0 |
| `curl -sSL https://raw.githubusercontent.com/Freetz-NG/freetz-ng/master/docs/wiki/60_Development/squashfs4-be.en.md` | HTTP 200, 1514 B, sha256 `100948f3...604875fc9` | 0 |
| `sha256sum .ufo/waves/round-37/probes/avm.txt`; `diff <(tail -n +2 freetz.md) avm.txt`; `diff avm.txt freetz.md` | `c1c43f6f...672a9a5d5`, 1496 B; body diff empty; the only delta is upstream line 1 `# SquashFS 4 (BE)` | 0 |
| `curl -sSL https://www.7-zip.org/` | HTTP 200, 6789 B, sha256 `06761967...61ddcafc`; line 109 `Unpacking only: ...`, line 111 `RPM, SquashFS, UDF, UEFI, VDI, VHD, VHDX, VMDK, XAR and Z.` | 0 |
| `7z` (no args) | `7-Zip 26.04 (x64) : ... : 2026-10-05` | 1 (usage) |
| `sha256sum tools/round-37/gen-squashfs.py`; `grep -n "MAGIC = \|mkfs = bytes_used\|add_argument('--endian'\|add_argument('--comp'"` | `1c7c5e88...01ba8dd5`, 216 lines; lines 7, 173, 213, 214 | 0 |

Carrier refusals and cross-tool results are **not** re-run by this seat; they are read from
`R38CrossToolK4` artifacts (`7z-refusal.txt` exit 2 on K1-K4, `unsquashfs-refusal.txt` exit 1 on
K1-K4). No REA call, no counter run, no census run, no git mutation.

## 5. Findings (reported, not repaired)

- **F1 — frozen-claim premise contradicted by the pinned source (calibration).** The frozen text
  (`plans/round-38-claims.md`: the P38-C1 parenthetical "run with stock unblob 26.6.4; no external
  extractor dependency" and the "Not claimed" paragraph's "the `squashfs_v4_be` handler publishing
  all oracle files without any external extractor") asserts no external extractor. The registered handler says
  otherwise: `EXECUTABLE = "sasquatch"` / `V4BE_EXECUTABLE = "sasquatch-v4be"` (lines 25-26),
  `case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE` (40-41), and `get_dependencies` returns
  both (69). For a standard BE v4 image the argv is `sasquatch-v4be -be -no-exit-code -f -d ...`.
  An empty `extraction_gaps` therefore cannot be read as "no external extractor was needed"; it is
  reachable only because `~/.local/bin/sasquatch-v4be` is installed (`ls -l ~/.local/bin/sasquatch*`:
  382824 B and 436232 B, mtime Oct 26 01:22, i.e. the S107 deb members).
  The counter cannot see this (it checks `provider.id == unblob`, handler name, gaps, oracle hits),
  so the prose, not the measurement, is the defect. Recommended wording for the entry and Core row:
  "unblob 26.6.4 dispatches its `squashfs_v4_be` handler and extracts through its declared
  `sasquatch-v4be` dependency". Do not repair the frozen predicate; report to the L1/closure.
- **F2 — brief URL defect (already worked around in the registered row).** The handler URL without
  the `python/` segment returns `404: Not Found` (14 B, sha256 `d5558cd4...`), and the `tree/26.6.4`
  directory listing 404s too; at tag 26.6.4 the package root is `python/`. S112 uses the resolving
  `python/` path (as does S108).
- **F3 — assignment path defect.** `.ufo/waves/round-38/probes/avm.txt` does not exist; the
  committed copy R37-CL2 refers to is `.ufo/waves/round-37/probes/avm.txt`
  (sha256 `c1c43f6f...672a9a5d5`). S114 names the round-37 path, and its body was re-verified as
  upstream minus the H1 line.
- **F4 — 7-Zip rejection framing hazard (discernment).** 7-Zip's own page lists SquashFS under
  "Unpacking only" (line 111), so a rejection worded "7-Zip cannot read SquashFS" would be a
  fabricated claim. S115's rejection rests only on the observed refusal of 7-Zip 26.04 on the four
  frozen BE v4 carriers (exit 2, "Cannot open the file as archive"), and its flip names the
  observable that would reverse it.
- **F5 — inadmissible candidate left out.** `onekey-sec/sasquatch` `debian/rules` (the
  `CFLAGS=-DFIX_BE` second build that produces `sasquatch-v4be`) was read by R38ScoutSasquatchReadme
  from branch `main` with no commit pinned. It is therefore not a registerable row (no pin, no
  digest). Flip: fetch the file at tag `sasquatch-v4.5.1-6`, record sha256 and line anchor, then add
  the row; until then the `-be`/`-le` flags' only located statement is the installed binary's own
  `-help` output, which is own observation, not a registered source.
- **F6 — used-by asymmetry the L1 must decide.** S107 (sasquatch release) and S110 (unblob README)
  are already mined with `used-by` = `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`.
  The r38 entry may cite them, but their `used-by` will not list it and they therefore cannot
  satisfy `c1-counter.py`'s binding (opened 2026-10-26 **and** entry in `used-by`). Only S112 does.
  If the L1 wants a two-sided used-by for S107/S110, the lane's own convention is a supersession row,
  not an in-place edit of a mined row.
- **F7 — carrier note precision.** `corpus/evidence/round-37/c1/carriers.json` calls K3 "(4kpad)";
  upstream, `squashfs_v4.4kpad.bin` and `squashfs_v4.bin` are one LFS object (same oid and size), so
  both names are correct but the entry should say "`squashfs_v4.bin` (identical to `.4kpad.bin`)".
- **F8 — oracle independence, flagged.** K3/K4's oracle is unblob's own `__output__` apples, i.e.
  the same project as the handler under test; it is independent of the REA run but not of unblob.
  `[INFERENCE]` how those `__output__` files were produced is not stated in the tree
  (unblob/sasquatch at fixture creation, most plausibly). The independent leg is the
  `sasquatch-v4be -be` cross-tool comparison in `R38CrossToolK4`, and the entry should say so.

## 6. Limits

- No counter (`c1-counter.py`) or census (`sources-census.sh`) run by this seat: both need the rows
  landed and belong to the L1 and to `R38ExecMirrorGate`/critic seats. The structural checks in §2
  are re-parsing of my own artifact, not a gate verdict.
- No write to `corpus/SOURCES.md` or any other lane file outside the two paths below; no VCS
  mutation; no REA call; no install or upgrade (tools used: curl, sha256sum, diff, grep/awk,
  python3 stdlib, the installed `7z` version string only).
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ScribeSOURCES` removed at end; nothing cited here
  lives under `/tmp` or scratch.
- `git status --porcelain` at the end of this seat showed ` M tools/round-38/c1-counter.py` plus the
  round-38 untracked trees; that modification is another seat's, not this one's (this seat wrote only
  the two files in §7).

## 7. Touched surfaces

- `.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md` (new, 5926 B)
- `.ufo/waves/round-38/w1/R38ScribeSOURCES.md` (this report)
- peer messages: `R38ExecMirrorGate` (x2), `R38ScribeEntry`, `R38ScribeLessonSkeleton`

Out of scope and untouched: `corpus/evidence/round-38/**`, `corpus/knowledge`, `PROVINCE.md`,
`corpus/README.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/lessons`, counters, carriers,
oracles, controls, `/home/vgpnk/Projects/shokuknow` (read-only; only `SOURCES.append.md` ids were
grepped).
