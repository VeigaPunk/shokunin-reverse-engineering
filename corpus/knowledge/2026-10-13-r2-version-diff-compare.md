<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/08-version-diff.md. -->

# 08 — Cross-version binary comparison end-to-end (pacman cache pairs)

Lane: kaidoku-shokunin. Date: 2026-10-13. Host: Linux x86_64, node v24.21.0, npx 11.19.0.
Package: `~/.npm/_npx/af752b90495482d7/node_modules/rea-agents` (rea-agents@6.4.0).
Provider: Ghidra 12.1.4 at `~/.local/opt/ghidra_12.1.4_PUBLIC` (`rea doctor` healthy;
Hopper absent — auto selection binds Ghidra under the `rea-workflow` composed provider).
Scratch: `/tmp/rea-vercmp` (deleted after run; `/tmp/rea-ghidra-*` untouched).

Targets — real multi-version pairs kept by the host pacman cache (`uniq -d` walk found
~380 duplicated pkgbases; three exercised):

| Pair | Members | Sizes | Type |
| ---- | ------- | ----- | ---- |
| `1password-cli` 2.34.1-1 → 2.40.0-2 | `usr/bin/op` | 41,210,040 → 43,475,106 B | ELF x86-64 static, **stripped Go** |
| `expac` 10-12 → 10-13 | `usr/bin/expac` | 31,424 → 31,496 B | ELF x86-64 PIE dyn, stripped C (pkgrel-only rebuild) |
| `bubblewrap` 0.11.2-1 → 0.12.0-1 | `usr/bin/bwrap` | 84,464 → 84,464 B | ELF x86-64 PIE dyn, stripped C (real upstream bump) |

sha256 (extracted via `tar -xOf <pkg> usr/bin/<name>`):
`op-2.34.1` `d24dc5d4…`, `op-2.40.0` `8d029d2c…`, `expac-10-12` `b35c11a6…`,
`expac-10-13` `a4ee2982…`, `bwrap-0.11.2` `6ad2138a…`, `bwrap-0.12.0` `7c44fa8e…`.

## Run log (exact commands + wall-clock)

| # | Command | Result |
| - | ------- | ------ |
| 1 | `rea analyze /tmp/rea-vercmp/op-2.34.1` | FAIL ~5.5 min — `provider_timeout` (retryable), `details.operation=list_documents`, `timeout_ms=330000` |
| 2 | `rea analyze expac-10-12 --format json` | 5.7 s — record `ev_0bca436b…`, op `binary_overview`, 203 procedures, 180 strings |
| 3 | `rea analyze expac-10-13 --format json` | ~5 s — `ev_6cbf4a97…`, 203 procedures |
| 4 | `rea compare bundle-expac-10-12.json bundle-expac-10-13.json` (TOON default output fed by mistake) | FAIL `evidence_integrity_mismatch`, `reason=invalid-json` — compare wants JSON |
| 5 | `rea compare` on single-JSON records | FAIL `evidence_integrity_mismatch` — "Expected an Evidence bundle with records and manifest arrays, but this JSON is one Evidence record … Export a session bundle with the MCP export_evidence_bundle tool" |
| 6 | hand-wrapped single-record bundles → `rea compare` | EXIT 0 — `status:unknown`, both records `unresolved_branch` (one-sided membership) |
| 7 | `rea search expac-* ".*" --kind procedures --mode regex --format json` | ~5 s each — 112 local + ~90 `<EXTERNAL>` names per side |
| 8 | `rea function expac-10-12/13 --procedure entry --format json` | ~15 s each — `analyze_function` dossiers 31,560 B each, `ev_da1101dd…` / `ev_253b07f9…` |
| 9 | `rea function expac-10-12/13 --procedure FUN_00102080` (main, LEA target in `entry`) | ~20 s each — dossiers 5.29 MB / 5.23 MB, `ev_4ed015d8…` / `ev_ca538e8f…` |
| 10 | `rea function bwrap-0.11.2/0.12.0 --procedure entry` | ~60 s each — dossiers 33,006 / 32,246 B |
| 11 | `rea analyze expac --snapshot s.json` + `search` + `function entry` + `function FUN_00102080` (all four, one snapshot) | **25 s total per side** — snapshot 10.7 MB mode 0600; `records:4, entries:2, workflow_entries:1`; inner `evidence_bundle` extracted to canonical bundle |
| 12 | `rea compare eb-12.json eb-13.json` (real snapshot bundles) | EXIT 0 — `status:unknown`, `unresolved:8`, every record one-sided |
| 13 | `rea compare-application-versions cav-input.json` (native records) | FAIL `invalid_request`/`invalid_input` — "Expected authenticated JavaScript analysis, runtime reconciliation, or managed application graph Evidence" at `left.operation` |
| 14 | `REA_GHIDRA_STARTUP_TIMEOUT_MS=800000 rea analyze op-2.34.1` (default TOON) then `op-2.40.0 --format json` | Both OK inside the raised bound — `ev_8e20ac5d…` / `ev_0b3c8101…`; 33,060 vs 11,595 procedures, 76,553 vs 76,338 strings, 18 vs 16 segments |
| 15 | `@toon-format/toon decode` on the TOON record → `rec-op-234.json` | Lossless — `parseEvidence` re-verified `evidence_id` during compare |

