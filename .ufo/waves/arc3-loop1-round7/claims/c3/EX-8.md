# EX-8 — C3 pacman archive-count calibration

**Verdict:** DISCREPANCY if the receipt's count is read as current; the dated historical snapshot is VERIFIED. **Disposition:** no corpus edit. This count is a retention-varying inventory observation, not a capability claim; preserve the receipt as an as-of record and record this adjudication.

## First-hand re-derivation

Measured the live `/var/cache/pacman/pkg/` immediately before this artifact was written (`2026-10-19T14:19:05-03:00`). Two independent enumerations agree:

```text
$ python3 - <<'PY'
from pathlib import Path
cache = Path('/var/cache/pacman/pkg')
files = sorted(p for p in cache.iterdir() if p.is_file() and p.name.endswith('.pkg.tar.zst'))
print(f'cache={cache}')
print(f'archive_count={len(files)}')
print(f'first={files[0].name if files else "<none>"}')
print(f'last={files[-1].name if files else "<none>"}')
PY
cache=/var/cache/pacman/pkg
archive_count=1350
first=1password-beta-8.12.42_34.BETA-1-x86_64.pkg.tar.zst
last=zydis-4.1.1-2-x86_64.pkg.tar.zst

$ bash -c 'shopt -s nullglob; files=(/var/cache/pacman/pkg/*.pkg.tar.zst); printf "archive_count=%d\n" "${#files[@]}"'
archive_count=1350
```

The recorded baseline is `1556` `.pkg.tar.zst` files, explicitly dated `verified-at: 2026-10-13` (`corpus/knowledge/2026-10-13-pacman-packages.md:21-25`). The live count is therefore `1350 - 1556 = -206` archives relative to that dated receipt. The live count above is this seat's fresh measurement; no earlier seat's count is used as evidence.

## Adjudication

The `1556` figure remains valid as the receipt's 2026-10-13 inventory snapshot, not as a current count. Its variance is explained by a mutable package-cache inventory; it does not change the available archive-analysis capability. No edit to the corpus receipt is warranted under C3's capability-class/no-edit disposition. This measurement establishes only the current archive count; it does not re-verify matching signature coverage, cache size, or signatures.
