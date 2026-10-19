# EX-37 — census interplay: does C3's custody-pair landing perturb the census?

Seat EX-37 · chain c3 · role executor · wave arc3-loop1-round2 · 2026-10-19.
Task (seat line): after EX-31 lands (`.ufo/gates/custody-pair/`), run the census
at HEAD — PASS expected, new files introduce no gated token; capture.

Typed claim under test: **the census's verdict at HEAD is invariant under EX-31's
landing** — the new custody-pair files cannot enter the census's read path, the
census's external inputs (the three client config files) are not written by the
custody tool, and the census's own instrument change (C2/EX-16, landed mid-seat)
does not disturb the verdict.

## 0. Verdict — CONFIRMED on landed bytes

EX-31 landed `.ufo/gates/custody-pair/{custody-pair.py,README.md}` at 12:03-12:07
UTC; the census at HEAD reads **`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)`, exit 0, `DECLARED FAIL CLASSES: []`**. The strongest form of the
invariance holds: **the pre-landing v10 instrument's full output is byte-identical
across the landing (4405 B both sides, `diff` exit 0)** while two new gated-token
files sit on disk — because the census reads only the three files named in its
SCOPE table and never walks the tree. The check is non-vacuous: the same token
class in a scoped file fires `undeclared=1 → FAIL exit 1` (T1/T4), and the landed
C2 closures fire on their own attack roots (T5/T6).

Two incidental findings for the parent are in §7 (landed instrument change
mid-seat; a new `README.md` inside EX-31's target dir, adjudication note).

## 1. Instrument and inputs pinned (sha256)

| object | pre-landing (T0) | post-landing |
|---|---|---|
| HEAD | `14b1682b1128d2e41085ebc79c9addeb8786d420` | same (nothing committed by seats) |
| `.ufo/gates/c1-census-v10.py` | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (23939 B) | at capture: `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` (C2/EX-16's H1+H3 landing); **later** `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` (per-file floor; §5 re-verification) |
| `PROVINCE.md` | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 L) | **identical** — C3's landing does not touch it |
| `SKILL.md` | `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` (371 L) | **identical** |
| `SCORECARD.md` | `a7c72950094ecae0e67204668dac21138c1d5d613bb9e36f1bec241b834f4a93` (1417 L) | **identical** |
| `.ufo/gates/custody-pair/custody-pair.py` | — | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (39157 B, ino 37769730) |
| `.ufo/gates/custody-pair/README.md` | — | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` (6180 B, ino 37777365) |
| live anchors (census re-derives) | `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}` | identical |

Evidence: `sha256.txt` (T0), `after/sha256.txt`, `instrument-before.sha`,
`after/instrument-landed.py`, `after/census.txt`, `after/census.json`,
`after/custody-pair-listing.txt`, `after/git-state.txt`.
`git status` post-landing: only ` M .ufo/gates/c1-census-v10.py` (C2's instrument
write), `?? .ufo/gates/custody-pair/` (EX-31's landing), the round-2 wave tree and
`__pycache__` — **no scoped production file is modified.**

## 2. Static reason the new files cannot enter the census

The census's read-set is built **from the declared SCOPE table, not by walking
the tree** (line numbers per revision, re-derived after each instrument change —
same two statements either side of C2's landing):

```
T0  instrument 6f1d19ff…     landed instrument 82fb807e…
:433  files = sorted({s[0] for s in SCOPE})      :484  (same statement)
:441  lines = open(os.path.join(args.root, f))   :493  (same statement)
```

Machine-checked against both revisions (`scope-static-assert.txt` for T0,
`after/scope-static-assert-landed.txt` for the landed bytes — each reports
`SCOPE rows: 20`, `read-set files: ['PROVINCE.md', 'SCORECARD.md', 'SKILL.md']`,
`any row path starting with .ufo/: False`):

```
SCOPE rows: 20 | read-set files: ['PROVINCE.md', 'SCORECARD.md', 'SKILL.md']
any row outside the 3 canonical files: False
any row path starting with .ufo/ : False
```

A file under `.ufo/gates/custody-pair/` is therefore not merely "out of scope"
in the sense of having no declared row — it is **never opened**. No code path
turns its bytes into a locus, a scope error or a gated-token reading.

Adjacent instrument (not this chain's claim, measured for completeness): the
citation-drift probe's target set contains **no** `.ufo/gates/` target
(`targets containing .ufo/gates/: NONE`; the one `custody` substring,
`pointer-table.json:17`, is inside a `must_match` *value* —
`"16:57:35Z custody receipt"` — not a target path), and the probe grades Git
objects at `--rev`, so an untracked new directory is invisible to it twice over.
Probe at HEAD, pre-landing: `clean findings=0 exit=0` (`--strict`) ; post-landing,
with `.ufo/gates/custody-pair/` on disk: `--strict → clean findings=0 exit=0`,
default → `reported findings=0 exit=0` (`after/probe-*-postlanding.out`).

## 3. Before — census at HEAD, T0 (pre-landing)

```
$ python3 .ufo/gates/c1-census-v10.py            # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

