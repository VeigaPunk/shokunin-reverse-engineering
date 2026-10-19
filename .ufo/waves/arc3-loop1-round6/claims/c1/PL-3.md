# PL-3 — c1 (census instrument): independent verification of PL-4's r10 G21 frontier register

Seat PL-3, chain c1, wave arc3-loop1-round6, 2026-10-19. Repo HEAD measured at
this seat's start and end: `c625d5de57e045188b5ce8cd450a57b349f90785` (records;
work `58c3db7` two entries below). Scratch: `/var/tmp/pl3-arc3r6/` (never
`/tmp`). Gate custody: `.ufo/gates/c1-census-v10.py` sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, 610
lines, unchanged before and after every measurement below. No tracked file,
gate, PROVINCE/SKILL/SCORECARD, corpus, or peer artifact was modified; git was
read-only (`rev-parse`, `log`, `status`, `show`). Every number below was
re-derived first-hand this session (rule #14); peer artifacts appear only in
the point-in-time landscape section, never as evidence.

## 0. Verdict

PL-4's r10 patch **satisfies the frozen C1 claim (a)/(b)/(c)** and the frozen
falsifiable under my own scratch trees and arms. The patch round-trips
byte-exactly to the claimed identity. I record **two corrections** to the
artifact's own residual claims — not to the frozen requirement:

- **C-1 (CORRECTED):** `PL-4.md:330-333` says insertions inside `:132-162`
  "shift register spans (REQUIRED-absent — measured via the seeded arms)". A
  one-line insertion at **every** point after `:119` is absorbed: 44/44
  insertion points `120-163` read PASS under r10.
- **C-2 (CORRECTED / limitation):** the register declares one FORBIDDEN
  literal (`untested`, row `91-93`). Anchor-preserving reintroductions of the
  other two `40de383` retractions (PE wall, cross-version) pass both v10 and
  r10; only their anchor-stripping full replacements fail (`REQUIRED` absent).

The frozen claim's own wording is met: (b) requires a *declared*-stale
literal, and the declared EVM literal is caught in three independent seed
forms. C-1 and C-2 are completeness/robustness gaps against the R1 goal
("make the repaired Frontier claims gradable"), not failures of (a)/(b)/(c).

| Frozen item | Verdict |
|---|---|
| (a) extended instrument still PASS on the current tree | **REPRODUCED** — real repo and byte-identical clean scratch, exit 0 |
| (b) seeded reintroduction FAILs with a named disposition | **REPRODUCED** — 5 independent seed classes, named classes `FRONTIER-STALE` / `FRONTIER-UNEVALUABLE` |
| (c) every existing SCOPE row and counter intact | **REPRODUCED** — 20/20 SCOPE rows identical, 17/17 shared JSON keys equal |
| Patch identity `80027570…`, 713 lines | **REPRODUCED** — zero-fuzz apply, `cmp` identical to PL-4's built copy |

## 1. Before-state, re-derived first-hand

Commands and captures: `evidence/versions.txt`, `evidence/scope-coverage.txt`,
`evidence/premise-scan.txt`, `evidence/json-v10-repo.json`.

| # | Fact | Measurement | Verdict |
|---|---|---|---|
| 1 | HEAD `c625d5d`, work `58c3db7` | `git rev-parse HEAD` → `c625d5de…f90785`; `git log --oneline -3` → `c625d5d … (measured at work commit 58c3db7)` / `58c3db7 …` | REPRODUCED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce8…97b5`; `wc -l` → 610 | REPRODUCED |
| 3 | PROVINCE SCOPE rows only `8-13, 15-26, 40-43, 44, 45-62, 64-71, 119-131` | module import of the gate: exactly `[(8,13,CURRENT),(15,26,CURRENT),(40,43,DATED@40),(44,44,CURRENT),(45,62,DATED@45),(64,71,CURRENT),(119,131,DATED@119)]` | VERIFIED |
| 4 | Frontier `73-93` + `133-162` UNDECLARED | zero covering rows for either range; 21 and 30 uncovered lines respectively (`scope-coverage.txt`) | VERIFIED |
| 5 | Frontier bullets are locus-free | direct scan of lines `73-93 + 133-162`: PIN **NONE**, VER **NONE**, PTR **NONE**, REA_GATE-bearing lines **NONE** (`premise-scan.txt`). The only PROVINCE VER hit is `:125` inside the DATED table; REA_GATE hits at `:103/:106/:109` are in Adjacent. This is why a SCOPE row alone could never fire: `classify()` continues before `scope_of()` when a unit has no occurrence (gate `:403-420`). | VERIFIED |
| 6 | v10 reads PASS identically on stale Frontier text | v10 PASS exit 0 on the repo and on the frozen-literal tree; the two `--json` documents have **equal key sets and zero differing keys**, identical counts (`PROVINCE 162 lines/6 loci`, `SCORECARD 1696/9`, `SKILL 390/2`) | REPRODUCED |
| 7 | v10 reads PASS on a 161-line PROVINCE | v10 exit 0 on `trunc161`; new blind-spot evidence beyond the frozen example (silent loss of the whole post-unlock region past SCOPE's max end 131) | REPRODUCED |
| 8 | "R4/R5 repairs clause-audited by hand" process claim | the operative half is item 4/5 (region ungraded); the historical by-hand audit itself is not re-derivable from artifacts | PARTLY — operative half VERIFIED, process UNVERIFIABLE |

## 2. Patch round-trip and clean-tree identity (requirements a, c)

`evidence/patch-roundtrip.txt`, `evidence/v10-clean-repo.txt`,
`evidence/r10-clean-repo.txt`, `evidence/json-compare.txt`,
`evidence/scope-identity.txt`.

- **Round-trip.** Copied the pristine HEAD gate, ran
  `patch -p0 -F0 --batch < PL-4/patch-v10-to-r10.diff` (zero fuzz): exit 0,
  resulting sha256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`,
  713 lines, `cmp` **IDENTICAL** to `PL-4/c1-census-v10-r10.py`. The diff's
  six removed lines are the docstring close, the verdict text, the `max_end`
  expression, the `declared` expression and the `ok` expression — **no SCOPE
  row is removed or edited**.
- **Requirement (a).** Real repo, default `--root`: v10 `PASS` exit 0; r10
  `PASS` exit 0 with `FRONTIER register (G21): 14 rows asserted, errors: []`.
  A byte-identical clean scratch tree gives the same result.
- **Requirement (c).** `--json` v10 vs r10 on the clean tree: **17 shared
  keys, 0 mismatched**; r10-only keys `['frontier_errors','frontier_rows']`;
  `counts`, `current_ok_per_file` (`17/14/3`), `live`, `g7`, `g11`,
  `historical` all equal. Module-level comparison: 20 SCOPE rows,
  `a.SCOPE == b.SCOPE` → `True`; PIN/VER/PTR/CACHE/REA_GATE/INLINE_MARKER/
  RECEIPT patterns identical; 14 FRONTIER rows live outside SCOPE.

## 3. Requirement (b): my own seeded-fault arms

I did not reuse PL-4's `seed.py`; I built the trees with
`evidence/build_trees.py` and ran both instruments on each
(`evidence/arm-<tree>-{v10,r10}.txt`). All mutations are line-count-neutral
unless stated; `clean` is sha-identical to the repo files.

| Tree | Mutation | v10 | r10 | r10 declared class |
|---|---|---|---|---|
| `clean` | none | 0 PASS | 0 PASS | `[]` |
| `frozen` | exact pre-r4 EVM before-state at `92-93` (both lines from `git show 40de383`) | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` |
| `forbidden-only` | keep `solc-0.8.37`/`vyper-0.4.3`, add `untested` | 0 PASS | **1 FAIL** | `['FRONTIER-STALE']` |
| `req-evm` | strip both required tokens, no forbidden literal | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| `req-riscv` | remove `r5-01` from `:137` | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` |
| `trunc161` | PROVINCE truncated to 161 lines | 0 PASS | **1 FAIL** | `['UNREADABLE','FRONTIER-UNEVALUABLE']` |
| `pin88` | append `rea-agents@6.3.0` to `:88` (instrument-visible boundary fault) | 1 FAIL `undeclared=1` | 1 FAIL `undeclared=1` | `[]` (frontier rows clean) |
| `ins75`, `ins82` | one blank line before `:75` / `:82` | 1 FAIL (G15 marker) | 1 FAIL | `['FRONTIER-UNEVALUABLE']` |
| `ins134` | one blank line before `:134` | 0 PASS | **0 PASS** | `[]` — absorbed (C-1) |
| `stale-wall` | pre-r4 wall claim added, `arc2-r7`/`90 MB PE` retained | 0 PASS | **0 PASS** | `[]` (C-2) |
| `stale-cross` | pre-r4 cross claim added, `r12-02\|r14-01` retained | 0 PASS | **0 PASS** | `[]` (C-2) |
| `stale-wall-full` | exact pre-r4 wall bullet, anchors stripped | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` (`arc2-r7` absent) |
| `stale-cross-full` | exact pre-r4 cross bullet, anchors stripped | 0 PASS | **1 FAIL** | `['FRONTIER-UNEVALUABLE']` (`r12-02\|r14-01` absent) |
| `evade1` | blank line before `:93`, `untested` moved to new `:94` | 1 FAIL (G15) | 1 FAIL (G15) | `[]` frontier errors |

Key excerpts (full text in the evidence files):

```text
frozen:        PROVINCE.md:91-93 REQUIRED 'solc-0\\.8\\.37' absent
               PROVINCE.md:91-93 REQUIRED 'vyper-0\\.4\\.3' absent
               PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
forbidden-only: PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)   [exactly one]
req-evm:       two REQUIRED-absent errors (solc + vyper) -> FRONTIER-UNEVALUABLE
trunc161:      UNREADABLE ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']
               + 14 x "frontier uncheckable (file unreadable)"
