# Routed R19 counter — author report

Axes: calibration (C1), coverage, depth. **Observation:** the scoped patch adds `.ufo/waves/round-20/tools/routed-r19.py`; it is the only implementation file staged (dual-name gate and 11 item IDs at `tools/routed-r19.py:54`, `:198-204`; immutable Git reads and revexec preflight at `:120-147`, `:227-247`; checks at `:339-1009`). It emits the requested JSON and `--strict` uses `open_count`; selftest fixtures keep token-only claims open (`:923-1034`, `:1058-1059`).

## Exact retained evidence

**Observation — one requested selftest invocation** (run before the later D1/D6e sandbox-path adjustment; no second selftest was run):

```text
SELFTEST_CASE: CLEAN case=token_only_closures_stay_open
SELFTEST_CASE: CLEAN case=missing_name_counts_open
SELFTEST_CASE: CLEAN case=strict_open_exit
SELFTEST_CASE: CLEAN case=ast_revexec_only
SELFTEST: CLEAN cases=4
exit=0
```

**Observation — final baseline measurement** (post-adjustment): exit 0, `open_count=11`, `named_open=11`, `substance_open=11`.

```json
{
  "items": [
    {"id":"D1","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; custody-pair selftest lacks the worktree-refusal or cleanup fixture"},
    {"id":"D2","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D3","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D4","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D5","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; final-census.json absent or invalid at REV"},
    {"id":"D6a","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D6b","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV for AST self-check"},
    {"id":"D6c","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D6d","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"},
    {"id":"D6e","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; wave-outcomes selftest lacks the seat_named_causes fixture"},
    {"id":"D6f","named":false,"substance":false,"why":"SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"}
  ],
  "named_open": 11,
  "open_count": 11,
  "rev": "14f0260ad319ecc26994381b2415d5a999003375",
  "substance_open": 11
}
```

The final D1 check uses a worktree refusal plus REV's `cleanup_after_run` selftest case and invokes the outside-worktree scratch as `.` inside revexec's isolated work directory (`:268-286`, `:339-378`). D6e binds the `seat_named_causes` selftest case in REV source and requires that selftest to be CLEAN (`:268-286`, `:862-881`). D4 archive extraction creates symlinks without following them (`:516-559`).

## Commands and exits

- `if test -e /tmp/kr20-RoutedR19Tool-2; then printf 'clone_exists\n'; else git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-RoutedR19Tool-2 || exit $?; fi && git -C /tmp/kr20-RoutedR19Tool-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-RoutedR19Tool-2 rev-parse HEAD` — exit 0; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `mkdir -p /tmp/kr20-RoutedR19Tool-2/.ufo/waves/round-20/tools` — exit 0.
- `python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --selftest; status=$?; printf 'exit=%s\n' "$status"; exit "$status"` — exit 0; exact result above.
- `python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --root /tmp/kr20-RoutedR19Tool-2 --rev 14f0260ad319ecc26994381b2415d5a999003375; status=$?; printf 'exit=%s\n' "$status"; exit "$status"` — first run exit 0, `open_count=11`; D4 extraction reported the baseline archive's absolute symlink `.ufo/waves/arc3-loop1-round4/claims/c3/EX-25/fixtures/scratch/alias-1.conf`. Safe non-following extraction replaced the initial `tarfile` data filter.
- Same baseline command — second run exit 0, `open_count=11`.
- Same baseline command — final run exit 0; exact JSON above.
- `git -C /tmp/kr20-RoutedR19Tool-2 add -- .ufo/waves/round-20/tools/routed-r19.py && mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-RoutedR19Tool-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/RoutedR19Tool.patch && git -C /tmp/kr20-RoutedR19Tool-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; initial stat 1 file changed, 1068 insertions.
- `git -C /tmp/kr20-RoutedR19Tool-2 add -- .ufo/waves/round-20/tools/routed-r19.py && git -C /tmp/kr20-RoutedR19Tool-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/RoutedR19Tool.patch && git -C /tmp/kr20-RoutedR19Tool-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; final stat ` .ufo/waves/round-20/tools/routed-r19.py | 1063 +++++++++++++++++++++++++++++++` (1 file changed, 1063 insertions).

## Risks / blockers

**Observation:** baseline 14f0260 has no round-20 counter/revexec; all 11 remain open, so no future-REV tool closures could be exercised here. D1's residue assertion is checked through the REV selftest's named cleanup fixture because revexec permits writes only in its isolated work directory; D6e likewise uses the required named selftest case. The selftest was not rerun after those revision-measurement refinements, honoring the single-run instruction; the final baseline invocation parsed and measured the updated script. No installs/updates were made. LSP was unavailable in the mounted tool inventory; no LSP operations were performed.

## Integration fix

