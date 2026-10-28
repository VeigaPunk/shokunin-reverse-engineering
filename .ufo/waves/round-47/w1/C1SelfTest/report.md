# C1SelfTest — audit of `tools/round-47/exact.py --selftest` (R47-C1, depth)

Scope: the frozen C1 counter `tools/round-47/exact.py` (561 lines, sha256
`dcef54f1b14326c3b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` at
`5017e1f7299c3a812e87e7950148f54313dd279e`) and its `--selftest` mode only. No frozen byte
was modified in the lane; every mutation below is a copy under
`/fast/scratch/hyaku/kaidoku-r47/C1SelfTest` (removed before yield; the drivers and their
outputs are retained in `receipts/` next to this file).

This file is duplicated at `.ufo/waves/round-47/w1/C1SelfTest/report.md` — the seat spec and
the `Report:` trailer named two paths; the bytes are identical.

## 0. Verdict

| question | measured |
|---|---|
| banner | `EXACT_SELFTEST: cases=16 failures=0`, exit 0 |
| registered cases | **16** = 15 `run(...)` calls (L500–L528) + 1 `cases.append(...)` (L550). There is no `case(` helper in the file (0 matches). Banner count == registered count. |
| every case honest? | **no** — one case name is false (`red-battery-green-forgery`), and 10 of the 15 real cases name a clause they do not isolate |
| clause coverage | **21 clauses deleted one at a time; 11 deletions leave the selftest green** (`cases=16 failures=0`) |
| are those 11 dead code? | **no** — 9 of them are live, exclusively-responsible guards (frozen counter returns 1 on an artefact whose *only* defect that clause names, 0 with the clause deleted). They are real guards with **zero** registered coverage. 1 is provably redundant, 1 is an unobservable message branch |
| frozen claim vs frozen counter | **two divergences**: clause 8's citation floor is under-enforced by one (a block with **two** line-selected citations scores clean), and clause 6's "names all four mutations" is a substring containment — R46-CL2's own defect class |

Net: C1's *artefact* predicate is sound enough to fail a real block (the do-nothing control
reproduces; see §1), but the **selftest is not evidence of that** — it would stay green under
11 of 21 single-clause deletions. The selftest is a unit test of `score()`; it is not a
coverage proof, and it cannot see the landed `SKILL.md` at all (§1.3).

## 1. Receipts

### 1.1 The commanded run (verbatim, menu command)

```sh
HYAKU_SCRATCH=$S python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py \
  --selftest --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 5017e1f7299c3a812e87e7950148f54313dd279e --rev 5017e1f7299c3a812e87e7950148f54313dd279e
```

| field | value |
|---|---|
| exit | **0** |
| stdout line 1 | `EXACT_SELFTEST: cases=16 failures=0` |
| stdout sha256 | `0249b80f58085f0d52cca3f7ae3f731d88d38dd4daaca6f84cefa023e3028aaa` |
| stderr | empty (0 bytes) |
| UTC | `2026-10-28T17:55:07Z` |
| retained | `receipts/selftest-frozen.out`, `receipts/selftest-frozen.err` |

### 1.2 The counter on the real tree (do-nothing control, reproduced)

`receipts/real-freeze-v3.out` (sha256 `88fafc60…`), `--freeze`=`--rev`=`5017e1f…`, v3:

```
EXIT=1   rule_blocks 23  marker_occurrences 0  block_present 0  touched 0  frozen_path_changed []
failing: ["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]
```

`receipts/real-freeze-v2.out` (sha256 `9c3f51b7…`), `--profile v2`: exit 1,
`failing: ["marker_block_count 0"]`, `battery: skipped (artefact fails a structural clause
first)`, `frozen_derived: ["tools/round-47/", "plans/round-47-claims.md"]`,
`frozen_path_changed: []`.

This matches the claims file's `ctl-c1-0-do-nothing` before-state exactly (block_present 0,
rule_blocks 23, marker_occurrences 0), and confirms the frozen paths are clean at the freeze.
It also confirms `battery.forgeries_total == 4` is unreachable before the landing (the battery
is never built: `cannot build a battery: marker blocks 0`), as `ctl-c1-2` claims.

