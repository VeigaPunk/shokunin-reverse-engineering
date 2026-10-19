# PL-1 — c1 (census instrument): independent verification of PL-4's r10 register + a measured competing build

Seat PL-1, chain c1, wave `arc3-loop1-round6`, 2026-10-19.
Repo HEAD measured this session: `c625d5de57e045188b5ce8cd450a57b349f90785`
(records; work `58c3db7`). Every number below is first-hand (rule #14): commands and
transcripts are under `PL-1/`, scratch was `/var/tmp/pl1-arc3r6/` (never `/tmp`).
The live gate was never edited — `sha256sum .ufo/gates/c1-census-v10.py` is
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` before and
after all work. Git read-only (`show`/`rev-parse`/`status`/`diff` only).

Peers read for reconciliation (not quoted as evidence; every value re-derived):
`claims/c1/PL-4.md`, `claims/c1/PL-2/prior-attempt/PL-2.md`,
`claims/c1/RV-3/prior-attempt.md`, `claims/verdicts/VZ-4.md`. At battery time the c1
chain held **three competing r10 patch texts**, not one. The PL-2 and RV-3 texts were
moved by their seats as the live wave ran, so they are cited by content sha (see the
live-tree note in §3).

## 0. Verdicts at a glance

| Target | Verdict |
|---|---|
| Frozen C1 before-state (Frontier UNDECLARED; instrument blind) | **REPRODUCED** |
| PL-4 patch round-trip (`80027570…`, 713 lines) | **REPRODUCED** |
| PL-4 requirement (a) clean PASS (scratch + repo root) | **REPRODUCED** |
| PL-4 requirement (b) seeded EVM literal caught, named class | **REPRODUCED** |
| PL-4 requirement (c) every SCOPE row / counter intact | **REPRODUCED** (17 shared JSON keys, 0 mismatches) |
| PL-4 extra: truncation 161/160 L → UNREADABLE | **REPRODUCED** |
| PL-4 §6.1: insertions inside `:132-162` are caught | **CORRECTED — one blank line at `:133`/`:134`/`:140`/`:150`/`:157` reads PASS** (fail-open across the region) |
| PL-4 forbidden coverage ("literals on record") | **CORRECTED (bounded)** — only `untested` is declared; the wall and cross clauses return with earned tokens retained and the register clean |
| PL-4 class list on a multi-class fault | **CORRECTION (minor)** — either/or drops `FRONTIER-UNEVALUABLE` when `STALE` also present |
| prior PL-2 faithful wall restore (entry 2) | **CORRECTED — dead on the wrapped text** (line-boundary blindness); one-line and token-retained clauses are caught |
| prior RV-3 faithful cross-version + token-retained wall/cross | **CORRECTED — all read PASS** (only `untested` is forbidden) |
| PL-1 merged build (PL-4 + 146-line delta) on all arms | **REPRODUCED** — closes every measured hole above |

## 1. Before-state, re-derived first-hand

| Fact | Measurement (this session) | Verdict |
|---|---|---|
| HEAD / work | `git rev-parse HEAD` → `c625d5de…`; `git log --oneline -3` → `c625d5d` over `58c3db7` | REPRODUCED |
| Gate identity | `sha256sum` → `d0772ce8…`; `wc -l` → 610 | REPRODUCED |
| Scoped file sizes | PROVINCE 162, SKILL 390, SCORECARD 1696 (`wc -l`) | REPRODUCED |
| SCOPE rows | gate `:216-222`: PROVINCE only 8-13 / 15-26 / 40-43 / 44 / 45-62 / 64-71 / 119-131; no row reaches 73-93 or 133-162 | VERIFIED |
| Frontier region | `PROVINCE.md:73` `## Frontier`; `:133` `### Round-4 frontier (post-unlock)`; bullets at 75-80, 82-93, 135-162; EOF at 162 | VERIFIED |
| Baseline | `python3 .ufo/gates/c1-census-v10.py --quiet` at repo root → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0; counts `PROVINCE lines=162 loci=6 / SCORECARD lines=1696 loci=9 / SKILL lines=390 loci=2`; G2 floor 17/14/3 | REPRODUCED |
| Blind spot | v10 on twelve fault trees (three faithful stale restores, two token-retained clauses, 161/160-line truncation, five one-line insertions at `:133`-`:157`) → **PASS exit 0 in all twelve**, counters identical to clean | REPRODUCED |
| Boundary | stale instrument-visible pin at `:88` → v10 `FAIL undeclared=1`, locus `:88 [pin] None=6.3.0 -> AMBIGUOUS (no client token in clause)` | REPRODUCED |

Seed fidelity: the stale seeds are the **byte-exact pre-`40de383` text**, not a hand paraphrase —
`git show 40de383~1:PROVINCE.md` (also 162 lines, same offsets) supplies `:92-93`
("real solc/vyper-compiled bytecode untested"), `:139-144` (the `~900s` wall form) and
`:157-160` ("probe-refused since r2"). Text and the normalization check are in
`PL-1/seed-derivation.txt`; the 20-tree builder is `PL-1/build_trees_full.py`
(commands in `PL-1/commands.txt`). A second, harder variant keeps the earned tokens
and re-inserts only the retracted clause — see §2.6.

## 2. PL-4's r10 patch — independent verification

### 2.1 Round-trip

```
git show HEAD:.ufo/gates/c1-census-v10.py > pristine.py     # sha d0772ce8…
patch -o pl4-r10.py pristine.py < claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum pl4-r10.py   # 8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
wc -l pl4-r10.py       # 713
```
Matches PL-4's claimed identity and its stored `PL-4/c1-census-v10-r10.py` exactly. **REPRODUCED.**

The patch touches no SCOPE row: every removed line is docstring, verdict, `declared`
or `max_end` text (`PL-1/commands.txt` records the grep). The new table is inserted
after the SCOPE `]`, and `max_end` widens to include register ends. **VERIFIED.**

### 2.2 Requirement (a) — clean PASS

- Scratch clean tree: exit 0, `FRONTIER register (G21): 14 rows asserted, errors: []`,
  `DECLARED FAIL CLASSES: []`, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`.
- Real repo root (`python3 /var/tmp/pl1-arc3r6/pl4-r10.py --quiet`): identical PASS, exit 0.
**REPRODUCED.**

### 2.3 Requirement (b) — seeded faults

| Seed (my own trees, faithful git before-state) | PL-4 exit | Declared class | First error |
|---|---|---|---|
| EVM `:92-93` full pre-state | 1 | `['FRONTIER-STALE']` | `PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)` |
| EVM token-only (earned tokens kept, `— untested` added) | 1 | `['FRONTIER-STALE']` | same FORBIDDEN line, no REQUIRED error |
| wall `:139-144` full pre-state | 1 | `['FRONTIER-UNEVALUABLE']` | `REQUIRED 'arc2-r7' absent` |
| cross `:157-160` full pre-state | 1 | `['FRONTIER-UNEVALUABLE']` | `REQUIRED 'r12-02\|r14-01' absent` |
| truncation to 161 / 160 lines | 1 | `['UNREADABLE','FRONTIER-UNEVALUABLE']` | `PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)` |

The frozen falsifier — reintroduce the retracted EVM literal, clean tree still PASS —
is **REPRODUCED** end-to-end. The wall and cross restores are also caught, but through
the positive floor (`REQUIRED` absent), not the `FORBIDDEN` arm; the disposition names
the file:line and pattern either way.

Minor correction: on the full EVM restore PL-4 reports three errors (one FORBIDDEN,
two REQUIRED-absent) but `frontier_class` is an either/or, so
`DECLARED FAIL CLASSES` lists only `['FRONTIER-STALE']`. The verdict is right; the
named-class list under-reports. Not a claim violation ("a named disposition" is flagged).

### 2.4 Requirement (c) — counter integrity

`--json` clean tree, v10 vs PL-4 (`PL-1/json-invariance.txt`):

```
shared keys: 17   mismatched: []
pl4-only keys: ['frontier_errors', 'frontier_rows']
counts equal: True | current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
text output diff (minus the new FRONTIER line): empty
```
**REPRODUCED.** Every pre-existing SCOPE row, counter and JSON key is intact.

### 2.5 The first DISCREPANCY — one-line insertions in the post-unlock region read PASS

PL-4 §6.1 states: "*inside `:132-162` they shift register spans (REQUIRED-absent —
measured via the seeded arms)*". Measured on trees that insert **one blank line** at
five positions (content otherwise byte-identical), plus `+2`/`+3` at the boundary:

| Insertion | PL-4 exit | Register errors |
|---|---|---|
| before `:133` (`### Round-4 frontier`) | 0 | `[]` |
| before `:134` | 0 | `[]` |
| before `:140` | 0 | `[]` |
| before `:150` | 0 | `[]` |
| before `:157` | 0 | `[]` |
| before `:133`, two blank lines | 1 | `['FRONTIER-UNEVALUABLE']` (REQUIRED absent) |
| before `:133`, three blank lines | 1 | `['FRONTIER-UNEVALUABLE']` |
| before `:92` (above the region) | 1 | register `[]`; caught by the pre-existing G15 DATED marker at `:119` |

