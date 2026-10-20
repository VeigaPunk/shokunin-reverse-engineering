# ScoutWasmSchema — REA wasm verb schemas, manifests, detail and WABT gate (round 20, w1)

Seat: `KaidokuR20.ScoutWasmSchema-2` (read-only scout, leaf). Report clock: `2026-10-20T17:51:38-03:00`
(`date -Iseconds`, immediately before this write). No installs/upgrades. Scratch (captures + fixtures) lives in
`/tmp/kr20-scout-wasm` and `/tmp/kr20-scout-wasm-fixtures.d8LtAj` (mktemp); nothing was written under the lane
except this report. No Go toolchain binary was executed; no REA analyze/decompile ran on Go files.

Labels: **[O]** observed from executed command output/bytes; **[I]** inference from source read; **[U]** unknown.

## 1. Commands executed and full-output digests

All from `npx -y rea-agents@6.5.0` (`rea@6.5.0`), cwd `/tmp/kr20-scout-wasm`. Every stderr file was 0 bytes
unless noted; error JSON arrives on **stdout** with exit 1.

| # | argv (exact) | exit | bytes | lines | sha256 of full stdout |
|---|---|---|---|---|---|
| 1 | `npx -y rea-agents@6.5.0 inspect-wasm-artifact --schema` | 0 | 468 | 22 | `19e52a729c74720351850c23db79e7e37f5815e2d970fc523af4bdd88d636a29` |
| 2 | `npx -y rea-agents@6.5.0 compare-wasm-interfaces --schema` | 0 | 220 | 8 | `d28e91c8537feab7ce613e582602b4771277603bc7cc22b534eadff117207dc1` |
| 3 | `npx -y rea-agents@6.5.0 inspect-wasm-artifact --llms-full` | 0 | 460 | 16 | `490d8f149135170e759a94bdc0294d20b6df10ea421bc76d6e2508748952997f` |
| 4 | `npx -y rea-agents@6.5.0 compare-wasm-interfaces --llms-full` | 0 | 316 | 9 | `48ec6f2ad2931a4908b0dbd41263c58e347f32ca7713d8ccc7203e1ab2a7a6f7` |
| 5 | `npx -y rea-agents@6.5.0 --llms-full` | 0 | 79524 | 2260 | `54c2fecd8ae358ffac3ffa98a8db74f77073feca067694f32c6c0c9f2c6a1061` |
| 6 | `npx -y rea-agents@6.5.0 --llms` | 0 | 17217 | 161 | `8c08f792b61d3d38f59e79e17341ea46dd7706b80bfdc500adb4324a7bfcd176` |
| 7 | `npx -y rea-agents@6.5.0 inspect-wasm-artifact --llms` | 0 | 299 | — | `0a909f10177a79349fc32d2d4feb165a643ac873193365bf1beafb8663ccf1a9` |
| 8 | `npx -y rea-agents@6.5.0 inspect-wasm-artifact --schema --format json` | 0 | 687 | — | `e5ce6f64bd8067e0be94441295b51e04e3ca24da9679729e87b7072504a92091` |
| 9 | `npx -y rea-agents@6.5.0 inspect-wasm-artifact --help` | 0 | 929 | 21 | `542832bc39be5188afb3ab2349a71809ee21cba4f18afde6710e11d9e872a0f1` |
| 10 | `npx -y rea-agents@6.5.0 compare-wasm-interfaces --help` | 0 | 876 | 17 | `9783f69f663cb8e676ca7b984ddfde67defa8292386bcb7dc1c12a2203743e38` |

Sections of the top manifest (capture 5): `# rea compare-wasm-interfaces` at `top-llms.out:285`,
`# rea inspect-wasm-artifact` at `top-llms.out:1269` (descriptions at :287 and :1271) **[O]**.
Per-command `--llms-full` is byte-identical to that section **minus the single trailing blank line** the
section extractor keeps (461 vs 460 B; 317 vs 316 B; `diff -u` showed only that line) **[O]**.
Per-command `--llms` is *not* the section: it prints a filtered top index (`# rea` + one command row +
`Run rea --llms-full for full manifest…`, 299 B) **[O]** — the help text at `iw-help.out:17` lists
`--llms, --llms-full` as one option but their outputs differ.