pin88:         VERDICT FAIL (undeclared=1); FRONTIER register errors []
```

The `evade1` arm is the adversarial check for C-1: an inserted line moves the
stale literal just past the fixed span, so the register itself reports no
error — but the run still fails on the pre-existing G15 marker at `:119`
(`SCOPE-ERRORS: ["PROVINCE.md:119 marker 'verified 2026-10-13' absent from '']`).
The declared stale literal cannot be laundered by reflow while the only
FORBIDDEN row sits above `:119`.

## 4. Correction C-1 — reflow/insertion tolerance (`PL-4.md:330-333`)

PL-4 claims: "Insertions anywhere inside `:73-162` are caught: above `:119`
they shift the DATED marker row (G15 SCOPE-ERROR …), inside `:132-162` they
shift register spans (REQUIRED-absent — measured via the seeded arms)."

My sweep inserted one blank line before every line `74-163` and re-ran both
instruments (`evidence/insertion-map.txt`, 90 points):

- **Caught: `74-119` (46 points).** Every insertion above the DATED marker at
  `:119` shifts that marker down, so the pre-existing G15 assertion fails —
  v10 fails too. G21 adds REQUIRED-absent errors for some points
  (`ins75`/`ins82`: `oldest-first`, `unsupported_host`), but G15 is the
  actual catch.
- **Absorbed: `120-163` (44 points).** Insertions at/after `:120` leave the
  `:119` marker in place. The fixed register windows still contain every
  REQUIRED token after a one-line shift (most multi-line bullets repeat their
  anchors inside the shifted window), so G21 reads clean and the run PASSes.
  Insert-before `120` is insert-after `119`; EX-3's independent sweep absorbs
  exactly the same 44 after-points (`119-162`), and RV-1's matrix shows the
  same for `ins134/137/140/150`.

So the §6 sentence is **CORRECTED**: insertions inside `:132-162` are not
caught at all by r10; the only insertion catch is the pre-existing G15 marker,
and it stops at `:119`. This is a structural-drift gap, not a stale-literal
false PASS for the declared EVM literal (see `evade1` above). A per-row
first-line anchor (as in RV-3's `FRONTIER_REGISTER` / PL-1's hardening patch)
would close it; PL-4's register deliberately has no anchor.

## 5. Correction C-2 — one FORBIDDEN literal; anchor-preserving stale claims pass

`git show 40de383 -- PROVINCE.md` is the measured repair commit. It records
three before-states, all replaced in that commit:

1. EVM `:92-93` — "real solc/vyper-compiled bytecode untested"; guarded in
   PL-4's register by FORBIDDEN `untested` on `91-93`.
2. PE wall `:139-144` — "hits REA's ~900s internal session deadline …
   Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` …"; **no FORBIDDEN row**.
3. Cross-version `:157-160` — "`compare-application-versions` still
   probe-refused since r2; multi-version pacman pairs beyond expac
   unexercised"; **no FORBIDDEN row**.

I built both the exact before-state replacement and the anchor-preserving
variant (the same isolation PL-4 used for `seeded-forbidden-only`: keep the
earning tokens, add the retracted claim):

- `stale-wall-full` / `stale-cross-full`: anchors gone → r10 FAIL
  `FRONTIER-UNEVALUABLE`, v10 PASS.
- `stale-wall` / `stale-cross`: anchors retained, retracted claim present →
  **v10 PASS and r10 PASS**; `FRONTIER register errors: []`.

So the REQUIRED floor catches anchor *removal*, not a contradictory claim
that keeps the anchors. For the EVM bullet the FORBIDDEN literal closes this;
for the other two repaired bullets it does not. Frozen (b) is literally "a
declared-stale literal" — PL-4 declares one and catches it — so this is a
completeness gap against the R1 goal, not a requirement failure. PL-4's own
§6 residual 3 says only one literal is declared; my measurement fixes the
exact boundary (anchor-stripping caught, anchor-preserving not). RV-1's
anchor-preserving `seed-wall`/`seed-cross` independently agree; PL-1's
hardening patch adds all three literals from `40de383~1`.

## 6. Peer landscape (point-in-time; not evidence for my numbers)

The c1 tree changed while I measured. At capture time it held three complete
designs plus a hardening patch:

- **PL-4** (`PL-4.md`, files timestamped 13:29-13:30): r10 = `80027570…`,
  713 lines, 14-row REQUIRED/FORBIDDEN register, no anchors, 1 FORBIDDEN
  literal. This is the artifact I verified.
- **PL-2** (`PL-2.md`; its files moved to `PL-2/prior-attempt/` mid-run, with
  a later `PL-2/verify/` hardening pass): prior attempt claimed sha
  `2d7ee95b…`, SCOPE `FRONTIER` rows + a 3-literal register. I did not audit
  it end-to-end (out of seat; VZ/CN own reconciliation).
- **RV-3** (`RV-3.md`; audited by VZ-4): 13-row `FRONTIER_REGISTER` with a
  per-row anchor line, REQUIRED/FORBIDDEN and citations; claimed sha
  `8e420679…`. Its anchor design catches reflow where PL-4 does not.
- **PL-1** (`PL-1/patch-pl4-to-pl1.diff`): PL-4 + per-row anchors + the three
  FORBIDDEN literals from `40de383~1`; its battery shows `reflow133` →
  `FRONTIER-ANCHOR`.
- Peer sweeps corroborate my C-1 boundary (EX-3 insertion sweep: absorbed
  after-points `119-162`; RV-1 matrix: PL-4 passes `ins134/137/140/150`) and
  C-2 (RV-1 anchor-preserving wall/cross seeds pass PL-4). These are
  convergence checks, not substitutes for my arms above.

The three designs are not byte-identical. The parent must land exactly one;
my verdict is on PL-4's files only, which were stable across my run.

## 7. What I did not do / residual notes

- Did not modify `.ufo/gates/c1-census-v10.py` or any tracked file; final
  custody check still `d0772ce8…` (610 lines). All scratch under
  `/var/tmp/pl3-arc3r6/`.
- Did not re-audit PL-2's / RV-3's / PL-1's patches end-to-end; VZ/CN own
  reconciliation. Did not run c2 command A or c3 rule landing.
- The register's REQUIRED patterns are substring-level: a rewritten bullet
  that keeps its tokens but contradicts them passes (C-2); novel frontier
  staleness is still ungraded by design (declared literals only).
- Cosmetic: error strings render patterns `%r`-escaped (`solc-0\\.8\\.37`);
  same nit VZ-4 recorded for RV-3.
- Past-the-bound append at `:163` passes (named residual in PL-4; my map
  confirms it at insertion point 163).
- Scratch `--root` runs read host live anchors and the npx cache read-only;
  `live` is identical for v10 and r10, so the comparisons stand.

## 8. Evidence inventory and reproduction

Under `claims/c1/PL-3/evidence/`:

- `build_trees.py` — my seeder (all mutations, line-count-neutral).
- `versions.txt` — HEAD/log/gate sha/wc/status.
- `patch-roundtrip.txt` — pristine sha, zero-fuzz apply, patched sha/lines,
  `cmp` against PL-4's built copy.
- `v10-clean-repo.txt`, `r10-clean-repo.txt`, `json-v10-repo.json`,
  `json-r10-repo.json`, `json-compare.txt`, `scope-identity.txt`.
- `arm-<tree>-{v10,r10}.txt` for all 14 trees in §3, each with its exit code.
- `insertion-map.txt` — the 90-point sweep with the 44 absorbed points.
- `premise-scan.txt`, `scope-coverage.txt`, `evade1-{v10,r10}.txt`.
- `json-v10-frozen.json`, `json-r10-frozen.json` — the fault-tree JSON pair.

Reproduction (from the repo root, scratch elsewhere):

```bash
sha256sum .ufo/gates/c1-census-v10.py            # d0772ce8…
patch -p0 -F0 --batch < claims/c1/PL-4/patch-v10-to-r10.diff   # on a copy
sha256sum c1-census-v10.py                       # 80027570…, 713 lines
python3 c1-census-v10-r10.py --quiet             # PASS, 14 rows, errors []
python3 c1-census-v10-r10.py --root <tree> --quiet   # per §3
```

Landing reminder: the patch applies to the real gate with zero fuzz; after
landing, re-run the clean and frozen arms and record the post-edit sha in the
landing receipt (not inline — the gate's own rule-#14 discipline). But first
choose one of the competing c1 designs; PL-4's meets the frozen claim, while
the anchor + three-literal variants close C-1/C-2.
