# EX-19 — neutered-needles fixture (H3): post-landing injection + partial neutering

Seat EX-19, chain c2, executor, arc3-loop1-round2, 2026-10-19.
Task: post-landing injection of the H3 class (neutered needles → blind PASS) against
the census instrument, expecting a declared FAIL after EX-16 lands the G2
positive-floor patch; plus partial neutering (half the needles).

**STATUS: COMPLETE — both halves measured.** Post-landing: EX-16 landed H1+H3 at
09:06:50 local (`82fb807e…`); the full-neuter injection now reproduces as a
declared FAIL (`DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`, exit 1), and the
partial-neutering residual is measured and named (§6).

## 1. Work performed (evidence pointers)

Instrument under test: `.ufo/gates/c1-census-v10.py`. Two identities, both captured
(read-only) into `receipts/post-landing/sha256-instruments.txt`:

- pre-landing `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`
  (snapshot `/var/tmp/ex19/instrument/pre-landing-v10.py`; = CR-5's round-1
  `claims/c3/CR-5/tools/census-after.py` byte-for-byte) — the "before" side.
- landed `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`
  (EX-16's r9 H1+H3 write, mtime 2026-10-19 09:06:50, 28606 B / 560 lines;
  snapshot `tools/landed-instrument-82fb807e.py`; diff
  `receipts/post-landing/landing-diff-6f1d19ff-to-82fb807e.patch`) — the "after"
  side. Two further revisions followed within five minutes (§6b, §6c); the sha was
  re-checked after every measurement batch and each revision is recorded with its
  own snapshot.

Repo HEAD for this seat's measurements: `14b1682`; `.ufo/gates/` was clean at
snapshot time (only the untracked `__pycache__/`), modified afterwards by EX-16's
landing.

Fixture harness (task artifact, tools/): `tools/neuter.py` — applies exact literal
needle replacements to a census source, asserts each replacement lands exactly once
(fail-closed), writes the copy, runs it, records exit code / verdict / G2 line.
Root fixture: byte copies of the three scoped files (`sha256` verified identical to
`PROVINCE.md d075a3c6…`, `SKILL.md 483b0eba…`, `SCORECARD.md a7c72950…`), under
`/var/tmp/ex19/roots/base/`; the real repo root was used as a cross-check.

Baseline at HEAD, pre-landing instrument (receipts/baseline.txt, baseline.json):
`live anchors {'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'}`, loci
`PROVINCE.md 6 / SCORECARD.md 9 / SKILL.md 2` (17 total), current-ok 5 loci /
11 dets, `VERDICT: PASS (0/0/0/0)`, exit 0. Same loci counts as the round-1
recorded run `claims/c3/EX-26/census-at-HEAD.txt` (sha `3b677b8e…`); the receipts
are not byte-identical because SCORECARD.md grew 1336 → 1417 lines when the
round-1 records landed (digest of this baseline: `d3da7509…`).

## 2. Pre-landing injection matrix (H3 reproduction + partial neutering)

`python3 tools/neuter.py --src instrument/pre-landing-v10.py --tag pre --root roots/base`
→ receipts/pre.matrix.json + per-spec `pre.<spec>.out`.

| spec | what is neutered | exit | verdict | G2 line | loci (P/S/K) |
|---|---|---|---|---|---|
| `full` | all 3 needles → never-match | 0 | **PASS** | ok | 0/0/0 |
| `pin` | PIN dead | 0 | PASS | ok | 6/9/2 |
| `ptr` | PTR dead | 0 | PASS | ok | 6/9/2 |
| `ver` | VER dead | 1 | FAIL | ok (STALE=1) | 3/3/2 |
| `pin+ver` | PIN+VER dead (2 of 3) | 1 | FAIL | SUSPECT | 1/1/0 |
| `pin+ptr` | PIN+PTR dead (2 of 3) | 0 | **PASS** | ok | 6/9/2 |
| `ver+ptr` | VER+PTR dead (2 of 3) | 0 | **PASS** | ok | 3/2/2 |
| `h-ver67` | VER narrowed to 6.7.x only | 1 | FAIL | ok | 4/5/2 (STALE=1) |
| `h-ver65` | VER narrowed to 6.5.x only | 1 | FAIL | ok | 4/6/2 (G11 `SCORECARD.md:530`) |
| `h-pin64` | PIN narrowed to 6.4 pins only | 0 | **PASS** | ok | 6/9/2 |
| `h-all67` | PIN+VER narrowed to 6.7 class, PTR to config.toml | 1 | FAIL | ok | 4/5/1 (STALE=1) |

