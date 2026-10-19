# RV-4 — C1 freshness re-derivation

Chain: c1 (`claims-frozen.md:14-28`; roster `:60`). Measured against lane `HEAD` `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. PROVINCE, corpus, and gate sources were read-only; the proposed row was tested only in a disposable `/var/tmp` copy, which was removed.

## Findings and verdicts

- **CORRECTED — pacman archive count.** `PROVINCE.md:50` says `pacman .pkg.tar.zst corpus 1556 signed archives` without an as-of date. First-hand live count:

  ```text
  $ pkg=$(ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l); sig=$(ls /var/cache/pacman/pkg/*.sig | wc -l); printf 'pkg.tar.zst=%s\n.sig=%s\ndelta_vs_1556=%s\n' "$pkg" "$sig" "$((pkg - 1556))"
  pkg.tar.zst=1350
  .sig=1350
  delta_vs_1556=-206
  $ date -u +%Y-%m-%d
  2026-10-19
  ```

  The current 1,350 and −206 are derived by this command, not adopted from another seat. The requested cross-reference is `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`; it identifies the 1,556 wording as a dated snapshot and contains the erratum.

  **Proposed one-line replacement** (text only; not applied):

  ```text
  | Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus: 1,556 signed archives (2026-10-13 snapshot); live cache: 1,350 (2026-10-19, −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` re-verified byte-identical to signed archive member (2026-10-19) |
  ```

  It is a one-physical-line replacement; the scratch check retained 162 lines.

- **UNVERIFIABLE as current — `available:true` in a live session.** This is the other time-sensitive value in the row. The phrase is session-scoped, but `PROVINCE.md:50` carries no session date or receipt; no live `binary_session {}` call was available in this seat. The census gate does not grade this value: its token families are pin, bare `6.x.y`, config pointer, and npx-cache identity (`.ufo/gates/c1-census-v10.py:310-316, 499-515`); a first-hand parse of its JSON detections returned PROVINCE assertions only at lines 44, 67, and 125, with `line_50_graded: False`. Do not present the availability value as freshly verified.

- **VERIFIED for 2026-10-19 — installed jq/archive byte identity.** This is in the row's “verified evidence” cell, so it is past-tense rather than a current inventory count, but it can perish. I rechecked it before proposing a dated wording:

  ```text
  $ pacman -Q jq
  jq 1.8.2-1
  $ pacman -Qkk jq
  jq: 25 total files, 0 altered files
  $ sha256sum /usr/bin/jq
  e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
  $ tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
  e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
  ```

  The other row material (`.MTREE` per-file sha256, `pacman -Qkk` verify, and `binary_session {}` capabilities) is a property/procedure or probe name, not another dated live count. The `available:true` value above remains the sole unverified current-state candidate.

## Census gate result — DISCREPANCY

Current-tree command: `python3 .ufo/gates/c1-census-v10.py --quiet`.

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1870 loci=11
SKILL.md       lines=413  loci=2
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

`python3 .ufo/gates/c1-census-v10.py --json` isolates the undeclared locus: `SCORECARD.md`, block `1833-1839`, assertion at line 1834, value `6.7.0`, disposition `AMBIGUOUS`; top-level `undeclared=1`. The declared SCORECARD scope ends at line 1813 in the gate source (`:276`), so this is the later r8 record, not the PROVINCE:50 count.

I applied the proposed PROVINCE row only to copied inputs under `/var/tmp` and ran the gate against that root. Output: `SCRATCH_PATCH: replacements=1 PROVINCE_lines=162`; `SCRATCH_GATE: exit=1 verdict=FAIL stale=0 ambiguous=0 undeclared=1 unresolved=0 scope_errors=0 frontier_errors=0`; `UNDECLARED: SCORECARD.md 1833-1839` (the same `:1834` assertion). Scratch was removed. Thus the requested same-line repair itself preserves 162 lines, but the required “instrument still PASS after” condition is **not reproduced**: the gate is already red for an out-of-scope r8 locus and the pacman number is not one of its graded token types. No protected gate or province file was changed.
