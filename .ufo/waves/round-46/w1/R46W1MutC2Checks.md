# R46W1MutC2Checks — mutants of `tools/round-46/registry.py`

Seat: `R46W1MutC2Checks` (mutation-tester), round 46 wave 1. Read-only on the lane; every
mutation was applied to a **copy** in `S=/fast/scratch/hyaku/kaidoku-r46/R46W1MutC2Checks`,
which is removed. Receipts live beside this file.

- Freeze under test: `31820472784284727546808acc31b3ea1e73919b`
  (`git log --format=%H -1 -- plans/round-46-claims.md` → same).
- Measured revision: `1e32827bd05328ee3b1e439d116008f40f078049` (`main`/HEAD at seat time).
- Two byte bases were mutated, because they are not the same file:
  - **head** — the landed working tree = HEAD: `tools/round-46/registry.py`
    sha256 `5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73`,
    git blob `26f9e9c6a92d`; `gate.py` sha256
    `847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223` (blob `9ab7e2a3962e`).
  - **frozen** — the bytes actually at the freeze commit
    (`git show 3182047:tools/round-46/registry.py`): sha256
    `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449`, blob `6581c1b2acb8`;
    `gate.py` sha256 `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e`
    (blob `d7cd9aace310`).
- Toolchain: `Python 3.14.8`, `git 2.56.0`. **No installs**, stdlib only, nothing under
  `/tmp`. Originals were never written: `git status --porcelain -- tools/round-46
  plans/round-46-claims.md SKILL.md` is empty and the working-tree shas above equal the HEAD
  blobs.

## 1. Baseline — the detector of record

```sh
cd $S/pristine
python3 -I -B registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 31820472784284727546808acc31b3ea1e73919b \
  --rev    1e32827bd05328ee3b1e439d116008f40f078049 --selftest
```

- exit **0**, stdout `REGISTRY_SELFTEST: cases=12 failures=0`,
  stdout sha256 `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e`, 2026-10-28T17:02:29Z.
- The **frozen** base prints the **same 12-case stdout, same sha256** (exit 0, 17:04Z): the
  F3/F4 commits changed the v1 profile and the battery gating, not the selftest's verdicts.

**B1 (calibration defect in the claims file, not the instrument).** `plans/round-46-claims.md`
§ Satisfiability preflight says "`registry.py --selftest` prints `cases=11 failures=0`". Two
exact contradictions, both measured:

| command | exit | stdout |
|---|---|---|
| `registry.py --selftest` (as the claims file words it) | **2** | empty (`--root/--freeze/--rev` are argparse-`required=True`) |
| `registry.py --root . --freeze F --rev R --selftest` | **0** | `cases=12 failures=0` |

Both byte bases print `cases=12`. The landed `SKILL.md` registry row for `gate.py` already
says `cases=12 failures=0`, so the artefact and the claims file disagree; the claims file is
the one that is wrong. L1 should reconcile the preflight sentence (it is frozen, so the
reconciliation is a record entry, not an edit).

## 2. Mutants — one defect each, run against the same detector

