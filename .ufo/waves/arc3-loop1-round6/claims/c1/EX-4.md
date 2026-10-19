# EX-4 — c1: independent verification of PL-4's r10 frontier-claim register

Seat EX-4, chain c1 (census instrument), wave arc3-loop1-round6, 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch lab
`/var/tmp/ex4-arc3r6/` (nothing under `/tmp`; EDQUOT avoided). Gate custody:
`sha256 .ufo/gates/c1-census-v10.py` = `d0772ce8…c8d97b5` before and after every
experiment; git used read-only (`rev-parse`/`log`/`show`/`status`). Every number
below is first-hand this session (rule #14); no prior seat's or round's value is
quoted as evidence. Evidence files live next to this artifact in `EX-4/`.

## 0. Verdict in one line

**VERIFIED.** PL-4's patch (`claims/c1/PL-4/patch-v10-to-r10.diff`, identical to
the diff printed inside `PL-4.md:119-302`) applies cleanly to the HEAD gate,
reproduces sha256 `80027570…d14aecca` / 713 lines, reads PASS on the real tree,
catches the frozen seeded literal with a named disposition, and preserves every
existing SCOPE row and counter (17/17 shared `--json` keys equal). Two secondary
statements in PL-4's residual prose are **CORRECTED** by measurement (the
`:132-162` insertion claim; the "literals on record" framing), and I found the
before-state blind spot is broader than PL-4 measured (v10 also reads PASS on a
131-line PROVINCE.md, where the entire post-unlock region is gone). None of this
breaks the frozen claim's falsifier; no change to the patch is required to land.
An optional scratch hardening is measured in §7 and is **not** part of the
delivered patch.

## 1. First-hand re-derivations of the frozen "before" state

| Frozen fact (`claims-frozen.md:30-53`) | My measurement | Verdict |
|---|---|---|
| HEAD records `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`; `git log --oneline -2` shows `c625d5d … (measured at work commit 58c3db7)` | VERIFIED |
| Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`; `wc -l` → 610 | VERIFIED |
| Scoped file sizes | `wc -l`: PROVINCE.md 162, SKILL.md 390, SCORECARD.md 1696 | VERIFIED |
| SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131 | gate `:215-237`: 20 rows total, the 7 PROVINCE rows are exactly that list; no row intersects 73-93 or 133-162 (programmatic coverage `[]` for both) | VERIFIED |
| Frontier region = 73-93 + 133-162 | `:73 ## Frontier`; intro `:75-80`; bullets `:82-83/:84-86/:87-88/:89-90/:91-93`; `:133 ### Round-4 frontier (post-unlock)`; bullets `:135-138/:139-144/:145-146/:147-148/:149-150/:151-156/:157-160/:161-162`; file is exactly 162 lines | VERIFIED |
| The bullets are ungradable by L3 (the mechanism) | importing the gate: region 73-93 has 7 block units, **0 `REA_GATE` units, 0 PIN/VER/PTR matches**; region 133-162 has 9 units, **0 / 0**. v10's six PROVINCE loci sit in blocks `44-44`, `64-71`, `125-125` — none intersects either region | VERIFIED |
| "instrument reads PASS identically whether or not those bullets are stale" | my own seed (`forbid-91`): v10 exit 0 **PASS**, `PROVINCE.md lines=162 loci=6` — byte-identical counts to the clean tree | REPRODUCED |
| v10 baseline PASS at HEAD | `python3 .ufo/gates/c1-census-v10.py --quiet` → exit 0, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, floor `PROVINCE.md=17 SCORECARD.md=14 SKILL.md=3`, live anchors `{'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'}` | REPRODUCED |
| The `:91-93` stale literal is a measured historical before-state | `git show 40de383 -- PROVINCE.md` removes `-  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay` and adds the held `solc-0.8.37`/`vyper-0.4.3` carrier text. The same diff removes two more stale forms (§6 P3) | VERIFIED |
| "R4/R5 repairs were clause-audited by hand, not instrument-graded" | operative half re-measured (the region is ungraded at HEAD, above); the historical by-hand process is not derivable from artifacts | PARTLY — process UNVERIFIABLE |

