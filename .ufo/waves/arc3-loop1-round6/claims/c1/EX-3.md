# EX-3 — c1 (census instrument): independent verification of PL-4's r10 G21 frontier register

Seat EX-3, chain c1, wave arc3-loop1-round6, 2026-10-19. Repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`c625d5de57e045188b5ce8cd450a57b349f90785` (work `58c3db7` below it).
Scratch `/var/tmp/ex3-arc3r6/` (never `/tmp`). Every number below was produced
this session; peer artifacts are used only for convergence comparison, never as
evidence (rule #14). The repo gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus
and custody paths were **not modified** — git used read-only.

## 0. Verdict

PL-4's patch `claims/c1/PL-4/patch-v10-to-r10.diff` **applies cleanly, reproduces
the declared identity byte-exact, and satisfies all three frozen C1
requirements** on my own scratch trees:

| Requirement | Verdict | First-hand measurement |
|---|---|---|
| (a) clean tree still PASS | **VERIFIED** | patched gate on a byte-identical scratch tree and on the real repo root → exit 0, `VERDICT: PASS`; text output differs from v10 by exactly one added line |
| (b) seeded stale literal FAILs with a named disposition | **VERIFIED** | literal back into `:91-93` with both version anchors kept → exit 1, `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)` |
| (c) every SCOPE row and counter intact | **VERIFIED** | `SCOPE` 20 rows identical by AST; 17 shared `--json` keys, **zero** value mismatches; `counts` and `current_ok_per_file` identical |

Patch identity: applies to the pristine gate (sha `d0772ce8…`, 610 lines) and
reproduces sha **`8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`**
at **713 lines**, byte-identical to `PL-4/c1-census-v10-r10.py`.

Two things a landing receipt must record, neither of which breaks the frozen
claim:

1. **CORRECTED** — PL-4 §6 residual 1 says insertions inside `:132-162` shift
   register spans and fail REQUIRED. My 90-point insertion sweep shows the
   opposite: **44/44 insertion points at 119-162 PASS**. The register adds no
   insertion detection at all beyond the pre-existing G15 marker, which only
   covers insertions above :119.
2. **MEASURED LIMITATION** — two other recorded pre-r5 stale clauses
   (`compare-application-versions still probe-refused since r2` and the
   `REA_GHIDRA_STARTUP_TIMEOUT_MS` remediation) can be reintroduced into the
   post-unlock bullets with their anchors kept and the run still PASSes. Only
   the EVM `untested` literal is declared FORBIDDEN. This is consistent with
   PL-4 residual #3's "earned, not exhaustive" framing, but the receipt should
   name the unguarded literals explicitly.

Also non-blocking: in mixed-fault runs the declared-class list names only
`FRONTIER-STALE`, dropping `FRONTIER-UNEVALUABLE` even when REQUIRED errors are
present (all errors remain in `frontier_errors` and in the text report). An
optional 3-line refinement is measured on scratch in §6.

**Recommendation: land PL-4's patch as-is** (sha above), with the corrected
residual wording in the landing receipt. Do not re-cut the patch for the
reporting nit unless the lane wants the class list exhaustive.

## 1. First-hand re-derivations of the frozen "before" facts

| # | Frozen-claim fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`; `git log --oneline -3` line 1 = `c625d5d … (measured at work commit 58c3db7)` | REPRODUCED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`; `wc -l` → **610** | REPRODUCED |
| 3 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131 | parsed `SCOPE` with `ast.literal_eval`: 20 rows total; the 7 PROVINCE rows are exactly those, table at gate `:216-222`; max PROVINCE end = **131** | REPRODUCED |
| 4 | Frontier region = 73-93 + 133-162 | `grep -n`: `73:## Frontier`, `95:## Adjacent`, `133:### Round-4 frontier (post-unlock)`; `wc -l PROVINCE.md` → **162**; bullets at 75-80 (intro), 82-83, 84-86, 87-88, 89-90, 91-93, 135-138, 139-144, 145-146, 147-148, 149-150, 151-156, 157-160, 161-162 | REPRODUCED |
| 5 | No SCOPE row covers either region | programmatic overlap query → `rows reaching 73-93: []`, `rows reaching 133-162: []` | REPRODUCED |
| 6 | v10 reads PASS identically whether or not the bullets are stale | v10 `--root` on my ten trees (clean + nine seeds): **exit 0, PASS on every staleness seed** — stale literal, stripped anchors, truncation, insertion, recorded stale clauses all blind | REPRODUCED |
| 7 | v10 baseline PASS at HEAD | repo-root `python3 .ufo/gates/c1-census-v10.py --quiet` → exit 0; `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696 loci=9`, `SKILL.md lines=390 loci=2`; floor `17/14/3`; `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` | REPRODUCED |
| 8 | Historical claim "R4/R5 repairs were clause-audited by hand, not instrument-graded" | operative half reproduced (region is not gradable at HEAD); the historical audit process is not re-derivable from the tree | operative REPRODUCED / process UNVERIFIABLE |

Mechanism of the blindness, re-read at the pristine gate: `classify()` is
`gate:403`, and a unit with no PIN/VER/PTR occurrence hits `if not occ: continue`
at `gate:419` before `scope_of()` (`gate:324`) is ever consulted. The Frontier
bullets carry none of those loci, so no SCOPE row — even a CURRENT one over
73-93 — could have graded them. That justifies PL-4's register option over an
option-(a) SCOPE declaration.

Baseline command A was also re-derived for the wave's before-state (read-only,
`SCORECARD.md:88-124` recipe): at both `58c3db7` and `c625d5d`,
`knowledge_files=84, mapped=84, missing=[], dangling=[], rule_blocks=14,
citation_resolved_rules=14` (`EX-3/commandA.txt`). C1 does not move these; the
numbers are recorded for the c2/c3 integrators.

