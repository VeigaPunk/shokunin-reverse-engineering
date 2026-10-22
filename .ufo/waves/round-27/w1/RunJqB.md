# R27-C1 wave 1 — seat RunJqB — carrier jq, verbs decompile and xrefs

Scope: the jq carrier and the two verbs named in my card. All work is in
`/fast/scratch/hyaku/kaidoku-r27/seats/RunJqB/`. The lane was read only; no lane file other than
this report was written, no git write, no jj command.

## Invocation

Form: `TMPDIR=<seat tmp> npx -y rea-agents@6.5.0 <verb> <PATH> 0x103fa0 --format json --full-output`.
argv from `claims.json` `verbs_argv` (decompile, xrefs); `<ADDR>` = `carriers.jq.address` = `0x103fa0`.
Base path `/usr/bin/jq`; renamed path `/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`.
Package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`, package.json `version`
6.5.0, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` — the frozen pair.
Six calls run one after another; no call was re-run.

## Carrier bytes before and after

Command: `sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`
before the first call and after the last call. Both snapshots are byte-identical (files unchanged),
and the renamed copy is byte-identical to the base carrier:

```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat
```

## runs.tsv

Header exactly as specified: `seat carrier verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256 pkg_version pkg_json_sha256`.
Full file (tab separated) is at `/fast/scratch/hyaku/kaidoku-r27/seats/RunJqB/runs.tsv`, sha256 `066ce1ca3a1d1f12037da1472a98de9fdec6e55f63d73a2a0bac1a8cef491f18`.

```
RunJqB	jq	decompile	base	/usr/bin/jq	decompile /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:54:51Z	2026-10-22T14:54:57Z	047463e3b1d207cbfc461d6a6c49465b190ed885658e9ec8b674ad61d54d44ae	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqB	jq	decompile	repeat	/usr/bin/jq	decompile /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:54:57Z	2026-10-22T14:55:02Z	3d09bd6e5a740feff90ad9cc92af13d0bc3faf304fd12ba05da866b012a03b27	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqB	jq	decompile	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	decompile /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat 0x103fa0 --format json --full-output	0	2026-10-22T14:55:02Z	2026-10-22T14:55:08Z	7db7a16279004f92c6ecfa87dd66a2b87504f17176319f0770449d543484378a	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqB	jq	xrefs	base	/usr/bin/jq	xrefs /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:08Z	2026-10-22T14:55:13Z	a61ab5d3ce4012fb1003d2ddb14efed152d134380e286d5f289cf29366966b30	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqB	jq	xrefs	repeat	/usr/bin/jq	xrefs /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:13Z	2026-10-22T14:55:19Z	6f36a7d336df75156de74a39fac9785840be6fff327b8aabc5790c24b40d6052	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqB	jq	xrefs	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	xrefs /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat 0x103fa0 --format json --full-output	0	2026-10-22T14:55:19Z	2026-10-22T14:55:24Z	30d9446aa4ec95db6108bc359ebb46b278f7da4c1735f6e4b8e622156dcfdbfb	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
```

## Per verb verdicts (claims.json rule: unstable if base != repeat, content-keyed if renamed == base, else rename-sensitive)

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
|---|---|---|---|---|---|---|
| decompile | ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df | same | same | yes | yes | content-keyed |
| xrefs | ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c | same | same | yes | yes | content-keyed |

Observation: both jq verbs are content-keyed. No rename-sensitive verb in my scope, so the
"differing JSON paths inside the hashed fields" section required for rename-sensitive verbs does
not apply. For completeness I ran the comparison anyway: between the base and the renamed
envelope of each verb, the only differing JSON paths are `.data.subject.local_path`
(`/usr/bin/jq` vs `/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`),
`.data.subject.name` (`jq` vs `jq-r27-renamed.dat`) and `.meta.duration` (`5010ms` vs `4960ms` for
decompile, `4889ms` vs `5199ms` for xrefs). All seven hashed fields (parameters, raw_result,
normalized_result, locations, environment, limitations, evidence_links) are equal between base
and renamed for both verbs, and so is every field the 6.5.0 semantic projection keeps
(subject.digest, subject.format, subject.architecture, provider, analysis_profile,
predicate_type, operation). The path and file name do not enter the id.

## subject name and local path per run