This is a **fail-open across the whole post-unlock region**, not one position: every
row's span carries ≥1 line of slack (the 2-line spans 145-146, 147-148, 149-150, 87-88,
89-90 over 2-line bullets; the wider spans carry more), so a one-line shift moves each
required token into the *next* row's shifted window and all checks still pass. The
register then grades shifted lines silently — the silent-mis-grade class a census
instrument exists to prevent — while the "re-key in the same commit" discipline has no
instrument enforcement. `+2`/`+3` fail only because the shift exceeds the slack.
PL-4's residual text needs the correction; the design needs a per-line anchor to close it.

### 2.6 The second DISCREPANCY — stale clauses survive if the earning tokens do

The frozen falsifier restores the *whole* pre-state line, which necessarily drops the
earned tokens (`solc-0.8.37`, `arc2-r7`, `r12-02`/`r14-01`), so PL-4's REQUIRED floor
catches the wall and cross restores as `FRONTIER-UNEVALUABLE`. A sharper, realistic
reintroduction keeps the earned tokens and re-adds only the retracted clause:

| Token-retained fault | v10 | PL-4 | PL-2 prior | RV-3 | PL-1 build |
|---|---|---|---|---|---|
| wall bullet + "The wall still hits REA's ~900s internal session deadline on rerun." (`CLOSED`/`arc2-r7` intact) | 0 | **0** | 1 `STALE` | **0** | 1 `STALE` |
| cross bullet + "`compare-application-versions` still probe-refused since r2." (`r12-02`/`r14-01` intact) | 0 | **0** | 1 `STALE` | **0** | 1 `STALE` |

