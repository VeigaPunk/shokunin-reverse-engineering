## CLAIM
Fidelity sweep and lane adjudication for item 1 (r1 ASAR framing) and item 2 (r4u-01 `.fwimage` decimals) across D1/D2, V1/V2 (Lane A) and VB1/VB2, DB1/DB2 (Lane B). DB1's item-1 block and DB2's item-2 block are the best-supported texts; adopt them as the merged texts.

## METHOD
Primary sources first, lanes unread until verification complete: `python3` hex recheck; own `readelf -S` and `sha256sum` on the four `/usr/lib/firmware/nvidia/610.57.04/` blobs; `git show HEAD` + `grep -n` pointer checks; X1 census run at HEAD (read-only). Then all six seat reports, plus G1/H1 for context.

## FINDINGS
- Item 1: D1, V1, G1, VB1, DB1 agree in substance — keep the launcher/main-entry observation; "renderer payload" understates `obsidian.asar` (45 literal `ipcMain` ops: 44 `on` + 1 `handle("register-cli")`; `main: index.js` absent → not separately launchable). DB1/VB1 is best supported: alone it keeps r2:3's main-process role while adding r3:107's "only its launcher" framing, and quantifies r2's internals (2 literal + 13 dynamic), `app.js` 64 `ipcRenderer`, 3 HTML entrypoints (r2:25, r3:31-37). D1 is faithful but flattens r2's "registers nothing statically" hedge to "found no … surface". V1's "incompletely calls it the main-process bundle" over-rotates vs r2:3 and V01a:9 ("'launcher' does not negate the main-process role"). No Lane-A-only content is lost in DB1.
- Item 2: numbers converge everywhere (`0x1c01dc8` = 29,367,752; `0x505b000` = 84,258,816; hex correct). DB2 is best supported: sha256-matched `readelf` ground truth (VB2), supersession language, :49 consistency arithmetic. The open "source not re-read" threat (D2:23; V2:18) is closed — I reproduced the `.fwimage` fields (`01c01dc8`/`0505b000`) via `readelf -S` and all four blob sha256 vs :10-13. DB2's :47→:49 pointer fix is correct (`grep -n`: wrong decimals at :41, extent at :49; VB2:8 miscited :47). Optional merge: D2's recheck command + round-4 debt pointer (:50-52).
- Census defect: SIZES tokens `29,367,752`/`84,258,816` are unsatisfiable — `h()` (X1.md:13,32; receipts/census-pre.sh:6,25) tests raw tokens against comma-stripped text; expected forms `29 367 752`/`84 258 816`, or normalize tokens. ASAR tokens unaffected. Command A at HEAD PASS (72/72, 9/9, TOKENSET 72/72, MAP-ROWS PASS).

## THREATS
r2/r3 counts are taken as recorded (no archive re-analysis); readelf/sha256 checks are host-current. Header spelling differs ("round 5" vs "luna-round-5") — integrator's call. The census fix is instrument debt, not erratum debt.

## VERDICT
FINDING: adopt DB1 (item 1) and DB2 (item 2) blocks as merged texts; fix the unsatisfiable SIZES census tokens; no numeric divergence between lanes.
