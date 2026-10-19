# C2 verdict — census fail-closures (H1 + H3), chain convergence, seat VZ-2

Wave arc3-loop1-round2 · chain c2 · 2026-10-19 · repo HEAD `14b1682` (no seat
commits; parent integrates records after the wave).
Target: `.ufo/gates/c1-census-v10.py` (path unchanged; revision identity is the
hash, not the filename).

Revision timeline (every claim below is bound to a sha256; the target moved
eight times inside ~15 minutes — CR-2/evidence timeline, RV-5 fixtures.sha256,
EX-16 §1/§5):

```
before (round-1 landed, HEAD blob)  6f1d19ff…  490 L  08:31 −0300  (copy: claims/c2/VZ-2/before/, tools/census-before.py)
intermediates (superseded)          2a89793a → 82fb807e (560 L) → 09e270c2 → c95a5cf3 → df9ffdf9 (601 L) → a4c16763
AFTER (this verdict is pinned to)   d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5  610 L  09:18:14 −0300
```

Identity discipline (rule #14) applied to the landing: EX-16's
`receipts/after/after-sha256.txt` was re-derived at the final bytes (captured
2026-10-19T12:18:18Z, `d0772ce8…` / 610 L), and I re-verified the ordinary-run
stdout digest at the final bytes: `1db2ec31e8f8896031f1f80a2d90f7e2801af645c4f685d2c55100534d1b7cc0`
— byte-identical to EX-16's receipt and to the `df9ffdf9` intermediate, i.e.
the last two edits are doc-only and behaviour-neutral. The landed file utters
no self-hash (grep `df9ffdf9|82fb807e|7b5a0e88|c95a5cf3|601 lines` → no hits).

## Verdict: **VERIFIED** (pinned to `d0772ce8…`)

Every measured clause of the frozen C2 claim holds on the final landed bytes and
was reproduced independently at this seat's hand (battery, creep audit, records
simulation, plus the reconciliation of 25 landed C2 seat reports). Two caveats
are named, neither contradicting the claim: (a) the **mid-wave defect** — the
intermediate per-file-floor revisions (`c95a5cf3`, `09e270c2`) broke the
ordinary-run invariant (block-unit floor false-FAILed HEAD; EX-14 §3, CR-2 A6,
PL-2 A2, RV-6 A6); it was caught in-wave and fixed at `df9ffdf9`, and the final
revision is what this verdict pins; (b) the claim's "after the round's commit"
clause is **pre-flighted, not committed** — parent-side, simulation below.

## Claim components — status and evidence (final bytes)

