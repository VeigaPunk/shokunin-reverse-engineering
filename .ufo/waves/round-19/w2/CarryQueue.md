# CarryQueue — round-18 Open items vs round-19 disposition

Axes checked: **calibration** (status/claim alignment), **freshness** (census result and scope), **depth** (nested lint coverage).

## Findings

**No actionable finding in the assigned scope.** The three dispositions are explicit and bounded; none is silently presented as fixed.

### R12 operability decision

- **[Observation]** Round 18 required an add-or-withdraw decision (`corpus/lessons/round-12-verifier-spotcheck.md:17`; carried at `corpus/lessons/round-18.md:88` and `corpus/lessons/round-18-verifier-spotcheck.md:201-206`). Round 19 records the decision explicitly: withdraw operability as an owned-axis improvement, leave the historical outside admission unchanged, retain operability only as an unowned fleet proxy, and keep coverage/depth/calibration as the owned axes (`corpus/lessons/round-19.md:101-110`).
- **[Observation]** The round-19 Open section distinguishes this from the separate R12 source/custody and Docker-identity qualifications (`corpus/lessons/round-19.md:95`). The `claims.json:32` `carried_open` value is the declaration-time carry-in; `claims.json:5,36-40` and the round-19 lesson provide the later amendment/disposition. I do not read the initial carry-in as claiming the axis decision remains unresolved after the explicit decision.
- **[Inference]** The operability debt is resolved without retroactively changing the historical review or claiming a round-19 axis gain.

### Census undeclared blocks

- **[Observation]** The round-19 amendment states that the two undeclared blocks remain, no `SCOPE`/`DATED` range is widened, and PASS is no longer claimed (`.ufo/waves/round-19/claims.json:37-39`). The lesson calls out the same blocks and says a scope-table re-key would be a gate change, not a freshness edit (`corpus/lessons/round-19.md:96`). The current fixed scope ends the SCORECARD range at line 2122 and covers only SKILL lines 10-20 (`.ufo/gates/c1-census-v10.py:253-277`); it does not declare SCORECARD 2380-2382 or SKILL 511-519.
- **[Observation — command, exit 1]**
  ```text
  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  ```
  Output: live pins all 6.7.0; `stale=0`, `ambiguous=0`, `undeclared=2`, `unresolved=0`; `VERDICT: FAIL`. The two findings are SCORECARD block 2380-2382 (6.5.0 / 6.7.0 bare values) and SKILL block 511-519 (6.5.0 bare value). `command_exit=1`.
- **[Observation]** The round-19 verifier expects census exit 1 and constrains the output to stale 0 / ambiguous 0 / undeclared 2 / unresolved 0 (`.ufo/waves/round-19/verify.py:113,617-618,681-684`). The gate reads live pins and the files under `--root` (`.ufo/gates/c1-census-v10.py:634-657`), so my command is a live worktree/host observation, not a revision-only snapshot.
- **[Inference]** No undeclared block was silently re-keyed or counted as a clean PASS. The unamended initial forecast at `claims.json:20` still contains the pre-amendment PASS wording, but the appended C2 amendment at `:39`, verifier expectation, lesson, and observed exit explicitly supersede it.

### Nested lint limit

- **[Observation]** The round-18 spot-check allowed either fixing the nested-read blind spot or registering its limits (`corpus/lessons/round-18-verifier-spotcheck.md:196`). Round 19 says the nested compare-only reads are a **registered limit, not fixed** (`corpus/lessons/round-19.md:97`). The SKILL registry entry names both nested reads and records that the wave-1 `nested`-class attempt failed its selftest and was not taken (`SKILL.md:587`). The linter itself documents that wrapper detection is intra-file and does not resolve helpers in another module (`.ufo/waves/round-18/tools/head-rev-lint.py:129-143`).
- **[Observation — command, exit 0]**
  ```text
  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/head-rev-lint.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
  ```
  At the observed revision it reported `files_scanned=40`, `live_count=0`, `fixture_count=15`, `annotated_count=6`, exit 0. Its returned `limits` still say cross-module wrappers are not followed; excluded seat-directory outputs are not counted as live lane instruments. `command_exit=0`.
- **[Inference]** The zero live count is not evidence that the nested reads are absent. The remaining limitation is disclosed rather than silently treated as fixed.

## Residual risk and verification gaps

- The declaration-time `claims.json` keeps its original carry-in and C2 forecast text. Interpret those through its timestamp and appended amendment, not as a final-state ledger; the round-19 lesson provides the explicit dispositions above.
- The census result is time-dependent on the host config and current lane files. The nested lint remains a static, intra-file scan with the registered cross-module blind spot.
- The observed lane had `HEAD` and `refs/heads/main` both at `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (rev-parse exit 0), but was not clean before this report. `git status --short` (exit 0) showed existing round-19 edits, including `corpus/lessons/round-19.md`, the R12 knowledge entry, and untracked `w2/`/`runs/pass2/`. The scoped read-only diff (exit 0) showed the lesson/entry source-index updates (including S039) outside the R12 decision lines; those in-progress edits are not attributed to the observed main tip.
- LSP was unavailable: `read xd://lsp` returned “No such tool” and listed the mounted devices. Therefore no LSP status/references/definitions/diagnostics could be requested; source statements above use direct file anchors and measured command output, not grep as semantic proof.
- No runtime was invoked, and no build, broad suite, formatter, install, or production edit was performed. Runtime rerouting/saturation claims were not part of these three scoped dispositions.

## Commands with observed exit codes

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD refs/heads/main
# exit 0; both resolved to 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --short
# exit 0; pre-existing dirty/untracked round-19 work listed above

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --unified=3 -- corpus/lessons/round-19.md corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
# exit 0; S039/source-index edits, not a change to the R12 axis decision

python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# exit 1; VERDICT FAIL, stale=0 ambiguous=0 undeclared=2 unresolved=0

python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/head-rev-lint.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# exit 0; files_scanned=40, live_count=0; registered cross-module limit remains
```