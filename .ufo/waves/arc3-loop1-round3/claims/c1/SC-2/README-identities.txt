# SC-2 draft identities — arc3-loop1-round3, c1 scribe

Re-derived by this seat after its final writes (rule #14), 2026-10-19T~13:47Z
(entry rev 3 — the fold-in of the convergence seat's roster + id data points).
HEAD at all reads: `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. All hashes
`sha256sum`, recomputed — not transcribed.

| artifact | bytes | sha256 |
|---|---|---|
| `records-drafts/knowledge-entry-draft.md` (rev 3) ≡ mirror `SC-2/knowledge-entry-draft.md` | 21,585 | `5c1818c7d13d1055f310f1f8d232c06778e5586d7c8cc473a02187f3a4b720af` |
| `records-drafts/map-token-patch.md` (≡ mirror) | 4,069 | `333ca590716b27126fadd0ca9747dce5742e26c0a897d5090d7d7e6dcea11841` |
| `records-drafts/records-drafts.md` (≡ mirror) | 12,617 | `f49aa9ee79198582cbd314bcbbae9e92a8955dc5ae25490cc8d02ed1627bf4f6` |
| `SC-2/recheck-opt200.json` (this seat's fresh run) | 10,620 | `05f76b33db9b42b0d71bd899125e7ec2ef1c3538f7ea8616f12f13548ebbd1bf` |
| `SC-2/recheck-rv2token.json` (this seat's fresh run) | 9,399 | `f2aec424c1edade81d7bbe58f0d99be7f5d2253749ffb09e9a2a4226425f42f8` |
| `SC-2/command-A-before.txt` | 220 | `9de3cbddb68f19ad99003ad329b87b6670c6c83eb7b6f7aef14e1f7af7473cc1` |
| `SC-2/commandA-rehearsal-before.txt` (82/82, 14/14) | 158 | `3100ff974a0f017f38ef18ccf9015b4e395abafa5a0e819bbbdd4413a791cdac` |
| `SC-2/commandA-rehearsal-after.txt` (83/83, 14/14) | 158 | `9555a677b9b3b75fd082f47bf07e2511fda11a7a0a07150649a37139536735b1` |
| `SC-2/parse-envelopes.py` (tool) | 1,782 | copied byte-identical from `/var/tmp/sc2/` |
| `SC-2/rehearsal.py` (tool) | 1,724 | copied byte-identical from `/var/tmp/sc2/` |
| `SC-2/README-identities.txt` (this file) | — | re-hash after write if quoting |

Cross-checks (not self-claims; the other party's value quoted):

- `records-drafts/map-token-patch.md` `333ca590…` — unchanged across rev 3; RV-4's
  report records the same sha256 for the producer artifact it reviewed and
  PASSes line-neutrality for both variants (`seats/RV-4.md`). Its independent
  PRIMARY after-state README measurement (`016b632e46e5852a…`) equals this
  seat's rehearsal README after-state.
- `SC-2/recheck-opt200.json` `05f76b33…` ≡ EX-10's
  `probe/probe-B-opt200-hex-6.4.0.json`; `SC-2/recheck-rv2token.json`
  `f2aec424…` ≡ EX-06's `evidence/recheck-rv2token-hex-6.4.0.json` ≡ VZ-1's
  `evidence/probe-toolcheck-rv2token-6.4.0.json` (three-way byte-identical
  envelopes; VZ-1's SHA256SUMS lists the same digest).

Rehearsal literal entry (the text that would land as
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`): 37 lines,
17,563 B, sha256 `189ac2a2cd564eca4c285a56e4ae649264c21733dc22dcfbfe380036834ddaf2`
(extracted from the rev-3 draft's marker block; a landing must re-derive the
landed file's own identity per rule #14 — the file's own first line is the
staging HTML comment).