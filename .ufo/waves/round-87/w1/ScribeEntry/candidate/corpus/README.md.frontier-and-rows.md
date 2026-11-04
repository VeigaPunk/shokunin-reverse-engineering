<!-- Candidate for corpus/README.md: three insertions.
     1. coverage-map row: after the `Record agreement, round 86` row (map table, ~line 137);
     2. knowledge-table row: top of `## Knowledge` (newest-first);
     3. frontier note: after the `Round-84 frontier note` paragraph (~line 366). -->

1. coverage-map row:

| UPX magic-tamper repair (round 87) | `2026-11-04-r87-upx-magic-tamper-repair` | **Core** — a UPX-packed ELF whose `UPX!` words are overwritten still runs but answers `NotPackedException`; `tools/round-87/upx-magic-repair.py` restores the three magic anchors from the PackHeader (checksum excludes the magic), `l_info` (cross-checked by version/format/`p_filesize`) and the end-of-chain `b_info` (chain walked past the loader), after which `upx -t`, `upx -d` to the pinned sha256 and REA `analyze` to the declared count hold — recovered <MEASURED> of 8 on four carriers × T1-zero/T2-foreign against 0/8 do-nothing and 4/8 naive-global; UPX 5.2.0 `--best`, LE x86-64; entry-altered stubs, other packers, BE/PE stay Frontier |

2. knowledge-table row:

| `2026-11-04-r87-upx-magic-tamper-repair` | the magic-altered anti-UPX class: three structural anchors (checksum-validated PackHeader, cross-checked `l_info`/`p_info`, walked end-of-chain `b_info`), the repair → `upx -t` → packed-ELF route, scored by the frozen tamper battery on four pinned carriers × two tamper values with refuse-plain / corrupt-payload / intact-idempotent controls; limits UPX 5.2.0 `--best` / LE x86-64 / magic-only tampers, bytes not provenance, jq/xxd repaired packed bytes differ from pristine by a loader `UPX!` occurrence | S306, S307; `tools/round-87/upx-magic-repair.py`, `tools/round-87/upx-tamper-battery.py`; receipts `.ufo/waves/round-87/pre/`, `<MEASURED: .ufo/waves/round-87/l1/scores/…>` | 2026-11-04 |

3. frontier note:

Round-87 frontier note, 2026-11-04: **UPX-packed ELF with tampered `UPX!` magic** is Core for the four pinned carriers (`jq`, `xxd`, `libz.so.1.3.2`, `docker-init`) under UPX 5.2.0 `--best`, little-endian ELF x86-64, magic-only tampers (`2026-11-04-r87-upx-magic-tamper-repair`; S306, S307; `tools/round-87/upx-magic-repair.py`, counter `tools/round-87/upx-tamper-battery.py`, recovered <MEASURED> of 8). This supersedes the "anti-UPX stub whose magic … is altered" / "anti-UPX stubs" clause of the round-68/70/72/73/76/77 notes (`corpus/README.md` lines 324, 355, 357, 360, 362, 364) for this class only. Still Frontier: an anti-UPX stub whose entry or loader code is altered, tampering of packer fields other than the magic, any other packer or UPX version/mode, big-endian ELF, packed PE/Mach-O, carriers outside the four, packed-byte equality of a repaired file, repair provenance beyond source review, and semantic inventory equality.
