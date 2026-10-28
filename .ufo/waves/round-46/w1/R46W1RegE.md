# R46W1RegE — three instrument-registry rows for the round-46 C2 census (tag `reg-e`)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, freeze
`31820472784284727546808acc31b3ea1e73919b`. Everything below was derived by reading the
three instruments **at that commit** (`git show <freeze>:<path>`) and by running them;
no other revision was read and nothing was mutated.

Deliverables:

- `.ufo/waves/round-46/w1/R46W1RegE/rows.md` — three rows, sha256 `8355f2a8f873c98ab369b065149a321f29971daade6fd7398801ffdee63b95f0`
- `.ufo/waves/round-46/w1/R46W1RegE/receipt.md` + `evidence/` — every command, exit code, stdout sha256, UTC time

## The rows (paste verbatim)

```
| `tools/round-41/c2-counter.py` | gate — R41-C2 depth: the frozen v3 triage interpreter and the frozen independent evaluator agree on every held-out envelope (twenty planned classes two each plus twelve combo) at --rev, and every binding holds (seed, carrier sha256, declared feature tuple, four real receipts) | 0=met, matched equals n and no binding false; 1=not met, a pair miss or a false binding, receipt still written; 2=unevaluable, frozen path changed, unknown or non-ancestor revision, or an absent or failing generator, evaluator or interpreter | python3 -I -B tools/round-41/c2-counter.py --selftest — 70 cases, 20 green 50 red, pass 70 fail 0, exit 0 on 2026-10-28 | plans/round-41-claims.md frozen paths plus the seed and carrier sha256 pins in corpus/evidence/round-41/c2/heldout/manifest.json | --json-out receipt; scratch under HYAKU_SCRATCH/kaidoku-r41 or the system temp dir, removed at exit | kaidoku |
| `tools/round-42/fetch-carrier.py` | probe — materialises the round-42 C1 third-party carriers into a cache, fail-closed at every pin link (url, image sha256, container member, carve window, carve sha256) and refusing a symlinked cache, image-cache or work path | 0=every managed carrier materialised and verified, and at least one carrier was managed; 1=a chain link failed, named as link in the JSON receipt, with no cache entry for that carrier; 2=usage, unreadable spec, or an unusable work or cache path | python3 -I -B tools/round-42/fetch-carrier.py --selftest — 36 cases, pass 36 fail 0, exit 0 on 2026-10-28 | .ufo/waves/round-42/c1/carriers.json chain pins, the --repo-spec default | --cache entries, --image-cache entries, download staging in --work, --json-out | kaidoku |
| `tools/round-44/c2-counter.py` | gate — R44-C2 calibration: re-derives every frozen rubric statement at --rev by running the rubric's own check argv in an exported scratch clone, so an appended note is never evidence | 0=met, no mismatch, no unevaluable entry, frozen paths clean and at least one entry evaluated; 1=not met, a mismatch with nothing unevaluable, the receipt still written, and a pre-freeze census mismatch is not a claim score; 2=could-not-evaluate, malformed rubric, frozen path changed, absent frozen file, no evaluable entry or a check that cannot run | python3 -I -B tools/round-44/c2-counter.py --selftest — 24 arms, ok true, exit 0 on 2026-10-28 | tools/round-44/c2-rubric.json and the counter sha256 pin at the freeze, read as claim_gate.usable_as_claim_score | --work scratch clone, removed unless --keep-work; --json-out | kaidoku |
```

`rows.md` is exactly these three lines (no header, no fence).

## Exit meanings — read from source, not inferred

`tools/round-41/c2-counter.py` (2499 lines). Docstring `Exit` (54–60): `0 target met`,
`1 not met (a pair miss or a binding false), receipt still written`,
`2 unevaluable: freeze integrity or a structural prerequisite` with the reason
vocabulary enumerated (`frozen_path_changed`, `freeze_not_ancestor_of_rev`,
`unknown_revision`, `no_manifest_at_rev`, `generator_absent_at_freeze`,
`evaluator_failed`, `interpreter_failed`, `met_target_inconsistent`, …). `main()`
(1605–1652): `--selftest` → `selftest()` (0/1); missing `--root/--rev/--freeze` → 2;
`Unevaluable` → 2 with `exit_code: 2` in the receipt; otherwise
`res['exit_code'] = 0 if met else 1` (1598). Exit 1 does write `--json-out` — the
docstring's own wording, confirmed in `main()`.

