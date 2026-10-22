# R27-C1 prediction — analyze, inspect, inspect-binary-layout at rea-agents 6.5.0

Seat PredictWholeFile. Prediction made from code before any round-27 envelope was read or
produced: I read nothing under `corpus/evidence/round-27` or `seats/Run*`, and ran no REA call.
Package root P = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(`package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`,
6.5.0). Corroboration uses the round-26 c1 envelopes (`git show main:...`).

## Prediction table (every row is inference, not observation)

| Verb | Prediction for the R27 renamed run | Hashed fields that could carry directory, file name or extension | file:line evidence | Confidence |
|---|---|---|---|---|
| analyze | rename-sensitive: renamed id differs from base; base == repeat | `normalized_result.document` only, because the Ghidra Program name embeds the caller's *extension*; `parameters` is `{}`; `subject.name` / `subject.local_path` are excluded | P/dist/cli/coreBinaryCommands.js:88; P/dist/application/WorkflowEvidence.js:26-41; P/dist/domain/evidence.js:156-182, 260-264; P/dist/ghidra/GhidraTargetSnapshot.js:13-14, 76-78; P/dist/ghidra/GhidraClient.js:441; P/dist/ghidra/GhidraLauncher.js:329-330; P/bridge/ghidra/ReaGhidraBridge.java:1972-1976 | high (medium on the extension step, see U1) |
| inspect | rename-sensitive: same mechanism, same predicted id as analyze | same | P/dist/cli/coreBinaryCommands.js:98; rest as above | high (medium on U1) |
| inspect-binary-layout | rename-sensitive: renamed id differs; a directory-only rename would also differ | `parameters.path`, `normalized_result.artifact.path`, `locations[0].path` — the caller path verbatim | P/dist/application/binaryDiagnostics/BinaryLayoutService.js:55-70; P/dist/domain/native/binaryLayout.js:17-19; P/dist/native/pwntools/PwntoolsLayoutProvider.js:15-20; P/dist/domain/evidence.js:156-182 | high |

Expected counter verdicts: analyze rename-sensitive, inspect rename-sensitive,
inspect-binary-layout rename-sensitive; base == repeat for all three.

## Observed facts (producing command → excerpt → exit, UTC 2026-10-22)

O1. `sed -n 154,183p P/dist/domain/evidence.js` (exit 0, 15:00:40Z). `semanticProjection`
hashes `subject.digest`, `subject.format`, `subject.architecture`, then `provider`,
`analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`,
`normalized_result`, `confidence`, `authority`, `environment`, `limitations`,
`relationship_coverage`, `locations`, `evidence_links`; `subject.name` and
`subject.local_path` are built at :211-212 / :260-264 and never projected. Comment at :181:
"Hash semantic content, including raw results and excluding display-subject fields."

O2. `sed -n 86,100p P/dist/cli/coreBinaryCommands.js` (exit 0, 15:00:46Z). Both verbs call
`runDirectAnalysis(args.path, "binary_overview", {}, ...)` (analyze :88, inspect :98), so
`parameters` is `{}` for both. `sed -n 250,262p P/dist/application/DirectAnalysis.js`
(exit 0, 15:00:46Z) passes `openedTarget`, `input.arguments`, the overview result, the
profile and upstream limitations to `createWorkflowEvidence`.

O3. `sed -n 25,45p P/dist/application/WorkflowEvidence.js` (exit 0, 15:00:46Z): workflow
evidence has `parameters: input.parameters`, `result: input.result`, no raw result, no
environment, and `locations` only for `batch_decompile`.

O4. `sed -n 8,17p` + `sed -n 75,80p P/dist/ghidra/GhidraTargetSnapshot.js` (exit 0,
15:00:40Z): the suffix comes from `safeExtension(sourcePath)` and the snapshot name is the
literal `target-` plus the first twelve hex characters of the sha256 plus that suffix, and
`safeExtension` returns the caller's
extension only when it matches `/^\.[A-Za-z0-9]{1,12}$/`, else `".bin"`. GhidraClient.js:441
passes `targetPath: this.#snapshotPath` to the launcher; GhidraLauncher.js:329-330 passes it
to `-import`. `sed -n 1970,1978p P/bridge/ghidra/ReaGhidraBridge.java` (exit 0, 15:00:40Z):
`listDocuments` returns `currentProgram.getName()`. The bridge never renames the Program
(only function/label `setName` at :1459, :1908-1911). So the document name is
`target-<sha12><extension-of-caller-path>`: the directory and file name never reach it, the
extension does.