Command per mutant (cwd = the mutant dir, which holds the module's own `gate.py`), modelled
on `driver.py` (in this directory):

```sh
python3 -I -B registry.py --root <lane> --freeze <F> --rev <H> --selftest
```

`KILLED` = the selftest turned a case red (`failures>0`, exit 1). `SURVIVED` = the selftest
still printed `failures=0` (exit 0) with the defect installed.

| # | defect (clause attacked) | mutant sha256 | exit | selftest | verdict | red case / note |
|---|---|---|---|---|---|---|
| m1 | cell 0 matched by `PATHCELL.search` instead of exact backtick equality (clause 3, `R45-CL14 b`) | `4c7e05781678…` | 1 | failures=1 | **KILLED** | `red-substring-cell` |
| m2 | `rows_in_section` made fence- and comment-blind (clause 1, `R45-CL14 a/c`) | `472ccc9f9eb1…` | 0 | failures=0 | **SURVIVED** | diagnostics only, see §3 |
| m3 | house-schema header equality dropped (clause 2, `R45-CL14 d`) | `bcae55edf398…` | 1 | failures=1 | **KILLED** | `red-header-not-house` |
| m4 | `absent_at_rev` arm dropped (clause 5, `R45-CL2`) | `92331cf2a872…` | 1 | failures=1 | **KILLED** | `red-absent-at-rev` |
| m5 | `EXITMAP` reverted to `\b([012])\b` (clause 4, `R45-CL14 d`) | `9d916759748c…` | 1 | failures=1 | **KILLED** | `red-prose-exit` |
| m6 | section bounds dropped: `rows_in_section(skill)` not `(mid)` (clause 1) | `40e2e40deb5f…` | 0 | failures=0 | **SURVIVED** | diagnostics only, see §3 |
| m7 | `close marker precedes open marker` guard removed (clause 1) | `82ead9968ed4…` | 0 | failures=0 | **SURVIVED** | equivalent on exit, see §3 |
| m8 | `by_path.setdefault` → last-wins (duplicate cell 0) | `fb111c7d0001…` | 0 | failures=0 | **SURVIVED** | verdict-divergent, no forgery gain |
| m9 | battery requirement changed `v2_green 0` → `v2_green 7` | `5deab4d01d94…` | 0 | failures=0 | **SURVIVED** | caught by a live battery run, see §3 |
| m9b | battery acceptance loop emptied (`for key, want in ()`) (clause 6) | `2c569e1137b4…` | 0 | failures=0 | **SURVIVED** | real gap, see §3 |
| m10 | marker uniqueness relaxed `!= 1` → `< 1` (clause 1) | `e6dcc8f9a350…` | 0 | failures=0 | **SURVIVED** | real gap, see §3 |
| m11 | `load_scope` accepts an empty path list (clause 3 scope) | `0b1f6645c5d1…` | 0 | failures=0 | **SURVIVED** | real gap, see §3 |
| m12 | `if flat == 2:` (frozen-touch verdict) dropped (clause 7) | `6a96f1c44626…` | 0 | failures=0 | **SURVIVED** | real gap, see §3 |

Per-mutant exit, stdout sha256 and UTC stamps: `mutants-head.json` / `mutants-frozen.json`.

Result on both bases: **4 killed, 9 survived** (12 mutants apply to the frozen bytes too; m4's
head anchor `if hard and spec["presence"]:` does not exist at the freeze, so it was re-cut
there as `if spec["presence"]:` → mutant sha256 `0fba60311a7c…`, exit **1**, `red-absent-at-rev`
turned red, i.e. **KILLED**). For **m7, m8, m9, m9b, m10, m11, m12 the selftest stdout is
byte-identical to the pristine baseline** (`0fa8c31a6419…`): the detector is blind to them.

## 3. Survivor triage — real gap, equivalent, or direction

Each survivor was then handed a *targeted* detector (probes `P1–P11` in `probes.json`, and
end-to-end `evaluate()` runs on real one- and two-commit git fixtures `F1–F4` in
`fixtures.json`; harnesses `probe.py`, `fixture.py` here). Probes score the same artefact with
`registry.score()` on pristine and mutant bytes in-process; fixtures commit the forgery and run
the counter's own `evaluate()`.

### 3.1 m2 (fence-blind) — real gap, case confounded
`red-fenced` and `red-html-comment` do turn red under m2's **diagnostics** but not their
verdict, because those fixtures put **only data rows inside the fence** — no header row — so
the *header* clause (`header != house schema (7 cells)`) is what rejects them, whether or not
fences are honoured. Measured `failing` for `red-fenced`:

- pristine: `['header != house schema (7 cells)', 'unregistered: 2 of 2']`
- m2:       `['header != house schema (7 cells)', 'unregistered: 1 of 2']`

Verdict unchanged (`ok` true in both) → the case passes for the wrong reason. A fenced table
that **carries its own house header** is accepted by m2 and rejected by pristine:

| detector | pristine | m2 |
|---|---|---|
| `P1-fence-with-house-header` (`score`) | exit **1** | exit **0** |
| `F1-fenced-table-with-house-header` (`evaluate`, committed fixture) | exit **1** | exit **0** |

So the instrument's fence rule is load-bearing and the selftest does not test it.

### 3.2 m6 (rows outside the section) — real gap, case confounded
Same shape: `red-outside-section` puts the table **before** the markers and leaves the section
empty, so pristine's `header` is `None` → `header != house schema`. m6 keeps that clause
failing (`unregistered: 1 of 2` instead of `2 of 2`) → verdict unchanged. A **complete table**
(header + rows) outside the section is accepted by m6 and rejected by pristine:

| detector | pristine | m6 |
|---|---|---|
| `P2-table-entirely-outside-section` | exit **1** | exit **0** |
| `F2-table-outside-section` (committed) | exit **1** | exit **0** |

### 3.3 m10 (two open markers) — real gap, no case at all
Marker uniqueness is asserted by clause 1 ("exactly one …") but no selftest fixture has a
duplicate marker (`red-no-markers` covers the *zero* side). `P3-two-open-markers`: pristine
**1** (`markers: 2 open, 1 close`), m10 **0** — the second section registers.

### 3.4 m11 (empty census) — real gap, no case at all
`load_scope` refuses an empty list, which is what keeps a census that names nothing from
scoring `unregistered == []` trivially. `P4-census-names-nothing`: pristine exit **2**
(`scope lists no path`), m11 exit **0**. A scope of nothing is silently a pass under m11.
The selftest always passes a two-or-three-path scope.

### 3.5 m9b (battery acceptance neutered) — real gap, zero battery coverage in the selftest
Every selftest case calls `evaluate(..., with_battery=False)`, so `run_battery` and the
`battery` acceptance loop (`forgeries_total 7 / v1_green 7 / v2_green 0 / genuine_green 1`)
are **never executed by `--selftest`**. `P7-battery-accepted-all-forgeries` passes a battery
that accepted all seven forgeries (`v2_green 7`) straight to `score()`: pristine exit **1**
(`battery v2_green 7 != 0`), m9b exit **0**. Clause 6 has no selftest case at all.

### 3.6 m12 (frozen-touch verdict ignored) — real gap, zero negative freeze cases
Every selftest fixture is built with `freeze == rev`, so the `flat == 2` branch is only ever
exercised on the clean path. With m12, a `FREEZE..REV` range that **touches a frozen path** is
scored instead of refused: `F3-frozen-dir-touched` (freeze `A`, rev `B` modifying
`tools/round-46/a.py`) → pristine exit **2** (`frozen_path_changed`, `restored
['tools/round-46/a.py']`), m12 exit **0**. This is the highest-severity survivor: the
instrument's admissibility gate becomes a scored `met`.

`F4-frozen-dir-touched-then-restored` confirms the claims' rule on the same harness: pristine
exit **2** with `restored ['tools/round-46/a.py']` (a later restore does not un-block).

### 3.7 m7 (close-before-open guard) — equivalent on the graded predicate
`P8-close-marker-before-open` returns **1 on both** pristine and m7. Dropping the guard only
removes the `close marker precedes open marker` *diagnostic*:

- pristine `failing`: `['close marker precedes open marker', 'header != house schema (7 cells)', 'unregistered: 2 of 2']`
- m7 `failing`:       `['header != house schema (7 cells)', 'unregistered: 2 of 2']`

`met_target` and exit are unchanged, so this survivor is an equivalent mutant on the graded
surface — a diagnostic-fidelity gap, not a discrimination hole. It does mean the clause-1
error message is not pinned by any case.

### 3.8 m8 (last-wins shadowing) — divergent, but no forgery advantage
Duplicate cell-0 rows for one path: first-wins vs last-wins *does* change the exit, symmetrically:

| detector | pristine | m8 |
|---|---|---|
| `P5` thin row first, good row last | **1** | **0** |
| `P6` good row first, thin row last | **0** | **1** |

Neither direction is a forgery vector: with either policy, one good row anywhere for the path
is enough to register it, and the fence rule (not ordering) is what defeats the
`first-wins-shadow` forgery. The predicate text is silent on duplicates and no selftest case
pins the policy, so this is a spec/coverage gap of low severity, worth one case if a re-cut
happens.

### 3.9 m9 (stricter requirement) — caught by a live battery run, not the selftest
m9 makes the counter demand `v2_green == 7`; a live battery run over the landed artefact
therefore fails: `score(..., battery=<real battery>)` → pristine exit **0**, m9 exit **1**
(`battery v2_green 0 != 7`). Its survival is a statement about `--selftest`'s scope (3.5), not
about the live counter.

## 4. Clause coverage of the 12 selftest cases

| C2 clause | selftest case(s) | verdict |
|---|---|---|
| 1 marker count (`== 1`) | `red-no-markers` (zero side only) | **half** — duplicates untested (m10) |
| 1 fence / HTML comment | `red-fenced`, `red-html-comment` | **confounded** — header clause rejects (m2) |
| 1 section bound | `red-outside-section` | **confounded** — empty section, header clause rejects (m6) |
| 1 close-before-open | none | untested (m7, diagnostic only) |
| 2 house header exact | `red-header-not-house`, `green` | covered (m3 killed) |
| 3 cell 0 exact equality | `red-substring-cell` | covered (m1 killed) |
| 4 verdict map binds 0/1/2 | `red-thin-exit`, `red-prose-exit` | covered (m5 killed) |
| 5 `absent_at_rev` | `red-absent-at-rev` | covered (m4 killed) |
| 3 scope completeness | `red-unregistered`, `green` | covered |
| 6 battery (7/7/0/1) | **none** — `with_battery=False` everywhere | **uncovered** (m9b) |
| 7 frozen-touch exit 2 | **none** — every fixture has `freeze == rev` | **uncovered** (m12) |
| v1 fidelity (positive) | `red-v1-accepts-fenced` (expects 0) | covered on the landed bytes |

Counting command for the map: `python3 -I -B registry.py … --selftest` (baseline above);
`red-v1-accepts-fenced` is the only case whose expectation is `0` besides `green`.

## 5. Frozen-instrument findings (for L1 — reported, not fixed)

The freeze is the rule for both counters, and this seat ran the C2 counter as both byte bases.

### F1 — the declared freeze does not contain the bytes it freezes; every rev ≥ freeze is exit 2
`git log --format=%H -1 -- plans/round-46-claims.md` = `3182047…` (the claims file is never
touched again), but `tools/round-46/` **is**: three commits inside `FREEZE..REV` modify it —

```
50862e4a  M tools/round-46/attest.py  M tools/round-46/gate.py  M tools/round-46/registry.py
65678df0  M tools/round-46/attest.py
04252247  M tools/round-46/registry.py
```

blob compare at the two revisions: `attest.py` `25883520`→`936910fe`, `gate.py`
`d7cd9aac`→`9ab7e2a3`, `registry.py` `6581c1b2`→`26f9e9c6` (all differ; `census.py`/`census.json`
identical). The counting command from the claims file, run on the landed bytes:

```sh
python3 -I -B tools/round-46/registry.py --root <lane> --freeze 3182047… --rev 1e32827… \
  --json-out .ufo/waves/round-46/w1/R46W1MutC2Checks/live-pristine.json
```

→ exit **2**, `reason frozen_path_changed`,
`frozen_path_changed ['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']`,
`touched` 3 paths, `restored` the same 3, `met_target` **absent**, stdout sha256
`66408e857fb1b5f56003bb73523539aa8b2a1a739df10a37c2eeb8541482b0da`, 2026-10-28T17:03:47Z.

Consequence, and it is structural: `touched` is non-empty for **every** rev that contains
those three commits, so **no rev at or after the freeze can produce a C2 score**, and rev ==
freeze has no v2 artefact (`markers: 0 open, 0 close`, `unregistered: 38 of 38`, exit 1,
sha256 `8841358751b18788f45ee394827140d59235a7251f51cae8e7cc1bad697c074c`). The claim is
unscorable as frozen, by the frozen instrument's own rule. Re-freezing at `04252247` is the
only way to admit a later rev, and that rev does not re-derive from the claims file's own
sentence ("the commit that first contains this file").

### F2 — the freeze-tree CLI crashes; the same command at the landed bytes works
Frozen bytes, non-selftest path (any clean freeze range), e.g. `--freeze F --rev F`:

```
stdout: {"reason": "unhandled AttributeError: 'NoneType' object has no attribute 'splitlines'"}
stderr: TypeError: cannot unpack non-iterable int object   (registry.py line 432, main)
exit:   1                                                  sha256 528c1d21d81389fa…
```

The frozen `gate.main_guard` returns the **int** `2` and prints the reason itself; the frozen
`registry.main` unpacks `code, receipt = gate.main_guard(...)`. The landed `gate.main_guard`
returns `2, {"reason": …}`, so the landed pair runs. So at the declared freeze the C2 counting
command cannot produce a receipt at all — and it fails as **exit 1** with a traceback, which
is a *verdict* under the round's exit contract (and exactly the `R45-CL13 (f)` defect class the
round claims to have removed). `--selftest` bypasses `main_guard`, which is why the selftest is
green on bytes whose CLI is broken.

