# EX-7 — C2 freshness receipt: pacman archive cache

**Item under test:** `PROVINCE.md:50` states that `/var/cache/pacman/pkg` currently contains 1,350 `.pkg.tar.zst` archives, each paired with a `.sig` sidecar. That recorded figure is the comparison target, not evidence for this receipt.

**Fresh measurement:** 2026-10-19T16:24:05-03:00. I enumerated regular, non-symlink files in the cache directory and checked sidecar basenames directly:

```bash
python3 - <<'PY'
import os
root = '/var/cache/pacman/pkg'
with os.scandir(root) as entries:
    names = {entry.name for entry in entries if entry.is_file(follow_symlinks=False)}
archives = sorted(name for name in names if name.endswith('.pkg.tar.zst'))
signatures = {name for name in names if name.endswith('.pkg.tar.zst.sig')}
missing = [name for name in archives if name + '.sig' not in names]
orphaned = sorted(name for name in signatures if name[:-4] not in archives)
print(f'archive_files={len(archives)}')
print(f'signature_files={len(signatures)}')
print(f'missing_sidecars={len(missing)}')
print(f'orphaned_sidecars={len(orphaned)}')
if missing:
    print('missing=' + ','.join(missing))
if orphaned:
    print('orphaned=' + ','.join(orphaned))
PY
date -Is
```

Exact output:

```text
archive_files=1350
signature_files=1350
missing_sidecars=0
orphaned_sidecars=0
2026-10-19T16:24:05-03:00
```

**Verdict: VERIFIED / REPRODUCED.** The fresh archive count is 1,350 (delta 0 from `PROVINCE.md:50`); all 1,350 counted archives have a same-basename `.sig` file, with no missing or orphaned sidecars. Disposition: retain the current count; no correction indicated.

**Scope limit:** This checks directory-entry counts and basename pairing only. It does not cryptographically verify signatures or validate archive contents.