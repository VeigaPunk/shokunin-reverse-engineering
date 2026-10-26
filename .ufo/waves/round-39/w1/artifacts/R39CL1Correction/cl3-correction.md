**Correction — trend sentence (R38-CL3).** `.ufo/reports/round-38/kaidoku.md:88` says the
attempt-1 v3 amendment "would have turned C1 green (v3: 4/4)"; it would have made C1
**carrier-green** — `c1-v3-at-3b960fe5-NOT-THE-RULE.json` reads `carriers_matched 4`,
`met_target false`, because no Core row exists.

---

One-line form, for a corrections sentence that must stay on one line:

> `.ufo/reports/round-38/kaidoku.md:88`: "would have turned C1 green (v3: 4/4)" → "would have made C1 carrier-green (v3: 4/4 carriers), not claim-green: `met_target false`, no Core row".

Receipt for the quoted numbers: `receipts/host-and-upstream.txt` (last block,
`jq '{carriers_matched, met_target}'` over `.ufo/waves/round-38/l1/scores/c1-v3-at-3b960fe5-NOT-THE-RULE.json`
→ `{"carriers_matched":4,"met_target":false}`), re-read 2026-10-26 by this seat.
