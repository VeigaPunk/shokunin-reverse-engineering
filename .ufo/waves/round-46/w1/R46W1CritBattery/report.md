# R46W1CritBattery — attack on the round-46 discrimination battery

Seat `R46W1CritBattery`, lane `kaidoku-shokunin`, round 46 wave 1.
Read-only on the lane tree. Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1CritBattery`
(exported as `TMPDIR` and `HYAKU_SCRATCH`), removed after the receipts were copied here.
No installs (nothing needed; `python3` 3.14.8, `git` present).

Read first, as ordered: `plans/round-46-claims.md` (both predicates, clause by clause),
then `tools/round-46/attest.py`, `registry.py`, `gate.py`, plus `SKILL.md:612-655`
(block 23) and `SKILL.md:1686-1737` (registry section).

---

## 0. Verdict in one paragraph

The **battery mechanics are sound and fail closed**: no mutation I could force produced a
false *pass* (every degenerate shape I built either stays red or makes the counter exit 1 on
`battery v2_green`/`battery v1_green`), and the no-op branch is unreachable in the scored
path. The **predicates the battery defends are not sound**: I built two artefacts that are
empty of content and still score `met_target: true`, with receipts byte-for-byte identical
in every *value* to the genuine landing — `F1` for C1 (13 rows of `| R45-CLn | x | commit | 1 |`)
and `F4` for C2 (38 rows of `| \`path\` | x | 0= 1= 2= | x | x | x | x |`). The round's
novelty — "the battery cannot drift from the artefact it defends" — is true, and is also the
limit: the battery defends *syntax*, so an artefact that has the syntax and no content is
certified by it. `R45-CL13` (a) and `R45-CL14` (d) are therefore **not closed**, only
narrowed to forgeries that omit the required tokens.

Second, independent of the battery: **both claims are unscoreable at the declared freeze**
(receipts R3/R4: exit 2 `frozen_path_changed` at `--freeze 3182047`), and **the frozen bytes
themselves cannot run the battery at all** (R14-R16). Those are recorded in §1 and §5.

---

## 1. The freeze blocks the score it is supposed to admit (my own receipt)

The claims file defines the freeze, not a flag: *"**Freeze** = the commit that first contains
this file and `tools/round-46/` (a directory pathspec)"*, re-derived by
`git log --format=%H -1 -- plans/round-46-claims.md`.

```
$ git log --format='%h %s' -- plans/round-46-claims.md
31820472 round-46: freeze — the two claim predicates, the discrimination battery, ...
$ git log --format='%h %s' -- tools/round-46/
04252247 round-46 F4: the v1 registry profile applies its own loose checks ...
65678df0 round-46 F3: the freeze is the instrument that can actually be scored — ...
50862e4a round-46: complete the freeze — the two instrument fixes found before any score ...
31820472 round-46: freeze — ...
```

So `FREEZE = 3182047` is unambiguous, and three commits **after** it rewrite
`tools/round-46/{attest,gate,registry}.py`. Per the claims file's own freeze rule that makes
both counters exit 2 at every revision where block 23 exists — which is every revision the
artefact can be scored at:

* **R3** `attest.py --root . --freeze 31820472… --rev HEAD` → **exit 2**,
  `reason: frozen_path_changed`,
  `frozen_path_changed: ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]`,
  `restored: [attest.py, gate.py, registry.py]`.
* **R4** `registry.py` same arguments → **exit 2**, identical reason.
* **R5/R7** the recorded `met` is reproduced only by passing `--freeze 0425224…`, i.e. the
  F4 commit itself → empty `FREEZE..REV` range. The counter accepts **any** `--freeze` the
  caller supplies and never compares it with the derivation the claims file names.

That is not a battery defect; it is the admissibility frame both claims sit in, and it means
the sentence "both claims met at 0425224" (commit `1e32827`) is true of the *instrument as a
program* and false of the *claim as written*. Corroborated independently by `R46W1RegI`
(receipts at 16:54-16:59) and `R46W1RegJ` (rows 14-22); I re-derived it rather than citing it.

