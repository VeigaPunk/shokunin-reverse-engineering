# PredictAddressVerbs — R27-C1 rename prediction from 6.5.0 code

Question: at rea-agents 6.5.0, for decompile, xrefs, read-bytes, function and instructions,
does a renamed copy (other directory, file name and extension) change the evidence id?

Method: read the pinned 6.5.0 bundle and the round-26 envelopes (`git show main:...`).
No round-27 envelope, no `seats/Run*` path and no REA call was read or made; this is a
prediction made before that data exists. Every prediction row below is labelled inference.

## Observations (producing commands, exit 0, UTC 2026-10-22T14:55–15:01Z)

O1. The id hashes the projection at `dist/domain/evidence.js:156-180`; the subject entry
    keeps only `digest`, `format`, `architecture` (lines 158-163). `subject.name` and
    `subject.local_path` are not in the projection; line 181 states the rule:
    "Hash semantic content, including raw results and excluding display-subject fields."
    `computeEvidenceId` = `ev_` + `digestCanonicalValue(semanticProjection(...), "Evidence")`
    (line 182).
O2. The only place a file name enters an evidence object is `evidence.js:211` and
    `evidence.js:260-262`, both `name: basename(target.path)`, i.e. the unhashed display
    subject. `grep -rn "basename(" dist/application/*.js dist/cli/*.js dist/domain/*.js`
    returns no other writer of a name into evidence.
O3. `parameters` *is* hashed (evidence.js:168) and every verb feeds it the CLI argument
    object (DirectAnalysis.js:282 `parameters: input.arguments`). Those objects hold only
    addresses/length: decompile `{procedure}` (coreBinaryCommands.js:130-137), xrefs
    `{address}` (:182-184), function `{procedure}` (:241-243), instructions `{procedure}`
    (:270-272), read-bytes `{address,length}` (coreNativeCommands.js:63). The positional
    `path` is passed to `runDirectAnalysis`, never into `arguments`.
O4. Subject format/architecture are byte-derived: ELF magic in `domain/binaryTarget.js:11-13`;
    `namedArtifactFormat` (BinaryTargetResolver.js:260-268) lists only `.asar`, `.plist`,
    `.map`, `m?js|cjs`, so `.dat` falls through to header parsing. Ghidra is launched as
    `-import <targetPath>` with no `-loader` for a normal ELF (GhidraLauncher.js:327-336),
    so the loader is header-selected, not extension-selected.
O5. Bridge results for the five verbs are content only: decompile returns
    `DecompiledFunction.getC()` (ReaGhidraBridge.java:3333); xrefs returns sorted
    reference source addresses (:1392-1412); read-bytes returns address, requested/returned
    counts, `bytes_hex`, `complete` (:732-738); instructions returns `procedureIdentity`
    plus `address: mnemonic operands` lines (:1034-1057, :3629-3643); function returns the
    dossier socket set built from references, comments, symbols and strings (:1539-1600).
    Procedure names come from `symbol.getName(true)` / `function.getName()`
    (:3765-3768) — Ghidra symbols, identical for identical bytes.
O6. The Ghidra program name (which equals the file name) exists at exactly two places:
    `sessionInfo` `target.name` (:486) and `list_documents` (:1974-1975). Neither is an
    evidence field. `requireDocument` accepts a null document (:4694-4698) and the wire
    schema defaults `document` to null (GhidraFunctionValues.js:33).
O7. Round-26 control (directory-only rename, /usr/bin/jq → .../carrier/alt/jq):
    decompile ev_03d786…, xrefs ev_d591ef…, read-bytes ev_99b0c6…, function ev_b2b7e9…,
    instructions ev_b20a0f… were each identical in base, repeat and copy; `subject.name`
    stayed "jq" while `local_path` changed. inspect-binary-layout alone changed
    (ev_294a44… → ev_52da4b…), and it is the one verb carrying `parameters.path`,
    `normalized_result.artifact.path` and `locations[0].path`.
O8. `sha256sum` (exit 0, 14:59:20Z) gives e8156675… on both /usr/bin/jq and
    jq-r27-renamed.dat, 7b1e5d0c… on both /usr/bin/tinyxxd and tinyxxd-r27-renamed.dat.

## Prediction (all rows inference; confidence is per row)

| verb | prediction | hashed fields that could carry the name | file:line evidence | confidence |
|---|---|---|---|---|
| decompile | content-keyed | `raw_result.value`, `normalized_result` (the C text), `parameters{procedure}`, `analysis_profile` | evidence.js:156-170,206-262; ReaGhidraBridge.java:3333; coreBinaryCommands.js:130-137 | high |
| xrefs | content-keyed | `raw_result`/`normalized_result` address array, `parameters{address}` | ReaGhidraBridge.java:1392-1412; coreBinaryCommands.js:182-184 | high |
| read-bytes | content-keyed | `bytes_hex`, counts, `parameters{address,length}` | ReaGhidraBridge.java:732-738; coreNativeCommands.js:63 | high |
| function | content-keyed | `raw_result.value` dossier, `referenced_strings`, `referenced_names`, `procedure.name`, `parameters{procedure}` | ReaGhidraBridge.java:1539-1600,3765-3768; coreBinaryCommands.js:241-243 | medium-high |
| instructions | content-keyed | `procedure.name`, rendered `address: mnemonic operands` lines, `parameters{procedure}` | ReaGhidraBridge.java:1034-1057,3629-3643; coreBinaryCommands.js:270-272 | medium-high |

