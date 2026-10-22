# RunJqD — R27-C1 table runs on carrier jq (/usr/bin/jq)

Seat: RunJqD. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (read-only for this seat).
Scratch: /fast/scratch/hyaku/kaidoku-r27/seats/RunJqD/
Verbs (claims.json order): instructions, inspect-binary-layout.
Carrier jq: base /usr/bin/jq, renamed /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat, address 0x103fa0.

## Summary

Six REA calls, all exit 0, no failures. Two table rows complete.

- instructions: base id == repeat id == renamed id → verdict **content-keyed**.
- inspect-binary-layout: base id == repeat id, renamed id differs → verdict **rename-sensitive**.

## runs.tsv content

Path: /fast/scratch/hyaku/kaidoku-r27/seats/RunJqD/runs.tsv (sha256 d12b22924fda0ac774a0947aa5cf0cd7576d052debb1320b413b90948c875e88).
Header (tab separated): seat carrier verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256 pkg_version pkg_json_sha256

RunJqD	jq	instructions	base	/usr/bin/jq	instructions /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:19Z	2026-10-22T14:55:25Z	bc3193082694394221041b49de5d78b65c0c45b44e3a2ca811da828116d4adcd	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqD	jq	instructions	repeat	/usr/bin/jq	instructions /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:25Z	2026-10-22T14:55:30Z	32c263e1521175dd29049344886e207fb8bec278457e49884a0b1e4ffc195b01	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqD	jq	instructions	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	instructions /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat 0x103fa0 --format json --full-output	0	2026-10-22T14:55:31Z	2026-10-22T14:55:36Z	29920103401287c054dd3b999bc3613ad8f420be0efead35ee1b40bc1b3a2332	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqD	jq	inspect-binary-layout	base	/usr/bin/jq	inspect-binary-layout /usr/bin/jq --format json --full-output	0	2026-10-22T14:55:36Z	2026-10-22T14:55:37Z	dfd4990be733af751b594cf155630e5caf8f634eb52cf39bfc61cd4c29ab7e5d	ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqD	jq	inspect-binary-layout	repeat	/usr/bin/jq	inspect-binary-layout /usr/bin/jq --format json --full-output	0	2026-10-22T14:55:37Z	2026-10-22T14:55:38Z	6b85eb5bcc75ced0abe175f2216b7c0f31069a13cb87ba11db9e0c6e3e2ba947	ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqD	jq	inspect-binary-layout	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	inspect-binary-layout /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat --format json --full-output	0	2026-10-22T14:55:38Z	2026-10-22T14:55:39Z	0621c8de2d2d662bbe4d6d02fbd43922a9b96c968ac63fcd34ea6d079bb51ae7	ev_43dec6e6a261a6c3ea6dc02cc889337d653d16f0d7d37c78051cd4a2378e45c6	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c

## Per verb verdicts (claims.json rule: unstable if base != repeat, content-keyed if renamed == base, else rename-sensitive)

instructions
- base id: ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b
- repeat id: ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b
- renamed id: ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b
- base == repeat: yes. base == renamed: yes. Verdict: content-keyed.

inspect-binary-layout
- base id: ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd
- repeat id: ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd
- renamed id: ev_43dec6e6a261a6c3ea6dc02cc889337d653d16f0d7d37c78051cd4a2378e45c6
- base == repeat: yes. base == renamed: no. Verdict: rename-sensitive.

## Subject fields per run

- instructions base: subject.name = "jq", subject.local_path = "/usr/bin/jq"
- instructions repeat: subject.name = "jq", subject.local_path = "/usr/bin/jq"
- instructions renamed: subject.name = "jq-r27-renamed.dat", subject.local_path = "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat"
- inspect-binary-layout base: subject.name = "jq", subject.local_path = "/usr/bin/jq"
- inspect-binary-layout repeat: subject.name = "jq", subject.local_path = "/usr/bin/jq"
- inspect-binary-layout renamed: subject.name = "jq-r27-renamed.dat", subject.local_path = "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat"

All six runs: subject.digest.sha256 = e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 (the jq carrier bytes, equal for both paths).

## Differing JSON paths for the rename-sensitive verb (inspect-binary-layout, base vs renamed)

Compared only inside the hashed fields parameters, raw_result, normalized_result, locations, environment, limitations, evidence_links. Three paths differ; all other paths in those fields are equal.