Run captures (Evidence, all under `/tmp/kr20-scout-wasm/`; not delivered to the lane):

| capture | purpose | exit | bytes | sha256 |
|---|---|---|---|---|
| `nowabt.json` | env unset | 1 | 559 | `81102a41126bd8d097dc2d4d0d77879b55f743d1b8731292fb84d2b171eeafee` |
| `inspect-a.json` | `a.wasm` (5-entry interface) | 0 | 7673 | `99846430d37f7e4a547c802fdf3aefe59630f287e66034a0d1d08f5a71402972` |
| `inspect-b.json` | `b.wasm` | 0 | 7555 | `18c9d1ad943caf86e5219bf0f93529041855110d37074566adfaae90ba14d216` |
| `inspect-rel.json` | relative path (same bytes as `inspect-a`) | 0 | 7673 | `99846430…2972` |
| `inspect-detail.json` | `--detail summary` on CLI | 1 | 63 | `4966d7e6e55a5eb1c7ccbd489aad1400ae955df127c8b4824e7bf07ddb68ae78` |
| `inspect-badwasm.json` | `a.wat` text as wasm | 1 | — | `24109cb339ca393b4d091c026bd1f5e295369af0c0a22f14361ada3e2ffcccdf` |
| `inspect-emptybin.json` | empty `REA_WABT_BIN_DIRECTORY` dir | 1 | — | `af725fe7d88d157b8156cb83ff943e5a4e8733f38b5210514e6c01a6c8682b3c` |
| `inspect-wrongver.json` | three tools symlinked to `/usr/bin/true` | 1 | — | `29b7aa1a9f284815d1762216518c3ceaecf55367ff312a8e22e804149712e573` |
| `inspect-17glue.json` | 17 `--glue_paths` | 1 | — | `5ff92eb5175e35635c05cafa2584612767c2131c08d914e84692a3ea4fcea928` |
| `inspect-big.json` | 9 MiB input | 1 | — | `8029395dd7d5e98aef7a7684f6a51cb9fd037d475d9aeedcac4577e13a776599` |
| `inspect-trunc.json` | first 50 B of `a.wasm` | 1 | — | `0df430cfcd7930dfc558b62d05b991fd1af5955620406fed44decbeecf7f1b65` |
| `inspect-dup.json` | duplicate `env.seed` imports | 0 | — | `8a5c155fc3bfb4cc824cc43810c7debd2c2ca4f3aeff9257289aefc29228316f` |
| `cmp-ab.out.json` | a vs b, `both` | 0 | 4877 | `de98bf3a45050c0ce7eb3fe9db83aad8a27ced542151824e46586d0b0573c65a` |
| `cmp-self.out.json` | a vs a, `both` | 0 | 4703 | `330cb2350207a5f11b1ffbda8e87b242ccff5621724200d3b3894dc0bb89b01d` |
| `cmp-self-full.json` | same, `--full-output` | 0 | 4785 | `0ac3eb7f4be04976103cc88115cc672f3cf46b9c267ba6a33c95988f6d7cb28f` |
| `cmp-inline.out.json` | same JSON inline instead of file | 0 | 4703 | `330cb235…b01d` (identical) |
| `cmp-imports.out.json` | a vs b, `imports` | 0 | — | `29498a858f076862896e6b1022e9b21ad780b4680a1d297e5d8978c1621d72bf` |
| `cmp-dup.out.json` | duplicate imports vs itself | 0 | 3505 | `59cb197a4043a94c4664da867d5454367bb3fdb3554c3d6fe4f25a28085edeac` |
| `cmp-noscope.out.json` | scope omitted | 1 | — | `a85b5907af2a0295a6fbe0a3a276679172da1155df69ed4e8b55342b345ce5e8` |
| `cmp-retained.out.json` | retained-evidence ref on CLI | 1 | — | `bc93bc1e5d7d7e5ad0389dc1a7e621914d6d81f11ab3d3d56c90a2a1ef5357fa` |
| `cmp-tampered.out.json` | left `artifact.sha256` altered | 1 | — | `50e497c0646ebf5805ddf5f113572fd49a0dd7b9e298c56f744a966af403e604` |
| `cmp-nr.out.json` | left = bare `normalized_result` | 1 | 2471 | `877a721df5c4b7e54209af42b3680e55be09559f55ae7762c4eac2f6fc8b0e88` |
| `cmp-wrongop.out.json` | left = compare Evidence | 1 | 371 | `61b07b9da08b536336854472880e333be64fc91c3db527934eb308b64f4c3ac2` |
| `cmp-extra.out.json` | extra `detail` key in input | 1 | 321 | `574d82e3c92febd4b667037973325d400d6c948bce67e45e7ca37d28193aca41` |
| `caps.json` | `capabilities --format json` | 0 | 23831 | `3ca959ade21d073aa8df53e8f1d56be6fd958d59b4a3b041566085bdd24d4b06` |

