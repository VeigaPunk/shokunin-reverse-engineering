## CLAIM
Draft the `inspect_sqlite_database` knowledge entry from two round-6 RESULTs only; this is not universal capability proof or Core promotion.

## METHOD
Read-only review of `corpus/QUALITY.md:11-19`, `.ufo/waves/luna-round-6/SC4.md:8-18`, and both L6 receipts. No probes or network calls. REA version is pinned by `.ufo/waves/luna-round-6/receipts/leg-6.md:3` and `.ufo/waves/luna-round-6/receipts-B/leg-6.md:10-15`.

## FINDINGS
Entry substance (labels retained): **Observation** — REA 6.5.0 / SQLite provider 3.54.0 returned RESULT for `/tmp/luna-round-6-leg-6.sqlite` (SHA-256 `71ac0b8ea43d2f841d019e97fac0f621d0b2dc600ab6fd1314cee831d3e5872b`), call `{path, table:"probe", row_limit:10}`; complete selected-table schema and one sampled row, `order:"unspecified"` (`.ufo/waves/luna-round-6/receipts/leg-6.md:8-13,19`; Evidence `ev_e0eb446a8de2f3749a0be949b881ff66a62dba26ed8c5cfe0159501ab435b3c8`). A path-only call on `/tmp/bb6-leg-6/sc4-index.db` (SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728`) returned complete inventory of `package_index`, 2 columns but columns not requested, `rows:null` (`.ufo/waves/luna-round-6/receipts-B/leg-6.md:20,22-28,35`; Evidence `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a`). SC4 ties that hash to the host index (`.ufo/waves/luna-round-6/SC4.md:8-18`). **Inference** — outputs are consistent with selected-table/sample versus inventory-only calls; differing carriers confound the comparison. **Unknown/limits** — no default row limit, WAL, encrypted, changing, deleted/uncommitted, recovery, or integrity-verification cases tested; output states snapshot stability, bounded unordered rows, unexecuted views/triggers, and virtual/shadow-table limitations (`.ufo/waves/luna-round-6/receipts/leg-6.md:19`, `.ufo/waves/luna-round-6/receipts-B/leg-6.md:35`).

Proposed rows, append after r14-02 before `## Knowledge`:
`| \`knowledge/2026-10-16-l7-04-inspect-sqlite-database\` | SQLite inspection: inventory versus selected-table schema/sample; sample order unspecified | REA 6.5.0; round-6 L6 receipts + SC4 |`
`| \`2026-10-16-l7-04-inspect-sqlite-database\` | SQLite inspector: path-only inventory versus selected-table schema and bounded rows; limitations retained | `.ufo/waves/luna-round-6/receipts/leg-6.md`, `.ufo/waves/luna-round-6/receipts-B/leg-6.md`, `.ufo/waves/luna-round-6/SC4.md` | 2026-10-16 |`

## THREATS
Lane-A carrier is generated (`.ufo/waves/luna-round-6/RV3.md:5`); lane-B is a copied pnpm index with hash checked against SC4. Two successful calls do not establish behavior beyond these carriers and arguments.

## VERDICT
CLEAN — bounded, cited entry draft ready for parent integration; no tracked files changed.
