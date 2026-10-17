## CLAIM
C1's recheck-fields clause independently reconfirmed: every current `recheck:` field uses `/tmp` only as scratch (cwd, `TMPDIR`, npm cache); none requires prior `/tmp` contents to persist.

## METHOD
Read-only at HEAD `a280e07`. Enumerated field-style lines: `grep -rIn -iE '^[[:space:]>*-]*recheck[[:space:]]*:' corpus/` → exactly 10 (seven 2026-10-16 l7/l8 entries + three 2026-10-15 lessons). Checked l7-04/l8-01 carrier lines; `test -e`/`ls -ld` on named `/tmp` paths; re-ran the Command A recipe (`SCORECARD.md:94-122`) for REV=a280e07. No probes, network, deletions, or `/tmp` writes.

## FINDINGS
- `/tmp` appears in 4/10 fields: `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5` (cwd + `TMPDIR=/tmp` + `npm_config_cache=/tmp/kaidoku-luna-round-6-npm-cache`), `l7-03:5`, `l7-05:5`, `l8-01:5` (cwd only). `l7-02:5`/`l7-06:5` name none; `l7-04:5` instructs copying the hash-pinned index to an absolute path — its historical `/tmp/bb6-leg-6/sc4-index.db` carrier is documented (`l7-04:9`) but not required.
- No field reads a required result from `/tmp`; targets are stable system paths (`/usr/bin/docker`, `/usr/lib/signal-desktop/signal-desktop`, `/bin/true`, `/usr/bin/rg`, `/usr/bin/jq` control) with expected Evidence IDs in-repo.
- Snapshot state: `/tmp/kaidoku-luna-round-6-npm-cache` exists (dir, Oct 16 19:00); l8-01's `/tmp/luna-round-8-leg-6.sqlite` fixture has an inline regeneration recipe (`l8-01:9`) and is unused by its recheck (refusals precede reads).
- All support citations in `C1.md:8-10` verified at the named files/lines; Command A exited 0 at the pinned REV: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "depth_score": 10.0, "knowledge_files": 79, "mapped": 79}`.

## THREATS
Static only: no recheck executed, so cold-cache/offline npx is untested. The l7-01 cache is scratch-class, not a results store, but its contents may be load-bearing for offline replay — S1 states the same facts at stricter emphasis; neither proves necessity. Legacy `verify:` recipes read retained `/tmp` scratch (e.g. `corpus/knowledge/2026-10-13-r3-renderer-asar.md:11`), outside this clause. Worktree: 0 tracked modifications; round-9 files untracked; only write is this file.

## VERDICT
CLEAN: C1's recheck-fields clause confirmed — `/tmp` is scratch-only in all 10 current recheck fields.
