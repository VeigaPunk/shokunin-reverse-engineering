# SEAT CR-1 | CHAIN c1 | ROLE critic — arc3-loop1-round2 (2026-10-19)

Seat-line task: attack the rule-formation itself — is queue-drain rule #14
(self-identity re-derivation discipline) craft or process decoration? To survive
it must (1) cite the demonstrated incident and (2) change a measurable
(command A rules count + a real failure mode caught). Strongest version of the
counterargument run; verdict here.

Snapshot: HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` (matches SC-1's
`head-sha.txt`). Writes: this report + `claims/c1/CR-1/` only. No git mutations,
no custody-path writes. Scratch: `/var/tmp/cr1-r2` (kept — EX-12 apply tree,
insertion-form checks, live-apply reproduction).

## Verdict on the seat-line question

**Rule #14 is craft — admits with named residuals.** The failure class is real,
demonstrated, reproducible, *and recurred live inside the rule's own landing
pipeline during this round* — while every committed instrument stayed blind to
it. The count measurable works (14/14, depth 10.0). The draft that should land
is EX-01's payload v2 (receipts real and content-verified), not the EX-05
fallback; two residuals must be fixed or explicitly recorded:

1. **Prior-13 byte-identity fails through the live insertion path** (rule-13's
   parsed segment loses one newline: 484 → 483 bytes, measured). Use a
   byte-preserving insert or grade byte-identity at rule-text level explicitly.
2. **The landing tool's own identity header is stale and its guard is inert:**
   `apply-rule14-from-artifact.py` (sha256 `3468c170…`, mtime 09:15:33) still
   documents payload v1 (896 B / `a47dc38d…`) and output 385 lines /
   `19057c13…`, while the live payload is 1,071 B / `6cc388cb…` and the output
   387 lines / `a8170b96…`; invoked as documented (2 args) both asserts are
   skipped (`if exp_payload:`/`if exp_skill:` never fire) — the tool prints
   "OK" without verifying anything. This is the rule-#14 failure class at the
   tool surface; the rule's text should either cover it or the residual be
   recorded.
3. (Minor) The live payload's one machine-counted citation
   (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`) resolves, but its
   gloss — "whose recheck line records the mid-wave revision" — misdescribes
   the line (it records the post-fix re-measurement, not a revision); and it is
   a bare line into a header that already drifted once this round.

The strongest counterargument (A5) stands against the earlier drafts only; the
live candidate answers it — the class repeated within minutes (A10), so the
"already caught and fixed without the rule" reading no longer holds.

## 1. Work performed (each bullet with an evidence pointer)

- **Baseline (command A at HEAD, read-only git):** `{"knowledge_files": 82,
  "mapped": 82, "missing": [], "dangling": [], "rule_blocks": 13,
  "citation_resolved_rules": 13, "coverage_score": 10.0, "depth_score": 10.0}`
  — `claims/c1/CR-1/command-a-head.txt`; per-rule block sha256 baseline (13
  blocks) `rule-blocks-before.json` (`e9e4b48e…`).
- **Parser experiments** (`rule14-parser-test.py`; command A's rule-parsing
  block replayed verbatim, knowledge read as Git objects at HEAD): results
  `rule14-parser-results.txt`; variants `T4-EX05-actual.SKILL.md`
  (`715b36f2…`), `T5-CR1-corrected.SKILL.md` (`a5ca7cfd…`); candidate texts in
  `rule14-candidates.md`.
