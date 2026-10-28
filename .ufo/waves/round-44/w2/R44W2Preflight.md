# R44W2Preflight — adversarial test of the M44-2 fix (`tools/round-45/frozen-path-preflight.py`)

Seat `R44W2Preflight`, round 44 wave 2. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(referenced below as `<LANE>`). Frozen bytes were never modified; every lane command is read-only
git/`python3 -I -B`. Scratch root `/fast/scratch/hyaku/kaidoku-r44/R44W2Preflight` was deleted at
the end of the seat; copies of every receipt named below are under
`<LANE>/.ufo/waves/round-44/w2/artifacts/R44W2Preflight/`.

Environment: `Python 3.14.8`, `git version 2.56.0`, `cmp (GNU diffutils) 3.12`, kernel
`7.2.11-arch1-1`. No tool installed, upgraded or removed by this seat (recorded per operator rule
2026-10-19: **no installs**).

## Verdict

The gate is **correct on all six assigned cases** and I found **no blindness** to merges,
mode-only changes, deletions, renames or modify-then-restore. It is **too lenient in one
false-green way** (a frozen pathspec that matches nothing at FREEZE exits 0 `clean`, defect D-1),
it **misstates its own default** (D-2), and as wired for round 44 it is a **tool, not a gate** —
nothing in the lane invokes it, and the demonstrated invocation covers one entry of round 44's
§"Frozen paths" list (D-3). M44-2's disclosure is honest and its evidence reproduces byte-for-byte,
but "sufficient" only after D-1/D-3 are fixed. C1's stop is the only defensible reading of the
frozen text; the record of *why* the counter is red at `55bcce69` needs one precision fix (D-5).

## Receipts

All gate runs: `python3 -I -B <LANE>/tools/round-45/frozen-path-preflight.py --root … --freeze …
--rev … [--pathspec …] --json-out …`. `sha256` is over the tool's stdout (the receipt JSON it
prints). Gate file at the lane tip: `sha256
a2ea675d0d89b462693e97d853d1c1af3122913ba2d0026105044421c9a0e174`, tracked at `HEAD` (=
`8bb1090a`), worktree identical to the committed blob.

| case | rev / fixture rev | pathspec | exit | verdict | `touched` | `blob_changed` | stdout sha256 | wall |
|---|---|---|---|---|---|---|---|---|
| 1 RED @ `c86ea508` | `c86ea508188c50e2645b1f9bba65df4177cda6b1` | `tools/round-44` | **1** | `frozen_path_changed` | 8 | 8 | `20a87d4d…a28896` | 0.094 s |
| 2 GREEN @ `55bcce69` | `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` | `tools/round-44` | **0** | `clean` | 0 | 0 | `c8a03c26…0a870f` | 0.096 s |
| 3 rev before freeze | `c29360e3ba5381a5ab69e372d0d9577970f85018` | `tools/round-44` | **2** | `could_not_evaluate` — `freeze is not an ancestor of rev` | — | — | `1b90500d…7dbb33` | 0.030 s |
| 4 unknown rev | `0000…0000` | `tools/round-44` | **2** | `could_not_evaluate` — `unknown rev revision` | — | — | `4caf3c85…95aae7` | 0.029 s |
| 4b unknown freeze | `1111…1111` / rev `55bcce69` | `tools/round-44` | **2** | `could_not_evaluate` — `unknown freeze revision` | — | — | `a41f9d29…bc51dc` | 0.028 s |
| 2b current tip `8bb1090a` | `8bb1090af3fef64477c4337855e4347472db2701` | `tools/round-44` | **1** | `frozen_path_changed` | 8 | 8 | `c302813c…8a1cdf99` | 0.091 s |
| 5 modify→restore (fixture) | `50549a67` vs freeze `dd42a2e1` | `frozen` | **1** | `frozen_path_changed` | 4 | **0** | `a8709610…c50de0` | — |
| 6a merge carries side edit | `3f81b75a` vs freeze `b48dfe69` | `frozen` | **1** | `frozen_path_changed` | 2 | 1 | `438776b3…ca621f` | — |
| 6b **evil merge** (edit in neither parent) | `4239fb7b` vs freeze `78d4f94e` | `frozen` | **1** | `frozen_path_changed` | 1 (`4239fb7b` M `frozen/a.txt`) | 1 | `866496bb…9bb3b9` | — |
| 6c `-s ours` merge, side edit dropped | `bafc04bc` vs freeze `4239fb7b` | `frozen` | **1** | `frozen_path_changed` | 1 (`8354faed` M) | **0** | `f8205d5c…74cb3e` | — |
| X1 pathspec typo (D-1) | `4239fb7b` vs freeze `78d4f94e` | `frozen/nope` | **0** | `clean` | 0 | 0 | `a8149ccc…95e6cbe` | — |
| X2 no `--pathspec` (D-2) | `4239fb7b` vs freeze `78d4f94e` | (none) | **1** | `frozen_path_changed` | 3 | **not evaluated** | `87b6bb6e…bb2049` | — |
| X3 rev == freeze | `78d4f94e` | `frozen` | **0** | `clean` | 0 | 0 | `c0442abd…` | — |
| X4 mode-only change (D-4) | `404d52b0` vs freeze `3bf461ac` | `f` | **1** | `frozen_path_changed` | 1 (M) | **0** | `caab8105…1649e4` | — |
| X5 delete + rename out | `78b05c03` vs freeze `b84eba8b` | `frozen` | **1** | `frozen_path_changed` | 2 (D,D) | 2 | `7d9613bf…181fe6` | — |

