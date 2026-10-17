## CLAIM
Independent four-section check of all ten luna-arc reports: `.ufo/reports/luna-round-{1..9}/kaidoku.md` plus round-10's draft (`.ufo/waves/luna-round-10/X4.md`). Each must contain the four required sections (Work performed, Landed changes, Before → after measurements, SHONEN) with non-empty bodies; round-10's landed report path must be absent-as-expected until closure.

## METHOD
Read-only; no probes, no sibling edits. Per report: `grep -n "^## "` heading map plus a Python scan asserting heading presence and non-empty bodies. Environment checks: `git ls-tree -r HEAD -- .ufo/reports/`, existence test for `.ufo/reports/luna-round-10/kaidoku.md`, `git status --porcelain -- .ufo/reports/` (clean ⇒ working tree = HEAD), `grep -n "^### "` on X4.md.

## FINDINGS
- Nine landed reports: all four sections present, bodies non-empty; my line numbers match Y2's exactly (`.ufo/waves/luna-round-10/Y2.md:8-16`) — r1 :7,32,40,72; r2 :8,36,43,70; r3 :8,33,45,70; r4 :8,24,29,70; r5 :9,41,48,69; r6 :7,23,33,69; r7 :6,19,35,58; r8 :6,20,30,53; r9 :7,32,39,58.
- Round-10 draft: `X4.md:2` self-identifies as the closeout draft; proposed text `# kaidoku luna-round-10 — arc closeout` (:10) carries the four sections at :12/:18/:21/:24, non-empty. No other draft exists in the repo; no wave file cites X4 yet.
- `.ufo/reports/luna-round-10/kaidoku.md` absent; `?? .ufo/waves/luna-round-10/` is untracked scratch. The landed path must be materialized at closure.
- Every landed report adds 2–3 extra top-level sections (6–7 headings); the operative reading is presence, not exclusivity (`R8.md:9-10`) — strict "exactly four" would fail 9/9.
- Scope note: `.ufo/reports/` holds ten tracked report files; the non-arc `.ufo/reports/round-1/kaidoku.md` likewise carries all four (:9,40,59,79). Both readings of "ten reports" pass.
- HEAD observation: actual HEAD is c343939 (6e83a20 + protocol-conformance append to LOG.md/SCORECARD.md only, 28 insertions, 0 deletions), not the briefed 6e83a20. Round-10 "final HEAD" measurements must name whichever of these (or successor) they used.

## THREATS
Presence/format only — not report substance, evidence quality, or admission claims. The draft's four sections exist only inside untracked scratch; landing may alter them. All "10 reports" counts include the draft, not only landed artifacts. No live probes, no tracked-file writes.

## VERDICT
CLEAN — 9 landed reports plus round-10's draft all carry the four required sections with non-empty bodies; the landed round-10 report path is absent, as closure expects.
