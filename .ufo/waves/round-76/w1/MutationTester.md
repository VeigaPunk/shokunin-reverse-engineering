# MutationTester — round 76 w1 (seat MutationTester-3)

Scope: the two round-76 instruments' own checks (`tools/round-76/record-audit.py`,
`tools/round-76/plan-command.py`). Nine single-point mutants were built on scratch
copies under `/fast/scratch/hyaku/kaidoku-r76/MutationTester-3/` (lane bytes never
modified) and each was scored by running the instrument's declared `--selftest`
(`python3 -I -B`, stdin `/dev/null`). Receipt:
`.ufo/waves/round-76/w1/MutationTester/receipt.json` (copy:
`.ufo/waves/round-76/w1/MutationTester-3/receipt.json`).

## Baselines (both green before any mutation)

- `record-audit.py --selftest`: rc 0, 17 cases, failures `[]`.
- `plan-command.py --selftest`: rc 0, 3 cases, failures `[]` — run at the
  declaration rev `be99e4f9`: the gate selftest `git show`s
  `.ufo/waves/round-76/pre/fixtures/r75-printed.md`, which does not exist at base
  `5303a662` (there it exits 2 unevaluable). Harness note, not a defect.

A mutant is killed when ≥1 declared case fails. `sole` = the failing set is
exactly the declared single detector.

## Scorecard (4 killed, 5 SURVIVORS)

| # | mutant | mutation (one point) | rc | failures | verdict | sole |
|---|--------|----------------------|----|----------|---------|------|
| a | d24-a | accept a row absent from the table | 0 | — | **SURVIVOR** | — |
| b | d24-b | drop evidence-pointer existence check | 1 | cap-absent-evidence-path-red | killed | yes |
| c | d24-c | drop first-working-round check | 1 | cap-round-mismatch-red | killed | yes |
| d | d24-d | drop stub-description check | 1 | cap-stub-description-red | killed | yes |
| e | d24-e | line-level claim parsing | 0 | — | **SURVIVOR** | — |
| f | gate-f | skip static placeholder scan | 1 | prose-plan, ellipsis-rev | killed | no (two detectors) |
| g | gate-g | accept `shell=True` | 1 | missing-required-arg | killed | yes (indirect) |
| h | gate-h | drop containment on `$OUT` | 0 | — | **SURVIVOR** | — |
| i | gate-i | drop argv allowlist | 0 | — | **SURVIVOR** | — |

## Survivor mechanisms (coverage findings, not contract changes)

- **a (guard-masked).** `cap-absent-row-red`'s fixture uses an *empty* table, so
  the `if not table: return ["the ## Capabilities table holds no data rows"]`
  guard fires identically on pristine and mutant — probe shows equal defect
  lists. The absent-row check itself has no case: no fixture claims a name that
  is missing from a *populated* table. Adding one row to the fixture's table
  (claimed name absent) would make the case discriminate.
- **e (no wrapped-claim fixture).** The paragraph grammar exists for the round-75
  shape: the claim sentence wraps and the name straddles the wrap
  (`` `A12 case-independence\nclosure` ``). Probe on that exact shape: pristine
  parses `["A12 case-independence closure"]` with zero defects; the line-level
  mutant parses `[]` and emits a **false defect on a correct record**
  ("round 75 claim line 9 names no capability"). All 17 declared cases use
  single-line claims, so the live behavior change is invisible to the selftest.
  A red/accept pair with a wrapped claim would close this.
- **h (unexercised $OUT containment).** All three gate controls build `$OUT`
  inside `--work`; `containment(out, work)` never bites in `--selftest`. The
  containment refusal arms live in the round-75 freeze-pins selftest (D22), not
  here. A control whose `$OUT` resolves outside the work root would kill it.
- **i (unexercised allowlist).** `prose-plan`/`ellipsis-rev` are refused
  statically before `build_argv`; `missing-required-arg` runs a
  `tools/round-76/` script. The prefix check only bites in battery
  `arm_fixture` (`allow_prefix="tools/round-75/"`), which `--selftest` does not
  run. A control pointing `$…` at a script outside the allowed prefix would
  kill it.

## Kill notes

- **f** removes both placeholder sub-checks, so both declared placeholder cases
  fail (`prose-plan`, `ellipsis-rev`) — `sole: false`. Sub-finding: the
  `UNBOUND_RE` (angle placeholder) half alone would **survive**: the
  `r75-printed` fixture carries a Unicode ellipsis, never an `<…>` placeholder.
- **g** is a real but *indirect* kill: `subprocess.run(list, shell=True)` makes
  `sh -c` execute bare `python3` (argv[0] only), so the declared rc-2 shape
  (`{"unevaluable": "--rev is required"}`) collapses to rc 0 +
  `RECEIPT_UNREADABLE`; `missing-required-arg` fails on the rc, not on a shell
  refusal. The gate's no-shell property is enforced only accidentally by the
  rc-2 expectation. Run with stdin `/dev/null` to keep the bare REPL at EOF.
- **b, c, d** are textbook kills, each by exactly its declared case.

## Restoration / hygiene

- Pristine sha256 (before and after, lane working tree):
  `record-audit.py` `18b2d7ba2adbe4f34603d86a15fa071ccba5dc6fcea868939f219ab8eece855d`,
  `plan-command.py` `4766df5091cc53138e0f5841c31f9549aaa9c5818272ca5ff1498374888bed72`
  — verified unchanged after all runs; no lane production file touched; no git
  writes anywhere. Mutant sha256s are in the receipt. Scratch dir
  `/fast/scratch/hyaku/kaidoku-r76/MutationTester-3/` deleted before yield.
- No tools installed or upgraded (none needed).
