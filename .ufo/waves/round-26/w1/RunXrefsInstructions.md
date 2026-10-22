# R26-C1 seat report: RunXrefsInstructions (verbs xrefs, instructions)

Seat: `KaidokuR26.RunXrefsInstructions`. Round 26, attempt 1, wave 1. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (base `a0639d8e61e486e2a716ff94cddd89a73200a02c`).
Scope: only the two verbs `xrefs` and `instructions` of the frozen eight-verb list in `.ufo/waves/round-26/claims.json` (`claims[0].verbs_argv`).

## 1. Verdict summary

| verb | base id | repeat id | copy id | base==repeat | base==copy | derived verdict |
|---|---|---|---|---|---|---|
| xrefs | ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c | same | same | yes | yes | content-keyed |
| instructions | ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b | same | same | yes | yes | content-keyed |

Derived-verdict rule applied verbatim from `claims[0].rules.derived_verdict`: all six envelopes carry a string `.data.evidence_id` starting with `ev_`, so `no-id` does not apply; base id equals repeat id for both verbs, so `unstable` does not apply; copy id equals base id for both verbs, so the verdict is `content-keyed` and `path-sensitive` is not reached. Observation, not inference: each comparison is over the literal id strings printed in `runs.tsv`.

## 2. Carrier integrity (sha256 before and after)

Command: `sha256sum /usr/bin/jq /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`; sizes from `stat -c '%n %s'`.

- Before, 2026-10-22T12:11:42Z (exit 0):
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq`
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`
  Sizes: `/usr/bin/jq 30800`, `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 30800`.
- After, 2026-10-22T12:12:48Z (exit 0): both lines byte-identical to the above. The alternate copy is byte-identical to the base carrier and neither file changed during the wave.
- Every envelope's subject digest equals the carrier sha256 `e8156675...7806`, so each run read the pinned bytes.

## 3. Invocations

Runner: `/fast/scratch/hyaku/kaidoku-r26/seats/RunXrefsInstructions/run_one.sh` (sha256 `424f8ea8de1b1e926c51809e7651e4aa27d4a7618285d3efe377e067d893c83e`), which runs one call at a time and captures stdout to `envelopes/<verb>-<run>.json`, stderr to `envelopes/<verb>-<run>.stderr`, and prints one TSV line with the exit code and UTC start/end.

Form used, matching `claims[0].invocation`:
`TMPDIR=/fast/scratch/hyaku/kaidoku-r26/seats/RunXrefsInstructions/tmp npx -y rea-agents@6.5.0 <verb> <PATH> 0x103fa0 --format json --full-output`
with `PATH` = `/usr/bin/jq` for base and repeat, and `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq` for copy. The argv column of `runs.tsv` records the exact expanded argv per row.

Version pinning: the npx cache used is `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`, whose `package.json` reports `"version": "6.5.0"` (read-only check, exit 0). The 6.7.0 tree `/home/vgpnk/.npm/_npx/a1722018f28f9df2/` was not used by these runs; its directory mtime stayed at 2026-10-22 07:46:32 -0300 while the 6.5.0 tree mtime advanced to 09:12:39 -0300 (12:12:39Z), the minute of the last run. Observation. No install or upgrade was performed by this seat; no tool was added or changed.

## 4. runs.tsv content

File: `/fast/scratch/hyaku/kaidoku-r26/seats/RunXrefsInstructions/runs.tsv`, sha256 `2c6783ea51c14a13def632099b5c3a8be030a1cb21555d9a65feb568e4d369b1`.
Header: `verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256`.

