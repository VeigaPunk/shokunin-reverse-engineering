## CLAIM
Re-ran leg 4 independently (lane B): `inspect_rust_binary` on SC2's carrier `/usr/bin/rg` returned a valid typed Evidence record (outcome class RESULT), matching the frozen L4 prediction. Hashed receipt: `.ufo/waves/luna-round-6/receipts-B/leg-4.md`.

## METHOD
Read the battery spec from lane-A seat report `P0.md` (protocol/method only); did not read lane-A receipts (no expected-output peeking). Carrier definition from `SC2.md:2,8-10`. Read-only preflight of the input (`file`, `sha256sum`, `stat`; `rg --version`). Wrote a minimal Python MCP stdio harness `/tmp/rea-bb4/mcp_leg4.py` (sha256 `9b40bde4…`) that spawns `npx -y rea-agents@6.5.0 --mcp` (cwd `/tmp`, own session), does `initialize` → `notifications/initialized` → one `tools/call` `inspect_rust_binary {"path":"/usr/bin/rg"}`, captures raw server stdout/stderr, closes stdin to terminate, then scans `/proc` for survivors. Exact command: `cd /tmp && timeout 285 python3 /tmp/rea-bb4/mcp_leg4.py > /tmp/rea-bb4/harness-stdout.raw 2> /tmp/rea-bb4/harness-stderr.raw` (exit 0). No config edits; writes limited to `/tmp/rea-bb4/`, the receipt, and this report.

## FINDINGS
- Input identity `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`, 4,377,936 bytes, ELF 64-bit LSB pie x86-64 stripped — exact match to SC2's carrier hash.
- Handshake: protocolVersion `2024-11-05`; serverInfo `rea` 6.5.0. Response id=2: `operation=inspect_rust_binary`, `evidence_id=ev_9ea97685…`, provider `rust-auditable` v1, `confidence=observed`, `authority=shipped-artifact`; artifact sha256 equals the input hash; format elf, amd64, 64-bit LE.
- `auditable_metadata: null` — "No `.dep-v0` section was found" (Arch ripgrep 15.2.0 is not cargo-auditable). Explicit limitation returned; still typed output, so class RESULT, not TYPED-REFUSAL.
- Termination: exit 0 on stdin close; in-harness and external scans found no surviving `--mcp` process.
- Receipt sha256 `162b4831ebbd719734407454cce53147525158026340cadf73435c22059afbcb`; embedded stdout block byte-exact (7,879 bytes, sha256 `84d489f7…`).

## THREATS
Result is static parsing of embedded metadata only; null metadata does not prove absence of dependencies (tool states this). npx wrote debug logs under `~/.npm/_logs` (npx side effect outside `/tmp`; no REA/agent config touched). Concurrent sibling seats' npx/MCP probes ran during my window; my scans and receipts cover only my own session. Single run — no repeat-run variance evidence.

## VERDICT
CLEAN
