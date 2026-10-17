## CLAIM
A process-free L1 receipt can be made internally hash-consistent; whether the final gate accepts such a forgery is unverified.

## METHOD
Read `.ufo/waves/luna-round-8/receipts/leg-1.md:3-11` and `EX1.md:5-11`. Ran `printf '6.4.0\n' | sha256sum` → `3754366908ac60b46e7aab559e5d23fa7eea0ff51835fb9fd72ba76aab3bcafd  -`. No npx/MCP call and no receipt was created or altered.

## FINDINGS
A concrete candidate attack is to copy the claimed command and `/tmp` working directory, then author stdout `6.4.0`, empty stderr, exit `0`, and the digest above—without running npx. This reproduces the receipt’s visible fields and hash. SHA-256 is unkeyed and stored beside the stdout, so it checks byte consistency only; the receipt has no nonce, trusted timestamp, process identity, environment/package-integrity record, or independent execution log. Freezing predictions prevents changing the expected answer, not fabricating its transcript. At this snapshot `git status --short -- .ufo/waves/luna-round-8` returned `?? .ufo/waves/luna-round-8/` (untracked, not committed provenance).

## THREATS
This is a feasible text-level spoof/replay candidate, not evidence that L1 was forged. I did not inspect or execute a final acceptance gate, so cannot claim this candidate would pass it or assess other legs.

## VERDICT
FINDING: Offline receipt spoofing is possible at the text/hash layer; end-to-end rejection is unproven.
