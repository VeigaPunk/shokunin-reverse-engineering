# BB2 — leg 2 re-run (L2 tools/list, REA 6.5.0)

## CLAIM
L2 re-run: JSON-RPC `tools/list` against REA 6.5.0 over MCP stdio returns the frozen outcome class RESULT with count 207, and this lane reproduces lane A's recorded stdout byte-for-byte (cross-lane agreement).

## METHOD
- Read lane A `receipts/leg-2.md` header only for protocol (command + three stdio frames); probe executed independently.
- Driver `/tmp/rea-bb2/driver.js`: spawns `npx -y rea-agents@6.5.0 mcp` (cwd `/tmp/rea-bb2`, `npm_config_cache=/tmp/kaidoku-luna-round-6B-npm-cache`, `TMPDIR=/tmp`; node v26.12.0, npx 11.20.0); sends `initialize` → `notifications/initialized` → `tools/list` as newline-delimited JSON frames; captures raw stdout/stderr to files; closes stdin (EOF) to terminate; 235 s cap.
- Pre-probe cache warm (`--version`, exit 0, printed 6.5.0) so the measured run does not spend budget on download.
- Receipt `.ufo/waves/luna-round-6/receipts-B/leg-2.md`: command, frames, count summary, full stdout, stderr, exit, sha256; embedded stdout re-hashed after write and matches the capture.

## FINDINGS
- id1 result: protocolVersion 2025-03-26, serverInfo `{"name":"rea","version":"6.5.0"}`.
- id2 result: count 207, 207 unique names, `nextCursor` key absent; first5 `[annotate_native_function, inspect_native_load_image, inspect_native_data_type, inspect_native_instruction, resolve_native_call_targets]`.
- stdout 3,089,024 B, sha256 `38d44bf8ee0944315a1d50d3e3acec1401be50efe7090ac22ec8498e853d4129` — identical to lane A's recorded hash. stderr 0 B.
- Termination: stdin closed at t+1690 ms, server exited cleanly t+1708 ms, exit 0, signal null; no SIGTERM/SIGKILL. No lingering processes.
- Predicted class RESULT hit; count equals frozen 207.

## THREATS
- Not blind: lane A's header read exposed their summary line (count 207, hash). Capture was independent and machine-generated, but blindness is lost; treat this as corroboration, not a blind replicate.
- Cache pre-warm differs from a cold run: my stderr is empty vs lane A's npm download notices. Affects stderr bytes only; stdout hash still matches.
- Single run — no repeat, so flakiness untested. Count derived by parsing my own capture; embedding verified by re-hash.
- Lane A's node/npx versions unknown; byte-identical stdout hash covers that gap.

## VERDICT
CLEAN