`tools/round-42/fetch-carrier.py` (936 lines). Docstring `Exit:` (72–73): 0 every
managed carrier materialised and verified; 1 a chain link failed (named as `link`);
2 usage / unreadable spec / unusable work or cache path. `main()` (897–934): 0/1 from
`selftest()`; `return 2` when `not a.cache or not (a.spec or (a.root and a.rev))`
(913); `ChainError` out of `load_spec` / `workdir` / `_check_path` → `return 2` (924);
else `recs, rc = run(…); return rc`. **`run()` (531–549) is stricter than its docstring:**
`ok = managed > 0 and all(...)`, so a spec with no `url`-bearing carrier exits **1**,
not 0. The row states "at least one carrier was managed" for that reason — the
docstring alone would have produced a wrong verdict map. `REPO_SPEC` (90) is
`.ufo/waves/round-42/c1/carriers.json`, the `--repo-spec` default.

`tools/round-44/c2-counter.py` (1719 lines). Docstring `Exit codes:` line plus
`score()`'s decision (1302–1307): `EXIT_MET` iff `not mismatches and not unevaluable
and (not frozen_path_changed or pre_freeze) and entries_evaluated > 0`; `EXIT_FAIL`
**only** when `mismatches and not unevaluable`; everything else `EXIT_CANT`. Constants
`EXIT_MET/FAIL/CANT = 0/1/2` (123–125). So an unevaluable entry is never scored as
"not met" — it is 2, which is why the row's `1=` says "with nothing unevaluable".
`--schema` prints the module docstring and returns 0 (measured). `--pre-freeze` can
produce exit 1 as a **census** with `claim_score: false`; the row says so, so the L1
does not have to guess which 1 it is looking at.

## Verification (all commands, exit codes, hashes in `receipt.md`)

| claim | command | exit | result |
|---|---|---|---|
| all three exist at the freeze | `git -C LANE cat-file -e <freeze>:<path>` | 0 ×3 | present |
| r41 selftest is green **and** the number in the row is true | `python3 -I -B tools/round-41/c2-counter.py --selftest` | 0 | `cases=70 green=20 red=50 pass=70 fail=0` |
| r42 ditto | `… tools/round-42/fetch-carrier.py --selftest` | 0 | `cases=36 pass=36 fail=0` |
| r44 ditto | `… tools/round-44/c2-counter.py --selftest` | 0 | 24 arms, `ok: true` |
| r42 exit 1 names a link (row's `1=`) | `… --spec <fixture with image_sha256 = 64 zeros> --cache <dir>` | 1 | `"link": "image_sha256"`, `detail` names both digests, `exit_code: 1` in the receipt |
| r42 exit 2 is usage (row's `2=`) | `… --cache <dir>` (no spec, no root/rev) | 2 | usage text |
| r41 exit 2 is usage (row's `2=`) | `… --root /nonexistent` (no `--rev`/`--freeze`) | 2 | `usage: --root --rev --freeze required (or --selftest)` |
| r44 exit 2 is usage (row's `2=`) | `… --root . --rev HEAD` (no freeze, no pre-freeze) | 2 | usage text |
| r44 `0` is not only a claim pass | `… --schema` | 0 | docstring, 5824 bytes |
| the three paths are in the round-46 census | census.json@freeze | 0 | `scope_size 38`, `named_but_absent 0`, all three members |

None of the three takes an exit code outside `{0,1,2}`: an AST scan that skips string
literals leaves only `return 0`, `return 2`, `EXIT_MET/FAIL/CANT = 0/1/2` and
`sys.exit(main())` in the three files' own code. The `sys.exit(3)` / `sys.exit(9)` hits
in `round-41/c2-counter.py` are inside the `STUB_EVAL` / `STUB_INTERP` fixture templates
— those are the *subjects* the selftest runs, not the counter's own codes, so they are
not reported as an out-of-range exit. Argparse adds `--help` → 0 and a bad option → 2,
both inside the set.

## Row-format check, scored by the frozen `registry.py` itself

I did not hand-roll the acceptance rule. `evidence/check_rows.py` copies
`tools/round-46/registry.py` and `gate.py` **from the freeze** into scratch, imports
`registry`, and calls `registry.score()` with an in-memory `files()` callable — no repo,
no lane write, so the *frozen* parser decides.

| case | input | exit | `unregistered` / `thin` |
|---|---|---|---|
| A | my three rows, census = those three paths | **0** | `[]` / `[]`, `met_target: true`, `header_ok: true` |
| B2 | the six **landed** round-45 rows alone | 1 | `[]` / **all six** |
| B3 | the six landed rows under their landed header | 1 | also `header != house schema` |
| C | my row 1 reworded the way the landed rows word it | 1 | `/ thin: that path` |
| D | my row 1 with cell 0 = `see \`path\` (wrapper)` | 1 | `unregistered: that path` |

