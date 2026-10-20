HOLDS

# MisrootSweep — round-18 wave 2 (falsify): fleet-root untracked sweep

Seat KaidokuR18.MisrootSweep · 2026-10-20 · Read-only. No tool installs (git/grep/sha256sum preinstalled; no pacman transaction run). No REA/Ghidra run, no carrier execution, no subagents, no lane or fleet writes except this report.

## Target commands (pasted, with exit codes)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain          # EXIT=0
 M .ufo/watchdog.log
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline

$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all   # EXIT=0
# identical list — no collapsed untracked directories anywhere in the fleet repo

$ cd /home/vgpnk/Projects/shokunin && grep -lE 'kaidoku|round-18' \
    .ufo/state/kaidoku.report-baseline .ufo/state/kake.report-baseline \
    .ufo/state/kama.report-baseline .ufo/state/mado.report-baseline \
    .ufo/state/mori.report-baseline .ufo/state/souji.report-baseline \
    .ufo/state/tabi.report-baseline .ufo/state/tameshi.report-baseline \
    .ufo/state/tsukuroi.report-baseline                            # no output, EXIT=1
# grep -l exit 1 = zero files matched; case-insensitive re-sweep also zero matches
```

## Findings

- **F1 (observation):** Zero untracked fleet-root files have *content* naming `kaidoku` or `round-18`. The prescribed `grep -lE 'kaidoku|round-18'` over all 9 untracked files returns an empty list (EXIT=1); a case-insensitive sweep matches nothing either. Repro: command block above.
- **F2 (observation):** The 9 untracked files are one line each, `<round> <sha256>`, all with digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` = `sha256("")` (verified: `printf '' | sha256sum` → EXIT=0). Rounds: kaidoku=18, kake=21, kama=17, mado=18, mori=16, souji=17, tabi=17, tameshi=17, tsukuroi=17.
- **F3 (observation):** The writer is the fleet driver, not a seat. `scripts/shokunin-watchdog.sh:31-32` documents the format ("`.ufo/state/<lane>.report-baseline` holds \"round SHA256\" for the report bytes captured immediately before launch"), `:122` and `:146` are the write/read sites. The script is fleet-tracked and unmodified (status shows only `watchdog.log` as `M`), so its working-tree line numbers equal fleet-HEAD line numbers.
- **F4 (observation):** The only other dirty file, `.ufo/watchdog.log`, is *tracked*-modified — outside the target's untracked grep list. Its uncommitted delta is 19 appended driver lines only (`git diff --stat` → "19 insertions(+)"), including `2026-10-20T12:07:53-03:00 launch kaidoku round=18 pgid=4070059 driver=hyaku-inline attempt=1`. Driver bookkeeping, no seat content.
- **F5 (observation, filename vs content):** Filename-level, exactly one untracked file's *name* contains "kaidoku" (`.ufo/state/kaidoku.report-baseline`); its content is `18 e3b0c442…` — the bare round number `18`, not the string `round-18`. The target's content grep is therefore genuinely empty, not an artifact of case or whitespace.
- **F6 (inference, corroborated):** These baselines are expected per-round driver state, not misrooted wave artifacts. The identical signature was recorded and cleared by prior rounds' misroot sweeps: `.ufo/reports/round-16/souji.md:77`, `.ufo/reports/round-16/tameshi.md:105`, `.ufo/reports/round-17/mado.md:149-152` ("shows only driver state (`.ufo/state/*.report-baseline`, watchdog.log) … no seat file at the fleet root"). All three are fleet-tracked and unmodified, so their line numbers are valid at fleet HEAD.
- **F7 (observation):** The lane is invisible to fleet status by design: fleet `.gitignore:1` is `*-shokunin/` (`git check-ignore -v kaidoku-shokunin` → `.gitignore:1:*-shokunin/	kaidoku-shokunin`, EXIT=0; `git ls-files -- kaidoku-shokunin` → 0 files). Fleet `.ufo/waves/round-18/` does not exist (`test -d` → DIR_NO; tracked count 0) — all round-18 wave content lives in the lane repo, none at the fleet root.

## Wave-1 claims touched

None broken, none confirmed. `claims.json` at REV is byte-identical to the working tree (`git -C kaidoku-shokunin show b2aad08…:.ufo/waves/round-18/claims.json | diff - <worktree>` → EXIT=0; lane HEAD = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`): C1 (:10-14), C2 (:17-21), C3 (:24-28), amendments (:33-42) make no fleet-root or misroot claim — all three are lane-internal tool claims. This sweep tests the standing per-round fleet-hygiene expectation, which holds.

## Anchors at REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94

- `.ufo/waves/round-18/claims.json:3` (`"lane": "kaidoku"`), `:33-42` (amendments) — cited at REV via `git show REV:path`, verified byte-identical to the working tree.
- The 9 untracked fleet files have no REV anchor: untracked in the fleet repo and absent from the lane repo (fleet-ignored). Their content is cited from the working tree with reproducing commands above; the fleet working tree is clean except `watchdog.log` (status EXIT=0), so cited fleet-file line numbers equal fleet HEAD.

## Verdict rationale

HOLDS: the fleet root carries no untracked seat strays whose content names kaidoku or round-18; the only untracked files are the driver's nine per-lane report baselines (content = round number + empty digest), matching the documented driver format (`scripts/shokunin-watchdog.sh:31-32,122,146`) and three prior rounds' sweeps. No wave-1 claim is contradicted by fleet-root evidence.