JSON (`census.json`): `verdict PASS`, `current_ok 5`, `historical 5`, locus
lines `PROVINCE :44 :67 :125 · SCORECARD :537 :619 :620 :699 :732 :753 ·
SKILL :12`. The three scoped files were byte-clean against HEAD at capture.

## 4. Landing shape ↔ census, simulated before the bytes existed

Both directions measured on scratch (`/var/tmp/ex37/sim/`; `runs/*.out|exit`):

**T2 — poison in the landing's shape (out-of-scope dir).** Scratch root = the
three scoped files + `.ufo/gates/custody-pair/{custody-receipt.py,receipts.txt}`
carrying heavy gated tokens (`rea-agents@6.7.0`, `~/.kimi-code/config.toml:12`,
`mcp_config.json`, `omp`, `devin`, `npx`):

```
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

Counts identical to T0 (`6/9/2`, `current_ok 5`).

**T1 — positive control: same token class, in-scope.** `rea-agents@9.9.9`
appended to scratch SCORECARD.md past the declared bound:

```
SCORECARD.md   lines=1419 loci=10
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)   exit=1
```

T1/T2 differ only in file placement, so T2's PASS is a reading, not a blind spot.

## 5. Instrument drift mid-seat — the prediction, then the actual bytes

C2's claim moves the instrument in the same round (EX-16). I pre-simulated the
predicted H1+H3 instrument (built from the r1 patch texts RV-11
`proposed-missing-file-guard` and CR-5 `proposed-g2-positive-floor`;
`h1h3-sim-diff.txt`) and measured: PASS on HEAD, PASS on the poison root, FAIL on
absent-SKILL (`UNREADABLE`), FAIL on a needles-neutered copy (`G2 SUSPECT`,
exit 1) — the same four cells the *actual* landed instrument produces (§8 T4-T6).

**EX-16 landed mid-seat** (between T0 and the post-landing capture; my poll's
stability watcher pinned EX-31's files, and the instrument hash moved
`6f1d19ff…` → `82fb807e…`). The landed bytes differ from my simulation in text
(they declare new classes `G19 UNREADABLE` / `G20 positive floor`, print
`DECLARED FAIL CLASSES: []` and `floor=1`) but agree in behaviour on all four
cells. Landed-instrument property relevant to this seat's claim, machine-checked:
**SCOPE rows identical before/after (20 rows, tuple equality True)** — C2's edit
did not widen, re-class or re-key the declared bounds, so my §2 disjointness
argument survives the instrument change unmodified.

**The instrument moved a second time within this seat** (`82fb807e…` →
`df9ffdf9…`; the floor became per-readable-file, EX-14's variant B). Because the
seat's claim is about the *landing*, not about any one instrument revision, the
whole matrix was re-run against the newest revision at 12:2x UTC and the
rest of §6 stands unchanged:

```
r3-head     VERDICT: PASS 0/0/0/0  exit 0   (per-file floor: PROVINCE 17 / SCORECARD 14 / SKILL 3)
r3-poison   VERDICT: PASS 0/0/0/0  exit 0   — same counts as HEAD with all custody-pair files present
r3-teeth    VERDICT: FAIL undeclared=1       exit 1
r3-missing  VERDICT: FAIL, UNREADABLE ['SKILL.md: FileNotFoundError']  exit 1
r3-blind    VERDICT: FAIL, G2 SUSPECT (0/0/0 per file), DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']  exit 1
```

and the byte-identity test re-passes on the current tree with the T0 instrument
(`diff` vs `before/census.txt` → identical, 4405 B). SCOPE rows remain
tuple-identical to T0 across both instrument revisions (`T0==landed2: True`),
so the neutrality result has now survived three instrument revisions and one
tree change. Outputs: `after/r3-*.out|exit`, `after/v10-full-on-tree-r3.out`,
`after/instrument-landed2.py` (sha in `after/sha256.txt`).

## 6. After — post-landing capture (the seat's deliverable measurement)

Capture time 12:09 UTC; files stable ≥ 90 s before and re-verified after
(`stability.log`: `custody-pair.py` `112d01dc…` unchanged across 6 samples;
`README.md` `fa484d57…`). Full outputs in `after/`.

```
$ python3 .ufo/gates/c1-census-v10.py                 # landed instrument, exit 0
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci=5, total loci=17, floor=1)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

