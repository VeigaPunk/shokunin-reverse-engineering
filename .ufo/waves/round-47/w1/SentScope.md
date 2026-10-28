# R47 w1 — SentScope: security & scope review of the two frozen counters

Seat `SentScope`, leaf member (no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`.
Measured at `a631bba01633d2b5353306a569be4ce2e683d364`; the lane then advanced **while this seat
ran** and every fact the advance could change was re-measured at tip
`b1a058f32c6908a6b92248052f151d0b0e2c76b1` (receipts `receipts/receipts-tip.jsonl`, counters
`SentScope/tip-c1-*.json`, `tip-c2.json`). The `--json-out` results were not re-run at the tip
because they cannot differ: the guard is `gate.out_path` in `tools/round-46/gate.py`
(`git diff a631bba HEAD -- tools/round-46/gate.py` is empty) called from a `main()` that the
tip's A6 does not touch (its diff is confined to `_fixture_files`). Both revisions are quoted
wherever they differ.

Scope is the assignment's: **can either counter write outside the lane?** — `--json-out` handling,
fixture-repo creation (toplevel assertion), scratch-root refusal, symlink handling in `gate.show`,
and whether a crafted `SCORECARD.md` or `SKILL.md` can make a counter execute something.
Nothing here "fixes" frozen bytes. `tools/round-47/` and `plans/round-47-claims.md` were read
only; every mutation happened in clones under `/fast/scratch/hyaku/kaidoku-r47/SentScope`.

Receipts: `SentScope/receipts/receipts.jsonl` (37 checks, each with exact argv, exit code,
stdout sha256, UTC), `SentScope/receipts/*.out` (raw stdout of each), and the five probe
drivers `probe1..probe5.py` + `capture.sh`. Counter receipts written by the counters
themselves: `SentScope/c1-a5.json`, `c1-declared.json`, `c1-prompt-freeze.json`, `c2.json`.

## Verdict table

| # | surface | verdict | receipt (exit) |
|---|---|---|---|
| 1 | counters are read-only on the lane tree | **PASS** | `lane_no_write_outside_ufo` (0), `lane_status_before` == `lane_status_after` sha `847843a590aa5851` |
| 2 | `--json-out` outside the lane root | **PASS** (4 forms refused, exit 2) | `jsonout_outside_lane`, `jsonout_traversal`, `jsonout_symlink_to_graded`, `jsonout_outside_lane` |
| 3 | `--json-out` onto a graded/frozen surface | **PASS** for paths, **FAIL** for hardlinks | `jsonout_graded_file` (2), `jsonout_graded_dir` (2) vs `jsonout_hardlink` (0, **SKILL.md overwritten**) |
| 4 | `--json-out` onto repo internals (`.git`, `.jj`) | **FAIL** — accepted | `jsonout_git_config` (0, repo bricked), `scratch_library` (`accept:.git/config`, `.git/hooks/pre-commit`, `.jj/repo/store/type` all `accepted: true`) |
| 5 | unwritable `--json-out` | **FAIL** — exit 1, receipt lost | `jsonout_missing_parent` (exit=1, `FileNotFoundError`) |
| 6 | fixture-repo creation asserts its toplevel | **PASS** (`exact.py`), **N/A/absent** (`record.py`) | `clone_toplevels` (0), `scratch_library` (`fixture_toplevel_symlinked_scratch.raised=true`) |
| 7 | scratch-root refusal (`/tmp`, `/var/tmp`, unset) | **PASS** (3/3, exit 2) | `scratch_no_env`, `scratch_tmp`, `scratch_var_tmp`, `scratch_library` |
| 8 | symlinks in `gate.show` cannot read out of tree | **PASS** | `symlink_blobs` (0) |
| 9 | crafted `SKILL.md`/`SCORECARD.md` cannot execute | **PASS** | `crafted_inputs_no_exec` (0), `argv_rev_help`, `argv_freeze_help`, `argv_record_output` |
| 10 | bytecode writes into the lane when `-B` is omitted | **FAIL (enforcement gap)** — invisible to the freeze gate | `pycache_clone_without_B` (0), `lane_pycache_preexisting` |
| 11 | freeze binding of the graded measurement | **FAIL for C2**, **stale for C1** | `record_freeze_calls`, `freeze_chain_tip`, `c1_declared_freeze_tip` (2) vs `c1_a6_freeze_tip` (0) |
| 12 | selftests runnable | **FAIL** as invoked bare, pass with dummy args | `exact_selftest_bare` (2), `record_selftest_bare` (2), `*_selftest_dummy` (0) |

Headline: **neither counter writes outside the lane root, and neither can be made to execute
code by artefact content.** What fails is narrower and more damaging to the claim: the
`--json-out` guard is path-based (hardlink and `.git`/`.jj` bypasses), one failure mode turns a
green measurement into exit 1, and — the two that matter for landing — **C2 has no freeze
binding at all** and **C1 is only green under an undisclosed third-to-fifth freeze amendment.**

## Findings

### F1 — HIGH — four undisclosed post-freeze amendments to a frozen counter
`plans/round-47-claims.md` discloses a series of **two** (A1 `9018c53`, A2 `62e33f7`, "the freeze
is a series of two, disclosed"). The chain is **six**, and it grew twice while this seat ran:

```
$ git -C <lane> log --format='%H %s' 62e33f7..b1a058f3 -- plans/round-47-claims.md tools/round-47/
f54b3b6d round-47: A6 - the battery fixture carries every citation the landed block names
07d2894e round-47: A5 - the ghost-atom forgery lands inside the corrections section
1e2c3102 round-47: A4 - the historical-correction selftest fixture gets its round-3 dispatch
2e4ae434 round-47: A3 - a seats/window correction for a round older than the window stays valid evidence
$ git -C <lane> diff --stat 62e33f7 HEAD -- plans/round-47-claims.md     # empty
```

The claims file is byte-identical to A2 at both revisions (`claims_unchanged_since_A2` and
`claims_unchanged_tip`, both stdout sha256 `e3b0c442…` = the empty string), so **A3–A6 have no
disclosure paragraph anywhere** — their only trace is the commit subject line. The consequence is
measured, not argued:

```
at a631bba
$ python3 -I -B tools/round-47/exact.py --root <lane> --freeze 62e33f7 --rev a631bba --json-out …
exit 2   reason=frozen_path_changed  frozen_path_changed=['tools/round-47/', 'tools/round-47/record.py']   (bdb58e730c76)
$ … --freeze 5017e1f --rev a631bba   →  exit 2, frozen_path_changed=['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/record.py']  (37c6258495)
$ … --freeze 07d2894e --rev a631bba  →  exit 0, failing=[], rule_blocks 24, refs 8, battery 4/4/0/1/0   (af195f2cb0)

at b1a058f3
$ … --freeze 62e33f7 --rev b1a058f3   →  exit 2, frozen_path_changed  (04d240e90c76)
$ … --freeze f54b3b6d --rev b1a058f3  →  exit 0, failing=[], battery 4/4/0/1/0  (a9b4756a4104)
```

**Impact.** R47-C1's target is reachable only under a freeze commit that the claims file does
not name, and the reachable one changes as the round proceeds (`07d2894e` → `f54b3b6d` within
this seat's run). A report citing `plans/round-47-claims.md@62e33f7` next to a green C1 is citing
an impossible measurement; citing the latest amendment cites a freeze nobody declared. This is
the round-46 M46-3 defect (undisclosed freeze series) recurring in a stricter form, and the
number in "a series of two" is now wrong by four.
**Smallest remediation.** The L1 states the freeze series' real length in the landing evidence
(A3–A6, with the reason for each) and cites the *last* amendment for the measured numbers — or
reverts A3–A6 and re-measures. Do not re-measure at `62e33f7` and call it green.

### F2 — HIGH — R47-C2 has no freeze binding: `record.py` never reads a freeze
```
$ grep -n 'freeze' tools/round-47/record.py
NO OCCURRENCE OF freeze IN record.py          (record_freeze_calls, sha 760fb5dcb4de6e31)
```
`record.py`'s CLI is `--root --rev --no-battery --selftest --json-out`; there is no `--freeze`,
no `gate.freeze_state` call, and the receipt has no `freeze`/`frozen_path_changed` key
(`c2.json` keys: `atoms atoms_by_class battery corrections corrections_bad counter exempted
failing …`). Yet it scored:

```
$ python3 -I -B tools/round-47/record.py --root <lane> --rev a631bba --json-out …
exit 0   met_target=true atoms=42 verified=41 exempted=1 corrections=2
         battery={correction_forgeries 3, forgeries_green 0}          (cedd96ed1c36be48)
$ python3 -I -B tools/round-47/record.py --root <lane> --rev b1a058f3 --json-out …
exit 0   atoms=44 corrections=2 battery={correction_forgeries 3, forgeries_green 0}, no freeze key   (3092e068b13f)
```

— at a rev where `record.py` itself had changed **three times after the declared freeze**. The
claims file's sentence "a change makes both counters exit 2 `frozen_path_changed`" is false for
this counter: the same rev makes `exact.py` exit 2 and `record.py` exit 0. The counter that
grades the lane's self-assessment is therefore not bound to the bytes that were frozen, and a
later edit to it is undetectable from its own receipt.
**Smallest remediation.** Add `--freeze` + `gate.freeze_state` to `record.py` and re-freeze
(disclosed), or — cheaper and sufficient — pin `sha256(tools/round-47/record.py)` inside the C2
receipt and quote that pin in the landing evidence next to the measured revision.

### F3 — MEDIUM — `--json-out` accepts repo internals (`.git/`, `.jj/`)
`gate.out_path` (gate.py:200-213) checks lane containment and a `GRADED` top-level denylist
(`SKILL.md LOG.md SCORECARD.md PROVINCE.md SHONEN.md plans tools corpus evidence`). `.git` and
`.jj` are neither, so they pass:

```
$ python3 -I -B tools/round-47/exact.py --root <clone> --freeze 07d2894e --rev a631bba \
      --no-battery --json-out <clone>/.git/config
exit 0                                        # receipt written into .git/config
$ git -C <clone> status --porcelain
fatal: bad config line 1 in file .git/config   (jsonout_git_config, sha 92dee49c2b62fd4a)
```
Read-only acceptance probe on the **real lane root** (`scratch_library`, sha 7b9d5232a7e9b8c7):
`accept:.git/config accepted:true`, `accept:.git/hooks/pre-commit accepted:true`,
`accept:.jj/repo/store/type accepted:true`. Nothing was written there.

**Exploit path.** The claims file's C1/C2 counting commands carry `--json-out <OUT>`, a
placeholder the L1 fills in. Any script or seat that fills it with a repo-internal path
(`.git/config`, `.git/hooks/*`, `.jj/repo/store/*`) writes receipt JSON into the repo's own
metadata; the measured effect is a lane repo that no longer runs git at all. A pre-existing
executable hook would also be replaced by JSON (mode preserved, content destroyed).
**Impact.** Lane-repo integrity/DoS, no artefact control needed — argv is operator-supplied.
**Smallest remediation.** One denylist addition: refuse when `rel.split("/")[0]` starts with `.`
and is not `.ufo` (covers `.git`, `.jj`, `.hg`); or add `.git`, `.jj` to `GRADED`.

### F4 — MEDIUM — `--json-out` hardlink defeats the graded-surface guard, no race needed
`os.path.realpath` (gate.py:205) does not resolve hardlinks, so a hardlink inside an accepted
directory resolves to itself and is written — into the inode of a graded file:

```
$ ln <clone>/SKILL.md <clone>/.ufo/SKILL-mirror.json          # inode shared with SKILL.md
$ python3 -I -B tools/round-47/exact.py --root <clone> --freeze 07d2894e --rev a631bba \
      --no-battery --json-out <clone>/.ufo/SKILL-mirror.json
exit 0
before=894e2864e5de8232  after=77939a4b8e094219  first line of SKILL.md = "{"
$ git -C <clone> status --porcelain -- SKILL.md
 M SKILL.md                                    (jsonout_hardlink, sha 775f3ab7ff43a6c5)
```
**Exploit path.** A seat that can write anywhere under `.ufo/waves/` (every seat can) plants
`.ufo/waves/round-47/l1/scores/<name>.json` as a hardlink to `SCORECARD.md` or `SKILL.md`; the
L1 then runs the documented command with that path as `<OUT>` and destroys the artefact it is
about to land. The same guard also has a check-then-use window (realpath at t0, `open` at t1
after the battery — seconds long): [INFERENCE] a symlink swapped in during that window is
followed, because `gate.emit` uses plain `open(path, "w")`.
**Impact.** A graded/frozen surface can be overwritten through a path the guard accepts.
**Smallest remediation.** After resolving, `os.stat` the target and refuse if `st_nlink > 1`
or if `(st_dev, st_ino)` equals any graded file's; open with `O_CREAT|O_EXCL|O_NOFOLLOW` via a
dirfd of the resolved parent.

### F5 — MEDIUM-LOW — an unwritable `--json-out` reports exit **1**, and loses the receipt
`gate.emit` is called **outside** `gate.main_guard` in both `main()`s (exact.py:436-437,
record.py:484-485), so an `OSError` escapes as a traceback and Python's exit 1 — which the
contract reads as "not met / violation":

```
$ python3 -I -B tools/round-47/exact.py --root <clone> --freeze 07d2894e --rev a631bba \
      --no-battery --json-out <clone>/.ufo/nodir/x.json
FileNotFoundError: [Errno 2] No such file or directory: '…/.ufo/nodir/x.json'
exit=1                                          (jsonout_missing_parent, sha cb08936260e0e233)
```
**Impact.** A green counter, correctly measured, is recorded as a red *and* leaves no receipt —
the exact failure mode the exit-code contract exists to prevent (a 2 must never be mistaken for
a verdict; here a could-not-write is mistaken for a violation).
**Smallest remediation.** Wrap `gate.emit` in `gate.main_guard` and return 2 with
`reason: json_out_unwritable`.

### F6 — LOW (enforcement gap) — bytecode writes into the lane, and the freeze gate cannot see them
```
$ python3 <clone>/tools/round-47/exact.py --root <clone> --freeze 07d2894e --rev a631bba …   # no -B
exit 0 ; pycache: gate.cpython-314.pyc ; git status (frozen paths): []
                                                (pycache_clone_without_B, sha f1fd77e8134deb5f)
$ stat -c '%y %n' <lane>/tools/round-47/__pycache__/*.pyc
2026-10-28 14:58:32 …/exact.cpython-314.pyc
2026-10-28 14:56:24 …/record.cpython-314.pyc    (lane_pycache_preexisting, sha 5c794650bc8550ef)
```
`-I` does **not** imply `-B` (`sys.flags.dont_write_bytecode == 0` under `-I`). The documented
counting command uses `-I -B`, so the specified invocation is clean — but the gate's
`dirty()` delegates to `git status`, and `__pycache__/` is in `.gitignore` (`.gitignore:1`), so a
`-B`-less run mutates the worktree of a frozen directory (`tools/round-47/__pycache__` already
exists in the lane, mtime 14:56/14:58, i.e. **before this seat's first command**) and the freeze
verdict still says clean.
**Impact.** "Nothing in `tools/round-47/` changes after the freeze" holds for committed bytes
only; worktree mutation of the frozen directory is not detected. No effect on the graded
measurement (bytecode cannot shadow a newer source; mtime/size invalidation applies).
**Smallest remediation.** None required for correctness; the landing evidence should state that
receipts are produced with `-B`, and a post-freeze `__pycache__` mtime under `tools/round-47/`
is a procedural smell to disclose, not a `frozen_path_changed`.

### F7 — LOW — a frozen clause of R47-C2 is unreachable (vacuous)
`CORR` admits only `seats|window|path|rev`:
```
$ python3 -B probe2.py   →  CORR_alternation "^- corrects (seats|window|path|rev) (\\S+):\\s*(.+)$"
   CORR_regex_matches_axes_line: false      axes_correction_parsed: false
   corrections_parsed_classes: ["seats"]                     (symlink_blobs, sha c9c2ea840d02940e)
```
So the claims file's clause-3 obligation "an `axes` correction must state `<resolved>/<total>`"
can never fire; `CORR_AXES` and the `axes` branch of `corrects()` are dead code, and a second,
unreachable `axes`/`rev` block in `corrects()` (record.py:299-306) dereferences an undefined
`atom` — a `NameError` waiting behind a condition that cannot occur.
**Impact.** An axes atom can never be exempted, only corrected in place; the clause is
unfalsifiable as written. Direction is safe (fail-closed) but the instrument is smaller than its
claim.
**Smallest remediation.** Disclose it, or re-freeze with `axes` added to the alternation and the
dead block deleted.

### F8 — LOW-MEDIUM — a crafted `SCORECARD.md` can assert an "empty" window over a pathspec of its own choosing
`derive()` takes the pathspec from the sentence after `--` and asks git whether *that* log is
empty (`window_empty`). A pathspec that nothing touched makes the claim trivially true:
```
$ python3 -B probe5.py
 bogus_pathspec_window : {"ok": true, "detail": {"empty": true, "pathspec": ["tools/round-47/does-not-exist/"]}}
 prose_pathspec_window : {"ok": true, "detail": {"empty": true, "pathspec": ["prose","words","here"]}}
 real_window           : {"ok": false, "detail": {"empty": false, "pathspec": ["tools/round-47/"]}}
                                                (window_vacuity, sha 922a8c935d8d6890)
```
Note the second row: an English prose tail is silently split into a pathspec, so an atom whose
sentence reads "… is empty at every measurement above" verifies against words, not paths.
**Impact.** One of C2's five atom classes accepts a claim that binds no evidence — the same
shape as the round-46 window defect (R46-V2) that this counter exists to catch.
**Smallest remediation.** Require the pathspec to exist at `--rev` (`git ls-tree` non-empty) or
to be one of the frozen paths; reject multi-token prose.

### F9 — LOW — A3 contradicts the frozen claims text about ghost corrections
The claims file says: "A correction that exempts an atom the card does not contain is itself a
defect." A3 (`2e4ae434`) carves out `seats`/`window` corrections whose key is a round older than
the last two sections, and such lines still count toward `corrections >= 2`:
```
$ python3 -B probe2.py  →  historical_corrections_counted: 2   historical_keys: ["3","2"]
```
**Impact.** `corrections >= 2` — one of C2's two landing requirements — is satisfiable by two
truthful-but-irrelevant corrections that exempt nothing in the graded window. Not a false green
on its own (mismatches must still be 0), but the "at least two re-derived corrections" wording
overstates what the counter enforces.
**Smallest remediation.** Disclose A3 in the landing evidence and state the narrowing in the
correction rows; do not read `corrections == 2` as "two record defects were repaired".

### F11 — PASS (with an implicit bound) — A6 gives the fixture an artefact-derived write path
A6 (`f54b3b6d`) makes `_fixture_files` add a fixture file for **every** `HARD_REF` name in the
landed block, and `_repo` writes each key with `open(os.path.join(d, p), "w")` — so artefact
content now chooses paths inside a repo the counter commits to. The only thing standing between
a crafted block and a write outside that fixture is `gate.show` returning `None` for a name git
cannot resolve. Attacked with a block citing
`tools/round-47/../../../../../../<scratch>/PWNED-outside.md:1-2`:
```
$ python3 -B probe_a6.py
 show_escape_path : null                     # git refuses `..`; the name is never added to `out`
 check_refs       : "…PWNED-outside.md: absent at rev"
 PWNED_outside_exists: false                 (a6_write_escape_probe, sha 2ee995655cc4)
```
`HARD_REF` admits `..` but cannot produce a leading `/`; git refuses `..` and absolute paths, so
the write set stays inside the fixture. No symlink can be planted either: `_repo` only ever
creates regular files. **Bound to state in the landing evidence:** A6's safety rests on a
property of `git show`, not on a check in `exact.py` — `_fixture_files` re-uses the names without
re-applying the `ALLOW` filter or a `..` test. It is reachable only from a green block (clause 8
already rejected every unvalidated name), so the direction is fail-closed today.

### F10 — LOW — `--selftest` is unreachable as a bare flag
`argparse` marks `--root`/`--rev` (and `--freeze` for `exact.py`) `required=True`, and
`selftest()` is only reached after `parse_args`:
```
$ python3 -I -B tools/round-47/exact.py --selftest            → exit 2 (argparse: --root, --freeze, --rev required)
$ python3 -I -B tools/round-47/record.py --selftest           → exit 2 (argparse: --root, --rev required)
$ … --root /nonexistent --freeze deadbeef --rev deadbeef --selftest  → exit 0, failures 0
$ … --root /nonexistent --rev deadbeef --selftest             → exit 0, RECORD_SELFTEST cases=10 failures=0
```
(exact_selftest_bare / record_selftest_bare exit 2; *_selftest_dummy exit 0, shas
`0249b80f5808` / `7c9a437c2b69`.) Both selftests themselves pass: `exact` 0 failures,
`record` 10/10 including `green-historical-correction` (A3's fixture).
**Impact.** The instrument's own smoke test reads as "could not evaluate" when invoked the
obvious way, and its pass cannot be cited without inventing dummy arguments.
**Smallest remediation.** Parse `--selftest` before the required-argument check (a subparser or
`parse_known_args`), or document the dummy invocation in the landing evidence.

## PASS evidence (the surface the assignment asked about)

**1. Read-only on the lane.** Both counters were run against the real lane root, with the
battery, and the lane's status is byte-identical before and after (`lane_status_before` and
`lane_status_after` both sha256 `847843a590aa5851`). The stricter check
`git status --porcelain --untracked-files=all -- SKILL.md SCORECARD.md LOG.md PROVINCE.md
SHONEN.md plans tools corpus evidence` prints `CLEAN` (`lane_no_write_outside_ufo`, sha
`0b98843240a0b1a2`). Every file read in either counter is `git show <rev>:<path>`
(gate.py:29-31), i.e. the object database — no counter reads the worktree, which is why artefact
content cannot redirect a read.

**2. `--json-out` containment.** Refused with exit 2: an absolute path outside the root
(`jsonout_outside_lane`), a `..` traversal (`jsonout_traversal`), a graded file, a graded
directory, and — because `realpath` runs first — a **symlink inside the lane pointing at
`SKILL.md`** (`jsonout_symlink_to_graded`; `realpath` → `…/SKILL.md`, refused with
`--json-out inside a graded or frozen surface: SKILL.md`). Rows 3–4 of the verdict table are the
two ways past this guard (F3, F4).

**3. Fixture-repo creation.** `exact._repo` (exact.py:301-320) writes a fixture-local
`user.email`/`user.name` **before** the first commit and asserts the toplevel:
```
top = git -C d rev-parse --show-toplevel ; if top != d: raise RuntimeError("fixture toplevel mismatch")
```
The assertion is live, not decorative: pointed at a *symlinked* scratch root, `mkdtemp` returns
`<link>/fx-…` while git reports the resolved path, and the run fails closed —
`fixture_toplevel_symlinked_scratch: {"raised": true, "error": "fixture toplevel mismatch"}`
(`scratch_library`, sha `7b9d5232a7e9b8c7`); the plain case is `{"raised": false,
"toplevel_ok": true}`. All five harness clones were asserted independently (`clone_toplevels`,
sha `fb93b32e5979b164`). `record.py` creates **no** fixture repo on the counting path (its battery
mutates card text in memory); its `selftest()` fixture (record.py:518-522) does **not** assert
its toplevel — the only asymmetry, and it is off the counting path.

**4. Scratch-root refusal.** Library and CLI agree, exit 2 with the reason:
`no HYAKU_SCRATCH/TMPDIR root set`; `scratch root is a temporary partition: /tmp`;
`… : /tmp/x`; `… : /var/tmp` (`scratch_no_env`, `scratch_tmp`, `scratch_var_tmp`,
`scratch_library`). `realpath` runs before the `/tmp` test, so a symlinked scratch root pointing
into `/tmp` is refused too. Fixtures are `rmtree`d in `finally`; no `shutil.rmtree` in either
counter can reach a non-scratch path (exact.py:372,401,495,549,556; record.py:594,598 — all
`mkdtemp`/`gate.scratch` values).

**5. Symlinks in `gate.show`.** A committed symlink is graded as its **target string**, never as
the target's bytes: `abs.md → "/fast/…/secret.txt"` (52 bytes, sha `e97bca9361356191`) while the
secret itself hashes `17a0f5fb52bf36f5`; `rel.md → "../../../etc/passwd"` (19 bytes,
`56bfa7338a2dfd1d`) while `/etc/passwd` line 1 hashes `13e2783884783ef4`. A symlinked directory
is not traversable (`outdir/secret.txt` → `returned: false`). Traversal in a *cited* path is
rejected by git itself: `git show rev:tools/round-47/../../SCORECARD.md` → `None`
(`show:` rows in `receipts/jsonout_symlink_to_graded.out` from `probe1.py`, and again in
`symlink_blobs.out` from `probe2.py`), so the `..`-bearing token that `HARD_REF` accepts cannot escape
the ALLOW set — it fails closed as `absent at rev`. Directory citations are rejected by the
trailing-slash rule (`corpus/knowledge:1-3` → "outside the validated path set"), so the tree
listing `gate.show` returns for a directory is not reachable as a citation.

**6. No execution from artefact content.** No `shell=True`, `os.system`, `eval`, `exec`,
`pickle` or `__import__` in `exact.py`, `record.py` or `gate.py`; every `subprocess.run` is an
argv list. Revision and window tokens are hex-constrained (`[0-9a-f]{7,40}`), so an
option-shaped ref cannot reach argv, and `gate.resolve` rejects one anyway:
`--rev=--help` → exit 2 `unknown rev revision`; `--freeze=--help` → exit 2;
`record.py --rev=--output=x` → exit 2 (`argv_*` receipts). A card and a `SKILL.md` stuffed with
`$(touch …)` in rev tokens, path atoms, window tails, correction keys and `Refs:` lines produced
`pwned_files: []`, `exact_refs: 1` (only the legitimate citation matched) and exit 1 with
substantive failures (`crafted_inputs_no_exec`, sha `30f5b23f7e581171`). Card-derived pathspecs
reach git only after `--`; card-derived correction keys reach `git rev-parse --verify --quiet`
and an option-shaped key returns rc 1 (`corrects_rev_help: [false, {"resolves": false}]`).

## Not run / not claimed
- Both counters were re-measured at the tip that existed when this seat finished
  (`b1a058f3`): C1 exit 0 only under the A6 freeze (`f54b3b6d`), C2 exit 0 with no freeze key.
  No measurement was taken at a *later* landing revision — the lane was still moving, so treat
  every number here as `@b1a058f3` and re-run the two counting commands after the landing.
  `SKILL.md` block 24 is already present at both revisions (`rule_blocks 24`,
  `marker_occurrences 1`, `refs 8`).
- No semantic attack on C1's clauses 2–7 or C2's clause 6 batteries: other seats own that; this
  seat attacked only the scope/security surface named in the assignment. F7–F9 are reported
  because they are reachable *through* crafted `SCORECARD.md` content, not as a full
  falsification pass.
- The concurrent TOCTOU variant of F4 is `[INFERENCE]`: the check-then-use gap is visible in the
  source (realpath at `gate.out_path`, `open` at `gate.emit`) but was not raced.
- No tool installs, no package manager transactions, no commits/stages; nothing was written
  outside `.ufo/waves/round-47/w1/SentScope{,.md}` and `/fast/scratch/hyaku/kaidoku-r47/SentScope{,2}`
  (both scratch roots removed after the receipts were copied here).
- Receipt inventory: `receipts/receipts.jsonl` (37 checks at `a631bba`),
  `receipts/receipts-tip.jsonl` (7 checks at `b1a058f3`), 54 files in `receipts/` including the
  raw stdout of every check and the six probe drivers.
