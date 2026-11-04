# ReviewerC2 — attack on R85-C2 (depth): 21-row table, frozen scorer, candidate cases

Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Declaration 91eeb72f6a7b13dc96e826117956f90ed89ae3f3.
Frozen counter read at 91eeb72f: `tools/round-84/mutation-closure.py` (blob sha256 e5cfd2ed…, as recorded in the BASE receipt).
Table `.ufo/waves/round-85/mutants.json`: lane bytes sha256 ef031dbe3525ff84… = declaration bytes (unchanged).
Candidates read (sha256 prefix): ExecPrintedCmd printed-command.py 4f5f6b15…; ExecPrintedRun printed-command.py 78ddfb4e…; ExecSourceBind source-bind.py 2fbaa264…, conjunction-gate.py d7f8d6f4….
Sandbox work: `$S/clone.*` (scratch, removed at exit); receipts copied to `receipts/`.
Tooling: no installs. No pacman. No lane writes. No counter re-definition: every scorer run is the unmodified frozen file on a sandbox root.

## 1. The frozen kill rule, as implemented (score(), lines 185–260 of the counter)

- target green iff `exit == 0 and not failures` in the pristine selftest; else every row of that target is `inconclusive: pristine-not-green`.
- row killed iff `declared_case ∈ pristine.case_names` AND `declared_case ∈ mutant.failures`.
- failures come from a JSON summary (`failures` list, `checks[].ok == False`) or `^selftest NAME: FAIL` lines; case names from `case_names`, `checks[].case`, `selftest NAME: ok`.
- `ok` = no survivors, no inconclusive, no pristine_failed, killed == table length, table identity not refuted.

## 2. Scorer attacks (all runs: frozen counter, unmodified, on sandbox roots)

