# RunTxD — R27-C1 tinyxxd runs for verbs instructions and inspect-binary-layout

Seat: RunTxD. Carrier: tinyxxd (/usr/bin/tinyxxd), sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, address 0x103d40.
Pin: rea-agents 6.5.0, package.json version 6.5.0, sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c (equal to the frozen value in claims.json). The package.json was read after every call; all seven reads returned version 6.5.0 and that sha256.
Scope: only the two verbs instructions and inspect-binary-layout, three runs each (base, repeat, renamed), six calls, all CLI, run one after another. No other verb was run by this seat.
Renamed copy /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat, read only, untouched. Carrier digests before the first call and after the last call are unchanged for both paths (carrier-sha256-before.txt and carrier-sha256-after.txt are identical, sha256 b329ea6dfe9c4fd47f493f321e6b6220bc3577da2237fd90e7ee5262163634c9).

## runs.tsv

Written at /fast/scratch/hyaku/kaidoku-r27/seats/RunTxD/runs.tsv (sha256 013cd311db48d600c001c26134438a0a3a74d93d3d78806f06a0f8928243bfc6). Header line, tab separated:

seat	carrier	verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256	pkg_version	pkg_json_sha256

Six data lines follow, in run order instructions/base, instructions/repeat, instructions/renamed, inspect-binary-layout/base, inspect-binary-layout/repeat, inspect-binary-layout/renamed:

RunTxD	tinyxxd	instructions	base	/usr/bin/tinyxxd	instructions /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:28Z	2026-10-22T14:55:35Z	c10c7f3ec8d60b57581b7a41a48cc3d1320e45e3b837ea7b1416c5a60801ec6c	ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxD	tinyxxd	instructions	repeat	/usr/bin/tinyxxd	instructions /usr/bin/tinyxxd 0x103d40 --format json --full-output	0	2026-10-22T14:55:35Z	2026-10-22T14:55:42Z	d2d48d05f3029285d77c1353a2d566bd344cb7e87f41fee9206a40f6e13dfb50	ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxD	tinyxxd	instructions	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	instructions /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat 0x103d40 --format json --full-output	0	2026-10-22T14:55:42Z	2026-10-22T14:55:49Z	140460a2fe567bd2308a9a112e15e3569e0e1b330cd76d2688634dc2857acbc9	ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxD	tinyxxd	inspect-binary-layout	base	/usr/bin/tinyxxd	inspect-binary-layout /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:55:49Z	2026-10-22T14:55:50Z	f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130	ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxD	tinyxxd	inspect-binary-layout	repeat	/usr/bin/tinyxxd	inspect-binary-layout /usr/bin/tinyxxd --format json --full-output	0	2026-10-22T14:55:50Z	2026-10-22T14:55:51Z	f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130	ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunTxD	tinyxxd	inspect-binary-layout	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat	inspect-binary-layout /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat --format json --full-output	0	2026-10-22T14:55:51Z	2026-10-22T14:55:51Z	bbfbc309da6016f5ab0ffc21a4f624db9cf74f5ab7cfe923e24b23c12f9e929c	ev_02e910c6b112a96422a5d93a29285de131aea2dcd3a8c758c5e99c1750f21891	7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

## Verdicts

Rule from claims.json applied literally: unstable if base != repeat; content-keyed if renamed == base; else rename-sensitive. The three ids above are read straight from .data.evidence_id of the three envelopes of that verb (observation, not inference).

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| instructions | ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739 | ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739 | ev_7ab9b9e874cd269fa0907f5da308b6e864b588c85906353f0f9d0869d89c8739 | yes | yes | content-keyed |
| inspect-binary-layout | ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6 | ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6 | ev_02e910c6b112a96422a5d93a29285de131aea2dcd3a8c758c5e99c1750f21891 | yes | no | rename-sensitive |

## Subject fields per run

- instructions/base, instructions/repeat, inspect-binary-layout/base, inspect-binary-layout/repeat: subject.name = tinyxxd, subject.local_path = /usr/bin/tinyxxd, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, subject.format = elf, subject.architecture = x86_64.
- instructions/renamed, inspect-binary-layout/renamed: subject.name = tinyxxd-r27-renamed.dat, subject.local_path = /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat, subject.digest.sha256 = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 (same bytes as the carrier), subject.format = elf, subject.architecture = x86_64.

## Rename-sensitive field differences (base vs renamed)

Diff script /fast/scratch/hyaku/kaidoku-r27/seats/RunTxD/diff-and-check.py, output diff-and-check.out. It compares the seven hashed fields (.data.parameters, .data.raw_result, .data.normalized_result, .data.locations, .data.environment, .data.limitations, .data.evidence_links) leaf by leaf.