Independent counter corroboration (my own runs, not the committed receipts):

| run | exit | observed |
|---|---|---|
| `c2-counter.py --root <LANE> --rev 55bcce69 --freeze c48f8a4b --work <scratch>` | **0** | `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true` (stdout sha256 `dd7c529b…a16a9b3`, 4.53 s) |
| `c2-counter.py --root <LANE> --rev 8bb1090a --freeze c48f8a4b --work <scratch>` | **2** | same 8 `frozen_path_changed` paths as the gate (stdout sha256 `0a81b8b2…9a064c64`, 4.62 s) |

The C1 counter at the tip was **not** re-executed (it requires `--pkg65` plus four live REA 6.5.0
reruns; the committed `.ufo/waves/round-44/l1/c1-score-at-tip.json` and sibling seat
`R44W2C1Rescore` carry that). Its committed receipt agrees with the gate path-for-path.

## Case findings

1. **RED at `c86ea508` — pass, and byte-identical to the committed evidence.** Exit 1, `touched`
   = `blob_changed` = exactly the 8 paths
   `tools/round-44/control-fixtures/{c3/manifest.json, c3/corpus/evidence/round-44/c1/v1le/after.json,
   pos/manifest.json, pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md,
   pos/corpus/evidence/round-44/c1/{v1be,v1le,v2be,v2le}/after.json}`, all status `M`, all from
   `c86ea508`. `cmp` of my `--json-out` against
   `<LANE>/.ufo/waves/round-44/l1/preflight-c86ea508.json` → **identical**. The same 8 paths are
   the list in both counters' `frozen_path_changed`, so the lesson's "byte-identical in both
   counters" claim holds.
2. **GREEN at `55bcce69` — pass.** Exit 0, `touched []`, `blob_changed []`; `cmp` against
   `<LANE>/.ufo/waves/round-44/l1/preflight-55bcce69.json` → **identical**.
3. **rev before the freeze — pass.** Exit 2, `freeze is not an ancestor of rev`. This is the arm
   that stops a "score the base and call it a descendant" mistake.
4. **unknown revision — pass.** Exit 2 `unknown rev revision`; unknown *freeze* also exits 2
   (`unknown freeze revision`), so neither endpoint can silently resolve to `HEAD`.
5. **modify-then-restore — pass, and the WALK arm fires.** Fixture: freeze `dd42a2e1`, then
   `ff4eef5e` modifies `frozen/a.txt`, `a4a1a6d2` restores it byte-for-byte (tree equals the
   freeze tree). At `50549a67` the tree is again identical to the freeze. Result: exit 1,
   `blob_changed []` (backstop clean — the restored blob hashes equal), `touched` = 4 entries
   (`a4a1a6d2` M, `ff4eef5e` M, `55ff6b54` A, `50549a67` D for `frozen/added.txt`). Because the
   backstop is clean, the **only** arm that reds is the commit walk — exactly the frozen rule
   "a later restore does not un-block". Consequence: the backstop is a redundancy net, never the
   primary detector; any future edit that narrows the walk silently converts a red into a false
   green on restored paths.
