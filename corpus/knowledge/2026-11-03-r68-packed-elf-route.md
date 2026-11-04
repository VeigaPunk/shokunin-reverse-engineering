# Round 68 — the packed-ELF triage route: detect, unpack with identity, recover the inventory

**Source:** S269 — UPX 5.2.0 documentation, `doc/upx-doc.txt` at tag `v5.2.0`
(https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt; opened 2026-11-03, HTTP 200, 37 208 B,
sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`; quote at fetched-bytes lines
441-442 under `NOTES FOR LINUX/ELF386`, the class these carriers belong to). Secondary locators in the
same pinned file: the general Linux section repeats the claim at lines 383-384, `--exact` at lines
101-106 bounds it as work in progress for some formats, and `-d`/`-l` are described at lines 74-79.
Instrument: `tools/round-68/packed-elf.py`; receipts `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json`
and `.ufo/waves/round-68/l1/scores/c2-at-*.json`.

## Why the route exists

A shipped Linux executable is sometimes UPX-packed: the file on disk is a decompressor stub plus the
program's code in compressed form. An analyzer that reads the bytes it is given therefore reads the
stub, not the program. On this host REA does exactly that: `analyze` on a packed 30,800-byte `jq`
returns **3 procedures, 3 segments, 3 strings** where the original returns **167 / 30 / 190**, and
`decompile <packed> 0x103fa0` is refused (`invalid_request`, rc 1) where the same address on the
original returns 4,841 bytes of pseudocode. The stub count is not an empty result and it is not an
error: it is a parsed-and-empty inventory of a file whose section header table does not exist.

## The route, as measured

| step | command | observed on the two carriers |
|---|---|---|
| detect | `upx -l <file>` (rc 0 lists it) **and** `readelf -SW` section-header count | both packed files: `upx -l` rc 0, **0 sections** ("There are no sections in this file"); both originals: rc 2 `NotPackedException`, 28/27 sections |
| before | `rea analyze --format json <packed>` | 3 procedures on both carriers, below each carrier's floor (50 for `xxd`, 100 for `jq`) |
| unpack | `upx -d -q -o <out> <packed>` | rc 0 on both |
| identity | `sha256sum <out>` against the carrier pin | `e8156675…` (`jq`) and `7b1e5d0c…` (`xxd`) — byte-identical to the pins |
| recover | `rea analyze --format json <unpacked>` | 167/30/190 and 99/29/103 — equal to the originals on all three counts |
| refusal | `rea decompile <packed> 0x103fa0` vs the same on the unpacked copy | packed rc 1 / `invalid_request`; unpacked rc 0, 4,841 bytes, `FUN_00103fa0` present |
| control | `upx -l <original>` and `upx -d` on the original | rc 2 and rc 2 (`NotPackedException`) — detection has a negative arm on the same bytes |

The identity arm is the load-bearing one: [observation] the manual states decompression restores the
original bytes (S269), and [observation] the two carriers' unpacked sha256 equal their pins exactly.
[inference] Because the unpacked bytes are the original, the inventory recovered from them describes
the program the packed file ships — a recovered count is not a reconstruction estimate. The manual's
own caveat bounds this: `--exact` ("require to be able to get a byte-identical file after
decompression") is documented as work in progress and not supported for all formats, so byte identity
is measured per carrier and never assumed.

## What the packed file itself still shows

[observation] The packed image keeps the original's `BuildID` note and gains the "statically linked,
no section header" shape: `file` reports `ELF 64-bit LSB pie executable, x86-64 … statically linked,
no section header` on both carriers, and `readelf -SW` prints no section list at all. [inference] A
triage row that reports "statically linked" because a tool said so, or "no symbols" because a section
lookup returned nothing, is describing the packer's output shape, not the program's linkage.

## The side effect that matters for instrument pins

[observation] `upx -d` writes the restored file only when the target is a packer output; on an
unpacked file it refuses (`NotPackedException`, rc 2) and writes nothing. [inference] A route that
unpacks every input therefore needs the detection step first, or it will treat a refusal as a failure
of the carrier rather than of the precondition.

## Limits (stated, never claimed covered)

- One packer: UPX 5.2.0 (`/usr/bin/upx`, sha256 `cf2f6e7c…`). No other packer, no UPX-modified stub
  whose magic or entry code has been altered, no packed PE/Mach-O carrier.
- Two carriers, both x86-64 PIE from the Arch package set (`/usr/bin/jq`, `/usr/bin/xxd` →
  `/usr/bin/tinyxxd`). A third carrier was probed in the wave, not in the frozen claim.
- Inventory equality is count equality on procedure, segment and string counts, not semantic equality
  of the recovered program.
- [unknown] Whether an anti-UPX stub (altered magic, patched entry, `upx -d` refusal by design) can be
  handled at all: no such carrier was measured.
- [unknown] Whether the route holds for a packed library (`.so`) or a packed static binary — neither
  was measured; the packer refuses some of them before analysis even starts.

## Evidence

- Instrument: `tools/round-68/packed-elf.py` (13-case selftest; exit 0 met / 1 not met / 2
  could-not-evaluate).
- Before-arm and route: `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` (carriers_matched 2,
  control_ok true, `before_procedures [3, 3]`).
- Controls: `.ufo/waves/round-68/l1/pre/controls-at-base.json` — `c2-packed-only` and `c2-no-identity`
  are both not met; no shortcut reaches the target.
- Decompile envelope shape: `normalized_result` is the pseudocode **string** on success and the
  envelope carries `code: invalid_request` on the packed bytes; a counter that reads a dict there
  reads nothing.
