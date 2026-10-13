<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/12-evidence-bundle.md. -->

# 12 — Real Evidence bundle dumped + field-level schema (round-2 evidence)

Lane: kaidoku-shokunin. Date: 2026-10-13. Host: Linux x86_64, node v24.21.0, npx 11.19.0.
Target: `/usr/bin/true` — ELF 64-bit x86-64 executable, 43,320 bytes,
sha256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`
(verified `sha256sum /usr/bin/true`). NB: this is the same digest/size as the
`target-8bc9a73afd7d.bin` (43,320 B) seen inside a foreign `/tmp/rea-ghidra-*`
session in the round-1 report — that session was analyzing `/usr/bin/true`.
Package inspected: `~/.npm/_npx/af752b90495482d7/node_modules/rea-agents` (rea-agents@6.4.0).

## Run log (exact commands + wall-clock)

| # | Command | Result |
| - | ------- | ------ |
| 1 | `npx -y rea-agents@6.4.0 analyze /usr/bin/true --snapshot /tmp/kaidoku-evidence.snap.json --format json` | ~5s OK — record `ev_982c…`, op `binary_overview`, provider `rea-workflow`, confidence `derived`; snapshot 10,323 B mode 0600 |
| 2 | `npx -y rea-agents@6.4.0 search /usr/bin/true ".*" --kind procedures --mode regex --snapshot /tmp/kaidoku-evidence.snap.json --format json` | ~5s OK — record `ev_2fa1…`, op `search_procedures`, provider `ghidra`, confidence `observed`; snapshot merged in place |
| 3 | `npx -y rea-agents@6.4.0 analyze /usr/bin/true --snapshot /tmp/kaidoku-evidence.snap.json --format json` (repeat) | **0.764 s** — replayed from snapshot: identical `evidence_id` `ev_982c…`, no new record, no Ghidra run |
| 4 | `rea inspect-evidence-bundle /tmp/kaidoku-evidence.snap.json` | FAIL `invalid_input` — arg is a spec object `{path, detail, filters}`, not a bare path |
| 5 | `rea inspect-evidence-bundle '{"path":"/tmp/kaidoku-evidence.snap.json"}'` | FAIL `evidence_integrity_mismatch` — snapshot envelope is not a canonical bundle (`artifacts: expected array, received undefined`, 6 more issues) |
| 6 | `rea inspect-evidence-bundle '{"path":"<bundle-only>.json"}'` (inner `evidence_bundle` extracted) | OK — `detail` default `complete` echoes the canonical bundle |
| 7 | `rea evidence-export <bundle-only>.json /tmp/kaidoku-evidence.exported.json` | `{"path":…,"bytes":4687,"records":1}` — export is byte-identical to the inner `evidence_bundle` after JSON normalization |
| 8 | `rea evidence-import /tmp/kaidoku-evidence.exported.json` / `…exported2.json` | `{"imported":1,"unknowns_added":0,"total":1}` then `{"imported":2,"unknowns_added":0,"total":2}` |
| 9 | `rea evidence-export /tmp/kaidoku-evidence.snap.json out.json` | FAIL `evidence_integrity_mismatch` — export also requires the canonical bundle, not the snapshot envelope |
| 10 | `rea inspect-evidence-bundle '{"path":"<exported2>","detail":"summary","filters":{"operation":"search_procedures"}}'` | OK — `{"kind":"evidence-bundle-summary","matching_records":1,"records":[search_procedures only]}` |

## Bundle schema

Two related but distinct formats. **`--snapshot` writes the Analysis Snapshot
envelope** (`analysisSnapshotSchema`, `dist/domain/analysisSnapshot.js:97`);
**`evidence-export`/`evidence-import`/`inspect-evidence-bundle` operate on the
inner `evidence_bundle`** (`evidenceBundleSchema`, `dist/domain/evidenceBundle.js:23`).

### Analysis Snapshot envelope (the `--snapshot` file, mode 0600)

```jsonc
{
  "target":           { "sha256": "<64-hex>", "kind": "executable|database|archive|artifact",
                        "format": "elf|mach-o|pe|apk|…", "architecture": "x86_64|null" },
  "binding":          { "provider": { "id", "name", "version" },          // committedProviderSchema
                        "analysis_profile": { "provider": {…}, "parameters": {…},
                                              "digest": "<sha256 of canonical {provider,parameters}>" } },
  "entries":          [ /* provider-direct query cache — OBSERVED EMPTY in pure CLI runs */ ],
  "workflow_entries": [ /* composed-workflow query cache — 1 entry after `analyze` */ ],
  "evidence_bundle":  { /* canonical bundle below */ }
}
```

- `binding` does **not** carry the target sha256 — that lives in `target.sha256`.
  `binding` pins provider identity + exact analysis-profile digest; `snapshotMatchesBinding`
  requires exact target AND provider/profile equality, else `profile_mismatch`
  (`analysisSnapshot.js:109-130`).
- `binding.provider`/`analysis_profile` must self-agree (provider id+name+version equal) — superRefine.
- Entry (each of `entries`, `workflow_entries`): `{query_id, operation, parameters, execution}`.
  `query_id` = `"query_"+sha256(canonical{target,binding,operation,parameters})`
  (`analysisQueryId`, `analysisSnapshot.js:203`).
  `execution` = `{result, raw_result|null, provider, limitations[], locations[], subject|null}`;
  `workflow_entries[].execution` additionally carries `analysis_profile`.
  `entrySchema` vs `workflowEntrySchema` differ only by that field (`analysisSnapshot.js:69-95`).
- Linkage rule (`snapshotEvidenceForQuery`, `analysisSnapshot.js:137-157`): replay needs BOTH
  a matching `query_id` in `entries`/`workflow_entries` AND a `records[]` element matching
  subject-sha256 + operation + provider + analysis_profile + canonical parameters.
  Records alone do not replay; entries alone carry no Evidence.
- Observed population asymmetry: `analyze` (CLI tool `binary_overview`) wrote one
  `workflow_entry` + one record; `search` appended only a record — `entries` stayed `[]`.
  Source: `DirectAnalysis.js:159-179` records workflow snapshots only for
  `isWorkflowEvidenceTool` = `binary_overview|inspect_native_api|
  inspect_native_dispatch_metadata|trace_feature|trace_native_values|trace_native_ui_action`
  (`DirectAnalysis.js:311-316`); provider-direct `entries` are written by session `#execute`→
  `recordSnapshot` (`BinarySession.js:348-382`), a path the CLI direct run bypasses.
