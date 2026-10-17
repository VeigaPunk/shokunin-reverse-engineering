## CLAIM
The quoted claim is not yet supported as a result. It conflates the preregistered target with measured completion and overstates the available evidence for receipt hashing and host non-mutation.

## METHOD
Compared the parent dispatch's frozen L1–L10 predictions and stated success condition with the currently visible round-6 artifacts. Reviewed `EX1.md:5-11` and `receipts/leg-1.md:3-11`; independently hashed the recorded stdout using `printf '6.5.0\n' | sha256sum`.

## FINDINGS
- The dispatch defines a 10-leg battery and ≥8/10 predicted-class criterion; that establishes the plan/threshold, not a measured 10-leg result.
- At this snapshot, `Glob .ufo/waves/luna-round-6/receipts/*` showed only `leg-1.md`. That receipt proves L1's exact result and has a matching stdout SHA-256 (`3eb8e06c…b2459b00`). It does not prove 8/10 or hash all ten receipts; the wording “receipts hashed” should specify whether it means stdout digests or hashes of the receipt files themselves.
- `EX1.md:10-11` explicitly says no broader host/config audit was performed. Thus “zero host mutation outside /tmp” is unverified. Literally, the authorized receipt/report writes are themselves outside `/tmp`; qualify this as probe-induced mutation and name the allowed artifact exception if that is intended.

## THREATS
Artifacts may be created concurrently after this snapshot. Running probes from `/tmp` alone does not establish that all side effects (for example, package-cache writes) were confined there.

## VERDICT
FINDING: only L1 is evidenced so far; the ≥8/10, ten hashed receipts, and zero-outside-`/tmp` claim are not established.
