# RV-3 — C1 perishable-value census

**Verdicts:** count **CORRECTED** (patch text below); installed-`jq` identity **VERIFIED**; live-session availability **UNVERIFIABLE** from this seat; scratch gate check **REPRODUCED**; whole-gate PASS expectation **DISCREPANCY**.

## First-hand observations

- `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. `PROVINCE.md` is unchanged in the worktree (`git diff -- PROVINCE.md` produced no output); its line count is 162.
- Live archive census command: `ls -1 /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` → `1350`; signature-sidecar count command: `ls -1 /var/cache/pacman/pkg/*.pkg.tar.zst.sig | wc -l` → `1350`; matching-name loop → `missing signatures=0 orphan signatures=0`. This establishes a live 1:1 sidecar inventory, not cryptographic revalidation of every signature.
- The dated baseline is the corpus record at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` (1556 archive/signature files at its receipt date). Its append-only erratum at `:73-83` identifies that as a 2026-10-13 snapshot and records the subsequent live count/delta. I independently counted the current files above; Python arithmetic `1350 - 1556` → `-206`. Thus 1556 is a historical snapshot, not today's count.
- Installed `jq` recheck: `pacman -Q jq` → `jq 1.8.2-1`; cached member `jq-1.8.2-1-x86_64.pkg.tar.zst`. `sha256sum /usr/bin/jq` → `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; `tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum` → the same digest. The volatile installed-file identity is therefore **currently VERIFIED**, and the patch dates this recheck explicitly.
- Row census (`PROVINCE.md:50`, with the table's date heading at `:40`): `available:true in live session` is a volatile session observation, but no REA `binary_session` tool was available here to refresh it; it is explicitly dated to the table's 2026-10-13 observation in the patch, not represented as current. `.MTREE per-file sha256`, `pacman -Qkk verify`, and `binary_session {}` are format/procedure/probe descriptions, not additional current inventory values. The installed-`jq` assertion is the other volatile state, and was rechecked above.

## Proposed same-line patch text — not applied

```diff
-| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed jq verified byte-identical to signed archive member |
+| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in 2026-10-13 live session); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live `.pkg.tar.zst` count 1,350, delta −206 as of 2026-10-19; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed jq verified byte-identical to signed archive member (re-verified 2026-10-19) |
```

## Gate re-run and candidate check

- Gate identity: `.ufo/gates/c1-census-v10.py`, SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`, 716 lines. It contains the G21 register and pointer checks. `PROVINCE.md:50` has no gate-recognized REA pin/version/cache/pointer locus; the count requires the explicit row census above.
- `python3 .ufo/gates/c1-census-v10.py --root .` → exit 1. Output included `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1870 loci=11`, `SKILL.md lines=413 loci=2`; G21 `14 rows asserted, errors: []`; G2 `ok` with current-ok counts `PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3`; final `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`. The undeclared item is `SCORECARD.md` block `1833-1839`, line `1834` (`6.7.0`, AMBIGUOUS/no client token). The instrument's declared SCORECARD range ends at line 1813 (`.ufo/gates/c1-census-v10.py:276`); the offending text is `SCORECARD.md:1833-1839`. This is independent of the PROVINCE row and cannot be repaired within RV-3's write scope.
- Scratch-only before/after run at `/var/tmp/kaidoku-rv3-r9-final-pl2hlyrv` applied exactly the proposed replacement to one copied row and reran the gate. `PROVINCE` stayed at 162 lines and 6 loci; all counts, G21 (14/0 errors), G2, and current-ok-per-file counts were unchanged. Both baseline and candidate returned exit 1 / FAIL solely on the same undeclared `SCORECARD.md:1833-1839` locus. Thus the same-line patch preserves 162 lines, but the requested whole-gate PASS is **not** reproducible on this HEAD absent an out-of-scope gate/scope repair.

No tracked file, `PROVINCE.md`, gate source, corpus entry, or other seat's artifact was edited.
