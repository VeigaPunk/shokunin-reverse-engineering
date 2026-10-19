# RV-3 — c1: independent verification of PL-4's r10 frontier-claim register

Seat RV-3, chain c1 (census instrument), wave arc3-loop1-round6, 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; HEAD
`c625d5de57e045188b5ce8cd450a57b349f90785` (`c625d5d`), work `58c3db7` — both
re-derived this session by `git rev-parse HEAD` + `git log --oneline -5`.
Gate custody: `sha256 .ufo/gates/c1-census-v10.py` =
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` before
and after every experiment below; the repo gate was never modified. Scratch
lab `/var/tmp/rv3-c1/` (nothing under `/tmp`; EDQUOT avoided). Git read-only
(`rev-parse`/`log`/`show`/`status` only).

## 0. Deliverable in one line

PL-4's patch (`claims/c1/PL-4/patch-v10-to-r10.diff`, identical to the diff
printed inside `PL-4.md:119-302`) **applies cleanly, reproduces the claimed
identity, and satisfies the frozen C1 clauses (a), (b), (c) on an independent
scratch lab**. Ten scratch trees × two instruments were measured; every row of
PL-4's §3 matrix reproduced. Two claims in PL-4's *residual prose* are
**CORRECTED** by measurement: a one-line insertion before `### Round-4
frontier` stays PASS (`PL-4.md:330-333`), and a recorded pre-r5 stale literal
reintroduced into `:157-160` stays PASS (`PL-4.md:337-341`). Neither breaks the
frozen claim's falsifier. Verdict: **VERIFIED with 2 corrections + 3 named
limitations**.

Note on a pre-existing file: `claims/c1/RV-3.md` already existed at this seat's
start (untracked, provider line zai glm-5.3-flash, no evidence dir, a different
`FRONTIER_REGISTER` design with per-row anchor+cite tuples). This seat owns
that path; the prior text is preserved verbatim at
`claims/c1/RV-3/prior-attempt.md` and no number below is taken from it.

## 1. First-hand re-derivations of the frozen "before" state (rule #14)

Every value was produced this session; none is quoted from PL-2/PL-4 or a prior
round.

| Frozen fact (`claims-frozen.md:30-53`) | My measurement | Verdict |
|---|---|---|
| HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -5` shows `c625d5d … (measured at work commit 58c3db7)` | VERIFIED |
| Gate at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce8…d97b5`; `wc -l` → 610 | VERIFIED |
| Scoped file sizes | `wc -l`: PROVINCE.md 162, SKILL.md 390, SCORECARD.md 1696 | VERIFIED |
| SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | Parsed `SCOPE` from the gate with `ast.literal_eval` (`rv3/RV-3/invariance.txt`): 20 rows total; PROVINCE rows exactly `[(8,13,CURRENT),(15,26,CURRENT),(40,43,DATED),(44,44,CURRENT),(45,62,DATED),(64,71,CURRENT),(119,131,DATED)]`; table at gate `:215` | VERIFIED |
| Frontier 73-93 + 133-162 UNDECLARED | `grep -nE 'PROVINCE\.md", *(7[3-9]\|8[0-9]\|9[0-3]\|13[3-9]\|1[4-6][0-9])' .ufo/gates/c1-census-v10.py` → `NO MATCH`. Programmatic coverage: fully-covering `[]`, overlapping `[]` for both ranges | VERIFIED |
| "instrument reads PASS identically whether or not those bullets are stale" | Own seed (§3): v10 PASS exit 0 on both clean and seeded trees; `counts` byte-identical (`PROVINCE.md lines=162 loci=6`) — the seeded region contributes zero detections | REPRODUCED |
| Bullets carry no pin/version/path loci (mechanism) | Zero `PIN`/`VER`/`PTR` matches in 73-93 and 133-162; **also zero `REA_GATE` matches** — `classify()` skips at its first `continue` (gate `:406-407`) before `scope_of()` is reached, and the no-occurrence `continue` is gate `:419-420` | VERIFIED |
| v10 baseline PASS at HEAD | repo-root run: `live anchors {'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'}`, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0; floor `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3` | REPRODUCED |
| The `:91-93` stale literal is a measured historical before-state | `git show 40de383 -- PROVINCE.md` shows `-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay` → `+  (Core, r3-07), real solc-0.8.37 carriers … vyper-0.4.3`. `git log --oneline -S 'bytecode untested' -- PROVINCE.md` → `40de383`, `8f89dbd`. The same diff also holds the post-unlock before-states (`Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS`, `compare-application-versions still probe-refused since r2`) | VERIFIED |
| "R4/R5 repairs were clause-audited by hand, not instrument-graded" | Operative half is now re-measured (the region is ungraded at HEAD); the historical by-hand process is **not derivable from artifacts** | PARTLY — process UNVERIFIABLE |

Scratch clean-tree copies were byte-copies of the repo files at HEAD:
PROVINCE.md `11a5c604…f0bcf2`, SCORECARD.md `0d10e18f…78ae08c`, SKILL.md
`8e56f3d9…a68bf` (`sha256sum`, `rv3/RV-3/arms.txt` header).

## 2. Patch application and identity

```
cp .ufo/gates/c1-census-v10.py /var/tmp/rv3-c1/pristine/gate.py   # 610 lines, sha d0772ce8…
cp …/PL-4/patch-v10-to-r10.diff /var/tmp/rv3-c1/pl4.diff
cp /var/tmp/rv3-c1/pristine/gate.py /var/tmp/rv3-c1/r10.py
patch /var/tmp/rv3-c1/r10.py < /var/tmp/rv3-c1/pl4.diff
# → patching file /var/tmp/rv3-c1/r10.py   (no fuzz/offset messages)
sha256sum /var/tmp/rv3-c1/r10.py
# → 8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
wc -l /var/tmp/rv3-c1/r10.py   # → 713
python3 -c "import ast; ast.parse(open('/var/tmp/rv3-c1/r10.py').read())"   # syntax OK
```

`80027570…` and 713 lines match `PL-4.md:114-117` exactly. The `diff` block
embedded in `PL-4.md` is **byte-identical** to the patch file (10,574 B each,
one block; compared with Python `re.findall(r'```diff\n(.*?)```')`). The patch
is additive: zero `-`/`+` lines inside the SCOPE table (the only hunk touching
SCOPE is an insertion after the closing `]`), and the new table is `FRONTIER`
at r10 `:291` with 14 rows.

## 3. Independent arm matrix (requirements a and b)

Seeds were constructed by this seat with content assertions, not by copying
PL-4's `seed.py`. Six trees hold byte-copies of the three scoped files; each
edit is line-count preserving except the truncation.

| Tree | My edit | v10 exit/verdict | r10 exit/verdict | r10 declared classes |
|---|---|---|---|---|
| clean | none | 0 PASS | 0 PASS | `[]` |
| seeded | `:91-93` restored to the measured pre-40de383 text ("…real solc/vyper-compiled bytecode untested…") | 0 PASS (blind) | 1 FAIL | `['FRONTIER-STALE']` |
| fonly | keep `solc-0.8.37`/`vyper-0.4.3`, append only `— untested` on :92 | 0 PASS (blind) | 1 FAIL | `['FRONTIER-STALE']` |
| reqevm | `:91-93` → `- **EVM bytecode (extended)** — see corpus.` (earning tokens stripped) | 0 PASS (blind) | 1 FAIL | `['FRONTIER-UNEVALUABLE']` |
| reqriscv | `:137` `r5-01` → `archived` | 0 PASS (blind) | 1 FAIL | `['FRONTIER-UNEVALUABLE']` |
| trunc | PROVINCE.md truncated to 161 lines | 0 PASS (blind) | 1 FAIL | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |

Exact r10 error lines (`rv3/RV-3/arms.txt`):

```
seeded:   PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
          PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
          PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
