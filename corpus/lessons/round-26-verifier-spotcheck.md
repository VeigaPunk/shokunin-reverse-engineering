# Round 26 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-22. Lane-round kaidoku r26, attempt 1. Base `a0639d8e61e486e2a716ff94cddd89a73200a02c`;
lane tip judged `ae8bcd860e2ee0e187f66bd2f047cc40b905ede1`. Report `.ufo/reports/round-26/kaidoku.md`
(fleet commit `252f3b4ed8e9ea906529972b5b78478e19ae0859`). Runtime model exposed to this closure:
`anthropic/claude-opus-5-5` (session workstation context). This closure did not author any part of
the round. It dispatched two read-only reviewer seats (C2 re-derivation; conformance, round shape
and harm sweep) and ran every other check itself. Only committed bytes were judged, plus live
re-opening of the two new sources.

## Decision

**Admitted.** R26-C1 (depth) and R26-C2 (calibration) both reach their frozen after-values on
committed bytes, re-derived by plain commands below without running either lane instrument. No
owned axis is harmed. Status `ok`.

## Driver digest (copied from `.ufo/watchdog.log`)

```
2026-10-22T08:54:45-03:00 launch kaidoku round=26 pgid=1976991 driver=hyaku-inline attempt=1
2026-10-22T10:51:57-03:00 complete kaidoku round=26; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -- .ufo/reports/round-26/kaidoku.md` | one commit, `kaidoku-shokunin <kaidoku@shokunin.local> 252f3b4e…` at 10:51:23-03:00 | pass |
| Report lands after its commit | `git show -s` on fleet `252f3b4e` and lane `ae8bcd86` | lane tip committed 10:51:14-03:00, report 9 s later; report cites the full hash `ae8bcd86…` | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]` with pointers | pass |
| Cited lane commits exist and are ancestors of `main` | `git cat-file -e <h>^{commit}` and `git merge-base --is-ancestor <h> main` for the 11 commits in the Landed table plus the base | all exist, all ancestors; `git log a0639d8e..ae8bcd86` has exactly those 11 commits | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain`; `git ls-remote origin refs/heads/main` | `local=remote=ae8bcd86… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `ae8bcd86…` | pass |
| Prompt carries the template contract | `.ufo/prompts/kaidoku-round-26.md` (committed, `4037433d`) against `templates/round-prompt.md` and `scripts/hyaku/lane-addendum.md` §6 | MISSION/AXES binding, L2 minimum, commit-then-push, push scope, L0 channel; report path, report-lands-last, SHONEN heading, hash citation rule, write scope; addendum §6 present (reviewer seat) | pass |
| Misroot sweep | fleet paths `.ufo/waves/round-26/w2/CustodyNoteReview.md`, `kaidoku-r26/seats/EntryCorrection/final-report.md`; `git cat-file -e ae8bcd86:<path>` | both absent at the fleet root, both present in the lane | pass |
| Not a marker | report names real committed work | yes | status `ok` |

Conformance defects (status-neutral): none found. Note: jj sets each commit's author date to the
time its change was created, so `c27f445e` shows author 08:53:49-03:00, before the launch line; its
committer time 09:01:20-03:00 (12:01:20Z) is the freeze time the report gives. Not a defect.

Round shape (reviewer seat, from `w1-spec.json`, `w2-spec.json`, both `swarm-registry.json` and the
committed seat reports at `ae8bcd86`): wave 1 has 33 items (executor 7, scribe 7, reviewer 7, scout 5,
critic 3, mutation-tester 2, connector 1, sentinel 1); wave 2 has 32 (reviewer 20, mutation-tester 7,
critic 5). Total 65 seats, attack roles 12 + 32 = 44 (67.7%). Spec item names and committed `.md`
reports match one to one in both waves (`comm -3` empty), so no dead seat. Eight sampled items each
name a claim or check target and a concrete surface.

## Freeze ledger entry (`corpus/claim-freezes.tsv`, row `round-26`, FLAGGED INSTRUMENT_ABSENT)

| Fact | Command | Observed |
|---|---|---|
| Counting rules and targets frozen first | `git log --format=%h a0639d8e..ae8bcd86 -- .ufo/waves/round-26/claims.json`; `git diff c27f445e ae8bcd86 -- <same>` | only `c27f445e` (committer 12:01:20Z) touches it; 0 diff lines after the freeze |
| Pre-freeze REA call disclosed | `claims.json` `.pre_freeze_probe` | one `inspect-binary-layout` call at 11:59:16Z, envelope sha256 `68968086…195a`; none of the 24 committed envelopes has that sha256 (24 distinct) |
| Table runs after the freeze | `runs.tsv` `utc_start` | 12:11:50Z to 12:15:45Z |
| C2 instrument before any repair | committer times | `81f63f36` 12:31:00Z, repair `46ebfd2f` 12:48:48Z |
| C1 instrument after its data | committer times; `git show --stat bd0c84bc` | C1 data `ebe2cb4a` 12:47:57Z; instrument and its after receipt land together in `bd0c84bc` 12:49:24Z |
| Instruments never revised | `git log a0639d8e..ae8bcd86 -- tools/round-26/<file>`; `sha256sum` at tip | one commit each; `11c27422…18fa` (C1), `3b0f6507…7e8e` (C2), equal to the report |
| Self-tests (committed evidence) | `before/c1-selftest.txt` (`-> PASS` lines); `before/c2-selftest.txt` `.failures`, `.detail` | C1 16 of 16 PASS; C2 18 cases, 0 failures |

The row is accurate. `claims.json` `freeze_kind` also says the instruments are "committed and
sha256-pinned before any after-measurement"; for C1 that did not happen (instrument and after
receipt in the same commit, after the data). The FLAGGED row and SCORECARD say so. The verdicts
below do not rest on the C1 instrument: the closure re-derived both claims from the frozen rules.

No target was narrowed: the frozen targets (`rows_complete` 8 of 8, `entry_ok` 1, exit 0; C2 6 items,
0 mismatches, exit 0) are the after-values the report states, and `claims.json` did not change.

## Claims — re-measured by the closure

### R26-C1 depth — identity table rows complete 0 → 8 of 8, entry_ok 0 → 1

Before, at `a0639d8e`: `git ls-tree -r --name-only a0639d8e corpus/evidence/round-26 | wc -l` = 0;
`git show a0639d8e:corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` fails (not in
`a0639d8e`). So 0 of 8 rows and `entry_ok` 0.

After, at `ae8bcd86` (`git diff --quiet ebe2cb4a ae8bcd86 -- corpus/evidence/round-26/c1/` exit 0, so
the same bytes as the claimed after-commit). The closure applied the frozen `row_complete` and
`derived_verdict` rules in its own Python over `git show ae8bcd86:<path>` bytes:

| Check per envelope (24) | Result |
|---|---|
| `.ok == true` | 24 of 24 |
| `.data.evidence_id` equals the `runs.tsv` id and the `table.tsv` cell | 24 of 24 |
| `.data.subject.digest.sha256` equals carrier `e8156675…7806` | 24 of 24 |
| envelope sha256 equals `runs.tsv` `envelope_sha256`; all 24 distinct | 24 of 24; 24 distinct |
| `runs.tsv` argv equals frozen `verbs_argv` with the run's path substituted | 24 of 24 |
| `.meta.command` equals the verb | 24 of 24 |
| envelope bytes contain the run's own path and not the other path | 24 of 24 |
| address verbs' envelopes contain `103fa0` | 15 of 15 |

Derived verdicts equal the table for 8 of 8 verbs: seven content-keyed, `inspect-binary-layout`
path-sensitive. `entry_ok` = 1: the entry exists; its `source:` line names
`corpus/evidence/round-26/c1/table.tsv`, S079 and S080; both rows have `opened` 2026-10-22 and status
`mined`; both ids appear in `corpus/lessons/round-26.md` `## Gate`.