### F3 — the freeze-tree `v1` profile is not the round-45 port, so clause 6 is false at the freeze
At the freeze the three v1 arms read `spec["strict_cell"] / ["strict_exit"] / ["presence"]`
without `and hard`, i.e. v1 uses the v2 checks. Measured on the **landed** section with each
base's own `run_battery` (`battery-bases.json`):

| base | forgeries_total | v1_green | v2_green | genuine_green |
|---|---|---|---|---|
| head (landed) | 7 | **7** | 0 | 1 |
| frozen | 7 | **0** | 0 | 1 |

Per-fixture at the freeze, every class scores `v1=1` (rejected) — e.g. `prose-exit`
`['thin verdict-map cells: 1']`. Cross-base probes agree: `P9-v1-substring-cell` and
`P10-v1-registered-path-absent` and `P11-v1-fenced-single-letter` are exit **0** (accepted) on
head and exit **1** on frozen. So `battery.v1_green == 7` (clause 6) is **unsatisfiable at the
declared freeze**, while the landed bytes satisfy it.

### F4 — the landed artefact itself is clean (landing evidence the L1 can use)
`score()` at `--rev 1e32827…` with the landed bytes (structural, then with the real battery):

- structural: exit **0**, `registry_rows 38`, `scope_size 38`, `unregistered []`, `thin []`,
  `absent_at_rev []`, header == house; the census's 38 paths are each an exact first cell.
