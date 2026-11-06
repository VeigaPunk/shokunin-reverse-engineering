# Coverage-map row draft for `corpus/README.md` (round 100, R100-C1)

Seat: ScribeEntry (scribe). Draft only — the lane corpus is not edited by this seat. Wording below is
proposed for the `## Coverage map` table row (and the matching `## Knowledge` index row and
`Round-100 frontier note`), replacing the rows committed at `b0a7bb8ca5ef66d459d786b9d2705c7fd866d502`
only in the respect named under "Correction" below.

## `## Coverage map` row (proposed)

| UPX-packed PE payload checksum refusal (round 100) | `2026-11-05-r100-pe-upx-payload-checksum-refusal` | **Core (refusal), ten pinned carriers** — a UPX 5.2.0 `--best` win32/pe or win64/pep pack of one of the ten pinned carriers (six exe, four DLL) whose compressed data was altered at intact length fails `upx -t`: with the PackHeader intact the packer reports `Exception: checksum error` (20 of 40 corrupt cells), and with the round-98 magic/name tamper also applied its anti-unpack gate refuses first with `CantUnpackException: file is modified/hacked/protected` (the other 20 of 40) — S327 `ph_decompress`, S324, S326; `tools/round-100/upx-pe-repair.py` refuses it `checksum` (rc 2, nothing written) by the Adler-32 of the `c_len` bytes after the 32-byte PackHeader against `c_adler`, where the round-99 repair answered `ok intact` (rc 0, byte-identical output) — `corrupt 40 of 40`, `effective 119 of 119` (counter `tools/round-100/pe-upx-corrupt-battery.py`; identity control `corrupt 0 of 40`) |

## `## Knowledge` index row (proposed)

| `2026-11-05-r100-pe-upx-payload-checksum-refusal` | UPX-packed PE with altered compressed data at intact length: the packer's Adler-32 `c_adler` test as the refusal rule (`ph_decompress`, S327), the round-99 repair's `ok intact` false green closed, the two distinct packer refusals separated (checksum error vs the anti-unpack gate), a process-level `exec` guard on the battery | S327 (`src/packhead.cpp`), S324 (`src/pefile.cpp`), S326 (`src/packer.cpp`); `tools/round-100/upx-pe-repair.py`, `tools/round-100/pe-upx-corrupt-battery.py`, red fixtures `tools/round-100/forgeries/`; receipts `.ufo/waves/round-100/pre/`, `.ufo/waves/round-100/l1/scores/` | 2026-11-05 |

## `Round-100 frontier note` (proposed)

Round-100 frontier note, 2026-11-05: **UPX-packed PE whose compressed data was altered at intact
length** is Core as a refusal for UPX 5.2.0 `--best` win32/pe and win64/pep packs of the ten
carriers pinned in `tools/round-100/pe-upx-corrupt-battery.py`
(`2026-11-05-r100-pe-upx-payload-checksum-refusal`; S327, S324, S326). This supersedes "payload
corruption at intact length" in the Round-99 note's still-Frontier list, for changes inside the
`c_len` compressed bytes that leave `c_adler` unmatched. Still Frontier: a corruption that also
rewrites `c_adler` (and the PackHeader's own checksum byte) to match, which the packer catches later
on its `u_adler` test after decompression and this tool cannot compute without the NRV/LZMA codec;
Mach-O and other UPX versions; carriers outside the pinned ten; PE header versions below 10 and
non-PE formats.

## Correction proposed to the committed row at `b0a7bb8c`

The row and the committed entry both write that the pack "fails `upx -t` with `checksum error`" for
the whole corrupt arm. The L1 receipt's 40 corrupt cells split 20/20: the 20 `corrupt-intact-*`
cells carry `Exception: checksum error` in `upx_t`, the 20 `corrupt-both-*` cells (the same payload
flip plus the round-98 magic/name tamper) carry
`CantUnpackException: file is modified/hacked/protected` — the anti-unpack gate (S324) refuses
before the compressed data is ever checksummed. The refusal is the packer's own in both halves and
the arm is effective 40 of 40; only the message differs. Counted from
`.ufo/waves/round-100/l1/scores/c1-at-a610671d7a01e1d762eb7103e6ee9f8a2be287ed.json` (cells with
`arm == "corrupt"`: 40; `upx_t` containing `checksum error`: 20; containing
`CantUnpackException`: 20).
