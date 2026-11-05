# ExecMatrix — round-89 field-class matrix (grounds craft block 29)

Seat: ExecMatrix (executor), leaf. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 89, L1 KaidokuR89.
Base revision `0ec2bb4016655f605657d6e0e700ec2e6893ac27`. Axes: coverage, depth, calibration.

## What was measured

48 cells = 4 pinned carriers × 12 field classes, every cell a private packed copy.

- Packer: `/usr/bin/upx`, sha256 `cf2f6e7c…969`, `upx 5.2.0` (verified, exit 0).
- Population packed by the battery's exact command `upx --best -q -o packed orig`. The four packed
  files hash to the pre-freeze population (`pre/c1-base-r88-repair.json`) byte-for-byte:
  jq `e8b6c9e7…268a`, xxd `1727faf9…89ff`, libz `a9c544e6…5da5`, dinit `b67ce1bd…14bc`.
  Verified by `probe_layout.py` → `layout-probe.txt` (4 lines `"matches_pre": true`).
- The pinned carrier files are **unpacked** (`upx -t -q` on each: jq rc 2
  `upx: /usr/bin/jq: NotPackedException: not packed by UPX`; libz rc 2 and dinit rc 2 the same
  `NotPackedException`; xxd rc 1 `upx: /usr/bin/xxd: IOException: is a symlink -- skipped`,
  because `/usr/bin/xxd` → `/usr/bin/tinyxxd`; the sha256 pin is of the resolved file, which
  `shutil.copy2` follows). Packing happens per run; no carrier was modified.
- Layout read from the packed bytes via round-87 locators: `b0 = m+20`; `p_filesize` at `m+12`
  equals the original size on all four (asserted by the instrument); `u_len` at `ph_off+16`.
  b0 offsets: jq 576, xxd 576, dinit 576, libz 9304. Block-0 `(sz_unc, sz_cpr)`:
  jq (904, 252), xxd (904, 249), libz (680, 201), dinit (736, 226).
- Per cell: `upx -t -q` rc and verbatim message; then `python3 -I -B upx-field-value-repair.py
  --in … --out … --info …` rc and `info.class`; then `upx -t -q` on the repaired output, and
  `upx -d` identity against the carrier pin.
- Pins re-checked by the instrument before the run: repair sha `332917f2…1070` (frozen pin, match),
  round-87 module `96da7d8e…24` (frozen pin, match); the repair's own `--selftest` rc 0.

## Commands run (every one, with exit)

| # | command (abridged) | exit |
|---|---|---|
| 1 | `sha256sum` on the five pinned hosts/tools; `upx --version`; `upx -t -q` on the four unpacked carriers | 0 (the `upx -t` rcs are listed above) |
| 2 | `field_matrix_r89.py --work <dir> --json-out matrix.json` (first attempt) | 2 — `"unevaluable": "work_unusable: …/work"` (the work dir did not exist; not a result) |
| 3 | `mkdir -p …/work && field_matrix_r89.py --work … --json-out matrix.json` | **0** — `cells=48 unclassified=0 met=True exit=0` |
| 4 | per-cell summary and verbatim extraction over `matrix.json` (python -I) | 0 |
| 5 | `tolerated-check` — pack jq, flip l_info version / format, `upx -t` then `upx -d` (jq only) | 0 |
| 6 | `probe_layout.py` re-run to `layout-probe.txt` | 0 |
| 7 | seat-dir copies of matrix, instrument, probe; sha256 receipts | 0 |
| — | `field_matrix_r89.py --selftest` | 2 (argparse: the instrument has no such flag; a mistaken invocation, **not evidence**, cited only to disclose it) |

Tool installs: none. Host unchanged. REA (`rea-agents@6.5.0`) was **not** run by this matrix (not in the
assignment); the battery's `rea_recover` arm is the L1's counter, not mine.

## Result: 48/48 cells classified; 0 `other-refusal`; 0 `noop`

- `noop` count is **zero**. Every tamper on every carrier changed at least one byte, so no cell was
  folded into `noop`. The `noop` branch exists in the instrument but no population cell exercised it.
- `tolerated` (packer rc 0): 8 cells — `l_info.version^=0xFF` ×4 and `l_info.format^=0xFF` ×4.

## Per-class table (verbatim packer refusal, repair verdict, redundancy)

Repair columns: `rc` (process exit), `class` (`info.class`), `clean` (upx -t on the repaired output),
`id` (upx -d sha equals the carrier pin), `Δ` (count of differing bytes between tampered input and output).

