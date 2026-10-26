# R42SrcUnblob — report (round 42, wave 1, pre-freeze sources)

**Verdict: DONE** — all three documents opened live (HTTP 200, digests recorded); S112 anchor extensions and a validated 11-column S130 row delivered; two draft-premise defects found in the fixture set.

Seat: sources scribe, leaf. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`. No tool installed or upgraded. No VCS mutation. No REA, unblob, sasquatch or reader was run on any published C1 candidate; every unblob run below used unblob's own MIT fixtures (development inputs for C2).

## 1. Files opened (live, this round)

| id | document | HTTP | bytes | sha256 | opened (UTC) |
|---|---|---|---|---|---|
| D1 | `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | 200 | 19842 | `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` | 2026-10-26T21:50:35Z (recheck 21:51:10Z, same digest) |
| D2 | `api.github.com/repos/onekey-sec/unblob/git/trees/1fcc7a0a584a70a96c31f5a276c20944d199a089?recursive=1` | 200 | 1522052 | `adb692a25b66718f9ed1dc237d87d72b4b6440a9a2f2ddbbb49e925df38b3ef2` | 2026-10-26T21:50:43Z |
| D3 | `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE` | 200 | 1068 | `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e` | 2026-10-26T21:50:35Z (recheck 21:51:10Z, same digest) |
| D4 | `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/.gitattributes` | 200 | 158 | `df86e28e5e3b04895438ccba79200a462d2e67daefd9042b5477d42b5b2ccede` | between 21:50:43Z and 21:51:10Z (recheck 21:51:10Z, 200, 158 B) |
| D5 | 58 LFS pointer blobs under `tests/integration/filesystem/squashfs/**/__input__/` | 200 each | 128-129 each | per-file, `fixtures-58.tsv` column `pointer_sha256` | 21:51:15Z-21:51:32Z |
| D6 | the same 58 paths via `media.githubusercontent.com/media/...` | 200 each | 307-4096 each, 161486 total | per-file `actual_sha256`; all 58 equal the pointer's LFS `oid` | 21:51:37Z-21:51:42Z |

D2 reported `"truncated": false`, so the 380 entries under the SquashFS fixture subtree are complete. The installed unblob 26.6.4 copy at `/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` hashes to the same `2d7b901b...`, so D1 is the code that runs locally.

## 2. D1 — new anchors for S112 (no new SOURCES row)

S112's present anchor covers `SquashFSExtractor` lines 24-70 and the v4-BE dependency; the v1-v3 handler lines below are the new anchors to append to S112's `anchor` cell (the document stays one source). Quotes are verbatim, each well under 25 words.

