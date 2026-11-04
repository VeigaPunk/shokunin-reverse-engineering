# ReviewerC2 — R86-C2 (operability) attack report

Seat: ReviewerC2 (reviewer, leaf, read-only). Full table: `.ufo/waves/round-86/w1/ReviewerC2/attack.md`;
receipts: `.ufo/waves/round-86/w1/ReviewerC2/receipts/` (21 JSON files). No production edit, no commit,
no subagent. Counter: `tools/round-86/gate-registry.py` (sha256 `b87ffb1b…c81a5`, same as the BASE pre-receipt).

## Measured

- BASE `--rev 2cf0b7ff…`: exit 1, agreed 0/5. Atoms and mismatches match `pre/c2-at-base.json`.
- Control `--control file-exists --rev 2cf0b7ff…`: exit 0, mismatches 0. Matches `pre/c2-control-file-exists-at-base.json`.
- Genuine fixture row (five fields true): exit 0, 5/5.
- Lane working-tree SKILL row (uncommitted, read-only `--worktree`): exit 0, 5/5. HEAD `0864a7bd`: 0/5.
- Counter selftest: exit 0, 8 cases.

## Fixtures that reach 5/5 with a row that does not describe the tool

| fixture | row defect | exit/agreed | why the counter accepts |
|---|---|---|---|
| a3 | cell is `python3 -c "import sys; sys.exit(0)" — exit 0`, no tool path | 0, 5/5 | `command_argv()` never checks the path; frozen G3 text says "on that tool path" |
| b1 | verdict cell is prose `0= 1= 2= … no exit map is declared` | 0, 5/5 | G2 is `"0=" in cell`, a substring test |
| b2 | verdict cell `10=clean 11=flagged 12=unreadable` | 0, 5/5 | `0=`, `1=`, `2=` match inside `10=`, `11=`, `12=` |
| c1 | pin `.ufo/waves/round-84/claims.json` on the round-85 tool | 0, 5/5 | G4 accepts any round's claims blob (presence only) |
| e3 | a 6-cell duplicate row inside the markers | 0, 5/5 | `registry_rows()` keeps only rows of ≥7 cells; the malformed row is dropped silently (G1 rows=1) |
| g3c | cell `python3 -I -B tools/round-85/predicate-bind.py --selftest; rm -rf <victim> — exit 2` | 0, 5/5 | argv has `--selftest;` (unknown flag); exit 2 is argparse refusal, and the row declares exit 2 |

Refusals that are right: d1 `kaidoku-r085` (G5), d3 `kaidoku-r85 (lane)` (G5), e1 duplicate row (G1 and all
others), a1 wrong success exit (G2 and G3), a2 (G2 alone catches a declared failing exit).
Accept that is right: d2 trailing space (cells are trimmed), e2 a row outside the markers (not the registry),
F00 genuine row.

## Process checks

- No shell: `subprocess.run` with list argv in every call; `$(touch …)` and `rm -rf …` in a cell never executed
  (sentinel not created, victim survived).
- Env: the child sees only `PATH`, `HOME`, `TMPDIR`, `LANG`; a parent canary did not leak; HOME/TMPDIR under `--work`.
- Filesystem is not bounded: the child wrote a file outside `--work` (g3d).
- `--worktree` mode without `--root` executes the caller's tool, not the fixture's (r0 accepted a forced-fail
  fixture 5/5 from the BASE tree). The frozen counting command passes `--rev` with `--root .`, which is consistent;
  the fixture form is a footgun.

## Verdict

The mechanical result is correct where the row is genuine, and BASE 0/5 and the control match their pre-receipts.
But 5/5 does not establish that the row describes the tool: six fixtures (a3, b1, b2, c1, e3, g3c) reach 5/5 on
rows that do not describe it, and one (r0) is a fixture-mode footgun. Under the frozen kill-rule wording, g3c is a
G3-green row whose command the tool cannot honour. The lane's measured row runs the tool (exit 0, 21 cases) and is
not affected. Whether a fixture acceptance counts against C2 is for the L1 to decide. I did not change any rule and
recommend the L1 record the G1 silent drop, the G2 substring, the G3 path gap and the G4 round gap as counter defects,
not as rule edits made mid-wave.

## Tools

No tool was installed or upgraded. Python 3.14.8 was used as-is.