My script also asserts on `rows.md` directly: 3 rows, 7 cells each, cell 0 exactly one
backticked path, exactly two backticks per line (none outside cell 0), no literal `|`
inside a cell — `shape_violations: []`.

## Findings the L1 must reconcile before landing

1. **All six landed rows are thin (B2) and the landed header is not the house header
   (B3).** The landed section's second header cell is `gate or probe`; the house schema
   in `plans/round-46-claims.md` clause 2 is `gate or probe - purpose`. And every landed
   verdict-map cell reads ``` `0` met; `1` not met; `2` could-not-evaluate ``` — digits
   in backticks with no `=`/`:`, which `EXITMAP = \b([012])\s*[=:]` binds to nothing.
   Adding my three rows without rewording those six leaves `thin` non-empty and the C2
   counter at exit 1. Measured, not predicted: B2/B3.
2. **Duplicate-path shadowing.** `score()` builds `by_path` with `setdefault`, so when a
   path has two rows the **first** in the section wins. My row for
   `tools/round-44/c2-counter.py` and the landed round-45 row for the same path are both
   real; if both land, the honest 7-cell row must come first or the old one must go.
   Case B showed exactly this (five thin, not six, because my row shadowed the landed
   one).
3. **`run()` is stricter than its docstring** (r42): exit 0 requires `managed > 0`. A
   registry row copied from the docstring's `Exit:` line would claim 0 for a spec with
   no `url` carrier, which the code scores 1. Worth a routed `RX-CL` note against
   `tools/round-42/fetch-carrier.py`'s docstring (not fixed by me — the file is frozen
   and not mine to edit).
4. **`EXITMAP` also accepts `:`.** A verdict-map cell may bind with `0:` as well as
   `0=`. My rows use `=` as the seat spec requires; both satisfy the counter. A cell
   that only mentions the digits ("0 of 1, 2") fails either way (case C).
5. **`1=` in the round-44 row is not "the claim failed" in every case**: with
   `--pre-freeze` a mismatch is a census (`claim_score: false`). The row says so; if the
   L1 wants a shorter cell it can drop that clause without changing the counter's
   verdict, but the meaning would be less true.

## Calibration — what I did not do

- I did **not** run either round-46 counter (`attest.py`, `registry.py` main) against
  the lane: that is the L1's score, and the section does not exist yet.
- I did **not** score the full 38-path census — only my three paths plus, for the header
  and wording questions, the six landed rows. Whether the other 35 census paths are
  registered is not measured here.
- Presence in case A was supplied in memory; the real presence claim rests on the three
  `git cat-file -e` reads above (exit 0 each), which is the same object read the
  counter's presence arm performs.
- Nothing was installed; nothing under `/tmp`; scratch
  `/fast/scratch/hyaku/kaidoku-r46/R46W1RegE` removed after its receipts were copied
  into `evidence/`. No git/jj mutation, no lane edit outside this wave directory.
