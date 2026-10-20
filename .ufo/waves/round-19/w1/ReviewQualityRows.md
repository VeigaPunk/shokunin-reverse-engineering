# QUALITY rows and prefix-control sizes

Axes: **calibration**, **freshness**, **depth**.

## Observations

- The pinned baseline is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (`2026-10-20 15:28:02 -0300`, `round-18 verifier spot-check (integrator, hyaku): non-author admit/reject`). The measured files are read from that revision, not the worktree. Source anchors: `corpus/QUALITY.md:9-31` (admission criteria 1–21), `corpus/QUALITY.md:35-42` (weak-material signals 1–6), `LOG.md:2169-2174` (round-18 log heading and records), `SCORECARD.md:2442-2447` (round-18 measured-record section).
- Requested digest command:
  ```sh
  git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:corpus/QUALITY.md | grep -E '^\| *([1-9]|1[0-9]|2[0-1]) *\|' | sha256sum
  ```
  Output: `837059236434bc08b314160a6962adc6d7f29c2222246b67e72bee07e27ea782  -`; pipeline exit **0** (component statuses `0 0 0`).
- Matched-row count command: `git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:corpus/QUALITY.md | grep -E '^\| *([1-9]|1[0-9]|2[0-1]) *\|' | wc -l` → `27`; pipeline exit **0** (component statuses `0 0 0`).
- Prefix-control byte-count commands and results:
  - `git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:LOG.md | wc -c` → **146631 bytes**, exit **0** (component statuses `0 0`).
  - `git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:SCORECARD.md | wc -c` → **174530 bytes**, exit **0** (component statuses `0 0`).
- Independent blob-size check also returned `146631` and `174530`: `git --no-optional-locks cat-file -s 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:LOG.md` (exit 0) and `git --no-optional-locks cat-file -s 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:SCORECARD.md` (exit 0).

## Inference

The supplied pattern is not scoped to the admission-criteria table: it matches its 21 numbered rows and the six numbered weak-signal rows, hence the 27-row count and digest scope. No inference is made about what file-size thresholds a downstream prefix control applies.