## 2. Patch application and identity

```
$ cp .ufo/gates/c1-census-v10.py /var/tmp/ex3-arc3r6/gate/pristine.py   # 610 L, d0772ce8…
$ cp .ufo/gates/c1-census-v10.py /var/tmp/ex3-arc3r6/gate/patched.py
$ patch /var/tmp/ex3-arc3r6/gate/patched.py \
    < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
patching file /var/tmp/ex3-arc3r6/gate/patched.py
$ sha256sum /var/tmp/ex3-arc3r6/gate/patched.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
$ wc -l /var/tmp/ex3-arc3r6/gate/patched.py
713
```

The patch file itself is 182 lines, sha
`3f94355cfe747c10c968c2382004ab1e95792518eba2f03ae99df2f7f16a6513`; the
delivered build `PL-4/c1-census-v10-r10.py` has the same sha
`80027570…` and 713 lines. Full receipt: `EX-3/apply-receipt.txt`.

Requirement (a), clean tree, scratch and real root:

```
$ python3 gate/pristine.py --root trees/clean --quiet   # exit 0 PASS
$ python3 gate/patched.py  --root trees/clean --quiet   # exit 0 PASS
$ diff <(grep -v '^FRONTIER register' r10-repo-root.txt) v10-repo-root.txt
# no output: every existing line byte-identical
$ grep 'FRONTIER register' r10-repo-root.txt
FRONTIER register (G21): 14 rows asserted, errors: []
```

The `VERDICT:` line, the per-file counters, the G2 floor, G7 and G11 lines are
unchanged. The new line is additive (`patched gate :698`).

## 3. Requirement (b) — independent seed matrix

Ten trees under `/var/tmp/ex3-arc3r6/trees/`, each started as a byte-copy of
the repo's three scoped files (PROVINCE.md sha `11a5c604…`, SCORECARD.md
`0d10e18f…`, SKILL.md `8e56f3d9…`). Seeds are my own, content-asserted against
the HEAD text (`EX-3/seeder.py`), not PL-4's `seed.py`.