fonly:    PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)   [exactly one error]
reqevm:   PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent … (x2 incl. vyper)
reqriscv: PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
trunc:    UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
          + 14 × "PROVINCE.md:<s>-<e> frontier uncheckable (file unreadable)"
```

Every row of `PL-4.md:84-91` is therefore **REPRODUCED**, including the named
disposition requirement (b): the seeded reintroduction FAILs exit 1 with
`FRONTIER-STALE`, while the clean tree still reads PASS exit 0. Requirement
(a) also holds on the **real repo root**: `python3 /var/tmp/rv3-c1/r10.py
--quiet` → exit 0, `FRONTIER register (G21): 14 rows asserted, errors: []`.

Coverage enumeration (independent): the two regions contain 13 bullets with
starts `[82,84,87,89,91]` and `[135,139,145,147,149,151,157,161]`; PL-4's 14
rows are `[(75,80),(82,83),(84,86),(87,88),(89,90),(91,93),(135,138),(139,144),
(145,146),(147,148),(149,150),(151,156),(157,160),(161,162)]` — every bullet is
covered, plus the section intro 75-80. Only `## Frontier` :73-74, the blank
`:81`, and `### Round-4 frontier` :133-134 (headers/blank) are outside the
register.

## 4. Invariance (requirement c)

- **SCOPE table:** parsed from pristine vs r10 with `ast.literal_eval` →
  `SCOPE identical: True`, 20 rows both sides. No row re-keyed, none removed.
