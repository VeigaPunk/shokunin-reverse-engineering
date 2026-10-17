# CB8 — prediction-fishing 2: did the lane-A receipt-command allowance leak outcomes?

## CLAIM
Yes, it leaked lane-A's *observed* outcomes in practice, though not the prediction classes (those were public): lane-A receipts have no commands-only artifact, and all three exception seats (BB2/BB7/BB10) self-document seeing lane-A output/hash before running. No fabrication is evidenced.

## METHOD
Read BB2.md, BB7.md, BB10.md and their receipts-B/leg-{2,7,10}.md; lane-A receipts leg-{1,2,7,9,10}.md for format; BB1.md, SB2.md, CC1.md, CA8.md for discipline context. Compared cross-lane stdout hashes and stderr fingerprints; recomputed `printf '6.5.0\n' | sha256sum` → `3eb8e06c…` (matches both lanes; CC1.md:10 corroborates).

## FINDINGS
- No commands-only artifact exists: lane-A receipts bundle command, full stdout, stderr, exit, declared hash. Leg-2's header itself carries `count:207` and `STDOUT SHA-256: 38d44bf8…` (receipts/leg-2.md:6-7); leg-9/10 print refusal payloads one line below the command (receipts/leg-9.md:1-11; receipts/leg-10.md:3-27).
- All three exception seats confirm exposure: BB2 "Not blind: lane A's header read exposed their summary line (count 207, hash)" (BB2.md:20); BB7 "expected output was known before my run" (BB7.md:18); BB10 "exposed Lane A's output/hash before my run" (BB10.md:20). The increment is lane-A's observed bytes/hash; predictions were already dispatch-public (CA8.md:2,8).
- Runs still read genuine, not copied: distinct stderr fingerprints (receipts-B/leg-7.md:46-47 times 1792188070078/1792188075154, durations 18.89/5072.89 ms vs lane-A receipts/leg-7.md:26-27: 1792186077613/1792186082642, 19.15/5023.4 ms), own cwd/cache (BB2.md:8), empty vs npm-notice stderr (BB2.md:21), captures re-hashed from own raw files. stdout matches byte-for-byte (BB2.md:15; BB7.md:13; BB10.md:4), as expected for deterministic output.
- Consequence: legs 2/7/10 cross-lane agreement is directed replay — it evidences command reproducibility, not blind independent convergence.

## THREATS
Strict line-1 command extraction would avoid class exposure; the leak came from header/route reads, disclosed honestly. Compliance rests on self-report (no access log) and receipt timestamps are owner-editable, so "genuine separate run" evidence is suggestive, not cryptographic. Other lane-B seats documented discipline (BB1.md:7 post-run read; SB2.md:5 no receipts read) but that too is unaudited. Snapshot ~19:03; remaining lanes' receipts may add evidence.

## VERDICT
FINDING: the allowance is not outcomes-blind in practice — all three exception seats saw lane-A output/hash before running (self-disclosed); legs 2/7/10 are non-blind directed replays. No fabrication evidence; leak scoped and disclosed, discipline unaudited.