PL-4's only `FORBIDDEN` literal is `untested`, so two of the three recorded stale forms
are unguarded once the tokens survive. PL-4 §6.3 frames coverage as "only literals on
record … new retractions extend the register"; the measurement bounds that framing —
one of three recorded literals is guarded today. This is not a violation of the frozen
claim (which names only the EVM literal), but it is a material limit on the stated goal
("Frontier-region staleness claims become gradable"). RV-3 forbids only `untested` too,
so it passes both rows; the prior PL-2 attempt catches both because its ranges span the
whole region and these clauses sit on one line.

## 3. Peer reconciliation — the other two c1 patches, same battery

Method: identical trees, five gates — the complete 5 × 18 matrix (90 runs) is
`PL-1/battery-full.tsv`, regenerated byte-identically after the final tree builder
(`PL-1/build_trees_full.py`). Exit 0 = PASS, 1 = FAIL. The earlier narrow tables
(`battery.tsv`, `battery-pl1.tsv`) are kept for diffing against the first pass.

**Live-tree note.** The PL-2 and RV-3 proposals I tested were moved/rewritten by their
seats while this wave ran. The exact texts I applied are preserved at
`claims/c1/PL-2/prior-attempt/` (patch sha `976188cc…`, built gate `2d7ee95b…`, 705
lines) and `claims/c1/RV-3/prior-attempt.md` (built gate `8e420679…`, 712 lines); my own
extraction of the latter is `PL-1/patches/rv3-extracted.diff`. All comparisons below are
by content sha, not by path; the PL-2 and RV-3 columns mean **prior attempts**.

