# PL-1 — C1 freshness: pacman row re-derivation

Seat: PL-1, c1 chain. Read-only source scope; no edits to `PROVINCE.md`, the gate, or corpus. Tested revision: `947091d6b6f52684faf9ca53adf94ff8a0f6b006` (`git rev-parse HEAD`). Measurement date: `date -I` → `2026-10-19`.

## Re-derived findings and verdicts

1. **`PROVINCE.md:50` archive inventory — CORRECTED (patch drafted, not applied).** The source line says `1556 signed archives`; the enclosing Core heading at `PROVINCE.md:40` dates its host verification to 2026-10-13. Independent live measurement:

   ```text
   $ ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
   1350
   $ ls /var/cache/pacman/pkg/*.sig | wc -l
   1350
   $ direct archive/sidecar filename match
   archives=1350 signatures=1350 matched_sidecars=1350 missing_sidecars=0 orphan_sidecars=0
   $ compare PROVINCE.md:50 baseline with direct archive glob
   PROVINCE baseline=1556; direct glob live=1350; signed-file glob=1350; live-baseline=-206
   ```

   The historical 1,556 is explicitly identified as the 2026-10-13 snapshot in `corpus/knowledge/2026-10-13-pacman-packages.md:75-83`; the live count and subtraction above were re-derived from the cache and source line, not taken from a prior seat. This verifies matching sidecars, not cryptographic validation of every signature.

2. **Other potentially perishable assertions in the complete row — VERIFIED / UNVERIFIABLE as current, itemized.** `available:true in live session` is a perishable session-state assertion, but `PROVINCE.md:40` dates the Core table's verification to 2026-10-13. This seat had no live REA MCP call to re-probe it, so it is **UNVERIFIABLE as a current-session assertion**; the patch below preserves it only as a dated 2026-10-13 observation. The `installed jq` byte-identity statement is also perishable and was rechecked now:

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

   `.MTREE per-file sha256` and `pacman -Qkk verify` name mechanisms, not additional mutable counts. No other unqualified numeric inventory value was found in the row. The installed-`jq` assertion is current and can be explicitly dated 2026-10-19 in the replacement text.

3. **C1 census gate — DISCREPANCY.** Ran `python3 .ufo/gates/c1-census-v10.py` against the source tree. Gate file SHA-256 is `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`, identical to `git show HEAD:.ufo/gates/c1-census-v10.py | sha256sum`. Output excerpt:

   ```text
   live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
   -- UNDECLARED (1) --
     SCORECARD.md block 1833-1839 [scope None]
         :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
   SCOPE-ERRORS (marker assertions): []
   FRONTIER register (G21): 14 rows asserted, errors: []
   DECLARED FAIL CLASSES: []
   VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
   ```

   Exit status: 1. `c1-census-v10.py:276` scopes the SCORECARD DATED range only through line 1813; the round-8 pin at `SCORECARD.md:1834` is outside it. The live PROVINCE pointer check does re-derive as current-ok, but this unrelated undeclared SCORECARD locus prevents PASS.

## Proposed same-line replacement for `PROVINCE.md:50`

This is draft patch text only; no source file was changed.

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in the 2026-10-13 live session); pacman `.pkg.tar.zst` corpus: 1,350 archives with matching `.sig` sidecars (1,350/1,350) as of 2026-10-19; the prior 1,556 is the 2026-10-13 snapshot (live delta −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:75-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` byte-identical to signed archive member (reverified 2026-10-19) |
```

A permitted `/var/tmp` scratch copy substituted only this line and re-ran the gate. Scratch `PROVINCE.md` remained 162 lines, line 50; gate output remained `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`, exit 1, at the same `SCORECARD.md:1834` locus. Thus the patch itself is line-neutral and does not introduce a census finding, but the frozen after-condition “census PASS held” is **not reproduced**. Clearing the unrelated gate finding is outside PL-1's write scope; source and gate remain untouched.
