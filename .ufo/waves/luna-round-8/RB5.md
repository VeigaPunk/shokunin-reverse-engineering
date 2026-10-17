## CLAIM
CA5's conditional recommendation holds: the receipts substantiate one consolidated note — drafted below (complete file text + its Coverage-map and Knowledge rows, per the round-7 E1D/FINAL-MANIFEST pattern). Landing raises the coverage denominator 78→79; the rows must ride in the same change.

## METHOD
Read-only at HEAD `6e2ee8f`. Read all 13 receipts, `MANIFEST.txt`, `census-pre.txt`; recomputed ten receipt SHA-256 and the leg-3 displayed-block hash; `wc -l`/`grep -nFw`/`sort -u` on `leg-2-tools.txt`; read `SCORECARD.md:92-123,467-532`, `QUALITY.md:7-25`, `README.md:11-67,69-151`, l7-01, round-7 `E1D.md`/`FINAL-MANIFEST.md`, and round-8 `CB6/CA9/CA6/RE1/FB2/VB3/VB5/VB6/VB7/ZB2.md`. No probes; this file is my only write.

## FINDINGS
- Classes confirmed: L1 `6.4.0`; L2 `count:170`/170 unique names; L3–L8 six `-32602 "Tool <name> not found"`; L9 six `grep -nFw` absences; L10 control RESULT (`ev_9befd8a5…`, 202/202) + fresh EX10 controls; CB6 6/6 A6 corroboration (`CB6.md:12`).
- Draft embedded below: RESULT/refusal-class only; meets QUALITY #1/#4/#5/#6/#7/#8/#10/#12; standard metadata fields, per the l7 entries.
- Denominator: file-only → `missing=["2026-10-16-l8-01-6p4-symmetry-battery"]`, coverage 9.87. With both rows → /tmp simulation (scratch commit `9d9eced3…`): `knowledge_files=79, mapped=79, missing=[], dangling=[], coverage 10.0, depth 10.0`; stem fullmatch; 79 tokens. Re-measure post-landing; token/knowledge digests change (`census-pre.txt:93,95`).
- Integrity notes: (a) leg-3's known defect is absent from current bytes — block lines 21-22 + LF = `5c682099…` = the `/tmp` raw (623 B); a mismatch reproduces only with the fence line in or trailing LF out (`FB2.md:12`, `VB7.md:18`) — no repair needed. (b) `MANIFEST.txt:10`/`CA6.md:10` leg-10 hash predates the post-census append (`VB5.md:14`); the entry cites content lines. (c) Receipts are untracked; round 6 landed tracked (`SCORECARD.md:479-480`) — parent's call.

FINAL FILENAME: `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md`

FINAL FILE TEXT:

