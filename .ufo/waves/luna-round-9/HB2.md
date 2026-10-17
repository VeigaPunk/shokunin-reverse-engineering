# HB2 — PROVINCE line-check (item 4)

## CLAIM
Verify PROVINCE.md:114-116 is the exact current refusal-of-safety-verdicts text cited in item 4 (per lane-A `P0.md:8`), and that the steer's `:107-109` pointer is stale.

## METHOD
- Read `PROVINCE.md:95-144`; `sed -n '114,116p' PROVINCE.md`.
- `git rev-parse HEAD`; `git show HEAD:PROVINCE.md | awk 'NR>=107 && NR<=116'`.
- `sha256sum PROVINCE.md` vs `git show HEAD:PROVINCE.md | sha256sum`; `git diff HEAD --numstat -- PROVINCE.md`.
- `grep -n -i -E 'safe|trustworthy|benign|compromise|reuse' PROVINCE.md`.

## FINDINGS
1. :114-116 verbatim:
   - 114 `- **Quality/safety verdicts on findings** — the lane answers "what does this`
   - 115 `  shipped artifact do, per evidence id X" — never "is it safe, trustworthy, or`
   - 116 `  licensed for reuse" `(unowned)`.`
   This is the refusal item 4 relies on ("never … safe, trustworthy, or licensed for reuse").
2. Citation matches committed HEAD. Working tree sha256 `fe7f3f61c6be…3b37c1c` == HEAD (a280e07133f52f719b0805fc73c0b997e77b5062) blob sha256; `git diff HEAD --numstat -- PROVINCE.md` empty.
3. Staleness confirmed: committed :107 is the tail of the source-available-reconstruction item (`anti-trigger `(unowned)`.`), :108-109 the head of the Installing-engines item — not the refusal.
4. Scope note: "compromise" occurs nowhere in PROVINCE.md (grep). Item 4's qualifier wording (safety/trust/compromise/reuse) is wider than :114-116; "benign" is additionally refused at :100-102 ("Malware triage at scale … does not run a triage queue or label samples malicious/benign"). Not a defect in P0's citation, but the parent may anchor the appended qualifier to both :102 and :114-116.

## THREATS
- Line numbers are HEAD-relative; any insert above :114 (forbidden in this round, none observed) would shift them — recheck post-integration.
- The steer's own text was not available to me; staleness is verified against P0's quote of it, not the original.
- "compromise" cannot be tied to any current PROVINCE line — unverifiable as quoted refusal language.

## VERDICT
CLEAN — PROVINCE.md:114-116 is verbatim the current safety-verdict refusal, byte-identical to HEAD a280e07; P0's `:107-109`-stale claim also holds.
