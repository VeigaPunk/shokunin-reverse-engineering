| manoeuvre | REV | C1 freeze walk | C2 freeze walk | C1 CLI (full counter) | note |
|---|---|---|---|---|---|
| S0_benign_nonfrozen | 1eb3f68d20df | touched [] | exit 1 reason=None mismatches=9 | exit 1 reason=None |  |
| S1a_touch_restore_c1counter | 7f39e580dcff | touched ['tools/round-49/c1-counter.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S1b_touch_restore_c2mismatch | 6e1e7c0c5cd3 | touched ['tools/round-49/c2-mismatch.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S1c_touch_restore_c1controls | 43bc8c725e7e | touched ['tools/round-49/c1-controls.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S1d_touch_restore_carriers | 632a5c459bc7 | touched ['tools/round-49/carriers.json'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S1e_touch_restore_c1oracle | 4c1b146cab9f | touched ['tools/round-49/c1-oracle.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S2a_new_file_tools | 9964698f297a | touched [] | exit 2 reason=frozen_path_changed mismatches=None | exit 1 reason=None |  |
| S2b_new_file_nested | 1af3e9b15e7b | touched [] | exit 2 reason=frozen_path_changed mismatches=None | exit 1 reason=None |  |
| S3a_merge_commit_edits_carriers | cddcf655a0f6 | touched ['tools/round-49/carriers.json'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S3b_side_edit_reverted_in_merge | e1a312ca4886 | touched ['tools/round-49/carriers.json'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S3c_side_new_tool_merged | 883929f0c092 | touched [] | exit 2 reason=frozen_path_changed mismatches=None | exit 1 reason=None |  |
| S4_rename_inside | d1569a21839a | touched ['tools/round-49/c1-controls.py', 'tools/round-49/c1-ctl.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S5_rename_out | 38b7a5321d82 | touched ['tools/round-49/c2-mismatch.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S6_rename_in_nonfrozen | 9cc58fa4e169 | touched ['tools/round-49/README.md'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S7_mode_change | 752f82af77cd | touched ['tools/round-49/c1-counter.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S8_symlink_swap | ac5f3c20db8a | touched ['tools/round-49/c2-mismatch.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S9_delete_file | 1f37d9ce9b11 | touched ['tools/round-49/c1-oracle.py'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed |  |
| S3d_side_edit_revert_on_side | 35eacf9fc42a | touched ['tools/round-49/carriers.json'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed (matrix) | freeze=34a25bac3921 |
| S10_rev_is_base | e4f2cfa5ebff | touched ['plans/round-49-claims.md', 'tools/round-49/c1-counter.py', 'tools/round-49/c1-run.sh', 'tools/round-49/carriers.json'] | exit 2 reason=freeze is not an ancestor of rev mismatches=None | not run | freeze=34a25bac3921 |
| S11_sibling_readd | db1acabb1c84 | touched ['plans/round-49-claims.md', 'tools/round-49/c1-controls.py', 'tools/round-49/c1-counter.py', 'tools/round-49/c1-oracle.py', 'tools/round-49/c1-run.py', 'tools/round-49/c1-run.sh', 'tools/round-49/c2-mismatch.py', 'tools/round-49/carriers.json'] | exit 2 reason=freeze is not an ancestor of rev mismatches=None | exit 2 reason=frozen_path_changed (matrix) | freeze=34a25bac3921 |
| S12_quoted_name_edit | e3cacfaa93f6 | touched [] | exit 2 reason=frozen_path_changed mismatches=None | exit 1 reason=None (matrix) | freeze=70293a992355 |
| S13_refreeze_operator_freeze | a6e75abc3bd5 | touched [] | exit 1 reason=None mismatches=9 | exit 2 reason=frozen_path_changed (matrix) | freeze=55de4cf94cd9 |
| S14_plain_copy_add | 2dff007a801c | touched [] | exit 2 reason=frozen_path_changed mismatches=None | exit 1 reason=None (matrix) | freeze=34a25bac3921 |
| S15b_replace_on (X replaced by tree=FREEZE commit) | e42dda7652b5 | touched [] | exit 1 reason=None mismatches=9 | exit 1 reason=None (matrix) |  |
| S15b_GIT_NO_REPLACE_OBJECTS=1 (mitigation probe) | e42dda7652b5 | touched ['tools/round-49/c2-mismatch.py'] | exit 2 reason=frozen_path_changed mismatches=None | not run (walk probe only, env set) |  |
| S27_squash (one commit, FREEZE tree) | 3aa86b104e81 | touched [] | exit 1 reason=None mismatches=9 | exit 1 reason=None (matrix) |  |
| S16_grafts (.git/info/grafts cuts touching commit) | 4eeae0a6c31e | touched [] | exit 1 reason=None mismatches=9 | exit 1 reason=None (matrix) |  |
| S24_plan_edit | d7fe2d93c2b6 | touched ['plans/round-49-claims.md'] | exit 2 reason=frozen_path_changed mismatches=None | exit 2 reason=frozen_path_changed (matrix) |  |
| S25_round42_fixtures_edit (plan: byte-frozen) | 59adefa60a98 | touched ['tools/round-42/fixtures.json'] | exit 1 reason=None mismatches=9 | exit 2 reason=frozen_path_changed (matrix) |  |
| S26_round44_oracle_edit (plan: byte-frozen) | 91e46038d475 | touched ['corpus/evidence/round-44/oracle/manifest.json'] | exit 1 reason=None mismatches=9 | exit 2 reason=frozen_path_changed (matrix) |  |