Independent id recomputation (closure's own Node script, importing `digestCanonicalValue` from each
installed package's `dist/domain/canonicalDigest.js` and rebuilding the semantic projection from
`dist/domain/evidence.js`): `n=24 match_6.5.0_rule=24 match_6.7.0_rule=3`. The 6.5.0 projection
adds `relationship_coverage` only when non-null (`evidence.js:175-177`); 6.7.0 always adds it
(`:178`). This ties the envelopes to the 6.5.0 rule, which the envelopes themselves do not name (no
version string in any of the 24).

Statement vs counter: **wider than the counter.** The statement says each verdict re-derives from a
base, a same-path repeat and a byte-identical copy at the alternate path, at the 6.5.0 pin. The
counter accepts forged envelope sets and reads neither `.meta.command`, the run path, the pin nor
the SOURCES status (`w2/MutC1Forgery.md`; lesson M26-5). The closure checked each of those wider
parts directly (tables above). They hold. The SKILL.md decision table "Evidence-ID identity per verb
at a named pin — round 26" cites the entry and agrees with the table. **Verdict: depth improved.**

### R26-C2 calibration — six fixed self-assessment items, mismatches 5 → 0

Reviewer seat ran SCORECARD recipe A itself (sections byte-identical at the three revisions) over
`git show` objects, never the lane instrument:

| Item | `a0639d8e` | `ae8bcd86` (rows identical at `46ebfd2f`) |
|---|---|---|
| K1 depth N/M = recipe A | mismatch: row `9/9`, recipe A 17/17 | pass: `17/17`, 17/17 |
| K2 depth evidence cell names craft span | mismatch: span 81-314, cell `SKILL.md:81-318` | pass: `SKILL.md:81-314` (heading 81, next `## ` at 319) |
| K3 depth measured revision | pass: `638fb211` gives 9/9 | pass: `ebe2cb4a` gives 17/17 |
| K4 coverage N/M and measured revision | mismatch: `measured 3395b6d` gives 78/78, row 108/108 | pass: 109/109 at tip and at `ebe2cb4a` |
| K5 calibration measured revision | mismatch: `75af886a` vs `result.json` `c265db9b…` | pass: `c265db9b…` |
| K6 SHONEN no-cross-domain-bleed line | mismatch: contains "contested" | pass: no "contested"; pointers 95-116, 8-14, 24 inside 303 lines |

5 of 6 → 0 of 6, equal to receipts `before/c2-at-a0639d8e.json` (5), `after/c2-at-46ebfd2f.json` (0),
`after/c2-at-16307c47.json` (0). Truth beyond the counter: `git ls-tree -r --name-only ae8bcd86
corpus/knowledge | grep -c '\.md$'` = 109; recipe A missing [] dangling []; `PROVINCE.md:8-14` and
`:24` state the pins the SHONEN clause says they state.

Statement vs counter: **not wider.** The statement is the six fixed items with the limit "not a full
audit". The rules check form (counts, revisions, a substring) and K6 accepts a false pin
(`w2/MutC2Shonen.md`); the closure checked the landed values for truth and they hold. The 11 further
stale SCORECARD statements from `w1/C2Cherrypick.md` are disclosed open at `SCORECARD.md:3075` and are
not claimed. **Verdict: calibration improved.**

### Other axes and harm

`git diff --numstat a0639d8e ae8bcd86`: deletions only in SCORECARD (3 lines, the depth, coverage and
calibration rows, rewritten with their old values kept as history) and SHONEN (1 line). SKILL.md,
QUALITY.md, README.md, SOURCES.md and all five touched knowledge entries are append-only (0
deletions). No value on an owned row got worse. Coverage: knowledge 108 → 109, recipe A 108/108 →
109/109, a new README coverage-map row; incidental to C1, not a claim.

| Axis | Verdict |
|---|---|
| depth | improved |
| calibration | improved |
| coverage | improved (incidental, not claimed) |

## Discernment spot-check

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
exit 0, five W04 duplicate-URL warnings (S033, S047, S054, S062, S069), then `kaidoku ok`. SOURCES
rows 78 → 80 (`git show <REV>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'`).