**Extractor (S112's existing ground, re-read for the record)**

- `:24` `class SquashFSExtractor(Extractor):`; `:25` `EXECUTABLE = "sasquatch"`; `:26` `V4BE_EXECUTABLE = "sasquatch-v4be"`.
- `:32` `def extract(self, inpath: Path, outdir: Path):`; `:34` `endian = get_endian(file, self.big_endian_magic)`.
- `:39-41` `match endian, self.version:` / `case Endian.BIG, 4:` / `executable = self.V4BE_EXECUTABLE` — the only place the v4 binary is selected.
- `:48-50` `is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm:` / `commands_args.append("-be")` — a BE v4 AVM image gets no `-be`.
- `:51-52` `case Endian.BIG, _:` / `commands_args.append("-be")`; `:53-54` `case Endian.LITTLE, _:` / `commands_args.append("-le")`.
- `:56-64` argv tail `-no-exit-code`, `-f`, `-d {outdir}`, `{inpath}`.
- `:68-69` `def get_dependencies(self) -> list[str]:` / `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]`.

**Handler family (new anchors)**

- `:73` `BIG_ENDIAN_MAGIC = 0x73_71_73_68`; `:75` `EXTRACTOR = SquashFSExtractor(3, 0x73_71_73_68)` — v1 and v2 handlers inherit a **version-3** extractor.
- v1 `:101-102` `class SquashFSv1Handler(_SquashFSBase):` / `NAME = "squashfs_v1"`; patterns `:110` `73 71 73 68 [24] 00 01`, `:118` `68 73 71 73 [24] 01 00`.
- v2 `:158-159` `class SquashFSv2Handler(SquashFSv1Handler):` / `NAME = "squashfs_v2"`; patterns `:167`, `:175` (`...[24] 00 02` / `...[24] 02 00`).
- v2 nonstandard `:199-200` `NAME = "squashfs_v2_nonstandard"`; `:204` `EXTRACTOR = SquashFSExtractor(2, 0x73_71_6C_7A)`.
- v3 `:244-245` `class SquashFSv3Handler(_SquashFSBase):` / `NAME = "squashfs_v3"`; patterns `:253` `73 71 73 68 [24] 00 03`, `:261` `68 73 71 73 [24] 03 00`; superblock `:284-315` `squashfs3_super_block_t` (both `bytes_used_2` and a trailing `uint64 bytes_used`).
- v3 DD-WRT `:318-319` `NAME = "squashfs_v3_ddwrt"`; `:321` `BIG_ENDIAN_MAGIC = 0x74_71_73_68`; `:323` `EXTRACTOR = SquashFSExtractor(3, 0x74_71_73_68)`; patterns `:331` `68 73 71 74 [24] 03 00`, `:339` `74 71 73 68 [24] 00 03`.
- v3 Broadcom `:363-364` `NAME = "squashfs_v3_broadcom"`; `:366` `BIG_ENDIAN_MAGIC = 0x71_73_68_73`; `:368` `EXTRACTOR = SquashFSExtractor(3, 0x71_73_68_73)`; patterns `:376` `73 68 73 71 [24] 03 00`, `:384` `71 73 68 73 [24] 00 03`.
- v3 nonstandard `:409-410` `NAME = "squashfs_v3_nonstandard"`; `:412` `BIG_ENDIAN_MAGIC = 0x73_71_6C_7A`; `:414` `EXTRACTOR = SquashFSExtractor(3, 0x73_71_6C_7A)`; patterns `:422` `7A 6c 71 73 [24] 03 00`, `:430` `73 71 6c 7A [24] 00 03`.

Structural reading of the pattern form (`magic`, 24-byte gap, two bytes): major/minor sit at offsets 28 and 30 in all four families, and **only the magic tokens differ**; a 24-byte gap of zeros carries no discriminator. Suggested scope wording for S112 if the L1 widens it: "SquashFS extractor selection/argv and the v1-v3 handler NAME/PATTERNS/EXTRACTOR lines at tag 26.6.4".

## 3. Live confirmation of the C1 extractor premise (development inputs only)

Running the installed unblob 26.6.4 CLI on its own v3/v2 fixtures, the `Running extract command` lines unblob logged (cwd = scratch, `unblob.log`):

```
v3 LE (squashfs_v3.le.nopad.bin) rc=0  sasquatch -le -no-exit-code -f -d <out>/..._extract <in>
v3 BE (squashfs_v3.be.nopad.bin) rc=0  sasquatch -be -no-exit-code -f -d <out>/..._extract <in>
v2 LE (squashfs_v2.0_le.bin)     rc=0  sasquatch -le -no-exit-code -f -d <out>/..._extract <in>
```

`-le`/`-be` is the argument form; `sasquatch-v4be` was never invoked; each run extracted its member set (apple1-4). This confirms the C1 wording "extractor `sasquatch -be|-le`, never sasquatch-v4be" **at unblob level**; it does not confirm the REA envelope, which is the draft's own open item.

## 4. D2 — fixture tree, inventory, and the S130 row

- 11 fixture directories (v1, v2, v2_nonstandard, v3, v3_adaptive, v3_broadcom, v3_ddwrt, v3_nonstandard, v4_be, v4_broadcom, v4_le), 58 `__input__` blobs, 380 entries in total; no README/COPYING inside the subtree (licence text lives only at the repo root, D3).
- LFS mechanics: the raw URL serves a 128-129 B pointer (`version https://git-lfs.github.com/spec/v1` / `oid sha256:...` / `size ...`); the `media.githubusercontent.com/media/...` URL serves the payload. All 58 payload sha256 values equal their declared oids, so `oid` is a sound pin.
- Payload sizes 307-4096 B; total 161486 B. Version tuples from the superblock: v1 1.0 (2 files), v2 2.0 (2) and 2.1 (2), v2_nonstandard 2.0 (2) and 2.1 (2), **v3 3.0 (9) and 3.1 (24)**, v4 4.0 (15).
- **Three payloads are byte-identical duplicates**: `squashfs_v3/big_endian/squashfs_v3_be.bin` = `squashfs_v3_broadcom/big_endian/squashfs_v3_be.bin` (oid `4e9493d9...`); `squashfs_v3/little_endian/squashfs_v3_le.bin` = `squashfs_v3_ddwrt/little_endian/squashfs_v3_le.bin` (oid `0161351c...`); `squashfs_v4_be/squashfs_v4.4kpad.bin` = `squashfs_v4_be/squashfs_v4.bin` (oid `9c7c523c...`).
- **Two fixture paths contradict their directory label.** `squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` carries `hsqs` and unblob detects **SQUASHFS_V3**; `squashfs_v3_broadcom/big_endian/__input__/squashfs_v3_be.bin` carries `sqsh` and unblob also detects **SQUASHFS_V3**. Controls in the same directories do land on their family (`shsq` → SQUASHFS_V3_BROADCOM, `tqsh` → SQUASHFS_V3_DDWRT), so the mismatch is specific to those two duplicate files, not a detection fault.

Draft S130 row (full text and validation in `sources-S130.md`):

> `| S130 | unblob 26.6.4 SquashFS integration fixtures — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (LFS payload base https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/) | dataset | A | MIT-licensed Git-LFS fixture bytes and expected member trees for the unblob 26.6.4 SquashFS handler family ... | commit 1fcc7a0a... ; tree API sha256 adb692a2... ; 58 __input__ blobs in 11 directories ... | Pin exact fixture bytes and the expected member list by URL plus LFS oid before generating C2 combos; a fixture path is not a handler label ... | mined | 2026-10-26 | 180d | .ufo/waves/round-42/w1/R42SrcUnblob.md (provisional; L1 re-points after integration) |`

Mechanically checked: 11 non-empty cells after splitting on `|`, no inner `|`, id S130 unused at base.

## 5. D3 — licence

`LICENSE` at the tag is MIT, 21 lines, sha256 `67303bbd...`:

- `:1` `MIT License`
- `:3` `Copyright (c) 2022 ONEKEY GmbH`
- `:5-10` `Permission is hereby granted, free of charge, to any person obtaining a copy ... subject to the following conditions:`
- `:12-13` `The above copyright notice and this permission notice shall be included in all` / `copies or substantial portions of the Software.`

Consequence: committing fixture bytes into the lane is permitted, but line 12-13 obliges carrying the copyright and permission notice with the copies. If the freeze does not want to carry that notice, the correct form is URL + oid + rebuild command rather than committed bytes.

## 6. Calibration against the draft (one risk, two cautions)

1. **Risk — the undefined `D` in R42-C2 step 3.** Handler-level `get_dependencies()` returns `[sasquatch, sasquatch-v4be]` for **every** SquashFS handler, v1-v4 (`squashfs.py:68-69`), and `unblob --show-external-dependencies` reports that union (`dependencies.py:21-31`, exit 1 if any is absent). If `D` were read from that list, a v1-v3 chunk with only `sasquatch-v4be` missing would match `D holds sasquatch-v4be` and be labelled `dep-missing-be`, which is wrong for v3. The per-extraction report is narrower: `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` is fed by `Command.get_dependencies()` = `[self._executable]` (`command.py:70-72`, `:101-102`; field `dependencies: list[str]` at `report.py:122`), i.e. only the binary that failed to spawn. The freeze should say `D` = the `dependencies` field of the `missing-extractor-dependency` report; under that reading the draft's rule is sound and `dep-missing-be` is unreachable for a v1-v3 chunk.
2. **Caution — "clean per handler" must be detected, not assumed.** Two of 58 fixtures sit under a DD-WRT/Broadcom directory and resolve to `squashfs_v3` (§4). A generator that derives the handler from the path produces a mislabelled legacy row.
3. **Caution — family and version coverage.** The subtree also holds 15 v4 fixtures; C2's "v1-v3 fixtures pinned in the freeze" must select them out explicitly. And the v3 fixtures split 9 x 3.0 and 24 x 3.1, so "v3" alone does not pin a minor.

[INFERENCE] The two duplicate/mislabeled fixtures look like copies made when the DD-WRT/Broadcom integration fixtures were assembled; the tree gives no comment saying so, and this is stated as inference only.

## 7. Limits

- No C1 carrier was fetched, opened or extracted; no REA run at all. All unblob runs used unblob's own fixtures, which the assignment designates C2/development inputs.
- The dependency-evidence is unblob-level. The draft's step-3 note "to be confirmed by wave 1 on real REA envelopes" is **not** discharged here.
- D2's completeness relies on the API's `truncated:false`; a recursive tree of this size could truncate on other repos.
- Scratch `/fast/scratch/hyaku/kaidoku-r42/R42SrcUnblob` was removed after copying; cited artifacts are in the lane.

## 8. Artifacts (all under `.ufo/waves/round-42/w1/artifacts/R42SrcUnblob/`)

| file | contents |
|---|---|
| `provenance.md` | per-document status/bytes/sha256/open time, rebuild commands, no-install statement |
| `anchors-squashfs-py.tsv` | 29 anchor rows: document, line range, symbol, quote, note |
| `fixtures-58.tsv` | one row per fixture (58 rows, 11 columns): path, bytes, actual sha256, LFS oid, pointer sha256, pointer bytes, magic, endian, major, minor, dir_family |
| `lfs-pointers.tsv` | raw pointer fetch record (HTTP, pointer bytes, pointer sha256, oid, declared size) |
| `sources-S130.md` | the draft row, its validation, and the two L1 edit options |
| `argv-evidence.txt` | the exact unblob invocations, the logged `sasquatch -le/-be` argv, handler-detection results, dependency-report behaviour |
| `LICENSE-quote.txt` | lines 1-13 of the MIT licence with digest and the notice-retention consequence |

Rebuild: `provenance.md` §rebuild re-fetches D1/D3/D4 by URL and checks each sha256; any fixture is reproduced with the `media.githubusercontent.com` URL plus the `lfs_oid` from `fixtures-58.tsv`.
