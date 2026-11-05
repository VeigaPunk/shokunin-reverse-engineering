- **Row 29 (a field's *value class* picks the move; the packer's refusal names the check that fired, not the field).** Block 0's twelve bytes are `sz_unc`, `sz_cpr`, `method`, `ftid`, `cto8`, `unused` at `b0+0..b0+11` (`b0 = l_info + 20`), and one label covers two fields: `upx -t` answers `CantUnpackException: b_info corrupted` for a zeroed `sz_unc` *and* for a zeroed `sz_cpr`, yet only the second is recoverable. Four pinned carriers x twelve single-field classes, 48 cells, 0 unclassified (`upx 5.2.0`; `.ufo/waves/round-89/w1/ExecMatrix/matrix.json`):

| field class | packer refusal | structural redundancy | lane move |
|---|---|---|---|
| `sz_unc := 0` | `b_info corrupted` | none — `sz_unc0` bounds the derivation | refuse |
| `sz_cpr := 0` | `b_info corrupted` | chain geometry | recover |
| `sz_cpr` wrong, in range | `compressed data violation` | chain geometry | recover |
| `sz_cpr` out of range | `b_info corrupted` | chain geometry | recover |
| `sz_cpr := sz_unc + 1` | `header corrupted` (executables), `corrupt b_info` (shared object) | chain geometry | recover |
| `b_info.method` | `bad method 0xfd at 0x240` (text varies by carrier) | the PackHeader's method | no repair (rc 0, delta 0) |
| `l_info.version`, `l_info.format` | tolerated, rc 0 | the PackHeader's version/format | no repair (rc 2) |
| `p_info.p_filesize` | `p_info corrupted` | duplicates `u_file_size` | refuse (rc 2) |
| `p_info.p_blocksize` | `p_info corrupted` | the packer's own block size | no repair (rc 0, delta 0) |
| `ph.u_len := 0` | `header corrupted 3` | the header checksum | no repair (rc 1) |

The packer's `sz_cpr > sz_unc` gate is a separate class from the wrong-value ones and its text is carrier-dependent, so a row keys on the class, never on the message. Recovery is chain geometry, stored-value blind: `sz_cpr` is the distance from `b0 + 12` to the next plausible `b_info`, bounded by `0 < derived <= sz_unc0`, and the survivor wins on the accounting key `(fits_u_len, total, -derived)`; the repair writes only the window `b0+4..b0+8`, and an equal stored value is left byte-identical. Exit 0 is not recovery: a `method` or `p_blocksize` tamper returns rc 0 and delta 0 while `upx -t` still refuses, so a move is judged by `upx -t` and `upx -d`, never by the repair's exit code.

  Refs: `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:29-47` (the bounds), `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md:85-89` (no redundancy for `sz_unc`), `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md:23-34` (`b_info` layout), `corpus/knowledge/2026-11-04-r86-record-agreement.md:9-19` (cells re-derived).
