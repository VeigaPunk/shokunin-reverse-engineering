# Seat report — SC-1 (chain c1, role scribe)

Wave `arc3-loop1-round2` · 2026-10-19 · lane HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`
(`git rev-parse HEAD`; unchanged throughout — all measurements read Git objects at this rev or
scratch copies). Writes by this seat: this report + `claims/c1/records-drafts/{scorecard-section-draft.md,
log-entry-draft.md}` + the `claims/c1/SC-1/` evidence directory (tools + measured outputs).
No git mutation in the lane repo; no custody-path writes; no LOG/SCORECARD/SHONEN/corpus edits.
Scratch: `/dev/shm/sc1/` only (`/tmp` quota-exhausted standing hazard; one scratch git clone
`/dev/shm/sc1/simrepo` carries this seat's simulation commits — lane repo untouched).

## 1. Work performed

- **Before-state capture** (all re-derived by this seat, not copied):
  `git rev-parse HEAD` → `14b1682b…`; command A at HEAD → 82/82 files, **13/13** rules,
  10.0/10.0, missing/dangling empty (`claims/c1/SC-1/command-A-before.txt`, sha256
  `d620c845…`); 13-block craft-section per-block sha256 baseline
  (`claims/c1/SC-1/craft-baseline-HEAD.json`, sha256 `05a85608…`, 161-line section) via
  `claims/c1/SC-1/craft-rules-baseline.py` (this seat's tool; `--compare` mode re-checks
  prior-block identity after a landing).
- **Records drafts** (the seat's deliverable, parent-facing, not applied):
  - `claims/c1/records-drafts/log-entry-draft.md` — LOG.md entry, C1 bullet drafted complete;
    C2/C3 as parent-merge slots; five sections per the required seat-report form's record shape.
  - `claims/c1/records-drafts/scorecard-section-draft.md` — SCORECARD.md round section, C1
    bullet + axis row complete; C2/C3 slots; pin-free (below).
  Both follow the arc3-loop1-round1 section's form (intro → wave → per-claim bullets → measured-at
  → axis table → learning trends/planned/carried debt) and the round-1 connector's pin-free
  discipline for the appended region.
- **Independent rehearsal of the chain's target text** (scratch clone, clean pre-image
  `483b0eba…`/371 lines): extracted the payload from `claims/c1/EX-01/rule14.patch.md` between its
  markers, re-hashed it (v1: 896 B `a47dc38d…`; v2: 1,071 B `6cc388cb…`), applied it via the
  artifact's anchor recipe, re-hashed the patched `SKILL.md` (v1: 385 L `19057c13…`; v2: 387 L
  `a8170b96…`), committed in the scratch clone (`396fc95a…` v1, `2e5df8b6…` v2), and ran the
  battery below. Also applied the executor's same-commit SHONEN refresh (v2 form: range end 254,
  "rules #11-14 … + arc3 round 2", 14/14) in the same scratch clone.
- **Instrument-movement tracking** (recorded, not absorbed): the worktree census was mid-rewrite
  during the round — observed revisions include the landed `82fb807e…`, plus `df9ffdf9…`,
  `a4c16763…`, `d0772ce8…` (EX-05/PL-1) and `c95a5cf3…` (this seat's capture). One revision's
  per-file floor reads `BLIND-INSTRUMENT` FAIL with `SKILL.md=0` **even on a pristine HEAD
  projection**, identical with and without the C1 artifacts → the C1 append is verdict-neutral;
  every census reading in the records must carry the instrument's sha256 at read time.
- **Polling**: re-listed `seats/` and `claims/c1/` on a ~60 s cadence through the round; at close
  **61/64 seat reports on disk** — missing: VZ-1 (c1 verifier), VZ-2 (c2), VZ-4 (cross); SC-1 =
  this report. Cross-seat
  evidence read and folded: EX-01 (patch + seat), EX-02 (prereg), EX-03 (attacks + scope census +
  blindness control), EX-04 (t-series geometry), EX-05 (census interplay + identity recheck),
  EX-06 (probe interplay), PL-1 (plan + merged variant), RV-1 (v2 review + prior-13 finding),
  RV-2 (audit tool + citation-form patch + candidate verdicts), CR-1 (candidates, replay,
  citation fix + insertion constraint).

## 2. Proposed changes

- No change applied by this seat. Deliverables are draft text only:
  `claims/c1/records-drafts/scorecard-section-draft.md` (sha256 `0ef9b975…`) and
  `claims/c1/records-drafts/log-entry-draft.md` (sha256 `75a50e0d…`) — both re-derived at close
  after the final write (this seat's own artifacts under the rule the round lands; the tool is
  `claims/c1/SC-1/craft-rules-baseline.py`, sha256 `37104d18…`). Both drafts carry `⟨FILL: …⟩` slots
  for values only the parent can produce (landed payload choice, records-commit re-measurements,
  delivery count, C2/C3 merges, reviewer/verifier verdicts).
- Landing-facing patch texts proposed by other C1 seats (named for the integrator, not written by
  this seat): `claims/c1/EX-01/rule14.patch.md` (executor payload v2, 1,071 B `6cc388cb…`);
  `claims/c1/PL-1/merged-rule-14.patch.md` (merged variant, block `5a235f18…`, 392-line patched
  SKILL, refresh end 259); `claims/c1/CR-1/rule14-citation-fix.patch.md` (fallback wording +
  byte-preserving insert constraint); `claims/c1/RV-2/proposed-rule14-citation-form.patch.md`
  (section-key citation fix) and `claims/c1/RV-2/proposed-pl1-verdict-path.patch.md`.
- C1's same-commit obligations (as measured, to ride the parent's landing commit): land one payload
  + the SHONEN range/count refresh (range end = the landed payload's last rule line: 254 executor
  text, 259 merged variant); re-run command A (expect 14/14) and the census (instrument sha at
  read time); re-derive and record the fresh `SKILL.md` identity; no pointer-table/census-scope
  widening.

## 3. Before → after measurement (chain claim: rules 13 → 14, 14/14 resolved, prior 13 intact)

Commands + outputs (all by this seat; outputs verbatim):

- **Before** (lane HEAD `14b1682b`, recipe A verbatim): `{"citation_resolved_rules": 13,
  "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82,
  "mapped": 82, "missing": [], "rule_blocks": 13}` — `claims/c1/SC-1/command-A-before.txt`.
- **After — rehearsal on the clean scratch pre-image** (executor v2 payload):
  - payload re-hash: 1,071 B / `6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f`
    (declared == derived); patched `SKILL.md` 387 lines /
    `a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28` (declared == derived);
    lines 1-239 byte-identical (`cmp`-equivalent prefix check in-memory: True).
  - command A at the scratch commit `2e5df8b6…`: `{"citation_resolved_rules": 14,
    "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82,
    "mapped": 82, "missing": [], "rule_blocks": 14}` — **13/13 → 14/14, no other counter moved**.
  - prior-block identity (`craft-rules-baseline.py --compare`): `rule_count 14`,
    `baseline_rule_count 13`, `prior_blocks_byte_identical: True`, `appended_blocks 1`.
  - citation-drift probe on the patched tree: `reported findings=0 exit=0` and
    `clean findings=0 exit=0` (strict); with the SHONEN refresh applied in the same scratch
    commit: still 0 in both modes (pre-refresh control also 0 — the needle stays inside the
    stated range).
  - census (committed instrument `6f1d19ff…`, extracted from HEAD): `VERDICT: PASS
    (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, `SKILL.md lines=387 loci=2`; pristine
    baseline 371/loci 2 — line counters move, loci hold.
  - RV-2's citation-audit tool (as landed) on the patched tree: 60 cites, 59 resolved (1
    external-custody stat-only by design), 0 dead, 2 form flags (1 pre-existing on the
    custody-pair rule, 1 on the new rule's round-1 records reference).
- **v1 rehearsal** (superseded text, kept as history): payload 896 B `a47dc38d…`, patched 385 L
  `19057c13…`, command A 14/14, probe 0/0, census PASS `SKILL.md 385/loci 2` (scratch commit
  `396fc95a…`).
- **Draft sections as injection vectors** (the round-1 connector's test, re-run): needle scan of
  both drafts over the census's four needle classes → **0 hits**; the filled SCORECARD section
  appended to a HEAD copy → census `PASS 0/0/0/0`, `SCORECARD.md lines 1417 → 1531, loci 9
  unchanged` (`claims/c1/SC-1/census-v10-projection-final.txt`); planted-pin control in the same
  region → `FAIL undeclared=1` (`census-projection-control.txt`) — the detector is live.
- **Measurement boundary (named)**: the after-state above is a rehearsal on a scratch clone; the
  work-commit run (`command A` at the real commit, 14/14) and the landed identities remain
  parent-side, and the drafts' slots say so.

## 4. Attacks / refutations attempted (with verdicts)

1. **Copy-vs-recompute on the payload and patched file** — re-hashed both generations from the
   artifact bytes; declared identities matched (v1, v2). One transient: a mid-write read of
   `rule14.patch.md` during EX-01's v1→v2 revision produced an inconsistent byte count for a
   moment — re-derived after the writers settled; recorded as the mid-write observation class,
   not a defect. Verdict: identities hold.
2. **Byte-identity of the prior 13 rules, strictest reading** — raw segment equality including the
   boundary blank structure is form-sensitive (±1 newline; the critic measured −1 for the live
   insert, an earlier harness +1; RV-1's checker prints `False` on its own normalization). Under
   trailing-newline-normalized block digests it is 13/13 identical, and the 239 text lines are
   byte-identical in every form. Verdict: "prior 13 byte-identical" is exact as *pure insertion +
   normalized blocks*; the record must grade the normalization and prefer the byte-preserving
   insert form. (Also cost two seat-side stale claims: EX-01's own splitter printed a spurious
   `DIFF rule 13`.)
3. **Census FAIL attribution** — the `BLIND-INSTRUMENT` FAIL reproduces on a pristine HEAD
   projection with the same in-flight revision → not caused by the C1 append. Verdict: C1
   verdict-neutral; instrument sha must be pinned per reading; the records-commit quote must come
   from C2's settled landing.
4. **Probe staleness** — probe clean with and without the SHONEN refresh (the needle stays inside
   the stated range). Verdict: no staleness; the refresh is prose-correctness (range end + count),
   which the record must still carry as a same-commit obligation.
5. **SHONEN end values** — computed 254 for the executor v2 payload (rule spans 240-254, heading
   258); EX-01's refresh text agrees; EX-04's 249 belonged to a different (non-executor) variant;
   the merged variant measures 259. Verdict: end must equal the *landed* payload's last rule line.
6. **Citation-form flag on the new rule** — RV-2's audit flags the round-1 records reference for
   missing stanza-key/stamp form (same class pre-exists on the custody-pair rule). Verdict:
   recorded, not waived; RV-2's fix or the merged variant's section-key citations resolve it; if
   the bare range lands, the parent must name the ruling.
7. **Trigger inclusiveness (EX-03's attack, corroborated)** — the literal "its own byte-identity"
   trigger matches nothing in-repo (0 self-bound files; the origin incident is other-directed).
   Verdict: sustained in part — the record should state the subject as the identity a verification
   block declares about its subject; the landed/v2 family does bind the described bytes.
8. **Metric-vs-craft discrimination (CR-1/EX-02, reproduced by this seat's reading)** — a
   wave-tree-only honest rule text scores 13/14 (depth 9.29) and a decoration-only control scores
   14/14. Verdict: the count alone cannot carry the verdict; the live-catch measurement does.
9. **Drafts as census tripwires** — needle scan 0; projection PASS; planted control FAIL (item in
   §3). Verdict: pin-free discipline holds on the filled text.

## 5. Blockers

- **VZ-1's verdict had not landed at this seat's close** (59/64 reports at last poll; the C1
  chain's verifier report absent). The drafts carry `⟨FILL: reviewer/verifier final verdict⟩`
  slots rather than assuming it.
- **Payload choice is not this seat's** — two peer-measured candidates (executor v2, planner
  merged) plus a critic fallback are on record; the drafts name all and mark the landed one as a
  parent slot. Numbers (patched-file identity, SHONEN end, citation count) must be re-derived for
  whichever text lands; this seat's rehearsal covers the executor v2 precisely and the merged
  variant by its own seat's measurements only.
- **The census instrument is moving** (C2's EX-16 target, multiple uncommitted revisions this
  round) — the records-commit census reading must pin the instrument's sha256 at read time; no
  census claim in the drafts relies on a moving revision.
- The real-repo landing (SKILL.md + SHONEN.md + records) is parent-side by the wave rules;
  the after-state here is a rehearsal, and the seat report's before→after says so explicitly.
