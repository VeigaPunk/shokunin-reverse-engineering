# ReviewerC2 — attack on R86-C2 (gate-registry counter)

Read-only seat. No production file edited, no commit, no subagent. Counter under test:
`tools/round-86/gate-registry.py` (sha256 `b87ffb1b…c81a5`, identical to the BASE pre-receipt).
Fixture command shape, per row:

```
python3 -I -B tools/round-86/gate-registry.py --root <fx> --worktree <fx> --work <scratch>/work/<name> --json-out receipts/<name>.json
```

`--root <fx>` is passed explicitly (see finding F-ROOT). Every fixture starts from a copy of the
R85 tree shape: `tools/round-85/predicate-bind.py` (BASE blob at `2cf0b7ff`), `.ufo/waves/round-85/claims.json`
(BASE blob). Only `SKILL.md` (and, for Fa1/Fa2, the tool's last line) differs. Receipts: `receipts/<name>.json`.

## Rows

Row text is the registry row as written into the fixture `SKILL.md` between the markers.
"Accepted" = `ok: true` / exit 0; "refused" = `ok: false` / exit 1.

| # | fixture | row / change | exit | agreed | mismatches | verdict |
|---|---|---|---|---|---|---|
| 0 | F00-genuine | five fields true: map `0=…; 1=…; 2=…`, cell `python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0, pin `.ufo/waves/round-85/claims.json`, owner `kaidoku-r85` | 0 | 5/5 | [] | correct accept (genuine row reaches 5/5) |
| a1 | Fa1-selftest-exit1-cell-exit0 | tool's `--selftest` forced to exit 1; cell declares `— exit 0` | 1 | 3/5 | G2, G3 | correct refusal. G2 observed 1 ≠ 0; G3 declared 0 ≠ observed 1 |
| a2 | Fa2-selftest-exit1-cell-exit1 | same forced-1 tool; cell declares `— exit 1` | 1 | 4/5 | G2 | correct refusal, but only by G2. G3 alone is satisfied when the cell copies the observed failure; G2 hard-codes success = 0 |
| a3 | Fa3-no-tool-path-python-c | genuine tool; cell `python3 -c "import sys; sys.exit(0)" — exit 0` (names no tool path) | 0 | 5/5 | [] | **wrong accept**. Frozen G3 text requires "a python3 command on that tool path"; `command_argv()` never checks the path. Counter defect against its own atom |
| b1 | Fb1-verdict-prose-tokens | verdict cell `see note: 0= 1= 2= are tokens; no exit map is declared here` | 0 | 5/5 | [] | **wrong accept**. G2 is a substring test on `0=`, `1=`, `2=`; the prose declares no map. Refusal is the right answer |
| b2 | Fb2-verdict-substring-10-11-12 | verdict cell `10=clean 11=flagged 12=unreadable` | 0 | 5/5 | [] | **wrong accept**. `0=`, `1=`, `2=` match inside `10=`, `11=`, `12=`. No exit 0/1/2 map is declared |
| c1 | Fc1-pin-other-round | pin cell `.ufo/waves/round-84/claims.json` (exists, blob at fixture rev, belongs to round 84) on the round-85 tool | 0 | 5/5 | [] | accepted by frozen G4 text (any `round-<N>` that is a blob). I judge refusal right: the pin should describe the tool's own container (round 85). G4 is presence-only and cannot see the round |
| d1 | Fd1-owner-r085 | owner `kaidoku-r085` | 1 | 4/5 | G5 | correct refusal (`085` ≠ `85`) |
| d2 | Fd2-owner-trailing-space | owner `kaidoku-r85  ` (trailing spaces inside the cell) | 0 | 5/5 | [] | correct accept: `split_row` trims cells; no value differs |
| d3 | Fd3-owner-suffix | owner `kaidoku-r85 (lane)` | 1 | 4/5 | G5 | correct refusal (`$`-anchored regex) |
| e1 | Fe1-dup-inside-plus-prose | the genuine row twice inside the markers; path also in prose | 1 | 0/5 | all five | correct refusal. G1 rows=2; `find_row` returns None, so G2–G5 report "no registry row" too |
| e2 | Fe2-row-inside-dup-outside | one genuine row inside; the same row as a pipe table outside the markers, plus prose | 0 | 5/5 | [] | correct accept: rows outside the markers are not the registry |
| e3 | Fe3-malformed-6cell-dup-inside | genuine row inside, plus a second row with 6 cells (owner cell missing) inside | 0 | 5/5 | [] | **wrong accept**. `registry_rows()` keeps only rows with `len(cells) >= 7`; the malformed row is dropped silently. G1 reports rows=1 |
| g3a | Fg3a-env-canary-and-home | cell is a `python3 -c` probe: exit 0 only if `PARENT_CANARY` is absent and HOME/TMPDIR end in `/home` and `/tmp`; the counter was run with `PARENT_CANARY=1` exported | 0 | 5/5 | [] | no leak: the child saw the four-key env only (`PATH`, `HOME`, `TMPDIR`, `LANG`); HOME/TMPDIR sit under `--work` |
| g3b | Fg3b-shell-subst | cell `python3 -c "import sys; sys.exit(0)" $(touch <S>/sentinel-subshell) — exit 0` | 0 | 5/5 | [] | no shell: the sentinel was NOT created. `$(touch` and the path are literal argv tokens. (Still a row whose command is not the tool, as in a3) |
| g3c | Fg3c-semicolon-rm | cell `python3 -I -B tools/round-85/predicate-bind.py --selftest; rm -rf <S>/victim — exit 2` | 0 | 5/5 | [] | no shell: `rm` never ran, victim survived. **G3 green on a command the tool cannot honour**: argv is `… --selftest; rm -rf …` (`--selftest;` is an unknown flag), exit 2 is argparse refusal, and the row declares exit 2. This is the failure the frozen kill-rule wording names |
| g3d | Fg3d-fs-escape | cell `python3 -c "open('<S>/escape-ReviewerC2.txt','w').write('x')" — exit 0` | 0 | 5/5 | [] | env is bounded, the filesystem is not: the child wrote a file outside `--work` (the escape file exists) |
| r0 | Fa1 run with **no** `--root` from cwd = BASE tree | same fixture as a1 (forced-1 tool), `--worktree` only | 0 | 5/5 | [] | **wrong accept** (footgun). `main()` sets `root` to `--root` (default `.`) and G2/G3 execute the tool there, not in the fixture |
| r1 | Fa1 run with no `--root` from scratch cwd | same fixture as a1 | 1 | 3/5 | G2, G3 | refused for the wrong reason: the caller's cwd has no `tools/round-85/` tool, so the child exits 2 |

## Controls and BASE

| run | exit | result | verdict |
|---|---|---|---|
| `--root <lane> --rev 2cf0b7ff…` (BASE) | 1 | agreed 0/5, all five atoms ok=false; atoms and mismatches identical to `.ufo/waves/round-86/pre/c2-at-base.json` | matches the pre-receipt |
| `--control file-exists --rev 2cf0b7ff…` | 0 | mismatches 0, accepted=True | matches `pre/c2-control-file-exists-at-base.json`; control accepts the unregistered state, as designed |
| `--root <lane> --rev 0864a7bd…` (HEAD) | 1 | 0/5 | HEAD has no registry row (lane working tree is ahead) |
| `--root <lane> --worktree <lane>` (uncommitted SKILL.md row, read-only) | 0 | 5/5, [] | the row currently in the lane's working tree (uncommitted, not a measured rev) reaches 5/5 |
| counter `--selftest` | 0 | cases=8, failures=0 | the counter's own selftest is green, so it does not catch a3, b1, b2, e3, c1 or g3c |

## Process checks

- Child execution: `subprocess.run(argv, …)` with a list and `env=` of four keys; no `shell=True`
  anywhere in `gate-registry.py` (grep: only list-form `subprocess.run` calls). Confirmed by g3a, g3b, g3c.
- Env bounding: `HOME`/`TMPDIR` point at `--work/home` and `--work/tmp`; the parent's `PARENT_CANARY`
  does not reach the child. Filesystem writes are NOT bounded (g3d).
- `sys.executable` replaces the cell's `python3` token, so the child runs under the counter's own interpreter.
- Only `shlex.split` decides what is executed; `;`, `$()`, and `--selftest;` are literal tokens.

## Findings (scope: R86-C2 counter, fixture-tested)

1. **F-ROOT (counter footgun).** `--worktree` mode does not move the executed tool into the fixture.
   G2 and G3 run in `--root` (default `.`). The frozen counting command uses `--rev` with `--root .`,
   so that path is consistent. The fixture form (`--worktree` only) silently tests the caller's tool (r0).
2. **F-G3-PATH.** G3 does not check that the cell's command is on the tool path, despite its
   docstring and frozen text (a3, g3b, g3c). The counter accepts a row whose command is not the tool,
   and the observed exit it compares is whatever that command returned.
3. **F-G2-SUBSTRING.** The verdict-map test is `"0=" in cell`, which passes prose and `10=`/`11=`/`12=` (b1, b2).
4. **F-G1-SILENT-DROP.** Rows with fewer than 7 cells, or without a backticked `tools/` cell 0, are dropped
   without being counted. A malformed duplicate passes G1 (e3).
5. **F-G4-ROUND.** G4 accepts any `round-<N>` claims blob, not the tool's own round (c1). This is a
   presence check as the frozen Limits paragraph says.
6. What holds: duplicate rows refused (e1); owner-round mismatch refused (d1, d3); the G2/G3 pair catches a
   wrong success exit (a1); the only real self-test is G2's hard-coded run, so a row cannot fake the
   tool's own exit (a2 is refused by G2 alone); the child env is four keys; no shell.

## Verdict on R86-C2 at the measured revision

The counter is right about the row it was built for: the lane's uncommitted row (5/5) and the genuine
fixture (5/5) are real, and BASE is 0/5 as the pre-receipt says. But `agreed 5/5` does NOT establish that
the row describes the tool. Fixtures a3, b1, b2, c1, e3, g3c and r0 reach 5/5 (or the wrong 5/5 in r0) with rows
that do not describe the tool. Under the frozen kill-rule wording, g3c is a G3-green row whose command the
tool cannot honour; the lane's measured row does not do that (its command runs the tool, exit 0, 21 cases).
Whether a fixture acceptance counts against the claim is for the L1, not for this seat. The mechanical
result stands; the claim's evidential strength is weaker than its predicate text.
