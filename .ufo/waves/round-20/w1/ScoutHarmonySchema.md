# ScoutHarmonySchema — `project-harmony-application-graph` input contract

Seat: `KaidokuR20.ScoutHarmonySchema-2` (read-only scout; no lane writes, no installs, no subagents).
Written: 2026-10-20T17:51:24-03:00 (`date -Iseconds`).
REA package under read: `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/` (rea-agents 6.5.0, already cached; nothing installed this seat).
Labels: **OBS** = directly observed (command output or read source); **INF** = inference from those observations.

## 1. `--schema` capture (OBS)

```
$ npx -y rea-agents@6.5.0 project-harmony-application-graph --schema ; echo "EXIT=$?"
args:
  type: object
  properties:
    inputJson:
      type: string
      description: Inline workflow JSON or JSON file path
  required[1]: inputJson
  additionalProperties: false
EXIT=0
```

The schema is only the CLI **args wrapper**: one required argument `inputJson` (`Inline workflow JSON or JSON file path`), supplied positionally in every run below. It does **not** expose the workflow payload. The payload schema is applied inside the command run against `harmonyApplicationProjectionInputSchema` (`cli/applicationCommands.js:158`); `--schema` cannot be cited as documenting `inventory_evidence` (INF: any report implying otherwise would be wrong).

Command identity: `cliCommandNames.js:155` (`projectHarmonyApplicationGraph: "project-harmony-application-graph"`); registration `cli/applicationCommands.js:108-116`; tool contract `contracts/applicationToolContracts.js:242-247` (name `project_harmony_application_graph`, predicate `rea.harmony-application-graph`).

## 2. Input payload (OBS, source)

`domain/mobileApplicationGraphProjection.js:13-15` — `z.strictObject({ inventory_evidence: z.array(evidenceSchema).min(1) })`, re-exported unchanged as the harmony input schema (`domain/harmony/harmonyApplication.js:12`). Strict: any extra top-level key is rejected.

## 3. What inventory Evidence is accepted (OBS)

1. **Envelope**: strict Evidence record with exactly the 16 fields at `domain/evidence.js:98-117`; `evidence_id` is `ev_<sha256>` over the canonical semantic projection and is *recomputed and enforced* (`domain/evidence.js:133-141`, `:182`, `:184-190`). A structurally plausible but recomputed-wrong id is rejected.
2. **Carrier operation** (`domain/artifactInventoryEvidence.js:16-23`):
   - `operation === "inventory_artifact"` → used directly, or
   - `operation === "inspect_artifact"` → `normalized_result.substeps[0].evidence` is taken (only index 0) and must itself be `inventory_artifact`. This second route is the only one reachable from the CLI (see §5).
3. **Payload** must satisfy `artifactInventoryResultSchema` (`domain/artifactGraph.js:177`): `manifest{manifest_id, root_artifact_id, root_sha256, root_format, graph_sha256, node_count, occurrence_count, edge_count}`, `nodes[]`, `occurrences[]`, `edges[]`, `provenance[]`, `integrity_contradictions[]`, `coverage{scope,status}`, `limitations[]` (`coverage_status` optional for legacy).
4. **Subject binding** (`artifactInventoryEvidence.js:42-47`): `subject` must be non-null, `subject.digest.sha256 === manifest.root_sha256`, and `subject.format === manifest.root_format`.
5. **Per-page invariants** (`:48-55`): unique `node/occurrence/edge` ids; every node id must be the content address `art_<sha256 of {sha256}>` (`domain/artifactIdentity.js:22`).
6. **Root invariants** (`:187-190`): a `.` occurrence must exist, its `artifact_id` must equal `manifest.root_artifact_id`, and its `artifact_format` must equal `manifest.root_format`. Multi-page merge requires *identical* manifest, coverage declaration, and contradictions (`:67-81`).
7. **Root format gate** (`domain/harmony/harmonyApplication.js:10`, `:104-108`): `manifest.root_format ∈ {hap, hsp, app-pack}`; anything else raises `HarmonyOS application projection requires HAP, HSP, or App Pack inventory Evidence (got <fmt>)`.

**Coverage rule** (`harmonyApplication.js:95`; `mobileApplicationGraphProjection.js:39-45`; `artifactInventoryEvidence.js:9-11`): `complete-within-inventory` requires `inventory.complete` (node/occurrence/edge counts equal the manifest counts, `:113-115`) **and** `coverage.scope === "container-entries"` **and** `coverage.status === "complete"` **and** bridge budget not exceeded **and** zero `unavailable_components`.

## 4. Archive members → component arrays (OBS; `harmonyApplication.js:110-127`)

