# R46W1MutC1Checks — mutation testing of the frozen C1 selftest

**Seat.** R46W1MutC1Checks, round 46 wave 1. Read-only on the lane tree; everything below is a
read of git objects plus copies under `HYAKU_SCRATCH`. No installs (nothing needed beyond
`python3` 3.14.8 and `git`). No mutating git: `init/config/add/commit` ran only inside
`mktemp` fixture repos under my scratch root, each asserted with
`git -C "$D" rev-parse --show-toplevel` before its first commit.

**Deliverable.** This report (also at `.ufo/waves/round-46/w1/R46W1MutC1Checks/report.md`) and
`receipts/` beside it: `mutation-matrix.md` (26 selftest runs with command, exit, stdout sha256,
UTC), `probes.jsonl` (36 probe runs, same fields), `summary.json` (machine matrix),
`mutants/*.diff` (24 single-hunk diffs), `manifest.txt` (sha256 of every receipt), plus the
counter/control/battery receipts cited below.

**Headline.** 12 one-change mutants of `tools/round-46/attest.py`, each aimed at one named
check, run against both byte-sets the lane calls frozen:

| byte-set | selftest | killed | survived | mutation score | required eight (m1–m8) |
|---|---|---|---|---|---|
| A — `31820472` (the freeze this seat names) | `cases=15` | 5 | **7** | 5/12 = 41.7% | 5/8 |
| B — `65678df` = `0425224` = HEAD (the pin in block 23) | `cases=16` | 8 | **4** | 8/12 = 66.7% | 6/8 |

Four weakening mutants of the **pinned** instrument still score the real landed block 23
`met_target: true` with `battery 9/9/0/1/0` (`receipts/real-m*.json`). Of the eight required
mutations, **three survive at the named freeze** (`m3`, `m4`, `m7`) and **two survive at the
pinned bytes** (`m4`, `m7`) — and those two keep the battery green while scoring the landed
block green, so this is not only a selftest gap but a scoring gap.

---

## 0. Which bytes are "the frozen instrument" — a finding before the campaign

The seat names freeze `31820472784284727546808acc31b3ea1e73919b`. The bytes that block 23 pins
and that the lane scores are **not** those bytes. Two later commits rewrote the frozen
directory; the lane's own commit messages say so ("the first freeze commit did not carry the
final bytes", `50862e4a`; "the freeze is the instrument that can actually be scored",
`65678df0`).

| ref | `tools/round-46/attest.py` blob | sha256 | selftest cases |
|---|---|---|---|
| `31820472` (freeze named by this seat) | `25883520b425…` | `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb` | 15 |
| `50862e4a` | `2f3d595c45efee9ecea8374b2af26d3d0a083549` | `eba599582bb32eab3c47d7c15cbd53852e257070ae756136e3cee059e37311fd` | 15 |
| `65678df0`, `0425224`, HEAD | `936910fe60b2…` | `e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346` | 16 |

`attest.py` has been byte-identical since `65678df0`, so byte-set B is both "the F3 repair" and
"the current pinned instrument". `gate.py` differs too: A `d7cd9aac…` /
`sha256:64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e`, B `9ab7e2a3…` /
`sha256:847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223`.

The freeze arm says the same thing from the other side (all runs read-only, `--no-battery`):

