# Round 45 claims — freeze

Lane `kaidoku`, round 45, attempt 1. Base `149133d47aa7e90796f96047afe6d251a3e65b2c`
(`git -C kaidoku-shokunin rev-parse main` at claim time; `jj-lane.sh state` printed
`local=149133d4 remote=149133d4 ahead=0`).

**Freeze** = the commit that first contains this file and `tools/round-45/` (a directory
pathspec). The receipts under `.ufo/waves/round-45/controls/` are not frozen: the
do-nothing controls can only be scored against the freeze that already exists. The report cites it as
`plans/round-45-claims.md@<freeze>`; `git log --format=%H -1 -- plans/round-45-claims.md`
re-derives it. Nothing in this file or in `tools/round-45/` changes after the freeze:
a change makes both counters exit 2 `frozen_path_changed`.

Owned axes are all tied at 10 (`SCORECARD.md` `## Owned axes`), none retired, and a
capability entered in round 43 — so the stagnation nudge does not waive the lowest-axis
obligation. Two claims, on two distinct tied-lowest axes; coverage gets no claim this
round (its proxy is the round-44 frozen tree at 137/137 and this round adds no domain
surface).

| claim | axis | surface |
|---|---|---|
| R45-C1 | depth | `SKILL.md` `## Queue-drain craft` rule block 22 — the freeze-integrity decision table — and its interpreter `tools/round-45/frozen-path-preflight.py` |
| R45-C2 | calibration | the `SKILL.md` instrument registry vs the instruments the two most recent frozen claim files name |

Causal separability: C1's counter reads `SKILL.md`'s craft section and the preflight's
selftest; it never reads a registry row. C2's counter reads the registry rows and the
scope file; it never reads block 22. Either lands and scores without the other.

## R45-C1 — depth: a freeze-integrity decision table whose arms are proven red

The prior state holds the *rule* (freeze integrity) only as prose inside claim files and
lessons, and the only instrument (`tools/round-45/frozen-path-preflight.py` at the base)
is an untested single-arm gate: no worktree arm, no pathspec requirement for a directory
freeze, and no restore classifier. Round 44 lost eight frozen control fixtures to a
non-author sweep because no gate looked at the worktree (`corpus/lessons/round-44.md:18,63`),
and the C2 arm could not tell append-then-restore from never-left
(`corpus/lessons/round-44.md:88`, `corpus/lessons/round-44-verifier-spotcheck.md:89-92`).

**Landed surface.** One new rule block in `## Queue-drain craft`, marker
`<!-- freeze-integrity-table v1 -->`, containing a table whose columns are
`trigger | arm | exit | receipt`, at least eight rule rows, every exit cell in `{0,1,2}`,
and located citations (four or more, all resolving at the measured revision). The block
cites `S140` (git-status porcelain, opened 2026-10-28) and the interpreter path. The
interpreter gains the four arms and an `--selftest`.

**Predicate (each clause is computed by `tools/round-45/c1-counter.py`).**

1. `rule_blocks == 22` — `^- \*\*` blocks inside `## Queue-drain craft` (21 at the base).
2. `block22_present == 1` — exactly one block contains the marker.
3. `block22_rows >= 8`; the table header carries `trigger`, `arm`, `exit`, `receipt`;
   every row's exit cell is exactly one of `0`, `1`, `2`.
4. `block22_refs >= 4` and `block22_unresolved_citations == []` — every `path:line` or
   `path:first-last` reference resolves at `--rev`.
5. The block cites `S140` and `tools/round-45/frozen-path-preflight.py`; the interpreter
   is present at `--rev`.
6. The interpreter extracted from `--rev` runs `--selftest` with exit 0 and
   `cases >= 11`, `failures == 0` (the red cases are named: touched, restored, dirty,
   pathspec-required, unknown freeze, non-ancestor, bulk sweep).

**Target.** `failing == []`, counter exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-45/c1-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze <FREEZE> --rev <REV> --json-out <OUT>
```

**Before (do-nothing control, receipt `controls/ctl-c1-0-do-nothing.json`).** At the
freeze, exit 1: `rule_blocks 21 != 22`, `block22_present 0 != 1`, `block22_rows 0 < 8`,
`block22_refs 0 < 4`. At the base the same receipt prints the same values.

**Kill rule.** A do-nothing SKILL.md cannot reach it (control above). A relabelled block
that keeps the 21-block count still scores 1 (`--selftest` case
`red-relabelled-21-block`); a block with three table rows scores 1 (`red-thin-table`);
a block whose citation points past the file scores 1 (`red-bad-citation`); a block
without `S140` scores 1 (`red-no-s140`); an interpreter whose selftest fails scores 1
(`red-interpreter-fails`). A commit in `FREEZE..REV` touching a frozen path makes the
counter exit 2 without printing `met_target`.

## R45-C2 — calibration: the registry names the instruments that carry the claims

The lane's own registry (`SKILL.md` `### Round-40 instrument registry` and earlier) says
which instruments exist and what their exits mean. Observed repo state at the base: the six
instruments of rounds 44 and 45 that carry frozen claims have **no** row
(`grep -c 'round-44' SKILL.md` printed 0 before this round), and round 44's closure
routed exactly that (`corpus/lessons/round-44-verifier-spotcheck.md:166`). This is a
self-assessment/gap mismatch, which is what the calibration axis measures.

