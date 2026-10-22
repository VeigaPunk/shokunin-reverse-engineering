# R26-C1 table runs — verbs `decompile` and `function` (seat RunDecompileFunction)

Date: 2026-10-22. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (read-only for this seat; only this report file was written inside it).
Carrier: /usr/bin/jq, 30,800 B, sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806.
Alternate (copy): /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq, 30,800 B, same sha256.
REA: rea-agents 6.5.0 CLI only, from the npx cache /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents. No MCP device was used. No package was installed or upgraded by this seat.

## Result summary

All six calls succeeded on the first attempt (exit 0, stderr empty). The retry-once path in the driver was armed but never fired; no envelope was edited.

| verb | base id | repeat id | copy id | base==repeat | base==copy | derived verdict |
|---|---|---|---|---|---|---|
| decompile | ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df | ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df | ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df | yes | yes | content-keyed |
| function | ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5 | ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5 | ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5 | yes | yes | content-keyed |

Derived verdict computed with the claims.json `derived_verdict` rule verbatim: no-id if any of the three envelopes lacks a string `.data.evidence_id` starting `ev_`; else unstable if base != repeat; else content-keyed if copy == base; else path-sensitive. Both verbs carry `ev_` ids in all three envelopes (no-id does not apply) and base == repeat (unstable does not apply), so both derive `content-keyed` (observation).

## runs.tsv content

Path: /fast/scratch/hyaku/kaidoku-r26/seats/RunDecompileFunction/runs.tsv (sha256 3d820933ac0870927d39dac4aff8f0f08357552d69c87a26b22cc047622c68b6), tab-separated, header `verb run path argv exit utc_start utc_end envelope_sha256 evidence_id subject_sha256`.

```
verb	run	path	argv	exit	utc_start	utc_end	envelope_sha256	evidence_id	subject_sha256
decompile	base	/usr/bin/jq	decompile /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:08Z	2026-10-22T12:15:14Z	b177af90a49aacde0097dc15df0ea94ee1560e6c5bc38f666e225fc226128f73	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
decompile	repeat	/usr/bin/jq	decompile /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:14Z	2026-10-22T12:15:20Z	779d6ffce7e110c543826a5daae8a2541593dd150895efb20199677d3f1553c3	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
decompile	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	decompile /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:20Z	2026-10-22T12:15:26Z	bc8d40c388801b1f2f31e3cb28c76f62f2f005543f0979037a9f314ec91f42f9	ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
function	base	/usr/bin/jq	function /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:26Z	2026-10-22T12:15:33Z	642c47b3134ed7e56d95c2b82c7c08bac427451c85733ad500edf61aa70418c6	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
function	repeat	/usr/bin/jq	function /usr/bin/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:33Z	2026-10-22T12:15:39Z	40616d4676496c555ee760348d5ea3bae7c642e9ebf23e17eca70e53096829ba	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
function	copy	/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq	function /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output	0	2026-10-22T12:15:39Z	2026-10-22T12:15:45Z	6dafee18478e7b34f77b5f673c2a094a1ddaab79c93937c0c89ac1488f524da5	ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5	e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

Producing commands (one command per row, run strictly one after another, never in parallel), cwd /fast/scratch/hyaku/kaidoku-r26/seats/RunDecompileFunction:

```
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 decompile /usr/bin/jq 0x103fa0 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 decompile /usr/bin/jq 0x103fa0 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 decompile /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 function /usr/bin/jq 0x103fa0 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 function /usr/bin/jq 0x103fa0 --format json --full-output
TMPDIR=$PWD/tmp npx -y rea-agents@6.5.0 function /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq 0x103fa0 --format json --full-output
```

argv strings are exactly the `verbs_argv` entries from .ufo/waves/round-26/claims.json for these two verbs, with `<PATH>` substituted for the run path and nothing else changed. Driver: /fast/scratch/hyaku/kaidoku-r26/seats/RunDecompileFunction/runner.py (sha256 42c481e613e5b612d3d978ade9ea8cd984a2e3bd5d8c1b9f77bbcd1a39ac1d72), which spawns the six calls sequentially via subprocess and appends one TSV row per call.

## Carrier custody across the wave

Before the first call, 2026-10-22T12:15:08Z (observation, file /fast/scratch/hyaku/kaidoku-r26/seats/RunDecompileFunction/before-sha256.txt):

```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq
```

After the last call, 2026-10-22T12:15:45Z (observation, file after-sha256.txt): both lines byte-identical to the above. Neither carrier was modified; the alternate copy was read only.

## Envelopes (sizes and hashes)

Directory: /fast/scratch/hyaku/kaidoku-r26/seats/RunDecompileFunction/envelopes/ (each stdout saved as `<verb>-<run>.json`, each stderr as `<verb>-<run>.stderr`; all six stderr files are 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855).

| file | bytes | sha256 | ok | evidence_id | subject sha256 | contains the path it ran on |
|---|---|---|---|---|---|---|
| decompile-base.json | 13032 | b177af90a49aacde0097dc15df0ea94ee1560e6c5bc38f666e225fc226128f73 | true | ev_03d786…014df | e815…7806 | yes (/usr/bin/jq) |
| decompile-repeat.json | 13032 | 779d6ffce7e110c543826a5daae8a2541593dd150895efb20199677d3f1553c3 | true | ev_03d786…014df | e815…7806 | yes (/usr/bin/jq) |
| decompile-copy.json | 13067 | bc8d40c388801b1f2f31e3cb28c76f62f2f005543f0979037a9f314ec91f42f9 | true | ev_03d786…014df | e815…7806 | yes (alternate path) |
| function-base.json | 840975 | 642c47b3134ed7e56d95c2b82c7c08bac427451c85733ad500edf61aa70418c6 | true | ev_b2b7e9…488b5 | e815…7806 | yes (/usr/bin/jq) |
| function-repeat.json | 840975 | 40616d4676496c555ee760348d5ea3bae7c642e9ebf23e17eca70e53096829ba | true | ev_b2b7e9…488b5 | e815…7806 | yes (/usr/bin/jq) |
| function-copy.json | 841010 | 6dafee18478e7b34f77b5f673c2a094a1ddaab79c93937c0c89ac1488f524da5 | true | ev_b2b7e9…488b5 | e815…7806 | yes (alternate path) |

The subject sha256 column was read from `.data.subject.digest.sha256` in all six envelopes (the first-present rule); `.data.normalized_result.artifact.sha256` is absent in all six (for `decompile` the normalized_result is a pseudo-code string, for `function` it is an object with a `procedure` key and no `artifact` key).

## Field-level differences between the three envelopes of one verb

Flattening each envelope to leaf paths and comparing base, repeat and copy gives exactly two differing leaves per verb (observation):

- `/data/subject/local_path`: `/usr/bin/jq` for base and repeat, `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq` for copy.
- `/meta/duration`: `5227ms` / `5510ms` / `5607ms` for decompile and `5847ms` / `5702ms` / `5413ms` for function.

Everything else, including `.data.evidence_id`, `.data.subject.digest.sha256` and the analysis payload, is byte-identical across the three runs of a verb. This is why the envelope file hashes differ while the evidence ids agree.

## Payload sanity (observation)

Both verbs resolved the frozen address 0x103fa0 to the same Ghidra procedure `FUN_00103fa0` with a real body (`available: true`, provider `ghidra` 12.1.4, `predicate_type` `rea.analysis`, `operation` `procedure_pseudo_code` for decompile and `analyze_function` for function, `confidence` `observed`). The decompile payload opens with `int FUN_00103fa0(undefined8 param_1)` and calls `jq_start()` / `jq_next()`.

## Failures and routed defects

Failures: none. All six calls returned exit 0 with empty stderr; no retry was needed, so there is no error text to report.

Routed defects: none of the seven routed defects in corpus/lessons/round-25-verifier-spotcheck.md (`## Routed defects`) is answered or contradicted by these two verbs' envelopes: defect 3 concerns the frozen counter instruments, defects 1, 2, 5, 6 and 7 concern lane documents, and defect 4 concerns a vyper carrier page count. Defect 7 (write new text with spaced tokens) applies to this report, which uses spaced words throughout.

