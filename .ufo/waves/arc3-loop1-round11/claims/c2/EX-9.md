# EX-9 — C2 freshness receipt

**Selection:** live pacman package-cache inventory in `/var/cache/pacman/pkg`.
**Observation:** read-only, 2026-10-19. The paths under the cache were only enumerated; no packages were opened, verified, or modified.

## Re-derived result

- **Archive count — REPRODUCED:** 1,350 immediate regular files named `*.pkg.tar.zst`.
- **Signature sidecars — REPRODUCED:** 1,350 immediate regular files named `*.pkg.tar.zst.sig`; exact-name pairing found 0 missing and 0 orphan sidecars.
- **Delta/disposition:** 0 versus the live 1,350 count recorded in `PROVINCE.md:50`; −206 versus the 1,556 count explicitly labeled as the 2026-10-13 snapshot there. The cache count is retention-varying: retain the historical snapshot as dated, with no correction to the current 1,350 figure. The historical 1,556 directory state is **UNVERIFIABLE from today's cache**; it is used only as the documented comparison baseline, not as fresh evidence.

## First-hand command evidence

```text
$ find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' | wc -l
1350
$ find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst.sig' | wc -l
1350
```

A separate Python enumeration checked exact sidecar-name correspondence:

```text
$ python3 -c 'from pathlib import Path; p=Path("/var/cache/pacman/pkg"); entries=[x for x in p.iterdir() if x.is_file()]; archives={x.name for x in entries if x.name.endswith(".pkg.tar.zst")}; signatures={x.name for x in entries if x.name.endswith(".pkg.tar.zst.sig")}; missing=sorted(name+".sig" for name in archives if name+".sig" not in signatures); orphan=sorted(name for name in signatures if name[:-4] not in archives); print(f"cache={p}"); print(f"archive_files={len(archives)} signature_sidecars={len(signatures)} missing_sidecars={len(missing)} orphan_sidecars={len(orphan)}"); print(f"delta_vs_recorded_live_1350={len(archives)-1350:+d}; delta_vs_recorded_snapshot_1556={len(archives)-1556:+d}")'
cache=/var/cache/pacman/pkg
archive_files=1350 signature_sidecars=1350 missing_sidecars=0 orphan_sidecars=0
delta_vs_recorded_live_1350=+0; delta_vs_recorded_snapshot_1556=-206
```

**Baseline paths (comparison only):** `PROVINCE.md:50`; `corpus/knowledge/2026-10-13-pacman-packages.md:21-26,73-83`. The live counts and deltas above come from this seat's commands, not a prior seat's output. This inventory does not establish cryptographic signature validity or archive integrity.
