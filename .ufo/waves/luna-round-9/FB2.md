## CLAIM
Anchor audit of lane-A receipts Y3 (r4-16 tail) and Y4 (jq-shadow / PROVINCE refusal): every cited line and byte anchor is correct at HEAD a280e07; no anchor error found.

## METHOD
All read-only at HEAD `a280e07133f52f719b0805fc73c0b997e77b5062` (`git rev-parse HEAD`): Read of cited ranges; `grep -n '^#'` heading scans; python3 last-128-byte ASCII repr; `git cat-file -s`, `sha256sum`; `git diff --exit-code` / `git status --short` / `git ls-files --error-unmatch`; command A from `SCORECARD.md:92-123` run verbatim at `REV=a280e07` (git objects only, no network).

## FINDINGS
- **Y3 exact**: r4-16 = 64,080 B (worktree == git object), 925 lines, EOF LF-terminated; last heading `:875` (`## Errata (… r14-01)`), none after; r12-01 block heading `:728`; final-128-byte repr matches Y3's quoted string character-for-character; tracked; diff exit 0. sha256 `622e3661…d22e`.
- **Stale two-site account confirmed** at r4-16 `:750-752` (clause `:751-752`): “identical … modulo caller output dir (`files[].path`) + per-run `chunks[].provider_id`”. Correcting errata exist at `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:99-104` (four sites / 7 values, not “exactly two”) and `:110-114` — a valid pointer target (file 120 lines; headings `:97`, `:110`). Prompt's `:751-752` vs P0's `:750-752` resolve to the same sentence. Grep `L197` → `:197`, `:652`, `:750`, `:841`: no other two-value account.
- **Y4 exact**: jq-shadow `:217` “Judgment: **benign payload, genuine artifact**”; `:236-237` “benign, intentional agent-installed” (the file's only “benign” occurrences); `PROVINCE.md:114-116` is the current safety-verdict refusal; `:107-109` is the installer bullet (stale steer pointer, corroborated). Addendum — Y4 recorded no append boundary; measured here: jq-shadow = 16,295 B, 242 lines, EOF LF, last heading `:221`, tail-128 `…"identical" phrasing overstated the\n  match precision.\n` (sha256 `541f3499…bf2e`).
- **Command A at HEAD**: `mapped 79/79, knowledge_files 79, citation_resolved_rules 9/9, rule_blocks 9, coverage_score 10.0, depth_score 10.0, missing [], dangling []` — invariant holds.

## THREATS
Static reads only; no probes, network, or non-receipt writes. Pins are HEAD-resolved (worktree/index fully clean). The jq-shadow tail measurement is mine, not Y4's. Y4's “qualification absent” remains true; nothing in either receipt was found false.

## VERDICT
CLEAN