Domain-level calls (same code the MCP tools wrap — `dist/domain/*`, invoked via
`node --input-type=module` from the installed package):

| # | Call | Result |
| - | ---- | ------ |
| 16 | `compareBundles(eb12, eb13, record_pairs=[4 op-matched pairs])` | `status:changed`, `records_changed:4`, all `observed_change`, `unresolved:0` |
| 17 | `compareFunctions(entry-12, entry-13)` expac | `status:changed`, match `matched`/`symbol`; 7/8 dims unchanged, `assembly` +13/−13 (2 hunks) |
| 18 | `compareFunctions(main-12, main-13)` expac | `status:unknown`, match `ambiguous`/`explicit` (FUN_* auto-name); `pseudocode` +390/−392 in 240 hunks, `cfg` 205→192 blocks, `references` 776→730, `strings_names` 603→604, `calls` 65→66 |
| 19 | `compareFunctions(entry-0.11.2, entry-0.12.0)` bwrap | `status:changed`, match `matched`/`symbol`; `pseudocode` +1/−1 (2 hunks), `assembly` +13/−13, `references`/`strings_names` changed |
| 20 | `compareFunctions(entry-12, entry-12)` (null case) | `status:unchanged`, 8/8 dims unchanged |
| 21 | `compareBundles(wrap(op-2.34.1), wrap(op-2.40.0), [overview pair])` | `status:changed`, `records_changed:1`, `observed_change` |

## What the comparison surfaces

- **Bundle level (`rea compare` / `compare_bundles`)**: canonical-bundle membership by
  `evidence_id` plus residual-unknown revision chains. Classes `added/removed/changed/
  unknown/history_advanced/history_diverged`; `conclusion_kind` ∈
  `observed_change|contradiction|unresolved_branch`. It does **not** align same-operation
  records across two binaries — unpaired records are always `unresolved_branch` with the
  standing limitation "EvidenceBundle has no inventory completeness marker; one-sided
  membership may reflect incomplete capture." The decisive channel is `record_pairs`
  (`bundleComparisonInputSchema`, `bundleComparison.js:18-27`), which reclassifies each
  explicit pair as `changed`/`observed_change`. **CLI `compare` exposes only
  `left`/`right` — `record_pairs` is an MCP-input-only field**, so a CLI-only run of two
  session bundles can never rise above `status:unknown`.
- **Function level (`compare_functions` / `compareFunctions`)**: eight typed dimensions —
  `identity, pseudocode, assembly, comments, calls, references, strings_names, cfg` —
  each with counts, digest equality, line-delta `{added,removed,hunks}` for text dims,
  `evidence_links`, per-dim limitations, `conclusion_kind`. `function_match`
  (`functionComparisonNormalization.js:9-25`): non-auto name equality →
  `matched`/`symbol`; equal auto-names (`FUN_*`/`sub_*`/`fcn.*`) → `ambiguous`/`explicit`;
  different names → `mismatched`. Overall status folds dims + match into
  `unchanged|changed|unknown` (`functionComparisonResults.js`).
- **Aggregate/artifact level**: `compare_artifacts` (MCP) diffs artifact-inventory
  evidence by logical path (`artifactComparison.js:59+`); `compare-application-versions`
  diffs two JavaScript Application Graph evidences node-by-node with
  `exact|strong|candidate` match tiers (`javascriptApplicationVersionComparisonSchemas.js`).
  Neither accepts native binary records.
- **Deltas are honest**: expac `entry` across the pkgrel rebuild shows identical
  pseudocode/cfg/calls and only literal `assembly` text churn (relocated address
  operands) — the dimension is flagged `changed` but carries
  "Assembly is opaque provider text; relocation normalization is unavailable." The
  same-version self-compare returns `unchanged`. Real signal is distinguishable from
  relocation noise at the pseudocode/cfg/reference dims.

## Candidate: `compare` is a membership diff; cross-version binary comparison needs `record_pairs`, which is MCP-only on the `compare_bundles` tool