| verb | run | .data.subject.name | .data.subject.local_path |
|---|---|---|---|
| decompile | base | jq | /usr/bin/jq |
| decompile | repeat | jq | /usr/bin/jq |
| decompile | renamed | jq-r27-renamed.dat | /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat |
| xrefs | base | jq | /usr/bin/jq |
| xrefs | repeat | jq | /usr/bin/jq |
| xrefs | renamed | jq-r27-renamed.dat | /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat |

Observation: `.data.subject.name` is the file name of the run path in all six envelopes.

## Envelope checks I ran (read-only, against my own artifacts)

Command: python3 over the six saved envelopes, using `tools/round-26/recompute-ids.py` from the
lane read-only, plus sha256 of the saved bytes. For all six envelopes: `ok` true; `.meta.command`
equals the verb; `.data.evidence_id` starts with `ev_`; `recompute.compute_evidence_id(data)`
equals `.data.evidence_id`; the envelope sha256 equals the `envelope_sha256` cell in runs.tsv and
the six digests are distinct; `.data.subject.digest.sha256` equals the carrier sha256
`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; the envelope bytes contain
their own run path and not the row's other path; `.data.subject.name` equals that path's basename.
`utc_start` values from 2026-10-22T14:54:51Z onward are later than the counter commit time
2026-10-22T14:51:23Z (`git log --diff-filter=A --format=%ct a4f674b... -- tools/round-27/c1-rename-identity.py`).

Failures: none. All six calls exited 0. Every stderr file is empty (sha256 of the empty byte
string `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). No call was re-run.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunJqB/)

Tool installs: none. The REA package was already installed at the frozen 6.5.0 root; node v24.21.0
and npx came from the existing fnm install. Nothing was installed or upgraded in this seat.

| file | sha256 |
|---|---|
| runs.tsv | 066ce1ca3a1d1f12037da1472a98de9fdec6e55f63d73a2a0bac1a8cef491f18 |
| run.sh | 7d867607a6713bcdb1b11c9948cb672815d1c59bacde25ac2bc28874e9975c7b |
| carrier-sha256-before.txt and carrier-sha256-after.txt (identical) | 5dcf4610cc9af827d62296d67e06c829c875364ae222315e4799e0928c71e988 |
| envelopes/jq-decompile-base.json | 047463e3b1d207cbfc461d6a6c49465b190ed885658e9ec8b674ad61d54d44ae |
| envelopes/jq-decompile-repeat.json | 3d09bd6e5a740feff90ad9cc92af13d0bc3faf304fd12ba05da866b012a03b27 |
| envelopes/jq-decompile-renamed.json | 7db7a16279004f92c6ecfa87dd66a2b87504f17176319f0770449d543484378a |
| envelopes/jq-xrefs-base.json | a61ab5d3ce4012fb1003d2ddb14efed152d134380e286d5f289cf29366966b30 |
| envelopes/jq-xrefs-repeat.json | 6f36a7d336df75156de74a39fac9785840be6fff327b8aabc5790c24b40d6052 |
| envelopes/jq-xrefs-renamed.json | 30d9446aa4ec95db6108bc359ebb46b278f7da4c1735f6e4b8e622156dcfdbfb |
| envelopes/*.json.stderr (all six files, each empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

## Risks and blockers

- Risk: the L1 must merge my six rows into `corpus/evidence/round-27/c1/runs.tsv` and the
  corresponding envelopes under `corpus/evidence/round-27/c1/envelopes/` with the file names the
  counter expects (`jq-<verb>-<run>.json`), and commit them after the counter commit so the
  first-commit-time rule holds. My files are named exactly that way.
- Observation: the lane already holds an untracked integration helper `tools/round-27/assemble-c1.py`
  (not mine). I read it read-only and did not run or modify it. Its expectations match my
  artifacts: seat directory `<seats>/RunJqB`, the frozen header, envelope file name
  `<carrier>-<verb>-<run>.json` under `<seats>/RunJqB/envelopes/`, envelope sha256 equal to the
  runs.tsv cell. My header check passed against that header list.
- Inference: the counter's "envelope contains the row's other path" check passes because the
  renamed envelope never mentions `/usr/bin/jq` and the base envelopes never mention the renamed
  path; verified by string search over the raw bytes of all six envelopes.
- No blocker.

Report: .ufo/waves/round-27/w1/RunJqB.md
