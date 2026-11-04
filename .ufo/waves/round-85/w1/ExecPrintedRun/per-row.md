# R85-C2 — ExecPrintedRun per-row results (target tools/round-82/printed-command.py)

Sandbox: declaration bytes 91eeb72f6a7b13dc96e826117956f90ed89ae3f3 + candidate commit
752e7a3e8b3a8a1f8c93aa48f1ac34daf8127cfd. Counter: frozen tools/round-84/mutation-closure.py,
table .ufo/waves/round-85/mutants.json, receipt `after-printed-run.json`.

Pristine outcome (target): exit 0, cases=30, failures=0, green — declared case present and
passing for every row below; candidate sha256 78ddfb4e0451e80f17325ba50745ffc72f81c3fb07013ab98b2abe9f8484cddf.
Declaration-bytes selftest: exit 0, cases=22, failures=0 (`selftest-pristine.txt`).

| id | declared case | status | failing case names under mutant | pristine outcome |
|---|---|---|---|---|
| pc-pin-normprefix | dot-slash-script-refused | killed | dot-slash-script-refused | present, passes; pristine green |
| pc-run-rc1-strict | rc1-without-expectation-executable | killed | rc1-without-expectation-executable | present, passes; pristine green |
| pc-run-counter-type | string-counter-refused | killed | string-counter-refused | present, passes; pristine green |
| pc-run-counter-mismatch-raw | int-counter-equals-string-expectation | killed | int-counter-equals-string-expectation | present, passes; pristine green |
| pc-run-defects-static-dropped | static-defect-ledger-copied | killed | static-defect-ledger-copied | present, passes; pristine green |
| pc-token-metachar-drop-pipe | pipe-metachar-refused | killed | pipe-metachar-refused | present, passes; pristine green |
| pc-token-ellipsis-drop-ascii | ascii-ellipsis-refused | killed | ascii-ellipsis-refused | present, passes; pristine green |
| pc-token-allowlist-widened | unbound-plan-variable-refused | killed | unbound-plan-variable-refused | present, passes; pristine green |

Every row: `declared_case_present=true`, mutant run's failure list is exactly its declared
case (no collateral failures), `restored_equal=true`, anchor_occurrences=1.

Isolated-sandbox note: counter totals on my run are killed=11 / survivors=10 / inconclusive=0;
the 10 survivors are the seven pc rows owned by ExecPrintedCmd plus sb-emdash-optional,
sb-id-substring, cg-frozen-detector-ge (other targets/seats). Exit 1 in this sandbox is the
expected isolated result, not a defect in these eight rows.

Changes to pre-existing cases: none. Candidate additions are eight top-level
`r85b_*` case functions plus three `r85b_`-prefixed fixture helpers at end of file, and one
`# R85-B cases` block of eight one-line `guarded(...)` registrations at the end of `selftest()`
(after the `fixture_roots` cleanup loop).