Fixtures (synthesized, not shipped carriers): `a.wasm` 87 B sha256 `7d8313f96cc49de89a11f69f79e69289692b8cdb12a1654ab48304378aff588f`;
`b.wasm` 93 B; `dup.wasm`; built with the contract-path `wat2wasm` 1.0.42. Real-carrier coverage is the sibling
`ScoutWasmCarriers.md` seat, not this one.

## 2. `inspect-wasm-artifact --schema` (capture 1, verbatim, 468 B)

```yaml
args:
  type: object
  properties:
    path:
      type: string
      description: Local WASM artifact
  required[1]: path
  additionalProperties: false
options:
  type: object
  properties:
    glue_paths:
      description: Selected local JavaScript glue paths
      type: array
      items:
        type: string
    candidate_paths:
      description: Explicit local WASM candidates
      type: array
      items:
        type: string
  additionalProperties: false
```

`--schema --format json` (capture 8) is the same object in JSON (`{"args":…,"options":…}`), i.e. the global
format flag applies to schema output **[O]**.

What the schema **omits** versus the shipped contract **[O schema vs source]**:

- no `detail` (MCP-only, see §5); no `maxItems: 16` and no absolute-path constraint, both enforced by the service
  (`dist/domain/wasm/wasmArtifact.js:12-15`), and observed as a refusal (`17 --glue_paths` →
  `invalid_request … {"path":["glue_paths"],"reason":"out_of_range","maximum":16}`, exit 1) **[O]**.
- no output schema at all: nothing in captures 1/3 describes the Evidence envelope or `normalized_result`.

Observed input behaviour beyond the schema: CLI resolves `path`/`glue_paths`/`candidate_paths` with
`path.resolve` (`dist/cli/wasmCommands.js:46-49`) so a relative `a.wasm` produced the same Evidence bytes as the
absolute path (`inspect-rel.json` ≡ `inspect-a.json`, both sha `99846430…`) **[O]**; the service still requires
absolute strings (`WasmArtifactService.js` path issues) — with the CLI that check can only fail for glue paths
containing something `resolve` cannot fix, i.e. effectively never **[I]**.

## 3. `compare-wasm-interfaces --schema` (capture 2, verbatim, 220 B)

```yaml
args:
  type: object
  properties:
    input:
      type: string
      description: Inline JSON or input file containing left/right complete Evidence and required scope
  required[1]: input
  additionalProperties: false
```

No `options` block and no output schema **[O]**. The nested input shape is invisible here; from
`dist/contracts/wasm/wasmComparisonContracts.js:6-13` it is a **strictObject**:

```
{ left:  <complete inspect_wasm_artifact Evidence> | {kind:"retained-evidence", evidence_id:"ev_<64hex>"},
  right: <same>,
  scope: "imports" | "exports" | "both" }
```

