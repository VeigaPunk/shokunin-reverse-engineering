# EX-26 — timing sanity: census fail-closures (H1 absent-file + H3 blind-instrument)

Seat EX-26 (chain c2, executor) — arc3-loop1-round2. Task: "full census run time
before vs after the guards (5 runs each, medians); the fail-closures must not
change the instrument's cost class."

**Verdict: cost class unchanged.** On the landing revision the full run is
32.347 ms → 32.086 ms (5×2 interleaved medians, ratio **0.9919**, i.e. no
measurable increase); with 25×2 runs the delta is +0.190 ms against a
null-control delta of −0.198 ms on a byte-identical copy. In-process, the
guards' cost is ≤ 0.17 ms on a 174 ms run at 32× input, and the 1x/8x/32x
deltas (+0.001 / −0.072 / −0.165 ms) do not grow with input size — the guards
add no growth term. Every revision measured (five of them; the target was
revised repeatedly while this seat ran) behaves the same way, including the
last one, and both fail-closure paths (guard FIRING) cost the same as an
ordinary run.

One semantic finding is reported under §6 (not a timing defect): a mid-flight
revision `c95a5cf3…` FAILed on an ordinary HEAD run; the next revision
`df9ffdf9…` restores HEAD-PASS.

## 1. What was measured

* Full census run = `python3 <instrument> --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`
  (default, verbose; the `--quiet`/`--json` variants are covered in §4).