**The frozen bytes are also broken (R14-R16):**

| frozen blob at 3182047 | probe | result |
|---|---|---|
| `attest.py` | `--selftest` | `ATTEST_SELFTEST: cases=15 failures=0` (R14) — explains the claims file's "cases=15" |
| `attest.py` | on the valid token artefact `fx/F1` | **rc 1**, stdout `{"reason": "unhandled NameError: name 'REF' is not defined"}` + traceback + `TypeError: cannot unpack non-iterable int object` at `gate.main_guard` (R15). A **crash is exported as exit 1**, the `R45-CL13` (f) class, in the freeze bytes. |
| `registry.py` | on the empty registry `fx/F4` | rc 1, `failing: ["battery v1_green 0 != 7"]`, all seven forgeries `v1_exit 1` (R16) — the frozen v1 profile is *strict*, so the claim "the v1 clause set scores all seven green" is false of the frozen instrument and true only after F4. |

So the pin `sha256:e6c44d2d…` in block 23 is the **post-freeze** supervisor, and the claims
file's preflight numbers (`cases=15`, `cases=11`) describe the freeze bytes (attest: true; see
§5 for registry).

---

## 2. (a) Can a mutation silently become a no-op, and can a forger force it?

**No in the scored path; yes only for artefacts that already fail clause 3; and forcing it
can only lose.**

Evidence:

* **R17 (probe-noop, part 1)** — all nine `MUTATIONS` applied to the landed block and to the
  token artefact `F1`: **every** mutation returns `changed` (no no-op), for both shapes.
  That is structural, not luck: clause 3 forces ≥13 rows (`m_thin` always removes rows
  9..N), clause 7's pin forces a `sha256:` (`m_stub_pin`), the marker is unique
  (`m_two_markers`), clause 5 forces ≥6 line-selected citations and `corpus/lessons/round-45.md`
  (`m_lineless`), clause 4 forces the ids and vocabulary tokens (`m_garbage`, `m_no_vocab`),
  and clause 1 forces a single `23. ` block (`m_header_substring`, `m_missing_id`,
  `m_self_refs`).
* **R17 (part 2)** — the branch *is* reachable, but only from an invalid artefact: an eight-row
  block makes `m_thin` a no-op (`data[8:]` empty) → `fixtures[{"name":"thin-rows",
  "error":"mutation was a no-op"}]`, `forgeries_total 9`, **`v2_green 1`**, `v1_green 7`.
  `evaluate()` on that same artefact never reaches the branch at all:
  `battery: {"skipped": "artefact fails a structural clause first"}`.
* Direction of the accounting: `out["v2_green"] += 1` for a no-op counts "v2 accepted a
  forgery", and the claim requires `v2_green == 0`, so **a forced no-op is a self-inflicted
  red**. A forger gains nothing. The residual defect is bookkeeping only: a no-op is counted
  as *accepted*, not as *not evaluated*, so `forgeries_total` (=9) stays 9 while nothing was
  scored — see (b).

Smallest safe correction (reported, not applied): raise `ValueError("mutation was a no-op")`
instead of counting it green, and count `forgeries_scored` separately from
`forgeries_total`, with `forgeries_scored == 9` required.

---

## 3. (b) Is a mutation that fails v1 *and* v2 counted in the denominator?

**Yes — and that is the right direction, but the denominator is not what it looks like.**

`run_battery` increments `forgeries_total` on every branch (scored, `ValueError`, no-op),
while `v1_green` increments only when `c1 == 0`. So `forgeries_total == 9` does **not** say
that nine forgeries were scored. Two receipts:

* **R11 (F3)** — a *valid* artefact whose citations are not on a `Refs:` line (clause 5 does
  not require that name). `m_self_refs` has nothing to rewrite → `ValueError` →
  `fixtures[{"name":"self-refs","error":"no reference paragraph found"}]`,
  `forgeries_total 9`, **`v1_green 8`**, counter **exit 1**
  (`failing: ["battery v1_green 8 != 9"]`). A mutation that fails v1 and v2 is in the
  denominator; it simply does not contribute to `v1_green`.
* **R17 (part 2)** — eight-row block: `forgeries_total 9`, `v1_green 7`, and the
  `missing-routed-id` fixture shows `v1_exit 1, v2_exit 1` (a forgery both profiles reject)
  while still being counted in the denominator.

So: counted, yes; punished, yes (`v1_green` is the real witness, `failing` names it). The
smallest correction is the `forgeries_scored` split above; the v1 column already makes the
claim fail closed.

---

## 4. (c) Does the fixture copy every file the refs name, and what happens when one is missing?

**Coverage: complete. Missing-at-rev: silently skipped, and unreachable as a masking path.**

* **R18 (probe-fixture)** — `need` for the landed block is
  `[SKILL.md, corpus/knowledge/2026-10-25-r34b-…md, corpus/lessons/round-45.md,
  corpus/lessons/round-46.md, plans/round-46-claims.md, tools/round-46/attest.py]`
  — the 9 citations in the block collapse to 6 distinct files, plus the pin, the claims file
  and `round-45.md`; `missing_at_rev: []`; and the fixture writes exactly those 6 files.
* **R18** also shows the skip: a path that does not exist at `rev` is dropped by
  `if body is None: continue` (`extra_nonexistent_path_silently_skipped: true`), with no
  error and no listing. Consequence: such a citation scores `absent at rev` inside the
  fixture instead of the mutation's defect class — i.e. the forgery goes red **for the wrong
  reason**. It cannot mask a pass, because a genuine artefact must resolve every citation
  (clause 5) or `evaluate` skips the battery.
* **R19/R20 (probe-gitdir)** — the registry fixture driver is **not** the guarded one.
  `--show-toplevel` appears once in `attest.py`, **zero times in `registry.py` and `gate.py`**;
  `registry.run_battery` issues `init / config / config / add -A / commit -q -m fixture` with
  no toplevel assertion. Replaying **exactly that command sequence** under
  `GIT_DIR=$S/decoy2wt/.git GIT_WORK_TREE=$S/decoy2wt`:
  `git -C d rev-parse --show-toplevel` → `…/decoy2wt`, and the decoy's log gains a `fixture`
  commit tracking `sc/fx-es873zpx/SKILL.md`. The same environment makes
  `attest.fixture_repo` raise `RuntimeError: fixture toplevel mismatch` (R20, attested). The
  contract's fixture rule is implemented on one side of the battery only; a polluted
  environment can therefore land a forged fixture commit in a caller-selected repo.

Smallest correction: have `registry.run_battery` call `attest.fixture_repo` (or repeat its
three-line assertion) before the first commit.

---

## 5. (d) Can the battery be made to pass by weakening the artefact so every mutation is a no-op?

**No. But the same weakening passes without needing a no-op — that is the finding.**

Weakening fails closed: a no-op raises `v2_green` (§2), an unconstructible mutation raises
`v1_green` short (§3), and an artefact that fails any structural clause never runs the
battery. I could not produce a false green from the mutation machinery.

What I *could* produce is a false green from the **predicate**, with the battery 9-0 / 7-0
green:

### F1 — C1 counterexample (R9, exit **0**, `met_target: true`)

Block 23 kept verbatim except the 13 data rows, each reduced to a token triple:

```
| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R45-CL2 | x | commit | 1 |
| R45-CL6 | x | commit | 1 |
... 13 rows, one per routed id ...
```

