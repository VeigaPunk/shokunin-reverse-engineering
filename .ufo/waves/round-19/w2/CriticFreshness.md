# CriticFreshness — attack on amended C2 (freshness)

Scope: amended C2 (claims.json:39) — stale loci 4→0, pin mismatches 2→0, census
stays FAIL on 2 pre-existing undeclared, no SCOPE/DATED widening, no harm.
Lane read-only; all revision work in `git clone --no-hardlinks` copies at
`/tmp/kr19-w2-CriticFreshness.8ozHyw/{base,main}` (base `8a8da7e…`, main
`d0690fd44f46d8a7fe9da5f01c6be723d12abd41`).

## Verdict

The numeric story is honest: 4→0, 2→0, FAIL retained, zero SCOPE/DATED change —
all reproduced. The **harm claim is incomplete and misattributes the residual
FAIL**: the rewrite introduced a *new, self-inflicted gate failure* — a G11
receipt-backing trigger at `PROVINCE.md:44`. The census now FAILs on **two
independent causes**, not one; the amendment's "stays FAIL on the 2 pre-existing
undeclared blocks" reads as cause-complete when it is not, and it silently
recedes the PASS horizon (fixing the scope-table re-key would still not PASS).

## Reproduced evidence

**Baseline census** — `cd /tmp/kr19-w2-CriticFreshness.8ozHyw/base && python3 -I -B .ufo/gates/c1-census-v10.py --root $T/base` →
`EXIT:1`, `VERDICT: FAIL (stale=4 ambiguous=0 undeclared=2 unresolved=0)`,
`G11 current-ok without receipt language: []`, `SCOPE-ERRORS: []`.
Stale blocks: PROVINCE.md 8-13 (pin omp=6.5.0), 15-26 (pin devin/omp=6.5.0),
44-44 (bare devin/omp=6.5.0), SKILL.md 18-20 (pin devin/omp=6.5.0).
Undeclared: SCORECARD.md block 2380-2382, SKILL.md block 511-519 — scope None.

**Main-tip census** — same command against `…/main` → `EXIT:1`,
`VERDICT: FAIL (stale=0 ambiguous=0 undeclared=2 unresolved=0)`, same two
undeclared blocks, **but `G11 …: ['PROVINCE.md:44']`** (line 113 of output),
`SCOPE-ERRORS: []`, `FRONTIER … 14 rows asserted, errors: []`, G2 ok.

**Pins probe** (main-tip tool, both revs; the tool does not exist at baseline):
`python3 -I -B $T/main/.ufo/waves/round-19/tools/province-pins.py --root $T/base --rev 8a8da7e… --strict` → `EXIT:1`, mismatches=2 (Devin lines 9/16/44, OMP lines 9/17/44, live 6.7.0).
`--root $T/main --rev refs/heads/main --strict` → `EXIT:0`, mismatches=[], unstated_clients=[].

**No widening** — `git diff 8a8da7e..refs/heads/main -- .ufo/gates/c1-census-v10.py`
→ empty (census SCOPE/FRONTIER tables identical; PROVINCE diff is 16 ins/16 del,
all hunks line-count-neutral, so no SCOPE/FRONTIER row re-keyed or widened).

## Findings

**F1 (freshness/calibration harm, fixable): new G11 FAIL cause at `PROVINCE.md:44`.**
Baseline `:44` stated pins "per the 2026-10-18 custody **receipt**"; the rewrite
to "Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary"
dropped every receipt token. G11 (`c1-census-v10.py:615-621`; verdict term at
`:698` `(not g11)`) requires a `current-ok` locus's block to carry RECEIPT
language (`2026-10-18|receipt|SHA-256|sha256|re-grepped`, `:321`). Baseline G11
was `[]`; post-edit G11 is `['PROVINCE.md:44']`. So the delivered revision FAILs
on undeclared=2 **plus** g11=1. Amended claims.json:39 names only the undeclared
blocks as the FAIL cause — the outcome statement understates residual failure
and, worse, a future seat that re-keys the scope table (the wave-1
ReviewC1CensusScope correction path) would still get FAIL with the cause now
buried outside `declared_fail_classes` (g11 is appended nowhere in `:691-695`).
Not a judge-level regression in verdict text (FAIL is honestly reported as
FAIL), but a real harm: an edit billed as freshness-only **created** a gate
finding. Smallest correction: restore a receipt term in the `:44` evidence cell
(e.g. "…see surface summary; round-19 pin probe receipt") **or** add
`g11: PROVINCE.md:44` to the amended C2 residual list.

