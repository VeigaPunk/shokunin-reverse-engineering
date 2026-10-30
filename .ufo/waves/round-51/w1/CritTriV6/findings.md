# CritTriV6 — R51-C2 pre-freeze design attack

Axes: depth/executability; calibration/provenance; coverage/non-regression; single authority/reproducibility. This reviews the claims design and committed v5 evidence, not a landed v6 implementation. No admission/judgment is made here.

## 1. One-pair change is feasible, but the claims give false reader provenance

**Counterexample / evidence.** The exact zero-file extractor-failure envelope set with `squashfs_v3_ddwrt` in HF is `{dmg_Z3_v3ddwrt_inode_table}` (count 1) in `.ufo/waves/round-50/c3/c3-after.json` (126 envelopes, pair mismatches 0). A FAILED-only row keyed on that handler, extractor-failure+, P=0 can therefore move exactly that pair: `legacy-body-failure/cross-read-legacy` to `legacy-body-unreadable/preserve-unresolved`. It must precede legacy-body-failure or remove ddwrt from that row's failing-handler cell, while preserving partial-failure and dependency precedence.

The claim's parenthetical that the two clean nopad `_ddefault` envelopes' “readers succeeded” is contradicted by the committed `.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`: BE nopad `daa8e72d355d` and LE nopad `e7482db480f9` both have unsquashfs=1, 7z=2 (NO-READER). Sasquatch extraction succeeded; independent readers did not.

Seven corpus envelopes remain `clean/none` on census-NO-READER bytes: `dep_A2_squashfs_v3.be.nopad`, plus `squashfs_v3_ddwrt_squashfs_v3.{be,le}.{1kpad,4kpad,nopad}_ddefault`. The v5 clean row still says to match files to an oracle. This is a residual of the same independent-oracle problem, excluded by a FAILED-only audit. Do not call zero FAILED-body findings universal executability.

**Axes:** calibration, depth, non-regression.

**Smallest safe correction.** Keep the one-pair scope if that is the canonical claim, but replace “their readers succeeded” with “sasquatch succeeded”; explicitly disclose the seven unchanged clean/oracle residues and the FAILED-only audit boundary. `preserve-unresolved` is appropriate epistemically; make the cause say reader support is unvalidated for the variant, not that corruption is proven. The label “unreadable” must not imply a damaged-body verdict.

Do NOT move ddwrt wholesale into NO_READER_FAMILIES: changing both cached evaluator sets moves **8** pairs (one failure plus seven clean), not 1. Corrected measurement is `receipts/corrected-envelope-sets.json`. The earlier `e2_label_moves.out` changed the tuple but omitted the cached READER_BACKED_SET: its seven-label result is clean-only and superseded, not evidence of a complete move.

## 2. Audit needs an explicit support oracle; actual damaged-body refusal is not reader absence

**Counterexample / evidence.** There are nine extractor-failure envelopes: two partial-body failures, six zero-file v1/v2/v3 failures, and the ddwrt failure. All nine damaged subject digests lack direct rows in the v3 reader census (`receipts/e3_envelope_census_binding.out`). `dmg_Z3` has subject sha `839c17a83b706589f1b634d0e19fbc6950c3028072e3952c1c74a290ad2150c8`; its healthy parent has sha `daa8e72d355d…`. The round-42 sibling `manifest.json` supplies its parent and recipe (zero bytes 144..203), not the v5 feature tuple.

I reconstructed that exact damaged sha from the committed ddwrt fixture. Guarded offline reader calls returned unsquashfs `-lls` exit **1**, 7z `l -tSquashFS` exit **2**; receipts name commands, UTC and stdout digests. This confirms refusal, not a general rule that every damaged body's refusal means no reader exists. The other damaged bodies are precisely where refusal can be the intended cross-read diagnostic.

The census is fixture-level: ddwrt is 6/7 no-reader, with readable `squashfs_v3_le.bin` (`0161351caec8…`), whose corpus fixture-matrix envelopes record plain `squashfs_v3`. An aggregate “any reader exists” test misses ddwrt's target; a “missing exact digest means no reader” test falsely flags other damaged bodies. The census file covers v3 families, not v1/v2. This does not prove a v6 false positive; it identifies concrete choices that must not be left implicit.

**Axes:** depth, calibration, coverage.

**Smallest safe correction.** Freeze and name the reader-support evidence and mapping rule (including healthy-parent lineage if used), preserve distinction between reader support and successful reading of damaged bytes, and define missing-evidence behavior explicitly. Audit the **table-prescribed action**, not the v6 evaluator's action, otherwise base already looks repaired. Require the complete before violation-ID set to equal the singleton above; enumerate the other eight examined cases and report unknown/abstained evidence rather than silently treating it as pass. No name-only envelope exception masquerading as a general feature is acceptable.

Retain v5 guards: duplicate handler alternatives are refused in both columns (H1, source 2002–2022); dead alternatives are malformed (1988–1999); named guard/failure row and synthetic witness bindings (2053–2087). Redefine the v6 mutation witnesses explicitly. Swapping two `preserve-unresolved` actions is a no-op; swapping with `cross-read-legacy` is meaningful. Existing v5 controls do not automatically test the new row or audit.

## 3. Registry census is a second gate, with actual C1 coupling

