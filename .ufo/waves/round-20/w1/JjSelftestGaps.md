# Round 20 D6f — jj selftest gaps

**Axes:** calibration (ground the residuals), coverage (two named cases), depth (exercise a real outside target and independent env observation).

**Observations.** The round-19 report lists “jj selftest coverage gaps” as residual at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/kaidoku.md:125`. The exact uncovered behaviors are documented in `.ufo/waves/round-19/w2/ToolJjSandbox.md:14-22`: (1) the old `rel` case's `../victim` resolved to the evaluator's temporary parent, not the selftest's victim, so the unchanged-byte check was vacuous; (2) `TMPDIR` was absent from the canary set, and `_shim_observations()` reused `_dirty_key()`, so omitting TMPDIR there masked its own regression. The prior selftest was recorded as `SELFTEST: CLEAN cases=9` at `ToolJjSandbox.md:26`.

**Change.** Added `jj_relative_traversal_refused`, pointing through `..` to an existing victim in the outer selftest mkdtemp and requiring the named `pointer_table_path_outside_sandbox` refusal plus unchanged victim bytes (`.ufo/waves/round-18/tools/jj-red-before.py:1191-1199`). Added `jj_tmpdir_scrubbed`, which injects a TMPDIR sentinel and checks shimmed Git children; its observer independently classifies `TMPDIR` instead of consulting `_dirty_key()` (`:1028-1044,1199-1228`). Existing selftest fixtures remain under `/tmp` mkdtemp and are removed by `finally` (`:1048-1049,1231-1232`).

**Counts/evidence.** Before: 9 cases (round-19 observation above). After: 11 cases; exact selftest last line `SELFTEST: CLEAN cases=11`, exit 0. Clone base observed as `14f0260ad319ecc26994381b2415d5a999003375`. Patch: `.ufo/waves/round-20/w1/patches/KaidokuR20.JjSelftestGaps-2.patch`; staged diff stat: `1 file changed, 50 insertions(+), 6 deletions(-)`.

**Commands and exits.**

```text
~/.local/bin/jj --version
exit 0; jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5

git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-KaidokuR20.JjSelftestGaps-2 && git -C /tmp/kr20-KaidokuR20.JjSelftestGaps-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-KaidokuR20.JjSelftestGaps-2 rev-parse HEAD
exit 0; printed 14f0260ad319ecc26994381b2415d5a999003375

python3 -I -B .ufo/waves/round-18/tools/jj-red-before.py --jj /home/vgpnk/.local/bin/jj --selftest; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"
exit 0; SELFTEST: CLEAN cases=11; EXIT=0

git -C /tmp/kr20-KaidokuR20.JjSelftestGaps-2 add -A && git -C /tmp/kr20-KaidokuR20.JjSelftestGaps-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-KaidokuR20.JjSelftestGaps-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/KaidokuR20.JjSelftestGaps-2.patch
exit 0; 1 file changed, 50 insertions(+), 6 deletions(-)
```

**Risk/blocker.** `read xd://lsp` returned `No such tool`; no LSP device is mounted. The shim verifies Git-child environments, not the environment actually observed by jj; this remaining observation limit is also stated in `ToolJjSandbox.md:58`. No blocker or tool install; no build/lint/formatter/broad suite run.