| # | attack | receipt | frozen result | what catches it |
|---|---|---|---|---|
| (a) | always-red case: `check("pc-always-red", False)` in printed-command selftest (attack B) | receipts/attackB.json | killed 6/21, ok false, pristine_failed=[printed-command], 15 pc rows `pristine-not-green` | CAUGHT by the frozen counter (green = exit 0 and no failures). Kills in other targets still score, so the count drops rather than the verdict silently passing. |
| (b) | source-text fabrication: in each of the 21 declared-case names, `check(NAME, b64(find) in open(__file__,'rb').read())` (needle encoded so the case's own bytes do not contain the find text) (attack A) | receipts/attackA.json | killed 21/21, ok true, inconclusive 0 | NOT CAUGHT. The mutant copy is written as `mutant_dir/<basename>`, the selftest reads its own `__file__`, the mutant removes the find text, so the case fails under mutant and passes pristine. The counter has no semantic check of case bodies. Only case-level review (section 4) catches this. Attack A is the strongest evidence that `ok: true` on C2 is not, alone, a certification of depth. |
| (c) | name-level collateral credit: a mutant that already fails pre-existing pristine-green cases credits any of them as "its" kill. BASE receipt: pc-cells-index-shift fails `sourced-entry-uncited`, `sourced-plan-missing`, `sourced-row-at-base` (receipts/BASE-closure-c7e2e8e1.json). Probe C: the table row's declared case replaced with `sourced-plan-missing` (scratch probe table, lane table untouched). | receipts/attackC.json, probe-C-table.json | row `pc-cells-index-shift` = killed | NOT CAUGHT. Kill binding is by name; the counter does not check that the failing case is the one exercising the edited anchor. The current table names `fully-mined-row-green` (sound, §3), so no violation today. |
| (d) | table shrink: one row dropped from a scratch copy of the table, run on attack-A candidate | receipts/attackD.json, probe-D-table.json | 20/20 killed, ok true | NOT CAUGHT. `table_identity` reads `.ufo/waves/round-85/claims.json` for the `fixtures.sha256` pin; no such container exists for round 85 (`expected: null, matches: null`), so the pin is not enforced and `ok` only checks `killed == len(table)`. The lane table is byte-identical to the declaration today (sha ef031dbe), so there is no violation today; the plan's kill rule clause "a table edited after the declaration" has no enforcement path in the frozen counter for R85. |
| (e) | rename an existing pristine-green case to a declared name whose body is changed | not run as a standalone; the same name-binding as (c) | would score as kill | NOT CAUGHT by the counter; caught only by the case-body diff (section 5). |
| (f) | not run as a separate attack: a relaxed `>= 1` detector check is the cg-frozen-detector-ge row itself (§3 row 20) | — | — | — |

Integration measurement (sandbox, not a scorer attack): ExecPrintedRun and ExecPrintedCmd both edit the same file tail
(selftest tail + appended functions). `git merge-file` yields 1 conflict block. Hand-resolving by keeping both sides
(receipts/after-pc-both-sandbox.json; printed-command selftest 36 cases, failures 0; the merged file is not a candidate
of mine, it is an integration probe) gives killed 15 of the printed-command rows. Adding the ExecSourceBind sb/cg files
gives killed 21/21, ok true (receipts/after-all-sandbox.json); frozen r84 regression arm 13/13, ok true
(receipts/after-all-r84-regression.json; table identity matches the r84 claims pin).

## 3. Per-row verdicts (21 rows)

Verdict key: SOUND = the declared case calls a production function, asserts the outcome the mutant flips, and fails only under that mutant (confirmed by the counter in §2 and by reading the case). WEAK = SOUND for the declared mutant, but a same-family sibling change survives. FABRICATED = passes under the mutant or asserts nothing about production code.

Candidate locations: `ExecPrintedCmd/candidate/tools/round-82/printed-command.py` (r85a_*), `ExecPrintedRun/candidate/tools/round-82/printed-command.py` (r85b_*), `ExecSourceBind/candidate/tools/round-83/source-bind.py` and `.../round-82/conjunction-gate.py` (r85c_*), all under `.ufo/waves/round-85/w1/`.

| # | row (target) | declared case | sound assertion (flipped outcome) | fabricated shape to watch for | candidate case (evidence) | verdict |
|---|---|---|---|---|---|---|
| 1 | pc-row-last (printed-command) | duplicate-row-first-binds | `sources_row` on two S299 rows returns the FIRST | returns True without calling sources_row | ExecPrintedCmd printed-command.py:797 `r85a_duplicate_row_first_binds` | SOUND |
| 2 | pc-row-prefix | id-prefix-not-bound | exact S299 row returned when S2999 decoy listed first | `startswith` check on text | :807 `r85a_id_prefix_not_bound` | SOUND |
| 3 | pc-cells-len-ge | row-width-thirteen-exact | 14-cell row with valid mined/date → UNMET only | accepts both widths | :827 `r85a_row_width_thirteen_exact` | SOUND |
| 4 | pc-cells-index-shift | fully-mined-row-green | fully mined row → arm dict with defects [] | asserts only one field | :838 `r85a_fully_mined_row_green` | SOUND |
| 5 | pc-entry-any-line | entry-second-source-line-ignored | entry whose 2nd source line cites S299 → not attributed | single-line fixture | :849 `r85a_entry_second_source_line_ignored` | SOUND |
| 6 | pc-pin-normprefix | dot-slash-script-refused | build_argv of `./tools/…` raises SCRIPT_NOT_PINNED | `assert True` | ExecPrintedRun printed-command.py:864 `r85b_dot_slash_script_refused` | SOUND |
| 7 | pc-run-rc1-strict | rc1-without-expectation-executable | rc 1 with expect None executes, no EXECUTION_FAILED | checks rc only | :874 `r85b_rc1_without_expectation_executable` | SOUND |
| 8 | pc-run-counter-type | string-counter-refused | string counter '3' → COUNTER_NOT_INTEGER | checks executed only | :881 `r85b_string_counter_refused` | SOUND |
| 9 | pc-run-counter-mismatch-raw | int-counter-equals-string-expectation | int 13 vs expect "13" → matched, no defect | str==str compare in the case | :890 `r85b_int_counter_equals_string_expectation` | SOUND |
| 10 | pc-token-metachar-drop-pipe | pipe-metachar-refused | `\|` → SHELL_METACHAR: \| | any defect present | :909 `r85b_pipe_metachar_refused` | WEAK: only `\|` is pinned; dropping `>`, `<` or `&` survives (existing `metachar-refused` covers `;` only) |
| 11 | pc-token-ellipsis-drop-ascii | ascii-ellipsis-refused | ASCII `...` → PLACEHOLDER_UNBOUND abbreviation | unicode ellipsis only (existing case) | :915 `r85b_ascii_ellipsis_refused` | SOUND (the existing unicode case covers the other member of the family) |
| 12 | pc-token-allowlist-widened | unbound-plan-variable-refused | `$PLAN` → VARIABLE_UNBOUND | `$REV` only | :921 `r85b_unbound_plan_variable_refused` | WEAK: only `PLAN` is pinned; widening with any other name survives |
| 13 | pc-cells-status-ne-queued | sourced-row-rejected-status | row status `rejected` → UNMET (queued kept) | queued-only (the BASE case) | ExecPrintedCmd :860 `r85a_sourced_row_rejected_status`, registered at :713 | SOUND (strengthened existing case, §5) |
| 14 | pc-cells-date-ge | sourced-row-later-date | row date 2026-11-05 → UNMET | 2025-12-31 (existing wrong-date case) | :873 `r85a_sourced_row_later_date` | SOUND |
| 15 | pc-run-defects-static-dropped | static-defect-ledger-copied | run_block `defects == static_defects` for an unbound placeholder | checks static_defects (existing static-defect-no-execution) | ExecPrintedRun :900 `r85b_static_defect_ledger_copied` | SOUND |
| 16 | sb-emdash-optional (source-bind) | entry-cites-no-em-dash-refused | `source: S299 is cited here` (no em dash) → not attributed (CLI rc 1) | `malformed` fixture (existing; `note:` prefix does not match the mutant regex) | ExecSourceBind source-bind.py:160 `r85c_entry_cites_no_em_dash_refused` | SOUND |
| 17 | sb-id-substring | id-prefix-not-attributed | `source: S2999 — …` does not attribute S299 (CLI rc 1) | `S286` only | ExecSourceBind :171 `r85c_id_prefix_not_attributed` | SOUND |
| 18 | sb-window-13th | late-single-header | header on line 12 (0-based) → refused | none | existing FIXTURES (unchanged) | SOUND (BASE killed) |
| 19 | sb-two-fields-first | duplicate | two source fields → refused | none | existing FIXTURES (unchanged) | SOUND (BASE killed) |
| 20 | cg-frozen-detector-ge (conjunction-gate) | frozen-duplicate-detector-refused | duplicated CASE row → frozen_killed False | len==1 single-row fixture (existing) | ExecSourceBind conjunction-gate.py:438 `r85c_frozen_detector_ge` | SOUND |
| 21 | cg-floor-le | genuine-synthetic-passes | exact floor 11 → accepted | none | existing (unchanged) | SOUND (BASE killed) |

Counts: SOUND 19 (rows 1–9, 11, 13–21); WEAK 2 (rows 10 and 12: sound for their declared mutant, family gap); FABRICATED 0. SOUND-or-WEAK: 21/21.

Candidate self-test and counter evidence per target (all ran in my scratch, same bytes as the candidates):
- printed-command, ExecPrintedRun candidate: selftest rc 0, 30 cases, failures 0 (`selftest-prc-cand.txt`).
- printed-command, ExecPrintedCmd candidate: selftest rc 0, 28 cases, failures 0 (`selftest-pcmd-cand.txt`); counter in sandbox killed 10/21 (its 7 pc rows + 3 existing), survivors = the other 11 rows, matching its `after-printed-cmd.json` exactly.
- source-bind, conjunction-gate (ExecSourceBind candidate): selftests rc 0 (`selftest-sb-cand.txt`, `selftest-cg-cand.txt`, 22 cg cases); counter killed 6/21 in isolation (its own receipt).
- combined (all three candidates, integration probe): killed 21/21, ok true; r84 regression 13/13 ok true.

## 4. Case-body check (are the declared cases real, not text-inspecting?)

Grep of the three candidates for `__file__`, `open(`, `read_text(` inside r85 functions: no r85 case reads a tool's own source bytes. The only `__file__` hits (`printed-command.py` lines 389, 750, 777; `conjunction-gate.py` 170, 465; `source-bind.py` 107) are pre-existing pin/fixture lines, not case bodies. Every r85 case calls a production entry point (`sources_row`, `sourced_arm`, `entry_cites`, `build_argv`, `run_block`, `static_defects`, `frozen_killed`, source-bind CLI) against fixture git repos or synthetic bytes. So none of the 21 is FABRICATED under the rule in §3, and attack (b) is not realised by the executors.

## 5. Weakened-case check (existing cases, against 91eeb72f)

- ExecPrintedRun printed-command.py: 0 removed or changed lines against 91eeb72f (only additions: the `# R85-B cases` block at the selftest tail and the r85b functions). Pre-existing case bodies byte-identical.
- ExecSourceBind source-bind.py: one changed line, the loop header `for name, text, sid, expected in FIXTURES:` → `fixtures = FIXTURES + (r85c_…(), r85c_…())`. The FIXTURES tuples are unchanged, so no existing case is weakened. conjunction-gate.py: additions only (one `check` line and the r85c function).
- ExecPrintedCmd printed-command.py: removes the single registration `guarded("sourced-row-rejected-status", lambda: sourced_case([base_state, with_sources(row_queued)], ["SOURCED_ROW_UNMET"]))` and re-registers the same name at :713 to `r85a_sourced_row_rejected_status`. That function asserts the identical queued refusal (`row_mined is False`, `defects == ["SOURCED_ROW_UNMET"]`, `met is False`) and adds the rejected row. The original assertion survives; it is strengthened, not weakened. Pre-existing names retained (per-row.md: 22/22). Arithmetic check: printed-command pristine cases = 22 + 8 (ExecPrintedRun) + 7 (ExecPrintedCmd) − 1 (replaced name) = 36, and the integration selftest reports 36 with failures 0, so no pre-existing name was dropped.

Result: NO weakened pre-existing case in any of the three candidates.

## 6. Residual risk and verification gaps

- Counter-level: `ok` does not certify case semantics (attack b, 21/21 with fabricated cases). Depth claim relies on review (this file), not the counter.
- Counter-level: kill binding is by name; collateral credit possible (attack c). Table currently names sound cases.
- Counter-level: the r85 table pin is unenforced (attack d). The lane table is byte-identical to the declaration; the plan's "table edited after declaration" clause has no enforcement path until a round-85 container with `fixtures.sha256` exists.
- Family gaps: rows 10 and 12 (WEAK). Siblings that drop `>`/`<`/`&` or widen the allowlist with other names survive.
- Integration: ExecPrintedRun and ExecPrintedCmd both edit printed-command.py at the same tail; a textual merge conflicts. The integrator must keep both blocks (verified: both kept gives 36 cases green and kills 15 pc rows).
- Not verified here: ExecPrintedCmd candidate's own counter is measured by the executor and by my sandbox (identical 10/21); I did not run the C1 counter (not in my seat).

## 7. Result

SOUND 19, WEAK 2, FABRICATED 0 of 21 rows. Scorer attacks: (a) caught; (b), (c), (d) not caught by the frozen counter, each documented in §2; weakened-case check: none.
