# RunTxC — R27-C1 tinyxxd runs for verbs read-bytes and function

Seat: RunTxC. Carrier: tinyxxd (/usr/bin/tinyxxd), sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, address 0x103d40.
Pin: rea-agents 6.5.0, package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c (equal to the frozen value in claims.json).
Scope: only the two verbs read-bytes and function, three runs each (base, repeat, renamed). No other verb was run by this seat.
Renamed copy: /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat (read-only, untouched).

## runs.tsv

Written at /fast/scratch/hyaku/kaidoku-r27/seats/RunTxC/runs.tsv (sha256 ae7a6eccf6fcf6fbc48f17c935f72d87de6f94bacf843fb91283ef15aaf76354). Header line, tab separated:

seat	carrier	verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256	pkg_version	pkg_json_sha256

Six data lines follow, in run order read-bytes/base, read-bytes/repeat, read-bytes/renamed, function/base, function/repeat, function/renamed:

RunTxC	tinyxxd	read-bytes	base	/usr/bin/tinyxxd	read-bytes /usr/bin/tinyxxd 0x103d40 --length 64 --format json --full-output	0	2026-10-22T14:55:53Z	2026-10-22T14:56:00Z	1392c3cb03559f810a0ffcb7780f09886f71b10c177508db834b2c75a98fab27	ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxC	tinyxxd	read-bytes	repeat	/usr/bin/tinyxxd	read-bytes /usr/bin/tinyxxd 0x103d40 --length 64 --format json --full-output	0	2026-10-22T14:56:00Z	2026-10-22T14:56:07Z	b9fd2cfdb7b196c71e6c5fc434be5409ccda962214e3e32196ce127fde80a458	ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxC	tinyxxd	read-bytes	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	read-bytes /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat 0x103d40 --length 64 --format json --full-output	0	2026-10-22T14:56:07Z	2026-10-22T14:56:13Z	a09691350b22a4ae0d4f4c74b6e964bdde58e2559ada648c2732c44c94c3bf1a	ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxC	tinyxxd	function	base	/usr/bin/tinyxxd	function /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:56:13Z	2026-10-22T14:56:20Z	76caaa932a672ff204a7e59986b3d71e3b90e85ee9af202b86cd39a2f14cc7e8	ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxC	tinyxxd	function	repeat	/usr/bin/tinyxxd	function /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:56:20Z	2026-10-22T14:56:27Z	f4a4ec49ef6fcd15170aeefafda5b31e254c384cf29a1eb8e01c9ea1e4ca6872	ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxC	tinyxxd	function	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	function /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat 0x103d40 --format json --full-output	0	2026-10-22T14:56:27Z	2026-10-22T14:56:33Z	443457139ba91a78efa624a3d1111e422db7590e9610c4b250ab677bfba16fd4	ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

## Verdicts

Rule from claims.json applied literally: unstable if base != repeat; content-keyed if renamed == base; else rename-sensitive.

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| read-bytes | ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4 | ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4 | ev_239012fb89045fc4a7eae8d2e0090ec81b1566cc2fac47e8df359d529223d6f4 | yes | yes | content-keyed |
| function | ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc | ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc | ev_8af5c38f4d264e35f3f746fd53b35a4166350d1cdab0bfa2328b431fd0e001fc | yes | yes | content-keyed |

Both verdicts are observations computed from the three ids above, not inferences. The function base id equals the id recorded in claims.json pre_freeze_probe (ev_8af5c38f...), so the same call at the same pin is reproducible across the probe and this table run.

## Subject fields per run

- read-bytes/base, read-bytes/repeat, function/base, function/repeat: subject.name = tinyxxd, subject.local_path = /usr/bin/tinyxxd, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65.
- read-bytes/renamed, function/renamed: subject.name = tinyxxd-r27-renamed.dat, subject.local_path = /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 (same bytes as the carrier).

## Rename-sensitive field differences (base vs renamed)

No verb of this seat is rename-sensitive, so no hashed-field difference list is required. For completeness, the diff was still run (diff-and-check.out, produced by diff_and_check.py) over the seven hashed fields (.data.parameters, .data.raw_result, .data.normalized_result, .data.locations, .data.environment, .data.limitations, .data.evidence_links), leaf by leaf:

- read-bytes: parameters, raw_result, normalized_result, locations, environment, limitations, evidence_links all 0 differing leaf paths between base and renamed.
- function: parameters, raw_result, normalized_result, locations, environment, limitations, evidence_links all 0 differing leaf paths between base and renamed.

Only two leaves differ anywhere in .data between base and renamed, and both sit outside the hashed projection (the 6.5.0 projection keeps only subject.digest, subject.format, subject.architecture from the subject):

- .data.subject.local_path — base: "/usr/bin/tinyxxd" ; renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat"
- .data.subject.name — base: "tinyxxd" ; renamed: "tinyxxd-r27-renamed.dat"

Why the ids do not move (observation from the envelopes): read-bytes returns .data.normalized_result with keys address, requested_bytes, returned_bytes, bytes_hex, complete and function returns procedure, pseudocode, assembly, callers, callees and related keys; neither carries a derived document or file name, so the rename changes nothing that the 6.5.0 semantic projection hashes. By contrast the analyze and inspect verbs on this carrier were reported by seat RunTxA as rename-sensitive because their .data.normalized_result.document carries a derived name whose extension follows the renamed file. This seat's data therefore supports the pattern "rename-sensitivity is a property of the verb's result shape, not of the carrier", but that pattern is an inference from two seats and is not claimed here.

