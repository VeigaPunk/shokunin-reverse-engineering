# EX-1 — c1 (census instrument): independent verification of PL-4's r10 frontier register, one measured residual correction, and a tested coverage delta

Seat EX-1, chain c1, wave arc3-loop1-round6, 2026-10-19. Repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; HEAD
`c625d5de57e045188b5ce8cd450a57b349f90785` (`c625d5d`), work commit `58c3db7`
(both re-derived this session via `git rev-parse HEAD` + `git log --oneline -2`).
Scratch `/var/tmp/ex1-arc3r6` (never `/tmp`). The gate
`.ufo/gates/c1-census-v10.py` was **not** modified: sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610 lines,
before and after every experiment (`git status --porcelain` on it is empty).
Git was read-only (`rev-parse`/`log`/`show`/`status`). Every number below is
first-hand this session (rule #14); I wrote my own seeder and did not import,
copy or quote PL-4's `seed.py` or any prior seat's measurements. Peer artifacts
in this chain (`PL-2.md`, `RV-3.md`) were read only after my measurements were
complete, for reconciliation; agreement is noted, never used as evidence.

## 0. Deliverable and verdict

PL-4's patch (`claims/c1/PL-4/patch-v10-to-r10.diff`) is **independently
VERIFIED** against the frozen C1 requirements (a), (b), (c). One claim in
PL-4's residual prose is **CORRECTED** by measurement: insertions at
`PROVINCE.md:132-:135` are *not* caught by r10 — a stale Frontier bullet
inserted there reads PASS exit 0, including the exact frozen stale literal.
The frozen falsifier itself (literal back into `:91-93`) is caught. I also
built and measured a scratch-only coverage assertion that closes every
insertion arm I could construct without changing any existing counter.

| Frozen requirement (`claims-frozen.md:30-54`) | Verdict | First-hand evidence |
|---|---|---|
| (a) clean tree still PASS | **VERIFIED** | patch applies to a pristine gate → sha `80027570…`, 713 lines; repo-root r10 `VERDICT: PASS`, exit 0; byte-identical clean scratch tree also PASS |
| (b) declared-stale literal reintroduced into a Frontier bullet FAILs | **VERIFIED** | `PROVINCE.md:91-93` stale literal → r10 exit 1, `DECLARED FAIL CLASSES: ['FRONTIER-STALE']`; stripped-anchor and truncation arms also FAIL; v10 is blind on all of them (PASS exit 0) |
| (c) every SCOPE row and existing counter intact | **VERIFIED** | `SCOPE` lists equal (20 rows, imported and compared); 17/17 shared `--json` keys equal on the clean tree; `counts` and `current_ok_per_file` identical; `VERDICT:` text line byte-identical |
| design choice: register, not a SCOPE declaration | **VERIFIED empirically** | a pristine-v10 variant with `CURRENT` SCOPE rows over `73-94`/`133-162` still reads PASS on the stale tree: `classify()` never reaches `scope_of()` for locus-free bullets (gate `:403-420`) |
| PL-4 residual #1: "insertions anywhere inside `:73-162` are caught" | **CORRECTED** | `:132`, `:133`, `:134`, `:135`, line-neutral compensated `:94`/`:135`, and `:163` appends all read r10 PASS exit 0 (§4) |
| whole frozen C1 claim | **SATISFIED** | land PL-4's patch; correct the residual wording in the landing receipt; optional delta in §5 |

## 1. First-hand re-derivations of the frozen "before" state

| # | Frozen fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -2` line 1 `c625d5d … (measured at work commit 58c3db7)`, line 2 `58c3db7` | REPRODUCED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce8…d97b5`; `wc -l` → 610 | REPRODUCED |
| 3 | SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | imported the gate (`importlib`): 20 SCOPE rows total; the seven `PROVINCE.md` rows are exactly `(8,13,CURRENT) (15,26,CURRENT) (40,43,DATED) (44,44,CURRENT) (45,62,DATED) (64,71,CURRENT) (119,131,DATED)`; max PROVINCE end = 131 (table at gate `:214-237`) | REPRODUCED |
| 4 | Frontier region = 73-93 + 133-162; file ends at 162 | `grep -n` headers → `73:## Frontier`, `95:## Adjacent`, `133:### Round-4 frontier (post-unlock)`; `wc -l PROVINCE.md` → 162; the `:91-93` EVM bullet and `:135-162` post-unlock bullets confirmed by direct read | REPRODUCED |
| 5 | Both regions UNDECLARED | programmatic coverage query over SCOPE: covering rows for `(73,93)` = `[]`, for `(133,162)` = `[]` | REPRODUCED |
| 6 | v10 reads PASS identically whether or not the bullets are stale | v10 `--root` on my own seeded trees: stale `:91-93`, stripped `:91-93`, stripped `:137`, 161-line truncation, `:132-:135` insertions and `:163` append all exit 0 `VERDICT: PASS` (matrix, §3-§4) | REPRODUCED |
| 7 | v10 baseline PASS at HEAD | repo-root run: `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696 loci=9`, `SKILL.md lines=390 loci=2`; floor `17/14/3`; `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 | REPRODUCED |
| 8 | The stale literal is grounded history, not invented | `git show 40de383 -- PROVINCE.md` (read-only) contains the before-line `-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay` and the repaired after-line naming `solc-0.8.37` / `vyper-0.4.3` | REPRODUCED |
| 9 | R4/R5 PROVINCE repairs were "clause-audited by hand" | operative half only: the region is not instrument-gradable at HEAD (items 3+5+6). The historical audit process itself is not re-derivable from artifacts | **UNVERIFIABLE** (process) / operative half REPRODUCED |

## 2. Patch identity, clean run, and counter integrity (requirements a + c)

Commands (all on scratch; the repo gate is untouched):

```
cp .ufo/gates/c1-census-v10.py /var/tmp/ex1-arc3r6/pristine/c1-census-v10.py
cp pristine/c1-census-v10.py r10-from-patch/c1-census-v10-r10.py
patch r10-from-patch/c1-census-v10-r10.py < claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum r10-from-patch/c1-census-v10-r10.py
```

`patch` reported all 8 hunks applied (`Hunk #8 succeeded at 695`); result:

```
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  713 lines
```

This is byte-identical to `PL-4/c1-census-v10-r10.py` and 103 lines longer than
the 610-line v10. **REPRODUCED.**

Repo-root r10 run (`--quiet`): exit 0, `FRONTIER register (G21): 14 rows
asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS
(stale=0 ambiguous=0 undeclared=0 unresolved=0)` — the `VERDICT:` line is
byte-identical to v10's. Clean scratch tree (byte copies of the three scoped
files; `PROVINCE.md` sha `11a5c604…0bcf2`, equal to the repo file) also PASS.

