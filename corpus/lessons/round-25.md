# Round 25 — explicit instrument-reference custody, prospective phase

Author: KaidokuR25AuthorS3, scoped worktree author; Main alone integrates,
publishes and decides admission. Baseline B is
`18e7eb6d9fe8842678af5f1cffbd680ead4ad473`. Parent actually landed and pushed
the four prerequisite files at I=`62feef9c0cbd5aadafa453456c55c28832175206`.
The author worktree remains on B; its HEAD is not a candidate or landed result.

## Declared proposal and dependencies

One proposed claim, R25-C1 on calibration (tied-lowest finite proxy 10;
coverage and depth also 10): acquire a **finite explicit-reference custody
CLI**, with every one of the 34 literal exit/primary-finding pairs in
`corpus/evidence/round-25/oracle/cases.json` retained. This is not an
R14–R24 cohort re-audit, arbitrary-shell parser, historical admission rule,
or repair of the old frozen calibration result. Main has not yet approved
or landed the round-25 claims SRT or a candidate implementation.

Fixed measurement authority: `tools/round-25/ruler.py`, sha256
`20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532`.
Fixed cases sha256
`6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0`;
contract `069f9119e7c81512f601e1ece804d4ca393d3c8f6f533a90525ceb95fb5b6824`;
derivation `59269265f74d272fa51d6da81cf2ca4d47afa0a7b53a92638a79c5e65587d683`.
These are the four files at I, not moving draft authorities.

The ruler **executes only the selected candidate CLI**, never the audited
instruments, carriers or fixture code. Its subject is
`tools/round-25/instrument-custody.py`, which does not yet exist. The candidate
must be implemented only after Main's actual claims landing and permission.
The author has executed no ruler, candidate, gate, fixture, test, build,
linter or formatter. Parent owns actual CLI measurements.

Absent candidate means unavailable, all cases `not_observed`, executed 0;
it is not 34 empirically observed old failures. A green producer would
establish only the named finite pairs, not outside admission or universal
conformance. Inputs are known historical Git facts plus explicit local
policy, not a blinded prediction experiment. The same author proposing
future code is not an independent outside verifier.

## Gate

Public sources opened on 2026-10-21. Each quoted passage is contiguous,
manually checked at the named rendered location, and at most 25 words.

| Item | Decision | Located source quotation and limit |
|---|---|---|
| S073, official Git manuals | Admit, docs/A scoped to CLI semantics | https://git-scm.com/docs/git-merge-base, OPERATION MODES `--is-ancestor`, page last updated 2.43.0: “Check if the first <commit> is an ancestor of the second <commit>”. https://git-scm.com/docs/git-cat-file, DESCRIPTION, page last updated 2.56.0: “Output the contents or other properties such as size, type or delta information of one or more objects.” These describe directional reachability and object inspection, not an authenticated execution or our implementation's correctness. |
| S068, Nosek et al.2018 | Reopened; reject as sole Git-custody semantics support, retain original row | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/, Abstract: “define the research questions and analysis plan before observing the research outcomes”. It supports plan/deviation transparency, not Git semantics, old-oracle substitution or audit accuracy. Flip: a claim limited to that planning distinction. |
| S049, RFC8259 | Reopened, reused; no new row | https://www.rfc-editor.org/rfc/rfc8259, section4 Objects: “The names within an object SHOULD be unique.” Rejecting duplicate request members is our declared application policy, not an RFC assertion that duplicate-name JSON is syntactically invalid. |

Existing registry rows, including S068/S049, are unchanged. S073 is a new
row whose used-by names this lesson. No old status/recheck/used-by cell is
changed. The search log counts three opened source families (Git manuals,
PNAS paper, RFC), one new row and two reused families; it is not a corpus-row
quota. Main's outside admit/reject spot-check is not yet recorded.

The actual initial root-owned source census was run before source edits
against unchanged canonical main=B and returned exit0, five W04 warnings
(S033/S047/S054/S062/S069), then the kaidoku `ok` line. Private producing
transcription is `/fast/scratch/hyaku/kaidoku-r25-author-handoff/initial-census.json`; it is
explicitly a whitespace-normalized transcription, not raw producer bytes.
The final census must be run after Main's candidate landing and bound to
that canonical revision, not to unchanged B while this worktree differs.

## Mistakes

