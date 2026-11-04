# ReviewerC1 — R88-C1 attack report (round 88, kaidoku, 2026-11-04)

Scope: attack R88-C1 (chain-geometry repair of a zeroed first `b_info` `sz_cpr`,
`tools/round-88/upx-chain-repair.py`, counter `tools/round-88/upx-chain-battery.py`).
Method: every attack was implemented as a repair command in scratch and scored with the
**frozen counter, unchanged** (`--repair-cmd` pointed at my scripts). No lane file outside
this seat dir was written. No tools were installed or upgraded (host `upx 5.2.0`,
`python3`, `node` only). Receipts: `attacks/results/*.json` (this dir), copied out of
scratch before its deletion.

## 0. Pins and freeze state (measured)

All sha256 measured this session and equal to `claims.json` pins: upx `cf2f6e7c…`,
carriers jq/xxd/libz/docker-init `e8156675…/7b1e5d0c…/6c78c5e5…/0bd49c8d…`, REA
package.json `a5003023…`, instruments `59ee51b0…/a01ed622…/0e055486…/458eeabd…`,
r87 module `96da7d8e…`, r87 counter `0f2d2bd8…`. Lane HEAD `d190c5b5739eae8f…`,
tracked tree clean; frozen instruments unchanged since freeze. Untracked in the lane:
`tools/round-88/field-tamper-matrix-v2.py` and wave state dirs (L1/wave work, not the
frozen instruments).

## 1. Claim reproduction (frozen counter, claimed repair)

Command (exact, per run; `<REPAIR>`/`<TAG>` varied per row below):

```
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-88/upx-chain-battery.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --repair-cmd <REPAIR> --upx /usr/bin/upx \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <SCRATCH>/work-<TAG> --json-out <SEAT>/attacks/results/<TAG>.json \
  --evidence-dir <SCRATCH>/results/rea-<TAG>
```

Result for `<REPAIR> = tools/round-88/upx-chain-repair.py` (rerun by this seat):
**`recovered 4 of 4`, controls_ok all true, regression `8 of 8` met, `met_target=True`,
exit 0** (196.9 s) — the predicate reproduces independently. Ground truth measured on
my own fixtures (`attacks/manifest.json`): true block0 `sz_cpr` jq 252, xxd 249,
libz 201, dinit 226; the claimed repair derives exactly those (checked via `--json`) and
its outputs are byte-equal to the clean packed files. libz chain accounts 98,592 of
`u_len` 108,560 — named limit 1 confirmed.

## 2. Attack A — cheaper derivation rules (each scored by the frozen counter)

| rule (as implemented in `attacks/rules/`) | score | exit | failure mode | verdict |
|---|---|---|---|---|
| R1 first-plausible (smallest structural candidate; no sentinel reach, no u_len) | `recovered 3 of 4` | 1 | dinit `test_ok` (fill 136 ≠ 226) | falsified as sufficient |
| R2 u_len key over the contiguous segment walk (no sentinel reach, no resume) | `recovered 3 of 4` | 1 | dinit `test_ok` (136) | falsified as sufficient |
| R3 sentinel-only, smallest reacher (no u_len preference) | `recovered 3 of 4` | 1 | dinit `test_ok`: `upx: Exception: compressed data violation` (136) | falsified as sufficient |
| R4 `sz_cpr := p_blocksize` | `recovered 0 of 4` | 1 | all `repair_rc0` (composed r87 pass refuses the fill) | falsified |
| R5 `sz_cpr := c_len - 12*blocks` | `recovered 0 of 4` | 1 | all `repair_rc0` | falsified |
| R6 global scan-and-fill (whole-file, no bounds/sentinel) | `recovered 0 of 4` | 1 | all `test_ok` (fills 65/65/35/4) | falsified |
| R7 packer-oracle (ascending structural candidates, `upx -t` accepts) | **`recovered 4 of 4`, met=True** | **0** | — | **passes — see §3** |
| R8 r87-class-only (no geometry at all) | `recovered 0 of 4` | 1 | all `repair_rc0`; regression 8/8 met | see §4 |

All eight runs had N1/N2/N3 true; all variants compose the frozen r87 repair, so every
regression arm read `8 of 8, met` — the regression arm does not separate any of them.

Measured facts behind the table: p_blocksize is per-carrier (9561/21717/63157/575549),
not a constant; `c_len == PackHeader offset` on all four carriers, so R5 is off by
orders of magnitude; dinit carries a decoy at derived = 136 inside block0's payload that
is **sentinel-reaching** (R3 accepts it) and defeats R2's u_len key. On jq/xxd/libz the
first structural candidate already equals the true value (R1 matches 3 of 4): the full
sentinel+u_len machinery only changes the outcome on dinit. No cheaper *structural*
rule scores 4/4 on this population; the claimed combination is the minimal winner among
the variants tried.

## 3. Attack B — the packer-oracle forge (R7): the label is forgeable

R7 does no chain geometry: it enumerates structural candidates in ascending offset
order, patches the 4 bytes, runs `upx -t` on the result, and keeps the first candidate
the packer accepts; the file is then served through the composed r87 anchor repair.
Oracle cost measured: **1 upx call per carrier on jq/xxd/libz, 2 on dinit**
(`attacks/results` probe; dinit candidate 136 fails `compressed data violation`, 226
passes). Frozen-counter result: **`recovered 4 of 4`, controls true, regression 8/8,
exit 0** — byte-identical outputs to the claimed repair on every carrier (per-carrier
`repaired_sha256` equal: jq `e8b6c9e7…`, xxd `1727faf9…`, libz `a9c544e6…`,
dinit `b67ce1bd…`).

