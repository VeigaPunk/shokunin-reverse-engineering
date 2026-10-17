# CB5 — scope freeze (map / PROVINCE Core / held surfaces), lane B

## CLAIM
The round's freeze scope is exactly the map, PROVINCE Core, and the held records. All three are byte-unchanged at HEAD `f0e8cde`, and the map control reproduces the pinned baseline. The battery measures only — nothing may be promoted to held.

## METHOD
Read-only, no REA/MCP probes. `git status --porcelain=v1`; worktree-vs-HEAD sha256 (`sha256sum` vs `git show HEAD:<f> | sha256sum`) for PROVINCE.md, SCORECARD.md, LOG.md, SKILL.md, corpus/README.md; canonical Command A (`SCORECARD.md:92-123`) at REV=HEAD; independent coverage-map token extraction + sorted-token digest from HEAD Git objects; scripted Core row count/section hash. Pinned baseline: `.ufo/waves/luna-round-5/P0.md:5` (72/72, 9/9, 10.0/10.0 at cfc84c2).

## FINDINGS
Freeze list, each verified current:
1. **Map.** (a) Coverage map (`corpus/README.md` "## Coverage map") must keep its 72-token set — sorted sha256 `c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0`, token set == the 72 `corpus/knowledge/` files; Command A must return 72/72 mapped, missing/dangling `[]`, 9/9 rules, 10.0/10.0 — reproduced exactly. (b) REA surface map in `corpus/knowledge/` (`PROVINCE.md:64-71`) stays byte-frozen; an entry refresh may not re-base frozen receipt commands/artifact paths.
2. **PROVINCE Core.** `PROVINCE.md:38-72` + `:119-131` (whole-file sha256 `fe7f3f61c6beb6d601bf6780194ad10f8641c402c2501067d6a93f29c3b37c1c`; Core section `948c85c5…6437b`; 28 held rows = 19 + 9 additions) must not be edited; no promotion may land.
3. **Held surfaces.** Held ground stays only LOG-earned (`PROVINCE.md:28-33`). `LOG.md` `7df0b16b…db4` and `SCORECARD.md` `aaf08a6a…8939` are unchanged; last LOG entry is round-5 records at f0e8cde — no round-6 promotion exists.

Controls: worktree == HEAD f0e8cde; `git status` shows only untracked `.ufo/` dirs; all five tracked files hash equal to their HEAD blobs.

## THREATS
Point-in-time, mid-battery: lane-B receipts present at my check were leg-1,2,7,9,10 (in flight). I cover tracked in-repo artifacts only — client-config drift (Devin/OMP/Kimi pins, `PROVINCE.md:15-24`) and host writes outside /tmp belong to other seats. The digest reads HEAD Git objects and cannot see untracked state (as intended).

## VERDICT
CLEAN — map token set/digest, PROVINCE Core, and held records byte-unchanged at f0e8cde; Command A reproduces the pinned 72/72–9/9–10.0/10.0 baseline.
