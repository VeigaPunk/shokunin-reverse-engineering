# UPX-packed PE whose PackHeader magic or `UPX0`/`UPX1` section names are tampered: structural repair (round 98, R98-C1)

source: S324 — UPX v5.2.0 `src/pefile.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/pefile.cpp — opened 2026-11-05, HTTP 200, 127340 bytes, sha256 `6783a926f339b8fa5051c3c0c105c078655513d96ca4bb0f94c74315911379fa` (copy `.ufo/waves/round-98/pre/s324-pefile-v5.2.0.cpp`); `PeFile::canUnpack0` at line 3157, the `memcmp(isection[0].name, "UPX", 3) == 0` test at line 3167, the two `readPackHeader(1024)` calls at lines 3170 and 3174, the "modified/hacked/protected" refusals at lines 3201 and 3203, and the pack-time section naming `strcpy(osection[0].name, "UPX0")` / `"UPX1"` / `".rsrc"`-or-`"UPX2"` at lines 2643-2652; grounds the gate the repair has to satisfy, the two windows it searches and the names it restores.
source: S308 (existing, round 87) — UPX v5.2.0 `src/packhead.cpp`, the PackHeader checksum that skips the four magic bytes, so a header whose magic was overwritten still validates.
source: S309 (existing, round 87) — UPX v5.2.0 `src/packhead.h`, the PackHeader field order (`u_len`, `c_len`, `u_file_size`).
verified-at: 2026-11-05 (round 98; measured revision `72346895a35a74af18151b125934fa0c09fe1e3c`, receipts `.ufo/waves/round-98/l1/scores/c1-at-72346895a35a74af18151b125934fa0c09fe1e3c.json` and `.ufo/waves/round-98/pre/`)
recheck: 180d — the counting command below, plus `python3 -I -B tools/round-98/stop-boundary-repair-battery-v8.py --selftest` (24 cases, failures 0) for the round's second claim.

## The class

[observation] Six sha256-pinned Windows PE carriers, packed by UPX 5.2.0 (`/usr/bin/upx`, sha256 `cf2f6e7c…c969`) `--best`:

| carrier | absolute path | sha256 | packed format |
|---|---|---|---|
| `t32` | `/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/t32.exe` | `6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b` | win32/pe |
| `t64` | `…/pip/_vendor/distlib/t64.exe` | `81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7` | win64/pe |
| `w32` | `…/pip/_vendor/distlib/w32.exe` | `47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b` | win32/pe |
| `w64` | `…/pip/_vendor/distlib/w64.exe` | `7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad` | win64/pe |
| `winhello` | `/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe` | `7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202` | win32/pe |
| `fastlist64` | `/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/node_modules/pnpm/dist/vendor/fastlist-0.3.0-x64.exe` | `d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11` | win64/pe |

Each pack carries exactly one `UPX!` word, at file offset 992, which is the PackHeader (format byte 9 = win32/pe or 36 = win64/pep, version byte 13); the section table holds three sections named `UPX0`, `UPX1`, `.rsrc`; `isection[1].rawdataptr` is 1024 on all six, so the gate's first window is `[960, 1984)` and contains offset 992 on every carrier, while the fallback window at `isection[2].rawdataptr` (36864…130048) never contains it.

[observation] Three tampers, applied to the packed file by the frozen counter: T1 *magic* — the PackHeader `UPX!` word zeroed; T2 *names* — every section header whose name starts with `UPX` renamed by position to `.text`, `.data`, `.rdata`; T3 *both* — T1 then T2. All 18 tampered files are refused: `upx -t` exits 1 on every one (`effective 18 of 18`).
[observation] The refusal message splits by architecture, not by tamper: the three win32/pe carriers answer `CantUnpackException: file is modified/hacked/protected; take care!!!` and the three win64/pe carriers answer `CantUnpackException: file is possibly modified/hacked/protected; take care!`. [source S324] The two strings are the `x` / `!x` branches of the x86-stub probe at lines 3192-3203 (`static const byte magic[] = "\x8b\x1e\x83\xee\xfc\x11\xdb"`; the code comments it as x86-only), so the difference is the packer's own architecture heuristic, not the tamper.
[inference] Both tampers defeat the same gate step, `found_ph`: the names tamper additionally defeats the `memcmp(isection[0].name, "UPX", 3)` precondition, and the magic tamper defeats the PackHeader search itself, because the packer's `readPackHeader` requires the `UPX!` magic it just lost.
[observation] The held ELF repair (`tools/round-87/upx-magic-repair.py`) refuses every one of the 18 files (exit 2); it reads ELF structures only.

## The repair rule (`tools/round-98/upx-pe-repair.py`)

1. Parse the PE section table; refuse (exit 2, nothing written) when the file is not PE or has fewer than three sections — the gate's own `min_sections` (S324 line 3158).
2. In the gate's two windows (`isection[1].rawdataptr - 64` and `isection[2].rawdataptr`, 1024 bytes each), find the offsets whose 32 bytes carry a PE format byte (9 win32/pe, 36 win64/pep), a version byte 10-14, a valid checksum (sum of bytes 4..30 mod 251, S308) and `0 < c_len < u_len`, `c_len` <= file size. Exactly one candidate, or refuse.
3. Rewrite that candidate's magic to `UPX!` when it differs; rename section 0 / 1 to `UPX0` / `UPX1` when they lack the `UPX` prefix; rename section 2 only when it is neither `.rsrc` nor `UPX2*` (to `.rsrc` when the resource directory RVA lies inside it, else `UPX2`). Nothing else changes. The output is written through `O_EXCL|O_NOFOLLOW` + fsync + `os.replace`.
The anchor is located structurally, never by the tampered value.

## The oracle

The oracle is **unpack equivalence**: `upx -d` of the repaired file has the same sha256 as `upx -d` of the untampered pack; the candidate never sees the untampered file.
[observation] For PE the unpack is *not* byte-identical to the original carrier (same length, different sha256 on all six — 386, 390, 405, 412, 974 and 216 differing bytes for `t32`, `t64`, `w32`, `w64`, `winhello`, `fastlist64`; e.g. `t32.exe` `6b4195e6…` vs its unpack `2a300a74…`), unlike the round-87 ELF class, so the oracle is unpack equivalence, not original bytes.
[observation] Unlike the round-87 ELF class there is no leftover word: the repaired file is **byte-identical to the untampered packed file** on all 18 recovered cells and on all 6 intact cells (`ok magic@992`, `ok name0,name1`, `ok magic@992,name0,name1`; the repair's own message lists no `name2` change because the third section is already `.rsrc`).

## The measurement

Frozen command (counter committed at `69c581c7`, before the candidate existed):
`python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd tools/round-98/upx-pe-repair.py --work <scratch> --json-out <receipt> --rev <rev>`

| candidate | label | exit |
|---|---|---|
| `tools/round-98/upx-pe-repair.py` at `72346895` | `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` | 0 |
| identity copy (do-nothing control, `tools/round-98/controls/identity-copy.py`) | `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18` | 1 |
| held ELF repair `tools/round-87/upx-magic-repair.py` | `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18` | 1 |

The refusal arm is the two *unpacked* originals `t64.exe` and `WinHelloCPP.exe`: the repair exits 2 with `refused: packheader-candidates:0` and writes no `--out`. The intact arm is the untampered pack: exit 0, `ok intact`, output byte-identical to the input.
Receipts: `.ufo/waves/round-98/l1/scores/c1-at-72346895a35a74af18151b125934fa0c09fe1e3c.json` (repair sha256 `2fa1102d…1dfa4`, counter sha256 `a34d1253…4feee8`); controls `.ufo/waves/round-98/pre/c1-identity-control.json`, `.ufo/waves/round-98/pre/c1-r87-control.json` (both at base `d0aebc28`, exit 1).

## Still Frontier (stated, never claimed covered)

- Other packers; Mach-O packed inputs; PE with a `UPX2`-named third section (the packer writes `UPX2` instead of `.rsrc` when the original has no resources, S324 line 2652 — none of the six carriers does, so the repair's section-2 branch is never exercised by the population); ARM64 PE and .NET PE (UPX 5.2.0 refuses to pack them at all — `win64/arm64 is not yet supported`, S324 line 142; `.NET files are not yet supported`, S324 line 2209 — so they are unreachable for this packer, not merely unmeasured); PE DLLs.
- Other UPX versions, and other UPX modes: the frozen population packs `--best` only. [out-of-population probe, not scored] On `t32` alone the same repair recovered all three tampers of packs made with `-1`, `--lzma` and `--best --brute` (PackHeader also at offset 992 in each), which is a probe, not a coverage claim.
- Header tampers beyond the magic and the `UPX0`/`UPX1` names: PackHeader fields other than the magic, the stub code, the section sizes and the old-version `isection[2]` header location are neither repaired nor measured. Section 2's own name is only renamed when it is neither `.rsrc` nor `UPX2*`.
- Offset diversity: all six carriers put the PackHeader at offset 992 and `isection[1].rawdataptr` at 1024, so the frozen battery does not separate the structural search from a fixed-offset patch.
- The repaired PE is accepted by the packer; whether it still runs on Windows is not tested (no Windows host on this lane).