Cheapest passing rule's exact command (persistent copy of the scratch script):

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1/attacks/rules/R7-oracle.py \
  --in <tampered> --out <output>
```

Verdict: **counter limit, not artifact falsification.** The claimed artifact does derive
the true values; the counter, however, cannot distinguish geometry from packer-oracle
search because it scores bytes. Named limit 3 ("reads the original carrier and re-packs
it") understates the surface: R7 reads no carrier at all — the tampered file plus `upx`
on PATH suffices. The kill-rule clause "a repair that names, reads or hashes a carrier
source path or pin" is audit-only (no machine check in the counter) and does not cover
packer-oracle use.

## 4. Attack C — arm satisfaction without the claimed work (measured)

- **`field_only` passes under a no-op: YES.** The frozen `identity` control receipt
  (`.ufo/waves/round-88/pre/c1-control-identity-at-base.json`) shows `field_only: true`
  on all four carriers (output == tampered ⇒ zero differing bytes); my R6 runs (rc 0,
  wrong fills) also pass `field_only`. `field_only` alone certifies nothing; only the
  conjunction does.
- **`identity` while `upx -t` fails: no counterexample found.** Arms are independent and
  conjoined; in every variant run where the fill was wrong, `test_ok` and `identity`
  failed together. A case needs all five arms; no single arm recovers it.
- **Regression arm satisfied by an r87-class-only repair: YES.** R8 (real path, serves
  only the magic class): main `recovered 0 of 4`, all controls true, **regression
  `8 of 8` met, rc 0, exit 1**. The regression arm carries zero information about the
  T3-chain class; it only guards the magic class.

## 5. Attack D — predicate / label / kill-rule drift

1. **Prose ordering contradiction in the claim sentence (named drift).**
   `plans/round-88-claims.md` R88-C1: "the **smallest** offset above `block0 + 12` that
   forms a plausible `b_info` … whose own chain reaches the end-of-chain sentinel yields
   `sz_cpr`" — on dinit the smallest sentinel-reaching candidate is 136 and is **wrong**
   (R3 measured: `upx -t` fails). The operative rule is the next clause ("the winner is
   the one that accounts for the most of … `u_len`", key `(fits_u_len, total,
   -derived)`), which the code and the prompt one-liner both implement and which
   selects 226. The "smallest … yields" clause is falsified as a derivation on the
   round's own population; harmless only because the selection clause overrides it.
2. **"under block0's method" is narrower than the code:** candidates accept block0's
   method *or* the PackHeader's method (`d[s1+8] in (m0, ph["method"])`). Measured
   `m0 == ph.method` on all four carriers (2/2/2/8), so the extra arm is unexercised
   here — wording drift, no behavioral difference on this population.
3. **"a candidate claiming more than `u_len` is impossible"** — the code deprioritizes
   (`fits` flag first in the key) but does not reject; a non-fitting candidate still
   wins when no fitting candidate exists. All four winners fit (30,800 / 38,928 /
   98,592 / 851,288 ≤ `u_len`).
4. **Label and arms match.** Receipt `label` is literally `recovered 4 of 4`; the five
   arms (`repair_rc0, field_only, test_ok, identity, rea_recover`) and the three control
   keys match the predicate enumeration word-for-word; "regression … its controls true"
   matches the r87 counter's `met_target` (which includes its controls).
5. **Counter wart (builtin repairs):** for `--repair-cmd identity|naive-global|
   r87-anchor` the regression arm is *unevaluable*, not measured — the builtin name is
   passed as a file path to the r87 counter (`missing_repair: …/r87-anchor`, rc 2;
   visible in `c1-control-r87-anchor-at-base.json` `regression.rc=2`). The plan's
   controls table makes no regression claim for builtins, so no falsehood — but the
   r87-anchor control did not exercise the regression arm.
6. **`--no-rea` cannot score partial arms:** with REA disabled `rea_recover` is forced
   false ("REA disabled") for every case, so any recovery measurement requires the REA
   pin to hold (calibration property, matches the predicate's REA requirement).

## 6. Verdict summary

- **R88-C1 claim (artifact + predicate + label): SOUND.** Independently reproduced
  end-to-end (`recovered 4 of 4`, controls, regression, exit 0); derived values equal
  ground truth measured from my own fixtures; outputs byte-equal clean packed files.
- **Counter: LIMIT.** The label is forgeable by the packer-oracle repair (R7) with
  byte-identical outputs; provenance is unscored and the carrier-pin kill clause is
  audit-only. Recommend the round record the R7 shape (it is cheaper and stronger than
  the carrier-repack shape admitted by named limit 3).
- **Plan text: DRIFT** in items 5.1–5.3 (smallest-clause ordering; "under block0's
  method"; "impossible" vs deprioritized).
- **Capability cheapness:** no cheaper structural rule reaches 4/4 on this population;
  dinit's sentinel-reaching decoy at 136 is the sole separator. The claim's capability
  is real, but its population is one carrier deep for the hard part of the rule.

## 7. Residual risk and verification gaps

- Population depth: the sentinel+u_len combination is load-bearing on exactly one
  carrier (dinit); a fifth carrier could re-separate R1/R2/R3. Named limit 2 admits the
  one-class scope; the *rule-selection* evidence is one carrier deep.
- REA declared counts (167/99/184/1268) accepted from round-70 corpus (dinit 1268
  spot-checked in `corpus/README.md` r70 receipts); jq/xxd/libz numbers were re-exercised
  by the counter's REA arms (all true) but not independently re-derived.
- R7 was measured with `upx` from `PATH` under the counter's four-key child env; a
  counter that required a geometry record or hashed provenance would close it. The
  frozen counter does not.
