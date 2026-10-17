## CLAIM
Merged sweep of the round-7 corpus at 20:40: 126 outputs read (123 lane reports + backfills BB2/BB5/FINAL-MANIFEST); BB3 absent. Everything converges except the numbered conditions below, which the parent must honor at integration.

## METHOD
Read the full corpus and both census receipts; read-only re-verified lane-B leg-6 tracking at HEAD (`git ls-tree`: 8b47efa7/372c8a8e tracked; SC4 untracked). No probes or writes.

## FINDINGS
1. Land `FINAL-MANIFEST.md`'s six texts/rows: it applies rulings (a)–(d) — hyphen stems, headers, QB2 carriers, G4 B-only, provider-exact fuse names + `electron-fuses` v1, `limit` as default. Don't land pre-manifest underscore drafts (M1:11-13, K3:8-10, K4:10-12, G1:2, P1); underscore maps 72/9.23 (CB3/RB5).
2. Entries 3 and 5 are composed in the manifest and no gate has seen those exact bytes (BB1 THREATS): gate them (CB7/XB1) before/after landing. Pre-manifest gaps (E2D:12-13 merge, E4D/M2/K4 lane-A rows, E3D names/pointer, E5D wording) are moot if the manifest lands as-is (CB5/DB3/RB3/Z3).
3. Still open: Knowledge-row anchor `:139→:140` (BB2 used it) vs `:130→:131` (four-commit precedent); FB3:10's ":131" is wrong; map `:61→:62` settled (RB6).
4. SC1–SC6/SC4/CB3 citations stay untracked auxiliaries (RB1/ZB/CB8; CB7 C13/XB1 warn-only): land or re-anchor. E4V:13-19's "receipts untracked" is false at 411175e (VB4/RB2; verified).
5. Stale, do not honor: Q1–Q6, F1–F5/F7 absence; Z2:5/Z5/E1D:2; F8's 62-file snapshot; PB2 provenance note — run CB7 (`cedc6e30`) or XB1 at the integrated REV. P2's LOG/SCORECARD drafts are records-stage only (RB4).
6. Bare Command A is semantic-blind (C4): four scratch sims print 78/78 with hyphenated names (CB3 d39ff53, RB5 85772d7, XB1 c4edcf3, BB2 8446747); expect 78 files/79 rows (README.md:131; RB7); prior-72 identity and real-landing 78/78 remain unmeasured (N1/N2/SB2).
7. CB8 policy open: inline provenance (bc91424, blob pins, legs 7–8 custody defect — CC7/CC8 replaced BB7/BB8 — "not re-executed in luna-round-7"); no "independent" wording.
8. SHONEN stays `[~]×4` (SH1); no promotion (CB2/RB8); PROVINCE/SKILL/QUALITY frozen (CB6); `/tmp` ≈1.21 GiB residue (SB3).

## THREATS
Snapshot 20:40: BB3 absent; manifest bytes not independently re-hashed here; later edits may supersede pointers.

## VERDICT
FINDING: eight conditions merged — manifest-vs-draft landing choice, entries 3/5 unverified bytes, table-anchor choice, scout durability, stale verdicts, gate runs, CB8 provenance policy.
