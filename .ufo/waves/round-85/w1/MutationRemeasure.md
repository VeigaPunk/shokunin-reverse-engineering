# MutationRemeasure — round-85 w1 (attack seat, R85-C2 independent re-measure)

Declaration rev `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`. Own harness (`harness.py`, Python stdlib), not the frozen counter; frozen counter `tools/round-84/mutation-closure.py` run once on BASE as a cross-check only.

Kill rule applied: pristine selftest green (rc 0, no failing case) AND mutant rc != 0 AND declared case in the mutant's failing names AND no traceback. Failing names are parsed from JSON `failures` lists and `selftest <name>: FAIL` lines. Pristine bytes are restored and re-hashed after every mutant; final re-hash OK for all three targets in every arm.

## 1. BASE (declaration rev) — 21-row table

Killed **3/21**: sb-window-13th, sb-two-fields-first, cg-floor-le. Matches the expected 3/21 (sb-window-13th, sb-two-fields-first, cg-floor-le). Pristine green: printed-command 22 cases, source-bind (plain-line shape), conjunction-gate 21 cases.

| id | declared case | in pristine inventory | status | mutant rc | failing names under mutant |
|---|---|---|---|---|---|
| `pc-row-last` | `duplicate-row-first-binds` | no | survived | 0 | — |
| `pc-row-prefix` | `id-prefix-not-bound` | no | survived | 0 | — |
| `pc-cells-len-ge` | `row-width-thirteen-exact` | no | survived | 0 | — |
| `pc-cells-index-shift` | `fully-mined-row-green` | no | survived | 1 | sourced-entry-uncited, sourced-plan-missing, sourced-row-at-base |
| `pc-entry-any-line` | `entry-second-source-line-ignored` | no | survived | 0 | — |
| `pc-pin-normprefix` | `dot-slash-script-refused` | no | survived | 0 | — |
| `pc-run-rc1-strict` | `rc1-without-expectation-executable` | no | survived | 0 | — |
| `pc-run-counter-type` | `string-counter-refused` | no | survived | 0 | — |
| `pc-run-counter-mismatch-raw` | `int-counter-equals-string-expectation` | no | survived | 0 | — |
| `pc-token-metachar-drop-pipe` | `pipe-metachar-refused` | no | survived | 0 | — |
| `pc-token-ellipsis-drop-ascii` | `ascii-ellipsis-refused` | no | survived | 0 | — |
| `pc-token-allowlist-widened` | `unbound-plan-variable-refused` | no | survived | 0 | — |
| `pc-cells-status-ne-queued` | `sourced-row-rejected-status` | yes | survived | 0 | — |
| `pc-cells-date-ge` | `sourced-row-later-date` | no | survived | 0 | — |
| `pc-run-defects-static-dropped` | `static-defect-ledger-copied` | no | survived | 0 | — |
| `sb-emdash-optional` | `entry-cites-no-em-dash-refused` | no | survived | 0 | — |
| `sb-id-substring` | `id-prefix-not-attributed` | no | survived | 0 | — |
| `sb-window-13th` | `late-single-header` | yes | killed | 1 | late-single-header |
| `sb-two-fields-first` | `duplicate` | yes | killed | 1 | duplicate, duplicate-after-window |
| `cg-frozen-detector-ge` | `frozen-duplicate-detector-refused` | no | survived | 0 | — |
| `cg-floor-le` | `genuine-synthetic-passes` | yes | killed | 1 | genuine-synthetic-passes |

Frozen counter cross-check (`tools/round-84/mutation-closure.py`, unmodified): killed 3/21, survivor set identical to mine (18 ids). Agreement on BASE.

## 2. BASE — frozen r84 13-row table

Killed **13/13** (floor, failure, binder, membership, pin-call, static-refusal, source-mined, source-date, source-base, source-plan, source-entry, sb-header-position, sb-duplicate-last). Expected 13/13: matches.

## 3. Candidates (bytes read from the candidate paths; not the lane tree)

Candidate bytes (sha256): `ExecPrintedCmd/printed-command.py` `4f5f6b158d34`; `ExecPrintedRun/printed-command.py` `78ddfb4e0451`; `ExecSourceBind/source-bind.py` `2fbaa264ddd0`; `ExecSourceBind/conjunction-gate.py` `d7f8d6f4e867`.

Candidate pristine selftests (all rc 0, no failures): ExecPrintedCmd printed-command 28 cases; ExecPrintedRun printed-command 30 cases; ExecSourceBind source-bind 10 cases; conjunction-gate 22 cases. Both printed-command candidates edit the same file independently (not merged; they conflict as whole-file alternatives). Each arm was tested alone, as instructed.

