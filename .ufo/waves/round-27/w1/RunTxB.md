# RunTxB — R27-C1 tinyxxd runs for verbs decompile and xrefs

Seat: RunTxB. Carrier: tinyxxd (/usr/bin/tinyxxd), sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, address 0x103d40.
Pin: rea-agents 6.5.0, package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c (equals the frozen value in claims.json).
Scope: only the two verbs decompile and xrefs, three runs each (base, repeat, renamed), six calls in total, all CLI, all run one after another. No other verb, no MCP device, no other file was analysed.

## runs.tsv

Written at /fast/scratch/hyaku/kaidoku-r27/seats/RunTxB/runs.tsv (sha256 9242fc73d8bdb8111742ea6b5101f9c3294b13b91ce6ea56232a301711335f9e). Header line, tab separated:

seat	carrier	verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256	pkg_version	pkg_json_sha256

Six data lines follow, in call order decompile/base, decompile/repeat, decompile/renamed, xrefs/base, xrefs/repeat, xrefs/renamed:

RunTxB	tinyxxd	decompile	base	/usr/bin/tinyxxd	decompile /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:21Z	2026-10-22T14:55:28Z	a436ac810d12b628ca947089bd325955e8ba17966be232cb98df763e1c290abc	ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxB	tinyxxd	decompile	repeat	/usr/bin/tinyxxd	decompile /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:33Z	2026-10-22T14:55:41Z	5aa8699e0b801afff2861a9d207ca6797e0e540e23c1358bd2da3022e925ffa9	ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxB	tinyxxd	decompile	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	decompile /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat 0x103d40 --format json --full-output	0	2026-10-22T14:55:41Z	2026-10-22T14:55:48Z	6b8244365179f3ec6ba7d2ca0bb38347b7a3e273c5bf34134a40a4aad849f929	ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxB	tinyxxd	xrefs	base	/usr/bin/tinyxxd	xrefs /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:48Z	2026-10-22T14:55:55Z	3b44dcc27fd39da8daec00459f73dc1fba19c995529634963ea54507b6fffa92	ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxB	tinyxxd	xrefs	repeat	/usr/bin/tinyxxd	xrefs /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:55Z	2026-10-22T14:56:01Z	73ec36a07b19e84824e4807237474bd097af51e56b551527d6e1cbdc340726f4	ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxB	tinyxxd	xrefs	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	xrefs /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat 0x103d40 --format json --full-output	0	2026-10-22T14:56:01Z	2026-10-22T14:56:08Z	d37850024cf07f44db62a049b699dce5d2b62b76d3332a32c7f6c8800689305e	ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

## Verdicts

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| decompile | ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422 | ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422 | ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422 | yes | yes | content-keyed |
| xrefs | ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a | ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a | ev_c9a0c962ea8cb74a0bf2c05b71bf6508e167970935de9e19e133a86ac054994a | yes | yes | content-keyed |

Verdict rule from claims.json applied literally: unstable if base != repeat; content-keyed if renamed == base; else rename-sensitive. Both verbs are content-keyed (observation, computed from the three ids above).

Note for the L1: the decompile id differs from the xrefs id, so the two verbs are distinct rows. Each verb's id is stable across all three runs, including the renamed copy, so the tinyxxd decompile and xrefs rows carry the same verdict kind as each other and differ from the analyze and inspect rows reported by RunTxA, which were rename-sensitive on the same carrier.

## Subject fields per run

- decompile/base, decompile/repeat, xrefs/base, xrefs/repeat: subject.name = tinyxxd, subject.local_path = /usr/bin/tinyxxd, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65.
- decompile/renamed, xrefs/renamed: subject.name = tinyxxd-r27-renamed.dat, subject.local_path = /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 (same bytes as the carrier).

## Rename-sensitive field differences (base vs renamed)

None, because neither verb is rename-sensitive. For completeness the same comparison was made anyway (script /fast/scratch/hyaku/kaidoku-r27/seats/RunTxB/diff-and-check.py, output diff-and-check.out). Over the seven hashed fields (.data.parameters, .data.raw_result, .data.normalized_result, .data.locations, .data.environment, .data.limitations, .data.evidence_links) compared leaf by leaf, base versus renamed gives 0 differing paths for every field, for both verbs:

    == hashed field diff decompile base vs renamed
       parameters differing_paths=0
       raw_result differing_paths=0
       normalized_result differing_paths=0
       locations differing_paths=0
       environment differing_paths=0
       limitations differing_paths=0
       evidence_links differing_paths=0
    == hashed field diff xrefs base vs renamed
       parameters differing_paths=0
       raw_result differing_paths=0
       normalized_result differing_paths=0
       locations differing_paths=0
       environment differing_paths=0
       limitations differing_paths=0
       evidence_links differing_paths=0

The only differences between the base and renamed envelopes anywhere in the envelope are the subject identity fields (.data.subject.name and .data.subject.local_path), which are outside the hashed projection. Between base and repeat the only difference in the whole envelope is meta.duration (decompile 6405ms vs 6963ms; xrefs 6243ms vs 6300ms), which is not hashed.

## Failures

None. All six calls exited 0. Every stderr file is empty (0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). No call was repeated to obtain a different result; base and repeat are two separate invocations, one after the other. No error text to report.

## Additional checks run by this seat (not part of the counter)