| Fault tree | v10 | PL-4 r10 | prior PL-2 r10 | prior RV-3 r10 | PL-1 build |
|---|---|---|---|---|---|
| clean (162 L) | 0 | 0 | 0 | 0 | 0 |
| seed-evm full pre-state | 0 | 1 `STALE` | 1 `STALE` | 1 `STALE+UNATT` | 1 `STALE+UNEVAL` |
| seed-evm token-only | 0 | 1 `STALE` | **0** | 1 `STALE` | 1 `STALE` |
| seed-wall full pre-state | 0 | 1 `UNEVAL` | **0** | 1 `UNATT` | 1 `STALE+UNEVAL` |
| seed-wall one-line isolate | 0 | 1 `UNEVAL` | 1 `STALE` | 1 `UNATT` | 1 `STALE+UNEVAL` |
| seed-wall tokens retained | 0 | **0** | 1 `STALE` | **0** | 1 `STALE` |
| seed-cross full pre-state | 0 | 1 `UNEVAL` | 1 `STALE` | **0** | 1 `STALE+UNEVAL` |
| seed-cross tokens retained | 0 | **0** | 1 `STALE` | **0** | 1 `STALE` |
| trunc161 / trunc160 | 0 | 1 `UNREADABLE` | 1 `UNREADABLE` | 1 `UNATT` / `ANCHOR` | 1 `UNREADABLE` |
| insert `:133` +1 (header) | 0 | **0** | 1 (scope-error) | 1 `ANCHOR` | 1 `ANCHOR` |
| insert `:134`/`:140`/`:150`/`:157` +1 | 0 | **0** | **0** | 1 `ANCHOR` | 1 `ANCHOR` |
| insert `:92` (above the region) | 1 (G15) | 1 (G15) | 1 (G15) | 1 `ANCHOR` | 1 `ANCHOR` |
| insert `:133` +2 / +3 | 0 | 1 `UNEVAL` | — | — | 1 `ANCHOR` |
| stale pin `:88` | 1 `undeclared=1` | 1 `undeclared=1` | 1 `ambiguous=1` | 1 `undeclared=1` | 1 `undeclared=1` |
| locus-free append past `:162` | 0 | 0 | 0 | 0 | 0 |

### 3.1 Prior PL-2 attempt — a dead entry on wrapped text (CORRECTED)

Its `FRONTIER_STALE` entry 2 declares `hits REA's ~900s internal session deadline` over
`PROVINCE.md:133-162`. On the **faithful** pre-`40de383` restore that phrase is split by
the line wrap — `:139` ends "hits REA's ~900s internal", `:140` begins "session
deadline" — and `frontier_scan()` tests line by line, so it reads **PASS**
(`transcripts/pl2-r10__seed-wall.txt`).

Causal isolate: the same literal placed on one line inside the wall bullet is caught
(`FRONTIER-STALE PROVINCE.md:139 …`, exit 1; `transcripts/pl2-r10__seed-wall-oneline.txt`).
So the entry is not mis-cited, it is **unreachable on the wrapped text it was derived
from**. Its §5 lists entries 2-3 as "UNVERIFIABLE (not exercised)"; entry 2 is now
exercised and negative on the faithful restore. Its entry 3 (`probe-refused since r2`)
and its broad regional ranges do catch the one-line and token-retained clauses, so the
attempt's register is stronger than entry 2 alone suggests; the defect is the
line-boundary blindness, and entry 1 is phrase-keyed (a token-only `untested` addition
with earned tokens retained passes — a coverage boundary, not the frozen literal).

Its other arms hold: clean PASS; EVM full restore FAIL; cross restore FAIL; truncation
FAIL `UNREADABLE`; insert `:133` +1 FAIL via its structural marker
(`scope_errors: PROVINCE.md:133 marker '^### Round-4 frontier \(post-unlock\)$' absent`,
declared classes `[]` — the pre-existing scope-error channel). Its clean-tree 17 shared
JSON keys are unchanged (my check: 0 mismatches; 2 additive keys `frontier_register`,
`frontier_stale`). On my `:88` pin tree its declared SCOPE row surfaces the pre-existing
`AMBIGUOUS` disposition as `ambiguous=1` where the other gates read `undeclared=1` —
same underlying locus line, different bucket; clean-tree counters are identical, so
claim (c) is met, but the semantic shift on fault trees is worth naming.

### 3.2 Prior RV-3 attempt — measured-stale restores read PASS (CORRECTED)

Its cross-version row requires `compare-application-versions` at `:157` and has no
forbidden literal. The **faithful** pre-`40de383` restore of `:157-160` still begins
"`compare-application-versions` still / probe-refused since r2; …", so anchor and
required token both match:

