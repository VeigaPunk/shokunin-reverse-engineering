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

Report: .ufo/waves/round-20/w1/RoutedR19Tool.md