- Evidence id recompute under the 6.5.0 rule: tools/round-26/recompute-ids.py recomputed all six stored ids and matched all six, exit 0, "recomputed ids: 6 match of 6 total" (output recompute-check.out). Excerpt: "stored_id: ev_d4916c80d703d2503ac988428a2dc2e6c893838acf373b831ef2a0d9e8338422 / recomputed: ev_d4916c80... / path-bearing fields in the hashed projection: none".
- Every envelope has ok true, meta.command equal to the verb, contains its own run path and does not contain the row's other path, and subject.name equals the run file name (diff-and-check.out).
- All six envelope sha256 values are distinct, so the counter's "envelope_sha256 shared with another run" condition is satisfied.
- Carrier digests before the first call (2026-10-22T14:55:21Z) and after the last call (2026-10-22T14:56:36Z) are unchanged: 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 for both /usr/bin/tinyxxd and the renamed copy (carrier-hashes-before.txt, carrier-hashes-after.txt). The renamed copy was read only, never modified.
- Package version and package.json sha256 were read from /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json immediately after each of the six calls; all six reads returned 6.5.0 and a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c.
- All six utc_start values fall after the counter commit a4f674b (2026-10-22T14:51:23Z), as the counter requires.
- Exact command form used for every call: TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/RunTxB/tmp npx -y rea-agents@6.5.0 <argv>, stdout redirected to the envelope file, stderr to the .stderr file, run through /fast/scratch/hyaku/kaidoku-r27/seats/RunTxB/run-one.sh.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunTxB/)

sha256 / path:

- 9242fc73d8bdb8111742ea6b5101f9c3294b13b91ce6ea56232a301711335f9e  runs.tsv
- a436ac810d12b628ca947089bd325955e8ba17966be232cb98df763e1c290abc  envelopes/tinyxxd-decompile-base.json
- 5aa8699e0b801afff2861a9d207ca6797e0e540e23c1358bd2da3022e925ffa9  envelopes/tinyxxd-decompile-repeat.json
- 6b8244365179f3ec6ba7d2ca0bb38347b7a3e273c5bf34134a40a4aad849f929  envelopes/tinyxxd-decompile-renamed.json
- 3b44dcc27fd39da8daec00459f73dc1fba19c995529634963ea54507b6fffa92  envelopes/tinyxxd-xrefs-base.json
- 73ec36a07b19e84824e4807237474bd097af51e56b551527d6e1cbdc340726f4  envelopes/tinyxxd-xrefs-repeat.json
- d37850024cf07f44db62a049b699dce5d2b62b76d3332a32c7f6c8800689305e  envelopes/tinyxxd-xrefs-renamed.json
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-decompile-base.json.stderr (empty)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-decompile-repeat.json.stderr (empty)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-decompile-renamed.json.stderr (empty)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-xrefs-base.json.stderr (empty)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-xrefs-repeat.json.stderr (empty)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/tinyxxd-xrefs-renamed.json.stderr (empty)
- f1df6d10a277d010717930135fa770003eeb981dea2a4b0242bac720c999c1e4  carrier-hashes-before.txt
- 0aa02c1fef03fe245f2c6a6988accd6c95f0ff6c888964af8c5be8da870dfae6  carrier-hashes-after.txt
- c9f489dc7d4a4bd771fcad986972f07a6cd82787397f98dbc35428d127923d1a  diff-and-check.py
- 9c5dd95d48e6e4ac234710ae96574bfb42d3af0fdd331e2b1d2c4fe76bc3468d  diff-and-check.out
- a20de056cb2454c344bc7ce7dce4a8a0b7f7f205e607ffe872e566c3a4b07790  recompute-check.out
- 03994d7c466f8ac2749e93140acaddea113f1752cbf7f888aa959e1a354640c1  run-one.sh
- dbb5e0412f184e80fab927aa37ef8e208321cc0296295095e45bf49482dc42e9  meta/decompile-base.tsv
- 05c0b7609722c07557620e6848e83301f6b20884e79801190d566082388ee8f4  meta/decompile-repeat.tsv
- ab3c3523fdb39a0f780de224f1dc832590254a78dd98c794bacf45f9e17dd984  meta/decompile-renamed.tsv
- ed1ad1f5e42b647ce9c1efd864859b18cadf548eed22f990dffc9338c2ca50b2  meta/xrefs-base.tsv
- 2764c2f115b8e68e2c0cd80e9b904ad9e4e6e4efc05ddf72b8a7b127af58104d  meta/xrefs-repeat.tsv
- 94de3f6afd753020608673392f676f6276e530e46c90fb58348c924eeb18f695  meta/xrefs-renamed.tsv

The meta/*.tsv files are the per-call records written by run-one.sh before the ids were filled in; runs.tsv is the final table for this seat.

## Tooling

No package was installed or upgraded by this seat. The only tools used were the already present npx cache of rea-agents 6.5.0, sha256sum, python3 and date, all from the base system.

## Risks and blockers

- No blockers.
- Risk for the L1 (observation): the tinyxxd rows for decompile and xrefs are content-keyed while the analyze and inspect rows on the same carrier, reported by RunTxA, are rename-sensitive. The table must therefore carry mixed verdict kinds, and any narrative that says the tinyxxd carrier is uniformly rename-sensitive would be wrong. The difference comes from the hashed fields: the analyze and inspect envelopes carry a document name inside .data.normalized_result that changes with the file extension, while the decompile and xrefs envelopes carry no such name inside the hashed fields.
- Risk (observation): the two decompile runs and the two xrefs runs are identical apart from meta.duration, so the base and repeat rows differ only in that wall-clock field. That field is outside the hashed projection, which is why the ids match.
- The seat did not run the pinned counter against a commit; the envelope files still have to be committed by the L1 before the counter can score these rows, since the counter requires each envelope to be first committed after the counter commit a4f674b.
