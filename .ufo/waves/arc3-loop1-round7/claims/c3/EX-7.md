# EX-7 — C3 calibration: pacman package-cache count

## Finding

**Verdict: REPRODUCED / DISCREPANCY.** I independently counted the live cache as **1,350** regular `.pkg.tar.zst` files using two methods; both returned the same result. Against the original receipt's recorded **1,556**, the measured delta is **−206**. Thus `PROVINCE.md:50`'s unqualified current-sounding count of 1,556 is stale if it describes the live cache.

The frozen C3 claim notes an r5 re-measure of 1,350 (`.ufo/waves/arc3-loop1-round7/claims-frozen.md:58-60`). That prior-round value is not evidence for this finding: the two commands below are this seat's independent live re-derivation. The live result happens to agree with the frozen note.

## First-hand measurement

From the repository worktree at HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804` (`git rev-parse HEAD`):

```text
$ find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf 'x' | wc -c
1350

$ python3 -c 'from pathlib import Path; p=Path("/var/cache/pacman/pkg"); print(sum(1 for x in p.iterdir() if x.is_file() and x.name.endswith(".pkg.tar.zst")))'
1350

$ python3 -c 'print(1350 - 1556)'
-206
```

Both enumerators count direct-child regular files matching the suffix. The arithmetic compares this measurement with the historical receipt; it is not a second cache measurement.

## Recorded comparison and disposition

- Historical baseline: `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` records 1,556 archives and the original count recipe. `PROVINCE.md:50` repeats 1,556 as the corpus count. These are the recorded comparison values, not current-state evidence.
- Current measurement: 1,350; delta from that receipt: −206.
- Scope of observation: filenames/count only. This run did **not** re-check signatures, signature coverage, or total bytes.
- Disposition: append-only erratum is warranted for any current-state presentation of the count. Preserve 1,556 as the historical receipt value; describe the live count as retention-varying inventory, not as a capability claim. This seat's write boundary permits only its own wave artifact, so the proposed erratum is recorded here for reconciliation and was **not** applied to the corpus or `PROVINCE.md`.

Proposed append-only erratum text:

> Live re-count: `/var/cache/pacman/pkg` contains 1,350 direct-child regular `*.pkg.tar.zst` files (independently counted with `find` and Python `pathlib`); this is 206 fewer than the original receipt's 1,556. The cache count is retention-varying inventory. The original count remains a historical snapshot and does not establish current signature coverage or archive bytes.