## Artifacts under this seat (sha256)

```
d135e480f0b5bcb3bfc2fddf6a367e2f6bb7a91d9fe40608c79ae149f5cb0449  after-sha256.txt
8215718d65fa8d0db5793531377700a5a5ba400659829ed64de215e908a3f897  before-sha256.txt
b177af90a49aacde0097dc15df0ea94ee1560e6c5bc38f666e225fc226128f73  envelopes/decompile-base.json
bc8d40c388801b1f2f31e3cb28c76f62f2f005543f0979037a9f314ec91f42f9  envelopes/decompile-copy.json
779d6ffce7e110c543826a5daae8a2541593dd150895efb20199677d3f1553c3  envelopes/decompile-repeat.json
642c47b3134ed7e56d95c2b82c7c08bac427451c85733ad500edf61aa70418c6  envelopes/function-base.json
6dafee18478e7b34f77b5f673c2a094a1ddaab79c93937c0c89ac1488f524da5  envelopes/function-copy.json
40616d4676496c555ee760348d5ea3bae7c642e9ebf23e17eca70e53096829ba  envelopes/function-repeat.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  envelopes/{decompile,function}-{base,repeat,copy}.stderr (6 files, 0 bytes each)
b7928d468ecc1b671ad007851b12d793f09a842e1a08e40c66787143286eb527  run-log.json
42c481e613e5b612d3d978ade9ea8cd984a2e3bd5d8c1b9f77bbcd1a39ac1d72  runner.py
3d820933ac0870927d39dac4aff8f0f08357552d69c87a26b22cc047622c68b6  runs.tsv
```

(tmp/ holds only the Node compile cache created by the runs.)

## Risks and unknowns

- Observation: the `copy` envelopes embed the alternate path in `.data.subject.local_path`, so the envelope bytes are path-dependent even though the evidence id is not. A future counter that keys on envelope bytes rather than `.data.evidence_id` would mis-read these rows; the claims.json rule keys on the id, so it is unaffected.
- Unknown: whether the evidence id would stay stable across a different Ghidra or REA build. This round pins 6.5.0 and one provider version only, as the claim states.
- Observation: the sibling seat `RunReadBytesLayout` measured `path-sensitive` for `inspect-binary-layout` at the same pin and carrier, so the eight-verb table will not be uniformly `content-keyed`. That is within the claim (any verdict value counts as complete); it is flagged so the L1 does not assume a uniform verdict.

Tooling: no tool was installed, upgraded or downgraded by this seat; the runs used the pre-existing npx-cached rea-agents 6.5.0. All pacman transactions remain paused host-wide.
