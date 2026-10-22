# R27-C1 wave 1 — seat RunJqC — carrier jq, verbs read-bytes and function

Scope: only the jq carrier and the two verbs named in my card. All artifacts are under
`/fast/scratch/hyaku/kaidoku-r27/seats/RunJqC/`. The lane was read only; no lane file
other than this report was written, no git write, no jj command, no delegation.

## Invocation

Form: `TMPDIR=<seat tmp> npx -y rea-agents@6.5.0 <verb> <PATH> <ADDR> --format json --full-output`.
argv taken verbatim from `claims.json` `verbs_argv` (`read-bytes` carries `--length 64`,
`function` does not); `<ADDR>` = `carriers.jq.address` = `0x103fa0`.
Base path `/usr/bin/jq`; renamed path `/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`.
Package root used: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`, package.json
`version` 6.5.0, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` — the frozen
pair in claims.json, re-read after every one of the six calls.
Order of calls: read-bytes base, read-bytes repeat, read-bytes renamed, function base,
function repeat, function renamed. Six calls, one after another; no call was re-run.

Driver script: `/fast/scratch/hyaku/kaidoku-r27/seats/RunJqC/drive.sh` (sha256
`8fc0235dd1ddba9a6c9fe9686f262640fdd94365299109a62a1141aa9c336a23`).

## Carrier bytes before and after

Command: `sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat`,
run before the first call (2026-10-22T14:55:30Z) and after the last call (2026-10-22T14:56:06Z).
Both snapshots are byte-identical; the carriers were not modified:

```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat
```

Observation: the renamed copy is byte-identical to the base carrier, matching
`claims.json` `carriers.jq.sha256`.

## runs.tsv

File: `/fast/scratch/hyaku/kaidoku-r27/seats/RunJqC/runs.tsv`, sha256
`bfad25b41a7d9d44dcb41d24bcbc97154b629843328801fe733ad0bc16542adb`.
Header is exactly the 14 specified columns, tab separated:
`seat carrier verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256 pkg_version pkg_json_sha256`.
Full content (tab separated):

```
RunJqC	jq	read-bytes	base	/usr/bin/jq	read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T14:55:30Z	2026-10-22T14:55:36Z	aa7478fdaa8d1f3d13d1721bf94edff530cae1fed82eda30c0a07d2cffe88328	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqC	jq	read-bytes	repeat	/usr/bin/jq	read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T14:55:36Z	2026-10-22T14:55:42Z	3719f662a787bee169b49e5f983ac254dc707056242667ca962c9adf34c66df6	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqC	jq	read-bytes	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	read-bytes /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T14:55:42Z	2026-10-22T14:55:48Z	208bcc1a79d4cba92b0fb38c1cc5a7d58eadaf5ad613657ca690704f1aad1b6b	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqC	jq	function	base	/usr/bin/jq	function /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:48Z	2026-10-22T14:55:54Z	c8636c8c739b3b968cd2c31def61e184224b0906813e858d21db26b0ac991dfd	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqC	jq	function	repeat	/usr/bin/jq	function /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T14:55:54Z	2026-10-22T14:56:00Z	aa0a6d7ae9ada48716a69cf7afa8a414e5a4bf068a726449c7d9c97b7775dcbe	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
RunJqC	jq	function	renamed	/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat	function /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat 0x103fa0 --format json --full-output	0	2026-10-22T14:56:00Z	2026-10-22T14:56:06Z	d0782e28a20b43cc724738b8c4ec40b75f5fe62aa7ef180d9ec8ffb2c8597dc3	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806	6.5.0	a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
```

## Per verb verdicts (claims.json rule: unstable if base != repeat, content-keyed if renamed == base, else rename-sensitive)

| verb | base id | repeat id | renamed id | base==repeat | base==renamed | verdict |
|---|---|---|---|---|---|---|
| read-bytes | ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c | same | same | yes | yes | content-keyed |
| function | ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5 | same | same | yes | yes | content-keyed |

Observation: both jq verbs in my scope are content-keyed. No rename-sensitive verb in my scope,
so the "differing JSON paths inside the hashed fields" section required for rename-sensitive
verbs does not apply. For completeness I ran the comparison anyway (artifact
`field-comparison.txt`): between base and renamed the only differing JSON paths are
`.data.subject.local_path`, `.data.subject.name` and `.meta.duration`; between base and repeat
the only differing path is `.meta.duration`. All seven hashed fields (parameters, raw_result,
normalized_result, locations, environment, limitations, evidence_links) are equal between base
and renamed for both verbs, and no difference falls inside a hashed field. The path and file
name do not enter the evidence id at 6.5.0.

## subject name and local path per run

| verb | run | .data.subject.name | .data.subject.local_path |
|---|---|---|---|
| read-bytes | base | jq | /usr/bin/jq |
| read-bytes | repeat | jq | /usr/bin/jq |
| read-bytes | renamed | jq-r27-renamed.dat | /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat |
| function | base | jq | /usr/bin/jq |
| function | repeat | jq | /usr/bin/jq |
| function | renamed | jq-r27-renamed.dat | /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat |

Observation: `.data.subject.name` is the file name of the run path in all six envelopes, so the
renamed run reports `jq-r27-renamed.dat` and the base runs report `jq`. Both paths are reported
verbatim in `local_path`.

## Envelope checks I ran (read-only, against my own artifacts)