| id | class | evidence pointer | captured-by | prospective fix and failure obligation |
|---|---|---|---|---|
| M25-1 | disclosure agreement mistaken for validated instrument custody | B:`.ufo/waves/round-24/tools/freeze-gate.py:89-113`; B:`corpus/lessons/round-24-verifier-spotcheck.md:19-24,45,55` | none in the retained detector: reason-bearing path/commit pairs are accepted without checking the supplied supersession digest | The new explicit-request contract must distinguish the genuine R24 supersession from the otherwise-identical wrong-digest or wrong-path entry, using the frozen cases. The fix is **not yet counted as working**; Main's actual frozen candidate CLI must produce the declared non-clean results. |
| M25-2 | noncommittable draft paths | Author's earlier unlanded R25 `.ufo` drafts; Main's helper contract `.ufo` ban and path-correction steer | Parent review before any prerequisite/SRT landing | Four prerequisite files were moved prospectively to durable tools/corpus evidence paths and actually landed at I. No draft is called a freeze, no force-add or guard bypass, no historical file changed. |
| M25-3 | input-epoch breach | Original proposal seat Kd25P55 disclosed reading the untracked WT ruler draft6207B once | Read-only immutable-BASE instruction, instructed not enforced | Preserve the breach as unqualified read-only input, not execution; do not use it as independent oracle authority, retro-authorize it or replace the seat. Private wave settlement also flags P18's forbidden scratch report and P17/P52's private-draft discussions. No expectation is retrospectively fitted to these reports. |
| M25-4 | overstrict optional preservation probe | Unlanded optional preservation.py draft, sha2563a148abd07904f064619b9d98f57419f13d2ad1908406507c6b7d3f32ed0db45; Main's concrete prerequisite review | Parent static review, before SRT or result | Removed from the prospective bundle, exact draft retained privately. No C1 target/case or full no-harm duty removed. Main independently reviews explicit allowed diffs, all prior blob/mode/source/index constraints and append-only history. This is a pre-freeze design rejection, not post-result scope reduction. |

## Custody, conduct and limits

The original proposal wave was validated as one 64-seat policy-v2 batch,
then actually spawned once under the capacity guard. All 64 original jobs
reached terminal completed, zero terminal failures/replacements; the last
sole-running P28's completion settled the barrier. This is not inferred
from report-file counts and does not mean every seat is qualified. Private
`wave1-settlement.json` pins each actual ID/report and qualification notes.
Canonical planner seat is held by this scoped author; P54 supplies a bounded
advisory data walk, and P52/P53/P60 are connector seats. None is Main or a
non-author admission verifier. A distinct ordinary distiller request was
capacity-refused with zero spawned; no replacement or reroute is credited.

QUALITY33 and its old detector/ledger remain byte-immutable. The new SRT
must name fixed authority and post-freeze candidate subject openly. Treating
all executed candidate code as a prerequisite counting instrument creates
literal cyclic conformance debt under the production-after-freeze order;
**that debt remains unmet, not solved by a role label**. The R24 detector
only discovers `.ufo/waves/round-N/claims.json`, not durable
`reports/round-25/claims.json`: R25 is **undetected**, never CLEAN under it.
The new ruler exposes no separate self-invocation mode; no conformant-gate
selftest certificate or self-custody CLEAN is claimed.

Root lstat/index/ref/status snapshots attest named instants only. They do
not establish continuous immutability, all-content equality, object-store
immutability, universal filesystem safety or enforcement. Changed state
or an unsettled execution stops the ruler at exit2 with partial receipts;
there is no restoration, retry or fabricated failed case. The caller must
actually own fast scratch outside the measured tree; the prefix test is
only a heuristic.

Original R24 frozen9/11 exit1 stays unmet. Revised11/11 remains disclosed
agreement, never rescue. R23's six-verb4/6 is distinct from R24's four-verb4/4.
No held ELF metadata item/question/fallback is resumed, no packet secret
body is opened, and no live network/device/chain/debugger action occurs.
No tool installation, host/config/service change, promotion, mastery,
capability-table admission or axis-score increase is claimed at this phase.

## Actual Parent prerequisite measurements

Main executed the committed I ruler on 2026-10-22 UTC, with measured
revision B and oracle revision I. Exact receipts are retained byte-for-byte
at `corpus/evidence/round-25/prerequisite/parent-before-process.json`,
`parent-tamper-process.json` and `parent-proof.json`. Before: exit2,
`candidate_unavailable`, total34, executed0, exact0, all34 `not_observed`,
candidate SHA null. A separate wrong-oracle-SHA invocation exited2 with
`could_not_evaluate` / `snapshot_tampered:oracle`. These are actual Main CLI
observations, not author executions, 34 old failures, an after result or
claim approval.

