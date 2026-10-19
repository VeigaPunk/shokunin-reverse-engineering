# CR-3 seat report — arc3-loop1-round2, chain c2, role critic

Seat CR-3 | chain c2 | role critic | 2026-10-19 | repo HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`
Scoped files at HEAD: PROVINCE.md 162 lines `d075a3c6…`, SKILL.md 371 lines
`483b0eba…`, SCORECARD.md 1417 lines `a7c72950…`.
Instrument sha256 keyed per measurement: pristine `6f1d19ff…` (490 lines),
landed `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`
(601 lines, matches EX-16's re-derived `after-sha256.txt` at 12:12:15Z).

**Seat task: attack H3 — is any SCOPE row legitimately zero-locus at HEAD
(which would make the floor a permanent false positive)?**

**Answer: yes — four of the twenty rows, all DATED.** A floor at SCOPE-row
granularity therefore FAILs an ordinary HEAD run forever. Attacking the same
question one level up found a second instance that was **live on disk**: the
12:10Z revision `c95a5cf3…` implemented the floor per-file in the census's
**block** unit, and SKILL.md legitimately has zero current-ok *blocks* (its
current-ok detections sit in a block disposed `info`), so that revision read
`VERDICT: FAIL … DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` on an unmodified
HEAD run. EX-16 re-keyed the floor to detections at `df9ffdf9…`; the landed
revision reads PASS at HEAD and still FAILs every blind/collapse fixture I ran.
The claim's after-state holds at the landed bytes; the refuted granularities are
now chain knowledge (patch text §2) because a future "simplification" of the
floor unit re-introduces the false FAIL.

## 1. Work performed (evidence pointers)

- Read: `claims-frozen.md`; the pristine census end-to-end (490 lines); the
  round-1 H3 patch text (`arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md`)
  and RV-11's H1 patch text; the c3 round-1 verdict H3 entry; EX-14's map
  (`claims/c2/EX-14/scope-locus-map.md`, landed 12:08Z) and its patch text.
- Built the independent row map: `claims/c2/CR-3/tools/map-rows.py` (imports the
  frozen instrument read-only, attributes every detection to the row owning its
  physical line) → `receipts/row-map-head.json`; per-row gate-bearing/needleless
  unit inventory → `receipts/row-gateblocks.json`.
- Built the floor-variant generator `tools/mkvariants.py` (sealed: it asserts the
  source sha `6f1d19ff…` before editing) → 11 variants; matrix receipts
  `receipts/v-*.out` (4 roots x 8 variants) including the blind, absent-file and
  needle-stripped fixtures.
- Fixtures, all under `/var/tmp/cr3/scratch` (never `/tmp`): `root-inj`,
  `root-gut` (SKILL.md 371 lines, all needles neutralized in place),
  `root-noskill`, `root-record` (needle-free SKILL.md with its rows re-keyed
  DATED in a scratch copy of the gate).
- Live-gate measurements at each revision, receipts `receipts/live2-head.*`
  (block-unit FAIL), `live3-head.out`, `live3-root-gut.out`,
  `live3-root-noskill.out`, `live4-blind-head.out`, `live-nop-{PIN,VER,PTR}.out`,
  `live-refined-*`, `live-record-record.out`.
- Cross-check versus EX-14's map: all 20 rows agree on blocks and detections and
  on the totals (17 blocks / 50 dets / 34 current-ok dets), disposition mixes
  included; 0 mismatches. Independently reproduced EX-14's unit-trap numbers:
  current-ok **blocks** per file `{PROVINCE 1, SCORECARD 4, SKILL 0}` vs
  current-ok **dets** `{17, 14, 3}`.
- Whole narrative with the revision timeline: `claims/c2/CR-3/revision-timeline.md`.

## 2. Proposed changes (patch-text paths or "none")

`claims/c2/CR-3/proposed-floor-granularity.patch.md` — **not applied** (CR-3 is a
critic; EX-16 owns the target).

- §2 text-only: name the floor unit (per readable file, current-ok detections) in
  the docstring and record the two refuted units (SCOPE row; per-file blocks)
  with their HEAD evidence, so the unit cannot be "simplified" silently.
- §3 optional, one behaviour change: gate the per-file floor on files that
  declare a CURRENT row (`{r[0] for r in SCOPE if r[3] == "CURRENT"}`), removing
  the last latent permanent-false-positive path — a pure record file (all-DATED
  rows) can never contribute a current-ok detection. Measured: HEAD PASS
  unchanged (17/14/3), stripped-SKILL fixture still FAILs, `root-record` fixture
  goes FAIL → PASS. Recommended only if the parent wants the floor proof against
  future re-keys; otherwise the path belongs in the named-residual list (latent,
  no scoped file is a pure record at HEAD).
- Refused, with cause: re-keying the four zero-locus rows, and widening
  `REA_GATE` to populate them (both are the laundering/widening moves the round
  rules refuse; the rows are load-bearing coverage — see A7).

## 3. Before→after measurement (chain c2 claim, at my own hand)

Before-state, pristine instrument `6f1d19ff…`, HEAD tree, scratch copies only:

```
$ python3 census-none.py --root <repo> --json            # ordinary run
VERDICT: PASS   exit=0   counts 6/9/2
$ python3 census-blind.py --root <repo> --json           # PIN/VER/PTR neutered (CR-5 method)
counts 0/0/0;  VERDICT: PASS  exit=0                     # H3 reproduces at HEAD
$ python3 census-none.py --root root-noskill --json      # SKILL.md absent
SKILL.md lines=0 loci=0;  VERDICT: PASS exit=0           # H1 reproduces at HEAD
$ python3 census-none.py --root root-gut --json          # SKILL.md needles stripped, 371 lines
SKILL.md loci=0;  VERDICT: PASS exit=0                   # file collapse invisible
  receipts: v-none-head / v-blind-head / v-none-noskill / v-none-gut
