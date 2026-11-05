# ReviewerFalsify — R91 wave 1 — falsification of "the stop-boundary tamper is NOT decidable by a packer-validated search"

Seat: ReviewerFalsify (reviewer, leaf — no subagents). Date: 2026-11-05. Lane frozen at declaration
`deb2765a55fef0e4e81500a027dfe59951b69e87` (base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`).
All work in scratch `/fast/scratch/hyaku/kaidoku-r91/ReviewerFalsify` (deleted before yield); receipts
copied to this seat directory. The lane repo was read-only: read-only git and file reads only; the only
lane writes are the three files listed at the end, all inside `.ufo/waves/round-91/w1/`.

## Verdict

**H holds — the target claim is falsified, on all eight cells, not just one.**

Hypothesis H (seat item): for at least one of the eight tampered cells, some in-range value v for the
last block's `sz_cpr` makes `upx -t` rc 0 on the candidate AND `upx -d` of the candidate reproduces the
carrier's pinned original sha256.

Measurement: for every carrier and both directions (−7, +7), the enumerated in-range candidates contain
**exactly one** `upx -t`-green value, and it is the pristine stored `sz_cpr`; the candidate at that v is
byte-identical to the pristine pack and its `upx -d` output reproduces the pinned original sha256.

Consequence: `upx -t` is a **decision procedure** for the last block's `sz_cpr` — red on every in-range
v except the true one. The claim that the last-block stop-boundary tamper "is NOT decidable by a
packer-validated search" is false. The refusal class contains recoverable inputs (all eight), recoverable
by a length-preserving, in-window (4-byte) rewrite that the packer itself validates. The refusal in
R91-C1 is a policy choice (refuse rather than search), not an information-theoretic necessity.

## Per-cell results

Packing per the frozen counter: `upx 5.2.0` (`/usr/bin/upx`, sha256
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` — matches the `claims.json` pin),
`--best -q`, carrier copies mode 0755. Last block from the frozen counter's own `layout()`
(`stop-boundary-battery.py` imported with importlib; counter sha256 `5998b6bd…`, r87 `96da7d8e…`,
r88 `59ee51b0…` — all match the `claims.json` pins). Carrier pins all matched before packing.

| carrier | packed sha256 | blocks | last-block off | stored sz_cpr | sz_unc | cell | tampered value | candidates tried | `-t` green | `-d`==pin | green/match v |
|---|---|---|---|---|---|---|---|---|---|---|---|
| jq | `e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a` | 5 | 9911 | 174 | 1184 | −7 | 167 | 1184 | 1 | 1 | 174 |
| jq | 〃 | 〃 | 〃 | 〃 | 〃 | +7 | 181 | 1184 | 1 | 1 | 174 |
| xxd | `1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff` | 5 | 15455 | 163 | 784 | −7 | 156 | 784 | 1 | 1 | 163 |
| xxd | 〃 | 〃 | 〃 | 〃 | 〃 | +7 | 170 | 784 | 1 | 1 | 163 |
| libz | `a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b` | 3 | 43103 | 17012 | 23584 | −7 | 17005 | 513 | 1 | 1 | 17012 |
| libz | 〃 | 〃 | 〃 | 〃 | 〃 | +7 | 17019 | 513 | 1 | 1 | 17012 |
| docker-init | `b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7` | 5 | 348349 | 4313 | 27304 | −7 | 4306 | 513 | 1 | 1 | 4313 |
| docker-init | 〃 | 〃 | 〃 | 〃 | 〃 | +7 | 4320 | 513 | 1 | 1 | 4313 |

Candidate-enumeration bound used (per seat spec): v over every integer in `[1, sz_unc]` when
`sz_unc <= 20000` (jq, xxd — full sweeps), otherwise `[stored-256, stored+256]` plus the walk-plausible
values (stored itself and the two tampered values, all inside the window) for libz and docker-init.
Baseline: `upx -t` on the tampered file itself (v = tampered value) is rc 1 on all eight cells
("Tested 1 file: 0 ok, 1 error."). Pristine controls: `-t` rc 0 and `-d` reproduces the pinned original
sha256 on all four carriers. Wall time 2.1 s; the 25-minute cap was not reached.