- parameters.path — base: "/usr/bin/jq" | renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat"
- normalized_result.artifact.path — base: "/usr/bin/jq" | renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat"
- locations[0].path — base: "/usr/bin/jq" | renamed: "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat"

raw_result, environment, limitations and evidence_links have zero differing paths between base and renamed.
For the content-keyed verb instructions, base vs renamed also has zero differing paths in all seven hashed fields.

## Supporting observations

- Envelope bytes differ between base and repeat for both verbs only in meta.duration ("5164ms" vs "5105ms" for instructions; "143ms" vs "144ms" for inspect-binary-layout). All six envelope sha256 values are distinct.
- Path containment check on the saved bytes: the renamed envelopes contain the renamed path 5 times (layout) and 2 times (instructions) and contain "/usr/bin/jq" 0 times; the base and repeat envelopes contain "/usr/bin/jq" 4 times (layout) and 1 time (instructions) and contain the renamed name 0 times.
- Independent id recompute under the 6.5.0 rule: command `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-26/recompute-ids.py envelopes/*.json`, exit 0, output tail "recomputed ids: 6 match of 6 total". For instructions the recompute reports "path-bearing fields in the hashed projection: none"; for inspect-binary-layout it lists /parameters/path, /normalized_result/artifact/path and /locations/0/path. This matches the verdict split above.
- Carrier integrity: sha256sum of /usr/bin/jq and of the renamed copy were recorded before the first call and after the last call; both are e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 at both times, so the byte-identical copy was not modified.

## Failures

None. All six calls exited 0 and every stderr file is empty (0 bytes). No call was re-run.

## Carrier hashes before and after

Command: sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat
Before first call, 2026-10-22T14:55:19Z, and after last call, 2026-10-22T14:55:39Z, both gave:
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat

## Package pin

After every call the seat read /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json: version 6.5.0, sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Both match the frozen pin in claims.json.

## Artifact list (sha256)

- runs.tsv — d12b22924fda0ac774a0947aa5cf0cd7576d052debb1320b413b90948c875e88
- run.sh (driver script) — e1bbc0ab2c73b5090c3b08b1e42de98f9a192525fd3fe179617ff776d174c334
- carrier-hashes-before.txt — 5dcf4610cc9af827d62296d67e06c829c875364ae222315e4799e0928c71e988
- carrier-hashes-after.txt — 5dcf4610cc9af827d62296d67e06c829c875364ae222315e4799e0928c71e988
- envelopes/jq-instructions-base.json — bc3193082694394221041b49de5d78b65c0c45b44e3a2ca811da828116d4adcd
- envelopes/jq-instructions-base.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- envelopes/jq-instructions-repeat.json — 32c263e1521175dd29049344886e207fb8bec278457e49884a0b1e4ffc195b01
- envelopes/jq-instructions-repeat.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- envelopes/jq-instructions-renamed.json — 29920103401287c054dd3b999bc3613ad8f420be0efead35ee1b40bc1b3a2332
- envelopes/jq-instructions-renamed.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- envelopes/jq-inspect-binary-layout-base.json — dfd4990be733af751b594cf155630e5caf8f634eb52cf39bfc61cd4c29ab7e5d
- envelopes/jq-inspect-binary-layout-base.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- envelopes/jq-inspect-binary-layout-repeat.json — 6b85eb5bcc75ced0abe175f2216b7c0f31069a13cb87ba11db9e0c6e3e2ba947
- envelopes/jq-inspect-binary-layout-repeat.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- envelopes/jq-inspect-binary-layout-renamed.json — 0621c8de2d2d662bbe4d6d02fbd43922a9b96c968ac63fcd34ea6d079bb51ae7
- envelopes/jq-inspect-binary-layout-renamed.json.stderr — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

All paths above are relative to /fast/scratch/hyaku/kaidoku-r27/seats/RunJqD/.

## Tools, installs and sources

- No package was installed or upgraded this run; the operator tooling directive required no action.
- No web source was opened this round; the claim rests on local files only (claims.json, the installed 6.5.0 package.json, the lane recompute tool).
- No lane file was edited except this report file. No git, no jj, no commit anywhere.

## Labels

All statements above are observations from the commands named, except the verdict mapping, which follows the frozen rule in claims.json.