- claim: `rea compare <left> <right>` classifies records purely by `evidence_id`
  membership; two independently analyzed binaries share no IDs, so every record lands
  `unresolved_branch` → `status:unknown` regardless of content. Supplying
  `record_pairs:[{left_evidence_id,right_evidence_id}]` reclassifies each pair as
  `changed`/`observed_change` → `status:changed` with `unresolved:0`. The schema
  (`bundleComparisonInputSchema`) supports it, but the CLI surface does not expose it —
  only the MCP `compare_bundles` tool input does.
- source: run log rows 6, 12, 16, 21; `dist/domain/bundleComparison.js:18-27` (schema),
  `:94-156` (`compareRecords` — pairs counted `changed`, one-sided counted `unknown`),
  `dist/server/registerBundleComparisonTool.js`; CLI `--schema` shows only `left,right`.
- verify: build two canonical session bundles (`--snapshot`, extract `evidence_bundle`),
  run `rea compare` → `unknown`/8 unresolved; call `compareBundles` (or the MCP tool)
  with pairs → `changed`/0 unresolved.
- verified-at: 2026-10-13
- suggested: admit — observed on both hand-wrapped and snapshot-exported bundles;
  limitation string itself documents one-sided membership as unknown-by-design.

## Candidate: function-level cross-version diffing works end-to-end and separates semantic change from relocation noise

- claim: `rea function <bin> --procedure <name>` yields `analyze_function` dossiers that
  `compareFunctions` (MCP `compare_functions`) diffs across 8 dimensions with per-dim
  counts, digests, text deltas, and evidence links. `entry`↔`entry` on a pkgrel-only
  rebuild → only `assembly` text differs (+13/−13, address operands); on `main`
  (FUN_00102080, same slot) → real codegen churn (+390/−392 pseudocode lines, cfg
  205→192); bwrap 0.11.2→0.12.0 `entry` → pseudocode +1/−1 plus reference/string churn.
  Auto-named functions pair as `ambiguous`/`explicit`, non-auto names as
  `matched`/`symbol`; self-compare returns `unchanged`.
- source: run log rows 8–10, 17–20; `dist/domain/functionComparison.js:9-33`,
  `functionComparisonNormalization.js:9-25,142` (`isAutoName`),
  `functionComparisonSchemas.js`.
- verify: `rea function a --procedure entry > l.json`, same on b → feed both records to
  `compare_functions` (MCP) or `compareFunctions` (domain); read `changes[]` for the
  differing dims.
- verified-at: 2026-10-13
- suggested: admit — three independent pairs + null case; limitation strings honestly
  scope what `assembly`-dimension churn means.

## Candidate: the sanctioned CLI path to comparable bundles is `--snapshot` accumulation; it is also ~10× cheaper than cold calls

- claim: `rea <verb> <target> --snapshot <file>` reuses one imported analysis DB and
  appends each record into the snapshot's inner `evidence_bundle`, which is exactly the
  canonical bundle `compare`/`evidence-export` accept (7-key
  `{artifacts,providers,environments,scenarios,captures,unknowns,records}`). Four ops on
  a 31 KB ELF cost 25 s total via one snapshot vs ~5–20 s **each** cold (every cold call
  re-imports to an ephemeral Ghidra project). Record `evidence_id`s are identical
  between snapshot and standalone runs — replay is deterministic.
- source: run log rows 11–12 vs 2, 8–9; sibling wave `12-evidence-bundle.md` (envelope
  schema, `analysisSnapshotSchema` vs `evidenceBundleSchema`); `evidenceBundle.js:46-80`
  (`createEvidenceBundle` projects manifests from sorted records).
- verify: `rea analyze t --snapshot s.json` then more ops with same `--snapshot`;
  `jq .evidence_bundle s.json > b.json`; `rea compare b.json other.json`.
- verified-at: 2026-10-13
- suggested: admit — measured 25 s vs ~60 s cold for the same 4-call set; IDs
  `ev_0bca436b…`, `ev_2333c35f…`, `ev_da1101dd…`, `ev_4ed015d8…` reproduced
  bit-for-bit across sessions.

## Candidate: `compare-application-versions` is JavaScript-application-only and refuses native records with a typed error

- claim: the verb takes `inputJson` `{left, right, left_native_observations[],
  right_native_observations[]}` where left/right must be JavaScript Application Graph
  evidence; native `binary_overview`/`analyze_function` records fail validation:
  `invalid_request`/`invalid_input`, "Expected authenticated JavaScript analysis,
  runtime reconciliation, or managed application graph Evidence" at `left.operation`.
- source: run log row 13; `javascriptApplicationVersionComparisonSchemas.js:38-44`
  (`compareApplicationVersionsInputSchema` = two `evidenceSchema` + native-observation
  arrays, superRefine on distinct IDs).
