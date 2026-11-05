## Gate

**Sources opened this round (CORPUS.md rule 1).**

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S318 (new) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | `<access date>` (`curl -fsSL` exit 0; lines re-read by `sed -n`) | `<HTTP>` / `<bytes>` / `<sha256>` | line `<N>` `<quote>` | `<what the row grounds>` |
| S318 (new) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | `<access date>` (`curl -fsSL` exit 0; `grep -n unpackExtent`) | `<HTTP>` / `<bytes>` / `<sha256>` | line `<N>` `<quote>` | `<the call sites that name the family>` |
| S318 (new) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_interp.cpp | `<access date>` (`curl -fsSL` exit 0; `grep -n unpackExtent`) | `<HTTP>` / `<bytes>` / `<sha256>` | line `<N>` `<quote>` | `<the interpreter family's call sites>` |
| S318 (new) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_mach.cpp | `<access date>` (`curl -fsSL` exit 0; `grep -n unpackExtent`) | `<HTTP>` / `<bytes>` / `<sha256>` | line `<N>` `<quote>` | `<the Mach-O family's call sites>` |
| `<row>` | `<url>` | `<access date>` | `<HTTP>` / `<bytes>` / `<sha256>` | line `<N>` `<quote>` | `<used for>` |

**Row changes (old → new, CORPUS.md rule 2).** S318 added (tier A, `mined`, opened 2026-11-05, recheck on-release, used-by `<the round-93 entries>`). S313 `used-by`: `<old>` → `<new>`; S313 `status` `mined` → `mined`; S313 `recheck` `on-release` → `on-release`; S313 `opened` unchanged (2026-11-04). S313's own row bytes are unchanged: the over-broad "every executable carrier" wording is superseded by the new row, not edited in place. S271 `used-by`: `<old>` → `<new>`; S317 `used-by`: `<old>` → `<new>`. `<any other changed cell, with the column named>`

**Admit / reject.** Admitted: `<row> (<tier reason, one phrase: source code → A>)`. Rejected: `<row or none>` — `<reason>`. `<the routed defect this row closes, named>`

**Assimilation.** `merge/kaidoku/` is absent and the lane has no `considerthese/` directory: `Assimilation: none`.

**Census (frontier step §2b).** Before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit `<0|1>`, `<ok|E-codes>`, `<rows>` registry rows, `<W04 count>` `W04` (`.ufo/waves/round-93/census-before.txt`). After the `<row>` append: exit `<0|1>`, `<ok|E-codes>`, `<rows>` rows, `<W04 count>` `W04` (`.ufo/waves/round-93/l1/scores/census-after.txt`). `E01/E03/E04` findings: `<none or the codes>`.

**Spot-check.** Pending the non-author closure (`corpus/lessons/round-93-verifier-spotcheck.md`, not written by this lane).