- with battery `forgeries_total 7 / v1_green 7 / v2_green 0 / genuine_green 1`: exit **0**,
  `failing []`.

So the only things between R46-C2 and a score are F1 (freeze identity) and, at the declared
freeze bytes, F2/F3.

### F5 — `--selftest` ignores `--root/--freeze/--rev`
`selftest()` builds its own fixture repos under `gate.scratch(...)`; the three arguments are
only argparse-`required=True` (which is why the bare command exits 2). The documented
self-test command's arguments are decoration — no fixture uses the caller's lane.

## 6. Kill rules this selftest lacks (for a re-cut; nothing was applied — the file is frozen)

Six fixtures, each in the same `mk()` shape already used, each turning exactly one survivor:

1. `red-fenced-header` — fenced table **with** its own house header row → expect 1 (kills m2).
2. `red-section-full-table` — complete header+rows table entirely **outside** the markers →
   expect 1 (kills m6).
3. `red-two-open-markers` — two `<!-- instrument-registry v2 -->`, one close → expect 1 (m10).
4. `red-empty-census` — `{"paths": []}` → expect 2 (m11; the scope refusal, not a red score).
5. `red-battery-accepts` — call `score()` with `battery={"forgeries_total":7,"v1_green":7,
   "v2_green":7,"genuine_green":1}` → expect 1 (kills m9b). This is the only way `--selftest`
   can reach the battery acceptance loop without running seven fixtures, and it is cheap.
