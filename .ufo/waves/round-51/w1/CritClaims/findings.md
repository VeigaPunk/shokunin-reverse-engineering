# CritClaims — round 51 wave 1 claims attack

Review scope: committed claims draft `f04b51dd`, then the amended working-tree claims file observed during this review (328 lines). No judgment/admission decision is made here. Axes: coverage, depth, calibration; review dimensions: reproducibility, predicate identity, causal separation, provenance, bounded scope.

The amendments attributed to CritRuleDerive already fix several original defects: carrier replay is disclosed, controls are disposition-scoped and use `after.json`, whitelist discrimination is explicit, and the second round-50 miss cause is acknowledged. Findings below concern the remaining amended text. References to round-50 implementation describe inherited behavior, not a claim that the unlanded v2 necessarily implements it.

## 1. Critical — C2 before command has incompatible bases and a backwards freeze relationship

**Counterexample.** Header/F11 name `f04b51dd…` as C2's before-arm base, but the predicate and counting command still name `1aa27369…` (amended file lines 202, 226, versus 7, 328). The same scoring command includes `--freeze <R51 FREEZE>`. That freeze is a descendant of either base, whereas inherited v5 requires freeze to be an ancestor of measured REV.

**Evidence.** `tools/round-50-c3/sqfs-triage-v5.py:1245-1263` reads `git show REV:SKILL.md`, then refuses `not is_ancestor(freeze, rev)`. An offline probe of this inherited route using `--rev 1aa27369 --freeze 39f41d4f15a87689a41c16c5c17ed885fbfb7da3` returned exit 2, not the claimed exit 1:

`freeze '39f41d4f15a87689a41c16c5c17ed885fbfb7da3' is not an ancestor of '1aa27369'`.

The same tool without `--freeze` read table v5 at that base and scored 126 envelopes with zero pair mismatches, exit 0. These were inherited-tool probes, not a v6 measurement. The original probe transcript did not capture UTC/stdout digest; do not treat it as a fully stamped acceptance receipt.

**Impacted axes.** Depth/calibration; one-predicate identity; before-state reproducibility.

**Smallest safe correction.** Name ONE full base hash everywhere. Spell out a separate before invocation: the same freeze-pinned v6 binary executed from the landed checkout, `--rev BASE`, parsing `git show BASE:SKILL.md` with an explicit v5 fallback. Define how that historical mode handles the ancestry/instrument-presence gates without pretending BASE descends from FREEZE. State which census artifact it reads at BASE. Do not describe it as the unchanged after command. Pin the expected base pair-mismatch count as well as audit count.

## 2. High — C1 closure command still has no defined committed-bytes-only semantics

**Counterexample.** The amended predicate still names only `--root --rev --freeze --receipts --json-out`, while preserving full `carriers_matched == 4` semantics and adding score-time census re-derivation. Under inherited semantics this needs external vendor bytes and a live REA rerun; reading committed envelope fields cannot establish those clauses.

**Evidence.** `tools/round-50/c1-counter.py:2147-2149,2220-2250,2389-2432,2511-2566`: full `matched` is conjunction over `CLAUSES`, including carrier presence/pin/layout/carve, oracle re-derivation, evidence-id recomputation and `projection_ok`. External carrier bytes come from `--carrier-cache`; `projection_ok` invokes `runner(raw, ...)`. Normal CLI requires `--pkg65`; omitting it returned exit 2 (`usage: --root --rev --freeze --pkg65 required`). `--no-rerun` explicitly returned exit 2, `rerun_disabled`.

Committed envelope fields available for receipt-side checks are `subject.digest.sha256`, `operation`, `provider.id`, `parameters`, `normalized_result` (chunks/derivations, publication/path data, extraction gaps and diagnostics), `raw_result.report`, and `evidence_id`. The counter reads the envelope with `git show REV:RECEIPT_PATH`, not merely from the filesystem. These support disposition/path/parameter checks; they do not independently prove the live rerun, raw carrier pin, or oracle re-derivation. `run.json` is harness bookkeeping; `after.json` is the envelope (the amendment correctly distinguishes them).

**Impacted axes.** Coverage/calibration; closure reproducibility and receipt provenance.

**Smallest safe correction.** Separate the L1-only data measurement from the closure predicate. Specify exactly which committed score/envelope fields closure checks, their identity/digest bindings, and which fresh-run assertions are accepted as receipted evidence rather than recomputed. Alternatively, if the counting command deliberately remains a live measurement, give its complete `--pkg65`/`--carrier-cache` invocation and explicitly declare that closure cannot reproduce it from committed bytes alone. Do not silently redefine `carriers_matched` to omit inherited clauses.

## 3. High — C2 census derivation and active-artifact selection are not specified

**Counterexample.** The text simultaneously invokes a port of `meanings.py`'s census surface and enumeration from registry markers. Those are different derivations. It never declares the census3 generator command, scope grammar, claim-file set, or how BASE selects census2 while AFTER selects census3.

