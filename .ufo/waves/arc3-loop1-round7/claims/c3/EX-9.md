# EX-9 — C3 calibration: pacman package-cache inventory

**Verdict:** REPRODUCED — the live `.pkg.tar.zst` count is 1,350. Relative to the 1,556-file value in the original receipt, the live inventory is lower by 206 files; presenting 1,556 as the current count would be a DISCREPANCY.

## First-hand re-derivation

Read-only host measurement at `2026-10-19T14:19:09-03:00`:

```sh
date -Is
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf '%f\n' | wc -l
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.sig' -printf '%f\n' | wc -l
shopt -s nullglob
archives=(/var/cache/pacman/pkg/*.pkg.tar.zst)
printf 'glob_count=%d\n' "${#archives[@]}"
```

Output:

```text
2026-10-19T14:19:09-03:00
1350
1350
glob_count=1350
```

The two independent archive counts agree (file-only `find` and shell glob); the detached-signature count is also 1,350. No cache files were changed and no scratch files were needed.

## Comparison and disposition

The original receipt states 1,556 cached archives and is marked `verified-at: 2026-10-13` (`corpus/knowledge/2026-10-13-pacman-packages.md:21-25`). The first-hand live count is therefore **−206** versus that dated snapshot. This establishes retention drift in the inventory, not a change to the underlying package-inspection capability.

**Disposition — recorded adjudication, no corpus edit:** keep the corpus entry as its dated 2026-10-13 observation rather than replacing a historical count with another retention-sensitive number. This is not a claim that 1,556 remains the live count. `PROVINCE.md:50` still phrases 1,556 without an explicit as-of date; it is discrepant if interpreted as a current inventory. That separate source was not changed under this seat's write fence.

Evidence is the command and output above; no prior-round measurement is used as evidence for the live value.
