# JjRedBeforeProbe — `W18/tools/jj-red-before.py`

- Seat `KaidokuR18.JjRedBeforeProbe` (leaf, advisory). Contract section `.ufo/waves/round-18/contract.md:88-98`; the six L1 amendments (sentinel + critic, 2026-10-20) are implemented and anchored below.
- **Files written:** `.ufo/waves/round-18/tools/jj-red-before.py` (new, 1046 lines, 48545 bytes, mode +x) and this report. No other lane file was written. No `jj`/git write in the lane; `jj` ran only inside `/tmp` sandboxes.
- **Installs:** none. Host already had jj `0.45.1-7c41cdeb`, git `2.56.0`, Python `3.14.8`; pacman was not touched.
- **No REA / Ghidra / analyzeHeadless / carrier execution** was performed (out of scope for this item).

## Behavior (observation from the run)

`--root LANE [--branch main] [--baseline-rev B] [--jj PATH] [--cd-probe PATH] [--custody-pair PATH] [--revpin PATH] [--out RECEIPT.json]`, plus `--selftest`. Stdlib only; every child gets `-I -B`, an explicit `cwd`, and a scrubbed env (`GIT_*`, `JJ_*`, `TMPDIR` removed — `jj-red-before.py:113`).

Sandbox: `mkdtemp(dir="/tmp")`, refused under the lane or fleet root (`:105`), `git clone --no-local` (`:237-243`), then L1 amendment (1): `git remote remove origin` and a no-remotes assertion (`:258-262`), a fake `refs/remotes/origin/main` at the tip (`:264-266`) so `pushed` checks have an unwritable target, `jj git init --colocate` with `--config` identity (`:277`), then state D0 (detached at tip, lane's current shape), then the cited-line rewrite + marker file and `jj -R sb commit -m off` (`:290-319`), which leaves `refs/heads/main` at B and HEAD off-branch. The sandbox is removed in `finally`; construction failures remove it too (`:224-234`).

Steps retained with full argv/exit/stdout/stderr: `d0-rev-parse-head`, `d0-fixed-citation-drift-rev-head`, `d0-fixed-custody-capture`, `d0-revpin-resolve-source`, `baseline-citation-drift` (+ `-finding`, `-control`), `fixed-citation-drift`, `fixed-citation-drift-rev-head`, `baseline-custody-capture` (cwd=sb), `fixed-custody-capture` (`--repo sb`), `baseline-rev-parse-head`, `revpin-resolve-source`, and `lane-tip-unchanged`. Receipt is `{steps, expectations:[{name, expected, observed, held}], all_held}` plus `setup`, `baseline_extracts`, `not_runnable`, `lane_tip`; `sort_keys=True, indent=2`; exit 0 all held / 1 any runnable step not held / 2 setup failure (or every step blocked).

## Selftest (exact)

Command (from `/tmp`):

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/jj-red-before.py --selftest
```

Last line:

```
SELFTEST: CLEAN cases=5
```

Exit code: **0**.

Cases: (1) all-fixed tools on a fixture lane → 14/14 held, exit 0; (2) regressed fixed citation-drift that resolves HEAD → must be not-held at `fixed-citation-drift` (exit 1); (3) regressed fixed capture omitting the `repo-HEAD-is-branch-tip` line → must be not-held at `fixed-custody-capture`; (4) the *baseline* tool already fixed → `baseline-citation-drift` and `-finding` must be not-held (a green "before" proves nothing); (5) fixed tools absent → exactly the five fixed-tool steps are `not_runnable` (held `null`), never held. Fixtures live under `mkdtemp(dir="/tmp")` and are removed (`jj-red-before.py:903-990`).

## Real run (fixed tools had landed: gate mtimes 12:36/12:37)

```
python3 -I -B .../jj-red-before.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --out /tmp/jrb-evidence/receipt.json
```

Exit **0**, `all_held: true`, `not_runnable: []`, 14 steps / 14 expectations. Lane tip `9011581d84527ba34c675f9cf912e54d2e72d470` before **and** after (observation; `lane-tip-unchanged` held). Sandbox D0 HEAD = tip; D1 HEAD = `5e9b835aac6ee9bca46bd5e463eb21df30b18f5d` (differs every run — jj commit ids are fresh; expectations compare relations, not fixed shas).

| expectation | observed | held |
|---|---|---|
| d0-rev-parse-head | HEAD == main == `9011581d…` | yes |
| d0-fixed-citation-drift-rev-head | exit 0, not refused (no false refusal at tip) | yes |
| d0-fixed-custody-capture | `repo-HEAD-is-branch-tip: yes` | yes |
| d0-revpin-resolve-source | no raise, `head_equals_source: true`, `pushed: true` | yes |
| baseline-citation-drift | `CITATION_DRIFT_REVISION: HEAD`, HEAD off-branch | yes |
| baseline-citation-drift-finding | `SCORECARD.md:59` cited-line `citation_dead` present | yes |
| baseline-citation-drift-control | `--rev refs/heads/main`: needle absent | yes |
| fixed-citation-drift | `CITATION_DRIFT_REV_RESOLVED: 9011581d…`, exit 0 | yes |
| fixed-citation-drift-rev-head | exit 2, `head_not_branch_tip` | yes |
| baseline-custody-capture | `# repo-HEAD: 5e9b835a…` (cwd-keyed) | yes |
| fixed-custody-capture | `repo-HEAD-is-branch-tip: no`, `repo-branch-tip: 9011581d…` | yes |
| baseline-rev-parse-head | `5e9b835a…` ≠ tip | yes |
| revpin-resolve-source | `RevPinError: head_not_branch_tip` | yes |
| lane-tip-unchanged | before == after | yes |

Contract deviation (observation): the contract says the fixed probe records `rev_resolved`, but the landed probe prints `CITATION_DRIFT_REV_RESOLVED:` (`citation-drift-probe.py:398-400`), not the baseline's `CITATION_DRIFT_REVISION:`. `probe_resolved_rev` accepts both (`jj-red-before.py:185-200`). The baseline probe was extracted from Git at B, never from the working tree (`baseline_extracts`).

## L1 amendments (all six)

1. Origin removed + no-remotes assertion + fake `refs/remotes/origin/main`: `jj-red-before.py:252-266`; sandbox refuses lane/fleet paths (`:105-111`).
2. `mkdtemp(dir="/tmp")` (`:237`), scrubbed child env (`:113-127`), sandboxed `HOME`/`XDG_CONFIG_HOME` for jj, `-R sb` on every post-init jj call (`:277`, `:313`), `-I -B` and explicit `cwd` on every child (`run`, `:130-147`).
3. Baseline citation-drift runs with `--table`/`--expected` pointed at sb's own gate files (`:505-509`), and the off-branch commit rewrites the pointer-table-cited line `SCORECARD.md:59` (`pick_cited_line`, `:203-220`; `:290-311`) so the red is a real `CITATION_DRIFT: citation_dead` finding; a control run at `refs/heads/main` proves the finding is off-branch-only (`:530-540`).
4. Baseline custody capture runs with `cwd=sb` (`:603-608`).
5. State D0 runs first (`:371-420`), asserting no false refusal (exit 0), `is-branch-tip: yes`, and a clean `resolve_source`.
6. Baseline `git rev-parse HEAD` line carries `# head-rev-lint: red-before` (`:377`, `:659`); lane tip before/after is recorded and asserted (`:701-704`).

## head-rev-lint self-check (independent instrument, already landed)

My file committed alone into a throwaway repo, then `head-rev-lint.py --root <tmp> --rev <sha>` → exit 0, `live_count: 0`, `fixture_count: 0`, `annotated_count: 2` (lines 377 and 659, both `rev-parse-HEAD`/`annotated`). The tool adds zero live HEAD sites; the two baseline expressions are the intended annotated red-before sites.

## Commands run (all shell invocations, with exit)

| # | command (trimmed) | exit |
|---|---|---|
| 1 | `ls -la .ufo/waves/round-18/ .ufo/waves/round-18/tools/` | **2** (tools/ not yet created) |
| 2 | `ls -la .ufo/gates/{citation-drift,custody-pair}/; git -C LANE rev-parse refs/heads/main HEAD` | 0 |
| 3 | `git -C LANE show B:.ufo/gates/citation-drift/citation-drift-probe.py > /tmp/baseline-cd.py && wc -l` (+ same for custody-pair) | 0 |
| 4 | `grep -n 'add_argument\|def capture\|…' /tmp/baseline-cp.py \| head -80` | 0 |
| 5 | `stat …; jj --version; git --version; python3 --version` | 0 |
| 6 | `grep -n -A6 'colocat\|commit -m\|detached\|bookmark\|HEAD' w1/ScoutJjColocation.md \| head -60` | 0 |
| 7 | `mkdir -p .ufo/waves/round-18/tools` | 0 |
| 8 | `python3 -c 'json.load(pointer-table.json) … entry shapes'` | 0 |
| 9 | `python3 -I -B jj-red-before.py --selftest` (first) | 0 |
| 10 | inline importlib driver: `evaluate()` on fixture lane, dump receipt | 0 |
| 11 | `jjprobe`: step-by-step clone/remote-remove/fake-ref/jj-init/jj-commit ref trace | 0 |
| 12 | `stat` fixed-tool mtimes + `grep -c` markers (6 and 6) + `git rev-parse refs/heads/main` | 0 |
| 13 | real run #1 (fixed tools present) | **1** (`fixed-citation-drift` parsed `REV_RESOLVED` as null) |
| 14 | receipt step dump (`fixed-citation-drift` stdout/stderr) | 0 |
| 15 | `grep -n 'rev_resolved\|…' citation-drift-probe.py \| head -40` | 0 |
| 16 | selftest + real run #2 (after parser fix) | 0 / 0 |
| 17 | selftest after adding case 4 (red-before premise) | 0 |
| 18 | real run + `/tmp` leftover count (3 were my receipt files, not dirs) | 0 |
| 19 | `ls -ld /tmp/jj-red-before-*; for d …` (confirmed no sandbox dirs) | 0 |
| 20 | `compile()` check, marker grep, anchor grep, `ls -la tools/` | 0 |
| 21 | `head-rev-lint.py --root /tmp/lintprobe/repo --rev <sha>` (first) | 0 |
| 22 | final selftest + real run (post emit-guard) | 0 / 0 |
| 23 | `head-rev-lint.py --root /tmp/lintprobe2/repo --rev <sha>` (final file) | 0 |
| 24 | `git status --porcelain -- tools/ gates/ w1/` (read-only) | 0 |
| 25 | `wc -l` / `stat` final file + contract line check | 0 |

## Risks / limits (observation unless marked)

- The real-run `d1` sha changes per invocation (`5e9b835a…` this run). The receipt is truthful for its run; no expectation depends on a fixed sandbox sha.
- `pick_cited_line` depends on the pointer table still carrying an `exact`/`quoted` entry with an in-range line. It currently picks `sc59-stanza-key-anchor` → `SCORECARD.md:59`. If the L1 edits that entry away, the fallback is `SCORECARD.md:1`, which may not be cited and would make `baseline-citation-drift-finding` not held — the probe would report red honestly rather than silently pass (inference from code path `:203-220`).
- `fixed-citation-drift` green accepts exit 0 or 1 and requires `rev_resolved == main tip`; in default (non-strict) probe semantics the observed exit is 0. Tightening to 0 would break nothing today, but 0/1 tolerates the probe's documented `--strict` mode.
- The tool clones the lane read-only; the no-write claim is asserted by `lane-tip-unchanged`, not by a filesystem snapshot. Untracked-lane writes by siblings are out of this instrument's scope.
- `head-rev-lint` is not yet committed at a revision containing my file; the self-check used a throwaway repo with my file as the only tracked site. The lane's real `live_count` at delivery depends on the L1's commit (inference; their instrument, their gate).
- No blockers. No REA/Ghidra/carrier work was attempted, per the lane contract.
