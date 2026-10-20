# InvocationAuditTool — round-17 w1 report

Delivered: `.ufo/waves/round-17/tools/invocation-audit.py` (new file, sole
assigned artifact). Contract section: `contract.md:80-88`. Python 3 stdlib
only; `python3 -I`-clean; JSON `sort_keys=True, indent=2`; exit 0 reported /
2 could-not-evaluate. Git-objects read-only — every byte comes from
`git ls-tree`/`git show`/`git rev-parse` against `--rev`; the working tree is
never opened (`_git`, `resolve_rev`, `list_ufo_paths`, `show` at
`tools/invocation-audit.py:57,72,76,81`). No installs made (pacman paused;
nothing needed beyond stdlib+git).

## Mechanism (observation)

- Registry rows: SKILL.md lines split on `|`; kept when cell 3 matches
  `^(probe|gate|tool)\s*/\s*kaidoku$` case-insensitively
  (`ROW_KIND_RE`, `invocation-audit.py:45,153-176`). Command = first
  backticked span of cell 4 (`first_backtick_span`, `:148`). 7 rows at REV.
- Receipts: 12 files under `.ufo/` at REV whose basename is
  `verification.json`/`final-recheck.json`/`gate-results.json` or matches
  `*receipt*.json` (`receipt_eligible`, `:233`; `RECEIPT_EXACT/RECEIPT_GLOB`,
  `:43-44`). Exercised argv = recursive walk emitting every `argv`/`orig_argv`
  list-of-strings at any depth (`iter_exercised_argvs`, `:222-231`) →
  50 argv records, 0 unreadable receipts.
- Matching: `tokenize_command` (`:87-146`) splits the command cell with
  quote/escape handling; `[...]`-bracketed tokens become independently
  optional; `<...>` whole-token placeholders match exactly one argv token
  (`argv_matches`, `:197-221`, DP). Normalization (`normalize_tokens`,
  `:187-194`): a leading `pythonX`/`pypy` interpreter token is stripped
  (per contract's "modulo leading python3/interpreter path"); interpreter
  flags such as `-I` are kept and must match literally; absolute path tokens
  under `--root` are re-pathed to repo-relative on both sides (needed:
  registry writes `.ufo/...` or absolute, receipts record absolute).
- Classes per contract: exercised_match → else row text contains
  `unexercised` → labelled_unexercised, else unlabelled_variant
  (`audit`, `:263-319`). `matched_receipt` = first match sorted by
  (receipt path, keypath); `matched_receipt_count`/`matched_keypath`/
  `matched_argv` retained for traceability.

## Selftest (observed run)

`python3 -I .../invocation-audit.py --selftest` → `SELFTEST: CLEAN cases=6`.
Builds a throwaway `git init` repo under `tempfile.mkdtemp()` with a fixture
SKILL.md (alpha exercised via relative path + wildcard; beta exercised via
absolute path + optional `[--label <L>]` skipped; gamma labelled unexercised;
delta unlabelled), a corrupt `run-receipt-v1.json` (counted, not fatal), a
nested `not-basename.json` (excluded by basename glob), a malformed argv
(ignored by the list-of-strings gate), and a non-kaidoku row (excluded).
Fixture removed in `finally`.

## Baseline run, REV b563c799d97774aae4351276fe43cb897311e349 (observed output)

Exit 0. counts: `rows=7, exercised_match=5, labelled_unexercised=0,
unlabelled_variant=2, receipt_files=12, argv_records=50,
unreadable_receipts=0, receipt_glob_pathform_excluded=71`.

| row (SKILL.md line) | class | matched receipt |
|---|---|---|
| interactive-r1-recovery (:447) | exercised_match | .ufo/rounds/interactive-r1/gate-results.json `/checks[0]/argv` |
| citation-drift (:448) | unlabelled_variant | — |
| custody-pair (:449) | unlabelled_variant | — |
| quote-fidelity (:450) | exercised_match | .ufo/waves/round-14/verification.json `/commands[7]/argv` |
| go-snapshot-inventory (:487) | exercised_match | .ufo/waves/round-15/verification.json `/commands[2]/argv` (2 matches) |
| go-selection-preview (:506) | exercised_match | .ufo/waves/round-16/verification.json `/commands[5]/argv` |
| round16-structural-controls (:507) | exercised_match | .ufo/waves/round-16/verification.json `/commands[19]/argv` |

Variant verification (observation, independent scan of all 12 receipts):
citation-drift WAS exercised 4× (round-14 verification `commands[8]`,
round-15 verification `commands[9]`, round-15 final-recheck `commands[1]`,
round-16 verification `commands[17]`) but every exercised argv appends
`--strict`, a flag absent from the registered command span — literal-token
equality correctly fails → `unlabelled_variant` is the contract-true class.
custody-pair has zero argv records in eligible receipts; its evidence lives
in `.txt`/`.out` files under `receipts/` dirs (e.g.
`.ufo/waves/arc3-loop1-round2/claims/c3/CR-4/receipts/custody-live-1.txt`),
which the basename JSON glob excludes → `unlabelled_variant`.

## Judgment calls made within spec latitude (inference, flagged for L1)

- `*receipt*.json` applied to the basename, not the path. 71 additional
  `.json` files live under `receipts/` dirs (path-glob reading); counted as
  `receipt_glob_pathform_excluded` so the L1 can see the margin. If the L1
  intends path-glob, custody-pair still would not match — those are `.txt`.
- `--selftest` uses real `git init` in a temp dir rather than a stubbed git;
  exercises the same `audit()` code path as the baseline run.
- `matched_receipt` is singular per contract; full match count preserved in
  `matched_receipt_count`.

## Limits (calibration)

- Equality is token-literal: extra flags (`--strict`), different flag order,
  or `--opt=val` joined forms are variants, never matches. `<...>` wildcards
  bind exactly one token; embedded placeholders like `--rev=<X>` match
  literally. Optional `[...]` applies per-token, not per-bracket-group.
- A receipt that is not parseable JSON is counted under
  `unreadable_receipts` and skipped (0 at baseline) rather than failing the
  run; SKILL.md/git failures are exit 2.
- Non-JSON evidence (`.txt` receipts, shell scripts) is invisible by design
  per the contract's receipt definition.

Checks the L1 may rerun: `--selftest` (exit 0) and the baseline invocation
above; both reproduced verbatim here.