The initial census transcription is now also retained at
`corpus/evidence/round-25/initial-census-transcription.json`; its normalized
transcription limitation is unchanged. The complete prospective SRT draft
is `reports/round-25/claims.json`. Ordinary distillation and Main's actual
SRT landing remain prerequisites to implementation.


## Prospective path erratum before claims freeze

Main corrected the earlier categorical `.ufo/**` landing-ban premise in
M25-2 and the custody discussion: the actual helper rejects bare `.ufo`
and runtime state, not every exactly named descendant artifact file.
No helper, config or source policy changed. The author's exact
`git check-ignore --no-index --verbose --non-matching --
.ufo/waves/round-25/claims.json` returned exit1/unmatched `::`, so that
future path is not ignored. No force-add or whole-directory tracking is
proposed.

Before any SRT landing, the selected future claims path is prospectively
`.ufo/waves/round-25/claims.json`, not the reports-path draft mentioned
above. The latter remains unlanded/unapproved, never authority; the earlier
private v1/v2 handoff history is retained. No claims side effect occurs
while ordinary distillation and Parent approval are pending. I and all34
oracle wants remain fixed.

This avoids an unnecessary planned reports-path discovery mismatch. It
does not clear QUALITY33's literal cyclic subject/instrument debt or imply
an actual old-detector CLEAN, and no old R24 matrix is rerun. This correction
is prospective and explicit, not a post-result target/oracle change.


## Actual ordinary seats and planner-attribution correction

Supersedes the earlier scoped-author-holds-canonical-planner wording:
the scoped author is not another L1/judge. Main alone retains planning,
judgment and integration authority. P54's actual role is reviewer, with a
bounded advisory planning data walk; it is never relabelled a native
planner.

After the zero-spawn capacity refusal and Parent's second priority callback,
the exact unchanged logical distiller request first actually admitted as
`KaidokuR25AuthorS3.Kd25Distill-2`. The suffix is transport naming after the
refusal, not a replacement. Main then required a distinct actual native
planner and scheduled it as the fourth owed ordinary seat. It first
actually admitted as `KaidokuR25AuthorS3.Kd25Planner`, **after** the original64
proposal terminal barrier, not before that wave. The missing pre-wave
native-planner chronology is retained, never retroactively repaired by
calling P54 or Main an actual spawned seat.

Actual spent is now66: original64, distinct distiller1, native planner1.
Both ordinary seats are readonly advisory and still awaiting their terminal
results at this entry. Native role routing is global, not overridden.
`corpus/evidence/round-25/proposal/{actual-seat-budget,distiller-admission,planner-admission}.json`
retains IDs, refusal accounting, chronology and role split. No new64 wave,
candidate implementation, admission or SRT landing is claimed.


### Proposal executor-floor debt retained

Main explicitly adjudicated the rendered three-executor proposal minimum:
W1 actual executor0 versus required3 is **UNMET**. Readonly proposal bounds
do not invent executor credit. No padding, retrospective relabelling or later
genuine implementation/probe seat repairs W1 chronology. The actual budget
and qualifications remain recorded; no full role-conformance claim follows
from64 reports or a later finite CLI result.


## Completed advisory barrier and pre-SRT adjudications

The actual distiller `KaidokuR25AuthorS3.Kd25Distill-2` and actual native
planner `KaidokuR25AuthorS3.Kd25Planner` are now terminal completed.
Actual total66 is unchanged, not inferred from file presence. Their original
reports are retained at `corpus/evidence/round-25/proposal/distillation.md`
and `planner-advisory.md`. The full distillation is54,497 bytes, sha256
`a4390dc1a649271ee83a7f5241e99849c659468ea04b7b640087431255756897`;
it is not rewritten to remove contradictions. Diagnostic facets proposed
by the planner are not new owned axes, claims or a UFO plan/schema.

Advisory alternatives were distilled, not silently admitted. The selected
prospective C1 remains the fixed I explicit-request contract and all34 wants:
unsupported forms exit2, bare names never guessed, supported exact missing
paths exit1, original freeze/pin and actual supersession post-images checked.
Whole-cohort discovery, claim-text immutability, alternate labels/oracles,
basename resolution and old9/11 rescue remain rejected or future scope,
not extra acceptance smuggled into this round.

