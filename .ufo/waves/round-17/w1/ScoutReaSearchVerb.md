# Scout — `rea search` verb (rea-agents 6.5.0): flags, cost, `--snapshot`, precise argv

Lane: kaidoku round 17, W1 advisory seat. Status: **read-only source inspection** of the installed
package plus `search --help` / `search --schema`. No carrier analysis, `search`, or `decompile` was
executed (round contract). The argv below is therefore **unexercised**; every claim is anchored.

Aliases used below:
- `R` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (npx cache for 6.5.0; `R/package.json` version `6.5.0`)
- `G` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`

## Answer

1. **Verb**: `rea search <path> [pattern] --kind procedures …` maps to provider operation
   `search_procedures`; `--kind strings` (the **default**) maps to `search_strings`.
   Registration: `R/dist/cli/coreBinaryCommands.js:275-318`; selector mapping
   `R/dist/cli/options.js:24-33`.
2. **Cost**: every CLI invocation is a fresh one-shot session. On a cache miss (`--snapshot` cannot
   hit for this verb — see §3) it launches Ghidra headless with `-import <target>`, no `-noanalysis`,
   and `-deleteProject`: full import + full auto-analysis (including the Go analyzers) per call, and
   the project is deleted at close. Source: `R/dist/cli-runtime/binary-BVOr2mgE.js:3869`
   (`-import`), `:3908` (`-readOnly`), `:3909` (`-deleteProject`); `grep -rn noanalysis R/dist R/bridge`
   returns nothing. The open handshake is `client.execute("health")` at `binary-BVOr2mgE.js:12871`.
3. **`--snapshot`**: accepted (help + schema), read and rewritten, but it is an *evidence/query cache*,
   not a Ghidra project. For `search_procedures` it can neither record nor replay from the CLI (§3),
   so it saves **zero** analysis time for `rea search`; it only adds a binding-mismatch failure mode.
4. **Precise argv** (one import, both names): §5. Expected: 2 hits on the in-range esbuild carrier,
   0 inventory rows on the out-of-range shfmt carrier (and that zero is *not* byte absence, §6).

## 1. Surface read from `search --help` and `--schema`

`npx -y rea-agents@6.5.0 search --help` (condensed, 2026-10-20; global options summarized on the
last line):

```
Usage: rea search <path> [pattern] [options]
  path       App or program path                                   (required positional)
  pattern    Literal text or regex pattern                         (optional positional)
  --pattern <string>                          complete pattern; use --pattern=<value> for leading dashes
  --kind <strings|procedures>                 default: strings
  --mode <literal|regex>                      default: literal
  --case-sensitive                            default: false
  --snapshot <string>                         "Load and update a local analysis snapshot"
  --target-format <dos-com|raw-binary>        headerless interpretation
  --architecture <6502|x86|x86_64|arm|arm64>  required with --target-format raw-binary
  --entry-point <0xhex>                       required with --target-format raw-binary
  --provider <value>                          provider ID or auto selection
  --filter-output / --format / --full-output / --token-* / --help / --schema / --llms[-full]