**T3 — byte-identity across the landing (the sharp form).** The T0 instrument
copy run *on the post-landing tree*, in the same mode as the T0 capture:

```
$ diff before/census.txt after/v10-full-on-postlanding-tree.out   → exit 0
$ wc -c before/census.txt after/v10-full-on-postlanding-tree.out  → 4405 / 4405
```

Identical instrument, tree changed by EX-31's landing → **byte-identical output**.
Determinism: the landed instrument's `--quiet` run repeated → identical
(`diff after/census-quiet.txt after/landed-head-2.out` → no output).

**T4 — landed instrument on the actual landing's bytes (poison cell).** All files
of `.ufo/gates/custody-pair/` copied into a scratch root beside the three scoped
files → `PASS 0/0/0/0`, counts `6/9/2`, `current_ok 5` — identical to HEAD.

**T4b — teeth control on the landed instrument.** In-scope
`rea-agents@9.9.9` appended to a scratch SCORECARD.md →
`VERDICT: FAIL (undeclared=1) exit 1`.

**T5 — H1 class closes (landed instrument).** Scratch root with SKILL.md absent →
`FAIL exit 1`, `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']`,
`DECLARED FAIL CLASSES: ['UNREADABLE']`. (Unpatched control on the same root at
this wave's HEAD: `PASS exit 0` — r1 RV-11 reproduced.)

**T6 — H3 class closes (landed instrument).** All three needle regexes neutered
(`after/blind-landed.py`, sha in `after/sha256.txt`), run at HEAD →
`FAIL exit 1`, `G2 SUSPECT (current-ok loci=0, total loci=0, floor=1)`,
`DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` — the landed floor is literal
(`c1-census-v10.py:518` `g2_ok = n_current_ok > 0`, the old second disjunct gone).
The unpatched v10 copy on the same
fixture reads `PASS exit 0` (vacuous G2) — H3's finding, re-measured.

**T7 — external anchors untouched.** The five custody paths re-hashed/re-stat'ed
post-landing: `after/custody-inputs.diff` **exit 0** — every sha256, size, mtime,
inode and ctime identical to the pre-landing capture. Static corroboration, with
line numbers **re-derived on the landed revision** (`custody-pair.py`
`112d01dc…`, 39157 B; an earlier grep of the mid-write revision is not cited —
line numbers moved by 2 between revisions): the landed tool's write calls target
only its own receipt/self-test outputs
(`custody-pair.py:567,569,572,686,707,720,758,775,785,796,810,851`), it never
references `PROVINCE.md`/`SCORECARD.md`/`SKILL.md` (grep: 0 hits), and its
docstring declares read-only custody (`custody-pair.py:13-15`).

**T8 — gated-token scan of the landed files** (using the census's own regexes,
`after/token-scan.json`): 2 files scanned, **9 lines matching `REA_GATE`**
(`README.md:7-9`, `custody-pair.py:7-9,112-114` — the five custody paths and the
client names), **0 of them carrying a `rea-agents@x.y.z` pin, a bare `6.x.y`
version or a `path:line` pointer.** All 9 would read `UNDECLARED` if the census
ever walked them; it does not walk them (§2), and this seat measured that the
walk does not happen. So: "new files introduce no gated token" is true in the
operative sense (no gated token enters the census's read-set); in the literal
sense the files *do* contain client-name/path tokens, which is expected of a
custody tool and inert here. The scan is the receipt for the difference.

## 7. Attacks / refutations attempted

- **A1 "the census might walk `.ufo/gates/` implicitly"** — REFUTED statically
  (§2) and behaviourally (T3 byte-identity, T4 identical counts).
- **A2 "T2/T4's PASS is vacuous"** — REFUTED by T1/T4b: same token class,
  in-scope file → `undeclared=1`, exit 1.
- **A3 "the custody tool could move the census anchors by touching a config"** —
  REFUTED on landed bytes: T7 diff exit 0 across all five paths (sha256 + mtime +
  inode + ctime), plus the tool's static write-path audit. This was the only
  channel by which C3's landing could plausibly reach the census (a moved anchor
  would re-pin `live_pins()` and could turn a current-ok locus STALE or trip
  ANCHOR-FAIL exit 2); it is closed.
- **A4 "C2's v11 instrument could couple the two chains"** — MEASURED, not
  merely argued: the landed instrument is neutral on HEAD and on the poison root
  (T3/T4), fail-closed on its own attack roots (T5/T6), and its SCOPE rows are
  tuple-identical to v10's (§5).
- **A5 "line-shift: the landing could shift scoped line numbers"** — REFUTED:
  the three scoped files' sha256 are unchanged from T0 (§1), so no line can move.
- **A6 "the census reads the worktree, so the parent's records append is the real
  coupling risk"** — ACCEPTED as a named residual (§8), owned by C2's chain, not
  by this landing.
- **A7 "EX-31 might still be writing while I capture"** — GUARDED: hash-stability
  watcher required ≥ 90 s of identical content over two files before capture, and
  the hashes were re-verified after the capture (identical). An early sample did
  catch the file mid-write (two different hashes 8 s apart at 12:04:22/12:04:30),
  which is why the watcher exists and its log is kept.

## 8. Residuals / gaps / notes for the parent

- **The census instrument moved twice inside this seat** (`6f1d19ff…` T0 →
  `82fb807e…` H1+H3 → `df9ffdf9…` per-file floor). All §6 cells are measured on
  landed bytes, and §5 re-runs the whole matrix against the newest revision;
  SCOPE rows are tuple-identical to T0 across both moves. If the instrument
  changes again before the records commit, T3's byte-identity must be re-run (it
  is instrument-dependent by construction; the T4-T6 class closures and the §2
  disjointness argument are the durable parts).
