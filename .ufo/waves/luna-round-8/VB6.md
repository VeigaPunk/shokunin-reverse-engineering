## CLAIM
Ten seats (PS1, PS2, PS3, RE2, RV6, RV8, RV1, CA7, XG1, RE6) read receipts before they landed and recorded absent/unscored verdicts. Each is superseded by the late evidence: all 10 canonical receipts present, CA6 census 10/10.

## METHOD
Read-only re-verification at HEAD 6e2ee8f. Recomputed receipt SHA-256s against `receipts/MANIFEST.txt` and `CA6.md:10`; counted `leg-2-tools.txt`; per-name L9 greps; read refusal payloads and version pins; swept receipts for `6.5`; searched `leg-10.md` byte-prefixes for the older hash boundary. No probes.

## FINDINGS

| Seat | Stale verdict | Superseding evidence | Scope |
|---|---|---|---|
| PS1 | `PS1.md:20` L1–L5 unscored, no receipts | leg-1..5.md present; `leg-3.md:22` `-32602` unknown-tool; tools list 170 lines | 5/5 |
| PS2 | `PS2.md:14` L6–L10 unscorable | leg-6..10.md present; refusals leg-6/7/8.md (`:11,:13,:10`); `leg-9.md:9-23`; `leg-10.md` control RESULT | 5/5 |
| PS3 | `PS3.md:27` final N/10 unestablished | all ten legs + tools list present; `CA6.md:8` | 10/10 |
| RE2 | `RE2.md:22` 1/10 confirmed | same as PS3 | 10/10 |
| RV6 | `RV6.md:14` pins unverifiable | 9 receipts pin `rea-agents@6.4.0` (`leg-1.md:3`…`leg-8.md:3`, `leg-10.md:3`) | resolved |
| RV8 | `RV8.md:14` leg-10 missing | `leg-10.md` 40401 B; five fields at `:3,:11,:17,:21,:22` | 10/10 |
| RV1 | `RV1.md:22` no preexisting L2 receipt | leg-2.md + leg-2-tools.txt landed (170 names); receipt is RV1's own capture | L2 match |
| CA7 | `CA7.md:14` leakage check unverifiable | `grep -E "6\.5"` over 10 legs + tools list: 0 matches | clean, full set |
| XG1 | `XG1.md:21` six classes unverifiable | raw `-32602` unknown-tool in leg-3/4/5; quoted at 6.4.0 in leg-6/7/8 | 6/6 schema-level |
| RE6 | `RE6.md:25` L9 unverified | `leg-9.md:18-23` six ABSENT, exit 1, stdout hash `e3b0c442…`; leg-2-tools.txt counts 0/6 | 6/6 absent |

Hash recompute: 9/10 equal MANIFEST. `leg-10.md` is `6cd389e9…`, not claimed `c89eea7a…` — but its first 27655 bytes still hash to `c89eea7a`, so EX10's fallback section (`:61-84`, mtime 21:14, post-census) was appended: extension, not corruption. Its internal stdout hash `23e94d0b…` (`:26`) recomputes against `/tmp/kaidoku-luna-round-8-leg10.stdout`. `leg-3.md`'s displayed stdout block verifies (`5c682099…`, LF-terminated) at current 1448 B.

## THREATS
`MANIFEST.txt:10`/`CA6.md:10` leg-10 hash citations are stale for current bytes. RV1's L2 receipt is self-authored. `leg-9.md` has no 6.4.0 pin (derived check). No pre-L1 snapshot exists, so prior absence is superseded, not re-auditable.

## VERDICT
FINDING: all ten stale verdicts superseded (all receipts present, CA6 10/10); leg-10.md whole-file hash citations need updating for the post-census append.
