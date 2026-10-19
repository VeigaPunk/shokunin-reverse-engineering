# EX-27 round-4 regression — before → after (measured, not asserted)

before  = round-3 landed tool `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 lines)
after   = round-4 landed tool `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 lines)

| leg/row | before (`7cd19c3c`) | after (`29bb45ae`) |
|---|---|---|
| A/A1_cp_a | HOLD exit=11 verdict=REWRITE-DRIFT | HOLD exit=11 verdict=REWRITE-DRIFT |
| A/A8_inplace_modify_no_restore | HOLD exit=10 verdict=CONTENT-DRIFT | HOLD exit=10 verdict=CONTENT-DRIFT |
| A/A12_reflink_replace | HOLD exit=11 verdict=REWRITE-DRIFT | HOLD exit=11 verdict=REWRITE-DRIFT |
| A/A14_chmod_only | HOLD exit=12 verdict=METADATA-DRIFT | HOLD exit=12 verdict=METADATA-DRIFT |
| A/A15_delete_after_capture | HOLD exit=13 verdict=ABSENT | HOLD exit=13 verdict=ABSENT |
| B/r1-canonical-vs-live | HOLD exit=10 label_defect=4 sha_agree=4 | HOLD exit=10 label_defect=4 sha_agree=4 |
| B/ex35-partial-1of5-default-vs-require5 | HOLD exit=0 require5_exit=2 | HOLD exit=0 require5_exit=2 |
| B/synth-v1-stanza-vs-live | HOLD exit=12 label_defect=1 | HOLD exit=12 label_defect=1 |
| B/synth-v1-sums-vs-live | HOLD exit=0 | HOLD exit=0 |
| C/v2-utc-render-tz-invariant | HOLD  | HOLD  |
| C/v1-label-defect-declared | HOLD exit=10 label_defect=4 | HOLD exit=10 label_defect=4 |
| D/selftest-missing-scratch | HOLD exit=2 traceback=False | HOLD exit=2 traceback=False |
| E/d2-eacces-capture | HOLD exit=14 | HOLD exit=14 |
| E/d2-failopen-both-absent | HOLD exit=14 verdict=UNEVALUABLE | HOLD exit=14 verdict=UNEVALUABLE |
| E/writeguard-paths-eq-out | HOLD exit=2 clobbered=False | HOLD exit=2 clobbered=False |
| F/live-pair-capture-vs-capture | HOLD exit=0 verdict=MATCH | HOLD exit=0 verdict=MATCH |
| F/scratch-live-pair-form | HOLD exit=0 verdict=MATCH | HOLD exit=0 verdict=MATCH |
| F/receipt-self-pin | HOLD receipt_pin=7cd19c3cfd83 | HOLD receipt_pin=29bb45ae0fd7 |
| G/a-sidecar-path-of-scoped-file | HOLD exit=0 clobbered=True | HOLD exit=2 clobbered=False |
| G/a2-sidecar-hardlink-alias | HOLD exit=0 clobbered=True | HOLD exit=2 clobbered=False |
| G/a3-control-ordinary-capture | HOLD exit=0 receipt_and_sidecar_written=True | HOLD exit=0 receipt_and_sidecar_written=True |
| G/b-out-parent-not-a-directory | HOLD exit=1 traceback=True | HOLD exit=2 traceback=False |
| G/b2-out-empty-arg | HOLD exit=2 traceback=False | HOLD exit=2 traceback=False |
| G/c-coverage-gate-duplicate-stanzas | HOLD exit=0 | HOLD exit=2 coverage_line=REFERENCE-COVERAGE: 1/5 paths present in reference |
| G/c2-coverage-gate-distinct-five | HOLD exit=0 verdict=VERDICT: MATCH  paths=5 | HOLD exit=0 verdict=VERDICT: MATCH  paths=5 |
| G/d-both-absent-plain | HOLD exit=0 verdict=MATCH | HOLD exit=0 verdict=MATCH |
| G/d2-both-absent-error-carrying | HOLD exit=14 verdict=UNEVALUABLE | HOLD exit=14 verdict=UNEVALUABLE |
| G/d3-readme-ruling-text | HOLD hits=0 | HOLD hits=10 |
| I/eq-same-content-rewrite-inplace-ctime-pin | HOLD exit=11 verdict=REWRITE-DRIFT | HOLD exit=11 verdict=REWRITE-DRIFT |
| I/eq-content-drift | HOLD exit=10 verdict=CONTENT-DRIFT | HOLD exit=10 verdict=CONTENT-DRIFT |
| I/eq-metadata-drift | HOLD exit=12 verdict=METADATA-DRIFT | HOLD exit=12 verdict=METADATA-DRIFT |
| I/eq-absent | HOLD exit=13 verdict=ABSENT | HOLD exit=13 verdict=ABSENT |
| I/eq-unparsable-receipt-usage | HOLD exit=2 | HOLD exit=2 |
| J/readme-exit-map-covers-tool-constants | HOLD  | HOLD  |
| J/readme-case-count-mentions | HOLD counts=[2, 22] | HOLD counts=[2, 28] |
| H/nonvacuity-baseline-sidecar | HOLD exit=0 clobbered=True | HOLD exit=0 clobbered=True |
| D/selftest-case-count | — | HOLD exit=0 cases=28 names_found=28 |
| D/selftest-prior-case-names-retained | — | HOLD names_found=28 |
| H/sabotage-sidecar-arm-removed | — | HOLD check_goes_red=True sabotage=applied 1 substitution(s) |
| H/sabotage-sidecar-alias-arm-removed | — | HOLD check_goes_red=True sabotage=applied 1 substitution(s) |
| H/sabotage-coverage-basis-reverted | — | HOLD check_goes_red=True sabotage=applied 1 substitution(s) |
| H/sabotage-unevaluable-arm-removed | — | HOLD check_goes_red=True sabotage=applied 1 substitution(s) |

Tally: before rows=70 hold=70 fail=0 obs=0; after rows=75 hold=75 fail=0 obs=0
