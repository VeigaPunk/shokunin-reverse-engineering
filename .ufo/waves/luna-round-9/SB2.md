# SB2 — sentinel append-only 2 / non-target byte-identity (lane B, deepseek-v4.1-flash)

## CLAIM
At the wave's current end state the entire tracked tree — both of the round's knowledge-file append targets included — is byte-identical to lane-A T2's pre-landing baselines at `HEAD a280e07`; no append has landed, so append-only holds with zero drift and every non-target file is byte-identical.

## METHOD
Three read-only captures, `2026-10-16T21:59:16`–`21:59:57 -03:00`: `date -Is`; `git rev-parse HEAD`; `git diff --quiet HEAD --`; `git status --porcelain=v1 -uno` and `-uall`/`--ignored`; `git stash list`; `git hash-object` vs `git rev-parse HEAD:<path>`; T2's protocol on both targets — `wc -c`, `sha256sum`, `head -c 64080 | sha256sum`, `head -c 16295 | sha256sum`, `tail -c 64 | sha256sum`, `tail -c 64 | base64 -w0`; `sha256sum PROVINCE.md`. No probes, network, or deletions; sole write is this report.

## FINDINGS
- **Targets vs T2** (`.ufo/waves/luna-round-9/T2.md:8-9`), identical in all three captures: r4-16 `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` 64,080 B, sha256 `622e3661…cce1d22e`; `head -c 64080` → same hash; tail-64 `908ced6d…9073ee`; base64 `Y2g7…Cg==`. jq-shadow `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md` 16,295 B, sha256 `541f3499…fe4dbf2e`; `head -c 16295` → same hash; tail-64 `374023ff…361e3bd7`; base64 `Z2Vk…Cg==`. Full-file equality makes prefix identity trivially true; mtimes unchanged (2026-10-14 04:54:37 / 2026-10-13 14:15:43). No append is present, matching `.ufo/waves/luna-round-9/S2.md:12`.
- **Non-target identity**: `tracked-diff-exit=0`; 0/170 tracked files modified; 0 stashes; worktree `git hash-object` == HEAD blob for both targets (`8116e6fa…`, `0b5e15c0…`) and PROVINCE (`8a1cec88…`); 0 untracked and 0 ignored entries outside `.ufo/` (untracked total grew 848→855 — concurrent seats, all under `.ufo/`).
- PROVINCE.md sha256 `fe7f3f61…` (18,590 B) equals the round-7 pin (`.ufo/waves/luna-round-7/CB6.md:10`) — untouched.

## THREATS
"End state" here is the pre-landing tree; no landing exists to certify. If integration later lands the two appends, rerun `head -c 64080 | sha256sum` / `head -c 16295 | sha256sum` vs `T2.md:8-9` to prove prefix identity. Ignored/binary files outside the index are outside the byte-identity claim. Command A was not rerun here (S2/E2/T1 cover it).

## VERDICT
CLEAN — zero drift: both append targets equal T2's baselines; all 170 tracked files byte-identical to `a280e07`.
