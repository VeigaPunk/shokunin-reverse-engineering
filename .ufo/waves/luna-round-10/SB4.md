# SB4 — SHONEN independent, Box 4 (lane B, deepseek-v4.1-flash)

## CLAIM
Independent assessment of SHONEN box 4 — "No cross-domain bleed (PROVINCE.md still accurate)" (`SHONEN.md:11-12`) — at HEAD `6e83a20`: does the province record still hold, and is any cross-domain bleed evidenced?

## METHOD
Read-only; no probes/network. Static pin re-checks (grep on the three cited client configs; `sed -n '17p'` on Ghidra application.properties; `java -version`; npx-cache scan; installed REA-skill frontmatter). Git-blob comparison of PROVINCE.md across luna work commits. Re-read nine reports' SHONEN sections, both jq bleed loci, sibling records (tsukuroi/revenger/Tameshi) and the L0 queue.

## FINDINGS
- PROVINCE drift pins verify exactly: `~/.config/devin/mcp_config.json:7` and `~/.omp/agent/mcp.json:8` → `rea-agents@6.5.0`; `~/.kimi-code/config.toml:1478` → `6.4.0`; Ghidra `application.properties:17` → `application.version=12.1.4`; `java -version` → `21.0.12.1`; npx cache holds only 6.5.0 + 6.4.0; installed skill metadata `version: "42"`, `tool_count: 207`. Round-2 doctor receipts record the same alignment (`receipts/l10-doctor-6.5.0.txt:244,267`; `l10-doctor-6.4.0.txt:241,67` "skill identity is stale") (`PROVINCE.md:15-25`). Catalog digests not re-derived — that needs executing package code.
- PROVINCE.md untouched since `7125dd4`: blob `8a1cec88` at every luna work commit 5→9; the round-2/5 PROVINCE edits were recorded work.
- Bleed evidence: (a) in-lane safety-verdict bleed against `PROVINCE.md:114-116` persists at two loci — `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:217,236-237` ("benign"), qualified only (`:244`; `SCORECARD.md:77-80` keeps correction debt), and `corpus/knowledge/2026-10-13-r3-jq-provenance.md:60,136` ("benign, intentional install"; "no malicious … pathway indicated"), named debt never qualified (`.ufo/reports/luna-round-9/kaidoku.md:53`). (b) kaidoku/revenger shipped-artifact RE ownership unarbitrated: `tsukuroi-shokunin/PROVINCE.md:42,70-71`; `.ufo/l0-questions.md:42`; revenger bounds only its own receipt/version fix (`revenger-shokunin/reports/round-1/connector.md:23,25`) and records the drift-governance question UNKNOWN (`:51`). (c) Tameshi still cites kaidoku's superseded universal evidence-ID formula (`tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:35,73`) though `corpus/QUALITY.md:25` supersedes it.
- Box 4's cited range `PROVINCE.md:88-109` excludes the safety refusal at `:114-116`. All nine reports keep box 4 `[~]`; no non-author verifier record found; all 47 repo commits are authored `kaidoku@shokunin.local`.

## THREATS
No live probe: readiness/staleness claims rest on receipts. Spot-checks cannot prove complete province accuracy or absence of bleed elsewhere. As a parent-dispatched lane-B seat I cannot satisfy the named non-author verifier bar (`.ufo/reports/luna-round-1/kaidoku.md:82-83`).

## VERDICT
FINDING: keep box 4 `[~]` — PROVINCE pins verify, but two recorded safety-scope bleed loci persist, the revenger overlap is unarbitrated, and no named non-author verifier exists.
