# EX-20 (c2) — post-landing injection: weakened-regex / open-ended-bound laundering (the r4 CR3 class)

Seat EX-20, chain c2, role executor, 2026-10-19. Harness:
`claims/c2/EX-20/launder-suite.py` (18 attack/tree combos) and
`claims/c2/EX-20/onarrow-probe.py` (follow-up probe). Receipts:
`claims/c2/EX-20/receipts/` (`before-suite.txt`, `after-suite.txt`,
`onarrow-before-after.txt`, plus every variant's stdout in
`receipts/{before,after}/`).

Instrument revisions measured (the real target was read and hashed only —
all attacks ran on `/dev/shm/ex20r2` copies):

| role | sha256 | mtime | note |
|---|---|---|---|
| BEFORE | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | 2026-10-19 07:18 | pre-landing; H1/H3 latent |
| AFTER  | `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` | 2026-10-19 09:06:50 | EX-16's r9 landing (H1+G19, H3+G20 global floor) — first full after-matrix |
| AFTER′ | `09e270c24952ad4dc89bb014136d6cfe7b72395f44a1ba6f95efdce5d63869dc` | 2026-10-19 09:10:50 | observed and diffed, not run (superseded within 6s) |
| AFTER″ | `c95a5cf30201a1f862849b04701330e65b3777c877fb9467e4ee38656bbb0d4f` | 2026-10-19 09:10:56 | per-file floor; full matrix run — see the transient defect in §3b |
| LIVE   | `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` | 2026-10-19 09:11:50 | last revision measured; stable across two 18s polls (09:12:28 / 09:12:46) and re-verified at write time |

**The target was a moving work-in-progress for the whole measurement window**
(EX-16 revised it four times between 09:06:50 and 09:11:50, i.e. the r14-class
self-identity problem in live form). Every row of §3 below is pinned to the
revision named in its column; the AFTER″/LIVE deltas are in §3b. Re-derive the
live hash before quoting any of this — `sha256sum .ufo/gates/c1-census-v10.py`.

## 1. Verdict

**Refused, with four residuals measured and named (R1–R4).** Every laundering
form exercised either (a) now reads a *declared FAIL* under the landed
revision, or (b) still reads PASS and is refused only at the certificate layer
(the round-1 `scope-diff.py` creep differ / diff review) — and in two of the
four residuals even that layer is flag-less. The landed r9 revision closes
*more* than the frozen C2 text required: it closes the whole
open-ended/overshooting-bound family **instrument-side**, not just via the
certificate. Re-verified unchanged on the final revision `df9ffdf9…` (see §3b,
which also records a transient FALSE FAIL on the untouched HEAD tree during the
landing churn — `c95a5cf3`, superseded within 54s).

## 2. The class under test (evidence pointers)