### 1.3 What `--selftest` does **not** measure

`main()` returns `selftest()` before `gate.out_path` and before `evaluate`
(`exact.py:423-425`). So `--selftest`:

- never reads `SKILL.md`, `plans/round-47-claims.md` or `tools/round-46/gate.py` at
  `--rev` — `--root`, `--freeze` and `--rev` are parsed and **discarded**;
- never runs `gate.freeze_state`, so it cannot report `frozen_path_changed`;
- builds its fixtures from the *running file's own* `open(__file__)` bytes, so a copy of the
  counter passes its own selftest regardless of what the lane's `exact.py` contains.

Consequence for the L1: a green `EXACT_SELFTEST` is not evidence about the landed block 24 or
about the freeze. Only §1.2's counting command, on the landing revision, is.

## 2. Deletion matrix (one clause at a time)

Driver: `receipts/deletion_matrix.py` (sha256 `92042198484a582c…`), exit 0, UTC
`2026-10-28T17:54:26Z`–`17:54:34Z`; full data `receipts/deletion-matrix.json`, stdout
`receipts/deletion-matrix.out` (sha256 `1c3d244a43ae865b…`). Each row: copy `exact.py` into a
mirrored tree, delete exactly that clause, run the copy's own `--selftest`.

Note: for `C5-arm-exact` and `Z-malformed-branch` a bare line-deletion leaves an empty
`if hard:` and the copy dies with `IndentationError` (exit 1, no stdout) — that is a driver
artefact, not a verdict, so the clause body is replaced with `pass` in those two rows. My first
attempt did the bare deletion and produced exactly that; the retained matrix is the corrected
one.

| clause | what it deletes | exit | banner | cases that fail | stdout sha256 | UTC |
|---|---|---|---|---|---|---|
| `C1-marker-occurrences` | `marker_occurrences != 1` | 1 | `cases=16 failures=1` | `red-two-markers` | `5a96d6b3b150…` | 17:54:26Z |
| `C1-block-is-last` | marked block is the last craft block | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:27Z |
| `C1-title-24` | title starts with `24. ` | 1 | `cases=16 failures=1` | `red-title-unnumbered` | `024e95981dab…` | 17:54:27Z |
| `C2-header-exact` | `header == HEADER` (v3 equality) | 1 | `cases=16 failures=1` | `red-header-inexact` | `c80451db21f3…` | 17:54:28Z |
| `C3-rows-four` | `rows != 4` | 0 | `cases=16 failures=0` | **NONE** | `7248914b1163…` | 17:54:28Z |
| `C3-four-cells` | every row exactly 4 cells | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:28Z |
| `C3-exit-set` | exit cell in `{0,1,2}` | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:29Z |
| `C4-one-id-per-row` | each row names exactly one routed id | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:29Z |
| `C4-cardinality` | routed ids exactly once each | 1 | `cases=16 failures=1` | `red-duplicate-routed-id` | `3ac402dd7c20…` | 17:54:29Z |
| `C5-arm-exact` | arm cell is an exact vocabulary token | 1 | `cases=16 failures=3` | `red-arm-substring`, `red-battery-green-forgery`, `battery-discriminates` | `2b55ed6db7b0…` | 17:54:30Z |
| `C6-mutations-digest` | `mutations_sha256 == MUT_DIGEST` | 1 | `cases=16 failures=2` | `red-digest-stale`, `battery-discriminates` | `411e426986ab…` | 17:54:30Z |
| `C6-mutation-names` | block states all four mutation names | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:31Z |
| `C7-flag-order` | gate.py flag-order clause | 1 | `cases=16 failures=2` | `red-flag-order-swapped`, `battery-discriminates` | `c9219a85873b…` | 17:54:31Z |
| `C8-refs-floor` | `refs >= 3` | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:31Z |
| `C8-bad-refs` | unresolved/unvalidated citations fail | 1 | `cases=16 failures=2` | `red-ref-no-selector`, `red-ref-outside-allowlist` | `a4c5865e9760…` | 17:54:32Z |
| `C8-must-cite` | `corpus/lessons/round-46.md` cited | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:32Z |
| `C8-interpreter-pin` | `interpreter_sha256` matches bytes at rev | 1 | `cases=16 failures=1` | `red-pin-mismatch` | `af276c25d524…` | 17:54:32Z |
| `C8-line-selector` | non-self reference carries a selector | 1 | `cases=16 failures=1` | `red-ref-no-selector` | `c8307291056d…` | 17:54:33Z |
| `C8-allowlist` | reference path inside `ALLOW` | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:33Z |
| `C9-battery-counts` | the five `battery.*` expectations | 0 | `cases=16 failures=0` | **NONE** | `0249b80f5808…` | 17:54:33Z |
| `Z-malformed-branch` | "heading lacks its trailing space" raise | 0 | `cases=16 failures=0` | **NONE** | `5460bfb8bdae…` | 17:54:34Z |