For instructions (content-keyed) all seven hashed fields are identical between base and renamed: parameters 1 leaf, raw_result 29 leaves, normalized_result 29 leaves, locations 0 leaves, environment 1 leaf, limitations 6 leaves, evidence_links 0 leaves. The instructions verb hashes no path: parameters is {"procedure": "0x103d40"} in both runs, locations is empty in both, and the 6.5.0 projection carries subject.digest, subject.format and subject.architecture but not subject.name or subject.local_path.

For inspect-binary-layout (rename-sensitive) three hashed leaves differ, all of them the run path:

- .data.parameters.path — base: "/usr/bin/tinyxxd" ; renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat"
- .data.normalized_result.artifact.path — base: "/usr/bin/tinyxxd" ; renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat"
- .data.locations[0].path — base: "/usr/bin/tinyxxd" ; renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat"

raw_result (1 leaf), environment (1 leaf), limitations (12 leaves) and evidence_links (0 leaves) are byte-for-byte equal between base and renamed. Two further differences sit outside the seven hashed fields: .data.subject.name ("tinyxxd" versus "tinyxxd-r27-renamed.dat") and .data.subject.local_path. The recompute tool confirms the path-bearing fields inside the hashed projection are exactly /parameters/path, /normalized_result/artifact/path and /locations/0.path, and that the interpreters display path /lib64/ld-linux-x86-64.so.2 is identical in both. The rename changes the id through those three path strings alone.

## Failures

None of the six required calls failed. Every one exited 0 and every stderr file is empty (0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). No required call was re-run to obtain a different result; base and repeat are two separate invocations, one after the other.

One counter-level failure does exist, and it is the main finding of this seat.

## Main finding: inspect-binary-layout base and repeat envelopes are byte-identical

The base and repeat envelopes for inspect-binary-layout have the same sha256 f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130 and are byte-for-byte equal (51287 bytes, zero differing byte offsets). The counter requires every run's envelope sha256 to be unique across runs.tsv, so this row fails.

Sandbox clone of the lane at /fast/scratch/hyaku/kaidoku-r27/seats/RunTxD/clone (now deleted), with this seat's six envelopes, runs.tsv and the two table rows committed. Command: python3 -I -B tools/round-27/c1-rename-identity.py --root . --rev HEAD. Output excerpt (counter-sandbox.out):

    INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run
    COMPLETE tinyxxd instructions
    rows_complete=1/16 entry_ok=0 rev=8c2e2590c7cf7c21036549913260f4f4ed891968

Cause, established by byte comparison (duration-collision-proof.out): the only volatile byte in the whole envelope is meta.duration, and the two runs reported the same duration. Base meta {"command": "inspect-binary-layout", "duration": "132ms"}; repeat meta identical; renamed meta duration "128ms". The string "duration":"132ms" occurs exactly once in the envelope. Replacing only that one byte (offset 51280) with "133ms" changes the file sha256 to 985501be99f70ead0522a4944a6a1c43fe836ea2019e6ed58b0901b2c71ab3cb while the evidence_id stays ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6 and still recomputes under the 6.5.0 rule. meta.duration is not part of the hashed projection, so this byte cannot change the evidence id.

This is a property of the carrier and the verb, not of the run method: for the same verb on the jq carrier the sibling seat RunJqD got three distinct durations (143ms, 144ms, 138ms) and three distinct sha256 values, while tinyxxd inspect-binary-layout is fast enough that two consecutive runs tie. A scan across all 50 run rows of the six sibling seats plus this one shows exactly one shared envelope sha256, and it is this seat's pair.

Extra invocation (unused; L1 decision). One additional invocation of the same command was made (base path, exit 0, utc 2026-10-22T15:09:45Z to 15:09:46Z, envelope sha256 81a069abb9c70a860d7faa63d53e6cc90d6982d7c53752b0364520f13dc1285e, meta duration 171ms, evidence_id ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6, that is the same id as base and repeat). It is saved as envelopes/tinyxxd-inspect-binary-layout-base-extra.json and described by one line in runs-extra.tsv. It is additive and changes nothing already measured. In a sandbox clone, using its bytes as the inspect-binary-layout repeat envelope made the row pass the counter (counter-sandbox-remedy.out):

## Additional checks run by this seat (not part of the counter)

- Evidence id recompute under the 6.5.0 rule: tools/round-26/recompute-ids.py recomputed all six stored ids and matched all six. Output excerpt (recompute-check.out): "recomputed ids: 6 match of 6 total".
- Every envelope has ok true, meta.command equal to the verb, contains its own run path and does not contain the row's other path (diff-and-check.out).
- The instructions envelopes are not byte-identical to each other: base meta duration 6817ms, repeat meta duration 6288ms, distinct sha256 values.
## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunTxD/)

