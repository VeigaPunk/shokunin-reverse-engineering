# ScoutSurface — insertion-surface map for round 85 / R85-C2 (read-only)

Lane bytes read at declaration rev `91eeb72f6a7b13dc96e826117956f90ed89ae3f3` (`git -C <lane> show 91eeb72f:<path>`).
Lane tree unmodified. Scratch `/fast/scratch/hyaku/kaidoku-r85/ScoutSurface` (removed on exit). No tools installed.

## 0. Verdict summary
- **All 21 frozen rows have anchor count exactly 1** at the declaration rev — the frozen table is not defective.
- **Only 4 of 21 declared case names exist in a pristine selftest inventory** (`sourced-row-rejected-status`,
  `late-single-header`, `duplicate`, `genuine-synthetic-passes`); **17 declared cases do not exist yet** and must be
  added as new selftest cases by the executors.
- BASE counter receipt `pre/c2/base-mutation-closure.json` (rev 91eeb72f): **killed 3 / 21**, survivors 18,
  inconclusive 0, pristine_failed 0, ok false. Target is **killed ≥ 16 / 21**.
- Frozen r84 table (13 rows) at rev 91eeb72f: **killed 13 / 13, ok true** (`pre/c2/base-frozen13-regression.json`);
  re-measured selftest rc for all three targets = 0.
