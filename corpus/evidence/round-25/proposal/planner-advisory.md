# kaidokuR25 — actual native planner advisory

This is the **actual native planner, POST original64 proposal barrier and after the first actual distiller admission**, under the assigned chronology; **not a retroactive pre-wave planner**. P54 stays reviewer. Advisory only: Main remains L1, judge and integrator and decides implementation authorization, admission and shipping. No second coordinator, dispatch, route change or substrate change occurred.

## Inputs and observed state

Source authority is immutable Git objects reachable from BASE `18e7eb6d9fe8842678af5f1cffbd680ead4ad473` and prerequisite I `62feef9c0cbd5aadafa453456c55c28832175206`, plus the expressly permitted Main receipts. I's recorded unique parent is BASE. I contains `tools/round-25/ruler.py` and `corpus/evidence/round-25/oracle/{cases,contract,derivation}.json`; an exact `ls-tree I -- tools/round-25/instrument-custody.py` returned no entry. No working-tree draft, private proposal metadata, other-lane report or candidate behavior supplies authority here.

- **Observed retained process evidence:** `parent-before-process.json` records Main's ruler invocation with measured BASE, oracle I and cases SHA-256 `6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0`: exit 2, `candidate_unavailable`, total 34, executed 0, exact 0, and 34 `not_observed` records with null observations. This is not 34 experimentally observed old failures.
- **Observed retained negative control:** `parent-tamper-process.json` changes the supplied oracle digest to zeros and records exit 2, outer finding `could_not_evaluate`, error `snapshot_tampered:oracle`. `parent-proof.json` corroborates these summaries but is not a substitute for those producing envelopes.
- **Fixed dependencies in that proof:** ruler SHA-256 `20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532`; contract `069f9119e7c81512f601e1ece804d4ca393d3c8f6f533a90525ceb95fb5b6824`; derivation `59269265f74d272fa51d6da81cf2ca4d47afa0a7b53a92638a79c5e65587d683`. These are retained Main assertions, not fresh planner recomputations.
- **Unobserved:** every candidate response, its output evidence quality, actual R25 claims first-add/SRT landing, implementation authorization, final no-harm result and admission. No executable, fixture, gate, test, build, linter or formatter was run by this seat. Only inert Git reads and two historical-blob SHA-256 pipelines were used; no installation was needed or performed.

## One real request: `valid_supersession`

The representative request is exactly the existing `cases.json` row, not a new fixture. It selects claims `.ufo/waves/round-24/claims.json`, reference `.ufo/waves/round-24/tools/freeze-gate.py`, measured BASE, and the following chain:

| Link | Observed Git evidence | Consequence for this request |
|---|---|---|
| Claims first-add F | `git log --diff-filter=A BASE -- <claims>` returns only `5dc49bfe25d21139693161c786e69c5a11a65bcc`, with sole parent `97ade2e5e2dcf6cfd01d0da8634879d14969f9cc`. Full claims-path history shows one A and one later M, no delete/re-add. | Declared freeze is the actual first addition, not an arbitrarily selected revision. |
| Frozen claims | `git show F:<claims>` and `ls-tree F` give claims blob `85532f7a85cdb331bbf8df90101bb1fa0da5e130`, mode 100644. Its `instruments` pin for the selected path is `1e2a937018feec21ad200f80a4c9a749b3de4af190fff548eb4dd84717b8870f`. | The request's frozen pin agrees with the original claim pin, not the later instrument bytes. |
| Instrument existed before F | `ls-tree F` and `ls-tree F^` both give selected-path blob `a7b2e46477729f7558a7b5423a12439233e1a906`, mode 100755. Claims has no F-parent entry. | Same regular blob and mode already existed in the unique freeze parent. |
| Frozen content | `git show F:<instrument> | sha256sum` returns `1e2a937018feec21ad200f80a4c9a749b3de4af190fff548eb4dd84717b8870f`. | Actual blob bytes, not the claims string alone, substantiate the frozen digest. |
| Exact-path revision S | Both ordinary and ancestry-path Git logs over F..BASE for this instrument return only `9fb4eacd23eb69ee9d659dd041e006e9ccd61480`. | S is the single post-freeze exact-path change in this measured history. |
| Revision post-image | `ls-tree S` gives regular mode 100755, blob `e17ada9bf61bb7cfd328c6b05052e2094e630ad8`; `git show S:<instrument> | sha256sum` returns `8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329`. | The supplied supersession digest is the post-image at S, not S's parent or today's filesystem. |
| Genuine disclosure | S's diff adds bare-name `INSTRUMENT_UNRESOLVED` detection. The separate subsequent commit `69e82c48be5614ce96f7c1c32445fe61c4870630` appends the path/S/digest/reason entry to claims; original claims had none. BASE retains it. | Instrument revision and disclosure-append commit are distinct identities. The request names S, correctly, with reason `Disclosed R24 bare-name correction; not old-result rescue`. |
| Fixed expectation | I's `valid_supersession` row declares exit **0**, finding **`clean`**. | This is a prospective custody-only expected pair, **not an observed candidate result or old R24 admission**. |

