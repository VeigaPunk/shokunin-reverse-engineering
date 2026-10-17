## CLAIM
K3/K4's six proposed Knowledge-table topics are checked clause-by-clause against the round-6 legs 3–8 receipts: five of six are evidence-faithful; row 4 is not landable under parent ruling (b), and all six entry tokens use the underscore stems ruling (a) forbids.

## METHOD
Read `K3.md`, `K4.md`, both lanes' legs 3–8 receipts, SC1–SC6, `corpus/README.md`, `corpus/QUALITY.md`, SCORECARD recipe A, and lane-A drafts (E1D/E2D/E4D, G1–G6, M2, Z1–Z6). No probes, MCP, or network; tracked files untouched; this report is the only write.

## FINDINGS
Faithful, each clause traced:
- `inspect_go_binary` (K3.md:8): `complete:true`, empty `unparsed_lines`, limitation "not proof of compiler identity … runtime behavior" (`receipts-B/leg-3.md:42`; decoded response `receipts/leg-3.md:52-96`).
- `inspect_rust_binary` (K3.md:9): "No .dep-v0 section was found … does not mean the binary has no dependencies"; "No /rustc/<40-hex>/ path … commit hash is unknown" (`receipts-B/leg-4.md:47`; `receipts/leg-4.md:28`). Caveat: one clause merges both carriers and omits lane A's inferred (not observed) rustc hash — keep artifacts separate per ruling (c) (`Z2.md:8`).
- `inspect_electron_fuses` (K3.md:10): nine fuses `complete:true`; `embedded_asar_integrity_validation` outcome `unknown`; "does not establish enforcement" (`receipts/leg-5.md:8`; `receipts-B/leg-5.md:28`).
- `search_bytes` (K4.md:11): "loader-adjusted memory independently per block" limitation; match `0x100000`, `file_offset:0`; lane-B stdout byte-identical (`receipts/leg-7.md:13,21`; `receipts-B/leg-7.md:58,67`).
- `inspect_with_objdump` (K4.md:12): `completion_status:"complete"`, `output_truncated:false`; "executable version … reported as unknown" (`receipts/leg-8.md:12,19`).

Not faithful — `K4.md:10` (row 4): topic "inventory or selected-table schema/sample" and its A+B receipt citation still rest on lane A's self-made fixture (`receipts/leg-6.md:8,10-12`; `corpus/QUALITY.md:22`), which ruling (b) excludes. Use lane B only: path-only inventory, one `package_index` table, columns not requested, `rows:null` (`receipts-B/leg-6.md:20,35`; host source `SC4.md:8`).

Naming: all six entry tokens are underscore stems (K3.md:8-10; K4.md:10-12) against ruling (a); `E1D.md:8`, `E2D.md:2`, `E4D.md:11-12`, `M2.md:10-12` already hyphenate. K4.md:14's regex-widening is superseded: command A scans only Coverage-map tokens with `2026-10-\d{2}-[a-z0-9-]+` (`SCORECARD.md:101-102`), and table tokens must match the landed hyphenated file stems.

## THREATS
Entry metadata fields (ruling d), the 78/78 count, and prior-entry byte identity are parent-integration checks, not verified here. Row 6 names no carrier although lane B's primary run used a different `jq` (`receipts-B/leg-8.md:7-8`); keep it carrier-pinned.

## VERDICT
FINDING: five of six topics are evidence-faithful; rewrite row 4 to lane-B-only per ruling (b) and hyphenate all six stems per ruling (a) before landing.
