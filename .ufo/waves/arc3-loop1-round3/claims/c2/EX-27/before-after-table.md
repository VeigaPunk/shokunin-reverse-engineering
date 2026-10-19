| row | before (112d01dc) | after (7cd19c3cfd83) | verdict |
|---|---|---|---|
| A/A1_cp_a | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A2_cp_a_remove_dest | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A3_cp_p | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A4_rsync_a_default | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A5_rsync_a_inplace | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A6_tar_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A7_copy_new_then_mv | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A8_inplace_modify_no_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A9_inplace_modify_then_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A10_restore_bytes_plus_touch_r | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A11_hardlink_alias_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A12_reflink_replace | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A13_rename_swap_pristine_hardlink | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A9s_truncate_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A10s_truncate_restore_touch | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A11s_hardlink_truncate_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A14_chmod_only | verdict=METADATA-DRIFT exit=12 sha_same=yes sha_only_view=BLIND | verdict=METADATA-DRIFT exit=12 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A15_delete_after_capture | verdict=ABSENT exit=13 sha_same=no sha_only_view=caught | verdict=ABSENT exit=13 sha_same=no sha_only_view=caught | HOLD |
| B/r1-canonical-vs-live | exit=10 label_defect=4 sha_agree=4 | exit=10 label_defect=4 sha_agree=4 | HOLD |
| B/r1-canonical-vs-fresh-v2 | exit=10 label_defect=4 sha_agree=4 | exit=10 label_defect=4 sha_agree=4 | HOLD |
| B/r1-metadata-pipe-vs-live | exit=10 label_defect=8 sha_agree=4 | exit=10 label_defect=8 sha_agree=4 | HOLD |
| B/r1-sums-vs-live | exit=10 sha_agree=4 | exit=10 sha_agree=4 | HOLD |
| B/ex35-partial-1of5-default | exit=0 require5_supported=no | exit=0 require5_supported=yes | HOLD |
| B/ex35-corrupt-sha-vs-live | exit=10 sha_agree=3 | exit=10 sha_agree=3 | HOLD |
| B/ex35-swap-sha-vs-live | exit=10 sha_agree=2 | exit=10 sha_agree=2 | HOLD |
| B/ex35-absent-path-vs-live | exit=10 sha_agree=3 | exit=10 sha_agree=3 | HOLD |
| B/junk-receipt | exit=2 | exit=2 | HOLD |
| B/synth-v1-stanza-vs-live | exit=12 label_defect=1 | exit=12 label_defect=1 | HOLD |
| B/synth-v1-sums-vs-live | exit=0 | exit=0 | HOLD |
| B/synth-v1-pipe-vs-live | exit=12 label_defect=1 | exit=12 label_defect=1 | HOLD |
| C/v2-utc-render-correct | exit=0 | exit=0 | HOLD |
| C/v2-utc-render-tz-invariant |  |  | HOLD |
| C/v1-label-defect-declared | exit=10 label_defect=4 | exit=10 label_defect=4 | HOLD |
| D/selftest-existing-scratch | exit=0 cases=15 | exit=0 cases=22 | HOLD |
| D/selftest-missing-scratch | exit=1 traceback=yes | exit=2 traceback=no | HOLD |
| E/d2-eacces-capture | exit=1 read_error=no | exit=14 read_error=yes | HOLD |
| E/d2-failopen-both-absent | verdict=MATCH exit=0 | verdict=UNEVALUABLE exit=14 | HOLD |
| E/d2-live-unreadable | exit=1 traceback=yes | exit=14 traceback=no | HOLD |
| E/writeguard-paths-eq-out | exit=0 clobbered=yes | exit=2 clobbered=no | HOLD |
| F/live-pair-capture-vs-capture | verdict=MATCH exit=0 | verdict=MATCH exit=0 | HOLD |
| F/receipt-self-pin |  |  | HOLD |
