# EX-14 — apply ALL patches to a /var/tmp scratch copy of PROVINCE.md; census PASS required

Seat EX-14 · chain c2 · role executor · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40`. Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback dispatch recorded in
`claims-frozen.md:11-15` after the hyper lane returned 402 out-of-credits on all
48 seats. No git mutation; no seat-scoped file written outside this seat's
artifact directory and `seats/EX-14.md`; custody paths never opened; scratch
under `/var/tmp/arc3r4-ex14` (never `/tmp`, standing EDQUOT rule); the real
`PROVINCE.md` was only ever read and copied.

## 1. Work performed (evidence pointers)

**Seat task.** Apply ALL C2 patches to a `/var/tmp` scratch copy of `PROVINCE.md`,
run `.ufo/gates/c1-census-v10.py --root <scratch-root-with-all-three-scoped-files>`,
**PASS required**, iterate the patch texts until PASS, and capture the final
patched file + census output.

**What the gate actually needs (measured, not assumed).** The census `SCOPE`
table names three files — `PROVINCE.md`, `SKILL.md`, `SCORECARD.md` — so a
scratch root carrying only `PROVINCE.md` cannot PASS: `SKILL.md` and
`SCORECARD.md` would be `UNREADABLE` (G19) and `G2`/`BLIND-INSTRUMENT` would
fire. Every run here therefore uses a scratch root with **all three** scoped
files copied from the repo. Evidence: `harness/run.sh`.

**Harness (re-runnable, committed under `harness/`).**

| file | what | sha256 |
|---|---|---|
| `harness/apply_patches.py` | patch applier: prose (`-`/`+` fenced hunks, RV-4 format, split on `@@` markers so a multi-hunk block applies hunk-by-hunk) **or** unified diff; content-anchored so a stale author line number still lands; per-hunk resolved offset reported; `--dry-run` resolves without writing (a bug where the prose path ignored `--dry-run` and mutated the baseline was found and fixed mid-wave — see §3d) | `abb8e921820fef4e59364498ef7b1b6667fe6d2cb28dc936ddc9866a9425f2b1` |
| `harness/run.sh` | one run: fresh scratch root → copy 3 scoped files → apply every patch → sha256 before/after → census → capture. **Fails closed**: a patch that does not apply aborts with `APPLY-FAILED` and exit 1, so a census verdict is never issued over unpatched bytes | `7d4fc6d5c5c8153219b7a98d589994781edf8855af1b9daa6a019ce3d2b3764a` |
| `harness/preflight.py` | predicts census impact before applying: per-file line delta + every added line that would carry a locus, with the scope class the census would assign it (imports the census's own regexes) | `4e8d486321d0be34cfac33a88e8e96c1ffb0fa6a823514b5cc7c589bc9606e46` |
| `harness/discover.sh` | enumerates round-4 patch texts targeting a scoped file, with identity | `fd53a486c4aed02d960a2099ed0418b82ad675be76db57654b7a81bd0c58374c` |

**Format parity with the C2 reviewer's applier.** RV-4 landed
`claims/c2/RV-4/prose-apply.py` + `harness/apply-and-census.sh`, which defines the
C2 patch format (fenced `-`/`+` hunks) and the differ
(`claims/c2/RV-4/census-diff.py`). This seat's applier was extended to consume
that same format and was cross-checked against RV-4's applier on the round-3
reference patch text `arc3-loop1-round3/claims/c2/EX-30/registry-row.patch.md`:
**both appliers report the identical per-hunk outcome** (`hunk 1 [SKILL.md]:
FAILED — search text not found verbatim`) and leave the three scoped files
byte-identical to each other. The failure is the r3 patch's own staleness (its
search text names SKILL.md rows that the r3 landing rewrote), not an applier
difference.

**Baseline (before) measurement, control.** Fresh scratch root, no patch:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`
(162 lines), `SKILL.md` `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f`
(390), `SCORECARD.md` `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7`
(1580) — all three byte-identical to the repo copies.
Census → **PASS exit 0**, `stale=0 ambiguous=0 undeclared=0 unresolved=0`,
scope-errors `[]`, unreadable `[]`, declared fail classes `[]`, G2 floor
`PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`. Evidence:
`evidence/head-sha256.txt`, `evidence/baseline-census.json`.

