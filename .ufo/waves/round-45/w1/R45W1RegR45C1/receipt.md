# R45W1RegR45C1 — receipt

Seat `R45W1RegR45C1`, round 45 wave 1, leaf, lane `kaidoku-shokunin`, read-only on the lane
tree. Every instrument run below executed the **frozen bytes** extracted from
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, with `TMPDIR`/`HYAKU_SCRATCH` pointed at
`/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45C1`. Nothing under `/tmp` is cited. All times
UTC, `2026-10-28`. Python `3.14.8`. No installs or upgrades were needed or made.

Hostile-review note on the tables: each row carries the command actually run, the process
exit code, the **sha256 of that process's stdout**, and the wall time. The three `E2-*`
digests are values printed *by* `sha256sum`, not stdout hashes; they are labelled that way.

## Identity

| item | value |
|---|---|
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` — derived twice, `git log --format=%H -1 -- plans/round-45-claims.md` and `git log --format=%H -1 -- tools/round-45/` (stdout sha256 `97150e76f53a53146147fe3d2c3d6318d1e08cd3e8d23cadde679512bf85b67f`, exit 0, both) |
| base | `149133d47aa7e90796f96047afe6d251a3e65b2c` (claims file header) |
| graded tip measured | `faa875bc0eb839d15b83c4afa6078819e5a7b381` (`HEAD` at run time) |
| claims revision cited by the report | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` ("round-45 amendment A1") |
| instrument blob at freeze | `4ce400b29d6eba3cb03e242db8ba8bdf9d4fcfdd` (mode 100755) |
| instrument sha256 | `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`, 14319 bytes, 366 lines |
| instrument sha256 at `HEAD` / worktree | identical — `git diff --stat f762b727..HEAD -- plans/round-45-claims.md tools/round-45/` printed nothing, and `sha256sum` of the worktree copy equals the extracted freeze copy |
| interpreter blob / sha256 | `b42398273da0449c01f6f26cc630853d58ea55ec` / `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`, 11987 bytes, 315 lines |
| claims blob / sha256 | `f93df4c3bd4069a0cd576d9649f1157609b6a5d5` / `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e`, 9461 bytes, 175 lines |
| commits in `FREEZE..HEAD` touching a frozen path | **none** (`git log --name-only --format= … -- plans/round-45-claims.md tools/round-45/` → empty) |
| merge commits in `FREEZE..HEAD` | **0** (`git rev-list --merges` → empty stdout, sha256 `e3b0c442…`) |

## Lane runs

