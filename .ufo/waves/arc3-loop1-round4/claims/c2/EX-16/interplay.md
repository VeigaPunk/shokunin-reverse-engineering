# EX-16 — interplay: citation-drift probe vs the drafted repairs (arc3-loop1-round4, chain c2)

Seat EX-16 · chain c2 · role executor · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40`. Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback dispatch recorded in
`claims-frozen.md:11-15`. No git mutation; custody paths never opened (the
custody-tool and README reads here are `sha256sum`/`read` only, and the one
custody-README mutation ran on a `/var/tmp` clone). Scratch under `/var/tmp/ex16`
(never `/tmp`).

## 1. Task and headline

Task: run the citation-drift probe at HEAD (findings=0 both modes) and check that
none of the drafted patch texts' target lines are probe-needled in a way the
repairs would stale. The seat line's parenthetical — *"the table pins some
custody-readme anchors, not PROVINCE lines — verify"* — is **half wrong**, and
the half that is wrong is the load-bearing one.

- **The custody-readme half is right, and stronger than stated.** All four
  `custody-readme-*` entries are `kind: anchor` and **no entry in the table
  carries a `pin_line` at all** (`pointer-table.json`, 57 entries + 5 quoted).
  A README repair cannot move a pinned line because no README line is pinned.
- **The PROVINCE half is false.** `PROVINCE.md` carries **two `exact`
  line-pinned entries at line 18** — `prov18-stamp-named` (`17:55:49Z receipt`)
  and `prov18-pin-value` (`rea-agents@6\.7\.0`) — plus a third entry that grades
  PROVINCE by range (`shonen-province-range`, extracted from `SHONEN.md:12`,
  range `88-116`, needle "Quality/safety verdicts on findings" at line 114).

Verdict: **no drafted repair stales a needle as written**, but two of the three
PROVINCE-side constraints are one edit away from reddening, and the census
instrument binds *tighter* than the probe on PROVINCE edits.

## 2. Probe at HEAD (the first half of the task)

`probe-head-both-modes.txt` (this seat's dir) — run from the repo root:

```
CITATION_DRIFT_VERDICT: reported findings=0 exit=0      (default mode)
CITATION_DRIFT_VERDICT: clean findings=0 exit=0         (--strict)
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

Frozen-run preflight holds: `pointer-table.json` sha256
`1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` == the
`pointer_table.sha256` pinned in `expected.json`. Identities at HEAD:
`head-identities.txt`.

## 3. Which needles touch which repair target

