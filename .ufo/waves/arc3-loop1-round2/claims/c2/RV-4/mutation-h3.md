# RV-4 — mutation test: revert ONLY the H3 floor → neutered needles return to blind PASS

Seat RV-4 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19.
Scope: **mutation test only.** This seat did not write `.ufo/gates/`; every
instrument under test is a scratch copy under `/var/tmp/rv4-mutation/work/`,
mirrored beside this file. Digests: `DIGESTS.md`.

Verdict up front: **the H3 floor is load-bearing and the mutation is killed.**
Reverting only the floor line (1 line, no other edit) restores the round-1
blind PASS on both the pre-landing patch construction and, decisively, on
EX-16's landed bytes.

## 0. Instruments and the mutation

Tested source revisions of `.ufo/gates/c1-census-v10.py`:

| revision | sha256 | what it is |
|---|---|---|
| pre-patch (round-1 close) | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | the state CR-5 measured H3 against |
| EX-16 landed | `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` | 560 lines, mtime 09:06:50 −0300; H1 (UNREADABLE/G19) + H3 (G20/BLIND-INSTRUMENT) |

The census moved twice while this seat worked (`7b5a0e88…` → `a4553911…` →
`82fb807e…`; the last delta was a `%-4d`→`%-4s` print fix, floor line
unchanged). All real-target receipts are stamped with the sha actually run.

**The H3 floor** (landed form, `c1-census-v10.py:518`, in `main()`):

```python
n_current_ok = len(out.get("current-ok", []))
g2_ok = n_current_ok > 0          # H3 floor; the old form was:
# g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
```

**The mutation** = revert that floor only, keeping everything else (the
`declared` list, the diagnostic print, the H1/UNREADABLE guard) byte-identical
(`instruments/real-target/mutation-landed.diff`, 1 hunk, 1 changed line;
`instruments/mutation.diff` is the same revert against the pre-landing
construction):

```diff
-    g2_ok = n_current_ok > 0
+    g2_ok = n_current_ok > 0 or (not stale and not unatt and not undecl and not unres)
```