The round's `## Gate` admits two rows and records "Rejected: none". Its one non-admit decision is in
the same Gate paragraph and the search log: the installed 6.7.0 package, read for the pin diff, got
no row because it "is already row S037's family". That decision is the reject sampled.

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S079 rea-agents 6.5.0 id minting source (new row, quote check) | admit, code/A, mined | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js` (package.json version 6.5.0) | agree | All six recorded file sha256 values reproduce. Quote at `:182` found verbatim: "const computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`;"; supporting quote at `:160-162` holds. The projection excludes `subject.path` and includes `parameters`, which explains the one path-sensitive verb. The tarball `rea-agents-6.5.0.tgz` (sha1 `7ea5e6f6…7ab3`) unpacks to a `dist/` identical to the installed copy (`diff -rq` empty), so "file-for-file identical" holds. |
| S080 rea-agents 6.5.0 registry record (new row, quote check) | admit, dataset/A, mined | https://registry.npmjs.org/rea-agents/6.5.0; https://registry.npmjs.org/rea-agents; https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.5.0 | agree | Version document sha256 `52184d31…5cde` and attestation sha256 `af5a2c20…f0b` equal the Gate's. Quotes found verbatim: `"integrity":"sha512-C6BG7Lyr…veD+A=="`, `"shasum":"7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3"`, packument `"6.5.0":"2026-10-14T12:56:14.513Z"`, DSSE payload `"gitCommit":"3b79af28e80785afce9f5998d8f03289402a1847"`. Each under 25 words. |
| Installed rea-agents 6.7.0 `dist/` (pin diff) | reject as a new row: "already row S037's family" | `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js` and S037 at `ae8bcd86` | disagree (minor) | S037 is the 6.7.0 *registry record* (dataset) and its scope cell says "not the package's runtime behaviour". The 6.7.0 code read here is runtime behaviour: `relationship_coverage` is always projected (`evidence.js:178`), and a SKILL.md decision rule rests on it ("`relationship_coverage` in the 6.7.0 projection"). By the Gate's own split (installed package = one family, registry = another), this is S079's analogue for 6.7.0, not S037. The rule is also backed by live measurement (`w1/PinSourceDiff.md`, and the closure's 3 of 24 recompute), so no admitted content is false; the gap is sourcing. |

Admits and rejects sampled: 2 admits (agree), 1 reject (disagree, minor). Routed below.

## Trend verdicts

- **expansion: improved.** One new entry on ground the lane did not hold: per-verb evidence-id
  identity at 6.5.0 (five of the eight verbs had no two-path control at any pin). Knowledge 108 →
  109; new README coverage-map row; `source:` cites S079 and S080, both `mined`, opened 2026-10-22,
  re-opened above with quotes found.
- **quality: improved.** Held knowledge was corrected. `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`
  held an `inspect-binary-layout` id "byte-exact" from same-path runs; the round-26 copy run shows the
  id is path-sensitive (`ev_294a449c…` vs `ev_52da4b3d…`, recomputed above). That entry, r4-16 and
  r17 got appended pointers; SKILL.md got a superseding section; QUALITY row 37 supersedes 15. The
  round-25 EVM entry got a correction section; the closure recounted its numbers
  (`git ls-tree … corpus/evidence/round-25/a2/c2`: 69 4byte files, 69 openchain files, 43 distinct
  selectors). All corrections are appended, no filed bytes rewritten.
- **discernment: improved.** The six fixed self-assessment items went 5 → 0 (re-derived above). The
  round-24 source-decision reversal routed by the round-25 spot-check (defect 5) became QUALITY row 35,
  then row 36 after the falsify wave showed 35 could not fail (`w2/QualityRow35.md`; lesson M26-4).
  This spot-check agrees with both admits and disagrees with the one reject (minor sourcing gap, routed
  as defect 1). The lane has not yet had a round to learn it, so it is not "left unlearned".

## SHONEN

All four boxes are `[~]`. None is checked here: promotion is operator-owned. The "No cross-domain
bleed" box (`SHONEN.md:12`, pointers `PROVINCE.md:95-116`, `:8-14`, `:24`) was read by the C2
reviewer seat and is content-accurate at the tip; it looks checkable by a non-author. The operator
may review it.

## Routed defects (lane owns; fix next round)

1. The 6.7.0 installed-package code read for the pin diff has no SOURCES row. S037 is the 6.7.0
   registry record and excludes runtime behaviour. Open a code row for the 6.7.0
   `dist/domain/evidence.js` projection (or make the SKILL.md rule cite only the measured
   envelopes), and record the decision in the Gate as QUALITY row 36 asks.
2. `claims.json` `freeze_kind` promised instruments "committed and sha256-pinned before any
   after-measurement"; C1's instrument landed with its after receipt, after the data. The round-25
   planned field asked for the script before any REA run. Next counter: commit it, with red fixtures,
   before the data it counts.
3. The C1 counter accepts forged envelope sets (M26-5) and the C2 K6 rule accepts a false pin or an
   `[x]` flip (`w2/MutC2Shonen.md`). Do not reuse either as a frozen counter without gating on
   `runs.tsv` `envelope_sha256`, `.meta.command` and the run path (C1), and on pointer content (K6).
4. Envelopes carry no package version; the 6.5.0 pin rests on the frozen invocation and the id-rule
   fit. Record the resolved package version (or `package.json` sha256) per call in `runs.tsv`.
5. The 11 stale SCORECARD statements from `w1/C2Cherrypick.md` (disclosed at `SCORECARD.md:3075`)
   remain open; correct or re-measure them.
