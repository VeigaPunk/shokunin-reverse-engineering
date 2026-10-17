## CLAIM
A replay-style fake can satisfy the visible receipt shape and stdout-hash checks, but whether it passes RV1–RV8 is unverifiable: the repository exposes only RV6/RV8 reports, not their full check contract or implementation.

## METHOD
Read `RV6.md:5-11`, `RV8.md:5-11`, `CA8.md:5-11`, and `receipts/leg-1.md:3-11`. `Glob .ufo/waves/luna-round-6/*.md` showed RV6 and RV8 but no RV1–RV5/RV7; repo-wide `Grep RV1` returned “No non-sensitive matches found.” Recomputed `printf '6.5.0\n' | sha256sum` → `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`.

## FINDINGS
A concrete one-leg forgery candidate (described only, not written): copy L1’s visible expected command, `6.5.0` stdout, empty stderr and exit 0 into a claimed new run’s receipt; include the recomputed digest. It is syntactically complete and internally hash-consistent, yet the text alone cannot show that a process ran now. Only L1’s transcript was available, so I cannot construct or claim a full ten-leg fake passed the suite.

RV8’s stated target is receipt presence/non-emptiness and command/stdout/stderr/exit fields; that can reject absent or malformed receipts, not this replay. RV6 aims at matching carriers to scout evidence and could catch a path/hash substitution if independently pinned and enforced; its report says the comparison was impossible at its inspection snapshot. A same-carrier replay is not ruled out. No evidence establishes what RV1–RV5/RV7 test.

## THREATS
The stdout SHA-256 is unkeyed and stored beside the claimed bytes. No visible signature, trusted timestamp, process identity, or execution log binds the receipt to a real invocation. CA8 also notes predictions were exposed before execution (`CA8.md:8-11`).

## VERDICT
FINDING: Visible completeness checks can reject missing/malformed receipts and carrier pinning may reject substitutions; execution authenticity and replay remain open, while full RV1–RV8 passability is unverifiable.
