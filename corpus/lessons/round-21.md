# Round 21 — record-bound evidence and bounded first-failure observations

Author: KaidokuR21, attempt 1. Baseline `2dd430cb6bcad60ff4db720c052074f1f75eecbc`; claims frozen and pushed at `f4e95af909d692156e984bf2049e1c7fb4a2a836` before tool measurements. The outside round-20 verifier is non-author MadoR20Recovery; its narrow admission is retained, not rewritten. This round owns calibration C1 and depth C2, with calibration tied-lowest under the existing finite 10.0 proxies. Neither proxy measures mastery.

## Gate

Source opening by the author on 2026-10-21:

| Row | URL and location | Located contiguous quote (at most 25 words) | Decision / scope |
|---|---|---|---|
| S049 | https://www.rfc-editor.org/rfc/rfc8259 — section 4 Objects, page 6 | “The names within an object SHOULD be unique.” | admit as JSON interoperability support; local Evidence binding additionally requires application fields. A string containing a verb is not the verb's operation member. The RFC does not authenticate Evidence. |
| S050 | https://docs.python.org/3/library/json.html — Repeated Names Within an Object, Python 3.15.0 documentation | “The object_pairs_hook parameter can be used to alter this behavior.” | admit as documentation of explicit decoder ambiguity policy; no host-version or execution claim. The preceding paragraph says default decoding retains the last name/value pair. |

Registry changes: S049/S050 added as mined tier A, used-by this lesson. Existing S001–S048 cells intentionally unchanged. Source rows are not counted as knowledge expansion. Bounded search: two official documents identified, screened and included; zero excluded documents. Stop: JSON mapping/decoder ambiguity is answered; REA-specific producer semantics remain grounded in retained REA records, not inferred from the JSON specification.

Candidate rejection rules frozen with the claims: reject a matching id/operation spread across unrelated records; reject a typed refusal as held success; reject missing or malformed observation metadata as bounded silence. Admit valid same-record success and valid bounded-null observations only within their declared scope. Actual decisions and exercised evidence are appended after integration; author-side workers cannot supply the required outside admit/reject spot-check.

## Mistakes

| Class | Motivating evidence | Captured-by | Fix and failure requirement |
|---|---|---|---|
| vacuous — record association mistaken for token co-occurrence | round-20 verifier R20-EVIDENCE; round-20 tools/verb-coverage.py bound_evidence | QUALITY #25, whose registered limitation is only token checking | C1 successor must associate the cited id and exact operation within one supported Evidence record and reject typed refusal records. A frozen independent negative must false-pass at baseline and fail under the successor, with a genuine positive retained. |
| vacuous — absent observation confused with bounded silence | round-20 tools/compare-first-failure.py run_extractor accepts bare JSON null without last_line | QUALITY #7 and #11; existing extractor documentation bounds absence through its last retained line | C2 requires the extractor envelope, explicit first_failure, and valid last_line. A frozen bare-null case must expose the old false clean; valid bounded silence and both asymmetric-null mismatches remain distinct. |
| scope — aggregate C1 harness reuses C3 carrier receipt | round-20 verifier R20-SEP and Causal separation ruling | causal separation is about independent verifiability, not mere helper sharing | Replace the current positive-control authority with a C1-owned isolated fixture, retaining both positive and package-decoy checks. The old aggregate remains historical. Shared validator use alone neither proves nor disproves causal coupling. |
| scope — scout report misroot | W1 `ScoutCatalogBytes` wrote `.ufo/waves/round-21/w1/ScoutCatalogBytes.md` at fleet root despite absolute-root context; KengakuR26 and ChousaR25 independently flagged it | prompt §6 absolute Report trailer rule | Fleet `git status --porcelain` found the untracked round-21 tree; `cp <fleet-path> <lane-path> && cmp <fleet-path> <lane-path> && rm <fleet-path>` exited 0. Exact original report bytes retained under the lane; only the seat-authored fleet copy was removed. This repairs location, not a claim of runtime path enforcement. |

## Routed residual dispositions

- R20-SEP: addressed within C1; actual correction and test evidence must be appended before closure.
- R20-EVIDENCE: record binding and refusal negatives are C1; bounded comparator negatives are C2. No cryptographic Evidence authentication claim is made.
- R20-TIME: exact two 2030 fixture/diagnostic allowances remain historical. Binary and zoneless text exclusions remain exclusions; no full-tree timestamp claim.
- R20-LINT-SANDBOX: duplicate-name nested-read D6a and host-HOME/AF_UNIX D6b remain open. No private HOME inspection, no sandbox/security certification.
- R20-CENSUS-GUARD: DATED shelter/same-line laundering and loader/copy/memfd/same-owner bypasses remain open. Green guard records attest instants only.
- R20-SOURCE: S041/S045/S046 rendered-quote caveats and S043 unrowed -c anchors remain documentation debt unless a fresh superseding source row is explicitly landed. Existing rows are not silently rewritten.
- R20-ADJACENCY: REA overlap with revenger remains unresolved; evidence-tool maintenance does not confer province ownership.
- R20 C3 remains nineteen exact-artifact outcome-held-out forecasts, not general Go-version prediction. This round's replay of those observations is retrospective regression, not new prediction. Pathless objdump subject:null, synthetic Harmony, and later objdump OOM remain explicit boundaries.

No native carrier, REA producer, provider probe, account/configuration, host package/service/boot, or secret material is in this round's planned execution. No tool installation is required.

## Exercised Gate decisions — recovery integration

