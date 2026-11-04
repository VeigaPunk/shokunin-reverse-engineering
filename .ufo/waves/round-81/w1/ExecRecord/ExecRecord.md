# ExecRecord — round 81 C2 candidate

Axes: calibration + depth; this slice improves committed-record integration depth only. No domain-coverage claim, promotion, or admission vote.

## Delivered

Candidate: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/strictness-battery.py`.
SHA256: `6bffdbc1c2f027c7b70cadfb70aabdf5ec6a9e3a6067484886d3560fad3efe3c`.
Copied round-80 battery, inserting only the two integration cases into selftest. Existing nine cases, scorer, CLI argument handling, and sole fixture commit call remain unchanged.

- `record-fixture-committed-clean`: real binder battery at HEAD; five matched, no mismatches/unparsed/duplicates, ok true.
- `record-fixture-committed-duplicate`: six matched cells, exactly `omp-pin` duplicated, no mismatches/unparsed, ok false.
- Real parser, git_show, declared_ok, bind and battery are not replaced. Only read_lines is redirected to synthetic fixture lines. Unknown inputs return None, never real-file fallback. Fake GHIDRA_INSTALL_DIR and read_lines are restored in finally.
- After committing each record, the worktree record is deliberately replaced with `not a record`. Passing pristine cases therefore distinguish committed bytes from worktree bytes, independently of the missing-commit mutation.
- Binder Unevaluable is caught locally so missing HEAD produces named pass=false cases and SELFTEST summary rather than a crash.

## Exact bounded evidence

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/counter.json` retains full pristine/mutant JSON cases, stdout/stderr, target and binder hashes. Frozen counter SHA256 `52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6`; binder SHA256 `a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438`.

Measured fixture revision: `def872d219d2681f580ff5b90fe19228b6db8d54` (scratch only; deleted after receipts).
Frozen counter exit 0: mutants 1, killed 1, survivors 0. Pristine exit 0, SELFTEST cases=11 failures=0. Commit-omission mutant exit 1, SELFTEST cases=11 failures=2. Both added cases report `PROVINCE.md absent at HEAD`; the unique declared clean case has pass=false. The original nine cases still pass in both arms. Both stderr streams are empty.

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/demonstration.json` retains exact argv, exit and guarded fixture root. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/demonstrate.py` is the reproducible bounded evidence driver. It copies binder and counter from frozen commit abdcfd3c28d98288a3dc6b4e98c88d115ed42b53, verifies fixture --show-toplevel before commit, and supplies TMPDIR and counter --work explicitly.
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/cleanup.json` records removal of the one scratch tree `/fast/scratch/hyaku/kaidoku-r81/ExecRecord`.
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/canonical-selftest.json` retains the canonical tools/round-81 layout demonstration without sibling binder: exit 0, SELFTEST cases=11 failures=0, empty stderr.

No repository build/test/lint sweep, lane git writes, production edits, real configuration reads, installs, or external-state remediation were performed. Mounted tool inventory has no LSP definition/reference/refactor tool; used displayed source instead, not a cold empty symbol result.

## Opened source and decision evidence

Opened 2026-11-04: https://git-scm.com/docs/git-show, official documentation, DESCRIPTION: “For plain blobs, it shows the plain contents.” This supports the specific claim that the real binder's git-show blob read is a committed-object boundary; the working-tree disagreement demonstration supplies local behavioral evidence. Reuse existing SOURCE S255 by URL; do not create another SOURCE row. Source scope extends from prior pinned-blob uses to R81 committed fixture selftests; L1/source-curation owner handles used-by update.

Opened rejection: https://git-scm.com/docs/git-cat-file, options excerpt “Exit with zero status if <object> exists and is a valid object.” Existing SOURCE S256, no new row. Reject as the primary command-semantics anchor here: actual binder git_show invokes git show, not cat-file. Flip condition: if the binder implementation used cat-file for this boundary, its manual would become the directly applicable anchor. This is a source-selection decision, not a fleet admission vote.

## Risks / integration boundary

ReviewerC2-13 conveyed L1's decision to preserve canonical selftest execution. Final candidate lines 275-278 prefer sibling pointer-bind.py (counter materialization), falling back to ../round-80/pointer-bind.py for the canonical tools/round-81 layout. No production binder copy or mocked implementation is introduced. Both layouts were demonstrated using scratch-only files. Existing non-selftest CLI semantics remain untouched. L1 owns final integration and integrated gates. Counter receipt proves the scratch candidate only, not a measured production commit.

No other blockers. Report location follows the stricter own-seat-directory write boundary rather than the conflicting outer-directory trailer.

## Self-evaluation

Accuracy 4/5: exact retained receipts, but no integrated production revision measured. Completeness 4/5: both layouts and assigned mutation demonstrated; L1 integration remains outside this seat. Clarity 4/5: dependency lookup explicitly described. Actionability 4/5: candidate and reproducible receipt paths supplied; L1 must integrate. Conciseness 4/5: provenance details make this longer than the terminal summary. Overall 4.0/5. Improvement: L1 should use the retained candidate digest when integrating. User agreement expected on scoped implementation, not production admission.

Report: .ufo/waves/round-81/w1/ExecRecord/ExecRecord.md
