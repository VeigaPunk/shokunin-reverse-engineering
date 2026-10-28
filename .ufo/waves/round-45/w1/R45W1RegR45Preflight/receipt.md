# Receipt — `tools/round-45/frozen-path-preflight.py` at `f762b727`

Seat `R45W1RegR45Preflight`, round 45 wave 1. All writes under
`S=/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45Preflight` with
`TMPDIR=$S`, `PYTHONDONTWRITEBYTECODE=1`; `$S` removed after these receipts were
copied here. Times are file mtimes in UTC (`date -u -d @$(stat -c %Y <file>)`), not
piped invocation stamps — the outputs are the retained evidence.

Frozen paths were never mutated: `git -C <lane> status --porcelain -- tools/round-45/
plans/round-45-claims.md` → empty, and `git diff --stat
f762b727..HEAD -- tools/round-45/ plans/round-45-claims.md` → empty.

## R1 — frozen bytes extraction

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show \
  f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/frozen-path-preflight.py \
  > $S/preflight@freeze.py
sha256sum $S/preflight@freeze.py tools/round-45/frozen-path-preflight.py
```

exit 0 · sha256 of both = `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`
· 2026-10-28T15:38:54Z · `git ls-tree -r --long f762b727 -- tools/round-45/`:
`100755 blob b42398273da0449c01f6f26cc630853d58ea55ec 11987 frozen-path-preflight.py`.

Base instrument for the arm delta:
`git show 149133d47aa7e90796f96047afe6d251a3e65b2c:tools/round-45/frozen-path-preflight.py`
→ 107 lines, sha256 `a2ea675d0d89b462693e97d853d1c1af3122913ba2d0026105044421c9a0e174`,
no `--selftest`, no `--check-dirty`, no `--require-pathspec`; it already parses
`--name-status` into `touched` and already runs the ls-tree/blob backstop.

## R2 — selftest of the frozen extraction

```
python3 -I -B $S/preflight@freeze.py --selftest > $S/selftest.out 2> $S/selftest.err
```

exit **0** · stdout sha256 `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c`
· 2026-10-28T15:38:54Z · stderr empty · 12 stdout lines · last line
`PREFLIGHT_SELFTEST: cases=11 failures=0`.

11 measured cases: `green-clean`, `red-touched`, `red-restored`, `red-dirty`,
`green-dirty-without-arm`, `red-dirfreeze-no-pathspec`, `green-dirfreeze-pathspec`,
`red-unknown-freeze`, `red-nonancestor`, `red-bulk-sweep`, `green-empty-range`.

## R3 — the gate on the real lane, freeze..HEAD

```
python3 -I -B $S/preflight@freeze.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev HEAD \
  --pathspec tools/round-45/ --freeze-path tools/round-45 \
  --pathspec plans/round-45-claims.md --freeze-path plans/round-45-claims.md \
  --check-dirty --require-pathspec --json-out $S/gate-real.json