Baseline command (rerunnable): `python3 .ufo/gates/c1-census-v10.py --quiet`
from the repo root. Full transcript: `EX-4/baseline.txt`.

## 2. Delivered patch identity

```
$ cp .ufo/gates/c1-census-v10.py pristine.py
$ patch pristine.py < claims/c1/PL-4/patch-v10-to-r10.diff
patching file pristine.py            # exit 0, no fuzz/offset
$ sha256sum pristine.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
$ wc -l pristine.py
713 pristine.py
$ cmp pristine.py claims/c1/PL-4/c1-census-v10-r10.py
IDENTICAL
```

The diff printed in `PL-4.md:120-301` is byte-identical to the shipped
`patch-v10-to-r10.diff` (`diff` exit 0, 182 lines each). Across the whole patch,
no `+`/`-` line touches a SCOPE row (`identity.txt`, `invariance.txt`).

## 3. Requirement (a) — clean tree still PASS

`python3 pristine.py --quiet` with the default `--root` (the real repo) → exit 0:

```
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Counters unchanged: `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696
loci=9`, `SKILL.md lines=390 loci=2`; floor `17/14/3`. REPRODUCED.

## 4. Requirement (b) — seeded-fault arms (my own trees, my own seeder)

Trees are byte-copies of the three scoped files at HEAD (clean copy sha256
matches the repo: `11a5c604…` / `8e56f3d9…` / `0d10e18f…`), seeded by
content-asserted edits (`EX-4/seeder.py`). Full matrix: `EX-4/arms-matrix.txt`.

| tree | edit | v10 | r10 | r10 declared class |
|---|---|---|---|---|
| clean | none | 0 PASS | 0 PASS | `[]` |
| forbid-91 | frozen literal "…real solc/vyper-compiled bytecode untested…" at `:93`, earning tokens kept | 0 PASS (blind) | **1 FAIL** | `['FRONTIER-STALE']` — `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested'` (exactly one error) |
| req-evm | `:91-93` replaced by "EVM bytecode — see corpus." | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` — REQUIRED `solc-0.8.37` and `vyper-0.4.3` absent |
| req-riscv | `r5-01` citation stripped from `:137` | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` — REQUIRED `r5-01` absent at `135-138` |
| trunc-161 | last line deleted | 0 PASS (blind) | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` — `161 lines < declared max 162` + 14 uncheckable rows |
| trunc-131 | last 31 lines deleted (the whole post-unlock region) | **0 PASS (blind)** | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` — `131 lines < declared max 162` |
| append-163 | new stale bullet appended past `:162` | 0 PASS | **0 PASS** | named residual (`PL-4.md:327-329`) reproduced |

The `forbid-91` arm isolates FORBIDDEN (both earning tokens remain), so the
FAIL is not a side effect of REQUIRED-absent. The frozen falsifier is met on
both halves: clean PASS + seeded FAIL with a named class.

`trunc-131` is a stronger before-state than PL-4 measured: v10's G19 threshold
for PROVINCE.md is its SCOPE max end 131, so a file truncated to exactly 131
lines passes v10 even though `:132-162` (the whole post-unlock frontier,
including `:161-162`) has vanished from the document. r10 raises the threshold
to the register max end 162 and fails closed.

## 5. Requirement (c) — counter integrity, measured

`--json` on the real repo, v10 vs r10 (`EX-4/invariance.txt`):

```
shared keys: 17   mismatched: []
v10-only: []      r10-only: ['frontier_rows','frontier_errors']
counts equal: True   floor: 17/14/3 -> 17/14/3   verdict: PASS -> PASS
```

SCOPE table byte-invariance: HEAD 20 rows vs r10 20 rows, `tables identical:
True`; the patch contains zero `+`/`-` lines matching a SCOPE row. Non-quiet
text delta is exactly one added line:

```
87a88
> FRONTIER register (G21): 14 rows asserted, errors: []
```