```markdown
# REA 6.4.0 operability-symmetry battery — six 6.5-only verbs refused, 170-tool list, live control

source: `.ufo/waves/luna-round-8/receipts/leg-1.md:3-11`; `leg-2.md:1,9,17` + `leg-2-tools.txt:1-170`; `leg-3.md:3-6,17-22`; `leg-4.md:4-13`; `leg-5.md:3-13`; `leg-6.md:3-4,11-19`; `leg-7.md:3-15,17-22`; `leg-8.md:3-13,15-19`; `leg-6-RV3-replay.md:3-13`; `leg-7-RV3-replay.md:3-14`; `leg-8-RV3-replay.md:3-13`; `leg-9.md:1-23`; `leg-10.md:4-26,28-59`; corroboration `.ufo/waves/luna-round-8/CB6.md:7,12,15,20` + `CA9.md:8-10`; A6 inventory `.ufo/waves/luna-round-2/A6.md:8`
verified-at: 2026-10-16
recheck: `cd /tmp && timeout 240 npx -y rea-agents@6.4.0 --version` → expect exactly `6.4.0`; then `cd /tmp && npx -y rea-agents@6.4.0 mcp`, send `initialize`, `notifications/initialized`, `tools/list`, and one `tools/call` per refused name; expect `count:170`, six JSON-RPC refusals `{"code":-32602,"message":"Tool <name> not found"}`, and control `inspect_binary_layout {"path":"/usr/bin/jq","detail":"summary"}` → view `ev_9befd8a5929e366be05a30766d94f8db891951aa45fc77d0afba4d942fe2af45`, `coverage.status:"complete-within-view"` 202/202.

REA pin: `rea-agents@6.4.0`; every `initialize` response reports `rea` `6.4.0`; protocol revisions `2024-11-05` (L3–L5, L8, RV3 replays) and `2025-03-26` (L2, L6, L7, L10); server invocation appears as both `… mcp` and `… --mcp` across legs.

Carriers (pinned per receipt): `/usr/bin/docker` (L3) and `/usr/bin/rg` (L4) path-only — refusal precedes any read; `/usr/lib/signal-desktop/signal-desktop` 223,513,856 B SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a` (L5); synthetic fixture `/tmp/luna-round-8-leg-6.sqlite` 8,192 B SHA-256 `03c5ec9eaa7ec177f71a47b69c3ca9848190a5cd59dd66c14bc0db0e30cf2fc2` with inline recipe `CREATE TABLE probe (id INTEGER PRIMARY KEY, label TEXT NOT NULL)` + one row `luna-round-8-leg-6` (L6; byte-exactness claimed for these fixture bytes only); `/usr/bin/true` 43,320 B SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d` (L7); `/home/vgpnk/.local/share/pnpm/package-manager-store/v11/index.db` 16,384 B SHA-256 `3701a7e3465525c57e14106987c66bed10b4938ec190c2692beb6e434eaf9728` (L6-RV3); `/usr/bin/jq` 30,800 B SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` (L8-RV3, L10 control).

- **Observation (RESULT legs):** L1 returned `6.4.0`, exit 0. L2 `tools/list` returned `count:170` and 170 unique names (`leg-2-tools.txt`), set-equal to A6's recorded 6.4.0 list (`CB6.md:7`). L7's same-session `open_binary` on `/usr/bin/true` returned ELF x86-64 RESULT before the refusal. L10's control view reports `parent_operation` `inspect_binary_layout`, `complete-within-view` 202/202, 28 sections/15 segments/80 symbols/79 relocations; EX10's fresh control adds `open_binary` RESULT, `binary_overview` RESULT (30 segments/167 procedures/190 strings; provider `rea-workflow`, upstream Ghidra 12.1.4), and `close_binary` `{"result":null}`.
- **Observation (refusal legs):** `inspect_go_binary` (L3), `inspect_rust_binary` (L4), `inspect_electron_fuses` (L5), `inspect_sqlite_database` (L6), `search_bytes` (L7), `inspect_with_objdump` (L8) each returned `{"code":-32602,"message":"Tool <name> not found"}`; the server kept serving and exited 0 on stdin close. Replays L6/L7/L8-RV3 (L6 on a different carrier) reproduce the same class; leg-8-RV3 is byte-identical to leg-8. L9's six `grep -nFw` checks over the 170-name list exit 1 with empty stdout (empty-string SHA-256 `e3b0c442…`).
- **Observation (corroboration of A6):** CB6 scores 6/6 per name against A6's recorded inventory (`.ufo/waves/luna-round-2/A6.md:8`; 170 vs 207 MCP tools): each name present in A6's 6.5-only list and 6.5.0 receipt, absent from both 6.4.0 records (`CB6.md:12`).
- **Inference:** On this pin the six names are absent from the served list and refused per call — a catalog/name-surface result, not a functional verdict on any 6.5.0 feature. The control legs show the refusals are name-addressed, not session loss.
- **Unknown / limitations:** Only six of A6's 37 6.5-only MCP names were probed, selected from A6's list — consistency, not independent discovery (`CB6.md:15`); the other 31 names and A6's CLI-side 6.5.0 names were not re-verified (`CA9.md:10`). No 6.5.0-side run this battery (that side rests on A6's round-2 receipts and the six 6.5.0-verb entries). Mixed protocol revisions; no per-protocol matrix. No config-drift pair. Refusal payloads carry no evidence ids; L3/L4 carriers path-only. leg-3's displayed stdout block and its raw `/tmp` copy (623 B) hash identically (`5c682099…`); `MANIFEST.txt:10`/`CA6.md:10` leg-10 whole-file hash predates a post-census append (`leg-10.md` current bytes `6cd389e9…`, first 27,655 bytes `c89eea7a…`), so leg-10 is cited by content lines. This is a name-surface battery: RESULT/refusal-class only, no capability promotion, no runtime-behavior claim.

