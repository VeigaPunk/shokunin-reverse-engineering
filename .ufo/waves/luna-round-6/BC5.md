# BC5 — lane-B report scribe (backfill seat)

## CLAIM
BC5 scribe (lane B, deepseek-v4.1-flash): the round report's one-paragraph lane-B summary — what the fast lane added to the luna-round-6 REA 6.5.0 operability battery. Scribe only: no probes, no promotion.

## METHOD
Read-only at HEAD `f0e8cde`: filed lane-B seat reports, `receipts-B/leg-1..10.md` + `MANIFEST.txt`, lane-A `receipts/`, both census artifacts. Own count audit: (a) ten `receipts-B` digests vs `receipts-B/MANIFEST.txt` → 10/10; (b) BB4's embedded stdout block (`receipts-B/leg-4.md:29-52`, markers excluded per `:26-27`) → `84d489f7…`, its declared digest; (c) presence-scan of the six claimed cross-lane digests across both receipt sets. Only this file written.

## FINDINGS
**Lane-B paragraph:** The fast lane (deepseek-v4.1-flash) supplied an independent second lane: BB1–BB10 re-ran all ten legs from `/tmp` with seat-owned harnesses and hashed transcripts — `receipts-B/leg-1..10.md`, pinned by the round's only complete 10-hash `receipts-B/MANIFEST.txt` (lane A's lists leg-1 only) — and the compare/control seats (CC\*, CB\*, RB\*, SB\*, QA\*, XB\*, TB\*, PB\*, ZB1) audited them cross-lane: both lanes 10/10 against the frozen register (L1 `6.5.0` exact, L2 `207` exact, L3–L8 RESULT, L9–L10 TYPED-REFUSAL), agreement 10/10, 20/20 receipt digests recompute, `CENSUS RESULT: PASS`. Divergences found are class-benign, carrier/route-level: L4 carrier Signal `.node` (A) vs SC2's `/usr/bin/rg` (B); L6 A-receipt is RV3's replay db, B ran SC4's `sc4-index.db`; L8's `which jq` is the 2,267,912-byte static build vs lane A's 30,800-byte PIE; L9's lane-B capture is a 772-byte pretty-printed frame (wire bytes only via CC9's third replay); L10 both lanes refused at prerequisite `inspect_wasm_artifact` (WABT absent) — the predicted compare route never ran, so class credit is contingent. The lane also filed what lane A lacked: CB1's forged-from-lane-A receipt (comparison is not fabrication-proof), CB8's three pre-run lane-A reads, CB6's tamper matrix, and the count-audit gap — `census-laneB-pre.txt` has no parseable Command A record, so the final census compares 1/2 baselines (AC3).

Count audit: receipts A=10/10, B=10/10; manifest 10 hashes; both lane scores 10/10; agreement 10/10. Roster itself uncountable (A 54 seat files vs stated 64, PB2).

## THREATS
Lane-B non-blindness (CB8) and forgeability (CB1; CB6: a self-consistent lane forgery passes ≥8, flagged). `receipts-B` is untracked; compare seats overwrote leg-3/7/8/9 (ZB1) — my audit pins today's bytes only. Byte-identity holds in both receipts for L1/L2/L7/L10 only; L3 `fb47bd53…` and L9 wire `2b596b31…` rest on compare seats. B4's census warning is a false positive per (b).

## VERDICT
CLEAN — lane-B paragraph delivered; recount 10/10 (≥8 gate), agreement 10/10, 10/10 receipts-B digests recompute.
