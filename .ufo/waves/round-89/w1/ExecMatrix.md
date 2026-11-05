# ExecMatrix (round 89, kaidoku) — field-class matrix for craft block 29

Full report: `.ufo/waves/round-89/w1/ExecMatrix/report.md`. Cells: `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`.

## Measured

- 48 cells = 4 pinned carriers (jq, xxd, libz.so.1.3.2, docker-init) × 12 field classes, packed by `upx 5.2.0` (sha256 `cf2f6e7c…969`) with `upx --best -q`. The four packed files hash to the frozen pre-freeze population.
- 48/48 classified. `other-refusal` 0. `noop` 0 (no population cell left bytes unchanged; the noop branch was not exercised).
- Instrument exit 0 (`met=True`), repair `--selftest` rc 0, repair sha `332917f2…1070` and round-87 module `96da7d8e…24` match their frozen pins.

## Per class (packer refusal verbatim → repair verdict → redundancy)

| class | packer (upx -t) | repair | redundancy / reading |
|---|---|---|---|
| `b0.sz_unc := 0` | `CantUnpackException: b_info corrupted` ×4 | refuses rc 2 `refused: no l_info candidate carries a derivable first block` ×4 | derivation needs `sz_unc0` as its bound; no second source |
| `b0.sz_cpr := 0` | `CantUnpackException: b_info corrupted` ×4 | recovers ×4, chain-geometry, clean, id, Δ 1 | chain geometry |
| `b0.sz_cpr := true−8` | `Exception: compressed data violation` ×4 | recovers ×4, field-value, clean, id, Δ 1 | chain geometry; payload-stage refusal |
| `b0.sz_cpr := true+8` | `Exception: compressed data violation` ×4 | recovers ×4, field-value, clean, id, Δ 2,2,1,1 | as above |
| `b0.sz_cpr := 0xFFFFFFF0` | `CantUnpackException: b_info corrupted` ×4 | recovers ×4, field-value, clean, id, Δ 4 | chain geometry |
| `b0.sz_cpr := sz_unc+1` | `header corrupted` ×3, `corrupt b_info` ×1 (libz) | recovers ×4, field-value, clean, id, Δ 2 | message varies by carrier |
| `b0.method ^= 0xFF` | `bad method 0xfd at 0x240` (jq, xxd), `0xfd at 0x2458` (libz), `0xf7 at 0x240` (dinit) | rc 0 `intact` ×4, Δ 0, **still fails upx -t** | pass-through, not recovery |
| `l_info.version ^= 0xFF` | `Tested 1 file.` rc 0 (tolerated) ×4 | refuses rc 2 ×4 (l_info gate) | repair over-refuses a clean file; unpack identity checked on jq only |
| `l_info.format ^= 0xFF` | `Tested 1 file.` rc 0 (tolerated) ×4 | refuses rc 2 ×4 (l_info gate) | as above |
| `p_info.p_filesize ^= 0xFF` | `CantUnpackException: p_info corrupted` ×4 | refuses rc 2 ×4 | `p_filesize` duplicates `PackHeader.u_file_size`; repair keys on it and refuses rather than restores |
| `p_info.p_blocksize ^= 0xFF` | `CantUnpackException: p_info corrupted` ×4 | rc 0 `intact` ×4, Δ 0, **still fails upx -t** | chain walk never reads `p_blocksize` |
| `PackHeader.u_len := 0` | `CantUnpackException: header corrupted 3` ×4 | **rc 1 traceback** (uncaught `r87repair.Refused`) ×4 | exit 1, not the documented rc 2 |

Totals: recovers 20, refuses clean (rc 2) 16, rc 0 pass-through still refused 8, rc 1 traceback 4, tolerated 8 (inside the refusals' classes), noop 0, other-refusal 0.

## Calibration findings for block 29

1. Exit 0 is not recovery: method and p_blocksize return rc 0 `intact` on files `upx -t` still refuses. Rows must cite `upx -t`, not the repair's exit.
2. The repair refuses l_info version and format tampers that `upx -t` and `upx -d` accept (its own gate, `l_info_candidates`, not the packer's).
3. `PackHeader.u_len := 0` exits 1 with a traceback. Cite it as exit 1, not as a refusal code.
4. The packer's message for `sz_cpr := sz_unc+1` depends on the carrier. Rows key on the class.
5. p_filesize refusal ignores a redundant copy. Not a claim violation; the row must say so.

## Not done / limits

- One four-carrier population, one packer build, one repair revision.
- `upx -d` identity checked on the l_info tolerated cells for jq only.
- REA not run by this matrix.
- A mistaken `--selftest` call (argparse rc 2, flag absent) is disclosed; it is not evidence.

## Host and tooling

- Tool installs: none. No system change. Scratch `/fast/scratch/hyaku/kaidoku-r89/ExecMatrix/` deleted after receipts (rm rc 0, absence confirmed).
- Receipts in the seat dir: `matrix.json`, `field_matrix_r89.py` (sha256 `f5ca2b35…d6dfbc`, matches the receipt's `tool_sha256`), `probe_layout.py`, `layout-probe.txt`, `report.md`.
