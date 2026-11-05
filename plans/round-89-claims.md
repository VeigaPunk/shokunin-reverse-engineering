# Round 89 — kaidoku — frozen plan (declared before data)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; round 89, attempt 1.
Base revision (lane branch tip at declaration): `0ec2bb4016655f605657d6e0e700ec2e6893ac27`.
Round-88 non-author spot-check (`corpus/lessons/round-88-verifier-spotcheck.md`) is the input:
its routed defects D1–D4 and D6 shape this round, and its §9 note ("all four SHONEN boxes look
checkable by a non-author") is not a promotion.

Owned axes at the round start: coverage 10.0, depth 10.0, calibration 10.0, freshness 10.0 — all
four tied on their finite proxies, so the lowest-axis obligation is met by either claim. Round 88
entered a capability, so the stagnation window restarts and no waiver is invoked.

Two claims, distinct axes, causally separable. C2's landed artifact cites only documents present
at the base revision (QUALITY 159): the base-present knowledge entries
`2026-11-04-r88-binfo-chain-geometry.md`, `2026-11-04-r87-upx-magic-tamper-repair.md` and
`2026-11-04-r86-record-agreement.md`. C1's entry is created by C1 and is not cited by C2.

## R89-C1 — coverage (capability): the wrong-value `b_info.sz_cpr` class enters Core

**Surface.** `PROVINCE.md` / `corpus/README.md` Frontier carry, from round 88, the limit "a
non-zero but wrong `sz_cpr` is left alone". This round moves that class — a block-0 `sz_cpr` that
is in range but wrong, so every arithmetic bound the packer applies passes — from Frontier to Core.

**Frozen predicate.** Over the four pinned carriers (jq, xxd, libz.so.1.3.2, docker-init), each
packed by the pinned packer (`upx 5.2.0`, sha256 `cf2f6e7c…969`) and tampered in class
`T4-chain-szcpr-wrong` (`stored - 8`, or `stored + 8` when `stored <= 8`), the round-89 repair
scores `recovered 4 of 4` under the round-89 counter's five arms
(`repair_rc0`, `field_only`, `test_ok`, `identity`, `rea_recover`), with `N1-refuse-plain`,
`N2-corrupt-payload`, `N3-intact-idempotent` and `isolation` all true, and the round-88 class
regression arm (`tools/round-88/upx-chain-battery.py`, same repair) met at 4 of 4.

**Before.** The round-88 repair on the same population and the same counter: `recovered 0 of 4`
(the round-87 anchor path reports `intact` and returns the input unchanged; the geometry gate
`sz_cpr0 != 0 → continue` skips the block), `upx -t` refusing each carrier at the payload stage.

**Counting command.**

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-89/upx-field-battery.py --root . \
  --repair-cmd tools/round-89/upx-field-value-repair.py --upx /usr/bin/upx \
  --pkg <rea-agents 6.5.0 dir> --work /fast/scratch/hyaku/kaidoku-r89/l1 \
  --json-out .ufo/waves/round-89/l1/scores/c1-at-<rev>.json --expect-recovered 4
```

**Kill rule.** The claim is killed if any of: the after run is below `--expect-recovered 4`; any
control is false; the regression arm is unmet; a case's `field_only` reports a changed byte outside
block 0's `sz_cpr` window; a case's repair invocation saw anything but the single input file; or the
receipt's `repair_sha256` differs from the frozen pin `332917f2…070`.

**Do-nothing and cheap controls (committed before this freeze).**
`pre/c1-base-r88-repair.json` (the unchanged round-88 repair, same counter, same population) and
`pre/c1-control-identity.json` / `pre/c1-control-naive.json` (the counter's builtins `identity` and
`naive-global`). A control that meets the target would mean the counter does not force the work.

**Instruments (pinned by sha256, re-hashed at the measured revision).**
`tools/round-89/upx-field-value-repair.py` `332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070`;
`tools/round-89/upx-field-battery.py` `f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720`;
composed `tools/round-88/upx-chain-repair.py` `59ee51b0e63d3e089c23cee066b637841133412cee50748d84d717d61f8a0b46`
and `tools/round-87/upx-magic-repair.py` `96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24`.

**Named limits (stated before the run, not after).** One field on four carriers; the repair does
not decompress what it repairs (the counter's `test_ok`/`identity` arms are the guard); a payload
corruption is invisible to the structural walk (selftest case `corrupt-payload-not-structural`);
the candidate scan keeps the round-88 cost profile (`M88-10`, measured at 1.02 s / 14.22 s /
221.85 s for 800 / 3,200 / 12,800 crafted candidates) — no new bound is claimed.

## R89-C2 — depth: craft rule block 29, and a depth counter whose target is an argument

**Surface.** The `## Queue-drain craft` rule blocks in `SKILL.md` (28 at base) and the depth atom
that counts them. The new block is the field-class decision table: for each `b_info`/PackHeader
field class, the refusal the pinned packer produces, the structural redundancy that makes it
recoverable or not, and the move the lane takes — with `sz_unc` (no redundancy → refuse),
`sz_cpr` zero / wrong-in-range / out-of-range (chain geometry → recover), `sz_cpr > sz_unc` and
the PackHeader classes (arithmetic gate → refuse) separated, which is the correction QUALITY 156
routed from round 88.

**Frozen predicate.** `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <measured
rev> --expect-blocks 29` reports `blocks 29, resolved 29, unresolved []`, `met_target true`,
exit 0.

**Before.** `pre/c2-depth-at-base.json` at `0ec2bb40`: `blocks 28, resolved 28, expect 29,
met_target false`, exit 1 — the counter encodes the target (QUALITY 157), so the base state is a
red arm rather than a pass.

**Kill rule.** Killed if any of: `blocks != 29`; `resolved != 29`; any unresolved item; the base
receipt is not red; the stub world (`pre/c2-control-stub-world.json`, a one-line citation-only
block appended to the real craft section) is not red; or block 29 cites a knowledge document absent
at the base revision.

**Controls (committed before this freeze).** `pre/c2-depth-at-base.json` (28 blocks vs target 29 →
exit 1) and `pre/c2-control-stub-world.json` (`blocks 29, resolved 28`, the stub refused by the
shape floor, exit 1).

**Instruments.** `tools/round-89/depth-blocks-v2.py`
`359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`; supersedes
`tools/round-88/depth-blocks.py` `458eeabdfd6209031e12b9081cbbe48d94d18763686db51f0d48f721507c7d5b`
(target-blind, kept as the round-88 record).

**Shape floor (declared).** A block counts only with `MIN_WORDS 25` and `MIN_SPANS 2`; measured at
base, blocks 1–28 range 39–2,902 words and 2–354 spans, so the floor removes nothing at base and
rejects the one-line stub.

## Frontier step (§2b)

- `corpus/SOURCES.md` census before: `pre/sources-census-before.txt`, exit 0, 215 rows.
- At least one source opened this round for C1's entry: the UPX v5.2.0 sources that bound the
  field (`src/p_lx_elf.cpp`'s `corrupt b_info` checks and/or `src/packhead.h`), with the URL,
  access date and a ≤25-word located quote in the lesson's `## Gate`. Rejections stay as rows.
- One mistake mined into `corpus/lessons/round-89.md` `## Mistakes` with class · evidence ·
  captured-by · fix, from the round-88 spot-check's routed defects (D1 docstring-vs-code,
  D3 target-blind counter, D4 answer-beside-input) and this round's own findings.
- Sourced claim: R89-C1's knowledge entry cites a `S###` row opened this round.

## Round shape

One v1 wave `r89-w1` of 12–14 seats under `scripts/hyaku/ufo-wave-policy.json` (band 8–16), attack
roles ≥ 25 % (reviewer, critic, mutation-tester, labrat), one connector; the L1 holds the planner
seat (the validator rejects `planner`). Residual call: none planned.

## Pre-freeze finding (candidate arm, before the freeze)

The first candidate of `tools/round-89/upx-field-value-repair.py` scored `recovered 4 of 4` on the
class with every control true but the **round-88 class regression arm unmet**
(`pre/c1-candidate-first-run.log`: `recovered 4 of 4 … met=False exit=1`): it derived the field
without composing the round-87 anchor path, so a magic-tampered carrier — the round-87 class — was
returned unchanged and the nested round-87 counter scored 0 of 8. The composition is now explicit
in `repair()` (anchor path first; on its refusal the derivation runs on the original bytes, and the
corrected bytes are re-validated through the anchor path), the selftest case
`magic-class-composed` covers it, and the declaration-time receipt carries the regression arm met.
This is the round's mined mistake (M89-1) and the reason the regression arm is part of the frozen
predicate rather than a separate no-harm claim.
