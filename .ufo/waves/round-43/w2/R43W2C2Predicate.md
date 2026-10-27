# R43W2C2Predicate — P43-C2 falsification

## Finding (high): score is an honest stop; target predicate is not met

**Measured revision:** `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` (score `--rev` and receipt `revision`). Freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. Lane tip observed at audit: `5856614ac4bf7f2363bbcd1956644474a82108e5`; do not transfer this earlier score result to the later tip without a new score.

The committed receipt `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` explicitly has `checks_ok:false`, `exit_code:1`, and `checks.sources_numstat_three_additions:false` (receipt lines 35, 37, 91). `sources_numstat` is `4\t0\tcorpus/SOURCES.md` (149), whereas P43-C2 requires exactly the appended three round-43 rows and zero deletions. Thus the full C2 target does not pass despite the successful gate and copy audit; the actual exit/status is correctly not green. This is the actionable predicate failure, not a counterexample that should be smoothed over.

## Clause audit

- Freeze ancestry: receipt says `freeze_is_ancestor:true`; scorer records `freeze_ancestor:true` (27, 93).
- Clean clone at measured REV: `clone.exit:0`, `clone_clean:true`, empty `clone_status`; child receipts identify a clone rooted at `/fast/scratch/hyaku/kaidoku-r43/l1-c2-score-final/clone`, `git_root` that same path, and exact revision `77d196c...` (38–43, 64–74, 107–117). This is receipt evidence; I did not independently recreate the clone.
- Gate: child invocation has no `--sources` or `--map` override (94–106); exit 0, `rows_checked:19`, `rows_failed:[]`, `rows_total:137` (108–123, 129, 136–138). This satisfies these measured clauses.
- Copy/provenance audit: scorer reports 136 checks, exit 0, zero failures (86–90). Child argv identifies `verify-copies-r43.py`, exact revision, freeze, and pinned external inputs (44–84). Its embedded stdout begins with EXPECT-source-frozen OK, duplicate-key absence, map version/object, key-set, uniqueness, and regular-copy checks; full output is present as receipt `stdout_text` with `stdout_truncated:false` (80–81). The standalone raw TSV/JSON artifact named by `copy_audit_receipt_path` is in scratch, not the lane; it was not found among committed wave files. Accordingly the committed wrapper provides tool output but not the separately named receipt file.
- Score tool frozen: true; digest at freeze and REV both `459cbcc...` (141–146). Gate tool digest at REV matches `cafe232a...` (125–127). Map digest matches frozen plan value `3158cdc...` (132); S126 preservation is true (139). SOURCES digest at REV is `251ec4a...` (150).
- SOURCE numstat: fails exact planned value: observed `4 0`, expected `3 0` (35, 149). The committed result therefore refuses success as required.
- Frozen-path/map predicates not separately established by this audit beyond receipt fields above. The receipt carries aggregate checks, but full claim includes no symlinks across stated paths, per-copy size cap, third-party firmware exclusion, each disposition/source-anchor derivation, and exact 17-copy/map tree commitments. Embedded audit stdout is lengthy and not independently inspected line-by-line here; no claim of independent validation for those clauses.

## Controls and evidence limits

Committed controls available under `.ufo/waves/round-43/controls/c2/` include CTL-C2-0..3 and gate/audit child outputs for CTL-C2-2. CTL-C2-0 summary says exit 1 (18 rows fail). There is no `controls/c2/c2-at-77d196c6.json`; the measured score is the L1 score path above. The C2 receipt records hashes for the scratch child receipts (`copy_audit_receipt_sha256:50b5...`, `gate_receipt_sha256:705b...`) but scratch files were not present as committed lane evidence. This limits independent byte-level recheck of those separate artifacts; does not negate the score's explicit failure.

## Read-only audit provenance

Plan read first: `plans/round-43-claims.md`, SHA-256 `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`. Score receipt SHA-256 `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6`. Commands: `git -C <lane> log --oneline -20`; `git -C <lane> rev-parse HEAD`; `git -C <lane> show --stat --oneline 77d196c6`; `git -C <lane> show --name-only --format='' 77d196c6`; `sha256sum` on plan and score; `find <lane>/.ufo/waves/round-43 -type f -name '*copy*audit*' -o -name '*c2*score*'`. Score file read at lines 22–150. The attempted hash of nonexistent `controls/c2/c2-at-77d196c6.json` returned ENOENT. No REA/extractor, tests, formatter, install, git mutation, or scratch creation was performed.

**Residual risk / verification gap:** score is for 77d196c, not lane tip 5856614; current-tip P43-C2 status is unmeasured in this seat. Full copy audit raw child receipts are scratch-only; this seat did not rerun the score or independently verify every provenance assertion. Inference: the 4-line numstat likely reflects an additional appended source row, but the specific fourth row is not attributed here absent direct row-level diff evidence.

Report: .ufo/waves/round-43/w2/R43W2C2Predicate.md