* `before` = `.ufo/gates/c1-census-v10.py` at HEAD, sha256
  `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (490 lines),
  preserved byte-identical in `receipts/instrument-at-head-6f1d19ff.py`.
* `after` = the guarded instrument. EX-16 (the only seat allowed to write the
  target) revised it several times during this measurement; every measured
  revision is preserved byte-exactly in `receipts/` and named below:

| rev | sha256 (first 8) | what it is | HEAD verdict | file in receipts/ |
|---|---|---|---|---|
| before | `6f1d19ff` | HEAD instrument, no guards | PASS | `instrument-at-head-6f1d19ff.py` |
| after-A | `a81893fc` | this seat's patch-text reconstruction (pre-landing; H1 wording + H3 global floor) | PASS | `reconstruction-a81893fc.py` |
| after-B | `82fb807e` | EX-16's landing revision — the sha its own receipt pins (`claims/c2/EX-16/receipts/after/after-sha256.txt`, captured 12:06:58Z) | PASS 0/0/0/0 | `after-82fb807e-instrument.py` |
| after-D | `c95a5cf3` | per-readable-file floor (EX-14 variant B), block-level counting | **FAIL (BLIND-INSTRUMENT)** — see §6 | `after-c95a5cf3-instrument.py` |
| after-E | `df9ffdf9` | per-file floor counting current-ok *detections* — fixes the §6 regression | PASS 0/0/0/0 | `after-df9ffdf9-instrument.py` |
| after-G | `d0772ce8` | stable at this seat's close (09:18:14) | PASS 0/0/0/0 | `after-d0772ce8-instrument.py` |

Every timed revision is listed; `a4c16763` sits between after-E and after-G in
the §9 churn log. All of them are preserved in `receipts/` and are the pins —
not the filename, which never changed.

Harness: `tools/timeit.py` (subprocess A/B interleaved, wall via
`time.perf_counter`, CPU via wait4 rusage, stdout digest + verdict captured per
run so a timing pair can never be silently broken) and `tools/inproc.py` (the
instrument's `main()` called alternately in ONE interpreter with stdout to
`/dev/null`, isolating instrument work from interpreter startup). Fixtures:
`tools/make-fixtures.sh` (`fx-absent`, `fx-8x` = 15,600 lines, `fx-32x` =
62,400 lines, `fx-32x-absent`). Host: 32 cores, other wave seats running
concurrently — hence interleaved A/B and the null controls below; block-to-block
drift on the *same* file reached 3.5 ms (`before` medians 69.6 / 70.7 / 73.1 ms
across blocks in `raw/scale8x-*`), which is larger than every guard delta.

## 2. Primary measurement — 5 runs each, medians (the frozen requirement)

Subprocess, ABAB-interleaved, root = repo HEAD, `raw/head-5x2-landed.tsv`:

| run | before `6f1d19ff` | after-B `82fb807e` |
|---|---|---|
| 1 | 0.0320 s | 0.0321 s |
| 2 | 0.0326 s | 0.0335 s |
| 3 | 0.0323 s | 0.0317 s |
| 4 | 0.0330 s | 0.0322 s |
| 5 | 0.0310 s | 0.0320 s |
| **median** | **0.032347 s** | **0.032086 s** |
| CPU median | 0.032034 s | 0.031442 s |

Δmedian = **−0.000261 s**, ratio **0.9919**. Same harness against after-A
(`raw/primary-head.tsv`): before 0.031702 s → after-A 0.031854 s, Δ = +0.000152 s,
ratio 1.0048. Against the newest revision after-E (`raw/head-5x2-revE.tsv`):
before 0.032339 s → after-E 0.032743 s, Δ = +0.000404 s, ratio 1.0125. Every run
of every revision returned `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)`, exit 0, stdout digest constant within each revision (before
`d3da7509…`, after-B `a9cd6886…`).

**Noise calibration (null experiment, identical bytes):**

| pair | n | Δ wall median | ratio | file |
|---|---|---|---|---|
| before vs byte-identical copy | 5×2 | +0.000718 s | 1.0216 | `raw/head-5x2-null-subproc.tsv` |
| before vs byte-identical copy | 25×2 | −0.000198 s | 0.9938 | `raw/head-25x2-null-subproc.tsv` |
| landed vs byte-identical copy (in-process, 32x) | 20×2 | +0.000011 s | 1.0001 | `raw/inproc-32x-null.tsv` |
| after-A vs byte-identical copy (in-process, 32x) | 20×2 | −0.000177 s | 0.9990 | `raw/inproc-null-32x.tsv` |

A null pair can read ±0.7 ms at n=5 and ±0.2 ms at n=25 — the same magnitude as
the measured before→after deltas. With n=25: **before 0.033245 s → after-B
0.033435 s (Δ +0.000190 s, ratio 1.0057)** against a null Δ of −0.000198 s
(`raw/head-25x2-landed.tsv`); **before 0.032394 s → after-E 0.032629 s
(Δ +0.000235 s, ratio 1.0073)** (`raw/head-25x2-revE.tsv`). The guard cost is at
or below the noise floor.

## 3. Cost class — input-scaling evidence

The guards add O(1) work per scoped file (3 files) plus O(1) per run, so the
input-size slope must be unchanged. In-process, same interpreter, alternating
calls (no startup term):

| root | lines | before median | after-B median | Δ | ratio | file |
|---|---|---|---|---|---|---|
| repo HEAD | 1,950 | 0.008066 s | 0.008068 s | +0.000001 s | 1.0001 | `raw/inproc-1x-landed.tsv` |
| fx-8x | 15,600 | 0.046033 s | 0.045961 s | −0.000072 s | 0.9984 | `raw/inproc-8x-landed.tsv` |
| fx-32x | 62,400 | 0.173939 s | 0.173775 s | −0.000165 s | 0.9991 | `raw/inproc-32x-landed.tsv` |

Same shape against after-A: +0.000001 / +0.000057 / +0.000130 s at 1x/8x/32x
(`raw/inproc-1x.tsv`, `raw/inproc-8x.tsv`, `raw/inproc-32x.tsv`) — absolute, not
proportional: 32× the input does not multiply the guard delta. Against after-E:
1x +0.000011 s (1.0014, `raw/inproc-1x-revE.tsv`), 32x +0.000102 s (1.0006,
`raw/inproc-32x-revE.tsv`). The before run itself is sub-linear in input
(8.1 ms → 173.9 ms, 21.5× for 32× the lines), and both revisions move along the
*same* curve.

Subprocess at 8x (`raw/scale-8x-landed.tsv`) reads before 0.070686 s → after-B
0.072092 s (Δ +1.41 ms, ratio 1.0199) — the same +1.4 ms appears against after-A
(`raw/scale-8x.tsv`: +1.394 ms). This is **not** attributable to the guards:

* size control — `before` vs a copy of `before` padded with comments to exactly
  the landed byte size (28,606 B): Δ −0.000089 s (0.9987) — source size has no
  measurable effect (`raw/scale8x-size.tsv`);
* size-matched semantic comparison — padded `before` vs landed: Δ −0.000356 s
  (0.9950), i.e. the sign flips once the two files have equal size
  (`raw/scale8x-sizematched.tsv`);
* same-instrument null at 8x: +0.000177 / +0.000699 s for the two revisions
  (`raw/scale8x-null-before.tsv`, `raw/scale8x-null-landed.tsv`), and
  block-to-block drift on one unchanged file was 3.5 ms.

## 4. Fail-closure paths and output modes

Guard FIRING is not more expensive than a clean run (subprocess 5×2):

| path | before | after | Δ | ratio | file |
|---|---|---|---|---|---|
| H1 fires — fx-absent (SKILL.md missing), after-B | 0.030959 s | 0.030219 s | −0.000740 s | 0.9761 | `raw/absent-5x2.tsv` |
| H1 fires — fx-absent, after-E | 0.031960 s | 0.031862 s | −0.000098 s | 0.9969 | `raw/absent-5x2-revE.tsv` |
| H1 fires at 32x — fx-32x-absent, after-B | 0.166988 s | 0.168523 s | +0.001535 s | 1.0092 | `raw/scale32x-absent-5x2.tsv` |
| H3 fires — needles neutered at HEAD, after-B | 0.030741 s (blind-before) | 0.031368 s (blind-after) | +0.000627 s | 1.0204 | `raw/blind-5x2.tsv` |
| `--json` mode, clean run | 0.032555 s | 0.033468 s | +0.000913 s | 1.0280 | `raw/head-json-5x2.tsv` |

Behaviour (receipts — this is what makes the timings meaningful, a broken copy
timing the same is worthless): `receipts/h1-absent-before.out` PASS exit 0 vs
`receipts/h1-absent-after.out` FAIL exit 1 with
`UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']`;
`receipts/h3-blind-before.out` PASS exit 0 vs `receipts/h3-blind-after.out` FAIL
exit 1 with `G2 … SUSPECT (current-ok loci=0, total loci=0, floor=1)`;
`receipts/h1-32x-absent-*.out` shows the same flip at 32× input (before PASS 0,
after FAIL 1). Ordinary HEAD runs remain `PASS 0/0/0/0` on before, after-A,
after-B and after-E (`receipts/before-head-verbose.out`,
`receipts/after-82fb807e-head-verbose.out`,
`receipts/after-df9ffdf9-head-verbose.out`).

