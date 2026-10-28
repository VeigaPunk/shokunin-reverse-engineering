# R46W1SentTools — adversarial security review of `tools/round-46/`

Seat `R46W1SentTools` (leaf; no subagent dispatch). Lane `kaidoku-shokunin`.
Target: `tools/round-46/{gate,attest,registry,census}.py` — command injection, path traversal,
hostile `SKILL.md`/`census.json`, writes outside scratch, attacker-controlled refs, timeouts.

Read-only on the lane tree: this seat wrote only `.ufo/waves/round-46/w1/R46W1SentTools/`
and `/fast/scratch/hyaku/kaidoku-r46/R46W1SentTools` (removed before yield). No git/jj
mutation was run in the lane; every fixture was `mktemp -d -p $S` + `git -C "$D"`
(`rev-parse --show-toplevel == $D` asserted before every first commit).

## 0. What was actually reviewed (two byte sets, because the lane is moving)

| byte set | commit | gate.py | attest.py | registry.py | census.py |
|---|---|---|---|---|---|
| **declared freeze** (prompt) | `31820472784284727546808acc31b3ea1e73919b` | `64626cca…` | `dd1e7df1…` | `307506d5…` | `960c516d…` |
| **current** | `22fd0d6b…` → `c0112995…` (tools unchanged) | `c3ba6b93…` | `c4056131…` | `5e16e4af…` | `960c516d…` |

Full sha256: see `current.json`/`verify.json` (`_bytes`), `frozen-probes.json` (`_bytes`).
The frozen copies were extracted with `git show 3182047:tools/round-46/…` into scratch and
probed through their own CLI; the current copies were probed through the lane CLI.
A finding is marked **open** only where I reproduced it on that byte set.

Exit codes are semantic: 0 met, 1 not met, 2 could-not-evaluate. Every receipt below names
the command, exit, stdout sha256 and UTC; the machine-readable set is in
`receipts.json`, `ab.json`, `frozen-probes.json`, `frozen-c2.json`, `current.json`,
`verify.json`, `shrink-cli.json`, `freezeathead.json` (same directory), indexed by
`receipts-table.md`.

## 1. Verdict

The **current** instrument survives the classic attack surfaces (no shell, no fixture-path
escape, no ref injection into the counters) and the two HIGH defects that wave 1 already
found — tip-derived frozen set and uncommitted-tool execution — are genuinely closed at
`332f4884`. What it does **not** survive is the attack it is actually built to face: an
artefact that satisfies the *shape* of the claim without the work, and a counter that trusts
a file the graded repo controls. Four findings are open at current bytes, two of them HIGH.
Additionally the **declared freeze is dead on both claims** and cannot be the citable
surface (§2).

