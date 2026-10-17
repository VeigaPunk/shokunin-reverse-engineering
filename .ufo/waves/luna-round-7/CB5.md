## CLAIM
Hunted every round-7 recommended text for cross-carrier merge claims on entries 2 and 4, whose lane carriers differ (parent rulings (b)/(c)). No false same-target or hash-conflation claim exists anywhere, but six texts carry joint-carrier claims, and P2's record draft rebases both entries on the wrong lane's carrier.

## METHOD
Read all 22 recommended texts (`E1D`–`E6D`, `G1`–`G6`, `Z1`–`Z6`, `M1`/`M2`, `K3`/`K4`) plus `E2V`/`E4V`, `P2`, `F4`, `Q2`, `Q4`; checked carriers against `.ufo/waves/luna-round-6/` receipts leg-4/leg-6 both lanes, `SC2`, `SC4`, and the pinned hash strings. Read-only; no probes, no tracked-file writes.

## FINDINGS
Entry 2 (`/usr/bin/rg` lane B; Signal `.node` lane A):
- `E2D.md:12-13` — the proposed entry body asserts a joint observation over both artifacts ("Both outputs report…"); lane A's fallback/unverified-assignment caveat stays outside the entry (only in `E2D.md:20`). Breaches ruling (c).
- `K3.md:9` — one Knowledge row: "no `.dep-v0` found in libsignal `.node` or `rg`", both receipts cited: merged basis in the cell.
- `M1.md:12` — one row, both carriers, but separate hashes and a "lane-A fallback" label retained: borderline, no identity merge.

Entry 4 (pnpm-index copy lane B; synthetic `/tmp` fixture lane A):
- `E4D.md:8,11-12` — entry substance and both proposed rows merge A's selected-table/sample with B's inventory ("inventory versus selected-table schema/sample"; both receipts cited). Violates ruling (b).
- `M2.md:10,15,19` — "Selected-table sample vs inventory-only"; "L6 receipts A/B"; entry-4 facts run A's call then B's carrier with no A-exclusion.
- `K4.md:10` — row "inventory or selected-table schema/sample" citing `receipts/leg-6.md + receipts-B/leg-6.md`.
- `P2.md:8` — LOG append pins entry 2 to lane A's Signal `.node` fallback and entry 4 to lane A's synthetic `/tmp` fixture, dropping the assigned lane-B carriers; entry 4 then rests on evidence ruling (b) excludes.

Clean: `G2.md:2,28`; `G4.md:2,22,25`; `E2V.md:2,13`; `E4V.md:10`; `Z2.md:8`; `Z4.md:9-10` keep carriers separate. Entry 6 documents two distinct jq carriers separately (`E6D.md:16-19`, `G6.md:9`, `Z6.md:9`) — declared aggregation, not a merge claim. Legs 3/5/7 share one carrier per lane, so their merged rows are legitimate.

## THREATS
Documentary only; several texts are stale (Z2/Z5/Z6 report absent drafts that now exist), so some recommendations may already be superseded. `E2D`/`E4D` entry bodies also lack `source:`/`verified-at:`/`recheck:` (ruling (d)) — adjacent finding, not adjudicated here. Landed-entry QUALITY pass and parent integration were not verified.

## VERDICT
FINDING: merged-carrier bases in `E2D.md:12-13`, `K3.md:9`, `E4D.md:8,11-12`, `M2.md:10,15,19`, `K4.md:10`, and wrong-carrier record draft `P2.md:8`; G2/G4/E2V/E4V/Z2/Z4 keep entries 2 and 4 carriers separate.
