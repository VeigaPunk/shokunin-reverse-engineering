## CLAIM
Battery leg 5 re-run in lane B (seat BB5): `inspect_electron_fuses` on SC3's carrier `/usr/lib/signal-desktop/signal-desktop` (Electron ELF). Frozen class RESULT. Receipt: `.ufo/waves/luna-round-6/receipts-B/leg-5.md` (sha256 `57ac012475aac4ba845185df0ab0e1cb1121ac32646f2ee93a513b2a28922f40`); measurement stdout sha256 `14ef0f1cff6db42dc52c1b126e0dce14078f85952dfbd29c875269d70f8211b3`.

## METHOD
- Input parity: lane-A `receipts/leg-5.md` read with `grep -o -E '/usr/[A-Za-z0-9._/-]+'` only — a single path surfaced; no output sections read. Carrier re-hashed pre-run (`sha256sum` = `f7a9b441…` = SC3.md:10).
- `npx -y rea-agents@6.5.0 --mcp` from `/tmp` via NDJSON MCP driver (`/tmp/rea-bb5/mcp_drive.py`, 240s deadline); prep `tools/list` for the tool's input schema; then `tools/call` with `{"path": ...}`.
- Captured full stdout/stderr/exit + raw-byte sha256; teardown verified by an instrumented connect-and-close probe (process group empty after stdin close).

## FINDINGS
- Observed **RESULT**, class **MATCH**: JSON-RPC `result`, no `error`, `isError` absent; typed dossier (`rea.analysis`, confidence `observed`, authority `shipped-artifact`), 9 fuse states, sentinel offset 35260752, subject sha256 = input sha256.
- stdout 9,085 B `14ef0f1c…`; response line 8,048 B `83f9d564…`; stderr one log line `status:"ok"` durationMs 148.94; driver/server exit 0; wall 1.86s.
- Fuse fingerprint for lane-A comparison: RunAsNode disabled / EnableCookieEncryption enabled / EnableNodeOptionsEnvironmentVariable disabled / EnableNodeCliInspectArguments disabled / EnableEmbeddedAsarIntegrityValidation disabled / OnlyLoadAppFromAsar enabled / LoadBrowserProcessSpecificV8Snapshot disabled / GrantFileProtocolExtraPrivileges enabled / WasmTrapHandlers enabled.
- Incidental: prep `tools/list` returned 207 tools; not a leg-2 measurement.

## THREATS
- Concurrent seats ran npx/MCP probes in my window (a process poller, and `npm exec rea-agents@6.5.0 mcp`), so one transient `--mcp` PID sighting (~19:01:4x) is not confidently attributable to my sessions; none remained in 19:02:28+ samples.
- Disclosure: my cleanup-checker v1 crashed pre-teardown and orphaned pgid 55068; killed manually (`kill -TERM -- -55068`) and verified gone; the leg-5 sessions themselves exited 0 via stdin close.
- Command A/token-set controls are other seats' scope (not run here); no config edits; tracked files untouched (`git status` unchanged).

## VERDICT
CLEAN — leg 5 re-run landed RESULT/MATCH with hashed receipt B.
