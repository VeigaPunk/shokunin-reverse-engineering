# inspect_sqlite_database — offline SQLite schema inventory

source: `.ufo/waves/luna-round-6/receipts-B/leg-6.md:10,20,23-28,34-35,50-55`; `.ufo/waves/luna-round-6/SC4.md:8-21`
verified-at: 2026-10-16
recheck: Copy the hash-pinned pnpm v11 index (SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728`) to an absolute path and call `inspect_sqlite_database({"path":...})` under `rea-agents@6.5.0`; expect Evidence `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a` with the complete `package_index` inventory and `rows:null`.

REA: `rea-agents@6.5.0`; provider `sqlite` (REA SQLite database inspector), SQLite 3.54.0.

Carrier: `/tmp/bb6-leg-6/sc4-index.db`, SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728`; byte-identical to `/home/vgpnk/.local/share/pnpm/package-manager-store/v11/index.db` (SC4 source). Call: `inspect_sqlite_database({"path":"/tmp/bb6-leg-6/sc4-index.db"})`; Evidence ID `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a`.

- Observation: This path-only call returned RESULT with `wal:null`, a complete `inventory` schema containing one `package_index` table (`column_count:2`; column details not requested), no indexes/views/triggers, and `rows:null`.
- Inference: On this pinned offline copy, the default call inventories schema without returning rows; one carrier does not establish general behavior.
- Unknown: This run did not request table columns or rows, and does not establish behavior for changing databases, WAL inputs, encrypted/corrupt files, or other schemas.
- Limitations: The provider describes stable-file inspection, not an atomic snapshot; deleted or uncommitted records, invalid WAL tails, encryption, forensic recovery, and full integrity verification are outside scope. Views/triggers are not executed; virtual-table column expansion is unsupported.

Sources: `.ufo/waves/luna-round-6/receipts-B/leg-6.md:10,20,23-28,34-35,50-55`; `.ufo/waves/luna-round-6/SC4.md:8-21`. Excluded comparator: lane A's separate synthetic-fixture run is not admitted (`corpus/QUALITY.md:22`; self-made fixture per `CB3.md:12`).
