# R26-C1 table runs — verbs `read-bytes` and `inspect-binary-layout` (seat RunReadBytesLayout)

Date: 2026-10-22. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (read-only for this seat).
Carrier: /usr/bin/jq, 30,800 B, sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806.
Alternate (copy): /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq, 30,800 B, same sha256 (distinct inode 1481018327 vs 125895; not a hardlink).
REA: rea-agents 6.5.0 from the npx cache /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents (package.json version 6.5.0). Node v24.21.0, npm 11.19.0. CLI only, no MCP device.

## Result summary

All six calls succeeded on the first attempt (exit 0, empty stderr). No retry was needed; the retry-once path in the driver was armed but never fired.

| verb | base id | repeat id | copy id | base==repeat | base==copy | derived verdict |
|---|---|---|---|---|---|---|
| read-bytes | ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c | ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c | ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c | yes | yes | content-keyed |
| inspect-binary-layout | ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd | ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd | ev_52da4b3df64645306a8046c6571ce7849fd2ae4383e8d05f16601fefcdccd161 | yes | no | path-sensitive |

Derived verdict computed with the claims.json `derived_verdict` rule verbatim: no-id if any of the three envelopes lacks a string `.data.evidence_id` starting `ev_`; else unstable if base != repeat; else content-keyed if copy == base; else path-sensitive. Both verbs have `ev_` ids in all three envelopes, so no-id does not apply; base == repeat for both, so unstable does not apply.

## runs.tsv content

Path: /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/runs.tsv (sha256 5159b2f134c2990ed68835853153934c519501b02e340f7c0f68266277e5a5a2), tab-separated, header `verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256`.

