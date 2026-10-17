## CLAIM
Final QUALITY gate for entry 4, `inspect_sqlite_database`: the Z4-recommended text (G4's B-only draft) admits only the lane-B real-carrier result; state what still blocks admission.

## METHOD
Read-only, 2026-10-16, HEAD `411175e3`. Read Z4/E4D/G4, both leg-6 receipts, SC4, CB3, C1, N1, P0, M2, K4, `QUALITY.md`, `CORPUS.md:17-19`, G3, E6D; ran `git ls-tree`/`git cat-file` and a read-only `ls`+`sha256sum` of the two `/tmp` carriers. No REA/MCP, network, or repo write; Command A not run.

## FINDINGS
- B-scope verified: G4.md:15-20 admits only the B call on `/tmp/bb6-leg-6/sc4-index.db`, SHA-256 `3701a7e3…9728`, Evidence `ev_7572e6…3d6f9a`; lane A appears only as "Excluded comparator" (G4.md:22,25) under `QUALITY.md:22`. Z4.md:2,9,16 recommends exactly this scope, not E4D's merged form.
- Exclusion corroborated: `receipts/leg-6.md:10-12` retains path/8192 bytes/hash only — no bytes or recipe (RV3.md:5 "generated"); `ls /tmp/luna-round-6-leg-6.sqlite` → `No such file`; `/tmp/bb6-leg-6/sc4-index.db` present, `sha256sum` = `3701a7e3…9728` (matches `receipts-B/leg-6.md:25,27`). Lane-A-side critic C1.md:11 concurs. E4D.md:8,11-12, M2.md:19, K4.md:10 still merge A+B → inadmissible as landed form.
- Resolvability: `git ls-tree -r HEAD` lists both leg-6 receipts; SC4/CB3/RV3 are worktree-only (auxiliary).
- Residuals: G4's body lacks `source:`/`verified-at:`/`recheck:` (`CORPUS.md:17-19`; G3.md:10; pattern E6D.md:12-14) — ruling (d) unmet. The stem must land hyphenated `2026-10-16-l7-04-inspect-sqlite-database` (rule (a); N1.md:16, P0.md:8, `SCORECARD.md:102`). Rest checks: labeled obs/inference/unknown (5), versions rea-agents@6.5.0/SQLite 3.54.0 (8), Evidence ID+call (6), path+hash (4), limits named (7), RESULT on real carrier, no promotion (10).

## THREATS
SC4/CB3/RV3 untracked; `/tmp` carriers volatile, so a recheck line must pin the hash. I did not rerun Command A or REA, nor verify the 72 prior entries byte-identically; some prior entries use `- verify:` list style, so the metadata requirement rests on `CORPUS.md:17-19` plus ruling (d).

## VERDICT
FINDING: B-only admission verified (lane A excluded per QUALITY-12; fixture now absent from /tmp), but entry 4 as drafted fails the gate — add source:/verified-at:/recheck:, land the hyphenated stem, keep merged A+B rows out.
