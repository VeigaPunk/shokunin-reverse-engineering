## CLAIM
RB5's draft landed 21:30:03 (`RB5.md`, 10,436 B, sha256 `6404312581f2656db890fc342148ddc9983305369c84b99f49ee36b1496a844d`) and passes the overclaim audit with two wording defects: "leg-8-RV3 is byte-identical to leg-8" holds only for raw stdout, and "`tools/list` returned `count:170`" attributes a computed count to the server. The battery's ceiling — six per-name absences/refusals, not the 37-name diff — is correctly carried in the title scope, corroboration bullet, and Unknown bullet.

## METHOD
Read-only; no probes; sole write this file. First pass 21:20–21:30 (bounded 10s poll, 21:24:14–21:30:04) found `RB5.md` absent; re-read after the 21:30:03 landing and audited its bytes at `64043125…844d`. Checks: re-parsed `leg-2.md` raw JSON (tools/list result keys = `["tools"]`; 170 names; no `count` key); `stat`/block-hash `leg-8.md` vs `leg-8-RV3-replay.md`; `grep -c '"version":"6.4.0"'` per receipt; replay heads (`"protocolVersion":"2024-11-05"`; carriers pnpm index.db, `/usr/bin/true`, `/usr/bin/jq`); `sed`-spot-checks `leg-10.md:15,24,45`, `leg-4.md:13`, `leg-5.md:9`, `leg-6.md:11`, `leg-8.md:10`; CB6:7,12,15.

## FINDINGS
- Verified: 170 unique, order-identical names and six absences (my `grep -nFw`: all rc=1, empty); leg-8-RV3 raw stdout = leg-8's (`65d740cf…`); all three replays use `2024-11-05`; every MCP leg's initialize reports `6.4.0`; EX10 figures (30/167/190; Ghidra 12.1.4) match `leg-10.md:47`; `CB6.md:7` supports "set-equal to A6's recorded 6.4.0 list"; `CB6.md:15`/`CA9.md:10` support "six-of-37 consistency, not independent discovery".
- FLAG 1: "leg-8-RV3 is byte-identical to leg-8" — only raw stdout is; the files differ (`leg-8.md` 1,593 B `a1cc891b…` vs `leg-8-RV3-replay.md` 1,646 B `1088b645…`). Fix: "leg-8-RV3's stdout is byte-identical to leg-8's (`65d740cf…`)".
- FLAG 2 (advisory): "L2 `tools/list` returned `count:170`" — the raw result carries only `tools[]`; `count:170` is the receipt's computed summary (`leg-2.md:9`). Fix: "returned 170 tool names (count computed from `tools[].name`)".
- No 6.5.0 query, no config-drift pair, no capability/runtime promotion — all disclosed in the entry's Unknown bullet; the map/Knowledge rows carry "six-of-37 scope"/"for these six names only".

## THREATS
Hunt covers `64043125…844d` only; if RB5.md is revised, re-audit. FLAG 1 may be intended as stdout-identity from context — ambiguous as written. RB5's METHOD says "13 receipt files"; the directory holds 16 (10 legs + 3 replays + `leg-2-tools.txt` + `MANIFEST.txt` + `census-pre.txt`) — scope wording, not a content claim. Receipt-level evidence only; no live probes.

## VERDICT
FINDING: RB5's draft is overclaim-clean against the battery's ceiling except two wording defects — qualify "leg-8-RV3 byte-identical" as stdout-only and "count:170" as computed.