Command: `python3 -I -B tools/round-26/recompute-ids.py --dir /fast/scratch/hyaku/kaidoku-r27/seats/RunJqC/envelopes`
run from the lane root (read-only use of the lane tool; no lane file modified), output saved to
`recompute-ids-output.txt`, exit 0, last line `recomputed ids: 6 match of 6 total`.
For all six envelopes: `ok` true; `.meta.command` equals the verb (`read-bytes`, `function`);
`.data.evidence_id` starts with `ev_`; the recomputed id equals the stored id; the envelope
sha256 equals the `envelope_sha256` cell in runs.tsv; the six envelope digests are distinct;
`.data.subject.digest.sha256` equals the carrier sha256
`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; the envelope bytes contain
their own run path and do not contain the row's other path (string search over the raw bytes:
0 hits of `/usr/bin/jq` in the two renamed envelopes, 0 hits of `jq-r27-renamed` in the four base
envelopes); `.data.subject.name` equals the basename of that run's path.
The recompute tool also reported that the hashed projection of the read-bytes envelopes has no
path-bearing field at all, and for the function envelopes the only path-bearing fields are
`/raw_result/value/native_value_flow/parameters/0/data_type` and its normalized twin, both
`/undefined8` (a type tag, not the carrier path).

Timing check: `git log --diff-filter=A --format='%ct %cI' a4f674b343d8564e21f7eb8984630a95089c82d6 -- tools/round-27/c1-rename-identity.py`
gives `1792680683 2026-10-22T11:51:23-03:00`, that is 2026-10-22T14:51:23Z. My earliest
`utc_start` is 2026-10-22T14:55:30Z, later than the counter commit, as the counter requires
(saved in `counter-commit-time.txt`).

## Failures

None. All six calls exited 0. Every stderr file is empty (sha256 of the empty byte string
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). No call was re-run and no
error text had to be preserved.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/RunJqC/)

| file | sha256 |
|---|---|
| runs.tsv | bfad25b41a7d9d44dcb41d24bcbc97154b629843328801fe733ad0bc16542adb |
| drive.sh | 8fc0235dd1ddba9a6c9fe9686f262640fdd94365299109a62a1141aa9c336a23 |
| carrier-sha256-before.txt | 0868505b97eb94dbb43a138859619f7e4fd020238026e708f07c73900da8f57f |
| carrier-sha256-after.txt | 3ccc76a998cb18689474b1e4dddfc899354952a06ed8b995690e8d25af9e7535 |
| counter-commit-time.txt | 49143adf84f1c02de3810c8e1db49d4b20c16d87460211b4fbacffbda74e85a4 |
| field-comparison.txt | 2a50dcef3c4af4423c5456e07476b6d7026bad3f876cd52b037249ab7f385fec |
| recompute-ids-output.txt | ee2ed94bd11348d8dd248e09f311d6cefc41e5374a0ad1348e56cb89de5b6add |
| envelopes/jq-read-bytes-base.json | aa7478fdaa8d1f3d13d1721bf94edff530cae1fed82eda30c0a07d2cffe88328 |
| envelopes/jq-read-bytes-repeat.json | 3719f662a787bee169b49e5f983ac254dc707056242667ca962c9adf34c66df6 |
| envelopes/jq-read-bytes-renamed.json | 208bcc1a79d4cba92b0fb38c1cc5a7d58eadaf5ad613657ca690704f1aad1b6b |
| envelopes/jq-function-base.json | c8636c8c739b3b968cd2c31def61e184224b0906813e858d21db26b0ac991dfd |
| envelopes/jq-function-repeat.json | aa0a6d7ae9ada48716a69cf7afa8a414e5a4bf068a726449c7d9c97b7775dcbe |
| envelopes/jq-function-renamed.json | d0782e28a20b43cc724738b8c4ec40b75f5fe62aa7ef180d9ec8ffb2c8597dc3 |
| envelopes/*.json.stderr (six files, each empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

The seat `tmp/` directory holds only the node compile cache written by npx under `TMPDIR`; it is
not a deliverable.

Tool installs: none. The REA package was already installed at the frozen 6.5.0 root; node
v24.21.0 and npx came from the existing fnm install. Nothing was installed or upgraded, and no
host package transaction was attempted.

## Risks and blockers

- Risk: the L1 must merge my six rows into `corpus/evidence/round-27/c1/runs.tsv` and copy the
  six envelopes under `corpus/evidence/round-27/c1/envelopes/` under the file names the counter
  expects (`jq-<verb>-<run>.json`), then commit them after the counter commit so the
  first-commit-time rule holds. My files are named exactly that way and the envelope digests
  match the runs.tsv cells.
- Observation: the lane holds an untracked integration helper `tools/round-27/assemble-c1.py`
  (not mine). I read it read-only and did not run or modify it. It looks for each seat's
  `runs.tsv` and `envelopes/<carrier>-<verb>-<run>.json`, checks the envelope sha256 against the
  seat's runs.tsv cell and copies the envelope byte-exact; my layout matches.
- Observation: stderr file naming was not fixed by the claim. I used
  `<envelope>.json.stderr`, matching the sibling jq seat, and the assemble helper copies only
  the `.json` envelopes, so stderr is not part of the integration.
- Inference: the counter's "envelope contains the row's other path" check passes for my rows
  because the renamed envelopes never mention `/usr/bin/jq` and the base envelopes never mention
  the renamed path; verified by string search over the raw bytes of all six envelopes.
- No blocker.

Report: .ufo/waves/round-27/w1/RunJqC.md
