# EX-03 — adversary-executor: attacks on the drafted queue-drain rule #14

Wave `arc3-loop1-round2`, chain c1, 2026-10-19. HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`
(`git rev-parse HEAD`; re-checked at every capture below). Read-only on the lane repo; every
scratch write under `/var/tmp/ex03/` (`/tmp` is EDQUOT-broken, standing round-1 record). No git
mutations in the lane repo; the scratch git repo used for command A is `/var/tmp/ex03/variants/repo`.

## 0. What I attacked (seat line: "poll for EX-01's text")

**UPDATE 12:15Z — EX-01 landed mid-seat.** My first 10 polls (12:01:05Z → 12:11Z, log
`/var/tmp/ex03-poll.log`) found no `claims/c1/EX-01/` and no `seats/EX-01.md`; at 12:11Z both
existed, and `rule14.patch.md` was revised again at **12:13:36Z** while I was capturing evidence
(the v1 → v2 payload change is attacked in **§4b**, including a citation that was false in v1 and
was corrected in v2). Attacks §1–§4 were written against the frozen wording before the text
landed; §4b attacks the actual draft. The texts attacked here:

| Text | Path | Status at attack time |
|---|---|---|
| frozen formulation | `claims-frozen.md:20-32` | operative claim text |
| T1 — literal frozen form, incident-only citations | `claims/c1/CR-1/rule14-candidates.md` §T1 | candidate |
| T2 — T1 + one adjacent `corpus/knowledge` citation | same, §T2 | candidate |
| T3 — content-free control | same, §T3 | candidate |
| EX-05 fallback candidate (the likely landing block; EX-05 owns the insertion harness) | `claims/c1/EX-05/fallback-rule14-candidate.txt` | candidate |
| scribe drafts embedding the frozen wording | `claims/c1/records-drafts/{log-entry-draft.md,scorecard-section-draft.md}` | draft for parent |

All four attacks below are stated against the frozen wording (identical in T1/T2/EX-05 on the
points attacked) and are re-stated against EX-05's fallback text where it differs.

## 1. Attack 1 — overreach: does it forbid legitimate revision workflows?

**Verdict: SUSTAINED in part.** Two independent defects, each measured:

**1a. The literal trigger matches nothing, including its own origin event.**
The rule's subject is "an artifact that records **its own** byte-identity". Measured over the
whole repo (text files, `.git`/`node_modules`/`__pycache__` excluded):
**0** files carry a sha256 token equal to their own hash — 4,022 files scanned, round-1 wave tree
1,163 files, round-2 wave tree 991 files (`evidence/A-scope-census.txt`, probe
`selfid-probe.py`). The 6 identity blocks in the round-1 wave tree are all *other-directed*: they
declare the identity of the file the artifact produces or of a clone of it — CR-2's
`entry-file-identity.txt:9` declares 8,316 B/31 lines while itself being 890 B/9 lines. The
origin incident is the same shape: `EX-12/knowledge-entry.patch.md:99-101` declares the identity
of `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` — the artifact it *produces* — not of
itself (CR-1's own T1 prose concedes this: "stopped describing the artifact it produced"). So
the rule as phrased is **under-inclusive against its own evidence**; the honest subject is the
produced-or-declared subject, not "its own".

**1b. Read at the intended breadth, it flags by-design workflows and legitimate evidence.**
Population under the broad reading ("any declaration of an artifact's identity must be current"):
**848 tracked files carry 4,724 `sha256 <hex>` recordings** (`A-scope-census.txt` §4). Among the
workflows a literal checker reddens:

- **Third-party pins.** Round-1 CR-1's additive patch opens with a base pin on *another seat's*
  artifact — EX-12's patch at `d662c195…` plus the produced entry at `a5119120…`
  (`claims/c1/CR-1/knowledge-entry-additions.patch.md:4-7`). The recording seat has no
  notification when the pinned seat revises; "re-derive after every revision" is unactionable
  for it. Chained patch workflows ("the two hunks below apply on top of that file") depend on
  exactly this pin.
- **Defect evidence.** Round-1 CR-2's `entry-file-identity.txt:9` *deliberately* records the
  superseded identity (8,316 B / `f95c5a05…`) as proof of the defect; a literal
  identity-vs-bytes checker flags 6/6 identity blocks in the round-1 wave tree, **all legitimate**
  (`A-scope-census.txt`). This is the same false-positive class the lane already refuted a gate
  form for in arc2-loop1-round3 (`SCORECARD.md:816-820`: a committed gate "would fire on the
  lane's own honest receipt-anchored citations (CR4's false-positive census)").
- **Frozen snapshots are the working practice.** The rule's own origin artifact is stale **at HEAD
  today**: EX-12's step 4 declares 9,513 B/32 lines/`a5119120…`; the landed entry is
  10,225 B/33 lines/`dd986f56…`, because landing applied CR-2's F1 recheck form and the parent
  recorded the fresh identity in `SCORECARD.md:1366` (`evidence/D-origin-staleness.txt` D1–D4).
  That is the *sanctioned* workflow — author declares, integrator re-derives — and under the
  rule's letter the round's own origin artifact is in violation while every downstream record is
  correct. The rule must scope its trigger to the authoring seat's own handoff, not to
  post-handoff state.

**Counter-attack on myself (1c).** A narrow reading — "the author re-derives before claiming" —
is not overreach: EX-12's mid-wave staleness was a real defect caught 3× (CR-2 F2, RV-3 Fix 0,
VZ-1 D9) and fixed in-wave. The overreach is in the *phrasing* ("its own", "after every
revision"), not in the discipline. Verdict stands as *partial*.

## 2. Attack 2 — enforceability

**Verdict: unenforceable as shipped; enforceable only with a new detector and a declared form.**
Measured, three ways:

**2a. No committed instrument sees the class.** Clean/stale pair over `git archive HEAD` scratch
copies (`evidence/B-instrument-blindness.txt`): control copy → census v10 `VERDICT: PASS
(stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0; the same copy with one appended **stale
self-identity line** (declares 9,513 B/32 lines/`a5119120…`; actual 10,375 B/`e24697a6…`) →
**identical PASS, exit 0** ("DECLARED FAIL CLASSES: []"). The census at capture was 560 lines,
sha256 `82fb807e…` — i.e. the *hardened* H1/H3 build, still blind. The citation-drift probe's
unit is `path:line` + needle over a 31-row table (`pointer-table.json`: kinds exact 15 /
extracted 11 / anchor 5; row 0 quoted in `B-instrument-blindness.txt`); it uses sha256 only to
pin its own table (`citation-drift-probe.py:96-97,160-162,295-307`). Command A's unit is rule
blocks + `corpus/knowledge` citation resolution (`SCORECARD.md:94-122`) — it cannot see an
identity claim at all.

**2b. The draft's own mechanization is not a detector.** CR-1's round-2
`self-identity-check.py` takes the declared sha256/bytes/lines as **argv** and compares them to
the file; it never locates a claim inside an artifact. Run against the incident it prints
`VERDICT: STALE … exit=1` for the historical declaration and `VERDICT: FRESH exit=0` for the
landed one (`evidence/D-origin-staleness.txt` D4) — correct, but it enforces nothing without a
human feeding each claim.

**2c. The class *is* mechanically detectable — by a new probe.** `selfid-probe.py` (this seat,
`claims/c1/EX-03/selfid-probe.py`) finds the injected stale claim in the same tree
(`blocks_size_mismatch=1 blocks_lines_mismatch=1` at line 35) while making **0** false claims on
the clean copy. But the *method* clause is not observable at all: no artifact can witness that a
re-derivation happened *after* the last revision — only that the declaration and the bytes agree
*now*. A rule whose sanction is "voids the verification block" therefore needs a reader (or a
probe) at handoff; it cannot self-enforce.

## 3. Attack 3 — duplication vs rules #1-13

**Verdict: PARTIAL duplication — same failure family as #10, same principle as #1/#6, new only
in the "self-authored artifact" unit and the maintenance trigger.** Rule first-lines at HEAD
(`SKILL.md:86-244`; 13 blocks):

- **#10 (`SKILL.md:196-206`)** — "Citations into an operator-mutable file anchor by stanza key +
  receipt, never by bare line number". This is the same recorded-vs-actual drift family; the
  difference is the unit (pointer position vs content hash) and the target (cited file vs the
  artifact's own/produced file). The round-1 wave shows the two classes co-occurring: the
  chain-ledger self-catch is a *cross-file hash* staleness
  (`claims/c1/receipts/chain-ledger.draft.md:121-125`: md cites `reconcile.py` `cbe2731…`, disk
  read `647395a0…`), already rule-#10 territory.
- **#1 (`SKILL.md:86-107`) / QUALITY #14–15 (`corpus/QUALITY.md:24-25`) / #6
  (`SKILL.md:162-169`)** — id-identity claims must state their domain and pin request bytes when
  identity matters; the "identity claims must be re-derivable" principle is already codified for
  evidence ids. #14 extends it to authoring artifacts, which is a genuine (if small) increment.
- **#4 (`corpus/QUALITY.md:14`)** — "names the artifact under analysis by absolute path plus a
  stable identity" — governs evidence about analyzed targets, not the lane's own records.

Duplication cost is concrete: two rules about recorded-vs-re-derived drift invite divergent forms.
Recommendation: if landed, #14's text should cross-reference #10 (one principle, two units) rather
than read as a separate doctrine.

## 4. Attack 4 — process decoration vs craft

**Verdict: decoration-risk CONFIRMED at the landing form; craft only if a form + detector ship
with it.** Three measurements:

**4a. The round's own metric cannot discriminate.** Independent re-run of command A over scratch
repos with each candidate inserted before the SOP marker (the EX-05 harness shape;
`evidence/C-variant-scoring.txt`, harness `variant-check.sh`):

| variant | rule_blocks | citation_resolved_rules | depth_score |
|---|---|---|---|
| base HEAD | 13 | 13 | 10.0 |
| T1 (honest: incident-only wave citations) | 14 | 13 | **9.29** |
| T2 (T1 + one subject-adjacent `corpus/knowledge` citation) | 14 | 14 | 10.0 |
| T3 (**content-free control** rule + one citation) | 14 | 14 | 10.0 |

T3 — "Cite the source you measured, not the one you remember." — scores *identically* to the real
rule. So `14/14 citation-resolved` is evidence that a rule block exists with a resolving
`corpus/knowledge` citation, not that craft landed; and the honest form (T1) is scored as depth
*loss* (9.29). My measurement agrees with CR-1's `rule14-parser-results.txt` on all four numbers.
(Discrepancy disclosed: CR-1's harness also reported `prior-13 byte-identical: False`; my
block-by-block split of the craft section reads `True` for all three variants — the difference is
section-tail bytes vs rule-block bytes. The frozen claim's "prior 13 rules byte-identical" is
satisfiable; whoever writes the records should state which comparison it means.)

**4b. EX-05's likely landing form carries a subject-adjacent citation.**
`fallback-rule14-candidate.txt` cites `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:1-12`;
the span resolves (file has 33 lines) and scores 14/14 — but that entry records **0** occurrences
of the incident (`stale|churn|revis|8,316|9,513` → 0 matches; `D-origin-staleness.txt` D5). It is
the T2 laundering shape CR-1 itself flagged, chosen because the honest form is metric-fatal.

**4c. The discipline is already practiced without the rule.** Round-1 RV-3 ran the exact check as
a graded attack row — "stale self-identity in the artifact | sha256 of applied file vs §4 claim |
caught on the 07:11 revision (Fix 0); current revision passes"
(`claims/c1/RV-3/quality-grade.md:116-119`); CR-2 prescribed the fix as patch text (F2); the
parent recorded the fresh identity at landing (`SCORECARD.md:1363-1367`). The defect class was
caught 3-way by review, in the same wave, with no rule. The rule adds no detection capability —
only a named obligation.

Net: the *discipline* is craft (it changed a real authoring behavior in round 1). The *rule text
as landable this round* is decoration-adjacent: no instrument enforces it, the metric cannot tell
it from a content-free control, and its citation is adjacent because the honest citation scores
9.29. If it lands, it should ship with (i) an explicit trigger scope, (ii) the declared form
("declares identity of X" where X is named), and (iii) the probe as an optional checker — and the
round record should say plainly that command A's 14/14 is a rule-count measure, not a craft
measure.

## 4b. Attacks against EX-01's landed payload (the actual draft)

Target: `claims/c1/EX-01/rule14.patch.md` — an 11,084 B patch text (`885fa537…` at 12:15Z;
mtime 12:13:36Z) carrying a 1,071 B payload (`6cc388cb…`, insert after the unique
`kernel-OOM-killed (…)` line = `SKILL.md:239`), and the sibling `identity-final.txt`
(mtime 12:10:04Z). Evidence: `evidence/E-ex01-payload-citations.txt`,
`evidence/F-ex01-identity-state.txt`, `evidence/audit-ex01-payload.json`.

**4b-1. Citation truth test — 4/5 true, and the false one was the metric-counting one (v1).**
In the v1 payload (captured 12:11Z, `896 B / a47dc38d…`) the block stated that the C1 entry
`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7` "(its own recheck line revised
mid-wave) recorded 8,316 B / `f95c5a05…`". Measured at that revision: line 7 is the recheck
*command* in CR-2's F1 disk-backed-TMPDIR form, and the file contained **0** occurrences of
`8,316`, `f95c5a05`, `d8d85949` or `9,513` (`evidence/E-ex01-payload-citations.txt` E3). The
claim lived only in round-1 wave artifacts (CR-2's F2, VZ-1's D9). The citation *span resolves*
→ command A scores it → the round's own metric cannot see the falsehood. **This is the sharpest
instance of attack 4's metric gap: the only citation that counts was the only citation that was
untrue.** EX-01's A1 self-check ("checked the counted citation resolves") tests resolution, not
truth — correct by construction, since no instrument tests truth.

**Superseded in v2 (12:13:36Z).** The current payload re-attributes the numbers to the patch's
own "step-4 claim" (`seats/CR-2.md:86-89` — verified line-for-line true) and the chain's three
applied identities (`claims/c1/verdict.md:149-153` — verified true), keeping the entry citation
only for "whose recheck line records the mid-wave revision" (true: line 7 carries the
`2026-10-19T10:14Z` re-derivation). The other v2 citations also verify: `SCORECARD.md:1366-1368`
(10,225 B / `dd986f56…`) and `LOG.md:1411-1412` (same). **Verdict on v2: citation-true; v1's
false citation is a resolved defect, retained here because it is the class the round must be
able to detect.**

**4b-2. The landing package went stale by the rule's own standard — and was repaired in-seat.**
`identity-final.txt` as captured at 12:15:0xZ (mtime 12:10:04Z, not re-derived) declared three
identities; all three were wrong because `rule14.patch.md` was revised at 12:13:36Z
(`F-ex01-identity-state.txt` F1–F3):

| declared in `identity-final.txt` (v1, 12:10:04Z) | derived at 12:15Z | verdict |
|---|---|---|
| artifact 8,833 B / `7cd9e950…` | 11,084 B / `885fa537…` | STALE |
| payload 896 B / `a47dc38d…` | 1,071 B / `6cc388cb…` | STALE |
| patched SKILL.md `19057c13…` | 387 lines / `a8170b96…` (EX-01's own anchor apply, reproduced exactly by me) | STALE |

**Superseded at 12:15:41Z:** EX-01 re-derived the record (its header carries a 12:14:21Z
derivation stamp and keeps v1 as history). I verified all three fresh values against the bytes
at 12:18Z: artifact 11,084 B / `885fa537…` ✓, payload 1,071 B / `6cc388cb…` ✓, patched SKILL.md
387 lines / `a8170b96…` ✓. So the stale window was ≈5 minutes and the defect class reproduced
*and was repaired* inside the seat that lands the rule.

That is the rule's best evidence and its sharpest scope question at once. The patch text was
never stale — its §3 table carries fresh numbers and its revision note discloses v1→v2. The
records that lagged were the *sibling* carriers: `identity-final.txt` (fixed) and EX-01's seat
report §2, which still describes "`rule14.patch.md` (8,833 B / `7cd9e950…`)" at 12:18Z
(measured: report unchanged since 12:11Z). "After every revision" therefore needs the rule to
name **which record carrier owes re-derivation and at what trigger** — otherwise it penalizes
frozen snapshots (the round-1 EX-12 case, deliberately stale after landing) while the seat
report — a report of work, not of bytes — is left in the class by accident.

**4b-3. The landing block already fails the lane's own citation-form audit (RV-2's tool).**
Running RV-2's round-2 `rule-citation-audit.py` over a scratch repo carrying the payload flags
exactly one form defect on the new rule: `SCORECARD.md` 1366-1368,
`bare_line_into_in_place_target`, no content anchor, no capture stamp, rule_line 241
(`evidence/audit-ex01-payload.json`). Baseline at HEAD has the same class once (the custody rule,
`SCORECARD.md:544-545`, rule_line 207) — so the draft adds a *second* instance of a class the
chain's own verifier flags. Trivial fix: cite the round-1 section by its content (the fresh
identity it records, "fresh identity recorded (10,225 B, `dd986f56…`)") instead of `:1366-1368`.