sha256 / path:

- 013cd311db48d600c001c26134438a0a3a74d93d3d78806f06a0f8928243bfc6 runs.tsv
- 83ab74833aa4fd495943952243559d8929646272b7bc8ee09f6d3ed2fbde4998 runs-extra.tsv
- c10c7f3ec8d60b57581b7a41a48cc3d1320e45e3b837ea7b1416c5a60801ec6c envelopes/tinyxxd-instructions-base.json
- d2d48d05f3029285d77c1353a2d566bd344cb7e87f41fee9206a40f6e13dfb50 envelopes/tinyxxd-instructions-repeat.json
- 140460a2fe567bd2308a9a112e15e3569e0e1b330cd76d2688634dc2857acbc9 envelopes/tinyxxd-instructions-renamed.json
- f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130 envelopes/tinyxxd-inspect-binary-layout-base.json
- f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130 envelopes/tinyxxd-inspect-binary-layout-repeat.json (same bytes as base, see the main finding)
- bbfbc309da6016f5ab0ffc21a4f624db9cf74f5ab7cfe923e24b23c12f9e929c envelopes/tinyxxd-inspect-binary-layout-renamed.json
- 81a069abb9c70a860d7faa63d53e6cc90d6982d7c53752b0364520f13dc1285e envelopes/tinyxxd-inspect-binary-layout-base-extra.json (the additional invocation, additive)
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 envelopes/*.json.stderr (all seven, empty)
- c606ffd10b5870af906f9016a33c4f17644e1cb56c198c9fc4f473cde36d8e34 run-tinyxxd.sh
- 4f43f82d484803fb8c8fcc431fbf5975e32d728cd1eec617ccd5eac3a1343d0d diff-and-check.py
- 0b93012d532dba573190d0c83fa2b96f86d8a292569daf79fc444d3642869d2e diff-and-check.out
- 378438ba5e6800bba02fe9cf3b6f870d56867425309a7f3456637d12071f644f recompute-check.out
- 7bb5f53710940acb895da81fb1407a5346f83ca1614a6f39217e8b849f1ed088 duration-collision-proof.out
- 06e7580ff49dd91f40789afd5a8bd25cb0ddc90e1c731007e60663d33cf5bc05 counter-sandbox.out
- 3fb6778238ec08f09e059f28dddfe3b140c25338049a875701f6ad1f68fd834d counter-sandbox-remedy.out
- 81a069abb9c70a860d7faa63d53e6cc90d6982d7c53752b0364520f13dc1285e envelopes/tinyxxd-inspect-binary-layout-base-extra.json (additional invocation; unused, L1 decision)
- b329ea6dfe9c4fd47f493f321e6b6220bc3577da2237fd90e7ee5262163634c9 carrier-sha256-after.txt (identical to the before receipt: both paths unchanged)
## Integration notes for the L1

- The two table rows this seat supplies are: (tinyxxd, instructions, content-keyed, ev_7ab9b9e8..., ev_7ab9b9e8..., ev_7ab9b9e8...) and (tinyxxd, inspect-binary-layout, rename-sensitive, ev_aeeab0db..., ev_aeeab0db..., ev_02e910c6...), subject_sha256 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 in both.
- The instructions row passes the counter as measured (COMPLETE in the sandbox).
- L1 decision (2026-10-22): the original repeat envelope is kept; the extra run is not substituted. The inspect-binary-layout row stays INCOMPLETE under the frozen counter with reason "envelope_sha256 shared with another run", so R27-C1 is a 15 of 16 miss. The extra run is unused.
- Envelope file names expected by the counter are corpus/evidence/round-27/c1/envelopes/tinyxxd-<verb>-<run>.json; this seat saved them as envelopes/tinyxxd-<verb>-<run>.json under the seat directory.
- No lane file was edited except this report, no git or jj write was performed, no tool was installed or upgraded, and no host service was restarted. The lane working tree shows PROVINCE.md and corpus/QUALITY.md modified, which is not this seat's work.
## Risks and blockers
- Observation worth a reviewer look: meta.duration is the only volatile field in a rea-agents 6.5.0 envelope and it is outside the hashed projection, so the counter's uniqueness rule on envelope sha256 can be defeated by a fast verb whose two runs report the same duration. This is a property of the instrument, not of any one seat, and the jq carrier happened not to hit it.
- Observation: the instructions verb hashes no path at all, so its id is content-keyed by construction for any rename; the inspect-binary-layout verb puts the path into parameters, normalized_result.artifact and locations, so its id is rename-sensitive by construction.
