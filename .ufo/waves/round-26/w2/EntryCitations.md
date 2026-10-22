# R26 W2 EntryCitations — package file:line citations in the round-26 C1 entry

Seat: KaidokuR26.EntryCitations. Target: every file:line citation the entry
`corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` makes into the
6.5.0 and 6.7.0 rea-agents packages. Package roots: 6.5.0
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`, 6.7.0
`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/`. All checks are reads
of package files and lane evidence; no lane file was modified, no git/jj command run,
no REA CLI call, no tool installed or upgraded.

Method: each cited file copied to scratch, sha256-pinned, then read through
`nl -ba <file> | sed -n 'A,Bp'` excerpts so line numbers are exact. Where a producing
command is given, it exited 0 unless stated.

## Verdicts

### 1. `dist/domain/evidence.js:182` (6.5.0) — mints `ev_` + SHA-256 of a canonical-JSON projection — HOLDS
Line 182 exactly: `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;`
`digestCanonicalValue` is "Streaming SHA-256 over canonical JSON" with RFC 8785 key
order (dist/domain/canonicalDigest.js:2-8). Observation; command `nl -ba evidence.js`
excerpt, file sha256 below.

### 2. `evidence.js:156-180` (6.5.0) — the semantic projection — HOLDS
156 `const semanticProjection = (evidence) => ({` … 180 `});`. Subject keeps only
`digest`, `format`, `architecture` (157-163); no `name`, no `local_path`. Kept fields
include provider (164), analysis_profile (165), parameters (168), raw_result (169),
normalized_result (170), limitations (174), locations (178), evidence_links (179) —
matching the entry's field list.

### 3. `evidence.js:175-178` in each package — relationship_coverage divergence — HOLDS, range is a loose bracket
- 6.5.0 lines 175-177: `...(evidence.relationship_coverage === null ? {} : { relationship_coverage: evidence.relationship_coverage }),` (3 lines) — omits the key when null. Line 178 is `locations` (unrelated).
- 6.7.0 line 178: `relationship_coverage: evidence.relationship_coverage,` — unconditional. Lines 175-177 are `authority`, `environment`, `limitations` (unrelated).
The claimed behavior is exactly right in both packages; the shared 175-178 bracket
contains the diverging construct in each (6.5.0: 175-177; 6.7.0: 178) plus one to three
uninvolved lines. Cosmetic imprecision only.

### 4. `BinaryLayoutService.js:61-67` (6.5.0) — path into three kept fields — HOLDS
61 `parameters: input.data,` (input.data carries `.path`); 62 `result: value,` where
`normalizeEvidenceObservation` maps result to `normalized_result` and value.artifact.path
is the run path (51, 55); 67 `locations: [{ kind: "artifact-path", path: value.artifact.path }],`.
Envelope side (observation, jq over `corpus/evidence/round-26/c1/envelopes/*-base.json`,
2026-10-22T13:05:55Z / 13:06:26Z): all seven other verbs have `parameters.path` null,
no `normalized_result.artifact.path`, empty locations; `inspect-binary-layout` has
`parameters.path` `/usr/bin/jq`, `normalized_result.artifact.path` `/usr/bin/jq`,
locations `[{"kind":"artifact-path","path":"/usr/bin/jq"}]`.

### 5. `GhidraTargetSnapshot.js:14` (6.5.0) — content-named byte copy — HOLDS
Line 14 exactly: `const snapshotPath = join(runtimeRoot, \`target-${expectedSha256.slice(0, 12)}${suffix}\`);`
— a copy named from the sha256 commitment, inside the private runtime root; the POSIX
branch copies bytes and verifies the streamed sha256 against the commitment (31-48),
and the copy is what the client snapshots at startup (GhidraClient.js:418-419).

### 6. `PrivateRuntimeRoot.js:38` (6.5.0) — fresh private root, deleted after the run — HOLDS with a pointer note
Line 38 exactly: `const path = await mkdtemp(join(options.parent ?? tmpdir(), options.prefix ?? "rea-provider-"));`
— fresh owner-only root per `create()`. Deletion is not on line 38 but in the same
file: `close()` 47-55 runs `rm(this.path, { recursive: true, force: true })`, and the
Ghidra client wires it after the run (`#cleanup` 563-614 calls `#removeRuntimeRoots`
638-663). The composite entry sentence is supported; a reader following only line 38
sees freshness and privacy, not the removal.

### 7. `AnalysisSnapshotCache.js` (6.5.0) — in-memory, content-keyed, replay adds a limitation — HOLDS
Header 44: "Bounded in-memory cache for one immutable binary identity"; state is two
`Map`s (46-47); the file does no file I/O. Keys are `analysisQueryId` = `query_` + sha256
of canonicalJson({target, binding, operation, parameters}) (dist/domain/analysisSnapshot.js:330-332),
and `snapshotTarget` is the "path-free identity used for cache invalidation"
(analysisSnapshot.js:234-252). A cache hit adds the limitation "Loaded from a local REA
analysis snapshot; this call did not re-run the provider." (183-186), which lands in the
hashed `limitations` field, so it would change the id. The snapshot file is read only
when the CLI `snapshot` option (rendered `--snapshot`; option declared in
dist/cli/coreBinaryCommands.js:24-28 and peers, mapped at dist/cli/options.js:33) is
set: dist/application/DirectAnalysis.js:317-321 `if (snapshotPath === undefined || !(await fileExists(snapshotPath))) return ok({});`.
The literal string `--snapshot` does not appear in dist (the parser composes the
prefix); the flag name in the entry is nonetheless correct.

## Artifacts (scratch, sha256)
All under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/EntryCitations/`:
- raw/evidence-650.js f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff
- raw/evidence-670.js a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb
- raw/BinaryLayoutService-650.js b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4
- raw/BinaryLayoutService-670.js 8967371dc654acfba131ff006cbc568b5502d0bf203c450dd384df90017d6d4d
- raw/GhidraTargetSnapshot-650.js a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b
- raw/GhidraTargetSnapshot-670.js f9677c4d7f63fa34380d107f0d7f49de3fcd5488d517a75fd4c1fad99ddd9b15
- raw/PrivateRuntimeRoot-650.js c2244a2c9b86b5c8dba68d424e6962b81a4749664b193fd8cf4a825d9e59bdcc
- raw/PrivateRuntimeRoot-670.js c2244a2c9b86b5c8dba68d424e6962b81a4749664b193fd8cf4a825d9e59bdcc
- raw/AnalysisSnapshotCache-650.js 63b5721b93aa94aa888cdf3e00f56c2dbd0b676bfe965482ccd44f0398fbab8e
- raw/AnalysisSnapshotCache-670.js 63b5721b93aa94aa888cdf3e00f56c2dbd0b676bfe965482ccd44f0398fbab8e
- excerpts/ev650-150-190.txt a6d9ba11eab44eeae37ecc9b68a22e122df49b25dacbf8c7fc15383af52dbc3d
- excerpts/ev670-158-198.txt 84c3b0f439d300167dae3d866261acc588d19c637d531150097750011b00e9d9
- excerpts/bls650-45-70.txt 4c01d7d5c50c35da71e882a9a07372b9e2d9242ab31f2d42b0191cca85168568
- excerpts/gts650-1-30.txt 043af405b6eff9eb04768f9b9c1ecb5ae68ebd3bb71e862c364122b032b314c9
- excerpts/prr650-28-56.txt b9d968a8fbb4464b40eed81b888876f7c02d3981d2e9f87559873a6314d13986
- excerpts/asc650-full.txt 6eb9fe64ec0e1c5f217a4ecb00ebb557e1f973ea5e59baf6316c8f65e0f7964c

## Residual risk and gaps
- I verified the cited lines, not the full wave result; envelope-level id recomputation
  and live reruns belong to other seats and were not repeated here.
- The 6.7.0 `function` analysis_profile naming change is a PinSourceDiff seat claim, not
  among my citations; not checked.
- Only `evidence.js` is cited in both packages; the other four files were confirmed
  present in 6.7.0 (hashes above) but the entry cites them only at 6.5.0, so 6.7.0 line
  numbers for them were not asserted or checked.
- First jq pass over the envelopes used a type-unsafe filter and errored on `decompile`
  (exit 5, 13:05:55Z); the null-safe rerun at 13:06:26Z covered decompile and xrefs and
  is the evidence of record for those two.
