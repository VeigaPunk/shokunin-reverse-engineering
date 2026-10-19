# C1 verdict — convergence reconciliation (SEAT VZ-1, chain c1)

Wave `arc3-loop1-round2`, 2026-10-19. Reconciled from `seats/` + `claims/c1/`
at 12:01–12:58Z; lane HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` at every
sample (`git rev-parse HEAD`, re-checked at each phase). Polling: own 60 s
poller (25 checks, 12:01→12:26Z; full log `claims/c1/VZ-1/evidence/poll.log`)
plus targeted re-lists to close. Writes by this seat: this verdict (+ mirror
`claims/c1/verdict.md`), `seats/VZ-1.md`, `claims/c1/VZ-1/evidence/*`. No git
mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/README edits; custody paths
untouched; scratch `/dev/shm/vz1r2` (never `/tmp`).

## VERDICT: C1 **VERIFIED** — tree-level, with 1 blocking landing condition

Every falsifiable component of the frozen claim (`claims-frozen.md:20-32`) is
reproduced first-hand at tree level, and a **rule-#11-form-conforming text is
measured end-to-end by this seat** (EX-01 rev B + RV-2's one-sentence rewrite:
payload `7e76e2e7…` → SKILL.md 388 lines `60dfbe02…`, command A **14/14**, 0 dead
citations, **0 new form flags**). What is NOT yet measurable is the claim's
"at the work commit" numbers, because that commit does not exist until the
parent integrates — the predicate is proven at tree level instead (round-1 E7
precedent). **One branch is NOT-VERIFIED by measurement: landing EX-01 rev B
verbatim** — its `SCORECARD.md:1366-1368` is a bare line range into an
in-place-rewritten file (freeze's "no bare line numbers"); it carries 1 form
flag in RV-2's instrument and in my independent scan, both on committed trees.

### Why VERIFIED (claim component → evidence; all recomputed by VZ-1 unless noted)

| # | Claim component | Verdict | Evidence |
|---|---|---|---|
| C1-a | queue-drain rules **13 → 14** | PASS (tree) | command A verbatim, before `14b1682b`: `{rule_blocks: 13, citation_resolved_rules: 13, mapped 82/82, 10.0/10.0}`; after (EX-01 rev B tree, committed): `{rule_blocks: 14, citation_resolved_rules: 14, …}` — E1/E3 |
| C1-b | **14/14 citation-resolved** at the work commit | PASS (tree); commit-level owed | 14/14 reproduced on 4 applied trees (EX-01 rev A/B, PL-1, T5, fixed variant — E2-E6); the countable citation is the incident's own entry (`…-evm-real-solc.md:7`/`:5-7`), not an adjacent file (CR-1 A3/EX-02/RV-1 F6 reviewed) |
| C1-c | prior 13 rules byte-identical | PASS as **pure insertion + rstrip-normalized 13/13** | my pure-insertion proof: `before == after[:k] + after[end:]` holds (zero modified bytes) for every candidate applied (E2-E6); raw block-split reads 12/13 (separator attribution — EX-02 §2.1/§4.3, CR-1 A9, PL-1 Q7, SC-1 A2 all name it; record must use the precise phrasing) |
| C1-d | citations in **rule-#11 form** (stanza key + receipt, no bare line numbers) | **CONDITIONAL — fails as-written on EX-01 rev B; PASSES on conforming texts** | EX-01 rev B: 1 flag, `SCORECARD.md:1366-1368` bare into an in-place-rewritten file (RV-2 instrument + my scan, committed trees); LOG.md:1411-1412 is append-only (exempt); conforming: fixed variant (0 flags — E7), PL-1 v5 (0 flags; 1 unrelated dead token), CR-1 T5 (0 flags; 1 wrapped-path token), PL-1 merged (0 flags; 2 text defects) |

## Candidate matrix (measured by VZ-1 on committed scratch trees; hashes first-hand)

| Candidate | Result SKILL.md | command A | pure insert / prior-13 norm | new-rule form flags | dead cites | Note |
|---|---|---|---|---|---|---|
| EX-01 v1 (superseded 12:13Z) | 385 L `19057c13…` | 14/14 | ✓ / ✓ | 1 (`SCORECARD.md:1366`) | 0 | payload 896 B `a47dc38d…`; kept as history only |
| **EX-01 v2 = current artifact** | 387 L `a8170b96…` | 14/14 | ✓ / ✓ | 1 (`SCORECARD.md:1366`) | 0 | payload 1,071 B `6cc388cb…`; artifact `885fa537…`; rule :240-254, heading :258 |
| **EX-01 v2 + RV-2 form rewrite (VZ-1 applied)** | 388 L `60dfbe02…` | 14/14 | ✓ / ✓ | **0** | 0 | payload 1,129 B `7e76e2e7…`; **fully conforming candidate — verifier PASS** |
| PL-1 v5 | 395 L `11647e6d…` | 14/14 | ✓ / ✓ | 0 | 1 (`claims/c1/verdict.md` shorthand) | block 1,736 B `51a87ef6…`; fix text = RV-2 `proposed-pl1-verdict-path.patch.md` |
| PL-1 merged block | (392 L, SHONEN end 259 per SC-1; not applied by VZ-1) | 14/14 (RV-2 sim) | n/a | 0 | 0 | **not quote-ready**: closing sentence duplicated; 5 continuation lines at column 0 (my read + RV-2 A9 + SC-1) |
| CR-1 T5 | 386 L `8ab17e6b…` | 14/14 | ✓ / ✓ | 0 | 1 (`claims/c1/`\n`VZ-1/verdict.md` wrapped path) | block 1,044 B `c829478b…`; fix = unwrap the path |

Instrument side-effects on the landing (committed census `6f1d19ff…`, first-hand):
HEAD `PASS 0/0/0/0` (SKILL.md 371/loci 2) → rev B tree `PASS 0/0/0/0`
(SKILL.md 387/loci 2), delta = the single benign line `SKILL.md 371 → 387`;
citation-drift probe: HEAD `findings=0 exit=0`, patched trees `findings=0`
(CR-1 + EX-06 peer runs on rev B; my run on rev A). No locus added anywhere.

## First-hand measurements (E-numbers used above)

- **E1 (before-state).** Recipe A verbatim at `14b1682b`: `{"citation_resolved_rules": 13,
  "rule_blocks": 13, "mapped": 82, "knowledge_files": 82, "missing": [], "dangling": [],
  "coverage_score": 10.0, "depth_score": 10.0}`; SKILL.md 371 L
  `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`.
- **E2 (EX-01 rev A).** Payload extracted strictly between the artifact markers: 896 B
  `a47dc38d…` (declared == derived); anchor-form apply → 385 L `19057c13…`; my verifier:
  14/14, pure insertion, prior-13 rstrip-identical, needle scan 0 loci; census delta
  `DELTAS=0` (only `SKILL.md 371→385`); probe findings=0.
- **E3 (EX-01 rev B).** Artifact `885fa537…` (11,084 B, mtime 12:13:36Z); payload
  1,071 B `6cc388cb…`; apply → 387 L `a8170b96…`; rule at :240-254, heading :258;
  verifier: 14/14, pure insertion, prior-13 rstrip-identical; needle-clean; 1 bare-line
  flag (`SCORECARD.md:1366`); all 5 citations resolve; census delta `DELTAS=0`.
  `identity-final.txt` re-derived at 12:14:21Z with v1 explicitly superseded — the
  rule-#14 discipline correctly applied to the rule's own artifact (window in L2).
- **E4 (PL-1 v5).** Its `rule-14.diff` applies cleanly to a fresh tree (`git apply
  --check` exit 0): +24/-0, 395 L `11647e6d…` == its rehearsal claim; block file =
  1,736 B `51a87ef6…` + trailing newline. Verifier: 14/14, no bare lines, needle-clean;
  1 dead citation `claims/c1/verdict.md` (shorthand; absent at repo root).
- **E5 (CR-1 T5).** Fenced block 1,044 B `c829478b…`; apply → 386 L `8ab17e6b…`;
  14/14; no bare lines; 1 dead token from the line-wrapped path
  (`claims/c1/`+newline+`VZ-1/verdict.md`).
- **E6 (round-1 incident facts).** Landed entry at HEAD = 10,225 B / 33 L /
  `dd986f56…` (matches `SCORECARD.md:1366-1368` + `LOG.md:1411-1412` content, read
  first-hand); CR-2's receipt and VZ-1 D9 (8,316/8,598/9,513 B identities) read.
- **E7 (conforming fixed variant, the landing demonstration).** Rev B payload with
  RV-2's one-sentence rewrite (RV-2 `proposed-rule14-citation-form.patch.md`, first
  variant): payload 1,129 B `7e76e2e7…` → 388 L `60dfbe02…`; my verifier **PASS all
  checks**; RV-2 instrument on the committed tree: 60 cites / 59 resolved (1 custody
  stat-only) / 0 dead / flags = the pre-existing rule-#12 only.
- **E8 (census, committed instrument).** `6f1d19ff…` bytes run with `--root` on HEAD
  and on the applied trees (rev A/rev B/fixed); all PASS 0/0/0/0, SKILL loci 2
  throughout; EX-05's delta tool: `DELTAS=0`.
- **E9 (citation content match).** All rev-B citations' targets hold the claimed facts
  (entry `:7` recheck line; CR-2.md:86-89; verdict.md:149-153; SCORECARD:1366-1368;
  LOG:1411-1412) — read at HEAD.
- **E10 (RV-2 instrument baseline + audit hygiene).** HEAD: 13 rules, 55 cites,
  54/54 in-repo resolved, 1 pre-existing flag (rule #12 `SCORECARD.md:544-545`). The
  tool grades `SKILL.md` at the tree's **committed** revision — applied-but-uncommitted
  trees read as base (my own mis-run reproduced this; corrected by committing; named L7).
- **E11 (pooling).** 25-sample poll log + seat counts 0→62; all 12 c1 seats delivered a
  report by 12:58Z; undelivered wave-wide at my close: **RV-9 (c2), VZ-2 (c2),
  VZ-4 (cross)** (VZ-1 = this verdict). Named, not backfilled.

### Per-seat reconciliation (all 12 c1 seats)

| Seat | Delivered | Reconciled with my recomputation |
|---|---|---|
| PL-1 | plan.md, own text v5, merged block, SHONEN refresh, late §6 reconciliation | v5 measured exactly (E4); merged text defects confirmed; §6's "254 if EX-01's payload lands" matches my E3 geometry (rev B); its rank-1 (EX-01 v2) matches RV-2's caveat |
| EX-01 | rule14.patch.md v1→v2 + identity sidecar + evidence | rev A/B both byte-reproduced (E2/E3); v1→v2 churn + stale-sidecar window (closed 12:14:21Z) is the rule's own class live (L2); component-4 flag stands on rev B |
| EX-02 | dry-run + pre-registration + fidelity controls | agrees: 385 L `19057c13…` from both recipes (rev A era); its strict/line-level phrasing of prior-13 matches E2/E3; scratch-shape note (L8) |
| EX-03 | scope census (1163 files / 6 identity blocks; repo-wide 50) + census-blindness control + T1/T2/T3 scoring | agrees: census is blind to a stale self-identity (C1's discipline is reviewer-enforced, L9-adjacent); candidate scores match E4's family |
| EX-04 | SHONEN enumeration + refresh patch text + silent-pass measurement + pre-existing 243-overshoot defect | range end must be re-derived (L3); its `81-252` is rev-A geometry (rev B = :254, E3) |
| EX-05 | census interplay v1/v2 + instrument pinning + A6 identity-window catch | agrees; its instrument-revision ladder `6f1d19ff→…→d0772ce8` (L5); A6's 12:14Z window matches E3 |
| EX-06 | probe battery + custom-table bite tests + SHONEN-range bite | agrees: probe blind to rule-#14 citations by table design (not widened, r4 precedent) |
| SC-1 | baseline, rehearsal (v2: 387 L `a8170b96…`, cmd A 14/14), records drafts + pin-free projection (control bites UNDECLARED=1) | agrees with E3 exactly (declared == derived); records pin-free control reproduced by its own evidence |
| RV-1 | candidate measurements T1/T2/T4 + fidelity list + D9 chain | agrees; T4's census-red warning is integration condition IC1's reason the text must stay needle-free |
| RV-2 | audit instrument + candidate verdicts + 2 fix texts | its EX-01 audit graded **rev A** (pre-12:13Z); my E3/E7 extends it to rev B and the fixed variant; its catalog of candidate verdicts matches my matrix |
| CR-1 | critic bundle + T5 + self-identity replay + insertion constraint | T5 measured (E5, 1 wrap defect); its decoration argument is answered by rev B's receipts + the replay; its insertion-form finding is honored by every measured candidate (pure insertions) |
| VZ-1 | this verdict + seat report + evidence | — |

## Named debts (all survive the VERIFIED verdict)

- **L1 — EX-01 rev B fails component C1-d as written** (1 bare `SCORECARD.md:1366-1368`).
  Fixes delivered: RV-2's one-sentence rewrite (measured by VZ-1: `7e76e2e7…`/`60dfbe02…`,
  all checks PASS), or PL-1 v5 + path fix, or T5 + unwrap. Landing rev B verbatim makes
  C1-d **NOT-VERIFIED** under the freeze's strict reading.
- **L2 — mid-wave churn on the rule's own artifact** (the rule's premise, live): v1
  `7cd9e950…` (8,833 B, payload 896 B `a47dc38d…`) → v2 `885fa537…` (11,084 B, payload
  1,071 B `6cc388cb…`); sidecar briefly stale at 12:14Z (EX-05 A6), re-derived
  12:14:21Z. Do not cite v1 identities as current; the landing record must re-derive.
- **L3 — SHONEN.md:6 is stale the moment the rule lands, and three end numbers
  circulate**: 252 (rev-A geometry: EX-01 §4.3/EX-04), **254 (rev B, my measurement)**,
  265 (PL-1's own text), 259 (merged, SC-1). Recompute from the landed bytes in the
  same commit; the probe will NOT catch the omission (EX-04 A2/A3, EX-06 bite via
  custom table only).
- **L4 — "prior 13 rules byte-identical" must be recorded as pure insertion (0 modified
  bytes) + rstrip-normalized 13/13**; raw block-split reads 12/13 (separator
  attribution). Three seats' harnesses printed a spurious `DIFF rule 13` from this.
- **L5 — census instrument churn**: five+ revisions during the wave
  (`6f1d19ff` committed → `82fb807e` → `df9ffdf9` → `a4c16763` → `d0772ce8` →
  `c95a5cf3`; C2/EX-16's write target). Every census reading in the records must carry
  the instrument sha256 at read time; my readings used the committed `6f1d19ff` bytes;
  re-run after C2's v11 lands.
- **L6 — undelivered wave seats at my close**: **VZ-4 (cross) only**; RV-9 (c2) and
  VZ-2 (c2) landed late (~12:5xZ) and are not reconciled here; VZ-1 = this verdict.
  All 12 c1 seats delivered and are reconciled above.
- **L7 — audit hygiene**: RV-2's audit grades `SKILL.md` at the tree's committed rev;
  run audits after committing the applied tree (my mis-run reproduced the read-at-base
  artifact; corrected).
- **L8 — fixture-shape dependence**: a 3-file scratch root makes the census read
  SCOPE-ERRORS (marker uncheckable) on both sides (EX-02 §2.2); use complete archives.
- **L9 — the class is not instrument-enforced**: census (EX-03 B) and probe (EX-06)
  are blind to a stale self-identity; rule #14's compliance is reviewer-enforced plus
  the mechanized replay (`claims/c1/CR-1/self-identity-check.py`); EX-05 A4 also
  showed even the whole patch document escapes the census needle vocabulary. Say this
  in the record — do not imply instrument enforcement.
- **L10 — freeze-text precision**: "the convergence seat (D9)" — D9 is VZ-1's debt id
  (CR-1 A8); "rule #14" is by block count (13→14) while the landing discipline is
  historically "rule #11" (now block #10) — the record uses both, correctly.

## Integration conditions (must hold or C1's after-state breaks)

1. **Land exactly ONE conforming text; recompute everything from its bytes.**
   Measured options: (a) EX-01 rev B + RV-2's form rewrite (VZ-1-applied:
   `7e76e2e7…` → `60dfbe02…`, verifier PASS, 0 flags) — recommended; (b) PL-1 v5 +
   `proposed-pl1-verdict-path.patch.md`; (c) T5 + unwrap. **Do not land rev B
   verbatim** (L1) or the merged block as-is (L3-adjacent text defects).
2. **Refresh `SHONEN.md:6` in the same commit**, range end = landed payload's last
   rule line (254 for rev B; 255/259 for other texts), count 14/14 (§L3).
3. **Records pin-free** (no `6.x.y` / `rea-agents@` tokens in the appended
   LOG/SCORECARD sections — SC-1's control bites `UNDECLARED=1` otherwise), and
   **re-derive the landed `SKILL.md` identity** (rev B: 387 L `a8170b96…`; fixed:
   388 L `60dfbe02…`) instead of carrying any rehearsal number.
4. **Re-run at the work commit**: command A (expect 14/14, 82/82), census (pin the
   instrument sha), probe (findings=0), and the SHONEN/reference checks.
5. **No pointer-table or census-scope widening** (r4 laundering precedent); no
   corpus edit — the countable citation's target already exists and is append-only.

## Attack log (what I tried to refute, and the outcome)

- *"The 14/14 count is real, not asserted."* Refuted-as-doubt: reproduced on four
  applied trees with two independent parsers (my verifier + RV-2's tool) (E2-E7).
- *"The count discriminates craft from decoration."* **Sustained**: T3/EX-02 control
  passes 14/14 with zero content (CR-1 A2, EX-02 attack 1). The count alone cannot
  carry the verdict; the receipted incident + replay certificate do (CR-1 A5).
- *"The rule text launders its citation."* Sustained against EX-05's fallback only
  (CR-1 A3); refuted for rev B/v5/T5 — their counted citation is the incident's own
  entry, receipts named (E9).
- *"The rule's own failure mode falsified its artifact."* **Sustained once, then
  closed**: v1→v2 churn + 12:14Z stale sidecar (L2); EX-01 re-derived at 12:14:21Z —
  the discipline held on the artifact that lands the discipline.
- *"The append moves an instrument."* Refuted: census delta single benign line,
  probe 0, custom tables bite only when pointed at the rule (E8, EX-06).
- *"A conforming text cannot simultaneously hold all four components."* **Refuted by
  construction**: E7 (fixed variant) passes every check, including 0 new form flags.
- *"The audits are vacuous."* Partially sustained as coverage: probe table has no
  rule-#14 entry (blind by design); RV-2's flags do not cover content (resolvability ≠
  content, CR-1 A3); no instrument enforces the discipline (L9). All named.
- *"My own harness is right because I wrote it."* Tested: my first RV-2-tool run on an
  uncommitted tree mis-read the base revision — caught, corrected, disclosed (L7);
  my citation CITE regex misses `.ufo/...`-prefixed paths (documented in E-number
  method notes; RV-2's tool covers them).
