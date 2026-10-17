## CLAIM
Registry/cache/space failures are normally per-leg outcome mismatches; failure to contain a hung MCP server or preserve the required complete evidence blocks safe completion of the round.

## METHOD
Read-only review of the round-2 npx inventory (`.ufo/waves/luna-round-2/receipts/L4-npx-cache.txt:1-24`), MCP runner precedent (`.ufo/waves/luna-round-2/receipts/L15-tools-6.5.0.txt:1-9`), and current L1 receipt (`.ufo/waves/luna-round-6/receipts/leg-1.md:3-11`). I did not test registry reachability, disk quota, current cache state, or processes.

## FINDINGS
- **Registry down / cache eviction — per-leg failure, not automatic stop.** L4 records 6.5.0 in `/home/vgpnk/.npm/_npx/...`; current L1 ran from `/tmp` and returned `6.5.0`, exit 0. Neither historical inventory nor L1 guarantees every later invocation resolves. If a pinned call cannot launch within its 240s limit, receipt it as `ERROR-UNEXPECTED` (the all-10-execute clause is then false) and continue other legs only if pinned 6.5.0 remains available. Do not substitute or manually install.
- **`/tmp` quota — per-leg if one carrier cannot be staged; round blocker if inputs/outputs cannot be captured and hashed for all required legs.** `/tmp` is the working directory, not proven storage isolation: the recorded npx cache is under `$HOME/.npm/_npx` (L4:3-12). Do not label an unexecuted carrier a typed refusal.
- **MCP hang — missing result by 240s is a per-leg mismatch.** Terminate the process group; L15:2 records SIGTERM and, on timeout, SIGKILL after 5s. If termination/reaping cannot be confirmed, stop the round before another MCP leg: a leaked server breaks containment. A server waiting for another request after returning a complete result is not itself proof of a hang; explicitly shut it down.
- **Honest stop:** stop only for shared inability to complete pinned legs with durable hashed receipts, failed MCP cleanup, or observed host/config drift. Record isolated failures and continue safely; no retries that replace the preregistered result.

## THREATS
The 240s bound is per leg; no overall deadline is specified. Current network/cache/quota, process teardown, and host/config deltas remain unverified. Required receipt files are outside `/tmp`; npx may also use its home cache, so `cwd=/tmp` alone cannot establish zero outside-`/tmp` mutation.

## VERDICT
FINDING: The literal zero-mutation claim needs an explicit carve-out or measurement boundary for required receipts and npx cache writes.