**Patch inventory at write time (measured by `harness/discover.sh`).**
**No round-4 C2 patch text existed when this seat ran.** The round-4 tree
contained only RV-4's review instruments (`census-diff.py`, `prose-apply.py`,
`harness/apply-and-census.sh`) and no `*.patch*`/`*.diff` file anywhere under
`.ufo/waves/arc3-loop1-round4/`. `claims/c2/EX-11/` (planner) and
`claims/c2/EX-12..EX-17/` (the other C2 executors) were empty directories. The
gap is named in §5, not papered over.

**Because the claim requires an actual PASS on patched input, and no authored
patch had landed, this seat produced and ran a demonstration patch against the
one debt the claim names by hand** — the stale PROVINCE Frontier bullet
("real solc/vyper-compiled bytecode untested"). The demonstration is *not* a
substitute for the chain's own patch texts; it is the proof that the pipeline
works, the measurement of what a conformant patch looks like, and a
pre-validated candidate the parent can adopt or discard.
`evidence/demo-frontier-repair.patch.md` (sha256
`507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51`, re-derived
at write time — see the identity table in §6).

## 2. Proposed changes

**Patch-text paths — this seat proposes none of its own** (the seat line is
apply-and-measure, and the C2 authors own the patch texts). What this seat
delivers instead:

- `evidence/demo-frontier-repair.patch.md` — a **demonstration** patch,
  line-neutral and needle-free, repairing the named stale Frontier bullet. It
  is offered as a pre-validated candidate, explicitly labelled a demo.
- `evidence/candidate-complete-frontier-repair.patch.md` — the complete
  line-neutral, needle-free repair covering the four stale rows the chain's
  census first named (`F1b`, `F5b`, `X1`, `R2`), measured to clear all four
  anchors with the census gate reading PASS (§3b).
- `evidence/candidate-complete-frontier-repair.v2.patch.md` — **the recommended
  candidate**: revision 2 repairs all **six** stale rows and fixes the false Core
  promotion the chain verdict sustained against the revision above (§3c). 6/6
  hunks, 162 → 162 lines, census PASS, all six stale phrases gone. The earlier
  revisions are retained as the measured history, not as landing candidates.
- `harness/*` — the applier + runner + preflight, for the parent and for the
  C2 authors to run their real patch texts through. A **multi-hunk patch must be
  written as a unified diff** or as a fenced block split by `@@` markers: the
  prose parser treats one fenced block as one hunk, so a multi-row repair
  written as a single undivided block fails to apply (measured, and the parser
  was then fixed to split on `@@`).

**The two constraints a C2 PROVINCE patch must satisfy** (both measured here,
both load-bearing, neither obvious from the claim text):

1. **Line-neutrality.** PROVINCE's DATED row `("PROVINCE.md", 119, 131)` declares
   its marker at line 119. Any patch that changes the line count above 119
   shifts that line and the marker assertion fails. Measured:
   `evidence/control-linecount-change-fails.txt` → a 3-line-replacing patch that
   adds one line yields
   `SCOPE-ERRORS: ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from ''"]`
   and **FAIL exit 1**.
2. **Needle-freedom in undeclared regions.** PROVINCE lines 72–118
   (Frontier + Adjacent) are **UNDECLARED** in the census scope table. A repair
   there is census-inert *only while it introduces no needle*: the named bullet's
   own unit parses `gated=False, needles=[]`, so a prose-only repair passes.
   Measured counter-direction: `evidence/sabotage-needle-in-undeclared.txt` —
   writing `rea-agents@6.5.0` into line 91 yields
   `VERDICT: FAIL (undeclared=1)`.

The demonstration patch satisfies both: 162 → 162 lines, and all three new
lines parse `scope=None, gate=False, pin=[], ver=[], ptr=[]`.

### 2b. Landing hazard measured for the parent's records commit (not the seat's)

