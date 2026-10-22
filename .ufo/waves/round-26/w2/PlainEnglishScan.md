# Round 26 wave 2 — PlainEnglishScan (run-together tokens and private jargon)

Scope: added lines of `a0639d8e61e486e2a716ff94cddd89a73200a02c..c327772653badd3b19b3954e1f8713973aa3f93e`, 4,252 lines in 47 files (prose 320, tool code 1,939, machine output 1,993). Line numbers are new-file numbers at `c327772653badd3b19b3954e1f8713973aa3f93e`. Paths are relative to the lane root. The lane was read only.

Verdict: hits exist. Section A lists nine lane-authored run-together or glued-label hits (R1–R9). Section C lists 23 private-jargon groups (J1–J23) with no definition in the committed lane. Section B lists the candidates I checked and exempted; the full row-level inventory is in the scratch TSV named in section E.

## A. Run-together tokens (hits)

- R1 [M] `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:92` — `arc3`, a word glued to a digit, used as a bare series label. The series name appears only in file names (`corpus/README.md:38`); no committed prose defines it. Fix: gloss it, or write "arc 3" with its meaning.
- R2 [L] `SKILL.md:855` — `round25-custody-ruler`, a registry key. The same key appears at `SKILL.md:807` and `corpus/lessons/round-25-verifier-spotcheck.md:184`. Keep it if the key must match; this is a registry decision for Main.
- R3 [L] `SKILL.md:872` — `kaidoku25-prerequisite`, a path segment in the fleet repository (`.ufo/waves/hyaku/...`). Keep it exact when quoting the path.
- R4 [L] `.ufo/waves/round-26/claims.json:50` and `:67`; `corpus/lessons/round-26.md:15` — `C1Cherrypick`, a seat-report file name. Line 67 uses it as `C1Cherrypick` E4. Gloss it once at first use; `claims.json:50` has no gloss.
- R5 [L] `corpus/lessons/round-26.md:17` — `C2BeforeManual`, a seat label. `corpus/lessons/round-26.md:43` — `C1Mutation` and `C2Mutation`, report file names.
- R6 [L] `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:5` and `:42` — `ReplayA`, `ReplayB`; `:23` — `AddressCheck`; `:47` — `IdentityClaimsMap`; `:65` — `PredictionCritic`; `:71` — `CacheConfound`; `:81` — `RecomputeIds`; `:86` — `PinSourceDiff`. Also `corpus/lessons/round-26.md:37` — `PinSourceDiff`. All are seat-report file names.
- R7 [L] `corpus/QUALITY.md:45` — `CapinfosFacts` (seat-report file name). `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:205` — `EntryNumbers` (same kind).
- R8 [L] `corpus/evidence/round-26/c1/runs.tsv` — seat labels in the `seat` column: `RunAnalyzeInspect` (lines 2–7), `RunDecompileFunction` (8–13), `RunXrefsInstructions` (14–19), `RunReadBytesLayout` (20–25). The last label names only read-bytes, but rows 23–25 are inspect-binary-layout.
- R9 [L] `tools/round-26/c2-calibration.py:611` — `KaidokuR26.MutR25Calib`, a seat id inside a comment.

R4–R7 name report files that exist on disk, so renaming them breaks paths. R8 and R9 are seat labels (a table column and a comment). Each of R4–R9 needs one plain gloss at first use; R1 needs a gloss or a plain rewrite.

## B. Candidates checked and exempted (not run-together)

- Placeholders: `tools/round-26/c2-calibration.py:469`, `:470`, `:484`, `:549` — `HASH1` (fixture revision).
- Address literal: knowledge `:21` — `0x3fa0`.
- Base64 integrity strings: `corpus/SOURCES.md:86`; `corpus/lessons/round-26.md:28` — `sha512-C6BG…`, `…1RqewCQla…`.
- JSON key paths: `evidence.subject` (lesson `:27`); `parameters.path` (knowledge `:59`, `:80`); `dist.integrity`, `dist.shasum` (SOURCES `:86`, lesson `:28`–`:29`); `predicate.buildDefinition` (lesson `:31`); `.data.subject` (`claims.json:14`).
- Upstream identifiers quoted from REA, npm or Ghidra sources: `canonicalDigest`, `analysisView`, `binaryLayoutView`, `DirectAnalysis`, `BinaryLayoutService` (SOURCES `:85`–`:86`; knowledge `:60`, `:72`, `:73`); `computeEvidenceId`, `semanticProjection`, `digestCanonicalValue`, `resolvedDependencies`, `gitCommit` (lesson `:27`–`:31`); `PcapProvider.js` (QUALITY `:45`); `agentId` (lesson `:44`).
- Technical names with digits: `sha256`, `sha512`, `python3`, `4byte`, `x86-64`, `lib64`, `rv2token`, `kdxtoken`, `stewardtoken`. ID-style labels: `R26-C1`, `S079`, `M26-1`, `K1`, `E4`, `C9`, `v42`, `W04`.
- Dictionary check (pyspellchecker 0.9.1): 86 prose rows hit 41 distinct words. Each is technical (`argv`, `json`, `ghidra`, `packument`, `tarball`, `shasum`, `decompile`, `xrefs`, `selftest`), a proper name (`kaidoku`, `hyaku`), a base64 fragment, or standard English missing from the list (`analyse`, `behaviour`, `diffing`, `unrepaired`, `undispatched`). No glued English word.
- Tool code (comments and strings via tokenize): 14 hit rows, all R9 or the `HASH1` placeholders.
- Machine output: 2,237 hit rows. 2,178 come from the 24 REA envelopes (Ghidra variables such as `auVar13`, Java class names such as `HighFunction`, base64 section names, hex addresses); these are sha256-pinned tool output and must not be edited. 24 come from `corpus/evidence/round-26/after/c1-at-ebe2cb4a.json` (`data.subject`). 24 are R8. 6 are colon labels (`analyze:table`, `before/c1-selftest.txt`). 5 are domain names (`before/census-start.txt:1`–`:5`).