```

- Input contract: `R/dist/contracts/analysisSearchContract.js:3-10` — `{pattern, mode=literal,
  case_sensitive=false, document?}`. Note `document` exists in the contract but **no CLI flag maps to
  it**; `grep -rn "document" R/dist/cli/*.js` shows no command passes it (only output-formatting hits).
- Output item schema: `R/dist/cli-runtime/binary-BVOr2mgE.js:4589-4605` — `search_procedures` is an
  array of `{address, value}`; `value` is the provider's qualified procedure name.
- `--json` is a **hidden incur alias** for `--format json` (`R/../incur/dist/Cli.js:1957-1960`), so the
  bridge's hint `rea search <path> . --kind procedures --mode regex --provider ghidra --json`
  (`R/bridge/ghidra/ReaGhidraBridge.java:1004`, also `:2231`) still works, but use the documented
  `--format json` in receipts.
- If both the positional pattern and `--pattern` are supplied and differ, the CLI rejects the call
  (`R/dist/cli/analysisSelector.js:3-22`).

## 2. Matching semantics and the name form

- **literal = substring, case-folded by default.** JS providers use `String.includes`
  (`binary-BVOr2mgE.js:10539-10549`); the Ghidra bridge uses `candidate.contains(needle)` after
  `toLowerCase(Locale.ROOT)` unless case-sensitive (`R/bridge/ghidra/ReaGhidraBridge.java:4601-4607`).
  So a literal `main.main` matches `main::main.main` and would also match the closure
  `main.main.func1`.
- **regex = unanchored search.** Ghidra compiles a **Java** `Pattern` and calls
  `pattern.matcher(value).find()` (`ReaGhidraBridge.java:4609-4632`); anchors are required for an exact
  match. Case-insensitive unless `--case-sensitive` (`Pattern.CASE_INSENSITIVE|UNICODE_CASE`).
  (Hopper instead uses an ECMAScript worker with a 5 s matching deadline, per the capability
  limitation at `binary-BVOr2mgE.js:2713`; pinning `--provider ghidra` keeps Java semantics.)
- **Procedure names are namespace-qualified.** The bridge emits `symbol.getName(true)`
  (`ReaGhidraBridge.java:3765-3768` `procedureName`, used by `procedureIdentity` at `:4365-4368`;
  `:2151` for the search inventory); Ghidra joins the namespace path with `"::"`
  (`G/Ghidra/Framework/SoftwareModeling/lib/
  SoftwareModeling-src.zip:ghidra/program/database/symbol/SymbolDB.java:180-193`;
  `G/Ghidra/Framework/SoftwareModeling/lib/SoftwareModeling-src.zip:ghidra/program/model/symbol/
  Namespace.java:55`).
- **Go names.** The Go analyzer creates each function with the full pclntab name inside the package
  namespace (`G/Ghidra/Features/Base/lib/Base-src.zip:ghidra/app/plugin/core/analysis/
  GolangSymbolAnalyzer.java:227-238`, `G/Ghidra/Features/Base/lib/Base-src.zip:ghidra/app/util/bin/
  format/golang/structmapping/MarkupSession.java:385-409`); the package
  namespace comes from `GoSymbolName.getSymbolNamespace`
  (`G/Ghidra/Features/Base/lib/Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoSymbolName.java:401-406`)
  and the name from `asString()` (`:347-348`). Result: `main` namespace + `main.main` name →
  **`main::main.main`**, observed on the round-4 Ghidra 12.1.4 run
  (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:32`, `:66-68`).

## 3. Cost: re-import/re-analyze every invocation — `--snapshot` cannot avoid it

Observed source path (`R/dist/cli-runtime/DirectAnalysis-BgvAtpN3.js`):

- `runDirectAnalysis` → `runAnalysis` creates a `BinarySession`, resolves the target/profile with
  `session.previewTarget` (no provider client), then:
  - replay check at `:346-360` (`allowsSnapshotReplay` + `snapshotEvidenceForQuery`); Ghidra declares
    every non-mutating capability `cachePolicy: "snapshot"` (`binary-BVOr2mgE.js:7967`), so the replay
    *is attempted* — it simply never finds a CLI-produced entry (§ below);
  - otherwise `session.open` / `openResolvedTarget` at `:366`, which runs `client.execute("health")`
    (`binary-BVOr2mgE.js:12871`) and therefore starts Ghidra headless with `-import`.
- **Replay gate**: `snapshotEvidenceForQuery` matches a query-id hash of
  `{target, binding, operation, parameters}` (`R/dist/cli-runtime/AnalysisSnapshotCache-BXS0wRd2.js:248-253`).
  Entries are only *recorded* when `cacheable` is true (`binary-BVOr2mgE.js:12670`, `:13087-13105`).
- **Why CLI search is never cacheable**: `isSnapshotCacheable` requires
  `typeof parameters.document === "string"` for every document-scoped operation
  (`AnalysisSnapshotCache-BXS0wRd2.js:560-562`), and `DOCUMENT_SCOPED_OPERATIONS` contains every
  official tool except `current_document`/`list_documents` (`:560`) — `search_procedures` included.
  The CLI passes exactly `{pattern, mode, case_sensitive}` (`coreBinaryCommands.js:311-317`), so
  `document` is absent → `cacheable=false` → no entry is written and no entry can be matched later.
  (The `trace_feature` workflow also calls `search_procedures` without `document`:
  `R/dist/cli-runtime/application__EnhancedTools-oFE2bOjs.js:1209-1222`, so it does not seed one
  either. An MCP caller that passes `document` could create an entry, but the CLI query id would then
  differ by that parameter, so CLI replay still cannot hit.)
- **What the snapshot is**: `target` + `binding` (provider id/name/version + analysis profile) +
  cached query entries + evidence bundle (`AnalysisSnapshotCache-BXS0wRd2.js`, `export`). It contains
  no Ghidra program database, so it cannot stand in for the `-import`.
- **Snapshot I/O behaviour**: a missing path is treated as empty and written after the run
  (`DirectAnalysis-BgvAtpN3.js:475-477`, write at `:397-405`, `overwrite=true`); an existing file is
  read and binding-checked — target sha/format/architecture plus provider profile — and a mismatch
  fails with `profile_mismatch` (`:478-489`).
- **Timeout**: `REA_GHIDRA_STARTUP_TIMEOUT_MS`, default **330 000 ms**
  (`R/dist/config/providerStartupTimeout.js:3`; schema `R/dist/config/environment.js:38`). A startup
  overrun is reported as `provider_timeout` attributed to the running operation; the round-4 log
  records `operation=search_procedures`, `timeout_ms=330000`, then success at `900000`
  (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:31-32`).

Measured prices (observation, not re-run by me):

| Evidence | Carrier | Import+analysis cost |
| --- | --- | --- |
| round-4, rea 6.4.0, row 4-5 | `op` 2.34.1, 41 MB | 5m31.8s → default-timeout FAIL; 6m57.9s with `900000`; 1 hit `main::main.main @ 0x1076920` (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:31-32`) |
| round-17 pilot, same Ghidra 12.1.4 | esbuild 0.25.12, 10,358,936 B | `ghidra.log` JVM start 10:18:19 → post-script 10:19:53 (94 s); reported `Total Time 91 secs` (`pilot/esbuild-0.25.12-log/ghidra.log`) |
| round-17 pilot, same Ghidra 12.1.4 | `/usr/bin/shfmt`, 3,601,168 B | 10:17:28 → 10:17:56 (28 s); `Total Time 24 secs`; Go bootstrap failed (`pilot/shfmt-log/ghidra.log`) |

Both pilot carriers reproduce the SHA-256 values in `pilot/README.txt`
(`58f76563…` shfmt, `bab29b2c…` esbuild). The 94 s / 28 s spans are Ghidra process-start to post-script
and are the floor each `rea search` pays again before the bridge answers the query.

## 4. Answer to "does it accept `--snapshot`?"

Yes — flag, read, binding validation, and write-back all exist. But for `rea search` it is
**cost-neutral at best and a failure mode at worst**: zero replay (source gate above; consistent with
the round-4 command that carried `--snapshot` and still paid a full 5m31.8 s import
(`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:31`).
Recommendation: omit it for searches; add it only if the L1 wants this search's evidence appended to an
existing round snapshot bundle, and expect a rewritten file with no reusable query entry.

## 5. Precise argv

Primary — one import serves both names, anchored so the observed namespaced form and a flat form both
match, while closure names (`main.main.func1`, `runtime.main.func1`) do not:

```sh
REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 \
npx -y rea-agents@6.5.0 search /usr/bin/shfmt \
  --pattern '(^|::)(main\.main|runtime\.main)$' \
  --kind procedures --mode regex --case-sensitive \
  --provider ghidra --format json
```

Same carrier as a Python argv list (raw string keeps the regex's single backslashes; no shell involved):

```python
["npx", "-y", "rea-agents@6.5.0", "search", "/usr/bin/shfmt",
 "--pattern", r"(^|::)(main\.main|runtime\.main)$",
 "--kind", "procedures", "--mode", "regex", "--case-sensitive",
 "--provider", "ghidra", "--format", "json"]
```

esbuild carrier: replace the path with
`/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild`.

Why each token:

- `--kind procedures` is **mandatory**: the default `strings` would search string objects and can hit
  the raw pclntab name string (`grep -ao … | wc -l` finds `main.main` 5 times and `runtime.main`
  4 times in **both** carriers), producing a hit that is not a procedure.
- `--mode regex` + Java `find()`: `(^|::)` accepts `main::main.main` (observed) and flat `main.main`;
  `$` excludes `.func1`/method suffixes. `^…$` alone would **miss** the observed namespaced form.
- `--case-sensitive` is optional (default is case-insensitive); include it for an exact query.
- `--provider ghidra` pins the provider so the evidence provider/profile is deterministic; auto
  selection on this host would also choose Ghidra, but pinning removes a silent route change.
- `--format json` prints the evidence object itself (`R/dist/cli/cliResultOutput.js:134-158`:
  `--full-output` would wrap it as `{ok,data,meta}`); rows are `normalized_result[].{address,value}`.
- `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` is not needed for these small carriers (91 s / 24 s analysis
  vs a 330 s default) but is the measured lever for large carriers; it is an env var, not a flag.

Fallback only if the anchored regex returns 0 on a carrier where recovery is expected (costs another
import): `--pattern 'main\.main|runtime\.main'` unanchored, or two literal calls `--pattern main.main`
and `--pattern runtime.main`.

## 6. Calibration cautions for this round

- **0 hits ≠ absent.** shfmt is go1.27.0, outside Ghidra's 1.15-1.25 range; its pilot log already shows
  `Untested Go version [1.27.0]`, `Missing Go bootstrap type info`, and
  `Go symbol analyzer error: unable to get GoRttiMapper` (`pilot/shfmt-log/ghidra.log:83-89`). Expect
  **0 inventory rows** for both names on shfmt even though the byte strings are present. Phrase it as
  "no inventory row", never "no `main.main`" — the r14 review corrected exactly this overclaim
  (`.ufo/waves/round-14/w1/ReviewGoInference.md:102`, `:125`;
  `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:33`, `:74`).
- **esbuild** (go1.23.12, in range) recovered Go symbols in the pilot (snapshot 1.23.12, 2248+2055
  signatures fixed: `pilot/esbuild-0.25.12-log/ghidra.log:62-74`), so it is the carrier where 2 hits
  (`...::main.main`, `...::runtime.main`) are expected. If it returns 0, suspect the name form or a
  provider route change before concluding absence.
- Two names in one invocation is the cheap move: two literal searches would pay two full imports
  (~2×94 s on esbuild at pilot scale, potentially ~2×7 min at round-4 scale).

## 7. Remaining unknowns (bounded)

- The argv was not executed; `search` invocation count for this round is L1-controlled. Flags are
  verified from `--help`, `--schema`, and registration source, not from a live response.
- Exact 6.5.0 wall time for `search` on these carriers is unmeasured; the 94 s / 28 s figures are the
  Ghidra start-to-post-script span from the pilot `analyze` runs, plus bridge/query time.
- The `runtime.main` name on this Go 1.23.12 build is inferred from Ghidra 12.1.4's documented naming
  plus the round-4 observation (`runtime::runtime.mstart0` in the same symbol family,
  `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:66-68`); the anchored pattern covers both
  namespaced and flat spellings.
- Cross-version snapshots (e.g. a 6.4.0-produced entry) were not inspected; 6.5.0's recorder cannot
  create a search entry from the CLI at all.

## 8. Tooling

No installs or upgrades were performed; all evidence came from the existing npx cache
(`rea-agents@6.5.0`, `incur`) and the installed Ghidra 12.1.4 source archives.