### 3a. Arm ExecPrintedCmd (printed-command from ExecPrintedCmd)

21-row killed **13/21**; frozen-13 regression **13/13**.

| id | declared case | in pristine inventory | status | mutant rc | failing names under mutant |
|---|---|---|---|---|---|
| `pc-row-last` | `duplicate-row-first-binds` | yes | killed | 1 | duplicate-row-first-binds |
| `pc-row-prefix` | `id-prefix-not-bound` | yes | killed | 1 | id-prefix-not-bound |
| `pc-cells-len-ge` | `row-width-thirteen-exact` | yes | killed | 1 | row-width-thirteen-exact |
| `pc-cells-index-shift` | `fully-mined-row-green` | yes | killed | 1 | fully-mined-row-green, sourced-entry-uncited, sourced-plan-missing, sourced-row-at-base |
| `pc-entry-any-line` | `entry-second-source-line-ignored` | yes | killed | 1 | entry-second-source-line-ignored |
| `pc-pin-normprefix` | `dot-slash-script-refused` | no | survived | 0 | — |
| `pc-run-rc1-strict` | `rc1-without-expectation-executable` | no | survived | 0 | — |
| `pc-run-counter-type` | `string-counter-refused` | no | survived | 0 | — |
| `pc-run-counter-mismatch-raw` | `int-counter-equals-string-expectation` | no | survived | 0 | — |
| `pc-token-metachar-drop-pipe` | `pipe-metachar-refused` | no | survived | 0 | — |
| `pc-token-ellipsis-drop-ascii` | `ascii-ellipsis-refused` | no | survived | 0 | — |
| `pc-token-allowlist-widened` | `unbound-plan-variable-refused` | no | survived | 0 | — |
| `pc-cells-status-ne-queued` | `sourced-row-rejected-status` | yes | killed | 1 | sourced-row-rejected-status |
| `pc-cells-date-ge` | `sourced-row-later-date` | yes | killed | 1 | sourced-row-later-date |
| `pc-run-defects-static-dropped` | `static-defect-ledger-copied` | no | survived | 0 | — |
| `sb-emdash-optional` | `entry-cites-no-em-dash-refused` | yes | killed | 1 | entry-cites-no-em-dash-refused |
| `sb-id-substring` | `id-prefix-not-attributed` | yes | killed | 1 | id-prefix-not-attributed |
| `sb-window-13th` | `late-single-header` | yes | killed | 1 | late-single-header |
| `sb-two-fields-first` | `duplicate` | yes | killed | 1 | duplicate, duplicate-after-window |
| `cg-frozen-detector-ge` | `frozen-duplicate-detector-refused` | yes | killed | 1 | frozen-duplicate-detector-refused |
| `cg-floor-le` | `genuine-synthetic-passes` | yes | killed | 1 | genuine-synthetic-passes |

### 3b. Arm ExecPrintedRun (printed-command from ExecPrintedRun)

21-row killed **14/21**; frozen-13 regression **13/13**.

| id | declared case | in pristine inventory | status | mutant rc | failing names under mutant |
|---|---|---|---|---|---|
| `pc-row-last` | `duplicate-row-first-binds` | no | survived | 0 | — |
| `pc-row-prefix` | `id-prefix-not-bound` | no | survived | 0 | — |
| `pc-cells-len-ge` | `row-width-thirteen-exact` | no | survived | 0 | — |
| `pc-cells-index-shift` | `fully-mined-row-green` | no | survived | 1 | sourced-entry-uncited, sourced-plan-missing, sourced-row-at-base |
| `pc-entry-any-line` | `entry-second-source-line-ignored` | no | survived | 0 | — |
| `pc-pin-normprefix` | `dot-slash-script-refused` | yes | killed | 1 | dot-slash-script-refused |
| `pc-run-rc1-strict` | `rc1-without-expectation-executable` | yes | killed | 1 | rc1-without-expectation-executable |
| `pc-run-counter-type` | `string-counter-refused` | yes | killed | 1 | string-counter-refused |
| `pc-run-counter-mismatch-raw` | `int-counter-equals-string-expectation` | yes | killed | 1 | int-counter-equals-string-expectation |
| `pc-token-metachar-drop-pipe` | `pipe-metachar-refused` | yes | killed | 1 | pipe-metachar-refused |
| `pc-token-ellipsis-drop-ascii` | `ascii-ellipsis-refused` | yes | killed | 1 | ascii-ellipsis-refused |
| `pc-token-allowlist-widened` | `unbound-plan-variable-refused` | yes | killed | 1 | unbound-plan-variable-refused |
| `pc-cells-status-ne-queued` | `sourced-row-rejected-status` | yes | survived | 0 | — |
| `pc-cells-date-ge` | `sourced-row-later-date` | no | survived | 0 | — |
| `pc-run-defects-static-dropped` | `static-defect-ledger-copied` | yes | killed | 1 | static-defect-ledger-copied |
| `sb-emdash-optional` | `entry-cites-no-em-dash-refused` | yes | killed | 1 | entry-cites-no-em-dash-refused |
| `sb-id-substring` | `id-prefix-not-attributed` | yes | killed | 1 | id-prefix-not-attributed |
| `sb-window-13th` | `late-single-header` | yes | killed | 1 | late-single-header |
| `sb-two-fields-first` | `duplicate` | yes | killed | 1 | duplicate, duplicate-after-window |
| `cg-frozen-detector-ge` | `frozen-duplicate-detector-refused` | yes | killed | 1 | frozen-duplicate-detector-refused |
| `cg-floor-le` | `genuine-synthetic-passes` | yes | killed | 1 | genuine-synthetic-passes |

