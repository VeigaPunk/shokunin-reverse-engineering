# RV-2 — c1: independent verification of PL-4's r10 frontier-claim register

Seat RV-2, chain c1, wave arc3-loop1-round6. Measured 2026-10-19 on this host.
Every number below was re-derived this session (rule #14); transcripts and the
seeder live under `RV-2/`, scratch was `/var/tmp/rv2-arc3r6/` (never `/tmp`).
Repo writes: **none** — the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus
and every tracked file were untouched; git was read-only
(`rev-parse`/`log`/`show`/`status`). The instrument ran only from scratch
copies, with `--root` pointed at scratch trees or the repo root (read-only).

## 0. Verdict

**PL-4's patch satisfies the frozen C1 falsifier.** It applies cleanly,
reproduces the claimed identity, reads PASS on the clean repo root, and FAILs
with a named disposition when the retracted `untested` literal is reintroduced
into `PROVINCE.md:91-93`, while v10 reads PASS blind on the same tree. Two
sentences in PL-4's *residual prose* are **CORRECTED** by measurement: a
one-line insertion inside `:132-162` is not caught (new-bullet admissions are
ungraded), and the "structural guard" on the pruned
bullets holds for replacement but not for additive reintroduction. Neither
correction touches the frozen claim; both narrow what the register may be said
to guarantee. A two-rule bullet-census guard that closes the first gap was
built and measured on scratch (`RV-2/r10-bulletcount-proposal.diff`), not
landed.

| Frozen item (`claims-frozen.md:30-53`) | Verdict | Where |
|---|---|---|
| Patch identity / applies to pristine gate | **REPRODUCED** | §2 |
| (a) extended instrument PASS on current tree | **REPRODUCED** | §3 |
| (b) seeded stale-literal reintroduction FAILs with named disposition | **REPRODUCED** | §4 |
| (c) every SCOPE row + every current counter intact | **REPRODUCED** | §3 |
| PL-4 §3 arm matrix | **REPRODUCED** (my own seeds) | §4 |
| PL-4 §6.1 "insertions inside :132-162 are caught" | **CORRECTED** | §5.1 |
| PL-4 §6.3 "pruned bullets guarded structurally by REQUIRED anchors" | **CORRECTED** (replacement-only) | §5.2 |
| "R4/R5 repairs clause-audited by hand, not instrument-graded" | operative half **REPRODUCED**; process **UNVERIFIABLE** | §1 item 7 |

## 1. First-hand re-derivations (the frozen "before" facts)

| # | Fact | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de57e045188b5ce8cd450a57b349f90785`; `git log --oneline -3` shows `c625d5d … (measured at work commit 58c3db7)` directly above `58c3db7` | VERIFIED |
| 2 | Instrument path/size | `sha256sum .ufo/gates/c1-census-v10.py` → `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`; `wc -l` → 610 | VERIFIED |
| 3 | SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | `grep -nE 'PROVINCE\.md", *[0-9]+, *[0-9]+'` → exactly those 7 rows at gate `:216-222`; table `SCOPE = [` at `:215`, close `]` at `:237` | VERIFIED |
| 4 | Frontier 73-93 + 133-162 UNDECLARED | no row covers either range (grep above); programmatic coverage with the imported gate → `[]` for both. Headers: `:73 ## Frontier`, `:133 ### Round-4 frontier (post-unlock)`; file 162 lines | VERIFIED |
| 5 | v10 reads PASS "whether or not those bullets are stale" | v10 on every stale/truncated tree in §4 reads PASS exit 0 (the one exception, `seeded-insert-one-evm`, deliberately shifts a DATED marker and fails on the existing G15 machinery, not on the frontier). Direct `classify()` enumeration: all 24 PROVINCE assertion entries (16 distinct lines) are outside 73-93/133-162 — the two regions produce **zero locus lines**, because `classify()` `continue`s on no `REA_GATE` match (`:406-407`) and on no PIN/VER/PTR occurrence (`:419-420`) | REPRODUCED |
| 6 | v10 baseline PASS at HEAD | repo-root run: `live anchors {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`; `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696 loci=9`, `SKILL.md lines=390 loci=2`; `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 | REPRODUCED |
| 7 | R4/R5 repairs were hand-audited, not instrument-graded | operative half re-measured (items 4-5); the historical by-hand process itself is not derivable from artifacts | PARTLY (process UNVERIFIABLE) |
| 8 | Stale literal is a measured historical before-state | `git show 40de383^:PROVINCE.md` → `:92 (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay`; `git merge-base --is-ancestor 40de383 HEAD` → true. The FORBIDDEN pattern is earned, not invented | VERIFIED |

Custody note: `git status --porcelain` also shows a **pre-existing** tracked
modification `.ufo/waves/arc2-loop1-round10/C3.md` (untracked wave tree
`?? .ufo/waves/arc3-loop1-round6/` is this wave). That modification is not mine
and predates this seat; a landing commit must not sweep it in.

## 2. Patch identity (REPRODUCED)

Pristine copy → `patch` → identity:

```
sha256sum .ufo/gates/c1-census-v10.py        d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5
sha256sum PL-4/patch-v10-to-r10.diff         3f94355cfe747c10c968c2382004ab1e95792518eba2f03ae99df2f7f16a6513  (10,584 B)
cp pristine gate → scratch/rebuilt.py; patch rebuilt.py < patch.diff
                                             exit 0, no fuzz/offset messages
sha256sum rebuilt.py                          8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca
wc -l rebuilt.py                              713
cmp rebuilt.py PL-4/c1-census-v10-r10.py      identical
```

- The diff block quoted inside `PL-4.md:119-302` is **byte-identical** to
  `PL-4/patch-v10-to-r10.diff` (extracted programmatically: 10,584 B both,
  exact string equality).
- `SCOPE` loaded from pristine vs r10 with `importlib` → **identical objects**,
  20 rows both sides. The patch contains no `-`/`+` line inside the SCOPE
  table (its first hunk inserts after the closing `]`); the only bounds change
  is the `max_end` line at v10 `:516` → r10 `:611-612`, which now also covers
  register rows (fail-closed for truncation, see §4).
- New machinery in r10: `FRONTIER` table at `:291` (14 rows),
  `frontier_check()` at `:421`, call at `:630`, class selection at `:664-667`.
  Revision block cites pre-edit sha `d0772ce8…`; in-place (not a v11 fork),
  rationale recorded at `PL-4.md:45-64`.

## 3. Requirement (a) PASS on the current tree, and (c) counter integrity

Repo root, both instruments, `--json` (full outputs `RV-2/v10-repo.json`,
`RV-2/r10-repo.json`):

```
v10 exit 0, verdict PASS
r10 exit 0, verdict PASS
counts equal: True  {'PROVINCE.md': {'lines': 162, 'loci': 6},
                     'SCORECARD.md': {'lines': 1696, 'loci': 9},
                     'SKILL.md': {'lines': 390, 'loci': 2}}
current_ok_per_file equal: True  {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
shared keys: 17 | r10-only: ['frontier_errors', 'frontier_rows'] | v10-only: []
shared mismatches: []
frontier_rows: 14 | frontier_errors: [] | declared_fail_classes: []
```

Requirement (c) therefore holds in the strongest available sense: every
pre-existing `--json` key is present and equal (17/17), only two additive keys
appear, and no counter changes value. Text mode differs by exactly one line:

```
6a7
> FRONTIER register (G21): 14 rows asserted, errors: []
```

The `VERDICT:` line is byte-identical (`v10-repo.txt:12`, `r10-repo.txt:13`).
A clean scratch tree (byte copies of the three scoped files, PROVINCE
`11a5c604…`) reproduces the same PASS/`[]` result, so (a) is not a repo-root
artifact.

## 4. Requirement (b): independent seeded-fault matrix

Trees were built by this seat (`RV-2/seed_rv2.py`, every edit asserted on
content; no reuse of PL-4's `seed.py`). All trees hold byte-copies of
PROVINCE.md/SKILL.md/SCORECARD.md; edits are line-count neutral except where
stated. Full transcript: `RV-2/verification-transcript.txt` §5.

| tree | seed | v10 | r10 (PL-4) | r10 classes |
|---|---|---|---|---|
| clean | none | 0 PASS | 0 PASS | `[]` |
| seeded-forbidden | `:91-93` → retracted literal, earning anchors removed | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` |
| seeded-forbidden-only | anchors kept, only `untested` added | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` (exactly 1 error) |
| seeded-forbidden-case | anchors kept, `UnTeStEd` | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` (case-insensitive) |
| seeded-required-evm | `:91-93` → "see corpus", anchors stripped | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| seeded-required-riscv | `:137` `r5-01` removed | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| clean-truncated | PROVINCE → 161 lines | 0 PASS | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |
| benign-edit | word added inside `:137`, anchors kept | 0 PASS | 0 PASS | `[]` |
| seeded-insert-one | one new bullet at `:135` (see §5.1) | 0 PASS | **0 PASS** | `[]` |
| seeded-stale-new-bullet | stale bullet inserted at `:135` (see §5.1) | 0 PASS | **0 PASS** | `[]` |
| seeded-insert-two | two new bullets at `:135` | 0 PASS | 1 FAIL | `['FRONTIER-UNEVALUABLE']` |
| seeded-insert-one-evm | one bullet inserted above `:119` | 1 FAIL | 1 FAIL | `['FRONTIER-UNEVALUABLE']` (v10 fails on the DATED marker — PL-4's "above :119" sentence confirmed) |
| seeded-append-163 | new bullet past `:162` | 0 PASS | 0 PASS | `[]` (PL-4's named past-the-bound residual, confirmed) |
| seeded-replace-crossversion-old | `:157-160` → measured pre-r5 text | 0 PASS | 1 FAIL | `['FRONTIER-UNEVALUABLE']` |
| seeded-stale-clause-crossversion | stale clause added, anchors kept (see §5.2) | 0 PASS | **0 PASS** | `[]` |

Key r10 error lines (verbatim):

```
seeded-forbidden:      PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register)
                       PROVINCE.md:91-93 REQUIRED 'vyper-0\.4\.3' absent (G21 frontier register)
                       PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
seeded-forbidden-only: PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
seeded-required-evm:   PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent … (×2 incl. vyper)
seeded-required-riscv: PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
clean-truncated:       UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
                       + 14 × "PROVINCE.md:<s>-<e> frontier uncheckable (file unreadable)"
```

The frozen falsifier's exact example — the retracted literal back into `:91-93`
— is caught on a scratch tree while the clean tree reads PASS (measured twice:
repo root and clean scratch). Requirement (b) is satisfied.

Register coverage is complete for existing bullets: the two regions hold 13
bullets, at starts `[82,84,87,89,91]` and `[135,139,145,147,149,151,157,161]`;
PL-4's 14 rows cover all 13 plus the intro `:75-80`. Every REQUIRED pattern
matches its span and no FORBIDDEN pattern fires on the clean tree (measured
row-by-row with `re.search`, §5 transcript before the matrix).

## 5. Measured corrections to PL-4's residual prose

### 5.1 §6.1 "insertions inside :132-162 are caught" — CORRECTED

`PL-4.md:330-333` states: "Insertions anywhere inside `:73-162` are caught …
inside `:132-162` they shift register spans (REQUIRED-absent — measured via the
seeded arms)." Measured false for a **one-line** insertion:

- `seeded-insert-one`: a new bullet line inserted after `:134` (file 163
  lines) → v10 PASS, **r10 PASS**, `frontier_errors: []`.
- `seeded-stale-new-bullet`: the pre-r5 stale bullet text
  `- **Managed PE/CLI** — pre-round-4 stale bullet, real PE untested.`
  inserted at `:135` → v10 PASS, **r10 PASS**, `frontier_errors: []`.
- Two-line insertion (`seeded-insert-two`) → FAIL
  `['FRONTIER-UNEVALUABLE']`; so the boundary is one line of shift, not zero.

Mechanism: all register windows start at a bullet's first line and end at its
last; a one-line insertion shifts the whole bullet, so the REQUIRED anchors
still fall inside the shifted window. An anchor would be evicted only if it sat
exclusively on a span's last line; no register row has that shape (for example
`:161-162`'s anchors sit on `:161`, which shifts to `:162` and stays inside).
The inserted bullet itself is never asserted: the register is a positive floor
plus a short FORBIDDEN list, not an admission check.

Why it matters: a new unearned frontier claim can be added with a one-line
insertion and the instrument reads PASS. This is a narrower hole than the one
closed (a *reintroduced retracted literal* is caught), but `PL-4.md:330-333`
overstates the guarantee. The frozen C1 falsifier does not require covering
this class.

**Proposed fix (measured, not landed):** declare the bullet census of each
region and fail on drift. `RV-2/r10-bulletcount-proposal.diff` adds:

```
REGION_BULLETS = [("PROVINCE.md", 73, 93, 5), ("PROVINCE.md", 133, 162, 8)]
```

and, inside `frontier_check()`, compares `sum(1 for ln in lines[s-1:e] if
re.match(r"^- ", ln))` with the declared count, appending
`FRONTIER-UNREGISTERED-BULLET` to `frontier_errors`. Measured on all 15 trees:

| tree | r10 | r10 + census |
|---|---|---|
| clean, benign-edit, append-163, the seeded-forbidden/required/truncated arms | unchanged | unchanged |
| seeded-insert-one | PASS | **FAIL** `:133-162 bullet census 9 != declared 8` |
| seeded-stale-new-bullet | PASS | **FAIL** same class |
| seeded-insert-one-evm | FAIL | FAIL (both; census `:73-93 6 != 5`) |
| repo root | PASS | PASS, `frontier_errors []`, counts equal to v10 |

The guard adds no false positive on a benign in-bullet edit and leaves the
past-the-bound append residual (which PL-4 names) unchanged.

### 5.2 §6.3 "pruned bullets guarded structurally by their REQUIRED anchors" — CORRECTED

`PL-4.md:337-341` says the six pruned pre-round-4 bullets are guarded
structurally by REQUIRED anchors rather than FORBIDDEN patterns. Measured:

- **Replacement** is caught: `seeded-replace-crossversion-old` restores the
  measured pre-r5 `:157-160` text (`git show 40de383^:PROVINCE.md:157-160`) →
  r10 FAIL `REQUIRED 'r12-02|r14-01' absent (FRONTIER-UNEVALUABLE)`.
- **Additive reintroduction** is not: `seeded-stale-clause-crossversion` keeps
  the earning anchors and adds the stale clause "still probe-refused since r2;
  multi-version pacman pairs beyond expac unexercised" → r10 **PASS**,
  `frontier_errors []`.

So "structurally guarded" is true for replacement, false for addition. This is
consistent with PL-4's own "earned, not exhaustive" caveat, but the sentence
should say replacement-only. Only `:91-93` carries a FORBIDDEN literal, so an
additive stale clause elsewhere is ungraded by design. The bullet-census guard
in §5.1 does not close this class either (it is not a bullet-count change).

Minor, no measurement impact: the gate provenance block at
`PL-4/c1-census-v10-r10.py:109` says the run gains "one counter
(`frontier_errors`)", while `--json` also adds `frontier_rows` (a register size,
not a counter). Cosmetic.

## 6. Reconciliation with peer c1 artifacts

- **PL-4** (`claims/c1/PL-4.md`) is the artifact my brief names as delivered;
  this seat verifies it end-to-end above. Verdict: **VERIFIED with 2
  corrections**, frozen falsifier satisfied.
- **PL-2** (`claims/c1/PL-2.md`) proposes a *different* r10: two SCOPE rows
  classed `FRONTIER`, a three-entry cited `FRONTIER_STALE` register, and a
  widened marker guard; it also changes the `VERDICT:` line (`frontier=%d`).
  I did not verify it — it is not the artifact my chain was asked to check, and
  only one such patch can land. Its different requirement-(c) surface (a
  changed verdict line) is worth the landing seat's attention if PL-2 is
  preferred.
- **RV-3** (`claims/c1/RV-3.md`, rewritten concurrently at 13:59) is an
  independent verification of PL-4 and reports the same insertion-class
  correction; that is convergence, not evidence, and no number here is taken
  from it. Its *prior* competing register design is preserved verbatim at
  `claims/c1/RV-3/prior-attempt.md`; I extracted that patch on scratch
  (`RV-2/rv3-patch.diff`), it applies cleanly and reproduces
  `8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`
  (712 lines, 13 rows). Measured: clean PASS; `seeded-insert-one` and
  `seeded-stale-new-bullet` **FAIL** with `FRONTIER-ANCHOR … anchor absent`;
  `seeded-forbidden-only` FAIL `FRONTIER-STALE`; truncation FAIL. Its per-row
  `anchor_line` assertion closes the §5.1 gap by construction.
- Recommendation: land at most one c1 patch. If PL-4's is chosen, either accept
  the two corrected residuals explicitly or append the measured two-rule
  bullet-census guard (`RV-2/r10-bulletcount-proposal.diff`, applies on top of
  PL-4's r10). If an anchored-row scheme is preferred instead, RV-3's prior
  design is the measured alternative; I did not audit its citations or its
  requirement-(c) invariance beyond the runs above.

## 7. Per-item verdicts on the frozen C1 text

| Frozen statement | Verdict | Evidence |
|---|---|---|
| SCOPE covers PROVINCE only at the seven listed ranges | VERIFIED | §1 item 3 |
| Frontier 73-93 + 133-162 UNDECLARED | VERIFIED | §1 item 4 |
| Instrument reads PASS identically with stale frontier bullets | REPRODUCED | §1 item 5, §4 |
| Claim: extend so frontier staleness is gradable | VERIFIED as implemented (register option b, in-place r10) | §2 |
| (a) still PASS on current tree | REPRODUCED | §3 |
| (b) FAIL/named disposition on seeded stale literal | REPRODUCED | §4 |
| (c) every SCOPE row + current counter intact | REPRODUCED | §3 |
| Record v11-vs-in-place and why | VERIFIED (in-place; rationale at `PL-4.md:45-64`) | §2 |
| Falsifiable: "grep SCOPE → none" before; seeded catch + clean PASS after | REPRODUCED | §1 item 4, §4 |
| R4/R5 hand audit, not instrument-graded | operative half REPRODUCED; process UNVERIFIABLE | §1 item 7 |

## 8. What I did not do

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, or any
  tracked file; did not land the patch. All instrument runs were scratch copies.
- Did not verify PL-2's patch or any c2/c3 artifact (outside this chain).
- Did not re-derive the historical by-hand R4/R5 audit process (not derivable).
- Did not audit RV-3's corpus citations; the RV-3 prior-design runs above are a
  design cross-check, not an endorsement of that patch.

## 9. Landing recipe for the parent

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet
  # expect exit 0, PASS, "FRONTIER register (G21): 14 rows asserted, errors: []"
```

Optional, only if the §5.1 gap is to be closed now: apply
`RV-2/r10-bulletcount-proposal.diff` **after** PL-4's patch (scratch-measured:
clean PASS; inserted-bullet arms FAIL; original arms unchanged). Record
post-edit identity in the landing receipt, not in the gate (PL-4's own rule
#14 discipline). Do not sweep the pre-existing
`.ufo/waves/arc2-loop1-round10/C3.md` modification into the landing commit.

## 10. Evidence inventory (`RV-2/`)

| file | sha256 | what it is |
|---|---|---|
| `verification-transcript.txt` | `382ccdfd…` | full rerunnable transcript: custody, patch identity, key comparison, classify() enumeration, 15-tree matrix, bullet census, git provenance, RV-3 cross-check |
| `verify.sh` | `ba5ff242…` | regenerates the transcript from scratch |
| `seed_rv2.py` | `960c5cdf…` | independent seeder (content-asserted edits, line counts) |
| `r10-bulletcount-proposal.diff` | `062b92ee…` | §5.1 guard, applies on top of PL-4's r10 |
| `v10-repo.json` / `r10-repo.json` | `10ad3788…` / `14178f7e…` | repo-root JSON, key-equality evidence |
| `bc-repo.json` | `14178f7e…` | guard variant on repo root (identical JSON to r10 on the clean tree) |
| `rv3-patch.diff` | `c9ab162e…` | RV-3 prior-design patch extracted from `claims/c1/RV-3/prior-attempt.md` |
| `MANIFEST.sha256` | — | hashes of the above (regenerate with `sha256sum` over the listed files) |
