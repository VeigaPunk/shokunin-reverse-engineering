# R39CL2Registry — round-39 wave-1 scribe report (routed defect R38-CL2)

**Verdict: DEFECTS FOUND** — the registry table is drafted and covers all 13 files, but three of the
instruments it must register are defective or non-conformant: `tools/round-37/c1-counter.py` cannot
return a verdict at all, two chained report fields are decorative, and the three QUALITY-bound gates
still carry no self-test.

Base read for every statement: `a2f64e1da78afcf8cc39287106604dbcc270844c` (lane `main`). Nothing was
frozen, scored, committed or run against a K5/K6 carrier; no REA run was made.

## 1. Deliverable

- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/registry.md` — the SKILL.md-ready section:
  `### Round-35/37/38 instrument registry`, 7 columns in the round-36 order (`tool | gate or probe |
  verdict map (exit codes) | self-test command | pinned-value path | write scope | owner`), one row
  per file, plus notes and an explicit "could not verify" list.
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/` — 19 files: the receipts and the exact
  command index (`README.txt`), fixture commit ids (`fixture-commits.txt`), the three
  `freeze-drift` JSONs, three `intended-doc` JSONs, the two `registry-immutable` outputs, five
  `gen-controls` receipts, and the six `gen-squashfs` images.

Coverage of the requested set (every non-`__pycache__` file):

| dir | files | rows |
|---|---|---|
| `tools/round-35/` | `c1-coverage-counter.py`, `c2-calibration-counter.py` | 2 |
| `tools/round-37/` | `c1-counter.py`, `c1-run.sh`, `gen-squashfs.py` | 3 |
| `tools/round-38/` | `c1-counter.py`, `c1-run.sh`, `c2-counter.py`, `freeze-drift.py`, `gen-controls.py`, `intended-doc.py`, `registry-immutable.sh` | 7 |
| `tools/round-38/selftest/` | `dev-after.json`, `dev-before.json`, `dev-oracle.tsv`, `dev-le-xz.sqsh` | 1 row, declared **data, not an instrument** |

Classification rule applied: `PROTOCOL.md` §Gate standard (a *gate* is a re-runnable verdict script
with a declared verdict map and a self-invocation over isolated fixtures; a tool that cannot fail is
a *probe*). Tools with a working self-test → `gate`. Tools without one → `probe` + `no selftest`,
**unless** `corpus/QUALITY.md` binds them into admission — those are `gate` with the self-test
recorded as being added this round by `R39CL2Selftests` (`--selftest`). Bound by QUALITY:
`freeze-drift.py` (79, 80), `intended-doc.py` (81). `registry-immutable.sh` is registered as a gate on
the round-38 spot-check's classification plus CORPUS rule 2 — see §7.3.

Counts, 13 rows total: **7 gate** (`round-35/c1-coverage-counter.py`, `round-35/c2-calibration-counter.py`,
`round-38/c1-counter.py`, `round-38/c2-counter.py`, `freeze-drift.py`, `intended-doc.py`,
`registry-immutable.sh`), **5 probe** (`round-37/c1-counter.py`, `round-37/c1-run.sh`,
`gen-squashfs.py`, `round-38/c1-run.sh`, `gen-controls.py`), **1 data** (`round-38/selftest/`).

## 2. Verification performed (commands, outcomes, exit codes)

Ran with `cd <LANE>`, `TMPDIR=<seat scratch>`, `HYAKU_SCRATCH=/fast/scratch/hyaku`. Full list in
`evidence/README.txt`.

**Self-tests (the self-test-column claims, exercised):**

| command | exit | stdout |
|---|---|---|
| `python3 -I -B tools/round-35/c1-coverage-counter.py --selftest` | 0 | `C1_SELFTEST: ok` / `green=0 red=1` |
| `python3 -I -B tools/round-35/c2-calibration-counter.py --selftest` | 0 | `C2_SELFTEST: ok` / `green=0 red=1` |
| `python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 $PKG65` | 0 | `{"cases":15,"green_ok":1,"red_ok":14,"failures":[]}` |
| `python3 -I -B tools/round-38/c2-counter.py --selftest` | 0 | `{"cases":14,"green_ok":1,"red_ok":13,"failures":[]}` |
| `python3 -I -B tools/round-37/c1-counter.py --selftest --pkg65 $PKG65` | **2** | argparse: `--root, --rev, --freeze` required |
| same + `--root <LANE> --rev <BASE> --freeze <BASE>` | **1** | `FileNotFoundError` at `selftest`/`make_fixture` (`:323`) |