6. **Merge-commit edit — pass in all three shapes, including a true evil merge.**
   - 6a (normal merge, side branch edited `frozen/sub/b.txt`): the **merge commit itself**
     (`3f81b75a`) is reported M together with the side commit, and `blob_changed` lists the path.
   - 6b (**evil merge**: `frozen/a.txt` set to content present in *neither* parent): reported as
     `4239fb7b M frozen/a.txt`, `blob_changed ['frozen/a.txt']`. This is the round-43
     `-m --diff-merges=first-parent` requirement, and the flag choice is load-bearing: on the same
     rev, `git log --name-status -- frozen` (round-42 style) prints the merge hash with **no diff
     lines at all** (`artifacts/R44W2Preflight/git-log-flag-variants.txt`, arm [C]), while arms
     [A] `-m --diff-merges=first-parent` and [B] `--diff-merges=first-parent` alone both print
     `M frozen/a.txt`.
   - 6c (`-s ours` merge that keeps the first parent and therefore *drops* the side edit):
     `blob_changed []`, red only via the side commit `8354faed`. Over-strict relative to "final
     bytes changed", but exactly what the frozen rule says ("no commit in `FREEZE..REV` touches a
     frozen path"), so it is correct behaviour, not a false positive to fix.
   - Deletion + rename-out of a frozen file (X5) reds through both arms.
   - Mode-only change `100644→100755` (X4): `blob_changed []` (blob SHA unchanged), walk M → exit 1.
     Correct, but see D-4.

## Defects

**D-1 (false green; must fix before wiring). A frozen pathspec that matches nothing at FREEZE
exits 0 `clean`.**
- Where: `<LANE>/tools/round-45/frozen-path-preflight.py:67-77`. The backstop iterates
  `git ls-tree -r --name-only <freeze> -- <pathspec>`; an empty listing makes the loop body
  unreachable, and `ok = not touched and not blob_changed` (line 79) is then true whenever no
  commit in the range happened to touch the misspelled path.
- Command: `python3 -I -B <LANE>/tools/round-45/frozen-path-preflight.py --root <fixture> --freeze
  78d4f94e… --rev 4239fb7b… --pathspec frozen/nope --json-out …`
- Exit **0**; observed `{"verdict": "clean", "touched": [], "blob_changed": [], "pathspec":
  ["frozen/nope"]}` even though that rev is a frozen-path violation under the correct pathspec
  (same rev, `--pathspec frozen` → exit 1).
- Why it matters for M44-2: a commit-time gate is invoked from a script or hook whose pathspec is
  hand-written. A typo (`tools/r44`, a stale round directory, a trailing-slash mismatch) turns the
  gate permanently green and the `c86ea508` class of violation lands exactly as before. Fix: when
  `--pathspec` is present and the FREEZE listing under it is empty, return `fail(2,
  "pathspec matches nothing at freeze", args)`.

**D-2 (misleading help text). `--pathspec` default is documented as "none (tree backstop only)",
but no pathspec *disables* the tree backstop.**
- Where: `<LANE>/tools/round-45/frozen-path-preflight.py:29-30` (help) vs `:69` (`if pathspec:`
  gates the whole backstop).
- Command: same gate, `--root <fixture> --freeze 78d4f94e… --rev 4239fb7b…` with **no**
  `--pathspec`; exit 1, observed `"blob_changed": []` — the backstop is skipped, so the promise
  "tree backstop only" is false; the real default is commit-walk-only. Either run the backstop over
  the whole tree when no pathspec is given, or reword to "Default: none (commit walk only; the tree
  blob backstop requires at least one pathspec)". A preflight gate whose description and behaviour
  disagree is the exact class of defect this round is auditing.