Sources: `.ufo/waves/luna-round-8/receipts/leg-1.md:3-11`; `leg-2.md:1,9,17` + `leg-2-tools.txt:1-170`; `leg-3.md:3-6,17-22`; `leg-4.md:4-13`; `leg-5.md:3-13`; `leg-6.md:3-4,11-19`; `leg-7.md:3-15,17-22`; `leg-8.md:3-13,15-19`; `leg-6-RV3-replay.md:3-13`; `leg-7-RV3-replay.md:3-14`; `leg-8-RV3-replay.md:3-13`; `leg-9.md:1-23`; `leg-10.md:4-26,28-59`; corroboration `.ufo/waves/luna-round-8/CB6.md:7,12,15,20` + `CA9.md:8-10`; A6 inventory `.ufo/waves/luna-round-2/A6.md:8`.
```

MAP ROW (3-cell — coverage map; insert after the `2026-10-16-l7-06` map row, i.e. after `corpus/README.md:67`, before `## Knowledge`):

```markdown
| `knowledge/2026-10-16-l8-01-6p4-symmetry-battery` | REA 6.4.0 MCP surface (170-name tools/list) with the six 6.5-only names absent and per-call typed-refused (`-32602`, `Tool <name> not found`: `inspect_go_binary`, `inspect_rust_binary`, `inspect_electron_fuses`, `inspect_sqlite_database`, `search_bytes`, `inspect_with_objdump`); live `inspect_binary_layout` control RESULT; per-name A6 corroboration (6/6), six-of-37 scope | REA 6.4.0 subprocess battery; round-8 `receipts/leg-1..10.md` + `leg-2-tools.txt` + `CB6.md:12` |
```

KNOWLEDGE ROW (4-cell — `## Knowledge` table; insert after the `2026-10-16-l7-06` Knowledge row, i.e. after `corpus/README.md:151`):

```markdown
| `2026-10-16-l8-01-6p4-symmetry-battery` | REA 6.4.0 symmetry battery: 170-name tools/list; six 6.5-only MCP names typed-refused per call; control RESULT; corroborates A6 for these six names only | rea-agents@6.4.0; `.ufo/waves/luna-round-8/receipts/` + `CB6.md:12`; pre-state Command A 78/78, 10.0 | 2026-10-16 |
```

Landing notes: diff = one new file + `corpus/README.md` +2 rows. Post-landing Command A (verbatim recipe) should print `knowledge_files=79, mapped=79, missing=[], dangling=[], coverage_score=10.0, depth_score=10.0, citation_resolved_rules=9`; token/knowledge digests change from `c6c025f3…`/`00891de8…` (`census-pre.txt:93,95`).

## THREATS
Unlanded draft: post-landing 79/79 and QUALITY acceptance remain parent-side measurements (mechanics predicted, not re-run; round-7 `RB4.md` precedent). A6 corroboration is consistency for six names selected from A6's own list (`CB6.md:15`); no independent 37-name or CLI-side proof (`CA9.md:10`). L3/L4 carriers path-only; refusals carry no evidence ids; receipt hashes do not prove execution (`CA6.md:16`).

## VERDICT
CLEAN: one consolidated entry + both README rows drafted from confirmed receipts; 78→79 denominator consequence and the leg-3/leg-10 integrity notes flagged for integration.
