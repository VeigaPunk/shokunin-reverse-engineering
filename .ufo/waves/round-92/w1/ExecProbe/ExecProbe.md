# ExecProbe — R92-C1 premise probe (independent of the candidate)

Seat: `ExecProbe` (executor), round 92 wave 1, lane kaidoku.
Question: can the packer verdict `upx -t` decide the last-block stop-boundary
window repair — i.e. is a green (`rc 0`) **unique** at the pristine `sz_cpr`
inside the declared ±16 window? Measured independently of any repair tool.

Measured at declaration commit `11f8606178dfd9e72001b31daf412c5463106a63`
(clone, `--shared`, checkout; lane tip equals it). Layout helpers loaded by
path from the frozen counter's own imports (`tools/round-87/upx-magic-repair.py`
`find_packheader`, `tools/round-88/upx-chain-repair.py` `l_info_candidates`,
`tools/round-92/stop-boundary-battery-v2.py` `CARRIERS`/`layout`/`env_for`).
Pin checks before any cell: upx sha `cf2f6e7c…a8c969` = frozen pin; all five
carrier sha256 = `CARRIERS` pins. Green rule: `upx -t -q` rc == 0 on a private
copy, counter env discipline (`LANG=C`, `HOME`/`TMPDIR` under scratch).

Command (exit 0):
```
TMPDIR=$S/tmp PROBE_ROOT=$S/clone PROBE_WORK=$S/work \
  PROBE_OUT=<seat>/premise.json python3 -I -B $S/work/probe.py
```
(`$S` = `/fast/scratch/hyaku/kaidoku-r92/ExecProbe`, deleted before yield; the
probe script was the only file in `$S/work` and is reproduced by this report.)

## Verdict: premise HOLDS on all five carriers

Every window scan, far cell and candidate-geometry scan behaves exactly as the
R92-C1 premise requires: **exactly one green value, equal to the stored
`sz_cpr`**; every other value in the scanned range is red (rc 1,
`Exception: compressed data violation`).

| carrier | pack deterministic | packed sha256 (run 1) | blocks | last-block off | stored | sz_unc | window greens (33 cells) | greens at −40 / +40 | cell s (min/mean/max) | geometry ±7 greens |
|---|---|---|---|---|---|---|---|---|---|---|
| jq | yes | `e8b6c9e76b542435…` | 5 | 9911 | 174 | 1184 | `[174]` | red 134 / red 214 (rc 1) | 0.002/0.0021/0.0031 | `[174]` both |
| xxd | yes | `1727faf91c381302…` | 5 | 15455 | 163 | 784 | `[163]` | red 123 / red 203 (rc 1) | 0.002/0.0022/0.0032 | `[163]` both |
| libz | yes | `a9c544e6da4f9341…` | 3 | 43103 | 17012 | 23584 | `[17012]` | red 16972 / red 17052 (rc 1) | 0.0022/0.0024/0.0031 | `[17012]` both |
| dinit | yes | `b67ce1bdda27880a…` | 5 | 348349 | 4313 | 27304 | `[4313]` | red 4273 / red 4353 (rc 1) | 0.0052/0.0054/0.0058 | `[4313]` both |
| xz-unseen | yes | `a7b4d929441c0167…` | 5 | 41726 | 852 | 5024 | `[852]` | red 812 / red 892 (rc 1) | 0.0022/0.0024/0.0035 | `[852]` both |

- Determinism: two `--best -q` packs per carrier produced identical sha256
  both times (`pack_deterministic: true` in `premise.json`); pack times
  0.005–0.497 s. Consequence: the packed image — and therefore the stored
  value and every cell verdict in this probe — is stable across runs, so the
  frozen counter's fresh packs measure the same images this probe did.
- Geometry scans are the candidate's true decision set: on a −7 / +7 tampered
  image the candidate would scan `[stored±7−16, stored±7+16]` (33 cells each,
  measured fully); greens are exactly `[stored]` there too. The declared ±16
  window scan around `stored` plus the two geometry scans jointly cover
  `[stored−23, stored+23]` for every carrier — 165 tamper-relevant cells over
  the five carriers, one green total per carrier.
- Per-cell time includes file write + subprocess: ~2 ms (small carriers) to
  ~5.5 ms (docker-init); a full 33-cell window costs ≲0.18 s, so the
  candidate's ±16 search is cheap (≈35 cells ≈ 0.1–0.3 s per input).

## Attack: what would falsify "exactly one green = pristine value"

The premise dies if any of these appear, none did:

1. **A second green inside the window** (any `v ≠ stored` with rc 0) — the
   candidate would face ambiguity and must type-refuse; with two greens at
   e.g. `stored−1`/`stored` the "exactly one green" gate never opens and
   `repaired` collapses to 0. Plausible mechanism: a decompressor that stops
   at the stream end marker and ignores `sz_cpr` — then every `v > stored`
   would decompress correctly and be green. The data kills this: `stored+1`
   is red everywhere (`compressed data violation`), i.e. UPX enforces the
   exact consumed-size end condition, not just stream-end. This was the
   single most dangerous failure mode and it is empirically excluded.
2. **A green far value** (`stored±40`) — would show the verdict accepts wrong
   sizes at distance, making the window rule arbitrary. Both far cells are
   red (rc 1) on all five carriers.
3. **Geometry greens ≠ `[stored]`** — would mean the battery's own ±7 tamper
   produces a decision set with zero or multiple greens (repair impossible or
   ambiguous). Measured: exactly `[stored]` on all ten scans.
4. **Pack nondeterminism** — would detach the probe's image from the
   counter's fresh packs. Excluded: identical double-pack sha256 on all five.

Residual limits (not premise-breaking, declared for honesty): the oracle is
unique *for this UPX 5.2.0 build (pinned sha) on these five images*; the
libz shared-object chain has 3 blocks vs 5 elsewhere, and its stored value
(17012) is the only one where `stored+40` stays well inside `sz_unc` — both
still single-green. A carrier *outside* these five (or a UPX rebuild) is not
covered by this probe; the unseen-carrier limit in claims.json (`xz`, not a
proof) applies to this measurement too.

## Deliverables

- `premise.json` — full record: commit, upx version+sha, per-carrier packed
  sha256 ×2, layout, every cell (v, rc, green, seconds, upx message), scans,
  verdicts. Written directly to this seat dir by the probe.
- `ExecProbe.md` — this report.

Lane untouched (read-only: reads of plans/, claims.json, tools/, and a
`--shared` clone in scratch). No installs were needed (python3 + pinned upx
sufficed). Scratch `/fast/scratch/hyaku/kaidoku-r92/ExecProbe` deleted before
yield. Exit codes: probe 0; no failed commands.
