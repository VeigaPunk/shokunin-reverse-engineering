# RV-1 — C1 freshness re-derivation

**Seat/chain:** RV-1 / c1.  
**HEAD observed:** `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.  
**Scope:** read-only source census; patch text only. No source, gate, corpus, or tracked file was changed.

## Findings and verdicts

- **Pacman cache count — CORRECTED.** `PROVINCE.md:50` says `1556 signed archives` without an as-of qualifier. A direct count on this host returned 1,350 `.pkg.tar.zst` files and 1,350 `.sig` files. An independent stem-set check returned `archives=1350 signatures=1350 missing-signatures=0 orphan-signatures=0`. Thus the current count is 1,350 with matching signature sidecars. Arithmetic against the row's existing 1,556 baseline is `1556 - 1350 = 206`, i.e. −206. The historical 1,556 is not a present-day observation; I did not reconstruct the 2026-10-13 cache. The dated source record is `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`.
- **Other perishable claims in the row — census.** (1) `available:true in live session` is session-dependent. `PROVINCE.md:40-43` dates the surface table to 2026-10-13; I did not re-probe the REA live session, so current availability is **UNVERIFIABLE**. The replacement text makes that historical status explicit. (2) `installed jq verified byte-identical` is also perishable; re-derived below and **VERIFIED** on 2026-10-19. (3) `.MTREE per-file sha256`, `pacman -Qkk verify`, and the `binary_session {}` probe reference describe format/method, not an asserted live count or availability value; no freshness repair indicated.
- **jq identity — VERIFIED.** Re-derived installed package and bytes directly:
  ```text
  installed package: jq 1.8.2-1
  candidate archive: /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst
  installed SHA-256: e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
  archive member SHA-256: e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
  byte comparison: identical
  jq: 25 total files, 0 altered files
  ```
  The command extracted `usr/bin/jq` from the currently cached `jq-1.8.2-1-x86_64.pkg.tar.zst`, hashed it, compared it with `/usr/bin/jq` using `cmp`, and ran `pacman -Qkk jq`.

## Proposed same-line patch text (not applied)

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` observed in a live session on 2026-10-13; not re-probed); pacman `.pkg.tar.zst` cache: 1,350 archives with 1,350 matching `.sig` sidecars, re-counted 2026-10-19 (−206 vs. the 1,556 archive snapshot recorded 2026-10-13; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | `/usr/bin/jq` (jq 1.8.2-1) verified byte-identical to its cached archive member on 2026-10-19 (SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; `pacman -Qkk`: 25 total files, 0 altered files) |
```

This replaces only `PROVINCE.md:50`; a scratch copy under `/var/tmp/kaidoku-rv1-c1.jwBq2P` retained 162 lines after substitution. The 1:1 sidecar result is a filename census, not a cryptographic verification of every signature.

## Instrument result — DISCREPANCY

Gate `.ufo/gates/c1-census-v10.py` SHA-256 re-derived as `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`. It returns FAIL on unmodified HEAD and also on the patched scratch copy; the row substitution does not cause the failure. The baseline run printed:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

The patched-copy JSON summary likewise returned `gate_exit=1`, `verdict=FAIL`, `province_lines=162`, `stale=0`, `ambiguous=0`, `undeclared` at `SCORECARD.md` block `1833-1839`, `unresolved=0`, `scope_errors=[]`, `frontier_errors=[]`, `unreadable=[]`, and `g11=[]`. Thus the required post-change PASS is **not reproduced** at this HEAD; the gate's declared scope ends at `SCORECARD.md:1813`, while the pin locus is at `:1834`. I did not modify the gate or its scope, which are outside this seat's write scope.

## Re-derived command outputs

Archive/signature counts and line count:

```text
archive count: 1350
signature count: 1350
province lines: 162
```

Filename-pair census:

```text
archives=1350 signatures=1350 missing-signatures=0 orphan-signatures=0
```

The gate baseline reported live anchors `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `SCOPE-ERRORS (marker assertions): []`, and `G2 positive-assertion guard: ok`; the sole reported verdict failure was the undeclared scorecard locus above.
