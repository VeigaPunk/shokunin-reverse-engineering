# MutReaders — round 71 frozen mutation probes

Axes: coverage (environment/isolation/binding seams), calibration (false-green resistance), operability (bounded reproducible detectors and exact restoration).

Freeze: `b827a8b5d54f2885ec9be7786389f356c59226ce`. Read the round-70 verifier spot-check, including routed defects and the six lying-field evidence gap. This probe changes no lane instrument or contract.

## Method and scope

Nine single-seam mutants in owned scratch only. `results.json` records actual pristine/mutated/restored selftests and fixture detectors, including stdout/stderr, exit codes, and hashes. All pristine and restored selftests exit 0; all pristine and restored behavioral detectors return `ok: true`. Route selftest inventory: 31 cases. Probe selftest outputs are retained verbatim.

`detector.py` is retained as executable method evidence, and `a.patch` through `i.patch` retain every mutation. The detector imports frozen target copies and executes their actual functions/source statements; it does not recreate the arm predicates. **This is bounded seam/fixture execution, not a full REA/UPX end-to-end probe invocation.** A8 executes the complete source arm block with a deterministic producer fixture writing a polluted raw log and a falsely clean summary. A9 executes the actual arm assignment with colliding directory fixtures. A10 executes the complete source block using the frozen route's real `nonce_clauses` for the receipt-check boundary. Thus any arm-flip statement below is fixture-scoped, not a 10/10 production-run assertion.

The initial detector attempt failed at selecting the wrong `run_root` AST assignment (NameError on receipt); that attempt is inconclusive, and its finally block restored all target bytes. The corrected detector selected the score assignment and then completed all nine baseline/mutated/restored sequences. No baseline failure is counted as a kill.

## Scores

| mutant | frozen lines | defect | built-in selftest | added behavioral detector |
|---|---|---|---|---|
| a | route:200 | inherit dict(os.environ), then override allowlist | killed; child-env-allowlist, observed-env-allowlist | killed |
| b | route:295 | omit launcher PYTHONCOERCECLOCALE pop | not-killed; exit 0 | killed |
| c | route:768 | fixed --work/packed-fixed root | not-killed; exit 0 | killed |
| d | route:370 | omit missing-nonce rejection | killed; nonce-clause-absent | killed |
| e | route:359 | hash nonce only | killed; run-binding-derives | killed |
| f | route:347-348 | all_allowlisted=True | killed; observed-env-canary | killed |
| g | probe:356 | allow superset raw environment keys | not-killed; exit 0 | killed |
| h | probe:446,452 | remove both distinctness predicates | not-killed; exit 0 | killed |
| i | probe:471 | binding_ok=True | not-killed; exit 0 | not-killed |

## Observations

- a: the parent-key canary is inherited. The selftest catches both `child-env-allowlist` and `observed-env-allowlist`.
- b: actual launcher invocation of `/usr/bin/env` shows `PYTHONCOERCECLOCALE` in both logged and executed key sets; pristine/restored have exactly four keys. Built-in selftest misses launcher execution.
- c: executing the real root-allocation statement three times yields distinct=3 pristine/restored and distinct=1 mutated. Built-in selftest never exercises allocation. This is an allocation fixture, not an actual concurrent packer run.
- d: an otherwise clean receipt without run_nonce yields `['run_nonce absent']` pristine/restored but `[]` mutated. Built-in `nonce-clause-absent` kills it too.
- e: nonce-only hash is `271a413bd339c5709fdceaec41f14f11e9fbfb5042d72d331c65f32b284cd09a`, not independently derived `48b846b5344e17d4bcb22bfb06792fa3a09443bc47f2053d99c0e803250a7c4c`.
- f: raw EXTRA key remains visible but summary falsely says all_allowlisted=true; `observed-env-canary` also kills the mutant.
- g: polluted raw records for upx/node/readelf plus a clean-looking summary make A8 flip false -> true -> false across pristine/mutated/restored. Extra key is not the exported canary, isolating the exact-key-set clause.
- h: three duplicate battery dirs and duplicate route roots make A9 flip false -> true -> false. Other shape/status/ownership conditions remain satisfied.
- i: A10 direct binding observation flips binding_ok=false -> true, but **the overall arm does not flip**: genuine_rc remains 1 because the frozen route rejects the broken binding. The complete A10 arm stays false in all three phases. This mutant survives the added detector; it demonstrates redundant protection for this fixture, not false acceptance by A10.

## Restoration and custody

Frozen route SHA256: `5cf95aaa0892c4e4f1b82edb60590b57e6667467ed607b15989bb867e7d8efe0`.
Frozen probe SHA256: `7c7734af66f571618bb948f90a5d2d7048f245de122f294574939970db1bf157`.
Both match claims.json pins. Each of nine copies was restored, tested in restored state, and subsequently overwritten again with fresh `git show` bytes. `restoration.json` records git-derived and restored SHA256 equality for all nine. `results.json` records each mutant SHA256. Evidence was copied to this findings directory before scratch removal; scratch paths inside receipts are historical run pointers, not evidence locations.

No tools installed/updated; no git mutations; no source or sibling changes. Findings are confined to this seat directory. The conflicting sibling report trailer is intentionally satisfied by this report inside the explicitly permitted seat directory rather than writing outside it.

## Self-evaluation

Accuracy 4/5: outputs and hashes retained; fixture execution is explicitly distinguished from full integration.
Completeness 4/5: all nine prescribed mutations scored; no full REA/UPX invocation is claimed.
Clarity 4/5: detector-specific survival and arm-flip distinctions are explicit.
Actionability 4/5: patches, executable detector and raw receipts retained; rerunning requires recreating frozen scratch copies.
Conciseness 4/5: table summarizes nine probes; raw verbose details stay in JSON. Overall 4.0/5. Highest-impact improvement for integration is a full pinned runtime rerun of b/c/g/h; no contract change is warranted by survival alone.

VERDICT: built-in-selftest survivors b route:295, c route:768, g probe:356, h probe:446/452, i probe:471; added-detector survivor i probe:471 (A10 remains false via genuine checker); exact restoration 9/9.