Counter integrity, `--json` on the clean tree, v10 vs r10:

```
shared keys: 17  mismatched: []
r10-only keys: ['frontier_errors', 'frontier_rows']
counts equal: True   {'PROVINCE.md': {'lines': 162, 'loci': 6},
                      'SCORECARD.md': {'lines': 1696, 'loci': 9},
                      'SKILL.md': {'lines': 390, 'loci': 2}}
current_ok_per_file equal: True   {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
declared: [] == []   frontier_rows: 14   frontier_errors: []
```

Imported-module comparison: `SCOPE` lists are equal (20 rows) between v10 and
r10; `FRONTIER` has 14 rows. The patch adds only the register, its checker, the
G19 `max_end` inclusion of register rows, the new JSON keys and the new report
line — no existing SCOPE row, class, marker or counter changes.

Design-choice check (option a is not viable). I built `v10-scope-declared.py`
= pristine v10 plus two `CURRENT` SCOPE rows, `("PROVINCE.md", 73, 94)` and
`("PROVINCE.md", 133, 162)`, and ran it on the stale `:91-93` tree: **PASS exit
0, `undeclared=0`**. A SCOPE row alone cannot fire because a unit with no
PIN/VER/PTR occurrence is `continue`d before `scope_of()` is called (gate
`:403-420`, specifically the `if not occ: continue` at `:416-420`). PL-4's
register choice is therefore necessary, not stylistic. **VERIFIED.**

## 3. Seeded-fault arms (requirement b), independent seeder