**Counterexample / evidence.** v5 declares two inputs: revision-selected SKILL table and envelopes. Registry census additionally reads registry markers, census artifacts and possibly claims files. Both R51 claims require registry rows in the same SKILL.md registry block; census3 must account for C1's new rows as well as C2's. This contradicts the introductory claim that only LOG/SCORECARD write surfaces are shared and that either claim is verifiable without the other landing.

**Axes:** maintainability, single authority, non-regression.

**Smallest safe correction.** Prefer a separate registry-census instrument/receipt with its own predicate and exit. A composite invocation is a tradeoff for the canonical judge, not something this critic admits: if retained, state the two independent sub-verdicts, the C1 registration dependency and final-registry ordering. Define frozen path sets explicitly; copying v5's whole-tree policy to tools/round-51 couples both instruments' drift outcomes. Shared freeze coverage is possible, but cannot also be described as disjoint authority.

## 4. v5 really reads SKILL at --rev; literal R51 before command has an ancestry problem

**Evidence.** `sqfs-triage-v5.py:1232–1250` calls `git_show(root, ns.rev, 'SKILL.md')` unless `--skill` is supplied. `parse_skill` at 599–631 selects v5 first, v4 only as red-before fallback; older markers are refused. Base `1aa27369…` already contains the v5 marker/table. It is not read from the current worktree or solely from embedded V5_ROWS.

**Counterexample.** Source 1257–1264 requires FREEZE to be an ancestor of REV, raising Unevaluable (exit 2) otherwise. A future R51 freeze descends from the declared base, so the literal “same command” with `--rev BASE --freeze R51_FREEZE` cannot produce the claimed exit 1. Round-50 freeze `435d41fd4ad9211d1579fc447936fb33d2b74467` is an ancestor of BASE (measured), but that does not automatically make it a valid v6 drift baseline.

**Axes:** reproducibility, calibration.

**Smallest safe correction.** Publish two complete commands: pre-freeze before measurement with explicit non-applicable R51 freeze gating, and after with R51 ancestor/drift gating. Do not weaken after gating to accommodate before. Specify v6-first/v5-before-fallback marker precedence and record selected table version/source in receipts. Keep block 26 verbatim history and put a complete v6 table under its own marker, not an implicit delta. Base pair mismatch on the changed pair is expected if the fixed evaluator is v6; distinguish it from the audit finding.

## 5. census3 changes authority, not merely bytes; census2 consumers remain

**Evidence.** At BASE, registry rows=55, census2 paths=42, outside=**13**, missing=0 (`receipts/e1_registry_vs_census2.out`). This confirms the declared base count and the six R49 + six R50 + one R50-C3 composition.

But census2's frozen rule is claims-named existing `.py/.sh` paths in rounds 41–48 (`tools/round-48/census2.py`), not registry enumeration. A scope-extended claims-derived rule through round 51 (including suffixed directories/attempt2 claims) produces 52 present paths against 55 registry rows: outside floor **3**, specifically `tools/round-49/c1-controls.py`, `c1-oracle.py`, `c1-run.py`, named in no claims file at the reviewed draft (`e4_census3_floor.out`). Those paths exist. This is a counterexample to assuming a range extension alone yields zero; it is fixable by an explicit independent rule or current-round naming amendment.

A registry-snapshot census can legitimately detect future staleness, but zero at its generating revision is by construction. That is a **different contract** from claims-derived independent enumeration; it must not be sold as retaining all of census2's detection power. Also the predicate only names outside (one direction), whereas meanings.py checks duplicates, missing, outside and fresh-derivation equality.

`tools/round-48/meanings.py` hardcodes CENSUS=`tools/round-48/census2.json`, CENSUS_TOOL=`tools/round-48/census2.py` (39–40, 283–304, 424–450). Adding census3 does not migrate that consumer. It continues reporting outside rows, with further R51 registrations increasing the set. Historical gate behavior can intentionally remain historical; do not claim its existing surface was silently repaired.

**Axes:** single authority, calibration, maintainability.

**Smallest safe correction.** Freeze census3's exact universe, source rule, artifact selection at BASE/after, provenance, and scoped supersession. Name the separate derive tool's path if one lands. Resolve the three-path floor without undocumented hand-listing. Preserve or explicitly disclaim missing/duplicate/derivation-equality checks. State that meanings.py remains historical on census2, or land an explicitly versioned consumer migration; mere `supersedes` text inside JSON does not redirect a hardcoded consumer.

## Evidence and limits

No REA, network downloads, commits or lane integration. Only own seat artifacts/scratch were written. Offline probes/imports and read-only git performed. No tool installs. Draft v6 implementation, its controls, and canonical judge were **not run**. Reader refusals are factual measurements; the audit and census failure scenarios above are design counterexamples, not claims that a landed v6 already exhibits them.

Receipts retain stdout/err, UTC, command and sha metadata. `capture.sh`, `e3.py`, `e10.py`, and the v5 source snapshot are reproduction aids, not proposed instruments. Initial E3 failure was corrected and captured. Initial seven-label family probe is superseded as explained in finding 1. Shell reader calls initially stopped on semantic nonzero exits; the final subprocess receipts preserve exits 1/2 without turning them into success. Scratch is removed before handoff.
