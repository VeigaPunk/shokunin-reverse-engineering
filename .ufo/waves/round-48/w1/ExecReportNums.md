# ExecReportNums — Round 48 number ledger findings

## Result

Created `ExecReportNums/numbers.md` with the number claims this seat can support: registry roster count and role mix, observed pre-landing counter state, skipped battery status, and self-test outcomes. The roster command parsed the JSON manifest and yielded 75 registered seats in `r48-w1`; this is not a count of completed agents. Role mix: executor 22, scribe 16, scout 9, reviewer 9, critic 6, mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1.

## Counter evidence and interpretation

The retained C1 receipt at `.ufo/waves/round-48/w1/C1IdsArms/receipt.json` reports marker occurrences 0, marker blocks 0, and 24 rule blocks; its battery was skipped because structural clauses failed. It does not report a valid registry meaning-row failure count. The attempted arm-permutation fixture result at `.ufo/waves/round-48/w1/C1IdsArms/fixtures/permuted-arms-result.json` has v3 and v2 both exit 1, but the same result lists malformed census, stale interpreter pin, and three unresolved citations; this is invalid as a discriminator and proves neither that the intended attack passes v2 nor that v3 rejects it for the arm clause alone.

The retained C2 receipt at `.ufo/waves/round-48/w1/C2Quote/counter-receipt.json` reports 2 axes atoms and valid axes score cells (`axis_score_bad=[]`), but also one unsupported quoted-number failure, zero re-derived corrections, and the round-47 seat-floor failure. Its battery is skipped because structural clauses fail. Neither live counter's required forgery battery is measured by these artifacts; do not report a green-count or before/after battery number.

`ExecSelftest.md` records C1 selftest `cases=16 failures=0`; C2 selftest output explicitly limits itself to parser checks. This is not the claim battery or end-to-end counter verification.

## Retained evidence and exact commands

- Number ledger: `.ufo/waves/round-48/w1/ExecReportNums/numbers.md`
- Roster derivation executed:
  `python3 -c 'import json,collections; p="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/swarm-registry.json"; d=json.load(open(p)); m=d["members"]; print("seats",len(m)); print("roles",dict(sorted(collections.Counter(x["role"] for x in m.values()).items()))); print("wave",d["wave"])'`
  Observed stdout: `seats 75`; `roles {'connector': 2, 'critic': 6, 'executor': 22, 'mutation-tester': 6, 'revenger': 2, 'reviewer': 9, 'scout': 9, 'scribe': 16, 'sentinel': 1, 'simplifier': 2}`; `wave r48-w1`. A stream SHA-256/UTC timestamp receipt was not captured; none is claimed.
- Required disk guard `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` returned `/fast/scratch/hyaku` at 32%, 546.1G available. No installation performed.
- Peer receipts referenced above preserve observed numeric details. For missing command/hash/time metadata, consult their reports; this seat does not assert complete capture tuples.

No lane source, frozen path, or other project artifact was changed. No git mutation, build, lint, test, or formatter was run by this seat. No blockers to the scoped ledger; quantitative live-battery counts remain unmeasured because the retained runs skipped those batteries.