| tree | my seed | v10 | r10 | r10 declared classes | frontier errors |
|---|---|---|---|---|---|
| clean | none | 0 PASS | 0 PASS | `[]` | 0 |
| seed-frozen-example | `:91-93` → "real solc/vyper-compiled bytecode untested" (anchors dropped) | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` | 3 |
| seed-forbidden-only | keep `solc-0.8.37`/`vyper-0.4.3`, append "Real … bytecode untested." | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` | 1 |
| seed-required-other | `:147-148` strip `unblob` (a bullet PL-4 did not seed) | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` | 1 |
| truncated-161 | delete last line → 161 lines | 0 PASS | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` | 14 |
| seed-insert-inside | insert one bullet after `:138` | 0 PASS | 0 PASS | `[]` | 0 |
| seed-append-past-162 | append a stale bullet after `:162` | 0 PASS | 0 PASS | `[]` | 0 |
| seed-rewrite-anchored | reverse the `.jsc` frontier claim, keep `.jsc`/`Ignition` | 0 PASS | 0 PASS | `[]` | 0 |
| seed-stale-159 | recorded pre-r5 clause back into `:157-160`, anchors kept | 0 PASS | 0 PASS | `[]` | 0 |
| seed-ghidra-139 | recorded pre-r5 remediation back into `:139-144`, anchors kept | 0 PASS | 0 PASS | `[]` | 0 |

Exact r10 error lines (`EX-3/transcripts/`):

```
seed-frozen-example:
  PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
  PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
  PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
seed-forbidden-only:
  PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)   [exactly one]
seed-required-other:
  PROVINCE.md:147-148 REQUIRED 'unblob' absent (G21 frontier register)
truncated-161:
  UNREADABLE (could-not-evaluate): ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
  + 14 x "PROVINCE.md:<s>-<e> frontier uncheckable (file unreadable)"
clean:
  FRONTIER register (G21): 14 rows asserted, errors: []
```

The isolated `seed-forbidden-only` arm is the one requirement (b) needs: the
FORBIDDEN pattern alone catches a reintroduced stale claim even when both
earning anchors survive. The two recorded-literal arms are discussed in §5.

## 4. Requirement (c) — counter integrity

`--json` on the clean tree, pristine vs patched (`EX-3/counter-integrity.txt`):

```
shared keys: 17  mismatched: []
r10-only keys: ['frontier_errors', 'frontier_rows']
v10-only keys: []
counts equal: True
counts: {"PROVINCE.md": {"lines": 162, "loci": 6},
         "SCORECARD.md": {"lines": 1696, "loci": 9},
         "SKILL.md": {"lines": 390, "loci": 2}}
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
SCOPE AST equality: rows 20 / 20, equal: True
```

The patch has eight hunks; none edits a SCOPE row literal (the FRONTIER block
is inserted after the SCOPE table). AST equality is the definitive check: all
20 rows, same tuple values, same order.

Existing-behavior regression: planting an instrument-visible pin
(`rea-agents@6.5.0`) in a Frontier line (`:89-90`) still reads
`FAIL undeclared=1` exit 1 under **both** instruments. The patch adds a class
without removing one.

G19 (`max_end`) now unions SCOPE ends with register ends (`patched :611`), so
PROVINCE's declared max moves 131 → 162 and a 161-line tree is `UNREADABLE`.
That is a strictness increase, measured by `truncated-161`; it also explains
why every one-line deletion in my deletion sweep fails (90/90, all as
`UNREADABLE`), independent of bullet semantics.

## 5. CORRECTED — the insertion residual is too strong

PL-4 §6 residual 1 (`PL-4.md:330-333`) says: "Insertions anywhere inside
`:73-162` are caught: above `:119` they shift the DATED marker row (G15
SCOPE-ERROR, existing machinery …), inside `:132-162` they shift register spans
(REQUIRED-absent — measured via the seeded arms)."

I swept one neutral bullet line inserted after every line 73..162, 90 runs
(`EX-3/insertion-sweep.json`):

```
INSERTION: caught 46 of 90
  caught with frontier errors (73-89):        17
  caught by the existing G15 marker only (90-118): 29
  PASSED at 119-162:                          44 of 44
```

Every insertion at or after the DATED marker (line 119) passes, including the
entire claimed `:132-162` region. The mechanism: register windows are
line-keyed bullet spans, and a ±1-line shift leaves each row's short REQUIRED
anchors inside its (shifted) window. For insertion after `:138`, the row
`139-144` window starts on the new bullet and still contains `90 MB PE` /
`arc2-r7`; row `145-146` shifts onto the previous bullet's tail and still
contains `.jsc` / `Ignition`; and so on for all 14 rows. The register is a
span-assertion table, not a line-identity table.

