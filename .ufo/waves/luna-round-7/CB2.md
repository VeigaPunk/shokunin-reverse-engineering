## CLAIM
All six luna-round-7 entry candidates (all RESULT-class) carry zero affirmative "held/works/promoted" phrasing; every Core mention is a denial — RESULT-class entries never claim Core promotion.

## METHOD
Read-only, no probes/network. Swept all 28 candidate artifacts (E1D–E6D, E1V–E6V, G1–G6, Z1–Z6, M1/M2, K3/K4) under `.ufo/waves/luna-round-7/`; read the six E*D bodies, G1/G2/G6, and K3/K4 in full. Exact sweeps from that directory: `grep -rniwE "held|hold" . --include="*.md"`; `grep -rniwE "works|worked|working" . --include="*.md"`; `grep -rniE "promot" . --include="*.md"` → 32 hits, each classified by context. Class check: `.ufo/waves/luna-round-6/receipts-B/leg-{3..8}.md` RESULT labels.

## FINDINGS
- `held|hold(s|ing)`: 0 hits across the 28 candidate artifacts; hits only in seat meta — C2.md:2,22; Q1.md:17; SH1.md:8; F8.md:17; TB1.md:14,25; RB7.md:8 ("holds 73 data rows").
- `works|worked|working`: 0 in any proposed entry body; P0.md:8 (plan bans universal "works"); G6.md:10 (a labeling recommendation, not entry text) would label a "worked" claim as inference — absent from E6D's body; S2.md:5 "working-tree".
- `promot*` (32 hits): all negations/instructions, none affirmative. Sole in-body hit: E2D.md:17 "it is not a Core promotion" (negated; Q2.md:16 flags only its label class). Remaining hits are seat text: E1D:30, E3D:2,14, E4D:2, E5D:11, E6D:2, E1V:14, E3V:2,16, G2:28, G3:9, G4:28, G5:14,17, G6:13,16, Z1:2, Z4:13, Z6:2, P0:2, P1:21, P2:2, M2:5, C2:22, C5:2, F3:2, Q5:15, S1:11, SH1:2. A structural grep for affirmative promotion (`promote[sd]? to core`, `promoted:`) matched only PB0.md:2 — itself a negation: "nothing here promotes to Core".
- RESULT class confirmed both lanes for all six: receipts-B/leg-3.md:84; leg-4.md:6,71; leg-5.md:50; leg-6.md:4,51,54; leg-7.md:72; leg-8.md:69,76.

## THREATS
Audits wave-7 draft text at write time, not landed files (`corpus/knowledge` still 72; l7 files absent, so C2.md:22's landed-file block persists). Parent integration may add wording; if entry 2 keeps E2D.md:17, the token "promotion" lands in-body (negated) — strip if a zero-token policy is preferred. Stem/matcher (K4.md verdict) and metadata (Z3.md:8) checks belong to other seats.

## VERDICT
CLEAN — all six: zero affirmative held/works/promoted phrasing; Core mentions all negated; RESULT class confirmed; no Core-promotion claim.