```
FRONTIER register (r10): 13 rows, 0 error(s)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit 0
```

Its only `FORBIDDEN` literal is `untested`, so both **token-retained** clauses also read
PASS (§2.6). A literal the arc already measured false can be back on the page with the
register clean. VZ-4's audit of this attempt tested only the EVM seed, so this is new.
RV-3 is otherwise the strongest anti-reflow design: its per-row anchors catch every
one-line insertion (8 `FRONTIER-ANCHOR` errors on the `:133` case), its wall row catches
the faithful wall restore (`FRONTIER-UNATTESTED`, `arc2-r7`/`CLOSED` absent), and
truncation is caught by anchor or by the `HOPPER_LAUNCHER_PATH` token on the dropped
last line. It does not raise G19 (`max_end` stays 131), so those truncations fail via
the register rather than the declared `UNREADABLE` class.

### 3.3 Shared residual — a locus-free append past `:162`

An appended, locus-free frontier bullet (163-line tree) reads **PASS in all five gates**
(v10 and the four r10s). PL-4 names it; it is inherent to a line-keyed register. Only a
locus-bearing append would fail (via `UNDECLARED`).

## 4. A competing build that closes every measured hole

Base: PL-4's r10 (sha `80027570…`) + `PL-1/patch-pl4-to-pl1.diff` (146 lines, 67+/32−)
→ `PL-1/pl1-r10.py`, 748 lines, sha
`7724adccdf6391cffc622b8fa3144ede421eb24aedc1431893c2482f892c12a1`. Built by
`PL-1/build_pl1.py` (scratch artifacts, not landed).

Changes, each answering a measured hole:

1. **Per-line anchors** — every row gains `(anchor_line, anchor_regex)`; the two section
   headers (`:73`, `:133`), the intro (`:75`) and all 13 bullets are anchored (16 rows).
   A shift fails `FRONTIER-ANCHOR` instead of silently grading the wrong window. Closes
   PL-4's `+1` fail-open.
2. **Whitespace-collapsed matching** — `seg = re.sub(r"\s+", " ", …)` before REQUIRED /
   FORBIDDEN search, so a literal split by PROVINCE's ~80-col wrap is seen. Closes PL-2's
   dead entry-2 class.
3. **The three measured-stale literals are declared FORBIDDEN**, each derived first-hand
   from `git show 40de383~1:PROVINCE.md`: `untested` (`:91-93`),
   `hits REA's ~900s internal session deadline` (`:139-144`),
   `probe-refused since r2` (`:157-160`). Closes PL-4's missing wall/cross arms and
   RV-3's cross-version hole.
4. **Claim words added to REQUIRED**: `CLOSED` (wall), `EXERCISED` (cross), so a
   CLOSED→OPEN or EXERCISED→un-exercised rewrite loses the floor.
