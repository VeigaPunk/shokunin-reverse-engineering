## CLAIM
SE1–SE4 hygiene claims re-checked against live state (2026-10-16 19:00–19:02): all four hold within ex-post limits; no contradiction found. Three self-report clauses remain unverifiable.

## METHOD
No leg re-run, no MCP started, no file written other than this report. Two `sha256sum` captures + `stat` on SE2's four files; three `ls -la /tmp` sweeps + `stat` on contested names; `ps -p 5401,5402,5403,5416,3014` and a full mcp/rea-filtered `ps -ww -eo`; `git rev-parse HEAD`, `git diff --name-only`, `git diff --cached --name-only`, `git status --short --untracked-files=all`; Read of `luna-round-2/S2.md:9-11`, `receipts/census-pre.txt:1-8`, `EX8.md`. No lane-A leg receipts read.

## FINDINGS
- SE2 verified, extended: current hashes match both captures (`16f496…`, `38d2a1…`, `4af277…`, `7d2ca2…`); mtimes 13:33/13:54/Oct-14 all predate battery start (leg-1 mtime 18:16), so in-window drift is precluded absent deliberate mtime forgery — closing SE2's "first capture after L1" caveat. `S2.md:9-11` hashes match; S2 hashed only three files (no `.bashrc`) ✓.
- SE1 consistent, listing not replayable: `census-pre.txt:1-8` is a Command-A repo baseline, not /tmp ✓. At 19:00:22 none of SE1's residue names existed; at 19:00:38–49 lane-B seats created `kaidoku-luna-round-6[-B]-npm-cache`, `cc3-luna6` (ctime 19:00:38–49) — the naming recurs, so baseline-free attribution is indeed impossible. Leg-7/leg-10 mtimes 18:28 postdate SE1's 18:26:55 check ✓.
- SE3 consistent: all five cited PIDs gone at 19:00 (`ps` exit 1). Current sweep finds live MCP — REA tree 14537/14558/14666 (started 19:00:37) and cli-agents-mcp `server.py` PID 3018 (18:47:58; path exists). `EX8.md:7` matches SE3's client label (ex8, tools/list), supporting the active-probe reading; historical liveness not replayable.
- SE4 verified: HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`; diff/cached empty; untracked 487 at 19:00:22 (waves 483 + sessions 4); waves-only recount 19:01 = 493 across rounds 1–6 (64/91/64/65/130/79) → "not limited to round 6" holds; growth = lane-B concurrency.

## THREATS
Counts drift intra-minute under concurrency (waves 483→493 in ~70s). Self-reports unverifiable: SE1 "none created/removed", SE3 "did not terminate", SE4 "no contents opened". Lane-B seats currently leave /tmp residue and live MCP mid-probe; terminal wave hygiene unproven — consistent with SE1/SE3, not contradictory.

## VERDICT
CLEAN: SE1–SE4 hygiene claims verified to ex-post limits; no contradiction found.