## C. Unexplained private jargon

Test: a term is unexplained when neither its added passage nor a committed lane file at `c327772653` defines it. I grepped the committed corpus, tools, root docs and round-26 wave files (467 files, extracted from REV) for definitions of seat, wave, L1, Main, receipt, closure, arc3, luna and learning claim; none was found. `corpus/README.md:8`, `MINT.md:4` and `MINT.md:43` cite LEARNING.md, CORPUS.md and PROTOCOL.md; an ls-tree check of all 19,707 entries at REV found none of those files (no matches). So the lane vocabulary is defined only in fleet documents the lane does not contain.

- J1 [H] `L1` (lane lead role): `.ufo/waves/round-26/claims.json:4`, `:70`; `corpus/lessons/round-26.md:3`, `:43`; `tools/round-26/c1-id-identity.py:6`.
- J2 [H] `seat` (one counted reviewer task with a report file): first unglossed uses `claims.json:33` ("<seat scratch>") and `:50`. About 24 uses across added prose and code. The only gloss is operational, at `corpus/lessons/round-26.md:44` ("Seats are counted from the task result's agent ids…").
- J3 [H] `wave`, `wave 1`, `wave 2`, `falsify wave`: `claims.json:6` ("written in wave 1"); `corpus/lessons/round-26.md:44`; `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:177` ("round 26 wave 1").
- J4 [M] `Main` (parent integrator, quoted from `LOG.md`): `corpus/lessons/round-26.md:44`.
- J5 [L] `lane-round base`: `corpus/lessons/round-26.md:3`, `:45`. `claims.json` calls the same commit "base".
- J6 [M] `closure`, `outside closures`: `SCORECARD.md:25`; `corpus/lessons/round-26.md:45` ("outside closure's conformance step").
- J7 [M] `rejected-honest-stop`, `operator-steered`: `SCORECARD.md:25`.
- J8 [L] `contradiction census`, `r3 semantic contradiction removal`: `SCORECARD.md:24`. `preselected reconciliation obligations`, `per-client REA surface`, `live receipts`, `failure-selected completeness`: `SCORECARD.md:25`.
- J9 [M] `round-25 first-row false accept`: `.ufo/waves/round-26/claims.json:53`.
- J10 [M] Item labels `E1, E2, E3, E5` and `E4`, and `C9 outside-verifier wording`: `claims.json:50`, `:67`. They name items in another file, which the claim does not list.
- J11 [M] `I4`, `M8`, `M9`, `M10`, `M26`: `corpus/lessons/round-26.md:43`. `M25-10`: `corpus/lessons/round-26.md:44`.
- J12 [H] Process jargon, one dense passage: `attack seat(s)`, `25% attack floor`, `2 h scope freeze`, `dispatch artifact`, `spawn`/`resume`, `swarm-registry.json`, `validated-but-undispatched wave`, `spec path` — `corpus/lessons/round-26.md:44`.
- J13 [M] `epoch line`: `corpus/lessons/round-26.md:45`. Elsewhere "epoch" means retention scope (`SKILL.md:407`).
- J14 [M] `learning claim`: `claims.json:20`; `corpus/lessons/round-26.md:9`.
- J15 [L] `hyaku` (fleet name): `claims.json:9`, `:22`; knowledge `:19`; `corpus/lessons/round-26.md:3`.
- J16 [M] `FLAGGED`, `INSTRUMENT_ABSENT`, `INSTRUMENT_REVISED`, `round-24 freeze gate`: `claims.json:6`; `SKILL.md:863`–`:864`; `corpus/lessons/round-26.md:45`. The legend is only implicit in `corpus/QUALITY.md:43` (row 33).
- J17 [L] `sharpens 34`, `flip clause`, `fired flip`, `admitting row`: `corpus/QUALITY.md:45`. The table header defines only "supersedes".
- J18 [L] `PROVINCE core`: `claims.json:20`. The `## Core` heading is `PROVINCE.md:38`, which the claim does not point to.
- J19 [L] `Coverage-map ground`, `two-path controls`, `family-wide statement`: knowledge `:9`, `:10`–`:12`.
- J20 [L] `captured-by` (table header): `corpus/lessons/round-26.md:41`.
- J21 [L] `family` (source family): `corpus/SOURCES.md:149`; `corpus/lessons/round-26.md:35`–`:37`.
- J22 [L] `W04` (check label, no legend): `corpus/evidence/round-26/before/census-start.txt:1`–`:5`.
- J23 [L] `wave-26 seat envelope roots`: `tools/round-26/recompute-ids.py:16`.

