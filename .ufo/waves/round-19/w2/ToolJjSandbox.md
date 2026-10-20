# ToolJjSandbox — round-19 wave-2 falsification

**Disposition:** no current environment/path escape reproduced. The candidate’s guards refused actual external pointer and marker targets in isolated `/tmp` fixtures. Two **LOW, test-only** gaps remain in the added selftest; details below. Author-side review, not an outside-verifier admission.

## Scope and freshness

- **[O]** The assigned path `.ufo/waves/round-19/round-18/tools/jj-red-before.py` does not exist. The single matching file is `.ufo/waves/round-18/tools/jj-red-before.py`; that is the reviewed target.
- **[O]** Lane `refs/heads/main` and the sandbox checkout both resolved to B, `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. B’s script blob SHA-256 was `cc2d7fb4d04b2ad6ef51d2aed52d743da780ec024defcd8891df9d4c3743a892`; the current working-tree candidate was `0b8522b00897694148fcc23b0643163709cbffc3a232ea1d23a8dac7e3eeaed7`. I copied the latter to a separate candidate file in `/tmp/kr19-w2-ToolJjSandbox` and tested that copy, keeping the clone’s checked-out B file intact. Thus the reviewed behavior is the current worktree delta, not the older B blob.
- **[O]** The caller `.ufo/waves/round-18/verify.py:118-124,191-192` inherits `os.environ` when launching the probe; its Python command is `python3 -I -B` (`:36`). The candidate removes `GIT_*`, `JJ_*`, and `TMPDIR` at `main()` entry (`jj-red-before.py:1209-1213`), filters them into explicit child environments (`:123-138,189-205`), and scrubs the process environment around the in-process `revpin` call (`:141-149,208-221`). The two `jj` invocations receive the explicit `jjenv` (`:347-350,394-398`).
- No lane source was edited. All `jj` mutation tests ran in fixture clones under `/tmp`; no `jj` command targeted the lane. No tools were installed.

## Findings

### LOW — Relative-traversal selftest does not check the file its pointer resolves to

**[O]** In `jj-red-before.py:1157-1168`, `escape_case` creates the victim under the selftest’s `tmp` directory. The relative case uses `../` plus that victim’s basename (`:1181`). But `evaluate()` builds a separate `tempfile.mkdtemp(dir="/tmp")` sandbox (`:296-312`), so this pointer resolves to `<evaluate-temp>/victim-rel.md`, not the selftest victim. `pick_cited_line()` selects only an existing file (`:270-289`); the relative case therefore falls back to `SCORECARD.md`. The `unchanged` assertion at `:1168` is vacuous for that relative target.

Mutation evidence: with `_inside()` changed in a sandbox copy to return `True`, `python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-path.py --selftest` exited **1**, but its relative-case detail was `exit=0 refusal=None unchanged=True`. This confirms the suite notices the missing refusal, but not an actual write through that relative path. Independently, a fixture pointer to the existing external file `../../kr19-w2-ToolJjSandbox/pointer-victim.md` was refused by the candidate (`evaluate` exit **2**, cause `pointer_table_path_outside_sandbox`, victim unchanged); the same fixture against the mutated guard rewrote the victim to `OFF-BRANCH REWRITE by jj-red-before ...` (`evaluate` exit **1**). **[I]** The production containment check is effective for this path; the selftest should point its `..` case at the actual existing external victim so it also proves non-mutation, not just refusal.

### LOW — Selftest does not protect the `TMPDIR` scrub contract against regression

**[O]** `_dirty_key()` currently includes `TMPDIR` (`jj-red-before.py:123-125`), but the env selftest canaries only `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `JJ_OPERATION_ID` (`:1121-1132`). `_shim_observations()` also classifies keys by calling the same `_dirty_key()` (`:1026-1039`). I changed only a sandbox copy’s predicate to omit `TMPDIR`, then ran `env TMPDIR=/tmp/kr19-w2-ToolJjSandbox/TMPDIR-CANARY python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-tmpdir.py --selftest`; it reported `SELFTEST: CLEAN cases=9`, exit **0**. The current candidate’s predicate is correct by inspection, but this selftest cannot catch a regression that drops the `TMPDIR` rule. Add a TMPDIR canary and classify it independently of the predicate under test.

