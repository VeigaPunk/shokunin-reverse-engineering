# SEAT VZ-1 | CHAIN c1 | ROLE convergence — arc3-loop1-round2

Window 2026-10-19T12:01→12:58Z (09:01→09:58-03). Lane HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420` at every sample (`git rev-parse HEAD`,
re-checked at each phase). This report, `claims/c1/VZ-1/{verdict.md,evidence/}`
and the byte-identical mirror `claims/c1/verdict.md` are this seat's only writes.
No git mutations in the lane repo (the only `git init/commit` runs are in scratch
copies under `/dev/shm/vz1r2`); no LOG/SCORECARD/SHONEN/corpus/SKILL/README edit;
custody paths not opened, hashed, or touched; no probes, no installs, no evidence
ids minted. Scratch: `/dev/shm/vz1r2` only (never `/tmp`; standing EDQUOT record).

## 1. Work performed (evidence pointers)

- **Polled the wave** per the seat line: own 60 s poller, 25 samples
  12:01:03→12:26:03Z (log preserved at `claims/c1/VZ-1/evidence/poll.log`,
  seats 0→35, c1 dirs 0→11), plus targeted re-lists to close; seats/ reached
  62/64 delivered by my close. No seat blocked on me; I blocked on none.
- **Reconciled all 12 c1 seats** into `claims/c1/VZ-1/verdict.md` (mirrored
  byte-identical at `claims/c1/verdict.md`; sha256
  `5a62eac278a2bc0e054fba59f52c4516038124dac28842c6c513bb4b7b2ce660`): claim
  component table (C1-a…C1-d), candidate matrix, per-seat table, E1-E11
  first-hand measurements, debts L1-L10, integration conditions 1-5, attack log.
- **Measured first-hand, independently of seat reports** (not taken from prose):
  before-state recipe A at HEAD (E1); the full candidate matrix on committed
  scratch trees — EX-01 rev A (payload 896 B `a47dc38d…` → 385 L `19057c13…`),
  **EX-01 rev B** (payload 1,071 B `6cc388cb…` → 387 L `a8170b96…`, rule
  :240-254), PL-1 v5 (`git apply` of its own diff → 395 L `11647e6d…`), CR-1 T5
  (block 1,044 B `c829478b…` → 386 L `8ab17e6b…`), and **a conforming fixed
  variant** built by applying RV-2's one-sentence citation rewrite to rev B
  (payload 1,129 B `7e76e2e7…` → 388 L `60dfbe02…`, verifier **PASS**, 0 new
  form flags) — E2-E7; census with the committed instrument `6f1d19ff…` on HEAD
  and every applied tree (PASS 0/0/0/0; delta = the single benign
  `SKILL.md 371→385/387` line) — E8; citation-content match on all rev-B
  citations — E9; RV-2's audit baseline + hygiene finding — E10.
- **Built seat-side verification tooling** (scratch, `/dev/shm/vz1r2`):
  `verify_rule14.py` — pure-insertion subsequence proof (`before == after[:k] +
  after[end:]`), command A on a fresh scratch commit, prior-13 rstrip-normalized
  block compare, census-needle scan of the inserted slice, rule-#11-form
  heuristic, per-citation resolvability; plus runs of RV-2's audit tool and
  EX-05's census-delta on the same trees.
- **Cross-checked and corrected a harness error of my own**: my first
  RV-2-tool run on an applied-but-uncommitted tree graded the base revision;
  caught, re-committed, re-ran (named as debt L7 in the verdict — a hygiene
  note for the integrator, not a peer defect).
- **Reconciled the mid-wave churn**: EX-01's artifact was revised v1→v2 at
  12:13:36Z with a brief stale-sidecar window (12:14Z, EX-05 A6), closed by
  EX-01's re-derivation at 12:14:21Z; my rev-A measurements are marked superseded
  in the verdict (L2). RV-2's EX-01 audit graded rev A; my E3/E7 extend it to
  rev B and the fixed variant.

## 2. Proposed changes

- **`claims/c1/VZ-1/verdict.md`** (+ mirror `claims/c1/verdict.md`) — the
  deliverable; a verdict document, not a repo patch. It requires one landing
  choice among delivered conforming texts (recommended: EX-01 rev B + RV-2's
  `proposed-rule14-citation-form.patch.md` rewrite — measured by this seat at
  `7e76e2e7…`/`60dfbe02…`, all checks PASS) and names the same-commit SHONEN
  refresh plus the records instructions. No patch text of my own is proposed for
  any repo file: the c1 landings belong to EX-01/PL-1 (patch texts already
  landed) and the round records to the parent.
- Evidence written by this seat: `claims/c1/VZ-1/evidence/` — `poll.log`,
  `verify-{ex01b,pl1,t5b,fix}.json`, `rv2-audit-{ex01b,pl1c,t5b,fix}.json`,
  `payload-EX01-revB.txt`, `payload-revB-fixed.txt`,
  `census-head-{base,ex01,ex01b}.json`, `census-delta-committed-instrument.txt`,
  `census-delta-revB.txt` (13 files, all first-hand outputs).

## 3. Before → after measurement for the chain's claim (commands + outputs)

Chain claim (frozen): queue-drain rules 13→14, 14/14 citation-resolved at the
work commit, prior 13 rules byte-identical, citations in rule-#11 form.

| Check | Before (HEAD `14b1682b`) | After (my committed scratch trees) |
|---|---|---|
| command A (recipe verbatim) | `{"citation_resolved_rules": 13, "rule_blocks": 13, "mapped": 82, "knowledge_files": 82, "missing": [], "dangling": [], "coverage_score": 10.0, "depth_score": 10.0}` | rev B `{"citation_resolved_rules": 14, "rule_blocks": 14, "mapped": 82, …}`; identical 14/14 on rev A, PL-1, T5, fixed trees |
| pure insertion / prior 13 | — | `before == after[:k]+after[end:]` True (zero modified bytes) on every candidate; rstrip-normalized 13/13 True; raw block-split 12/13 is a separator-attribution artifact (L4) |
| census (committed `6f1d19ff…` bytes, `--root`) | `PASS 0/0/0/0`, `SKILL.md 371/loci 2` | rev B: `PASS 0/0/0/0`, `SKILL.md 387/loci 2`; delta (EX-05 tool) = one benign line `SKILL.md 371→387`, `DELTAS=0` |
| citation-drift probe | `findings=0 exit=0` | patched trees `findings=0` (my rev-A run; CR-1 + EX-06 peer runs on rev B) |
| citation resolvability (RV-2's tool, committed trees) | 13 rules, 55 cites, 54/54 in-repo, 0 dead, 1 flag (pre-existing rule #12) | rev B: 60 cites, 59 resolved (1 custody stat-only), **0 dead, 2 flags** (rule #12 + rule #14's `SCORECARD.md:1366-1368`); **fixed variant: 0 dead, 1 flag (rule #12 only)**; PL-1 v5: 1 dead (`claims/c1/verdict.md` shorthand); T5: 1 dead (wrapped path) |
| needle scan of added text | — | 0 loci on every candidate (census vocabulary + unit gate) |

Verdict components: C1-a PASS (tree), C1-b PASS (tree; work-commit number owed),
C1-c PASS as pure insertion + normalized 13/13, C1-d **conditional** — fails on
EX-01 rev B as written (1 flag), passes on the fixed variant (measured PASS).
Headline: **VERIFIED, conditional on landing a rule-#11-conforming text**;
landing rev B verbatim = C1-d NOT-VERIFIED.

## 4. Attacks / refutations attempted (with verdicts)

| Attack | Method | Verdict |
|---|---|---|
| "The after-state is asserted, not measured" | applied every candidate to committed scratch trees; two parsers (mine + RV-2's) | **refuted** (numbers reproduced; E2-E7) |
| "A conforming text cannot hold all four components at once" | built rev B + RV-2's rewrite and measured it | **refuted** — verifier PASS, 0 new form flags, 0 dead (E7) |
| "The count discriminates craft" | decoration control (CR-1 T3 / EX-02) passes 14/14 | **sustained as a metric limit** — the receipted incident + replay carry the verdict (verdict attack log) |
| "The rule's own artifact was not subject to its rule" | tracked v1→v2 + sidecar timeline | **sustained once (12:14Z window), closed 12:14:21Z** by EX-01's re-derivation (L2) |
| "The append moves an instrument or widens scope" | census + probe + delta on every tree; scope constant checked | **refuted** — no locus added, no scope move, table untouched (E8) |
| "The audits are vacuous" | probe blind to rule-#14 citations by table design; census blind to stale identity (EX-03 B) | **partially sustained / named** — L9: discipline is reviewer-enforced + mechanized replay, not instrument-enforced |
| "My own harness is right because I wrote it" | my uncommitted-tree audit mis-read the base revision; my CITE regex misses `.ufo/`-prefixed paths | **sustained against myself**; corrected/disclosed (L7, method notes) |

## 5. Blockers

- None for this seat. Named for the parent (all in the verdict): **L1** landing
  choice (rev B as-written fails C1-d; conforming options measured), **L3**
  `SHONEN.md:6` stale + three divergent end numbers (252/254/265) — recompute
  from landed bytes in the same commit, **L5** census-instrument churn (pin the
  sha per reading; my readings used the committed `6f1d19ff` bytes; re-run after
  C2's v11 lands), **L6** undelivered at my close: **VZ-4 (cross)** (RV-9/VZ-2
  landed late, unreconciled here). The work commit does not exist yet: every
  after-number above is tree-level; the integrator owes command A (14/14, 82/82),
  the census/probe re-runs, the landed SKILL.md identity, and the SHONEN refresh.