Row set that is byte-identical to the frozen green selftest output (stdout sha
`0249b80f5808…`): 8 of the 11 unnoticed deletions print **exactly the frozen run's stdout** —
the strongest form of "no case notices".

Deleted clause named in the assignment: `C5-arm-exact` — the v3 arm equality
(`if any(a not in VOCAB for a in arm)`), i.e. the clause that closes R46-CL2. Its deletion
turns the selftest red with `failures=3` and the case that names it (`red-arm-substring`)
fails. That clause is honestly covered (three times over).

## 3. The 11 unnoticed deletions: live, redundant, or dead?

Driver: `receipts/liveness_probes.py` (sha256 `fb47986a1c8af1fb…`, equal to the
`driver_sha256` recorded inside the JSON), exit 0, stdout sha256 `18f81ca9c94a9431…`,
UTC `2026-10-28T17:54:48Z`; data `receipts/liveness-probes.json`. Method: build one artefact
whose **only** defect is the one that clause names, score it with the frozen `score()` at v3,
then score the identical artefact with the clause deleted. `frozen=1 / deleted=0` ⇒ the clause
is a live, exclusively-responsible guard.

| clause | artefact whose only defect is | frozen | with clause deleted | verdict |
|---|---|---|---|---|
| `C1-block-is-last` | a second craft block after the marked one | 1 `marker block is not the last craft block` | 0 | **LIVE, uncovered** |
| `C3-four-cells` | a five-cell row with a valid exit cell | 1 `a row does not have exactly 4 cells` | 0 | **LIVE, uncovered** |
| `C3-exit-set` | exit cell `3` | 1 `exit cells outside {0,1,2}: 1` | 0 | **LIVE, uncovered** |
| `C4-one-id-per-row` | one row names two ids, one names none | 1 `rows naming != 1 routed id: [0, 3]` | 0 | **LIVE, uncovered** |
| `C6-mutation-names` | block drops the name `flag-order-drift` | 1 `mutation names not stated: ['flag-order-drift']` | 0 | **LIVE, uncovered** |
| `C8-refs-floor` | one line-selected citation only | 1 `refs 2 < 3` | 0 | **LIVE, uncovered** |
| `C8-must-cite` | three resolving refs, none of them round-46.md | 1 `does not cite corpus/lessons/round-46.md` | 0 | **LIVE, uncovered** |
| `C8-allowlist` | a resolving ref outside `ALLOW` (`tools/round-46/gate.py:1`) | 1 `unresolved or unvalidated citations: 1` | 0 | **LIVE, uncovered** |
| `C9-battery-counts` | `battery.forgeries_total=3` | 1 `battery forgeries_total 3 != 4` | 0 | **LIVE, uncovered** |
| `C3-rows-four` | — | 5 rows → 1; 3 rows → 1 | both still 1 via cardinality | **redundant by construction** |
| `Z-malformed-branch` | craft heading without trailing space now reports "no section" | exit still 2 | — | **unobservable message** |