| id | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| `E1-freeze-claims` | `git log --format=%H -1 -- plans/round-45-claims.md` | 0 | `97150e76f53a53146147fe3d2c3d6318d1e08cd3e8d23cadde679512bf85b67f` | 15:42:55 |
| `E1-freeze-tools` | `git log --format=%H -1 -- tools/round-45/` | 0 | `97150e76…` (same commit string) | 15:42:55 |
| `E2-c1-hash` | `sha256sum <S>/frozen/c1-counter.py tools/round-45/c1-counter.py` | 0 | value: `2cfc5a48…` (direct digest; both lines equal) | not stamped |
| `E2-pre-hash` | same for `frozen-path-preflight.py` | 0 | value: `633ebc05…` (both lines equal) | not stamped |
| `E2-claims-hash` | `git show f762b727:plans/round-45-claims.md \| sha256sum` | 0 | value: `56bacf31…` | not stamped |
| `E3-c1-selftest` | `python3 -I -B <S>/frozen/c1-counter.py --selftest` | **0** | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 15:42:55 |
| `E4-pre-selftest` | `python3 -I -B <S>/frozen/frozen-path-preflight.py --selftest` | **0** | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 15:42:55 |
| `E5-freeze-control` | `c1-counter --root <LANE> --freeze $FRZ --rev $FRZ --json-out …` | **1** | `e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` | 15:42:55 |
| `E6-base-control` | same with `--freeze $BASE --rev $BASE` | **1** | `5aebf06e5ffd91c20857660cae4b4170b5ca877fd9c242908f0b6cbe8efef2d9` | 15:42:56 |
| `E7-measured-rev` | same with `--rev 1f4b27f8` | **0** | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 15:42:56 |
| `E8-head` | same with `--rev faa875bc` | **0** | `0c83a7b3fc340e8f65f6d052b5d1b2905e6e1e4bf4d836788e3257394226ce14` | 15:42:56 |
| `E9-real-preflight` | `frozen-path-preflight --root <LANE> --freeze $FRZ --rev HEAD --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty` | **0** | `aa8c6163b8092fa5a54cb8a01f4e928453b62f38eb8751a5489e8828a2d15396` | 15:42:56 |
| `E9-merges` | `git rev-list --merges $FRZ..HEAD` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 15:42:56 |
| `E10-merge-counter` | `c1-counter --root <fixture> --freeze $F1 --rev <merge>` | **0** | `3d98f1ea844fdcf736c5d01cf1b67f250f05541283cee5fe09806d5e4c7f9c3a` | 15:42:57 |
| `E10-merge-preflight` | `frozen-path-preflight --root <fixture> --freeze $F1 --rev <merge> --pathspec tools/round-45/ --freeze-path tools/round-45` | **1** | `bd4f311157d2646a62ad55fe1c66f42e5aae09033a62dece50873ccc718bc6b3` | 15:42:57 |
| `E10-mergelog` | `git log --name-only --format='C %H' $F1..<merge> -- tools/round-45` | 0 | `d7c7e4a6aed9650b9cf9a5685a92d9476f54d0a73cce9a39e2a822d960063114` | 15:42:57 |
| `E11-heading` | `c1-counter --root <fixture> --freeze $F1 --rev <heading-edited>` | **1** | `e3b0c442…` (empty stdout; stderr ended `IndexError: list index out of range`) | 15:42:57 |
| `E12-usage` | `python3 -I -B c1-counter.py` (no arguments) | **2** | `ceadf6938045a1df52a6ff56ffc4797e7a6788eec4c5b40b3c0dc79b5764bf9b` | 15:42:57 |

### What the lane runs say

- **Selftest from frozen bytes: exit 0, `C1_SELFTEST: cases=9 failures=0`.** stdout sha256
  equals the value the sibling seat `R45W1C1CounterMutants` and the sibling
  `R45W1C1SelftestFromFreeze` measured independently (`296734f2…`), and is
  byte-identical to `.ufo/waves/round-45/controls/c1-selftest.txt`.
- **Embedded interpreter selftest: 11 cases, 0 failures**, sha256 `9f03df65…`, byte-identical
  to `controls/preflight-selftest.txt`. Every green receipt reports
  `preflight_selftest {cases: 11, exit: 0, failures: 0, ok: true}` because the counter
  extracts the interpreter from `--rev` and runs it in a private scratch directory.
- **Do-nothing control at the freeze: exit 1** and the parsed JSON **equals** the committed
  `.ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json` (compared as objects, `True`):
  `rule_blocks 21`, `block22_present 0`, `block22_rows 0`, `block22_refs 0`, five named
  clauses in `failing`. The base run **equals** `ctl-c1-0-base.json` (also `True`,
  `rule_blocks 21`, `interpreter_present true` because the pre-freeze single-arm gate
  existed at the base).
- **Graded tip and the report's measured revision: exit 0**, `met_target true`,
  `failing []`, `rule_blocks 22`, `block22_present 1`, `block22_rows 10`,
  `block22_refs 7`, `block22_unresolved_citations []`, `block22_cites {S140: true,
  interpreter: true}`, `preflight_selftest {cases: 11, failures: 0}`.
- **Freeze integrity of the real range: clean.** The standalone gate exits 0 with
  `touched []`, `restored []`, `blob_changed []`, `dirty []`, `verdict clean` over
  `f762b727..HEAD` with the directory pathspec; there are no merge commits in the range.

## Frozen-path arm, isolated fixture