Findings, each a receipt:

- **H3 reproduces exactly as CR-5 measured** (`claims/c3/CR-5/receipts/census-blind-at-head.out`):
  with all three needles dead the run reports `loci=0` on all files, prints
  `G2 positive-assertion guard: ok` and `VERDICT: PASS (0/0/0/0)`, exit 0. A blind
  instrument is indistinguishable from a clean one (receipts/pre.full.out).
- **The negative direction is also live: needle loss can turn FAIL into PASS.**
  `ver` alone → FAIL (STALE=1, below); `ver+ptr` → **PASS** exit 0 (receipts/pre.ver+ptr.out).
  Removing PTR removes the failing assert, and the H3 floor's second disjunct
  (everything-clean) is still satisfied because the run keeps 6.7.0 loci. Blindness
  laundering is not only "PASS with no loci" — it is also "PASS by dropping the
  locus that was failing".
- **Partial neutering (reading A: 2 of 3 needles dead)**: `pin+ptr` PASS with
  counts unchanged, `ver+ptr` PASS with reduced counts. **Reading B (each needle's
  coverage halved)**: `h-pin64` **PASS** — the tree's only live pin (`6.7.0`,
  SCORECARD.md:699) becomes invisible to PIN and the run still reads green; the
  FAILs of `h-ver67`/`h-ver65`/`h-all67` are accidents of the tree (they expose the
  masked pointer of §4 as STALE, or trip G11 at `SCORECARD.md:530`), not floors —
  the pre-landing instrument has no floor at all.
- **No floor catches partial blindness, only total blindness** — the class boundary
  measured here, and the boundary the landed patch inherits (see §6).
- No PTR loci exist at HEAD under the baseline instrument, so PTR-only muting is
  invisible on this tree (`ptr` ≡ baseline); the `ver+ptr` row shows this is not
  harmless — PTR matters exactly as a suppressor of the STALE the VER muting exposes.

## 3. Proposed change (patch text; scratch prototype only — EX-16 owns the target)

`tools/proto.py` generates a scratch prototype `P1` of the census with (a) the H3
floor (`g2_ok` requires ≥1 current-ok locus), (b) a total-loci floor, and (c) a
**needle-liveness self-test**: each of PIN/VER/PTR must match an embedded sample
(`"rea-agents@6.7.0"`, `"6.5.0"`, `"~/.kimi-code/config.toml:1478"`), and the G2
line prints `current-ok`, `total-loci` and the per-needle booleans.

Measured effect (receipts/proto.matrix.json + `proto.<spec>.out`):

| spec | proto exit | proto verdict | proto G2 line |
|---|---|---|---|
| `full` | 1 | FAIL | SUSPECT (current-ok=0 total-loci=0 needles=[F,F,F]) |
| `pin` | 1 | FAIL | SUSPECT (5, 17, [F,T,T]) |
| `ver` | 1 | FAIL | SUSPECT (4, 8, [T,F,T]) |
| `ptr` | 1 | FAIL | SUSPECT (5, 17, [T,T,F]) |
| `pin+ver` | 1 | FAIL | SUSPECT (0, 2, [F,F,T]) |
| `pin+ptr` | 1 | FAIL | SUSPECT (5, 17, [F,T,F]) |
| `ver+ptr` | 1 | FAIL | SUSPECT (4, 7, [T,F,F]) |
| `h-ver67` | 1 | FAIL | SUSPECT (7, 11, [T,F,T]) |
| `h-ver65` | 1 | FAIL | ok (9, 12, [T,T,T]) — survives the liveness samples; FAILs via G11 |
| `h-pin64` | 1 | FAIL | SUSPECT (5, 17, [F,T,T]) |
| `h-all67` | 1 | FAIL | SUSPECT (9, 10, [T,F,T]) |

