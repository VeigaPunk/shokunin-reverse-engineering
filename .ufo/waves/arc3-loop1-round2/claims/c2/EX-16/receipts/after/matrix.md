# EX-16 battery matrix — v10 before (sha256 6f1d19ff…) vs landed r9 (d0772ce8…)

Source: receipts/before/SUMMARY-before.txt + receipts/after/SUMMARY-after.txt.
Each case = a fresh copy of the three scoped files at HEAD, one single-file mutation
(or an instrument copy for the h3/w cases), run as `python3 <instrument> --root <case>`.
Class column = DECLARED FAIL CLASSES from the report line.

| case | before exit | before class | after exit | after class | delta |
|---|---:|---|---:|---|---|
| t0-baseline | 0 | - | 0 | - | unchanged |
| t1-false-current-pin | 1 | - | 1 | - | unchanged |
| t2-undeclared-append | 1 | - | 1 | - | unchanged |
| t3-marker-strip | 1 | - | 1 | - | unchanged |
| t4-anchor-fail | 2 | - | 2 | - | unchanged |
| t5-dated-shelter | 0 | - | 0 | - | unchanged |
| t6-ptr-out-of-range | 1 | - | 1 | - | unchanged |
| h1-skill-absent | 0 | - | 1 | UNREADABLE | **silent PASS closed** |
| h1-province-absent | 1 | - | 1 | UNREADABLE | class added |
| h1-scorecard-absent | 1 | - | 1 | UNREADABLE | class added |
| h1-skill-zero-byte | 0 | - | 1 | UNREADABLE | **silent PASS closed** |
| h1-skill-truncated | 0 | - | 1 | UNREADABLE | **silent PASS closed** |
| h1-skill-isdir | 0 | - | 1 | UNREADABLE | **silent PASS closed** |
| h1-skill-eacces | 0 | - | 1 | UNREADABLE | **silent PASS closed** |
| h3-nullskill | 0 | - | 1 | BLIND-INSTRUMENT | **silent PASS closed** |
| h5-skill-padded | 0 | - | 1 | BLIND-INSTRUMENT | **silent PASS closed** |
| q0-quiet-baseline | 0 | - | 0 | - | unchanged |
| h3-blind-all | 0 | - | 1 | BLIND-INSTRUMENT | **silent PASS closed** |
| h3-blind-pin | 0 | - | 0 | - | unchanged |
| h3-blind-gate | 0 | - | 1 | BLIND-INSTRUMENT | **silent PASS closed** |
| w1-scope-widen-tail | 0 | - | 0 | - | unchanged |
| w2-scope-widen-overshoot | 0 | - | 1 | UNREADABLE | **silent PASS closed** |

Silent-PASS cases closed by this landing (10): h1-skill-absent, h1-skill-zero-byte, h1-skill-truncated, h1-skill-isdir, h1-skill-eacces, h3-nullskill, h5-skill-padded, h3-blind-all, h3-blind-gate, w2-scope-widen-overshoot.

Named residuals, still PASS on both sides (3): t5-dated-shelter, h3-blind-pin, w1-scope-widen-tail.

H4 certificate: scope-diff.py (CR-5's tool, sha256 e0d2384c…) before→after gives
`rows before=20 after=20, ADDED 0, REMOVED 0, CHANGED 0, CREEP FLAGS: []`, exit 0
(after/scope-diff.txt). The same tool flags the w1 instrument (DATED end widened to
1419) with `CREEP wide added DATED row` + `CREEP widen-by-add/remove` — i.e. the
instrument cannot see its own widening but the external audit can (after/h4-scope-diff-widened.txt).
