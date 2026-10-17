## CLAIM
Round-10 SHONEN gate: retain all four `[~]`; SB5's proposed final text matches the box evidence, with two pointer amendments.

## METHOD
Read `SHONEN.md`, all nine reports' §SHONEN, `SKILL.md`/:42-205, `LOG.md`/:455-514,:780-840, `PROVINCE.md`/:1-116, `corpus/lessons/2026-10-15-round-1.md`, lane-A `S1-S5.md`, `SB5.md`, `../PROTOCOL.md:59-73,410-435`; replayed command A verbatim (`SCORECARD.md:92-123`) at actual HEAD `c3439392`; ran `git show --stat c343939` and `git show c265db9:SKILL.md` section map. Read-only; no probes or network.

## FINDINGS
- HEAD: actual `c343939` (parent pinned `6e83a20`, one behind); diff LOG +16 / SCORECARD +12, 0 deletions, `SHONEN.md` untouched; tracked tree clean.
- Command A (independent replay): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 9}` — same values as `SB5.md:8`.
- Retention: all nine §SHONEN sections keep 4×`[~]` (r1:72-83 … r9:58-60); SB5's examples resolve.
- Box 1: SB5's `SKILL.md:86-195` is exactly the nine rules at HEAD; `SHONEN.md`'s `77-191` was the section range at authoring commit `c265db9` (craft heading then :77, now :81 — SKILL.md gained 4 lines), so stale-at-HEAD, not wrong-at-write. Amendment A: the box-1 rider artifacts (decision table `:42-66`, error patterns `:68-79`, checklist `:197-205`; `../PROTOCOL.md:69-70`) lie outside SB5's range.
- Box 2/3 pointers verified: `LOG.md:464-472` and bundle `evidence/round-1-2026-10-15/rea-bundle.json` present; `LOG.md:784`/`:835` are the round-6/8 battery headings; `SCORECARD.md:86-123`, r1`:42-53` resolve.
- Box 4: `PROVINCE.md:95-109` resolves (adjacent list ends :116); lesson `:62-83` carries the version caveat. Amendment B: "contested RE ownership" is unsupported by `SHONEN.md:11-12`; add `S4.md:8-16`.
- SB5 deltas confirmed: `S2.md:4`'s `LOG.md:467-501` is round-1 text; S5's "S1–S4 absent" stale (they exist, retain `[~]`; SB5 cites their VERDICT headings :14/:15/:15 — findings are :15/:16/:16).
- No named non-author verifier: `SHONEN.md` ×4, r1:82-83, `LOG.md:456`, `../PROTOCOL.md:63-68`.

## THREATS
Lane-dispatched seat — not a qualifying verifier; this cannot cure the `[x]` bar. Kaidoku-side records only; a verifier named outside the repo was not exhaustively searched. Final wording must re-pin the post-integration HEAD.

## VERDICT
FINDING: retain 4×`[~]`; adopt SB5's text with Amendment A (rider ranges) and B (`S4.md:8-16`), re-pinned at final HEAD.