Unmutated control under P1: PASS `(stale=0 ambiguous=0 undeclared=0 unresolved=0)`
exit 0 on both the scratch root and the real repo root
(`current-ok=5 total-loci=17 needles=[True, True, True]`).

Consequence for the frozen claim's wording: **the H3 patch as drafted
(`g2_ok = len(current-ok) > 0`) hardens only the total-blindness corner.** Measured
on the pre-landing instrument it leaves `pin`, `ptr`, `pin+ptr`, `ver+ptr` and
`h-pin64` as green PASSes (5 of the 11 injections), plus it cannot see coverage
narrowing at all — `h-ver65` survives even the prototype's liveness samples because
the sample value `6.5.0` still matches the narrowed needle. The prototype closes
needle *death* (all 7 death-specs FAIL) but not needle *narrowing*: the honest
residual is H4/self-certification — only the external locus-count + scope-diff
audit sees narrowing. The landing (§6) took the floor only, which is exactly this
boundary.

## 4. Side finding — pointer shadowing (new, measured; adjacent to H3, not the H3 class)

Baseline SCORECARD.md block 288-295 holds INFO (mixed dispositions): `:289 bare
omp=6.5.0 current-ok`, `:291 bare kimi=6.4.0 historical`. Its `~/.kimi-code/config.toml:1478`
pointer is **never evaluated** because `classify()` collects PTR only when no PIN/VER
matched in the block (`c1-census-v10.py:340-342`). Under VER-muting the block's
bare asserts vanish, PTR fires, and `ptr_check` reads the live line
(`capabilities = [ "image_in", "always_thinking", "tool_use" ]`, measured read-only
at `~/.kimi-code/config.toml:1478`) → `STALE (line holds no rea-agents pin)` →
FAIL. So at HEAD a stale pointer sits in a block the census cannot see it in, and
the injection that exposes it (needle loss) is the same class H3 is about: the
instrument's PASS is partly vacuous there. Not a HEAD verdict defect under the
instrument's own unit (the pointer is out of unit as long as the block carries a
version), but it belongs in the round's named debt.

## 5. Attacks / refutations attempted (this seat)

- A1 full-neuter → declared PASS (blind): **reproduced**, pre-landing (H3 open).
- A2 needle-pair neutering (all three pairs) → 2 PASS / 1 FAIL: **partial blindness
  escapes** any loci-floor that keeps ≥1 locus; the FAIL is accidental (STALE).
- A3 needle-narrowing: `h-ver67`/`h-ver65`/`h-all67` FAIL by accident (masked
  pointer STALE at SCORECARD:291, or G11 at SCORECARD:530), never by a floor;
  `h-pin64` (a narrowing that keeps only a non-live-equal value class) reads
  **PASS** — measured, not inferred (receipts/pre.h-pin64.out). Under the landed
  floor it still reads PASS (receipts/post-landing/post.h-pin64.out).
- A4 FAIL→PASS laundering under `ver+ptr`: **confirmed** pre-landing, and it
  **survives the landing**: post `ver+ptr` still PASS exit 0
  (receipts/post-landing/post.ver+ptr.out) — the floor needs only one surviving
  current-ok locus.
- A5 blind-pass fixture equivalence to CR-5's round-1 fixture: checkable by digest
  (`pre-landing-v10.py` == `census-after.py`, §1); the receipts differ in tag only.
- A6 prototype false-positive check: unmutated run under P1 → PASS (no over-firing
  on the real tree / byte-identical scratch root).

## 6. Post-landing half (COMPLETE)

EX-16 landed the r9 H1+H3 write at 2026-10-19 09:06:50 local; landed instrument
sha256 `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`
(28606 B, 560 lines). Snapshot `tools/landed-instrument-82fb807e.py`, diff
`receipts/post-landing/landing-diff-6f1d19ff-to-82fb807e.patch`. The landing adds
G19 (unreadable/truncated scoped file → `UNREADABLE` fail class) and G20 (`g2_ok =
current-ok loci ≥ 1`, with `DECLARED FAIL CLASSES` in the text report and
`declared_fail_classes`/`g2_floor` in `--json`). Gate sha re-checked unchanged
after each measurement batch.

