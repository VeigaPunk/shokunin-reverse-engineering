# ExecDeriveIndep — round 90 (kaidoku), independent derivation of the interior `sz_cpr` law

Seat `ExecDeriveIndep`, wave `r90-w1`, lane `kaidoku-shokunin`, base `fc52cc9dc`.
Task: derive the round-90 law independently from scratch (no import of
`tools/round-90/upx-break-repair.py`), dump the chain layout of the four pinned
carriers, score the derivation on the six P1 cells, and state + measure where
the law is not decidable. Everything below is measured on this host, 2026-11-05;
every number carries the command that produced it. Seat tool:
`.ufo/waves/round-90/w1/ExecDeriveIndep/szcpr_law.py` (self-contained, imports
neither tools/round-87 nor round-88 nor round-90 — only their documented layout
conventions, re-implemented). Driver: `.ufo/waves/round-90/w1/ExecDeriveIndep/matrix.py`.

## Environment

- Packer: `/usr/bin/upx --version` → `upx 5.2.0`, UCL 1.03, zlib 1.3.1.1-motley,
  LZMA SDK 4.43. `sha256sum /usr/bin/upx` →
  `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` — equals the
  frozen `pins.upx_sha256`.
- Carriers (copies in scratch; `cp -L` for the `xxd` symlink):
  `sha256sum` of originals: `jq` 30,800 B
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`;
  `xxd`→tinyxxd 38,928 B
  `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`;
  `libz.so.1.3.2` 108,560 B
  `6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9`;
  `docker-init` 851,288 B
  `0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115`.
  These four hashes are the carrier pins used by the `upx -d` arm.
  Pack: `for n in jq xxd libz.so.1.3.2 docker-init; do /usr/bin/upx --best -o
  packed/$n.upx orig/$n; done` → rc=0 ×4. Packed sha256: jq 14,036 B
  `e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a`;
  xxd 19,560 B `1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff`;
  libz 65,580 B `a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b`;
  docker-init 357,784 B `b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7`.
  Baseline per carrier (matrix step 2): intact packed passes `upx -t` rc 0 and
  `upx -d` reproduces the pin hash and size ×4 — receipt `baselines` in
  `receipts/matrix.json`.

## 1. The derivation (my own law)

From the round-87/round-88 conventions (re-implemented, not imported):
`l_info` magic at `m` with `l_version/l_format` at `m+6/m+7` matching the
PackHeader; `p_info` at `m+12` carrying `u_file_size` (the locator anchor);
first `b_info` at `m+20`; each `b_info` = `sz_unc u32, sz_cpr u32,
b_method u8, b_ftid u8, b_cto8 u8, b_unused u8`; successor at `pos+12+sz_cpr`;
the chain stops at an embedded loader and resumes at a later offset whose own
walk ends in an end-of-chain sentinel (`sz_unc==0`, `b_method..b_unused==0`);
the PackHeader (`sum(buf[4:31]) % 251 == buf[31]`) declares `u_len`.

**Law.** A block at `pos` whose stored `sz_cpr` breaks the chain is justified
by exactly one value, `sz_cpr = s − (pos + 12)`, where `s` is the successor's
position. A candidate `s` is accepted only when, with that value written, the
whole chain (first segment + loader resume) ends in the end-of-chain sentinel,
the uncompressed bytes it accounts equal the declared `u_len` **exactly**, and
they **strictly exceed** what the stored chain accounts. The filter must leave
exactly one candidate; zero (a chain that can never cover `u_len`) or more
than one (every in-range value leaving a stop before the resume accounts the
same total) leave the bytes unchanged — never a guess.

Exit contract: 0 with `--out` written (byte-identical when unchanged),
2 refused with nothing written (plain ELF, no PackHeader, no anchored chain).

## 2. Chain layout of the four pinned carriers

Command: `python3 -I -B szcpr_law.py dump --in packed/<n>.upx --json`
(receipts `receipts/dump-<n>.json`; cross-check `tools/round-87/
upx-magic-repair.py --in … --json`, receipts `receipts/r87-crosscheck-<n>.json`).

| carrier | first-segment blocks (idx: off, sz_unc, sz_cpr) | first stop | resume | sentinel | accounted = first_sum + resumed_sum | u_len | full coverage |
|---|---|---|---|---|---|---|---|
| jq (ph 14000, l_info 556) | 0: 576, 904, 252 · 1: 840, 5408, 1651 · 2: 2503, 9561, 4758 · 3: 7273, 5528, 2626 · 4: 9911, 1184, 174 | 10097 | 13228 (4 blocks) | 13988 | 30,800 = 22,585 + 8,215 | 30,800 | **yes** |
| xxd (ph 19524, l_info 556) | 0: 576, 904, 249 · 1: 837, 2856, 950 · 2: 1799, 21717, 11492 · 3: 13303, 4528, 2140 · 4: 15455, 784, 163 | 15630 | 18756 (4 blocks) | 19509 | 38,928 = 30,789 + 8,139 | 38,928 | **yes** |
| docker-init (ph 357748, l_info 556) | 0: 576, 736, 226 · 1: 814, 592, 202 · 2: 1028, 575549, 265172 · 3: 266212, 230752, 82125 · 4: 348349, 27304, 4313 | 352674 | 355828 (4 blocks) | 357734 | 851,288 = 834,933 + 16,355 | 851,288 | **yes** |
| libz.so.1.3.2 (ph 65544, l_info 9284) | 0: 9304, 680, 201 · 1: 9517, 63157, 33574 · 2: 43103, 23584, 17012 | 60127 | 62944 (4 blocks) | 63717 | **98,592** = 87,421 + 11,171 | 108,560 | **no** |

Per-carrier statement: **jq, xxd, docker-init: the intact chain accounts the
full `u_len`. libz: it does not — 98,592 of 108,560 (9,968 bytes of appended
non-chain data), independently reproducing the declared measured limit.**

Geometry cross-check: my dump agrees with the round-87 tool on all four
carriers (`blocks_first`, `resume`, `sentinel+4` all True ×4, receipts
`r87-crosscheck-*.json`); `tools/round-88/upx-chain-repair.py --json` classes
all four `intact` (rc 0 ×4).

## 3. P1 scoring — six cells, all recovered (6 of 6)

Cells: block index 1 of the first segment, `sz_cpr` → stored − 7 and stored + 7.
Command per cell (driver `matrix.py`): patch 4 bytes at `block_offset+4`,
`upx -t` the tampered file, then
`python3 -I -B szcpr_law.py repair --in tampered --out out --json`, then the
three arms. Receipts: `receipts/matrix.json` (`p1_cells`),
binaries `receipts/binaries/p1-*-{tampered,out}.upx`.

| cell | block1 (off, sz_unc, stored) | tampered value | `upx -t` on tampered | repair | arm1 bytes==intact | arm2 `-t` rc 0 | arm3 `-d` sha==pin | deciding values | elapsed |
|---|---|---|---|---|---|---|---|---|---|
| p1-jq-b1-delta-7 | 840, 5408, 1651 | 1644 | rc 1, `Exception: compressed data violation` | rc 0 `recovered`, derived 1651 | yes | yes | yes | **1** (1651) | 0.009 s |
| p1-jq-b1-delta+7 | 840, 5408, 1651 | 1658 | rc 1, same exception | rc 0 `recovered`, derived 1651 | yes | yes | yes | **1** (1651) | 0.010 s |
| p1-xxd-b1-delta-7 | 837, 2856, 950 | 943 | rc 1, same | rc 0 `recovered`, derived 950 | yes | yes | yes | **1** (950) | 0.004 s |
| p1-xxd-b1-delta+7 | 837, 2856, 950 | 957 | rc 1, same | rc 0 `recovered`, derived 950 | yes | yes | yes | **1** (950) | 0.005 s |
| p1-docker-init-b1-delta-7 | 814, 592, 202 | 195 | rc 1, same | rc 0 `recovered`, derived 202 | yes | yes | yes | **1** (202) | 0.118 s |
| p1-docker-init-b1-delta+7 | 814, 592, 202 | 209 | rc 1, same | rc 0 `recovered`, derived 202 | yes | yes | yes | **1** (202) | 0.082 s |

Every repaired cell is byte-identical to the intact packed carrier (arm1),
`upx -t` rc 0 (arm2), and `upx -d` reproduces the original's sha256 and size
(arm3: pins in Environment). Decidability sweep on each tampered file
(`szcpr_law.py derivations --block-offset <off>`): exactly **one** swept value
reaches `u_len`, and it is the intact original (1651/950/202) — the tampered
stored value never does. **P1 = 6 of 6; the unique-decision filter is what
makes each cell decidable.**

## 4. Where the law is not decidable (measured)

**(a) The last block before a chain stop — under-determined.**
`docker-init`, block index 4 (off 348349, sz_unc 27304), sz_cpr 4313 → 4306
(`receipts/binaries/undecidable-last-block-docker-init-tampered.upx`).
`upx -t` on the tampered file: rc 1, `Exception: compressed data violation`
(the packer sees it). My repair: rc 0, **bytes unchanged** (verdict
`unchanged-intact` — the tampered chain itself still accounts exactly 851,288,
because every in-range value leaves a stop that the resume scan papers over
with the same accounting). Derivation sweep on the tampered file:
derived ∈ {1, 2, 2153, 4299, 4306, 4313} **all** account exactly 851,288 —
6 deciding values for 6 candidate positions; only overshooting values past the
stop region (27303, 27304) drop the accounting to 823,984. The exact-total
filter cannot discriminate among the six; the law leaves the bytes unchanged,
as declared.

**(b) A chain that under-accounts `u_len` — out of class.**
`libz.so.1.3.2`, block 1 (off 9517, sz_unc 63157), sz_cpr 33574 → 33567
(`receipts/binaries/undecidable-libz-undercovering-tampered.upx`). Repair:
rc 0, verdict `unchanged-out-of-class`, **bytes unchanged**. Derivation sweep:
no value reaches `u_len` — the stored/intact value 33574 gives the intact total
98,592; 33560/33567/16783/1/2 give 75,008; 63156/63157 give 11,851; **0
deciding values** against `u_len` 108,560. The exact-total rule has no
solution here, so it can neither confirm nor repair — declared limit
reproduced exactly (98,592 of 108,560).

**(c) Calibration extras.** Intact `jq` → rc 0 `unchanged-intact`,
byte-identical; intact `libz` → rc 0 `unchanged-out-of-class`, byte-identical
(idempotent); plain ELF (`orig/jq`) → rc 2, refused
(`no validated PackHeader in the tail window`), nothing written.

## Verdict

Within this seat's independent implementation and test: **the derivation is
the law.** It recovers exactly the six P1 cells (each through a unique
`u_len`-deciding successor position, repaired bytes equal to the intact packed
carrier, `upx -t` rc 0, `upx -d` pin reproduced), reproduces the declared libz
limit (98,592/108,560) and the last-block under-determination (six in-range
values accounting the same total), and never writes a guessed value. Measured
cost per repair: 0.004–0.118 s (one resume-scan precompute per file + one
O(log n) probe per candidate), consistent with the declared "scan with one
find_sentinel per candidate, measured not claimed linear".

## Receipts (absolute paths)

- Tool + driver: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ExecDeriveIndep/szcpr_law.py`, `…/matrix.py`
- `…/ExecDeriveIndep/receipts/matrix.json` — every cell: commands, rcs, arms, sweep rows, timings
- `…/ExecDeriveIndep/receipts/dump-{jq,xxd,libz.so.1.3.2,docker-init}.json` — chain layouts
- `…/ExecDeriveIndep/receipts/r87-crosscheck-*.json` — geometry agreement with tools/round-87
- `…/ExecDeriveIndep/receipts/binaries/` — tampered + repaired binaries for all six P1 cells and both undecidability cells
- Wave-render copy of this report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ExecDeriveIndep.md`

Scratch `/fast/scratch/hyaku/kaidoku-r90/ExecDeriveIndep/` (carriers, tamper
working set) was used for all runs and removed after copying receipts. No
install was needed (upx 5.2.0, python3 present); nothing under PATH or the
fleet tree outside this seat dir was written.
