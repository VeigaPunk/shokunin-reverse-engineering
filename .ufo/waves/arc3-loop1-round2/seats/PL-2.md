# PL-2 seat report — arc3-loop1-round2, chain c2, role planner

Seat PL-2 | chain c2 | role planner | task: plan the merged census v11
(H1 missing-file guard + H3 positive floor) — declared FAIL classes, exit
codes, fixture list, header recording; artifact `claims/c2/PL-2/plan.md`.

Timing note: the designated implementer (EX-16) landed the edit while this seat
was still reading the upstream patch texts, then re-landed it twice more. This
plan is therefore a design-of-record *plus* as-built verification: every
statement is sha-anchored, and the mid-wave churn is itself a reported finding
(§4, F0). No clarifying question was asked; the work proceeded on measurements.

## 1. Work performed (evidence pointers)

- Read: frozen claims (`claims-frozen.md:34-50`), both round-1 patch texts
  (`claims/c3/RV-11/proposed-missing-file-guard.patch.md`, `claims/c3/CR-5/
  proposed-g2-positive-floor.patch.md`), the live instrument end-to-end
  (v10 `6f1d19ff…`, 490 lines), the round-1 c3 verdict H-item inventory
  (`claims/c3/verdict.md:40-95`), SCORECARD recipes + arc3-loop1-round1 section,
  round-1 cross consistency, and the live round-2 peer artifacts (EX-11 runner,
  EX-14 floor scoping, EX-17 before-receipts, EX-21 scope auditor, RV-6 before
  copy, RV-8 review harness + report).
- Established the re-anchor fact: both patch texts cite the superseded v9
  (`36e96cd5…`, lines 382-398); in v10 the targets sit at `:438-447` and `:453`
  — verbatim application would mis-apply.
- Authored the plan: `claims/c2/PL-2/plan.md` (sha256 `2ff75ed5…`), containing
  the revision banner (§0), design of record (§3), exit-code decision (§4),
  fixture list (§5), findings F0-F10 (§6), certificates (§7), handoff (§8).
- Built and ran an independent fixture matrix: `claims/c2/PL-2/tools/matrix.py`
  (sha256 `82296672…`), outputs under `claims/c2/PL-2/receipts/` (`matrix.txt`
  for r1 `82fb807e…`, `matrix-c95a5cf3.txt` for the transient, `matrix-final.txt`
  for r3 `df9ffdf9…`), plus `head-text-delta.txt`, `json-key-delta.txt`,
  `invariance-*.txt`, `scope-*.txt`, `artifact-shas.txt`.
- Reviewed EX-16's receipts (`claims/c2/EX-16/receipts/{before,after}/`,
  `after-sha256.txt` — which still cites r1, see §4/F0) and EX-14's
  `proposed-h3-floor-scoping.patch.md` + `floor-probe.out` (their Trap 1
  predicted the r2 regression this seat then measured live).
- Scratch only in `/dev/shm/pl2` (`/tmp` untouched). This seat wrote nothing
  outside its seat report and `claims/c2/PL-2/`; the real target was written
  only by EX-16.

## 2. Proposed changes

- Target `.ufo/gates/c1-census-v10.py`: **none pending** from this seat — the
  landed r3 semantics match the design of record, and the matrix is green.
  Verbatim patch texts are deliberately NOT proposed: both are stale-anchored
  (§1) and the merged form has landed. Open text nits only (plan §6, F1/F9:
  docstring title/usage still say v9; the "Still named, NOT closed here"
  paragraph is duplicated in the header) — recommended only as piggy-back on any
  other required re-land, never for cosmetics alone.
- Plan artifact: `claims/c2/PL-2/plan.md` (contains the header-recording spec:
  origin + before-sha, classes with load-bearing fixtures, exit map, residuals
  H2/H4 + partial blindness, standing rule for appended text, no self-hash).

## 3. Before→after measurement for the chain's claim (census fail-closures)

Baseline: `.ufo/gates/c1-census-v10.py` sha256 `6f1d19ff4b0878…` (RV-6 before
copy, verified against HEAD `14b1682`). After: the wave landed four revisions
in ~9 minutes — r1 `82fb807e…` (560 lines, tree floor), transient r2
`c95a5cf3…` (claim-breaking false FAIL, below), r3 `df9ffdf9…` (601 lines,
per-file det floor), r4 `a4c16763…` (**603 lines, the live file at handoff,
text-only over r3**; re-verified at my own hand: HEAD PASS, H1 FAIL
`UNREADABLE`, nullskill FAIL `BLIND-INSTRUMENT`, invariance HOLDS, creep 0).
Receipts: `receipts/{matrix.txt,matrix-c95a5cf3.txt,matrix-final.txt,
matrix-final2.txt,live-target-sha-final.txt}`; r4 was copied by sha into
`/dev/shm/pl2/snap/final-a4c16763.py` before the final verification.