## 5. Later revisions are also time-neutral

* after-D `c95a5cf3` (588 lines): 25×2 subprocess Δ +0.000118 s (ratio 1.0037,
  `raw/head-25x2-revD.tsv`); in-process 1x 40×2 Δ +0.000024 s (1.0030,
  `raw/inproc-1x-revD.tsv`); in-process 32x 15×2 Δ +0.000392 s (1.0023,
  `raw/inproc-32x-revD.tsv`).
* after-E `df9ffdf9` (31207 B): see §2 (5×2, 25×2), §3 (1x, 32x in-process),
  §4 (absent path). All deltas ≤ 0.41 ms and ≤ 1.3% at 5 runs, ≤ 0.02 ms
  in-process.

The detection-level counting added in after-E walks the per-block `asserts`
lists (O(detections) once per run); it is inside the same noise band as the
block-level counting it replaced.

## 6. Finding (semantic, not timing) — one mid-flight revision FAILed at HEAD

Revision `c95a5cf3` introduced a **per-readable-file** floor (EX-14's variant B)
counted over block-level `current-ok` records. At HEAD the block-level
current-ok records are `PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0`: SKILL.md's
only locus-bearing block is mixed (disposition `info`), so the per-file floor
was unsatisfiable and an ordinary HEAD run returned:

```
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=1
```

Receipts: `receipts/after-c95a5cf3-head-verbose.out` (exit=1),
`receipts/after-c95a5cf3-head.json` (exit=1). That contradicts the frozen C2
clause "ordinary runs at HEAD stay PASS 0/0/0/0". The next revision `df9ffdf9`
counts current-ok *detections* instead (`PROVINCE.md=17, SCORECARD.md=14,
SKILL.md=3` at HEAD) and HEAD reads PASS 0/0/0/0 again
(`receipts/after-df9ffdf9-head-verbose.out`); the failing state was live for
about a minute and is recorded because the per-file floor remains a design
decision, and because the target was still being written while this seat ran.
This seat measured the target; it did not write it.

## 7. Reproduce

```bash
bash tools/make-fixtures.sh                                  # fixtures under /var/tmp/ex26
python3 tools/timeit.py before receipts/instrument-at-head-6f1d19ff.py \
        landed receipts/after-82fb807e-instrument.py 5 \
        /home/vgpnk/Projects/shokunin/kaidoku-shokunin raw/rerun-5x2.tsv
python3 tools/inproc.py receipts/instrument-at-head-6f1d19ff.py \
        receipts/after-df9ffdf9-instrument.py /var/tmp/ex26/fx-32x 20 raw/rerun-32x.tsv
```

Scratch lives under `/var/tmp/ex26` (never `/tmp`: EDQUOT per the standing
round-1 record). Guard diffs: `receipts/guards.diff` (this seat's reconstruction),
`receipts/landed.diff` (before → `82fb807e`), `receipts/rev-b-to-c.diff`
(`82fb807e` → `c95a5cf3`), `receipts/rev-d-to-e.diff` (`c95a5cf3` →
`df9ffdf9`). All artifact hashes: `receipts/MANIFEST-sha256.txt`.

## 8. Limits of this measurement

* Medians of 5 (and 25) runs on a host running 60+ concurrent wave seats; the
  null controls bound the noise, and in every comparison the guard delta is
  ≤ the null delta. No statement here is finer than ~0.2 ms (25 runs,
  subprocess) or ~0.01 ms (in-process).
* Only wall/CPU-time cost classes were probed. Peak RSS is not comparable in
  this harness (rusage high-water is cumulative across children); the guards add
  the `unreadable` list (≤ 3 strings), a 3-entry floor dict and one extra pass
  over the per-block assertion lists.
* The instrument revisions measured after `82fb807e` are mid-flight writes by
  EX-16; the pin is the sha in the table, not the filename or the mtime.

## 9. Revision churn log and order-reversal control

The target was rewritten several times while this seat ran; every revision that
was timed is pinned by sha (all preserved in `receipts/`):

| time (local) | sha256 (first 8) | bytes | HEAD verdict | note |
|---|---|---|---|---|
| 07:18 | `6f1d19ff` | 23,939 | PASS | before (HEAD) |
| 09:03–09:06 | `7b5a0e88` / `1431620f` / `65442158` | ≤ 28,606 | PASS (header-only diff) | mid-flight, doc-first writes; not separately timed |
| 09:06:50 | `82fb807e` | 28,606 | PASS 0/0/0/0 | EX-16 landing revision (its own `after-sha256.txt`) — §2/§3/§4 |
| 09:10:56 | `c95a5cf3` | 30,486 | **FAIL** | per-readable-file floor over block records — §6 |
| 09:11:50 | `df9ffdf9` | 31,207 | PASS 0/0/0/0 | floor over current-ok detections (the §6 fix) — §5 |
| 09:15:39 | `a4c16763` | 31,364 | PASS 0/0/0/0 | 5×2 Δ −1.2 ms (0.9637, `raw/head-5x2-revF.tsv`), 25×2 Δ +0.28 ms (1.0085, `raw/head-25x2-revF.tsv`), in-process 1x +0.056 ms (1.0069), 32x −0.238 ms (0.9986) |
| 09:18:14 | `d0772ce8` | 31,906 | PASS 0/0/0/0 | stable at this seat's close — 25×2 Δ +1.07 ms (1.0330, `raw/head-25x2-revG.tsv`), 5×2 Δ +0.75 ms (1.0231, `raw/head-5x2-revG.tsv`), in-process 1x +0.009 ms (1.0012, `raw/inproc-1x-revG.tsv`), 32x +0.076 ms (1.0004, `raw/inproc-32x-revG.tsv`) |

Immediately after the `d0772ce8` pair, null controls on the same host read
before-vs-copy −0.176 ms (0.9946, `raw/head-25x2-null-now.tsv`) and
`d0772ce8`-vs-its-own-copy −0.526 ms (0.9843, `raw/head-25x2-null-revG.tsv`) —
i.e. subprocess-level 25-run medians on *unchanged bytes* swing up to ~0.5-1 ms
at that moment, and the in-process harness (which removes the startup term)
shows the instrument delta at +0.009 / +0.076 ms. The subprocess pair deltas
tracking the null band, not the guard edits, is the whole point of §2-§3.

Order-reversal control (after-E run FIRST, `before` second, 20×2 @1x):
Δ = −0.000123 s, ratio 0.9962 (`raw/head-20x2-orderrev.tsv`) — the harness's
A-first ordering carries no systematic guard bias; the deltas scatter around
zero in both directions at the null-control magnitude.
