# ExecAuditBase — round-75 w1 (executor)

Seat receipt: `.ufo/waves/round-75/w1/ExecAuditBase/receipt.json` (raw run outputs alongside: `base.json`, `decl.json`, `selftest.json`, `validate.json`).

## What ran

All runs used the **frozen** instrument blob — `git show 8dff07b9:tools/round-75/record-audit.py`, git blob `44a567d5`, sha256 `bba8b8cd…` — which equals the `record-audit.py` pin in `.ufo/waves/round-75/claims.json` (freeze `ec149dc4`). The working-tree file was superseded twice mid-wave (see O2); the frozen blob was extracted to scratch and executed with `python3 -I -B`.

| run | command | exit | result |
|---|---|---|---|
| base | `--root <lane> --rev 3c15a156239af06114e1ece8d1044a0d8205379b` | 1 | `ok false`, `mismatch_count 8`, atom ids exactly D16–D23, every atom `ok false`; embedded validate block `{atoms: 8, defects: []}` |
| declaration | `--rev 8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a` | 1 | same eight mismatches — the record is not written yet |
| selftest | `--selftest` | 0 | 10 cases (`d9-negated-path-red`, `d9-exact-path-accepts`, `d9-token-grammar-red`, `d10-token-only-red`, `d10-counts-required-red`, `d11-empty-flip-red`, `d11-complete-accepts`, `d12-reversed-values-red`, `d12-bound-values-accepts`, `receipt-defects-red`), `failures: []` |
| validate | `--validate .ufo/waves/round-75/pre/c2-at-base.json` | 0 | `defects: []` |

All acceptance criteria met. No atom raised an exception at either revision (clean JSON, exit 1 both times).

## Atom-by-atom: routed defect and base falsity reason

| atom | routed defect (spot-check §6) | false at base because | mechanical? |
|---|---|---|---|
| D16_validate_embedded | 1 — C2 `--validate` conjunct had no committed landing evidence | landing receipts `l1/scores/c2-at-landing.json` + `c2-validate-at-landing.json` absent (`receipt_present=false`, `validate_receipt_present=false`) | no — absence |
| D17_s275_used_by_relog | 2 — S275 old→new logged outside the lesson | `corpus/lessons/round-75.md` absent (`lesson_present=false`, `s275_lines=0`); atom's old/new strings and the named `.ufo/waves/round-74/w1/ScribeRows.md` match defect 2 verbatim | no — absence |
| D18_canary_sole_detector | 3 — `b-drop-canary-field` cross-binding | landing battery receipt `c1-at-landing.json` absent | no — absence |
| D19_critic_classes_bound | 4a — three further A12 survivors | same receipt absent; bound (mutant → case) pairs match defect 4a exactly (`d-home-under-truthy`→`a12-genuine-field-identity`, `d-name-samples-last-wins`→`a12-sample-name-merge`, `d-lie-clean-superset`→`a12-lie-clean-keys-exact`) | no — absence |
| D20_grammar_reds | 4b — four cosmetic atom passes | receipt `l1/scores/audit-selftest.json` absent; the nine in-process grammar cases already pass at base, so only the absent-receipt conjunct fails | no — absence |
| D21_binding_and_pins | 5 — D14/D15 coverage limits | plan, claims and `pre/c1-base-arm.json` all absent at base (`plan_tools=[]`, `pinned=[]`, `runner_ok=false`) | no at base — **but structurally defective at claims-bearing revs, see D1** |
| D22_security_arms | 6 — SentinelScope SS74-1/4/5/6 (+ QUALITY 128 shim-values class) | the three selftest receipts and the landing `target_pin` absent; required case names map cleanly onto the SS74 items | no — absence |
| D23_opened_convention | 7 — retrospective rows vs row-is-a-claim | `stated=false` genuinely: base SOURCES *has* `## Search log` (line 226) but no Convention/first-opened statement; `followed=false` because the lesson is absent | no — property not yet written |

No path typos, no wrong regexes, no exceptions: every atom is false at base for the named reason (artifact absent or property not yet written).

## D20 check — the four red fixtures really reject the four cosmetic constructions

Re-ran the frozen module's parse functions directly on the exact fixture inputs:

- negated used-by token → rejected: `["negated path token: not corpus/knowledge/x.md", "no affirmative path token"]`
- token-only search line (tokens without counts) → rejected: 4× `missing integer count: …`
- rejected row with empty reason/flip → rejected: `["teaches does not carry REJECTED: <reason>; flip: <condition>"]`
- erratum that does not bind the measured values → rejected: `["erratum does not name the measured 25 rows"]`

The four constructions are exactly spot-check defect 4b's list, and the green counterparts (`d9-exact-path-accepts`, `d10-counts-required-red`, `d11-complete-accepts`, `d12-bound-values-accepts`) pass — 10/10 selftest cases green.

## D21 check — pin set vs the plan's `tools/round-75/*.py` set: **DEFECT**

- claims.json (freeze) pins **5** instruments: seam-probe, probe-mutation, record-audit, controls, freeze-pins — each sha256 equals its blob at the freeze (re-verified; D21's `pins_match` all true at the freeze revision).
- The plan text (blob `14a135b3`, byte-identical at declaration and freeze) names only **4** `tools/round-75/*.py` literals; `tools/round-75/freeze-pins.py` appears **nowhere** in the plan with the `tools/round-75/` prefix.
- Frozen D21 requires `sorted(pins) == named` → 5 ≠ 4, structurally false at **every** revision where claims exist. The landing supersessions (`4e93c1a5`, `7edb005e`) kept the same clause (working-tree line ~422). Consequence: R75-C2's "0 at the landing revision" cannot hold through D21 as things stand.

**D1 (defect, for L1):** resolve by a plan supersession/erratum naming the fifth instrument, or an atom supersession widening the plan-set extraction. Not fixed here — outside this seat's target.

## Observations

- **O1:** `pre/c1-base-arm.json` binds `runner.sha256 = d7757ae2…`, which equals the probe-mutation.py blob committed at supersessions `ad53c1e`/`0465f251` (the executed bytes), not the freeze-time blob `ec089411…` that claims.json pins; the frozen D21 runner clause (rev-blob comparison) scores that binding false at the freeze. Supersession `ad53c1e` explicitly reworked the binding to executed-runner bytes — consistent story, no action for this seat.
- **O2:** instrument drift during the run: `record-audit.py` superseded twice mid-wave (`4e93c1a5` D21 freeze-ledger clause, `7edb005e` D20 live-record parsing). All four seat runs used the extracted frozen pin blob; base/declaration outputs are byte-identical to the pre-drift runs (`diff -q` clean), so the receipts above are the frozen-audit results.

## Hygiene

No environment values written anywhere; no git/jj writes (read-only `show`/`status`/`rev-parse`/`log` only); nothing written outside `.ufo/waves/round-75/w1/ExecAuditBase{,.md}`; scratch dir `/fast/scratch/hyaku/kaidoku-r75/ExecAuditBase/` removed before yielding.