Matrix, same byte-identical root (`tools/neuter.py --src instrument/landed.py
--tag post`; receipts/post-landing/post.matrix.json + `post.<spec>.out`):

| spec | pre exit | post exit | post verdict | post G2 line | post declared class |
|---|---|---|---|---|---|
| `full` | 0 PASS | **1** | **FAIL** | SUSPECT (current-ok loci=0, total loci=0, floor=1) | `['BLIND-INSTRUMENT']` |
| `pin` | 0 PASS | 0 | PASS | ok (5, 17, floor=1) | `[]` |
| `ver` | 1 FAIL | 1 | FAIL | ok (4, 8, floor=1) | `[]` (STALE=1) |
| `ptr` | 0 PASS | 0 | PASS | ok (5, 17, floor=1) | `[]` |
| `pin+ver` | 1 FAIL | 1 | FAIL | SUSPECT (0, 2, floor=1) | `['BLIND-INSTRUMENT']` |
| `pin+ptr` | 0 PASS | 0 | PASS | ok (5, 17, floor=1) | `[]` |
| `ver+ptr` | 0 PASS | 0 | PASS | ok (4, 7, floor=1) | `[]` |
| `h-ver67` | 1 FAIL | 1 | FAIL | ok (7, 11, floor=1) | `[]` (STALE=1) |
| `h-ver65` | 1 FAIL | 1 | FAIL | ok (9, 12, floor=1) | `[]` (G11 :530) |
| `h-pin64` | 0 PASS | 0 | PASS | ok (5, 17, floor=1) | `[]` |
| `h-all67` | 1 FAIL | 1 | FAIL | ok (9, 10, floor=1) | `[]` (STALE=1) |

Verified points:

1. **Declared FAIL for the H3 class — PASS.** `full`: exit 1,
   `VERDICT: FAIL`, `G2 SUSPECT (current-ok loci=0, total loci=0, floor=1)`,
   `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` (receipts/post-landing/post.full.out);
   `--json` agrees: `{'verdict': 'FAIL', 'g2_ok': False, 'g2_floor': 1,
   'declared_fail_classes': ['BLIND-INSTRUMENT']}`, exit 1 (post.full.json).
2. **Unmutated control unchanged — PASS 0/0/0/0, exit 0**, loci `6/9/2`,
   `current-ok loci=5 total loci=17`, `DECLARED FAIL CLASSES: []`, on both the
   byte-identical scratch root and the real repo root.
3. **Independent agreement with EX-16's own receipts**: their `h3-blind-all`
   (needles `(?!x)x`) → `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` exit 1, and
   their `h3-blind-pin` → PASS exit 0 (`claims/c2/EX-16/receipts/after/`) replicate
   this seat's `full` and `pin` rows. Their `ordinary-at-head.txt` is line-identical
   to this seat's `post.baseline.txt` (only a trailing `exit=` marker differs) —
   same landed instrument, same tree, independent run.
4. **H1 cross-check (not this seat's task, same landing)**: absent `SKILL.md` →
   `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']`,
   `DECLARED FAIL CLASSES: ['UNREADABLE']`, exit 1 (post.h1-absent-skill.out).
5. **Residual, measured, and named in the landed header**: `pin`, `ptr`,
   `pin+ptr`, `ver+ptr`, `h-pin64` stay PASS — partial blindness (needle death with
   ≥1 surviving current-ok locus, or coverage narrowing) is out of the floor's
   reach. The landed header states the same boundary and assigns it to H4/self-
   certification (external locus-count + scope-diff audit). This seat's pre-landing
   and prototype measurements independently confirm that boundary, and the
   prototype's needle-liveness self-test (`tools/proto.py`, this seat's patch text)
   would additionally catch all needle-death partials, but not narrowings.

### 6b. Revision 2 of the landing (`c95a5cf3…`) — non-regression BREAK, measured

