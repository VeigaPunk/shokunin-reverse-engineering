# Wave 2 critic: CriticEntryMechanism (round 27)

Seat: KaidokuR27.CriticEntryMechanism. Lane tip under attack 4084d8975b684a8837b1c858eea0008ce9ab49e0. Read-only; no REA run (item does not authorize REA); no installs.
Attacked: the causal claim in `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` (Why, Decision rule, Limits) and SKILL.md round-27 section that only the file extension, not the directory or the rest of the name, changes the `analyze` and `inspect` ids.

## Verdicts

1. Core claim on the tested route (Ghidra provider, Linux, CLI, regular-file copy): holds.
2. Mechanism sentence "the suffix is the caller's extension": fails. Counterexample: a symlink. On Linux the resolver calls `realpath` first, so the snapshot suffix comes from the canonical target, not the caller's name.
3. Decision-rule row "address verbs: equal ids whatever the path, name or extension" (also SKILL table: "no hashed field carries the path, name or extension"): fails for carriers or settings that route by extension. Counterexample: a byte copy named `jq.js`, `.mjs`, `.cjs`, `.map`, `.plist`, `.asar` or `.hop`. The extension picks the hashed `subject.format` (or a Hopper database route) before Ghidra is reached. This is inference from the code, not run.
4. Limits: they do not say enough. They omit the provider (Hopper builds `document` differently), the platform (Windows keeps the caller path), symlinks, the extensions that change the route, and the case-sensitive suffix.

## Checks (all exit 0; labels: OBS observation, INF inference, UNK unknown)

C1. 2026-10-22T15:35:53Z. `python3 -I -B diff_leaves.py <lane>/corpus/evidence/round-27/c1/envelopes`. Every leaf of base vs renamed and base vs repeat, for all 16 pairs.
Excerpt: `jq analyze ... base-vs-renamed differing=5`; the only hashed one is `renamed HASHED data.normalized_result.document: 'target-e815667571d0.bin' -> 'target-e815667571d0.dat'`. The others are `evidence_id`, `subject.local_path`, `subject.name` and `meta.duration`. tinyxxd `analyze` and `inspect` show the same pattern with `target-7b1e5d0c970a`. The five address verbs have no differing hashed leaf. `parameters` is `{}` for analyze and inspect, `locations` is `[]`, and `evidence_links` is `[]` in all 16 renamed envelopes.
OBS: on these envelopes the directory and the file stem appear in no hashed leaf of `analyze` or `inspect`. Verdict 1 holds.

C2. 2026-10-22T15:36:14Z. `sha256sum` and `sed -n` on the 6.5.0 package (`package.json` a500302319c1…0a6c). The CLI entry is `scripts/rea.mjs`. The code that actually runs is the bundle `dist/cli-runtime/binary-BVOr2mgE.js` (sha256 64c07dae…00df). Its lines 5258-5320 contain `const suffix = safeExtension(sourcePath)` and `/^\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : ".bin"`, the same logic as the cited `dist/ghidra/GhidraTargetSnapshot.js:13-14, 76-78` (a27e4107…3f52b).
OBS: the cited file is not the one that executes, but its logic is identical. This is a provenance nit only.

C3. 2026-10-22T15:38:50Z. `sed -n` on `dist/cli-runtime/application__EnhancedTools-oFE2bOjs.js`, lines 1009-1022 and 1718-1737, and `bridge/ghidra/ReaGhidraBridge.java`, lines 1973-1977.
Excerpt: `#binaryOverview` gets `document` from `resolveAnalysisDocument`, which tries `current_document` and then `list_documents`. The Ghidra bridge answers `result.add(currentProgram.getName())`. The bridge never calls `getExecutablePath` (grep at 15:36:24Z found nothing), and the session `target.name` is dropped by `sessionInfoSchema` (lines 5171-5200).
OBS: on the Ghidra route the program name is the only channel. The runtime directory (TMPDIR) does not enter. This supports Verdict 1.

C4. 2026-10-22T15:37:29Z. `grep -n` and `sed -n` on `dist/cli-runtime/BinaryTargetResolver-CVIJ_s1A.js`, lines 962-963 and 1018-1019, and binary bundle line 8579.
Excerpt: `const canonical = await realpath(candidate);` `const sourcePath = process.platform === "win32" ? candidate : canonical;`, then `targetPath: installation.platform === "win32" ? target.sourcePath ?? target.path : target.path`.
OBS: on Linux the snapshot suffix is taken from the realpath, not from the name the caller typed. On Windows it is taken from the caller's path.

