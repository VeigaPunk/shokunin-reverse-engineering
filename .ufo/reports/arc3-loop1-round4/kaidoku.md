# arc3-loop1-round4 — kaidoku-shokunin — round report

**Schedule slot:** R4 — 32–64 seats, `hyper/deepseek-v4.1-flash`.
**Executed as:** 48 seats on `devin/deepseek-v4-1-flash-max` — the declared
fallback: hyper returned 402 on all seats within ~30 s of dispatch (account
exhausted, not rate-limited); the token-plan monthly quota had died mid-R3, so
the devin lane was the declared substitute. All 48 seat reports delivered.
**Work commits:** `520341d` (C3 custody residuals, landed mid-wave) +
`40de383` (C1 corpus entry + C2 PROVINCE repairs, coupled single commit).
**Records commit:** this commit.

## Work performed

- **C1 — coverage: the r3-named Unknown (Vyper-compiled EVM bytecode) closed.**
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`: vyper
  `0.4.3+commit.bff19ea2` (the round's one authorized install), runtime 1,562 B
  sha256 `57d6fd0a…`, `inspect-evm-interface` → 15/15 planted selectors K/K at
  both pins (`ev_405e2a2a…` @6.4.0 + 6.7.0 run), `dispatch:"abi"`, a third
  dispatch shape (modulo-indexed jump table, distinct from the solc linear and
  binary-search classes). The draft carried four pre-landing fix sets (the
  `69656e74` PUSH32-substring fix, the same-path sentence, the argument-count
  inference mechanism, the QUALITY.md:24-25 citation) and the wave's CR-1/RV-1
  corrections folded into its Unknowns. `corpus/README.md` map token landed.
- **C2 — freshness: PROVINCE staleness census + same-line repairs.** The
  chain's census grew 6 → 9 stale rows across three peer corrections, each
  re-measured first-hand by the convergence seat (VZ-2): F2 (a sub-cap 17.6 MB
  organic crashpad core inspects exit 0 — the "all 3 organic cores exceed the
  cap" universal is false), C2 ("35 features" is the corpus entry's own
  miscount of its 34-name list — matches disk), C3 (the asar row names 9
  archives where the host holds 12, incl. chatgpt-bin post-sweep + the zcode
  squashfs copy + the config-dir obsidian copy). Landing = EX-15's 8-hunk
  line-neutral set + EX-12's Core-asar-row patch + PL-2's coupled
  `corpus/knowledge/2026-10-13-ghidra-install.md` erratum (the PROVINCE↔corpus
  coupling, trimmed to avoid duplicating the entry's existing round-2 erratum).
  All nine stale literals cleared; `PROVINCE.md` 162→162 lines; no line shifts
  above :116 (SHONEN:12 clause at :114-116 preserved); B2's X1 clause cites
  `r12-02` (JS + managed) **and** `r14-01` (runtime-reconcile,
  `ev_8f0ac46c…`). `JEB (unprobed)` adjudicated NO-CHANGE-with-cause (the verb
  was probed at r2 and re-probed this wave; no JEB install exists — wording is
  shorthand for "no JEB surface held").
- **C3 — operability: custody-pair residuals closed** (landed mid-wave as
  `520341d`): sidecar scope fix, mkdir guard, distinct-path gate, both-absent
  ruling; selftest 22 → 28; the SKILL.md registry row now carries the 28-case
  form. Probe findings=0 both modes; live pair MATCH 5/5.
- **Landing-form discipline (rule #14):** every identity was re-derived at the
  work commit — `PROVINCE.md` sha256 `11a5c604…` / 162 lines, corpus entry
  `e7670382b171869f`, all instruments re-run on the landed tree, not quoted
  from the wave.

## Landed changes

- `40de383` — work commit: `PROVINCE.md` (9 same-line repairs),
  `corpus/README.md` (EVM map token), `corpus/knowledge/2026-10-13-ghidra-install.md`
  (append-only erratum), `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`
  (EX-07 line-neutral correction), `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
  (new), plus the committed wave tree `.ufo/waves/arc3-loop1-round4/`.
- `520341d` — C3 work commit (landed mid-wave): `.ufo/gates/custody-pair/`
  hardening + registry row.
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | counting command | measured at |
|---|---|---|---|---|
| C1 coverage | corpus 83 files; the Vyper leg an explicitly named Unknown | 84 files; 15/15 K/K at both pins | command A (`SCORECARD.md:88`) `mapped` count | `40de383` → 84/84 |
| C2 freshness | PROVINCE stale=9 (the wave's measured census) | stale literals all absent (clause audit `grep -F`); 162→162 lines | `grep -cF "<literal>" PROVINCE.md` per row + `wc -l` | `40de383` |
| C3 operability | selftest 22 cases; 3 open residuals | selftest 28; residuals closed; pair MATCH 5/5 | `.ufo/gates/custody-pair/custody-pair.py --selftest` | `520341d` |

Gate confirmations at `40de383`: `c1-census-v10.py` PASS
(stale=0 ambiguous=0 undeclared=0 unresolved=0); citation-drift probe
`findings=0` in both default and `--strict` modes; command A 84/84 mapped,
14/14 rules, coverage 10.0, depth 10.0.

**The honest instrument note (the wave's own finding, carried as R1
residual):** the census gate cannot grade any of the C2 repairs — the whole
Frontier region (PROVINCE:73-93) and the post-unlock frontier (:133-162) are
UNDECLARED in its SCOPE table, so it reads PASS identically before and after.
The movement the claim records lives in the clause-level audit (9 stale
literals → 0) and the adjudication ledger, which is exactly what the claim's
wording ("census-checked … or adjudicated NO-CHANGE with cause") prescribes.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| depth | unchanged | 10.0 → 10.0 (14/14 measured) |
| coverage | **improved** | 83 → 84 corpus files; the named Unknown closed |
| operability | **improved** | custody residuals closed; selftest 22 → 28 |
| freshness | **improved** | 9 stale rows → 0 at a held line count |
| calibration | unchanged | 10 → 10 |
| adjacency | unchanged | PROVINCE boundary untouched; no cross-lane writes |

Admission: all three claims verified by measurement; no axis harmed →
**admitted**.

## Carried debt (named, not smoothed)

1. Census blind spot: Frontier-region repairs are clause-audited, not
   instrument-graded (R1 — needs a same-commit SCOPE re-key of
   `c1-census-v10.py`, an instrument-round job).
2. `ptr_check` unreachable on clauses carrying an inline pin (R2).
3. Wave-tree record-only corrections (RV-1's patch file, `EX-05/runtime-presence.txt`,
   `RV-2/evidence/push4-census.txt`, `seats/EX-05.md`) remain as wave artifacts —
   the corpus content landed; those sibling files are wave records, flagged.
4. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` stays unstaged.
5. `/tmp` quota (standing host constraint).

## SHONEN

- `[~]` SKILL.md real decision tables / error patterns / checklists with cited
  sources — asserted `SKILL.md:81-255`; this round added no rule blocks but
  landed the C3 registry row's 28-case form; no named non-author verifier.
- `[~]` end-to-end domain task executed and logged — the Vyper leg is a new
  end-to-end leg (install → compile → probe → entry); logged this round.
- `[~]` instructions executable without oral context — the same-line repair
  recipe and the coupled-landing sequencing are recorded in the wave's
  `claims/c2/verdict.md` closing procedure and this report.
- `[~]` no cross-domain bleed — PROVINCE boundary section (:95-117) untouched;
  the repairs are all Core-table / Frontier content, not scope.
