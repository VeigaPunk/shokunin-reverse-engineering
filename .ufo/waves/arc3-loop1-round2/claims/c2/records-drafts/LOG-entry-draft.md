# LOG.md entry — DRAFT (arc3-loop1-round2, C2 chain records)

Status: DRAFT by seat SC-3 (chain c2, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the wave's
sealed receipts (or the sentence rewritten to the honest-stop branch) before
landing. The C1/C3 bullets are shape-only: fill from those chains' records
drafts. **Pin-free discipline applied**: no bare version numerals, no pin-form
token, no absolute `path:line` — the records append must stay locus-free in the
census unit (round-1 connector injection test). Pasteable text is the block
below the horizontal rule; the SC-3 notes and evidence inventory at the bottom
are not part of the entry.

---

### arc3-loop1-round2 — depth (self-identity rule) + freshness (census fail-closures) + operability (custody receipt v2)

- Motivating evidence: C2 — the round-1 c3 verdict's named latent holes H1
  (an absent CURRENT-only scoped file reads silent PASS, `lines=0 loci=0`) and
  H3 (needles neutered → `loci=0` → blind PASS via G2's vacuous second
  disjunct); patch texts `claims/c3/RV-11/proposed-missing-file-guard.patch.md`
  and `claims/c3/CR-5/proposed-g2-positive-floor.patch.md` (round-1 tree,
  `.ufo/waves/arc3-loop1-round1/`). C1 — the r1 self-identity defect (EX-12's
  revision-1 text carried a stale byte-identity claim; the r1 records landed
  that lesson as a queue-drain rule candidate). C3 — the r1 cross seats'
  custody findings (local-time mtime labelled as UTC; sha256-only custody blind
  to a same-content rewrite). Round declaration:
  `.ufo/waves/arc3-loop1-round2/claims-frozen.md` (64-seat roster frozen
  PRE-DISPATCH; roster enumerated mechanically in the freeze, draft miscount
  discarded pre-dispatch).
- Dispatch: 64 seats (items array == frozen roster, counted at dispatch),
  `opencode-go` key 2 of 7 (rotation advanced after round 1, per the freeze).
  Delivered [[FILL: n/64]].
- C1 depth — [[FROM C1 CHAIN: queue-drain rules 13 → 14 — the self-identity
  re-derivation discipline (an artifact recording its own byte-identity must
  re-derive it after every revision; a stale self-identity voids the
  verification block, not the work); rule text in the SKILL.md craft section;
  command A 14/14 citation-resolved at the work commit; prior 13 rule blocks
  byte-identical; citations in stanza-key + receipt form, no bare line
  numbers. See the c1 records drafts for the fill shape.]]
- C2 freshness — the census fail-closures land (EX-16's real-target write of
  `.ufo/gates/c1-census-v10.py`, v11 semantics: H1 unreadable-file class +
  H3 positive-floor). Before at HEAD `14b1682` (instrument sha256
  `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`,
  490 lines, round-1 landed revision): census run at HEAD reads PASS
  `stale=0 ambiguous=0 undeclared=0 unresolved=0`, exit 0, scope-errors [],
  counts PROVINCE 162/6, SCORECARD 1417/9, SKILL 371/2; the H1 injection
  (scratch root without SKILL.md) reads silent `VERDICT: PASS` exit 0 with
  `SKILL.md lines=0 loci=0` (both its declared rows are CURRENT, so no marker
  assertion fires); the H3 injection (needle regexes neutered, CR-5 fixture)
  reads all-zero loci with `G2 positive-assertion guard: ok` and `VERDICT:
  PASS` exit 0 — a non-empty scope graded clean by a blind instrument. Controls
  measured: SCORECARD.md absent → FAIL, marker-uncheckable scope errors (the
  declared-CNE side exists today only for files with DATED rows). After
  (landed file sha256 `d0772ce8…`, 610 lines, worktree-modified — the file
  moved during the wave, `82fb807e…` → `c95a5cf3…` → `df9ffdf9…` → `a4c16763…`
  → `d0772ce8…`; parent
  commits at records; SC-3 re-ran the whole matrix independently on a scratch
  copy of the settled revision, `evidence/after-*.out`): the ordinary run
  stays PASS 0/0/0/0 exit 0 with counts unchanged (PROVINCE 162/6, SCORECARD
  1417/9, SKILL 371/2), `DECLARED FAIL CLASSES: []`, `G2 … ok (current-ok
  loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total
  loci=17; floor=1/file)`. The H1 class is now declared: an absent / EACCES /
  zero-byte / truncated / is-a-directory scoped file → `UNREADABLE
  (could-not-evaluate)` plus `DECLARED FAIL CLASSES: ['UNREADABLE']`,
  `VERDICT: FAIL` exit 1 (SC-3's re-run: SKILL.md absent →
  `['SKILL.md: FileNotFoundError']`; EACCES → `['SKILL.md: PermissionError']`;
  EX-16's receipts also cover PROVINCE/SCORECARD absent, zero-byte, truncated,
  isdir — `claims/c2/EX-16/receipts/after/`). The H3 class is now declared as
  a per-readable-file positive floor (EX-14's variant B, adopted on
  measurement): an all-needles-neutered copy → `G2 … SUSPECT (per file 0/0/0;
  total loci=0; floor=1/file)`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`,
  exit 1; a full-length scoped file stripped of its needles is likewise
  declared now (SC-3's null-SKILL attack — the global-floor variant alone had
  swallowed it). Every round-1 silent-PASS injection re-run on the landed file
  returns its declared class (before receipts `claims/c2/EX-16/receipts/before/`,
  after receipts `…/receipts/after/`, plus SC-3's independent re-run in
  `evidence/`). Scope bounds otherwise byte-stable — external diff audits on
  the v11 diff: the independent AST creep audit (RV-6's tool, run by SC-3)
  reports 20 rows unchanged, key set and canonical row digest identical, 0
  flags (`evidence/rv6-creep-audit-sc3.out`); EX-16's own scope-diff reports
  ADDED(0) REMOVED(0) CHANGED(0) (`claims/c2/EX-16/receipts/after/scope-diff.txt`).
  Named residual: H4 self-certification (the census cannot certify its own
  scope; the external audit is the certificate for any future re-key);
  per-needle partial blindness (the pin needle neutered alone keeps each
  file's count above zero and still reads PASS — a token floor is not a
  coverage floor; the header names it, EX-14 §5 measured it); H2/H5 stay
  carried debt (not this claim). The header deliberately does not carry its
  own post-edit hash (an artifact recording its own byte-identity must
  re-derive it after every revision) — the identity lives in the landing
  receipt.
- C3 operability — [[FROM C3 CHAIN: `.ufo/gates/custody-pair/` lands as a
  committed tool; v2 receipt per path = sha256 + mtime epoch (UTC-rendered and
  correctly labelled) + inode + ctime; the label defect gone; a live
  same-content rewrite detects via inode/ctime movement; v1 receipts remain
  verifiable against the tool's sha256 fields; live pre/post pair exit 0, 5/5.
  See the c3 records drafts for the fill shape.]]
- Custody: pre-pair [[FILL: receipt path, capture time, 5/5]]; post-pair
  [[FILL: receipt path, capture time, 5/5]]; zero drift across the wave
  [[FILL: corroborating captures]].
- Process notes: `/tmp` (tmpfs + usrquota) standing rule — scratch under
  `/var/tmp` or `/dev/shm`; the wave's `df` shows free space on `/tmp` while
  the per-user quota is the binding constraint (standing r1/r4 record).
  Untracked `.ufo/gates/__pycache__/` present at wave start (round-1 residual)
  — keep out of the commit. Round-2 waves write only their own artifacts; the
  real targets written this round are the census file (C2, EX-16) and the new
  custody-pair tool dir (C3, EX-31).
- Carried debt (named): the census's remaining named residuals — H2
  (same-line inline-marker excusal of an arbitrary pin value), H4
  (self-certification: the instrument cannot certify its own scope; the
  external audit is the certificate for any future re-key), H5 (gate-free
  version statement outside the unit), per-needle partial blindness (the pin
  needle neutered alone keeps each file's count above zero; a token floor is
  not a coverage floor — header-named, EX-14 §5 measured), and the r1 C2
  custom-table re-pin contract [[FILL: plus C1/C3 debts]]. (Closed on the
  landed revision, not carried: the per-file collapse — a full-length scoped
  file stripped of its needles now reads the declared BLIND-INSTRUMENT FAIL;
  SC-3 measured, `evidence/atk-nullskill-v2.out`.)
- Retired: the r1 c3 latent holes H1 (absent-file silent PASS) and H3
  (blind-instrument PASS) — closed as declared FAIL classes on the landed v11
  guards, measured (SC-3's independent re-run; EX-16 receipts)
  [[FILL: parent confirms at the records commit; else "none"]].
- Scope: no config edits, no pushes, repo-local.

---

## SC-3 notes (not part of the entry)

**Why the drafts carry no version numerals or pin forms.** The round-1
connector proved by injection that an unmarked pin-form or version token in a
newly appended records section flips the census to `FAIL undeclared=1`
(`arc3-loop1-round1/claims/cross/consistency.md` §3b, variant C) — the
records-commit census runs after the append, so the appended text must be
locus-free in the instrument's unit. This draft therefore renders measured
values with masks (e.g. live-anchor values as `<live>`) and points to the
verbatim evidence files; no absolute `path:line`, no `~`-form path pointer, no
bare version numeral, no pin form appears anywhere in this file. The
self-check receipt is `evidence/pin-free-check.out`.

**Before-values are SC-3-measured** (2026-10-19, wave in progress), all on
scratch copies — the real files were only read/hashed:

- HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` (round-1 records commit).
- Census sha256 `6f1d19ff…`; HEAD run → `VERDICT: PASS` (0/0/0/0), exit 0
  (`evidence/before-head-baseline.out`, `evidence/before-head-baseline.json`).
- H1a SKILL.md absent → `VERDICT: PASS` exit 0, `SKILL.md lines=0 loci=0`
  (`evidence/before-h1-skill-absent.out`).
- H1b SCORECARD.md absent → `VERDICT: FAIL` exit 1 with marker-uncheckable
  scope-errors (`evidence/before-h1-score-absent.out`) — the existing CNE side.
- H3 all-needles-neutered fixture (round-1 CR-5 tool, sha256 `24e95a47…`) →
  all-zero loci, `G2 … ok`, `VERDICT: PASS` exit 0 (`evidence/before-h3-blind.out`).
- Shared instruments at HEAD: probe selftest 13/13 exit 0, normal run
  `reported findings=0 exit=0` (`evidence/probe-selftest.out`,
  `evidence/probe-head.out`); command A `82/82, missing [], dangling [],
  13/13, 10.0/10.0` at `14b1682…` (`evidence/commandA-head.json`).
- Custody 5-path capture (sha256 + inode, read-only) at 12:02:52Z
  (`evidence/custody-sc3-capture.txt`).

**After-values are SC-3-measured on the landed revision `d0772ce8…`** (610
lines; the file was still moving at SC-3's close; the gate file moved
`82fb807e` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8` during the wave
— an intermediate block-level floor revision broke the ordinary
HEAD run, because SKILL.md carries 0 current-ok blocks, and was replaced by the
det-level floor; EX-23 seat report §6): ordinary run PASS 0/0/0/0 exit 0
(`evidence/after-t0-present.out`, `after-q0-quiet.out`,
`after-head-json.json`); SKILL.md absent → FAIL `['UNREADABLE']`
(`after-h1-absent-skill.out`); SKILL.md EACCES → FAIL `['UNREADABLE']`
(`after-h1-eacces-skill.out`); full-length needle-stripped SKILL.md → FAIL
`['BLIND-INSTRUMENT']` (`after-atk-nullskill.out`); the all-neutered blind
fixture → FAIL `['BLIND-INSTRUMENT']` (`after-h3-blind.out`; SC-3 re-run —
EX-25's addendum re-ran the same battery at its own final revision). Creep
audit before→after (RV-6's independent AST tool, run by SC-3): 20 rows
unchanged, canonical row digest identical, 0 flags, exit 0
(`evidence/rv6-creep-audit-sc3.out`). The landed header labels the two
closures G19 (unreadable/undeclarable scoped file) and G20 (positive floor,
not vacuous).

**Named label defect in the landed revision** (EX-19 seat report §3, SC-3
concurs from the G2 line): the per-file counts printed as "current-ok loci per
file" are disposition counts (JSON `current_ok_per_file`), and the "total
loci=17" beside them counts blocks — value right, label over-claims. It is the
same defect class as the round-1 custody `MTIME_UTC` label finding; recorded,
not repaired by this seat (the instrument target is EX-16's).

**Poll notes.** See `evidence/poll-log.txt` for the observation log. Any
after-value claimed by another seat is folded in only with its receipt path;
prototype numbers must not be pasted as landed numbers (round-1 SC-5 rule).

**Fill-order for the parent** (suggested): (1) replace the dispatch delivery
count; (2) check `sha256sum .ufo/gates/c1-census-v10.py`; if it is not
`d0772ce8…`, re-run the c2 matrix (repo-root baseline + absent / EACCES /
needle-stripped / all-neutered scratch roots + RV-6's creep audit) and re-stamp
before pasting; (3) fold the C1/C3 bullets from their drafts; (4) run the
census and the probe at the records commit and quote the verdicts verbatim;
(5) fill carried debt / retired once the wave's verdicts are known.
