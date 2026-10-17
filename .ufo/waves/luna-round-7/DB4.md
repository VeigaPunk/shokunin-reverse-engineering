## CLAIM
Entry-4 content-derivability audit, real-carrier scope: the lane-B claim set for `inspect_sqlite_database` is fully derivable from tracked round-6 evidence; the lane-A half attached by E4D/M2/K4 is not admissible, so those texts over-claim.

## METHOD
Read-only. `git ls-tree`/`git show` at HEAD `411175e`: `receipts-B/leg-6.md` (blob `372c8a8e`, worktree==HEAD) and `receipts/leg-6.md` (`8b47efa7`); drafts E4D, G4, Z4, M2, K4; `corpus/QUALITY.md:22`; CORPUS.md:17. One read-only local re-hash of the cited carrier; no REA/MCP/network; only this file written.

## FINDINGS
- Derivable — G4:13-22 vs tracked receipt: 6.5.0 version (:34; preflight :14-15); provider `sqlite`/SQLite 3.54.0 (:35); carrier path + `3701a7e3…9728` (:20,:25,:35); path-only request (:20); Evidence `ev_7572e622…` (:35,:51); complete `inventory` schema, one `package_index` table `column_count:2`/`columns_completeness:not_requested`, empty indexes/views/triggers, `rows:null`, `wal:null` (:35); RESULT class (:50-54); pre/post hash equality (:27-28); no `-wal/-shm` (:26). G4:19-20 limitation/unknown text maps to :35 items (stable-file/no-atomic-snapshot; deleted/uncommitted/WAL-tail/encrypted/forensic/full-integrity out of scope; views/triggers not executed; virtual-table expansion unsupported). G4:18's "default call" is labeled inference and carrier-hedged — keep the hedge.
- Live re-hash (not required for derivability): `sha256sum …/v11/index.db` → `3701a7e3…9728`, 16384 B, mtime 1792051409 = receipt :25, so G4:15's byte-identity still reproduces.
- Not derivable in real scope: E4D:8 merges lane A's selected-table/sample result and its differential inference; E4D:11-12, M2:15 and K4:10 name "selected-table schema/sample" for entry 4. That half rests on the synthetic fixture (`receipts/leg-6.md:3-14`; RV3:5 "generated"; CB3.md:12) with no retained bytes/recipe — `QUALITY.md:22`, parent ruling (b).
- Format gate: G4:11-22 lacks `source:`/`verified-at:`/`recheck:` (shokunin protocol CORPUS.md:17; ruling d); E6D:12-14 is the pattern.
- Durability: G4:22 cites `SC4.md`; exclusion rationales cite CB3 (`CB3.md:12`) and RV3 (`E4D:15`) — all untracked (`git ls-files --error-unmatch` → "did not match"). Hash/path facts survive in tracked receipt :23-28 alone; cite those, or land SC4.

## THREATS
No REA re-execution; receipts are retained records, not independent re-derivation. Host pnpm index is mutable (identity is a 2026-10-16 snapshot). Command A counts and the other five entries were not checked here.

## VERDICT
FINDING: land entry 4 from the G4 B-only set (fully derivable, needs the three metadata fields) and strip lane-A selected-table/sample wording from E4D/M2/K4 entry-4 rows (`QUALITY.md:22`).