**F2 (residual freshness debt inside the edited claim's own scope): `PROVINCE.md:47`.**
The claim targets drift-prone values "Ghidra/JDK". The surface summary was
correctly updated to `.bashrc:28-29` (live check: `export JAVA_HOME` is at
`.bashrc:29`; `sed -n '23,29p' ~/.bashrc` shows `:28` `GHIDRA_INSTALL_DIR`,
`:29` `JAVA_HOME`). The Core row at `PROVINCE.md:47` still reads
"exported in `.bashrc:24` + `.profile:4`" — now a wrong line pointer for the
same fact the claim just re-derived. It sits inside the DATED 45-62 row
(marker `2026-10-13` at `:45`), so the gate cannot see it; it is exactly the
class of stale pointer the claim exists to retire. Smallest correction:
`.bashrc:29`. Fixable; mildly cuts against "drift-prone values re-verified" as a
complete story.

## Spot-checks of the rewrite's new assertions (all verified true)

- Devin `/home/vgpnk/.config/devin/mcp_config.json` and OMP
  `~/.omp/agent/mcp.json` pin `rea-agents@6.7.0` (observed); Kimi
  `~/.kimi-code/config.toml:4126` `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`
  (observed). mtimes 16:35:56Z match the "13:35:56 -03" rewrite claim.
- OMP `enabled` key genuinely absent (live `mcp.json` rea entry keys:
  type/command/args/env only) — consistent with w1 `LiveConfigPins.md:36-66`
  observation chain and PROVINCE.md:18's disclosure. Correct handling:
  PROVINCE records the disable *history*, not a live flag.
- npx caches: `a1722018f28f9df2`=6.7.0, `ad9a3fdbcad992c6`=6.5.0 present;
  `dea9475797100b20` absent — matches the new "historical, absent 2026-10-20"
  framing (previously asserted present).
- `tools_sha256` `af39310c…`/`805433f1…`/`25802f6d…` match
  `.ufo/waves/round-19/evidence/rea-catalog.json`.
- `.bashrc:63-69` provider exports verified live (`REA_PWNTOOLS_PYTHON`…
  `REA_JADX_MCP_JAR`), below the interactive guard at `:34`; `REA_APKTOOL_COMMAND`
  now at `:66` as stated.
- `Ghidra/application.properties:17` `application.version=12.1.4` observed.
- Doctor story corroborated: `evidence/doctor/doctor-6.7.0.txt` has no
  `registration:devin`/`registration:omp` checks (clients appear in the
  aligned-provider listing, devin `state: aligned` at :315-320);
  `doctor-6.5.0.txt:91-95` reports "registration requests rea-agents@6.7.0".
  PROVINCE.md:24's paraphrase is accurate.
- Contract consistency: contract.md:35-36 still instructs `rea-agents@6.5.0`
  CLI; PROVINCE.md:12 now labels that pin "superseded client pin" — the
  semantic is correct and non-conflicting (contract pin ≠ client pin), and the
  amendment's "no client-config edit" non-goal was respected (configs untouched;
  PROVINCE documents them).

## Residual unknowns / not falsified

- Whether `PROVINCE.md:44`'s "6.7.0 doctor" cell asserting a *verdict* in a
  CURRENT row will itself go stale when client configs next drift is inherent
  to the instrument design, not a defect of this edit.
- The `undeclared=2` misattribution is one sentence of framing; the recorded
  before/after counts remain exactly as claimed. F1/F2 are fixable defects,
  not grounds to reject the C2 outcome: stale 4→0 and pins 2→0 are real,
  measured, and the FAIL is honestly retained rather than laundered to PASS.

## Tooling

No installs or upgrades performed; nothing essential was missing.