5. **All error classes reported** (no either/or): `sorted({cls for cls, _ in errs})`.
6. G19 `max_end` from register ends (PL-4's) retained.

Battery on the same trees (`PL-1/battery-full.tsv`, PL-1 rows):

| Fault | Exit | Declared classes | Named error (first) |
|---|---|---|---|
| clean scratch + repo root | 0 | `[]` | `16 rows asserted, errors: []` |
| EVM full / token-only / tokens-retained | 1 | `STALE+UNEVAL` / `STALE` | `FORBIDDEN untested matched untested` |
| wall full / tokens-retained | 1 | `STALE+UNEVAL` / `STALE` | `FORBIDDEN hits REA's ~900s internal session deadline matched …` |
| cross full / tokens-retained | 1 | `STALE+UNEVAL` / `STALE` | `FORBIDDEN probe-refused since r2 matched …` |
| trunc161 / trunc160 | 1 | `UNREADABLE+UNEVAL` | `161 lines < declared max 162 (rows beyond EOF)` |
| insert +1 at `:133`/`:134`/`:140`/`:150`/`:157` | 1 | `ANCHOR` | `:133 anchor ^### Round-4 frontier \(post-unlock\)$ absent` |
| insert `:133` +2 / +3 | 1 | `ANCHOR` | same |
| stale pin `:88` | 1 | `[]` (pre-existing) | `undeclared=1` — unchanged v10 class |
| append past `:162` | 0 | `[]` | declared residual, unchanged |

Requirement (c) holds: 17 shared JSON keys, 0 mismatched; only `frontier_errors` /
`frontier_rows` added; counts equal; floor 17/14/3; clean text output byte-identical to
v10 minus the new FRONTIER line (`PL-1/json-invariance.txt`).

New residuals, named: (a) a novel semantic change that keeps every declared token still
passes — a text register is not a semantics engine; (b) whitespace collapse could in
principle join a wrap into a false positive (not observed; every pattern is a full
claim phrase or a distinct token); (c) anchors pin absolute lines, so any legitimate
frontier edit fails closed until re-keyed — intended, and now enforced rather than
advisory; (d) the past-`:162` append residual is unchanged.

## 5. Landing recommendation

1. **PL-4 is the patch that meets the frozen claim's letter**, and all three requirements
   reproduce first-hand. It is safe to land as the c1 closure **only with its residual
   text corrected**: (i) one-line insertions at `:133`/`:134`/`:140`/`:150`/`:157` read
   PASS, not `REQUIRED-absent`; (ii) only one of the three recorded stale literals has a
   `FORBIDDEN` arm — the wall and cross clauses return with the register clean when the
   earned tokens are kept.
2. **Preferred if the integrator will take a 146-line delta**: apply PL-4, then
   `PL-1/patch-pl4-to-pl1.diff` (measured here; resulting sha `7724adcc…`). It closes the
   reflow fail-open, both token-retained clauses, and PL-2's wrap blindness, with the same
   (a)/(c) invariants (17 shared JSON keys unchanged).
3. **Do not land the prior PL-2 attempt as-is** without normalizing entry 2's match (or
   keying a one-line literal): on the faithful wall restore it reads PASS. It is otherwise
   the broadest literal catcher on this battery (it catches both token-retained clauses)
   and its structural-marker/reflow and truncation arms hold.
4. **Do not land the prior RV-3 attempt as-is** without forbidden arms for the wall and
   cross-version clauses (and optionally G19 `max_end`): all three stale restores read
   PASS when the earned tokens survive. Its per-row anchor discipline is the best of the
   three and is the model the PL-1 delta borrows.
5. **Convergence note (not audited here).** While this seat ran, the live c1 tree also
   gained verification artifacts (EX-2, EX-3, RV-1, and a rewritten RV-3) that independently
   reproduce PL-4 and, in at least RV-3's case, the same two deficiencies (insertion
   silence; missing forbidden arms). I did not audit those artifacts — full wave
   reconciliation is the VZ/CN chain's job; the content-sha comparisons above stand on
   their own.

## 6. Files, scope, and what I did not do

Writes (only this seat's artifact dir):
`claims/c1/PL-1.md`; `claims/c1/PL-1/{battery-full.tsv,battery.tsv,battery-pl1.tsv,
commands.txt,json-invariance.txt,seed-derivation.txt,build_pl1.py,build_trees.py,
build_trees_full.py,pl1-r10.py,patch-pl4-to-pl1.diff}`,
`claims/c1/PL-1/patches/rv3-extracted.diff` and `claims/c1/PL-1/transcripts/`
(50 selected arm outputs, listed by filename).
`pl1-r10.py` is the built instrument (sha `7724adcc…`, 748 lines); the patch is the
authoritative delta for a reviewer.

**Live-tree caveat.** The wave tree was being written by other seats throughout this run.
The PL-2 proposal I tested now lives at `claims/c1/PL-2/prior-attempt/` and the RV-3
proposal at `claims/c1/RV-3/prior-attempt.md`; my extraction of the latter is preserved
under `PL-1/patches/` so the round-trip (`8e420679…`) is reproducible regardless of later
rewrites. Every peer claim above is tied to a content sha, not a path.

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, `.ufo/gates/`,
  or any tracked file. Gate sha re-checked after all runs: unchanged `d0772ce8…`.
- Did not run command A or the c2/c3 halves — outside this seat's chain; c2/c3 are
  EX-7/SC-3/RV-7 territory.
- Did not audit the final landing receipt; post-edit identity belongs there, not inline.
- Observed but not mine: the working tree carries a pre-existing unstaged modification
  to `.ufo/waves/arc2-loop1-round10/C3.md` (round-10 working copy, 184+/29−). I did not
  touch it; flagging it so the parent is not surprised at records time.
