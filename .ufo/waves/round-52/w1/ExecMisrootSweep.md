# ExecMisrootSweep — r52-w1

Verdict: settled; lane-side helper drafted at `.ufo/waves/round-52/w1/ExecMisrootSweep/misroot-sweep.sh` (the L1 can port it to the frozen `tools/round-52/` location).

- Classifies `git -C <fleet> status --porcelain` untracked paths by file content; excludes `.scratch/`, `.ufo/state/`, and all `.ufo/waves/` paths. Default is report-only. `--apply` prints lane-classified copy plans and then copies, `cmp`s, and deletes only those files; non-lane entries remain untouched.
- Fixture selftest exit 0: planted lane stray classified, copied byte-exactly (copy operation `cmp`), then removed from fixture; unrelated stray remains. `bash -n` exit 0.
- Exact evidence: `bash -n /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecMisrootSweep/misroot-sweep.sh` exit 0, stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, UTC `2026-10-30T10:46:47Z`; output saved as `ExecMisrootSweep/bash-n.stdout`.
- Exact evidence: `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecMisrootSweep/misroot-sweep.sh --fleet /fast/scratch/hyaku/kaidoku-r52/w1-ExecMisrootSweep/fixture.7kbWiC --lane-seat /fast/scratch/hyaku/kaidoku-r52/w1-ExecMisrootSweep/lane.AXn7NI --selftest` exit 0, stdout SHA-256 `97409b07ec0d2ca0c124e87ec12a5e196b236ef322796d1b2e00992abb2658b6`, UTC `2026-10-30T10:46:47Z`; output saved as `ExecMisrootSweep/selftest.stdout`.
- Mistakes: none observed from this scoped sweep. Operator-side preventive note remains with L1.
- Risks: helper selftest has isolated fixtures, not live fleet sweep. Helper is draft-only; no actual fleet files scanned/copied/deleted. Disk guard `status` was attempted but timed out after 30 seconds (reported /tmp 24%, /var/tmp 41%, /fast/scratch/hyaku 46%). No tools installed.
