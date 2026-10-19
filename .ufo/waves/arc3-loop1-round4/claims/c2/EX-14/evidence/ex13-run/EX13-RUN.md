# EX-14 — apply-and-census of EX-13's real patch texts (the seat's actual task)

Wave arc3-loop1-round4, chain c2. Runner: `harness/run.sh` (this seat).
Baseline: a fresh `/var/tmp` scratch root carrying all three census-scoped files
(`PROVINCE.md` `d075a3c6…` 162 lines, `SKILL.md` `5eec51c0…`, `SCORECARD.md`
`21042196…`), copied from the repo — the repo was only ever read.

## Result: 7/7 patches applied, PROVINCE 162 -> 162 lines, census PASS exit 0

| patch (current bytes, sha256 prefix) | hunk | balanced |
|---|---|---|
| `province-core-fallback-readers-inventory.patch.md` `1913e11ed5aa967f` | 1-/1+ | yes |
| `province-frontier-pe-subtypes-reserve.patch.md` `25de1d22c2f88826` | 2-/2+ | yes |
| `province-frontier-recorded-crashes-organic.patch.md` `c16fd02bf2804587` | 3-/3+ | yes |
| `province-frontier-alternate-providers-jeb.patch.md` `203fd3acb383bfdb` | 2-/2+ | yes |
| `province-frontier-evm-solc-held.patch.md` `a9515f743e705677` | 3-/3+ | yes |
| `province-round4-frontier-pe-wall-closed.patch.md` `1ce9b5a2a4017b54` | 6-/6+ | yes |
| `province-round4-frontier-cross-version-residuals.patch.md` `8db47d240fc6027b` | 4-/4+ | yes |

- PROVINCE.md after: sha256 `f951f161d8a7526ed0043eb41e9d92ee3b65b5c1dda51146e637aadd6d0ddcc5`, **162 lines**.
- Census: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0;
  `SCOPE-ERRORS []`, `UNREADABLE []`, `DECLARED FAIL CLASSES []`, G2 floor 17/14/3.
- All six named stale phrases verified ABSENT from the patched tree by `grep -F`:
  `Reserve: 91MB`, `JEB (unprobed)`, `real solc/vyper-compiled bytecode untested`,
  ``absent: `7z` ``, `probe-refused since r2`, `Next: raise`.

## Two defects measured in the patch texts (the census gate cannot see either)

**D1 — the pe-wall patch was not line-neutral at the revision first measured.**
`province-round4-frontier-pe-wall-closed.patch.md` sha256 `32f6052d92de6816`
carried a `-6/+5` hunk: 6 search lines replaced by 5, i.e. a net **line
reduction**. Applied, PROVINCE went **162 -> 161 lines**, contradicting the
patch's own conformance text ("Line-neutral: 6 -> 6 lines; `PROVINCE.md` stays at
162 lines"). The census still read **PASS** because the bullet sits at 139-144,
*below* the DATED row whose marker is asserted at line 119 — the marker line does
not shift. **This is the class the census cannot catch**: a line-count change
below the last asserted marker is invisible to G18, and the gate's only
line-count check is the "rows beyond declared max end" floor (162 is far above
the max declared end of 131).

EX-13 has since revised the patch to `-6/+6` (sha `1ce9b5a2a4017b54`); the run
above uses the current bytes, which ARE line-neutral. Only the sha measured at
landing time is authoritative (the round's own R5 residual).

**D2 — the EVM patch repeats the false Core promotion the chain verdict
sustained against EX-14's revision 1.** On the patched tree, `PROVINCE.md:92`
reads `(Core, r3-07) and real solc-0.8.37 carriers (Core, arc3-r1)`. Re-derived
by this seat: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` states
"RESULT-class exercise only — **no Core promotion**, no availability->holding
claim"; `grep -n arc3-r1 PROVINCE.md` finds the string ONLY on the patched line
(the promotion test); and `PROVINCE.md:75-76` requires a `LOG.md` entry for
promotion, which does not exist. So the patch asserts a promotion the corpus
disclaims — the same defect class the verdict fixed against this seat's v1.

**D2b — the same patch leaves the vyper half standing.** It still writes
`vyper-compiled bytecode untested`, although round-4's C1 leg measured 15/15 K/K
on vyper-0.4.3-compiled runtime (`claims/c1/EX-05/planted-vs-probe.txt`,
`ev_405e2a2a…`). That clause is stale against the wave tree (though its corpus
entry is still only staged, which is why EX-14's v2 gates that clause on the
entry landing in the same commit).

**EX-14's v2 candidate** (`evidence/candidate-complete-frontier-repair.v2.patch.md`,
sha256 `0b8ad045e19cee5a3120706853f9950bb90522b2ebaebb418db25f586c21d9a8`)
avoids both: it states RESULT-class instead of asserting Core, and covers the
vyper half — with the landing dependency named.

---

## ADDENDUM — re-run after EX-13's revision (final bytes)

EX-13 revised two patches after the run above; the seat re-ran all seven from the
then-current bytes on a fresh root (`harness/run.sh handoff`):

| patch | sha256 prefix (was -> now) |
|---|---|
| `province-frontier-evm-solc-held.patch.md` | `a9515f743e705677` -> **`66df2d6cf096f101`** |
| `province-round4-frontier-pe-wall-closed.patch.md` | `32f6052d92de6816` -> **`1ce9b5a2a4017b54`** |

**Result: 7/7 applied, PROVINCE 162 -> 162 lines, census PASS exit 0.**
PROVINCE.md after: sha256
`dcfdb6a2fea6374caba5daf229b97c59ae4a69efa6ae14943909436e19eb81ca`, 162 lines.
Evidence: `ex13-census-pass-final.txt`, `ex13-apply-final.log`.

**D2 (false Core promotion) is FIXED by EX-13's revision.** The bullet now reads
`(Core, r3-07) and real solc-0.8.37 carriers (RESULT-class, arc3-r1)` —
re-derived on this tree: `grep -n "Core, arc3-r1"` returns **no match**. The
promotion assertion is gone; the wording now matches the corpus entry's own
"RESULT-class, no Core promotion" scope.

**D1 (line-neutrality) is FIXED** — the pe-wall patch is now `-6/+6` and the
file holds at 162 lines.

**Still open in the final bytes (D2b):** the EVM bullet still reads `vyper
bytecode untested`. That clause is stale against the wave tree (C1's r4 leg
measured 15/15 K/K on vyper-0.4.3 runtime) but its corpus entry is still only
staged, so the clause is not yet false against *admitted* corpus state. It must
be repaired in the same commit that lands C1's entry, or left with that
dependency named — which is exactly the coupling EX-14's v2 candidate encodes.