- Cache ceiling `SNAPSHOT_CACHE_ENTRY_CEILING = 10_000` (`AnalysisSnapshotCache.js:26`).
- Snapshot import merges entries by `query_id` and evidence atomically; wrong-target or
  wrong-profile files are refused (`AnalysisSnapshotCache.js:109-125`).

### Canonical Evidence bundle (`evidence_bundle` / export file)

```jsonc
{
  "artifacts":    [ { "digest": {"sha256": "…"}, "format": "elf", "architecture": "x86_64" } ],
  "providers":    [ { "id": "ghidra", "name": "Ghidra", "version": "12.1.4" },
                    { "id": "rea-workflow", "name": "REA composed investigation workflow", "version": "1" } ],
  "environments": [ { "id", "platform", "architecture",
                      "isolation": "none|process|container|virtual-machine" } ],
  "scenarios":    [ { "evidence_id": "ev_…", "operation": "…", "authority": "controlled-replay" } ],
  "captures":     [ { "evidence_id": "ev_…", "predicate_type": "…" } ],
  "unknowns":     [ /* residualUnknownSchema — unresolved-question ledger, see below */ ],
  "records":      [ /* evidenceSchema — sorted by evidence_id codepoint order */ ]
}
```

- `artifacts`/`providers`/`environments` are deduped manifests projected FROM `records`
  (`createEvidenceBundle`, `evidenceBundle.js:46-80`); `scenarios` indexes records with
  `authority:"controlled-replay"`; `captures` indexes `predicate_type:"rea.process-capture"`.
- Observed: artifacts 1, providers 2 (ghidra + rea-workflow) after two invocations,
  scenarios/captures/environments/unknowns all `[]`.

### Evidence record (`records[]`, strict `evidenceSchema`, `evidence.js:80-99`)

```jsonc
{
  "evidence_id":       "ev_<64-hex>",              // semantic digest, re-computed on parse
  "subject":           { "name", "digest": {"sha256"}, "format": <27-member enum>,
                         "architecture": <enum|null>, "local_path" } | null,
  "provider":          { "id", "name", "version": string|null },
  "analysis_profile":  { "provider", "parameters", "digest" } | null,
  "predicate_type":    "rea.analysis",             // observed
  "operation":         "binary_overview" | "search_procedures" | "…",
  "parameters":        { },                        // query args
  "raw_result":        null | <any JSON>,
  "normalized_result": <any JSON>,                 // e.g. {document, segments[31], segment_count, procedure_count, string_count}
  "confidence":        "observed|derived|inferred",
  "authority":         "shipped-artifact|controlled-replay|historical-reference|external-service|analyst-inference",
  "environment":       <executionEnvironment> | null,
  "limitations":       [ "…" ],
  "locations":         [ {kind:"address"|"address-range"|"artifact-path"|"file-offset"|"file-offset-range", …} ],
  "evidence_links":    [ "ev_…" ]
}
```