6. `red-frozen-touch` — two commits, freeze `A`, rev `B` modifying `tools/round-46/a.py` →
   expect 2 with `restored` naming the path (kills m12).
   Optional: `red-duplicate-cell` (pins first-wins, m8) and a close-before-open expectation that
   asserts the diagnostic string (m7).

Note for whoever cuts them: cases 3–6 must assert the **exit code**, not just "some clause
fired", because that is exactly how m2/m6 hid (verdict unchanged, reason changed).

## 7. Evidence inventory (all in this directory)

| file | content |
|---|---|
| `mutants-head.json` | 13 mutants on landed bytes: anchor, mutant sha256, exit, stdout sha256, UTC, flipped cases, verdict; baseline receipt |
| `mutants-frozen.json` | the same 12 applicable mutants on the freeze-tree bytes (m4 anchor mismatch recorded) |
| `probes.json` | P1–P11 targeted `score()` detectors, pristine vs mutant, both bases |
| `fixtures.json` | F1–F4 committed-fixture `evaluate()` runs, pristine vs mutant |
| `battery-bases.json` | each base's own `run_battery` over the landed section (F3 table) |
| `live-pristine.json` | counting command at `--rev HEAD`: exit 2 `frozen_path_changed` |
| `live-headbytes-at-freeze.json` | counting command at `--rev <freeze>`: exit 1, 38 unregistered |
| `live-frozenbytes-at-head.json` | freeze-tree bytes at `--rev HEAD`: exit 2, same receipt |
| `driver.py`, `probe.py`, `fixture.py` | the exact drivers; re-run requires only `python3` and `git` |

Restoration: every mutation was applied to a copy under `S`; `S` was removed after the
receipts were copied here (`/fast/scratch/hyaku/kaidoku-r46/R46W1MutC2Checks` no longer
exists). At **2026-10-28T17:08:25Z** the lane's `tools/round-46/registry.py`, `gate.py` and
`plans/round-46-claims.md` were byte-identical to the then-HEAD (`git status --porcelain`
empty for those paths; `registry.py` still has sha256 `5e16e4af…` at the end of the seat).
`gate.py` and `attest.py` were changed **after** that check by another seat — see §9.