Base versus repeat, whole envelope: exactly one leaf differs for each verb, /meta/duration (read-bytes base "6403ms" vs repeat "6355ms"; function base "6024ms" vs repeat "6236ms"). The evidence id is unchanged, so the verdict is stable under the claims.json rule.

## Failures

None. All six calls exited 0 and every stderr file is empty (0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). No call was repeated to obtain a different result; base and repeat are two separate invocations run one after the other, in the order read-bytes then function.

## Additional checks run by this seat (not part of the counter)

- Evidence id recompute under the 6.5.0 rule: `python3 -I -B tools/round-26/recompute-ids.py --verbose <six envelopes>` recomputed all six stored ids and matched all six. Output excerpt (recompute-check.out): "recomputed ids: 6 match of 6 total", exit 0.
- Every envelope has ok true, meta.command equal to the verb, contains its own run path and does not contain the row's other path (diff-and-check.out: "contains own path=True contains other path=False" for all six).
- All six envelope sha256 values are distinct, so the counter's "envelope sha256 shared with another run" check is satisfied.
- Carrier digests before the first call (2026-10-22T14:55:09Z) and after the last call (2026-10-22T14:57:40Z) are unchanged and equal: 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 for both /usr/bin/tinyxxd and the renamed copy (carrier-sha256-before.txt, carrier-sha256-after.txt).
- Package version and package.json sha256 were read after each of the six calls; all six read version 6.5.0 and sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c.
- The pre-run `--help` and post-run recompute used the pinned package only; no other tool was installed or upgraded.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunTxC/)

sha256 / path:

- ae7a6eccf6fcf6fbc48f17c935f72d87de6f94bacf843fb91283ef15aaf76354 runs.tsv
- 1392c3cb03559f810a0ffcb7780f09886f71b10c177508db834b2c75a98fab27 envelopes/tinyxxd-read-bytes-base.json
- b9fd2cfdb7b196c71e6c5fc434be5409ccda962214e3e32196ce127fde80a458 envelopes/tinyxxd-read-bytes-repeat.json
- a09691350b22a4ae0d4f4c74b6e964bdde58e2559ada648c2732c44c94c3bf1a envelopes/tinyxxd-read-bytes-renamed.json
- 76caaa932a672ff204a7e59986b3d71e3b90e85ee9af202b86cd39a2f14cc7e8 envelopes/tinyxxd-function-base.json
- f4a4ec49ef6fcd15170aeefafda5b31e254c384cf29a1eb8e01c9ea1e4ca6872 envelopes/tinyxxd-function-repeat.json
- 443457139ba91a78efa624a3d1111e422db7590e9610c4b250ab677bfba16fd4 envelopes/tinyxxd-function-renamed.json
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-read-bytes-base.json.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-read-bytes-repeat.json.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-read-bytes-renamed.json.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-function-base.json.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-function-repeat.json.stderr
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/tinyxxd-function-renamed.json.stderr
- 1c2f0754d3d45aad0e85b2144526d94d6b4572fa5ea741b39b4b1da511f79d54 run_calls.py (the driver that made the six calls)
- 7d244546b2db219fe4be48cd96bdd34db86cd71c276f8fc36a1a50dd3ff10d9e diff_and_check.py
- 1334cd5a13732354453b652368469957ac7cc18582d4fef113d012c5b183a929 diff-and-check.out
- 524ef12a715162cdaa66808e135506c390e5d8bc184de54ebfe8d9df698b1943 recompute-check.out
- 84f35feb458f276dda0e769a696c8e4c1f592027f90b34d2fff0e3d23325f3c6 carrier-sha256-before.txt
- b852a594ebcb6bfc91a8f8e451611e13636efacac85a3de1d27739675d725e24 carrier-sha256-after.txt
- 4e58fe39e4719fd9851131d517b7e9c0a16beac85fc74127fd2a04087af5ed23 artifacts-sha256.txt (sha256sum listing of the 19 files above; it does not list itself)
- tmp/ holds only the Node compile cache created by npx during the six calls; it is scratch, not evidence, and is not hashed here.

## Integration notes for the L1

- The two table rows this seat supplies are: (tinyxxd, read-bytes, content-keyed, ev_239012fb..., ev_239012fb..., ev_239012fb...) and (tinyxxd, function, content-keyed, ev_8af5c38f..., ev_8af5c38f..., ev_8af5c38f...), subject_sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 in both.
- Envelope file names expected by the counter are corpus/evidence/round-27/c1/envelopes/tinyxxd-<verb>-<run>.json; this seat saved them as envelopes/tinyxxd-<verb>-<run>.json under the seat directory. The stderr sidecars are named <envelope>.json.stderr here, because the card named the stdout file with the .json suffix.
- The runs.tsv lines carry the argv string without the npx prefix, as the card requires, and each argv matches the claims.json verbs_argv template with <PATH> and <ADDR> substituted.
- No lane file was edited apart from this report, no git or jj write was performed, no tool was installed or upgraded.

## Risks and blockers

- No blockers.
- Risk for the reviewer: the two verdicts here are content-keyed while the analyze and inspect rows of the same carrier are rename-sensitive (seat RunTxA). If the round-27 lesson states a rule of the form "renaming changes the id", it must not be written from the analyze and inspect rows alone; the read-bytes and function rows show the opposite for two of the eight verbs.
- Risk for the counter: this seat's envelopes are not committed, so the counter's "envelope first committed after the counter commit" check depends on the L1 committing them in this wave.
