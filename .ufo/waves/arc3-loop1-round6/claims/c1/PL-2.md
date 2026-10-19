# PL-2 — c1 (census instrument): independent verification of PL-4's r10 frontier register

Seat PL-2, chain c1, wave arc3-loop1-round6. Measured 2026-10-19 on this host.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`c625d5de57e045188b5ce8cd450a57b349f90785` (work `58c3db7` below it in
`git log --oneline`). Scratch `/var/tmp/pl2-arc3r6-verify` (never `/tmp`).
Every number below is first-hand this session (rule #14); transcripts are in
`claims/c1/PL-2/verify/`. The live gate, PROVINCE.md, SKILL.md, SCORECARD.md,
corpus and custody paths were **not** modified — git used read-only
(`rev-parse`, `log`, `show`, `status`).

## 0. Deliverable and verdict

PL-4's patch (`claims/c1/PL-4/patch-v10-to-r10.diff`) is **independently
VERIFIED** against all three frozen-claim requirements:

| Requirement | Verdict | First-hand measurement |
|---|---|---|
| (a) clean tree still PASS | **PASS** | patch applies to a pristine gate and the resulting instrument reads `VERDICT: PASS`, exit 0, on the real repo root and on a byte-identical clean scratch tree |
| (b) seeded stale literal FAILs with a named disposition | **PASS** | retracted literal back into `PROVINCE.md:91-93` → exit 1, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`, error names `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested'` |
| (c) existing SCOPE rows and counters intact | **PASS** | `SCOPE` lists are equal (20 rows); 17 shared `--json` keys, **zero** value mismatches; `counts` and `current_ok_per_file` identical |

One **CORRECTION** to the delivered artifact's residual #1: not every insertion
inside `PROVINCE.md:132-162` is caught. I measured three insertion positions
(`:133`, `:134`, `:150`) and a header rename that all still read PASS, because
register spans absorb ±1-line shifts. The core claim is unaffected (§5).

I also found an **earlier PL-2 attempt's competing design** already in this
seat directory (not among the three artifacts the parent named as delivered).
It is preserved under `claims/c1/PL-2/prior-attempt/` (provenance there) and re-tested
first-hand in §6. Recommendation: **land PL-4**, optionally with the two-row
header hardening I tested on scratch in §7; do not substitute the prior design.

## 1. First-hand re-derivations of the frozen claim's "before" facts

| # | Frozen-claim fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`; `git log --oneline -3` line 1 = `c625d5d arc3-loop1-round5: records … (measured at work commit 58c3db7)` | REPRODUCED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`; `wc -l` → **610** | REPRODUCED |
| 3 | SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | loaded the gate with `importlib`; `SCOPE` has 20 rows total, the 7 `PROVINCE.md` rows are exactly `(8,13,CURRENT) (15,26,CURRENT) (40,43,DATED) (44,44,CURRENT) (45,62,DATED) (64,71,CURRENT) (119,131,DATED)`; `max` PROVINCE end = **131** | REPRODUCED |
| 4 | Frontier region = 73-93 + 133-162 | `grep -n '^## Frontier$\|^## Adjacent$\|^### Round-4 frontier (post-unlock)$' PROVINCE.md` → `73:## Frontier`, `95:## Adjacent`, `133:### Round-4 frontier (post-unlock)`; `wc -l PROVINCE.md` → **162** (EOF at :162) | REPRODUCED |
| 5 | The two regions are UNDECLARED | programmatic coverage query: `covering (73,93) = []`, `covering (133,162) = []` | REPRODUCED |
| 6 | v10 reads PASS identically whether or not the bullets are stale | v10 `--root` on my five seeded trees: **all exit 0, `VERDICT: PASS`** (`verify/matrix.txt`, `verify/transcripts/*.v10.txt`) | REPRODUCED |
| 7 | v10 baseline PASS at HEAD | repo-root `python3 .ufo/gates/c1-census-v10.py --quiet` → exit 0; `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696 loci=9`, `SKILL.md lines=390 loci=2`; `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` (`verify/baseline-v10-repo.txt`) | REPRODUCED |
| 8 | The HISTORICAL claim that R4/R5 repairs were "clause-audited by hand" | not re-derivable from artifacts; the operative half (the region is not instrument-gradable at HEAD) is items 5+6 | **UNVERIFIABLE** (historical process) / operative half REPRODUCED |
| 9 | The stale literal is grounded history, not invented | `git show 40de383 -- PROVINCE.md` (read-only) contains the exact before-line `-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay` / `-  bare hashes (no signature DB → no name resolution).` and the repaired after-lines naming `solc-0.8.37` / `vyper-0.4.3` (`verify/40de383-PROVINCE.diff`) | REPRODUCED |

Mechanism of the blindness, re-read at the pristine gate (`classify()`, gate
`:403-421`): a unit with no PIN/VER/PTR occurrence hits `if not occ: continue`
before `scope_of()` is ever consulted, and `units()` also requires `REA_GATE`
to fire. Frontier bullets carry neither, so no SCOPE row — even a `CURRENT`
one over 73-93 — could have graded them. That is why PL-4's register option
(direct text assertion, not a SCOPE declaration) is the correct shape.

## 2. Independent patch application

Commands and output, full transcript `verify/patch-apply.txt`:

```
$ cp .ufo/gates/c1-census-v10.py /var/tmp/pl2-arc3r6-verify/gate/pristine-for-patch.py
$ cd /var/tmp/pl2-arc3r6-verify/gate
$ patch --dry-run -p0 pristine-for-patch.py < .../claims/c1/PL-4/patch-v10-to-r10.diff
checking file pristine-for-patch.py            # clean
$ patch -p0 pristine-for-patch.py < .../patch-v10-to-r10.diff
patching file pristine-for-patch.py
$ sha256sum pristine-for-patch.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
$ wc -l pristine-for-patch.py
713
$ cmp -s pristine-for-patch.py .../claims/c1/PL-4/c1-census-v10-r10.py && echo BYTE-IDENTICAL
BYTE-IDENTICAL
```

The patch file itself is 182 lines, sha256
`3f94355cfe747c10c968c2382004ab1e95792518eba2f03ae99df2f7f16a6513`.
The patched gate's sha and line count match PL-4's stated `80027570…` / 713
lines, and the byte comparison shows the delivered build and the mechanically
patched pristine copy are the same file.

Structural preservation, measured by `importlib` + `inspect` on pristine vs
patched:

```
SCOPE identical: True | rows: 20 20
scope_of source identical: True
classify source identical: True
assert_markers source identical: True
PIN/VER/PTR identical: True
FRONTIER rows: 14
```

`FRONTIER[]` covers every one of the 13 bullet lines in the two regions
(bullet starts: 82, 84, 87, 89, 91, 135, 139, 145, 147, 149, 151, 157, 161);
the 14th row, 75-80, covers the section intro. No frontier bullet is
uncovered. The register's spans are exactly:
`75-80, 82-83, 84-86, 87-88, 89-90, 91-93, 135-138, 139-144, 145-146,
147-148, 149-150, 151-156, 157-160, 161-162`.

## 3. Requirement arms — my own trees, my own seeds

Six trees under `/var/tmp/pl2-arc3r6-verify/`, each started as byte-identical
copies of the repo's `PROVINCE.md` (`11a5c60450cc736a5b5443fa559191dc35b246386927cbd854b5e9fef1f0bcf2`),
`SKILL.md` and `SCORECARD.md`; seeds are content-asserted edits in
`verify/seed2.py`. Full output: `verify/matrix.txt`.

| tree | seed | v10 exit/verdict | r10 exit/verdict | r10 declared classes |
|---|---|---|---|---|
| `clean` | none | 0 PASS | 0 PASS | `[]` |
| `seed-forbidden` | frozen example literal back into :91-93 | 0 PASS (blind) | **1 FAIL** | `['FRONTIER-STALE']` |
| `seed-forbidden-only` | keeps `solc-0.8.37`/`vyper-0.4.3`, adds `untested` (isolates FORBIDDEN) | 0 PASS (blind) | **1 FAIL** | `['FRONTIER-STALE']` |
| `seed-required-evm` | :91-93 earning citations stripped | 0 PASS (blind) | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| `seed-required-riscv` | :137 `r5-01` citation removed | 0 PASS (blind) | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| `trunc-161` | PROVINCE truncated to 161 lines | 0 PASS (blind) | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

Key r10 error lines (mine, `verify/transcripts/`):

```
seed-forbidden:
  PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
  PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
  PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
seed-forbidden-only:
  PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)   [exactly one error]
seed-required-evm:
  PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)    [x2, incl. vyper]
seed-required-riscv:
  PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
trunc-161:
  UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
  + 14 x 'frontier uncheckable (file unreadable)'
```

The isolated arm matters: `seed-forbidden-only` proves the FORBIDDEN pattern
alone catches a reintroduced stale claim, not merely the collateral loss of
the required tokens. Conversely `seed-required-evm`/`seed-required-riscv`
prove the REQUIRED floor catches a bullet rewritten to strip its earning
citations even when no forbidden literal is present. Clean tree: `FRONTIER
register (G21): 14 rows asserted, errors: []`.

## 4. Requirement (c) — counter integrity, measured

`--json` on the real repo root, v10 vs r10 (`verify/json-compare.txt`):

```
v10 repo verdict: PASS | r10 repo verdict: PASS
shared keys (17): [counts, current_ok, current_ok_per_file, declared_fail_classes,
  g11, g2_floor, g2_ok, g7, historical, live, scope_errors, stale, ambiguous,
  undeclared, unresolved, unreadable, verdict]
mismatched shared keys: []
r10-only keys: ['frontier_errors', 'frontier_rows']
counts equal: True
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}  (equal)
```

So all 17 pre-existing JSON keys keep their values; the run only gains the two
new keys `frontier_rows=14` and `frontier_errors=[]`. The text `VERDICT:` line
is byte-identical to v10's; the G21 line is an additional line. No SCOPE row is
touched (`SCOPE` equality above), and `classify()`, `scope_of()`,
`assert_markers()` sources are identical.

One observation, not a defect against the claim: when a seeded tree produces
both FORBIDDEN and REQUIRED errors (`seed-forbidden`), the declared-class list
is only `['FRONTIER-STALE']` (the FORBIDDEN branch wins in `frontier_class`,
patched gate `:664-665`). The REQUIRED errors remain visible in
`frontier_errors` and in the text report, so the disposition is not lost.

## 5. Edge probes — one CORRECTION to the delivered artifact's residual #1

PL-4 §6 residual 1 says insertions "inside `:132-162` … shift register spans
(REQUIRED-absent — measured via the seeded arms)" and therefore are caught.
My measurements (`verify/edge-probes.txt`) show that is too strong. Each edge
tree started from a byte-identical copy; edits are content-asserted.

| edge tree | edit | v10 | r10 | what caught it |
|---|---|---|---|---|
| `edge-header-rename` | `## Frontier` → `## Frontier (renamed)` at :73 | 0 PASS | **0 PASS** | nothing — header line is not in any FRONTIER row |
| `edge-insert-133` | one line inserted before the `### Round-4 frontier` header | 0 PASS | **0 PASS** | nothing — spans shifted, anchors still inside |
| `edge-insert-134` | one line inserted after that header | 0 PASS | **0 PASS** | nothing |
| `edge-insert-150` | one continuation line inserted inside the adb bullet | 0 PASS | **0 PASS** | nothing |
| `edge-insert-74` | one line inserted above the Frontier section | 1 FAIL | **1 FAIL** | `SCOPE-ERRORS: PROVINCE.md:119 marker 'verified 2026-10-13' absent` + required-absent at 84-86/89-90 |
| `edge-delete-line` | `r5-01` citation line deleted (161 lines) | 0 PASS | **1 FAIL** | G19 `UNREADABLE: 161 lines < declared max 162` + register uncheckable |
| `edge-empty-bullet` | macOS bullet emptied to header + blank | 0 PASS | **1 FAIL** | `PROVINCE.md:89-90 REQUIRED 'unsupported_host' absent` → `FRONTIER-UNEVALUABLE` |

Interpretation, in the claim's terms: requirement (b) is about **stale literals
inside declared bullets**, and those are caught (FORBIDDEN) as are stripped
earning anchors (REQUIRED) and truncation (G19). The register is a
span-assertion table, not a line-identity table, so a ±1-line insertion whose
anchors remain inside the shifted span is not a failure — by construction.
The correction is to the artifact's blanket residual sentence, not to the
delivered behavior. Two consequences a landing receipt should record:

1. The `## Frontier` and `### Round-4 frontier` header lines are not asserted;
   renaming either is invisible to r10. (Their spans' required anchors still
   keep the bullets honest.)
2. Insertions inside `:132-162` are invisible unless they displace a required
   anchor out of its span or change the file's line count below 162. The
   "any insertion is caught" wording should read "insertions that displace a
   declared anchor are caught; ±1-line insertions can be absorbed."

## 6. Competing design in this seat dir — re-tested, not quoted

At dispatch, the seat's artifact path `claims/c1/PL-2.md` and its evidence dir
`claims/c1/PL-2/` held an earlier attempt's full artifact (a 195-line patch, a
705-line proposed instrument, an `arms.txt`, a seed diff and two JSONs). It is
not one of the three artifacts named as delivered. The evidence files were
moved byte-unchanged to `claims/c1/PL-2/prior-attempt/`; its `.md` was
reconstructed there at 217 lines (matching the pre-dispatch read) after this
seat's artifact write reused the path. I tested the design myself
(`verify/prior-attempt-and-hardening.txt`) rather than quoting it.