## 8. Not run

- A CLI run of the battery at `--rev HEAD` — impossible while F1 holds (exit 2 before the
  battery); the battery was measured through `run_battery()` and `score(battery=…)` instead.
- `attest.py` (C1) mutation — another seat's target; nothing here says anything about it
  beyond the freeze-byte divergence recorded in F1.
- No installs were needed, so there is nothing to record under the tooling directive.

## 9. Post-verification lane movement (observed, not this seat)

The lane advanced **during** this seat, and `tools/round-46/gate.py` / `attest.py` were
rewritten in place while wave 1 ran. Dated facts, all read-only observations:

| when (local, -0300) | what | evidence |
|---|---|---|
| 14:00:26 | seat copies `registry.py`/`gate.py`; then-HEAD `1e32827…` | file shas in §0 |
| 14:08:25 | restoration check: tools + claims byte-identical to HEAD, `status` empty for those paths | §7 |
| 14:09:07 | `gate.py` rewritten in the working tree (`9ab7e2a3` → `dac075f1`), +27 lines; derives the frozen set at both ends and unions it, and refuses an uncommitted frozen-tool change | `git diff` at 17:09:2xZ |
| 14:09:19 | `attest.py` rewritten in the working tree (`936910fe` → `7aaa9b72`), +26 lines, two new selftest cases | same diff |
| 14:08:11–14:09:45 | new commits land: `47b5e265` (B1 rows), `3ffbe0f8`, `80fec3ca`, `deee6595` (LOG/SCORECARD "both claims met at 0425224, the four-commit freeze disclosed"), `332f4884` (F5), `58eb04b6` (A4), `b5c4ea60` | `git log 1e32827..HEAD` |

Not this seat: every write here was under `S` (removed) or this report directory. The
commit messages attribute the edits to the L1's own F5/A4/CL7–CL11 work, not to
`R46W1MutC2Checks`. `registry.py` itself was **not** touched by any of those commits — its
blob is `26f9e9c6` at `1e32827`, at `332f4884` and at `58eb04b6` — so every mutant result in
§2/§3 stands against the current bytes.

Re-checks against the current lane (2026-10-28T17:10:04Z), with a fresh scratch that was
removed again:

- `registry.py --root <lane> --freeze 3182047… --rev <HEAD 58eb04b6> --selftest` → exit **0**,
  `cases=12 failures=0`, stdout sha256 `0fa8c31a6419…` — the new `gate.py` leaves the 12
  verdicts untouched.
- `--freeze 3182047… --rev 58eb04b6` → exit **2** `frozen_path_changed`, `restored
  ['tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']`
  (F1 holds at the new HEAD too).
- `--freeze 3182047… --rev 04252247` → exit **2** as well: the exit-2 condition is a property
  of the *range*, not of the tip.

### 9.1 Reconciliation with the re-freeze the record names — the pattern recurs
The record (`deee6595`) says the claims were scored at `0425224` with a disclosed four-commit
freeze. That pair does score met, and I reproduce it:

```sh
python3 -I -B tools/round-46/registry.py --root <lane> --freeze 04252247 --rev 04252247
```

→ exit **0**, `met_target true`, `failing []`, `scope_size 38`, `registry_rows 38`,
`frozen_path_changed []`, battery `forgeries_total 7 / v1_green 7 / v2_green 0 /
genuine_green 1`, `genuine_exit 0`, stdout sha256
`d3869553edf79e572238c1aecac68ccbe408c0daa8b28f51b5971d7314539ac1`.

But the same command with `--rev HEAD` → exit **2** (`frozen_path_changed:
['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py']`, `restored`
`attest.py` and `gate.py`), because **F5 (`332f4884`) and A4 (`58eb04b6`) themselves touch
two frozen tools after `0425224`**. So `0425224` is scorable only *at* `0425224`: the
instrument that repairs the freeze defects re-breaks the freeze it repairs, and any rev after
`58eb04b6` is inadmissible. That is the same shape as the round's own M46-3/M46-4 finding
("four freeze commits; the proxy-harm recurrence") reproduced inside wave 1 — worth one row
in the ledger, because wave 2 must falsify at a rev, and every candidate rev is exit 2 under
every freeze this lane has declared so far.

For completeness: the freeze-tree bytes at the declared freeze could not have produced even
that receipt (F2) and would have failed clause 6 there (F3); the artefact and the landed
instrument are sound (F4), which is why the re-cut at `0425224` scores clean.
