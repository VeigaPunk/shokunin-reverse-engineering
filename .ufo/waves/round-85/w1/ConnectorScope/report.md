# ConnectorScope — Sibling Overlap & Province Scope Scan (Round 85)

## 1. Sibling Overlap Scan (C1 & C2 Patterns)
`grep -rl --include=*.py -E 'CLAIM_NO_COUNTER_PATH|mutation-closure|declared_case|predicate-bind|PB_NO_PREDICATE'` across `*-shokunin/tools` and `scripts/`:

| Path:Line | Owning Lane | Duplicate Status |
|---|---|---|
| `kaidoku-shokunin/tools/round-74/controls.py:14,100,113` | kaidoku-shokunin | No (lane-local prior probe controls) |
| `kaidoku-shokunin/tools/round-75/controls.py:15,112,139` | kaidoku-shokunin | No (lane-local prior probe controls) |
| `kaidoku-shokunin/tools/round-79/gate-mutation.py:50,69` | kaidoku-shokunin | No (lane-local prior gate-mutation) |
| `kaidoku-shokunin/tools/round-81/record-integration.py:58` | kaidoku-shokunin | No (lane-local prior integration) |
| `kaidoku-shokunin/tools/round-82/conjunction-gate.py:287` | kaidoku-shokunin | No (lane-local prior conjunction gate) |
| `kaidoku-shokunin/tools/round-84/freeze-precheck.py:14,91` | kaidoku-shokunin | No (lane-local base instrument) |
| `kaidoku-shokunin/tools/round-84/mutation-closure.py:33,172` | kaidoku-shokunin | No (lane-local C2 frozen counter) |
| Siblings (`*-shokunin/tools` excluding kaidoku; `scripts/`) | None | 0 hits; zero sibling duplicates found |

## 2. PROVINCE.md Scope Check
`PROVINCE.md:99-102` defines Adjacent ground:
> "## Adjacent"
> "Ground the lane refuses or defers — reported to the orchestrator, never absorbed."
Lines 104-128 list unowned surfaces (malware triage, dynamic analysis, etc.). Claim surfaces are absent from Adjacent and held in **Core**:
- `PROVINCE.md:554`: `"| Reader-seam mutation closure — the three reader defects the round-72 probe reported as selftest survivors are bound to named cases | tools/round-73/packed-elf.py ..."`
- `PROVINCE.md:560-562`: `"- **Core — kernel-witness selftest case closure:** tools/round-74/seam-probe.py binds the A12 verdict, kernel-sample parsing and arm wiring to declared cases; tools/round-74/probe-mutation.py scores ten defect classes..."`
- `PROVINCE.md:622`: `"- **Core — attack gate:** tools/round-78/attack-gate.py materialises ten committed attack fixtures (.ufo/waves/round-78/attacks/), measures that the frozen round-77 instruments accept each one..."`

## 3. Sibling Round-84/85 Wave Writes Check
Grep across all sibling `.ufo/waves/round-8[45]*` directories for `kaidoku-shokunin/tools` yielded 0 hits. No sibling lane writes into or references `kaidoku-shokunin/tools/`.

## 4. L1 Recommendations
- **Claim R85-C1 (calibration):** Proceed — fully lane-local predicate-binding counter with no sibling collisions.
- **Claim R85-C2 (depth):** Proceed — lane-local mutation closure over 21 mutants in kaidoku tools, completely in Core scope.

## 5. Non-Obvious Move Synthesis
- **Evidence:** C1 checks counter paths in predicates; C2 relies on immutable 21-row `mutants.json` fixture.
- **Affected Axes:** Calibration and Depth (no negative interference on Coverage).
- **Proposal:** Synthesize C1/C2 verification: have `predicate-bind.py` confirm that fixture files referenced by claim counters exist at `$REV` and match pinned digests in the container's `fixtures` table.
- **Risks:** Unintended failure on fixtureless claims; mitigated by conditioning check on presence of `--mutants`/fixture CLI args.
- **Verification:** Run `predicate-bind.py` against `.ufo/waves/round-84/claims.json` and ensure clean exit.
