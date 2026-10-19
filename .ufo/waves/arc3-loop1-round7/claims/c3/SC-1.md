# SC-1 — C3 calibration: pacman cache count

## Receipt and first-hand re-derivation

Chosen drift class: cached pacman `.pkg.tar.zst` inventory. The recorded receipt at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` states 1,556 archives and gives `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` as its count recipe.

Re-ran that exact command against the live cache:

```text
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
1350
```

Independent path enumeration returned the same count:

```text
$ find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf '%f\n' | wc -l
1350
```

Measured delta from the recorded receipt: `1350 - 1556 = -206` archives. The live observation is the count of matching direct-child cache entries; this was not a signature or package-integrity audit.

## Verdict and disposition

**DISCREPANCY** against the recorded 1,556 count: the live cache now contains 1,350 by both enumerations. The receipt's 1,556 remains the historical, dated observation; it is not the current count.

**Disposition (b), adjudication/no corpus edit:** this number is a retention-varying inventory count, not a capability claim. Preserve the historical receipt; record the re-derivation and delta here rather than changing corpus knowledge. The r5 count was not used as evidence for this measurement.
