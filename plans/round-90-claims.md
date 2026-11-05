# Round 90 — declared claims (frozen before data)

Lane: `kaidoku-shokunin`. Round 90, attempt 1. Base revision: `fc52cc9dc`
(branch `main`, the tip at declaration). Owned axes: coverage, depth,
calibration, freshness — all four sit at 10.0 on their finite proxies, so the
lowest-axis obligation is satisfied by any tied-lowest axis and no stagnation
waiver is invoked (round 88 entered a capability, so the window restarted).

Two claims, distinct axes, causally separable. Every predicate below is the same
sentence in this plan, in the counter's code and in the receipt label.

## R90-C1 — coverage (capability acquisition; Frontier → Core)

**Class `T5-chain-szcpr-wrong-later`.** A packed UPX 5.2.0 `--best` little-endian
ELF x86-64 carrier whose first contiguous `b_info` segment is intact except for
an *interior* block's `sz_cpr`, overwritten with a different in-range value
(`0 < value <= sz_unc`, both directions: stored − 7 and stored + 7). `upx -t`
answers `Exception: compressed data violation`; the round-87 anchor path reports
the file intact and the round-89 block-0 law returns the bytes unchanged
(`corpus/README.md` round-89 frontier: "later-block `sz_cpr` values").

**Target (frozen predicate).** `P1 6 of 6; P2 4 of 4; P3 4 of 4`, all controls
true, exit 0:

- **P1** — 3 carriers whose chain accounts the full `u_len` (`jq`, `xxd`,
  `docker-init`) × 2 directions = 6 cells. A cell is `recovered` only when the
  repair exits 0, every differing byte lies inside the tampered 4-byte `sz_cpr`
  window, `upx -t` answers rc 0, `upx -d` produces bytes whose sha256 equals the
  carrier pin, and REA 6.5.0 reports the original's own
  procedure/segment/string counts.
- **P2** — block 0's `sz_cpr` wrong (the round-89 class) on all four carriers:
  the new repair must compose the class it supersedes (QUALITY 161).
- **P3** — block 0's `sz_cpr` zeroed (the round-88 class) on all four carriers.
- **Controls (all required):** `N1` a plain ELF is refused; `N2` a flipped
  payload byte is never reported recovered; `N3` an intact carrier returns
  byte-identical; `isolation` each invocation's directory, listed *after* the
  child exits, holds only `in` and the repair's own `out` (QUALITY 170);
  `carrier_blind` the six P1 cells are re-scored in a `bwrap` sandbox where every
  pinned carrier path holds decoy bytes and the run root is a tmpfs, and a probe
  proves the blinding (QUALITY 168); `no_work` the unchanged round-89 repair
  scores 0 of 6 on P1; `cheat_live` the declared `cheat-repack` control
  reproduces the intact packed bytes unblinded and `cheat_killed` fails blinded.

**Counting command**

```
python3 -I -B tools/round-90/upx-later-block-battery.py --root . --rev <REV> \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch> --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" \
  --json-out <receipt>
```

**Kill rule.** Any control false, any cell short of its arms, or a label that
differs from `--expect` fails the claim. A candidate is written only when it
accounts for exactly the declared `u_len` and, where the stored chain is intact,
strictly more than the stored chain does — a filter, not a rank key (QUALITY 171).

**Separability.** C1's artifacts are `tools/round-90/*`; they cite only paths
that exist at the base (`tools/round-87/`, `tools/round-88/`, `tools/round-89/`
and the r87/r88/r89 knowledge entries), so C1 verifies without C2 landing.

**Measured limits (declared before data, not discovered after).**
- The class excludes `libz`: the shared object's chain accounts 98,592 of
  108,560 `u_len` bytes, so the exact-total rule cannot decide there and the tool
  returns the bytes unchanged. Its block-0 classes still compose (P2/P3).
- The *last* block before a chain stop is under-determined (every derived value
  that still leaves a stop before the resume offset accounts for the same total);
  the tool leaves it unchanged.
- The derivation is a scan with one `find_sentinel` per candidate: measured cost
  is reported, not claimed linear.
- A packer-validated brute force over `1..sz_unc` is an alternative mechanism
  that would also repair these cells; the counter does not force the chain walk,
  so this claim is the *capability*, not the mechanism (QUALITY 152).

## R90-C2 — depth (craft rule block 30)

**Claim.** `SKILL.md`'s `## Queue-drain craft` section gains rule block 30: the
guard-and-control set a *superseding instrument revision* must inherit, as a
decision table whose rows route each revision defect class to the guard that
answers it, each row citing the base-revision criterion it restates (QUALITY
161/163/167/168/169/170/171 and `corpus/lessons/round-89.md`).

**Target (frozen predicate).**

```
python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <REV> \
  --expect-blocks 30 --json-out <receipt>
```
→ `blocks 30, resolved 30, expect 30, unresolved []`, exit 0. Every block must
clear the counter's shape floor (≥25 words, ≥2 backticked spans) and its
citations must resolve at the measured revision.

**Base arm.** At `fc52cc9dc` the same command with `--expect-blocks 30` reports
`blocks 29 … met=False`, exit 1 (`.ufo/waves/round-90/pre/c2-depth-at-base.json`).
The citation-only stub arm is the counter's own selftest (10 cases, 0 failures).

**Separability.** Block 30 cites only documents present at the base — no
round-90 artifact — so it verifies without C1 landing (QUALITY 159).

## Do-nothing and cheap controls (both committed with the declaration)

- **No work** — the unchanged round-89 repair on P1: 0 of 6
  (`.ufo/waves/round-90/pre/c1-candidate-at-declaration.json` `controls.no_work`).
- **Provenance cheat** — `tools/round-90/control-cheat-repack.py`: live unblinded
  (reproduces the intact packed bytes) and killed blinded.
- **C2 no work** — the base arm above (29 blocks vs the frozen 30).

## Round shape

One v1 wave `r90-w1` of 13 seats (executor 4, scribe 2, scout 1, reviewer 2,
critic 1, mutation-tester 1, sentinel 1, connector 1; attack roles
reviewer/critic/mutation-tester/sentinel = 5 of 13 = 38.5 % ≥ 25 %; one
connector). The L1 holds the planner seat, which the wave validator rejects as a
frozen-topology role.

## Inherited state

Round 89's L1 (`KaidokuR89`) is still landing its own record work on this
checkout; its paths (`LOG.md`, `SCORECARD.md`, `tools/round-89/`,
`corpus/lessons/round-89.md`, `corpus/QUALITY.md`, `.ufo/waves/round-89/`) are
excluded from every round-90 write until it reports closed. The round-89
spot-check's routed defects D-89-1…D-89-7 are answered in the round-90 report
with a disposition each.
