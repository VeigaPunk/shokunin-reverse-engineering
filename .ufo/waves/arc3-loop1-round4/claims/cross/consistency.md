# Cross-chain consistency sweep — arc3-loop1-round4 (SEAT CN-1, chain cross, connector)

Scope (frozen seat line): the three chains' readings must not contradict —
(i) command A baseline at HEAD `015e1ba` (83/83, 14/14), (ii) custody digests,
(iii) census/probe states. Reconcile or flag here.

Method: every shared reading was re-derived by CN-1 from the instruments
themselves, and every *landing* was simulated on scratch copies (repo tree
never edited). Scratch `/var/tmp/cn1-arc3r4` and `/dev/shm` only; custody paths
opened read-only; no git mutation in the repo (scratch fixtures are their own
throwaway git repos). No LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README
writes by this seat.

Receipts: `claims/cross/CN-1/receipts/` (`baseline-pins.txt`,
`census-head.out`, `probe-head-strict.out`, `custody-t0.txt`, `poll.log`,
plus per-experiment census outputs).

## 1. Baseline — the shared numbers (all CN-1 first-hand, at HEAD `015e1ba`)

| Reading | Command | Result |
|---|---|---|
| HEAD | `git rev-parse HEAD` | `015e1bab914713568f339fd53999bc180459cc40`; worktree dirty only in ` M .ufo/waves/arc2-loop1-round10/C3.md` (pre-existing) + untracked wave tree |
| command A (SCORECARD recipe A, `REV=015e1ba`) | verbatim recipe | `{"coverage_score": 10.0, "depth_score": 10.0, "dangling": [], "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "015e1ba", "rule_blocks": 14, "citation_resolved_rules": 14}` → **83/83, 14/14** |
| census (`c1-census-v10.py`, `d0772ce8…`) | `python3 .ufo/gates/c1-census-v10.py` | **PASS** `stale=0 ambiguous=0 undeclared=0 unresolved=0`, exit 0; scope-errors `[]`, unreadable `[]`, declared fail classes `[]`; G2 floor PROVINCE=17 / SCORECARD=14 / SKILL=3 |
| citation-drift probe (`e2665074…`, table `1b3ab955…`, expected `9df0452c…`) | default / `--strict` / `--selftest` | `reported findings=0 exit=0`; `clean findings=0 exit=0`; selftest **13/13 CLEAN** |
| custody tool at round start (`7cd19c3c…`, README `f30df42e…`) | `selftest` | 22/22 CLEAN exit 0 (the r3 identity — the C3 "before" state) |
| custody 5-path t0 | read-only sha256 + live verify vs r3 post-pair receipt | devin `16f496e6…`, omp `38d2a1d0…`, kimi `bc66d543…`, bashrc `7d2ca28a…`, profile `6c6be761…`; `verify config-post-pair-v2r3.txt --live --require-paths 5` → **MATCH 5/5 exit 0** |
| prior-83 byte identity | `git show` blob vs worktree, all 83 knowledge files | **0 differences**; `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md` also byte-identical to HEAD |