**Verdict maps exercised on isolated git fixtures** (`mktemp -d` under the seat scratch, identity
only via `-c user.name=fx -c user.email=fx@fx` inside the fixture, `rev-parse --show-toplevel`
asserted equal to the fixture path before its first commit):

- `freeze-drift.py`: clean `0`; one-commit drift `1` (verdict `drift`, `net_changed
  ["plans/round-38-claims.md"]`, `ships_freeze_bytes false`, commit `a0b577c4`); unknown revision `2`;
  freeze-not-an-ancestor `2`.
- `intended-doc.py`: repaired row naming the document that exists at base → `0` `bound`
  (`object_at_rev == object_at_base == 921b95ea…`); base tree with the un-named path → `1`
  `not-bound` (`intended path not named in the unit row`); unknown revision → `2`.
- `registry-immutable.sh`: status+used-by-only change → `0` silent; widened `scope` cell → `1`
  `S100 changed columns: 6`.
- `gen-controls.py` kinds `c1-1 c1-2 c2-1 c2-2 c2-3` → each `exit 0`, receipt `counter_exit 1`,
  `kill false`. `c1-0`/`c2-0` deliberately not exercised (they replay the live counters — L1's
  control seat; scoring the C1/C2 predicate at base from this seat would be an unowned score).
- `gen-squashfs.py`: `le`/`be`/`avm` gzip and `le` xz all exit `0`; magics `68737173` (`hsqs`) for
  LE, `73717368` (`sqsh`) for BE and AVM; a repeated `--endian le --comp gzip` build is
  byte-identical (`fb080c75b912cce0…`); missing operand → `2`.

**Harness usage paths (no REA invoked, no carrier touched):** `round-37/c1-run.sh` bare → `2`;
`before KNOPE` → `1` (`unknown carrier`); `round-38/c1-run.sh` bare → `1` (`${1:?}`), bad mode → `2`.

**Missing-argument exit codes:** `round-35/c1`, `round-35/c2`, `round-38/c1`, `round-38/c2`,
`freeze-drift`, `intended-doc` with no args → `2` each.

**Fixture digests** `tools/round-38/selftest/*` equal the round-38 wave record
(`.ufo/waves/round-38/w1/R38ExecSelftests.md:33-34`): `dev-after.json d9193aea…920ca9`,
`dev-before.json ff1587fe…fa9a57e`, `dev-le-xz.sqsh acc64a3d…3394b93`, `dev-oracle.tsv 69a8abd5…adcd67`.

## 3. Behaviour recorded (what each row asserts)

- **Counters are git-object readers.** `round-35/*`, `round-37/c1-counter.py`,
  `round-38/{c1,c2}-counter.py` read `git show <rev>:<path>` only; the r35 pair also writes
  `--json-out`. None has a digest-pinned `expected.json`; expectations are in the script constants,
  the frozen claims/carriers blobs or the selftest case table (round-36 registry limit 7 repeats).
- **The r38 pair is the only pair that both reads and writes the repository's own selftest fixtures**
  (`tools/round-38/selftest/{dev-after.json,dev-oracle.tsv}` and `tools/round-27/xpin-attribute.mjs`)
  from the **working tree**, so its self-test input moves with the worktree.
- **Receipts vs verdicts.** `round-37/c1-run.sh` and `round-38/c1-run.sh` are data producers:
  the r37 harness maps the child to `0/2/3` and records carrier sha256, `sasquatch_v4be`
  path/sha256/version, `unblob`, `rea_package_root`, UTC and exit; the r38 harness has **no map of
  its own** and returns the child's status.
- **The QUALITY gates read git state, not files:** `freeze-drift` = `git log freeze..rev` over
  pathspecs plus a net `git diff`; `intended-doc` = identity of `<rev>:<path>` vs `<base>:<path>`;
  `registry-immutable` = field-by-field comparison of `| S### |` rows at BASE and REV, allowing only
  columns 9/11/12.

## 4. Touched surfaces