Spot-check (diagnostics, one carrier per enumeration mode): every non-stored v tested fails with
`Exception: compressed data violation` (v near stored, v=1) or `checksum error` / `EOFException:
premature end of file` (v=sz_unc); v=stored gives `Tested 1 file.`, candidate bytes == pristine pack
(`candidate==pristine: True`), and `-d` output sha256 == pin. Full log: `falsify-spotcheck.txt`.

## Exact commands (reproduction)

Setup (exit 0 throughout; scratch only):

```
S=/fast/scratch/hyaku/kaidoku-r91/ReviewerFalsify
mkdir -p "$S/tmp" "$S/work" "$S/cand" "$S/home"
export SEAT_SCRATCH="$S" TMPDIR="$S/tmp"
python3 "$S/search.py"          # exit 0; wrote $S/results.json; wall 2.1 s, cap_reached=false
```

Minimal H proof for one cell (jq, −7; v = 174 = stored; block offset 9911 from the frozen `layout()`):

```
cp /usr/bin/jq $S/jq && chmod 0755 $S/jq
/usr/bin/upx --best -q -o $S/packed $S/jq                     # sha256 e8b6c9e7…5268a
python3 -c "import struct;d=bytearray(open('$S/packed','rb').read());struct.pack_into('<I',d,9911+4,167);open('$S/t7','wb').write(bytes(d))"
python3 -c "import struct;d=bytearray(open('$S/t7','rb').read());struct.pack_into('<I',d,9911+4,174);open('$S/fix','wb').write(bytes(d))"
/usr/bin/upx -t -q $S/fix                                     # rc 0
/usr/bin/upx -d -q -o $S/unp $S/fix                           # rc 0
sha256sum $S/unp                                              # e815667571d07cb7… == pinned original
```

## Reading against the frozen claims

- The frozen label `refused 8 of 8; unsafe 0; intact 4 of 4` is an honest description of the candidate
  tool's behaviour — this attack does not dispute the measurement or the label.
- What it falsifies is the plan's declared limit: *"The class is refused, not repaired: no successor and
  no decompression decides the last block (the geometry leaves `sz_cpr` under-determined)."* A
  packer-validated search decides the last block uniquely — `upx -t`, the same packer verdict C1 relies
  on for its intact arm, is green for exactly one in-range v and that v restores a file whose `-d`
  output is the pinned original. Under the battery's own taxonomy such an output is in-window,
  length-preserving, and passes `packer_test` → class **recovered**, not refused.
- Scoping caveat (honest bounds): global uniqueness outside the libz/docker-init ±256 windows is not
  enumerated (their `sz_unc` > 20000, so the spec's window applies). The full sweeps on jq/xxd (every
  in-range v), the mechanism (per-block stream validation: `compressed data violation`, `checksum
  error`), and the unique green at stored on every tested carrier support uniqueness globally, but the
  window bound is stated rather than saturated for those two carriers.
- The `-d`-reproduction oracle uses the pinned original sha256, which a blind repairer lacks; decidability
  does not depend on it, because the `-t` green set is a singleton — a repairer needs only the packer.

## Files written (lane)

- `.ufo/waves/round-91/w1/ReviewerFalsify.md` — this report.
- `.ufo/waves/round-91/w1/ReviewerFalsify/falsify-search.py` — the search driver (exact code that ran).
- `.ufo/waves/round-91/w1/ReviewerFalsify/falsify-search-results.json` — full per-carrier/per-cell JSON.
- `.ufo/waves/round-91/w1/ReviewerFalsify/falsify-spotcheck.txt` — spot-check log (exit 0).

Tooling: no installs or upgrades (pinned `upx` 5.2.0 and system `python3` were sufficient); no pacman
use. Scratch `/fast/scratch/hyaku/kaidoku-r91/ReviewerFalsify` deleted before yield.