Reviewed and not flagged, because a pointer or a lane document defines them: `207/153` and `v42` (`SHONEN.md:12` points to `PROVINCE.md:8`–`:12` and `:24`); `command A`, `command B` (SCORECARD measurement recipes A and B, `SCORECARD.md:86`–`:143`); `Queue-drain craft` (`SKILL.md:81`); `owned axes` (SCORECARD); `routed defect` (`corpus/lessons/round-25-verifier-spotcheck.md:181`); `held narrowly` (`SKILL.md:31`–`:32`); `content-keyed`, `path-sensitive` (QUALITY row 15); `Gate` (QUALITY rows 16–17); `luna-round-N` (SCORECARD section headings); `custody`, `ruler` (`SKILL.md:780`–`:806`, the section the note supersedes); `carrier` (glossed by example at knowledge `:18`); `decoy`, `red`, `green` (`claims.json:63`); `REA` (`MINT.md:9`–`:11`); `envelope` (standard REA output term); `PROVINCE`, `SHONEN`, `SCORECARD`, `LOG`, `QUALITY`, `SOURCES`, `lane` (`README.md:3`–`:19`).

## D. Residual risk and verification gaps

- The jargon call is a judgement. J1–J23 are unexplained as written. A reader holding the fleet protocol could resolve them, and that protocol is not in the lane.
- Labels: sections A, B and E are observations (scanner and grep output). The verdicts in section C and the H/M/L tags are inferences.
- Working tree was dirty at about 13:16Z (`git status --porcelain`: uncommitted edits to SKILL.md, corpus/SOURCES.md, the round-26 knowledge entry and corpus/lessons/round-26.md, made by others). Not judged. Findings concern committed bytes at c327772653 only; some hits may already be changed in the working tree.
- The dictionary is a proxy. A glued pair that forms a real word (for example "inline") would pass. Three-letter glue was not checked.
- The 2,178 envelope rows were classified by rule, not read one by one. Every row is in the TSV.
- No REA calls, no tests, no lane writes, and no external sources opened. Commit subjects, which are not diff lines, were not scanned.

## E. Artifacts (sha256; scratch `/fast/scratch/hyaku/kaidoku-r26/seats/w2/PlainEnglishScan/`)

- `scan.py` e6627868e2819a7846ca9e3d6fe8d8189012a637cdb79ff7147397f44b753d65 — run as `python3 scan.py <dir>/out`; exit 0; 2026-10-22T13:13:02Z (produced the `out/` files below).
- `out/glue_candidates.tsv` 8bf42de21c71d2a7d653c07a1541f8160f6b9ffb348810d4d87e7fd6cb41b807 — 18,493 rows: path, line, class, kind, token, status, reason.
- `out/jargon_terms.tsv` 55f9e3fe0ecd8519ae59f377110b6a4de2db4083b23f14da82f209074c36668a.
- `out/added_lines.jsonl` 7fc72b58932dedb35934e31ade38d9cf794bccd0d040aaafde2231a4ad652624 — 4,252 added lines.
- `out/summary.txt` 9570e326c25540280e1d61f1dd6e6bd9df2af411cd4342eaabf76c39a9eeb4a0.
- `diff_full.txt` 2e25d95edab73a9b6224cc3e208a9807d35f6acf8893ae6d1b264d15d6dfc980; `diffstat.txt` 2b0d04a67e584a2f43eac833517f254f76b37cf8e6e01beedbb26bc8c3c014d2; `tool_text_items.tsv` 9c8d702aa7ff3b364050ee3657ff6e13ce2df852d3791b7f2a3d77e966fdb1e7.
- Installed: pyspellchecker 0.9.1 with `uv pip install` into a `uv venv` (uv 0.13.0 was already present). Reason: an English word list for the glue check. No system package changed.
- Grep-check copies of committed files at REV: `tree/` (467 files from `git archive`; manifest sha256 d15bb86d5a1d33c55539ff49511811914798eae83126c473c916026f77c2c3e4) and `rev/` (13 files; manifest sha256 65e46d8bf96d5e4719d713122f6745500bc8694c2d5e530821c12f938274f415). Manifest = sorted lines of `sha256  path`, then sha256 of that text.