Writes, in full: this report; `artifacts/R39CL2Registry/registry.md`; 19 files under
`artifacts/R39CL2Registry/evidence/`. **No** lane file was created or modified outside the seat's
report and artifact paths: `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
`SKILL.md`, `LOG.md` were read only. No VCS mutation: only read-only git
(`show`, `log`, `rev-parse`, `cat-file`, `ls-tree`, `diff`, `merge-base`) plus fixture-local
`init/add/commit` inside `mktemp -d` scratch with `-c user.name=fx -c user.email=fx@fx`. No
`pacman`, no install, no tool upgrade, no host service change, no `chattr`.

## 5. Integration instructions for L1 (exact SKILL.md edits)

1. **Replace** `SKILL.md:1285-1287` (the round-36 registry's limit item 8) with:

   ```
   8. This registry covers the two round-36 counters only. The round-35, round-37 and round-38
      instruments are registered in `### Round-35/37/38 instrument registry` below (round 39, seat
      R39CL2Registry), which discharges the debt reported in round 36. That section also records the
      row-3 finding that `tools/round-37/c1-counter.py` is unrunnable at this revision.
   ```

   Keep items 1-7 and 9-10 verbatim: item 9's provenance limit and item 10's C2 shortcut list still
   bind the round-36 pair, and the r38 counters inherit item 9's shape (they recompute an id, they do
   not authenticate provenance).

2. **Append** the registry section from `registry.md` at end of file (after line 1297's item 10), as
   `### Round-35/37/38 instrument registry`. Appending as `###` keeps it inside the existing
   `## Squashfs recursion through sasquatch — round 36` section, i.e. it does not disturb any `##`
   topology; a separate `##` heading is also defensible, and nothing mechanical depends on the choice
   (the only eight-cell section checks in the lane are `tools/round-35/c2-calibration-counter.py`
   `EIGHT_CELL_SECTIONS`, which names `### Round-32 instrument registry` and
   `### Round-34 run-6 instrument registry` only, and this section's 7-column rows match the
   round-36 table's own 7 columns).

3. Do **not** add `tools/round-38/selftest/` to the round-36 "Selftest fixtures" prose: its
   `dev-before.json` and `dev-le-xz.sqsh` are not read by any instrument under `tools/` (F8).

4. If `R39CL2Selftests` lands different flag spellings, correct rows 9-11 before the freeze; the
   rows currently record a plan, and the plan is listed in §7.6 as unverified.

## 6. Findings

**F1 (blocking for any R37-C1 citation) — `tools/round-37/c1-counter.py` cannot produce a verdict.**
`git()` (`:33-36`) runs without `text=True`, so `show()` returns bytes; `load_oracle` (`:93`) splits
`'\t'` on bytes → `TypeError: a bytes-like object is required, not 'str'`. Demonstrated at base:
exit `1` with a traceback. Its `--selftest` is double-broken: argparse marks `--root/--rev/--freeze`
required so `--selftest` alone exits `2`, and with placeholder args the selftest crashes
(`FileNotFoundError`, `make_fixture` `:323` never creates `corpus/knowledge`). `measure()` also holds
a spliced fixture-writing block (`:163-186`) that references an undefined `d` — the same block exists
in its proper place inside `selftest()` (`:304+`). Registered as `probe`, `no selftest`.

**F2 (the R38-CL2 ask is half-discharged) — three QUALITY-bound gates still have no self-test.**
`freeze-drift.py`, `intended-doc.py`, `registry-immutable.sh`: `grep -c selftest` = 0 in all three.
`PROTOCOL.md` §Gate standard requires a self-invocation asserting exit code and a stable finding on
isolated fixtures. Until `R39CL2Selftests` lands it, the honest status is "gate by criterion,
non-conformant self-test"; the rows say exactly that rather than claiming conformance.

**F3 — a crash reads as `failed` in all five Python counters.** Uncaught exceptions exit `1`, the
code reserved for `failed`; `2` (`could-not-evaluate`) is reachable only through explicit
`sys.exit(2)` / `Unevaluable` paths. F1 is the live instance. The registry's verdict map cells say
this in every affected row; a reader who trusts `1` as "measured miss" would mis-read a traceback.

**F4 — `round-35/c1-coverage-counter.py` receipt field `checks` is always all-true.** `:184` builds
`{f"c1_{i}": (f not in fails)}` over six literals (`entry_exist`, `trio`, …) that never occur as
whole entries in `fails` (which holds `entry_missing:<path>`, `trio_missing_source:<path>`, …), so
every value is `True` even when `pass` is false. Read `failing`/`pass`; the row records this.

**F5 — `round-38/c1-run.sh` has no verdict map of its own.** It returns the child's status:
REA's own exit codes propagate unmapped through `before`/`after`, `oracle` maps a `sasquatch-v4be`
failure to `1`, bad mode to `2`, and a missing argument to **`1`** (`${1:?}` — `round-37/c1-run.sh`
uses `2` for the same condition). No REA run was made here, so the propagated codes are unenumerated.

**F6 — `round-37/c1-run.sh` has an undeclared `exit 1`.** An unknown carrier id aborts under
`set -e` from the python lookup (observed: `unknown carrier KNOPE`, exit `1`), outside its documented
`0/2/3` map.

**F7 — `registry-immutable.sh` has no `2` code.** A bad revision makes the `git show` row set fail
under `set -e`, so bash exits with git's status (128 expected, not exercised). Undeclared ⇒ reads
`could-not-evaluate` under §Gate standard's default.

**F8 — two committed selftest fixtures have no consumer.** `tools/round-38/selftest/dev-before.json`
and `dev-le-xz.sqsh` are referenced by no file under `tools/` (`grep -rn` → only the round-36/38 wave
artifacts mention them); the r38 c1 self-test reads only `dev-after.json` + `dev-oracle.tsv`
(`c1-counter.py:273-274`, `gen-controls.py:42-43`). This is the round-36 D5 pattern repeating in the
round-38 directory; the registry's data row states which files are read so a later reader does not
assume the self-test exercises the BE/LE images.

**F9 — `gen-controls.py` is not independent of the counters it exercises.** Each kind builds its
fixture by importing `c1-counter.py` / `c2-counter.py` module code, so a counter and its control
share the fixture construction (the QUALITY 28 concern). Registered as a probe with that limit
stated; QUALITY 80's gate over its bytes is `freeze-drift.py` against this path, which is why the row
says the file must ship in the freeze commit.

**F10 (supporting, not a defect) — `gen-squashfs.py` is byte-stable.** Two `le/gzip` builds from the
same tree are byte-identical; `MKFS_TIME`, `UID` and block size are constants, so there is no
seed/time input. Relevant to R39-C2's "every carrier regenerates byte-identically from that seed"
premise: this generator has no seed parameter, so seed control must come from the tree content or a
wrapper — flagged for L1, not decided here.

## 7. Statements I could not verify (carried verbatim into `registry.md`)

1. `registry-immutable.sh`'s admission binding *by QUALITY*: no QUALITY row names it
   (`grep -n registry-immutable corpus/QUALITY.md` → 0 hits); the binding is CORPUS rule 2 plus the
   round-38 spot-check's §5 classification.
2. `gen-controls.py c1-0` / `c2-0` exit codes — not exercised (would score the live predicates).
3. `registry-immutable.sh`'s exit code on an unknown revision — inferred `[INFERENCE]` from `set -e`
   + git, not executed.
4. REA's own exit codes as propagated through `round-38/c1-run.sh` — no REA run in this wave.
5. Whether R35-C1/C2, R37-C1, R38-C1/C2 met or missed their targets at their measured revisions —
   only self-tests were exercised; this seat owns no score.
6. That `R39CL2Selftests` will land `--selftest` on the three QUALITY gates (and define a flag
   spelling for the bash script) — it has not run.
7. Whether `gen-squashfs.py` images are accepted by unblob / `sasquatch-v4be` / `unsquashfs` —
   acceptance is another instrument's verdict; only determinism, magic and exit codes were checked.

## 8. Out of scope (not done, by bounds)

- No edit to `SKILL.md`, `tools/`, `corpus/`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
  `LOG.md` — the table is a draft for the L1 to integrate and commit.
- No registry row for `tools/round-27/*` or any other round; `xpin-attribute.mjs` is recorded only as
  a shared dependency in the notes.
- No REA run, no carrier build, no held-out carrier, no C1/C2 claim scoring, no freeze, no commit.
- No tool installation or upgrade (nothing was needed; `python3`, `node`, `git`, `jq` already present).

## 9. Scratch and side effects

`S=/fast/scratch/hyaku/kaidoku-r39/R39CL2Registry` held the fixtures (`fx.*`, `fx2.*`, `fx3.*`), the
tree and the six images; the cited receipts were copied into `evidence/` and the scratch tree is
removed after writing. Two residual paths were created by tool code that hardcodes its own scratch
root and were **not** deleted, because that root is shared with peer seats running the same tools:
`/fast/scratch/hyaku/kaidoku-r37/selftest/green` (left by the crashed r37 self-test probe) and empty
`/fast/scratch/hyaku/kaidoku-r38/controls-*` directories. Neither is cited as evidence.

## 10. Artifact paths

- `Report: .ufo/waves/round-39/w1/R39CL2Registry.md`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/registry.md`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/README.txt`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/fixture-commits.txt`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/{freeze-drift-clean,freeze-drift-drift,freeze-drift-unknown-rev}.json`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/{intended-doc-bound,intended-doc-notbound,intended-doc-unevaluable}.json`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/registry-immutable-{scope.jsonl,ok.txt}`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/ctl-{c1-1,c1-2,c2-1,c2-2,c2-3}.json`
- `.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/img-{le,le2,be,avm,le-xz}.sqsh`