```

After-state, landed instrument `df9ffdf9…` (601 lines), same fixtures:

```
$ python3 .ufo/gates/c1-census-v10.py --quiet            # ordinary run at HEAD
lines 162/1417/371;  loci 6/9/2
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit=0
  receipts/live3-head.out

$ python3 live4-blind.py --root <repo> --quiet           # needles neutered
G2 … SUSPECT (0, 0, 0; total loci=0);  DECLARED ['BLIND-INSTRUMENT'];  FAIL exit=1
$ python3 … --root root-noskill --quiet
UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError'];  DECLARED ['UNREADABLE'];  FAIL exit=1
$ python3 … --root root-gut --quiet
G2 … SUSPECT (17, 14, 0; total loci=15);  DECLARED ['BLIND-INSTRUMENT'];  FAIL exit=1
  receipts/live4-blind-head.out, live3-root-noskill.out, live3-root-gut.out

$ python3 … --quiet                                      # on the intermediate revision c95a5cf3… (12:10Z)
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  exit=1                                    # ordinary HEAD run — claim-blocking
  receipts/live2-head.out + live2-head.json
```

Scope-bounds invariance: the SCOPE table is byte-identical between pristine
`6f1d19ff…` and the first landing `82fb807e…` (`diff` of the `SCOPE = […]`
block: no output). All twenty rows at HEAD are in bounds; no detection line
falls outside a declared row (`row-map-head.json: undeclared_assert_lines []`),
so the four zero-locus rows are content facts, not truncation artifacts.

## 4. Attacks/refutations attempted, with verdicts

| # | attack | verdict | receipt |
|---|---|---|---|
| A1 | The seat question: row-level floor at HEAD | **CONFIRMED zero-locus rows; per-row floors refuted** — FAIL, 4 permanent violations (PROVINCE.md:40-43, SCORECARD.md:417-466, 467-502, 769-855) | `v-row-head.out`, `v-rowany-head.out` |
| A2 | Per-file floor in the *block* unit at HEAD | **REFUTED (and found live)** — revision `c95a5cf3…` reads FAIL BLIND-INSTRUMENT with `SKILL.md=0`; SKILL.md's 3 current-ok dets sit in a mixed block disposed `info` | `live2-head.out` |
| A3 | Do the surviving granularities hold at HEAD and still catch the blind class? | **CONFIRMED**: per-file detections (landed), per-file any-locus, CURRENT-row-only, corpus-level all PASS at HEAD and FAIL under neutered needles | `live3-head.out`; `v-class-head.out`, `v-file-head.out`, `v-global-head.out`, `v-blind-*.out` |
| A4 | Is the zero-locus row dead, or a functional declaration? | **FUNCTIONAL** — a `rea-agents@6.3.0` planted inside 769-855 reads `historical` (block 780-781); a pin planted in a CURRENT row reads STALE (plus a line-shift artifact of my own fixture, named) | `v-none-inj.out` |
| A5 | Partial blindness against the landed floor (EX-16's named H4 residual) | **RESIDUAL STANDS**: PIN-only neuter → PASS with *identical* counts (VER covers the version inside the pin); PTR-only → PASS; VER-only → FAIL but on a spurious STALE, not on the floor | `live-nop-{PIN,VER,PTR}.out` |
| A6 | Latent permanent false positive: pure record file (all-DATED rows) | **CONFIRMED latent** — landed floor FAILs the `root-record` fixture; the §3 refinement PASSes it and still FAILs `root-gut` | `live-record-record.out`, `live-refined-record-record.out`, `live-refined-gut.out` |
| A7 | Would deleting/re-keying the four zero-locus rows be the safer fix? | **REFUSED with evidence** — the rows date planted pins as `historical` (A4) and removing them converts such a locus to UNDECLARED (r4 laundering path); 3 of 4 rows have no gate-bearing line, so no re-key can "populate" them without widening vocabulary | `v-none-inj.out`, `row-gateblocks.json` |
| A8 | Is EX-14's map (the seat line's required instrument) correct? | **VERIFIED** — 20/20 rows and totals agree with my independent harness; their block-vs-det unit trap independently reproduced | this report §1 |
| A9 | Scope creep in the landing | **NONE FOUND** — SCOPE table byte-identical; no row added, no bound widened, no class flipped | `diff` output, §3 |

Custody: the five custody paths were not opened, hashed or stat'ed by this seat;
the instrument's own live-anchor re-derivation read the three client configs as
designed. No git mutation; no LOG/SCORECARD/SHONEN/corpus/SKILL write; scratch
under `/var/tmp/cr3` only.

## 5. Blockers, if any

- **None blocking.** The seat's question is answered with receipts, and the
  landed instrument was verified after the churn.
- Named gaps and cautions for the integrator:
  1. The target moved **five times** while this seat ran (`6f1d19ff…` →
     `59975ae0…` → `82fb807e…` → `076bd621…` → `c95a5cf3…` → `df9ffdf9…`);
     every CR-3 claim is keyed to a sha and time. The claim-blocking window was
     one revision (`c95a5cf3…`, ~12:10–12:12Z) and is closed at `df9ffdf9…`.
  2. EX-14's §6 map snippet (block-count floor) is the exact false-FAIL
     reproduction; their patch text is the det-level form and is correct. If any
     later seat ports the snippet as written, the false FAIL returns — patch
     text §2 exists to prevent that.
  3. The §3 refinement (CURRENT-row gating) is **proposed, not applied**:
     decision for the parent/EX-16. If declined, `root-record` (pure record file)
     should be in the named-residual list beside H4 and partial blindness.
  4. `info`-disposition blocks are the mechanism behind the block-unit trap and
     are otherwise unnamed in the instrument's class list; the landed docstring
     now names it, my receipts measure it (SKILL.md block 18-20: 3 current-ok +
     1 historical det -> block `info`).

## Addendum (post-report, 12:16Z) — re-verified at the next revision

The target moved once more after this report was written:
`a4c167631269e5110fbdcf323b6be2a779eaa1e0ca79c98201419261ba9c6bfb` (603 lines).
Re-measured at that sha, so no claim above rests on superseded bytes:

```
$ python3 .ufo/gates/c1-census-v10.py --quiet            # ordinary HEAD run
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  exit=0
$ live5.py --root root-gut     -> DECLARED ['BLIND-INSTRUMENT']  FAIL exit=1
$ live5.py --root root-noskill -> DECLARED ['UNREADABLE']        FAIL exit=1
$ live5-blind.py --root <repo> -> DECLARED ['BLIND-INSTRUMENT']  FAIL exit=1
  receipts/live5-gut.out, live5-noskill.out, live5-blind-head.out
```

The newest revision keeps the floor per-file over current-ok detections (per-file
report line 17/14/3 identifies the unit; a block-unit floor would print 1/4/0),
so the seat's verdicts stand unchanged at `a4c16763…`.
