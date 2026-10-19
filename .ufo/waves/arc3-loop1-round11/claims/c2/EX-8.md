# EX-8 — C2 freshness receipt: pacman package cache

**Verdict: REPRODUCED.** `PROVINCE.md:50` records a dated 2026-10-13 snapshot of 1,556 `.pkg.tar.zst` archives and a later/current count of 1,350. I independently enumerated the configured cache on 2026-10-19: 1,350 archives, all with a same-name `.sig` sidecar. Against the dated snapshot, the measured count delta is `1,350 - 1,556 = -206` archives. The present tally agrees with the row's 1,350 value; the historical snapshot is not a current-count claim.

## First-hand measurement

Commands run:

```sh
$ pacman-conf CacheDir
/var/cache/pacman/pkg/
$ python3 -c 'from datetime import datetime,timezone; from pathlib import Path; p=Path("/var/cache/pacman/pkg"); entries={x.name for x in p.iterdir() if x.is_file()}; archives={n for n in entries if n.endswith(".pkg.tar.zst")}; sigs={n[:-4] for n in entries if n.endswith(".pkg.tar.zst.sig")}; print("measured_at_utc="+datetime.now(timezone.utc).isoformat(timespec="seconds")); print("cache="+str(p)); print("pkg_tar_zst_archives="+str(len(archives))); print("archives_with_matching_sig="+str(len(archives & sigs))); print("archives_missing_sig="+str(len(archives - sigs))); print("orphan_pkg_tar_zst_sigs="+str(len(sigs - archives)))'
measured_at_utc=2026-10-19T19:22:29+00:00
cache=/var/cache/pacman/pkg
pkg_tar_zst_archives=1350
archives_with_matching_sig=1350
archives_missing_sig=0
orphan_pkg_tar_zst_sigs=0
```

## Disposition

Retain the 1,556 value only as the dated snapshot and the 1,350 value as a cache count observed at the stated measurement time. No correction to the current count is indicated by this measurement. Sidecar matching checks filename presence only; this receipt does not cryptographically verify signatures or package contents. No files outside this EX-8 artifact were changed.