O5. Round-26 c1 envelopes, `git show main:... | jq -c` (exit 0, 15:01:09Z):
`analyze-base` id `ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328`,
`document` `target-e815667571d0.bin`, `parameters` `{}`, `environment` null, `raw_result`
null, `locations` `[]`; `analyze-copy` (same file name, directory
`/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq`) keeps the same id and document
(observation: directory and file name do not perturb the id when the extension is absent).
`inspect-binary-layout-base` id
`ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd` with
`parameters.path`, `normalized_result.artifact.path` and `locations[0].path` all `/usr/bin/jq`;
`inspect-binary-layout-copy` (same bytes, other directory) id `ev_52da4b3d...` — differs.

O6. Counterfactuals under the 6.5.0 rule with `python3 -I -B tools/round-26/recompute-ids.py`
on mutated copies of those envelopes (UTC 15:02:04Z–15:02:20Z):
- subject.name and subject.local_path set to the renamed jq values only: `MATCH`,
  recomputed `ev_14f9d92f...`, "path-bearing fields in the hashed projection: none", exit 0.
- `normalized_result.document` changed `target-e815667571d0.bin` → `target-e815667571d0.dat`
  only: `MISMATCH`, recomputed
  `ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2`, exit 1.
- `parameters.path`, `normalized_result.artifact.path` and `locations[0].path` set to the
  renamed jq path only: `MISMATCH`, recomputed
  `ev_43dec6e6a261a6c3ea6dc02cc889337d653d16f0d7d37c78051cd4a2378e45c6`, exit 1; the tool
  lists `/parameters/path`, `/normalized_result/artifact/path`, `/locations/0/path` as
  path-bearing hashed fields (plus the content-derived
  `/normalized_result/linkage/interpreters/0/display` = `/lib64/ld-linux-x86-64.so.2`).

O7. `node -e '...extname...'` (exit 0, 15:02:35Z): extname of `/usr/bin/jq`,
`/usr/bin/tinyxxd`, the renamed jq copy and the renamed tinyxxd copy is
`["","",".dat",".dat"]`. Base snapshots therefore end `.bin`; the R27 renamed copies end
`.dat`.

## Inference

I1. analyze: the renamed run's id differs from base because the single differing hashed field
is `normalized_result.document`, `target-e815667571d0.bin` → `target-e815667571d0.dat`. If the
renamed copy had kept a name without extension, the verb would stay content-keyed.
I2. inspect: identical code path and parameters, so the same verdict and the same predicted
id as analyze on the same carrier.
I3. inspect-binary-layout: the caller path is hashed verbatim in three fields, so the renamed
run differs; unlike analyze/inspect, this verb is path-keyed at every component.
I4. Predicted ids for the jq rows, assuming the renamed run reproduces the round-26 projection
apart from `document`: analyze and inspect renamed `ev_a60580a9d89e...`; layout renamed
`ev_43dec6e6a261...`. Base/repeat keep `ev_14f9d92f...` (analyze, inspect) and
`ev_294a449c...` (layout) if the Ghidra version and environment are unchanged.
I5. Counter impact: the layout pair is path-keyed by construction; analyze and inspect depend
on I1. The C1 claim counts any verdict, so neither outcome changes completeness.

## Unknowns

U1. Not observed: whether Ghidra's import preserves a non-fallback extension in the Program
name. Only `.bin` (the fallback) is observed in round-26, and no rename step exists in the
bridge. If Ghidra normalized the imported name, the `.dat` copy would keep the same document
and analyze/inspect would be content-keyed (U1 is the only fork for those two verbs).
U2. No txt prediction for tinyxxd's exact ids: round-26 holds no tinyxxd overview projection to
perturb; the mechanism is identical.
U3. The renamed `.dat` import must succeed for the row to exist; loader choice is content-based
in the launcher (no extension check observed), but I did not run Ghidra.

## Artifacts (sha256)

All under `/fast/scratch/hyaku/kaidoku-r27/seats/PredictWholeFile/`:
`predict-evidence.txt` `5293d8f7f1637d147c1d3bd50c4e1bcd489e7b6121e70544c494297399f8654a`;
`prediction-counterfactual.txt` `9f0318790a17e7da01208e36e62850d51cc02346cc1a7479cf3534acee6f47b6`;
`analyze-base.json` `3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb`;
`cf-subject.json` `eb32edc8e7224b909fb88412767af050c95e4c499a7d753b4849dc4f37188c7a`;
`cf-document.json` `4c06a3a3a4acbc3dbd150b5a7ffcd2ce886aae9d9ef2138eacd46a3315d0cce4`;
`layout-base.json` `4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f`;
`cf-layout-renamed.json` `36d2b0ccfaca819fa1db19206d8e9c73c722683203cb2a2650dbac699592f28b`.
No tools installed or upgraded; no REA invocation; no lane write other than this report.
