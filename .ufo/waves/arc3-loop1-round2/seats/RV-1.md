# RV-1 seat report — arc3-loop1-round2, chain c1, role reviewer

Seat RV-1 | chain c1 | role reviewer | 2026-10-19 | repo HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420` (pinned at every sample).
Task: review EX-01's rule text for claim fidelity — does it describe exactly the
measured D9 incident, bounded and falsifiable?

Writes: this report + `claims/c1/RV-1/` only. No git mutations; no repo writes;
custody paths untouched (no probe this seat). Scratch `/dev/shm/rv1` (not `/tmp`).
**Verdict binds to the current revision of EX-01's artifact** — `rule14.patch.md`,
11,084 B, sha256 `885fa5379f009a5e81135fffe2a8384ac9bab10532b493fc06d3e12b3fb250eb`,
mtime 09:13:36 -03, payload v2 1,071 B / `6cc388cb…` — with its identity record
`identity-final.txt` v2 (mtime 09:15:41, 1,492 B / `ee899a2a…`). EX-01's v1
(payload `a47dc38d…`) is reviewed below as history and was superseded mid-seat.

## 1. Work performed (evidence pointers)

- Read the frozen round-2 claims (`claims-frozen.md:20-33`), the C1 claim text,
  and the round-1 incident record directly: CR-2's F2
  (`claims/c1/CR-2/proposed-fixes.patch.md:36-49`), `entry-file-identity.txt`,
  `entry-version-diff.txt`, `seats/CR-2.md:86-89`, VZ-1 `seats/VZ-1.md:115` +
  §1, `claims/c1/verdict.md:149-168,202`, `SCORECARD.md:1363-1369`,
  `LOG.md:1409-1412`, `SKILL.md:81-239` (13 rules), recipe A
  (`SCORECARD.md:86-124`).
- Built a scratch measurement harness (no repo writes; `/dev/shm/rv1`):
  `git archive HEAD` full tree → insert a candidate rule text after rule #13 →
  measure. Scripts kept in `claims/c1/RV-1/` (`recipeA-tree.py`, `apply-rule.py`,
  `measure.sh`). The tree recipe A reproduces the SCORECARD git-object recipe
  exactly at HEAD (`baseline-measurement.txt`).
- Measured the D9 chain first-hand rather than from prose:
  `git apply` of EX-12's patch (sha `d662c195…`) on a fresh `e845c2b` tree →
  9,513 B / 32 lines / `a5119120…`; landed entry (HEAD and `fbbbd45`) →
  10,225 B / 33 lines / `dd986f56…`; the landing revision differs from the
  applied patch in 3 entry edits + 1 README edit
  (`d9-chain-measurement.txt`, `landing-diff.txt`).
- Pre-fixed the ground truth for the review with candidate forms
  (`candidate-forms-measurement.txt`): T1 incident-only citations → 13/14,
  depth 9.29; T2 + adjacent `corpus/knowledge` citation → 14/14; T4 = T2
  carrying the incident's `recheck:` command verbatim → **census v10 FAIL
  (undeclared=1), exit 1** while recipe A stays 14/14 (`rea-agents@6.4.0` is a
  locus outside SKILL.md's declared census rows `:10-16`, `:18-20`; EX-05's
  scan shows `needle_hits=2`).
- Reviewed EX-01's artifact: extracted both payload generations, applied EX-01's
  own unified diff verbatim (`patch -p1 --fuzz=0`, exit 0), and ran recipe A,
  census v10 (taken from the committed object `6f1d19ff…`, so EX-16's in-flight
  edit cannot contaminate it), EX-05's needle scan, and RV-2's
  `rule-citation-audit.py` in draft mode.
  Evidence: `ex01-review-measurement.txt` (v1) and
  `ex01-review-measurement-v2.txt` (v2).

## 2. Proposed changes

**none required for EX-01's artifact** (its v2 text measured clean; see §5).
Offered as a measured alternative, not a demand:
`claims/c1/RV-1/proposed-rule14-rewording.md` (and `.patch.md`) — a rewording
that moves the bound into the lede ("its own, or of the bytes it produces and
lands") and keeps the example's recorder explicit. Measured on a fresh HEAD
tree: 14/14, coverage 82/82, depth 10.0, census `PASS 0/0/0/0` exit 0,
needle scan 0 hits, prior-13 byte-identical.

## 3. Before → after measurement for this chain's claim (rules 13 → 14)

Before (HEAD `14b1682`, two implementations agree): `rule_blocks 13`,
`citation_resolved_rules 13`, `82/82`, `10.0/10.0`; census `PASS 0/0/0/0` exit 0;
citation-drift probe `findings=0 exit=0`.

After, on EX-01's **current** post-image (their diff applied verbatim):
`rule_blocks 14`, `citation_resolved_rules 14/14`, `82/82`, `10.0/10.0`;
SKILL.md `371 → 387` lines, sha256
`a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28`
(reproduced by my independent apply of their own diff — matches their claim);
prior 13 rules byte-identical; census `PASS 0/0/0/0` exit 0 with output
identical to baseline apart from the line count (`SKILL.md lines=387 loci=2`);
EX-05 needle scan `added_lines=16 needle_hits=0`; RV-2 audit 5/5 citations
resolve (1 form flag, below).

(For the record, v1 measured the same on its own post-image: `19057c13…`, 385
lines, 14/14, census PASS, 0 needle hits — the defect in v1 was fidelity, not
measurement.)

## 4. Attacks / refutations attempted (verdicts)

| Attack | Method | Verdict |
|---|---|---|
| "the after-state is asserted" | independent harness, two implementations, their diff applied by me | **refuted** — numbers reproduce |
| "the payload hash is not reproducible" | extracted payload v2 and hashed | **refuted** — 1,071 B / `6cc388cb…` exact |
| "the rule text adds a census locus" | census v10 on the post-image + EX-05 scan | **refuted** — PASS 0/0/0/0; 0 needle hits |
| "the rule text reds the citation-drift probe" | probe run on post-image trees | **refuted** — `findings=0 exit=0` |
| "the rule text's SCORECARD citation is rule-#11-form clean" | RV-2's audit, draft mode | **sustained, minor** — `SCORECARD.md:1366-1368` bare line into an in-place-rewritten target; the same flag already exists at HEAD on landed rule #11 (`SCORECARD.md:544-545`), so it is the section's existing convention, not a new class |
| "the incident-citation family can pass on decoration" | CR-1's T1/T2/T3 + my T1/T2/T4 | **sustained as a metric caveat** — 14/14 alone cannot distinguish a faithful citation from an adjacent one (T2/T3 both pass); fidelity must be judged on the text, not the score |
| "a faithful text can name the incident's recheck command" | T4 measured | **sustained** — census FAIL undeclared=1; C1's rule text must stay needle-free |
| "EX-01 v1 describes the incident exactly" | greps + git -S on the landed entry; audit of the patch artifact | **sustained (v1 only)** — the numbers were attributed to the entry, which never carried them; the cited anchor was the recheck line; the bound ("its own") excluded the case; the recheck line was named as the churn cause (measured cause: path-style edits) |
| "v1's defects survive in v2" | re-measured v2 end to end | **refuted** — recorder corrected, three identities named, re-establishment clause added |
| "the rule's falsifiability is untested" | watched the author's own v1→v2 revision | **refuted** — the writer's identity record went stale for ~2 min (artifact 09:13:36 vs record 09:10:04) and was repaired by re-derivation at 09:15:41, v1 kept as labelled history (their A8) |

## 5. EX-01 review — verdict (binding to v2, `885fa537…`)

**Fidelity: PASS on v2 (v1 FAILED on three counted points — history above).**
The current text states the mechanism the round measured: a patch's step-4 claim
kept 8,316 B / `f95c5a05…` while its applied bytes hashed 8,598 B / `d8d85949…`,
with three applied identities in ~20 minutes (`verdict.md:149-153`), the landing
hash recorded by the integrator (10,225 B / `dd986f56…`, `SCORECARD.md:1366-1368`,
`LOG.md:1411-1412`), and the re-establishment clause ("the voided block is
re-established by re-running its checks against the current bytes"). Every
quoted number re-derives at HEAD; every cited path resolves.

**Bounded: PASS with one residual nit.** The lede still says "its own
byte-identity"; the measured case is a claim about the bytes an artifact
*produces*. The body binds it ("claims bind the bytes they describe"), so the
text as a whole covers D9; tightening the lede would remove the ambiguity
(my rewording does exactly that, measured clean).

**Falsifiable: PASS, and demonstrated.** Recipe A is a real binary test (13/14 →
9.29 vs 14/14 → 10.0, measured both ways); the incident numbers are checkable
(and one v1 formulation was checked and failed); and the rule fired in practice
against its own author's record within the hour.

**Instrument status of the landing candidate (all measured by me):** post-image
SKILL.md `a8170b96…` / 387 lines; 14/14, 82/82, 10.0/10.0; census PASS 0/0/0/0;
probe findings=0; needle-clean; prior 13 rules byte-identical.

## 6. Blockers

- None for this seat's verdict. Integration notes the parent may want:
  (a) re-derive SKILL.md's identity at landing (any whitespace change while
  landing moves `a8170b96…`) and record it per the rule it lands;
  (b) `SHONEN.md:6` range/count refresh is a same-commit dependency (EX-01 §4.3);
  (c) EX-16's in-flight census edit means the census evidence must name the
  instrument revision it ran (I used the committed object `6f1d19ff…`);
  (d) EX-01's artifact was revised under the wave (v1 → v2) — anyone citing it
  must cite `885fa537…`/payload `6cc388cb…`, not the v1 numbers.
