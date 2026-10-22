# EntryTruth: falsify verdicts on the R26 native reader evidence-ID entry

Seat: KaidokuR26.EntryTruth (leaf; read-only on the lane: no lane edits, no git writes, no jj). Access date 2026-10-22; times UTC.
Judged bytes: corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md at HEAD 003de8cc (sha256 1ba5d5d9...), the L1 correction commit. Earlier committed bytes at ebe2cb4a and fe3eb4ed (sha256 b03fcdc4...) were also read. Commit 003de8cc rewrote the Coverage paragraph, Pin dependence, Use and Limits; false sentence F1 is identical in both versions. Working tree equals HEAD.
Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/EntryTruth/ (MANIFEST.sha256 sha256 a6ae3975...; 586 files).
Tools: none installed or upgraded. Used: npx rea-agents@6.5.0 and @6.7.0 from the npx cache (CLI, one call at a time), python3, readelf, objdump, curl (S080, plain HTTP).

## Bottom line
One sentence is false as written (F1). Nine are imprecise, incomplete, over-scoped or unverifiable (I1-I9), plus one pin-provenance sentence to reword (U1). The rest checks out against the committed envelopes, table, instrument, installed 6.5.0 and 6.7.0 sources, and my own runs.

## Sentence verdicts (T true, P partly true, F false, I inference, U unverifiable)
Header
- H1 T: source line. S079 and S080 rows dated 2026-10-22; both ids under ## Gate in lessons/round-26.md. c1-id-identity.py at ebe2cb4a, fe3eb4ed, 003de8cc: rc 0, rows_complete 8, entry_ok 1.
- H2 P: "24 CLI calls 12:11:50Z-12:15:45Z ... (version 6.5.0)". Times T (runs.tsv first utc_start, last utc_end); version T (package.json 6.5.0). The call record argv does not name the pin (U1).
- H3 T: "re-derives each verdict ... (offline)". The tool calls subprocess only for git (read-only, line 654) and to re-run itself for its selftest (lines 671, 752); no npx or REA.
- H4 T: live-recheck procedure. I made the copy (cmp exit 0; sha256 e815...7806) and ran the frozen argv with a private TMPDIR.
- H5 P: "the verbs need GHIDRA_INSTALL_DIR and the REA_* provider variables ... provider_unavailable, ok: false, no id". T for GHIDRA_INSTALL_DIR: env-free decompile on third/jq gave rc 1 (13:07:44Z), {"ok":false,"error":{"code":"provider_unavailable"...}, zero evidence_id strings; ReplayA F1 and ReplayB F5 agree. REA_* necessity untested (I6).

Coverage paragraph
- C1 T: README Known gaps evidence-ID bullet at a0639d8e (corpus/README.md line 203, under "## Known gaps" at line 199).
- C2 T: two-path controls at 6.4.0: r5-01 line 85 (analyze and inspect at another path, identical ids; Env line 7 pins 6.4.0); r9-02 lines 146-169 (analyze_function, same id for libc.so.6 and libsystem_c.so; pin 6.4.0 at lines 1 and 67).
- C3 T: two-path controls at 6.7.0 for four inspect-* verbs: arc3 r7 inspect_evm_interface (67-base1, 67-copyA), r10 inspect_rust_binary (arc3-r10 entry line 28), r11 inspect_artifact (copy), r12 inspect_go_binary (go-base1, go-copyA). Pair byte identity not re-run.
- C4 not contradicted (limited search): "No two-path control existed at 6.5.0 for any of the eight verbs." Searched every parseable .ufo/waves JSON with envelope shape and the 27 pre-entry knowledge files citing 6.5.0; no two-path pair found.
- C5 not contradicted (limited search): "five of them ... had none at any pin." Lane envelopes hold only binary_overview (64) and analyze_function (12) among the eight verbs' operations. inspect-binary-layout at 6.4.0 appears only as same-path /usr/bin/jq repeats (r4-13 line 155, r12-01 line 26, r12-02 lines 119, 262). No two-path ev_ record for decompile, xrefs, read-bytes or instructions.
- C6 T: the eight verbs are the PlannerWalk set (.ufo/waves/round-25/a3/w1/PlannerWalk.md lines 40-42); search-bytes, address-to-file-offset and inspect-native-instruction exist (dist/cliCommandNames.js lines 43, 44, 46).

Observation
- O1 T: /usr/bin/jq 30,800 B, sha256 e815...7806; the alt copy is byte-identical (cmp exit 0).
- O2 T: one FDE starts at pc 0x3fa0 (readelf --debug-dump=frames, count 1); two "call 3fa0 <process>" sites (objdump -d, count 2); image_base "0x100000" (analyze-base); FUN_00103fa0 (decompile-base); no symtab (readelf -S, count 0); the name process comes from BuildID cc56d2fd... debug data in ~/.cache/debuginfod_client.
- O3 T: 24 calls, base/repeat/copy per verb in runs.tsv, exit 0; 24 of 24 ok true; subject sha256 equals the carrier for all 24 (check_entry.py section 1, rc 0, 13:08:53Z).
- O4 T: table verdicts (seven content-keyed, inspect-binary-layout path-sensitive); all eight id cells equal the envelope ids; every truncated id in the entry matches table.tsv (section 2).
- O5 T: analyze and inspect share ev_14f9d92f...b3d328.

Envelope paragraph
- E1 T: base and repeat differ only in /meta/duration (8 of 8).
- E2 T: base and copy differ in /data/subject/local_path; for inspect-binary-layout also /data/parameters/path, /data/normalized_result/artifact/path, /data/locations/0/path (and /data/evidence_id, left implied).
- E3 T: file sha256 differs base vs repeat for all 8 verbs; ids equal.
- E4 T: the two replays together cover all eight verbs (ReplayA: analyze, decompile, xrefs; ReplayB: inspect, read-bytes, function, instructions, inspect-binary-layout); each base id matches the table.
- E5 T: content-keyed verbs keep their id at a third directory. My third/jq runs (13:03:02-13:03:36Z, rc 0) match the table for seven verbs; ReplayA alt2 and ReplayB alt3 agree.
- E6 T: inspect-binary-layout gives a third distinct id at a third directory: mine ev_03afa456... (not base, not copy); ReplayB alt3 ev_8de0a0dc....
- E7 P: "kept the id after only the file's modification time changed". T for inspect-binary-layout only (ReplayB F3; my touch test 13:04:44Z, same id). Not tested for the other seven (I5).
- E8 T: analyze and inspect both call binary_overview with {} (dist/cli-runtime/cli.js lines 10347, 10355); .meta.command (analyze, inspect) tells them apart.

Mechanism
- M1 P: "evidence.js:182 mints ev_ plus the SHA-256 of a canonical-JSON semantic projection (:156-180)". Lines 182 and 156-180 correct; second mint at :250-254 uncited (I3).
- M2 T: projection keeps subject digest, format, architecture; drops local_path and name; keeps parameters, raw and normalized results, limitations, locations, profile, provider (evidence.js 156-180).
- M3 I: "path-sensitive exactly when it writes the path into one of those kept fields". Inferred rule, consistent with the eight verdicts, structural diffs and renamed-copy replay; only-if direction untested; not falsified.
- M4 P: inspect-binary-layout writes the run path into the three fields (values verified); citation BinaryLayoutService.js:61-67 incomplete (I4).
- M5 T: the other seven put no run path in kept fields (structural diffs). Providers: analyze, inspect rea-workflow; decompile, xrefs, read-bytes, function, instructions ghidra. Function carries Ghidra type names beginning "/" (for example "/undefined8"), not file paths.
- M6 T: Ghidra copy named target-<sha12><ext> (GhidraTargetSnapshot.js lines 13-14); extension kept (jq has none).
- M7 U: "A blind prediction ... matched all eight verdicts (PredictionCritic.md, predictions at 12:16:14Z)". The 8 of 8 match is T (against the table); "before the run outputs were read" rests on the seat's statement (I8).
- M8 I: "No cache served the repeats." Source-based; no cache-hit test (I9). M9 I: equal ids across runs are provider determinism; consistent with M8.
- M10 T: recompute-ids.txt "24 match of 24 total"; my independent 6.5.0 recompute gives 24 of 24 (section 1).
- M11 T: changing subject.local_path keeps the recomputed id; changing parameters.path or normalized_result.artifact.path changes it (my mutation test, section 4).

Pin dependence
- P1 T: table ids are 6.5.0 values.
- P2 P: "two causes". relationship_coverage T (6.5.0 evidence.js 175-177 conditional; 6.7.0 line 178 unconditional). "function result carries changed analysis_profile.parameters names" is wrong wording (I1).
- P3 T: live pairs: inspect-binary-layout 6.7.0 ev_d1256a96... (my run 13:04:45Z, rc 0); function 6.7.0 ev_177586c6... (13:04:51Z, rc 0).
- P4 F: "The lane's stored 6.7.0 envelopes (arc3 rounds 7, 10, 11, 12) recompute exactly under the 6.7.0 rule and never under the 6.5.0 rule." See F1.
- P5 P: "compare ids only within one pin and one provider build ... changing only that string ... changes the recomputed id for decompile, analyze and read-bytes". Source lines (GhidraInstallationPolicy.js 39, 44, 50) and the three verbs are right; list understated (I2).
- P6 T: the two 6.7.0 calls are single base runs testing no relation; "same eight relations at 6.7.0" labelled inference.

Use and Limits
- U-a P: "for inspect-binary-layout ... the parameters other than parameters.path" (I7). Other Use bullets T (equal analyze/inspect ids are not evidence the verbs agree; equal ids do not authenticate subject path or module name, r9-02 lines 146-169).
- L1 T: one carrier, one pin, one Ghidra build 12.1.4 (provider.version in decompile-base), one address, default parameters, three runs per verb.
- L2 T: copy kept the name jq. Renamed replay (ReplayRenamedCopy.md present in w2): analyze, decompile, function keep table ids (my runs rc 0, 13:10:03-13:10:15Z); inspect-binary-layout new id (mine ev_48a4fb69...; ReplayRenamedCopy ev_6a4412e2...). Other four verbs not run.
- L3 T: r9-02 renamed copy keeps the function id (libc.so.6 to libsystem_c.so). L4 T: r17 gave analyze two ids for one file across two passes (carrier /usr/bin/aether, r17 line 71; string_count 29118 to 29117, lines 116-122); same path inferred from the carrier table.
- L5 T: inspect-binary-layout at 6.4.0 gives ev_294a449c... on /usr/bin/jq (r12-01 line 26): 6.4.0 and 6.5.0 agree for that verb.
- L6 T: disclaimers make no claim. L7 P: "the envelopes do not record the package version" T (no "6.5.0" substring in any of 24 envelopes); "the pin rests on the call records" see U1.

## False or unsupported sentences, with counterexamples
- F1 (FALSE, Pin dependence): "The lane's stored 6.7.0 envelopes (arc3 rounds 7, 10, 11, 12) recompute exactly under the 6.7.0 rule and never under the 6.5.0 rule." Counterexample: all 12 round-12 analyze_function envelopes match the 6.5.0 rule too, each with non-null relationship_coverage, e.g. .ufo/waves/arc3-loop1-round12/claims/c1/EX-7/evidence/function-base-1.json and claims/c1/CR-2/evidence/base.json (full list: check_entry.py section 6, rc 0, 13:08:53Z). Round 7: 20 envelopes match 6.7.0, none matches 6.5.0; the 19 matching 6.5.0 are 6.4.0 files. Rounds 10 (32 of 32) and 11 (38 of 38) hold. Repair: limit "never" to null-coverage envelopes, or say both rules agree when coverage is non-null.
- I1 (wording, P2): "changed analysis_profile.parameters names". Key sets are identical (25 keys each); values change: function_boundary_observations ghidra-function-boundary-limitations-v3 to -v4; instruction_references exact-address-incoming-v1 to exact-address-incoming-without-synthetic-entry-v2; analysis_profile.digest also differs. Say "values".
- I2 (understated, P5): changing "12.1.4" to "12.1.3" in a committed envelope changes the recomputed id for all seven Ghidra or rea-workflow verbs (analyze, inspect, decompile, xrefs, read-bytes, function, instructions), not three; inspect-binary-layout unchanged (pwntools version string). Recompute equals stored: False for seven, True for inspect-binary-layout (my _eval run, 13:10:35Z).
- I3 (incomplete citation, M1): the mint also sits at evidence.js lines 250-254 ("const digest = yield* canonicalJsonDigestSteps(semanticProjection(normalized));", createImmutableEvidenceSteps). Same projection; cite both.
- I4 (incomplete citation, M4): normalized_result.artifact.path is set at dist/native/pwntools/PwntoolsLayoutProvider.js lines 17-21 ("artifact: { path: input.path, ..."), carried at BinaryLayoutService.js line 62 and checked at line 51. Cited 61-67 covers parameters (61) and the location (67) only.
- I5 (scope, E7): the mtime-only test covers inspect-binary-layout only; name the verb.
- I6 (overstated, H5): "the verbs need GHIDRA_INSTALL_DIR and the REA_* provider variables". Only GHIDRA_INSTALL_DIR is shown necessary; REA_* necessity untested (ReplayB lists it as unknown).
- I7 (minor, Use): inspect-binary-layout parameters are only {"path"} (python: ['path']), so "parameters other than parameters.path" is empty; the advice reduces to the subject digest.
- I8 (unverifiable, M7): "before the run outputs were read" rests only on the seat's statement. Predictions sealed 12:16:14Z, 29 s after the last run ended (12:15:45Z). The 8 of 8 match is verified.
- I9 (inference stated as fact, M8): "No cache served the repeats." Source reading only; CacheConfound.md labels it "Inference (high)"; no cache-hit test run.
- U1 (source, H2 and L7): "the pin rests on the call records". runs.tsv argv (e.g. "analyze /usr/bin/jq --format json --full-output") does not name rea-agents@6.5.0; the spec is in claims.json invocation text and seat commands; npx cache root ad9a3... is 6.5.0. Reword.

## Process and residual gaps
- runs.tsv shows the 24 calls overlapped across four seats (xrefs base 12:11:50-12:11:57; analyze base 12:11:51-12:11:58), so not one at a time; all exited 0 and ids reproduced.
- Entry changed in 003de8cc after my first read (13:00:02Z; b03fcdc4 to 1ba5d5d9); judged the new bytes; F1 applies to both.
- C4 and C5 rest on grep-level searches. Pair identity for the four 6.7.0 controls rests on file names. Cache claims are source-based. IdentityClaimsMap.md and RecomputeIds.md checked by grep plus my runs; EntryOverreach.md checked for existence and cited lines.
- Not tested: other 12.1.x builds (labelled inference), names or extensions beyond jq-renamed.bin, MCP, error envelopes.

## Artifacts (sha256)
- My REA runs (npx; rc; UTC): third/jq eight verbs rc 0 13:03:02-13:03:37Z; touched-mtime inspect-binary-layout rc 0 13:04:44Z; 6.7.0 inspect-binary-layout and function rc 0 13:04:45Z, 13:04:51Z; renamed copy four verbs rc 0 13:10:03-13:10:16Z; env-free decompile rc 1 13:07:44Z.
- check_entry.py 6cb263065cd89571599b8ba6c8c8b614b11591e40aef5858d19f35723505c8d4 (rc 0, 13:08:53Z); check_entry.out 327cd4a1e3079de136e955d9189f9e75f8d526fe8b416bc31d285190215d911d; MANIFEST.sha256 a6ae397524b3c338bfd7b259b19cf398daef2ee7472fd3aa5d5a80c7648bde7e (586 files).
- Entry 1ba5d5d909eecb2db638677388f9bcc0429b5263469905a936fc3c2a6185a941 (003de8cc); b03fcdc450869e65337a81b009ca0f67008c4864d32630dfd858da5e99143a20 (ebe2cb4a, fe3eb4ed).
- Installed 6.5.0 evidence.js f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff and canonicalDigest.js f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9 (both match S079); 6.7.0 evidence.js a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb (matches PinSourceDiff).
- S080 registry record 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde (matches lesson Gate; integrity and shasum match a live fetch 13:07:23Z).