- **Incident receipts (read):** CR-2 `claims/c1/CR-2/entry-file-identity.txt`
  (patch output `d8d85949…` / 8,598 B vs claimed `f95c5a05…` / 8,316 B);
  VZ-1 debt D9 (`claims/c1/VZ-1/verdict.md:149-166` = merged
  `claims/c1/verdict.md:149-153`, content verified); `claims/cross/
  wave-summary.md:49-53`; landing record `SCORECARD.md:1366-1368` ("fresh
  identity recorded (10,225 B, sha256 `dd986f56…`…)" — content verified),
  `LOG.md:1411-1412`.
- **Independent re-derivation of the current EX-12 revision:** hunk A extracted
  from the on-disk patch (`d662c195…`) applied in `/var/tmp/cr1-r2/ex12-tree` →
  9,513 B / 32 lines / `a5119120…` = its own step-4 claim → fresh. Extraction
  `ex12-hunkA.patch` (`6eea944a…`); transcript `identity-replay.txt`.
- **Rule-#14 as a mechanism:** `self-identity-check.py` + replay
  `identity-replay.txt`: FRESH on the landed entry (`dd986f56…`/10,225/33) and
  the rev-B output; STALE on `stale-twin-demo.md`.
- **Coverage check for the class:** census v10 normal run with the stale twin
  in-repo → normal verdicts; scope = {PROVINCE.md, SCORECARD.md, SKILL.md}
  (source-extracted) — `census-scope-check.txt`; citation-drift probe at HEAD
  with twin in-repo → `findings=0 exit=0`, no round-1 wave artifact among its
  31 targets — `citation-drift-head.txt`; C3's custody tool covers 5 operator
  config paths only (`custody-pair.py:111-117`).
- **Chain's own citation audit on the EX-05 fallback draft:** RV-2
  `rule-citation-audit.py --block …` → `rules 2 | citations 1 | resolved 1 |
  dead 0 | form_flags 0` — resolvability-clean; content gaps invisible
  (`rv2-audit-on-draft.txt`).
- **Insertion-form checks:** EX-05 `insert-rule.py` (fallback candidate) →
  rule-13 segment +1 newline (`insertion-form-check.txt`; variant
  `EX05-tool-inserted.SKILL.md` `079d44ab…`); live path (EX-01 payload v2 via
  `apply-rule14-from-artifact.py`, `3468c170…`) reproduced in
  `/var/tmp/cr1-r2/live-apply` → `payload_bytes=1071 payload_sha256=6cc388cb…`,
  `anchor_hits=1 anchor_line=[239]`, `skill_lines=387 skill_sha256=a8170b96…`,
  printed `OK` with both identity checks skipped (CLI args omitted) → rule-13
  segment **−1 newline** (484 → 483 bytes).
- **Live-candidate identity claims (verified):** EX-01 `rule14.patch.md`
  (`885fa537…`, mtime 09:13:36) records payload v2 `6cc388cb…` (:45), output
  387 lines / `a8170b96…` (:10-11, :97, :102), and the v1 supersession
  ("Revision note (rule #14 applied to this artifact)", :15-16) — the
  discipline applied to the patch itself.

## 2. Proposed changes

- `claims/c1/CR-1/rule14-citation-fix.patch.md` — T5 replacement text (for the
  fallback-wording path) + byte-preserving insertion requirement + landing
  verification command; the insertion requirement also applies to the live
  EX-01 landing path (residual 1 above). NOT applied; C1's rule lands via the
  chain/parent.
- Residual 2 (tool docstring/guard) and 3 (citation gloss) belong to EX-01 /
  EX-05 artifacts — named for the chain, not patched here.

## 3. Before→after measurement for the chain's claim

Claim: rules 13 → 14, 14/14 citation-resolved, prior 13 rules byte-identical.

| candidate | rules | resolved | depth | prior-13 segment identity |
|---|---|---|---|---|
| base HEAD | 13 | 13 | 10.0 | — |
| T1 incident-only citations | 14 | **13** | **9.29** | true |
| T2 incident + adjacent corpus ref | 14 | 14 | 10.0 | true |
| T3 decoration control (tautology + corpus ref) | 14 | 14 | 10.0 | true |
| T4 EX-05 fallback draft | 14 | 14 | 10.0 | true |
| T5 CR-1 corrected | 14 | 14 | 10.0 | true |
| **T6 live: EX-01 payload v2 + EX-05 tool** | **14** | **14** | **10.0** | **false (rule-13 −1 newline)** |

Commands: `python3 claims/c1/CR-1/rule14-parser-test.py` →
`rule14-parser-results.txt`; T6 via the live-apply reproduction (A1 pointer).
The metric asymmetry stands: incident-only citations drop depth to 9.29; 14/14
needs a `corpus/knowledge` reference; T3 shows the count alone cannot
discriminate craft from decoration.

Replay of the failure class: `identity-replay.txt` — FRESH ×2 on current
artifacts, STALE on the revised twin.

## 4. Attacks / refutations attempted, with verdicts

**A1 — is the demonstrated incident real? CONFIRMED.** Receipts above; the
round-2 claim's incident sentence is accurate in substance (residual: "the
convergence seat (D9)" should name VZ-1 — no seat named "convergence" in either
roster, r1 `claims-frozen.md:92-95`; D9 is VZ-1's debt id).

**A2 — is command A's rule count gameable? CONFIRMED (T3).** Any 14th bullet
with one in-range corpus reference reads 14/14; a content-free tautology passes.

**A3 — did the draft cite the demonstrated incident? CONFIRMED DEFECT for the
EX-05 fallback** (0 receipt paths; its `:1-12` citation presented as defect
evidence while containing none — 0/6 keywords; already drifted). **Fixed in the
live candidate** (receipts real: CR-2.md:86-89, c1/verdict.md:149-153,
SCORECARD.md:1366-1368, LOG.md:1411-1412; residual 3 = the `…md:7` gloss).

**A4 — landing risk to the owned axis. CONFIRMED.** Incident-only citations →
13/14 → depth 9.29 at 14 rules; the count metric is not symmetric — a citation
mistake is an axis regression, not a flat move.

**A5 — strongest counterargument (decoration).** "Rules 1–13 cite corpus
records of REA behavior; #14's incident is fleet paperwork. Depth cannot rise
(10.0 → 10.0), so the count bump is the only guaranteed movement; the incident
was caught in-round and fixed at landing without the rule (`SCORECARD.md:1366`),
and no committed instrument enforces the discipline — so the rule adds text,
not capability." **Verdict: true against the fallback draft; false after A10.**
The class recurs (measured twice inside the rule's own landing pipeline in one
round), and the corrected/live forms carry receipts. Without receipts + a
replay certificate, the decoration reading would stand.

**A6 — redundant with existing rules/instruments? REFUTED.** Rule #11 covers
citations into operator-mutable files; census G19/G20 (H1/H3) cover
census-scope file absence/positive floor; the citation-drift probe pins
registered table citations; the C3 custody tool covers 5 operator config paths.
None re-derives an arbitrary artifact's declared self-identity — measured:
stale twin in-repo, census normal + probe findings=0.

**A7 — "norms can't be craft without an instrument" REFUTED as family-wide.**
None of rules 1–13 has an enforcing instrument; the discriminating criterion is
receipted incident + reproducible catch (both now present).

**A8 — attribution check on the frozen claim.** See A1 residual (VZ-1/D9
naming). Minor.

**A9 — prior-13 byte-identity through the landing tools. CONFIRMED DEFECT on
both paths, in both directions.** `insert-rule.py` (fallback) adds one newline
to rule 13's segment; the live `apply-rule14-from-artifact.py` path removes one
(484 → 483). Land via a byte-preserving insert (form B) or state the grading
level explicitly and accept the delta.

**A10 — does the class recur? CONFIRMED, live, inside rule #14's own landing
pipeline.** (i) EX-01's patch was revised v1 → v2 within the seat's own writes
(896 B/`a47dc38d…` → 1,071 B/`6cc388cb…`) — the patch *records the
supersession* ("Revision note (rule #14 applied to this artifact)"), the
discipline working; (ii) EX-05's tool kept v1 pins in its docstring while its
CLI path drops both identity asserts — a stale declared identity plus an inert
guard, the class recurring at a surface the rule's current wording does not
name. Verdict: strengthens "craft, needed"; feeds residual 2.

**A11 — live-candidate citation integrity. PASS with one gloss defect.** All
incident/landing receipts resolve and hold the claimed content;
`corpus/…:7` resolves under command A (that is what makes 14/14 work) but its
gloss misdescribes the line, and the bare-line form into the entry's header is
the drift class rule #11 warns about (the line already changed between rev-B
and landing). Recommend path-only reference to the entry, gloss corrected.

## 5. Blockers

- None for this seat. Named gaps: (1) the live landing path is EX-01 payload
  v2 + EX-05 tool; fixed-form text (T5) is an alternative if the chain reverts
  to the fallback wording; (2) EX-03's scoped variant
  (`claims/c1/EX-03/proposed-rule14-scoped.md`) exists and independently
  reaches the same citation-disclosure conclusions — the chain has three
  candidate texts and must pick one; (3) residual 2 (tool docstring/guard) is
  the one I would fix before the work commit — it is the class the rule exists
  to prevent, sitting inside the rule's own landing tool.
