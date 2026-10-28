# R46W1MutGate — mutation probe of `tools/round-46/gate.py`

Seat: `R46W1MutGate`, round 46, wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Frozen bytes: `31820472784284727546808acc31b3ea1e73919b`. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1MutGate`, removed at end of run.

**Result in one line: all six assigned mutants survive both frozen `--selftest`s with
byte-identical output (0 of 6 killed). Behavioural probes show five of the six are real
defects, not equivalent mutants — the frozen harness cannot see any of them. Two of the
defect families these mutants open were closed at HEAD by the post-freeze `F5` commit (the
tip-only frozen-set derivation, and the dead `dirty` arm); at HEAD one mutant is caught, by
`attest.py`'s selftest only. The rest are open at HEAD too.**

---

## 1. Bytes under test, and a fence-post problem with the freeze

| file | sha256 @ freeze `3182047` | sha256 @ HEAD `c0112995` | same |
|---|---|---|---|
| `plans/round-46-claims.md` | `a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` | `a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` | yes |
| `tools/round-46/attest.py` | `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb` | `c405613170f0581661b9e2afb4bf278da8ac1f936eeb00eb4b456a9e70ad8e5c` | **NO** |
| `tools/round-46/gate.py` | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` | **NO** |
| `tools/round-46/registry.py` | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` | `5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73` | **NO** |
| `tools/round-46/census.py` | `960c516d3b5cb1bb0306bf7f44f848a76b9c795c5319328954b5021b234c1fd5` | `960c516d3b5cb1bb0306bf7f44f848a76b9c795c5319328954b5021b234c1fd5` | yes |

**Four** commits touched the frozen paths inside `3182047..HEAD`:

```
$ git log --format='%h %s' 3182047..HEAD -- plans/round-46-claims.md tools/round-46/
50862e4a round-46: complete the freeze — … (gate.py, attest.py, registry.py)
65678df0 round-46 F3: the freeze is the instrument that can actually be scored — … (attest.py)
04252247 round-46 F4: the v1 registry profile applies its own loose checks … (registry.py)
332f4884 round-46 F5: close the two HIGH instrument defects wave 1 found — … (gate.py)
$ git rev-list --count 3182047..HEAD -- plans/round-46-claims.md tools/round-46/
4
```

Consequence, measured over every candidate pair
(`receipts/freeze-admissibility.txt` was produced in scratch, summary in §6):

* `--freeze 3182047 --rev <anything after 50862e4a>` → **exit 2 `frozen_path_changed`**,
  for every rev without exception (the frozen tool bytes moved).
* The only revs that score `exit 0 / met_target true` are pairs whose freeze is itself a
  post-freeze commit, up to and including `--freeze <rev>`.

So the round's own instrument refuses the round's own declared freeze, and the green
numbers that were landed (`1e32827b`, "both claims met at 0425224") come from a freeze that
is not the commit the plan defines as the freeze. That is a claims-level issue for L1, filed
as **F-D** below; it is not caused by any mutant.

Mutation sites are quoted at frozen line numbers:

| id | site | mutation |
|---|---|---|
| m1 | `gate.py:99` | delete `--diff-merges=first-parent` from the `git log` argv |
| m1b | `gate.py:99` | swap the two flags: `--diff-merges=first-parent -m` |
| m2 | `gate.py:159` | `changed = []` (blob arm dropped) |
| m3 | `gate.py:69` | `frozen_set` returns a hard-coded two-entry list, claims file unread |
| m4 | `gate.py:136` | `["--", pathspecs[-1]]` (replace, not union) |
| m5 | `gate.py:179` | `return path, None` before the lane/graded checks |
| m6 | `gate.py:40` | `TEMP_PARTITIONS = ()` |

Each mutation is a one-line change at the site above; the exact unified diff is quoted at the
start of its subsection in §4, so every mutant can be re-applied to a scratch copy in a
minute. The mutated trees themselves lived only in scratch and were deleted with it.

## 2. Harness and the runnable form of `--selftest`

`--root/--freeze/--rev` are `required=True`, so the plan's documented invocation
(`attest.py --selftest`) exits 2 from argparse with empty stdout — `R46-CL8` is correct and
applies to attest as well:

```
$ python3 -I -B tools/round-46/attest.py --selftest
usage: attest.py [-h] --root ROOT --freeze FREEZE --rev REV ...
attest.py: error: the following arguments are required: --root, --freeze, --rev
exit=2   stdout sha256 3ed94b41f2837c05d27b9c05e94e8b82de953e398d3936edf35a3550079069e9
```
(`receipts/` note only; the live-lane run in §7 documents it.) The runnable form used here
passes dummy required args; `selftest()` returns before they are read:

```
python3 -I -B <tools>/attest.py   --root <tools-root> --freeze 000…0 --rev 000…0 --selftest
python3 -I -B <tools>/registry.py --root <tools-root> --freeze 000…0 --rev 000…0 --selftest
```

Baseline on pristine frozen bytes (`gate.py = 64626cca…`), python 3.14.8, git 2.56.0:

| counter | exit | stdout sha256 | banner |
|---|---|---|---|
| `attest.py` | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | `ATTEST_SELFTEST: cases=15 failures=0` |
| `registry.py` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | `REGISTRY_SELFTEST: cases=12 failures=0` |

`attest` prints **15**, which matches the claims file. `registry` prints **12**, the claims
file says 11 — `R46-CL8` corroborated independently. At HEAD the same two commands print
`cases=18 failures=0` and `cases=12 failures=0`.

## 3. The matrix

Every row is the same bounded detector (both `--selftest`s) on a fresh copy of the tree.
`mutated ≠ base` is confirmed by the `gate.py` sha256 on each row. Citable receipt with
command, exit code, stdout sha256 and UTC timestamps: `receipts/mutation-matrix.json`.

| tree | mutation | gate.py sha256 | attest exit / stdout sha | registry exit / stdout sha | verdict |
|---|---|---|---|---|---|
| `base` | none (frozen) | `64626cca…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | baseline green |
| `m1` | drop `--diff-merges=first-parent` | `6aa38854…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m1b` | reorder the two flags | `c2217850…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m2` | drop the blob arm | `4617cb72…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m3` | hard-coded frozen list | `214cc6a0…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m4` | `dirty` replaces | `53ab144f…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m5` | `out_path` passthrough | `1a0edb91…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `m6` | `/tmp` scratch allowed | `9b904d8a…` | 0 / `ac22e9c7…` | 0 / `0fa8c31a…` | **SURVIVES** |
| `headbase` | none (HEAD bytes) | `c3ba6b93…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | baseline green |
| `h1` | m1 at HEAD | `54686137…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | SURVIVES |
| `h2` | m2 at HEAD | `482d0887…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | SURVIVES |
| `h3` | m3 at HEAD | `fa6f4287…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | SURVIVES |
| `h4` | m4 at HEAD | `73975595…` | **1** / `b19cb61b…` | 0 / `0fa8c31a…` | **KILLED by attest** |
| `h5` | m5 at HEAD | `1479ebfb…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | SURVIVES |
| `h6` | m6 at HEAD | `ce7709ca…` | 0 / `6aa73c61…` | 0 / `0fa8c31a…` | SURVIVES |

