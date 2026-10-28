# R46W1ExecGap — the round-45 discrimination gap measured live (scoped findings)

Full report, all commands, every receipt (command, exit, stdout sha256, UTC):
`.ufo/waves/round-46/w1/R46W1ExecGap/report.md` + `receipts.json`, `battery-full.json`,
`freeze-probes.json`, `lane-admissibility.json` and the four drivers in that directory. Lane tree read-only: no writes outside
`.ufo/waves/round-46/w1/R46W1ExecGap*`, no git mutation, no installs. Python 3.14.8, git 2.56.0.

## Verdict

The gap is real on committed bytes, not just quoted from round 45.

The round-45 cheapest-green forgery (`R45W1CritC1` label `fx-a6-cheapest-green`; surviving text
`.ufo/waves/round-45/w2/R45W2Lesson/fx-a6-SKILL.md`, sha256 `cc523958…`, **40** lines — the record's
"44" is not reproducible from the surviving bytes) was rebuilt into a one-commit fixture with a
`plans/round-45-claims.md` naming the round-45 frozen paths and the **real**
`tools/round-45/frozen-path-preflight.py` (sha `633ebc05…`):

| scoring | exit | `met_target` | stdout sha256 |
|---|---|---|---|
| frozen round-45 `c1-counter.py`@3182047 (`2cfc5a48…`) | **0** | **true** | `2190dce38491eaaa83866e3494a6526550d7d428e2900c3cdb0dc8b6c12b231e` |
| `attest.py --spec r45 --profile v1` @freeze bytes (`dd1e7df1…`) | **0** | **true** | `1828bf2205319256d6b92b0a8458e41706ec91831a5c41aeee5101f7ca9ac23f` |
| `attest.py --spec r45 --profile v1` @HEAD bytes (`e6c44d2d…`) | **0** | **true** | same `1828bf22…` (byte-identical) |
| control: same fixture, `--profile v2` | **1** | false | `27c7515423ab…` |

The counter's clause values on the forgery: `rule_blocks 22`, `rows 8`, `refs 4`,
`unresolved []`, `header_ok true`, `preflight_selftest cases=11 failures=0`. The 4-line-stub
variant (the critic's exact artefact) is also exit 0 / `08b01417…`. **The acceptance is the
artefact's shape, not the interpreter's identity.**

**Answer to the seat's question: yes** — the forgery round 45 accepted is still accepted by the
round-46 v1 profile, on both byte sets; `ctl-c1-1-v1-profile`'s premise is confirmed by
measurement. `--no-battery` is required for the comparison (with the battery on, `score()` demands
the r46 battery constants regardless of profile and the v1 run exits 1 for a reason outside the
round-45 predicate).

Calibration note: under `--spec r45`, the v2 code path rejects this artefact through the citation
allowlist only (`tools/round-45/…: outside the validated path set`); the garbage rows stay
invisible there because `routed`/`vocab` are r46-only. Row discrimination lives in the r46 v2
surface (block 23), not in an r45 replay at v2.

## Finding (not fixed): the freeze the file defines is not the freeze that was scored

Frozen text: freeze = `git log -1 -- plans/round-46-claims.md`; nothing in `tools/round-46/`
changes after it.

- `git log --format=%H -1 -- plans/round-46-claims.md` → `3182047…` (as the seat states).
- `git diff --stat 3182047..HEAD -- plans/round-46-claims.md tools/round-46/` → attest.py ±59,
  gate.py ±3, registry.py ±12; frozen-byte shas `attest dd1e7df1→e6c44d2d`, `gate 64626cca→847aa33b`,
  `registry 307506d5→5e16e4af`.
- `attest.py --freeze 3182047… --rev <head>` → **exit 2** `frozen_path_changed`
  `[tools/round-46/, attest.py, gate.py, registry.py]`, `restored` mislabels them as restored
  (sha `4800c402…`).
- The landing was scored against `65678df0…`, a freeze declared only in commit-message text
  ("declared as the authoritative freeze"), which the frozen file does not contain.
- Even that freeze is now broken: `0425224` (F4) rewrote `registry.py`, so both counters at
  `--freeze 65678df0… --rev 0425224…` exit **2** `frozen_path_changed [registry.py]`
  (C1 `1f75bcb0…`, C2 `4cbd87d5…`) — while `1e32827b` reports "both claims met at 0425224".
  At rev `781e19ae`, before F4, the same command exited 0 (`9494851b…`).
- Receipt-label defect: `restored` names paths whose bytes genuinely differ (directory-entry
  blob comparison), e.g. `registry.py` `db5adc02…`→`5e16e4af…`. Verdict right, label wrong.

I did not re-declare a freeze or edit frozen bytes; the L1 owns reconciliation.