Consequence for the landing receipt: state the measured envelope — a one-line
insertion at ≥119 (and any append past `:162`, which PL-4 correctly names)
is invisible unless it displaces a declared anchor or drops the file below 162
lines. This does **not** violate C1: the frozen falsifier is the reintroduction
of a declared-stale literal, and that is caught (§3). It corrects the delivered
prose, not the delivered behavior.

The header lines `## Frontier` (:73) and `### Round-4 frontier` (:133) are also
outside every row; renaming or shifting them is not asserted by the register
(an insertion before :133 sits at ≥:119, so the DATED marker stays in place and
G15 does not fire either — measured, insertion after :132 passes).

## 6. Non-blocking note — mixed-fault declared classes

`seed-frozen-example` produces three frontier errors (two REQUIRED-absent +
one FORBIDDEN) but `declared_fail_classes` is `['FRONTIER-STALE']`: the
patched `:664-665` ternary picks the FORBIDDEN branch and drops UNEVALUABLE.
All three errors remain visible in `frontier_errors` and the text report, so
the disposition is not lost and requirement (b) is unaffected.

A 3-line scratch refinement (`EX-3/refined-class-variant.diff`) makes the list
additive:

```python
_fstale = ["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors) else []
_fun = ["FRONTIER-UNEVALUABLE"] if any(("REQUIRED" in e) or ("uncheckable" in e)
                                      for e in frontier_errors) else []
frontier_class = _fstale + _fun
```

Measured on scratch: clean-tree text byte-identical to the patched gate; mixed
arm now reports `['FRONTIER-STALE','FRONTIER-UNEVALUABLE']`; isolated arms
unchanged (`['FRONTIER-STALE']`, `['FRONTIER-UNEVALUABLE']`, truncation
`['UNREADABLE','FRONTIER-UNEVALUABLE']`). Refined scratch sha `2de9cf80…`.
Not required by C1; offered only if the lane wants exhaustive class reporting.

## 7. Measured limits (not claim violations)

1. **Recorded stale clauses outside the EVM row are unguarded.**
   `git show 40de383 -- PROVINCE.md` records three before-states that the r4
   work replaced: `real solc/vyper-compiled bytecode untested`,
   `compare-application-versions still probe-refused since r2`, and
   `Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS`. Only the first is a FORBIDDEN
   pattern. Reintroducing either of the other two with anchors kept reads
   PASS (trees `seed-stale-159`, `seed-ghidra-139`). This is consistent with
   PL-4 residual #3 ("earned, not exhaustive"), but the receipt should list
   which recorded literals are unguarded.
2. **Anchor-preserving rewrites pass.** Reversing the `.jsc` bullet's frontier
   claim while keeping `.jsc` and `Ignition` reads PASS
   (`seed-rewrite-anchored`). A positive-floor + earned-forbidden register
   cannot detect novel falsehoods; that remains the round audit's job.
3. **Past-the-bound appends pass.** Confirmed (`seed-append-past-162`), exactly
   as PL-4 residual 1's first sentence names.
4. **Forbidden matching is literal-based.** `untested` is matched
   case-insensitively anywhere in `:91-93`; a future legitimate sentence such
   as "the earlier `untested` claim is retracted" would false-FAIL and require
   a re-key. Re-key discipline is already declared in the provenance block.