```
verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256
read-bytes	base	/usr/bin/jq	read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T12:12:19Z	2026-10-22T12:12:25Z	3eb2f92c3d98761c421c3867b22aaceefb8a5299585b73fc93b4b59f9c711552	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
read-bytes	repeat	/usr/bin/jq	read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T12:12:25Z	2026-10-22T12:12:31Z	b6fa9c4eae2be4507a3f5f158f85366acde36669338abd85de1a126ac219aaa1	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
read-bytes	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	read-bytes /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --length 64 --format json --full-output	0	2026-10-22T12:12:31Z	2026-10-22T12:12:37Z	5a893e0e0b5dcb136a6d2051d9b187f54f455110a91b775f73845aac068618de	ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect-binary-layout	base	/usr/bin/jq	inspect-binary-layout /usr/bin/jq --format json --full-output	0	2026-10-22T12:12:37Z	2026-10-22T12:12:38Z	4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f	ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect-binary-layout	repeat	/usr/bin/jq	inspect-binary-layout /usr/bin/jq --format json --full-output	0	2026-10-22T12:12:38Z	2026-10-22T12:12:39Z	98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf	ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect-binary-layout	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	inspect-binary-layout /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq --format json --full-output	0	2026-10-22T12:12:39Z	2026-10-22T12:12:40Z	bfa78b4d3a4174256e8fde069c4671ab9f40b02d9689d72983fc7b89c50e46e9	ev_52da4b3df64645306a8046c6571ce7849fd2ae4383e8d05f16601fefcdccd161	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

Producing command (one command per row, run strictly one after another, never in parallel):

```
cd /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 read-bytes /usr/bin/jq 0x103fa0 --length 64 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 read-bytes /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --length 64 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 inspect-binary-layout /usr/bin/jq --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 inspect-binary-layout /usr/bin/jq --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 inspect-binary-layout /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq --format json --full-output
```

argv strings are exactly `verbs_argv` from .ufo/waves/round-26/claims.json for each verb, with `<PATH>` substituted for the run path and nothing else changed. Driver: /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/driver.py (sha256 dd09adc409ba8204ef917dc7269fe03f28afd69197c696934331b73938526994), which spawns the six calls sequentially via subprocess and appends one TSV row per call.

## Carrier custody across the wave

Before the first call, 2026-10-22T12:11:48Z (observation, file /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/before-sha256.txt):

```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq
```

After the last call, 2026-10-22T12:13:08Z (observation, file after-sha256.txt): both lines byte-identical to the above. The alternate copy was read only; neither carrier was modified.

## Envelopes (sizes and hashes)

Directory: /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/envelopes/

| file | bytes | sha256 | ok | evidence_id | subject sha256 | contains the path it ran on |
|---|---|---|---|---|---|---|
| read-bytes-base.json | 3347 | 3eb2f92c3d98761c421c3867b22aaceefb8a5299585b73fc93b4b59f9c711552 | true | ev_99b0…500c | e815…7806 | yes (.data.subject.local_path) |
| read-bytes-repeat.json | 3347 | b6fa9c4eae2be4507a3f5f158f85366acde36669338abd85de1a126ac219aaa1 | true | ev_99b0…500c | e815…7806 | yes |
| read-bytes-copy.json | 3382 | 5a893e0e0b5dcb136a6d2051d9b187f54f455110a91b775f73845aac068618de | true | ev_99b0…500c | e815…7806 | yes |
| inspect-binary-layout-base.json | 80065 | 4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f | true | ev_294a…a71bd | e815…7806 | yes (.data.parameters.path, .data.normalized_result.artifact.path, .data.locations[0].path, .data.subject.local_path) |
| inspect-binary-layout-repeat.json | 80065 | 98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf | true | ev_294a…a71bd | e815…7806 | yes |
| inspect-binary-layout-copy.json | 80205 | bfa78b4d3a4174256e8fde069c4671ab9f40b02d9689d72983fc7b89c50e46e9 | true | ev_52da…d161 | e815…7806 | yes |

Every `.stderr` file is 0 bytes (sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, the empty-file digest).

Subject sha256 came from `.data.subject.digest.sha256` in every envelope (the claims.json fallback `.data.normalized_result.artifact.sha256` is absent for `read-bytes` and equals the same carrier digest for `inspect-binary-layout`).

## Why the two verbs differ (mechanism, read from the installed 6.5.0 package)

Observation: `evidence_id` is computed as `ev_` + digest of a semantic projection (rea-agents 6.5.0, dist/domain/evidence.js: `computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\``). The projection keeps `subject.digest`, `subject.format`, `subject.architecture`, `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, `evidence_links`; it drops display-only subject fields such as `local_path`.

Observation from the envelopes: `read-bytes` puts only `{"address": "0x103fa0", "length": 64}` in `.data.parameters` and its `normalized_result` carries no path, so the alternate-path copy produces the identical semantic projection and therefore the identical id (content-keyed). `inspect-binary-layout` puts the run path in `.data.parameters.path` and in `.data.normalized_result.artifact.path` and in `.data.locations[0].path`, so the same bytes at a different path yield a different id (path-sensitive).

Inference (not independently measured here): a same-path repeat of `inspect-binary-layout` is stable because the path component is unchanged, not because the tool caches; the repeat produced a fresh envelope whose only differing field is `duration`, and the seat's TMPDIR (/fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/tmp) holds only a node-compile-cache directory after the six calls, with no REA analysis snapshot file written. The `read-bytes` content-keying is likewise a property of what the semantic projection covers, not of caching. A sibling seat (KaidokuR26.CacheConfound) is tasked with the cache confound; this seat did not audit caching.

Cross-check (observation): the L1 pre-freeze probe envelope /fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json (sha256 689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a) carries evidence_id ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd, identical to my base and repeat ids; the probe file differs from my base envelope only in the `duration` field ("192ms" vs "194ms").

## Failure record

None. Six of six calls exited 0 with empty stderr; there is no error text to report. The retry-once rule in the card was implemented in the driver (a non-zero exit would trigger exactly one more attempt, with the failed attempt's stdout and stderr preserved as `<verb>-<run>.attempt1.json` / `.stderr` and an extra TSV row) but it never fired, so no attempt1 artifacts exist.

## Risk: envelope bytes are not byte-reproducible

Observation: base and repeat envelopes for the same verb differ in envelope sha256 even when the evidence_id is identical, and the only differing field is `duration` (read-bytes "5500ms" vs "5344ms"; inspect-binary-layout "194ms" vs "159ms"; copy "193ms"). Consequence for the counter: the table's `base_id`/`repeat_id`/`copy_id` cells and the committed envelopes' `.data.evidence_id` values are stable, but any check that compares committed envelope file digests against a re-run will fail on the `duration` line. The claims.json `row_complete` rule reads evidence_id and subject digest, not envelope file digests, so the claim as frozen is unaffected (inference).

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/RunReadBytesLayout/, sha256)

- driver.py — dd09adc409ba8204ef917dc7269fe03f28afd69197c696934331b73938526994
- runs.tsv — 5159b2f134c2990ed68835853153934c519501b02e340f7c0f68266277e5a5a2
- before-sha256.txt — 39af4eb38eedbaf9e95897954b61443039bbebe7506aa72b9bb1c52c35463059
- after-sha256.txt — 5a2b693d0150eb6feac06ece7921757ba4de261298270983df8e34de12f61dcd
- driver.log — 57b0ea2e024185e61f6fcc12335f6a269012d7025f1d9cc7bd326a1d6b8f9083
- envelopes/read-bytes-base.json — 3eb2f92c3d98761c421c3867b22aaceefb8a5299585b73fc93b4b59f9c711552
- envelopes/read-bytes-repeat.json — b6fa9c4eae2be4507a3f5f158f85366acde36669338abd85de1a126ac219aaa1
- envelopes/read-bytes-copy.json — 5a893e0e0b5dcb136a6d2051d9b187f54f455110a91b775f73845aac068618de
- envelopes/inspect-binary-layout-base.json — 4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f
- envelopes/inspect-binary-layout-repeat.json — 98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf
- envelopes/inspect-binary-layout-copy.json — bfa78b4d3a4174256e8fde069c4671ab9f40b02d9689d72983fc7b89c50e46e9
- envelopes/*.stderr (six files) — e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

Note: driver.log is the stderr progress log of the six calls, not evidence.

Tooling: no tool was installed or upgraded. Existing npx (npm 11.19.0), Node v24.21.0 and python3 were used. No pacman, uv, cargo or npm -g activity. The alternate carrier was opened read-only; nothing in the lane was modified except this report file.

## Open items for the L1

- The committed corpus/evidence/round-26/c1/envelopes/<verb>-<run>.json files should be these six envelopes byte-for-byte (they were written once and never edited).
- The table rows for these two verbs should carry verdict `content-keyed` for read-bytes and `path-sensitive` for inspect-binary-layout, with the three ids and subject sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806.
- Routed defect 4 of corpus/lessons/round-25-verifier-spotcheck.md concerns a vyper carrier page count, not these verbs; the routed defects list contains no item that these two verbs' envelopes answer or contradict.
