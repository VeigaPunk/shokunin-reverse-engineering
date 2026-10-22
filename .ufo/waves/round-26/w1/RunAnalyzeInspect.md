# RunAnalyzeInspect — R26-C1 table runs for verbs `analyze` and `inspect`

Seat: `KaidokuR26.RunAnalyzeInspect`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Round 26, attempt 1, wave 1. Claims source: `.ufo/waves/round-26/claims.json` (`R26-C1`).
Date of runs: 2026-10-22 UTC. No lane file other than this report was written; lane is otherwise read-only here.

## Carrier custody (observation)

Command: `sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`, run before the first call at
2026-10-22T12:11:42Z and after the last call at 2026-10-22T12:12:40Z. Both runs produced identical bytes.

```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq
```

Both files are 30,800 bytes and byte-identical to the carrier sha256 named in `claims.json`
(`carrier.sha256`). The alternate copy was only read; it was never written.

## Invocation form (observation)

Every call was exactly the `verbs_argv` template with `<PATH>` substituted, run sequentially (never parallel):

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r26/seats/RunAnalyzeInspect/tmp npx -y rea-agents@6.5.0 <verb> <PATH> --format json --full-output
```

`npx -y rea-agents@6.5.0` resolved to the installed package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` whose `package.json` reports version
`6.5.0` (read at 2026-10-22T12:12:45Z). The 6.7.0 root `a1722018f28f9df2` was not used.

## runs.tsv content (verbatim, tab separated)

Path: `/fast/scratch/hyaku/kaidoku-r26/seats/RunAnalyzeInspect/runs.tsv` (sha256
`d885e43581a7607590aaf3ff62f39468ac000b3210219d06881d3d8b01b05944`). Header-less; columns are
verb, run, path, argv, exit, utc_start, utc_end, envelope_sha256, evidence_id, subject_sha256.