Base: fresh clone `/tmp/kr20-RoutedR19Fix` at `aad0869012eef957f22e32b748833cc7370d6515`. The patch changes only `.ufo/waves/round-20/tools/routed-r19.py`; final diff stat: 1 file, 136 insertions, 88 deletions. Dual-name counting and strict exit remain unchanged. D1 now finds the real `_cmd_selftest` cases and reports live status even when the sandboxed outside-scratch selftest fails (`:344-389`). D2 uses the revision tool's `future_line_flagged` and `past_line_clean` selftest cases after checking the baseline defect (`:405-426`). D3 reads the actual arm/check schema, compares the arm carrier paths with the header-bearing TSV, and runs a fresh `check` through revexec (`:477-533`). D6a matches round-17 `verify.py` and round-18 `tools/revpin.py` (`:661-703`). D6f counts `jj_` IDs from the selftest function AST and passes the explicit local `jj` path (`:901-953`).

Observation: both integration-clone selftest invocations were CLEAN, 4 cases, exit 0 (the later run was after the final diagnostic refinement). Baseline `14f0260ad319ecc26994381b2415d5a999003375` remained open 11/11 (named 11, substance 11), exit 0.

Observation: final `--live` measurement at `aad0869012eef957f22e32b748833cc7370d6515` was open 11, named-open 11, substance-open 4, exit 0. Item lines:

```text
D1 named=false substance=false — outside-workdir selftest exit 1; live status exit 0, no nested .git (12 status rows)
D2 named=false substance=true
D3 named=false substance=true
D4 named=false substance=false — c1-census exit 2, ANCHOR-FAIL: {'devin': None, 'omp': None, 'kimi': None}
D5 named=false substance=false — final-census.json absent
D6a named=false substance=true
D6b named=false substance=true
D6c named=false substance=true
D6d named=false substance=true
D6e named=false substance=true
D6f named=false substance=false — jj_ source IDs 2 vs baseline 0; selftest exit 1, OSError [Errno 30] Read-only file system at /tmp/jj-red-before-selftest-...
```

Measured non-counter blockers, not waived closures: D1's `cleanup_after_run` case calls custody selftest with a nested scratch path under `/tmp`; custody-pair intentionally rejects `/tmp` as EDQUOT, while revexec only permits writes in its `/tmp/revexec-work-*` directory. The direct `/var/tmp` success reported by L1 is not reproducible under that sandbox. D4's census computes its client config/cache paths from `HOME`; revexec sets `HOME` to the empty work directory, producing the quoted `ANCHOR-FAIL` instead of the L1's direct-worktree PASS. D6f's fixed selftest hard-codes `tempfile.mkdtemp(..., dir="/tmp")`; passing `/home/vgpnk/.local/bin/jj` does not overcome revexec's read-only `/tmp`. These are tool/sandbox integration constraints; I did not alter the counter to certify them closed. D5 remains open as expected until its final record exists; names remain open pending SCORECARD/lesson rows.

Commands/exits for the integration fix:

`if test -e /tmp/kr20-RoutedR19Fix; then printf 'clone_exists\n'; else git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-RoutedR19Fix || exit $?; fi && git -C /tmp/kr20-RoutedR19Fix checkout -q --detach aad0869012eef957f22e32b748833cc7370d6515 && git -C /tmp/kr20-RoutedR19Fix rev-parse HEAD` — exit 0; observed base `aad0869012eef957f22e32b748833cc7370d6515`.

`python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --selftest; status=$?; printf 'exit=%s\n' "$status"; exit "$status"` — run twice, both exit 0; final output `SELFTEST: CLEAN cases=4`.

`python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --root /tmp/kr20-RoutedR19Fix --rev 14f0260ad319ecc26994381b2415d5a999003375; status=$?; printf 'exit=%s\n' "$status"; exit "$status"` — exit 0; 11 open (named 11, substance 11).

`python3 -I -B /tmp/kr20-RoutedR19Fix/.ufo/waves/round-20/tools/routed-r19.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev aad0869012eef957f22e32b748833cc7370d6515 --live; status=$?; printf 'exit=%s\n' "$status"; exit "$status"` — run twice, both exit 0; final item lines above.

`git -C /tmp/kr20-RoutedR19Fix add -- .ufo/waves/round-20/tools/routed-r19.py && mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-RoutedR19Fix diff --cached --binary aad0869012eef957f22e32b748833cc7370d6515 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/RoutedR19Fix.patch && git -C /tmp/kr20-RoutedR19Fix diff --cached --stat aad0869012eef957f22e32b748833cc7370d6515` — exit 0; 1 file changed, 136 insertions, 88 deletions.

Report: .ufo/waves/round-20/w1/RoutedR19Tool.md