**4b-4. Instrument-count divergence (disclosed, not an attack).** RV-2's tool counts the
craft **section heading** as an entry: it reports `rules=14` at HEAD (command A: `rule_blocks=13`)
and `rules=15` with the payload (command A: 14), and would label the new rule entry #15. Two
instruments in the same chain disagree on the rule count by exactly one; the round record should
quote whichever it means, and should not present the two counts as corroborating.

**4b-5. The payload's own token hygiene verified.** `PIN=0 VER=0 PTR=0 CACHE=0 REA_GATE=0` over
the 1,071 payload bytes (my re-run of the census's patterns), matching EX-01's claim; and the
pre-image/post-image identities they record are exact under their documented anchor apply
(371 lines `483b0eba…` → 387 lines `a8170b96…`, prefix 1-239 byte-identical — I reproduced both).
Disclosure: my first harness (heading-anchored) produced 386 lines / `a07091f1…`; that difference
is *my* harness's blank-line handling, not an EX-01 error (`F-ex01-identity-state.txt` F4).

## 5. Recommended landing form (patch text, not applied)

`claims/c1/EX-03/proposed-rule14-scoped.md` — scoped text: trigger names *whose* identity
(self or produced), the maintenance duty is scoped to the author's handoff (not to third-party
pins made by other seats), the incident citations keep their wave paths, and the corpus citation
is labelled as the principle's record with the incident disclosed as wave-scoped.

