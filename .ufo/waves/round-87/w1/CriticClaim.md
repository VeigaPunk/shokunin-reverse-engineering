# CriticClaim — round 87 (kaidoku) — adversarial review of R87-C1

Critic seat, read-only on production files. Full attack log with receipts:
`.ufo/waves/round-87/w1/CriticClaim/critique.md`; receipts under
`.ufo/waves/round-87/w1/CriticClaim/receipts/`. Scratch deleted at yield.

## Verdict

**R87-C1 survives as a predicate; its difficulty rationale is falsified by measurement.** A
~60-line chain-walk-free repair ("v4": checksum-validated PackHeader + version/format l_info
cross-check + zero-surround sentinel heuristic, no `b_info` chain walk) scores the frozen
predicate identically to the committed tool: `recovered 8 of 8`, `controls_ok` all true,
`met=True exit=0` **with REA enabled**
(`receipts/cheap-v4-checksum-lite-rea.json`; REA counts 167/99/184/1268, matching
`DECLARED_ORIG` and the committed candidate evidence `evidence_id`s), and its 8 repaired outputs
are **byte-identical** to `tools/round-87/upx-magic-repair.py`'s on this population.

## Attacks and receipts (frozen counter, carrier/packer pins passed preflight)

| Cheap repair | non-REA recovered | controls | receipt |
|---|---|---|---|
| fixed offsets learned from jq | 2/8 | N1 false | `receipts/cheap-v1-fixed-offsets-no-rea.json` |
| word-at-len-36 except long zero runs (thresh 12 / 24) | 4/8 / 4/8 | N1 false | `receipts/cheap-v2-thresh12-no-rea.json`, `receipts/cheap-v2-thresh24-no-rea.json` |
| last two windows before EOF | 0/8 | N1 false | `receipts/cheap-v3-lasttwo-no-rea.json` |
| checksum-PH structural-lite (no chain walk) | **8/8** | **all true** | `receipts/cheap-v4-checksum-lite-no-rea.json`, `receipts/cheap-v4-checksum-lite-rea.json` |

A1–A3 fail on anchor-layout non-universality (libz sentinel 1859 bytes from EOF; l_info at 9284 on
libz) and/or N1 (no structural refusal). The only control any cheap rule fails is N1, and one
checksum scan satisfies it.

## Findings

- **F1 weakened:** the plan's sentence "it needs the zeroed class, which only a structural repair
  reaches" is false — the zeroed class is reached by a rule the counter cannot separate from the
  committed tool (byte-identical outputs on all 8 cases; my packing == battery packing on all 8).
  The predicate, kill rules and controls are untouched: the claim still passes as frozen.
- **F2 limits (out-of-population, jq, committed repair):** per-anchor distinct values (T3) and
  l_info-only zeroing (T4) are recovered (`upx -t` PASS, `upx -d` → pinned sha256
  `e815667…7806`); T2 + p_info.p_filesize zeroed is NOT recovered (repair restores magics only;
  `upx -t`/`-d` fail); removing the `$Info: This file is packed with the UPX` string does not
  break `upx -t` at all (outside the population's own precondition).
- **F3 confirmed declared limit:** provenance is unscored — v4 passes the review-enforced
  `--in/--out` clause too.
- **F4 counter quirk:** under `--no-rea` the label always reads "recovered 0 of 8"
  (`rea_recover` pinned false); non-REA pre-checks must read per-case arms.
- **F5:** the REA arm is not a repair discriminator — `rea_recover` is fully determined by
  `identity` (deterministic `evidence_id` per carrier across T1/T2 and across repairs).
- **F6 positive:** N1/N2/N3 each exclude real degenerate classes; packing deterministic;
  counter selftest clean.

## Axis fit

Coverage is the right axis for the Frontier→Core move; the predicate enumerates all five arms and
its "controls_ok all true" maps to exactly the three named controls — no unenumerated universal
clauses. The weakness is discriminative power above the naive control, not axis misfit. Smallest
safe correction (for a future revision, not this frozen round): freeze a saturating cheap-rule
control (v4) alongside naive-global.

## Tooling authorization

No installs or upgrades; pacman untouched.