## Runtime observations

- **[O]** `python3 -I -B /tmp/kr19-w2-ToolJjSandbox/candidate-jj-red-before.py --selftest` → `SELFTEST: CLEAN cases=9`, exit **0** (Python 3.14.8, Git 2.56.0, jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5).
- **[O]** A separate fixture pointer-table attack to the existing external victim above returned the named `pointer_table_path_outside_sandbox` refusal (inner evaluator exit **2**) and preserved victim bytes. An outside-target symlink at `JJ_RED_BEFORE_MARKER.txt` returned `marker_path_outside_sandbox` (inner evaluator exit **2**) and preserved victim bytes. Both fixtures and all mutations were confined to `/tmp`.
- **[O]** `python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-env.py --selftest` with `_dirty_key()` replaced by `return False` → `SELFTEST: FAILED cases=9` naming the env-scrub case, exit **1**. The built-in test therefore detects broad GIT/JJ filtering loss.
- **[O]** Running the candidate selftest with inherited `GIT_DIR`, `GIT_INDEX_FILE`, and `GIT_WORK_TREE` aimed at the sandbox clone returned `SELFTEST: CLEAN cases=9`, exit **0**; clone HEAD remained B and its index SHA-256 was unchanged (`2302798b214b13b9de4cd20bf1cf72a0737387ab178234f596901078b2bd08bd` before and after).

## Commands and exit codes

```text
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-ToolJjSandbox && git -C /tmp/kr19-w2-ToolJjSandbox checkout -q --detach 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 && git -C /tmp/kr19-w2-ToolJjSandbox rev-parse HEAD
# exit 0; printed 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0

python3 -I -B /tmp/kr19-w2-ToolJjSandbox/candidate-jj-red-before.py --selftest
# exit 0; SELFTEST: CLEAN cases=9

env GIT_DIR=/tmp/kr19-w2-ToolJjSandbox/.git GIT_INDEX_FILE=/tmp/kr19-w2-ToolJjSandbox/.git/index GIT_WORK_TREE=/tmp/kr19-w2-ToolJjSandbox python3 -I -B /tmp/kr19-w2-ToolJjSandbox/candidate-jj-red-before.py --selftest
# exit 0; SELFTEST: CLEAN cases=9; HEAD/index hashes unchanged

python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-env.py --selftest
# exit 1; env-scrub mutation detected

python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-path.py --selftest
# exit 1; path mutation detected, with the relative-victim limitation above

env TMPDIR=/tmp/kr19-w2-ToolJjSandbox/TMPDIR-CANARY python3 -I -B /tmp/kr19-w2-ToolJjSandbox/mutant-tmpdir.py --selftest
# exit 0; TMPDIR mutation not detected
```

The two direct pointer-table harness calls used `build_fixture_lane()` plus `evaluate()` in the copied candidate module with (1) `file="../../kr19-w2-ToolJjSandbox/pointer-victim.md"` and (2) symlink `JJ_RED_BEFORE_MARKER.txt` to an external victim. The harness process exited **0** after printing the inner evaluator receipt; the receipt outcomes are recorded above. The corresponding unguarded traversal mutation rewrote the victim before the harness restored it.

## Residual risk and verification gaps

- **[O]** The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”; the mounted-device list contained no `lsp`), so no LSP status/references/definition/diagnostics were available. Literal `grep` was used only to locate the verifier caller and runner call sites; semantic judgments above come from source reads and fixture execution, not grep output.
- **[O]** The env shim observes Git children; it does not wrap `jj` itself. The current source explicitly supplies scrubbed `jjenv` at `:347-350,394-398`, but there is no separate captured environment record from the `jj` process.
- No ordinary lane run, broad suite, build, formatter, or REA operation was performed. The supplied path discrepancy is noted above; review is limited to the actual round-18 script’s current worktree delta.