This is useful to an actual caller: it distinguishes the original pinned instrument from a later disclosed implementation, checks the latter's exact changed path and bytes, and reports enough identities to inspect the evidence. It does not decide whether the correction was scientifically justified, whether the historical before record was actually retaken, or which code historically executed.

## Proposed axes for Main's round plan

Main should declare these axes in its `ufo-round-plan-v1`, stable for this round, without retroactively replacing historical coverage/depth/calibration scores:

1. **Custody correctness:** exact claims first-add, prior regular blob/mode, original pin, exhaustive exact-path revisions, and valid supersession post-images.
2. **Decision calibration:** deterministic primary precedence; unsupported, unresolved, proven absent and unevaluable never collapse into clean absence.
3. **Consumer usefulness:** one explicit request produces actionable Git identities/digests/error metadata, not a source-text assertion, default-green branch, discovery proxy or ledger-agreement tautology.
4. **Non-regression and authority discipline:** immutable oracle/old results, no audited-source execution, full Main-owned no-harm duties, honest epochs and native-role chronology.

## Smallest ordered end-to-end skeleton — prose only

| Step | Proposed implementation/decision | Per-step evidence and gate |
|---|---|---|
| 1. Preserve the authorization boundary | Main authors the bounded round plan and actually lands the prospective R25 claims/SRT under its authorized prerequisite exception before candidate implementation. Keep ruler, cases, contract and derivation identities fixed. No stub candidate. | Existing I and actual before/tamper envelopes establish only the prerequisite/availability stage. Claims/SRT landing is not established by this advisory. Keep the plan under the 4 MiB read-time bound. |
| 2. Deliberately overfit one case in the design | Follow only the `valid_supersession` chain above: literal request decoding → claims freeze identity → exact regular tree entries at F/F-parent → original digest → F..BASE path-change set → S membership/post-image digest → custody-scoped output. Initially reason with those concrete values; do not ship a hardcoded ID/path/expected-answer recognizer. | The trace table provides every positive link; I fixes the expected 0/clean pair. The first eventual demonstration must expose the same object identities, not merely print `clean`. No execution is authorized to this seat. |
| 3. Generalize the data, not the oracle | Replace those selected values with typed request fields. Use one straightforward CLI, strict duplicate-member-rejecting JSON decoding, one conservative reference normalizer, explicit Git-object reads, a digest operation, and an ordered decision pipeline. Do not import the ruler/oracle/old gate as candidate decision logic; do not add claim discovery, shell parsing, basename resolution, extra targets or another oracle. | I's contract and all 34 unchanged request/expected rows are the sole finite behavior target. The table below is a reading index, not a replacement fixture. |
| 4. Make the answer usable | Return one JSON object with the exact primary finding and `scope: explicit_reference_custody_only`, plus normalized selected path, applicable claims/freeze/measured/blob identities, computed/requested digests and revision/disclosure differences or error metadata. Never execute/import the instrument. | Static ruler inspection shows it grades exit/finding only and retains full stdout/stderr; Main must review the retained evidence fields separately. A bare green pair is insufficient evidence of useful output. |
| 5. Main's eventual fixed gate and preservation review | Only after actual authorized claims and candidate landings, Main runs the unchanged I ruler against the immutable candidate commit, with the pinned oracle digest; retains full process records and names any unobserved/unsettled cases. Gate: all 34 exact pairs, no narrowing, plus Main's separate output-meaning and full no-harm review. | Existing red controls remain in the 34: undisclosed revision, wrong digest, wrong/wrong-path/missing supersession, wrong frozen pin, and unavailable inputs must fail as specified. No new fixtures or alternate target are proposed. Ruler mismatch/unevaluable is not admission. |