| repair target | needle(s) that grade it | kind | line-pinned? |
|---|---|---|---|
| `PROVINCE.md` line 18 | `prov18-stamp-named`, `prov18-pin-value` | exact | **yes — line 18, twice** |
| `PROVINCE.md` lines 88-116 | `shonen-province-range` (via `SHONEN.md:12`) | extracted range | range end 116 is the binding value |
| `PROVINCE.md` line 18 chain | `prov18-receipt-exists` | exact | pins the receipt file, not PROVINCE |
| `.ufo/gates/custody-pair/README.md` | `custody-readme-{v2-fieldset,rewrite-identity,precedence,scratch-never-tmp}` | anchor | **no** (content anywhere) |
| `.ufo/gates/custody-pair/custody-pair.py` | **nothing** | — | the tool is not in the table |
| `SKILL.md` custody row | `skill-registry-custody-pair-row` | anchor | no (deliberately, rule #11) |

## 4. Battery — measured before → after per mutation

`interplay-battery.txt` (this seat's dir), re-runnable harness
`interplay-battery.py`. Every case: fresh `/var/tmp` clone → one mutation →
commit in the clone → grade **both** instruments. Line counts are
`wc -l`-equivalent (HEAD PROVINCE = 162 lines).

| case | PROVINCE lines | probe (`--strict`) | census |
|---|---|---|---|
| base (no mutation) | 162 | clean 0/0 | PASS |
| insert +2 lines below the Frontier bullets | 164 | **clean 0/0** | **FAIL** — `:119 marker 'verified 2026-10-13' absent` |
| insert +3 lines below the Frontier bullets | 165 | **FAIL** 1 — `citation_dead shonen-province-range` | FAIL — same marker |
| insert +1 line above line 18 | 163 | **FAIL** 2 — `prov18-pin-value`, `prov18-stamp-named` | FAIL — `:40` + `:119` markers |
| insert +1 line above line 119 (below Frontier) | 163 | clean 0/0 | FAIL — `:119` marker |
| insert +1 line at EOF (below the declared max end) | 163 | clean 0/0 | **PASS** |
| Surface-summary line rewritten, line count held | 162 | clean 0/0 | PASS |
| Surface-summary paragraph grown by +1 line | 163 | **FAIL** 2 — both `prov18-*` | FAIL — `:40` + `:119` markers |
| Frontier EVM bullet rewritten, line count held | 162 | clean 0/0 | PASS |
| custody README: drop `never \`/tmp\`` | 162 | **FAIL** 1 — `custody-readme-scratch-never-tmp` | PASS |
| custody README: drop the precedence sentence | 162 | **FAIL** 1 — `custody-readme-precedence` | PASS |
| custody README: `MTIME_UTC_RENDER` → `MTIME_UTC` | 162 | **FAIL** 1 — `custody-readme-v2-fieldset` | PASS |
| custody README: drop the rewrite-identity clause | 162 | **FAIL** 1 — `custody-readme-rewrite-identity` | PASS |

Four consequences, each measured rather than argued:

1. **Every custody-readme anchor has teeth.** Neutering any one of the four
   reddens exactly its own entry. The README is not defensively pinned by
   accident — the anchors are load-bearing.
2. **The census binds tighter than the probe on PROVINCE.** +1 line anywhere
   above line 119 already fails the census (`:119 marker 'verified 2026-10-13'`
   is a DATED-row marker assertion) while the probe still reads clean at +2.
   The probe's own PROVINCE failure needs **+3**.
3. **The probe's PROVINCE failure mode is positional, not semantic.** +1 above
   line 18 reddens the two `exact` entries; +1 above line 119 does not. The
   line-18 pin is what makes an "insert a line at the top of the drift-prone
   paragraph" repair fatal.
4. **Growth below the declared max end is free.** The EOF insert passes both
   instruments — but that is not a licence to grow PROVINCE, because the frozen
   C2 claim independently requires the line count unchanged.

The +3 boundary is exact and explained: `SHONEN.md:12` asserts
`PROVINCE.md:88-116`, the safety-refusal clause sits at line 114, so the range
end tolerates +2 lines of growth below the Frontier region and fails at +3.

## 5. The drafted patch texts, applied and graded

| patch text | target | applied? | probe | census |
|---|---|---|---|---|
| `arc3-loop1-round4/claims/c2/EX-14/evidence/demo-frontier-repair.patch.md` | `PROVINCE.md` Frontier EVM bullet | **yes** (RV-4's `prose-apply.py`, rc 0; 2−/2+; 162→162 lines; sha `1bfb5dd7…`) | clean 0/0 | PASS |
| `arc3-loop1-round4/claims/c3/EX-26/evidence/ruling-block.txt` (+29 lines before `## Exit codes (declared)`) | custody README | **yes** (verbatim, anchor asserted unique; 185→214 lines; sha `f54d9467…`) | clean 0/0 both modes | n/a (README not census-scoped) |
| `arc3-loop1-round3/claims/c2/EX-30/readme.patch.md` | custody README | **no — stale base** | — | — |
| `arc3-loop1-round3/claims/c2/CR-3/typeswap-declarations.patch.md` | README + tool | not applied (its own header says "do not apply" against `f30df42e`) | — | — |

**The EX-14 draft is needle-safe and census-safe as written.** It is the shape
every C2 PROVINCE repair must take: rewrite in place, line count held, no version
needle introduced into the undeclared Frontier region.

**EX-30's r3 README patch is superseded, and this is a live landing hazard.**
Its header declares base `fa484d57…` (132 lines) → patched `42b07ee5…`. The
README landed in place during r3 at `f30df42e…` (185 lines) and EX-21 has since
revised it further in this wave. Applied against current bytes it fails:
`hunk 1 [.ufo/gates/custody-pair/README.md]: FAILED — search text not found
verbatim`. RV-8's own r3 review had already flagged its two text gaps; the base
staleness is the third reason it must not be the text the parent applies. The
r4 README text is EX-26's ruling block (measured above) or EX-21's in-place
revision.

**CR-3's precedence edit preserves its own anchor.** Its `-`/`+` pair both begin
`Severity precedence for the verdict of a \`verify\` run: \`CONTENT-DRIFT\` >` —
the anchor phrase survives the rewrite verbatim, which is exactly the property
`custody-readme-precedence` requires.

## 6. The live EX-21 revision (graded mid-flight)

EX-21 (C3's authorized writer) was revising `.ufo/gates/custody-pair/` while this
seat measured. The worktree README moved `f30df42e…` (185 lines) →
`125e7e02…` (267 lines) and the tool `7cd19c3c…` → `29bb45ae…` during this
window. Graded on a `/var/tmp` clone carrying those bytes:

```
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

with the four anchors present (`MTIME_UTC_RENDER` ×2, the other three ×1) and
the new `## The both-absent \`MATCH\` (ruling, arc3-loop1-round4)` section at
line 151 — i.e. EX-26's ruling content has landed in substance, and the
`## Exit codes (declared)` heading survives at line 182. **This is a snapshot of
a file under active revision, not a settled identity**: the parent must re-derive
the README sha and re-run the probe at the landing commit. The needle-safety
conclusion is revision-independent for the README (anchors, no line pins) but
the digest in any receipt must be re-derived.

## 7. Attacks / refutations attempted, with verdicts

| # | attack | expected | measured | verdict |
|---|---|---|---|---|
| 1 | probe is vacuously clean (no needle can redden) | one redden per neutered anchor | each of the 4 README anchors reddens its own entry; PROVINCE pins redden on a 1-line shift | **refuted** — the table has teeth |
| 2 | parenthetical: "not PROVINCE lines" | no line pins on PROVINCE | two `exact` entries at `PROVINCE.md:18` | **parenthetical falsified** |
| 3 | a same-line PROVINCE repair stales a needle | reddens | clean 0/0 (EX-14's shape, applied and graded) | refuted — same-line repairs are safe |
| 4 | the census is the only PROVINCE constraint | probe tolerates what census does | probe fails at +3, census fails at +1 above line 119 | **refuted** — both bind, census first |
| 5 | README repairs are line-coupled | a +29-line insert reddens | clean 0/0; and no entry anywhere carries a `pin_line` | refuted |
| 6 | EX-30's r3 README patch is still applicable | applies cleanly | `FAILED — search text not found verbatim` (base `fa484d57` vs live bytes) | **confirmed stale** |
| 7 | table digest is unpinned / stale | `pointer_table_tampered` or `_unpinned` | sha256 == pinned digest; preflight passes | refuted |

## 8. Blockers

- **No round-4 C2 patch text existed when this seat ran.** `claims/c2/EX-11/`
  (planner) and the sibling executor dirs are empty; the only r4 PROVINCE-side
  artifact is EX-14's *demo* patch, which EX-14 itself labels a demonstration and
  explicitly says must not be landed as-is (its vyper half depends on C1's
  outcome). This seat graded that demo plus C3's EX-26 ruling and the r3
  residuals; when the real C2 texts land, `interplay-battery.py` re-grades them
  in one command.
- **The census's binding constraint is not in the probe's contract.** The
  census's DATED-row marker at `PROVINCE.md:119` fails at +1 line while the
  probe tolerates +2. A repair validated only against the probe can still fail
  the census; the round's landing check must run both.
- **The custody README/tool were under active revision during measurement.**
  Every identity this seat records for them is a snapshot; re-derive at landing.

## 9. Identity discipline (rule #14)

All digests re-derived at write time unless marked a snapshot.

| object | sha256 | note |
|---|---|---|
| `HEAD` | `015e1bab914713568f339fd53999bc180459cc40` | `git rev-parse HEAD` |
| `pointer-table.json` | `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` | == pinned |
| `expected.json` | `9df0452c5c132ad00e211781ebccc332de9b1aa1af7eeb50c91bcb0ed2015763` | |
| `citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` | |
| `PROVINCE.md` | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | 162 lines |
| `SHONEN.md` | `3edb044cf1e7742ab47cbdeb88c2aee29daf4f93a2240e615a9226dcff69e99b` | |
| `SKILL.md` | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | 390 lines |
| `SCORECARD.md` | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` | |
| `.ufo/gates/c1-census-v10.py` | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | |
| custody README (r3 landed) | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` | 185 lines |
| custody README (EX-26 block applied on clone) | `f54d9467030bb250f85f11f18d8575e7eec9082ab76610de9681bf0fef847e10` | 214 lines |
| custody README (live worktree, **snapshot**) | `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186` | 267 lines; moved during measurement |
| `custody-pair.py` (live worktree, **snapshot**) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` | moved from `7cd19c3c…` during measurement |
| EX-14 demo patch | `507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51` | per EX-14's own receipt |
| EX-26 ruling block | `8e0a88ee293209da05529ba73c9f55e62232a2d9877cd2507be94a4f8de4fe77` | 1,834 B; re-derived here |

## 10. Files written by this seat

- `.ufo/waves/arc3-loop1-round4/seats/EX-16.md` — seat report
- `.ufo/waves/arc3-loop1-round4/claims/c2/EX-16/interplay.md` — this artifact
- `claims/c2/EX-16/evidence/probe-head-both-modes.txt` — the three HEAD runs
- `claims/c2/EX-16/evidence/head-identities.txt` — HEAD + sha256 roster
- `claims/c2/EX-16/evidence/interplay-battery.txt` — the battery transcript
- `claims/c2/EX-16/interplay-battery.py` — the re-runnable battery harness
