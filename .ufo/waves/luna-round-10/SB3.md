## CLAIM
Box 3 ("instructions executable by an agent without oral context") independently reproduces on every deterministic path; `[~]` is correct and owed only to the missing named non-author verifier (`../PROTOCOL.md:63-72`), not to any Box 3 content defect.

## METHOD
Read `SHONEN.md:9-10`, `../PROTOCOL.md:63-72`, `SCORECARD.md:92-123,131-142`, `corpus/lessons/2026-10-15-round-1.md`, and the seven l7/l8 `recheck:` fields. Replayed SCORECARD command A verbatim at `c343939` (actual HEAD), `6e83a20`, `40162fc`, `66455858`, `c265db9b`; command B verbatim; the lesson's `sha256sum`/`objdump` cross-check; and hashed six pinned carriers. No live MCP probes, no network, no tracked-file writes.

## FINDINGS
- Command A at `c343939`/`6e83a20`/`40162fc`: `mapped:79, knowledge_files:79, missing:[], dangling:[], citation_resolved_rules:9, rule_blocks:9, coverage_score:10.0, depth_score:10.0`; at `66455858`/`c265db9b`: 70/72, missing both r14 files, 9/9, no dangling — matches `SCORECARD.md:244-253,573-574`.
- Command B: baseline `0/9` score 0; after `9/9` score 10.
- Lesson cross-check reproduces byte-exact: `7e8bccc6…5e8b6b  /usr/lib/libjq.so.1.0.4`; `17070: f3 0f 1e fa endbr64`; Evidence `ev_f5e5da50…780481` present in `evidence/round-1-2026-10-15/rea-bundle.json`.
- All six l7/l8 pinned carriers exist with SHA-256 equal to the recheck text: docker `70f68a77…`, rg `d006acfe…`, jq `e8156675…`, `/bin/true` `8bc9a73a…`, signal-desktop `f7a9b441…`, pnpm `index.db` `3701a7e3…`. Cited receipts are tracked (`git ls-files`: 14/12/17 files); operation names grounded at `SKILL.md:11-25`.
- Actual HEAD is `c343939` (post-briefing conformance commit); Box-3 measurements unchanged at both revisions.

## THREATS
MCP-side legs (lesson + seven rechecks) were not re-executed under the no-live-probe rule — package/network availability and Evidence-ID repeatability remain unverified; that is the only untested layer. Carrier hashes are host-today; another host or a mutated system file fails the pins. This seat is lane-dispatched, so it cannot be the `[x]` verifier.

## VERDICT
CLEAN: Box 3's self-containment/executability reproduces under independent replay; keep `[~]` only for the absent named non-author verifier (gate condition, not a content defect).
