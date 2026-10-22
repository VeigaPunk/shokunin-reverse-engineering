# RunJqA — R27-C1 carrier jq, verbs analyze and inspect

Seat RunJqA. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin (read-only for this seat).
Claim source .ufo/waves/round-27/claims.json (sha256 ff45e9ce64b417f11bea12884feb26499d30ce30766bec674f9f0d03a37662b2). Counter tools/round-27/c1-rename-identity.py (pinned sha256 e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7). Package pin rea-agents 6.5.0, package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c.

All six REA calls exited 0. No call failed and no call was re-run.

## Carrier integrity

`sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat` before the first call (2026-10-22T14:55:12Z) and after the last (2026-10-22T14:58:42Z) — identical both times, and equal to the frozen carrier sha256:

    e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
    e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat

Observation: both carriers stayed byte-identical and unmodified.

## Invocation

Each call: `TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/RunJqA/tmp npx -y rea-agents@6.5.0 <verb> <PATH> --format json --full-output`, run one at a time, never in parallel. Seat driver `run.sh` wrote stdout to `envelopes/jq-<verb>-<run>.json`, stderr to `envelopes/jq-<verb>-<run>.stderr`, and one runs.tsv line per call. Address from claims.json `carriers.jq.address` = 0x103fa0; neither verb takes an address, so it appears in no argv.

## runs.tsv content

/fast/scratch/hyaku/kaidoku-r27/seats/RunJqA/runs.tsv — 7 lines, 1 header + 6 rows. Header columns are exactly the frozen set: seat, carrier, verb, run, path, argv, exit, utc_start, utc_end, envelope_sha256, evidence_id, subject_sha256, pkg_version, pkg_json_sha256.

    RunJqA	jq	analyze	base	/usr/bin/jq	analyze /usr/bin/jq --format json --full-output	0	2026-10-22T14:55:42Z	2026-10-22T14:55:48Z	361365bcb96846c9e4bf55cb0c7b34204289fb8f559fe4eeafe3bf178617344f	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
    RunJqA	jq	analyze	repeat	/usr/bin/jq	analyze /usr/bin/jq --format json --full-output	0	2026-10-22T14:55:52Z	2026-10-22T14:55:58Z	c2b466d17b73dbd31130077add8a3b8b2e15dac95eeee0438eee41b84b7489f7	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
    RunJqA	jq	analyze	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	analyze /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat --format json --full-output	0	2026-10-22T14:56:10Z	2026-10-22T14:56:16Z	77747b24d488ca521fb4d36a02cc39ab619412bfe8db0689cec3dc971cb854e9	ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
    RunJqA	jq	inspect	base	/usr/bin/jq	inspect /usr/bin/jq --format json --full-output	0	2026-10-22T14:56:19Z	2026-10-22T14:56:24Z	e2ffb5f6cb000fdc787cfe7c491505260941b7468f4608f66374d535247c6560	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
    RunJqA	jq	inspect	repeat	/usr/bin/jq	inspect /usr/bin/jq --format json --full-output	0	2026-10-22T14:56:29Z	2026-10-22T14:56:34Z	e735720c28e26d2ef36f52c1373cba766488c99e8f7b451775bfb12dad1f192f	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
    RunJqA	jq	inspect	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	inspect /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat --format json --full-output	0	2026-10-22T14:56:37Z	2026-10-22T14:56:43Z	fbd02368513a538a5edab930aed8ec83dcb86e6467df425ed70ae408ee74eb06	ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

Note for the integrator: the counter requires every envelope_sha256 to be unique across runs.tsv. These six are unique. Base and repeat differ in bytes only through meta.duration, so the two same-path envelopes have different sha256 but the same evidence_id.

## Per-verb ids, equality, verdict

Rule from claims.json as coded in the pinned counter: unstable if base != repeat; content-keyed if renamed == base; otherwise rename-sensitive.

    verb analyze: base   ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328
                  repeat ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328
                  renamed ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2
                  base == repeat yes; base == renamed no; verdict rename-sensitive

    verb inspect: base   ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328
                  repeat ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328
                  renamed ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2
                  base == repeat yes; base == renamed no; verdict rename-sensitive

Observation, not part of the claim: at 6.5.0 analyze and inspect on jq produce byte-identical `data` payloads (the two data objects compare equal), so both verbs share one id per path; only meta.command and meta.duration differ. The claim counts per (carrier, verb) row, so no verdict changes, but the two jq table rows will carry the same three ids.

## .data.subject.name and .data.subject.local_path per run

    jq analyze base     name=jq                   local_path=/usr/bin/jq
    jq analyze repeat   name=jq                   local_path=/usr/bin/jq
    jq analyze renamed  name=jq-r27-renamed.dat   local_path=/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat
    jq inspect base     name=jq                   local_path=/usr/bin/jq
    jq inspect repeat   name=jq                   local_path=/usr/bin/jq
    jq inspect renamed  name=jq-r27-renamed.dat   local_path=/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat

Observation: subject.name equals the run path's file name in every envelope, as the counter requires. The renamed envelopes contain the renamed path and not /usr/bin/jq; the base and repeat envelopes contain /usr/bin/jq and not the renamed path.

## Rename-sensitive verbs: differing JSON paths inside the hashed fields