The round's SCORECARD section and LOG entry will be appended by the parent past
the declared bound (`SCORECARD.md` DATED rows end at 855). The instrument's own
standing rule requires such text to be **locus-free in its unit** — no
`rea-agents@x.y.z`, no bare `6.x.y`, no `~`/`-absolute path:line`. Measured both
ways on scratch copies:

| appended round-4 SCORECARD text | census |
|---|---|
| contains `rea-agents@6.5.0` (the natural way these sections are written — every prior round section does) | **FAIL exit 1, `undeclared=1`** |
| same section, needle-free (`the pinned REA surfaces`) | **PASS exit 0** |

This is a real, live hazard for the round's own records commit, and it is
invisible until the census is run on the appended tree. Flagged for the parent;
the fix is wording, not scope (the alternative — re-keying the bound — is the
instrument's own documented fail-open path and was refused in the r1/r3 rounds).

## 3. Before → after measurement for the chain's claim

The C2 claim's falsifiable form: *the staleness census (each checked bullet:
stale / current / adjudicated, with evidence) → stale count N → 0; PROVINCE line
count unchanged; census PASS at the work tree after the parent applies the
patches.*

| unit | before | after (demo applied) | evidence |
|---|---|---|---|
| census verdict | PASS exit 0 | **PASS exit 0** | `evidence/baseline-census.json`, `evidence/demo-census-pass.txt`, `evidence/demo-census.json` |
| stale / ambiguous / undeclared / unresolved | 0 / 0 / 0 / 0 | **0 / 0 / 0 / 0** | same |
| scope-errors / unreadable / declared fail classes | `[]` / `[]` / `[]` | **`[]` / `[]` / `[]`** | same |
| G2 floor per file | 17 / 14 / 3 | **17 / 14 / 3** | same |
| PROVINCE line count | 162 | **162** | `wc -l`, `harness/run.sh` |
| PROVINCE sha256 | `d075a3c6…` | **`1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2`** | `harness/run.sh` before/after capture |
| Frontier bullet text | "real solc/vyper-compiled bytecode untested" | "real solc-0.8.37 carriers (Core, arc3-r1); vyper-compiled bytecode untested" | `diff` of lines 89–95 |

**Reproduction from the artifact's own bytes (rule #14).** The pipeline was
re-run a second time from the *committed* copy of the demo patch
(`evidence/demo-frontier-repair.patch.md`, not the scratch original) against a
fresh scratch root, after re-deriving the three repo-side scoped files:
`PROVINCE.md d075a3c6…` / `SKILL.md 5eec51c0…` / `SCORECARD.md 21042196…`
(unchanged, so the patch's search text still applies). Result: identical
after-state `1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2`
and **census PASS exit 0**. The measurement reproduces from the delivered
artifact, not only from this seat's transient scratch.

**Independent re-application by two other seats.** VZ-2 re-applied the same demo
patch first-hand and recorded before `d075a3c6…` → after `1bfb5dd7…`, 162 lines,
census PASS — byte-identical to this seat's claim
(`claims/c2/VZ-2/evidence/demo-patch-independent-reapply.txt`). RV-4's harness
graded it `RESULT: CLEAN — no new gated locus, no regression` then
`RESULT: CONFORMANT — census PASS` (`claims/c2/RV-4/runs/ex14-demo-apply-census.out`).
This seat also ran RV-4's harness itself: `evidence/rv4-harness-confirmation.log`.

### 3b. The complete repair — all four stale rows, stale count → 0

The demo patch repaired one row. The chain's own staleness census (VZ-2's
instrument) names **four**: `F1b`, `F5b`, `X1`, `R2`. This seat built and
measured the complete line-neutral repair:
`evidence/candidate-complete-frontier-repair.patch.md`.

| unit | before | after (complete patch) |
|---|---|---|
| census gate verdict | PASS exit 0 | **PASS exit 0** (0/0/0/0) |
| PROVINCE line count | 162 | **162** |
| PROVINCE sha256 | `d075a3c6…` | **`dfa70b42b51dd45bd82bbf3037b707c0e1f10518ec9b0d5f68d72dbda652d27e`** |
| stale anchors still present (`claim_present`) | `F1b` `F5b` `X1` `R2` all **True** | **all four False** |
| hunks applied | — | 4/4, each `-n/+n` balanced |