| member pattern (case-insensitive) | lands in | other effect |
|---|---|---|
| `(^|/)module\.json$` | `components.manifests` | `packaging_model: "stage"` (wins over FA) |
| `(^|/)config\.json$` | `components.manifests` | `packaging_model: "fa"` only if no `module.json` |
| `(^|/)pack\.info$` | `components.manifests` | **no** effect on `packaging_model` |
| `\.(abc\|pa)$` | `components.bytecode` | `runtime_families += ark`; left side of every bridge candidate |
| `(^|/)resources\.index$`, `^(resources/\|assets/<x>/resources/)` | `components.resources` | — |
| occurrence `format === "elf"` **or** `(^|/)libs/<abi>/<name>\.so$` | `components.native_libraries` | `runtime_families += native` **only** when `format === "elf"` |
| occurrence `format === "javascript-bundle"` **or** `\.(m?js\|cjs)$` | `components.javascript` | `runtime_families += javascript` **only** on the suffix |
| `^META-INF/<name>\.(p7b\|sig\|cer\|crt\|pem\|provision)$` | `components.signing` | ZIP signing block is not an entry (`:65`) |
| `.hap`/`.hsp` occurrence, `root_format === "app-pack"` | `app_pack_children` | `:89-91` |
| exact segments `libreactnative.so`, `libhermes.so`, `libflutter.so`, `libunity.so`, `*.framework` set | `runtime_families` | `domain/nativeConvention.js:3-21` |

- `.har` is never identified (`:73`), by design.
- Component `format` is the **occurrence** `artifact_format` (full `artifactFormatSchema`, `domain/artifactGraph.js:32-60`), not the node content format (`:62-73`); `mobileApplicationGraphProjection.js:47-62`.
- `bridge_candidates` = full Cartesian `bytecode × native_libraries` (`harmonyApplication.js:144-152`); basis `napi-library-convention` iff the native path matches `libs/<abi>/lib<name>.so` (`:154-156`), else `managed-and-native-content`. JavaScript is **not** a managed side; a JS-only HAP yields zero candidates.
- Budget: retained candidate JSON capped at 2 MiB (`domain/bridgeCandidateProjection.js:12`); overflow flips `bridge_candidate_coverage.status` to `partial`, adds a limitation, and flips projection coverage to `partial`.
- Projection output is `confidence: inferred`, `authority: analyst-inference` (`application/InventoryProjectionEvidence.js:32-33`), never `observed`; it records `parameters.inventory_evidence_ids` from the same list as `source_evidence_ids` (`:25`).

## 5. Producer side: how admissible Evidence is obtained (OBS)

- There is **no CLI `inventory-artifact` verb** (`cliCommandNames.js` has none; only `inspectArtifact: "inspect-artifact"` at `:35`). The CLI producer is `inspect-artifact` (`cli/artifactCommands.js:144-168`), whose output `normalized_result.substeps[0]` is the `inventory_artifact` Evidence.
- Root classification: `.hap`/`.hsp` from suffix (`domain/zipPackageFormat.js:45-47`); `.app` → `app-pack` **only** for root inputs and only after ZIP signature verification (`artifacts/inventory/classify.js:73`, `:102-104`; `domain/zipPackageFormat.js:15-23`).
- Global `--format json` emits the bare Evidence object (no `{ok,value}` wrapper); `--schema`, `--llms`, `--filter-output` exist as global options (`inspect-artifact --help`, EXIT=0).

## 6. Runs (all in `mktemp -d /tmp/kr20-harmony-scout.GdjYcJ`; no lane/Go/Ghidra execution)

