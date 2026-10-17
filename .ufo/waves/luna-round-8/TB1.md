# TB1 — command-A guard 2 (lane B)

## CLAIM
Post-battery Command A (SCORECARD.md:92-123) at frozen HEAD `6e2ee8f` reproduces the frozen pre-dispatch census byte-for-byte: 78/78 mapped, 9/9 rules, coverage/depth 10.0, empty missing/dangling, token-set SHA-256 `c6c025f3…`; no tracked or recorded-config drift.

## METHOD
Read the frozen pre-dispatch record `receipts/census-pre.txt:84-100` and `P0.md:15,21`. `git rev-parse HEAD` → `6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4`. Ran Recipe A verbatim at `REV=HEAD` twice (stdout `/tmp/tb1-r8/run{1,2}.out`; exit 0, stderr 0 bytes each); diffed my executed script against the `HEAD:SCORECARD.md` recipe fence (only difference: trailing newline, no execution effect). Re-ran census-pre's token/aggregate/config computation at the same revision. Guards: `git diff --quiet HEAD` → exit 0; `git status --porcelain=v1` tracked lines 0. Read-only throughout; no probe, no MCP.

## FINDINGS
- Runs 1 and 2 identical; stdout SHA-256 `5885833a6b1429cc983d544216c80383a4f11896dbd309eea6a287a21b2c51de`. Stdout equals the census-pre `COMMAND_A_STDOUT` line exactly: 78/78, 9/9, 10.0/10.0, `[]`/`[]`, revision full SHA.
- MAP_TOKEN_COUNT=78, MAP_TOKEN_SHA256 `c6c025f3aee5fb93966f9da4eca22ade1ac3af9207d9ad26b8bca6807f6ae83b` — equals `census-pre.txt:92-93`; KNOWLEDGE_MD_COUNT=78, aggregate `00891de8600a2bf8eba44c5ecc4d32eba3d58bf2e7222124ea643fa447640076` — equals `:94-95`. Tokens equal the 78 file stems (missing/dangling empty).
- Post configs equal `:98-100` exactly: devin `16f496e6…`, omp `38d2a1d0…`, kimi `4af27747…` (full SHA-256s recomputed; zero drift at these three paths).
- Tracked state at `2026-10-16T21:18-03:00`: tracked porcelain lines 0, worktree diff clean, nothing staged, HEAD and log top still `6e2ee8f`.
- The pending consolidation entry (`…l8-01-6p4-symmetry-battery…`) is not in HEAD knowledge; at this HEAD the denominator remains 78.

## THREATS
Snapshot timestamp is the only guarantee; later writes are invisible. Recipe A reads Git objects, not the worktree — untracked wave artifacts are unguarded by design. Config equality covers only the three recorded paths. Receipt-hash verification is owned by CA6/CE2, not re-run here. Guard held to scope: no probes executed.

## VERDICT
CLEAN — Command A at `6e2ee8f` reproduces the frozen census exactly (78/78, 9/9, 10.0/10.0, token `c6c025f3…`) with no tracked-state or recorded-config drift.