**The injection** (CR-5's round-1 technique, unchanged): the three needle
regexes replaced by never-matching patterns —
`PIN = re.compile(r"rea-agents@(ZZZ\d+)", re.I)`,
`VER = re.compile(r"(?<![\d.])9\.\d+\.\d+")`,
`PTR = re.compile(r"((?:~|/)ZZZ\.(?:json|toml|ya?ml)):(\d+)")` —
and, as a second, independent blindness channel, `REA_GATE` reduced to a
never-matching pattern.

## 1. Real-target matrix — EX-16 landed `82fb807e…`, live repo root, read-only

Receipts: `receipts/real-target/` (`REAL-TARGET-MATRIX.txt` + one `.out` per run).

| instrument | injection | loci P/S/K | G2 line | declared classes | verdict | exit |
|---|---|---|---|---|---|---|
| landed | none | 6/9/2 | `ok (current-ok loci=5, total loci=17, floor=1)` | `[]` | PASS | 0 |
| **landed** | **needles neutered** | **0/0/0** | **`SUSPECT (current-ok loci=0, total loci=0, floor=1)`** | **`['BLIND-INSTRUMENT']`** | **FAIL** | **1** |
| landed-nog2 (mutant) | none | 6/9/2 | `ok (5, 17, floor=1)` | `[]` | PASS | 0 |
| **landed-nog2 (mutant)** | **needles neutered** | **0/0/0** | **`ok (current-ok loci=0, total loci=0, floor=1)`** | **`[]`** | **PASS** | **0** |
| landed | `REA_GATE` neutered | 0/0/0 | `SUSPECT (0, 0, floor=1)` | `['BLIND-INSTRUMENT']` | FAIL | 1 |
| landed-nog2 (mutant) | `REA_GATE` neutered | 0/0/0 | `ok (0, 0, floor=1)` | `[]` | PASS | 0 |

The **entire observable delta** between kill and survival is three output lines
(`diff receipts/real-target/landed82fb807e-neut.out
receipts/real-target/landed82fb807e-nog2-neut.out`: the G2 line, the
`DECLARED FAIL CLASSES` line, the `VERDICT` line). `--json` carries the same
signal: `g2_ok: false` + `declared_fail_classes: ["BLIND-INSTRUMENT"]` +
`verdict FAIL`/exit 1 versus `g2_ok: true` + `[]` + `PASS`/exit 0 at identical
zero counts (`receipts/real-target/*-json.out`). Every key run re-run
byte-identical (`*.rerun.out`).

## 2. Pre-landing matrix — the patch text as applied to `6f1d19ff…`

Run before EX-16 landed, using the CR-5 strict form (`instruments/instr-h3.py`).

| instrument | injection | G2 line | verdict | exit |
|---|---|---|---|---|
| head (pre-patch) | none | `ok` | PASS | 0 |
| **head (pre-patch)** | **needles neutered** | **`ok`** | **PASS** | **0** |
| h3 (floor applied) | none | `ok (loci=5, total=17)` | PASS | 0 |
| **h3 (floor applied)** | **needles neutered** | **`SUSPECT (loci=0, total=0)`** | **FAIL** | **1** |
| h3-nog2 (mutant) | none | `ok (5, 17)` | PASS | 0 |
| **h3-nog2 (mutant)** | **needles neutered** | **`ok (0, 0)`** | **PASS** | **0** |
| h3 | `REA_GATE` neutered | `SUSPECT (0, 0)` | FAIL | 1 |
| h3-nog2 | `REA_GATE` neutered | `ok (0, 0)` | PASS | 0 |

Receipts `receipts/instr-head*.out`, `instr-h3*.out`, `instr-h3-nog2*.out`,
`MATRIX.txt`. `instr-h3.out` and `instr-h3-nog2.out` are byte-identical
(`5fd9520a…`): on ordinary runs the mutation is invisible.

## 3. Controls and attribution

- **Attribution to the floor, not to the diagnostic print.** `instr-h3-noprint-neut.py`
  = floor intact, diagnostic print reverted to the plain form, needles neutered
  → `G2 … SUSPECT`, FAIL exit 1 (`receipts/instr-h3-noprint-neut.out`). The kill
  is the boolean, not the message.
- **Harm none.** Mutant and patch read byte-identical at the live root
  (`a9cd6886…` both, real target) and on the narrow-gate probe. The floor bites
  only on total blindness.
- **Sole detector.** In the neutered run the counters stay 0 and
  `SCOPE-ERRORS`, `G11`, `G7` stay empty — no other assertion separates blind
  from clean. The floor is the *only* thing that catches this class, which is
  why its removal is invisible except under injection.
- **Separable from H1.** On an empty root both `instr-h3` and `instr-h3-nog2`
  FAIL exit 1 on `SCOPE-ERRORS` (`…marker uncheckable…`); reverting H3 neither
  masks nor resurrects the absent-file class
  (`receipts/instr-h3-emptyroot-quiet.out`, `…‑nog2-emptyroot-quiet.out`).

## 4. Residuals, named (bounds of the H3 guarantee)

1. **Total blindness only — partial narrowing passes.** Narrowing `REA_GATE`
   to `rea-agents` alone drops the locus surface 17 → 8 (P 6→4, S 9→2, K 2→2)
   and PASSes on both the floor and the mutant (`instr-h3-narrowgate.out`,
   `…‑nog2‑narrowgate.out`, identical digests `4c1efd19…`). PIN alone neutered:
   loci unchanged, PASS both sides (`…‑pinonly.out`). The guarantee is "cannot
   be silent", not "locus count cannot regress" — this matches EX-16's own
   header note (per-needle partial blindness → H4/self-certification, external
   locus-count + scope-diff audit).
2. **The label is coupled to the floor.** Reverting the line also empties
   `DECLARED FAIL CLASSES` (it is derived from `g2_ok`), so the mutant's blind
   run carries no declared class at all — a second, independent reason the
   revert is detectable from the receipt alone.
3. **Zero-locus-but-legit scope FAILs by design** (fail-closed, per the C2
   claim: "FAILs when its positive-floor assertion finds zero loci in a
   non-empty scope"). No observed run is in that state: historical floors were
   current-ok 3/5 (round-1 receipts survey), 5 at HEAD here.

## 5. Reproduce

```bash
cd /var/tmp/rv4-mutation
python3 <claims>/c2/RV-4/harness/build.py          # pre-landing construction -> work/instr-*.py
<claims>/c2/RV-4/harness/run.sh                    # pre-landing matrix -> receipts/
python3 <claims>/c2/RV-4/harness/run-landed.py landed82fb807e   # rebuild from LIVE census + real-target matrix
```
(`harness/run-landed.py` re-reads `.ufo/gates/c1-census-v10.py`, re-applies the
one-line revert, stamps every receipt with the sha it ran, and re-prints the
matrix — re-runnable against any later revision of the instrument.)

## 6. Status

Real target confirmed at landed `82fb807e…` (H3 floor killed the mutant). If
EX-16 revises again, `harness/run-landed.py <tag>` reproduces the test against
the new bytes in one command; a floor expressed differently (e.g. a total-loci
conjunct rather than `n_current_ok > 0`) would need the revert string retargeted
— the assertion at the top of that script fails loudly rather than testing the
wrong line.
