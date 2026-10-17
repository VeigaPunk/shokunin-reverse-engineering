## CLAIM
The planned SCORECARD known-limits note (B2's `### Known instrument limits` block; Z2's final paragraph) is block-parser safe for command A: the recipe re-extracted from a post-landing SCORECARD is byte-identical, and command A returns the invariant 79/79 + 9/9 (10.0/10.0) at a simulated landed revision. Two placement constraints apply.

## METHOD
Read-only at HEAD `a280e07` (origin checkout verified untouched afterward: `git status --porcelain -uno` empty, HEAD unchanged). Extracted recipe A's 31-line body from `SCORECARD.md:92-123` (sha256 `2cc0f1c0…be06`). Simulated placements in memory: B2 block between recipes A/B (V1), after recipe B (V2), Z2 paragraph in a `## luna-round-9` EOF section (V3), `##`-level variant (V4), note before recipe A (V5). End-to-end: scratch `git clone --no-hardlinks` (no network; removed after), applied append-only landing — SCORECARD V1+V3, pointer append to `2026-10-13-r4-16-frontier-rescan.md`, qualification append to `2026-10-13-r2-jq-shadow-verdict.md` — committed (scratch rev `d8e9b136`), re-extracted the recipe from the modified SCORECARD, ran it with `REV=<scratch>`.

## FINDINGS
- Baseline at `a280e07`: exit 0, `{"mapped": 79, "knowledge_files": 79, "missing": [], "dangling": [], "citation_resolved_rules": 9, "rule_blocks": 9, "coverage_score": 10.0, "depth_score": 10.0, …}`.
- Post-landing clone run: exit 0, identical JSON except `"revision": "d8e9b136…"`. Inputs unaffected: appends only grow the two knowledge files, neither referenced by any SKILL queue-drain rule; README/SKILL bytes held.
- Recipe re-extraction sha identical in V1–V5 (fence/marker extraction stable).
- Caveat (a): V4 — a `##` heading between recipes truncates the `## Measurement recipes` section for `\n## `-splitting consumers (recipe B drops out); use `###` as drafted, or EOF.
- Caveat (b): V5 — inserting before recipe A shifts naive line references (A fence-open 92→97). V1/V2/V3 insert at/after line 125, so `SCORECARD.md:92-123` stays valid at landing; still extract by fence, not hardcoded lines.

## THREATS
Candidates B2/Z2 and representative append text were used; the integrator's final wording/placement may differ — re-verify with the exact landed text. The landed revision was a scratch commit, not the real integration commit; no live census/instrument was rerun. Temp clone removed; no tracked file written.

## VERDICT
CLEAN — note is command-A block-parser safe; place `###` or at EOF, never `##` inside Measurement recipes or before recipe A.