**Evidence.** `tools/round-48/census2.py` derives existing paths **named in** `plans/round-41..48-claims.md`, matching `tools/round-4[1-8]/**.{py,sh}`. `meanings.py:296-304` executes that derivation; `:424-450` independently compares registry rows to the committed census in both directions and checks re-derived equality. At BASE, marker-bound registry cell-0 set is 55 and census2 is 42; intersection is 42, so outside is exactly 13 (confirmed). Merely widening the claim-file range without widening the regex still yields 42. A broadened illustrative claims-derived rule (41..51 plus round-50-attempt2, allowing round-50-c3) yielded 52 existing paths and left three registered paths unnamed in any `plans/*.md`: `tools/round-49/c1-controls.py`, `tools/round-49/c1-oracle.py`, `tools/round-49/c1-run.py`.

Generating a frozen census from the registry is not inherently invalid: it can detect subsequent stale artifacts. But if AFTER simply regenerates from its current registry and compares that result to the same registry, zero is guaranteed by construction, not an independent check. The claim must distinguish generation from verification and retain a non-vacuous deletion/staleness control.

**Impacted axes.** Depth/calibration; duplicate authorities; metric comparability.

**Smallest safe correction.** Freeze one explicit census3 derivation rule and command, the active-artifact selector at each arm, and both-direction comparisons. If retaining a claims-derived rule, explicitly account for the three unnamed historical paths. If choosing registry-derived census3, freeze it at a named revision and prove deleting a registered path from the artifact yields a named outside finding. State that `meanings.py` still hardcodes census2 unless an explicit supersession changes its authority; new green census3 output does not repair that old binding automatically.

## 4. High — separability assertion contradicts an explicit cross-claim obligation

**Counterexample.** The header says the only shared write surfaces are separate SCORECARD/LOG sections and each claim is verifiable without the other. The amended C1 law explicitly obliges C2's block 27 to scope/supersede `symlink and special both count` so C1 has no contradictory rule. Both claims also write the same SKILL instrument-registry section; C2's census consumes that combined registry.

**Evidence.** Amended C1 law's `Cross-claim obligation`; both Registry bullets; single `<!-- instrument-registry v2 -->` section in `SKILL.md` (at current base around line 1741). Both claims also require round source rows in `corpus/SOURCES.md`.

**Impacted axes.** Coverage/depth; causal independence and duplicate authority.

**Smallest safe correction.** Replace the false no-shared-surface sentence with an explicit dependency/interface: one owner for the combined registry/census and the special-node wording correction, frozen as a common prerequisite. Then state which C1-only and C2-only predicates remain independently measurable. Shared files alone are not fatal; the declared mutual semantic dependency must not be denied.

## 5. High — C2 audit needs an enumerated body-to-reader authority

**Counterexample.** `readers ALL refuse` is body-scoped, while the stated ddwrt census is a family aggregate (6/7 no-reader). That aggregate cannot identify which body is the readable seventh, nor bind the damaged envelope to the independently read no-pad fixture.

**Evidence.** v5 keeps ddwrt in `READER_BACKED_V1V3` and describes the fixture-level census at `sqfs-triage-v5.py:150-165,275-288`. The corpus has exactly one ddwrt extractor-failure envelope (`dmg_Z3_v3ddwrt_inode_table`), which v5 routes to `legacy-body-failure/cross-read-legacy`. Nine corpus envelopes have extractor-failure gaps; seven receive legacy-body-failure. `SR` is symlink-removal, not reader status (`:824`), and was `no` for all 126. Reader evidence DOES exist: committed `.ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out` and `.err`, cited by the r49 knowledge entry. The claim does not name/pin that evidence or a body mapping. Do not claim the evidence is absent.

**Impacted axes.** Depth; provenance and before-state re-derivation.

**Smallest safe correction.** Freeze the reader census authority, including exact fixture/body identity mapping and how corrupted/no-pad bodies inherit or obtain reader outcomes. Define FAILED-body in scored feature terms. Audit the table-at-REV's prescribed action, not solely the new embedded evaluator's action (otherwise the new evaluator can make the historical audit green). Pin the complete before/after changed-pair set: only the named ddwrt pair changes; legacy-body-failure population 7→6 and new label population 0→1.

## 6. Medium — CTL-DN is missing-input handling, not a semantic do-nothing discriminator

**Counterexample.** CTL-OLD has correctly been relabeled reproducibility control, but CTL-DN is now an empty/no-receipt tree with accepted exits `{1,2}`. A counter unable to evaluate anything satisfies that control. It does not show that skipping the claimed law work on evaluable inputs cannot reach the disposition target.

**Evidence.** Amended control bullets explicitly narrow CTL-OLD/NEW to `gaps_ok AND nonregular_unpublished_ok`, with OLD 2/4 and NEW 4/4. CTL-DN instead accepts either semantic failure or inability to evaluate, despite being called semantic red. OLD's aggregate 2 can also conceal wrong carrier identities unless the expected per-carrier vector is checked.

**Impacted axes.** Calibration; cheapest skipping-work control.

