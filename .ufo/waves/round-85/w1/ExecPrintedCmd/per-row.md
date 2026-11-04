# ExecPrintedCmd — owned mutant outcomes

Sandbox revision: `4cb063b8bda3460ef3a5745ff5a010a4e89e5aa2` (declaration parent `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`).
Evidence: `after-printed-cmd.json`, measured by the unchanged frozen counter.

| id | declared case | status | failing case names under mutant | pristine outcome |
| --- | --- | --- | --- | --- |
| `pc-row-last` | `duplicate-row-first-binds` | killed; rc 1; anchor 1 | `duplicate-row-first-binds` | PASS; present; rc 0 |
| `pc-row-prefix` | `id-prefix-not-bound` | killed; rc 1; anchor 1 | `id-prefix-not-bound` | PASS; present; rc 0 |
| `pc-cells-len-ge` | `row-width-thirteen-exact` | killed; rc 1; anchor 1 | `row-width-thirteen-exact` | PASS; present; rc 0 |
| `pc-cells-index-shift` | `fully-mined-row-green` | killed; rc 1; anchor 1 | `fully-mined-row-green`, `sourced-entry-uncited`, `sourced-plan-missing`, `sourced-row-at-base` | PASS; present; rc 0 |
| `pc-entry-any-line` | `entry-second-source-line-ignored` | killed; rc 1; anchor 1 | `entry-second-source-line-ignored` | PASS; present; rc 0 |
| `pc-cells-status-ne-queued` | `sourced-row-rejected-status` | killed; rc 1; anchor 1 | `sourced-row-rejected-status` | PASS; present; rc 0 |
| `pc-cells-date-ge` | `sourced-row-later-date` | killed; rc 1; anchor 1 | `sourced-row-later-date` | PASS; present; rc 0 |

All seven declared cases fail under their own mutant, pass pristine, and have `restored_equal: true`.
Original selftest: 22 cases, failures [], rc 0. Candidate selftest: 28 cases, failures [], rc 0.
Pre-existing case names retained: 22/22; removed names: [].

## Existing-case change

`sourced-row-rejected-status` previously supplied only a `queued` row. Its registration now calls `r85a_sourced_row_rejected_status` exactly once in `# R85-A cases`. That function retains the queued refusal and also supplies an otherwise-valid 13-cell row with status `rejected`. Both go through production `sourced_arm`; both must report `row_mined is False`, exactly `["SOURCED_ROW_UNMET"]`, and `met is False`. Thus the original defect assertion is retained and strengthened, not weakened. The mutant rejects queued but accepts rejected, so this same declared case now fails.
