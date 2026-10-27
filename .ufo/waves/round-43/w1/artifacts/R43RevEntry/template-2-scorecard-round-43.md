# Template 2 — SCORECARD `## Round 43` section

Mirrors `## Round 42` (`SCORECARD.md:3469-3487` at base `6b9e64fe`). The claim
table columns are exactly the round-42 seven:

`| claim | axis / surface | before | after | counting command | measured at | verdict (author) |`

followed by the `Owned scores:` paragraph, the optional capability table, the
`- **planned (round 44, after a steer):**` bullet and `- **retired:** none.`

```markdown
## Round 43 — <one-line round summary: e.g. triage table v4 re-scored 78/78 on a fresh freeze-seeded held-out set under a refusing generator; the 18 host-local SOURCES rows became resolvable from in-lane copies>

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`; freeze `<<L1:FREEZE>>` (`plans/round-43-claims.md`, every round-43 tool, the round-42 frozen v4 tools and fixtures, the SKILL v4 table region, the S135 row, the wave-1 evidence); controls `<<L1:controls hash>>`; data `<<L1:data hash>>`; measured revision `<<L1:REV>>`; scores `<<L1:scores hash>>`. Wave 1: <<L1:N>> seats (`.ufo/waves/round-43/w1/`). Lesson `corpus/lessons/round-43.md`.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R43-C1 | depth — SKILL rule block 21 (`<!-- sqfs-triage-table v4 -->`, 13 columns, 15 rules), interpreter `tools/round-42/sqfs-triage-v4.py`, evaluator `tools/round-42/indep-eval-v4.py`, round-43 generator `tools/round-43/heldout-gen-v4r43.py` that refuses a manifest whose declared tuple differs from its own observed `--run` | exit 2 `no_manifest_at_rev` at the freeze (CTL-C1-0, `.ufo/waves/round-43/controls/c1/`); the round-42 manifest copied to the round-43 path rejected (CTL-C1-1, seed ≠ freeze); the round-42 C02 manifest refused by the frozen tuple check, exit 3, red receipt (CTL-C1-2); round-42 shortcut controls re-scored by the frozen round-43 counter stay below 78 (CTL-C1-3) | `matched <<L1:matched>>` of `n 78`, `observed_features_match_declared true`, `combo_unseen_majority <<L1:x>>` of 24 on the frozen lookup control, every binding true, `frozen_path_changed []`, exit `<<L1:exit>>` (`.ufo/waves/round-43/l1/scores/c2-at-<<L1:REV>>.json`, `counter_sha256 <<L1:…>>`, `counter_sha256_at_freeze <<L1:…>>`) | `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <<L1:FREEZE>> --json-out <OUT>` | `<<L1:REV>>` | **met** |
| R43-C2 | coverage — `corpus/SOURCES.md` rows S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079 S081 S082 S083 S090 S092 (host-local URL cells), `tools/round-41/local-source-gate.py`, map `corpus/evidence/local-sources.json`, copies under `corpus/evidence/round-43/local-sources/` | gate exit 1, `rows_failed` length 18 at the freeze (CTL-C2-0 committed receipt); a sandbox-clone control with an absent/digest-mismatched copy keeps the gate red (CTL-C2-1) | gate exit 0, `rows_failed []`, `rows_total <<L1:N>>` ≥ 129, 17 in-lane copies plus the preserved S126 entry and the map committed, every copy digest re-verified against the live host object it copies (receipt at the measured revision) | `python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV>` (exit 0; `jq '.rows_failed | length' <receipt>` prints 0) | `<<L1:REV>>` | **met** |

Owned scores: coverage 10 → 10 (map proxy 135/135 → <<L1:N>>/<<L1:N>>, command A at `<<L1:scores hash>>`); depth 10 → 10 (rule blocks 21 → 21; the claim re-scores the frozen block-21 table, so no rule-block count moves); calibration 10 → 10 (no calibration claim). Saturation line and stagnation window unchanged; a perfect finite proxy retires no axis. Capability row entered: **<none new this round, or name it>**. <No capability row for triage v4 scoring unless the L1 judges the re-score a new capability — the round-42 card entered none for v4.>

<Optional, only if a capability is demonstrated: `### Capability addition (demonstrated before this row)` + the 4-column table `| Capability | What it can now do | Evidence pointer | First-working round |`.>

- **planned (round 44, after a steer):** <from the round-43 closure / wave-2 routed defects; carry the open items: R42-CL2's wave-2 attack on the round-42 C1 landing if not run this round; R40-CL2 remains open unless closed.>
- **retired:** none.
```

Format notes the L1 must keep:
- The `Base … freeze … controls … data … measured revision … scores …` header paragraph is one line, commit hashes abbreviated the way round 42 abbreviated them (`b024051c`, `d4b4b4fb` style — 8 chars where unambiguous).
- `before` cells name the control receipt ids (CTL-C1-0 etc.) and their exits; `after` cells quote the measured numbers from the score receipt, not from memory.
- The verdict column carries the author verdict only (`**met**` / `**not met — honest stop**`); the non-author closure verdict lives in the fleet report, not here.
- Every score receipt records the scorer's exit code and `counter_sha256` plus `counter_sha256_at_freeze` (round-41 closure D4, carried in `plans/round-43-claims.md` §Freeze-integrity rule).
