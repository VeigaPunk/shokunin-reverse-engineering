# ReviewCriterion — QUALITY #18 contract review (round 16)

Seat: `KaidokuR16.ReviewCriterion` (leaf; no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: outside-route grounding and "no second research method" for the proposed QUALITY #18. Read-only. No gate, selftest, fixture, measure, control, build, test, lint, or REA/target call was executed. Only `read`, `grep`, `jq` on JSON, and read-only `git show` were used. No installs or updates.

## Candidate availability

`CriterionDraft.candidate.md` / `CriterionDraft.md` are **absent** from `.ufo/waves/round-16/w1/` (only `swarm-registry.json` exists there). The `KaidokuR16.CriterionDraft` seat is `pending` with empty output in `.ufo/waves/round-16/wave1-result.json`. This review therefore checks the **source contract** (spec task text at `.ufo/waves/round-16/wave1-spec.json`, the drafting prompt) and **proposed failure modes** against the repository. It is not a review of drafted text. Re-review when a candidate lands.

Contract under review (verbatim intent, `wave1-spec.json` drafting prompt): "Draft QUALITY #18 for recorded argv vs guidance, registry supplemental-baseline discoverability, and producing-command provenance. Cite r15 outside routes and round16 lesson; do not change #17."

## Axes

- **depth** — whether the three named obligations are reached at the anchors where they actually fail.
- **calibration** — whether the proposed row and its red control measure what they claim, and do not duplicate or overreach existing law.

## Findings (by severity)

### F1 — High (calibration): red-before control is presence-only and can go green without fixing the routed defect

`.ufo/waves/round-16/documentation-red.json`, script in `argv[3]`:
- `invocation_correction` = `'Round-16 correction' in kn and 'python3 -I /home/…/round-15/snapshot-inventory.py' in kn`.
- At baseline `6235498`, the second conjunct is already true via `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83` (the "Executed inventory" argv). The only missing piece is the literal marker `Round-16 correction`.
- The check never reads line 3 (`recheck:`, which still omits `-I`). A marker-only append would turn the control green while the routed defect 1 guidance is unchanged.

Consequence: the "red-before documentation control" for defect 1 does not discriminate. The round-15 closure itself states "Presence controls are not semantic proof" (`corpus/lessons/round-15-verifier-spotcheck.md`, independent claim recount section). Criterion18 must not cite this control as proof of the correction.

Fix (for L1 / the control owner, not this seat): require the `recheck:` line itself to equal the exercised argv or to carry an explicit distinction label.

### F2 — High (depth/scope): `producing_command_retained` checks the wrong object

- Routed defect 3 (`round-15-verifier-spotcheck.md:187`) asks for a producing command **alongside future `no-harm-controls.json` booleans and structural tallies**.
- The control instead checks `bool(co) and 'argv' in co` on `.ufo/waves/round-16/controls.py` (`documentation-red.json`, `argv[3]`).
- `'argv' in co` passes for any Python file that touches `sys.argv`. It does not test that any recorded value carries its own command.

Criterion18's "producing-command provenance" must be anchored to the value records (`.ufo/waves/round-15/no-harm-controls.json`, which currently has no per-field command), not to a helper's source text.

### F3 — High (calibration/duplication): the producing-command rule already exists

- `corpus/QUALITY.md:16` (#6): claims cite "the exact reproducing call (tool name, target SHA-256, detail level, filters)".
- `corpus/QUALITY.md:23` (#13): "the recorded verify command must itself reproduce".
- `corpus/CORPUS.md:34`: "**A count carries its command.** Any number in a corpus entry … is written as `<number> — <command> <date>`."

A new #18 that restates "producing command for counts/controls" is a second row for an obligation already held by #6, #13, and CORPUS:34. The QUALITY convention for refinement is `sharpens N` (`corpus/QUALITY.md:20`, #10 "sharpens 8"). If #18 exists at all for this point, it must be `sharpens 6, 13` and must add only what is new (retained for future value records). Otherwise drop it.

### F4 — Medium (citation integrity): the "round16 lesson" does not exist

- `corpus/lessons/` ends at `round-15.md` and `round-15-verifier-spotcheck.md`. No `round-16` lesson file exists, and `.ufo/waves/round-16/` has no lesson.
- The QUALITY header requires every criterion to cite the lesson that produced it (`corpus/QUALITY.md:4`), and #1 requires a resolvable source.
- A row citing an uncreated round-16 lesson is a dangling citation at draft time. `corpus/lessons/round-15.md:67` records the same failure class ("registry used-by was extended before new targets were created"; fix "Future ordering must create targets first").

Fix: cite the outside route directly, `corpus/lessons/round-15-verifier-spotcheck.md:181-188`, and `corpus/lessons/round-15.md:65-67` for the existing Mistakes rows. Cite a round-16 lesson only if it is created in the same integration, before the row is committed.

### F5 — Medium (scope): registry discoverability is not an REA admission criterion

- `corpus/QUALITY.md` header scopes the bar to "reverse engineering of shipped artifacts with REA"; #3 requires "Domain-specific".
- Routed defect 2 (`round-15-verifier-spotcheck.md:186`) is a SKILL registry-row content fix: add `.ufo/waves/round-15/boundary-fixtures/expected.json` to the `quote-fidelity` row. The row is `SKILL.md:450`; its pinned-values cell currently names only `.ufo/waves/round-14/fixtures/expected.json`.
- Making a registry-row completeness rule a QUALITY criterion turns a documentation index into admission law. The closure said "No new gate or classifier is required" for this item.

Fix: correct `SKILL.md:450` as a named edit. Keep #18, if any, limited to claim-level provenance.

### F6 — Medium (outside-route coverage): the same argv defect also sits in an unrouted registry row

- Routed defect 1 (`round-15-verifier-spotcheck.md:185`) names only the knowledge entry `recheck:` line (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3`).
- `SKILL.md:487` (`go-snapshot-inventory` row, "Entry / status map" column) carries the same omission: `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra …`, with no `-I` and a relative path.
- The repository's own quote-fidelity registry row (`SKILL.md:450`) does use `python3 -I`, so the two rows are inconsistent with each other.

A criterion or measure that cites only the knowledge line discharges half of defect 1. Scope #18 (or its control) to both `knowledge:3` and `SKILL.md:487`.

### F7 — Medium (over-constraint versus route): "-I and absolute script" exceeds the routed options

- The route allows either (a) align future recheck guidance with the exercised isolation flag, or (b) "explicitly distinguish intended recheck from recorded argv" (`round-15-verifier-spotcheck.md:185`).
- The spec's measure/control requirement "named r15 correction using -I and absolute script" forces option (a) and adds an absolute-path requirement that the route does not contain.
- Repository convention is relative paths: `SKILL.md:450`, `SKILL.md:487`, and `knowledge:3` all use `.ufo/waves/…`. Only the executed argv (`knowledge:83`, `verification.json` argv) is absolute.

Fix: a method-neutral rule — "guidance either equals the recorded argv, or states the difference; recorded argv is reproduced verbatim". Do not mandate absolute paths.

### F8 — Medium (second research method / #17 conflict): argv and count evidence must not route through the quote gate

- QUALITY #16/#17 exclude "command output" and JSON from machine-gradeable quote input and mandate manual source checks under #1 (`corpus/QUALITY.md:26-27`).
- A #18 that says recorded argv or command output is "checked by quote-fidelity" contradicts #17 and creates a second verification path.
- `corpus/lessons/round-15-verifier-spotcheck.md` and `.ufo/waves/round-15/w1/SiblingBoundary.md:20,110-112` already bar absorbing chousa-shokunin's admission method, and bar any new quote-gate feature. A criterion must not introduce a new admission method, gate, or classifier. "No second research method" is violated by any wording that makes `controls.py`, `measure.py`, or a new checker the admission route.
- `controls.py` (round-16 spec task) is an authored measurement helper, not a registered gate. It must not be cited as a claim-admission instrument.

Fix: keep #18 method-neutral. Name only registered instruments (`quote-fidelity` for raw prose, `sources-census.sh` for SOURCES, the exact-argv recording rule) and state that no new classifier or gate is added.

### F9 — Medium (retroactivity / append-only): the row must not reach back into round-15 records

- The routed defects are explicitly "status-neutral… not reasons to rerun or reject the declared claims" (`round-15-verifier-spotcheck.md:181-183`).
- `corpus/QUALITY.md` header: "A criterion is replaced by a new row … never rewritten"; criteria apply forward (#16/#17 scope to "New" quotations).
- The round-15 lesson and knowledge entry are append-only per the closure (`corpus/lessons/round-15.md:150-151`: "Prior lesson/entry and LOG edits are append-only"). C2 in `.ufo/waves/round-16/claims.json` asks for a "named append-only correction", not an in-place edit of `knowledge:3`.

Fix: scope #18 to records created or updated after its commit. State explicitly that round-15 values without per-field commands are not invalid under #18.

### F10 — Low (coverage routing): the SHONEN item is not a criterion matter, and is partly already repaired

- Routed defect 4 (`round-15-verifier-spotcheck.md:188`) concerns SHONEN box 3 wording, not claim admission. It must not be folded into #18.
- Current working tree `SHONEN.md:10` reads "historical 2026-10-15 operator-steered round 1". `git show HEAD:SHONEN.md` line 10 still reads "this round executed". The repair is uncommitted; L1 must verify it at the integration revision.

### F11 — Low (control coverage): spec asks the red control to assert "retain red-before"; the control is baseline-only

- `documentation-red.json` runs at baseline `6235498…` only. That shows 0/4 resolved, which is the expected red. It does not show that any green state discriminates (see F1, F2).
- No "after" pass is claimed by this seat. Any statement that #18 is "discharged" must cite the after-revision run, not the red file.

## What is grounded (no defect)

- The three named obligations are real and traceable: routed defect 1 (`round-15-verifier-spotcheck.md:185`), defect 2 (`:186`), defect 3 (`:187`).
- The round-15 red-before evidence is retained in `.ufo/waves/round-15/verification-initial.json` and the lesson section "First execution failure retained". A #18 that cites it for execution-failure provenance is grounded.
- QUALITY #17 (`corpus/QUALITY.md:27`) is present and unchanged by this seat.

## Proposed-failure checks for the eventual candidate (to run at re-review)

1. Grep the candidate for `round-16.md`, `controls.py`, `measure.py`, `absolute`, `-I`, `quote-fidelity`. Each hit must be justified against F4, F7, F8.
2. Confirm the row text says `sharpens 6, 13` or explains why it is distinct from them (F3).
3. Confirm the row does not require any change to `knowledge:3`, `SKILL.md:450`, or `SKILL.md:487` (F5, F6, F9).
4. Confirm the red control references `no-harm-controls.json` value records, not `controls.py` text (F2).

## Residual risk and verification gaps

- No candidate text exists, so all findings are contract- and anchor-based. Several are `[INFERENCE]` about how a future draft would be written; they are labelled as such by their "Fix" framing.
- I did not verify the after-state of any control. The defects above are about discriminating power and scope, not about a claimed pass.
- Lesson-level outside-route grounding (`round-15-verifier-spotcheck.md:181-188`) was read, not re-derived. The independent recount in that file was not re-executed here (per assignment).

## Installs / updates

None.
