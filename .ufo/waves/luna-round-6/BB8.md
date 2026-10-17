# BB8 — leg 8 independent re-run (lane B)

## CLAIM
Lane-B re-run of leg 8 (`inspect_with_objdump` on /usr/bin/jq, REA 6.5.0) reproduces lane A byte-for-byte: identical stdout sha256, both RESULT class. Frozen L8 prediction matches; cross-lane agreement confirmed.

## METHOD
Command A `cd /tmp && npx -y rea-agents@6.5.0 --mcp` (240s deadline). Independent Python stdio harness (`/tmp/rea-bb8/harness.py`): initialize (protocol `2025-03-26`) → notifications/initialized → tools/call `inspect_with_objdump` `{path:/usr/bin/jq, operation:file_headers, follow_debug_links:false}`; stdin closed, normal exit; raw stdout/stderr/exit captured to files. Target preflight `file` + `sha256sum`. Lane-A receipt read only after my run, hash, and receipt were recorded. No config edits; MCP terminated, no orphan. Receipt: `receipts-B/leg-8.md`.

## FINDINGS
- Exit 0; wall 0.72s (npx cache hit); stderr = one pino log line; stdout = 2 JSON-RPC frames, 5,301 bytes, sha256 `e0b2d5058e2a28ed41857cc3672d9b7e3354072bc474a8eb349c7065333c232b`.
- RESULT class: typed Evidence, operation `inspect_with_objdump`, provider `gnu.objdump`, argv `["-f","/usr/bin/jq"]`; objdump stdout `file format elf64-x86-64`, `architecture: i386:x86-64, flags 0x00000150`, `HAS_SYMS, DYNAMIC, D_PAGED`, raw exit 0; subject/post digest `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` = preflight; artifact_changed=false.
- Byte-identical to lane A: same stdout sha256 recorded at `receipts/leg-8.md:13`, same evidence_id `ev_aa75cc2e…` — evidence_id is content-deterministic, not session-random.
- stdout invariant across lanes despite differing clientInfo name (RV3 vs bb8) and their `params:{}` on the initialized notification — framing metadata does not leak into hashed output.
- Receipt re-verified: embedded stdout/stderr blocks byte-exact; `git status` shows no tracked modifications (only untracked `.ufo/`).

## THREATS
- Independence is process-level only: same host, node v26.12.0, warm npx cache (0.72s run); cold fetch not exercised.
- stderr pino `time`/`durationMs` differ cross-lane — nondeterminism exists outside the hashed stdout stream.
- One re-run, one input; other targets and objdump operations (e.g. disassembly) uncovered. Config-drift and Command A/token audits are out of this seat's scope; host-wide write audit not performed.

## VERDICT
CLEAN — leg 8 byte-identical cross-lane, RESULT class matched, receipt filed.
