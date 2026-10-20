# Final Census Recorder — D5

Axes: calibration (revision/worktree state), coverage (both census validators), depth (retained stdout digest and UTC timestamp).

**Observation.** Added `W20/tools/final-census.py`. It requires `--root` and `--out-dir`, resolves the lane worktree root, reads `refs/heads/main`, and refuses tracked modifications with exit 2 before running commands (`W20/tools/final-census.py:85-90,130-151`). It records the C1 invocation and the fixed fleet `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` invocation in `argv` (`:153-160`), concatenates their stdout in execution order into `final-census.stdout`, and records its SHA-256, root-relative path, aggregate status, `worktree_clean` (porcelain contains only the two generated output files), revision, and write-time UTC timestamp in `final-census.json` (`:161-191`).

**Observation.** `--selftest` creates and removes a `tempfile.mkdtemp()` fixture Git repo outside any worktree. It covers the clean record/digest, an untracked-file cleanliness report, and tracked-change refusal (`:215-293`). Selftest command returned exit 0; exact last line: `SELFTEST: CLEAN cases=3`. This invocation preceded the final guard tightening at `:85-90,143`; it broadens refusal to all tracked paths (rather than exempting tracked output paths). The existing tracked-change selftest case exercises a non-output tracked path and remains applicable; the requested once-only selftest was not repeated.

**Commands and exits.**
- `test ! -e /tmp/kr20-FinalCensusRecorder && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-FinalCensusRecorder && git -C /tmp/kr20-FinalCensusRecorder checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-FinalCensusRecorder rev-parse HEAD` — exit 0; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `mkdir -p /tmp/kr20-FinalCensusRecorder/.ufo/waves/round-20/tools` — exit 0.
- `python3 -I -B .ufo/waves/round-20/tools/final-census.py --selftest` (cwd `/tmp/kr20-FinalCensusRecorder`) — exit 0; last line as above.
- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-FinalCensusRecorder add -A && git -C /tmp/kr20-FinalCensusRecorder diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/FinalCensusRecorder.patch && git -C /tmp/kr20-FinalCensusRecorder diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0.

Patch stat: `.ufo/waves/round-20/tools/final-census.py | 328 ++++++++++++++++++++++++++++++` (1 file changed, 328 insertions).

**Limitations.** Production census commands were not run here; selftest substitutes fixture scripts. LSP was unavailable in the supplied tool inventory. No tools were installed. No blockers.