The coordinator retained the predecessor's frozen declaration, fixture contract,
source rows and lesson after reopening both official sources. It discarded no
claimed result: the predecessor had run no implementation. The three external
worktrees remain unused after all executor seats died; no file from them is
credited. Stable measured source V=`a75c3c67e4e658a232e1842ab1aceb383b711269`.

- **Admit within scope:** valid same-record/wrapped Evidence, pathless
  architecture listing with its exact parameter, bounded-null observation,
  typed nullable EOF and kind/index match with different phase/va.
- **Reject:** cross-record/prose id-operation association, typed execution
  refusal/could-not-evaluate envelopes, wrong objdump operation parameter.
  Unsupported/malformed/duplicate-member JSON is unevaluable (exit2), not an
  admitted success. Both well-formed asymmetric-null outcomes remain mismatches
  (exit1); naked null is unevaluable rather than bounded silence.
- **Execution evidence:** `.ufo/waves/round-21/verify/summary.json`, producer
  `python3 -I -B .ufo/waves/round-21/verify.py --root <LANE> --before
  2dd430cb6bcad60ff4db720c052074f1f75eecbc --after V`, exit0,13/13 expected exits.
  Each child record retains producing argv/stdout/stderr and measured revision.
- **Shown able to fail:** same frozen C1 battery at B exits1 with nine false
  clean accepts, at V exits0 with all twelve expected decisions; C2 at B exits1
  with five false cleans and one `KeyError: 'index'`, at V exits0 with all
  twenty expected decisions. See `verify/before-C1.json`, `before-C2.json`,
  `after-C1.json`, `after-C2.json`. Expectations/inputs are the same frozen
  Git blobs; only each claim's selected validator changes.
- **R20-SEP current authority:** `verify/isolated-without-C3.json` shows the
  C1-owned metadata positive exit0 and package-decoy exit1 with
  `analyze_step_unauthenticated`, from a scratch root containing only the R17
  validator/pins. Recorded fixture argv is never executed. Old R20 aggregate
  and original C3 authority bytes remain historical, not silently patched.
- **No-harm:** `verify/no-harm.json`:1134 prior files byte-identical,
  map102/102 and citation rules17/17 unchanged, prior25 admission rows retained.
  `verify/verb-coverage.json`: all five old target booleans still supported by
  genuine record ids,133/153 mentions. Nineteen retained R20-C3 log pairs match
  with equal log digests; these are retrospective, not new predictions.
- **Frozen-input negative:** `verify/frozen-input-red.json` mutates a copied
  fixture to `{}`; same battery returns2 `snapshot_tampered`. Expected manifest
  keys and digests are checked against fixed contract/fixture Git revisions;
  no authentication or temporal-continuity claim follows.
- **Outside sample:** pending the independent non-author closure. Every W1/W2
  seat is author-side and cannot supply that sample or SHONEN promotion marks.

## Sources census and frontier disposition

Source rows48→50, A42→44/B5/C1 unchanged, mined46→48/rejected2 unchanged —
re-runnable argv and raw output: `.ufo/waves/round-21/verify/source-rows.json`.
S049/S050 were reopened on2026-10-21 with the original located quotes above;
both are mined by this lesson and ground R21-C1/QUALITY26. No prior row's
status/recheck/used-by cell changed; new rows are additions, not old→new edits.
No new knowledge entry or province frontier surface is admitted; expansion
therefore remains unchanged.

Recovery-start census command and actual exit0 output are retained in
`.ufo/waves/round-21/start-census.json`; inherited source drafts were already
present then. The original round-start48-row count is frozen in claims.json.
Final identical command/exit0 is in `verify/sources-census.json`:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku W04 S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

This round incorporates the outside R20-EVIDENCE/SEP feedback as bounded
criteria26–27; all other residual dispositions above stay open. No install,
package/service/boot mutation, provider call or analyzed-carrier execution
occurred in the coordinator's implemented work.

## Post-wave correction

W2 `R21Attack63.md` correctly distinguishes removing a C3-file dependency from
an independently authored positive: the initial control invoked the validator's
own `_carrier_receipt` builder. Supersedes only the initial control's
independence wording above, not the observed V exits or the frozen12/20 cases.

| Mistake class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous — self-generated positive oracle | `.ufo/waves/round-21/w2/R21Attack63.md`; initial control at V | none; new QUALITY28 captures it | A separately authored inert receipt template and expected exits were frozen at `174948f0e6052ec90a0c51f14516ded210b99273` before the replacement demonstration. Rendering uses no validator import/builder or decision code; both validator/pins digests and template digest are retained. An altered template must return2, while independent positive0 and otherwise-identical package-decoy1 remain required. |
| reference-drift — aggregate CLI refusal class escaped the successor | coordinator source review of `verb-coverage.py` old-helper boundary | existing 0/1/2 registry contract | Convert only the old helper's declared Refusal exception to the successor's unevaluable error class. A supplementary invalid-revision pre-fix1/post-fix2 pair is separate from the frozen twelve-case denominator. |

W2 settled68 seats:49 reports,19 terminal errors; W1 settled64:26 reports,
19 terminal errors and19 aborts. Per-seat names, actual answering providers/models,
terminal text and cutoffs are in `wave1-terminal.json`/`wave2-terminal.json`;
all missing-report causes resolve in the corresponding causes/outcomes files.
No dead seat was replaced. All four assigned schema mutations were killed
with positive controls and restored bytes (`w2/R21Attack65.md`–`68.md`).
These are author-side results, not the required outside sample.

The source registry also adds the explicit S049→S050 study path and bounded
direct-opening Search log; no prior table row was edited. Post-correction
measurements use a separate `verify/final/` output directory when exercised,
preserving every initial V receipt rather than overwriting it.