```
$ python3 <v10> --root <root-with-SKILL.md-absent> --quiet        # H1
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)  exit=0   <- hole
$ python3 <r3>  --root <same> --quiet
UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']
DECLARED FAIL CLASSES: ['UNREADABLE']
VERDICT: FAIL  (…)  exit=1

$ python3 <v10> --root . --quiet     # H3 (PIN/VER/PTR neutered copy, same root)
G2 positive-assertion guard: ok | VERDICT: PASS  exit=0                  <- hole
$ python3 <r3>  --root . --quiet     # neutered copy
G2 positive-assertion guard: SUSPECT (current-ok loci per file: …=0, …=0, …=0)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT'] | VERDICT: FAIL  exit=1

$ python3 <r3> --root <repo> --quiet                                # ordinary
G2 … ok (per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3) | VERDICT: PASS  exit=0
```

Fixture matrix (v10 vs r3, `receipts/matrix-final.txt`): H1 family (absent /
0-byte / 5-line truncation / EACCES / is-a-directory) all v10 PASS → r3 FAIL
`UNREADABLE`; H3 family (all needles neutered, REA_GATE narrowed) v10 PASS →
r3 FAIL `BLIND-INSTRUMENT`; the r3 floor additionally fails `nullskill`
(present, readable SKILL.md with needles stripped — v10 and r1 PASSED); DATED-
bearing files keep their marker scope-errors and gain the class; empty root →
classes `[UNREADABLE, BLIND-INSTRUMENT]`; PIN-only narrowing stays PASS (named
residual). Parity: HEAD run PASS 0/0/0/0; 13/13 shared `--json` keys equal to
v10 at HEAD (4 keys added); HEAD text delta exactly 3 lines, verdict line
byte-identical (`receipts/head-text-delta.txt`). Certificates at r3:
EX-21 invariance `HOLDS`, EX-21 scope-audit rows 20/20 with all detector
constants `same` and `CREEP FLAGS: []`, CR-5 `scope-diff.py` flags `[]` exit 0
(`receipts/{invariance-final,scope-compare-final,scope-diff-final}.txt`). Seven
historical trees: identical verdicts v10↔r3 (6 FAIL / 1 PASS — no regression).
Verdict: claim's after-state reproduced at my own hand; scope bounds byte-stable
(creep audit 0 flags); H4 residual stays named with the external audit green.

## 4. Attacks/refutations attempted (verdicts)

| # | Attack | Verdict |
|---|---|---|
| A1 | "Both round-1 patch texts can be applied verbatim" | **REFUTED** — stale v9 anchors (`:382-398`); re-anchor required (plan §1) |
| A2 | "The per-file floor revision is safe" | **REFUTED, measured live**: r2 `c95a5cf3…` made the ordinary HEAD run FAIL exit 1 `['BLIND-INSTRUMENT']` (SKILL.md has 0 current-ok *blocks*, 3 *dets*) and broke EX-21 invariance (3 diffs) — the claim's "ordinary runs at HEAD stay PASS 0/0/0/0" broken for ~1 minute of wave time; fixed in r3 by the det unit (plan §0, F0) |
| A3 | "v11 still lets a readable file collapse to zero loci" | **UPHELD for r1** (nullskill PASS), **REFUTED at r3** — per-file det floor now fails it (F10; beyond the frozen claim) |
| A4 | "v11 catches narrowing (partial blindness)" | **REFUTED, honestly**: PIN-only narrowing (cD1b) and h3-blind-pin stay PASS; that is the named H4 residual, covered only by the external diff audit (plan F5) |
| A5 | "The instrument edit creeps scope" | **REFUTED** by two independent auditors (identical scope-literal sha `000b74e2…`, 20/20 rows, detectors `same`, flags `[]`) |
| A6 | "Old trees regress under the new prongs" | **REFUTED** on the 7 materialized historical trees (verdict parity); class composition changes only where the tree is short (UNREADABLE added) |
| A7 | "The new code can crash on the unreadable path" | **REFUTED** for r3 (`counts` `None` guarded in the printer/arith; text and `--json` both exercised); flagged as a consumer-contract note for out-of-tree readers (F2) |
| A8 | Symlink swap / line-count-preserving blanking / inode-dedup root | **NOT ATTEMPTED** — handed to verifiers with explicit definitions (plan F8) |

## 5. Blockers

None. Live-target churn (five landings in ~10 minutes; the final bytes were
re-verified at handoff — see the revision list above) is not a blocker but
carries a handoff requirement: **EX-16's `after-sha256.txt` and after-receipts
cite r1 `82fb807e…` and predate r2→r5; they must be re-derived at the final sha
before the records commit** (C1 rule-#14 discipline; plan §0/§8). Verifiers
should re-run any receipt captured against r1/r2.
