# R46W1SentTools — scoped findings (adversarial review of `tools/round-46/`)

Seat: `R46W1SentTools` (leaf). Read-only on the lane; all writable output is in
`.ufo/waves/round-46/w1/R46W1SentTools/` (full report: `report.md`; raw receipts:
`receipts.json`, `ab.json`, `current.json`, `verify.json`, `frozen-probes.json`,
`frozen-c2.json`, `shrink-cli.json`, `freezeathead.json`; index: `receipts-table.md`).
Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1SentTools` was removed after the receipts
were copied. No installs, no lane writes, no git/jj mutation, no fixture outside `$S`.

## Bytes reviewed — two sets, because the lane moved under me

| set | commit | gate.py | attest.py | registry.py | census.py |
|---|---|---|---|---|---|
| declared freeze | `3182047` | `64626cca` | `dd1e7df1` | `307506d5` | `960c516d` |
| current | `22fd0d6b`/`c0112995` | `c3ba6b93` | `c4056131` | `5e16e4af` | `960c516d` |

Every finding is labelled **open** only where reproduced on that set.

## P0 (blocking) — the declared freeze is not the instrument, and it cannot score

Four commits in `3182047..HEAD` touch the frozen paths (`50862e4a`, `65678df0`, `04252247`,
`332f4884`). At HEAD the counters correctly refuse it:

```
attest.py --root . --freeze 3182047… --rev HEAD --no-battery   exit 2  frozen_path_changed
  frozen_path_changed = [tools/round-46/, …/attest.py, …/gate.py, …/registry.py]
  stdout sha256 47dc11dd28b2b526df108f00d3a5f80d9629bc496133acf13dbea840d5ed2881  17:15:00Z
```

and the frozen bytes are broken on both claims, so the freeze could never have scored:

* **C1** — `attest.py:322` calls `REF.search`; `REF` is undefined in the frozen file (only
  `HARD_REF`/`LOOSE_REF`). Any artefact that passes the structural clauses then dies in the
  battery with `NameError`, and because the frozen `gate.main_guard` (gate.py:215-221) returns
  the int `2` while `attest.py:476` unpacks it, the outcome is **exit 1 + traceback**, not
  exit 2 — a reincarnation of `R45-CL13`(f). The frozen `--selftest` (15 cases) never runs the
  battery, so `cases=15 failures=0` is green over a battery that cannot execute.
* **C2** — a legitimate green fixture with the real counting command:
  `exit 1  failing=["battery v1_green 5 != 7"]`; clause 6 is unsatisfiable at the freeze.

**Action:** re-declare the freeze at the commit carrying the final bytes, as an explicit
superseding amendment in `plans/round-46-claims.md`; stop citing `3182047` (and the
`cases=15` / `sha256:dd1e7df1…` record entries that describe it).

## Open findings at current bytes

| id | sev | input → verdict | code | evidence |
|---|---|---|---|---|
| **S1** | HIGH | `census.json` = `{"paths":["tools/round-46/a.py"]}` while `census.py` derives 3 → **exit 0, met** | `registry.py:125 load_scope` reads the checked-in file; `:50 "scope_size": None`; `census.census()` never called | `scope_size 1`, `failing []`, sha `44c6e0af…` 17:11:53Z |
| **S2** | HIGH | block 23 = 13 rows `\| R45-CL<id> \| filler \| commit \| 0..2 \|` + pin + S142 + 6 line-selected refs → **exit 0, met**, battery 9/9/0/1/crash 0 | `attest.py:150 score` reads only cell 0 (ids), cell 2 (arm substring), cell 3 (0/1/2); column 1 and exit semantics unvalidated | sha `34cfb222…` 17:11:53Z; frozen structural pass sha `3afd25e5…` |
| **S3** | HIGH | an earlier **fenced** `## Queue-drain craft (example) ` holding the good block; the real section has no block 23 → **exit 0, met** | `attest.py:88 craft_section` = `skill.split(CRAFT,1)[1]`, first occurrence, fence/comment-blind | measured section head `["(example) "]`, sha `1f9893e5…`; frozen sha `1427ae7f…` |
| **S4** | MED | rows inside a comment opened **mid-line** (`note: <!-- begin`), and inside a ``` fence closed by `~~~` → **exit 0, met** (both) | `registry.py:85 rows_in_section`: fence toggled by any ``` /`~~~` (line 91); comment entered only if the line *starts* `<!--` (line 99) | sha `53b1a4e5…`, `ffdee675…`; frozen `95f831da…`, `57f1bf18…` |
| **S5** | MED | rows with 5 of 7 house columns empty → **exit 0, met** | only header (169) and cells 0/2 (182/196) are read | sha `e64b7fc9…` |
| **S6** | MED | `--json-out .git/config`, `.git/HEAD`, `.git/objects/info/alternates`, `.ufo/state/*` → accepted; write landed (0644) | `gate.py:198 out_path`, GRADED list at `:208` excludes `.git`/`.ufo` | `e2_out_path`, `7_write_scope` |
| **S7** | MED | `census.py --out <outside lane>` → written; `--out <fixture>/tools/round-46/a.py` → tool clobbered by JSON, exit 0 | `census.py:65-71`, no `gate.out_path`, `--rev` unresolved | `p8_census_out`, `e3_*` |
| **S8** | MED | measured repo with `core.fsmonitor` → script executes during `git status`; counter still exit 0 met | `gate.py:43 git()` inherits repo config; `:132 dirty()` now called from `freeze_state` | marker file created, sha `c262081a…` 17:13:16Z |
| **S9** | LOW | cited file with `0xFF` → frozen exit 1+traceback, current exit 2 `unhandled UnicodeDecodeError` | `gate.py:43 text=True` (strict UTF-8) | `p9_nonutf8_blob`, earlier lane run |
| **S10** | LOW | `HYAKU_SCRATCH=<lane>/tools/round-46` accepted; `mkdtemp` creates a dir inside the frozen surface | `gate.py:213 scratch()` rejects only `/tmp`,`/var/tmp` | `p5_scratch_inside_frozen` |
| **S12** | LOW | `--no-battery` → `exit 0, met_target true` with clause 7 never computed (receipt has no `battery` key at all) | `attest.py:441 evaluate` skips the battery but `score()` still sets `met_target = not failing` | frozen C1 structural run sha `3afd25e5…`; `e5/e6` earlier-lane receipts |
| **S11** | LOW | record drift: `cases=15` only true of frozen bytes (current 18); `cases=12` vs claims' 11; bare `--selftest` exits 2 (argparse requires `--root/--freeze/--rev`) | `main()` parses before the selftest branch | `8_selftests` |