```
analyze	base	/usr/bin/jq	analyze /usr/bin/jq --format json --full-output	0	2026-10-22T12:11:51Z	2026-10-22T12:11:58Z	3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
analyze	repeat	/usr/bin/jq	analyze /usr/bin/jq --format json --full-output	0	2026-10-22T12:12:00Z	2026-10-22T12:12:06Z	b65e650292b9f475d1c9d029adfe032ce1aed883ef408b594bb293ea7b0d84a6	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
analyze	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	analyze /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq --format json --full-output	0	2026-10-22T12:12:06Z	2026-10-22T12:12:12Z	be1dd0c4c57dde68d760f06cc00b8afcb8f30a0805a1982e491a1d4339089243	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect	base	/usr/bin/jq	inspect /usr/bin/jq --format json --full-output	0	2026-10-22T12:12:15Z	2026-10-22T12:12:21Z	9421d1f8701987b669c2ca6f1ed5d1343c24b304b6fa06a63bab0b3bdd98eab1	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect	repeat	/usr/bin/jq	inspect /usr/bin/jq --format json --full-output	0	2026-10-22T12:12:21Z	2026-10-22T12:12:27Z	f509fcfeb1ab4aa9e530b71e42ff94da6fa822e9c3c4795c1ccb957394c0eaaa	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
inspect	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	inspect /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq --format json --full-output	0	2026-10-22T12:12:27Z	2026-10-22T12:12:33Z	62e09a1e8ecb1d2cc06eddc3695799c1f272bcff4224236eccb56edc2576da89	ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

## Per-verb identity results (observation)

| verb | base id | repeat id | copy id | base==repeat | base==copy | derived verdict |
|---|---|---|---|---|---|---|
| analyze | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | same | same | yes | yes | content-keyed |
| inspect | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | same | same | yes | yes | content-keyed |

`subject_sha256` in every row came from `.data.subject.digest.sha256` (that field was present in all six
envelopes; the fallback `.data.normalized_result.artifact.sha256` was absent, `None`). In all six rows
the value equals the carrier sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.

## Derived verdict derivation (observation, per `claims.json` `rules.derived_verdict`)

Rule: no-id if any of the three envelopes lacks a string `.data.evidence_id` starting `ev_`; else
unstable if base != repeat; else content-keyed if copy == base; else path-sensitive.

- All six envelopes have `.ok == true` and `.data.evidence_id` a string starting `ev_`, so the
  no-id branch does not apply for either verb.
- For `analyze`: base == repeat, therefore not unstable; copy == base, therefore content-keyed.
- For `inspect`: base == repeat, therefore not unstable; copy == base, therefore content-keyed.

Verdict for both verbs: `content-keyed`. No `unstable` and no `path-sensitive` verdict was produced
by these two verbs.

## Envelope inventory (observation)

Envelopes directory: `/fast/scratch/hyaku/kaidoku-r26/seats/RunAnalyzeInspect/envelopes/`.
Sizes are bytes on disk; sha256 is of the file bytes. All `.stderr` files are 0 bytes
(sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the empty-file digest).

| file | size | sha256 |
|---|---|---|
| analyze-base.json | 7559 | 3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb |
| analyze-repeat.json | 7559 | b65e650292b9f475d1c9d029adfe032ce1aed883ef408b594bb293ea7b0d84a6 |
| analyze-copy.json | 7594 | be1dd0c4c57dde68d760f06cc00b8afcb8f30a0805a1982e491a1d4339089243 |
| inspect-base.json | 7559 | 9421d1f8701987b669c2ca6f1ed5d1343c24b304b6fa06a63bab0b3bdd98eab1 |
| inspect-repeat.json | 7559 | f509fcfeb1ab4aa9e530b71e42ff94da6fa822e9c3c4795c1ccb957394c0eaaa |
| inspect-copy.json | 7594 | 62e09a1e8ecb1d2cc06eddc3695799c1f272bcff4224236eccb56edc2576da89 |

Each envelope is one line of JSON with top-level keys `ok`, `data`, `meta`. `meta.command` equals the
verb; `meta.duration` was `5912ms`, `5346ms`, `5225ms`, `5300ms`, `5225ms`, `5304ms` respectively.

## Envelope differences (observation, per-key diff)

- analyze base vs analyze repeat: only `/meta/duration` differs (`5912ms` vs `5346ms`).
- analyze base vs analyze copy: `/data/subject/local_path` differs
  (`/usr/bin/jq` vs `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`) and `/meta/duration` differs.
- analyze base vs inspect base: only `/meta/command` (`analyze` vs `inspect`) and `/meta/duration` differ.

So the id is invariant to path, to repetition and to the choice of `analyze` vs `inspect`; the envelope
bytes differ only in the recorded local path, the verb label and the wall-clock duration.

Diagnostics (non-gating per `claims.json`): each envelope text contains the path it was run on —
`/usr/bin/jq` in the base and repeat envelopes, `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq` in the
copy envelopes; the other path never appears in the same file.

## Failures and retries

None. All six calls exited 0, produced non-empty JSON on stdout, empty stderr, and needed no retry.
There is therefore no second-attempt record: `runs.tsv` has exactly six data lines, one per call.

## Warnings and risks (inference)

- Inference: `analyze` and `inspect` both dispatch to the same `binary_overview` operation
  (`data.operation == "binary_overview"`, `data.predicate_type == "rea.analysis"`,
  `data.confidence == "derived"`, `data.authority == "shipped-artifact"`) and produce the same
  `evidence_id`. Their table rows will therefore carry identical id cells. That is consistent with the
  frozen rule, which compares ids within a verb and states that any verdict value counts as complete,
  but it means an id cell alone does not identify the verb.
- Observation: the frozen pre-freeze probe in `claims.json` (`inspect-binary-layout`) recorded a
  different id (`ev_294a449c...`). So id equality does not extend across all eight verbs; this seat
  measured only `analyze` and `inspect` and says nothing about the other six.
- Inference: because `evidence_id` is stable across path and repetition here, a table whose verdict
  is `content-keyed` for these two verbs cannot distinguish "content keyed" from "id is a constant of
  the tool version"; the counter would see the same outcome either way.

## Artifacts (all under the seat scratch, listed for the L1)

Directory: `/fast/scratch/hyaku/kaidoku-r26/seats/RunAnalyzeInspect/`

- `envelopes/analyze-base.json` 3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb
- `envelopes/analyze-repeat.json` b65e650292b9f475d1c9d029adfe032ce1aed883ef408b594bb293ea7b0d84a6
- `envelopes/analyze-copy.json` be1dd0c4c57dde68d760f06cc00b8afcb8f30a0805a1982e491a1d4339089243
- `envelopes/inspect-base.json` 9421d1f8701987b669c2ca6f1ed5d1343c24b304b6fa06a63bab0b3bdd98eab1
- `envelopes/inspect-repeat.json` f509fcfeb1ab4aa9e530b71e42ff94da6fa822e9c3c4795c1ccb957394c0eaaa
- `envelopes/inspect-copy.json` 62e09a1e8ecb1d2cc06eddc3695799c1f272bcff4224236eccb56edc2576da89
- `envelopes/<verb>-<run>.stderr` (six files) e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- `runs.tsv` d885e43581a7607590aaf3ff62f39468ac000b3210219d06881d3d8b01b05944
- `carrier-before.sha256` 7dde6ebf9481b7368dc55e0708105a8d742367885a271bf0f39e2c2f585fd744
- `carrier-after.sha256` 7dde6ebf9481b7368dc55e0708105a8d742367885a271bf0f39e2c2f585fd744
- `run-one.sh` (the single-call driver used) 70d6b53851950a86e3d2a7f085dd3ddb194e231a616f76740429a8e586f5905c

Nothing was written under `/fast/scratch/hyaku/kaidoku-r26/carrier/`.

## Tooling

No package was installed or upgraded by this seat; `npx -y rea-agents@6.5.0` was already present in
the npx cache and was used as pinned by the claims file.

## Handoff

The envelopes directory path was messaged to `KaidokuR26.RecomputeIds` and `KaidokuR26.CounterC1`:
`/fast/scratch/hyaku/kaidoku-r26/seats/RunAnalyzeInspect/envelopes/`.