Mechanics: its patch applies with `patch -p0`, reproduces sha256
`2d7ee95ba2743bde0b658c91d867a46e04e3e9e14de41d2cb60f2ff46238ce7b` at 705
lines, byte-identical to its `c1-census-v10-r10-proposed.py`. Its design adds
two `SCOPE` rows (`PROVINCE.md` 73-93 and 133-162, class `FRONTIER`) with
structural header markers, plus a 3-entry literal-only register
(`FRONTIER_STALE`), and widens `assert_markers` to `FRONTIER`.

What I measured on my trees:

| arm | prior design | PL-4 design |
|---|---|---|
| clean | PASS exit 0 | PASS exit 0 |
| exact r4 stale literal (`seed-forbidden`) | FAIL exit 1, `FRONTIER-STALE`, hit `PROVINCE.md:92` | FAIL exit 1, `FRONTIER-STALE` |
| paraphrase `…solc-0.8.37/vyper-0.4.3-compiled bytecode untested` (`seed-forbidden-only`) | **PASS exit 0 — missed** (literal register matches the exact r4 string only) | FAIL, FORBIDDEN alone |
| stripped earning citations (`seed-required-evm`, `seed-required-riscv`) | **PASS exit 0 — missed** (no REQUIRED floor) | FAIL, `FRONTIER-UNEVALUABLE` |
| truncated 161 lines | FAIL, class `['UNREADABLE']` | FAIL, `['UNREADABLE','FRONTIER-UNEVALUABLE']` |
| header rename | **FAIL** via `SCOPE-ERRORS: :73 marker '^## Frontier$' absent` | PASS (gap) |
| insertion at :133 | **FAIL** via `SCOPE-ERRORS: :133 marker … absent` | PASS (gap) |
| insertion at :150 | PASS | PASS |