Evidence: `evidence/candidate-census-pass.txt` (gate),
`evidence/staleness-anchor-diff.txt` + `evidence/staleness-census-after.json`
(the per-row anchor flip).

### 3c. Revision 2 — the chain verdict's two requirements, both closed

The chain verdict (`claims/c2/verdict.md`) graded the revision above as the
wave's best patch and sustained two defects against it. This seat re-derived
both, agreed, and shipped `evidence/candidate-complete-frontier-repair.v2.patch.md`.

**Defect 1 (verdict R4) — a false Core promotion, sustained on re-derivation.**
The previous revision's F5b replacement read `real solc-0.8.37 carriers
(Core, arc3-r1/r3) … held`. Re-derived by this seat: both corpus entries open
`RESULT-class, no Core promotion` (`2026-10-19-arc3-r1-evm-real-solc.md:1`,
`…-r3-evm-optimizer-shapes.md:1`); `grep -n arc3-r1 PROVINCE.md` finds nothing
outside the patched bullet; and `PROVINCE.md:75-76` requires a `LOG.md` entry for
promotion, which does not exist. **Landing that text would have written a false
promotion into a scoped file.** v2 drops `Core`/`held` and states RESULT-class;
verified absent on the v2 tree.

**Defect 2 (verdict R3) — two stale rows left untouched.** v2 repairs `F3`
(`JEB (unprobed)` → `JEB (probed; operator-gated)`) and the Core host-fallback
absence list. Both verified first-hand by this seat: the JEB verb returns a
declared refusal, and `command -v` shows `7z` `/usr/bin/7z`, `xxd` `/usr/bin/xxd`,
`radare2` `/usr/bin/radare2`, `strace` `/usr/bin/strace`, `upx` `/usr/bin/upx`
present while `cabextract`, `rizin`, `ltrace` are absent.

| unit | before | after (v2) |
|---|---|---|
| census gate verdict | PASS exit 0 | **PASS exit 0** (0/0/0/0) |
| PROVINCE line count | 162 | **162** |
| PROVINCE sha256 | `d075a3c6…` | **`69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5`** |
| hunks applied | — | **6/6**, each `-n/+n` balanced |
| the six named stale phrases | all present | **all absent**; all six replacements present |

Evidence: `evidence/v2-census-pass.txt` (gate), `evidence/v2-clause-audit.txt`
(the per-phrase before→after audit), `evidence/v2-staleness-census-after.json`.

**Iteration cost, recorded honestly.** v2's EVM hunk first came out `-2/+3`
(net +1 line) → the tree read 163 lines and the gate **FAILed**; the preflight had
flagged `LINE-DELTA approx=+1` before the run. Compressing the replacement to
2→2 restored 162 lines and PASS. Two revisions of the complete candidate were
measured by this seat (`8a0e12ff…` → `0b8ad045…`); per the verdict's R5, only the
sha measured at landing time is authoritative.

**A caveat the chain must know, measured.** VZ-2's census **hardcodes each row's
verdict** at build time (`add(..., "stale", ...)`), so its `SUMMARY stale=N`
tally does **not** move when a repair lands — it is a census of the corpus, not a
grader of the patched document. The gradable signal is `claim_present`. Two
further rows it flags (`F3`, `C1`) were added by a mid-run revision of that
instrument (24 → 26 rows) and are wording defects about IDA/Hopper/JEB and the
host fallback-reader list — **not** the four rows the frozen claim names. Any
final grading of the C2 claim should therefore be stated as "the four named
stale rows' anchors are cleared and the census gate reads PASS", not as
"the instrument's stale count reads 0".

**Staleness of the named bullet is confirmed against admitted corpus state, not
asserted:** `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (title:
"selectors recovered K/K on on-host 0.8.37 compiles") and `corpus/README.md:38`
(`| EVM | … 2026-10-19-arc3-r1-evm-real-solc … | held — EVMole selectors recovered
… from real solc-0.8.37-compiled runtime carriers (arc3-r1)`) both record the
real-solc leg as held, while PROVINCE.md:92 still reads "untested". The residual
`vyper-compiled` half of the bullet is **not** stale at write time and the demo
patch deliberately keeps it (the r3 entry's own Unknowns read "Vyper and solc
versions other than 0.8.37").

**Census is deterministic across reruns:** two consecutive `--json` runs on the
same patched tree are byte-identical (`evidence` T1 in §4).

**Independent confirmation by the chain's own differ.** RV-4's
`census-diff.py`, run by this seat over the baseline and demo census JSONs:
`baseline assertions=16  candidate assertions=16`, `NEW gated loci — 0`,
`REMOVED assertions — 0`, `DISPOSITION MOVES — 0`, all verdict rows unchanged,
`RESULT: CLEAN — no new gated locus, no regression`, exit 0.

### 3d. The chain's own patch texts applied (the seat's actual task)

**EX-13 landed seven real patch texts** (one per stale row plus the Core
host-fallback row). This seat applied **all seven** on a fresh scratch root
carrying all three scoped files, from the current bytes:

| unit | before | after (EX-13's seven patches) |
|---|---|---|
| patches applied | — | **7/7**, every hunk balanced `-n/+n` |
| PROVINCE line count | 162 | **162** |
| PROVINCE sha256 | `d075a3c6…` | **`f951f161d8a7526ed0043eb41e9d92ee3b65b5c1dda51146e637aadd6d0ddcc5`** |
| census gate verdict | PASS exit 0 | **PASS exit 0** (0/0/0/0) |
| the six named stale phrases | all present | **all absent** (`grep -F`) |

Evidence: `evidence/ex13-run/` (`EX13-RUN.md`, `ex13-apply.log`,
`ex13-census-pass.txt`).

**Two defects in those texts, measured — neither visible to the census gate.**

**D1 — a non-line-neutral revision (since FIXED by EX-13).** The pe-wall patch
at sha `32f6052d92de6816` carried a `-6/+5` hunk: PROVINCE went **162 → 161
lines**, contradicting the patch's own text ("stays at 162 lines"). The census
still read **PASS**, because that bullet sits at 139–144, *below* the DATED
marker asserted at line 119 — the marker line does not shift, and the gate's only
line-count check (rows beyond the declared max end of 131) is far from firing.
**A line-count change below the last asserted marker is invisible to this
instrument.** EX-13 revised it to `-6/+6` (`1ce9b5a2a4017b54`); re-verified
line-neutral.

**D2 — the false Core promotion, repeated (since FIXED by EX-13).** On the
patched tree at that revision, `PROVINCE.md:92` read `(Core, r3-07) and real
solc-0.8.37 carriers (Core, arc3-r1)`. Re-derived by this seat: the r1 entry
states "RESULT-class exercise only — **no Core promotion**, no availability→
holding claim"; `grep -n arc3-r1 PROVINCE.md` found the string only on that
patched line; and `PROVINCE.md:75-76` requires a `LOG.md` entry for promotion,
which does not exist. This is the same defect the chain verdict sustained against
this seat's revision 1 — it recurred in the chain's own text. EX-13 revised the
patch (`66df2d6cf096f101`); re-derived on the final tree, `grep -n "Core,
arc3-r1"` returns **no match**.

**D2b — still open in the final bytes.** The EVM bullet still reads `vyper
bytecode untested`. That clause is stale against the wave tree (C1's r4 leg
measured 15/15 K/K on vyper-0.4.3 runtime) but its corpus entry is still only
staged, so it is not yet false against *admitted* corpus state. It must be
repaired in the same commit that lands C1's entry, or left with the dependency
named — the coupling this seat's v2 candidate encodes.

All three are recorded in `evidence/ex13-run/EX13-RUN.md` (including an addendum
with the before/after shas of both revised patches); the final re-run reads
**7/7 applied, 162 lines, census PASS**, after-sha
`dcfdb6a2fea6374caba5daf229b97c59ae4a69efa6ae14943909436e19eb81ca`.

## 4. Attacks / refutations attempted, with verdicts

The gate must be shown *load-bearing* before a PASS on it means anything, so the
instrument was attacked five ways plus one sabotage arm. Every arm was expected
to FAIL and every one did.

| # | attack (all on scratch copies) | expected | measured | verdict |
|---|---|---|---|---|
| 1 | false current claim in a CURRENT range (line 12: "Kimi is pinned at `rea-agents@6.4.0`") | FAIL | **PASS** — masked by the same-line inline marker "historical" (the census's named, unclosed **H2** class) | **arm refuted; H2 confirmed open** — recorded, not smoothed |
| 2 | stale pin in a CURRENT range (line 44: `Devin/OMP 6.3.0`) | FAIL stale=1 | `VERDICT: FAIL (stale=1)` exit 1 | holds |
| 3 | locus planted in an UNDECLARED range (line 92, `rea-agents@6.6.6`) | FAIL undeclared=1 | `VERDICT: FAIL (undeclared=1)` exit 1 | holds |
| 4 | PROVINCE truncated below the declared max end (G19) | FAIL `UNREADABLE` | `DECLARED FAIL CLASSES: ['UNREADABLE']` exit 1 | holds |
| 5 | needles stripped from SKILL.md (G20 blind floor) | FAIL `BLIND-INSTRUMENT` | `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` exit 1 | holds |
| 6 | DATED marker stripped (G15/G18) | SCOPE-ERROR | `["PROVINCE.md:45 marker '2026-10-13' absent from …"]` exit 1 | holds |
| 7 | **sabotage arm** — needle into the very line the C2 repair targets (line 91, `rea-agents@6.5.0`) | FAIL | `VERDICT: FAIL (undeclared=1)` exit 1 | holds |
| 8 | line-count-changing patch (the failure mode a careless same-line repair produces) | FAIL | `SCOPE-ERRORS: ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from ''"]` exit 1 | holds |

**Arm 1 is the honest negative.** The instrument cannot see a false current
claim that shares its physical line with an inline historical marker — this is
the pre-existing, already-named H2 residual
(`c1-census-v10.py` r9 provenance block: "Still named, NOT closed here: H2
same-line inline-marker excusal"), carried as debt in SCORECARD.md's round-3
record. A PASS from this instrument therefore certifies **locus hygiene and
anchor agreement, not claim truth**; the C2 chain's own evidence table is the
certificate for truth. Reported as a limitation of this seat's measurement, not
as a defect in the chain.

**Non-vacuity.** The PASS is not vacuous: the run detects 16 assertions across
three files (PROVINCE 6 loci / SCORECARD 9 / SKILL 2) and the G2 per-file floor
reads 17/14/3.

## 5. Blockers

**The primary blocker, stated plainly: no round-4 C2 patch text existed at the
time this seat ran.** The seat line requires applying ALL patches; there were
none to apply. What this seat did instead of stopping:

- built and verified the applier/runner against the *round-3* reference patch
  texts and against RV-4's applier (format parity measured, §1);
- proved the gate load-bearing with 8 arms (§4);
- established the two hard constraints a C2 PROVINCE patch must meet (§2);
- produced and fully measured a **demonstration** patch on the claim's own named
  debt, so a PASS-on-patched-input exists as evidence rather than a promise.

**What is NOT delivered, named explicitly:**

1. The chain's real patch texts were not applied — they do not exist yet. When
   they land, `bash harness/run.sh <label> <patch...>` reproduces the whole
   measurement in one command; the parent or any seat can run it.
2. The demo patch is **not** a proposal to land. It repairs only the solc half of
   the named bullet and is labelled a demo in its own header. If the parent
   adopts it, the vyper half must be adjudicated in the same commit — and if the
   round-4 C1 chain lands its Vyper leg, that half also goes stale, meaning the
   correct final wording depends on C1's outcome. **The C2 repair cannot be
   finalized before C1's Vyper result lands** — that is a genuine cross-chain
   dependency, not a scheduling excuse. **Measured at write time:** C1's Vyper
   leg has already *succeeded in the wave tree* — `CarrierV.vy` compiled with
   vyper `0.4.3+commit.bff19ea2` (`615f792c…`) and `inspect-evm-interface`
   recovered **15/15** selectors, `missing: none / extra: none`, across hex and
   raw at both the 6.4.0 and 6.7.0 pins (`ev_d1792f57…`;
   `claims/c1/EX-05/planted-vs-probe.txt`), with a second carrier
   (`Ex09Vault`, 7/7) and a `StewardToken` leg alongside — **but the corpus
   entry has not landed**: `corpus/knowledge/` is still 83 files and
   `corpus/README.md:38` still lists only the r1/r3 EVM entries. SC-1 has staged
   the entry as patch text for the parent
   (`claims/c1/records-drafts/knowledge-entry-draft.md`, proposed stem
   `2026-10-19-arc3-r4-evm-vyper-leg`), explicitly not applied. So the bullet's
   `vyper-compiled bytecode untested` clause is stale **against the wave tree**
   but not yet **against admitted corpus state** — and a C2 repair must track
   the latter. Repairing it now would assert what the corpus cannot yet back;
   leaving it is correct until C1's entry lands, at which point the same-line
   repair covers both clauses.
3. PROVINCE's Frontier/Adjacent region (lines 72–118) remains UNDECLARED in the
   census scope table. Any C2 repair that *must* carry a version needle there
   requires a same-commit scope re-key — a change to `.ufo/gates/c1-census-v10.py`,
   which is **chain c1's instrument and not this seat's to edit** (frozen rule;
   the r3 EX-31 precedent handled the same ownership boundary with a patch text).
   Flagged for the parent as a cross-chain coordination point.
4. Only the four bullets this seat could check against corpus state were checked.
   A full "every Frontier bullet and surface-summary claim" census is the C2
   authors' deliverable, not this seat's; this seat supplies the instrument that
   grades their result.

## 6. Identity discipline (rule #14)

Every identity below was re-derived after the final revision of the artifact it
describes; the artifact files' own digests are listed by the seat report, not
inside the files they hash.

| object | sha256 | how re-derived |
|---|---|---|
| census instrument | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | `sha256sum .ufo/gates/c1-census-v10.py` |
| PROVINCE.md (repo, before) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | `sha256sum PROVINCE.md` |
| SKILL.md (repo, before) | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | `sha256sum SKILL.md` |
| SCORECARD.md (repo, before) | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` | `sha256sum SCORECARD.md` |
| PROVINCE.md (demo, after) | `1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2` | `sha256sum` on the scratch root after apply |
| PROVINCE.md (complete candidate, after) | `dfa70b42b51dd45bd82bbf3037b707c0e1f10518ec9b0d5f68d72dbda652d27e` | re-derived on a fresh root, `harness/run.sh ex14-final` |
| `evidence/candidate-complete-frontier-repair.patch.md` | `8a0e12ffc8c48a809d60b06e7c13a4e93f3e1af131f08e9b7914fef86b06b1b2` | `sha256sum` |
| `evidence/candidate-complete-frontier-repair.v2.patch.md` (recommended) | `0b8ad045e19cee5a3120706853f9950bb90522b2ebaebb418db25f586c21d9a8` | `sha256sum` |
| PROVINCE.md (v2, after) | `69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5` | re-derived on a fresh root, `harness/run.sh v2b` |
| harness files | see §1 table | `sha256sum harness/*` |

The three repo-side scoped files were re-read at write time and still carry the
digests above, so the demo patch's search text is still applicable.

## 7. Files written by this seat

- `.ufo/waves/arc3-loop1-round4/seats/EX-14.md` — this report
- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-14/apply-and-census.md` — this artifact
- `claims/c2/EX-14/harness/{apply_patches.py,run.sh,preflight.py,discover.sh}`
- `claims/c2/EX-14/evidence/` — the census captures, control transcripts, the
  demo patch, the baseline/demo census JSONs, and the head identity receipt
