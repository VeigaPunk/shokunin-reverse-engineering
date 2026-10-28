- **22. Freeze integrity: decide from the arm, not the tip.** <!-- freeze-integrity-table v1 --> S140 (git-status porcelain v1) fixes the dirty arm's parse; the gate is `tools/round-45/frozen-path-preflight.py`.

  | trigger | arm | exit | receipt |
  |---|---|---|---|
  | no commit in FREEZE..REV touches a frozen path | commit | 0 | `verdict: clean` (corpus/lessons/round-44.md:18) |
  | post-freeze commit touches a frozen path | commit | 1 | `frozen_path_changed` (corpus/lessons/round-44.md:63) |
  | path touched then restored to its FREEZE bytes | restored | 1 | `restored: [...]` (corpus/lessons/round-44-verifier-spotcheck.md:89-92) |
  | worktree dirty under the frozen pathspec | dirty | 1 | `dirty: [...]` (corpus/lessons/round-44.md:88) |
  | directory freeze scored without --pathspec | pathspec | 2 | `pathspec_required` (plans/round-45-claims.md:1) |
  | freeze revision unknown to the repo | commit | 2 | `unknown freeze revision` (plans/round-45-claims.md:20) |
  | freeze is not an ancestor of rev | commit | 2 | `freeze is not an ancestor of rev` (plans/round-45-claims.md:24) |
  | bulk sweep commits frozen fixtures with unrelated paths | commit | 1 | `touched: [...]` (corpus/lessons/round-44.md:63) |