Fixture built by `git archive` from the frozen commit (`SKILL.md`, `tools/round-45/`,
`plans/round-45-claims.md`) plus `corpus/` from `1f4b27f8`; its own `git init`, toplevel
verified equal to the fixture dir, throwaway identity inside the fixture only.
`F0 = 4404664f…` (freeze-shaped: 21 blocks), `F1 = 5553049f…` (block 22 landed).

| id | shape | exit | stdout sha256 | receipt |
|---|---|---|---|---|
| `A-touch` | direct commit appends to `tools/round-45/c1-counter.py` in `F0..rev` | **2** | `0db762f175737cad808e625fa7b5672b6896e6ec140d85747d9ce3a3a1d864ec` | `verdict could_not_evaluate`, `frozen_path_changed ['tools/round-45/c1-counter.py']`, no `met_target` |
| `A-restored` | same edit, then restored to the freeze bytes and committed | **2** | `0db762f1…` (identical — see limit 4) | same path still reported: history, not tip equality |
| `A-bulk` | one commit edits the interpreter and an unrelated file | **2** | `7b942b02725d4209884dcc54adc9c033cfc3426a12098fb13d0d62cdce2bf332` | `frozen_path_changed ['tools/round-45/frozen-path-preflight.py']` |
| `A-claims-touch` | commit appends to `plans/round-45-claims.md` only | **2** | `66314013c27ee84b9bab8a90d0472bef4677b992ad667eb3fb616cbcf12d2097` | `frozen_path_changed ['plans/round-45-claims.md']` |
| `A-nonancestor` | `--freeze` is a sibling branch, not an ancestor | **2** | `2ad451743ac05872bfaad8c1e1a88d91055a0e3e0b770116c4f2f003e6c24ea6` | `reason "freeze is not an ancestor of rev"` |
| `A-unknown-rev` | `--rev 000…0` | **2** | `260f72034176c55d342d21ef4e92066d7b5f006e7c7edcf9ddfd048f8d4b7b9a` | `reason "unknown rev revision"` |

So the claim's `frozen_path_changed → exit 2` clause is real for **every direct shape
tested**, including a touch that a later restore undid.

## SKILL-surface mutations (predicate clauses under attack)

Each variant is one committed edit on top of `F1`; exit code and `failing` list are from the
frozen counter.