**D-3 (insufficiency, wiring). The demonstrated invocation covers one entry of the frozen-path
list.**
- Round 44 freezes, per `<LANE>/plans/round-44-claims.md` §"Frozen paths": `plans/round-44-claims.md`,
  `tools/round-44/` (directory), `tools/round-42/fixtures.json`, `tools/round-42/c1-counter.py`,
  `tools/round-43/c1-counter.py`, the four carrier bins under
  `corpus/evidence/round-42/c2/fixtures/`, the four oracle trees under
  `corpus/evidence/round-44/oracle/`, `tools/round-44/control-fixtures/**`, `SKILL.md`,
  `corpus/SOURCES.md`, plus the pinned historical receipts.
- The lesson (`<LANE>/corpus/lessons/round-44.md`, M44-2 row and `## Routed defects` R44-CL1, as
  committed at `8bb1090a`; the file is unfrozen and was being edited by another wave-2 seat while
  this report was written, so no line numbers are cited), `LOG.md:3203` and `SCORECARD.md:3530`
  demonstrate only `--pathspec tools/round-44`. `--pathspec` is repeatable (X-verified: two
  pathspecs filter independently), so the gate *can* express the whole vector; no recorded
  invocation does. Fix: commit the round's frozen-pathspec vector next to the gate (a
  `--pathspecs-file` or an explicit repeated-`--pathspec` command line in the lesson), and
  re-demonstrate red at `c86ea508` and green at `55bcce69` with it.

**D-4 (documented asymmetry). The tree backstop compares blob SHAs, not tree entries, so it is
blind to mode changes; only the walk catches them.** Evidence X4. Keep the walk's status set
(`M,D,R,T,U,A,C`) intact when reusing this tool, or the mode arm disappears.

**D-5 (record precision, R44-CL2). "No run can satisfy the whole frozen text" overstates; the
counter does not implement the clause the stop rests on, and the red at `55bcce69` comes from the
withdrawn doc rows.**
- The frozen clause at `<LANE>/plans/round-44-claims.md:34-35` requires
  `parameters.output_directory` to name a `corpus/evidence/round-44/c1/` path; the predicate at
  `:137-138` requires the `/kaidoku-r44/` segment. Under the strict reading (output_directory
  *must be* the committed path) the conjunction is unsatisfiable for a scratch run — so the stop is
  right.
- But the frozen counter never checks the first clause: `<LANE>/tools/round-44/c1-counter.py:1176-1183`
  `provenance_ok()` only requires an absolute path containing `/kaidoku-r44/` with no `..`.
  Probe (`artifacts/R44W2Preflight/provenance-ok-probe.txt`):
  `provenance_ok('/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out')` →
  **True**; `provenance_ok('/fast/scratch/hyaku/kaidoku-r44/x/corpus/evidence/round-44/c1/v1le')` →
  **True**; `provenance_ok('<LANE>/corpus/evidence/round-44/c1/v1le')` → **False**. So a
  substring-shaped scratch path satisfies *both* prose clauses and the counter — a loophole a
  future freeze must close by stating provenance as an exact path equality / run-directory prefix,
  not "names".
- Consequently the counter's `met_target false` at `55bcce69` is **not** caused by provenance:
  `.../l1/c1-score-at-55bcce69.json` has `failing: []` and exactly three falsy bindings —
  `province_core_section`, `province_core_row`, `frontier_note` — i.e. the Core row the round
  withdrew. The same counter scored `met_target true, exit 0` at lane rev `4cc1ac11` with the same
  scratch-form receipts (`.../l1/c1-score-4cc1.json`). `LOG.md:3201` does disclose the
  `4cc1ac11` met score and names the false bindings, so the record is honest; the one sentence to
  amend is "so no run can satisfy the whole frozen text", which should read "the frozen text's
  committed-path clause is not implemented by the counter (it passes the scratch form), so the
  score was withdrawn rather than claimed".

**D-6 (wording, no action needed).** The lesson and handoff call `c86ea508`'s writes
"added/edited 8 files"; `git show --name-status c86ea508` shows 8 × `M tools/round-44/…` and no
addition under `tools/round-44/`. The count 8 is exact; only the verb is wrong.

## M44-2 — is the record honest and sufficient?

