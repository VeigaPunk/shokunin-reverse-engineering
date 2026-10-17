# RB6 — map/Knowledge rows

## CLAIM
Draft both `corpus/README.md` rows (3-cell map row + 4-cell Knowledge row) for the pending consolidated entry `2026-10-16-l8-01-6p4-symmetry-battery`, keyed to the round-8 6.4.0 battery receipts. Read-only: no tracked file touched.

## METHOD
Read `P0.md:7-21`, receipts 1–10, `leg-2-tools.txt`, `MANIFEST.txt`, `census-pre.txt`; re-ran `sha256sum` over the canonical receipts; byte-extracted `leg-3.md`'s stdout fence vs its claim and the `/tmp` raw; re-ran L9's six `grep -nFw` checks and the 170-line/unique count; placement per round-7 precedent (`git show 3395b6d`). Siblings `RB2/RB4/RB8.md` corroborate. Polled `RB5.md` ~7 min — absent at write time.

## FINDINGS
- Hashes recompute vs `MANIFEST.txt` except `leg-10.md`: `c89eea7a…` recorded vs current `6cd389e9…` (40,401 B, mtime 21:14; appended sections `leg-10.md:28-84`); `RB2.md:9-10` concurs.
- `leg-3.md` stdout fence = 623 B, sha256 `5c682099…a569` = claim (`leg-3.md:6`) = `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`; the known display defect does not reproduce at current bytes; `census-pre.txt:97` leg-3/leg-4 lines are pre-final snapshots (`RB4.md:9`).
- Pinned: L1 `leg-1.md:7,10`; L2 `leg-2.md:9` (170/170 unique); L3–L8 refusals `leg-3.md:22`, `leg-4.md:13`, `leg-5.md:9`, `leg-6.md:11`, `leg-7.md:13`, `leg-8.md:10`; my six `grep -Fw` rc=1; L10 RESULT `leg-10.md:15,24`.
- Drafts insert after `corpus/README.md:67` and `:151` (single-line appends; 78→79 arithmetic: `RB8.md:4,23`):

```markdown
| `knowledge/2026-10-16-l8-01-6p4-symmetry-battery` | Kimi-resolved REA 6.4.0 symmetry battery at HEAD `6e2ee8f`: 10/10 frozen predictions matched — `--version` stdout exactly `6.4.0`; MCP `tools/list` exactly 170; six 6.5-only verbs each TYPED-REFUSAL (`-32602 Tool <name> not found`); all six names absent (L9 exact); control `inspect_binary_layout` returned RESULT on `/usr/bin/jq`; strict zero config drift unproven | REA 6.4.0 live stdio MCP probes; `.ufo/waves/luna-round-8/receipts/leg-1.md`–`leg-10.md` + `leg-2-tools.txt` + `MANIFEST.txt` |
| `2026-10-16-l8-01-6p4-symmetry-battery` | REA 6.4.0 operability symmetry battery, 10/10: version exact, 170 tools, six 6.5-only verbs typed-refused, six absences, jq control RESULT; zero config drift unproven | rea-agents@6.4.0 live MCP; `.ufo/waves/luna-round-8/receipts/leg-1.md:7,10`; `leg-2.md:9`; `leg-3.md:22`; `leg-4.md:13`; `leg-5.md:9`; `leg-6.md:11`; `leg-7.md:13`; `leg-8.md:10`; `leg-9.md:9-14`; `leg-10.md:15,24`; `MANIFEST.txt:1-9` | 2026-10-16 |
```

## THREATS
- `RB5.md` never landed; rows key to frozen facts, not RB5 prose — reconcile wording parent-side.
- No round-8 pre/post config pair → zero drift unprovable (`CA6.md` THREATS); rows mark it unproven.
- `MANIFEST.txt:10` is stale; re-measure `leg-10.md` at landing if the entry cites it.
- L4–L9 raw witnesses gone; display hashes self-referential (`RB2.md:14`).

## VERDICT
CLEAN — both rows drafted and verified against recomputed evidence; provisional pending RB5's entry text.