Mutation score on the frozen instrument: **0/6**. On HEAD bytes: **1/6**, and only by
`attest.py`; `registry.py`'s selftest is blind to every mutation including the one its own
counter would execute.

Every surviving mutant produced **byte-identical stdout** to its baseline. That is the
strongest form of survival: the harness output is not merely still-green, it is unchanged.

## 4. Each mutant: real defect, or equivalent?

### m1 / h1 — `--diff-merges=first-parent` dropped (`gate.py:99`)

```diff
-    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
+    r = git(root, "log", "-m", "--name-status", "-z",
```

Harness: survives both, at both byte heights. Real defect: **yes, but in the over-report
direction only.**

Direction probe (`probe/p1c.py`, `receipts/p1c-merge-direction2.json`), frozen file
`tools/round-46/frozen.py`, three merge shapes, `touched[]` for that file only:

| shape | A frozen (`-m --diff-merges=first-parent`) | C m1 (`-m`) | D no merge flags (R45-CL6's hole) |
|---|---|---|---|
| evil merge (resolution is the only edit) | sees | sees | **misses** |
| side commit edits, merge keeps it | sees | sees | sees |
| frozen file changed *before* freeze, merge introduces nothing | **clean** | **sees (false positive)** | clean |

`{paths seen by A} ⊆ {paths seen by C}` in every shape: plain `-m` diffs the merge against
*both* parents, so dropping the flag can only add paths. It can never hide a tamper.

End-to-end verdict change (`probe/p1p2_final.py`, P1b): one clean merge, frozen **file**
entry, `freeze..rev` = the merge commit only.

| tree | exit | touched | blob_changed | restored |
|---|---|---|---|---|
| `base` | **0** | `[]` | `[]` | `[]` |
| `m1` | **2** | `[tools/round-46/gate.py]` | `[]` | `[tools/round-46/gate.py]` |
| `h1` (HEAD) | **2** | `[tools/round-46/gate.py]` | `[]` | `[tools/round-46/gate.py]` |

Classification: **coverage hole with a real defect — a clean history is scored
exit 2 `frozen_path_changed`, i.e. an admissible score is destroyed, and the receipt
additionally calls an untouched file `restored`.** Fail-closed, so it cannot inflate a
score; it can only refuse one. No fixture in either selftest builds a merge at all
(`grep -n 'merge --no-ff\|"merge",' tools/round-46/*.py` → no hit outside the vocabulary
tuple and a table row), which is exactly why it survives.

### m1b — the R46-CL6 reorder (`--diff-merges=first-parent -m`)

Survives both selftests (identical stdout). Behaviourally identical to m1 in every shape I
measured: the later flag wins, so the merge is diffed against both parents — a **superset**,
not a return to blindness.

**This contradicts the direction recorded in `corpus/lessons/round-46.md` `R46-CL6`**, which
says the reorder "restores the very blindness `R45-CL6` was about". Measured on git 2.56.0
the reorder widens the arm (it reports `M` where the frozen instrument reports nothing) and
never narrows it; the shape that is genuinely blind is `git log --name-status` with **no**
`-m` at all (column D above). `-m` is the load-bearing token; `--diff-merges=first-parent`
is the narrowing token. Either way the flag order is unenforced by the selftests — a
`R46-CL6` selftest case is still worth adding, but its stated failure mode should be
corrected to "over-reports", not "goes blind".

### m2 / h2 — blob arm dropped (`gate.py:159`)

```diff
-    changed = blob_changed(root, base, tip, entries)
+    changed = []  # MUTANT m2
```

Harness: survives both at both heights. On the **real lane** the receipt changes while the
exit code does not (`receipts/real-base-attest.json` vs `receipts/real-m2-attest.json`,
`--freeze 3182047 --rev c0112995 --no-battery`):

| tree | exit / reason | `frozen_path_changed` | `blob_changed` |
|---|---|---|---|
| `base` | 2 `frozen_path_changed` | `['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']` | `['tools/round-46/']` |
| `m2` | 2 `frozen_path_changed` | `['…/attest.py', '…/gate.py', '…/registry.py']` — directory entry gone | `[]` |

(identical shape in `real-base-registry.json` / `real-m2-registry.json`.)
Real defect: **yes at the receipt level; not verdict-level over 13 tamper shapes.**

`probe/p2e.py` matrix (`receipts/p2e2-base.json`, `receipts/p2e2-m2.json`), 5 shapes against a
frozen **file** entry and 8 against a frozen **directory** entry (edit, edit-then-restore,
unrelated-only, rename-away, chmod-only, copy-into-dir, rename-within, delete-readd,
chmod-inside, symlink-add): **exit code identical on 13/13**; `blob_changed` differs on **8/13**
and `restored` on **2/13** (exactly the two tamper-kept shapes at a frozen file entry: `edit`
and `rename-away`).

The sharp one (`probe/p1p2_final.py`, P2b — tamper committed and never reverted):

| tree | exit | touched | blob_changed | restored |
|---|---|---|---|---|
| `base` | 2 | `[gate.py]` | `[gate.py]` | **`[]`** |
| `m2` | 2 | `[gate.py]` | `[]` | **`[gate.py]`** |

`restored` is defined by the claims file as "a path the history arm saw and the blob arm
finds clean". Under m2 it means "a path the history arm saw", so a persisted tamper is
reported as restored, and the claim's "independent blob arm" agreement is never checked.
Classification: **coverage hole; the arm is corroborating for the verdict on every shape I
could build, and load-bearing only for the receipt's `restored` field.** Bounded statement: I
did not prove verdict-equivalence in general — I found no shape where the blob arm alone
changes the exit code, including renames with the destination inside a frozen directory
where `--name-status -z` emits `R100\0old\0new\0` and the token-pair parser drops `new`
(`probe/p2d.py`: the source name is in scope, so the history arm still fires).

### m3 / h3 — frozen set hard-coded instead of derived (`gate.py:69`)

```diff
+    return [("plans/round-46-claims.md", False), ("tools/round-46", True)], None
     body = show(root, rev, claims)
```

Harness: survives both at both heights. Real defect: **yes**, and it is the R45-CL18 property
("the file is the rule") that it removes.

* **Equivalent on this round's data**: the hard-coded pair equals what the claims file
  derives at HEAD (`['plans/round-46-claims.md', 'tools/round-46']` for both trees), so no
  probe on round-46 data can separate them — the mutant is invisible because it is currently
  correct by accident.
* **Non-equivalent one claims-file edit away** (`probe/p3b.py`,
  `receipts/p3b-base.json` / `receipts/p3b-m3.json`; gate shas `64626cca…` / `26cdd449…`, the
  same one-line insertion as §3's `214cc6a0…` with the comment placed differently). A claims
  file naming a **third** frozen path, and one commit touching only that path:

  | tree | `frozen_derived` | `touched` | exit | `evidence/C1.json` at rev |
  |---|---|---|---|---|
  | `base` | `[tools/round-46/, claims, evidence/C1.json]` | `[evidence/C1.json]` | **2 `frozen_path_changed`** | `C1-TAMPERED` |
  | `m3` | `[tools/round-46/, claims]` | `[]` | **0, clean** | `C1-TAMPERED` |

  A tampered frozen entry, scored clean. Its second case (the claims file deleted in
  `freeze..rev`) separates the *reason* rather than the exit code: pristine
  `2 claims file absent at rev`, mutant `2 frozen_path_changed` — both refusals, different
  evidence.

Classification: **coverage hole; latent soundness defect.** Detector that would catch it: a
selftest fixture whose claims file lists a path the hard-coded list does not, plus a commit
touching it.

### m4 / h4 — `dirty` replaces instead of unions (`gate.py:136`)

```diff
     if pathspecs:
-        args += ["--", *pathspecs]
+        args += ["--", pathspecs[-1]]  # MUTANT m4
```

*Frozen instrument:* `gate.dirty` has **no caller** — `grep -n 'gate\.dirty\|\.dirty('
tools/round-46/*.py` finds none, and exec-line coverage confirms it (0/9 lines executed by
either selftest). m4 is therefore an **equivalent mutant of the frozen instrument**: it cannot
change any verdict, and it survives for a structural reason, not a tuning reason.

*HEAD instrument:* `332f4884` ("F5") added the caller `dirty(root, paths)` and a
`frozen_worktree_dirty` exit 2. The union is now load-bearing, because the frozen set has two
entries and `paths` puts the directory first:

```
paths = ["tools/round-46/", "plans/round-46-claims.md"]   →  mutant scans only the claims file
```

| fixture (HEAD bytes) | pristine | h4 |
|---|---|---|
| `tools/round-46/t.py` dirty | exit 2 `frozen_worktree_dirty`, `dirty=[t.py]` | **exit 0, clean** |
| `plans/round-46-claims.md` dirty | exit 2, `dirty=[claims]` | exit 2 (the only pathspec left) |
| nothing dirty | exit 0 | exit 0 |

(`probe/p4b.py`, `receipts/`.) At HEAD this **is a false clean** — an uncommitted edit to a
frozen tool scores green. It is killed there by `attest.py`'s case
`red-dirty-frozen-tool-is-exit-2` (expect 2, got 0), which is the one kill in the whole
matrix; `registry.py`'s selftest does not have that case and does not catch it.

Classification: **equivalent at the freeze; real false-clean defect at HEAD; caught by one of
the two counters only.** This is the calibration point of the whole probe: whether a mutant
matters depends on which byte height you mutate, and the two counters' harnesses have
different coverage of the same shared core.

### m5 / h5 — `out_path` returns the path unchanged (`gate.py:179`)

```diff
     if not path:
         return None, None
+    return path, None  # MUTANT m5
     full = os.path.realpath(path)
```

Harness: survives both at both heights — `out_path` is **never executed** by either selftest
(0/12 exec lines). Real defect: **yes, severe.** End-to-end through the real CLI, on a fixture
lane (`probe/p5b.py`, `--json-out` pointed at the fixture's own graded surface):

| tree | `--json-out SKILL.md` | SKILL.md overwritten | exit |
|---|---|---|---|
| `base` | `{"reason": "--json-out inside a graded or frozen surface: SKILL.md"}` | **no** | 2 |
| `m5` | the counter's JSON receipt | **yes** | 1 |
| `h5` | the counter's JSON receipt | **yes** | 1 |

The same holds for `plans/round-46-claims.md` (frozen bytes). Classification: **coverage
hole; the R45-CL22 guard can be deleted with the harness still green.** Compounding scope
note — `out_path` refuses against the static `GRADED` tuple, not against the derived frozen
set, so a frozen path outside `GRADED` is accepted even by the pristine instrument
(`probe/p5c.py`: `notes/frozen.md` "frozen, NOT graded" → `allowed=True`, base bytes). It does
not bite round 46 because both frozen entries live under `plans`/`tools`, which are `GRADED`.

### m6 / h6 — `/tmp` accepted as a scratch root (`gate.py:40`)

```diff
-TEMP_PARTITIONS = ("/tmp", "/var/tmp")
+TEMP_PARTITIONS = ()  # MUTANT m6
```

Harness: survives both at both heights. Real defect: **yes** — a direct call creates evidence
under a shared temporary partition (`probe/p46_m4_m6.py`):

| env | pristine | m6 |
|---|---|---|
| `TMPDIR=/tmp` | `(None, 'scratch root is a temporary partition: /tmp')` | `('/tmp/p6-ghp5ektd', None)` |
| `TMPDIR=/var/tmp` | refused | `('/var/tmp/p6v-khy37emf', None)` |
| both unset | refused, `no HYAKU_SCRATCH/TMPDIR root set` | refused (that branch is untouched) |

Classification: **coverage hole; a contract violation the harness cannot see.** `scratch`'s
refusal branches are unexecuted: the selftests set `HYAKU_SCRATCH` to a good root and take the
success path (line 197, the `TEMP_PARTITIONS` refusal, and line 194, the "no root" refusal,
are both missed). Detector: one selftest case that sets `TMPDIR=/tmp` with `HYAKU_SCRATCH`
unset and expects exit 2.

*Disclosure:* this probe created and immediately removed `/tmp/p6-*` and `/var/tmp/p6v-*`.
The seat contract forbids writing under `/tmp`; the write is produced by the mutant itself
and is what the probe measures. Nothing was left behind (`ls -d /tmp/p6-*` → empty).

## 5. Why they survive: executable-line coverage of `gate.py`

`sys.settrace` over one `selftest()` per counter, intersected with the compiled line table
(`probe/cov2.py`; receipts in `receipts/coverage/`). Docstrings and `def` lines excluded —
they emit no line events.

Frozen bytes (`64626cca…`), `hit/total` executable lines:

| function | via `attest --selftest` | via `registry --selftest` |
|---|---|---|
| `git`, `show`, `blob`, `resolve` | 2/3 each (missed line = its own `def`, executed at import before tracing starts) | 2/3 each |
| `frozen_set` | 17/21 (missed 63 `def`-at-import, 71/73 claims-absent, 87 empty-section) | 17/21 |
| `history_touched` | 16/19 (missed 91 `def`-at-import, 98 empty-paths, 102 log-failed) | **11/19** (also 108–112: the token-pair loop body) |
| `blob_changed` | 9/11 (missed 117 `def`-at-import, 125 directory-append / elif-arm) | 8/11 (missed 117, 125, 128) |
| `dirty` | **0/9 — never entered** | **0/9 — never entered** |
| `freeze_state` | 22/27 (missed 144 `def`-at-import, 149/151 unknown-rev, 154/158 ancestry+claims errors) | 20/27 |
| `out_path` | **0/12 — never entered** | **0/12 — never entered** |
| `scratch` | 7/12 (missed 190 `def`-at-import, 194 no-root, 197 temp-partition, 201/202 OSError) | 7/12 |
| `emit` | **0/8 — never entered** | **0/8 — never entered** |
| `main_guard` | **0/6 — never entered** | **0/6 — never entered** |

(The `<module>` row is 0/13 for both: the module was imported before tracing began, so its
`def` lines never fire. That is an artifact of the instrument, not a hole; I note it so the
missed-line lists are not over-read.)

Frozen totals: 79/150 (`attest`), 71/150 (`registry`). HEAD totals: 102/166, 91/166.

The survivors follow mechanically: m4/m5 live in functions the selftests never enter at the
freeze; m6 lives in an unexecuted branch; m1/m2 live in branches exercised only by
single-parent histories (no merge fixture exists anywhere in `tools/round-46/`).

## 6. Instrument findings that are not mutants (for L1, not fixed here)

**F-A — `--no-battery` yields `met_target: true` with clause 7 unrun and unrecorded.**
`receipt["met_target"] = not failing`; the battery clauses are appended only when
`battery is not None`, and `evaluate(..., with_battery=False)` passes `None` and adds no
`battery` key at all. Measured on the real lane, frozen bytes:

```
python3 -I -B tools/round-46/attest.py   --root <lane> --freeze 04252247 --rev 1e32827b --no-battery
  → met_target True, failing [], key "battery" ABSENT
python3 -I -B tools/round-46/registry.py --root <lane> --freeze 04252247 --rev 1e32827b --no-battery
  → met_target True, failing [], key "battery" ABSENT
```
The `failing` list does not name the skipped clause, so a receipt scored this way is
indistinguishable from one that ran the 9-forgery battery. In `evaluate`'s `elif with_battery`
branch the skip is recorded (`{"skipped": …}`), but only when the artefact already fails a
structural clause — the green path has no such record when the flag is used.

**F-B — the `--freeze` argument is unvalidated, and `freeze == rev` scores green.**
Nothing derives the freeze from the claims file's origin commit; `gate` only checks ancestry.
Measured against the real lane:

* HEAD bytes, full battery, `--freeze c0112995 --rev c0112995` → `exit 0`,
  `met_target true`, `battery {forgeries_total 9, v1_green 9, v2_green 0, genuine_green 1}`,
  `rows 13`, `rule_blocks 23` (`receipts/selfref-attest-fullbattery.json`).
* Frozen bytes, `--no-battery`: **19 of the 25** revisions I enumerated score
  `exit 0 / met_target true` as their own freeze (every green revision in the round).

The freeze-integrity clause is therefore vacuous for any caller who picks the measured
revision. The receipt does record the freeze used (`"freeze": <oid>`) and `frozen_derived`,
so the only defence is that the L1 reads those two fields — nothing in the instrument refuses
`freeze == rev`.

**F-C — the frozen `gate.py` (3182047) is defeated by a one-commit scope shrink.** One commit
that (a) tampers a frozen tool and (b) rewrites `## Frozen paths` to a single untouched decoy
entry scores **exit 0, clean**, with the tampered tool at `rev`
(`probe/p3_shrink.py`; `counter_at_rev = TAMPERED`). The frozen instrument derives the set at
`tip` only. HEAD bytes (`332f4884`, base∪tip union) return exit 2 on the same attack. Round 47
should carry the union property as a *frozen* property, and a selftest case for it; the
round-46 plan's clause 8 is only half-satisfied by the bytes it froze.

**F-D — the plan's freeze commit cannot produce a score.** See §1: every
`--freeze 3182047 --rev <later>` is exit 2 `frozen_path_changed` (4 post-freeze commits touch
the frozen paths). The landed green receipts necessarily cite a *later* freeze. Either the
plan's freeze hash must be restated to the commit that carries the final instrument bytes, or
the instruments must be declared outside the freeze — as written, the claim is unsatisfiable
at the freeze it names.

**F-E — `corpus/lessons/round-46.md` `R46-CL8` corroborated and extended.** Bare `--selftest`
exits 2 from argparse for **both** counters (registry's usage line was the only one recorded);
registry prints `cases=12`, not the plan's 11; attest prints `cases=15` at the freeze and
`cases=18` at HEAD.

**F-F — `out_path`'s "frozen" half is the static `GRADED` tuple, not the derived frozen set.**
A frozen path outside `GRADED` is accepted (`probe/p5c.py`: `notes/frozen.md` → allowed at the
pristine bytes). Harmless for round 46, wrong for any round that freezes something else.

**F-G — the two counters' selftests do not cover the same core.** `attest.py` at HEAD kills m4;
`registry.py` does not, for the same `gate.py`. Any argument of the form "the harness would
catch a regression in the shared core" is true for one counter and false for the other.

## 7. Restoration, hygiene, verification not run

* Originals never written: the lane's frozen bytes were read with `read`/`git show` only.
  Final `sha256sum` of the live lane files and `git status --porcelain -- tools/round-46
  plans/round-46-claims.md` (empty) are in §1's command output; every mutation happened in
  `/fast/scratch/hyaku/kaidoku-r46/R46W1MutGate/<tree>/` copies, which were deleted.
* `$S` removed at the end of the run; `/tmp` and `/var/tmp` leftovers from the m6 probe were
  deleted by the probe (`ls -d /tmp/p6-*` empty).
* Tooling installed: none. `pacman` untouched (host transactions paused); no `uv`/`npx`/binary
  install was needed. python 3.14.8, git 2.56.0 as found.
* Reproduce: `probe/` holds every driver; `receipts/mutation-matrix.json` holds the 30-row
  matrix with exact commands, exit codes, stdout sha256 and UTC start/end times.
* Not run (and therefore not claimed): the full 9-forgery battery per mutant. The frozen
  `attest.py` cannot run it at all: its self-mutation `m_self_refs` references an undefined
  `REF` (`attest.py:322` at the freeze), `gate.main_guard` catches the `NameError` but
  returns an `int` (the freeze's signature), so `evaluate`'s `code, receipt = gate.main_guard(…)`
  raises `TypeError: cannot unpack non-iterable int object` and the process exits **1** with a
  traceback after printing `{"reason": "unhandled NameError: name 'REF' is not defined"}`.
  Measured on the real lane, frozen bytes, `--freeze HEAD --rev HEAD`. The F3 commit message
  records this ("the battery's dead REF name"); it is worth knowing that the bytes the plan
  freezes therefore cannot execute the clause-7 battery at all.
* I also make no judgement on which claim lands; that is L1's reconciliation.