EX-16 (or a c2 seat acting on EX-14's variant B) replaced the global floor with a
**per-readable-file floor** at 2026-10-19 09:10:56 local: sha256
`c95a5cf30201a1f862849b04701330e65b3777c877fb9467e4ee38656bbb0d4f` (30486 B),
snapshot `tools/landed2-instrument-c95a5cf3.py`; rev1→rev2 diff
`receipts/post-landing/landing-diff-82fb807e-to-c95a5cf3.patch`.

**The unmutated run at HEAD — both the byte-identical scratch root and the real
repo root — now reads `VERDICT: FAIL`, exit 1, `DECLARED FAIL CLASSES:
['BLIND-INSTRUMENT']`**:

```
G2 positive-assertion guard: SUSPECT (current-ok loci per file:
   PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Receipts: `receipts/post-landing/post2.baseline.txt` (scratch root, exit 1),
`post2.baseline-repo.txt` (real repo root, exit 1), `post2.baseline.json`
(`--json` exit 1, `declared_fail_classes: ['BLIND-INSTRUMENT']`).

Cause, measured: SKILL.md carries no current-ok locus at HEAD — its two loci are
one historical pin (`:12 rea-agents@6.4.0`, inline marker) and one DATED-section
locus — so the per-file floor is unsatisfiable for that file on the clean tree
(`floor['SKILL.md'] = 0`). The `G2 ... per file` line is the receipt.

Consequences:

- The chain c2 claim's own non-regression clause ("ordinary runs at HEAD stay
  PASS 0/0/0/0") is **violated** by revision 2 as it currently stands. The clean
  tree must not fail a fail-closed instrument.
- The revision-2 matrix therefore loses discriminating power: `pin`, `ptr`,
  `pin+ptr`, `h-pin64` flip to FAIL, but by the *same* per-file floor that the
  clean tree trips (SKILL.md=0 in every one of them), not because the injection
  was detected. `receipts/post-landing/post2.matrix.json`; the only spec that
  still PASSes is `ver+ptr` (SKILL.md=1 there via a different assert path).
- Either the landing needs a current-ok-bearing locus in SKILL.md's CURRENT rows
  (a scope/text edit, i.e. outside the instrument — EX-16 may not own it), or the
  floor needs the per-file variant restricted to files the declared unit can
  actually make current-ok (EX-14's occupancy map is the input), or the floor
  reverts to revision 1's global form plus the liveness self-test of §3.
- Revision 1 (`82fb807e…`) remains the last identity this seat measured as
  non-regressing *of that pair*; the live instrument must pass the ordinary run,
  so the parent should treat the instrument as mid-iteration until a sha does
  (see §6c — revision 3 does).

### 6c. Revision 3 (`df9ffdf9…`) — non-regression restored; this is the state this seat certifies

Landed 2026-10-19 09:11:50 local, sha256
`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` (snapshot
`tools/landed3-instrument-df9ffdf9.py`; live-sha re-verified identical).
Change from revision 2: the floor counts **current-ok detections** (asserts) per
file instead of current-ok *blocks* — SKILL.md's only locus-bearing block is mixed
(info) and carries current-ok dets, so the block-count form false-FAILed the
ordinary run and the det form does not (the instrument's own comment says exactly
this). Diff: `receipts/post-landing/landing-diff-82fb807e-to-c95a5cf3.patch` covers
rev1→rev2; rev2→rev3 is the counting change quoted above.

Measured on the same byte-identical root and on the real repo root:

- **Ordinary run: PASS `(stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0**,
  `G2 ok (... PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)`,
  `DECLARED FAIL CLASSES: []` — `receipts/post-landing/post3.baseline.txt`,
  `post3.baseline.json` (`current_ok_per_file` = `{PROVINCE.md: 17, SCORECARD.md: 14,
  SKILL.md: 3}`, `g2_floor: "1/readable-file"`, exit 0).
- **H3 discriminator holds**: `full` (all needles dead) → exit 1, FAIL,
  `G2 SUSPECT (... all files =0; total loci=0; floor=1/file)`,
  `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` (post3.full.out). `pin+ver` → FAIL
  same class. Residual unchanged: `pin`, `ptr`, `pin+ptr`, `ver+ptr`, `h-pin64`
  still PASS (`post3.matrix.json`) — partial blindness is out of a token floor's
  reach, exactly as the landed header states.
- **Coin-flip check on the count semantics**: with the ordinary run PASS and
  `full` FAIL, the rev-3 floor is discriminating; the earlier rev-2 FAILs of
  `pin`/`ptr`/`pin+ptr`/`h-pin64` were the false-positive class, not detection.
- **Label defect, minor**: the G2 line prints `current-ok loci per file: …` but the
  numbers are current-ok *dets* (assertions) — the JSON field is named
  `current_ok_per_file` with the same numbers. Same class as the round-1 C3 label
  finding (`MTIME_UTC` mislabel): the value is right, the label over-claims. Named,
  not blocking.
- Order of identities certified by this seat, in time: `6f1d19ff` (before, PASS +
  blind-PASS), `82fb807e` (rev1, PASS + declared FAIL), `c95a5cf3` (rev2, clean-tree
  FAIL — regression, recorded), `df9ffdf9` (rev3, PASS + declared FAIL), `a4c16763`
  (rev4, same verdicts as rev3 — see §6d).

### 6d. Revision 4 (`a4c16763…`) — header/docstring only; identical verdicts; FINAL CERTIFIED STATE

Landed 2026-10-19 09:15:39 local, sha256
`a4c167631269e5110fbdcf323b6be2a779eaa1e0ca79c98201419261ba9c6bfb` (31364 B),
snapshot `tools/landed4-instrument-a4c16763.py`; rev3→rev4 diff
`receipts/post-landing/landing-diff-df9ffdf9-to-a4c16763.patch` is the module
docstring title (now "v10-r9") and the usage line — no logic change. Re-ran the
whole battery: identical results to rev3 — ordinary run PASS 0/0/0/0 exit 0 on both
roots (`post4.baseline.txt`, `post4.baseline-repo.txt`, `post4.baseline.json`),
`full` → exit 1 FAIL `['BLIND-INSTRUMENT']`, `pin+ver` → FAIL same class, residual
PASS set `{pin, ptr, pin+ptr, ver+ptr, h-pin64}` (`post4.matrix.json`). The
6f1d19ff→a4c16763 full diff is also saved
(`landing-diff-6f1d19ff-to-a4c16763.patch`) for a single-identity review of the
landing. **rev4 `a4c16763…` measured clean; superseded by rev5 below (same
  verdicts).**

### 6e. Revision 5 (`d0772ce8…`) — doc-only; verdicts identical; re-run tool

Landed 2026-10-19 09:18:14 local, sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`. rev4→rev5 diff
`receipts/post-landing/landing-diff-a4c16763-to-d0772ce8.patch` touches only the
G20 provenance docstring and the verdict-line wording ("current-ok DETECTION per
readable scoped file"); no logic change. Quick battery re-run (control + the H3
discriminators + residual subset): ordinary run PASS 0/0/0/0 exit 0 on the live
repo root, `full` → exit 1 FAIL `['BLIND-INSTRUMENT']` (all files 0), `pin+ver` →
FAIL same class, residual PASS set `{pin, ptr, pin+ptr, ver+ptr, h-pin64}` unchanged
(`receipts/post-landing/post5.baseline.txt`, `post5.matrix.json`).

Churn note for the parent: the gate changed **five times in twelve minutes**
(`6f1d19ff` → `82fb807e` → `c95a5cf3` → `df9ffdf9` → `a4c16763` → `d0772ce8`);
one revision (rev2) broke the ordinary run and was corrected one minute later. Any
certification here is bound to a sha and a time. To re-certify after further edits
run `tools/certify.sh` — it copies the live gate + the three scoped files to
`/var/tmp/ex19-cert`, prints the live sha, the ordinary-run verdict, and the full
11-spec matrix (expect: ordinary PASS 0/0/0/0; `full`/`pin+ver` FAIL
`['BLIND-INSTRUMENT']`; `pin`, `ptr`, `pin+ptr`, `ver+ptr`, `h-pin64` residual PASS).

## 7. Blockers

- None. All scratch under `/var/tmp/ex19` (never `/tmp`).
- Separately named (round-1 item, still open): the pointer-shadowing hole of §4
  (stale `~/.kimi-code/config.toml:1478` pointer at SCORECARD.md:291 invisible while
  the block carries a version) — block 288-295 still reads INFO under the landed
  instrument, so the pointer remains unevaluated at HEAD.
