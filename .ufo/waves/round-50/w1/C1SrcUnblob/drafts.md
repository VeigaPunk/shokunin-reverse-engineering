# C1SrcUnblob drafts (wave 1, pre-freeze; L1 reviews and may rewrite)

## D1. Registry row (new; append to `corpus/SOURCES.md` after the last row)

Id: `S151`, not `S150`. `S150` is cited in `corpus/lessons/round-35.md`, `round-36.md`, `round-38.md`, `round-39.md`, `round-40.md`, `round-43.md` and their spot-checks as a refused staged Zenn row that was never registered (`corpus/SOURCES.md` ends at `S149`). Reusing `S150` would make those refusals read as this row. Final id is the L1's call.

```
| S151 | unblob SquashFS v4 little-endian handler at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | The `squashfs_v4_le` class (name, `hsqs` v4 pattern, superblock fields) and its little-endian argv only; not the BE AVM branch (S108, S112), not sasquatch's decoding, not any carrier, not other unblob versions | tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; fetched 2026-10-28T23:31:51Z HTTP 200 19842 B sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287 equal to S108 and the installed uv-tool copy (cmp exit 0); line 25 `EXECUTABLE = "sasquatch"`; lines 53-54 `case Endian.LITTLE, _:` and `commands_args.append("-le")`; line 455 `NAME = "squashfs_v4_le"`; line 463 pattern `68 73 71 73 [24] 04 00`; no EXTRACTOR in the LE class, so line 75 base `SquashFSExtractor(3, 0x73_71_73_68)` applies; the only `is_avm` is line 48, inside `case Endian.BIG, 4:` (line 40) | Name little-endian v4 extraction as `sasquatch -le -no-exit-code -f -d OUT IN` with no AVM-marker test, so an AVM-marker LE member and a standard LE member take one handler and one argv | mined | 2026-10-28 | 180d | corpus/knowledge/<R50-C1 entry stem>.md
```

Cell check: 11 cells, no `|` inside any cell (`corpus/SOURCES.md` schema). The `<R50-C1 entry stem>` placeholder is for the L1 to replace with the real entry path before the freeze.

Why a new row and not S112 or S108:
- **S112** (opened 2026-10-26) teaches only the BE v4 extractor dependency (`case Endian.BIG, 4`, `get_dependencies`). Its scope excludes the LE class. Re-using it for the LE claim changes its `teaches` and scope; the registry is append-only.
- **S108** (same URL and same sha256, opened 2026-10-26) names "the LE/BE argv and the AVM test", but its anchor lines (24-26, 48-50, 58-62, 68-69) do not include the LE class (453-511) or the LE branch (53-54), and its `opened` date is outside the 2026-10-28..29 window the plan's C1 binding requires.

## D2. `## Gate` text for `corpus/lessons/round-50.md` (C1SrcUnblob seat draft)

```
## Gate

Sources opened this round (2026-10-28 UTC). A located quote is an exact line of the fetched Python source (leading indentation removed); no HTML normalisation applies, because the source is not HTML.

| row | source | accessed | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S151 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py (sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, 590 lines) | 2026-10-28T23:31:51Z, HTTP 200, 19,842 B; `SquashFSv4LEHandler` located at lines 454-511 | `NAME = "squashfs_v4_le"` (line 455); `case Endian.LITTLE, _:` (line 53) then `commands_args.append("-le")` (line 54) | **admit** (tier A, `mined`) as a new row, because the LE class lies outside S108 and S112 anchors and both carry 2026-10-26; the LE class has no EXTRACTOR and no AVM test, so it inherits the v3 base extractor and takes the LE branch for every `hsqs` version-4 member |
| S108 | same URL, same bytes | 2026-10-28, sha256 equal | `is_avm = header.bytes_used == header.mkfs_time` (line 48), inside `case Endian.BIG, 4:` (line 40) | re-checked, **kept** `mined`, row unchanged; the AVM test is the BE branch only |
| S112 | same URL, same bytes | 2026-10-28 | `case Endian.BIG, 4:` (line 40) then `executable = self.V4BE_EXECUTABLE` (line 41) | re-checked, **kept** `mined`, row unchanged; not re-used for R50-C1 (BE-only scope, opened 2026-10-26) |

- **Round-50 probe (not a source, not a carrier).** A host-built little-endian v4 xz image (mksquashfs 4.7.5) and a synthetic twin whose `mkfs_time` is set to `bytes_used` were both extracted by unblob 26.6.4: both chunks report handler `squashfs_v4_le`, both run `sasquatch -le -no-exit-code -f -d … …`, and both extracted content trees are equal (receipt `.ufo/waves/round-50/w1/C1SrcUnblob/receipts/`). The probe is evidence that the LE path does not read the marker; it says nothing about vendor images.
- **Negative, stated as located fact.** No line of the LE class or its LE branch tests the AVM marker; the `is_avm` test exists only in the BE branch. Disclosed limit (1) of R50-C1 is therefore a source fact, not an inference.
```

## D3. Control note for the L1 (CTL-C1-3)

On the frozen probe, removing `sasquatch` from the child PATH makes unblob 26.6.4 exit 1 and attaches `ExtractorDependencyNotFoundReport` with `dependencies: ["sasquatch"]` to the chunk's `extraction_reports`. The chunk still reads `handler_name: squashfs_v4_le`. A counter that tests the handler name alone would pass that run. The handler clause must also require `extraction_reports == []` on that chunk and unblob exit 0.