- **`--json` on the real repo:** shared keys 17, `mismatched []`; v10-only keys
  none; r10-only `['frontier_errors','frontier_rows']`; `counts` equal
  (`162/6, 1696/9, 390/2`); `current_ok_per_file` equal (`17/14/3`);
  verdicts `PASS/PASS`; `frontier_rows 14`, `frontier_errors []`.
- **Text output on a clean tree:** `diff` of v10 vs r10 stdout is exactly one
  added line — `FRONTIER register (G21): 14 rows asserted, errors: []`. The
  `VERDICT:` line, counters, floor line and G7/G11 lines are byte-identical.
- **G19 max-end:** r10 `:611` computes `max_end` as SCOPE ends ∪ FRONTIER ends,
  so PROVINCE's declared max moves 131 → 162. Measured by the `trunc` arm:
  v10 still PASSes a 161-line PROVINCE; r10 fails it as declared
  `UNREADABLE`. This is a strictness increase, not a silence.

## 5. Per-item verdicts on PL-4's artifact

| PL-4 claim (path:line) | Verdict | My evidence |
|---|---|---|
| HEAD `c625d5d` / work `58c3db7` | VERIFIED | §1 |
| gate sha `d0772ce8…`, 610 lines | VERIFIED | §1 |
| SCOPE rows exactly the frozen list; no Frontier coverage | VERIFIED | ast + grep, §1 |
| v10 PASS on the real tree with 162/6, 1696/9, 390/2 and floor 17/14/3 | REPRODUCED | §1, §4 |
| v10 blind to the stale `:91-93` literal (PASS, counters identical) | REPRODUCED | `seeded` vs `clean`, §3 |
| patch sha `80027570…`, 713 lines, embedded diff = file | VERIFIED | §2 |
| 14 register rows, all bullets covered | VERIFIED | §3 enumeration |
| r10 clean PASS incl. `frontier_errors []` | REPRODUCED | §3, real root and scratch |
| seeded catch with `FRONTIER-STALE` + exact `:91-93` disposition | REPRODUCED | `seeded`/`fonly`, §3 |
| six-tree matrix (`PL-4.md:84-91`) | REPRODUCED | all six rows, §3 |
| 17-key JSON identity, two new keys, counts/floor unchanged (`PL-4.md:304-323`) | VERIFIED | §4 |
| G19 threshold 131 → 162 | REPRODUCED | `trunc`, §4 |
| Register design rationale: SCOPE row alone could not grade these bullets | VERIFIED | zero `REA_GATE`/PIN/VER/PTR hits; classify skips at `:406-407`/`:419-420` |
| Past-the-bound append residual (`PL-4.md:327-329`) | REPRODUCED | `app163` → r10 PASS, §6 |
| "Insertions anywhere inside :73-162 are caught … inside :132-162 they shift register spans (REQUIRED-absent)" (`PL-4.md:330-333`) | **CORRECTED** | `ins132` → v10 PASS **and r10 PASS**, §6 |
| "only literals on record … are declared" + new retractions extend (`PL-4.md:337-341`) | **CORRECTED (incomplete)** | `stale159` → r10 PASS, §6 |
| mixed-fault declared-class granularity | minor limitation | `seeded` classes `['FRONTIER-STALE']` despite 2 UNEVALUABLE errors, §6 |
| per-row corpus citations in the register | gap vs rule #14 | rows are 5-tuples with no cite field; provenance is the r5-audit code comment + the single FORBIDDEN literal |

## 6. Corrections and measured residuals (all from `rv3/RV-3/probes.txt`)

**C1. One-line insertion at the post-unlock boundary is silent.**
Tree `ins132`: a blank line inserted before `### Round-4 frontier` (old
`:133`), file 163 lines. v10 exit 0 PASS; **r10 exit 0 PASS**, `frontier_errors
[]`. The spans are line-keyed, so every post-unlock bullet shifts one line and
the required patterns still fall inside their declared windows; old `:162`
(`(`HOPPER_LAUNCHER_PATH`), JEB.`) drifts to `:163` and out of every row. So a
boundary shift can silently unregister the tail of the region. By contrast
`ins81` (blank line before `:82`) fails both: v10 via the existing G15 marker
at `:119` (`marker 'verified 2026-10-13' absent from ''`), r10 additionally
with `:84-86 REQUIRED 'oldest-first' absent` and `:89-90 REQUIRED
'unsupported_host' absent`. Correction applies to `PL-4.md:330-333`, which
says insertions inside `:132-162` shift spans and fail REQUIRED — that is not
universally true; a shift that leaves every pattern inside its window passes.

