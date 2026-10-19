# SC-2 — C3 calibration: pacman archive inventory

## Re-derived quantity

Measured the current top-level `*.pkg.tar.zst` path count in `/var/cache/pacman/pkg/` on the live host. This was a fresh measurement; no prior-round current count was used as evidence.

Commands:
```bash
python3 -c 'from pathlib import Path; p=Path("/var/cache/pacman/pkg"); matches=list(p.glob("*.pkg.tar.zst")); print("python_glob_path_count=%d" % len(matches)); print("python_non_file_matches=%d" % sum(not f.is_file() for f in matches))'
bash -c 'shopt -s nullglob; files=(/var/cache/pacman/pkg/*.pkg.tar.zst); printf "bash_glob_path_count=%d\n" "${#files[@]}"'
```

Exact stdout:
```text
python_glob_path_count=1350
python_non_file_matches=0
bash_glob_path_count=1350
```

The independent Python and Bash glob counts agree; the Python check found zero matches that are not files.

## Receipt comparison and verdict

The historical record states 1,556 `.pkg.tar.zst` archives in `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` (the measured count is at `:22`, with its original glob recipe at `:23`). `PROVINCE.md:50` carries the same count as a summary. These are historical baselines, not evidence for the live result above.

**DISCREPANCY — current inventory:** 1,350 now versus the recorded 1,556, a delta of **−206 archive paths**. This re-derives only the archive-path count; it does not remeasure signature coverage, archive integrity, or cache size.

## Disposition

**Recorded adjudication; no corpus edit.** The changing number is cache inventory, not a REA capability. The original entry is an as-of observation (verified 2026-10-13); a lower live count is consistent with retention/eviction and does not invalidate that historical observation or change REA/tool capability. Keep the source corpus read-only; use a fresh measurement whenever a current inventory is needed.
