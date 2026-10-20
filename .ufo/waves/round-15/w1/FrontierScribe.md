# Round 15 w1 — FrontierScribe: source-use / quote / delta / Mistakes checklist draft

Seat: `KaidokuR15.FrontierScribe` (leaf; no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: C2 routed duties (round-14 outside review) and the frontier source-use checklist for L1. Access date: 2026-10-20.

## Limits and custody

- Read-only. No gate, selftest, census, build, test, lint, REA call, Ghidra run, or target execution was performed. No installs or updates.
- Shell use was limited to `sha256sum`, `unzip -p` to stdout (no extraction to disk), and line-range views. No network fetch was made; S004 (upstream commit) was **not reopened this round**.
- No corpus, SKILL, QUALITY, SOURCES, LOG, SCORECARD, or MANIFEST write. Nothing in this report is a count; row, tier, status, and mapped-file counts belong to L1.
- Source opening for every Gate quote and every cited source must occur in the round that admits it. Digests recorded in round 14 are inputs to re-check, not evidence for this round.

## A. Observed this round (exact anchors)

| # | Observation | Anchor | Status |
|---|---|---|---|
| O1 | S001 SKILL.md SHA-256 `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0` | `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | matches `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` table |
| O2 | S003 Base-src.zip SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | matches `SOURCES.md` S003 and knowledge entry |
| O3 | S007 ChangeHistory.md SHA-256 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` | matches knowledge entry |
| O4 | `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` | S003 `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | observed |
| O5 | Out-of-range branch: `Msg.error(... "Untested Go version [%s]")`, no throw and no return; snapshot `get` follows at :174 | S003 `GoRttiMapper.java:170-176` | observed |
| O6 | `super(program, null)` in the mapper constructor | S003 `GoRttiMapper.java:331` | observed |
| O7 | `initStructMappings`: `registerStructures` in `try`; `IOException` handler throws `BootstrapInfoException("Missing Go bootstrap type info…")` only if `apiSnapshot.isInvalid()`; otherwise a different `IOException("Invalid Go bootstrap struct mapping info…")` | S003 `GoRttiMapper.java:351-366` | observed |
| O8 | `getType(String, Class)` override delegates to `goTypes.findDataType(name)` | S003 `GoRttiMapper.java:379-382` | observed |
| O9 | `DataTypeMapper.registerStructure` calls `getType(structNames, Structure.class)`; `getType(List,…)` calls `getType(dtName, clazz)` on `this` (virtual dispatch) | S003 `structmapping/DataTypeMapper.java:172-176`, `:310-313` | observed |
| O10 | Non-primitive type lookup reads `apiSnapshot.getTypeDef(typeName)` | S003 `rtti/GoTypeManager.java:443-451` | observed |
| O11 | `getApiSnapshotJsonFile` requests patch 0 of the same major.minor; returns null if the base file is absent; `get` returns `EMPTY` on that path | S003 `rtti/GoApiSnapshot.java:115`, `:118-126` | observed |
| O12 | `isInvalid()` is `arches.isEmpty()` | S003 `rtti/GoApiSnapshot.java:503-505` | observed |
| O13 | S007 line 585 contains the round-14 quote verbatim: "Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files." Enclosing heading `# Ghidra 12.0 Change History (December 2025)` at :564, `### Improvements` at :582 | S007 `docs/ChangeHistory.md:564, 582, 585` | observed |
| O14 | Installed snapshot listing under `Ghidra/Features/Base/data/typeinfo/golang/`: `go1.15.0.json` … `go1.25.0.json`, `golang_1.15…1.23_anybit_any.gdt`, `patchverdiffs/` directory. No `go1.26*` entry. (Count is L1's.) | installed Base data directory | observed (listing only) |

### Correction-relevant contradiction (duty 1)

`.ufo/waves/round-14/w1/ReviewGoInference.md:56-58` (Finding 2) states that `registerStructures` "does not consult the snapshot," so snapshot absence "changes the log text, not the analyzer outcome."

Source chain observed this round:

`registerStructures` (`GoRttiMapper.java:353`) → `DataTypeMapper.registerStructure` (`DataTypeMapper.java:176`) → `getType(List,…)` (`:313`) → virtual `GoRttiMapper.getType` override (`GoRttiMapper.java:380-382`) → `GoTypeManager` non-primitive branch (`GoTypeManager.java:449`) → `apiSnapshot.getTypeDef`.

Consequences:

- **Observed:** the claim "registerStructures does not consult the snapshot" is contradicted at the cited anchors. Snapshot absence is an input to struct-type resolution, not only to message wording.
- **[INFERENCE]:** an `EMPTY` snapshot yields no type definition for non-primitive names, so struct resolution can fail and reach the `IOException` branch. `GoApiSnapshot.EMPTY`/`getTypeDef` was not opened this round.
- **Not re-opened this round:** the claim that both `IOException` and `BootstrapInfoException` branches return null (`GoRttiMapper.java:102-129`, cited by the round-14 artifact). Carry it as unverified here.
- **Unchanged and still correct:** the knowledge entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (lines 39-50) already states that the failure is conditional and that the cause of the historical run is UNKNOWN. The advisory artifact's wrong mechanism must not be propagated.

### QUALITY #16 wording (duty 2)

`corpus/QUALITY.md` row 16 says the local instrument "does not grade" markup-spanning quotations, code members, commit objects, JSON, and command output.

Observed in `.ufo/waves/round-14/tools/quote-fidelity.py`:

- `grade_quote` applies `quote["quote"] not in text` to the raw captured bytes with no normalization (`:250-257`; docstring `:34-36`).
- A rendered-text quote that spans markup is not a substring of raw bytes. It returns `quote_not_contiguous` (exit 1, FAILED); `exit_code` maps only `invalid_manifest`, `source_tampered`, and `snapshot_tampered` to exit 2 (`:97-100`).
- A raw-HTML quote that includes its markup can match and return exit 0.

So the instrument **does** produce a machine verdict on these inputs. "Does not grade them" is an overclaim. The accurate statement is that the verdict on those input classes is a raw-substring result, and the input class must not be submitted as machine-gradeable evidence. The gate's exit map is unchanged.

## B. Frontier source-use / quote / delta checklist (draft for L1; not written to corpus)

Each line is a yes/no gate for the round's Gate table. "L1 check" names a proposed command. L1 runs it once after all seats finish; this seat did not run it.

### Source use
1. **Open every cited source this round.** S001, S003, S007 at minimum. Record `sha256sum` at open time and compare with the registry digests (O1-O3). A mismatch stops the admission. *L1 check:* `sha256sum` of the three paths.
2. **Reopen the upstream commit only if the Gate cites its diff.** S004 was not reopened here. If cited, fetch the commit patch this round, record its SHA-256 (round-14 value `f44945bc879d46f2e16624f7823246416d625229e57930db13a040862c170538`, to be compared, not assumed), and quote only the lines read. Otherwise state "not reopened this round." *L1 check:* `sha256sum` of the fetched patch.
3. **Upstream is not installed behavior.** The GP-6528 master commit must not be cited as present in the installed 12.1.4 release. *L1 check:* grep the installed Base source for the cited symbol at the cited anchor.
4. **Caller-chain claims name every hop.** Any statement that a method does or does not consult a source must cite each virtual-dispatch hop, as in O7-O10. A single-class read is insufficient. *L1 check:* re-open the chain at the anchors in section A.
5. **Installed listing claims state the directory and the command.** A "missing" or "present" file claim cites the directory listing and the exact path. Counts are L1's. *L1 check:* `ls` of the cited data directory.
6. **Registry deltas change only `used-by`.** No new SOURCES row without a fresh open and tier decision. *L1 check:* `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (expect `ok`, exit 0, per round-14 precedent) and a diff of `corpus/SOURCES.md` against the round-14 commit showing only permitted cells.

### Quote
7. **Contiguous, ≤25 words, located.** Each quote is one contiguous substring of the source, names its section (heading or line), and was re-opened this round (QUALITY #1, #16). *L1 check:* `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-14/fixtures/expected.json` as regression only; no new manifest without a reviewed reason.
8. **Manual-only classes are not machine-graded.** Code members, commit objects, JSON, command output, and markup-spanning text get a manual source check. Their gate output is not cited as evidence. (Proposed QUALITY row 17; see C.)
9. **Section locator from the same rendering.** Do not reuse a line number from a different rendering or a reader view. Raw-HTML headings use the literal line or visible label (gate docstring `:24-29`). *L1 check:* confirm the quote's section by re-opening the raw bytes.

### Delta
10. **Before and after for every changed claim.** State the prior measured value, the command and revision, and the new value. Do not restate a prior count as current. Counts are L1's to measure and state.
11. **Historical causes stay UNKNOWN unless retained.** The round-4 op run's analyzer log was not retained (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:72-73`, cited by the round-14 entry). No new historical-cause sentence is admitted without a retained log or replay.
12. **Advisory artifacts are not corrected in place.** A wrong mechanism in a filed review (`ReviewGoInference.md:56-58`) is superseded by an appended correction in the lesson or LOG that names the artifact, its line range, and the corrected anchors. The artifact bytes stay unchanged.

### Mistakes (deduplicated from round-12 to round-14 tables; applies to this round)
13. **Quote splice / attribution** (r13 #3; r14 row 1). Caught by non-author re-open, not by machine. Check item 7 is the control.
14. **Reference drift** (r13 #4; r14 row 2). Re-open the exact section for each quote. Item 9 is the control.
15. **Causal overreach** (r14 row 3; r15 new instance: `ReviewGoInference.md` Finding 2). Caught only by re-reading the source chain. Item 4 is the control.
16. **Instrument overreach / wording overclaim** (r14 row 4; r15 new instance: QUALITY #16 "does not grade"). Check the claim against the code's actual behavior before writing it. Item 8 and the proposed row 17 are the control.
17. **Edit-anchor provenance** (r14 row 5). Re-read the target range and use its returned tag before any hashline edit. Applies to L1's QUALITY and SKILL edits.
18. **Line-shift into pinned citations** (r12 #9). Append-only edits; no line-number citation into a file that is still growing. Use keys plus section names.
19. **Measurement on the wrong tree** (r12 #10). Every census or measure run in a worktree passes an explicit `--root`. Applies to L1's verification.
20. **Digest without serializer or source** (r12 #7). Record the file being hashed and the exact command, not only the digest.
21. **Stale status clause in a cited range** (r12 #5). Re-read the cited lines after any append.

## C. Candidate text for L1 integration (not written)

### C1 — QUALITY row 17 (supersedes 16; row 16 bytes unchanged)

Candidate row to append at the end of the admission table:

| 17 | Manual-only inputs are not submitted to the raw `quote-fidelity` gate as machine evidence. Rendered-page text, quotations spanning markup, code members, commit objects, JSON, and command output require manual source check under #1. The gate applies raw substring matching with no normalization (`quote-fidelity.py` `grade_quote`); exit 1 on such an input is a raw-substring non-match, not evidence of misquotation or absence, and exit 0 on a markup-containing raw quote is not evidence of rendered wording. The gate's exit map is unchanged; this row narrows admissible use only. | `corpus/lessons/round-14-verifier-spotcheck.md` routed item 2; `.ufo/waves/round-14/tools/quote-fidelity.py:97-100, 250-257` | supersedes 16 (row 16 is not edited) |

Notes for L1: the QUALITY header says a criterion is replaced by a new row naming the row it supersedes, never rewritten. Append row 17; do not edit row 16's text. Keep the sentence about exit 2 and substring/section consistency in row 16 intact.

### C2 — Append-only correction for the Go advisory artifact (duty 1)

Candidate correction text for the round-15 lesson or LOG (do not edit `ReviewGoInference.md`):

> Correction to `.ufo/waves/round-14/w1/ReviewGoInference.md` Finding 2 (lines 56-58). The statement that `registerStructures` does not consult the snapshot is incorrect. Struct resolution reaches the snapshot through `DataTypeMapper.registerStructure` (`DataTypeMapper.java:176`) and `getType(List,…)` (`:310-313`), which dispatch virtually to `GoRttiMapper.getType` (`GoRttiMapper.java:380-382`), which reaches `GoTypeManager.java:449` `apiSnapshot.getTypeDef`. Snapshot absence therefore affects whether struct resolution succeeds. [INFERENCE] The outcome-level claim (both IOException branches return null) was not re-opened in round 15. The knowledge entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` is unaffected; the historical cause remains UNKNOWN.

Also qualify the round-14 lesson's Mistakes row "causal-overreach" pointer to `ReviewGoInference.md` by appending a pointer to this correction. Preserve the artifact bytes.

## D. Proposed L1 checks (named; not run by this seat)

1. `sha256sum` on S001, S003, S007 and compare with O1-O3.
2. Re-open the anchors in section A (`GoRttiMapper.java:79, 170-176, 331, 351-366, 379-382`; `DataTypeMapper.java:172-176, 310-313`; `GoTypeManager.java:443-451`; `GoApiSnapshot.java:115, 118-126, 503-505`; `ChangeHistory.md:564, 582, 585`) with `unzip -p … | nl -ba` and `sed -n`.
3. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`; diff `corpus/SOURCES.md` against the round-14 commit `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22` to confirm only permitted cells changed.
4. `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` and `--frozen .ufo/waves/round-14/fixtures/expected.json`, as regression evidence that the gate is unchanged.
5. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff 3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22 -- corpus/QUALITY.md` shows only appended row 17; row 16 unchanged.
6. `git diff 3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22 -- .ufo/waves/round-14/w1/ReviewGoInference.md` is empty (the artifact stays unedited).
7. Any census or measure run passes an explicit `--root` (Mistake 19).
8. Re-derive the round-15 C1 installed JSON inventory against the installed Base data directory; this seat did not produce its counts.

## E. Residual uncertainty

- The `EMPTY`/`getTypeDef` step (C2 bracketed [INFERENCE]) was not opened.
- `GoRttiMapper.java:102-129` (both branches return null) was not re-opened this round.
- `patchverdiffs/` contents and the patch-diff fallback at `GoApiSnapshot.java:148-166` were not opened this round.
- S004 was not reopened this round; no claim about its diff is made here.
- The historical round-4 op counts and the 2.34.1 side remain corpus-recorded and unverified locally.

## F. Tooling

No tools installed or updated. Record: none.