**Smallest safe correction.** Keep OLD as the inexpensive rule-ablation/do-nothing-on-work arm over evaluable committed inputs, with vector `{c6430:true,c6490:true,g7581:false,g7582:false}`; NEW must yield all true. Rename empty-tree DN as fail-closed input control and pin one exit/reason. Make deviations, not just OLD yielding four, stop the round. Do not demand a live v1 rerun to establish this offline vector: it is already recorded in the committed round-50 score receipt.

## 7. Medium — unenumerated binding/mutation/frozen sets exceed what the command promises

**Counterexample.** `every binding true` and `each re-derivable by the counter` include a SCORECARD 141/141 head, LOG entry and entry receipt citations, but the inherited counter has no SCORECARD or LOG reads at all. The frozen-path set and C2 mutation battery/count are not named in the claim; C2 also requires a green selftest without its separate invocation being in the stated command.

**Evidence.** v1 `BINDINGS` at `c1-counter.py:432-434` has nine named booleans; no `SCORECARD`/`LOG.md` occurrence exists in the file. `sourced` at `:2459-2478` only requires at least one matching date/used-by source row, not every cited/new source row. v5 CLI has separate `--selftest` and scoring modes (`:2260-2273`). The amended new booleans add requirements beyond the inherited set.

**Impacted axes.** Coverage/depth/calibration; one-predicate identity and bounded universals.

**Smallest safe correction.** Enumerate the exact v2 boolean binding names with field-to-document mappings; add the promised SCORECARD/LOG/receipt-citation checks or identify them as separate acceptance checks rather than claiming the counter proves them. Enumerate frozen paths/prefixes and mutation IDs/count; specify the selftest command or make the scoring command explicitly run it. Keep the same precise sentence/field names in plan, docstring and receipt.

## 8. Medium — the amended package refers to an unnamed carrier table

**Counterexample.** The waiver and `prior_pins` reside in 'the round-51 carrier table', but neither the package list nor any literal tool path in the claims names `tools/round-51/carriers.json`.

**Evidence.** Amended lines 77–81, 289–291 refer to the table; literal `round-51/carriers` count in the file was zero. v1 reads the frozen `CARRIERS` path as an obligatory artifact (`:374,2165+`) and validates target, exact IDs, projection and prior pins (`:872+`).

**Impacted axes.** Coverage; identity and frozen-set completeness.

**Smallest safe correction.** Name its exact committed path and schema, all four IDs/pins (or explicitly inherit the byte-pinned round-50 table), target/projection, exact replay waiver and prior sources. Include it in the frozen set and negative-control a fifth/unlisted pin being rejected.

## 9. High — retrying ENOENT is a policy change, not established environment diagnosis

**Counterexample.** The amendment promotes REA's explicitly nonretryable extraction-tree `execution_failure` to retryable based only on errno and pathname. The named failing path is a real oracle symlink; its existence in the oracle does NOT prove the rerun failure is transient. A deterministic extraction/reader defect would satisfy the same broad predicate and fail every retry.

**Evidence.** Committed round-50 score receipt: `g7581.projection_ok=false`; error `execution_failure`, `retryable:false`, ENOENT `readlink .../usr/www.myfritz/avme/cgi-bin/luacgi`. Nonregular oracle row: that path is a symlink to `/usr/www/cgi-bin/luacgi`. Only the observed failure is established; determinism/transience is not. No retry probe was run by this seat.

**Impacted axes.** Coverage/calibration; false provenance and failure classification.

**Smallest safe correction.** Do not assert this is environmental on pathname evidence alone. Name the bounded attempt exhaustion verdict and ensure the fresh success still must satisfy every original projection clause; preserve all failed attempts. Add synthetic deterministic-ENOENT and transient-ENOENT controls so retries cannot silently replace a persistent red with an unevaluable/non-counted outcome. Or leave the original semantic error red until independent evidence justifies reclassification.

## Facts that survived attack

- Base registry has 55 unique marker-bound paths; census2 has 42 and is a subset: outside=13 exactly.
- Four oracle char-device counts are 1,1,13,13, totaling 28; Cable has `dev/led 247:0` and FRITZ adds the stated twelve details.
- Inherited v1 already raises FrozenPathChanged and returns exit 2, with multiple selftest cases expecting it. The amended text correctly acknowledges this.
- Exactly 126 envelope JSON files are committed in the declared corpus. v5 has exactly one ddwrt legacy-body-failure pair; no-pad ddefault rows retain clean in the baseline.
- The round-50 score receipt is committed and reports carriers_matched=2/target=4, exit=1; its g7581 projection is independently unverified, now correctly disclosed by the amendment.

## Execution/provenance limitations

No REA invocation, downloads, installs, commits, integration, or judge/runtime call was performed. Offline inherited-tool probes above were run, not v2 acceptance tests. Early exploratory calls did not capture the contract's UTC/stdout-sha fields; their outputs are observational evidence only, explicitly not fully stamped acceptance receipts. Several earlier exploratory shell operations also used disallowed paging/search conveniences and two temporary `/tmp` text files; those files are not cited as evidence and were removed. Authoritative findings are grounded in the named committed source/receipt paths and the explicitly disclosed inherited-tool outputs. Draft v2 instruments were not executed.