- verify: `rea compare-application-versions <file containing {"left":<native rec>,"right":<native rec>}>`.
- verified-at: 2026-10-13
- suggested: admit — typed refusal reproduced; the catalog description already said
  "JavaScript Application Graph versions".

## Candidate: large stripped Go binaries clear the bound only by raising `REA_GHIDRA_STARTUP_TIMEOUT_MS`; function-level diff at that scale is untested

- claim: 41–43 MB statically-linked stripped Go binaries exceed the default 330 s
  Ghidra startup budget → `provider_timeout` (retryable, `operation=list_documents`,
  `timeout_ms=330000`; `DEFAULT_GHIDRA_STARTUP_TIMEOUT_MS`,
  `dist/config/ghidraStartupTimeout.js:3`). Setting
  `REA_GHIDRA_STARTUP_TIMEOUT_MS=800000` (env, `dist/config/environment.js:34`) let both
  `op` overviews complete in the (>330 s, <800 s) band — 33,060 vs 11,595 procedures,
  a real overview-level delta (segments 18→16, strings ~76.5k→76.3k). Per-function
  dossiers were not attempted at this scale: each cold `function` call re-imports the
  whole program, and a snapshot run would still pay the ~10 min import once.
- source: run log rows 1, 14; `dist/ghidra/GhidraClient.js:83`,
  `dist/config/ghidraStartupTimeout.js`, `dist/config/environment.js:34`.
- verify: `time rea analyze <41MB stripped Go>` → `provider_timeout` at 330 s; rerun
  with `REA_GHIDRA_STARTUP_TIMEOUT_MS=800000` → `binary_overview` record.
- verified-at: 2026-10-13
- suggested: admit — bounded honestly; both op overviews analyzed and paired (run log
  21). Recommended next probe: `--snapshot` on one op binary, then one `function` call
  against a named procedure to price dossier cost at 40 MB scale.

## Candidate: `compare`/`evidence-export` consume canonical JSON records, never the default TOON text — always pass `--format json`

- claim: default CLI output is TOON (`key[N]:` count-annotated rows); feeding it to
  `compare` or `evidence-export` fails `evidence_integrity_mismatch`/`invalid-json`.
  `--format json` emits the Evidence record JSON. TOON decodes losslessly via the
  bundled `@toon-format/toon` (record re-verified its `evidence_id` inside
  `parseEvidenceBundle` — a TOON→JSON rescue is integrity-safe).
- source: run log rows 4, 15; global `--format <toon|json|yaml|md|jsonl>` flag.
- verify: `rea analyze t > r.toon`; `rea compare r.toon r.toon` → invalid-json;
  `decode(toon)` → `compare` accepts.
- verified-at: 2026-10-13
- suggested: admit — observed both failure and successful rescue.

## Error taxonomy observed

| code | category | retryable | trigger |
| ---- | -------- | --------- | ------- |
| `provider_timeout` | `timeout` | true | Ghidra startup >330 s on 41 MB stripped Go (`list_documents`) |
| `evidence_integrity_mismatch` | `execution_failure` | false | TOON fed where JSON expected (`reason=invalid-json`) |
| `evidence_integrity_mismatch` | `integrity_mismatch` | false | single Evidence record where `{records,manifest}` bundle expected |
| `invalid_request` | `invalid_input` | true | `compare-application-versions` on native `rea.analysis` records |

## Summary

**Cross-version diffing is HELD as machinery, FRONTIER as a one-shot lane.** Every
comparison stage runs end-to-end on real pacman-cache pairs with typed, deterministic,
integrity-verified output — and every verdict is checkable: `entry` vs `entry` on a
rebuild flags only assembly-text churn, on a version bump flags pseudocode+references,
and self-vs-self returns `unchanged`. What is missing is a single verb that goes
binary→binary: the operator must (a) `--snapshot`-accumulate records per version,
(b) extract `evidence_bundle`, (c) pair records by operation/name and feed
`record_pairs` — which today only the MCP `compare_bundles`/`compare_functions` tools
(or a direct domain call) expose. CLI `compare` alone cannot rise above
`status:unknown` on two session bundles. Function-level `compareFunctions` is the real
semantic differ (8 dimensions, honest `ambiguous`/`mismatched` match status, per-dim
limitations); `compare-application-versions` is JS-graph-only (typed refusal on
native); scaling bound lands at ~40 MB stripped Go where default 330 s Ghidra startup
times out unless `REA_GHIDRA_STARTUP_TIMEOUT_MS` is raised (overviews then complete;
dossier-level at that scale untested — priced at one ~10 min import per side via a
snapshot). Scratch dir `/tmp/rea-vercmp` removed; no files outside this report touched.
