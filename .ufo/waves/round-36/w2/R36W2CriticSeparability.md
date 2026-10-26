# R36-W2 critic — causal separability, distinct axes, lowest axis

Seat `R36W2CriticSeparability`. Lane `kaidoku-shokunin`, round 36, wave 2. Anchors: base
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`, freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`, C2 landing
`d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`, C1 + assimilation landing
`ffc813417d3bceeeb7b028b12ce0be8a5dc33d95`, integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`.
Rule tested: `AXES.md:31-33` — "each [claim] verifiable without the others having landed — and name
**distinct axes** … At least one claim works the lane's **lowest-scoring non-retired axis**".

## Verdict

| Question | Answer | Basis |
|---|---|---|
| C1 verdict dependent on C2 having landed? | **No** | counter reads no SCORECARD/SHONEN byte (code read + `grep`, exit 1); C1 still `met_target true` at a commit whose SCORECARD.md and SHONEN.md are byte-identical to base |
| C2 verdict dependent on C1 having landed? | **No, at its own measured revision** `d2e46ef5` | no `2026-10-26*` knowledge file exists at that revision; C2 green there with every round-36 C1 artifact deleted from the tree |
| Any coupling at all? | **One, one-way, disclosed** | C2's *second* cited revision `ffc81341` is co-produced by C1's commit (coverage count 122→124, SHONEN box4 range 97-118→97-125). C1 is never downstream of C2 |
| Claims name distinct axes? | **Yes** | `SCORECARD.md:3391` coverage / `:3392` calibration; each label names the surface its own recipe reads |
| Lowest-axis rule met? | **Yes** | three-way tie at 10, none retired → coverage is a lowest axis |

No rejection-worthy defect found. Three record-level findings below (F-1..F-3), none of which changes
either verdict.

## Counterexamples tried (all in a bare clone; lane never mutated)

Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2CriticSeparability`; `C=$S/lane.git` created with
`git clone --bare /home/vgpnk/Projects/shokunin/kaidoku-shokunin lane.git`; test commits built with
`git -C "$C" read-tree <rev>` + `git -C "$C" write-tree` + `git -C "$C" commit-tree … -p <parent>` on a
private `GIT_INDEX_FILE`, each given the parent above so the freeze and base commits stay resolvable.
Counters were invoked with `--root "$C"` (git objects only), so no worktree edit by peers can enter.

### Test A — C1 with C2's work reverted (the strongest C1 counterexample)

Commit `cef2a3de2ab9ecc598a19414e580cfa9b9d0e63b`: tree of `ffc81341`, with `SCORECARD.md` and
`SHONEN.md` replaced by the base blobs `d57b01e6df0959f90c50389daf9c2eaac00a434f` /
`f25bc87721ab4898e6b3610f4132a4f96e9d4a1d` — i.e. C2's repairs *and* C1's restatements removed.

```
python3 -I -B tools/round-36/c1-counter.py --root $C --rev cef2a3de… --freeze 790561d4… --pkg65 <rea-6.5.0> --json-out $S/c1-with-base-surfaces.json
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"], "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "cef2a3de2ab9ecc598a19414e580cfa9b9d0e63b"}
EXIT=0
```

Construction validity (the surfaces really were reverted): the same commit scores C2 red —

```
python3 -I -B tools/round-36/c2-counter.py --root $C --rev cef2a3de… --base cab59f22…
{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [124, 124], "stated": [116, 116]}, {"check": "R3 SHONEN box4 Adjacent range", "observed": [97, 125], "stated": [97, 118]}], "guards_ok": false, "met_target": false, "mismatches": 4, …, "unresolved": [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B/"], ["shonen:No cross-domain bleed (PROVINCE.md still accurate)", "ScoutSkillPlacement.md"]]}
EXIT=1
```

### Test B — C2 with every round-36 C1 artifact deleted

Commit `49584bd2be52327b351abd8da179cd2068655f8d`: tree of `d2e46ef5`, with `corpus/evidence/round-36/`
(carriers, oracle, before/after receipts) and `tools/round-36/selftest/` removed — 39 files, 7435 deletions.

```
python3 -I -B tools/round-36/c2-counter.py --root $C --rev 49584bd2… --base cab59f22…
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "49584bd2be52327b351abd8da179cd2068655f8d", "unresolved": []}
EXIT=0
```

Construction validity: `git -C $C show 49584bd2…:corpus/evidence/round-36/c1/carriers.json` → exit 128
(object absent).

### Test C — C1 without the assimilated entry (rule C1's dependence on unclaimed content)

Commit `dd9089079b73ced86a637983097343deae1ba82a`: tree of `ffc81341` minus
`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`.

```
C1 → {"carriers_matched": 4, "carriers_unchanged": true, "met_target": true, …, "entry_source_ids": ["S107", "S108", "S109"], …}  EXIT=0
C2 → {"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [123, 123], "stated": [124, 124]}], "guards_ok": true, "met_target": false, "mismatches": 2, …, "unresolved": [["owned:coverage", "corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md"]]}  EXIT=1
```

This is the direction of the residual coupling in one line: delete round-36 knowledge content and only
C2 breaks.