| id | severity | one line | frozen `3182047` | current `c4056131` |
|---|---|---|---|---|
| P0 | **blocking** | declared freeze does not contain the reviewed bytes; 4 commits in `FREEZE..HEAD` touch frozen paths; at the freeze C1 crashes (`NameError: REF`) and C2's battery cannot reach its floor, so neither claim can ever return 0 there | **broken** | exit 2 `frozen_path_changed` (correct) |
| S1 | **HIGH** | C2 met by a fabricated `census.json` (1 row instead of the derived 3) — the census is never re-derived | **open** | **open** |
| S2 | **HIGH** | C1 met by a 13-row placeholder table (`\| R45-CL2 \| filler \| commit \| 0 \|`) — v2 is a shape test, and the battery only mutates shape | open (structural) | **open** (battery 9/9/0/1) |
| S3 | **HIGH** | C1 measures the *first* `## Queue-drain craft` in the file: a fenced `(example)` decoy hijacks the verdict while the real section has no block 23 | **open** | **open** |
| S4 | **MEDIUM** | C2 registers rows inside an HTML comment opened mid-line, and inside a ``` fence broken by a `~~~` | open | **open** |
| S5 | **MEDIUM** | C2 never validates 5 of its 7 house columns (purpose, self-test, pinned value, write scope, owner) | open | **open** |
| S6 | **MEDIUM** | `--json-out` may overwrite `.git/config`, `.git/HEAD`, `.git/objects/info/alternates`, `.ufo/state/*` | **open** | **open** |
| S7 | **MEDIUM** | `census.py --out` has no guard at all: writes outside the lane and can clobber `tools/round-46/` itself | **open** | **open** |
| S8 | **MEDIUM** | repo-configured command execution: `core.fsmonitor` from the measured repo runs during `git status` | unreachable (`dirty()` dead) | **reachable, RCE proven** |
| S9 | LOW | non-UTF-8 blob turns a red verdict into exit 2 (or, at the freeze, exit 1 + traceback) | open | open |
| S10 | LOW | `scratch()` accepts a root inside the graded surface (`HYAKU_SCRATCH=tools/round-46`) | open | open |
| S12 | LOW | `--no-battery` prints `met_target: true` with clause 7 unevaluated | **open** | **open** |
| S11 | LOW | record drift: `--selftest` counts and the documented self-test command | — | — |

## 2. P0 (blocking) — the declared freeze is not the instrument

`3182047` is what the prompt and `plans/round-46-claims.md` cite. It is not what is on disk,
and it cannot be scored.

**Input / evidence**

```
$ git log --format='%H %s' 3182047..HEAD -- tools/round-46 plans/round-46-claims.md
50862e4a… round-46: complete the freeze — … (declared as the authoritative freeze …)
65678df0… round-46 F3: the freeze is the instrument that can actually be scored — the battery's dead REF name, …
04252247… round-46 F4: the v1 registry profile applies its own loose checks …
332f4884… round-46 F5: close the two HIGH instrument defects wave 1 found …
$ git rev-list --count 3182047..HEAD -- tools/round-46 plans/round-46-claims.md
4
$ python3 -I -B tools/round-46/attest.py --root . --freeze 3182047… --rev HEAD --no-battery
exit 2   reason=frozen_path_changed
         frozen_path_changed=[tools/round-46/, …/attest.py, …/gate.py, …/registry.py]
         dirty=[]   met_target=null
         stdout sha256 47dc11dd28b2b526df108f00d3a5f80d9629bc496133acf13dbea840d5ed2881   17:15:00Z
```

The claims file's own rule — "Nothing in this file or in `tools/round-46/` changes after the
freeze: a change makes both counters exit 2 `frozen_path_changed`" — therefore makes the
round unscorable at the revision the record names. `git log --format=%H -1 --
plans/round-46-claims.md` still returns `3182047`, so a reader who re-derives the freeze the
way the claims file says to gets the stale one.

This is not merely staleness: the frozen bytes cannot produce a met verdict at all.

* **C1 (frozen)** — `attest.py:322` calls `REF.search(...)`; `REF` is defined nowhere (only
  `HARD_REF`/`LOOSE_REF` exist, lines 54/58). Every run that reaches the battery dies:

  ```
  exit 1
  stdout: {"reason": "unhandled NameError: name 'REF' is not defined"}
  stderr: Traceback … frozen/attest.py line 476, in main
              code, receipt = gate.main_guard(
  ```
  and the crash is *exit 1*, not 2, because the frozen `gate.main_guard` (gate.py:215-221)
  returns the int `2` while `attest.py:476` unpacks it — so `R45-CL13`(f) ("a malformed
  heading crashed to exit 1 with empty stdout instead of exit 2") is reincarnated in the
  bytes that claim to close it.
  The frozen `--selftest` never exercises the battery (no `battery=True` case), so
  `ATTEST_SELFTEST: cases=15 failures=0` is green over a battery that cannot run.
* **C2 (frozen)** — a legitimate green fixture with the real counting command:
  `exit 1  failing=["battery v1_green 5 != 7"]` (battery: 7/5/0/1). Clause 6 is
  unsatisfiable at the freeze: the v1 port applies v2's strict checks, so `v1_green` can
  never reach 7.

**Smallest remediation.** Re-declare the freeze at the commit that carries the final bytes
(`332f4884` or later, whichever the L1 lands last) as a *superseding* line in
`plans/round-46-claims.md`, record `3182047` as superseded with this receipt, and delete the
stale `cases=`/`sha256` references that point at `dd1e7df1…`. Do not cite `3182047` anywhere
in the landing evidence. (Editing the claims file is itself a frozen-path change: the honest
move is a new claims file commit that states the supersession, accepted as a *new* freeze,
not a silent amendment.)

## 3. S1 (HIGH, open) — C2 is met by a fabricated census

**Hostile input** — `tools/round-46/census.json` committed as `{"paths": ["tools/round-46/a.py"]}`
where `census.py` derives 3 paths from the same revision, plus one registry row.

**Code** — `registry.py:125 load_scope()` reads the checked-in file and nothing else;
`registry.py:50` sets `"scope_size": None` for the v2 spec, so no count is pinned; the counter
never calls `census.census()`, and `run_battery` (`registry.py:341`) builds its fixture from
`need = ["SKILL.md", spec["census"]] + scope`.

**Exploitable: yes.**

```
python3 -I -B tools/round-46/registry.py --root <fixture> --freeze <rev> --rev <rev>
exit 0   met_target true   scope_size 1   failing []
census.py on the same rev: 3 paths
stdout sha256 44c6e0af80961f3932c483d194f687249fa833a97d220aeacf094d86decc4da5  17:11:53Z
(frozen bytes: same construction, masked only by the frozen battery defect — `battery v1_green 5 != 7`)
```

**Impact** — C2's clauses 3 and 5 reduce to "the file the graded repo ships says so". The
claim's own words ("every path matching `tools/round-4[1-6]/**.{py,sh}` that is *named in* a
`plans/round-4[1-6]-claims.md` at `--rev`") are not computed by the counter; a one-row registry
is green while 37 real instruments are unregistered. This is the same class as `R45-CL2`, one
level up: the *scope* itself is a forgery surface.

**Smallest remediation** — in `registry.score`, re-derive and compare:
`derived = census.census(root, rev)["paths"]`; require
`json.loads(files(spec["census"]))["paths"] == derived` (else exit 2 `census_stale`), and set
`scope_size = len(derived)` so the count is pinned by derivation, not by the file.

## 4. S2 (HIGH, open) — C1 is met by a placeholder table

**Hostile input** — block 23 whose rows carry only the required tokens:

```
| R45-CL2 | filler | commit | 0 |      … 13 rows, ids R45-CL2/6/7/9/13/14/15/18/19/20/22/23/24,
| R45-CL6 | filler | commit | 1 |         column 1 always "filler", exit cycling 0/1/2
```

plus `S142`, the `sha256:` pin of the measured `attest.py`, and six line-selected citations
(`corpus/lessons/round-45.md:1-2` … `plans/round-46-claims.md:4-5`).

**Code** — `attest.py:150 score()` validates cell 0 (routed ids), cell 2 (arm vocabulary,
*substring* at `any(t in r[2].lower())`), cell 3 ∈ {0,1,2}, and row width. Column 1
("v1 hole") and the *meaning* of the exit values are never read.

**Exploitable: yes.**

```
python3 -I -B tools/round-46/attest.py --root <fixture> --freeze <rev> --rev <rev>
exit 0   met_target true   failing []
battery {forgeries_total 9, v1_green 9, v2_green 0, genuine_green 1, v2_crash 0}
rows 13   block_title "23. Placeholder."
stdout sha256 34cfb2225fd3aabeae2ef7a15ae402796514cd1c1012a37c343f4ae48add447f  17:11:53Z
```

The battery does not catch it **by construction**: all nine mutations are shape mutations
(garbage cells, thin rows, stripped selectors, header suffix, doubled marker, zeroed pin,
self-refs, dropped id, non-vocabulary arm). An artefact that keeps the shape and drops the
content is green in both profiles. (At the frozen bytes the same artefact passes the
structural clauses: `exit 0`, `rows 13`, `refs 7`, `--no-battery`;
sha256 `3afd25e5beb04e3d46765580c403bed3b94129ba5ef61224ae186fdda24a6643`.)

**Impact** — round 45 was rejected because a 44-line forgery scored `met_target: true`. This
is the same disease one abstraction higher: the v2 measure is a syntactic contract, so a
13-line table of `filler` is `met`. Nothing in the predicate distinguishes block 23 from a
stub that names the ids.

**Smallest remediation** — make each cell carry a checkable binding instead of a token:
require `cell0` ↔ `cell1` to name the routed lesson anchor and the lesson file/line
(`corpus/lessons/round-45.md` occurrence of the id), require `cell2` to be an exact
vocabulary member (`r[2] in ARMS`, not substring), and require a per-row citation that
resolves. That converts "names an id" into "cites where the id is defined", which a
placeholder cannot satisfy.

## 5. S3 (HIGH, open) — C1 measures a decoy craft section

**Hostile input** — `SKILL.md` whose *first* `## Queue-drain craft` occurrence is a fenced
example:

```
# SKILL
intro
```
## Queue-drain craft (example) 
- **23. Placeholder.** <!-- freeze-integrity-table v2 --> …   (a passing block)
```
## Real
body
## Queue-drain craft 
- **1. Plain rule 1.** body
- **2. Plain rule 2.** body
```

**Code** — `attest.py:88 craft_section()` is `skill.split(CRAFT, 1)[1]` — first occurrence,
fence- and comment-blind.

**Exploitable: yes.**

```
exit 0  met_target true  failing []
attest.craft_section(skill) head == ["(example) "]
real craft section: 1 block, no block 23
stdout sha256 1f9893e5c4c18bf330166d1ee3f994d1ea0c41120e0ad9c27dad11558678fe6e  17:11:53Z
(frozen bytes: exit 0, measured ["(example) "], sha256 1427ae7f2cf84de0a1bfac6593669f92d228f9cf39c3770c47b6504fb3577658)
```

**Impact** — the measure and the graded surface can be different objects: the landed craft
section can be empty while a fenced example is what scores. `block_is_last` is computed
*inside* the decoy, so it passes too.

**Smallest remediation** — take the **last** occurrence, or require the heading to be exactly
`## Queue-drain craft (…)` at column 0 with no fence open at that point; simplest correct
form: scan lines with a fence/comment state machine, collect every column-0 heading that
starts `## Queue-drain craft `, and refuse (exit 2 `ambiguous_craft_section`) unless exactly
one exists.

## 6. S4 (MEDIUM, open) — C2 registers rows inside an HTML comment and inside a broken fence

**Hostile input (a)** — the section's rows wrapped in a comment that *opens mid-line*, so the
parser's `s.startswith("<!--")` test never fires:

```
note: <!-- begin hidden
| `tools/round-46/a.py` | gate | 0=met; 1=not met; 2=could-not-evaluate | … |
end -->
```

**Hostile input (b)** — a ``` fence whose state the parser flips back off with a `~~~`:

```
```
~~~
<rows>
~~~
```
```

**Code** — `registry.py:85 rows_in_section()`: fence toggled by any line starting ``` ``` ``` or
`~~~` (line 91), so `~~~` inside a ``` block closes it; comment state entered only when the
line *starts* with `<!--` (line 99).

**Exploitable: yes** — both, at both byte sets:

```
(a) exit 0  met_target true  failing []   sha256 53b1a4e586898775aeacb2981dcec6459fc4f9a5d8638063d3277781919efbae 17:11:53Z
(b) exit 0  met_target true  failing []   sha256 ffdee675f626e87cd8e6b291a02ab932b93617e052ffa0a654b73e6025f96a31 17:11:53Z
frozen: (a) exit 0 met  sha256 95f831dae0efbb4c7e37b6eff5e4fe722ff20750d76e762aba37d626b85972e9
        (b) exit 0 met  sha256 57f1bf18ed11a5a0bf83c96165ac8419ebf5e56d0959f9688d28ad5fe2d2b2eb
```

**Impact** — clause 1 ("rows register only between them, outside fenced blocks and outside
HTML comments") is false for two ordinary Markdown constructions; the tiered-defence claim
"nothing outside it … registers" is a parser claim with a parser bug.

**Smallest remediation** — track the fence *token* and length (`^(`{3,}|~{3,})` → remember
the char and count; close only on the same char with ≥ the count), and detect `<!--`/`-->`
anywhere on the line, with a single pass that also refuses an unterminated comment/fence at
end of section (exit 2).

## 7. S5 (MEDIUM, open) — five of seven house columns are unvalidated

**Hostile input** — rows with only cells 0 and 2 populated:

```
| `tools/round-46/a.py` |  | 0=met; 1=not met; 2=could-not-evaluate |  |  |  |  |
```

**Code** — `registry.py:169` checks only `header == HOUSE`; per row only `row[0]` (line 182)
and `row[2]` (line 196) are read.

**Exploitable: yes** — `exit 0  met_target true`, sha256
`e64b7fc92d2023a83a4ad953e286d5c9b39476f8eed220368d50e67ea6ffc12b` (17:11:53Z).

**Impact** — the registry's purpose ("gate or probe – purpose", "self-test command",
"pinned-value path", "write scope", "owner") is exactly the part an operator reads and the
part the counter cannot see; a wall of empty cells scores 38/38 if cell 0 is right.

**Smallest remediation** — require cells 3–6 non-empty, and require cell 3 to start with
`` ` `` (a command), cell 5 ∈ {repo, scratch, none} (fixed vocabulary).

## 8. S6 (MEDIUM, open) — `--json-out` writes into `.git/` and `.ufo/`

**Code** — `gate.py:198 out_path()` refuses only `GRADED = (SKILL.md, LOG.md, SCORECARD.md,
PROVINCE.md, SHONEN.md, plans, tools, corpus, evidence)` (line 208). `.git` and `.ufo` are not
in it, and the resolved path is inside the lane root, so both pass.

**Exploitable: yes.**

```
gate.out_path(d, d/".git/config")                     -> accepted
gate.out_path(d, d/".git/HEAD")                       -> accepted
gate.out_path(d, d/".git/objects/info/alternates")    -> accepted
gate.out_path(d, d/".ufo/state/wave.json")            -> accepted
write landed: .git/hooks/pre-commit   mode 0644
sha256 e2/d7: 7_write_scope (17:11:53Z); receipts.json e2_out_path
```

**Impact** — `--json-out` is an operator-supplied path, and the counter is documented to
"never write inside the repo it measures". `.git/config` overwrite corrupts the measured repo;
`.git/objects/info/alternates` redirects the object store a later measurement reads;
`.ufo/state/*` is the wave bookkeeping every seat is forbidden to touch. The mode is 0644, so
a hook is not directly executable — the object-store and config writes are the real damage.

**Smallest remediation** — refuse any relative path with a `.git` or `.ufo` component
(`if {".git", ".ufo"} & set(rel.split("/"))`), and write with
`os.open(full, O_WRONLY|O_CREAT|O_TRUNC|O_NOFOLLOW, 0o644)` after the `realpath` check.

## 9. S7 (MEDIUM, open) — `census.py` has no output guard

**Code** — `census.py:65-71`: `ap.add_argument("--out")` … `with open(args.out, "w")`. It never
calls `gate.out_path`, and `--rev` is passed to `git show` unresolved (`census.py:30 _read`).

**Exploitable: yes.**

```
census.py --root <fixture> --rev <rev> --out /fast/scratch/…/census-out.json
  exit 0   file written outside the lane
census.py --root <fixture> --rev <rev> --out <fixture>/tools/round-46/a.py
  exit 0   the tool file is now census JSON
frozen bytes: identical (p8_census_out)
```

**Impact** — the generator can silently overwrite the instrument it feeds, including the
frozen surface; `R45-CL22`'s arm covers only the two counters, so the tool that *builds C2's
scope* is the softest write path in the round.

**Smallest remediation** — `full, err = gate.out_path(args.root, args.out)` before opening,
and `gate.resolve(args.root, args.rev)` before any read (which also closes the leading-dash
option vector below).

## 10. S8 (MEDIUM, open at current bytes) — repo-configured command execution

**Code** — `gate.py:43 git()` builds `["git", "-C", root, *args]` with no
`-c core.fsmonitor=`/`GIT_CONFIG_NOSYSTEM`/`--literal-pathspecs`; `gate.py:132 dirty()` runs
`git status --porcelain`, and at current bytes `freeze_state` (line 144) calls it. (At the
frozen bytes `dirty()` exists but no caller — deadline code, harmless.)

**Hostile input** — a measured repo with `core.fsmonitor` pointing at a script:

```
git -C "$D" config core.fsmonitor ./h.sh     # h.sh: touch $D/FSMON; exit 1
python3 -I -B tools/round-46/attest.py --root "$D" --freeze "$REV" --rev "$REV" --no-battery
exit 0   met_target true   FSMon exists: TRUE
stdout sha256 c262081a1549c5a743a02fbd3486656cb57f10665af668ec3fc836356cb4f155  17:13:16Z
```

**Exploitable: yes, end-to-end**, but only against a repo the operator points `--root` at:
the lane's own `.git/config` is trusted, so this is a hardening gap, not a lane compromise.
It contradicts the module docstring ("Reads Git objects only; never writes inside the repo it
measures") — it *executes* repo-configured code.

**Smallest remediation** — harden the one constructor:
`["git", "-C", root, "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null",
"-c", "log.showSignature=false", "--literal-pathspecs", *args]`, and set
`GIT_CONFIG_NOSYSTEM=1` in `env`. `--literal-pathspecs` also removes pathspec-magic
interpretation of claims-file entries (an entry like `:(exclude)tools/` is currently honoured
as magic — `history_touched`'s `--` does not make it literal).

## 11. S9/S10/S11 (LOW)

* **S9 — non-UTF-8 blob.** `gate.py:43` uses `text=True` (strict UTF-8) for every blob read.
  A cited file containing `0xFF` makes the counter die:
  frozen `exit 1` + traceback; current `exit 2`
  `unhandled UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 240`.
  An artefact can therefore convert "violation" into "could-not-evaluate". Fix: `binary=True`
  in `git()` and `body.decode("utf-8", "surrogateescape")` in `show()` (as
  `history_touched` already does).
* **S10 — scratch inside the graded surface.** `gate.py:213 scratch()` rejects only `/tmp`
  and `/var/tmp`; `HYAKU_SCRATCH=<lane>/tools/round-46` is accepted and `mkdtemp` creates
  `tools/round-46/probe-…` (measured, accepted). Fix: also refuse a root inside
  `os.path.realpath(root)`'s `GRADED` subtrees.
* **S12 — `--no-battery` manufactures `met_target: true`.** `attest.py:441 evaluate()` skips
  the battery entirely — when `with_battery` is False neither battery branch runs, so the
  receipt carries **no `battery` key at all** — while `score()` still sets
  `met_target = not failing`. A run with
  the flag is therefore `exit 0, met_target true` with clause 7 never computed — that is
  how the frozen C1 structural pass above reads (`c1_vacuous_structural`, sha
  `3afd25e5…`). Anyone scoring must read `battery`, not `met_target`, or the instrument
  must set `met_target: null` when the battery is skipped. Same shape in `registry.py`.
* **S11 — record drift.** `ATTEST_SELFTEST: cases=15` is true only of the frozen bytes
  (current prints `cases=18`); `REGISTRY_SELFTEST: cases=12` at both byte sets while
  `plans/round-46-claims.md` says 11. And `--selftest` with no `--root/--freeze/--rev` exits
  2 (`argparse` required args are validated before the `if args.selftest` branch), so the
  preflight command *as written in the claims file* does not run. Any registry row or block
  23 self-test cell must therefore be
  `` `python3 -I -B tools/round-46/attest.py --root . --freeze x --rev y --selftest` ``.

## 12. Verified negatives (do not re-litigate)

| surface | result | evidence |
|---|---|---|
| **(a) command injection** | **no.** Every `git` call is an argv list; no `shell=True`, `os.system`, `eval`, `exec`, or string-built command anywhere in the four files. SKILL rows and claims entries never become a command. | `grep -n "shell=True\|os.system\|os.popen\|eval(\|exec(" tools/round-46/*.py` → no matches (`E3/p7` receipts) |
| **(b) fixture path traversal** | **no.** `registry.run_battery` does `os.path.join(d, p)` at line 364 for census-derived `p`, but it is reached only after `gate.show` returned a body, and git refuses `..` and leading `/` in `<rev>:<path>`: `HEAD:../x` and `HEAD:/tmp/pwn` → `fatal: … outside repository` / `does not exist`; `HEAD:./tmp/pwn` resolves but `os.path.join(d,"./tmp/pwn")` stays inside `d`. A tree entry literally named `..` (built with `git mktree`) is not traversable. | `A3_traversal_negatives` (17:07Z) |
| **(b′) `--json-out` traversal** | **no** for `../`/absolute targets (`commonpath` check + `realpath`); **yes** for `.git`/`.ufo` (S6). | `e2_out_path`, `7_write_scope` |
| **(c) hostile SKILL/census** | **yes** — S1, S2, S3, S4, S5. | §3–§7 |
| **(d) writes outside scratch** | **cleanup: yes.** No `fx-*`/`kaidoku-*` dir or repo survives a CLI run; `evaluate()` removes the battery scratch root in `finally`. `attest.run_battery` calls `fixture_repo` outside its `try`, so an exception there leaks `d` — but the same `finally` removes the whole root, so nothing escapes scratch. **But** S6/S7 write outside scratch on request. | `e12_cleanup` (`new_entries_in_scratch []`, `leftover_fx_dirs []`) |
| **(e) attacker-controlled refs** | **no, for both counters.** `resolve()` rejects every leading-dash probe (`--all`, `-h`, `--branches`, `--revs-only`, `--end-of-options`, `--glob=*`, `--output=…`) → `freeze_state` exit 2 `unknown … revision`; afterwards `base`/`tip` are hex, and `history_touched` uses `base..tip` with `--`. **Partial, for `census.py`:** `--rev` reaches `git show` unresolved, but the appended `:path` always contains `/`, so `--output=` cannot create the file git tries to open (`fatal: could not open '…/injx:plans/…': No such file or directory`). Not a write, but resolve it as S7 says. | `e4_dash_refs`, `e3_census_rev_option_injection`, `e3_git_show_output_probe` |
| **(f) subprocess without timeout** | **read path: no gap** — every `gate.git` call carries `timeout=120`. **Fixture path: 12 `subprocess.run(["git", …])` calls with no timeout and `check=True`** (`attest.py:362-386`, `registry.py:357-371`); they act only on tool-created fixtures, so a hostile census with thousands of paths is a slow `git add -A`, not RCE. | `grep -n "subprocess.run" tools/round-46/*.py` |
| **(g) frozen-set shrink (wave-1 HIGH)** | **closed at current bytes, open at the declared freeze.** At the freeze `frozen_set(root, tip)` alone let one commit rewrite the section and hide its own tools edit: `exit 0`, `frozen_derived ["corpus/unused.txt"]`, `frozen_path_changed []`. At current bytes both counters return `exit 2 frozen_path_changed` for tamper-only *and* tamper+shrink (`registry` too). | `p10_frozen_gate_shrink`, `c1_tamper_plus_shrink`, `c2_tamper_plus_shrink` (17:13Z) |
| **(h) uncommitted tool executes (wave-1 HIGH)** | **closed at current bytes.** Clean fixture `exit 0`; one appended line in `tools/round-46/gate.py` → `exit 2 reason=frozen_worktree_dirty`, `dirty ["tools/round-46/gate.py"]`. Absent at the freeze. | `dirty_arm` (17:13:15Z) |

## 13. For the L1 (paste-time notes, not a registry row)

1. Do not cite `3182047` as the freeze (P0). Re-declare, then re-run both counters at the
   new freeze; the current counter correctly refuses the stale one.
2. S1 and S2 are the two that decide whether this round repeats round 45: both produce
   `met_target: true` with an artefact that does no work, at the bytes that would be landed.
3. S3 means the *landed* block 23 must be the only `## Queue-drain craft` heading in
   `SKILL.md` — otherwise the verdict may describe a fenced example.
4. Any self-test command written into block 23 or a registry row must include
   `--root . --freeze x --rev y`, else it exits 2.
5. `census.py` must not be run with `--out` pointing at a tracked path until S7 is fixed.
6. Never accept `met_target: true` from a `--no-battery` run (S12): the battery is
   half the predicate for C1 and all of clause 6 for C2. Read the `battery` block.

## 14. Receipts

`receipts-table.md` indexes every probe below (command, exit, stdout sha256, UTC). Raw:
`receipts.json` (an earlier HEAD `47b5e265`, attest `e6c44d2d…`), `ab.json`, `current.json`
(`22fd0d6b`), `verify.json` (`c0112995`), `frozen-probes.json`, `frozen-c2.json`
(`3182047`), `shrink-cli.json`, `freezeathead.json`. Environment: Python 3.14.8,
git 2.56.0, `HYAKU_SCRATCH=TMPDIR=/fast/scratch/hyaku/kaidoku-r46/R46W1SentTools`.
No installs were made. Scratch was removed after the receipts above were copied here.
