# Round-30 pre-freeze gate: round-29 routed defect 3 (M29-3) as an exit-code check

## Scope and result

Built `prefreeze-gate.py` for routed defect 3 of `corpus/lessons/round-29-verifier-spotcheck.md`: the run-before-freeze step becomes an exit-code check, and a `tools/` path named in a claim's own text that is neither sha256-pinned nor listed under `instrument_supersessions` fails the round. The tool was written in scratch (the L1 integrates it as `tools/round-30/prefreeze-gate.py`); the lane was read-only for this seat.

Acceptance runs against a scratch clone of the lane (`clone` at `4ee65c6771058284aa947a266475839d196ed4d4`):

- **round 29 → FLAGGED, exit 1**, naming `tools/round-28/c1-heldout-naming.py` (freeze `dbd87cfa09eb89306c4e07d3171a4556eb732024`). This is exactly M29-3.
- **round 30 → CLEAN, exit 0** (freeze `4ee65c6771058284aa947a266475839d196ed4d4`).

**[OBSERVATION]** Both runs on the lane itself (`--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only `git` object reads) printed byte-identical stdout and the same exit codes, so the clone result is not an artifact of the clone.

## Tool

- Scratch path: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecPrefreezeGate/prefreeze-gate.py`
- SHA-256: `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542`
- Interface: `python3 -I -B tools/round-30/prefreeze-gate.py --root <LANE> --round <N> [--rev <REV>]`, plus `--selftest`. `--rev` defaults to `HEAD`; `--round` accepts `29` or `round-29`.
- Reads Git objects only (no working-tree read, no write); `GIT_*` environment is stripped and `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0` are forced.

For round `<N>` the gate computes the freeze commit (first commit reachable from `--rev` that adds `.ufo/waves/round-<N>/claims.json`) and checks three things:

1. **pins** — every path recorded under `instruments`/`frozen_inputs` (round-30 shape) and `loaded_by_counter`/`producers_not_counters` (round-29 shape) in the claims file at the freeze commit must be a blob at that commit; a string value is a sha256 and must equal the blob's. A list value records paths without a digest and is checked for presence only.
2. **data** — no path under `corpus/evidence/round-<N>/` that lies in an `envelopes/` directory or is named `runs.tsv` may have been added at or before the freeze commit (run-before-freeze).
3. **tools** — every `tools/*.py|sh|mjs|js` path named in a claim's own strings must be digest-pinned in the claims file at the freeze commit, or listed under `instrument_supersessions` (non-empty `path` and `reason`) in the claims file at `--rev`.

Findings print as `FINDING <code> <path> ...`, sorted by code then path: `PIN_ABSENT`, `PIN_MISMATCH`, `DATA_BEFORE_FREEZE` (with `commit=`), `TOOL_UNPINNED`. Exit: 0 clean; 1 any finding; 2 unevaluable (root not a repository top, no freeze commit, unreadable claims file, bad `--round`).

**[INFERENCE]** The freeze record is what is audited: pins and claim text are read at the freeze commit, so a post-freeze edit to `claims.json` alone does not change the verdict (observed in the first control attempt below); the prescribed M29-3 remedy is a pin or an `instrument_supersessions` entry, which the gate honours from either the frozen file or the file at `--rev`.

## Selftest

Command (2026-10-23T02:46:28Z): `timeout 300 python3 -I -B prefreeze-gate.py --selftest` — exit 0. Full stdout (`selftest.txt`):

```text
ok clean got=code=0 codes=[]
ok round_arg_form got=code=0 codes=[]
ok round_invalid got=code=2 codes=[]
ok pin_absent got=code=1 codes=['PIN_ABSENT']
ok pin_mismatch got=code=1 codes=['PIN_MISMATCH']
ok r29_keys got=code=1 codes=['PIN_ABSENT']
ok r30_list got=code=0 codes=[]
ok r30_list_absent got=code=1 codes=['PIN_ABSENT']
ok envelope_at_freeze got=code=1 codes=['DATA_BEFORE_FREEZE']
ok runs_before_freeze got=code=1 codes=['DATA_BEFORE_FREEZE']
ok data_after_freeze got=code=0 codes=[]
ok other_round_data got=code=0 codes=[]
ok tool_unpinned got=code=1 codes=['TOOL_UNPINNED']
ok tool_pinned got=code=0 codes=[]
ok tool_superseded got=code=0 codes=[]
ok tool_supersession_no_reason got=code=1 codes=['TOOL_UNPINNED']
ok late_pin_not_counted got=code=1 codes=['TOOL_UNPINNED']
ok no_claims got=code=2 codes=[]
ok bad_json got=code=2 codes=[]
ok not_repo got=code=2 codes=[]
selftest cases=20 failures=0
```

**[OBSERVATION]** The fixtures are throwaway `git init` repositories under `tempfile.mkdtemp()`, deleted at the end; they cover both pin shapes (`r29_keys`, `r30_list`, `r30_list_absent`), pins absent/mismatched, data at the freeze commit, data in an earlier commit (with `commit=` attribution checked) and after the freeze, unrelated-round data, tool named unpinned/pinned/superseded/with an empty-reason supersession, a pin added only after the freeze (`late_pin_not_counted` — must still flag), no claims file, invalid JSON and a non-repository root.

## Acceptance runs (clone)

Commands and full stdout at 2026-10-23T02:46:33Z, run from the seat directory:

```text
timeout 900 python3 -I -B prefreeze-gate.py --root clone --round 29
prefreeze round=round-29 freeze=dbd87cfa09eb89306c4e07d3171a4556eb732024 rev=4ee65c6771058284aa947a266475839d196ed4d4 claims=.ufo/waves/round-29/claims.json
FINDING TOOL_UNPINNED tools/round-28/c1-heldout-naming.py
pins=12 present=12 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=6 tools_unpinned=1 findings=1
verdict=FLAGGED
exit=1

timeout 900 python3 -I -B prefreeze-gate.py --root clone --round 30
prefreeze round=round-30 freeze=4ee65c6771058284aa947a266475839d196ed4d4 rev=4ee65c6771058284aa947a266475839d196ed4d4 claims=.ufo/waves/round-30/claims.json
pins=6 present=6 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
exit=0
```

**[OBSERVATION]** Round 29: 12 pins (2 `instruments`, 5 `loaded_by_counter`, 5 `producers_not_counters`) all present and digest-matching at the freeze; 6 tools/ paths named in claim text, of which 5 are pinned and `tools/round-28/c1-heldout-naming.py` is not — the single finding. Round 30: 6 pins (3 `instruments`, 3 `frozen_inputs`), 3 list-recorded paths present, 2 tools/ paths named in claim text, both pinned; no `envelopes/` or `runs.tsv` added at or before the freeze. **[INFERENCE]** Round 30 is green on the pre-freeze side only; the post-freeze checks (instrument revisions, committed envelopes agreeing with live runs) belong to the counters and the round-29 freeze gate, not to this tool.

## Controls

All three were run at 2026-10-23T02:47Z in scratch sandbox clones; no lane state was touched.

1. **Live fail-ability on real round-30 data** (`clone-mut`, sandbox freeze record at `ae36c4b4554d53181f68b227085ff6ab5e1a1580` = `0dbabf78` plus the real `claims.json` with one added probe sentence in `claims[0].limits` naming `tools/round-30/unpinned-probe.py`): `timeout 900 python3 -I -B prefreeze-gate.py --root clone-mut --round 30` → `FINDING TOOL_UNPINNED tools/round-30/unpinned-probe.py`, `pins=6 present=6 … tools_named=3 tools_unpinned=1 findings=1`, `verdict=FLAGGED`, exit 1 (`control-live-round30-unpinned.txt`). So the round-30 CLEAN is not vacuous.
2. **Pre-freeze boundary**: `--root clone --round 30 --rev 0dbabf78b6abbead98d96a720089b8490452a46c` → stderr `prefreeze round=30 unevaluable: freeze_commit_unknown: no commit adds .ufo/waves/round-30/claims.json`, exit 2 (`control-pre-freeze-rev.txt`). Before the claims file exists the gate is unevaluable, not silently green.
3. **M29-3 remedy accepted** (`clone-fix`, sandbox commit `d240bf353bf1cd97254b567a761df20b52f6faf4` appending `instrument_supersessions` with `path=tools/round-28/c1-heldout-naming.py` and a reason to the round-29 claims file): `--root clone-fix --round 29` → `tools_named=6 tools_unpinned=0 findings=0`, `verdict=CLEAN`, exit 0 (`control-fix-supersession.txt`). **[OBSERVATION]** This is the exact remedy the routed defect prescribes, and the gate turns green on it while the frozen round-29 record stays untouched.
4. **Post-freeze edit note**: a first control attempt committed the probe name only after the round-30 freeze commit (`3c97ce18141eb44c623b02199b996369e9678469`) and the gate still printed `tools_named=2 … CLEAN` — because claim text is audited at the freeze commit. **[INFERENCE]** That is the intended semantics (the frozen record is the audited object), demonstrated also by the `late_pin_not_counted` and `tool_superseded` selftest cases.

## Labels

- **[OBSERVATION]** Everything quoted above is tool output produced by the named commands at the stated UTC times; the clone HEAD and both freeze commits were also read with `git log --format=%H --diff-filter=A` in the lane.
- **[INFERENCE]** The gate's coverage claim is bounded to what it checks: pins recorded in the claims file, data paths of the two named shapes under the round's evidence directory, and tools/ paths named in claim strings. It does not verify REA runs, envelopes, entries or PROVINCE lines.
- **[UNKNOWN]** None of the checks was run against any other round, and no carrier or mutant was executed.

## Risks, limits and blockers

- A path recorded only in a list (round-30 `loaded_by_counter` shape) is presence-checked only; there is no digest to compare. If a future freeze wants digest coverage for those paths, it must pin them in `instruments`/`frozen_inputs`.
- An `instrument_supersessions` entry is honoured on non-empty `path` and `reason`; its `commit` and `sha256` fields are not verified (same convention as `tools/round-29/freeze-gate.py`). This matches the routed-defect remedy text ("record a supersession or pin note") but is a weaker check than a commit-verified one.
- Bare file names (no `tools/` prefix) and paths named only in prose outside the claims file are not seen — the round-29 freeze gate's `INSTRUMENT_UNRESOLVED` covers the bare-name class.
- Commit timestamps and authorship are not authenticated; the gate identifies the freeze by the first adding commit.
- No blockers. No REA run, no build/lint/test beyond the tool's own `--selftest`, no tools installed or updated. The lane was not written except for this report.

## Files changed

- Lane: `.ufo/waves/round-30/w1/ExecPrefreezeGate.md` (this report) — nothing else.
- Intended lane integration (by the L1): `tools/round-30/prefreeze-gate.py`, SHA-256 `1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542` (source in scratch, below).

## Retained artifacts and hashes

`sha256sum` at 2026-10-23T02:46:51Z and 02:47:40Z; paths relative to `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecPrefreezeGate/`:

```text
1a4ee3e500bedfb9953c8e469007b653d2958d19c4e2d7297fb0da636434a542  prefreeze-gate.py
50ec7061b0635a0d913493b03e01ad5a828bb79283390f42cd7c3010daa67777  selftest.txt
84637809341cb0833ded94eaf974358a2ba0aa0468a8e83ad868e23b3ea22732  round-29-clone.txt
f45444d60538d065613e2c292eba80a1b1785c7b3481ca9d0d6c32358458071d  round-30-clone.txt
b6d04c2ee3ebd313cc2d92b2b7f4aaf7505caedff1e18146d6cf2c4da93c566e  control-live-round30-unpinned.txt
45c72bb6af66b317fb8cf5a32d0448ca3fef701d479bffb735e9fda0541475be  control-pre-freeze-rev.txt
e6a6e1113b78abb67a66f064024394afc95edab4157eaa86f36f9d6d869afc61  control-fix-supersession.txt
```

Sandbox clones (scratch, deletable): `clone/` (lane at `4ee65c67`), `clone-mut/` (detached at the sandbox round-30 freeze `ae36c4b4`), `clone-fix/` (at `d240bf35`).