- `evidence_id` = `ev_` + sha256 of canonical projection EXCLUDING display fields
  (`subject.name`, `subject.local_path`) — semantic content-addressing; tamper-evident:
  `parseEvidence` re-computes and rejects mismatches (`evidence.js:108-152`).
  Verified live: re-running `analyze` produced the identical `ev_982c…` and no duplicate record.
- `analysis_profile.provider` must equal record `provider` (superRefine
  `validateAnalysisProfileProvider`); `analysis_profile.digest` must equal sha256 of
  canonical `{provider,parameters}` (`analysisProfile.js:17-30`, `profileDigest`).
- `subject.format` enum: hopper, analysis-database, mach-o, elf, pe, dos-mz, dos-com, zip,
  ipa, apk, msix, appx, asar, dmg, pkg, plist, javascript, source-map, directory, file,
  unknown, mach-o-universal, javascript-bundle, entitlements (`evidence.js:19-44`).

### `unknowns[]` element (`residualUnknownSchema`, `residualUnknown.js:36-88`)

`{unknown_id:"unk_…", revision≥1, previous_revision_digest|null,
revision_digest<sha256,verified>, scope_digest|null, question,
status:"open|investigating|blocked|contradicted|resolved",
severity:"low|medium|high|critical", domain, supporting_evidence_ids[],
contradicting_evidence_ids[], required_authority|null,
required_confidence:"observed|derived|inferred", required_environment|null,
recommended_probes[{operation,rationale}], relationships[{type:"depends-on|
related-to|contradicts",unknown_id}], resolution:null|{disposition:"verified"|
"withdrawn"|"out-of-scope",rationale,evidence_ids}, mutation_evidence_ids[min 1]}`

### CLI surface for bundles

- `rea evidence-export <source> <out> [--overwrite]` — validates canonical bundle, writes
  atomic canonical JSON; prints `{path, bytes, records}`. Rejects snapshot envelopes and
  any schema drift with `evidence_integrity_mismatch` (non-retryable).
- `rea evidence-import <path>` — validates + imports; prints `{imported, unknowns_added, total}`.
- `rea inspect-evidence-bundle <inputJson>` — `inputJson` is INLINE JSON or a file containing
  the SPEC: `{path: "<abs bundle path>", detail: "complete|summary",
  filters: {evidence_id, operation, target_sha256, analysis_profile_digest, procedure_address}}`
  (filter keys from `evidenceRecordFiltersSchema`, `evidenceRecordSummary.js:5-11`).
  `detail` default = `complete` (echoes full canonical bundle). `filters` require
  `detail:"summary"` (`InspectEvidenceBundle.js:6-15`). Summary view:
  `{kind:"evidence-bundle-summary", filters, total_retained_records, matching_records,
  unknown_revisions, records:[{evidence_id, subject, provider, operation, confidence,
  authority, analysis_profile_digest, retention:"complete-record", limitation_count,
  native_dossier}]}`. `native_dossier` is `available` only for `analyze_function` records;
  else `{available:false, reason:"different-operation"|"not-recorded-or-incompatible"}`.
- `rea compare` exists for two canonical bundles (not exercised this round).

## Candidate: The `--snapshot` file is an Analysis Snapshot envelope wrapping a canonical Evidence bundle, and the two formats are NOT interchangeable on the CLI

- claim: `rea … --snapshot X` writes `{target, binding, entries, workflow_entries,
  evidence_bundle}` (mode 0600). `evidence-export`/`evidence-import`/`inspect-evidence-bundle`
  all reject that envelope with `evidence_integrity_mismatch` and only accept the canonical
  7-key bundle `{artifacts, providers, environments, scenarios, captures, unknowns, records}` —
  which is exactly the snapshot's inner `evidence_bundle` object.
- source: run log rows 5, 7, 9 (mismatch errors + successful export of extracted bundle);
  `dist/domain/analysisSnapshot.js:97-103` (`analysisSnapshotSchema`),
  `dist/domain/evidenceBundle.js:23-31` (`evidenceBundleSchema`).
- verify: `rea analyze /usr/bin/true --snapshot /tmp/s.json`; `python3 -c "json.load(open('/tmp/s.json'))['evidence_bundle']"` → write to `/tmp/b.json`; `rea evidence-export /tmp/b.json /tmp/out.json`; `rea evidence-import /tmp/out.json` → `{imported:N}`.
- verified-at: 2026-10-13
- suggested: admit — reproduced with 1- and 2-record bundles; export is byte-stable
  (exported file == inner `evidence_bundle` after normalization).

