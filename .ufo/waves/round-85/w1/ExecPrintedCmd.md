# ExecPrintedCmd — R85-C2 scoped implementation

## Results and retained evidence

- Owned rows: **7/7 killed** at sandbox revision `4cb063b8bda3460ef3a5745ff5a010a4e89e5aa2`.
- Frozen full table: **10/21 killed**, counter exit **1**; 11 surviving rows are assigned elsewhere. `inconclusive: []`, `pristine_failed: []`.
- Original declaration selftest: **22/22**, rc **0**. Candidate selftest: **28/28**, rc **0**. All **22** pre-existing case names still pass; none removed. Exact inventories and stdout are retained in `ExecPrintedCmd/selftest-pristine.txt` and `ExecPrintedCmd/selftest-candidate.txt`.
- Every owned mutant has one anchor, rc 1, its declared case in `failures`, and exact restoration. Per-row statuses and all failing-case names: `ExecPrintedCmd/per-row.md`; machine evidence: `ExecPrintedCmd/after-printed-cmd.json`.
- All three target pristine selftests are green in the frozen-counter receipt.

## Candidate and behavior

Complete file: `ExecPrintedCmd/candidate/tools/round-82/printed-command.py`.
Unified diff against declaration `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`: `ExecPrintedCmd/candidate.diff`.
Candidate SHA-256: `4f5f6b158d3442b029c1c214a54c0fbe0102c138ccb51aa1a74991a61d60b09d`.

The seven top-level `r85a_` cases directly invoke production `sources_row`, `entry_cites`, or `sourced_arm`. Fixtures live under TMPDIR; sourced-arm cases reuse the existing fixture-repository helper, whose git mutations are guarded by fixture-root identity checks. The cases bind first duplicate row, exact id instead of prefix, exact 13-cell width, fully valid mined-row acceptance, first source-line attribution, rejected status, and later date 2026-11-05.

Production code and frozen mutant anchors are unchanged. Registrations are one `guarded(...)` line each in `# R85-A cases`, immediately before the existing fixture cleanup. New functions are at EOF before `if __name__`. This is disjoint from ExecPrintedRun's `r85b_` functions and post-cleanup `# R85-B cases`; integrate additive edits rather than replacing that sibling's full candidate.

### Existing-case change

The pre-existing `sourced-row-rejected-status` name was backed only by a queued fixture. Its registration is moved, not duplicated, into `# R85-A cases`. The replacement retains the original queued fixture and adds an otherwise-valid rejected fixture; both must preserve the original exact `SOURCED_ROW_UNMET` defect and additionally assert `row_mined is False` and `met is False`. The frozen `!= queued` mutant now fails this declared case. All other existing cases and fixtures are unchanged.

## Exact measurement provenance

- Declaration: `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`; clone checked out that revision before applying the candidate.
- Sandbox root was `/fast/scratch/hyaku/kaidoku-r85/ExecPrintedCmd/clone.L828`; `git -C <sandbox> rev-parse --show-toplevel` matched it before staging/committing. Commands and outputs are retained in `ExecPrintedCmd/sandbox-commands.json`.
- Exact frozen-counter invocation, stdout, stderr, and rc are in `ExecPrintedCmd/counter-output.txt`. Counter SHA-256: `e5cfd2ededbdfa7af4b6d2a40cfc23685edc58828f971efd4a5739a07904f6ad`.
- Frozen table SHA-256 reported by counter: `ef031dbe3525ff8454b1b120ed18f88a8918c981c7a4726ab626430e72e1ec41`.
- The exact authorized invocation supplies no claims path; `table_identity.claims/expected/matches` are null. Therefore this receipt records the table digest but does not independently establish its container pin.
- Scratch/clone were removed by the requested shell EXIT trap after measurement. Receipts are retained outside scratch. No lane-tree git mutation, commit, push, or production-file edit occurred.

## Risks, tooling, and integration handoff

No scoped blockers. Eleven table survivors are outside this seat's implementation, not a claim that the full-round target is met. Parent owns merged-candidate measurement and the frozen 13-row regression arm; neither was run here. No builds, linters, or formatters were run.

LSP was unavailable: no LSP device is exposed in the active tools or the complete `xd://` inventory; source inspection was used, not an empty cold LSP response. No tools were installed or upgraded.
