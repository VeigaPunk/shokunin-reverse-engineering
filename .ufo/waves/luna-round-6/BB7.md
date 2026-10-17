# BB7 — leg 7 re-run (search_bytes ELF magic on SC5's small ELF)

## CLAIM
Leg 7 re-run (BB7): REA 6.5.0 `search_bytes` with ELF magic `7f 45 4c 46` on SC5's small ELF (`/bin/true` -> `/usr/bin/true`) yields outcome class RESULT — frozen prediction MATCHed, with stdout byte-identical to lane A.

## METHOD
- Command/pattern from lane A `receipts/leg-7.md` (command reading, per assignment): `npx -y rea-agents@6.5.0 --mcp` spawned from `/tmp/rea-bb7`; wire traffic: initialize -> `open_binary` `/bin/true` -> `search_bytes {"pattern":"7f 45 4c 46"}`; 240s MCP deadline (observed id-3 response at t+6.0s).
- Independent client identity `luna-round-6-BB7-L7-rerun`; raw stdout/stderr captured to `/tmp/rea-bb7/stdout.raw` / `stderr.raw`; sha256 via `sha256sum`; stdin closed after id-3 response, exit 0; `ps` confirms no lingering server.
- Own receipt: `.ufo/waves/luna-round-6/receipts-B/leg-7.md` — full stdout/stderr verbatim, mechanically assembled from raw captures; embedded stdout re-hashes to the reported sha256.

## FINDINGS
- id1 serverInfo `rea` version 6.5.0; id2 `open_binary` -> `/usr/bin/true`, elf/executable/x86_64, sha256 `8bc9a73a…` (matches SC5.md:9); id3 `search_bytes` -> matches `[{address 0x100000, segment segment_2.1, file_offset 0}]`, complete=true, evidence_id `ev_4b0badc6…`, confidence `observed`, authority `shipped-artifact`.
- Stdout sha256 `3492d27d66e086d683935f396ea05fce4cbddc660874052a955c9133866629a8`, 19,151 bytes — exactly lane A's reported stdout sha256 (`receipts/leg-7.md:14`). Byte-level cross-lane agreement, evidence_id included.
- Stderr: two `status:ok` bunyan lines (`open_binary` 20.5ms; `search_bytes` 5131.59ms); differs from lane A only in timestamps/durations, as expected.
- Outcome class RESULT; prediction RESULT -> MATCH.

## THREATS
- The assignment directed me to lane A's full leg-7 receipt for the command, so expected output was known before my run. Mitigation: fresh independent process; hashes computed mechanically from captured bytes; equality with lane A verified by `sha256sum`, not judgment.
- Client identity string differed between lanes; stdout still byte-identical, so clientInfo is not echoed in responses.
- Single host, single REA install, one replay: determinism observed once; stderr is timing-dependent and not hash-comparable.
- No config edited; HEAD f0e8cde; only untracked `.ufo/waves/` written (git status shows no tracked-file changes).

## VERDICT
CLEAN