- **`.ufo/gates/custody-pair/README.md` (new, `fa484d57…`) exists** inside EX-31's
  sanctioned target dir. Low-risk observation, flagged for adjudication: the seat
  rules forbid seats *editing* README files; whether a *new* README created by the
  designated implementer inside its own target dir counts as sanctioned is the
  parent's call, not this seat's. The census is indifferent to it (T3/T4).
- The parent's records append to SCORECARD.md is **not** covered by this claim
  (§7 A6): text appended past `SCORECARD.md:855` must be locus-free in the
  census's unit (`rea-agents@x.y.z`, bare `6.x.y`, `~`/`/`-absolute `path:line`),
  or the bound must be re-keyed in the same commit. The landed H1 truncation rule
  also means any later scoped-file edit that *shrinks* a file below its declared
  max end now reads `UNREADABLE` (fail) — not exercised by this landing, named so
  the records commit does not trip it.
- All simulations used scratch roots under `/var/tmp` (standing `/tmp` EDQUOT
  hazard). Scratch kept for the parent's convenience; nothing under `/var/tmp`
  is evidence-of-record — every cited output is also committed under
  `claims/c3/EX-37/`.
- Evidence index: `before/` (T0: `census.txt`, `census.json`, `sha256.txt`,
  `custody-inputs-pre.txt`, `instrument-before.py`), `after/` (post-landing:
  `census.txt`, `census.json`, `sha256.txt`, `custody-pair-listing.txt`,
  `git-state.txt`, `token-scan.json`, `v10-full-on-postlanding-tree.out`,
  `v10-invariance-modesmatched.diff`, `landed-*.out|exit`,
  `teeth-actual-instrument.*`, `poison-actual-instrument.*`,
  `scope-static-assert-landed.txt`, `blind-landed.py`, `probe-*-postlanding.out`,
  `instrument-landed2.py`, `blind-landed2.py`, `r3-*.out|exit`,
  `v10-full-on-tree-r3.out`), `runs/` (T1/T2 + simulated-v11 matrix),
  `scope-static-assert.txt`, `h1h3-sim-diff.txt`, `poll.log`, `stability.log`.
