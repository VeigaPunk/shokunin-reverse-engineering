## CLAIM
Lane-A integrity audit of the wave receipts and reports at HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`.

## METHOD
Read all 53 top-level seat reports, ten `receipts/leg-*.md`, `MANIFEST.txt`, and `census-pre.txt`. Read-only Python recomputation checked recorded stdout digests and required report headings; `git rev-parse HEAD` returned `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`. No probes, MCP servers, or config edits.

## FINDINGS
- Recomputed stdout hashes match the captured bytes for L1–L8 and L10; L3 matches after excluding the extra code-fence separator LF. L9’s target-response hash matches, but its separate raw-process hash cannot be recomputed: the receipt omits the initialize response bytes (`leg-9.md:2-12`). No mismatch among recheckable hashes.
- `MANIFEST.txt:1` lists only `leg-1.md` with `24bfd90f…e2e91`; recomputing that receipt-file hash matches. Legs 2–10 are absent, so the manifest does not list exactly ten legs.
- All 53 seat reports contain all five required headings (read-only heading scan: 53 reports, no missing-heading output).
- `census-pre.txt:3,40,45` records the full requested HEAD and `EXIT_CODE 0`; local `git rev-parse HEAD` agrees.
- Contradictory findings to reconcile: RV2’s L10 Harmony-refusal route vs EX10’s Wasm inspection route (`RV2.md:6,10`; `EX10.md:2,5-8`; `receipts/leg-10.md:9,16-17`); EX6’s L6 attribution vs RV3’s generated-database receipt overwrite (`EX6.md:3,7,15-19`; `RV3.md:2,8,13-16`; `receipts/leg-6.md:10-14`); EX8’s L6 digest-mismatch finding vs the current receipt’s matching recomputation (`EX8.md:10`; `receipts/leg-6.md:13,16-20`). RV2’s separate L4 replay used `/usr/bin/rg`, whereas the canonical L4 receipt records Signal’s `.node` carrier (`RV2.md:9`; `receipts/leg-4.md:12-21`).

## THREATS
Receipt-path overwrites and reports taken at different snapshots explain some divergences but do not establish their exact chronology. The census transcript records its revision but has no independent timestamp/signature; L9’s raw-process digest remains unverifiable.

## VERDICT
FINDING: the manifest is incomplete; L9’s raw-process digest is unverifiable, while all other recheckable stdout hashes, report headings, and recorded census HEAD pass.
