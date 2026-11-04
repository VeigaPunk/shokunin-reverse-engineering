# ScribeLesson — round 66, w1 (scribe, leaf)

Scoped findings for the L1. Draft deliverable:
`.ufo/waves/round-66/w1/ScribeLesson/draft.md` (15,745 bytes, sha256
`0d3a2d6792d6f410b1f73a7e550e9284661b3d6590b36c588e3e73c7098a8aaa`). Prose only; nothing landed.

## What was read (no re-runs)

| path | read for | state observed |
|---|---|---|
| `plans/round-66-claims.md`, `.ufo/waves/round-66/claims.json` | both predicates, frontier step, round shape | present at the freeze commit `7b63dd5d` (`git show --stat`: 124 + 48 lines) |
| `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` | M66-1 arms, M66-3 detail | 1/5; a2 `r65_order_state.cache_present []` vs `cache_on_disk_after_probe ["__pycache__", "__pycache__/fixture_mod.cpython-315.pyc"]`; a4 r65 exit 0, `entries 29, ok true, findings []`; a5 `r65_closure.ok true` |
| `.ufo/waves/round-66/l1/controls/c2-do-nothing.json` | Gate (c), M66-2 | 0/3; date mode shares only `mapped`; `population_dropped 3`, no name key |
| `.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json` | base arm | `recipe_a_equivalent true`, `recipe_a_diffs {}`, hidden 3, A2 false (`[142,142]` vs `[145,145]`), `mismatches 1`, exit 1 |
| `.ufo/waves/round-66/w1/ExecClosure/verify.json`, `skiprun.json`, `instrument-before/after.txt`, `toolchain-cache-after.txt` | C1 after-arm | 5/5, exit 0; a2 finding `cache present after probe 2: …pyc`; a4 `count_ok false`, `count 29 != 30`; a5 `closure null`, `closure_claimed false`, `runs_total 0`; instrument sha `3c5cfb03…` unchanged; toolchain cache file 0 bytes |
| `.ufo/waves/round-66/w1/ExecCoverage/selfcheck-at-freeze.json`, `instrument-before/after.txt` | C2 after-arm | exit 1, `mismatches 1` at rev `7b63dd5d`; `recipe_a_hidden_count 3`; instrument sha `1be9d046…` unchanged |
| `.ufo/waves/round-66/l1/pre/selftest-c1.txt`, `selftest-c2.txt` | battery state | 30 cases / 0 failures; 26 cases / 0 failures |
| `.ufo/waves/round-66/l1/records/r66-order.txt` | M65-3 duty | carry-in `b5b02e1f` ancestor of freeze: PASS exit 0 |
| `corpus/lessons/round-65.md`, `corpus/QUALITY.md:118-166`, `corpus/SOURCES.md:183` | house shape, row style, S266 | rows 94–103 are bullet-style; S266 is the last of 173 rows |

Read-only git checks run (no mutations): `merge-base --is-ancestor 78fa9666 <freeze>` exit 0;
`merge-base --is-ancestor b5b02e1f <freeze>` exit 0; `show --stat 7b63dd5d` and `78fa9666`;
`ls-files .ufo/waves/round-66`, `tools/round-66`; `check-ignore -v`; `status --porcelain --ignored tools/round-66`.

## Findings

1. **R66-C2 is not verified at the freeze, by construction.** `--selfcheck --rev 7b63dd5d` is exit 1 with
   `mismatches 1` (A2: claimed `[142,142]`, observed `[145,145]`). The predicate's measured revision is the one
   where the `## Owned axes` coverage row carries the repaired stem score and fraction — i.e. the landing. The L1
   must land the row (145/145, three hidden names) and file a `--selfcheck --rev <landing>` receipt at
   `mismatches 0`, exit 0, before any text says C2 verified. Recommend the landing receipt land in
   `w1/ExecCoverage/` or `l1/`, not as a post-landing rewrite of the freeze receipt.
2. **M66-3's contaminated first run is not retained.** `git show 78fa9666` holds only the fixed control and the
   1/5 receipt; the pre-fix receipt was overwritten in place. The draft states this as a limit and grounds the class
   in the control's own fix comment plus the corrected receipt's separated detail keys. If the L1 wants a red
   demonstration, it must be produced fresh (two arms, one shared root) — this seat did not run it.
3. **Lane tree is not cache-free at the freeze (new, M66-4).** `tools/round-66/__pycache__/` holds
   `closure-boundary.cpython-314.pyc` and `coverage-selfcheck.cpython-314.pyc` (mtime 21:13:29, freeze 21:13:44);
   `.gitignore:1:__pycache__/` makes them ignored, so `git status --porcelain tools/round-66` is clean while
   `--ignored` shows them. The round's cache-free evidence covers only the toolchain root
   (`toolchain-cache-after.txt`, 0 bytes). Impact on both predicates: none measured — the fixture probes run in
   `/fast` scratch under the venv interpreter (their caches carry `cpython-315`), and the manifest counts real
   files. Recommend the L1 remove `tools/round-66/__pycache__/` before the landing and extend the closure census to
   `tools/round-<N>/`, or state the limit in the closure.
4. **Gate (a) locator caution (QUALITY #91).** r65 measured the `sys.dont_write_bytecode` sentence's nearest
   enclosing heading as the module-level `h1`, so the new row's anchor must be `#sys.dont_write_bytecode`, not a
   heading. If the scout's row anchors only the h1, the row fails #91 and `claims.json` A8's sourced claim fails
   with it. This is a gate condition, not a claim change.
5. **Gate rows (b)–(d) are rejects with measured grounds**, not preferences: S266 already holds the `-B` locator;
   the date mode differs from recipe A in population and field set; the 30-vs-29 fixture is a control receipt.

## Not run

No counter, selftest, census closing pass, or closure was executed; no scratch directory was created
(`/fast/scratch/hyaku/kaidoku-r66/ScribeLesson` does not exist). No file outside
`.ufo/waves/round-66/w1/ScribeLesson/draft.md` and this file was written. No tool installs or upgrades.

## Artifact

- `.ufo/waves/round-66/w1/ScribeLesson/draft.md` — the lesson draft (Gate table, four Mistakes rows, Outcome,
  Census, QUALITY #104–#106 drafts).