Mechanism: the file name reaches the digest only if a verb (a) puts the path in `parameters`
or (b) returns text echoing the path or program name; none of these five does either, so the
renamed run should reproduce the base id while `subject.name`/`local_path` differ.

Per verb, the name-bearing candidate and why it is empty: decompile — `getC()` returns raw C
text whose only names are address-derived (`int FUN_00103fa0(undefined8 param_1)`); xrefs —
referring instruction addresses only; read-bytes — memory bytes and counts only; function —
`procedure.name` is `FUN_00103fa0` and the "jq" tokens in the 840 KB round-26 dossier are
`.rodata` strings such as `jq: error (at %s): %s`, present because the bytes contain them;
instructions — operands resolve to the binary's own symbols.

## Falsifier

The prediction fails if, for any of the ten (carrier, verb) cells, the renamed envelope's
`evidence_id` differs from its base id while base equals repeat. The first fields to diff
between base and renamed are `raw_result` and `normalized_result`; a token such as
`jq-r27-renamed` or `tinyxxd-r27-renamed` inside either would name the mechanism.

## Unknowns / residual risks

U1. Repeat determinism on tinyxxd is unobserved (round 26 covered jq only); a base != repeat
    would make a row "unstable" for reasons unrelated to the rename and hide the test.
U2. Ghidra-internal analysis could in principle key on the program name. No code path in the
    shipped bridge or provider does; this is an inference about the bundled source, not a run.
U3. Two carriers, one address per carrier, one pin; nothing is predicted for other verbs,
    other pins or error envelopes.
U4. grep was the literal fallback: no `lsp` device is registered in this session (only
    `xd://ast_edit` and `xd://debug`) and no server answers a bundled `.js` or the Ghidra
    `.java` bridge, so every pointer above is a text locator, not a semantic rename trace.

## Sources (opened 2026-10-22, ordinary local reads)

| path | sha256 | quote (<=25 words) |
|---|---|---|
| .../rea-agents/dist/domain/evidence.js | f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff | "Hash semantic content, including raw results and excluding display-subject fields." (line 181) |
| .../rea-agents/bridge/ghidra/ReaGhidraBridge.java | db16aed4d16ab94da883843281ef7a8a33a244cd8379bd4013e8dee479c0a105 | "return value == null ? null : value.getC();" (line 3333) |
| .../rea-agents/dist/application/BinaryTargetResolver.js | 8a07f32df3e9554687a82194763feab35aa97f139114005a377ffa88606e136f | "const namedArtifactFormat = (lowerPath) => {" (line 260; `.dat` absent) |
| .../rea-agents/dist/ghidra/GhidraLauncher.js | 739676ebc64bd7b23ed1bc4a9395d596efe7bf8080eb67af1ff3e00d86609a67 | `"-import",` `options.targetPath,` (lines 329-330) |
| .../rea-agents/dist/cli/coreBinaryCommands.js | e5faf2533eb7e5f12bc40197727561292e2b831a5ca06d908fc06098da8236ed | "runDirectAnalysis(args.path, \"procedure_pseudo_code\", {" (line 130) |
| .../rea-agents/dist/cli/coreNativeCommands.js | 1ca9f8e3a53b1eabe0065eafb76ca33d528b77d739b216d2b21e3f83ec9a0170 | "runDirectAnalysis(args.path, \"read_bytes\", { address: args.address, length:" (line 63) |
| .../rea-agents/dist/application/DirectAnalysis.js | 09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617 | "parameters: input.arguments," (line 282) |
| .../rea-agents/package.json | a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c | "version": "6.5.0" (line 4) |

package root: /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/ (read-only).

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/PredictAddressVerbs/)

| path | sha256 |
|---|---|
| artifacts/r26-verb-field-map.txt | d1eeeaab6fb1cb81ce8682af904c2e1631d64da795e01367aba1154936cf4744 |
| artifacts/source-excerpts.txt | 4d4047aeba0111ca1c1a37a63ef4ed3858c9eefbd6fb74cc0e7240a52763143e |

`r26-verb-field-map.txt` records per round-26 verb and run kind the id, subject name, local
path, sha256, operation, parameters, locations and environment (`git show main:...`).
`source-excerpts.txt` holds the numbered line ranges cited above. No tool was installed or
upgraded; nothing in the lane was written except this report.