```
xrefs	base	/usr/bin/jq	xrefs /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:11:50Z	2026-10-22T12:11:57Z	125ee6d20bda824ce80c16a9b061305dc8e4f1ac6b803330f2e7b024c59130df	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
xrefs	repeat	/usr/bin/jq	xrefs /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:12:05Z	2026-10-22T12:12:11Z	dd68e7835954f0845b623c22848be8039c3a2e697738d7513ef171e47a17d664	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
xrefs	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	xrefs /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:12:14Z	2026-10-22T12:12:20Z	6587e077e6d495ba0a4d8a493d2e923d8301d5e35b93f4cdfa8f9eeeacaba675	ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
instructions	base	/usr/bin/jq	instructions /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:12:22Z	2026-10-22T12:12:28Z	c8852498ce38f9c3a5f353aec00fb72e7abef7bc9a8644d753bb33cac411fb11	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
instructions	repeat	/usr/bin/jq	instructions /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:12:30Z	2026-10-22T12:12:37Z	00da0fb3d1b8b1b13ab37db3687c490b47a60859658738267d1567bedf7f57ad	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
instructions	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	instructions /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:12:39Z	2026-10-22T12:12:45Z	f87583348512577e86438163262248c95043b8083b9ba569078a691a84592757	ev_b20a0f25f149070fc49cf79cce749a34fa359d123a7a674deca7c464a1125f8b	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

All six exits are 0. No retry was needed, so no second attempt exists for any call.

## 5. Envelope inventory

Envelopes directory: `/fast/scratch/hyaku/kaidoku-r26/seats/RunXrefsInstructions/envelopes/`.

| file | bytes | sha256 | ok | evidence_id |
|---|---|---|---|---|
| xrefs-base.json | 3089 | 125ee6d20bda824ce80c16a9b061305dc8e4f1ac6b803330f2e7b024c59130df | true | ev_d591ef8c…96b27c |
| xrefs-repeat.json | 3089 | dd68e7835954f0845b623c22848be8039c3a2e697738d7513ef171e47a17d664 | true | ev_d591ef8c…96b27c |
| xrefs-copy.json | 3124 | 6587e077e6d495ba0a4d8a493d2e923d8301d5e35b93f4cdfa8f9eeeacaba675 | true | ev_d591ef8c…96b27c |
| instructions-base.json | 22977 | c8852498ce38f9c3a5f353aec00fb72e7abef7bc9a8644d753bb33cac411fb11 | true | ev_b20a0f25…a1125f8b |
| instructions-repeat.json | 22977 | 00da0fb3d1b8b1b13ab37db3687c490b47a60859658738267d1567bedf7f57ad | true | ev_b20a0f25…a1125f8b |
| instructions-copy.json | 23012 | f87583348512577e86438163262248c95043b8083b9ba569078a691a84592757 | true | ev_b20a0f25…a1125f8b |

Stderr files: six files, each 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty-file digest).

Envelope sha256 differs between base and repeat only because of a non-identity field. Diff of `jq -S` output, base vs repeat: one line, `"duration": "6174ms"` vs `"duration": "5457ms"` for xrefs, `"5218ms"` vs `"5533ms"` for instructions. Diff base vs copy: the same duration line plus `"local_path": "/usr/bin/jq"` vs `"/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq"`. The `evidence_id` and subject digest are unchanged. Observation from `diff <(jq -S . a) <(jq -S . b)`.

Diagnostics (not gating, per `claims[0].rules.diagnostics_not_gating`): each of the six envelopes' text contains the path it was run on. Checked with `grep -qF <path> <file>`, exit 0 for all six.

## 6. Failures

None. No call returned a non-zero exit, produced stderr output, or produced an envelope without a string `ev_`-prefixed `.data.evidence_id`. Consequently no retry was performed and no second-attempt row exists.

## 7. Artifacts (all outside the lane; the L1 integrates and commits)

Directory `/fast/scratch/hyaku/kaidoku-r26/seats/RunXrefsInstructions/`:

- `runs.tsv` sha256 `2c6783ea51c14a13def632099b5c3a8be030a1cb21555d9a65feb568e4d369b1`
- `run_log.tsv` sha256 `09d3ad9db51bc503aaa5df97f3fd9e39a1b03303b421c2971fb3b3b0592b4aff` (raw per-call argv/exit/times as printed by the runner)
- `run_one.sh` sha256 `424f8ea8de1b1e926c51809e7651e4aa27d4a7618285d3efe377e067d893c83e`
- `envelopes/xrefs-base.json` sha256 `125ee6d20bda824ce80c16a9b061305dc8e4f1ac6b803330f2e7b024c59130df`
- `envelopes/xrefs-repeat.json` sha256 `dd68e7835954f0845b623c22848be8039c3a2e697738d7513ef171e47a17d664`
- `envelopes/xrefs-copy.json` sha256 `6587e077e6d495ba0a4d8a493d2e923d8301d5e35b93f4cdfa8f9eeeacaba675`
- `envelopes/instructions-base.json` sha256 `c8852498ce38f9c3a5f353aec00fb72e7abef7bc9a8644d753bb33cac411fb11`
- `envelopes/instructions-repeat.json` sha256 `00da0fb3d1b8b1b13ab37db3687c490b47a60859658738267d1567bedf7f57ad`
- `envelopes/instructions-copy.json` sha256 `f87583348512577e86438163262248c95043b8083b9ba569078a691a84592757`
- `envelopes/*.stderr` six files, each 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `tmp/` REA scratch dir (TMPDIR target), not an artifact to commit.

This report is the only file this seat wrote inside the lane.

## 8. Risks and limits

- Observation: both verbs are content-keyed at 6.5.0 for this carrier and this single address `0x103fa0`. The claim as frozen says nothing about other carriers, other pins, other addresses, other parameters, MCP sessions, or error envelopes; this seat measured neither.
- Observation: the two verbs' ids differ from each other, so the id is verb-scoped as well as content-scoped at this pin.
- Risk for the L1: the counter `tools/round-26/c1-id-identity.py` reads envelopes from Git objects at a revision, so these six envelopes must be committed under `corpus/evidence/round-26/c1/envelopes/` before the counter is run. This seat did not write there (lane read-only for the wave).
- Unknown: whether the six envelopes' other six verbs (owned by sibling seats) agree on their ids; not this seat's scope.