| # | Claim clause (claims-frozen.md:44-50) | Status | Evidence (this seat unless noted) |
|---|---|---|---|
| 1 | FAILs with a declared class when a scoped file is absent | **DELIVERED** | absent SKILL → `FAIL` exit 1, `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']`, `DECLARED FAIL CLASSES: ['UNREADABLE']` (`final/t1-absent-skill.out`); absent PROVINCE / SCORECARD / all three: same class, every file named (`final/t11`, `t12`); variants zero-byte / truncated / directory / EACCES all FAIL `UNREADABLE` (`final/t2`, `t9`, `t10`); converges with EX-16 `h1-*` receipts, EX-12/EX-17/CR-3 measurement, CR-2 A2/A5, EX-18 §3, EX-19, EX-25 |
| 2 | FAILs when its positive-floor assertion finds zero loci in a non-empty scope | **DELIVERED** | needles neutered → `FAIL` exit 1, `G2 … SUSPECT (current-ok loci per file: PROVINCE.md=0…)`, `['BLIND-INSTRUMENT']` (`final/t5`); floor is per-readable-file over current-ok **detections** (final header; REFUTED alternatives recorded: per-row floors, per-file block floors — CR-3 unit table, EX-14 map); non-vacuity: RV-3 reversed only the H1 verdict term → guard reports but does not fail (load-bearing link), RV-4 reverted only the floor → blind PASS returns |
| 3 | every round-1 silent-PASS injection now reproduces as a declared FAIL | **DELIVERED for the two named classes — reading stated** | H1 family: 5 injection shapes flip silent-PASS → declared FAIL; H3: full-neuter and `REA_GATE`-neuter flip (`final/t5`; RV-4 A3; EX-16 matrix "10 cases flipped 0→1"). Round-1 injections outside the two patch texts stay as they were and are named below (H2, H5, t5-dated-shelter, partial-needle narrowing, H4) — the frozen text itself keeps H4 open, so "every" cannot include them |
| 4 | ordinary runs at HEAD stay PASS 0/0/0/0 | **DELIVERED at `d0772ce8`** | `final/t0-baseline.out` + live root `final/ordinary-full.txt`: `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0; counts 162/6, 1417/9, 371/2; floor line `current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file`; stdouts sha `1db2ec31…`; **not held at `09e270c2`/`c95a5cf3`** (mid-wave defect, fixed) |
| 5 | scope bounds otherwise byte-stable (creep audit 0 flags) | **DELIVERED** | CR-5 `scope-diff.py` `6f1d19ff → d0772ce8`: `rows before=20 after=20 / ADDED 0 / REMOVED 0 / CHANGED 0 / CREEP FLAGS: []` (`final/scope-diff.txt`); converged: RV-6 own auditor (scope-literal sha `000b74e2…`, 20/20 rows, 12-fixture non-vacuity), PL-2 A5 (two independent auditors), EX-21/EX-23 |
| 6 | H4 self-certification residual stays named; external diff audit is the chain's certificate | **DELIVERED** | the audit above IS the certificate; H4 named in the landed header and by EX-11 §5 / EX-23 §4 / RV-4 A5 / RV-5; measured: a widened instrument still PASSes itself while the differ flags `CREEP wide added DATED row` + `widen-by-add/remove` (EX-16 `h4-scope-diff-widened.txt`); residual is structural — only an external differ can see a shape-preserving widening |

## Before → after injection matrix (this seat's harness, final bytes)

Roots are byte copies of the three scoped files at HEAD (worktree == HEAD blob:
PROVINCE `d075a3c6…`, SKILL `483b0eba…`, SCORECARD `a7c72950…`); custody paths
read-only (anchor re-derivation). `before` = `6f1d19ff…`, `after` = `d0772ce8…`;
re-runnable via `tools/battery.sh <instrument> <tag>` (fixtures: `tools/injections.md`).

| t | injection | before | after |
|---|---|---|---|
| t0 | pristine | PASS 0/0/0/0 | PASS 0/0/0/0, counts identical |
| t1 | SKILL.md absent (H1) | **PASS silent** | FAIL `['UNREADABLE']` |
| t2 | SKILL.md 0 bytes | **PASS silent** | FAIL `['UNREADABLE']` (`0 lines < declared max 20`) |
| t3 | PROVINCE.md absent | FAIL (marker class) | FAIL (marker class + file named) |
| t4 | files empty/gate-free | FAIL (marker class) | FAIL (marker class) |
| t5 | blind instrument (H3) | **PASS silent** | FAIL `['BLIND-INSTRUMENT']` |
| t6 | inline-marker excuse (H2) | PASS | PASS — named residual |
| t7 | gate-free version at EOF (H5) | PASS | PASS — named residual |
| t8 | planted pin in DATED range (CR-5 t5) | PASS | PASS — documented refusal class |
| t9 | directory at scoped path | **PASS silent** | FAIL `['UNREADABLE']` |
| t10 | chmod 000 | **PASS silent** | FAIL `['UNREADABLE']` |
| t11 | SCORECARD.md absent | FAIL (anonymous) | FAIL `['UNREADABLE']` (named) |
| t12 | all three absent | FAIL (anonymous) | FAIL `['UNREADABLE']` (all named) |

## Records-commit pre-flight

Parent appends one records section per chain past the census's fixed bound
(SCORECARD max declared end 855). Simulated at the final bytes: baseline + the
three chains' **literal** sections (C1 85 L + C2 86 L + C3 104 L → 1689-line
SCORECARD) → `PASS 0/0/0/0`, zero loci added, floor satisfied
(`final/records-sim.txt`). Non-vacuity: one planted `rea-agents@9.9.9` in the
appended region → `FAIL undeclared=1` exit 1 (`final/records-sim-control.txt`).
Precision for the parent: the C3 draft's `rea-agents@6.4.0` control-table token
is in its "Notes for the parent" block, not its pasteable section — append the
literal section only.

## C2 seat reconciliation (write time: 29/29 non-VZ-2 reports landed, all read)

Reconciled seats and their products (all read; digests + evidence in the seat
reports themselves):

| seat | role / product | disposition |
|---|---|---|
| PL-2 | planner; plan.md + F0..F8 ledger | plan executed; F0 (receipt re-derivation) discharged by EX-16 at the final sha; A8 hand-offs covered (nullskill/padded-file by EX-16 A4, CR-3) |
| EX-11 | baseline repro + attack matrix | confirmed defects, residuals honest; F1 record nit upheld in part by RV-7 |
| EX-12 | H1 re-anchored hunks + partial-application analysis | anchors stale as reported; closure verified by behaviour |
| EX-13 | pinned R0..R4 matrix | H1+H3 closed at R4; 2 independent creep audits |
| EX-14 | floor unit map + dominant-variant fix; found the c95a5cf3 defect | defect fixed in-wave; its R1..R3 named (ptr-fallback, token≠coverage, SKILL margin) |
| EX-15 | (landed; consistent) | no refutation |
| EX-16 | **implementer**; landed d0772ce8; 24-fixture battery; certificates | landing verified at final bytes; identity receipt fresh |
| EX-17 | rows-beyond-EOF leg measured load-bearing | folded into G19; no refutation |
| EX-18 | H1 matrix over 8 unreadable shapes; JSON consumer view | all classes hold; JSON carries cause |
| EX-19 | 11-variant matrix; pointer-shadowing side finding | full-neuter closed; partial residual named; pointer shadowing reproduced by me at the live config (SCORECARD.md:291) |
| EX-20 | (landed; consistent) | no refutation |
| EX-23 | header/records patch text; superseded draft (token `BLIND`) | landed token is `BLIND-INSTRUMENT`; draft not authoritative (EX-23 §5b); identity/usage nits handed over |
| EX-24 | (landed; consistent) | no refutation |
| EX-25 | citation-drift interlock, probe 13/13, findings=0 | probe clean both before/after; HEAD-vs-worktree limit named (post-commit re-run parent-side) |
| EX-26 | timing/containment; guards cost-neutral (≤32x run) | verdict identical across five revisions |
| SC-2 | scribe (records evidence) | drafts locus-safe; see pre-flight |
| SC-3 | scribe (records text, C2) | drafts complete (evidence manifest 221/221 verified); pasteable sections locus-safe; 25× polls |
| RV-9 | reviewer: ordinary-verdict identity vs pre-edit | REFUTED AS WORDED, SEMANTICS PRESERVED: whole-stdout byte-identity refuted — delta is exactly 4 lines (extended G2 line + 3 declaration lines), none a verdict line; verdict/PASS/counters byte-identical; exemption clause inert on ordinary runs |
| EX-21 | executor: external creep audit of the landed diff | HOLDS: scope-literal sha identical both sides (`000b74e2…`), 20/20 rows, ordinary VERDICT line byte-identical, 1/29 non-scope block changed (main), auditor itself pinned/re-ran |
| EX-22 | executor: round-1 capture reproduction + boundary cases | round-1 capture `3b677b8e…` reproduced byte-identical on the round-1 tree, delta = 3 declaration lines; boundary `130 < max 131` FAIL / `131` PASS; records-append verdict/loci unchanged; two doc-only lags in the landing receipt noted (since re-derived) |
| RV-3 | H1 mutation: guard load-bearing; verdict term the link | confirmed (whole-H1 revert restores silent PASS; verdict-term-only revert reports without failing) |
| RV-4 | H3 mutation: floor sole detector | confirmed; A6 partial blindness bound stated |
| RV-5 | false-positive hunt; 1 mid-flight FP caught; 1 open label defect | confirmed on the pinned landing; label defect named (CR-2 A10) |
| RV-6 | independent creep audit + 12-fixture non-vacuity | confirmed: 0 flags, rows unchanged, final audited revision = final |
| RV-7 | review of EX-11 artifacts | F1 record-honesty nit; classes unaffected |
| RV-8 | review apparatus for EX-23 header text | interim: EX-23's draft is superseded by the landed header; the landed still-named list carries H2/t5/H4 |
| RV-10 | conformance review | CONFORMS on the final revision (re-verified) |
| CR-2 | H1 attack matrix (15 roots) + deltas patch text | no false fire on coherent rename/symlink/unscoped move; A6 caught the c95a5cf3 false FAIL; operability deltas open (cosmetic) |
| CR-3 | unit/granularity critic + 11 variants | unit table recorded; all-DATED exemption measured, unapplied by design; addendum re-verified at the next revision |

Undelivered at write: **none** — all 29 non-VZ-2 C2 seats landed and were read
(the last four, EX-21/EX-22/SC-3/RV-9, arrived after this seat's poll window;
their reports corroborate every claim clause above, with RV-9 adding the
wording-level caveat on whole-stdout byte-identity and EX-22 the two doc-only
receipt lags, both reconciled in place).

## Attacks / refutations attempted (this seat)

1. **Vacuous closure?** controls both ways: clean root PASS with floor met;
   omission/plant flips to FAIL; classes in text AND `--json`.
2. **Class conflation** (false fire on legitimate renames): coherent rename +
   same-edit SCOPE re-key → PASS (CR-2 A1/A2; my matrix agrees); guard reach =
   exactly the declared set (CR-2 A4).
3. **Historical-tree regression**: 7 round-1 trees + 8 commits — H1 changes no
   historical verdict (CR-2 A8, PL-2 A6); `UNREADABLE` composition added only
   where the tree is short.
4. **Self-certification (H4)**: instrument cannot see its own widening; external
   differ does, exit 1. Residual stands, certificate works, claim names it.
5. **Mid-write/torn revisions**: `9373964c` crashed on the H1 path (TypeError,
   `lines=None` vs `%-4d`; EX-23 A5, EX-11 item 7); final prints
   `lines=None loci=None` and does not crash (CR-2 A9; my t1 receipt).
6. **Partial blindness**: PIN-only neuter and VER-only narrowing survive the
   floor — named residual (EX-14 §5 R2, EX-19 A2/A3, RV-4 A6, EX-11 A5,
   EX-16 A7).
7. **Pointer shadowing**: SCORECARD.md:291 names `~/.kimi-code/config.toml:1478`
   → Kimi `6.4.0`; live :1478 now holds `capabilities = [...]`; the census skips
   pointer checks in blocks carrying versions (`classify()` `if not occ`), so the
   stale pointer is never evaluated. Reproduced by me; EX-19 measured the path.
   Named debt, out of the two closures' scope.

## Named debt (open, with owners)

1. **Records commit + post-commit re-run** — parent; pre-flight above is not the
   commit. Standing rule: appended text locus-free or re-key in the same commit.
2. **Residual ledger**: H2 (inline-marker excusal), H5 (gate-free statement =
   unit boundary; not spelled out in the landed header's still-named list),
   t5-dated-shelter, partial-needle/`REA_GATE` narrowing (token floor ≠ coverage
   floor; incl. EX-11's weakened-`REA_GATE` channel), H4 self-certification.
3. **CR-2 operability deltas** (patch text): remedy not named in messages;
   `UNREADABLE` label also covers rows-beyond-EOF of readable files; G2 per-file
   figures are assertions. Cosmetic; parent's call.
4. **CR-3's all-DATED-file exemption** — measured, deliberately unapplied
   (EX-16 §2c): no file is all-DATED at HEAD; applying it would invalidate
   verifier receipts for a false-positive risk that does not exist at HEAD.
5. **Revision-identity cosmetics** — docstring now self-describes as v10-r9;
   frozen claim text says v11 (EX-23 §5a). Non-blocking.
6. **Verifier/seat pins to superseded revisions** — PL-2 §7, EX-12 §7 and my own
   earlier draft were pinned to `82fb807e`; CR-2/CR-3/EX-21/EX-23 receipts to
   `df9ffdf9`. Final bytes are `d0772ce8` (behaviour-identical to `df9ffdf9`,
   strictly stronger than `82fb807e` on `nullskill`/padded-file). This verdict is
   pinned to the final bytes; any further edit invalidates it (re-run
   `tools/battery.sh` + scope-diff).
7. **Pointer shadowing** (attack 7) — named, out of scope.