### Complete unchanged finite case index

All requests remain verbatim at I, including `duplicate_json_member`'s **raw** JSON; do not round-trip it through a decoder that erases its duplicate key. Grouping below does not merge measurements or change denominators.

| Exact exit / primary finding | Existing case IDs |
|---|---|
| 0 / `clean` | `exact_prior_pin`, `dot_prefix`, `lane_placeholder`, `dollar_lane_placeholder`, `valid_supersession` |
| 2 / `request_invalid` | `nonstring_reference`, `malformed_digest`, `supersession_missing_reason`, `supersession_duplicate`, `duplicate_json_member`, `whitespace_reason` |
| 2 / `reference_unresolved` | `bare_reference` |
| 2 / `reference_unsupported` | `parent_traversal`, `internal_parent_traversal`, `directory_reference`, `module_reference`, `tree_reference`, `unsupported_absolute_root`, `leading_dash` |
| 1 / `instrument_absent` | `named_absent_blob`, `actual_absent_at_claim_freeze`, `scripts_root_missing`, `typescript_missing`, `uppercase_suffix_missing` |
| 1 / `pin_mismatch` | `wrong_pin`, `later_pin_not_frozen` |
| 1 / `revision_undisclosed` | `revised_undisclosed` |
| 1 / `supersession_digest_mismatch` | `supersession_wrong_digest` |
| 1 / `supersession_not_revision` | `supersession_wrong_commit`, `supersession_wrong_path` |
| 2 / `supersession_commit_unavailable` | `supersession_missing_commit` |
| 2 / `freeze_mismatch` | `freeze_not_claims_first_add` |
| 2 / `measured_commit_unavailable` | `invalid_measured_commit` |
| 1 / `instrument_not_prior` | `instrument_added_with_claims` |

### Precedence and absence semantics

Use the fixed order: request validity → unresolved/unsupported reference → measured commit availability → freeze/claims identity → absent/nonregular/unreadable freeze entry → prior-parent identity → frozen pin → supersession commit availability → revision membership → post-image digest → undisclosed revisions → clean. Validate all supplied supersessions at each precedence class before advancing; do not let array iteration determine which class wins.

`later_pin_not_frozen` must fail `pin_mismatch` despite a valid supersession. `supersession_wrong_commit` and `supersession_wrong_path` must report `supersession_not_revision` before the still-undisclosed real revision. Duplicate supersessions or blank/whitespace reason are `request_invalid` before Git decisions. An unavailable supersession object is exit 2, not merely an undisclosed revision.

Chosen input policy strips **at most one** supported leading `./`, `<LANE>/` or `$LANE/`; it does not interpolate a shell variable. Validate the remaining ASCII components and case-insensitive py/sh/js/mjs/ts suffix, without a root allowlist. Bare names are unresolved even if uniquely guessable; absolute paths, traversal, commands and malformed shapes are unsupported. A syntactically supported exact path proven missing from an otherwise evaluable freeze tree is `instrument_absent`/1: `scripts/nonexistent.py` and uppercase/TypeScript suffix cases must reach that check. A tree-shaped reference rejected by syntax is unsupported, not a blob absence finding. Nonregular Git entries, unreadable objects, ambiguous/re-added/nonlinear unsupported claims history or Git failures are unevaluable/2, never guessed absent or clean. Same regular mode **and** blob in the unique freeze parent is required. The 34 do not independently exercise every general contract boundary, so do not describe them as universal coverage.

## Independence, history and real consumer value

