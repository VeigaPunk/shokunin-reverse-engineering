# RunTxA — R27-C1 tinyxxd runs for verbs analyze and inspect

Seat: RunTxA. Carrier: tinyxxd (/usr/bin/tinyxxd), sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, address 0x103d40.
Pin: rea-agents 6.5.0, package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c (matches the frozen value in claims.json).
Scope: only the two verbs analyze and inspect, three runs each (base, repeat, renamed). No other verb was run.

## runs.tsv

Written at /fast/scratch/hyaku/kaidoku-r27/seats/RunTxA/runs.tsv (sha256 3f888cf0592d588454d81a5ab61ef1ff44d1001add1e943d3cf1480ac8137938). Header line, tab separated:

seat	carrier	verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256	pkg_version	pkg_json_sha256

Six data lines follow (one per call), in run order analyze/base, analyze/repeat, analyze/renamed, inspect/base, inspect/repeat, inspect/renamed:

RunTxA	tinyxxd	analyze	base	/usr/bin/tinyxxd	analyze /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:54:53Z	2026-10-22T14:54:59Z	c8ca34fc8c43b231fcf7ad7d7693d5c806e96ae5acf5a50c4097f9095a42042b	ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxA	tinyxxd	analyze	repeat	/usr/bin/tinyxxd	analyze /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:54:59Z	2026-10-22T14:55:06Z	217003ac0c9ab25255ad4d1a6ee2ba212b26c3c36c1419c68fa41f497522c4a4	ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxA	tinyxxd	analyze	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	analyze /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat --format json --full-output	0	2026-10-22T14:55:06Z	2026-10-22T14:55:13Z	9da2571d92af2f5d8fa29536f11f9554c0d8970d7ca73187e5ff26bea168acbe	ev_65e0dbfb6cca1cce703a51a18ab821b984e5344b4f6377ef51ffd510a0a17efb	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxA	tinyxxd	inspect	base	/usr/bin/tinyxxd	inspect /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:55:13Z	2026-10-22T14:55:19Z	8c30a1393f882206210ebcf77caaf65a24b19df3e862ea636f9502740d44a24a	ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxA	tinyxxd	inspect	repeat	/usr/bin/tinyxxd	inspect /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:55:19Z	2026-10-22T14:55:26Z	6ddc607df2fa56cf64301b2e31d96f79c95509c9edb0680906c9ae676587850d	ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxA	tinyxxd	inspect	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	inspect /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat --format json --full-output	0	2026-10-22T14:55:26Z	2026-10-22T14:55:34Z	aeece412cb635f25ab208f48cd12212014d9b64341529d66d856e6a2b991a629	ev_65e0dbfb6cca1cce703a51a18ab821b984e5344b4f6377ef51ffd510a0a17efb	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

## Verdicts

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| analyze | ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b | ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b | ev_65e0dbfb6cca1cce703a51a18ab821b984e5344b4f6377ef51ffd510a0a17efb | yes | no | rename-sensitive |
| inspect | ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b | ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b | ev_65e0dbfb6cca1cce703a51a18ab821b984e5344b4f6377ef51ffd510a0a17efb | yes | no | rename-sensitive |

Verdict rule from claims.json applied literally: unstable if base != repeat; content-keyed if renamed == base; else rename-sensitive. Both verbs are rename-sensitive (observation, computed from the three ids above).

Extra observation for the L1: the analyze and inspect envelopes for the same path carry the same evidence id, so the id depends on the analyzed bytes, not on the verb name. Both are still separate rows in the table because the counter keys rows by (carrier, verb).

## Subject fields per run

- analyze/base, analyze/repeat, inspect/base, inspect/repeat: subject.name = tinyxxd, subject.local_path = /usr/bin/tinyxxd, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65.
- analyze/renamed, inspect/renamed: subject.name = tinyxxd-r27-renamed.dat, subject.local_path = /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 (same bytes as the carrier).

## Rename-sensitive field differences (base vs renamed)

Diff script: /fast/scratch/hyaku/kaidoku-r27/seats/RunTxA/diff-and-check.py, output diff-and-check.out. Compared the seven hashed fields (.data.parameters, .data.raw_result, .data.normalized_result, .data.locations, .data.environment, .data.limitations, .data.evidence_links) leaf by leaf.

For analyze and for inspect the result is identical: parameters, raw_result, locations, environment, limitations and evidence_links are byte-for-byte equal between base and renamed; normalized_result has exactly one differing leaf.

- .data.normalized_result.document — base: "target-7b1e5d0c970a.bin" ; renamed: "target-7b1e5d0c970a.dat"