Per-arm killed sets are listed in `candidate-results.json`. Neither arm alone reaches the R85-C2 target (killed ≥ 16 of 21). The set union of the two printed-command arms plus the shared source-bind/conjunction-gate arm kills 21/21 by per-row union, but that union was **not** measured as a single merged tree; it is an inference from the two measured arms, not a result.

## 4. Survivors and one-line reasons

BASE (18 survivors): for 17 rows the declared case name is absent from the BASE pristine inventory, so no case can bind; for `pc-cells-index-shift` the mutant turns red on three other sourced cases but not on the absent declared case; `pc-cells-status-ne-queued` is the only row whose declared case is present but green under the mutant (its input is a `queued` row, which the mutant still refuses).

ExecPrintedCmd arm (8 survivors):

- `pc-pin-normprefix`: declared `dot-slash-script-refused` absent; all 28 cases stay green when `./`-prefixed scripts are accepted.
- `pc-run-rc1-strict`: declared `rc1-without-expectation-executable` absent; no case runs a rc-1 script with no counter expectation.
- `pc-run-counter-type`: declared `string-counter-refused` absent; no case passes a string counter.
- `pc-run-counter-mismatch-raw`: declared `int-counter-equals-string-expectation` absent; no int-vs-string expectation case.
- `pc-token-metachar-drop-pipe`: declared `pipe-metachar-refused` absent; no case asserts a `|` is refused.
- `pc-token-ellipsis-drop-ascii`: declared `ascii-ellipsis-refused` absent; no case asserts `...` is refused.
- `pc-token-allowlist-widened`: declared `unbound-plan-variable-refused` absent; no case binds $PLAN unbound.
- `pc-run-defects-static-dropped`: declared `static-defect-ledger-copied` absent; no case asserts the result defects ledger equals the static defects.

ExecPrintedRun arm (7 survivors):

- `pc-row-last`: declared `duplicate-row-first-binds` absent; no duplicate-row case.
- `pc-row-prefix`: declared `id-prefix-not-bound` absent; no prefix-id case.
- `pc-cells-len-ge`: declared `row-width-thirteen-exact` absent; no 14-cell row case.
- `pc-cells-index-shift`: declared `fully-mined-row-green` absent; mutant is red on three other sourced cases, but not on a fully mined row.
- `pc-entry-any-line`: declared `entry-second-source-line-ignored` absent; no multi-source-line entry case.
- `pc-cells-status-ne-queued`: declared `sourced-row-rejected-status` present but its only input is a `queued` row, which the mutant still refuses; no `rejected`-status input in this arm.
- `pc-cells-date-ge`: declared `sourced-row-later-date` absent; no later-date case.

ExecSourceBind arm: source-bind and conjunction-gate rows all killed (sb 4/4, cg 2/2 in both arms).

## 5. Notes
- Candidate ExecPrintedCmd modifies an existing case (`sourced-row-rejected-status` now also feeds a `rejected` row). The 22 base case names are all still present in both candidate inventories (checked); no base name removed.
- Killed-set check: every killed row in every arm has its declared case in that arm's pristine inventory (checked, none absent).
- Frozen counter cross-check on BASE agrees exactly with this harness (same 3 kills, same 18 survivors).
- Harness: `harness.py` (copied to the wave dir `MutationRemeasure/harness.py`); run with `python3 -I -B harness.py --table .ufo/waves/round-85/mutants.json --rev 91eeb72f… --work <scratch> --out <json>`; `--overlay <dir>` supplies candidate targets.
- Tooling: no installs or updates performed.
- Not run: no pacman, no git writes, no commits; no candidate bytes were produced by this seat.