Counter integrity of the prior design on the clean tree: 17 shared `--json`
keys, zero mismatches, counts equal; its extra keys are `frontier_register` and
`frontier_stale`. So both designs preserve existing counters; the prior one
additionally adds SCOPE rows (by design, not a violation of "keep every
existing row", but it does change SCOPE bounds) and its `VERDICT:` line gains a
`frontier=%d` suffix.

**Recommendation:** land PL-4's patch. It is the stronger fit to the frozen
claim: the REQUIRED floor catches stripped/reworded bullets (the prior design
does not), the FORBIDDEN regex catches both the exact r4 before-state and the
paraphrase, it satisfies requirement (c) with SCOPE untouched, and its
residual behavior is documented (with the §5 wording correction). The prior
design's one real advantage is structural header assertion; that is a two-row
addition, tested below.

## 7. Optional hardening (scratch only — NOT landed, NOT part of PL-4's patch)

Adding two rows to `FRONTIER[]`:

```python
("PROVINCE.md", 73, 73, [r"^## Frontier$"], []),
("PROVINCE.md", 133, 133, [r"^### Round-4 frontier \(post-unlock\)$"], []),
```

Measured on a scratch copy of the patched r10 (`verify/prior-attempt-and-hardening.txt`):

| tree | hardened r10 (16 rows) |
|---|---|
| clean | PASS exit 0, `errors: []` |
| header rename | **FAIL** exit 1, `PROVINCE.md:73-73 REQUIRED '^## Frontier$' absent` |
| insertion at :133 | **FAIL** exit 1, `PROVINCE.md:133-133 REQUIRED '^### Round-4 frontier …' absent` |
| insertion at :134 | PASS (header position unchanged) |
| `seed-forbidden` | FAIL, `FRONTIER-STALE` (unchanged) |
| `trunc-161` | FAIL, `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

This closes the header-rename/insert-before-header gap and keeps the clean tree
green. It changes only the new `frontier_rows` counter (14 → 16), not any
pre-existing key. It is offered as a 2-line follow-up if the lane wants it; the
claim does not require it.

## 8. Per-item verdicts

| Item | Verdict | Evidence |
|---|---|---|
| HEAD `c625d5d` / work `58c3db7` | **REPRODUCED** | §1 item 1 |
| Gate sha `d0772ce8…`, 610 lines | **REPRODUCED** | §1 item 2 |
| SCOPE exactly the seven PROVINCE rows, max end 131 | **REPRODUCED** | importlib dump, §1 item 3 |
| Frontier boundaries 73-93 / 133-162, EOF 162 | **REPRODUCED** | §1 item 4 |
| Both regions UNDECLARED; no covering row | **REPRODUCED** | §1 item 5 |
| v10 blind on stale/truncated frontier (5 seeded trees PASS) | **REPRODUCED** | §3, `verify/matrix.txt` |
| v10 baseline PASS at HEAD, counters 6/9/2 | **REPRODUCED** | §1 item 7 |
| PL-4 patch applies clean; sha `80027570…`, 713 lines, byte-identical | **REPRODUCED** | §2 |
| SCOPE/classify/scope_of/assert_markers unchanged; 20 SCOPE rows equal | **REPRODUCED** | §2 |
| Register covers all 13 frontier bullets | **REPRODUCED** | §2 coverage query |
| (a) clean tree PASS | **REPRODUCED** | §3, §4 |
| (b) seeded literal FAIL with `FRONTIER-STALE` | **REPRODUCED** | §3 |
| (b, stronger) paraphrase caught | **REPRODUCED** | `seed-forbidden-only` |
| (b, stronger) stripped anchors caught | **REPRODUCED** | `seed-required-evm/riscv` |
| (c) 17 shared JSON keys zero mismatch; counts/floor equal | **REPRODUCED** | §4 |
| PL-4 residual #1 "any insertion inside :132-162 caught" | **CORRECTED** | §5: insertions at 133/134/150 and header rename PASS |
| PL-4 residual "above :119 insertion shifts DATED marker" | **REPRODUCED** | `edge-insert-74`: G15 at :119 |
| Historical "clause-audited by hand" process claim | **UNVERIFIABLE** | not re-derivable from artifacts; operative half reproduced |
| Prior in-tree PL-2 design: clean/invariance/exact seed | **REPRODUCED** | §6, sha `2d7ee95b…`, 705 lines |
| Prior design catches paraphrase / stripped anchors | **DISCREPANCY (misses both)** | §6 |
| Prior design header protection | **REPRODUCED** | `SCOPE-ERRORS` at :73 and :133 |
| Two-row hardening (clean PASS; rename/insert-133 caught) | **REPRODUCED (scratch)** | §7 |

## 9. Residuals and what I did NOT do

- Did not edit `.ufo/gates/c1-census-v10.py` (sha still
  `d0772ce8…` after all work), nor PROVINCE.md, SKILL.md, SCORECARD.md, corpus,
  `.ufo/gates/` or any tracked file. Did not touch `PROVINCE.md` / `LOG.md` /
  `SCORECARD.md` even though the wave would normally record a landing.
- Did not test c2 (command A, corpus entry) or c3 (`rule_blocks`) — outside the
  c1 chain; their numbers in this artifact would be second-hand and are omitted.
- Did not re-derive the historical hand-audit process (UNVERIFIABLE above).
- The `FRONTIER[]` register only catches literals it declares; new frontier
  staleness remains with the round audit. Past-the-bound appends (a new bullet
  after :162) remain outside the register — PL-4 names this residual, and my
  `trunc-161` arm only covers short files, not appended ones.
- The optional §7 hardening was tested on scratch; it is not in PL-4's patch
  and not landed. If the parent wants it, apply it as a follow-up and re-run
  the clean arm + `seed-forbidden` + header-rename arm.

## 10. File inventory and landing recipe

Writes under this seat's dir only:

- `claims/c1/PL-2.md` — this artifact.
- `claims/c1/PL-2/verify/commands.txt` — exact command list.
- `claims/c1/PL-2/verify/matrix.txt` — six-tree, two-instrument raw output.
- `claims/c1/PL-2/verify/json-compare.txt` — v10 vs r10 key comparison.
- `claims/c1/PL-2/verify/edge-probes.txt` — edge-tree results.
- `claims/c1/PL-2/verify/prior-attempt-and-hardening.txt` — prior-design and
  §7-hardening runs.
- `claims/c1/PL-2/verify/baseline-v10-repo.txt`, `baseline-r10-repo.txt`,
  `patch-apply.txt`, `40de383-PROVINCE.diff`, `seed2.py`,
  `verify/transcripts/*` (per-tree v10/r10/prior/hardened logs),
  `verify/*.json`.
- `claims/c1/PL-2/prior-attempt/` — the earlier attempt's files (evidence
  byte-unchanged; `.md` reconstructed per `PROVENANCE.txt`), not quoted as
  evidence.

Landing recipe for the parent (re-verified by me from a pristine copy):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py \
  < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py    # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet
# expect exit 0, VERDICT: PASS, FRONTIER register (G21): 14 rows asserted, errors: []
```

Record the post-edit identity in the landing receipt, not inline in the gate
(the gate's own rule-#14 discipline, pristine gate `:89-93`). If the §7
hardening is accepted, add the two rows and change that expected count to 16.
