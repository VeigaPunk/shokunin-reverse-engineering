# CC9 — compare leg 9 (identify_flutter_build on /usr/bin/jq)

## CLAIM
Leg 9 agrees across lanes: lane B (BB9 receipt + my independent re-run) and lane A both observe the frozen TYPED-REFUSAL; A↔CC9 wire captures are byte-identical (target frame sha `2b596b31…be41`, raw stdout sha `1ff84c06…6909`, each equal to lane A's recorded digest).

## METHOD
Compared lane A `.ufo/waves/luna-round-6/receipts/leg-9.md` + `EX9.md` against lane B `receipts-B/leg-9.md` (BB9) + `BB9.md`. Independent re-run from `/tmp/rea-cc9`: `python3 harness9.py` (sha `cb6b2d50…3ee5`) spawning `npx -y rea-agents@6.5.0 mcp` (cwd `/tmp/rea-cc9`, 240 s deadline): `initialize` (2025-03-26) → `notifications/initialized` → `tools/call` `identify_flutter_build {"path":"/usr/bin/jq"}`; stdin closed, exit awaited; raw stdout/stderr byte-captured; sha256 + xxd. Programmatic compare: extracted fenced frames from both receipts, parsed payloads, recomputed hashes. No config edits (`git status` = pre-existing untracked `.ufo/` only); jq identity `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` matches lane A's record.

## FINDINGS
- Class: all runs TYPED-REFUSAL — `isError:true`, `invalid_request`/`invalid_input`/`invalid_format`, operation `identify_flutter_build`, identical text "ZIP archive is malformed: End of central directory not found"; exit 0; graceful stdin-EOF shutdown; no residual `rea-agents`. Frozen L9 → MATCH.
- Bytes: my target frame (659 B) hash equals lane A's recorded hash, and lane A's quoted frame is byte-identical to my capture; my raw stdout (1696 B = init 1037 + target 659) hash equals lane A's recorded raw digest — independently recomputing the digest `XA.md:8` called unverifiable.
- BB9's receipt hash `2a20c456…e747bd` recomputes exactly over its 772-byte pretty-printed transcript, not raw wire bytes (659 B, compact); A/B receipt hashes are not directly comparable, though parsed payloads are equal.
- Collision: BB9 and CC9 both wrote `receipts-B/leg-9.md`; BB9's later write (mtime 19:02:06) replaced mine. I left BB9's receipt in place; my capture is `/tmp/rea-cc9/{stdout.raw,frame-target.bin,stderr.bin,harness9.py}`.
- Stale pointer: `EX9.md:11` cites the failed batch attempt at `receipts/leg-9.md:21-35`, but that receipt is 13 lines; the cited section is absent.

## THREATS
My re-run was protocol-informed (lane A receipt read before running, as the assigned method source). Warm npx cache (init 0.64 s) — cached artifact, not cold fetch; shared host/toolchain common-mode risk. Command A/map-token set and other legs not audited here; nothing promoted to held.

## VERDICT
CLEAN — leg 9 class agrees A/B/CC9; A↔CC9 bytes identical; BB9's receipt preserved, collision noted.