### 1. `b0.sz_unc := 0`  — refuse (the law has no bound)
- Packer, all 4: `CantUnpackException: b_info corrupted` (rc 1).
- Repair, all 4: **refuses** rc 2 — `refused: no l_info candidate carries a derivable first block`.
- Redundancy: `derive()` skips a block whose `sz_unc0 == 0`, and the derivation needs `sz_unc0` as its
  upper bound (`0 < derived <= sz_unc0`). The repair has no second source for block 0's `sz_unc`. Refusal is correct and clean.

### 2. `b0.sz_cpr := 0`  — recover (chain geometry)
- Packer, all 4: `CantUnpackException: b_info corrupted` (rc 1).
- Repair, all 4: rc 0, `class chain-geometry`, `clean` true, `id` true, Δ = 1 byte (in the sz_cpr window).
- Redundancy: the chain (next `b_info` candidate reaching the end-of-chain sentinel, bounded by `sz_unc0`).

### 3. `b0.sz_cpr := true − 8`  — recover (field-value)
- Packer, all 4: `upx: …/tampered: Exception: compressed data violation` (rc 1). The arithmetic gate passes; only the payload stage refuses.
- Repair, all 4: rc 0, `field-value`, `clean` true, `id` true, Δ = 1 (jq 1, xxd 1, libz 1, dinit 1).

### 4. `b0.sz_cpr := true + 8` (guard `true+8 <= sz_unc`: holds on all four)  — recover (field-value)
- Packer, all 4: `Exception: compressed data violation` (rc 1).
- Repair, all 4: rc 0, `field-value`, `clean` true, `id` true, Δ = 2,2,1,1 (jq, xxd, libz, dinit).

### 5. `b0.sz_cpr := 0xFFFFFFF0`  — recover (field-value)
- Packer, all 4: `CantUnpackException: b_info corrupted` (rc 1).
- Repair, all 4: rc 0, `field-value`, `clean` true, `id` true, Δ = 4 (all four bytes of the window).

### 6. `b0.sz_cpr := sz_unc + 1`  — recover (field-value)
- Packer: `CantUnpackException: header corrupted` (jq, xxd, dinit — rc 1); `CantUnpackException: corrupt b_info` (libz — rc 1).
  **The packer's message for one tamper varies by carrier, so the decision cannot key on the message.**
- Repair, all 4: rc 0, `field-value`, `clean` true, `id` true, Δ = 2.

### 7. `b0.method ^= 0xFF`  — repair exits 0 with `intact` on a file that still fails (calibration)
- Packer, all 4: `CantUnpackException: bad method 0xfd at 0x240` (jq), `… bad method 0xfd at 0x240` (xxd),
  `… bad method 0xfd at 0x2458` (libz), `… bad method 0xf7 at 0x240` (dinit) — rc 1.
- Repair, all 4: rc 0, `intact: stored 252 -> derived 252 at block0 576` (jq; analogous for others), Δ = 0,
  output byte-identical to the tampered input, `upx -t` still rc 1 → `clean` **false**.
- Redundancy: none used. The method byte is not in the chain geometry, so `intact` is the repair's pass-through. **Exit 0 is not a recovery.**

### 8. `l_info.version ^= 0xFF`  — packer tolerates; repair refuses a clean file (over-refusal)
- Packer, all 4: `Tested 1 file.` rc 0 (`tolerated`). Unpack identity verified on jq only (upx -d rc 0, sha = pin).
- Repair, all 4: **refuses** rc 2 — `refused: no l_info candidate carries a derivable first block`.
- Cause: `l_info_candidates` (`tools/round-88/upx-chain-repair.py:67`) requires `d[m+6] == ph["version"]` and
  `d[m+7] == ph["format"]`. The packer does not check these bytes; the repair does.

### 9. `l_info.format ^= 0xFF`  — packer tolerates; repair refuses a clean file
- Packer, all 4: `Tested 1 file.` rc 0 (`tolerated`). Unpack identity verified on jq only.
- Repair, all 4: rc 2 — same refusal as class 8, same gate.

### 10. `p_info.p_filesize ^= 0xFF`  — refuse, though a second copy exists
- Packer, all 4: `CantUnpackException: p_info corrupted` (rc 1).
- Repair, all 4: **refuses** rc 2 — `refused: no l_info candidate carries a derivable first block`.
- Redundancy exists and the repair does not use it: the candidate scan keys on `p_filesize` matching
  `PackHeader.u_file_size` (`find(want, 12)`), so the corrupted field removes the candidate. The repair refuses where it could restore. **Named gap, not a claim violation.**

