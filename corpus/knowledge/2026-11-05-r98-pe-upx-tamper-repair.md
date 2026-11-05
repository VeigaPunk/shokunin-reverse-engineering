# UPX-packed PE whose PackHeader magic or `UPX0`/`UPX1` section names are tampered: structural repair (round 98, R98-C1)

source: S324 — UPX v5.2.0 `src/pefile.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/pefile.cpp — opened 2026-11-05, 127340 bytes, sha256 `6783a926f339b8fa5051c3c0c105c078655513d96ca4bb0f94c74315911379fa` (copy `.ufo/waves/round-98/pre/s324-pefile-v5.2.0.cpp`); lines 3167-3170: "if (memcmp(isection[0].name, "UPX", 3) == 0) { // current version fi->seek(isection[1].rawdataptr - 64, SEEK_SET); found_ph = readPackHeader(1024);"; grounds the gate the repair has to satisfy and the window it searches.
source: S308 — UPX v5.2.0 `src/packhead.cpp` (opened round 87); the PackHeader checksum skips the four magic bytes, so a header whose magic is overwritten still validates.
source: S309 — UPX v5.2.0 `src/packhead.h` (opened round 87); the PackHeader field order.
verified-at: 2026-11-05 (round 98; measured revision and receipt in SCORECARD `## 2026-11-05 — round 98`)
recheck: on-release — the counting command below, re-run when UPX or a pinned carrier changes.

## The class

[observation] UPX 5.2.0 `--best` packs of six Windows PE carriers (three win32/pe: distlib `t32.exe`,
`w32.exe`, Ghidra's `WinHelloCPP.exe`; three win64/pep: distlib `t64.exe`, `w64.exe`, pnpm's
`fastlist-0.3.0-x64.exe`; sha256 pins in `tools/round-98/pe-upx-tamper-battery.py`) carry one `UPX!`
word, the PackHeader at file offset 992, and the section names `UPX0`, `UPX1`, `.rsrc`. Zeroing the magic,
renaming `UPX0`/`UPX1` to `.text`/`.data`, or both, makes `upx -t` exit 1 on all 18 tampered files
(`effective 18 of 18`); the renamed files answer `CantUnpackException: file is modified/hacked/protected;
take care!!!` on the three win32/pe carriers and `file is possibly modified/hacked/protected; take care!` on
the three win64/pep carriers — the split is the gate's own x86-stub byte probe (S324 lines 3180-3203), not a
difference in the tamper (wave seat ScribeEntry, finding 2).
[source S324] The packer's PE gate `PeFile::canUnpack0` looks for a PackHeader only when section 0's name
starts with `UPX`, first from `isection[1].rawdataptr - 64` over 1024 bytes, then from
`isection[2].rawdataptr`; a file that looks packed without a found PackHeader throws the
"modified/hacked/protected" refusal. At pack time the sections are named `UPX0`, `UPX1` and `.rsrc` or
`UPX2` (lines 2643-2652).
[observation] The held ELF repair (`tools/round-87/upx-magic-repair.py`) refuses every one of these
files (exit 2): it reads ELF structures only.

## The repair rule (`tools/round-98/upx-pe-repair.py`)

1. Parse the PE section table; refuse (exit 2, nothing written) when it is not PE or has fewer than three
   sections — the gate's own minimum.
2. In the gate's two windows, find the offsets whose 32 bytes have a PE format byte (9 win32/pe,
   36 win64/pep), a version byte 10–14, a valid checksum (sum of bytes 4..30 mod 251, S308) and
   `0 < c_len < u_len`, `c_len` ≤ file size. Exactly one candidate, or refuse.
3. Rewrite that candidate's magic to `UPX!` if it differs; rename section 0 / 1 to `UPX0` / `UPX1` when
   they lack the `UPX` prefix; rename section 2 only when it is neither `.rsrc` nor `UPX2*` (to `.rsrc`
   when the resource directory lies in it, else `UPX2`). Nothing else changes. The output is written
   through `O_EXCL|O_NOFOLLOW` + fsync + `os.replace`. The section-2 branch is never exercised by the
   frozen population (all six carriers name section 2 `.rsrc` at pack time).

## The measurement

Command (frozen at `69c581c7`, before the candidate existed):
`python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd tools/round-98/upx-pe-repair.py --work <scratch> --json-out <receipt> --rev <rev>`

| candidate | label | exit |
|---|---|---|
| `tools/round-98/upx-pe-repair.py` at `72346895` | `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` | 0 |
| identity copy (do-nothing control) | `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18` | 1 |
| held ELF repair `tools/round-87/upx-magic-repair.py` | `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18` | 1 |

Oracle: `upx -d` of the repaired file has the same sha256 as `upx -d` of the untampered pack; the
candidate never sees the untampered file. [observation] For PE the unpack is *not* byte-identical to the
original carrier (same size, different sha256 on all six — e.g. `t32.exe` `6b4195e6…` vs unpack
`2a300a74…`), unlike the round-87 ELF class, so the oracle is unpack equivalence, not original bytes.
Receipts: `.ufo/waves/round-98/l1/scores/c1-at-72346895a35a74af18151b125934fa0c09fe1e3c.json`,
controls in `.ufo/waves/round-98/pre/`.

## Limits (stated, never claimed covered)

- All six carriers put the PackHeader at offset 992 (`isection[1].rawdataptr` 1024), so the population does
  not separate the structural search from a fixed-offset patch. The wave's critic seat built three repairs the
  frozen battery admits at the full target label: a size-keyed cache that never reads its input, a lazy
  anchor that skips the checksum and uniqueness tests, and a validated fixed-offset patch
  (`.ufo/waves/round-98/w1/CriticC1.md`, f2/f7/f1h). The frozen predicate therefore establishes that the
  candidate meets it, not that only a structural repair can; a battery with held-out carriers, moved
  PackHeader offsets and a checksum-valid decoy is routed to round 99.
- Out of the frozen population, not scored: the same candidate recovered 48 of 48 tamper cells and 12 of 12
  intact arms on three unpinned win32/pe carriers (Ghidra `WallaceSrc.exe`, `WallaceVersion2.exe`, pnpm
  `fastlist-0.3.0-x86.exe`) under `--best`, `-1`, `--lzma` and `--best --brute`
  (`.ufo/waves/round-98/w1/ExecHeldOut.md`); on a checksum-valid decoy at offset 960 it refuses (exit 2)
  where the lazy-anchor forgery writes a broken file (CriticC1 V2).
- A packed PE truncated to any length ≥ `c_len` is reported `ok intact` (exit 0) although `upx -t` then fails
  (ExecHeldOut finding 2): the tool checks structure, not payload integrity. Routed.
- Not in the frozen population: `UPX2`-named third sections, other UPX versions, DLLs, Mach-O and other
  packers. ARM64 PE and .NET PE are not merely unmeasured: UPX 5.2.0 refuses to pack them (S324 lines 141-142
  `win64/arm64 is not yet supported`, lines 2207-2208 `.NET files are not yet supported`), so no tampered pack
  of either exists for this class.
- Tampers beyond the magic and the `UPX0`/`UPX1` names (PackHeader fields, stub code, section sizes,
  the old-version `isection[2]` header location) are not repaired or measured.
- The repaired file is accepted by the packer; whether it still runs on Windows is not tested.