Every chain's frozen before-state matches these numbers; no chain contradicts
the baseline. (C1 `VZ-1/evidence/baseline-commandA.json` and `RV-2/evidence/commandA-before.txt`
reproduce the same JSON field-for-field; C2's `EX-14/evidence/baseline-census.json`
and C3's `EX-23/before-probe.out` reproduce the census/probe states.)

## 2. Agreement matrix — chain claims vs CN-1 re-derivations

| Shared reading | Chain artifact | CN-1 independent | Verdict |
|---|---|---|---|
| command A before 83/83, 14/14 | C1 `VZ-1/evidence/baseline-commandA.json`, `RV-2/evidence/commandA-before.txt`; C2 draft §C2 bullet; C3 draft §C3 | identical JSON, run on `015e1ba` git objects | **consistent** |
| census PASS 0/0/0/0 at HEAD | C2 `records-drafts/scorecard-section-draft.md` (reports PASS + floor 17/14/3); RV-4 `evidence/census-baseline-realtree.txt` | identical, byte-for-byte on every quoted number | **consistent** |
| probe findings=0 both modes; selftest 13/13; table/expected digests | C1 `VZ-1/evidence/baseline-probe-*.txt` | identical | **consistent** |
| custody tool before = `7cd19c3c…`, selftest 22/22 | C3 `EX-21/sha256s.txt` (r3 revision, 1155 lines) | re-derived: same digest, 22/22 | **consistent** |
| C1 selector recovery K/K | C1 `EX-04/out/verify-report.json`, `EX-05/planted-vs-probe.txt`, entry draft | CN-1 re-derived ABI → keccak selectors (pycryptodome) and compared to the probe envelope `probe-6.7.0-hex.json`: **ABI-derived == probe-recovered, 15/15, zero missing, zero extra** | **consistent** |
| C1's entry + map token landing | `records-drafts/knowledge-entry-draft.md` (18,166 B) + `map-token-patch.md` PRIMARY (additive-only) | simulated on a scratch tree: command A → **84/84, missing [], dangling [], 14/14**; prior 83 byte-identical (0 diffs); probe `--strict` → **findings=0 exit 0** | **consistent (projection)** |
| C2's PROVINCE repairs | `records-drafts/scorecard-section-draft.md`: 7 stale → 0, same-line (162→162), census PASS at patched tree | independently reproduced: line-neutral rewrite on scratch → census PASS 0/0/0/0; probe clean | **consistent** |
| C3's live revision | tool `29bb45ae…` (1343 L), README now `9d9400da…` (272 L), selftest 28/28 | re-derived: selftest **28/28 CLEAN**; live pair `live-pre`/`live-post` verify **MATCH 5/5**; `live-post --live --require-paths 5` → **MATCH 5/5 exit 0**; probe `--strict` against a fixture carrying the revision → **findings=0** | **consistent** |

## 3. Cross-chain coupling experiments (each run, not asserted)

All experiments use scratch git fixtures carrying the probe's 26 target files at
their current bytes (probe baseline in that fixture: findings=0 both modes).

### 3a. C1's README edit: line-neutral passes, row insert reddens 5 entries

| variant | README lines | probe result |
|---|---|---|
| control | 190 | clean, findings=0 |
| **line-neutral token append** (PRIMARY form) | 190 | **clean, findings=0** |
| row insert (new physical map row) | 191 | **failed, findings=5**: `sc69-readme-177`, `sc72-readme-nitrow`, `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2` all `citation_dead` |

The freeze's "line-neutral map token" clause is load-bearing, not cosmetic.
CN-1's measurement extends the r3 finding: the row insert now reddens **five**
entries (r3 measured three) — the `sc69`/`sc72` pair joined when round 2-3
landed their own README-pinned rows.

### 3b. C2's PROVINCE repairs: only exact line-neutrality is safe

| variant | PROVINCE lines | census | probe |
|---|---|---|---|
| line-neutral rewrite (3 lines → 3 lines) | 162 | **PASS 0/0/0/0** | clean |
| +1 net (4-line replacement) | 163 | **FAIL** — `PROVINCE.md:119 marker 'verified 2026-10-13' absent` → scope-error, exit 1 | clean |
| +1 above, −1 at EOF (compensating, total 162 held) | 162 | **FAIL** — same :119 marker error (the marker row itself moved) | clean |
| +3 shift above the safety clause | 165 | — | **failed, findings=1**: `shonen-province-range` — SHONEN:12 cites `PROVINCE.md:88-116` and the safety clause moved out of it |

Consequence: "line count held" is necessary but **not sufficient** — the shift
must be zero above every DATED marker line (40/45/119) *and* above the
safety-clause region the SHONEN range cites. C2's own draft names both
constraints; CN-1 reproduces each with a counterexample.

### 3c. C2's Frontier repairs are census-invisible in content, and that is fine

The Frontier bullet is not in the census's declared SCOPE table, and its text
does not match `REA_GATE` (no client token), so no content edit there creates a
locus — measured: both my line-neutral variants (receipt-anchored prose; a
version-shaped `solc 0.8.37 / vyper 0.4.3` variant) read PASS. Independently,
C2's RV-4 measured the same blindness (`evidence/census-blindness-proofs.txt`).
The census's PASS therefore certifies locus hygiene only — C2's own draft says
so; the two agree.

### 3d. A census-graded token in any new text fails — the round's repair texts must stay prose-only

| adversarial variant | result |
|---|---|
| `rea-agents@6.7.0` in the line-neutral Frontier text | **UNDECLARED** (block 91-93, scope None) → census FAIL exit 1 |
| `rea-agents@6.5.0` appended to the SKILL.md custody registry row (:390) | **UNDECLARED** (block 390-390) → census FAIL exit 1 (SKILL scope is :10-16/:18-20 only) |

C2's RV-4 ran the same SKILL-row plant independently
(`evidence/attack-skillrow-gated-token.txt` → UNDECLARED=1, exit 1). Both
chains' texts are pin-free by construction; the constraint is real, measured,
and satisfied.

### 3e. C3's README rewrite and registry row

- The live revision's README keeps all four probe anchors
  (`MTIME_UTC_RENDER`, `Rewrite identity is \`INODE\` + \`CTIME\``, `Severity
  precedence for the verdict of a \`verify\` run`, `never \`/tmp\``): probe
  clean on the fixture. Adversarial control: dropping the `never \`/tmp\``
  phrase reddens `custody-readme-scratch-never-tmp` (failed, exit 1) — the
  anchor is live.
- The registry row's precedence needle
  (`precedence CONTENT-DRIFT > (UNEVALUABLE > )?ABSENT > …`) survives the row
  revision; verified by direct match against the current SKILL.md row.
- The (d) ruling text is landed in the README (`## The both-absent MATCH
  (ruling, arc3-loop1-round4)`), with the declared design stated: only
  error-carrying stanzas are UNEVALUABLE; a cleanly-absent both-sides stanza is
  a MATCH on recorded existence, and one-sided absence is still ABSENT 13.

## 4. Divergences and flags

**F-1 (flag, repair exists — application is the parent's): the SKILL.md registry
row still declares "22 fixture cases" while the tool and README now run 28.**

- Measured state: SKILL.md:390 (blob `5eec51c0…`, unchanged since HEAD) contains
  `selftest\`; 22 fixture cases`; the tool prints `CUSTODY_PAIR_SELFTEST: CLEAN
  cases=28 passed=28 failed=0 exit=0`; the README's Selftest section declares 28
  with the six round-4 case names. No instrument grades this cell (the row is
  outside the census's SKILL.md scope :10-16/:18-20; the probe's custody-row
  anchor pins the precedence phrase, not the count).
- **The fix is already drafted and CN-1 verified it sound**:
  `claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md` +
  `patch/skill-registry-row.patched.md` (`8e56f3d9…`, 390 lines — exactly one
  differing line, :390; count cell reads 28; precedence needle intact). CN-1
  applied it on a scratch root: census **PASS 0/0/0/0** (SKILL.md loci 2, same
  as HEAD); probe `--strict` against a fixture carrying it: **findings=0 exit 0**.
  The patch text's own declared row digest `8f8e5408…` is the newline-inclusive
  hash (verified; the no-newline hash is `52824e8e…`).
- Therefore the C3 claim's "registry row + README re-derived same-commit" clause
  is met **only if the parent applies this patch in the coupled landing**. C3's
  own verdict (`claims/c3/verdict.md` §R1) names the same leg as uncovered. No
  contradiction between chains — a shared, verified landing requirement.

**F-2 (flag, informational): the round-3 landed README wording is the base for
the round-4 rewrite.** The README at HEAD is `f30df42e…` (185 L); the live
revision reads 272 lines with the round-4 section. Both are internally
consistent; no contradiction — recorded because the receipt pair self-pins
`29bb45ae…` and the README changed twice after my first read (13:09→13:12Z
window), so the final identity must be re-derived at the records commit per
rule #14.

**F-3 (reconciliation, not a contradiction): the census's UNREADABLE class
fired live in CN-1's own scratch.** Running the census against a scratch root
without the three scoped files reads `UNREADABLE` + marker-uncheckable
scope-errors → FAIL exit 1. That is the arc3-r2 H1 fail-closure working as
designed; it also means any scratch-root census run must carry all three scoped
files (C2's EX-14 reached the same conclusion independently).

**F-4 (honest note): the "custody digests" leg of my seat line is verified
against the r3 post-pair receipt, not a round-4 pre-pair.** At my first read
the round-4 pre-pair had not been captured (the wave's own C3 chain captures
it). The r3 post-pair re-verifies MATCH 5/5 live at 14:10Z, so there is **zero
custody drift since 13:17:23Z**; the round-4 pair (`EX-21/receipts/live-pre.txt`
/ `live-post.txt`, self-pinning `29bb45ae…`) also verifies MATCH 5/5. Both
readings agree.

**F-5 (coupling, reconciled — not a contradiction): C2's PROVINCE repair asserts
C1's outcome, so the two must land together.** EX-14's complete candidate patch
(`claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md`) rewrites
the Frontier EVM bullet to "…real solc-0.8.37 carriers (Core, arc3-r1/r3) and
**Vyper 0.4.3 (r4) held**…". CN-1 applied the patch on scratch: all 11 anchor
lines unique, PROVINCE 162 → 162, census **PASS 0/0/0/0**, probe `--strict`
clean. But the "Vyper 0.4.3 (r4) held" clause cites a leg whose corpus entry is
still staged as patch text (`claims/c1/records-drafts/knowledge-entry-draft.md`,
stem `2026-10-19-arc3-r4-evm-vyper-leg`; `corpus/knowledge/` is still 83 files at
HEAD). The patch text itself discloses this and prescribes the fallback: if the
repair lands **without** C1's entry in the same commit, the clause must drop back
to the solc-only form. Landing both in one commit is the intended coupling —
consistent with C1's claim (entry + token) and C2's claim (repairs), and the only
cross-chain ordering constraint the round has.

**F-6 (divergence, resolved by measurement): C2's records draft claims "stale 6 → 0",
but the first complete patch (v1) drives only 6 → 2.** CN-1 reproduced the
divergence first-hand:

- VZ-2's chain verdict reads **NOT-VERIFIED**: its census (26 rows) is
  `stale=6` (F1b, F3, F5b, X1, C1, R2), and v1
  (`8a0e12ff…`) repairs 4 — **F3** (`JEB (unprobed)`) and **C1** (the Core
  host-tools row naming `7z`/`xxd`/`radare2`/`strace`/`upx` as absent) survive
  verbatim. CN-1 re-ran VZ-2's census script on the real tree: **SUMMARY: total=26
  stale=6 adjudicated=2 current=18 — reproduced exactly**; and on my own v1-patched
  copy: the two literals still present at :88 and :62.
- The records draft (`scorecard-section-draft.md`, revised to "6 → 0") and the
  LOG draft ("After: stale 6 → 0") therefore overstate the v1 patch's coverage.
- **Resolution measured by CN-1**: EX-14's **v2** candidate
  (`candidate-complete-frontier-repair.v2.patch.md`, `0b8ad045…`, 13 −/13 + lines)
  repairs **all six**: every stale literal gone, every replacement present,
  PROVINCE 162 → 162 (`69ceea9b…`), census **PASS 0/0/0/0**, probe `--strict`
  **findings=0**. It also drops v1's content defect (the false `(Core, arc3-r1)`
  promotion) and states `RESULT-class` instead.
- Note on the census script: VZ-2's `province-staleness-census.py` prints
  hardcoded verdicts (it re-checks only anchor presence), so it reads "6 stale"
  even on a fully repaired tree — the acceptance evidence for the repair set is
  the clause-level audit above, not that script's summary line.
- Consequence: C2's claim verifies **only if the parent lands the v2 patch**
  (and C1's entry in the same commit per F-5). Landing v1 as-is leaves the claim
  at 6 → 2 — not the "N → 0" the frozen claim requires.
- **Residual pointer check (carried to the parent):** three downstream records
  still describe the pre-v2 state, each written before or within seconds of v2's
  landing (11:14:53Z) — they are **not** contradictions, but they must not be
  quoted as the round's final state:
  (i) CN-2's `records-outline.md` §R6 (line 32) and §236 cite the **v1** path as
  the parent's apply target;
  (ii) VZ-4's `wave-summary.md` §C2 reads "**NOT-VERIFIED (stale 6 → 2, not 0)**"
  and cites v1 `8a0e12ff…` (mtime 11:15:10, 17 s after v2 landed);
  (iii) the same summary's admission input offers "extend the repair patch to F3
  and C1" — which is exactly what v2 already does, measured by CN-1 above.
  The v2 file (`…v2.patch.md`, `0b8ad045…`) is the recommended candidate per
  EX-14's own apply-and-census.md (`:90-93`, `:199`, `:364-365`); landing v1
  would leave the claim at 6 → 2.

## 5. Consistency verdict

- Command A baseline: **agreed by all three chains and re-derived** (83/83,
  14/14, missing [], dangling [], 10.0/10.0 at `015e1ba`).
- Custody: **no drift**; r3 post-pair and the round-4 pair both verify MATCH
  5/5; the round-4 tool revision self-pins correctly.
- Census/probe: **PASS / findings=0 at HEAD**, and each chain's landing
  simulation keeps them so — **provided** (a) C1's README edit is line-neutral,
  (b) C2's PROVINCE repairs are exactly line-neutral with zero net shift above
  the DATED markers and the SHONEN-cited safety range, (c) every new text stays
  free of census-graded tokens, (d) C3's registry row count is refreshed in the
  coupled landing (F-1).
- No chain contradicts another on any shared reading. The single actionable
  divergence is F-1 — its repair is drafted, verified sound by CN-1, and pending
  only the parent's application in the coupled landing. The one cross-chain
  ordering constraint is **F-5** — C1's entry/token and C2's PROVINCE repair must
  land in the same commit (or C2's Vyper clause drops to the solc-only form).