### 11. `p_info.p_blocksize ^= 0xFF`  — repair exits 0 with `intact` on a file that still fails (calibration)
- Packer, all 4: `CantUnpackException: p_info corrupted` (rc 1).
- Repair, all 4: rc 0, `intact: stored … -> derived … at block0 …`, Δ = 0, `clean` **false**.
- Redundancy: the chain walk never reads `p_blocksize`. Same reading as class 7: `intact` is pass-through, not a repair.

### 12. `PackHeader.u_len := 0`  — **traceback, not the documented refusal (defect)**
- Packer, all 4: `CantUnpackException: header corrupted 3` (rc 1).
- Repair, all 4: **rc 1**, uncaught `r87repair.Refused: no validated PackHeader in the tail window`
  (traceback, `raise Refused(…)` at `tools/round-87/upx-magic-repair.py`). The round-89 `main()` catches
  only its own `Refused` class and documents refusals as rc 2; the round-87 `Refused` escapes from
  `find_packheader` inside `derive()`.
- Refusal is still a refusal (no output written), but its exit is 1 not 2, and it is a traceback.

## Summary across the 48 cells

| bucket | cells | classes |
|---|---|---|
| packer `tolerated` (upx -t rc 0) | 8 | l_info.version, l_info.format (×4 each) |
| repair **recovers** (rc 0, field-value/chain-geometry, clean, id, Δ inside window) | 20 | sz_cpr:=0, true−8, true+8, 0xFFFFFFF0, sz_unc+1 (×4 each) |
| repair **refuses** clean rc 2 (no bound / no candidate) | 16 | sz_unc:=0; l_info.version; l_info.format; p_filesize |
| repair rc 0 `intact` but still refused (pass-through) | 8 | method ^=0xFF; p_blocksize ^=0xFF |
| repair rc 1 traceback (uncaught round-87 Refused) | 4 | PackHeader.u_len:=0 |
| `noop` | 0 | — |
| `other-refusal` | 0 | — |

Total 20 + 16 + 8 + 4 = 48. The **claim class** (`T4-chain-szcpr-wrong`, the 4 sz_cpr-in-range cells
`true±8`) is the subset of bucket 2 with `true−8`/`true+8`; the wider sz_cpr classes (zero,
out-of-range) recover in the same way, and that is the block-29 row content.

## Calibration findings for block 29 (route to L1)

1. **`rc 0` is not recovery.** Two classes (method, p_blocksize) return exit 0 with `intact` on files
   `upx -t` still refuses. Block 29 must say that a repair's exit status proves nothing; the test is `upx -t`.
2. **Refusal of a clean file.** The repair refuses `l_info.version` and `format` tampers that `upx -t`
   and `upx -d` accept. Block 29 must not describe this as "the packer rejects it"; the rejection is the repair's own l_info gate.
3. **Traceback exit.** `PackHeader.u_len := 0` exits 1 with a traceback, not the documented rc 2.
   Block 29 must cite exit 1 as observed, not as a refusal code.
4. **Message is carrier-dependent.** `sz_cpr := sz_unc+1` gives `header corrupted` on three carriers and
   `corrupt b_info` on libz. Rows must key on the class, not the message.
5. **p_filesize refusal where redundancy exists.** Not a claim violation; the block's refusal row must say the redundancy is unused.

## Limits (stated before reading the numbers)

- One four-carrier population; one packer build; one repair revision (`332917f2`).
- Only `upx -d` identity was checked for the l_info tolerated cells, on jq. xxd, libz, dinit: `upx -t` rc 0 only.
- The `noop` branch is implemented but not exercised; the matrix shows no noop cell by construction of the population.
- REA was not run here (outside this matrix's assignment).

## Files (seat directory)

- `matrix.json` — full 48 cells (`was`, `new`, `upx_t` rc/tail/text, repair rc/info/`repair_diff`, `repaired_tests_clean`, `repaired_identity`), receipt pins, `repair_selftest_rc`.
- `field_matrix_r89.py` — the instrument (sha256 `f5ca2b35…d6dfbc`; the receipt's `tool_sha256` is the same bytes at run time).
- `probe_layout.py` (sha256 `c656b439…7798b0`), `layout-probe.txt` (sha256 `b4e3c806…5b2447`).