C5. 2026-10-22T15:38:28Z. `node name_probe.mjs` (Node v24.21.0). It extracts `safeExtension` and `namedArtifactFormat` verbatim from the package as pure string functions, makes symlinks to `/usr/bin/jq` under the seat directory, and runs Node `realpathSync` on each.
Excerpt: `dirA/jq.dat  /usr/bin/jq  .bin` and `dirA/other-name.dat  /usr/bin/jq  .bin` (Linux suffix `.bin`, Windows-style suffix `.dat`). For regular-file names: `dirA/jq.js .js javascript`, `dirA/jq.map .map source-map`, `dirA/jq.plist .plist plist`, `dirA/jq.asar .asar asar`, `dirA/jq.hop .hop database/analysis-database (Hopper route)`, `dirA/jq.DAT .DAT`, `dirA/jq.tar.gz .gz`, `dirA/.jq .bin`, `dirA/jq.abcdefghijkl .abcdefghijkl`, `dirA/jq.abcdefghijklm .bin`, `dirB.dat/jq .bin`.
OBS: the symlink realpath and the outputs of the extracted functions.
INF: `analyze` on the symlink `jq.dat` returns the `/usr/bin/jq` id (`ev_14f9d92f…d328`), although the entry's rule predicts a different id (Verdict 2). A copy named `jq.js` gets `subject.format` `javascript`. That field is hashed (`dist/domain/evidence.js:156-163`), so every verb's id changes or the verb refuses (Verdict 3). `.dat` and `.DAT` give different ids because the suffix rule is case-sensitive, while format routing lowercases first.

C6. 2026-10-22T15:39:10Z. `sed -n 2855,2885p` on the binary bundle and `grep` on `bridge/hopper_bridge.py` and `dist/hopper/HopperTargetLease.js`.
Excerpt: `targetPath: target.path` (no `target-<sha>` snapshot; the lease file is only a socket); `if method == "current_document": return _document().getDocumentName()`.
OBS: under the Hopper provider, `document` comes from Hopper's document name for the real path, not from the snapshot rule.
UNK: whether Hopper's document name contains the file stem or the directory. Hopper is not installed (`command -v Hopper hopper` exit 1 at 15:40:00Z). If it contains the stem, the rest of the name enters the `analyze` id under Hopper.

C7. 2026-10-22T15:37:43Z. `grep` on `officialToolContracts-CCFF0an9.js` (lines 1273-1413) and `AnalysisSnapshotCache-BXS0wRd2.js:560`.
Excerpt: `document = z.string().optional()` on document-scoped tools; `list_documents` and `current_document` are in `MCP_TOOLS_WITHOUT_DEDICATED_CLI` (`dist/cliCommandNames.js`).
INF: a caller who passes `document` (MCP) puts `target-<sha12><suffix>` into the hashed `parameters` of any document-scoped verb, address verbs included. The entry already excludes MCP sessions, so this is not a defect.

C8. 2026-10-22T15:39:19Z. `grep -n -i 'realpath|symlink|hopper|win32|windows|javascript|plist|asar|provider'` on the entry, `corpus/lessons/round-27.md` and SKILL.md lines 912-936.
Excerpt: no match in the entry or the lesson. The SKILL section says "map each name's extension through the suffix rule" and "no hashed field carries the path, name or extension".
OBS: none of these conditions is named anywhere (Verdict 4).

## Impacted axes
Correctness of the decision rule outside the tested route (symlinks, routing extensions, Windows, Hopper); completeness of Limits; a minor provenance point (C2). The measured table, the 16 ids and the Ghidra mechanism are unaffected.

## Smallest safe correction (for the L1; this seat edits nothing)
- Entry Why and SKILL table: state that the suffix is the extension of the realpath-resolved target on Linux and of the caller's path on Windows, and that the rule is case-sensitive.
- Decision rule (entry and SKILL): scope it to the Ghidra provider and extensions that keep the ELF/PE route. Name the exceptions: `.js .mjs .cjs .map .plist .asar .hop` for any bytes; `.zip .ipa .apk .msix .appx .hap .hsp .app` and similar for ZIP bytes. These change the hashed `subject.format` or the route for every verb.
- Limits: add that symlinks, Windows, the Hopper provider (whose `document` comes from `getDocumentName` and may include the stem) and the extensions that change the route were neither run nor covered. A live check could run `analyze` on a symlink `x.dat` that points to `/usr/bin/jq` and on a copy named `jq.js`.

## Artifacts (/fast/scratch/hyaku/kaidoku-r27/seats/w2/CriticEntryMechanism/)
- diff_leaves.py 5bff1e8a1e998bd15202a3f23f4dc35eee97a5b520fd31fe1036269959b007da
- diff_leaves.out ff97326d4de6d2587250934c24a97079883d441aa052a151e887e6489d4c2556
- name_probe.mjs 3260e40e972872cc4a56bf6c0f281f904e08b66802fd28d4c4ee7d80eaeaf51c
- name_probe.out b69ac445f4f143e9bc699bfcea0d14e8ef2521c0a7a1942942575bcc990d057f
- code_refs.out c9a5c6167146a04e40c9f94da2918e642dfd3965b1d901234d44ae4e72825e96 (package file sha256 values and code excerpts)
- names/ (24 symlinks to /usr/bin/jq used by C5)