Two of these deserve the L1's attention:

- **`C3-rows-four` is redundancy, not a gap.** In v3, `one-id-per-row` (each row contributes
  exactly one id) plus `cardinality` (four distinct ids, each once) *imply* `rows == 4`, so no
  artefact can be caught by `rows != 4` alone. Measured: 5 rows → `rows 5 != 4` **and**
  cardinality; 3 rows → `rows 3 != 4` **and** cardinality. Deletion-neutral by proof, safe.
- **`Z-malformed-branch`**: `red-malformed-heading-is-exit-2` only asserts exit 2. With the
  trailing-space raise deleted, that heading still exits 2 through the *other* Malformed
  branch, so the case cannot distinguish "heading lacks its trailing space" from "no craft
  section". There is also **no case at all** for a `SKILL.md` with no craft section (measured:
  exit 2, `reason: no '## Queue-drain craft ' section`). Both are exit-2 branches; both are
  live; neither is covered.

## 4. A case whose name is false

`red-battery-green-forgery` (L527) is **byte-identical in effect to `red-arm-substring`**
(L511): same `skill_text(good_block(rows=[... "order-ish" ...]))`, same default
`profile="v3"`, no overrides — and `run()` hard-codes `battery=None` (L490), so the case
*cannot* reach any battery clause.

Evidence:
- the two cases' receipts are identical: `failing == ['arm cells not exact vocabulary tokens:
  ['order-ish', 'order-ish', 'order-ish', 'order-ish']']` for both (from
  `receipts/selftest-frozen.out`);
- deleting `C5-arm-exact` flips **both** together (`failures=3`);
- deleting `C9-battery-counts` — the clause the name claims — flips **neither** (still
  `failures=0`).

So the selftest registers 16 cases but only 15 distinct ones, and the name that claims the
"v2 stays green on a forgery" property tests something else. The v2 arms *are* exercised
indirectly by `battery-discriminates` (v2_green 4 / v3_green 0 measured on four fixtures), but
no case scores a forgery under `--profile v2` directly, and there is no case at all that
supplies a wrong `battery` dict from the outside.

## 5. Findings against the frozen claim (most valuable for the L1)

### F3 — clause 8's citation floor is under-enforced by one (actionable at landing)

The claim requires "at least three citations **carry a line selector**" and, in predicate 8,
"`refs >= 3`, **every** reference carries a line selector". The counter exempts the self
reference from the selector requirement (`check_refs`: `if name == SELF: continue`) but still
counts it in `refs = len(HARD_REF.findall(block))`. Measured:

```
refs = "`corpus/lessons/round-46.md:10-30`, `corpus/lessons/round-46.md:40-60`"   (2 selected)
+ the block's own `tools/round-47/exact.py` token (no selector)
→ exit 0, CLEAN, refs=3, cited={corpus/lessons/round-46.md, tools/round-47/exact.py}
```

One selected citation → exit 1 (`refs 2 < 3`). So the **measured** floor is two line-selected
citations, not three. A landing block with two selected citations and the interpreter token
scores 0 while the claim's prose says it should not.

Action for the L1 (no frozen byte to change): land block 24 with **≥3 line-selected
citations** (as intended), and record that the counter cannot distinguish 2 from 3 — otherwise
the round's own landing evidence is weaker than the claim it cites. Also note the corollary
for the drafter: `tools/round-46/gate.py` **cannot** be cited with a line selector (only
`corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-47/` are in `ALLOW`), even
though clause 7 reads that file.

### F4 — clause 6's name check is a containment test (R46-CL2's class, inside the v3 matrix)

`unnamed = [n for n in names if n not in block]` is a substring test over the whole block.
Measured: a block whose mutation names appear only as loose words in an unstructured aside
(`(aside, no structure: substring-arm / duplicate-routed-id / stale-mutations-digest /
flag-order-drift)`) scores **exit 0, CLEAN**. The names sentence is thus satisfiable by
prose, not by a structured list — the same shape as R46-CL2 (`blobberish` satisfies `blob`)
and R46-CL3 (an id in *some* row).

