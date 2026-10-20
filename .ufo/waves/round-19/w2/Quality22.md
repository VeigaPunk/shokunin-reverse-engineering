# QUALITY #22 — scoped review

**Axes reviewed:** calibration (lesson grounding), freshness (revision/input binding), depth (what the red/green evidence actually proves).

**Snapshot:** baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; `refs/heads/main` observed at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. The working tree also had an uncommitted edit to `corpus/lessons/round-19.md` and an untracked `.ufo/waves/round-19/w2/` directory at the status check; findings about the committed change below use the observed main snapshot. `corpus/QUALITY.md` had no working-tree diff.

## Findings (by severity)

### Low — the lesson misidentifies the green run's input file

**Observation:** `corpus/lessons/round-19.md:27` says the green run used `r18-dead-seats.json` causes. The retained green result instead records its actual `causes` input as `evidence/wave-outcomes/r18-w2-causes.json` at `.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-outcomes.json:3-8`; it records the cause-file digest as `235c5fb6d9760e4025c963ebc7ed25f9bdffe3246563b62a2ca6d9ab5f76afd2`. The separately retained `.ufo/waves/round-19/evidence/r18-dead-seats.json` is the richer per-seat source record (source pointers at lines 34, 46, 58, and 70), while `r18-w2-causes.json:1-6` is the four-string map consumed by the green run. The digest check below matches the output record's recorded digest.

**Inference:** This is a provenance-label mismatch, not evidence that the green outcome or the four cause strings are false. Make the lesson distinguish the green input map (`r18-w2-causes.json`) from its provenance source (`r18-dead-seats.json`); otherwise the exact recorded run is not the file named in the lesson.

## Evidence and checks

- `corpus/QUALITY.md:32` adds one criterion, #22, requiring an observation cutoff, separate terminal/not-yet-returned dispositions, and retained per-seat causes or explicit unknowns. Its cited R18 defect is present at `corpus/lessons/round-18-verifier-spotcheck.md:146,197`; `corpus/lessons/round-19.md:84` also records the mistake and its red/green correction.
- Exact retained red: `.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-red.stdout:1-4` reports 98 seats, 94 reports, 4 missing and 4 uncaused, naming all four; `r18-w2-red.exit:1` records exit 1.
- Exact retained green: `r18-w2-green.stdout:1-4` reports the same 98/94/4 population, 4 causes and 0 uncaused; `r18-w2-green.exit:1` records exit 0. The green JSON at `r18-w2-outcomes.json:15-25` agrees on the counts and missing names. The retained outputs therefore support the narrow red/green claim.
- Recorded reproduction in `.ufo/waves/round-19/w1/WaveOutcomesTool.md:77-89`: `printf '{}\n' > /tmp/kr19wo-empty-causes.json` → exit 0; then `cd /tmp/kr19-WaveOutcomesTool && python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --registration .ufo/waves/round-18/wave2-registration.json --report-dir .ufo/waves/round-18/w2 --causes /tmp/kr19wo-empty-causes.json --out /tmp/kr19wo-r18w2.json` → exit 1, with 98/94/4 and the four names. This is the retained acceptance command, not a command rerun for this review; its temporary `--out` path differs from the integrated red stdout's `/tmp/kr19-wo-red.json` at `r18-w2-red.stdout:5`.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks rev-parse refs/heads/main` → `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks diff --unified=0 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- corpus/QUALITY.md` → exit 0; diff is one insertion at line 32 and zero deletions. A read-only Git-object comparison of the numbered criterion lines found rows 1–21 byte-identical (21/21; SHA-256 of their concatenation `d8a1077cefb00086179bd235d0729f247d8faacf8c74d070fdea8da3041ad73d`), and exactly one row #22; comparison exit 0. The underlying `git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:corpus/QUALITY.md` and `git show refs/heads/main:corpus/QUALITY.md` each exited 0.
- `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-causes.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/wave2-registration.json` → exit 0; digests `235c5fb6d9760e4025c963ebc7ed25f9bdffe3246563b62a2ca6d9ab5f76afd2` and `4e43ca53a889c50c862560d512c11079d9bf93fbb9f539267137427778e0892f`, respectively, matching `.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-outcomes.json:4,8`.

## Residual risk and verification gaps

- The green result proves only the tool's narrow rule: every missing report has a non-empty cause. The green record has `cause_sources: {}` (`r18-w2-outcomes.json:29`); `WaveOutcomesTool.md:139-141` explicitly says the tool does not verify cause provenance. Thus this red/green pair does **not** by itself establish QUALITY #22's stronger cutoff/source-pointer requirements. Those need the separate per-seat source record and manual admission check; do not describe the green exit as a full #22 verifier.
- LSP was unavailable: `read xd://lsp` returned “No such tool.” No LSP status, references, definition, or diagnostics requests were possible. Literal search was used only to locate references; it is not semantic proof.
- No mutation tests, builds, or broad tests were run in this review; no tools were installed or updated. 