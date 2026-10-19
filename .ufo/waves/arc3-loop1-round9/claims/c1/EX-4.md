# EX-4 — C1 freshness re-derivation

Status: the PROVINCE edit below is patch text only; no source, gate, corpus, custody, or tracked file was changed. All scratch gate tests were under `/var/tmp`.

## Identity and fresh measurements

- `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.
- `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4  .ufo/gates/c1-census-v10.py`.
- **CORRECTED — live archive inventory.** On `2026-10-19`, I independently counted `/var/cache/pacman/pkg/*.pkg.tar.zst` and matching `.sig` paths; a second pairing pass checked names both ways:

  ```text
  2026-10-19
  archives=1350 signatures=1350 missing_matching_signatures=0 extra_signatures=0
  missing_sample= []
  extra_sample= []
  ```

  The historical source record identifies 1,556 as its 2026-10-13 snapshot and documents its original counting command at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`; its appended erratum is at `:73-83`. I did not treat that old count as a present-day measurement. Arithmetic using the fresh count and the recorded snapshot is `1,350 − 1,556 = −206`. The current filename census establishes matching signature files, not cryptographic validity of every signature.
- **VERIFIED — installed jq byte identity, current check.** `pacman -Q jq` → `jq 1.8.2-1`; the only matching cached archive was `/var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst`. `sha256sum /usr/bin/jq` and `tar -xOf <that archive> usr/bin/jq | sha256sum` both returned `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`. This verifies installed bytes against the cached member now; it does not independently validate the archive signature.

## Whole-row perishables census (`PROVINCE.md:50`)

- **CORRECTED — `1556 signed archives`.** This is a dated cache count, not a present count. Replace it with the patch text below: preserve the historical value with an explicit snapshot date, add the freshly measured count/date/delta, and point to the erratum.
- **UNVERIFIABLE as a current REA-session claim — `available:true` / `binary_session {}`.** Availability is session-relative and perishable. The row says “in live session”; the surrounding Core heading says each surface was verified on `2026-10-13` (`PROVINCE.md:40`), and the census scope likewise dates `PROVINCE.md:45-62` from line 45 (`.ufo/gates/c1-census-v10.py:259`). I have no REA `binary_session` tool in this session, so I did not claim a fresh availability observation. The proposed row makes the historical date explicit.
- **VERIFIED — installed `jq` equality.** This is another potentially perishable result in the row, and the direct 2026-10-19 hash/`pacman -Qkk` checks above reproduce it. The patch dates that recheck.
- `.MTREE per-file sha256` and `pacman -Qkk verify` describe archive metadata / a verification capability, not another unqualified live count. I did not make a new claim about every archive’s metadata or cryptographic signature validity.

The C1 instrument does not grade the row’s freshness value: direct classifier checks on the exact row returned `REA_GATE_matches_row_= False`, `PIN_matches_row_= []`, `VER_matches_row_= []`, `PTR_matches_row_= []`; `archive_row_scope_= ('DATED', 45, '2026-10-13')`. The relevant implementation is `.ufo/gates/c1-census-v10.py:310-315,499-514`. Thus a clean gate result would not itself prove the pacman count current.

## Proposed same-line patch (not applied)

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@
-| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
+| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in a live session, verified 2026-10-13); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; as of 2026-10-19: 1,350, delta −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to its cached archive member (rechecked 2026-10-19) |
```

The candidate replaces only line 50; a scratch candidate retained 162 `PROVINCE.md` lines.

## Gate result / limitation

**DISCREPANCY — frozen “instrument still PASS” condition is not met at this HEAD, before or after this row-only candidate.** First-hand command `python3 .ufo/gates/c1-census-v10.py --json --root .` exited 1 and returned `"verdict": "FAIL"`, counts `PROVINCE.md 162 lines/6 loci`, `SCORECARD.md 1870/11`, `SKILL.md 413/2`, and one undeclared block: `SCORECARD.md` `1833-1839`, `UNDECLARED`, pin `6.7.0` at line 1834. The gate’s SCORECARD scope ends at `1813` (`.ufo/gates/c1-census-v10.py:276`); the offending text is in the appended R8 record (`SCORECARD.md:1833-1839`).

I copied the three scoped documents and gate to `/var/tmp`, applied only the proposed line-50 text to that scratch copy, and reran the gate. Baseline scratch and candidate scratch both returned exit 1 / `FAIL`, with the same sole undeclared `SCORECARD.md:1833-1839` pin. The candidate did not introduce a Province locus or alter the gate’s counts. Repairing this unrelated SCORECARD/gate-scope discrepancy is outside EX-4’s artifact-only scope; therefore I cannot report a PASS or claim the frozen gate condition was satisfied.