`parseCliJsonInput` accepts inline JSON first, else a JSON file path (`dist/cliJsonInput.js:8-15`); inline and file
forms produced byte-identical output (sha `330cb235…`) **[O]**. `left`/`right` accept the *complete Evidence*, not
`normalized_result`: a bare `normalized_result` was rejected with 18 `missing_argument` issues for
`evidence_id`, `subject`, `provider`, `analysis_profile`, `predicate_type`, `operation`, … (exit 1) **[O]**.
A retained reference cannot resolve in CLI (no session): `evidence_integrity_mismatch`, message
"Evidence ev_f2bfc192… is not retained in this session…" (exit 1) **[O]**. A non-`inspect_wasm_artifact`
Evidence is rejected with `invalid_value` "Expected complete inspect_wasm_artifact Evidence" (exit 1) **[O]**.
An extra top-level key `detail` is `unknown_argument` (exit 1) **[O]**. Missing `scope` →
`invalid_value`, `expected:["imports","exports","both"]` (exit 1) **[O]**.

## 4. `--llms-full` sections (captures 3 and 4, verbatim)

inspect-wasm-artifact (16 lines, 460 B; top manifest at `top-llms.out:1269`):

```md
# rea inspect-wasm-artifact

Inspect an explicit local WASM artifact with WABT

## Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `string` | yes | Local WASM artifact |

## Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--glue_paths` | `array` |  | Selected local JavaScript glue paths |
| `--candidate_paths` | `array` |  | Explicit local WASM candidates |
```

compare-wasm-interfaces (9 lines, 316 B; top manifest at `top-llms.out:285`):

```md
# rea compare-wasm-interfaces

Compare core WASM interfaces from two exact inspection Evidence records

## Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input` | `string` | yes | Inline JSON or input file containing left/right complete Evidence and required scope |
```

Lossiness **[O]**: neither section names the output fields, the global flags (`--format`, `--full-output`,
`--filter-output`, `--token-*`, `--schema`), the `detail` option, or `REA_WABT_BIN_DIRECTORY`. The token "WABT"
appears only in the inspect title/description. The help output (captures 9/10) discloses the global flags but
still not `detail` or the env var; `--help` never lists an output schema.

## 5. Detail options

- **MCP only.** `inspect_wasm_artifact`'s contract input adds `detail: analysisDetailSchema.unwrap().optional()`
  (`dist/contracts/wasm/wasmToolContracts.js:8`); MCP output is the discriminated detail output
  (`…:17` `analysisDetailOutputSchemaOf(wasmArtifactSchema, wasmArtifactSummaryViewResultSchema)`), and the handler
  splits it: `const { detail, ...input } = parsed.data; … detail === "summary" && inspected.ok ?
  summarizeRetainedAnalysis(…) : inspected` (`dist/server/registerWasmTools.js:36-38`). Contract description
  (`wasmToolContracts.js:15`): omitted/complete returns SHA-256, sections, import/export WAT forms and decoded WAT
  inline; `detail:"summary"` returns counts/validation/WAT identity without WAT text and is read back through
  `inspect_analysis_view` with `normalized_result.parent_evidence_id`.
- **CLI has no detail switch.** `inspect-wasm-artifact --detail summary` → exit 1, 63 B,
  `{"code":"UNKNOWN","message":"Unknown flag: --detail"}` **[O]**; `dist/cli/wasmCommands.js:33-42` defines only
  `glue_paths`/`candidate_paths`, and `service.inspect` is called with no detail. CLI therefore always emits the
  complete Evidence (7.6 kB for an 87 B module; headers 600 B + details 451 B + WAT 371 B observed) **[O]**.
- **compare-wasm-interfaces has no detail option on any surface** (neither contract nor CLI) **[O]**. It always
  emits the full `changes` array; the partiality signal is the `coverage` enum, not a summary view **[O]**.

## 6. Output shapes (source-anchored, one observed instance each)

`inspect-wasm-artifact` envelope (CLI `--format json` prints the Evidence itself; `--full-output` wraps it as
`{"ok":true,"data":<evidence>,"meta":{"command":"…","duration":"…"}}`, 4785 vs 4703 B) **[O]**:

- envelope keys: `evidence_id` (`ev_`+64 hex), `subject{name,digest.sha256,local_path,format:"file",architecture:null}`,
  `provider{id:"wabt-artifact",name:"REA WABT artifact adapter",version:"wabt@1.0.42"}`, `predicate_type:"rea.analysis"`,
  `operation:"inspect_wasm_artifact"`, `parameters{path,glue_paths,candidate_paths}`, `raw_result:null`,
  `normalized_result`, `confidence:"observed"`, `authority:"shipped-artifact"`, `limitations[5]`, `locations[1]`,
  `evidence_links:[]` **[O]**.
- `normalized_result` (`dist/domain/wasm/wasmArtifact.js:20-74`): `artifact{path,sha256,bytes}`;
  `validation:"valid"` (literal — any bad module is an error, never `validation:"invalid"` **[O]**, bad-magic
  run); `sections[{kind,start,end,bytes,description}]` (observed 8 sections, byte ranges covering 0…87);
  optional `interface` (`wasmInterfaceSchema.exactOptional()`); raw `imports[]`/`exports[]` WAT strings;
  `headers`/`details` (objdump `-h`/`-x` text); `wat{text,sha256(over UTF-8 text),representation:"decoded-wat"}`;
  `tool_profile`; `candidates[]` (index 0 is the selected artifact); `glue[{artifact,parse_status:
  complete|partial|failed,references[{value,line,column,candidate_paths,association:
  local-path-candidate|basename-candidates|unresolved,evidence_kind:"static-literal"}]}]`;
  `runtime_execution:"not-performed"`, `network_fetch:"not-performed"`, `limitations[]`.
- `interface` (`dist/domain/wasm/wasmInterface.js:47-73`): `state: complete|partial`, `issues[]`,
  `entries[]{direction:import|export, module (null for export), name, kind: func|table|memory|global|tag|unknown,
  index (int|null), signature, wat_form, issue (string|null)}`. Signatures are a discriminated union (`:13-45`):
  func/tag `{params,results: valueType[]}`; table `{element:funcref|externref, address_type:i32|i64,
  minimum,maximum|null, shared}`; memory `{page_size:"65536", address_type, minimum, maximum|null, shared}`;
  global `{value_type, mutable}`. Limits are decimal strings, not numbers — observed `"minimum":"1"`,
  `"maximum":"2"` **[O]**.

`compare-wasm-interfaces` output (`dist/contracts/wasm/wasmComparisonContracts.js:20-38`): envelope with
`predicate_type:"rea.wasm-interface-comparison"`, `operation:"compare_wasm_interfaces"`, `confidence:"derived"`,
`authority:"analyst-inference"`, `subject:null`, `parameters{left_evidence_id,right_evidence_id,scope}`,
`evidence_links:[left_id,right_id]`, and `normalized_result{left{evidence_id,artifact}, right{…}, scope, coverage,
changes[], summary{added,removed,changed,unchanged,unknown}, limitations[2]}` **[O]**.
Each `changes` item is `{direction,module,name,state,left[],right[],reason}` with `left`/`right` typed entries
(`wasmInterfaceSchema.shape.entries`). Decision order (`WasmInterfaceComparisonService.js:91-121`): duplicate
names on either side → `unknown` "Duplicate interface names are ambiguous; all occurrences retained"; either
inventory not `complete` → `unknown` "Incomplete interface inventories cannot establish per-key uniqueness or
absence"; present entry with null signature / non-null issue / kind `unknown` → `unknown` "Signature/type
semantics were not admitted for every present entry"; absent left → `added`; absent right → `removed`; kind
differs → `changed`; else signature JSON equality → `unchanged|changed`. `coverage` (`:133-139`): `unknown` iff
both interfaces absent, `partial` iff either inventory incomplete or `summary.unknown>0`, else
`complete-within-inputs`. Keys are `JSON.stringify([direction,module,name])` (`:61`), so an import and an export
of the same name never pair; rows sort by direction, module, name (`:126-128`) — observed exports before imports
(byte order `"export" < "import"`) **[O]**.

Observed instance semantics **[O]**: a vs b (`both`) → `{added:2,removed:2,changed:2,unchanged:1,unknown:0}`,
`complete-within-inputs` (`g` and `mem` changed, `run`,`t` removed, `run2`,`env.extra` added, `env.seed`
unchanged); a vs a → 5 unchanged; a vs b `imports` → `{added:1,unchanged:1}`, only import rows; duplicate
`env.seed` imports vs itself → `{unchanged:1,unknown:1}`, coverage `partial`, reason as quoted above.

## 7. WABT requirements (source + observed refusals)

Source: `dist/wasm/WabtArtifactProvider.js`, `dist/wasm/WabtRelease.js`; observed runs used the contract path
`/home/vgpnk/.local/opt/wabt-1.0.42/bin` (each `--version` printed `1.0.42`) **[O]**.

- `REA_WABT_BIN_DIRECTORY` must be an absolute tool directory (`WabtArtifactProvider.js:71-73`); unset/relative →
  `capability_unavailable`, `retryable:false`, message "REA_WABT_BIN_DIRECTORY must be an absolute tool directory.
  Supply WABT 1.0.42 via absolute REA_WABT_BIN_DIRECTORY; REA does not install tools." (exit 1, 559 B) **[O]**.
- Exactly three executables are resolved by `realpath` + `X_OK`: `wasm-validate`, `wasm-objdump`, `wasm2wat`
  (`:75-80`). An empty dir → `capability_unavailable` with the `ENOENT … realpath '<dir>/wasm-validate'` text
  **[O]**; tools symlinked to `/usr/bin/true` → `capability_unavailable` "Unsupported wasm-validate version
  banner; expected 1.0.42." so the first tool is checked first **[O]**.
- Version gate: `<tool> --version` must exit 0, stdout `.trim() === "1.0.42"`, and stderr exactly `""`
  (`:137-140`); the retained `version_banner` is the *raw* stdout with newline — observed `"1.0.42\n"` **[O]**,
  while the schema re-check trims (`wasmArtifact.js:99`).
- Invocation (`WabtArtifactProvider.js:86-89`, re-validated at `wasmArtifact.js:95-104`):
  `wasm-validate --enable-all module.wasm`, `wasm-objdump -h -x module.wasm`, `wasm2wat --enable-all module.wasm`.
  The selected bytes are copied into a private runtime root as `module.wasm` and the snapshot hash is re-verified
  before each command (`:91-99`); tool bytes are re-hashed before each run (`:130-135`).
- Budgets (`WabtRelease.js:8-11`): input ≤ 8 MiB, each tool binary ≤ 64 MiB, per-command output ≤ 32 MiB,
  timeout 30 s. Observed: 9 MiB input → `invalid_request … "Selected artifact exceeds 8388608 bytes"` (exit 1);
  output `tool_profile` echoes `timeout_ms:30000`, `output_budget_bytes:33554432` **[O]**. Timeout/output-budget
  paths not exercised **[U]**.
- Pinned provenance in every result: `tool_profile{source:"https://github.com/WebAssembly/wabt",
  release:"1.0.42", source_commit:"ff0ef7e0009402740c805a9744c09b05be063e48", commands[3] (tool,path,sha256,
  version_banner,arguments)}` — the commit matches `SourceWabtRelease.md`'s tag commit **[O]**.
- No execution of the module and no fetch: literals `runtime_execution:"not-performed"`,
  `network_fetch:"not-performed"` plus limitation "No target execution or implicit fetch… No OS memory sandbox is
  claimed." **[O]**. Invalid WABT input returns `invalid_request` `invalid_format` with
  `captured_output{stdout:"",stderr:"0000004: error: bad magic value\n",truncated:false}` and a
  `partial_observation` Evidence object (exit 1) **[O]** — the header alone does not establish validity.

## 8. Calibration notes for the corpus (all [O] unless marked)

1. `--schema` is **input-only and lossy**: no output shape, no `detail`, no array bounds, no absolute-path rule,
   no WABT discovery. It cannot be used to write an accurate knowledge entry on its own.
2. CLI/MCP parity gap: the same operation has a wider MCP input (`detail`) than the CLI. Recording `detail` as an
   `inspect-wasm-artifact` CLI option would be false; recording that the CLI rejects it is calibrated.
3. `--llms-full` is a one-screen table of positional args and command-specific options; it omits global flags,
   outputs, `detail`, and the env gate. The word "WABT" is title-only.
4. `compare-wasm-interfaces` hides its entire real input contract behind one `string`; both `--schema` and
   `--llms-full` require the operator to already know `{left,right,scope}`.
5. Capability discovery gap: `capabilities --format json` (23 831 B) contains neither `wabt` nor `wasm` (checked
   lowercase over the full JSON) **[O]**; `binary-session` is not a CLI command — `COMMAND_NOT_FOUND` (exit 1)
   **[O]** — yet the MCP remediation text says "check its availability in binary_session". For CLI users the only
   discovery path is the failure message itself.
6. REA uses exit **1** for both `invalid_input` and `capability_unavailable` (11 failure runs observed); error JSON
   is on stdout, stderr stayed empty in every run. Distinguishing refusals requires reading `code`/`category`, not
   the status.
7. Default `--format json` = bare Evidence; `--full-output` = `{ok,data,meta}`. A corpus recipe that says
   "capture the JSON" is ambiguous unless it names `--full-output`.
8. `evidence_id` is content-addressed over the record: altering `normalized_result.artifact.sha256` is caught as
   "Evidence semantic identifier does not match its record" *before* the subject/selection cross-check
   (`WasmInterfaceComparisonService.js:15-24`), reported as `invalid_request` (exit 1).
9. `validation` is only ever `"valid"` in a returned result; invalid bytes never yield a result object.
10. Limits are strings (`"1"`, `"65536"`), and `maximum:null` means unbounded — do not type them as numbers.

## 9. Remaining unknowns

- [U] `detail:"summary"` payload — CLI rejects the flag and the lane forbids the MCP devices, so no observed summary
  Evidence; the shape is source-only (`wasmArtifactSummaryViewResultSchema`).
- [U] `interface.state:"partial"` and non-null entry `issue` were not triggered (only `complete` observed, and
  `unknown` came solely from duplicate names). Which WABT forms produce issues is untested.
- [U] Signatures other than func(i32)->i32, memory i32 65536/1..2, global mut i64, table funcref i32 1, absent tag;
  i64 address types, shared memories/tables, externref and v128 paths untested.
- [U] 30 s timeout and 32 MiB output budget; token-count/limit/offset filters; `md|toon|jsonl` formats; OOM/cancel.
- [U] `glue_paths` association output (`references[].association`) not exercised, so its three-way classification is
  source-only.
- [U] Asymmetric duplicate sets (one side 1 occurrence, other 2) not exercised; only symmetric duplicates.
- [U] Whether the CLI's `--schema` omission of `detail` is intentional delivery-only parity or a gap; source shows
  the contract carries it and the CLI command schema does not (both read, no defect claim made).

## 10. Round-20 relevance

- C2 coverage [O]: `grep -rl` over `corpus/` + `README.md` for either hyphen or underscore verb name returned **no
  files**, and `REA_WABT_BIN_DIRECTORY|wabt-1.0.42` had **no corpus hits** — so a knowledge entry naming these two
  verbs is new coverage. The run Evidence here is scratch-only: the `ev_` ids (`ev_f2bfc192d91ffbfe5a354066c4639c10cc899365b28b276a9629340caad73153`,
  `ev_a95158dc6380a114e55b507d0d6bedfb176cbcd30a5f51cc57bf319b67330830`, partial `ev_ae265b9d5ceb04db71c6eb121d591a5d5b347606e4e27dad571355fa9801bfa1`)
  are CLI-session ids with no bundle retained under `.ufo/waves/round-20/evidence/c2/`; the L1 must retain the
  capture bytes there for the `exercised` check (`verb-coverage.py` needs `ev_<64hex>` + existing path at REV).
- Cross-references: `w1/SourceWabtRelease.md` (release/tag identity; its `ff0ef7e…` commit matches
  `tool_profile.source_commit`), `w1/SourceWasmSpec.md` (what an import/export entry is), `w1/ScoutWasmCarriers.md`
  (real shipped carriers). This seat adds no carrier claim: all wasm here is synthesized.
- Inference for the C2 entry author **[I]**: the honest entry is "CLI schema/manifest is input-only; the operator
  must supply absolute `REA_WABT_BIN_DIRECTORY` with exact-1.0.42 tools, pass complete Evidence to compare, and
  read `coverage`/`unknown` rather than treating `changed` counts as compatibility".