| id | mutation | exit | stdout sha256 | observed |
|---|---|---|---|---|
| `M-rows8` | table cut to exactly 8 data rows | **0** | `03200e929048950046822959567f47800df78400c03fe7bb60ab58a579a21979` | boundary met |
| `M-rows7` | table cut to exactly 7 data rows | **1** | `5d41457773a0bae42245ce97130bdfe581ce8eadf00a4b797b9e284a9f08435d` | `block22_rows 7 < 8` |
| `M-exitcell_ok` | first row's exit cell `1` → `ok` | **1** | `024f80e1bb96e235971adf4a3effcd321b7f1e5c125b03ac302347dac1934ab3` | `block22 exit cells outside {0,1,2}: 1` |
| `M-junk8` | all 10 rows replaced by `\| x \| y \| 0 \| z \|` | **0** | `509e653abbb62077566717808f4a162fe5d3aa0afb191aa41b2b310a35ef0a97` | **passes** — structural-only limit is real |
| `M-bogus_tool_cite` | adds `` `tools/round-45/not-a-file.py:9999` `` to the block | **0** | `e560a821705f5986ebd2b62a7e2a5479057bb63acb9c07799bd403d0aced0007` | **passes** — citation regex only validates `corpus/(knowledge\|lessons)/*.md` and `plans/*.md` |
| `M-no_s140` | every `S140` removed | **1** | `7bd041989e2c3cdb0397ea31280c29f5f9cbfde2d1b54254bbb160d494c9dbb6` | `block22 does not cite S140` |
| `M-s140_as_s1400` | every `S140` → `S1400` | **1** | `27d5a8bf8bf7ecb5041d4cdcca0fa17b0c0a434d817fcae0224498167acf95e9` | word-boundary regex is correct: `S1400` does not satisfy `\bS140\b` |
| `M-no_interpreter` | interpreter path replaced by prose | **1** | `9178e2f7fa7f56eb9da53548c245c6f7e350f9b5f37b7536432e88c417040622` | `block22 does not cite interpreter` |
| `M-bad_header` | header cell `exit` → `code` | **1** | `1f1935d856a89a1513ba678517dc148a925e6997b3e4ba66baab0f1d805567cf` | header reason + all 10 exit cells bad |
| `M-no_marker` | marker removed | **1** | `e229d2a8f19793165f0cc5d8cc653b13d6183f52da9666acd8f267f396097b57` | `block22_present 0 != 1` plus the four dependent clauses |
| `M-empty_range` | `--freeze F1 --rev F1` | **0** | `d440d2319cafc95665a51ff0c98e79a6df2bb80293471c011ebb324b2f010621` | `met_target true` |
| `B-no-skill` | `SKILL.md` deleted at rev | **2** | `c260a7e4aeb157c764f78adfdc0058d760164337d6aae328c391f10111499a34` | `reason "SKILL.md absent at rev"` |
| `B-dirty-worktree` | uncommitted junk appended to `SKILL.md`, scored at committed rev | **0** | `de91c708d482fe70275056ba2f4bc268b4ec13fede8d7ee10200777bf34eab18` | reads git objects only; dirt invisible (by design, and the row's write scope does not claim otherwise) |

Earlier in the same fixture, without retained stdout hashes (values quoted from the
receipts, not asserted beyond the fields shown): a 23rd craft block → exit 1
(`rule_blocks 23 != 22`); a duplicated marker on a 23rd block → exit 1
(`rule_blocks 23`, `block22_present 2`); a citation to `plans/round-45-claims.md:99999` →
exit 1 (`unresolved citations`). Those three shapes are already covered by named selftest
cases (`red-relabelled-21-block`, `red-bad-citation` plus the sibling's mutant analysis),
so no hash was retained for the duplicates.

## The finding: the frozen-path arm fails open on merge commits

`frozen_path_changed()` runs `git log --name-only --format= <freeze>..<rev> -- <frozen>`,
with no `-m` and no `--diff-merges`. Git prints **no file list** for a merge commit under
that invocation, so a merge whose *resolution* edits a frozen path is invisible:

```
git -C <fixture> log --name-only --format='C %H' F1..M2 -- tools/round-45
C 7f870839df63aced411f9d83cb8fa14ab235de74
[end]                                   # no path, no status

git -C <fixture> log -m --diff-merges=first-parent --name-status --format='C %H' F1..M2 -- tools/round-45
C 7f870839df63aced411f9d83cb8fa14ab235de74

M	tools/round-45/c1-counter.py

git -C <fixture> rev-parse F1:tools/round-45/c1-counter.py M2:tools/round-45/c1-counter.py
4ce400b29d6eba3cb03e242db8ba8bdf9d4fcfdd
d98d51e31ad7754fa73592ea2423c7113a7850d7      # tip blob != freeze blob
```

Both parents of `M2` are clean of the frozen path; only the resolution changed it.

| instrument | same range `F1..M2` | result |
|---|---|---|
| `c1-counter.py` | | **exit 0**, `frozen_path_changed []`, `met_target true`, `failing []` |
| `frozen-path-preflight.py` | | **exit 1**, `touched [{commit: 7f8708…, path: tools/round-45/c1-counter.py, status: M}]`, `blob_changed [tools/round-45, tools/round-45/c1-counter.py]` |

Consequences, stated exactly:

1. Claim R45-C1's kill rule — "A commit in `FREEZE..REV` touching a frozen path makes the
   counter exit `2` without printing `met_target`" — is false for merge commits. The counter
   does not merely miss the `2`; it **continues** and can print `met_target: true` over a
   changed frozen instrument.
2. The selftest cannot see this: `red-frozen-touched-is-exit-2` builds a direct commit, and
   `red-unknown-rev`/`red-nonancestor` do not merge. This is the same class block 22 itself
   cites from R34b — the registered case set holds while the surface is shortcut-reachable.
3. **No measured score is affected.** The round's real history has zero merge commits
   (`E9-merges` empty), the frozen-path diff over `FREEZE..HEAD` is empty, and both gates
   score `HEAD` clean. The preflight — which is what blocks a landing — does catch the
   shape. The hole is in the counter's arm and in the claim's wording, not in the landed
   value.

## Limits measured alongside the target

1. **Structural-only block passes.** `M-junk8`: eight rows of `| x | y | 0 | z |` score
   `met_target: true`. Block 22's own prose discloses this ("a table of structurally valid
   but empty rows would pass it"), and the measurement confirms it.
2. **Citation validation is narrower than "citation".** `REF` admits only
   `corpus/knowledge|lessons/*.md` and `plans/*.md`. `M-bogus_tool_cite` shows a
   `tools/…:9999` reference is neither counted nor resolved; `block22_refs` stayed 7 and the
   run stayed green. Omission under-counts rather than over-counts, but the row should not be
   read as "every reference in the block resolves".
3. **Crash is mapped to `1`, not `2`.** Renaming the heading to `## Queue-drain craft(`
   makes `craft_blocks` raise `IndexError`; exit 1, empty stdout. `SKILL.md` is the graded,
   unfrozen surface, so a later round can produce this by renaming a heading — and the
   receipt will say "not met" for a predicate that was never evaluated.
4. **Exit-2 receipts drop their identity.** `main()` wraps early returns as
   `{"counter", "verdict", **receipt}` where `receipt` is `{"reason", …}`; there is no
   `freeze`/`rev`. `A-touch` and `A-restored` therefore hash **identically**
   (`0db762f1…`) although they scored different revisions. A `2` is auditable only from the
   command line that produced it.
5. **Direct `frozen-path-preflight.py --selftest` leaves fixture debris** under
   `$HYAKU_SCRATCH/kaidoku-r45/preflight-selftest/` — `tempfile.mkdtemp` per case, no
   removal (24 directories were present when inspected after the runs in this seat). The
   counter-driven path is clean because
   the counter removes its wrapper directory; the registry row's write scope for the
   *preflight* should say so. (This is the preflight's row, not this one; recorded here
   because the same scratch was measured.)
6. **Worktree dirt is invisible to the counter** (`B-dirty-worktree`, exit 0). That is the
   documented design — "reads Git objects only" — and the dirty arm belongs to the
   preflight. A lane that edits `SKILL.md` and scores without committing gets the committed
   verdict.

## Not run (and therefore not asserted)

- No test against a corrupted object store, a shallow/partial clone missing the freeze, or a
  read-only `--json-out` target.
- No test of `git log` rewrite shapes (rebase, amend across the freeze, replacement refs);
  the arm's behaviour there is unmeasured.
- No re-scoring of R45-C2 or the round-44 instruments; those belong to sibling seats.
- No network source opening (S140/S141 belong to the sources seats); only the *citation
  resolution inside this repo* was measured.

## Cross-seat agreement

- `--selftest` stdout sha256 `296734f2…` (9 cases) and the interpreter's `9f03df65…`
  (11 cases) match `.ufo/waves/round-45/w1/R45W1C1CounterMutants.md` and
  `R45W1C1SelftestFromFreeze.md`; the do-nothing and base receipts match the committed
  controls.
- `R45W1C1CounterMutants.md` mutates the counter's *code* and reports two survivors
  (block-count tested only from below; marker clause exit-redundant). This seat mutates the
  *SKILL surface* and the *history*; the two results are disjoint and consistent: the
  surface paths I exercised (23 blocks, duplicate marker) are caught by `evaluate()`
  exactly as that report predicts for the pristine code.
- No disagreement with any sibling finding recorded at the time of writing.

## Scratch hygiene

All work happened under `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45C1` (frozen copies,
one fixture repo, `--json-out` receipts, the four TSVs). The directory is removed after
these files were written; the fixture was never inside the lane tree and no git mutation
touched the lane (all lane git calls were `log`, `show`, `rev-parse`, `cat-file`, `ls-tree`,
`diff`, `rev-list`, `archive`).