For the text that actually landed (`claims/c1/EX-01/rule14.patch.md`, v2), my recommendation is
to land it **with three amendments**, none of which change its meaning:

1. **Scope wording** — add "or of a file it produces" to the trigger; as written ("its own
   byte-identity") it matches 0 of 4,022 scanned files and none of its own incident (§1a).
2. **Citation form** — replace `SCORECARD.md:1366-1368` with the content it carries ("fresh
   identity recorded (10,225 B, `dd986f56…`)"); RV-2's own audit flags the bare line as
   `bare_line_into_in_place_target` (§4b-3).
3. **Absolute-duty wording** — soften "after every revision" to the handoff point, because the
   live counter-example is in this very package: `identity-final.txt` went stale 3.5 minutes after
   it was written while the artifact it describes was legitimately revised (§4b-2).

If the parent prefers to land EX-01 v2 unchanged, then record explicitly in the round's
SCORECARD/LOG text: (a) the citation-truth gap (command A scores resolution, not truth — §4b-1),
(b) the `identity-final.txt` staleness at the rule's own handoff (§4b-2), and (c) that the
`SCORECARD.md:1366-1368` form is already flagged by the chain's own audit tool (§4b-3), matching
the pre-existing custody-rule flag.

## 6. Before → after measurement (my chain's claim)

The claim under attack (`claims-frozen.md:30-32`): "queue-drain rules 13 → 14, 14/14
citation-resolved at the work commit (command A), prior 13 rules byte-identical".

- **Before** (independent, at HEAD `14b1682b`): `{"citation_resolved_rules": 13, "depth_score":
  10.0, "knowledge_files": 82, "mapped": 82, "rule_blocks": 13}` (`evidence/C-variant-scoring.txt`
  base row; corroborated by `.ufo/waves/arc3-loop1-round2/claims/c1/CR-1/command-a-head.txt`).
- **After, measurable today**: T1 → 13/14, 9.29; T2/T3/EX-05-fallback → 14/14, 10.0. The claim's
  "14/14" is therefore reachable, but only in the citation-adjacent form; the honest form fails
  it. Nothing in my measurements blocks the claim; they bound *what it will mean*.
- **The landed draft (EX-01 v2) measured**: payload 1,071 B `6cc388cb…`; patched SKILL.md 387
  lines / `a8170b96…` (reproduced under EX-01's own anchor apply); payload token scan
  `PIN=0 VER=0 PTR=0 CACHE=0 REA_GATE=0`; command A after = 14 rules / 14 resolved / 82/82 /
  10.0 (EX-01's §3 table, with their worktree-adapted runner; my independent variant runs agree
  on the rule/resolution numbers). Its v1 → v2 revision left `identity-final.txt` stale (§4b-2),
  and its `SCORECARD.md:1366-1368` citation carries one audit form flag (§4b-3).
- **Also measured**: prior-13 block byte-identity holds under a clean insertion (True ×3).

## 7. Attacks on my own findings (limits)

- My scanner is text-only and form-based: it detects the canonical "N bytes, M lines" block and
  full self-hash tokens. A self-identity written in free prose or with a truncated prefix would
  be missed by `selfid-probe.py` (measured prefix-scan: 0 hits in the round-1 wave, so the
  false-negative surface is unexplored, not proven empty).
- "0 self-bound sha256 in 4,022 files" is scoped to text files in this repo at this revision; it
  is not a claim about intent, only about literal phrasing.
- The census at capture (`82fb807e…`, 560 lines) is itself moving — C2's chain is landing
  fail-closures in-round. My blindness result is pinned to the capture stamp above; a future
  census build must be re-measured before reusing it.
- My variant tests use the EX-05 insertion shape; if the block lands elsewhere in the craft
  section, scores should hold (command A splits on `- **`), but the byte-identity reading may not.
- §4b-1's truth test checks the *current* payload and the v1 text I captured at 12:11Z; if EX-01
  revises again, re-derive the citation truth with the commands in `evidence/E-…txt` rather than
  reusing my verdict.
- RV-2's audit is a peer artifact under active revision; I ran the byte-version present at 12:13Z
  (its `--selftest` passes) and did not modify it.

## 8. Blockers / gaps

- **N-1 (resolved): EX-01 landed at 12:11Z** (report + `rule14.patch.md`), revised at 12:13:36Z,
  identity record re-derived at 12:15:41Z; attacked in §4b. Residual at my close (12:18Z):
  EX-01's **seat report** §2 still describes the artifact as "8,833 B / `7cd9e950…`" (v1) while
  the artifact is 11,084 B / `885fa537…` — the only stale record left in the package, and it is a
  report-of-work rather than a byte-record, which is exactly the scope question §4b-2 raises.
  If EX-01 revises again, the integrator must re-derive rather than quote.
- Evidence files: `claims/c1/EX-03/evidence/{A-scope-census.txt, B-instrument-blindness.txt,
  C-variant-scoring.txt, D-origin-staleness.txt, E-ex01-payload-citations.txt,
  F-ex01-identity-state.txt, audit-head.json, audit-ex01-payload.json}`; tooling
  `selfid-probe.py`, `variant-check.sh`.