Receipt values: `rule_blocks 23, marker_occurrences 1, block_present 1, block_is_last true,
header_ok true, rows 13, refs 9, cites {"S142": true, "tools/round-46/attest.py": true},
battery 9/9/0/1/0` — **identical in every reported field to the genuine landing (R5)**.
Clause 4 is a *token census*: `re.finditer(r"R45-CL\d+", r[0])` for the ids and
`any(t in r[arm_col].lower() for t in ARMS)` for the arm. Nothing binds a row's id to its arm,
its exit, or its content; cell 1 is unconstrained. The kill rule's claim — "A 44-line artefact
with garbage rows fails clause 4" — is true only for garbage that *omits* the tokens.
`R45-CL13` (a) in tokenised form still scores met.

### F4 — C2 counterexample (R12, exit **0**, `met_target: true`)

All 38 census rows reduced to:

```
| `tools/round-4X/<tool>` | x | 0= 1= 2= | x | x | x | x |
```

Receipt: `scope_size 38, registry_rows 38, registered 38, unregistered [], thin [],
absent_at_rev [], battery 7/7/0/1` — **identical to the genuine registry (R7)**. Clause 4's
check is `set(EXITMAP.findall(cell)) == {"0","1","2"}` with
`EXITMAP = r"\b([012])\s*[=:]"`; the string `0= 1= 2=` satisfies it exactly while binding no
meaning to any code. The house schema is enforced on the **header row only**; cells 1, 3, 4,
5 and 6 of every row are unconstrained. This is `R45-CL14` (d) ("accepted any cell containing
`0`, `1` and `2`") narrowed to a separator, not closed.

### The mutation classes are artefact-shape dependent (fail-closed, still worth fixing)

| probe | shape | outcome |
|---|---|---|
| **R10 F2** | 14 rows; an extra row mentions `R45-CL18` in cell 1 before the real row | `missing-routed-id` drops the mention row, the artefact stays valid → `v2_green 1` → exit 1 |
| **R13 F5** | the `Refs:` line already equals `m_self_refs`'s target, `round-45.md` cited on its own line | `self-refs` rewrites the line to itself → still valid → `v2_green 1` → exit 1 |

Both are caught by the `v2_green == 0` requirement, so neither is a pass; both show the
nine/seven "defect classes" are properties of one artefact shape, not of the class they name.
`m_missing_id` should drop *every* row naming the id (or assert exactly one row names it);
`m_self_refs` should remove *every* citation of `corpus/lessons/round-45.md`, not one line.

---

## 6. (e) Does the battery leave scratch behind?

**No — with one residue that predates the battery.**

* **R21/R22** — `HYAKU_SCRATCH=/tmp` → exit 2 `scratch root is a temporary partition: /tmp`;
  both variables unset → exit 2 `no HYAKU_SCRATCH/TMPDIR root set`. `gate.scratch()` refuses
  rather than degrading, as claimed.
* After 9 counter invocations and 6 fixture repos: `find $S -maxdepth 2 -name 'kaidoku-r46-*'`
  → empty. Each fixture is `rmtree`d in a `finally`, and `evaluate` `rmtree`s the whole
  scratch root in its own `finally` (so a `check=True` failure inside a fixture cannot leak).
* **Residue:** `tools/round-46/__pycache__/{attest,gate,registry}.cpython-314.pyc` exists in
  the lane *now*, created by operator runs without `-B` (reproduced: running the tool copy
  with bytecode enabled writes `gate.cpython-314.pyc`). It is gitignored
  (`.gitignore:1 __pycache__/`), so `git status --porcelain -- tools/round-46` is empty and
  the directory arm (`blob_changed`, a tree-id comparison) cannot see it. It cannot change a
  verdict — **because the dirty arm is dead code**: `grep -rn "dirty(" tools/round-46/*.py`
  returns the definition only; neither counter calls `gate.dirty()`. The claims file's
  §"Frozen paths" says the derived set is "used for the history arm, the blob arm **and the
  dirty scope**"; no counter uses it, so uncommitted and untracked bytes under a frozen
  path are never inspected. Report the prose as unbacked or wire the arm.

---

## 7. Secondary findings (record drift, all reproducible)

1. **Three control receipts named by the frozen claims file do not exist**:
   `controls/ctl-c1-1-v1-profile.json`, `controls/ctl-c2-1-v1-profile.json`,
   `controls/ctl-c2-2-ghost-tool.json`. On disk: `ctl-c1-0-do-nothing.json`,
   `ctl-c1-fidelity.json`, `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v1-scope.json`,
   `ctl-c2-fidelity.json` (the last is labelled `counter: "round-45-c2"` and scores the
   6-path scope, not the seven forgery classes).
2. **The control as described cannot be produced**: `--profile v1` does **not** rescore the
   battery. `run_battery` always scores each fixture with `v1` *and* `v2` and reports both
   columns, so R6 (C1 `--profile v1`) and R8 (C2 `--profile v1`) differ from R5/R7 only in the
   outer `profile` field — the battery numbers are identical (`9/9/0/1/0`, `7/7/0/1`). The v1
   discrimination gap is a column in every receipt, not a run; the claims file's
   "the nine forgery fixtures scored with `--profile v1` at the freeze, exit 0" describes an
   invocation the instrument does not have (and at the freeze the battery is skipped anyway,
   as `ctl-c1-0-do-nothing.json` itself shows).
3. **Selftest counts drift**: landed `attest.py` prints `cases=16` (R1), the claims file says
   15 (true of the freeze blob, R14); landed `registry.py` prints `cases=12` (R2), the claims
   file says 11. The registry row for `tools/round-46/attest.py` says "15 cases … at the
   freeze" — true of the frozen blob, false of the bytes the row describes at HEAD. That is
   `R45-CL24` (record vs instrument) inside the round that claims to close it; the pin clause
   covers only the sha256, not the row's prose.
4. **`FAILING`/exit contract of the freeze bytes**: R15 exports a crash as exit 1 with a
   traceback; the docstring's "unhandled exception → 2" holds only in the post-freeze bytes.
5. `attest.fixture_repo` requires an existing `scratch_root` (`mkdtemp` raises otherwise);
   harmless in the scored path (`gate.scratch` creates it), worth a line in the docstring if
   the function is ever exported.

---

## 8. Receipts (exact command, exit code, stdout sha256, UTC)

`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`S=/fast/scratch/hyaku/kaidoku-r46/R46W1CritBattery`, `T=$S/tools/round-46` (byte-copies of
HEAD blobs, verified: attest `e6c44d2d…`, registry `5e16e4af…`, gate `847aa33b…`,
census.py `960c516d…`, census.json `573ec008…`), `F=0425224756791b414454df28a9abf93dcdf154ce`,
`REV=deee6595ae3dda094aa5a577fac0f6903e873e16` (lane HEAD at measurement; the tip moved
during the wave, receipts pin the resolved SHA), `Z=31820472784284727546808acc31b3ea1e73919b`.

| id | command | rc | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `cd $L && python3 -I -B tools/round-46/attest.py --root . --freeze HEAD --rev HEAD --selftest` | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 17:04:40Z |
| R2 | `cd $L && python3 -I -B tools/round-46/registry.py --root . --freeze HEAD --rev HEAD --selftest` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 17:04:43Z |
| R3 | `cd $L && python3 -I -B tools/round-46/attest.py --root . --freeze $Z --rev HEAD --json-out .ufo/waves/round-46/w1/R46W1CritBattery/receipts/c1-head.json` | **2** | `3a471c33fde8fc8be01997a6a98e8fa133c0bd296090fb0ece66721b0d09d7e0` | 17:04:51Z |
| R4 | `cd $L && python3 -I -B tools/round-46/registry.py --root . --freeze $Z --rev HEAD --json-out …/c2-head.json` | **2** | `dec44f8737a43fd6caa16e13a2e40411c8971ee3bdd2eac62b7329f643f8f445` | 17:04:51Z |
| R5 | `cd $L && python3 -I -B tools/round-46/attest.py --root . --freeze $F --rev $REV --json-out …/c1-v2-0425224.json` | 0 | `3d028eab71f1d4c363d29ea88dc741a1a5321848691e1bac2864047d7b669b08` | 17:05:53Z |
| R6 | same, `--profile v1` | 0 | `c0533c0a7d86f19aed1fb09f6a7facd0626b56bc3b739b85a3d6d78a2ab50b0b` | 17:05:54Z |
| R7 | `cd $L && python3 -I -B tools/round-46/registry.py --root . --freeze $F --rev $REV --json-out …/c2-v2-0425224.json` | 0 | `e0c457de655942465540e85d010571d26cd30a33008e53e26f800e18f1e58396` | 17:05:56Z |
| R8 | same, `--profile v1` | 0 | `22f59b8daf87a4235f7fc80d5cc2a992b5fd9dd758ec2d80394ce09e70a4144d` | 17:06:00Z |
| — | `cd $S && python3 -I -B build.py F1 attest` (also F2, F3, F5, F6 attest; F4 registry) | 0 | fixture revs: F1 `7a9af6801db4…`, F2 `810c7b994f4e…`, F3 `35357d35202e…`, F4 `4263a332614e…`, F5 `c1554bfdb2e8…`, F6 `c5fc844ad5f1…` | 17:06-17:09Z |
| R9 | `cd $S && python3 -I -B tools/round-46/attest.py --root fx/F1 --freeze 7a9af6801db48e960ed216c164efaaf69b5a3d7a --rev 7a9af6801db48e960ed216c164efaaf69b5a3d7a` | **0** | `498e038c6ffa54148f65f05d973b0ff86504ab390b774a92c305d0d847a6c4b3` | 17:07:05Z |
| R10 | same, `--root fx/F2 --freeze 810c7b994f4ec7638bd88c8bc885cd6203691b29 --rev …` | 1 | `22eba303175519a191c1250a5364c27d38b11c3eb9f324ab4b67896a4df69d13` | 17:07:07Z |
| R11 | same, `--root fx/F3 --freeze 35357d35202e58b3e8261474a68332ab903bff16 --rev …` | 1 | `34349ddad960b03dc66ece110478311375025e8fe86f17cf060a0836c4ff561b` | 17:07:09Z |
| R12 | `cd $S && python3 -I -B tools/round-46/registry.py --root fx/F4 --freeze 4263a332614ee6efb37cfb813232c247efc87aed --rev 4263a332614ee6efb37cfb813232c247efc87aed` | **0** | `e4b0eadfc700d367055e57b7097dcdacdb48d18601b4dc574ae82850841a6a74` | 17:07:11Z |
| R13 | same attest, `--root fx/F5 --freeze c1554bfdb2e8bafddf0d7becfbaed8c9b6fc2211 --rev …` | 1 | `ea8203541a63c91d00b780e253c7edc1abeaee0f8d9690e584306b31d05ca4c1` | 17:09:32Z |
| R14 | `cd $S && python3 -I -B frozen/attest.py --selftest --root frozen --freeze HEAD --rev HEAD` (blobs from `git show $Z:…`) | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 17:08:2xZ |
| R15 | `cd $S && python3 -I -B frozen/attest.py --root fx/F1 --freeze 7a9af680… --rev 7a9af680… 2>&1` | 1 | `221b186f5abc89cfdcaad25c0d3cb4b5f953df1d80378fc5dfca7371bf93f8cb` | 17:08:2xZ |
| R16 | `cd $S && python3 -I -B frozen/registry.py --root fx/F4 --freeze 4263a332… --rev 4263a332…` | 1 | `b47cd0c92e1e3c4f71212b7e922a61de996b91f1088127ada600dfe8fd2d657d` | 17:08:2xZ |
| R17 | `cd $S && python3 -I -B probe_noop.py` | 0 | `6f3d263e9515d9530d648eb89a9c79584a9a682a61b0c50f3a78a6cf991bfbaf` | 17:07:53Z |
| R18 | `cd $S && python3 -I -B probe_fixture.py` | 0 | `ebbd422da306164f34e7ca64785706329e0aab6cde28428420724b607518daf5` | 17:08:03Z |
| R19 | `cd $S && python3 -I -B probe_gitdir.py` (no `GIT_DIR`) | 0 | `c3a4312aa1e359a4daf1b05b1c4bac27e05db35cfe66ccda578708596d514812` | 17:08:38Z |
| R20 | `cd $S && GIT_DIR=$S/decoy_wt/.git GIT_WORK_TREE=$S/decoy_wt GIT_REPO_FOR_TEST=$S/decoy_wt python3 -I -B probe_gitdir.py` | 0 | `1b35297ff79d56f201442b3b3a8e21897f008a871c923127525e18348396e514` | 17:08:38Z |
| R21 | `cd $S && HYAKU_SCRATCH=/tmp TMPDIR=/tmp python3 -I -B tools/round-46/attest.py --root $L --freeze $F --rev $REV` | 2 | `ac933f17baee4849e88ff7f0a24e231116e5f697550822907710354b49c77756` | 17:08:3xZ |
| R22 | `cd $S && env -u HYAKU_SCRATCH -u TMPDIR -u TMP python3 -I -B tools/round-46/attest.py --root $L --freeze $F --rev $REV` | 2 | `ef924935c38575054567f5f29b2c1b4a929567330d8e338489150e5093a5fa36` | 17:08:3xZ |

Probe sources, receipts and the fixture hooks are copied beside this report (`probes/`,
`receipts/`), including `c1-head.json`, `c2-head.json`, `c1-v2-0425224.json`,
`c2-v2-0425224.json`.

## 9. Impacted axes and the smallest safe corrections (reported, not applied)

* **depth (R46-C1)**: clause 4 is a token census. Smallest fix that kills F1: bind each
  routed id to its expected `(arm, exit)` pair in a table derived from the lesson (e.g.
  `R45-CL18 → ("restored", "1")`, `R45-CL6 → ("merge", "2")`), and require each row's
  cell 1 to carry a line-selected `corpus/lessons/round-45.md` citation resolving inside that
  id's section. Then no row can be `x`.
* **calibration (R46-C2)**: clause 4 accepts `0= 1= 2=`. Smallest fix that kills F4: require
  each code to bind a clause — at minimum a non-empty word after `0=`/`1=`/`2=`, at most a
  small vocabulary, and require cell 3 (`self-test command`) to start with
  `python3 -I -B <the same path>` or be exactly `none`, cell 4 to be a path that exists at
  `--rev` or `none`, cell 5 to be a closed vocabulary, cell 1 to name its claim id.
* **battery**: `m_missing_id` must drop *all* rows naming the id (F2); `m_self_refs` must
  remove every `round-45.md` citation (F5); `m_*` must raise on a no-op rather than count it
  green, with `forgeries_scored` required alongside `forgeries_total`; `registry.run_battery`
  must assert `rev-parse --show-toplevel == d` (R20).
* **freeze frame**: derive the freeze inside the counter
  (`git log -1 --format=%H -- plans/round-46-claims.md`) and exit 2 unless `--freeze` equals
  it — otherwise the "met at 0425224" receipt (R5/R7) is a caller-chosen empty range, and the
  declared freeze yields exit 2 (R3/R4). The only clean resolution is a re-freeze whose single
  commit carries the final instrument bytes **and** the claims file.
* **record**: land or restate the three named control receipts (§7.1), state that the v1
  profile is a column not a run (§7.2), correct `cases=15/11` (§7.3), and either wire
  `gate.dirty()` or drop the phrase from §"Frozen paths" (§6).