The `VERDICT:` line is byte-identical to v10's. VERIFIED.

## 6. Adversarial probes — corrections and measured limits

All numbers below are from my trees; exact outputs in `EX-4/residuals.txt`,
`EX-4/insertion-sweep.txt`, `EX-4/arms-matrix.txt`.

**P1 — insertion sweep: 32/32 positions in `:132-162` are absorbed.**
I inserted one neutral line before every 1-based line P for P = 132…163 and ran
r10 on each tree: **PASS 32 / 32**, `frontier_errors=[]` in every case. The
spans are line-keyed but their REQUIRED patterns sit inside contiguous windows,
so a +1 shift leaves every pattern inside its shifted window; for insertion
positions 132-162, old `:162` drifts to `:163` and out of the last row,
unnoticed.

This **CORRECTS** `PL-4.md:330-333` ("insertions … inside `:132-162` … shift
register spans (REQUIRED-absent — measured via the seeded arms)"). It is not
universally true — for a +1 insertion in that region it is uniformly false.
By contrast, my `ins-76` and `ins-95` trees (insertions above the `:119` marker
line) fail under **v10** with `SCOPE-ERRORS: PROVINCE.md:119 marker 'verified
2026-10-13' absent`, so that catch is pre-existing G15 machinery, not the
register; I did not probe insertions between `:120` and `:131`. No stale claim
is introduced by a neutral insertion; the correction is to the residual prose,
not to the requirement.

**P2 — the declared literal outside its declared span is not caught.**
`forbid-84` appends "Real solc/vyper-compiled bytecode untested." to the
`:84-86` bullet (the crashes bullet). r10 exit 0 **PASS**, `frontier_errors=[]`;
v10 also PASS. The FORBIDDEN regex `untested` is declared only on row `:91-93`.
Read literally, the frozen requirement says FAIL "when a declared-stale literal
is reintroduced into a Frontier bullet"; that holds for the claim's own
`:91-93` example but not for the same literal in a sibling bullet. This
**CORRECTS** the framing of `PL-4.md:337-341`: only the `:91-93` span carries
FORBIDDEN at all.

**P3 — 2 of the 3 recorded stale literals are unguarded.**
`git show 40de383 -- PROVINCE.md` records three before-states removed by the
same repair: the EVM `bytecode untested` form, the `>90 MB PE` form
("hits REA's ~900s internal session deadline … Next: raise
`REA_GHIDRA_STARTUP_TIMEOUT_MS`"), and the cross-version form
("compare-application-versions still probe-refused since r2"). PL-4 declares
FORBIDDEN only for the first. Measured:

- `stale-159`: the pre-r5 clause "compare-application-versions still
  probe-refused since r2" appended to `:160`, keeping `r12-02`/`r14-01` → r10
  exit 0 **PASS**, `frontier_errors=[]`.
- `stale-ins-162`: a brand-new stale bullet containing "real solc/vyper-compiled
  bytecode untested" inserted inside the declared region (before old `:162`) →
  r10 exit 0 **PASS** (the `:161-162` REQUIRED anchors survive the shift; the
  literal is outside the only FORBIDDEN row).

The second case is sharper than the named past-the-bound residual: novel
staleness can be inserted *inside* the declared region and pass. This is
consistent with `PL-4.md:337-341`'s spirit ("coverage is earned, not
exhaustive") but the sentence "only literals on record … are declared" reads as
broader than the measurement: **one** recorded literal is guarded, not all
three, and the guard is span-scoped.

**P4 — headings are not asserted.** `header-rename` (`## Frontier` →
`## Frontier (renamed)`, line-count neutral) → v10 PASS and r10 PASS. The
register starts at `:75`, so the section header is outside every row. Not a
claim failure (a heading is not a staleness claim); a two-row hardening is
measured in §7.

**P5 — a semantically stale rewrite with anchors intact passes.**
`sem-riscv` rewrites `:136-137` to "fully CLOSED and unremarkable … (r5-01:
superseded)" while keeping `RISC-V` and `r5-01` in span → r10 PASS. Inherent:
the register is a text-assertion floor, not a semantics engine. Confirms
`PL-4.md:337-341`.

**P6 — past-bound append reproduced.** `append-163` → v10 PASS, r10 PASS.
Exactly the named residual at `PL-4.md:327-329`; no discrepancy.

**P7 — declared-class reporting is exclusive, not additive.** Tree `mixed-91`
replaces `:91-93` with "EVM bytecode (extended) — real solc/vyper-compiled
bytecode untested." (no `solc-0.8.37`/`vyper-0.4.3`). r10 exit 1,
`frontier_errors` holds **three** entries (two REQUIRED-absent + one FORBIDDEN),
but `declared_fail_classes` is `['FRONTIER-STALE']` only (r10 `:664-666`
branches STALE first). All errors remain in `frontier_errors` and the text
report, so the disposition is not lost; the class list names one class, not the
set. Cosmetic. Exact extract: `EX-4/residuals.txt` (mixed-91 section).

## 7. Optional hardening, measured on scratch (NOT landed, NOT part of PL-4's patch)

Two additive changes to a scratch copy of r10 (`EX-4/hardening.txt`):

1. a register-global FORBIDDEN list (`untested`, `probe-refused since r2`,
   `REA_GHIDRA_STARTUP_TIMEOUT_MS`) checked across the union of the declared
   frontier spans — closes P2/P3's cross-bullet and second-literal gaps;
2. two rows asserting the section headings (`:73`, `:133`) — closes P4.

Measured on 16-row hardened instrument:

| tree | result |
|---|---|
| real repo root | PASS exit 0, `FRONTIER register (G21): 16 rows asserted, errors: []` |
| `header-rename` | FAIL — `PROVINCE.md:73-73 REQUIRED '^## Frontier$' absent` |
| `ins-133` | FAIL — `PROVINCE.md:133-133 REQUIRED '^### Round-4 frontier …' absent` |
| `forbid-84` | FAIL — `FORBIDDEN-GLOBAL 'untested'` |
| `stale-159` | FAIL — `FORBIDDEN-GLOBAL 'probe-refused since r2'` |
| `stale-ins-162` | FAIL — `FORBIDDEN-GLOBAL 'untested'` at `161-162` |
| `req-evm` / `req-riscv` / `trunc-161` | FAIL exactly as before (no regression) |
| `append-163`, `sem-riscv` | still PASS (past-bound and novel-wording limits remain) |

Clean-tree PASS and `frontier_rows` 14 → 16 only; no pre-existing key changes.
Offered as a follow-up if the lane wants it; the frozen claim does not require
it, and I did not modify the gate.

## 8. Cross-check against the competing design (archived PL-2 patch)

When I started, `claims/c1/` carried a second complete r10 design at
`PL-2/c1-census-v10-r10.patch` — a 195-line patch whose proposed instrument is
705 lines with sha `2d7ee95b…` — plus a third design inside the then-current
`RV-3.md`. Both peer paths have since been rewritten to
verify PL-4; I record the comparison against the patch I applied first-hand,
not against peer prose. On identical trees:

| arm | archived PL-2 design | PL-4 design |
|---|---|---|
| clean | PASS, 17/17 shared JSON keys | PASS, 17/17 shared JSON keys |
| frozen literal at `:91-93` | FAIL `FRONTIER-STALE` | FAIL `FRONTIER-STALE` |
| paraphrase / stripped anchors (`req-evm`, `req-riscv`) | **PASS — missed** | FAIL `FRONTIER-UNEVALUABLE` |
| literal in a sibling bullet (`forbid-84`) | FAIL (region-wide literal) | PASS (span-scoped) |
| header rename / insertion before `:133` | FAIL via marker assertions | PASS (gap, see §7) |
| `VERDICT:` line | changes (`frontier=%d`) | byte-identical |

The archived design has the stronger structural guard; PL-4 has the stronger
positive floor (stripped or reworded bullets fail) and the stricter
requirement-(c) identity. The lane converged on PL-4; my §7 hardening is the
cheap way to recover the structural advantage without touching SCOPE or the
`VERDICT:` format. No conflict remains at landing: as of 14:00 local
(2026-10-19) both rewritten peer artifacts (`PL-2.md` mtime 13:58, `RV-3.md`
mtime 13:59) verify PL-4 rather than propose their own patch.

## 9. Per-item verdicts

| Item | Verdict | Evidence |
|---|---|---|
| HEAD `c625d5d` / work `58c3db7` | VERIFIED | §1 |
| gate sha `d0772ce8…`, 610 lines | VERIFIED | §1 |
| SCOPE rows exactly 8-13/15-26/40-43/44/45-62/64-71/119-131; zero coverage of 73-93/133-162 | VERIFIED | §1 |
| Frontier bullets carry no `REA_GATE` unit and no PIN/VER/PTR locus | VERIFIED | §1 (7/9 units, 0/0 matches) |
| v10 baseline PASS, counters and floor | REPRODUCED | §1, `baseline.txt` |
| v10 blind to the seeded stale literal | REPRODUCED | §4 |
| v10 blind to a 131-line truncation (whole post-unlock region gone) | REPRODUCED (new) | §4 |
| Patch applies; sha `80027570…`, 713 lines; built file and inline diff identical | VERIFIED | §2 |
| Requirement (a): clean PASS, 14 rows, `errors: []` | REPRODUCED | §3 |
| Requirement (b): seeded literal FAILs with named class | REPRODUCED | §4 |
| Requirement (c): 17/17 shared keys equal; SCOPE table identical; text delta one line | VERIFIED | §5 |
| PL-4 §6.1 "insertions inside `:132-162` fail REQUIRED" | **CORRECTED** | §6 P1 (32/32 pass) |
| PL-4 §6.3 "literals on record are declared" framing | **CORRECTED** | §6 P2/P3 (1 of 3; span-scoped) |
| Past-bound append residual | REPRODUCED as documented | §6 P6 |
| "By-hand R4/R5 audit" historical process | UNVERIFIABLE | §1 |
| Archived PL-2 competing design | MEASURED, superseded | §8 |

## 10. What I did NOT do

- Did not modify `.ufo/gates/c1-census-v10.py`, PROVINCE.md, SKILL.md,
  SCORECARD.md, corpus, or any tracked file. Custody sha re-checked after all
  work: `d0772ce8…c8d97b5`. Git read-only.
- Did not land the §7 hardening (scratch copy only) and did not write the gate.
- Did not re-derive c2 (command-A counts) or c3 (`rule_blocks`) — outside this
  seat's chain.
- Probe trees read live HOME configs for anchors, read-only; `live` is the
  host's, identical for v10 and r10, so the comparisons stand.
- The insertion sweep uses a neutral line; semantically stale insertions are
  covered only by `stale-ins-162` (§6 P3), not exhaustively.

## 11. Landing recipe (endorsed)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet
  # expect exit 0, VERDICT: PASS, FRONTIER register (G21): 14 rows asserted, errors: []
```

Record post-edit identity in the landing receipt, not inline (the gate's own
rule-#14 discipline). If the lane takes the §7 follow-up, land it as a separate
revision after this one and re-key in the same commit.

## File inventory (this seat's writes)

- `claims/c1/EX-4.md` — this artifact.
- `claims/c1/EX-4/identity.txt` — patch application, shas, custody before/after.
- `claims/c1/EX-4/baseline.txt` — v10 and r10 runs on the real tree + text diff.
- `claims/c1/EX-4/arms-matrix.txt` — 17 trees × 2 instruments.
- `claims/c1/EX-4/invariance.txt` — 17-key JSON comparison + SCOPE invariance.
- `claims/c1/EX-4/insertion-sweep.txt` — 32 insertion positions.
- `claims/c1/EX-4/residuals.txt` — P1-P7 probe diffs and instrument output.
- `claims/c1/EX-4/hardening.txt` — scratch global-FORBIDDEN + header hardening.
- `claims/c1/EX-4/seeder.py` — tree builder/seeder.