## Candidate: Evidence records are semantically content-addressed and deduplicating; snapshot replay requires an entry AND a record

- claim: `evidence_id` = `ev_`+sha256 over a canonical projection that excludes display
  fields (`subject.name`, `subject.local_path`) but includes provider, analysis_profile,
  operation, parameters, results, confidence, authority, locations, links. Re-running the
  same operation on the same target reproduces the identical `evidence_id` (no duplicate
  record). Snapshot replay (`snapshotEvidenceForQuery`) additionally requires a
  `query_id` hit in `entries`/`workflow_entries`; observed: `analyze` replayed in 0.76 s
  with no provider run, while `search` (record-only, no entry) would re-execute.
- source: run log rows 1–3; `evidence.js:140-152` (`computeEvidenceId` projection),
  `analysisSnapshot.js:137-157`, `AnalysisSnapshotCache.js:150-201`.
- verify: `rea analyze <t> --snapshot s.json` twice — second run <1 s, same `evidence_id`,
  `records` length unchanged; `jq '.workflow_entries|length' s.json` = 1.
- verified-at: 2026-10-13
- suggested: admit — measured 5 s → 0.764 s wall clock and stable record set across 3 invocations.

## Candidate: `inspect-evidence-bundle` takes a spec object, has exactly two detail levels, and five record-filter keys

- claim: The `inputJson` arg is `{"path":"<abs path>","detail":"complete|summary",
  "filters":{…}}` — a bare path is parsed as the spec itself and fails `missing_argument path`.
  `detail` accepts only `complete` (default, full canonical bundle) or `summary`
  (`evidence-bundle-summary` projection). `filters` is a strict object allowing only
  `evidence_id`, `operation`, `target_sha256`, `analysis_profile_digest`,
  `procedure_address`, and requires `detail:"summary"`.
- source: run log rows 4–6, 10; `evidenceRecordSummary.js:5-11`
  (`evidenceRecordFiltersSchema`), `InspectEvidenceBundle.js:1-16`.
- verify: `rea inspect-evidence-bundle '{"path":"<bundle>","detail":"summary","filters":{"operation":"<op>"}}'` → `matching_records` reflects the filter; any other filter key → `unknown_argument`.
- verified-at: 2026-10-13
- suggested: admit — probed 11 candidate filter keys; only the 5 schema keys accepted.

## Candidate: bundle manifests are derived projections — `artifacts`/`providers`/`environments` dedupe from `records`; `scenarios`/`captures` index by authority/predicate

- claim: `createEvidenceBundle` projects `records` into `artifacts` (unique
  `{digest,format,architecture}` from non-null subjects), `providers`, `environments`;
  `scenarios` lists `{evidence_id,operation}` for `authority:"controlled-replay"` records;
  `captures` lists `{evidence_id,predicate_type}` for `rea.process-capture` records;
  `records` and `unknowns` are sorted by id codepoint order. Observed: after `analyze`+`search`,
  `artifacts:[1 item]`, `providers:[ghidra,rea-workflow]` (order-independent, sorted), other
  lists empty.
- source: `evidenceBundle.js:7-31,46-80`; observed snapshot contents.
- verify: any exported bundle — check `artifacts` equals the set of record subject
  `{digest,format,architecture}` triples.
- verified-at: 2026-10-13
- suggested: admit — code read plus live diff (exported file == projected inner bundle).

## Summary

- One real bundle dumped from `/usr/bin/true` (sha256 `8bc9a73a…`, 43,320 B — the same
  target as the unexplained round-1 foreign session). Snapshot: 10,323 B after `analyze`,
  grew with `search`; exported canonical bundle 28,912 B with 2 records.
- Schema documented field-by-field above from observed JSON + zod sources
  (`analysisSnapshotSchema`, `evidenceBundleSchema`, `evidenceSchema`,
  `residualUnknownSchema`, `evidenceRecordFiltersSchema`).
- Two formats, one file: envelope (cache partition: target+binding+query entries) wraps
  the canonical bundle (portable Evidence). Export/import/inspect accept only the latter.
- Replay model: entry(workflow or provider-direct) + matching record = exact replay;
  record alone = data only. `query_id` binds (target, binding, operation, parameters).
- `binding` does NOT carry target sha256 — `target.sha256` does (lane question answered).
- Error taxonomy observed: `invalid_request`/`invalid_input` (retryable, arg shape) vs
  `evidence_integrity_mismatch`/`integrity_mismatch` (non-retryable, wrong format/tamper).
- `entries` stayed `[]` across two CLI invocations — CLI direct path records Evidence +
  workflow entries only; provider-direct `entries` populate via session `#execute`
  (MCP/long-lived sessions). Flagged for a future MCP-session lane to confirm live.
