## CLAIM
Four final texts audited at HEAD `a280e07` (RB1–RB4, items 1–4): receipts are five-section/verdict-clean and every append is a purely additive tail land. Defects: RB1's heading breaks the target's seat-id/blank-line conventions; RB4's item-4 text is one unwrapped 919-char line; item 3 (RB3) has no landing text.

## METHOD
Read `.ufo/waves/luna-round-9/{RB1,RB2,RB3,RB4,YB1,YB2,VB4,CB5,Z2}.md`; heading/word/fenced-line scans in python3; `grep -n "^## Errata"` on both knowledge targets; wrap stats over `r4-16:728-796` and `r2-jq-shadow:221-242`; `grep -n "730|105-108|row-7" RB1.md` → exit 1; command A replayed at `REV=a280e07`. Read-only; no probes, network, `/tmp`.

## FINDINGS
- Receipts: all four carry the five sections in order with a `FINDING`/`CLEAN` verdict; words 327/318/318/368 (≤400). RB1 shows six `## ` lines only because its fenced append text embeds a heading (`RB1.md:15`) — content, not a section; fence-blind heading checkers misread it.
- Appends vs targets: r4-16's 13 erratum headings all name a seat (`… Queue-B lane, r12-01`), each preceded by a blank line (`:727,:797,:874`); RB1's `## Errata (round 9 freshness, 2026-10-16, append-only)` has no seat id and no leading blank. RB4's bullet (`RB4.md:11`) is one 919-char line vs the target's wrap (`r2-jq-shadow:221-242`: max 92, mean 76). RB2's note wraps ≤76, and SCORECARD has precedent for `.ufo/waves` citations (9); its “rounds 4–5” en dash differs from SCORECARD's “rounds 4-5” (`:470,:558`) — cosmetic.
- Append-only: RB1 lands after `:925` (64,080 B, LF EOF), RB2 inside the new EOF round-9 SCORECARD section (`:559`), RB4 after `:242` (16,295 B) — original prefixes survive, so T2/S3/S4 `head -c` byte checks stay valid; every text preserves historical wording.
- Coverage: YB1 (22:00:12) flags a second stale r4-16 locus `:730-733` vs `r12-01:105-108`; RB1 (22:00:21) never references it — item 1's text leaves YB1's finding open.
- Item 3: RB3 is disposition-only; nothing appendable to audit.
- Invariants: command A `79/79`, `9/9`, `10.0/10.0`; tracked diff clean; PROVINCE blob `8a1cec88…` == HEAD.

## THREATS
Snapshot at 22:01 while lane-B seats still landed (RB2 arrived mid-audit). Checks are mechanical; content claims were not re-verified (Q1/VB1/VB2/VB4 cover those). No source file was touched.

## VERDICT
FINDING: four finals audited — append-only mechanics are tail-safe and receipts format-clean; fix RB1's heading/blank line, wrap RB4's 919-char line, rule on YB1's `:730-733` locus, and record that item 3 has no landing text.
