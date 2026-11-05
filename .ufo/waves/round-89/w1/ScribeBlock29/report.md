# ScribeBlock29 — round 89, kaidoku — craft rule block 29 revision candidate

Seat: ScribeBlock29 (scribe), leaf. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 89, L1 KaidokuR89.
Base revision `0ec2bb4016655f605657d6e0e700ec2e6893ac27`. Axes: coverage, depth, calibration.

**Status: NOT a replacement for the landed block.** L1 KaidokuR89 ruled that craft block 29 is
**frozen** — it landed at commit `8bbb40cc` in the declaration batch, and R89-C2's frozen kill rule
reads "the block text changed after this declaration", so an edit now kills the claim whatever it
improves. This draft is kept as the **round-90 revision candidate**. No production file was edited.

## Deliverable

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-89/w1/ScribeBlock29/block29.md`
— the block text only, starting `- **Row 29 (`. **399 words, 55 backticked spans.**

## Confirmations requested by the L1

| item | result |
|---|---|
| word count | **399** (band 250-400) |
| backticked spans | **55** (floor `MIN_SPANS` 2) |
| all three citations present at `0ec2bb40` | **yes** — `git show 0ec2bb40:<path>` exit 0 for `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`, `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`, `corpus/knowledge/2026-11-04-r86-record-agreement.md` |
| round-89 entry cited | **no** — the round-89 knowledge entry does not exist at base and is not cited anywhere in the draft |
| counter `shape()` on the draft | `(True, [])` |
| counter `resolve()` against `git show 0ec2bb40:<path>` | `(True, [])` |

## Routed items for the lesson and the QUALITY rows

### R1 — the plan's routing of `sz_cpr > sz_unc` is wrong as a *lane move*

The frozen plan (`plans/round-89-claims.md`, R89-C2 surface) routes "`sz_cpr > sz_unc` and the
PackHeader classes (arithmetic gate -> refuse)". The measurement says the opposite **for the lane
move**: the round-89 repair **recovers** that class, and every out-of-range wrong `sz_cpr`, because
the derivation never reads the stored value.

- Matrix pointer: `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, class `b0.sz_cpr:=sz_unc+1`,
  4 cells, `repair.rc 0`, `repair.info_class "field-value"`, `repaired_tests_clean true`,
  `repaired_identity true` on all four carriers; and class `b0.sz_cpr:=0xFFFFFFF0`, 4 cells, the
  same verdict (`rc 0`, `field-value`, clean true, identity true).
- Tool-level pointer: `tools/round-89/upx-field-value-repair.py` selftest case
  **`wrong-out-of-range-recovered`** (line 214, with `wrong-out-of-range-class` at 215) — the
  comment above it reads "An out-of-range stored value is the same class: the derivation never reads
  it, so the packer's arithmetic gate firing early changes nothing here."
- I ran that selftest myself, read-only: `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest`
  -> `SELFTEST cases=16 failures=0`, **exit 0**.
- The correction: **`sz_cpr > sz_unc` is a packer-side refusal class, not a lane refusal.** The
  gate decides which refusal *message* the packer prints; the redundancy decision (chain geometry,
  stored-value blind) decides the lane move, and that is "recover" for every wrong-value `sz_cpr`.
  Only `sz_unc` has no redundancy and is refused.

### R2 — the `header corrupted` message for that class is carrier-dependent

- Matrix pointer: same file, class `b0.sz_cpr:=sz_unc+1`: **libz answers `corrupt b_info`**, the
  three executables answer `header corrupted` (jq, xxd, docker-init). All four are `upx -t` rc 1.
  A row keyed on the message text would split one class into two; the row must key on the class.
- Packer-side explanation (UPX v5.2.0 `src/p_lx_elf.cpp`, fetched for this seat; sha256
  `551fc867…d2dc`, matching the `S307` row at base): line 7105 `throwCantUnpack("corrupt b_info")`
  sits in the shared-object `un_shlib_1` path, while the executables reach the executable path.
  `S311`/`S312` (which would license citing these lines in a corpus row) are **absent at base** —
  `git show 0ec2bb40:corpus/SOURCES.md | grep -c "^| S311 "` -> 0 — so this is recorded here and
  not in the block's Refs line.

## The exact matrix cell ids relied on (carrier, class, `upx -t` message)

All from `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`, `cells[]`, read with `python3 -I`. The
receipt's scratch paths are normalized to `<work>`; the messages are verbatim.

| # | carrier | class | `upx -t` message | repair |
|---|---|---|---|---|
| 1 | jq | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 2 | xxd | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 3 | libz | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 4 | dinit | `b0.sz_unc:=0` | `CantUnpackException: b_info corrupted` | rc 2 |
| 5 | jq | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 6 | xxd | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 7 | libz | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 8 | dinit | `b0.sz_cpr:=0` | `CantUnpackException: b_info corrupted` | rc 0, chain-geometry |
| 9 | jq | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 10 | xxd | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 11 | libz | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 12 | dinit | `b0.sz_cpr:=true-8` | `Exception: compressed data violation` | rc 0, field-value |
| 13 | jq | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 14 | xxd | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 15 | libz | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 16 | dinit | `b0.sz_cpr:=true+8` | `Exception: compressed data violation` | rc 0, field-value |
| 17 | jq | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 18 | xxd | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 19 | libz | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 20 | dinit | `b0.sz_cpr:=0xFFFFFFF0` | `CantUnpackException: b_info corrupted` | rc 0, field-value |
| 21 | jq | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 22 | xxd | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 23 | libz | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: corrupt b_info` | rc 0, field-value |
| 24 | dinit | `b0.sz_cpr:=sz_unc+1` | `CantUnpackException: header corrupted` | rc 0, field-value |
| 25 | jq | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x240` | rc 0, `intact`, clean **false** |
| 26 | xxd | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x240` | rc 0, `intact`, clean **false** |
| 27 | libz | `b0.method^=0xFF` | `CantUnpackException: bad method 0xfd at 0x2458` | rc 0, `intact`, clean **false** |
| 28 | dinit | `b0.method^=0xFF` | `CantUnpackException: bad method 0xf7 at 0x240` | rc 0, `intact`, clean **false** |
| 29 | jq | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 30 | xxd | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 31 | libz | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 32 | dinit | `l_info.version^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 33 | jq | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 34 | xxd | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 35 | libz | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 36 | dinit | `l_info.format^=0xFF` | `Tested 1 file.` (rc 0) | rc 2 |
| 37 | jq | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 38 | xxd | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 39 | libz | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 40 | dinit | `p_info.p_filesize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 2 |
| 41 | jq | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 42 | xxd | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 43 | libz | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 44 | dinit | `p_info.p_blocksize^=0xFF` | `CantUnpackException: p_info corrupted` | rc 0, `intact`, clean **false** |
| 45 | jq | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 46 | xxd | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 47 | libz | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |
| 48 | dinit | `PackHeader.u_len:=0` | `CantUnpackException: header corrupted 3` | **rc 1** (traceback) |

Cells 1-4 and 5-8 are the QUALITY-156 pair: **identical verbatim refusal text, opposite lane
moves.** Cells 21-24 are R2 (the carrier split). Cells 25-28 and 41-44 are the "exit 0 is not
recovery" calibration (`repaired_tests_clean false`, `repair_diff.positions` empty, delta 0,
`info.class "intact"`). Cell 45-48's repair tail is
`raise Refused("no validated PackHeader in the tail window")` / `r87repair.Refused: no validated
PackHeader in the tail window` — exit 1, not the documented rc 2.

## Citations (all present at the base revision 0ec2bb40 — QUALITY 159)

| citation | what it grounds | line count at base |
|---|---|---|
| `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:29-47` | the structural bound (`0 < s1 - (b0 + 12) <= sz_unc0`) and the accounting bound (`u_len`, most-bytes-wins, smaller-derived tie-break) | 99 |
| `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:85-89` | "there is no redundancy for the uncompressed length: the repair refuses (`sz_unc0 == 0` guard)" — the `sz_unc` refuse row | 99 |
| `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md:23-34` | the `l_info`/`p_info`/`b_info` layout (`struct b_info` field order; `b0 = l_info + 20`) | 125 |
| `corpus/knowledge/2026-11-04-r86-record-agreement.md:9-19` | "a record cell is a claim about bytes, and the claim is re-derived by command" | 27 |

The round-89 knowledge entry is **not** cited. No round-89 receipt path appears in the Refs line; the
one wave path in the block body (`.ufo/waves/round-89/w1/ExecMatrix/matrix.json`) is the matrix
receipt the counts are read from, and it lives outside `corpus/knowledge/`, so the counter's citation
pattern (`corpus/knowledge/<stem>.md`) does not resolve it as a knowledge citation.

## Where each number came from

All cell numbers are from **ExecMatrix's receipt**, `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`
(tool `field_matrix_r89.py`, sha256 `f5ca2b35ac10f12b2f88e2e35d560a3899d9a6ee1220a29d4a7c3f7cd8d6dfbc`,
`exit 0`, `met_target true`, `unclassified []`, `skipped_cells []`, `repair_selftest_rc 0`; population
4 carriers x 12 classes = 48 cells). I re-aggregated `matrix.json` myself with `python3 -I` rather
than copying ExecMatrix's prose table.

- "Four pinned carriers x twelve single-field classes, 48 cells, 0 unclassified" — `population`
  (`carriers`, `classes`, `cells: 48`, `expected: 48`) and `unclassified: []`.
- per-class packer refusal strings — `cells[].upx_t.tail[-1]`, verbatim (see the table above).
- thresholds `b0+4..b0+8`, `0 < derived <= sz_unc0`, `(fits_u_len, total, -derived)` — from the
  pinned repair source `tools/round-89/upx-field-value-repair.py`: `struct.pack_into("<I", out, info["block0"] + 4, derived)`
  (the 4-byte `sz_cpr` window), `if not (0 < derived <= sz_unc0): continue`, and
  `key = (total <= ph["u_len"], total, -derived)`; `b0 = m + 20` where `m` is the `l_info` offset.
- "leaves an already-correct field byte-identical" — `repair()` returns `anchor_out` unchanged when
  `info["stored_sz_cpr"] == derived` (`info["class"]` = `intact`, `info["delta"] = 0`); selftest
  cases `intact-is-byte-identical` (line 186) and `intact-class` (187).
- chain-geometry law, the `sz_unc` no-redundancy limit and the `b_info` layout — the base-present
  knowledge entries cited in the Refs line.

Packer source quotes I checked but did **not** put in the block (they need a source row absent at
base — `S311`/`S312` are absent from `corpus/SOURCES.md` at `0ec2bb40`): UPX v5.2.0 `src/p_lx_elf.cpp`
line 7812 (`throwCantUnpack("b_info corrupted")` after the `ph.c_len == 0 || ph.u_len == 0` gate) and
line 7105 (`throwCantUnpack("corrupt b_info")`, the shared-object `un_shlib_1` site);
`src/p_unix.cpp` lines 680-682 (`sz_cpr > sz_unc` -> `"corrupt b_info %#x %#x"`); `src/packhead.cpp`
lines 283 (`"header corrupted 3"`) and 343 (`"header corrupted"`); `src/packhead.cpp` line 54
(`"bad method %#x at %#x"`); `src/except.cpp` line 122 (`throwCompressedDataViolation`). Files fetched
from `raw.githubusercontent.com/upx/upx/v5.2.0/src/` (HTTP 200; sha256 `551fc867…d2dc` `p_lx_elf.cpp`,
`ab274d67…e040` `packer.cpp`, `41b4a51b…8d6f` `packhead.cpp`, `6cf2b14d…7672` `packhead.h`,
`bf83c413…642e` `p_unix.cpp`) — the first four match the `S307`–`S310` rows at base.

## Shape / separability checks actually run

`python3 -I -B` loading `tools/round-89/depth-blocks-v2.py` and calling its own `shape()` and
`resolve()` on the draft file, with a reader that serves `git show 0ec2bb40:<path>`:

- `shape()` -> `(True, [])` — 399 words >= `MIN_WORDS` 25, 55 spans >= `MIN_SPANS` 2.
- `resolve()` at base -> `(True, [])` — every cited stem exists at `0ec2bb40` and every line range is
  inside the file's base line count.
- `git show 0ec2bb40:SKILL.md` -> 28 blocks in `## Queue-drain craft` (base is 28; the draft makes 29).
- `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` -> `SELFTEST cases=16 failures=0`,
  exit 0 (read-only; the repair's own cases, including `wrong-out-of-range-recovered`).

## Boundaries (what this seat did not do)

- **No production edit.** `SKILL.md`, `claims.json`, `MANIFEST.json`, `corpus/`, `plans/`, `tools/`,
  `.ufo/state/`, `.ufo/watchdog.log`, the fleet root and sibling lanes are untouched;
  `git status --porcelain` shows no modified tracked file. The landed block 29 stays as it is.
- **Concurrent changes observed, not mine, left alone.** While this seat worked, other seats landed
  commits `5a46542a5`, `5068ba641` and `fd9f840bd` (the round-89 entry, the instrument-registry rows,
  and "QUALITY 166-167"), and `corpus/QUALITY.md` carries an **uncommitted** in-flight edit adding
  Rows 166-168 (visible in `git diff -- corpus/QUALITY.md`). Those are other seats' artifacts; I did
  not write to `corpus/QUALITY.md` and did not stage, commit or revert anything. `git diff 8bbb40cc HEAD
  -- SKILL.md` touches only the instrument-registry table — the frozen Row 29 text is byte-identical to
  what landed at `8bbb40cc`.
- I did **not** rerun the frozen counters (`upx-field-battery.py`, `depth-blocks-v2.py --expect-blocks`)
  as my own evidence — the L1 owns that measurement. The pre-freeze receipts under
  `.ufo/waves/round-89/pre/` were read, not rerun.
- I did **not** add a SOURCES row for the UPX v5.2.0 lines above, and did **not** touch the plan.
- The draft's `sz_cpr := sz_unc + 1` row reports the **measured** lane move (recover, 4/4) and names
  the gate as a packer-side refusal class; that is the revision candidate's position, and R1 above is
  the correction the L1 is to carry into the lesson and the QUALITY rows.

## Tooling

No tool installed or upgraded. Host unchanged. Scratch
`/fast/scratch/hyaku/kaidoku-r89/ScribeBlock29/` held only the UPX v5.2.0 source fetch
(`src/`, `tree/`, `upx-5.2.0.tar.gz`, sha256 `e58526f3e198164d63b99b3580dbb9a5111a02a3e4ab1b22b05add4f04c56bbc`)
and was deleted before this report was written.