- r4 refusal precedent: `SCORECARD.md:883-884` ("the open-ended-bound
  laundering path (CR3/P3/R3, measured) was refused"), rationale at
  `SCORECARD.md:908`; the exact attack shape re-measured by RV-10 in round 1
  (`.ufo/waves/arc3-loop1-round1/claims/c3/RV-10/proposed-fixed-bound-guard.patch.md`:
  fixed bound → `FAIL undeclared=1`; `900`/`10**9` → `PASS 0/0/0/0` with the
  locus read `historical`).
- Weakened-regex precedent: CR-5's blind-instrument fixture (H3), patch text
  `.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md`,
  receipt `receipts/census-blind-at-head.out`; and CR-5's own conclusion that
  the census cannot detect its own widening (H4).
- Frozen round-2 claim text: `.ufo/waves/arc3-loop1-round2/claims-frozen.md:34-50`
  (caps C2 at "every round-1 silent-PASS injection now reproduces as a declared
  FAIL … the H4 self-certification residual stays named").

## 3. Matrix (before → after)

Trees: `clean` = byte copies of PROVINCE.md / SCORECARD.md / SKILL.md;
`noSKILL` = SKILL.md removed; `P6` / `P7` = clean + an appended tail past the
declared bound carrying `rea-agents@6.3.0` / `rea-agents@7.3.0`; `P6M` = P6 with
the planted line carrying INLINE_MARKER words; `P6S` = P6 with the
`arc2-loop1-round3` marker token stripped at `SCORECARD.md:769`. Each attack
edits the *instrument copy*; `ctl` is the unedited control.

| attack | tree | BEFORE (`6f1d19ff…`) | AFTER (`82fb807e…`) | refused by |
|---|---|---|---|---|
| ctl | clean | PASS exit 0 | PASS exit 0 (`current-ok loci=5, total loci=17`) | — (control) |
| ctl | noSKILL | **PASS exit 0** (H1 hole) | **FAIL exit 1** `UNREADABLE ['SKILL.md: FileNotFoundError']` | G19 (landed) |
| ctl | P6 | FAIL exit 1 `undeclared=1` | FAIL exit 1 `undeclared=1` | fixed bound |
| ctl | P7 | FAIL exit 1 `undeclared=1` | FAIL exit 1 `undeclared=1` | fixed bound |
| ctl | P6M | **PASS exit 0** (H2 hole) | **PASS exit 0** | *nothing — R4* |
| ctl | P6S | FAIL (SCOPE-ERROR + undeclared=1) | FAIL (same) | G15 + fixed bound |
| W-blind (PIN+VER+PTR dead) | clean | **PASS exit 0** (H3 hole) | **FAIL exit 1** `G2 … SUSPECT` | G20 (landed) |
| W-blind | P6 | **PASS exit 0** | **FAIL exit 1** `SUSPECT` | G20 (landed) |
| W-gate (REA_GATE dead) | P6 | **PASS exit 0** | **FAIL exit 1** `SUSPECT` | G20 (landed) |
| W-pin (PIN dead) | P6 | FAIL `undeclared=1` | FAIL `undeclared=1` | VER still sees 6.3.0 |
| W-pin7 (PIN dead) | P7 | **PASS exit 0** | **PASS exit 0** | *nothing — R2* |
| W-pinv (PIN+VER dead) | P6 | FAIL `stale=2` + SUSPECT | FAIL `stale=2` + SUSPECT | backfires on attacker |
| W-marker (`r"."` at :769) | P6S | FAIL `undeclared=1`, SCOPE-ERRORS clean | FAIL `undeclared=1`, SCOPE-ERRORS clean | fixed bound |
| O-open (769→1000000000) | P6 | **PASS exit 0** | **FAIL exit 1** `['SCORECARD.md: 1422 lines < declared max 1000000000 (rows beyond EOF)']` | G19 rows-beyond-EOF (landed) |
| O-overshoot (769→9999) | P6 | **PASS exit 0** | **FAIL exit 1** (same class, `max 9999`) | G19 (landed) |
| O-addrow (new 856→1000000000) | P6 | **PASS exit 0** | **FAIL exit 1** (same class) | G19 (landed) |
| O-ineof (769→1422 = EOF) | P6 | **PASS exit 0** | **PASS exit 0** | *certificate only — R1* |
| O-tailrow (new 856→1422) | P6 | **PASS exit 0** | **PASS exit 0** | *certificate only — R1* |
| O-narrow (new 1420→1422) | P6 | **PASS exit 0** | **PASS exit 0** | *certificate flags empty — R1b* |

Certificate layer (round-1 `CR-5/tools/scope-diff.py`, base = the same revision
unedited), AFTER column:

| attack | scope-diff exit | `CREEP FLAGS` |
|---|---|---|
| W-blind, W-gate, W-pin, W-pin7, W-pinv | 0 | `[]` (needle edits invisible to the differ) |
| W-marker | 1 | `[]` (visible only in the `CHANGED` printout) |
| O-open / O-overshoot | 1 | 3 flags each (open-ended bound + wide added row + widen-by-add/remove) |
| O-ineof | 1 | 2 flags (wide added row 769-1422 + widen-by-add/remove) |
| O-addrow | 1 | 2 flags (open-ended bound + wide added row) |
| O-tailrow | 1 | 1 flag (wide added row 856-1422) |
| O-narrow | 1 | **`[]`** (the `ADDED` section carries the only signal) |

Evidence of the laundering *succeeding* in the R1 forms, AFTER instrument,
`receipts/after/O-ineof-P6.out`:

```
  SCORECARD.md block 1421-1422 [scope DATED]
      :1421 [pin] kimi=6.3.0 -> historical (dated scope)
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci=5, total loci=18, floor=1)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit 0
```

## 3b. Re-measurement on the later revisions (per-file floor)

EX-16 revised the target four times in five minutes; the full matrix was re-run
on the last revision, **LIVE `df9ffdf9…`** (`receipts/live-suite.txt`,
`receipts/live/`, copy `receipts/census-live-df9ffdf9.py`). Every §3 AFTER
result holds verbatim: `ctl` clean PASS exit 0 (and the real root PASS 0/0/0/0
exit 0, stdout `1db2ec31…`), `noSKILL` FAIL (`UNREADABLE ['SKILL.md:
FileNotFoundError']`), `W-blind`/`W-gate` FAIL `SUSPECT`, `O-open`/`O-overshoot`/
`O-addrow` FAIL `rows beyond EOF`, `ctl P6`/`P7` FAIL `undeclared=1`, `W-pin`
FAIL `undeclared=1`, `W-pinv` FAIL `stale=2`. Residuals R1 (`O-ineof`/`O-tailrow`
PASS), R2 (`W-pin7` PASS), R3 (`W-marker`: SCOPE-ERRORS clean but still FAIL
`undeclared=1`) and R4 (`ctl P6M` PASS) are unchanged on LIVE, and the
certificate flags are identical.

**Transient defect, observed and superseded (AFTER″ `c95a5cf3`, 09:10:56):**
that revision's per-file floor counted *block-level* current-ok records, read
`SKILL.md=0`, and failed the **untouched HEAD tree** —
`G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1,
SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)` /
`DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` / `VERDICT: FAIL` exit 1
(`receipts/final/ctl-clean.out`). It was replaced 54s later; LIVE counts
assertion-level (`d["disp"] == "current-ok"` over every record's `asserts`,
`.ufo/gates/c1-census-v10.py:546-557`) and reads `PROVINCE.md=17,
SCORECARD.md=14, SKILL.md=3` → PASS. Recorded because a wave that lands a
fail-closed guard must show it does not fail closed on a clean tree.

**Reporting split worth naming (LIVE, no verdict effect):** the same run's
`--json` emits a block-level `current_ok` array (PROVINCE 1 / SCORECARD 4 /
SKILL 0) while the text line's per-file floor is assertion-level (17/14/3).
An auditor who checks the floor from `--json` alone still sees `SKILL.md` with
zero current-ok **blocks**. Two counters, one name.

## 4. Residuals (all measured; none hidden)

- **R1 — bound widened *within* EOF is not caught instrument-side.** The r9
  boundary check fires only when `declared end > len(lines)`. `O-ineof`
  (769→1422, exactly EOF), `O-tailrow` (new 856→1422) and `O-narrow` (new
  1420→1422) all launder the planted pin to `historical (dated scope)` and read
  `PASS 0/0/0/0` exit 0 on the landed revision. R1 stays refused at the
  certificate layer for the wide forms (flags, above); `O-narrow`'s flag list is
  empty — the differ exits 1 but the `CREEP FLAGS` line reads `[]`, so a
  flags-only audit is blind to a 3-line shelter row (R1b). Note the census's own
  stdout cannot distinguish `O-ineof` from `O-narrow` (both `d409262b…`): the
  only discriminating signals live in the diff.
- **R2 — surgical needle blindness is invisible everywhere.** `W-pin7` (only
  `PIN` neutered, plant `rea-agents@7.3.0` — the one form the bare-version
  needle cannot see) reads `PASS` with the floor satisfied, and `scope-diff`
  reports `0 flags`. This matches EX-16's own header note (r9: "per-needle
  partial blindness … keeps loci>0 and still reads PASS -- that residual is
  H4/self-certification"). The external certificate that *does* see it is a
  locus-count/digest comparison (headless-blind run `total loci=17` vs the
  landed HEAD digest), not the creep differ.
- **R3 — marker-regex weakening is flag-less in the differ.** `W-marker`
  (`r"arc2-loop1-round3"` → `r"."`) defeats G15 on a marker-stripped tree
  (SCOPE-ERRORS empties) and restores byte-identical output to a clean
  `ctl`-on-P6 run (`5ce9fe2d…` both revisions). It does not by itself launder
  the tail plant (the fixed bound still reads it `UNDECLARED`), and the differ
  does print the marker change in its `CHANGED` section — but raises **no**
  creep flag.
- **R4 — H2 is reachable by a content writer alone.** `ctl` on `P6M`: a tail
  line whose own text carries `historical`/`baseline` (INLINE_MARKER) reads
  `historical (inline marker)` *outside any declared scope* and the run is
  `PASS 0/0/0/0` on **both** revisions — no instrument edit is needed at all.
  This is round-1's H2 (`.ufo/waves/arc3-loop1-round1/claims/c3/verdict.md`
  item 5), still open after r9. Discovery note: this hole was found by accident
  — my first fixture's plant line began "Historical note:", which self-laundered
  the plant and produced a spurious PASS; the fixture was corrected and the
  class was then measured deliberately (`P6M`).

## 5. Attacks attempted on my own measurements (verdicts)

| # | attack on my own result | verdict |
|---|---|---|
| 1 | "The AFTER runs might have raced EX-16's landing" | REFUTED — the AFTER copy was taken at 09:06:59 from the landed file, all attacks ran on that copy, and the target re-hashes to `82fb807e…` unchanged after every run above |
| 2 | "The BEFORE control digest should equal round-1's `3b677b8e…`" | REFUTED as a harness defect — round-1's digest was captured at a 1336-line SCORECARD; HEAD is now 1417 lines (round-1/2 records), so the stdout legitimately differs; the *verdict* line and counts (PROVINCE 6 / SCORECARD 9 / SKILL 2) match round-1 exactly |
| 3 | "Neutering needles is free for the launderer" | REFUTED — `W-pinv` turns two in-scope pointer loci `STALE` (`SCORECARD.md:288` pointer resolution) once the pin needle stops masking them; the attack *backfires* (`stale=2`, exit 1) |
| 4 | "PIN-neutering alone hides the classic 6.3.0 plant" | REFUTED — `W-pin` still FAILs `undeclared=1` because the bare-version needle sees `6.3.0`; the attacker must choose a value outside `6.\.\d+\.\d+` (hence `W-pin7`) |
| 5 | "The r9 rows-beyond-EOF check makes the r4 class fully closed" | **CONFIRMED FALSE** — see R1 (in-EOF widening passes, and one form leaves the flag list empty) |
| 6 | "The creep differ's flags are the certificate" | **CONFIRMED FALSE as stated** — `O-narrow` exits 1 with `flags=[]`; the `ADDED`/`CHANGED` sections, not the flag list, carry that signal (and needle edits appear in neither) |

## 6. Reproduction

```
# scratch harness (never the repo target; /tmp is quota-exhausted — /dev/shm)
cp .ufo/gates/c1-census-v10.py /dev/shm/ex20r2/tool-after.py
python3 claims/c2/EX-20/launder-suite.py --tool /dev/shm/ex20r2/tool-before.py --label before
python3 claims/c2/EX-20/launder-suite.py --tool /dev/shm/ex20r2/tool-after.py  --label after
python3 claims/c2/EX-20/onarrow-probe.py /dev/shm/ex20r2/tool-before.py /dev/shm/ex20r2/tool-after.py
# landed instrument, ordinary run at HEAD (certificate that nothing moved):
python3 .ufo/gates/c1-census-v10.py --root .   # PASS 0/0/0/0 exit 0, stdout sha256 a9cd6886…
```

## 7. Proposed changes

**None to any real target.** This seat is confirmatory; the landing is EX-16's
and the frozen C2 text is met (and exceeded — the O-open/overshoot/addrow
family is now refused instrument-side, which the frozen text only required to
be refused via the certificate). The residuals above are advisories for the
*next* instrument touch, in the order they cost the least to close:
R2/R3 are covered by making the certificate a needle/marker diff plus a
locus-count comparison (no code change to the census); R1b wants the differ's
flag list extended to "any DATED row whose end moved later or whose added
width exceeds the file's tail slack"; R4 is a content-side rule (no
INLINE_MARKER token may excuse a locus outside the declared scope) and is the
only one of the four a writer can reach without touching the instrument.
