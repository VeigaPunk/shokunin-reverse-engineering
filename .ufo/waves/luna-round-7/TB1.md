# TB1 — command-A guard (lane B)

## CLAIM
Command A (`SCORECARD.md:93-123`, recipe body diffed identical in worktree and at HEAD) run with `REV=411175e` returns the pre-integration baseline — 72/72 knowledge files mapped, missing/dangling `[]`, citation rules 9/9, coverage/depth 10.0/10.0 — byte-identical over two runs. The six l7 entries are absent at HEAD, so the round's 78/78 claim is a post-integration target, not reproducible now.

## METHOD
- Recipe body extracted verbatim: `git show 411175e:SCORECARD.md | sed -n '93,123p' > /tmp/tb1-r7/recipe-A-body.sh`; `sed -n '93,123p' SCORECARD.md | diff - /tmp/tb1-r7/recipe-A-body.sh` → identical.
- Two runs from repo root: `REV=411175e337c0725ae9bee3fd478ae9bf05bedf3f bash /tmp/tb1-r7/recipe-A-body.sh > /tmp/tb1-r7/run{1,2}.out` (both exit 0, stderr empty); `diff` + `sha256sum`.
- Guards: `git status --porcelain=v1`, `git diff --name-only HEAD`, `git diff --cached --name-only HEAD`, `git log --oneline -3`, `git reflog -4`, `git stash list`, `git ls-tree -r --name-only HEAD -- corpus/knowledge | grep -c '\.md$'`, plus per-path existence checks for the six l7 files at HEAD and in the worktree.
- Cross-check: `sed -n '11p' .ufo/waves/luna-round-7/receipts/census-pre.txt | diff - /tmp/tb1-r7/run1.out` → no differences.

## FINDINGS
- stdout (both runs): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "411175e337c0725ae9bee3fd478ae9bf05bedf3f", "rule_blocks": 9}`
- stdout sha256 `77b106394efd11dadc4f414c77fa0fbe100e9acf5ca454957320542dc5aa2b79` (run1 = run2; raw copies held at `/tmp/tb1-r7/`).
- 72 knowledge `.md` files at HEAD; all six paths `2026-10-16-l7-01-inspect-go-binary` … `2026-10-16-l7-06-inspect-with-objdump` absent at HEAD and in worktree (agrees with `receipts/census-pre.txt:22-28`; my stdout line diffs clean against `receipts/census-pre.txt:11`).
- No tracked-state drift: `git diff`/staged empty; reflog top is the round-6 records commit; stash empty; observation stamped 2026-10-16T23:10:19Z.

## THREATS
- Recipe A reads Git objects, not the worktree: untracked round-7 artifacts are invisible to it by design; this guards the token set only.
- Snapshot caveat: later seats may write (untracked) artifacts after this check; only the timestamped observation is claimed.
- 78/78 is contingent on integration landing six hyphenated files + six map tokens (ruling a); unverifiable until then, as is "all six pass QUALITY.md" and the byte-identity of the 72 prior entries (outside this seat).
- `revision` embeds the REV string, so raw stdout line-hashes differ across revisions; compare payload fields, not whole-line hashes.

## VERDICT
CLEAN — pre-integration guard held: command A at `411175e` = 72/72 mapped, 9/9 rules, 10.0/10.0, empty missing/dangling; six l7 entries absent; expected post-integration delta is +6 files/+6 map tokens.