## Verified negatives — closed, with the probe that shows it

* **(a) command injection — no.** All `git` calls are argv lists; no `shell=True`/`os.system`/
  `eval`/`exec` in the four files. SKILL rows and claims entries never reach a command.
* **(b) fixture path traversal — no.** `os.path.join(d, p)` (`registry.py:364`) is reached only
  after `gate.show` returned a body; git refuses `..` and leading `/` in `<rev>:<path>`
  (`HEAD:../x` → “outside repository”, `HEAD:/tmp/pwn` → “does not exist”); `HEAD:./tmp/pwn`
  resolves but joins inside `d`; a `mktree` entry literally named `..` is not traversable.
* **(c) hostile SKILL/census — yes**: S1–S5.
* **(d) scratch cleanup — no leak.** No `fx-*`/`kaidoku-*` survives a CLI run; `evaluate()`
  removes the battery root in `finally`, which also reaps a fixture left by an exception in
  `fixture_repo` (called outside its `try`, `attest.py:362-386`).
* **(e) attacker-controlled refs — no, for both counters.** `resolve()` returns null for
  `--all`, `-h`, `--branches`, `--revs-only`, `--end-of-options`, `--glob=*`, `--output=…`
  → exit 2 `unknown … revision`; afterwards base/tip are hex and `base..tip` is used with `--`.
  `census.py`'s unresolved `--rev` reaches `git show`, but the appended `:path` always has a
  slash, so `--output=` cannot create the file (measured: `fatal: could not open '…/injx:plans/…'`).
* **(f) timeouts — read path complete** (every `gate.git` call has `timeout=120`); **fixture
  path has 12 untimed `subprocess.run(["git", …], check=True)` calls** against tool-created
  fixtures only → worst case a slow `git add -A`, no escape.
* **(g) frozen-set shrink (wave-1 HIGH) — closed at current, open at the freeze.** At
  `3182047`: tamper + rewritten `## Frozen paths` → `exit 0`, `frozen_derived ["corpus/unused.txt"]`,
  `frozen_path_changed []`. At current: tamper-only and tamper+shrink both `exit 2
  frozen_path_changed` for `attest.py` and `registry.py` (`c1_tamper_plus_shrink`,
  `c2_tamper_plus_shrink`, 17:13Z). My first run of this probe reported it open at current
  bytes — that was a stale `gate` module imported in-process; the CLI receipts above are the
  ones to trust.
* **(h) uncommitted frozen tool (wave-1 HIGH) — closed at current.** Clean → exit 0; one
  appended line in `tools/round-46/gate.py` → `exit 2 frozen_worktree_dirty`,
  `dirty ["tools/round-46/gate.py"]`.

## What the L1 should do with this

1. Re-declare the freeze (P0) before landing anything; do not cite `3182047`.
2. S1 and S2 are the round-45 disease returning: both are `met_target: true` with an artefact
   that does no work, on the bytes that would be landed.
3. S3 means `SKILL.md` must contain exactly one `## Queue-drain craft ` heading, or the verdict
   may describe a fenced example rather than the landed block.
4. Self-test cells in block 23 / registry rows must read
   `` `python3 -I -B tools/round-46/attest.py --root . --freeze x --rev y --selftest` ``.
5. Don't run `census.py --out` against a tracked path until S7 is fixed.
