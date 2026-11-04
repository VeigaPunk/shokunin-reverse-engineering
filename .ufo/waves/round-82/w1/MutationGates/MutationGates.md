# MutationGates — round 82 bounded probe

Axes: guard sensitivity, execution-boundary coverage, exact restoration.

## Scope and detector

Probed only isolated copies of `tools/round-82/conjunction-gate.py` and `tools/round-82/printed-command.py`, using their existing `--selftest` detectors. Declaration supplied: `42c78912733357dabe8fcaf513a09c4a3c4ba2aa`; container freeze supplied: `2d63e1a7d04d4dcff45c3908bb51be787a2f22e1`. These references were not independently adjudicated. Tested working-file hashes identify the actual bytes below.

Command per mutant (identical pristine → mutated → restored):

```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r82/MutationGates/tmp python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/w1/MutationGates/detector.py /fast/scratch/hyaku/kaidoku-r82/MutationGates/<mutant>.py
```

Cwd was the private scratch root. The detector invokes the original selftest CLI, with explicit `--work` for printed-command and explicit TMPDIR for both. It adds only a fixture-safety subprocess adapter: `git init` becomes `git -C <absolute fixture> init`, all git operations are constrained to private scratch, and repository toplevel is asserted before add/commit. No instrument assertions or verdicts are replaced. The same adapter applies to all three phases. Each subprocess has a 45-second outer bound; no timeouts occurred. Four independent copies were run concurrently, with no delegation.

## Results

All 11 pristine runs passed: C1 `SELFTEST cases=19 failures=0`; C2 `SELFTEST cases=15 failures=0`. All 11 restored runs produced the same respective passing summaries. Four mutants killed; seven survived; zero inconclusive.

| Mutant | Single behavior change | Mutated rc | Failed selftest cases | Verdict |
|---|---|---:|---|---|
| floor | `if len(cases) < PRISTINE_FLOOR:` → `if False and len(cases) < PRISTINE_FLOOR:` | 1 | floor-refused | **killed** |
| failure | `elif summary[1] != 0:` → `elif False and summary[1] != 0:` | 1 | failures-refused | **killed** |
| binder | `if receipt.get("binder_sha256") != BINDER_SHA256:` → `if False and receipt.get("binder_sha256") != BINDER_SHA256:` | 1 | binder-refused, first-declared-defect-binder | **killed** |
| membership | `if script not in pins:` → `if False and script not in pins:` | 1 | bare-name-refused, unpinned-path-refused | **killed** |
| pin-call | `pin_matches(root, rev, script, pins[script])` → `pass  # runtime pin recheck omitted` | 0 | none; 15/0 | **survived** |
| static-refusal | `if result["static_defects"]:` → `if False and result["static_defects"]:` | 0 | none; 15/0 | **survived** |
| source-mined | `row_ok = bool(row and "mined" in row and "2026-11-04" in row)` → `row_ok = bool(row and "2026-11-04" in row)` | 0 | none; 15/0 | **survived** |
| source-date | `row_ok = bool(row and "mined" in row and "2026-11-04" in row)` → `row_ok = bool(row and "mined" in row)` | 0 | none; 15/0 | **survived** |
| source-base | `base_absent = sources_row(base_text, SOURCED_ROW) is None` → `base_absent = True` | 0 | none; 15/0 | **survived** |
| source-plan | `plan_names = SOURCED_ROW in read_text(root, rev, PLAN)` → `plan_names = True` | 0 | none; 15/0 | **survived** |
| source-entry | `entry_ok = entry_cites(entry_text, SOURCED_ROW)` → `entry_ok = True` | 0 | none; 15/0 | **survived** |

## Coverage findings and limits

- Runtime `pin_matches` call removal survives although direct pin function tests still pass: these selftests do not establish that the execution path calls the guard.
- Runtime static-refusal bypass survives although direct parser tests still pass: these selftests do not establish no execution on static defects.
- All five sourced-arm predicate weakenings survive. Existing parser tests do not exercise the actual sourced-arm conjunction. In particular the queued-row selftest duplicates the mined/date expression instead of invoking `sourced_arm`, so deleting `mined` from the production predicate does not affect it.
- Membership removal is killed by `bare-name-refused` and `unpinned-path-refused`; C1 floor, nonzero-failure, and binder guards are individually detected.
- A survivor is a selftest coverage finding, not an admission decision or evidence that the full battery also survives. No batteries, repository sweeps, promotion, integration, production edits, or other runtimes were used. No contract changes are proposed here.

## Restoration and receipts

`mutation-results.json` retains exact argv, exit, stdout/stderr, mutation text, and pristine/mutant/restored SHA-256 per mutant. All restored SHA-256 values equal their pristine hashes; every mutated digest differs. Exact source snapshots retained beside this report identify tested bytes:

- `conjunction-gate.py`: `6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af`
- `printed-command.py`: `d447f6b487f2f9b39e0585ddf48f41cf4068cb5da6f64a299cf7be3066aacd8c`

Private scratch is removed after retaining evidence. Production was never modified. Python 3.14.8 and Git 2.56.0 were already installed; no installation/update/channel transactions occurred. Authorization rules were read; pacman remained paused.

## Self-evaluation

Accuracy 4/5: raw outputs and hashes retained; declaration/freeze provenance was not independently adjudicated. Completeness 4/5: every assigned guard family probed; only selftest sensitivity, not full-battery sensitivity, was assigned and measured. Clarity 4/5: separate output table and explicit adapter limitation; long mutation expressions remain in the table. Actionability 4/5: seven surviving loci named; no integration authority or production patch. Conciseness 4/5: detailed reproducibility kept primarily in the JSON receipt. Overall 4.0/5. Highest-impact improvement for L1 consideration: execute runtime refusal and sourced-arm cases rather than only helper predicates. Would the user agree: the scope and limits are explicit, with no promotion claim.