Both jq verbs are rename-sensitive, so base and renamed were compared field by field over the hashed set named in the claim (parameters, raw_result, normalized_result, locations, environment, limitations, evidence_links) and over the remaining projection fields. Command: a Python walk over the saved JSON comparing flattened values base vs renamed, per field.

    verb analyze: parameters identical; raw_result identical (both null); locations identical (both []);
                 environment identical; limitations identical; evidence_links identical;
                 normalized_result: 1 differing key -> data.normalized_result.document
                     base    "target-e815667571d0.bin"
                     renamed "target-e815667571d0.dat"
    verb inspect: parameters identical; raw_result identical (both null); locations identical (both []);
                 environment identical; limitations identical; evidence_links identical;
                 normalized_result: 1 differing key -> data.normalized_result.document
                     base    "target-e815667571d0.bin"
                     renamed "target-e815667571d0.dat"

Outside the hashed set the only base-versus-renamed differences are the display fields data.subject.local_path and data.subject.name (values above). provider, analysis_profile, predicate_type, operation, confidence, authority and relationship_coverage are identical.

Mechanism, inference from installed package source, consistent with the observation: the Ghidra snapshot name is built in dist/ghidra/GhidraTargetSnapshot.js:76-79, where safeExtension(path) returns the file extension when it matches /^\.[A-Za-z0-9]{1,12}$/u and ".bin" otherwise. /usr/bin/jq has no extension so it becomes .bin; jq-r27-renamed.dat keeps .dat. That name lands in normalized_result.document, which is inside the hashed projection (dist/domain/evidence.js:156-180), so the id changes. The label rename-sensitive therefore reflects extension-driven naming inside the hashed payload rather than the file name or directory. Marked inference: the code path was read, not executed.

## Failures

None. All six calls exited 0 and every stderr file is empty (0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, the hash of the empty string).

## Independent id recompute (cross-check, read-only use of the lane script)

`python3 -I -B tools/round-26/recompute-ids.py --dir /fast/scratch/hyaku/kaidoku-r27/seats/RunJqA/envelopes`, exit 0. Output excerpt:

    recomputed ids: 6 match of 6 total
    stored_id   : ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328   (analyze base)
    recomputed  : ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328
    stored_id   : ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2   (analyze renamed)
    recomputed  : ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2

Observation: all six stored ids recompute under the 6.5.0 rule. The tool reported "path-bearing fields in the hashed projection: none" for every envelope, consistent with the differing field being a derived snapshot name rather than a path.

## Artifacts, all under /fast/scratch/hyaku/kaidoku-r27/seats/RunJqA/

    5afc78eb2a22b18dabe7a71038fc5c29d03634f8c7dfaa69e089e58a0212a9e9  run.sh
    b94a74c5d451a827881e07fc2c193057ea0d416506fd6d318906c2c90acd24e3  runs.tsv
    361365bcb96846c9e4bf55cb0c7b34204289fb8f559fe4eeafe3bf178617344f  envelopes/jq-analyze-base.json
    c2b466d17b73dbd31130077add8a3b8b2e15dac95eeee0438eee41b84b7489f7  envelopes/jq-analyze-repeat.json
    77747b24d488ca521fb4d36a02cc39ab619412bfe8db0689cec3dc971cb854e9  envelopes/jq-analyze-renamed.json
    e2ffb5f6cb000fdc787cfe7c491505260941b7468f4608f66374d535247c6560  envelopes/jq-inspect-base.json
    e735720c28e26d2ef36f52c1373cba766488c99e8f7b451775bfb12dad1f192f  envelopes/jq-inspect-repeat.json
    fbd02368513a538a5edab930aed8ec83dcb86e6467df425ed70ae408ee74eb06  envelopes/jq-inspect-renamed.json
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-analyze-base.stderr
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-analyze-repeat.stderr
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-analyze-renamed.stderr
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-inspect-base.stderr
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-inspect-repeat.stderr
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/jq-inspect-renamed.stderr

## Bounds, risks, open items

- No lane file was edited. The only file written inside the lane is this report at .ufo/waves/round-27/w1/RunJqA.md. No git add, commit, checkout, reset, stash, switch, pull or push was run in the lane; no jj command was run at the fleet root; this seat committed and updated no ref anywhere. Read-only git used: git log, git status --porcelain.
- The renamed carrier was read only, never modified; sha256 unchanged before and after.
- Tooling: no install or upgrade was needed. npx 11.19.0, node v24.21.0 and the cached rea-agents 6.5.0 under /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6 were used as-is, and that package.json sha256 matched the frozen pin on every run.
- Integration risk: the counter expects the jq envelopes at corpus/evidence/round-27/c1/envelopes/jq-<verb>-<run>.json and the rows in corpus/evidence/round-27/c1/runs.tsv. This seat wrote them under its scratch directory only; integration and committing are the L1's work.
- Timing risk: the counter requires every utc_start to fall after the counter's own commit time (2026-10-22T14:51:23Z for a4f674b3). All six utc_start values are later, from 2026-10-22T14:55:42Z.
- Open item for the L1: the two jq rows (analyze, inspect) hold the same three ids because the two verbs yield identical hashed payloads on this carrier. Any verdict counts under the claim, so this is not a defect, but the table cells will look duplicated.