### Reproductions of the cited receipts, plus the tip measurement

| run | rev | result | exit |
|---|---|---|---|
| C2 recheck at own landing | `d2e46ef5` | `mismatches 0, guards_ok true, met_target true`, observed command_a `122/122` | 0 |
| C1 at C2's landing rev | `d2e46ef5` | `carriers_matched 4` but every binding false → `met_target false` | 1 |
| C2 recheck at C1 landing | `ffc81341` | `met_target true`, observed `124/124` | 0 |
| C1 recheck at C1 landing | `ffc81341` | `met_target true` (matches committed `after/c1-at-ffc81341.json`) | 0 |
| C2 at integration tip | `01a44db` | `met_target true`, observed `{'adjacent_range': [97, 125], 'command_a': {'knowledge_files': 124, 'mapped': 124, 'resolved_rules': 17, 'rule_blocks': 17}, 'command_b': [9, 9], 'craft_range': [81, 314]}`, pointers 41 vs base 34, `missing_units []`, `unrepaired []` | 0 |
| C1 at integration tip | `01a44db` | `met_target true` | 0 |

Two facts fall out of the `d2e46ef5` C1 run (row 2): C1's green at `ffc81341` comes from C1's own
bindings (they are all false at `d2e46ef5`), and C1's *receipt* half (`carriers_matched 4`) was already
green at `d2e46ef5` because the after receipts landed at `3310d8fa` — before C2's commit, not because
of it.

## The C2-before-C1 claim, literally

```
$ git ls-tree -r --name-only d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be corpus/knowledge | grep -c '2026-10-26'
0            (grep exit 1)
$ git show --stat --format='' d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be
 SCORECARD.md | 4 ++--
 SHONEN.md    | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
$ git merge-base --is-ancestor d2e46ef5… ffc81341…   →  0
$ git log -1 --format='%cI' d2e46ef5…  → 2026-10-26T01:27:16-03:00 ; ffc81341… → 01:47:30-03:00
```

So C2's measured revision contains no C1 entry, no `## Round-36 additions to Core`, no S107-S109 rows, no
README coverage row for the stem; and C2's landing changed only the two self-assessment files — none of
the paths C1's counter opens.

## Code read: exactly which bytes each counter touches

`tools/round-36/c1-counter.py` — path literals at `:25-31` (`CARRIERS`, `EVDIR`, `ENTRY`, `STEM`,
`CORE_HEADING`, `XPIN`, `OPENED`); every read is a `git show <rev>:<path>` at `:83` (freeze's
`xpin-attribute.mjs`), `:144,:147` (carriers), `:158,:159` (oracle), `:164` (before/after envelopes),
`:199` (`PROVINCE.md`), `:204` (the entry), `:212` (`corpus/SOURCES.md`), `:226` (`corpus/README.md`).
Nothing else. `grep -nE 'SCORECARD|SHONEN' tools/round-36/c1-counter.py` → **no match, exit 1**.

`tools/round-36/c2-counter.py` — reads at `:61,:62` (SCORECARD, SHONEN), `:112` (pointers), `:121`
(README), `:124` (SKILL), `:133` (knowledge files), `:144` (`evidence/round-1-2026-10-15/result.json`),
`:183,:184` (SKILL, PROVINCE). Its `command_a` (`:119`) is `git ls-tree -r --name-only <rev> --
corpus/knowledge` restricted to `.md` — at `d2e46ef5` that is 122 files, matching the receipt's
`knowledge_files 122` (the extra entry is `corpus/knowledge/.gitkeep`).

## The coupling that does exist (one-way, disclosed, not a rule violation)

```
$ git diff d2e46ef5 ffc81341 -- SCORECARD.md SHONEN.md
SCORECARD.md | 2 +-     coverage row: 122/122 → 124/124
SHONEN.md    | 2 +-     box4: `PROVINCE.md:97-118` → `PROVINCE.md:97-125`
```