## 8. Per-item verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | HEAD `c625d5d` / work `58c3db7` | REPRODUCED |
| 2 | Gate sha `d0772ce8…`, 610 lines | REPRODUCED |
| 3 | SCOPE exactly seven PROVINCE rows; max end 131; no Frontier coverage | REPRODUCED |
| 4 | Frontier boundaries 73-93 / 133-162; EOF 162; 13 bullets | REPRODUCED |
| 5 | v10 blind to all nine seeded trees | REPRODUCED |
| 6 | v10 baseline PASS, counters 162/6, 1696/9, 390/2, floor 17/14/3 | REPRODUCED |
| 7 | Patch applies clean; sha `80027570…`; 713 lines; equals delivered build | REPRODUCED |
| 8 | (a) clean tree PASS, text identical modulo one added line | VERIFIED |
| 9 | (b) declared stale literal FAILs with `FRONTIER-STALE` (isolated arm) | VERIFIED |
| 10 | (b) FORBIDDEN + REQUIRED mixed arm FAILs (3 errors) | VERIFIED |
| 11 | (b) REQUIRED-strip on an independently chosen bullet FAILs | VERIFIED |
| 12 | (b) 161-line truncation FAILs as `UNREADABLE` + 14 uncheckable | VERIFIED |
| 13 | (c) SCOPE 20 rows identical (AST) | VERIFIED |
| 14 | (c) 17 shared JSON keys, zero mismatches; counts/floor equal | VERIFIED |
| 15 | (c) existing UNDECLARED locus behavior unchanged | VERIFIED |
| 16 | G19 max end 131 → 162 (strictness increase) | REPRODUCED |
| 17 | PL-4 §3 six-tree matrix outcomes | REPRODUCED on my own trees |
| 18 | PL-4 §6 "insertions inside :132-162 caught" | **CORRECTED** — 44/44 at 119-162 PASS |
| 19 | PL-4 residual "past-:162 append unregistered" | REPRODUCED |
| 20 | PL-4 residual #3 "forbidden coverage earned, not exhaustive" | REPRODUCED; two recorded literals measured unguarded |
| 21 | Mixed-fault declared class list | NON-BLOCKING NOTE; optional refinement measured |
| 22 | Historical "clause-audited by hand" process | UNVERIFIABLE (not re-derivable) |

## 9. Peer convergence (context only — not used as evidence)

- `claims/c1/PL-2.md` independently reaches the same insertion correction
  (it probed :133/:134/:150); my 90-point sweep generalizes it: **all** 119-162
  insertion points pass, and the 73-118 catches come from the existing G15
  marker plus 17 register hits.
- `claims/c1/RV-3.md` independently found the recorded-literal gap
  (`stale159`); I re-derived both recorded-literal probes first-hand in §7.
- `claims/verdicts/VZ-4.md` audits a **different** c1 design — a 13-row
  `FRONTIER_REGISTER` with sha `8e420679…`, which RV-3 preserves as a
  superseded prior attempt. VZ-4's C1 ruling therefore does **not** certify
  PL-4's sha `80027570…`; the two should not be conflated in the convergence
  record.

## 10. Landing recipe

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py \
  < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet
# exit 0, VERDICT: PASS,
# FRONTIER register (G21): 14 rows asserted, errors: []
```

Record post-edit identity in the landing receipt, not inline in the gate (the
gate's own rule-#14 discipline). In the same receipt, record the corrected
residual envelope from §5 and the unguarded recorded literals from §7.

## 11. What I did not do

- Did not modify `.ufo/gates/c1-census-v10.py` (custody sha re-checked after
  all work: still `d0772ce8…`), nor PROVINCE.md, SKILL.md, SCORECARD.md,
  corpus, gates, or any tracked file. Writes are confined to
  `claims/c1/EX-3.md` and `claims/c1/EX-3/`.
- Did not write the gate patch itself; the optional class refinement exists
  only as a scratch diff under `EX-3/`.
- Did not re-derive c2/c3 after-states (EX-7's corpus entry, SC-3's rule #15) —
  outside the c1 chain; only their before-state via command A is recorded.
- Did not re-run the historical by-hand audit; it is not derivable from the
  tree.

## 12. Evidence index

- `EX-3/apply-receipt.txt` — pristine/patch/patched/built shas and line counts.
- `EX-3/counter-integrity.txt` — 17-key JSON compare + SCOPE AST equality.
- `EX-3/insertion-sweep.json`, `EX-3/deletion-sweep.json` — 90 + 90 runs.
- `EX-3/commandA.txt` — command A at both commits.
- `EX-3/40de383-before-states.txt` — the three recorded pre-r5 literals.
- `EX-3/refined-class-variant.diff` — optional scratch-only class refinement.
- `EX-3/seeder.py` — all ten seed mutations, content-asserted.
- `EX-3/transcripts/<tree>.txt` — v10 and r10 raw output per tree (10 trees).
- `EX-3/json-*.json` — clean and seeded `--json` captures.