Trees are byte-copies of `PROVINCE.md`/`SKILL.md`/`SCORECARD.md` with one
content-asserted `PROVINCE.md` edit each (`EX-1/verify/seed_independent.py`).
The exact frozen literal used is `real solc/vyper-compiled bytecode untested`
(the `40de383` before-state, item 8).

| tree (edit) | v10 | r10 | r10 declared class |
|---|---|---|---|
| `clean` (byte copies) | PASS exit 0 | PASS exit 0 | `[]` |
| `forbidden` — literal back into `:91-93`, all REQUIRED tokens kept, line-count neutral | **PASS (blind)** | **FAIL exit 1** | `['FRONTIER-STALE']` |
| `required-evm` — earning tokens stripped from `:91-93` | PASS (blind) | FAIL exit 1 | `['FRONTIER-UNEVALUABLE']` |
| `required-riscv` — `r5-01` citation removed from `:137` | PASS (blind) | FAIL exit 1 | `['FRONTIER-UNEVALUABLE']` |
| `truncated` — `PROVINCE.md` cut to 161 lines | PASS (blind) | FAIL exit 1 | `['UNREADABLE', 'FRONTIER-UNEVALUABLE']` |

Exact r10 error lines (first-hand, `EX-1/verify/seeded-arms-errors.txt`):

```
forbidden:       PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
required-evm:    PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
                 PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
required-riscv:  PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
truncated:       UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
                 + 14 x "frontier uncheckable (file unreadable)" + 3 marker-uncheckable SCOPE-ERRORs
```

The `forbidden` arm is deliberately stronger than PL-4's `seeded-forbidden`
copy in one respect: it keeps every REQUIRED anchor, so it produces **exactly
one** error (the FORBIDDEN match) and isolates the stale arm from the
REQUIRED-absence arm. That is the frozen falsifier, caught. **VERIFIED.**

New blind-spot instance beyond the frozen example, reproduced independently:
v10 reads PASS on a 161-line `PROVINCE.md` — content loss past SCOPE's max
PROVINCE end (`:131`) is invisible to v10. r10's G19 extension catches it
because the register's max end is 162.

## 4. CORRECTION — the post-unlock insertion gap

PL-4 §6 residual 1 (`PL-4.md:330-334`) says:

> "Insertions anywhere inside `:73-162` are caught: above `:119` they shift the
> DATED marker row (G15 SCOPE-ERROR …), inside `:132-162` they shift register
> spans (REQUIRED-absent — measured via the seeded arms)."

That is false for insertions at `:132-:135`. Each of these trees inserts the
exact frozen stale literal as a new bullet, line-count +1:

| tree | v10 | r10 | why r10 misses |
|---|---|---|---|
| `insert-132` (before blank `:132`) | PASS exit 0 | **PASS exit 0** | new line sits outside every registered span; shifted spans still contain their REQUIRED anchors |
| `insert-133` (before `###` header) | PASS | **PASS** | same |
| `insert-134` (after header, before first bullet) | PASS | **PASS** | same |
| `insert-135` (before first post-unlock bullet) | PASS | **PASS** | new line is inside row `135-138`, but that row declares no FORBIDDEN literal and its REQUIRED tokens remain in the shifted window |
| `compensated-94` (insert at `:94`, delete blank `:118`) | PASS | **PASS** | line-count-neutral, so the G15 marker at `:119` stays put; the new bullet is before `## Adjacent` |
| `compensated-135` (insert at `:135`, delete `:144`) | PASS | **PASS** | line-count-neutral; shifted rows still satisfy REQUIRED |
| `append-163` (new bullet past EOF) | PASS | **PASS** | named past-the-bound residual (PL-4 §6.1) — G19 only fails on `len < max_end`, never on growth |
| `insert-94` (line-count +1) | FAIL | FAIL | caught **incidentally** by G15: the DATED marker declared at `:119` shifts to `:120` (`SCOPE-ERRORS: :119 marker 'verified 2026-10-13' absent`), not by G21 |

