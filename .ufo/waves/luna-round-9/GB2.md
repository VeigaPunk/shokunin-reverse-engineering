## CLAIM
Second-seat review of lane A's E chain (E1/E2), F chain (F1–F3), and G chain (G1–G4): do their claims, citations, and the round invariants independently reproduce at HEAD `a280e07`?

## METHOD
Read E1–G4 and their cited primaries (r4-16, r12-01, r2-jq-shadow, PROVINCE, SCORECARD, r4–r8 reports, AC2, ZB2, SB1, SB3, RB8). Replayed command A verbatim (`SCORECARD.md:92-123`, `REV=a280e07…`): identical JSON, 79/79, 9/9, 10.0/10.0, exit 0. `git hash-object` matched HEAD for the five cited corpus/control files; `git diff --quiet HEAD --` exit 0. Re-ran F1's grep; rebuilt G3's token set and both hash serializations. No probes, network, `/tmp`, or tracked writes.

## FINDINGS
- **Actionable — F2:** it cites the SH1 safety-language-bleed disposition at `ZB2.md:19` (`F2.md:5,10`); `:19` is "CA1 offline spoofing" — SH1 is `ZB2.md:28`. No other round-9 file contains this catch; fix before integration.
- **G1 stale items:** its "B1 `X1.md:12-16,32` ambiguous" fix is already satisfied — current `B1.md:9` carries the full `.ufo/waves/luna-round-5/X1.md:12-16,32` (B1 mtime 21:51 > G1 21:50; revised post-audit or misread). Its X1 glob also predates `luna-round-9/X1.md` (present). Other G1 items verified: six `2026-10-16-l7-*.md`; the two PROTOCOL.md copies are identical (md5 375e5f3a…) and `:341-343` states the closure-time evidence rule.
- **G3 digest:** confirms TB1/HB4 — published `bd70aa5f…750c` is 63 hex chars (truncated); full value `bd70aa5f…750c4` = sha256(sorted unique token lines + trailing newline); without trailing newline `bc971a10…84860`.
- **E chain:** E1/E2 reproduce (identical command-A stdout; blob identities OK; `:750-754`, `:99-104`, `:112-120`, `:114-116` vs stale `:107-109`, `:217`/`:236-237` all verified). Nits: E1:11 places "not binary compromise" at `:218` — it is `:219` (D4/H4/QB2 agree); E2:10's "only A1.md" snapshot predates the current inventory (disclosed, non-actionable).
- **Reproductions:** F1's grep output matched mine exactly (r6:28, r6:47, r8:33); F3's cites verified (r2 report `:64-66` stale-L7-hash item; r4–r8 blocks); G2's stdout identical to my replay; G4's no-append/byte-identity baseline holds.

## THREATS
Wave files change mid-read (lane-B seats landed concurrently); mtimes are not read-order proof; snapshot ~22:0x. No `/tmp` or live-state checks; G3's post-landing comparison remains pending.

## VERDICT
FINDING: F2's ZB2 pointer is wrong (:19→:28); G1's B1-X1 item is already satisfied; G3's digest is a truncated 63-hex string; E1 `:218` should be `:219`; otherwise E/F/G chains and invariants reproduce.