Severity is bounded, not fatal: the digest pin (`mutations_sha256 == MUT_DIGEST`, covered by
`red-digest-stale` + `battery-discriminates`) is the real binding, and the interpreter pin
makes editing `MUTATIONS` self-defeating. But the claims file presents clause 6 as the fix
for R46-CL4's "no digest"; the *names* half of that clause is still a containment test, so
the landing report should not describe block 24 as closing the substring class everywhere.

### F5 — calibration note: 10 of 15 real cases do not isolate the clause they name

`red-rows-not-four` is caught by cardinality, not `rows != 4`. `red-marker-missing` is caught
by both `occurrences != 1` and `marked != 1`. `red-ref-no-selector` and
`red-ref-outside-allowlist` are both caught by the aggregate `bad_refs` append, so the
*specific* message ("no line selector", "outside the validated path set") has no case that
asserts it. None of these is a false green; they are weaker cases than their names imply.
The honest claim for the L1 is "16 cases, 21 clauses, 10 clauses with a case that flips on
deletion", not "every clause is covered".

## 6. Landing guidance (derived, not executed — landing is the L1's move)

Block 24 must satisfy, on the measured floor: marker once, title `24. `, last craft block,
exact header, 4 rows × 4 cells, exits in `{0,1,2}`, one routed id per row and each of the four
exactly once, arm cells exactly one of `symbol|once|digest|order`, `mutations_sha256` =
`sha256("\n".join(["substring-arm","duplicate-routed-id","stale-mutations-digest",
"flag-order-drift"]))`, `interpreter_sha256` = sha256 of `tools/round-47/exact.py` at the
measured rev, `gate.py` containing `"-m", "--diff-merges=first-parent"` exactly once and the
reversed pair zero times, ≥3 citations of which **at least 3 must carry selectors by the
drafter's own discipline** (F3), and `corpus/lessons/round-46.md` cited with a selector.
Do not cite `tools/round-46/gate.py` (outside `ALLOW`).

## 7. Limits

- Not run: the battery on a landed block (`battery.forgeries_total == 4` is unreachable before
  landing; §1.2 shows it is skipped). So the four forgery fixtures were exercised only through
  the selftest's own `battery-discriminates` case and my clause deletions — never against the
  real `SKILL.md`.
- Not run: `--profile v2` against a landed block. v2 at the freeze returns 1
  (`marker_block_count 0`), so the claim's `ctl-c1-1-v2-profile` control is only reachable
  after landing, as the claims file itself says.
- The liveness probes call `score()` in-process rather than through `main()`, so they carry no
  `freeze_state` receipt. They measure clauses, not the freeze.
- No installs; nothing written outside this report directory and the scratch root. Scratch
  (`/fast/scratch/hyaku/kaidoku-r47/C1SelfTest`) removed before yield; the two drivers and all
  JSON/stdout receipts are retained in `receipts/`.

## 8. Sources

- `tools/round-47/exact.py` @ `5017e1f…` (selftest L471–L561, `score` L166–L301, `check_refs`
  L142–L164).
- `plans/round-47-claims.md` @ `5017e1f…`, R47-C1 "Landed surface" and predicate clauses 1–9.
- `receipts/`: `selftest-frozen.out` `0249b80f…`, `deletion-matrix.json` / `.out`
  `1c3d244a…`, `liveness-probes.json` / `.out` `18f81ca9…`, `real-freeze-v3.out`
  `88fafc60…`, `real-freeze-v2.out` `9c3f51b7…`, drivers `deletion_matrix.py`
  `92042198484a…`, `liveness_probes.py`
  `fb47986a1c8a…`. Both JSONs record `driver_sha256` and `frozen_exact_sha256`
  (`dcef54f1b143…`); re-hashing the two retained drivers reproduces both values exactly.