Mechanism: `FRONTIER[]` rows are positional line windows. The post-unlock rows
declare only REQUIRED anchors, whose tokens sit in the first lines of each
bullet, so a ±1-line shift still lands them inside the window; and none of the
post-unlock rows declares a FORBIDDEN literal. A new bullet therefore only
fails if it displaces a REQUIRED token or changes the file length below 162.
This is a completeness gap in the region the claim says is now gradable, and
it is not the named past-`162` residual: `:132-:135` are inside `133-162` (or
the section header gap immediately above it).

Independent corroboration (read after my measurement, not used as evidence):
PL-2 §5 measured insertions at `:133`, `:134`, `:150` and a header rename
PASS (`claims/c1/PL-2.md:167-199`); RV-3 §0 measured an insertion before the
`### Round-4 frontier` header PASS (`claims/c1/RV-3.md:20-24`). All three
measurements agree with mine.

Effect on the frozen claim: requirement (b) is phrased as a declared-stale
literal reintroduced **into a Frontier bullet** and exemplified at `:91-93`;
that arm is caught. The region-level "now gradable" statement and PL-4's
residual prose are what need correction. Verdict on the patch: **VERIFIED with
one CORRECTED residual claim**; the patch can land as-is if the landing receipt
records the corrected residual, as peers also recommend.

## 5. Tested strengthening (scratch only — NOT landed)

I built `r10-coverage.py` = r10 + a `REGIONS`/`region_check()` assertion
(G22) and a per-row bullet-shape check. It is a **proposal**, not part of
PL-4's patch and not applied to the gate. Delta:
`EX-1/verify/r10-to-coverage.diff` (79 lines, sha
`27d854196905ae11cdba08acd9c09cbfdab9b819bc05d9e9ce13282718b29db8`); built
instrument 767 lines, sha
`3db1df4b783c343964ca20f1be35515c7cb22feb1c512900f5185056fbdec499`.

Mechanics:

- `REGIONS = [("PROVINCE.md", 73, 94, {73: "^## Frontier$"}),
  ("PROVINCE.md", 133, 162, {133: "^### Round-4 frontier \(post-unlock\)$"})]`.
- Every non-blank line inside a region must be a declared header anchor or sit
  in a `FRONTIER[]` row span; otherwise `FRONTIER-UNREGISTERED`.
- No non-blank content past the register's declared tail (`:162`).
- `FRONTIER_SHAPE` for each bullet row: the row's first line must open a
  bullet (`- **`) and no later line in the row span may open another one —
  catches a compensated insertion that puts a second bullet inside a shifted
  window.
- Errors fold into `frontier_errors`, so the existing verdict path fails them
  (the declared class is `FRONTIER-UNEVALUABLE`; the error text names
  `FRONTIER-UNREGISTERED` — refine the class label if the lane wants one).

Measured, same trees as §3-§4 (full matrix in `EX-1/verify/matrix.txt`):

| tree | r10 | r10-coverage | coverage errors (first) |
|---|---|---|---|
| `clean` (repo root and scratch) | PASS 0 | **PASS 0** | `[]`; 17 shared `--json` keys still equal, counts/floor unchanged |
| `forbidden` | FAIL `FRONTIER-STALE` | FAIL `FRONTIER-STALE` | unchanged |
| `required-evm` / `required-riscv` | FAIL `FRONTIER-UNEVALUABLE` | FAIL `FRONTIER-UNEVALUABLE` | unchanged |
| `truncated` | FAIL `UNREADABLE`+`FRONTIER-UNEVALUABLE` | same | unchanged |
| `append-163` | PASS | **FAIL** | `:163 content past declared tail 162` |
| `insert-94` / `compensated-94` | FAIL (G15) / PASS | **FAIL / FAIL** | shape/anchor errors; `:94 non-registered content` on the compensated tree |
| `insert-132` / `-133` / `-134` | PASS | **FAIL** | non-registered/hdr-anchor + second-bullet errors |
| `insert-135` / `compensated-135` | PASS | **FAIL** | `second bullet inside registered span 135-138` / shifted-row shape |
| `rewritten-claim` (REQUIRED kept, new stale wording, no FORBIDDEN literal) | PASS | PASS | inherent limit, not closed by coverage — see §6 |

