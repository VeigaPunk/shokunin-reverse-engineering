# ExecC2 independent seam report

Detailed comparison: `.ufo/waves/round-70/w1/ExecC2/rederive.md`.

Evidence retained under `.ufo/waves/round-70/w1/ExecC2/`: `harness.py`, aggregate `evidence.json`, `producer-checks.json`, and twelve scenario JSON records (`base-*`, `freeze-*`, `battery-1.json`, `battery-2.json`). Exact invocations, stdout, stderr, return codes and producer pins are retained.

Observed: base impostor executed before rejection; frozen impostor did not execute. Base broken node reported an inventory floor; freeze named broken_tool. Base malformed packer crashed; freeze refused its hash without traceback. Base/freeze selftests passed 20/23 cases respectively. Real pinned-copy runs passed 3/3 and 4/4; base pack/unpack argv ignored the copy while freeze used it. Frozen environment registry adds three cases; live audit names only HOME/LANG/PATH/TMPDIR under work. Two frozen mutation runs using the same work root returned distinct work_dir values and killed all five mutants. Genuine frozen receipt passed its producer-bound checker; changing producer hash alone was rejected.

No official seam-probe invocation. Full base 0/7 not independently measured; see detailed limitations. No repairs or instrument edits. No tools installed; scratch removed. No blockers for assigned experiments.

VERDICT: met — assigned independent R70-C2 experiments support the repairs and reproduce the base defects; full predicate remains parent integration evidence.
