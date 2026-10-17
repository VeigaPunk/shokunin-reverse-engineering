# TB1 — command-A guard (lane B)

## CLAIM
Command A (SCORECARD.md:92-123) at HEAD `f0e8cde` reproduces the unchanged baseline — 72/72 knowledge files mapped, 9/9 rule blocks citation-resolved, coverage/depth 10.0/10.0, no missing/dangling tokens — and lane B did not change tracked state.

## METHOD
- `git rev-parse HEAD` → `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`. Recipe A run verbatim, twice, with `REV=f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`, from repo root; stdout captured to `/tmp/tb1-r6/run{1,2}.out`; `diff` + `sha256sum`.
- Guard: `git status --porcelain=v1`, `git diff --exit-code HEAD --stat`, `git diff --cached --stat HEAD`, `git log --oneline -3`, `git reflog -5`, `git stash list`.

## FINDINGS
- Runs byte-identical. stdout: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "f0e8cdecb216d71cf7df974675c0f6b16ba4f82f", "rule_blocks": 9}`
- stdout sha256 `258dc8695e0fa3809a9aceb289077b0e0c66a5c1b7d020cfb32b4db7d5567b45` (both runs).
- Token set + scores unchanged vs every r5 recorded measurement (mapped 72, 9/9, 10.0/10.0 — SCORECARD.md:353-356, 395-398, 441-444). No drift.
- Tracked state at check (2026-10-16T22:01Z): `git status --porcelain` shows only untracked `?? .ufo/interactive-sessions/` and `?? .ufo/waves/` (expected wave artifacts); `git diff --exit-code HEAD` clean, nothing staged — lane B changed no tracked file.
- No lane-B history mutation: HEAD still `f0e8cde`, reflog top entry is the r5 records commit, stash empty.

## THREATS
- Recipe A reads Git objects via `git show`, not the worktree: intra-round lane-B writes under untracked `.ufo/` are invisible to it by design; this guards the token set, not untracked artifacts.
- Snapshot caveat: later lane-B seats (battery legs 2-10) may write after this check; only the timestamped observation above is claimed.
- The `revision` field embeds the REV string, so cross-revision comparison must use the JSON payload fields, not the raw line hash.

## VERDICT
CLEAN — command A at `f0e8cde` returns the unchanged 72/72, 9/9, 10.0/10.0 baseline; no tracked-state drift attributable to lane B at check time.