| command (root = lane) | exit | value |
|---|---|---|
| `attest.py --freeze 31820472 --rev 0425224` | **2** | `frozen_path_changed: ['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']` |
| `attest.py --freeze 65678df0 --rev 0425224` | **2** | `frozen_path_changed: ['tools/round-46/', 'tools/round-46/registry.py']` |
| `attest.py --freeze 0425224 --rev 0425224` | **0** | `met_target: true`, `rule_blocks 23`, `rows 13`, `refs 9`, `battery 9/9/0/1/0` |
| `attest.py --freeze 31820472 --rev 31820472` | **1** | `rule_blocks 22`, `marker_occurrences 0`, `block_present 0` (the claims' do-nothing control) |

Receipts: `receipts/rev-0425224-frozen-freeze.json`, `rev-F4-freeze-65678df.json`,
`c1-battery-F4.json`, `ctl-freeze-only-frozen-attest.json`. So under either declared freeze the
claimed revision is inadmissible by the claims' own rule, and only `freeze == rev == 0425224`
scores. I report this; I do not adjudicate it (freeze-manifest seats own that question) — but it
decides which bytes a mutation campaign can call "the instrument", so both are attacked below.

---

## 1. Method

Each mutant is **one** semantic change to **one** check, applied to a copy of the byte-set:

```
cp <byteset>/{attest.py,gate.py} $S/mutants/<ver>-<id>/
python3 -  # exactly-one-occurrence anchor assertion, then replace
cd $S/mutants/<ver>-<id> && TMPDIR=<dir>/tmp HYAKU_SCRATCH=<dir>/scr \
  python3 -I -B attest.py --root /nonexistent --freeze deadbeef --rev deadbeef --selftest
```

`--root/--freeze/--rev` are required by argparse even for `--selftest` (see F4); `--selftest`
returns before `--root` is read, so the values are inert. Every anchor occurred exactly once
(`text.count(old) == 1`, asserted); each diff is a single hunk
(`receipts/mutants/<ver>-<id>.diff`).

A mutant is **killed** when a case green in the baseline goes red; **survived** when every case
stays green. For survivors the campaign goes one step further: a crafted artefact that the
pristine instrument rejects (`exit 1`) is re-scored with the mutant, and it must accept it
(`exit 0`) — otherwise the mutant is a no-op, not a hole.

Baselines (`receipts/baseline-*.out/.exit/.utc`):

| byte-set | exit | stdout first line | stdout sha256 | UTC |
|---|---|---|---|---|
| A | 0 | `ATTEST_SELFTEST: cases=15 failures=0` | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T17:04:25Z |
| B | 0 | `ATTEST_SELFTEST: cases=16 failures=0` | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 2026-10-28T17:04:25Z |

Both baselines are green, so no verdict below is a baseline failure.

---

## 2. The matrix

Full command/exit/sha256/UTC per run: `receipts/mutation-matrix.md`. `flipped` names the case
that went red relative to that byte-set's baseline.

| # | mutation (one change) | byte-set | exit | flipped | verdict |
|---|---|---|---|---|---|
| m1 | `marker_occurrences != 1` → `< 1` | A | 1 | `red-two-markers` | **KILLED** |
| m1 | same | B | 1 | `red-two-markers`, `green-with-battery` | **KILLED** (double cover) |
| m2 | drop the is-last-craft-block check | A | 1 | `red-marker-not-last` | **KILLED** |
| m2 | same | B | 1 | `red-marker-not-last` | **KILLED** |
| m3 | header cells matched by prefix, not equality | A | 0 | — (stdout byte-identical) | **SURVIVED** |
| m3 | same | B | 1 | `green-with-battery` only | KILLED, but by the battery, not its own case |
| m4 | r46 `min_rows` 13 → 8 | A | 0 | — | **SURVIVED** |
| m4 | same | B | 0 | — | **SURVIVED** |
| m5 | drop the exit-cell membership check | A | 1 | `red-exit-cell` | **KILLED** |
| m5 | same | B | 1 | `red-exit-cell` | **KILLED** |
| m6 | drop the routed-id check | A | 1 | `red-routed-id-missing` (and `red-rows-thin` loses one reason) | **KILLED** |
| m6 | same | B | 1 | `red-routed-id-missing` | **KILLED** |
| m7 | vocabulary matched by substring over the whole row | A | 0 | — | **SURVIVED** |
| m7 | same | B | 0 | — | **SURVIVED** |
| m8 | pin compared by length only | A | 1 | `red-pin-mismatch` | **KILLED** |
| m8 | same | B | 1 | `red-pin-mismatch`, `green-with-battery` | **KILLED** (double cover) |
| m9 | drop the citation allowlist | A | 0 | — (stdout byte-identical) | **SURVIVED** |
| m9 | same | B | 0 | — (stdout byte-identical) | **SURVIVED** |
| m10 | drop the `refs >= 6` floor | A | 0 | — (stdout byte-identical) | **SURVIVED** |
| m10 | same | B | 0 | — (stdout byte-identical) | **SURVIVED** |
| m11 | hard profile stops requiring a line selector | A | 0 | — | **SURVIVED** |
| m11 | same | B | 1 | `green-with-battery` only | KILLED, but by the battery |
| m12 | `must_cite_refs` no longer enforced | A | 0 | — (stdout byte-identical) | **SURVIVED** |
| m12 | same | B | 1 | `green-with-battery` only | KILLED, but by the battery |

"stdout byte-identical" means the mutant's entire `--selftest` output hashes to the baseline
`sha256` — the selftest cannot even see the change, which is a stronger statement than
"no case flipped".

---

## 3. Killed mutants — and whether the catching case is isolated

| mutant | catching case | isolated? |
|---|---|---|
| m1 | `red-two-markers` | **yes** — baseline failing is exactly `['marker_occurrences 2 != 1']`, and that reason disappears under m1 |
| m2 | `red-marker-not-last` | **yes** — single reason |
| m5 | `red-exit-cell` | **yes** — single reason |
| m6 | `red-routed-id-missing` | **yes** — single reason (the case red no longer isolates it: m6 also removes one of its two reasons, but the dedicated case is clean) |
| m8 | `red-pin-mismatch` | **yes** — single reason; B adds the battery as a second detent |
| m3 (B only) | `green-with-battery` | **no** — its own case `red-header-inexact` stays red because it mutates `v2 arm` → `arm` (truncation); prefix matching still rejects truncation. Only the *extension* direction (`v2 arm code`) is the hole, and no discrete case tests it |
| m11 (B only) | `green-with-battery` | **no** — see §4.2 |
| m12 (B only) | `green-with-battery` | **no** — no discrete case exists for `must_cite_refs` at all |

---

## 4. Survivors — the case that SHOULD have caught each, with the artefact it misses

### 4.1 m4 — the row floor is not isolated (A and B)

Baseline `red-rows-thin` fails for **two** reasons at once:
`['rows 12 < 13', "routed ids not named by any row: ['R45-CL24']"]` — it builds 12 rows by
slicing `GOOD_ROWS[:12]`, which also drops `R45-CL24`. Under m4 the first reason vanishes
(`['routed ids not named by any row: …']`) and the case is still red, so the selftest never
notices the floor moved. The battery cannot see it either: its own `thin-rows` forgery deletes
rows 8–12, so it also loses `R45-CL19..CL24` (`receipts/c1-battery-F4.json` → `thin-rows`
failing `['rows 8 < 13', "routed ids … ['R45-CL19','R45-CL20','R45-CL22','R45-CL23','R45-CL24']"]`).

Exploit (`probe = p-g4-rows8-all-ids`: 8 rows, two routed ids per trigger cell, all 13 ids
named, valid header/vocab/exit/refs/pin):

| instrument | exit | failing |
|---|---|---|
| pristine A | 1 | `['rows 8 < 13']` |
| `A + m4` | **0** | `[]` |
| pristine B | 1 | `['rows 8 < 13']` |
| `B + m4` | **0** | `[]` |

The case is real though: with `min_rows 8`, the landed block 23 still scores
`met_target: true` (`receipts/real-m4-rows-floor-8.json`), so an 8-row artefact is accepted.
**Repair:** make `red-rows-thin` 12 rows that still name all 13 ids (put two ids in a trigger
cell), so the floor is the only failure; and make the battery's `thin-rows` forgery drop rows
without dropping ids.

### 4.2 m7 — the arm check is a substring test, and the case is 5/13 isolated (A and B)

The pristine check is already loose: `not any(t in r[arm_col].lower() for t in ARMS)` is a
substring test, so an arm cell that *contains* a token without naming it passes. Probe
`p-arm-substring` (every arm cell = `unpinned`, i.e. `pin` embedded):

| instrument | exit | failing |
|---|---|---|
| pristine A | **0** | `[]` |
| pristine B | **0** | `[]` |

That is clause 4 (`every arm cell is in the vocabulary`) false while the counter prints met — a
defect of the frozen instrument itself, not of a mutant. Under m7 (whole-row substring) the
hole widens, and `red-arm-vocabulary` cannot see it: its 13 rows have arm cells `zzz` but 5 of
their other cells contain real tokens (`merge-introduced`, `dirty`, `pathspec`, `restored`, …),
so the mutant's count drops 13 → 8 and stays non-zero.

Exploit (`p-g7-vocab-wrong-column`: all 13 arm cells `zzz`, hole cells say
`merge-introduced edit described here`):

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `['arm cells outside the vocabulary: 13']` |
| `A + m7`, `B + m7` | **0** | `[]` |

`B + m7` still scores the landed block `met_target: true` (`receipts/real-m7-vocab-whole-row.json`).
**Repair:** match the arm cell after splitting on whitespace/`/`, by equality; and make the case's
non-arm cells token-free, or assert the exact count `13`.

### 4.3 m9 — the allowlist case never tests the allowlist (A and B)

`red-ref-outside-allowlist` swaps in `corpus/QUALITY.md:3`, but the selftest fixture never writes
`corpus/QUALITY.md`, so under m9 the rejection changes *reason* rather than disappearing:

| instrument / probe | exit | unresolved citations |
|---|---|---|
| `iso-ref-allow`, pristine B | 1 | `['corpus/QUALITY.md: outside the validated path set']` |
| `iso-ref-allow`, `B + m9` | 1 | `['corpus/QUALITY.md: absent at rev']` |

Identical failing count (1) → the case is byte-for-byte green as a red case. With the file
present (`p-g9-outside-allow`), the mutant is exposed:

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `['unresolved or unvalidated citations: 1']` (`outside the validated path set`) |
| `A + m9`, `B + m9` | **0** | `[]` (`refs` 7 → 8: the outside path is counted) |

`B + m9` scores the landed block green (`receipts/real-m9-drop-allowlist.json`).
**Repair:** create the outside-allow path in the fixture so only the allowlist can reject it.

### 4.4 m10 — no case covers `refs_min` at all (A and B)

Every case uses the 6-ref `GOOD_REFS`, so the floor `refs >= 6` is never exercised; the mutant's
stdout is byte-identical to the baseline on both byte-sets. Exploit `p-g10-refs3` (4 refs, all
resolving, one of them `corpus/lessons/round-45.md:12-30`; the fourth is the pin citation in the
block body):

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `['refs 4 < 6']` |
| `A + m10`, `B + m10` | **0** | `[]` |

`B + m10` scores the landed block green (`receipts/real-m10-drop-refs-min.json`).
**Repair:** add a case with 3–5 resolving, line-selected refs that still cite
`corpus/lessons/round-45.md`.

### 4.5 m11 — the selector case is red for an accidental reason (A survives; B battery-only)

`red-ref-no-selector` builds its refs with `.replace(":12-30","").replace(":20","")`. The second
replace also eats the `:20` inside `:200-210`, producing the phantom path
`corpus/lessons/round-45.md0-210`. Baseline has three bad refs, not two:

```
pristine A/B, probe iso-ref-selector → unresolved_citations:
  ['corpus/lessons/round-45.md: no line selector',
   'plans/round-46-claims.md: no line selector',
   'corpus/lessons/round-45.md0-210: no line selector']
```

Under m11 two reasons disappear and the phantom remains → the case stays red and the whole
15-case build is blind to the change (stdout differs only in the `red-ref-no-selector` row).
Exploit `p-g11-no-selector` (6 resolving refs, selectors stripped with one regex):

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `['unresolved or unvalidated citations: 6']` |
| `A + m11` | **0** | `[]` ← survives A |
| `B + m11` | **0** | `[]` ← selftest blind, battery catches it |

**Repair:** strip selectors with `re.sub(r":\d+(?:-\d+)?", "", GOOD_REFS)`, so the case fails on
the selector clause alone.

### 4.6 m3 — the header case tests truncation, the hole is extension (A survives; B battery-only)

`red-header-inexact` uses `| trigger | v1 hole | arm | exit |`. Under prefix matching the
*header* cell must start with the *spec* cell, so a shorter cell still fails — the case cannot
see the mutant. The hole is a cell that extends a spec cell. Exploit `p-h3-header-prefix`
(`v2 arm` → `v2 arm code`):

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `["header ['trigger','v1 hole','v2 arm code','exit'] != ['trigger','v1 hole','v2 arm','exit']"]` |
| `A + m3` | **0** | `[]` ← survives A |
| `B + m3` | **0** | `[]` ← selftest blind; battery's `header-substring` forgery (which appends `code`) kills it |

**Repair:** the case should extend a cell (`v2 arm code` or `exit-code`), which is exactly the
battery's forgery, so the discrete case carries the clause and the battery duplicates it.

### 4.7 m12 — `must_cite_refs` has no discrete case (A survives; B battery-only)

No case removes `corpus/lessons/round-45.md` from the citation set; the mutant's `--selftest`
stdout is byte-identical to the baseline at A. Exploit `p-g12-no-round45` (6 resolving claims
refs, none in `corpus/lessons/`):

| instrument | exit | failing |
|---|---|---|
| pristine A / B | 1 | `['does not cite corpus/lessons/round-45.md']` |
| `A + m12` | **0** | `[]` ← survives A |
| `B + m12` | **0** | `[]` ← selftest blind, battery's `self-refs` forgery kills it |

**Repair:** add the discrete case; do not rely on the battery for a clause the claim states
separately.

---

## 5. Findings against the frozen instrument itself (reported, not fixed)

### F2 — at `31820472` the battery cannot run, and its failure path reports 1, not 2

`m_self_refs` calls `REF.search(...)` (line 322) and `REF` is defined nowhere in the file
(`grep -n '^REF' tools/round-46/attest.py` → no match; only `HARD_REF`/`LOOSE_REF`). Running the
byte-set-A instrument on a genuine artefact with the battery enabled:

```
$ python3 -I -B base/attest.py --root <fixture> --freeze <rev> --rev <rev>
EXIT: 1
STDOUT: {"reason": "unhandled NameError: name 'REF' is not defined"}
STDERR: … File "base/attest.py", line 476, in main
          code, receipt = gate.main_guard(
        TypeError: cannot unpack non-iterable int object
```

(receipt `receipts/frozen-battery-raw.txt`, sha256 `a51e6ae2029e9f07…`, UTC 2026-10-28T17:10:28Z).
Chain: the battery raises → A's `gate.main_guard` catches, prints the reason JSON and returns an
**int** → `main` unpacks → `TypeError` → interpreter exit **1**. So at the declared freeze the C1
counter (a) cannot complete one battery run and (b) turns a could-not-evaluate into exit 1, the
exact `R45-CL13` (f) class the claims say is closed. Byte-set B fixes both (`main_guard` returns
a tuple; a `green-with-battery` case exists) and B's battery is green on a genuine artefact:
exit 0, `failing []`, and on the real block `forgeries_total 9 / v1_green 9 / v2_green 0 /
genuine_green 1 / v2_crash 0` (`receipts/c1-battery-F4.json`). Consequence for wave 1: the
15-case build's green selftest is **not** evidence that its battery works — the selftest at A has
no battery case at all, and four mutants (m3, m9, m10, m12) produce byte-identical output.

### F3 — clause 4's vocabulary test is a substring test

See §4.2: arm cells `unpinned` (contains `pin`) score green on both byte-sets
(`p-arm-substring`, exit 0, `failing []`). The claim says "names a token from the fixed
vocabulary"; containment is not naming. `rows`/`narrows`, `refs`/`prefs`, `pin`/`spinner` are
all open.

### F4 — the claims' preflight command, as written, exits 2

`plans/round-46-claims.md` says "`attest.py --selftest` prints `cases=15 failures=0`". Literally:

```
$ python3 -I -B tools/round-46/attest.py --selftest
attest.py: error: the following arguments are required: --root, --freeze, --rev
exit 2
```

Same exit 2 for both byte-sets (`receipts/bare-selftest-{base,head}.out`, sha256
`3ed94b41f2837c05…`). The landed registry row for `tools/round-46/attest.py` already states the
correct command (`--selftest --root . --freeze HEAD --rev HEAD …`) and "15 cases at the 3182047
and 50862e4a bytes, 16 from the F3 repair at 65678df0 onward". I verified that row's numbers from
git objects and they are exactly right (§0 table). Only the claims file's sentence is
under-specified; the registry row needs no change.

### F5 — informational, cross-seat: the freeze arm under either declared freeze

See §0. `freeze 31820472 → rev 0425224` and `freeze 65678df0 → rev 0425224` both exit 2
`frozen_path_changed`; only `freeze == rev == 0425224` scores. If the L1 keeps `31820472` as the
freeze, the C1/C2 counting commands as written cannot produce a verdict anywhere past it.

---

## 6. What this changes for the landing (C1 rule block 23 / registry)

Rule block 23 itself is green at `freeze == rev == 0425224` and its battery discriminates the
nine defect classes it enumerates (9 forgeries red under v2, green under v1; genuine green).
That is measured, not inferred (`receipts/c1-battery-F4.json`).

The selftest is the weaker of the two instruments, and the claim's preflight sentence leans on
it. Concretely, for the L1:

1. **Three of the eight required mutations survive at the named freeze (`m3`, `m4`, `m7`); four
   of twelve survive at the pinned bytes (`m4`, `m7`, `m9`, `m10`), and all four still score the
   landed artefact `met_target: true`.** The
   selftest is arm-covering but not clause-pinning: two clauses (`refs_min`, `must_cite_refs`)
   have no discrete case at all, two cases are non-isolated (`red-rows-thin`,
   `red-ref-outside-allowlist`), one case is red for a typo artifact (`red-ref-no-selector`), and
   one tests the wrong direction (`red-header-inexact`).
2. **The battery, not the discrete cases, is what kills m3/m11/m12 at B.** Any repair that drops
   the `green-with-battery` case re-opens three clauses silently.
3. **Clause 4's substring vocabulary is a live hole in the frozen check** (F3), independent of
   any mutant; a repaired check should split-and-equate, and the repair should be scored against
   the existing block 23 before landing (it stays green: every landed arm cell is a bare token).
4. **The claims' preflight command needs its three flags** (F4); the landed registry row is
   already correct and its case-count history verified.

Suggested case additions, each of which kills exactly one survivor (all six verified as
pristine-red / mutant-green above): isolated 12-row floor case; token-free arm cells with an
exact count; outside-allow path present in the fixture; a 4-ref floor case; one-regex selector
strip; a no-`round-45.md` citation case.

---

## 7. Not run, and limits

- **`registry.py`** and the C2 battery: not mutated (another seat's lane).
- **`--profile v1` fidelity** (`--spec r45`, `--fidelity` at `f59565b7`/`f762b727`): not run.
  My m1/m8/m3 fixtures do exercise the v1 arm indirectly through the battery's `v1_exit` column,
  but I did not reproduce the round-45 receipt.
- **`gate.py`**: not mutated as a unit; it is exercised only through both `attest.py` byte-sets
  and the freeze-arm receipt above.
- **`--json-out` refusal, scratch-root refusal** (`R45-CL20`/`R45-CL22` arms): not mutated here;
  the frozen selftest has `red-frozen-touched-is-exit-2` and no case for either, which I did not
  test. Say "not run", not "passed".
- Every `--selftest` run used `--root /nonexistent`; the selftest returns before `evaluate`, so
  the lane repo is never read by those runs. Fixture repos for probes are one-commit repos under
  `HYAKU_SCRATCH`, each asserted to be its own toplevel.
- Installs: none. No mutating git outside scratch fixtures; scratch removed after the receipts
  were copied.