**Honest: yes, verified.**
- `c86ea508` is the only commit in `c48f8a4b..tip` touching `tools/round-44/`
  (`git log --oneline c48f8a4..8bb1090a -- tools/round-44/` → `c86ea508` alone), and it modified
  the 8 files the counters and the gate both name.
- Both counters exit 2 `frozen_path_changed` with that identical 8-path list at the tip: C1
  committed receipt `.../l1/c1-score-at-tip.json`; C2 re-run by me at the **current** tip
  `8bb1090a`, one commit past the dispatch tip, still exit 2 with the same 8 paths. The round
  therefore measures at `55bcce69` — admissible under the frozen rule, which constrains `REV`
  relative to `FREEZE`, not to the branch head — and `LOG.md:3203`, `SCORECARD.md:3530` and the
  lesson all say the admissible revision is `55bcce69`, not the tip. Nothing scores green at the
  tip anywhere in the record.
- The red/green pair it cites is real: my independent runs are byte-identical to
  `preflight-c86ea508.json` and `preflight-55bcce69.json`.

**Sufficient: not yet.** Three gaps, in order of risk: (i) D-1 makes the gate's most likely
wiring failure silent-green; (ii) D-3 leaves the rest of the frozen-path list unguarded by the
demonstrated invocation; (iii) the tool is invoked by nothing — `<LANE>/.git/hooks/` contains no executable hook at all (the directory lists
only `.` and `..`) and no script in the lane references the tool. The lesson discloses (iii) honestly as routed
defect R44-CL1 ("wire it into the round's commit sequence before the next freeze"), so this is a
disclosed incompleteness, not a false claim. What the record does **not** say is the operational
consequence: the round's headline numbers (C2 80/80, C1 4/4 measured) are reproducible only at a
revision that is no longer the branch head, and a reader re-scoring `main` today gets exit 2 from
both counters. Recommend one sentence in the lesson saying exactly that, and fixing D-1 before the
gate is trusted.

## C1 — is the stop the only correct reading?

**Yes, on the frozen text; the record says so, with the causality caveat of D-5.**
- The frozen predicate plus the wave-1 controls amendment (`plans/round-44-claims.md:34-35`,
  `:137-139`) require `parameters.output_directory` to name a committed
  `corpus/evidence/round-44/c1/` path *and* the `/kaidoku-r44/` segment. The four committed C1
  receipts carry the scratch form only — e.g.
  `<LANE>/corpus/evidence/round-44/c1/v1le/after.json` →
  `"output_directory": "/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out"`.
  Under the strict reading no scratch run can name the committed path, so the claim cannot be met
  and `met_target false` is the correct verdict: no promotion, no Core row.
- The stop is also consistent in the record: `LOG.md:3201` (met at `4cc1ac11`; red at `55bcce69`
  with the three doc bindings false; cause; no Core row; R44-CL2 routed), the lesson's
  `## Routed defects` R44-CL2, and `PROVINCE.md`'s rewritten
  `## Round-44 measured, not promoted (R44-C1 honest stop)` section plus its frontier note, which
  keep `squashfs_v1`/`squashfs_v2` Frontier. "The record says exactly that" holds for the claim
  state and the tip red; D-5 is the one place where the *reason* sentence needs the qualifier that
  the counter passes the scratch provenance.
- Not re-executed here: the C1 counter's own run at `55bcce69` (needs `--pkg65` and four live REA
  reruns). I verified its committed receipt's shape (`carriers_matched 4`, `met_target false`,
  `exit_code 1`, `frozen_path_changed []`, `failing []`) and the lane state that produces it.

## Limits of this seat's evidence

- C1 counter not re-run (above); C2 counter re-run only.
- Scratch fixtures are synthetic (2–3 files, `git 2.56.0` defaults): no submodule/gitlink, no
  sparse checkout, no shallow clone, no case-colliding paths, no pathspec magic (`:(glob)`,
  `:(exclude)`) were exercised.
- The gate was not exercised as a hook (none exists) and not under `--pathspec` values containing
  spaces or newlines.
- Over-strictness seen and judged correct, not reported as defects: any `A`/`C` under the pathspec
  reds unconditionally (the frozen rule only makes `A` a change when the path existed at FREEZE),
  and a merge that drops a side edit still reds via the side commit.
