# Round-98 corpus drafts — ScribeEntry (not written into `corpus/`)

Drafted at `.ufo/waves/round-98/w1/ScribeEntry/`; the seat item forbids writing into `corpus/`.
The knowledge entry draft is `2026-11-05-r98-pe-upx-tamper-repair.md` in this directory.

## 1. Coverage-map row (the `## Coverage map` table, after the round-92 row)

| UPX-packed PE magic / section-name tamper repair (round 98) | `2026-11-05-r98-pe-upx-tamper-repair` | **Core** — a UPX 5.2.0 `--best` win32/pe or win64/pe pack whose PackHeader `UPX!` is zeroed, whose `UPX0`/`UPX1` names are renamed, or both, is refused by `upx -t` (`effective 18 of 18`) and by the held ELF repair; `tools/round-98/upx-pe-repair.py` locates the PackHeader in the packer's own `canUnpack0` windows by checksum (S324, S308) and restores the magic and the `UPX0`/`UPX1` names: `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` on six pinned carriers by unpack equivalence (counter `tools/round-98/pe-upx-tamper-battery.py`; identity control `recovered 0 of 18`, held ELF repair `recovered 0 of 18`); the repaired file is byte-identical to the untampered pack, and PE unpack is not byte-identical to the original carrier |

## 2. Knowledge-table row (the `## Knowledge` table)

| `2026-11-05-r98-pe-upx-tamper-repair` | UPX-packed PE anti-unpack tampers (PackHeader magic, `UPX0`/`UPX1` names): the packer's PE unpack gate, the structural PackHeader search, the unpack-equivalence oracle, and the two refusal messages the packer gives per architecture | S324 (`src/pefile.cpp`), S308, S309; `tools/round-98/upx-pe-repair.py`, `tools/round-98/pe-upx-tamper-battery.py`; receipts `.ufo/waves/round-98/pre/`, `.ufo/waves/round-98/l1/scores/` | 2026-11-05 |

## 3. `Round-98 frontier note` line (the file-tail note series, in the style of the round-88/89/90/91/92 notes)

Round-98 frontier note, 2026-11-05: **UPX-packed PE with a tampered PackHeader magic and/or renamed `UPX0`/`UPX1` sections** is Core for the six pinned carriers (distlib `t32`/`t64`/`w32`/`w64`, `WinHelloCPP.exe`, `fastlist-0.3.0-x64.exe`) under UPX 5.2.0 `--best`, win32/pe and win64/pe (`2026-11-05-r98-pe-upx-tamper-repair`; S324, S308, S309; `tools/round-98/upx-pe-repair.py`, counter `tools/round-98/pe-upx-tamper-battery.py`, `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`). This supersedes the "packed PE" half of the "PE and Mach-O packed inputs" clause of the round-92 note (and "packed PE/Mach-O" in the round-76/77 notes) for this class only. Still Frontier: Mach-O, other packers, PE with a `UPX2`-named third section, PE DLLs, other UPX versions and modes (only `--best` is measured), PackHeader offsets other than 992 (all six carriers share it), tampers of PackHeader fields or stub code beyond the magic and the section names, and whether a repaired PE still runs.

Note on the ARM64 PE / .NET PE clauses: UPX 5.2.0 refuses to *pack* `win64/arm64` (S324 line 142, "win64/arm64 is not yet supported") and `.NET` files (S324 line 2209), so for this packer those classes are unreachable rather than merely unmeasured; they are named here as not-covered, not as measured negatives.