Recommendation: **land PL-4's patch first** (it satisfies the frozen claim).
If the lane wants the region actually fail-closed this round, apply the
79-line delta in the same landing commit and record the new sha; otherwise
record the corrected residual in the landing receipt and queue the delta as a
round-7 item. Either way, do not claim "insertions anywhere inside `:73-162`
are caught" without this delta.

## 6. Residuals and limits (named, not silently open)

1. **Forbidden coverage is earned, not exhaustive.** A same-bullet rewrite
   that keeps all REQUIRED tokens and avoids the one declared FORBIDDEN literal
   (`rewritten-claim`: "selectors are name-resolved from a live signature DB")
   passes r10 and the coverage delta. This is inherent to assertion-based
   grading; PL-4 §6.3 names it. New retractions must add FORBIDDEN patterns.
2. **Obfuscation.** The FORBIDDEN regex `untested` does not match `un tested`
   or a Unicode homoglyph. Declaration-level, not solvable by this design.
3. **Within-span continuation injection.** The delta's shape check catches a
   second *bullet* inside a span, not an injected continuation line that keeps
   the row's REQUIRED tokens. Same class as limit 1.
4. **Past-tail policy.** The delta chooses fail-closed on any non-blank content
   past `:162` (closing the named append residual). A lane that wants to keep
   the records-commit append freedom must not adopt that part; PL-4's original
   named residual is the alternative.
5. **Historical process claim.** "R4/R5 repairs were clause-audited by hand"
   is not re-derivable from artifacts; only the operative half (the region was
   not instrument-gradable) is measured.
6. **Headroom of the frozen falsifier.** Requirement (b) is satisfied literally
   by the `:91-93` arm; if a reviewer reads "the Frontier region becomes
   gradable" as "any new stale bullet anywhere in the region fails", the
   correction in §4 stands until the delta lands.

## 7. What I did NOT do

- Did not modify the gate, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, corpus,
  `.ufo/gates/`, or any tracked file; no git mutation. Gate sha before/after:
  `d0772ce8…d97b5`, 610 lines, `git status` clean for it.
- Did not apply the §5 delta to the gate; it exists only as scratch evidence.
- Did not re-derive c2 command-A counts or c3 `rule_blocks` — outside this
  seat's chain.
- Did not reuse PL-4's `seed.py`, `build_r10.py`, or the built r10 as the
  source of truth: the r10 binary was rebuilt from the pristine gate + patch,
  and every tree was seeded by `EX-1/verify/seed_independent.py`.

## 8. Landing recipe for the parent

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # expect exit 0, PASS,
  # FRONTIER register (G21): 14 rows asserted, errors: []
```

Record post-edit identity in the landing receipt, not inline (the gate's own
rule-#14 discipline, gate `:89-93`), and record the corrected residual: shifts
at `:132-:135` and line-neutral compensated inserts are absorbed by the
positional windows; the `:91-93` stale arm is caught.

Optional same-commit strengthening (scratch-tested, parent's call):

```
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/EX-1/verify/r10-to-coverage.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 3db1df4b783c3439…6fbdec499, 767 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # expect exit 0, PASS, 14 rows, errors: []
```

## Evidence index (`claims/c1/EX-1/verify/`)

- `repo-root-v10.txt`, `repo-root-r10.txt`, `repo-root-coverage.txt` — clean
  repo-root runs, exit codes.
- `matrix.txt` — 14 trees × 3 instruments (v10 / r10 / r10-coverage), exits,
  verdicts, declared classes.
- `gap-probes.txt` — insertion probes `:94` (plain + compensated), `:132`,
  `:133`, `:134`, `:135` (plain + compensated), `:163`, with r10/coverage error
  lines.
- `json-parity.txt` — 17 shared `--json` keys, zero mismatches; new keys.
- `seeded-arms-errors.txt` — exact r10 error arrays for the forbidden / REQUIRED /
  truncation arms (§3).
- `design-option-a.txt` — SCOPE-declared v10 variant still PASS on the stale
  tree (register necessity).
- `seed_independent.py` — my seeder (content-asserted, independent).
- `build_delta.py` — scratch builder for the coverage delta.
- `r10-to-coverage.diff` — the 79-line tested delta.
- `hashes.txt` — sha256 of the delta, seeder, builder, built coverage
  instrument, and clean `PROVINCE.md`.