| # | command | exit | observed |
|---|---|---|---|
| 1 | `project-harmony-application-graph --schema` | 0 | args wrapper only (§1) |
| 2 | `project-harmony-application-graph '{"inventory_evidence":[]}'` | 1 | `operation: project-harmony-application-graph`, `issues[1] path inventory_evidence reason out_of_range minimum 1` |
| 3 | `node build.mjs` (hand-built content-addressed inventory + `createEvidence`) | 0 | valid Evidence, 11 nodes/11 occurrences |
| 4 | `project-harmony-application-graph hap-input.json` | 0 | `packaging_model: stage`; manifests `module.json,pack.info`; bytecode 1; resources 2; native 2; javascript 1; signing 1; families `ark,flutter,javascript,native`; 2 bridge candidates; `coverage complete-within-inventory`; `limitations[6]` |
| 5 | `project-harmony-application-graph apk-input.json` (root_format changed, root occurrence not) | 1 | `Artifact root occurrence does not match its manifest representation` — inventory validation runs **before** the root-format gate |
| 6 | consistent `apk` variant | 1 | `requires HAP, HSP, or App Pack inventory Evidence (got apk)` |
| 7 | consistent `app-pack` variant | 0 | `app_pack_children[1] child.hap`; `limitations[8]` (+2 app-pack notes); `coverage complete-within-inventory` |
| 8 | `config.json` only | 0 | `packaging_model: fa`; `manifests[2] config.json,pack.info` |
| 9 | `module.json` + `config.json` + `libunity.so` | 0 | `packaging_model: stage` (stage precedence); families `javascript,native,unity` |
| 10 | `python3` builds real `carrier.hap` ZIP (module.json, pack.info, ets/modules.abc, resources.index, resources/base/element/string.json, assets/main.js, META-INF/CERT.p7b, `libs/arm64-v8a/libentry.so` = copy of `/usr/bin/true`) | 0 | 17,999 bytes |
| 11 | `inspect-artifact carrier.hap --format json` | 0 | 14,458-byte **bare Evidence**; `operation: inspect_artifact`; `substeps[0].operation == inventory_artifact` |
| 12 | wrap `{"inventory_evidence":[<inspect evidence>]}` → `project-harmony-application-graph wrapped.json --format json` | 0 | `root_format hap`, `packaging_model stage`, native `libentry.so[elf]`, javascript `main.js[javascript-bundle]`, all others `[file]`, `runtime_families [ark,javascript,native]`, 1 bridge candidate, `coverage complete-within-inventory`, `limitations[7]` |

Run 12 result ids (OBS): input inspect `evidence_id ev_9bc6e68d25cbb888e0e7da673eb3797ef99d30e1b63caa424b196cf89e6f6f07`, subject sha256 `2da95e4c79f158d5a6597deeb9a99d1593262e28d8a83d72ae34975af6ab2ff5`; projection cites **that outer id** in `source_evidence_ids`/`parameters.inventory_evidence_ids` (**not** the nested inventory id).

## 7. Notes for C2 evidence (INF)

1. **Hand-built Evidence is schema-valid but not admissible.** The node-built fixtures (runs 3-9) pass every gate yet no `inventory_artifact` process observed the carrier. C2 wants "runs on real (or recipe-retained synthesized) carriers"; cite only Evidence produced by run 11 on a real/recipe ZIP.
2. **Recipe** (deterministic, ~30 KB): build the ZIP from §6 run 10's member list, `inspect-artifact <hap> --format json > inspect.json`, wrap as `{"inventory_evidence":[<inspect.json>]}`, run the projection with `--format json`. Retain `inspect.json`, the wrapped input, the projection output, and the ZIP recipe under `.ufo/waves/round-20/evidence/c2/`; cite the **outer** `ev_` id and `subject.digest.sha256` (= `root_sha256`) in the knowledge entry.
3. `--schema` must not be cited as evidence of the `inventory_evidence` shape; cite `domain/mobileApplicationGraphProjection.js:13-15` + run 12.
4. Error identity differs by layer (OBS): CLI zod rejection reports `operation: project-harmony-application-graph`, while domain/inventory failures report `operation: project_harmony_application_graph`. Both are `code: invalid_request`, `category: invalid_input`, exit 1.
5. No Harmony carrier exists in the lane: `find . -path ./.git -prune -o \( -iname '*.hap' -o -iname '*.hsp' -o -iname '*.har' \) -print` → EXIT=0, **no output**. A carrier must be synthesized (recipe above) or downloaded.
6. Do not expect `runtime_families` to contain `native` from a path alone: `libs/<abi>/*.so` with non-ELF bytes is listed under `native_libraries` but adds no `native` family (INF: `harmonyApplication.js:128-138` gates the family on `format === "elf"`; run 3 set the occurrence `artifact_format` to `elf` and did emit `native`).
7. Environment observation: `git rev-parse --short refs/heads/main` → `d1d981d` (EXIT=0); the dispatched baseline in `contract.md` is `14f0260`. No lane write was made.

## 8. Unresolved

- Encrypted-entry path into `unavailable_components` not exercised (synthetic ZIP cannot easily carry a real encrypted member).
- Multi-page (`inventory_evidence` length > 1) merge not exercised; merge code at `artifactInventoryEvidence.js:67-81` is unverified by run.
- A true `.app` App Pack root (ZIP magic + `.app` suffix, with `pack.info` and child `.hap`) was simulated only via manifest `root_format`, not via producer classification.
- `.hsp` root accepted by enum but not exercised end-to-end.
- No claim about the MCP surface: the OMP `rea` MCP entry is operator-owned and was not used.