**C2. The post-unlock region has no FORBIDDEN arm, so a recorded stale clause
can be reintroduced with its earning tokens intact.** Tree `stale159`: the
pre-r5 clause ``compare-application-versions still probe-refused since r2`` was
appended to `:160` (the cross-version bullet), keeping `r12-02`/`r14-01`.
r10 exit 0 PASS, `frontier_errors []`. That literal is on record in the
`40de383` diff (§1) — the same repair that produced the EVM before-state — but
only the EVM row declares FORBIDDEN in PL-4's register. `PL-4.md:337-341`
frames coverage as "literals on record"; the measurement shows the register
covers one of the three recorded literals. This is a coverage limit consistent
with the spirit of residual 3, but the prose's framing overstates what is
guarded. The same is true of the pre-r7 `Next: raise
REA_GHIDRA_STARTUP_TIMEOUT_MS` form at `:139-144` (not separately measured;
same mechanism, no FORBIDDEN row).

**C3. Declared-class reporting is exclusive, not additive.** On `seeded`, three
errors fire (two REQUIRED-absent + one FORBIDDEN) but
`declared_fail_classes` is `['FRONTIER-STALE']` only: r10 `:664-666` picks
STALE first and drops UNEVALUABLE. The text and `frontier_errors` carry all
three, so this is a reporting granularity issue; a mixed-fault run names one
class, not the set.

**C4. Per-row citations absent.** PL-4's rows carry no `cite` element
(compare the pre-existing competing design at `RV-3/prior-attempt.md`, whose
register rows include an anchor line/regex and a corpus cite). The frozen C1
does not require citations, so this is a recommendation, not a claim failure;
rule #14 would favor adding them when the register is next re-keyed.

**Residual confirmed as documented:** `app163` (bullet appended past `:162`
carrying `untested`) → v10 PASS and r10 PASS, exactly the named
past-the-bound residual (`PL-4.md:327-329`). The register is not a
novel-staleness detector; it grades declared spans only.

## 7. Verdict

**Frozen C1 is satisfied by PL-4's design and patch.** (a) PASS on the clean
tree, measured on both scratch and the real repo root; (b) the seeded
reintroduction of the frozen example literal FAILs with a named disposition
and a citation-quality error line; (c) every SCOPE row, counter and JSON key
is preserved (SCOPE identical, 17/17 shared keys equal). The design choice
"secondary register, not SCOPE declaration" is independently justified:
neither Frontier region contains a single `REA_GATE` unit, so `classify()`
never reaches `scope_of()` there.

**Landing recommendation:** land PL-4's patch as-is, and in the landing receipt
(not inline — the gate's own rule-#14 discipline, gate `:89-93`) record the
post-edit identity and the *corrected* residual list: shift of the
post-unlock boundary at `:132` can pass silently; FORBIDDEN coverage is the EVM
row only; past-bound appends remain unregistered. If a same-round strengthening
is wanted, two cheap additions (not required by the frozen claim) close the
measured gaps: (i) anchor-line assertions per row plus a per-row `cite`, in the
style of the preserved competing design; (ii) FORBIDDEN literals for the two
other `40de383` before-states (`probe-refused since r2`,
`REA_GHIDRA_STARTUP_TIMEOUT_MS`-as-remediation), each with a seeded arm.

## 8. Custody, write scope, files

- Repo gate sha before/after: `d0772ce8…d97b5` (unchanged; `sha256sum` at the
  end of the session). No tracked file, PROVINCE/SKILL/SCORECARD, corpus,
  `.ufo/gates/` source, or custody path was modified. `git status --short`
  shows only the pre-existing ` M .ufo/waves/arc2-loop1-round10/C3.md` and the
  untracked round-6 wave dir (the `M` was present in my first status call,
  before any writes).
- Scratch: `/var/tmp/rv3-c1/` — `pristine/gate.py`, `r10.py`, six arm trees,
  four probe trees, raw outputs.
- Seat writes:
  - `claims/c1/RV-3.md` (this artifact)
  - `claims/c1/RV-3/arms.txt` (12 arm runs, full output; sha256 `4dd7507d…b591`)
  - `claims/c1/RV-3/invariance.txt` (ast SCOPE, JSON/floor/text diffs; sha256 `6aef76f5…cd15d`)
  - `claims/c1/RV-3/probes.txt` (four shift/residual probes; sha256 `a54ed14c…b757`)
  - `claims/c1/RV-3/prior-attempt.md` (verbatim preservation of the
    pre-existing file at this seat's path; not evidence, not relied upon)

## 9. Landing recipe (endorsed from `PL-4.md:355-361`)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # expect exit 0, PASS,
  # FRONTIER register (G21): 14 rows asserted, errors: []
```

Then record post-edit identity in the landing receipt, not in the gate.
