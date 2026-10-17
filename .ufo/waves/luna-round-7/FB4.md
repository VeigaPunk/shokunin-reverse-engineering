## CLAIM
Fields audit across all six round-7 entry drafts: only l7-06 carries the contract metadata fields (`source:`, `verified-at:`, `recheck:`); the other five carry neither the literal fields nor a house-equivalent bullet field, so as drafted they are not admission-ready per G3's catch (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17-19`) and C4's proposed gate (`C4.md:8`).

## METHOD
Read-only field scan with `grep -nE '^[[:space:]]*(>|-)?[[:space:]]*\**?(source|verified-at|recheck)\**?[[:space:]]*:'` over the ten candidate bodies: `E1D E2D G1 G2 E3D E4D G4 E5D G5 E6D`. House survey: same field-name regexes over all 72 `corpus/knowledge/*.md`. `git show HEAD:…` line-count check on E6D's cited receipt ranges. No probes, MCP, or network.

## FINDINGS
- **l7-06 (PASS):** `E6D.md:12-14` carries all three fields; its values resolve — `receipts/leg-8.md` (25 lines) and `receipts-B/leg-8.md` (78 lines) exist in HEAD 411175e and contain the cited ranges `:3-14` and `:41-55,67-76`; `verified-at: 2026-10-16` matches the round date.
- **l7-01…l7-05 (FAIL):** zero field-form lines in any candidate body — `E1D.md:12-27`, `E2D.md:10-17`, `E3D.md:8`, `E4D.md:8-12`, `E5D.md:2-11`, plus lane-A bodies `G1.md:9-16`, `G2.md:10-25`, `G4.md:10-23`, `G5.md:8-16`. Only trailing inline `Sources:` prose exists (`E1D.md:26`, `G2.md:24`, `G4.md:22`); E3D and E5D have neither fields nor a Sources line.
- **House equivalents:** 64/72 entries carry `- source:` bullets and 70/72 carry `- verified-at:` (e.g. `corpus/knowledge/2026-10-14-r14-01-queue-b-residual.md:43,49`), but 0/72 carry a `recheck:` field — nearest are inline prose (`corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:129`) and a table cell (`corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:320`). No house precedent substitutes for `recheck:`.
- Each of the five has material to fill the fields: resolvable receipt/scout paths at `E1D.md:26`, `G2.md:24`, `G4.md:22`, `E3D.md:8`, `E5D.md:2-8`; carrier path + 64-hex SHA-256 and Evidence IDs are inline.

## THREATS
Audit covers drafts only; the parent may add the fields at landing, which this seat cannot verify. Cited ranges were read read-only from Git objects, not re-executed. Row-level `verified-at` date cells in M1/M2/K3/K4 were not re-audited (`F7.md:8` covers them). Lane A's `F8.md:10` independently reports the same five-of-six gap — corroboration, not independent evidence.

## VERDICT
FINDING: 5/6 entry bodies (l7-01…l7-05) lack `source:`/`verified-at:`/`recheck:` as drafted; prepend the E6D-style field block (or fail C4's per-blob content gate) before landing.
