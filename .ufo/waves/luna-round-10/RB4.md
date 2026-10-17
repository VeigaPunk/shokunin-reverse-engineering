## CLAIM
RB4 reviewer of adversary seats CB1–CB6: which findings stand? All six stand on their core facts — none refuted. The only divergence is normative: CB1's "no conformant-complete close" vs CB2's materiality analysis; CB2's facts govern (living rows, record sections frozen, no score changed), so the outcome is disclosure plus append-only round 10.

## METHOD
Read CB1–CB6 and their subjects (N1.md, X4.md). Re-ran `git diff --numstat <c>^ <c> -- LOG.md SCORECARD.md` for all nine records commits plus `-U0` hunk analysis; parsed fleet `../MANIFEST.json` kaidoku rows; read `.ufo/waves/luna-round-6/BC6.md`, `SHONEN.md`, `AXES.md:65-83`; `git grep -n 'f(content, path, params)'`; sibling files read-only (tsukuroi `PROVINCE.md` ADJ-06). HEAD `c343939`, `git diff --quiet HEAD` exit 0. No writes beyond this file.

## FINDINGS
- **CB1 stands.** Deletions reproduce exactly: `a4bd355` 4, `a9580eb` 8, `0772d54` 7, `cfc84c2` 1, `6e2ee8f` 1 (LOG: 0 everywhere). MANIFEST notes confirm five short-counts — luna2 58/64, luna4 58+6, luna5 58/64, luna6 127 (`BC6.md:2`: luna's 64th seat never existed), luna7 59+5. Six prose values in five luna rows (`MANIFEST.json:2791,2805,2819,2846-2847,2860`). `SHONEN.md:5,7,9,11` = four `[~]`, zero `[x]`. tsukuroi ADJ-06 still "kaidoku/revenger ownership unresolved".
- **CB2 stands.** All deletion hunks land at pre-image line ≤68 (23, 53-55, 25, 56-62, 24, 61-66, 68); first `## luna-round-` heading at `:236`; fixes disclosed (`SCORECARD.md:71-72`). Five commits / 8 sites / 21 lines.
- **CB3 stands.** Four dated sites reproduce (`2026-10-13-r2-evidence-bundle-schema.md:245`, `2026-10-13-r3-mcp-session.md:153`, `lessons/2026-10-13-round-4.md:11`, `README.md:162`); spaced form = 7 files; Open gaps `:51-90` has no such item; `:355` is active-surface-scoped.
- **CB4 stands** (adverse check of X2 found no fault): receipts 80 = `[0,27,0,1,4,26,3,17,2]`; 896 = 4×64+5×128; 36 = 9+27+0+0 — independently corroborated.
- **CB5 stands.** X4 mis-cites verified: `Y3.md:11` disclaims lane identity vs `X4.md:13`; `W9.md:26` not 7-19 (`X4.md:15`); five-commit disclosure omitted (`X4.md:19`).
- **CB6 stands.** N1 omits rounds 2/4; mis-cites verified: `R3.md:10` is a short-count bullet (correct support `W3.md:10`), `R7.md:10-11` is CB3 text (`W7.md:10`), `W6.md:9-13` carries no arbitration text.

## THREATS
Window is open: lane B still landing (RB3/RB6-RB8 unseen). Absence claims (no named verifier) rest on search, not proof. Command A not re-run by me — cited from C1/RB1/CB5. Conformance severity is a parent adjudication.

## VERDICT
FINDING: all six adversary findings stand — disclose the five-commit/21-line SCORECARD rewrite class (CB2's living-region materiality), five-commit seat shortfalls with r6 at 127/128, six prose MANIFEST values in five rows, SHONEN 4×`[~]`, and K1's outbound debt; CB1's veto is parent policy.