The distiller observed63/64 settlement report pins matching and one P55
post-barrier mismatch: expected
`1582406dc5f984eeb19bc0cee93166b37ebe9b7cdd16060c937f2732434d606d`,
current observed
`1df3c360f5a1fe6b7e238bc0b4d79a6b71dcf553d681192fce7a7127621c38bb`.
The expected pin is not reissued, current bytes are not called the original,
and no complete raw-byte custody or qualification certificate is claimed.
P55 remains unqualified for WT/draft alignment as well. P17/P52/P33's draft
epochs are not independent corroboration of I. P18's native scratch-cleanup
disclosure is not exonerated by its pinned report's omission; P17/P25 have
additional outside-scratch metadata. Full extent remains limited to the
available metadata; no source execution, cleanup, reproduction, leaf wake
or replacement is inferred or performed.
`corpus/evidence/round-25/proposal/qualification-erratum.json` retains these observations separately
from the unchanged initial settlement and distillation.

S073 was contested only between readonly proposals, not duplicated in the
actual registry. Main accepted keeping the one author-proposed Git
merge-base/cat-file row matching I's authorities. No old row is renumbered,
aliased or overwritten; I and the34 oracle wants remain unchanged.

The obsolete unlanded reports-path SRT draft was cut over **path-only**
to the exact `.ufo/waves/round-25/claims.json` (WITH dash) for Parent review;
this is not an actual Main freeze. Old phase references above are history,
not live aliases. Only after an actual F could the retained detector observe
a twelfth freeze. Main explicitly authorizes a prospective **truthful R25
FLAGGED append only after actual F and full measured Git findings are known**:
preserve the existing ledger header and all11 old rows byte-for-byte,
report all supported absent/unpinned/revised findings with as-of F/measured
identities, and fabricate no anticipated row or CLEAN. No row is written now.
Any eventual current-gate exit0 means disclosure agreement only, not12 clean
rounds; require-clean R25 remains red. Literal cyclic debt is not waived.
Main alone may approve, actually land the SRT, and permit implementation.


## Pre-F v2 — outside-critic corrections, not a changed34 oracle

Main held first-add F after bounded outside review. The exact frozen v1
23-file packet and hash manifest are preserved privately under
`/fast/scratch/hyaku/kaidoku-r25-author-handoff/frozen-prereg-v1/`.
No candidate, gate, fixture or source executable was run by this author.
I's four blobs and all34 literal requests/expected pairs remain unchanged.

### Distiller scratch/provenance qualifier

Main's outside critic reported that native transcript
`history://KaidokuR25AuthorS3.Kd25Distill-2:58-63` shows `pickle.dump`
writing `/tmp/kd25_digest.pkl`. The unchanged original distillation's
line237 sole-file statement is therefore false. The report is an
**unqualified scratch/provenance advisory source**, not a blanket-clean
cluster, independent oracle, role/custody certificate or admission.
Its original54,497 bytes/hash remain untouched; qualifications are recorded
separately in the erratum, claims and actual-seat budget.

The pickle file has not been opened, unpickled, read, reproduced or deleted
by this author and must not be. This is metadata/history attribution only;
no leaf wake, replacement distiller or source re-execution is authorized.
P55's old/current pin mismatch and all earlier scratch/epoch/role debts
remain, not replaced by this additional defect.

### Full contract and non-tautology failure rule

Correct34 exit/finding pairs are the original finite score, **not enough
to verify C1**. Unique-first-add identity, freeze ancestry and supersession
at-or-before measured, the same regular parent blob **and mode**, nonregular
and re-added-history handling, duplicate/unknown member rejection, direct
candidate Git-environment isolation, and required scope/useful output
evidence remain load-bearing even where34 does not exercise them.
They are not moved into `not_claimed`.

Separate prospective Main-held controls H01–H16 and variants are declared
before any candidate output in
`corpus/evidence/round-25/main-held-contract-controls.json`, with inert
derivation in `control-git-facts.json`. They include actual later-touch
commit69e82c48 versus first-add5dc49bfe, real nonancestor/future objects,
a real modified-in-freeze blob, and fully declared Main-owned isolated
history recipes for mode-only/nonregular/re-added/unique-parent/replacement
conditions. Exact-member, malformed claims-path, complete otherwise-valid
raw duplicate request, direct environment and semantic output controls
are separate from34; no denominator is folded, narrowed or re-pinned.
No recipe is claimed materialized or executed by this author. Main must
retain actual bound full Git identities/inputs before its subject calls,
and cannot choose expected values from candidate output.