C1's own PROVINCE edit added 15 lines, which invalidated C2's box-4 range and moved the coverage count;
C1's commit repaired both in the same landing. Consequence: C2's *second* cited measurement (`ffc81341`,
`SCORECARD.md:3392`) is jointly produced, and test A shows C2 red if those two C1 lines are removed.
This differs from the r35 defect (`corpus/lessons/round-35.md:9`, M35-1) in the decisive respect: there
C2 could not verify at all without C1; here C2 verifies standalone at `d2e46ef5` and with C1's artifacts
deleted (test B). The plan discloses the dependence in the same sentence that pins the separable point —
`plans/round-36-claims.md:89-90` ("measured at its own landing commit before C1's entry lands, then again
at the final tip … the row is re-stated then") — so `AXES.md:31` "each verifiable without the others
having landed" is satisfied by the first measurement point.

## Distinct axes

`SCORECARD.md:3391` labels R36-C1 **coverage** (surface: the `PROVINCE.md` Frontier bullet moving into
`## Round-36 additions to Core`); `:3392` labels R36-C2 **calibration** (surface: SCORECARD owned/capability
rows and SHONEN boxes vs observed state). Both labels match the axis-table definitions
(`AXES.md:12-13`) and the bytes their counters read: C1's recipe resolves a PROVINCE Core row, the entry,
S107-S109 and a README coverage row; C2's recipe compares stated counts/ranges/pointers against
`git ls-tree`/file-length observations. Two claims, not one relabelled claim.

The one place the two instruments touch is the coverage count. It is a truth repair, not a coverage move:
at base the counter's own observable was already `[122, 122]` against the stale stated `[116, 116]`
(`.ufo/waves/round-36/controls/ctl-c2-0-do-nothing.json`), and the proxy only reaches 124 via the two
entries added at `ffc81341`. So neither claim double-counts the other's move.

## Lowest axis

Base owned rows: coverage `9.72 → 10.0`, depth `10 → 10`, calibration `0 → 10` (`SCORECARD.md` `## Owned
axes`, all three rows) → three-way tie at 10; tip `- **retired:** none`. Under the tie any owned axis is a
lowest axis (`corpus/lessons/round-31.md:23`), so C1 working coverage meets `AXES.md:33`. The statement
is made at `plans/round-36-claims.md:9-10`. `SCORECARD.md:12` ("calibration is the lowest axis") is scoped
by `:8-10` to the 2026-10-15 baseline retrospective and does not contradict the tie.
No axis harmed at the tip: coverage proxy up, depth 17/17 (my tip run), calibration mismatches 3→0.

## Findings (minor; none justifies rejection)

**F-1 — lowest-axis basis missing from the round's own SCORECARD section.** It is stated in the frozen
plan (`plans/round-36-claims.md:9-10`) but the round-36 SCORECARD section (`SCORECARD.md:3385-3396`) never
says the axes are tied at 10 or why coverage counts as lowest. Round 30's routed defect asked for exactly
this placement (`corpus/lessons/round-30-verifier-spotcheck.md:148`: "The lowest-axis basis is unstated …
State it in the round's SCORECARD section"). Rule not violated (the basis is committed and correct); the
record is one clause short of the earlier remedy.
*Smallest safe correction:* append the one clause to the round-36 section as a correction bullet (no
counter, predicate or carrier touched), or carry it as a routed defect.

**F-2 — the coverage row's counting authority lives in the calibration claim's instrument.**
`SCORECARD.md:23` (tip) cites "the command-A observable in `tools/round-36/c2-counter.py`", while
`tools/round-36/c1-counter.py` never measures the count. The pointer resolves and the implementation is
honest (tested: 122/122 at base, 124/124 at tip), so no score is fabricated; but the coverage axis's
number is now defined by a file authored for R36-C2, so a defect found in that counter would propagate to
the coverage row's evidence without either claim being re-measured.
*Smallest safe correction:* name the recipe itself in the row (`git ls-tree -r --name-only <rev> --
corpus/knowledge | grep -c '\.md$'`, intersected with the README `## Coverage map` stems) and cite the
c2-counter as one implementation of it.

**F-3 — the plan's "final tip" measurement has no committed receipt.** `plans/round-36-claims.md:89-90`
promises a second measurement "at the final tip"; the record carries `ffc81341`
(`.ufo/waves/round-36/after/c2-at-ffc81341.json`), which was the tip when measured, but the integration
tip `01a44db` added a C2-governed unit (the capability row at `SCORECARD.md:627`) with no C2 receipt.
Outcome is not in doubt — I ran it: `met_target true`, exit 0, pointers 41, `missing_units []`,
`unrepaired []` — so this is a citation gap, not a false verdict.
*Smallest safe correction:* commit that tip receipt, or drop the "final tip" phrasing in round 37.

## Limits of this review

- Receipt provenance/evidence-id forgery is not my seat; I exercised the counters as frozen and read the
  receipts as committed. QUALITY 77/78 shortcut classes are disclosed by the round itself
  (`SCORECARD.md:3391-3392`).
- Every measurement used `git show <rev>:<path>` at a pinned revision. The worktree currently carries
  peer edits (`git status --porcelain` → ` M corpus/SOURCES.md`, ` M corpus/knowledge/2026-10-26-unblob-
  sasquatch-dependency.md`, ` M corpus/lessons/round-36.md`); none of it enters a pinned-rev read, so no
  number above depends on uncommitted state.
- No VCS mutation in the lane: read-only `git show/log/diff/ls-tree/merge-base/rev-parse/cat-file`; the
  three test commits exist only in the scratch clone, which was deleted.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2CriticSeparability` removed (`test ! -e "$S"` → true).
  Disclosed: one `du -sh` was run, once, against my own seat directory (`$S/lane.git`, 115M) to size the
  clone; no `find`, and no `du` against any other lane's tree under `/fast/scratch`. Two convenience runs
  used `/tmp` (a 1.1 KB receipt JSON and a `HYAKU_SCRATCH` temp dir), both deleted; nothing cited above
  lives outside this report.
- Tooling: nothing installed or upgraded (no pacman, no `uv`, no `npx`); rea-agents 6.5.0 was read from
  the pre-existing package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `node`
  only via the frozen `tools/round-27/xpin-attribute.mjs`. No subagents, no background jobs.