**Scope** (exact repo-relative paths, committed at `tools/round-45/registry-scope.json`
and enumerated from there): the instrument set named by `plans/round-44-claims.md` and
`plans/round-45-claims.md`.

1. `tools/round-44/c1-counter.py`
2. `tools/round-44/c1-run.sh`
3. `tools/round-44/c2-counter.py`
4. `tools/round-45/frozen-path-preflight.py`
5. `tools/round-45/c1-counter.py`
6. `tools/round-45/c2-counter.py`

**Predicate (each clause is computed by `tools/round-45/c2-counter.py`).**

1. `scope_size == 6` — read from the scope file, never assumed.
2. `unregistered == []` — for each scope path, some `SKILL.md` registry row's **first
   cell is exactly** that path (backticked, path equality; a row naming another tool
   does not count).
3. `thin == []` — that row's exit-code cell (third column) names `0`, `1` and `2`; a
   bare "non-zero" cell is thin.

**Target.** `unregistered == []` and `thin == []`, counter exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-45/c2-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze <FREEZE> --rev <REV> --json-out <OUT>
```

**Before.** At the base the counter exits 2 `scope file absent at rev`
(`controls/ctl-c2-0-base-unevaluable.json`) — the instrument does not exist there, so the
base is not a measurable before. The measurable before is the freeze, the do-nothing
control: exit 1, `unregistered` = the six paths, `registered []`, `thin []`
(`controls/ctl-c2-0-do-nothing.json`).

**Kill rule.** Six rows naming other tools still report six unregistered (`--selftest`
case `red-wrong-path-rows`); a row that names the path but writes a bare "non-zero"
exit cell reports `thin` (`red-thin-exit-cell`); a five-path scope file fails
`scope_size` (`red-scope-size`). Row counting cannot substitute for path equality.

## Frozen paths (exact)

- `plans/round-45-claims.md`
- `tools/round-45/` — a **directory** freeze: scoring passes `--pathspec tools/round-45/`
  and `--freeze-path tools/round-45`, and `--require-pathspec` refuses a directory freeze
  without the pathspec (the round-44 defect: a whole-tree scan hid the frozen eight).

`SKILL.md` is the graded surface and is **not** frozen. `corpus/SOURCES.md`,
`corpus/lessons/round-45.md`, `LOG.md` and `SCORECARD.md` are not frozen either; they are
record, not instrument.

## Freeze-integrity rule (both claims)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path;
a later restore does not un-block (the counter's arm reads commit history, not tip
equality); a touch makes the counter exit 2 `frozen_path_changed` and print no
`met_target`. Both counters implement the arm themselves; `frozen-path-preflight.py` is
the standalone gate that reports it before a commit is treated as landed.

## Satisfiability preflight (before any seat scores)

Every predicate clause above is one value the claim's own instrument computes, and each
was exercised before this freeze: the three `--selftest` receipts under
`controls/` (`preflight-selftest.txt`, `c1-selftest.txt`, `c2-selftest.txt`) cover every
red clause, and the two do-nothing controls were scored with the frozen counters. No
clause asks for a value the instrument cannot derive; provenance is stated as exact path
equality, never as "names a path".

## Sources

R45-C1 cites two rows opened this round, with their located quotes in
`corpus/lessons/round-45.md` `## Gate`:

- **S140** `https://git-scm.com/docs/git-status` — the porcelain-v1 stability guarantee
  and the `-z` machine-parsing paragraph; the dirty arm parses `--porcelain -z`.
- **S141** `https://git-scm.com/docs/git-diff-tree` — `--name-status` with `-z` uses NUL
  field terminators and does not munge pathnames; the commit arm parses that.

## Round shape

Two v1 waves under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 32–64 each): wave 1 verifies the freeze instruments and drafts the landing evidence
before data; wave 2 falsifies the landing after data. Seat counts, role mix and dead seats
come from `.ufo/waves/round-45/<wave>-results.json` and are reported from there.