Even34/34 **fails C1** if the exact subject uses oracle/test descriptors,
contract/derivation/ruler/R24gate/helper/fixture content **as decision logic
or expected answers**, imports/executes/interprets their semantics, or embeds
case-keyed answer tables. Main explicitly clarified the purpose boundary:
an explicitly caller-selected grammar-valid instrument Git blob may be
read opaquely for raw identity/hash/mode/history, including a ruler/gate/
test-helper when selected. Its semantics are never imported, executed or
interpreted; claims/object reads serve the Git custody API only, not an
expectation lookup. Main reviews real Git dataflow/static implementation
and held consumer outcomes, not a brittle source-word/name/wiring test.

Shared worktrees/jj/ref/index writers must be quiesced by Main for final
measurement. Root pins are shared, non-atomic named-instant snapshots;
they are not continuous containment, global absence or all-content proof.
A root-guard/resource/setup abort is **CNE**, not a fabricated candidate
failure or success. Observed typed API exit2 test replies are distinct from
an aborted measurement. No guard weakening, automatic retry into a pass,
operator-state restoration or partial-receipt masking is permitted.

### Supplemental Gate — S074, primary primitives versus local policy

Five additional Git manual pages were individually opened on
2026-10-22 UTC. Each quote below is a contiguous located passage of at most
25 words; this is a manual source check, not a census certificate.

| Source/anchor | Located quote | Bounded support |
|---|---|---|
| https://git-scm.com/docs/git-log, 2.56.0, History Simplification, full-history without parent rewriting | “This mode differs from the default in one point: always follow all parents of a merge” | Traversal semantics; choosing a unique first-add and rejecting unsupported history is local API policy. |
| https://git-scm.com/docs/git-log, 2.56.0, `--diff-filter` | “Select only files that are Added” | The A-filter primitive; not proof that a naive date-ordered or single-path sweep handles every history. |
| https://git-scm.com/docs/git-ls-tree, 2.42.0, FIELD NAMES, objectmode/objecttype | “The mode of the object.” | Mode/type evidence fields; exact path and regular-entry acceptance must still be checked. |
| https://git-scm.com/docs/git-rev-list, 2.56.0, DESCRIPTION | “List commits that are reachable by following the `parent` links from the given commit(s)” | Reachability/range primitive, not timestamp authenticity or execution provenance. |
| https://git-scm.com/docs/git, 2.56.0, Environment Variables, GIT_WORK_TREE | “Set the path to the root of the working tree.” | Inherited Git variables can affect the selected view; isolation is an API obligation, not proven by a wrapper's normal run. |
| https://git-scm.com/docs/git, 2.56.0, GIT_NO_REPLACE_OBJECTS | “ignore replacement refs and do not replace Git objects.” | Replacement behavior; no claim of universal configuration/host containment. |
| https://git-scm.com/docs/git-fast-import, 2.56.0, filemodify modes | “A normal, but executable, file.” | The documented100755 mode class;100644 is non-executable normal file,120000 symlink,160000 gitlink,040000 directory. No fast-import command was executed. |

S073 remains limited to merge-base/cat-file primitives. S074 carries these
additional primitive authorities. Unique-first-add, equal unique-parent
blob/mode, regular-only conservative decisions, exact member set, scope
members and new error labels are explicitly prospective local policy,
not claims that the manuals mandate them. The source census does not
validate every associated/second URL or quotation; each was opened manually.
All pre-round registry rows remain unchanged.

### Actual tamper labels and landing/ledger boundaries

The actual wrong-oracle-SHA process receipt has
`finding=could_not_evaluate` and `error=snapshot_tampered:oracle`, exit2.
The unchanged Parent proof's summary key named `tampered_oracle_finding`
contains the error text; it is not the actual JSON finding. The raw process
receipt controls this statement; no old receipt is rewritten.

Main will copy the approved new/append packet into canonical at I, not
commit the author worktree. Actual first-add F must be the exact
`.ufo/waves/round-25/claims.json`, with unique parent I and I's four blobs
unchanged. No author HEAD/reset/rebase/raw-Git fix is needed.
After F the claims are immutable: no added supersession entry may launder
the subject's post-freeze absence/unpinned/revision debt. The one truthful
new R25 FLAGGED ledger row is computed only at the final post-candidate
measured commit, preserving the old header/all11 rows and every as-of F/M
finding. No12-CLEAN interpretation or original9/11 rescue is allowed.
There is still no F, candidate/code/runtime permission or admission.