- **Git facts** are the inert identities, modes, history and hashes traced above. They establish custody relations, not authorship authenticity, reason truth or historical execution.
- **Chosen input policy** supplies the reference grammar, duplicate-key rejection, required typed fields/nonblank reasons, conservative unsupported histories and primary-finding order. These are deliberate API rules, not discoveries about R24. RFC 8259's uniqueness SHOULD does not itself require this API's rejection policy.
- **Known-history unblinding:** BASE and the R24 correction were already known when expectations were authored. `derivation.json` expressly identifies the same scoped author proposing the contract and later authoring the candidate. Prospective pre-candidate literals provide bounded causal separation, not an outside verifier or blinded holdout.
- **Unobserved candidate behavior:** no present result establishes that it traverses Git correctly, resists routing/replacement redirection, never executes audited bytes, or returns useful evidence. The candidate must derive findings from request plus Git objects; expectations must not be generated from/imported from candidate helpers. Sharing Git facts, JSON schemas or SHA-256 algorithms does not alone create or disprove circularity.
- The old verifier's source recursively extracts claim strings with root/suffix regexes, accepts disclosures by path/commit with a truthy reason, and compares author-written ledger verdict/code sets. The new consumer instead accepts an already-selected reference and validates revision membership and actual post-image digests. It does **not** replace historical discovery/admission coverage. A ledger matching a gate is agreement, not independent semantic evidence; source wiring or an output default cannot substitute for the fixed process pairs and object evidence.
- The fixed ruler checks the cases digest, not separate contract/derivation digests at execution, and grades only exit/primary finding. Its root guard observes lstat/index/refs/status at named instants, not continuous enforcement, all-content integrity, object-store integrity or universal no-execution. Main must preserve/review these dependencies and limitations separately rather than crediting absent checks.

## Concrete conflicts and hard boundaries before implementation

1. **Literal QUALITY33 conflict remains:** BASE QUALITY #33 requires counting instruments committed before claims, pinned there, and later revisions disclosed with a re-taken before record. The authorized R25 order puts independent ruler/oracle before claims but candidate implementation after actual claims. Therefore the candidate cannot simultaneously be represented as a preexisting subject at that freeze. No stub, rebased freeze, candidate-as-ruler relabeling, rewritten QUALITY33, or self-CLEAN assertion resolves this subject-after-freeze/role cycle. The assignment's exception is disclosed, not full conformance. This is a concrete ordering conflict, not a contradiction requiring an alternate 34-case oracle.
2. **Old results remain unmet:** BASE's retained original `after-c2-frozen.json` has exit 1, executed original digest, 9/11 ledger agreement and mismatches round-17/18. Revised `after-c2-revised.json` has exit 0 and 11/11 agreement, but only 1 clean freeze. `final/summary.json` labels both checks passed because the original exit 1 was expected; its 12/12 is not proof the original calibration target passed. Do not replace original 9/11 with revised 11/11 or conflate R23 six-verb 4/6 with R24 four-verb 4/4.
3. **No internal conflict found in the representative expected pair:** its observed prior blob, frozen pin, sole exact-path revision and correct post-image support the chosen finite 0/clean expectation. That is a static derivation, not candidate observation. No oracle edit is justified by this datawalk.
4. **Authorization/measurement prerequisite remains unproven here:** actual R25 claims/SRT landing and later candidate results are not in the inspected permitted inputs. Proposal metadata cannot prove them or authorize this seat to implement. Main must establish those stages; this advisory does not certify or perform them.
5. **Full no-harm stays Main-owned:** retain old evidence, knowledge/source rows, LOG/SCORECARD prefixes, historical denominators and failure records, maps/separators and existing controls; preserve frozen dependencies and complete read-set/epoch qualifications. Optional preservation-draft removal does not relax that duty. The old reports-path detector remains UNDETECTED per assignment, with that draft unlanded; no old gate/ledger or oracle repair is proposed. Main's corrected categorical `.ufo` ban and the assignment's actual `check-ignore` exit 1 for exactly `.ufo/waves/round-25/claims.json` are scoped context, not planner-executed checks or permission for arbitrary paths.
6. **Epoch/role honesty:** retain P55 working-tree-read, P18 scratch and P17–P52 post-BASE draft qualifications; never relabel them immutable-BASE evidence. This native post-proposal advisory does not erase those epochs or make P54 a planner. No resumed-run continuity is proved by prior reports/cache or by this advisory; if Main resumes, continuity assumptions must be handled under canonical `resume_continuity_v1`, not treated as proof.

No code or fixture was drafted. No gate was executed. This report is the bounded round-plan advice only; Main alone determines subsequent action and judgment.
