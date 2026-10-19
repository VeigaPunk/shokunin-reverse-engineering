# RV-3 — C3 calibration re-derivation

## Item and verdict

**Item:** live `/var/cache/pacman/pkg/*.pkg.tar.zst` inventory count.

**Verdict:** **REPRODUCED** for the live count; **DISCREPANCY** against the historical receipt. The corpus receipt records 1,556 archive paths (`corpus/knowledge/2026-10-13-pacman-packages.md:21-25`). A fresh local glob count returned 1,350, a delta of -206 from that receipt.

## First-hand measurement

Command run in the current host environment:

```bash
shopt -s nullglob; files=(/var/cache/pacman/pkg/*.pkg.tar.zst); live=${#files[@]}; printf 'live_pkg_tar_zst=%d\nrecorded_receipt=1556\ndelta=%+d\n' "$live" "$((live - 1556))"
```

Exact stdout:

```text
live_pkg_tar_zst=1350
recorded_receipt=1556
delta=-206
```

The 1,556 comparison value is the historical corpus receipt at `corpus/knowledge/2026-10-13-pacman-packages.md:22-23`; this measurement does not use another seat's or round's re-measurement as evidence.

## Disposition

Record an **append-only inventory erratum**: the 1,556 value remains a valid historical snapshot, but the live cache currently has 1,350 matching archive paths (-206). This is a retention-varying inventory count, not a capability invariant; preserve the original entry and append this correction when corpus-write scope permits. This wave artifact is the record for this seat; the canonical corpus was not modified because this seat's write scope is limited to its own artifact directory.

Scope limitation: only the `.pkg.tar.zst` path count was re-derived. The historical entry's matching `.sig` count, total byte size, and sampled signature/integrity claims were not rechecked and are not endorsed by this measurement.
