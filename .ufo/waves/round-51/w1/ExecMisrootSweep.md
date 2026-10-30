# ExecMisrootSweep

## Result
Drafted `ExecMisrootSweep/misroot-sweep.sh`; did not run against the actual fleet/lane trees and did not apply changes there. Operator-side preventive control is out of scope.

## Behavior
Default mode reports all untracked files from `git -C <fleet> status --porcelain --untracked-files=all -z` with no pathspec. Classification checks content and filename; `.ufo/state/` and `.scratch/` are protected even if they contain lane keywords. `--apply` prints proposed actions, then only for lane-classified files creates destination parents, refuses overwrite, copies, verifies byte equality with `cmp`, and removes the source. `--selftest` creates a fixture under `${TMPDIR:-/tmp}`, verifies its top-level before committing, and scopes fixture identity config to that repo.

## Evidence
Selftest command: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ExecMisrootSweep/misroot-sweep.sh --selftest`
Observed exit: 0. Output included `SELFTEST PASS: content-classified stray copied byte-exact then removed; foreign and protected untouched`; the lane fixture source was absent and destination content matched, and foreign/protected fixture strays remained. UTC: `2026-10-30T04:58:00Z`. Exact stdout SHA-256: `931e0dac4d21258695d6e2e46f0fbf3fed5bf9427d6ea532c483e8e591143b9f`. Raw stdout retained in scratch only.

## Mistakes
No fleet-repo untracked files were created by this seat, so no copy/cmp/delete protocol was needed.

## Risks / blockers
Content matching is substring-based and text-oriented; actual lane/fleet apply was not run. Operator-side preventive control is out of scope. No tools installed.