```

exit **0** · stdout sha256 `4b5a685dc4274637efd76b2349acd384bfb817ec70b8203ca891c69c6b20c658`
· 2026-10-28T15:39:12Z · `rev faa875bc0eb839d15b83c4afa6078819e5a7b381`,
`touched []`, `blob_changed []`, `restored []`, `dirty []`, `verdict "clean"`.

## R4 — adversarial fixtures A1–A6 (`attack.py`, private repos under `$S/a1..a6`)

Each fixture: `git init -q` in `$S/aN`, identity set locally, one freeze commit, then the
named history; the table lists exit and verdict from `$S/attack.out`
(sha256 `04def84ea87ba98711bf1bdc1cb1a7f766c1ca10a3099a1deb4a2c0a5aff51fa`,
2026-10-28T15:40:17Z).

| fixture | history / flags | exit | verdict | reading |
|---|---|---|---|---|
| A1 | sibling `frozen/ghost.txt` added then deleted in `FREEZE..REV`; `--pathspec frozen/a.txt`, `--freeze-path frozen`, `--require-pathspec` | **0** | clean | false clean — the narrow pathspec is certified by `covers()` yet the commit arm never lists the sibling |
| A2 | same history, `--pathspec frozen/` | **1** | frozen_path_changed | both the add and the delete appear in `touched` |
| A3 | clean history, `--pathspec .`, `--freeze-path frozen` | **2** | could_not_evaluate (`pathspec_required`) | a strictly broader pathspec is refused |
| A4 | dirty `frozen/a.txt`, `--check-dirty --dirty-pathspec elsewhere.txt` | **0** | clean | the dirty scope is replaced, not unioned |
| A4b | same dirty file, default dirty scope | **1** | `dirty: [" M frozen/a.txt"]` | dirty arm works when its scope reaches the frozen dir |
| A5 | sibling `frozen/b.txt` modified, `--pathspec frozen/a.txt` | **1** | `blob_changed: ["frozen"]` | the literal directory entry is a tree hash and catches existing-path changes |
| A6 | file-only freeze path `frozen/a.txt`, no `--pathspec`, unrelated `other.txt` change | **1** | `touched: [other.txt M]` | whole-tree fallback: a false positive, nothing frozen changed |

## R5 — behavioural mutants M0–M4 (`mutants.py`: `evaluate` wrapped to zero one arm's field)

Driver exit 0 · stdout sha256 `0fd4462007f1f341a2941d3f4cb975c8a4d489b170e4358a55a244cbbc429908`
· 2026-10-28T15:40:54Z.

| mutant | selftest exit | summary | failed case |
|---|---|---|---|
| M0 unmutated | 0 | cases=11 failures=0 | — |
| M1 blob arm dead | **0** | cases=11 failures=0 | none — blob arm not independently killed |
| M2 restored arm dead | **0** | cases=11 failures=0 | none — restored arm not independently killed |
| M3 dirty arm dead | **1** | cases=11 failures=1 | `red-dirty` |
| M4 commit arm dead | **0** | cases=11 failures=0 | none — `red-touched`/`red-restored`/`red-bulk-sweep` are each still met by the blob arm |

## R6 — mutants M5–M6 (`mutants2.py`)

Driver exit 0 · stdout sha256 `f8049aa776837da1cd5b553287ff625a022fe85fb40a68640dc735fc2e965a82`
· 2026-10-28T15:41:08Z.

| mutant | selftest exit | summary | failed case |
|---|---|---|---|
| M5 `--require-pathspec` forced off | **1** | cases=11 failures=1 | `red-dirfreeze-no-pathspec` |
| M6 `covers()` → always true | **1** | cases=11 failures=1 | `red-dirfreeze-no-pathspec` |

## R7 — `restored ⊆ touched` (`restored_shape.py`)

Tamper commit then restore commit in one fixture; `evaluate(d, f, r, ["frozen/"],
["frozen"], False, [], True)`.
exit **1** · stdout sha256 `e70dc979dfe369d04d6d068ed330695c043bbd1594d61ba733e0045a363e34de`
· 2026-10-28T15:41:07Z · `touched_paths ["frozen/a.txt","frozen/a.txt"]`,
`restored ["frozen/a.txt"]`, `blob_changed []`, `restored_subset_of_touched true`.

## R8 — registry recognition, frozen `c2-counter.py` at HEAD

```
python3 -I -B tools/round-45/c2-counter.py --root <lane> \
  --freeze f762b727… --rev HEAD --json-out $S/c2-head.json
```

exit **0** · stdout sha256 `398b6dc6e7f0a76656bf26b1e806e602c7f1346a585658434e4a6ab51aaa6c9d`
· 2026-10-28T15:39:12Z · `scope_size 6`, `registered` = all six,
`unregistered []`, `thin []`, `failing []`.

## R9 — same counter at the freeze (do-nothing shape)

`--rev f762b727…` → exit **1**, stdout sha256
`d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0`
· 2026-10-28T15:41:27Z · `unregistered` = the six scope paths including
`tools/round-45/frozen-path-preflight.py`, `thin []`, `scope_size 6`.

## R10 — frozen `c1-counter.py` at HEAD (cross-evidence only)

```
python3 -I -B tools/round-45/c1-counter.py --root <lane> --freeze f762b727… --rev HEAD \
  --json-out $S/c1-head.json
```

exit **0** · stdout sha256 `0c83a7b3fc340e8f65f6d052b5d1b2905e6e1e4bf4d836788e3257394226ce14`
· 2026-10-28T15:41:27Z · `met_target true`, `failing []`, `rule_blocks 22`,
`block22_present 1`, `block22_rows 10`, `block22_refs 7`.

## R11 — row shape, parsed by the frozen counter's own parser

Proposed row taken from `row.md`, fed to `tools/round-45/c2-counter.py`'s
`parse_rows` / `exits_ok` via `importlib` (read-only import):
`cells 7`, `parsed_rows 1`, `tool tools/round-45/frozen-path-preflight.py`,
`exits_ok true`, `name_matches_scope true`, driver exit 0. This one check's stdout
was not retained to a file (printed inline), so it carries no sha256.
Independent shell count: `awk 'NR==1639{print gsub(/\|/,"|")}'` on the drafted row → 8
pipes = 7 cells; table header `SKILL.md:1634` → 8 pipes = 7 cells.

## R12 — scratch fallback, no write performed

```
env -u HYAKU_SCRATCH -u TMPDIR python3 -I -c 'import tempfile;print(tempfile.gettempdir())'
```

→ `/tmp`. Code path in `scratch_root()`: `$HYAKU_SCRATCH` → `$TMPDIR` →
`tempfile.gettempdir()`. No fixture was created there.

## R13 — selftest leftovers

`ls $S/kaidoku-r45/preflight-selftest | wc -l` → **99** directories, `du -sh
$S/kaidoku-r45` → 15M, after 9 selftest invocations (11 `mkdtemp` fixtures each,
never removed). The instrument has no cleanup path.

## Commands not run (not passed)

- No full-repo gate run with `--pathspec tools/` or any pathspec broader than the
  freeze beyond fixture A3.
- No write to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`.
- No git/jj mutating command; no install or upgrade (nothing needed: python3 and
  git 2.56.0 present).