That single string is the whole difference and it is what the 6.5.0 semantic projection hashes into the evidence id, so the renamed copy gets a different id for identical bytes.

## Failures

None. All six calls exited 0. Every stderr file is empty (0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). No call was repeated to obtain a different result; the base and repeat runs are two separate invocations, one after the other.

## Additional checks run by this seat (not part of the counter)

- Evidence id recompute under the 6.5.0 rule: tools/round-26/recompute-ids.py recomputed all six stored ids and matched all six (recompute-check.out). Output excerpt: "tinyxxd-analyze-base.json stored=ev_89338dd2... recompute=ev_89338dd2... match=True".
- Every envelope has ok true, meta.command equal to the verb, contains its own run path and does not contain the row's other path (diff-and-check.out).
- All six envelope sha256 values are distinct, so the counter's "envelope_sha256 shared with another run" check is satisfied.
- Carrier digests before the first call and after the last call are unchanged: 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 for both /usr/bin/tinyxxd and the renamed copy (carrier-sha256-before.txt, carrier-sha256-after.txt).
- Package version and package.json sha256 were read after each of the six calls; all six read 6.5.0 and a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunTxA/)

sha256 / path:

- 3f888cf0592d588454d81a5ab61ef1ff44d1001add1e943d3cf1480ac8137938 runs.tsv
- c8ca34fc8c43b231fcf7ad7d7693d5c806e96ae5acf5a50c4097f9095a42042b envelopes/tinyxxd-analyze-base.json
- 217003ac0c9ab25255ad4d1a6ee2ba212b26c3c36c1419c68fa41f497522c4a4 envelopes/tinyxxd-analyze-repeat.json
- 9da2571d92af2f5d8fa29536f11f9554c0d8970d7ca73187e5ff26bea168acbe envelopes/tinyxxd-analyze-renamed.json
- 8c30a1393f882206210ebcf77caaf65a24b19df3e862ea636f9502740d44a24a envelopes/tinyxxd-inspect-base.json
- 6ddc607df2fa56cf64301b2e31d96f79c95509c9edb0680906c9ae676587850d envelopes/tinyxxd-inspect-repeat.json
- aeece412cb635f25ab208f48cd12212014d9b64341529d66d856e6a2b991a629 envelopes/tinyxxd-inspect-renamed.json
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-analyze-base.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-analyze-repeat.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-analyze-renamed.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-inspect-base.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-inspect-repeat.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-inspect-renamed.stderr
- 4f19c2ea9fc3b4e778d80d17a79fd7652996dbca4c2ba1aa37e104742313d4fa run-tinyxxd.sh
- 522451f5c3f7605621fa753e8d272d7aee7c0745ed19d6372f01548a8be22c39 diff-and-check.py
- 411cf98a14c0d3216e613df6dfe23ceae65cf0abeb9e85ef7d4861effd9b69bd diff-and-check.out
- bd65a5fd7694eda54ae2e318d2152590b5bb4c215a9323a7072f2984acd65909 recompute-check.out
- d9a0db9cffc6ea08a97fd353733a6e32ac780e25083e33d171225625dd5a2e72 carrier-sha256-before.txt
- d9a0db9cffc6ea08a97fd353733a6e32ac780e25083e33d171225625dd5a2e72 carrier-sha256-after.txt (identical to the before receipt: both paths unchanged)
- 825d759336fa0a391d3b8cb76923988fe11e5c72bcdc954f16d1619739c1c876 artifacts-sha256.txt (sha256sum listing of the artifacts above)

## Integration notes for the L1

- The two table rows this seat supplies are: (tinyxxd, analyze, rename-sensitive, ev_89338dd2..., ev_89338dd2..., ev_65e0dbfb...) and (tinyxxd, inspect, rename-sensitive, ev_89338dd2..., ev_89338dd2..., ev_65e0dbfb...), subject_sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 in both.
- Envelope file names expected by the counter are corpus/evidence/round-27/c1/envelopes/tinyxxd-<verb>-<run>.json; this seat saved them as envelopes/tinyxxd-<verb>-<run>.json under the seat directory.
- No lane file was edited, no git or jj write was performed, no tool was installed or upgraded.

## Risks and blockers

- Blocker for the counter's "envelope sha256 unique" rule: none, all six are distinct.
- Observation worth a reviewer look: the id for tinyxxd is the same for analyze and for inspect, and the only rename-driven difference inside the hashed fields is the derived document name target-7b1e5d0c970a.bin versus target-7b1e5d0c970a.dat. If the L1 wants a separate claim about verb-discriminating ids, this data does not support it for tinyxxd.
- No blockers.