- Census `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → **rc 0**, 27 × `W04`,
  final line `kaidoku ok …/corpus/SOURCES.md`. Manual census at rev: **rows 208**, malformed (NF≠13) **0**,
  tiers A=190 B=10 C=8.

## 1. Per-file structure and insertion points

### 1.1 `tools/round-82/printed-command.py` (789 lines) — 15 of 21 rows target this file
Top-level functions: `sha256_bytes` 61, `get` 65, `read_text` 73, `extract_block` 77, `static_defects` 88,
`claim_pins` 110, `build_argv` 119, `pin_matches` 140, `containment` 155, `child_env` 163, `run_block` 176,
`sources_row` 250, `entry_cites` 257, `sourced_arm` 264, `battery` 302, `validate_battery` 413, `control` 442,
`fixture_block` 481, `selftest` 485, `main` 724. Constants: `ALLOWED_VARS` 39, `METACHARS` 41, `ELLIPSIS` 46, `CONTROLS` 434.
- **Selftest entry**: `def selftest(root, rev, json_out=None) -> int` at **485**; dispatched from `main` 749–750
  (`--selftest` → `selftest(a.root, a.rev, a.json_out)`). **Selftest returns at line 721** (`return 0 if not failures else 1`).
- **Case registration (two mechanisms)**: (1) `cases: dict[str, bool]` **486** + nested `def check(name, cond)`
  **488–489** (direct `check(...)` at 491–520, 561–580); (2) nested `def guarded(name, thunk)` **614–618**, a
  try/except wrapper used by every fixture-driven case (`guarded("name", lambda: …)` at 636, 653, 691, 693, 695, 698, 702).
- **Fixture helpers**: `fixture_repo(states)` **583–612** (scratch git repo from per-commit file states; asserts
  `rev-parse --show-toplevel` == repo root); `run_case(command, pin)` **623–632** (wraps `run_block` over a fixture
  repo); `static_case()` **645–651**; `sourced_case(states, expected)` **675–679**; `with_sources(row)` **686–689**.
  Fixture blobs: `row_mined` 658, `row_queued` 661, `row_old` 662, `entry_citing` 664, `entry_other` 666,
  `plan_naming` 668, `plan_silent` 669, `base_state` 670, `full_state` 681, `member` 620.
- **Insertion point**: new `guarded(...)` calls after the last one at **702–707** and before the fixture cleanup loop
  **709–710**, i.e. before `failures = sorted(...)` **712** (summary/`case_names` 713–715). `check`/`guarded` write
  into the `cases` dict, so new names appear in the printed `case_names` inventory (printed at 719) the counter parses.
- **Mutation-sensitive code**: `sources_row` 250–255; `entry_cites` 257–262; `build_argv` 119–138 (pin lookup **135**);
  `run_block` 176–243 (static-defect ledger copy **183**, rc-1 gate **215–216**, counter-type check **237**, counter
  compare **240**); `static_defects` 88–107 (`ELLIPSIS` loop 94–96, `ALLOWED_VARS` loop 97–100, `METACHARS` loop
  102–104); `sourced_arm` 264–299 (`row_ok` **273–274**, `base_absent` 276, `plan_names` 277, `entry_ok` 280).

### 1.2 `tools/round-83/source-bind.py` (183 lines) — 4 of 21 rows target this file
Top-level functions: `entry_cites` **37**, `assess_text` **53**, `emit` **59**, `unavailable` **71**, `selftest` **104**,
`main` **156**. Module constant `FIXTURES` **81–101**.
- **Selftest entry**: `def selftest(json_out) -> int` at **104**; dispatched from `main` 163–164.
  **Returns at line 149** (`return 0 if passed else 1`).
- **Case registration**: the **fixture tuple list `FIXTURES` (81–101)** — each entry is `(name, text, sid, expected_rc)`.
  `selftest` iterates it (loop 111–137), appends to `checks` (108) and prints `selftest <name>: ok|FAIL rc=[…]`. The
  counter's `parse_selftest` (`tools/round-84/mutation-closure.py` 46–90) reads this line shape for this file, so
  **a new case must be a new `FIXTURES` tuple named exactly the declared case**.
- **Fixture helper**: none beyond `FIXTURES`; the selftest writes each fixture to a temp file (114–117), runs the
  tool's own CLI twice via `sys.executable -I -B script --entry … --sid …` (118–124), and requires stable findings +
  the expected finding (125–131); `work = mkdtemp` 106.
- **Insertion point**: a new tuple inside `FIXTURES` (after line 100, before the closing `)` at 101).
- **Mutation-sensitive code**: `entry_cites` 37–46 — `source:` field scan **38–39**, window/field-count gate **40**,
  em-dash regex **42–43**, id membership **46**.

### 1.3 `tools/round-82/conjunction-gate.py` (465 lines) — 2 of 21 rows target this file
Top-level functions: `sha256_bytes` 62, `get` 66, `load_receipt` 70, `frozen_killed` 78, `conjunction` 102, `arm` 149,
`battery` 167, `validate_receipt` 237, `_write` 273, `synthetic_genuine` 283, `selftest` 303, `main` 435. Constants:
`PRISTINE_FLOOR` **31**, `ORIGINAL_CASES` 33–43, `CASE` 30, `DECLARED_RULES` 49–60.
- **Selftest entry**: `def selftest() -> tuple[dict, int]` at **303**; dispatched from `main` 454–455.
  **Returns at line 432** (`return summary, 0 if not failures else 1`).
- **Case registration**: `cases: dict[str, bool]` **304** + nested `def check(name, cond)` **306–307**; every case is a
  direct `check("name", …)` call (311–424). **No `guarded` helper and no fixture tuple list** here — new cases are
  direct `check(...)` calls. Summary/`case_names` 427–429, printed 430.
- **Fixture helper**: `synthetic_genuine()` **283–300** (synthetic receipt: `ORIGINAL_CASES` pristine rows + a mutant
  row); mutations via `copy.deepcopy(base)` inside the selftest (314–318, 321–323, 347–350, 358–363).
- **Insertion point**: new `check(...)` calls after the last one at **424**, before `failures = sorted(...)` **426**.
- **Mutation-sensitive code**: `conjunction` 102–147 (binder 110, exit 112, `summary[1] != 0` 118, pristine floor
  **120–123**, detector-count conjunction **137–138**); `frozen_killed` 78–99 (its own detector-count clause **97–98**).

### 1.4 The two counters (read-only; do not edit)
- `tools/round-84/mutation-closure.py` (386 lines) — the frozen C2 counter. `parse_selftest` 46–90 (three accepted
  stdout shapes: JSON `case_names`/`failures`, JSON `checks[].case`, `selftest <name>: ok|FAIL` lines); `run_selftest`
  92–104; `table_identity` 106–136; `score` 139–234; **kill binding 222–228** — a mutant is killed only when its
  `declared_case` is in the mutant's failing list **and** in the pristine inventory (an absent declared case is scored
  `survived`, never a pass); exact-restore check 230–233.
- `tools/round-84/freeze-precheck.py` (275 lines) — the frozen r84 gate (do-nothing control for C1): `SCRIPT_RE` 39–40,
  `PIN_KEYS` 41, `check_container` 73–106, `cheap_rule` 108–120, `selftest` 128, `main` 195 (CLI 197–204), exit 271.
  Structural template for the new `tools/round-85/predicate-bind.py` (R85-C1 counter).

## 2. Anchor-count table — 21 rows, frozen table `.ufo/waves/round-85/mutants.json`
Anchor = the row's `find` string; literal substring occurrences in the target's bytes at rev 91eeb72f (python3 string
count over `git show` output). Line = 1-based line of the unique hit. `src` = declared case found in the pristine target
source (`grep -n -F`); `inv` = declared case in the pristine printed selftest inventory; `BASE` = status in
`pre/c2/base-mutation-closure.json`.

| # | id | target | occ | line | declared_case | src | inv | BASE |
|---|---|---|---|---|---|---|---|---|
| 1 | pc-row-last | printed-command.py | 1 | 251 | duplicate-row-first-binds | – | no | survived |
| 2 | pc-row-prefix | printed-command.py | 1 | 252 | id-prefix-not-bound | – | no | survived |
| 3 | pc-cells-len-ge | printed-command.py | 1 | 273 | row-width-thirteen-exact | – | no | survived |
| 4 | pc-cells-index-shift | printed-command.py | 1 | 273 | fully-mined-row-green | – | no | survived |
| 5 | pc-entry-any-line | printed-command.py | 1 | 258 | entry-second-source-line-ignored | – | no | survived |
| 6 | pc-pin-normprefix | printed-command.py | 1 | 135 | dot-slash-script-refused | – | no | survived |
| 7 | pc-run-rc1-strict | printed-command.py | 1 | 215 | rc1-without-expectation-executable | – | no | survived |
| 8 | pc-run-counter-type | printed-command.py | 1 | 237 | string-counter-refused | – | no | survived |
| 9 | pc-run-counter-mismatch-raw | printed-command.py | 1 | 240 | int-counter-equals-string-expectation | – | no | survived |
| 10 | pc-token-metachar-drop-pipe | printed-command.py | 1 | 41 | pipe-metachar-refused | – | no | survived |
| 11 | pc-token-ellipsis-drop-ascii | printed-command.py | 1 | 46 | ascii-ellipsis-refused | – | no | survived |
| 12 | pc-token-allowlist-widened | printed-command.py | 1 | 39 | unbound-plan-variable-refused | – | no | survived |
| 13 | pc-cells-status-ne-queued | printed-command.py | 1 | 273 | sourced-row-rejected-status | 691 | **yes** | survived (present, not failing) |
| 14 | pc-cells-date-ge | printed-command.py | 1 | 274 | sourced-row-later-date | – | no | survived |
| 15 | pc-run-defects-static-dropped | printed-command.py | 1 | 183 | static-defect-ledger-copied | – | no | survived |
| 16 | sb-emdash-optional | source-bind.py | 1 | 43 | entry-cites-no-em-dash-refused | – | no | survived |
| 17 | sb-id-substring | source-bind.py | 1 | 46 | id-prefix-not-attributed | – | no | survived |
| 18 | sb-window-13th | source-bind.py | 1 | 40 | late-single-header | 95 | **yes** | **killed** |
| 19 | sb-two-fields-first | source-bind.py | 1 | 40 | duplicate | 88 (6 substring hits) | **yes** | **killed** |
| 20 | cg-frozen-detector-ge | conjunction-gate.py | 1 | 97 | frozen-duplicate-detector-refused | – | no | survived |
| 21 | cg-floor-le | conjunction-gate.py | 1 | 120 | genuine-synthetic-passes | 311 | **yes** | **killed** |

**No row has an anchor count ≠ 1 — the frozen table has no defect to report.** Rows 3/4/13 all anchor in the same
`row_ok` expression (printed-command.py:273–274) with *different* `find` strings, so each still counts 1 on its own.
Rows 18/19 share anchor line source-bind.py:40 with different `find` strings; each counts 1.

**17 of 21 declared cases exist in no pristine inventory** — the executors must add them (`guarded(...)` in
printed-command.py, a `FIXTURES` tuple in source-bind.py, `check(...)` in conjunction-gate.py). Rows 4 and 13 mutate the
same `cells[8] == "mined"` expression at printed-command.py:273, so their new cases must be distinguishable.

**Anchors shared with the frozen r84 table** (an edit touching these lines must keep the r84 anchor count at 1 too):
`cells[8] == "mined"` (r84 `source-mined` ↔ r85 rows 4, 13); `cells[9] == "2026-11-04"` (r84 `source-date` ↔ r85
row 14); `if script not in pins:` (r84 `membership` ↔ r85 row 6); `if len(fields) != 1 or fields[0][0] >= 12:`
(r84 `sb-header-position` ↔ r85 rows 18, 19); `len(cases) < PRISTINE_FLOOR` (r84 `floor` edit 1 ↔ r85 row 21).

## 3. Pristine printed selftest inventories (the case names the counter will see)
- printed-command.py — 22: bare-name-refused, ellipsis-refused, entry-cites-no-source-line, entry-cites-true,
  entry-cites-wrong-row, fixture-repo-top, metachar-refused, pin-match-accepts, pin-mismatch-refused,
  placeholder-refused, prefix-refused, row-parse-absent, row-parse-mined, row-parse-queued-unmet,
  runtime-pin-mismatch-refused, sourced-entry-uncited, sourced-plan-missing, sourced-row-at-base,
  sourced-row-rejected-status, sourced-row-wrong-date, static-defect-no-execution, unpinned-path-refused.
- source-bind.py — 8: positive, withdrawn, malformed, duplicate, duplicate-after-window, late-single-header,
  duplicate-target-second, unavailable.
- conjunction-gate.py — 21: binder-deficiency-frozen-accepts, binder-refused, detector-absent-refused,
  detector-nonunique-refused, detector-passing-refused, failures-deficiency-frozen-accepts, failures-refused,
  first-declared-defect-binder, floor-deficiency-frozen-accepts, floor-refused, frozen-rule-agrees-genuine,
  frozen-rule-not-killed-refused, genuine-synthetic-passes, mutants-refused, original-names-refused,
  pristine-exit-refused, summary-bool-refused, summary-floor-independent, survivors-refused,
  validate-consistent-clean, validate-refused-mismatch.

## 4. Frozen r84 regression surface (13 rows, `.ufo/waves/round-84/mutants.json`)
Same three target files. Selftest rc measured at rev 91eeb72f (scratch copy, `TMPDIR` in scratch):
printed-command.py → **rc 0**, 22 cases, 0 failures; source-bind.py → **rc 0**, 8 checks, 0 failures;
conjunction-gate.py → **rc 0**, 21 cases, 0 failures. BASE frozen-13 receipt
`pre/c2/base-frozen13-regression.json`: **killed 13 / 13, survivors [], inconclusive [], pristine_failed [], ok true**.
Every r84 anchor count is 1 at 91eeb72f (the `floor` row has two edits, both count 1 — conjunction-gate.py lines 120
and 122). All r84 declared cases already exist in the pristine inventories, so the 13-row arm needs only **added** cases.

## 5. Census numbers (with commands)
```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
exit code: 0
first two lines:
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
last line: kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
(27 × W04 warnings; 28 stdout lines)
```
Frozen manual census (CORPUS.md §Census) over the rev bytes:
```
$ git -C <lane> show 91eeb72f:corpus/SOURCES.md > $S/SOURCES.md
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $S/SOURCES.md          → 208
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' $S/SOURCES.md   → 0
$ awk -F'|' '…{t=$5; …} END{…}' $S/SOURCES.md                                → A=190 B=10 C=8
```
Census `census` mode agrees: `kaidoku rows 208`, tier.A 190, tier.B 10, tier.C 8, status.mined 186. The enum-violation
awk (CORPUS.md line 145) prints nothing at rev 91eeb72f. **After S304 is added the row count becomes 209.**

## 6. C1 insertion surface (read-only observation, for the executor)
- `tools/round-85/predicate-bind.py` and the r85 container `.ufo/waves/round-85/claims.json` do **not** exist at
  91eeb72f; under `.ufo/waves/round-85/` only `mutants.json`, `pre/c1/F1.json`, `pre/c1/F2.json` are present.
- Frozen template: `tools/round-84/freeze-precheck.py` — `SCRIPT_RE` 39, `PIN_KEYS` 41, `check_container` 73,
  `cheap_rule` 108, CLI `--root/--rev/--container/--expect/--control instruments-only/--selftest/--json-out` (197–204).
- The r84 positive-control container `.ufo/waves/round-84/claims.json` names one counter path per predicate, each
  pinned in `instruments` at its blob digest; its predicates contain the token `none` ("mismatches none", "survivors
  none") that must not read as negation.
- Forgery fixtures (frozen): F1's predicate names no counter and its `kill_rule` names
  `tools/round-84/freeze-precheck.py`; F2's predicate names that counter in a negated sentence ("does not score this
  container").

## 7. Receipts (copied into this wave dir)
- `receipts/sources-census-validate.out` — census stdout (28 lines, rc 0).
- `receipts/selftest-printed-command.out` — rc 0, 22 cases, 0 failures.
- `receipts/selftest-source-bind.out` — rc 0, 8 checks, all ok.
- `receipts/selftest-conjunction-gate.out` — rc 0, 21 cases, 0 failures.
- `receipts/SOURCES-at-91eeb72f.md` — the registry bytes the counts were taken over.
