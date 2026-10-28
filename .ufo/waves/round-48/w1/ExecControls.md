# ExecControls — round-48 control re-verification at the declared freeze

Seat: ExecControls (w1). Assignment: re-run and record the round's controls at the
declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`
(`ctl-c1-0-do-nothing.json`, `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v2-profile.json`),
and verify the committed ones under `.ufo/waves/round-48/controls/` reproduce
byte-identical JSON (modulo timestamps). Report dir:
`.ufo/waves/round-48/w1/ExecControls/receipts/`.

## Headline

- **All three committed controls reproduce byte-identical** (`cmp` exit 0, same
  sha256) at `2026-10-28T18:52:46Z`, lane HEAD `0f06251b`. No drift in any scored
  field.
- **Three discrepancies found**, none silent, all recorded below: (1) the frozen
  interpreter moved A1→A4 after the control receipts were committed — output happens
  to stay identical for the do-nothing card, but this is luck of the code path, not
  pinning (R47-CL1 class); (2) `ctl-c1-1-v2-profile.json` is named in the claims
  `## Controls` list but **absent** from `.ufo/waves/round-48/controls/`
  (my supplementary rerun receipt is committed here instead); (3) `--no-battery`
  is a **no-op under `--profile v2`** — both flag forms of `ctl-c2-1` produce the
  same bytes.

## Commands (exact) and receipts

Every run: `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`HYAKU_SCRATCH=TMPDIR=/fast/scratch/hyaku/kaidoku-r48/ExecControls`,
`python3 -I -B`, `--root` = lane root, `--freeze = --rev = dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`.

| run | command tail | exit | stdout sha256 (= receipt sha256; `emit` writes what it prints) | UTC |
|---|---|---|---|---|
| c1-0 | `meanings.py --freeze $F --rev $F --json-out …/ctl-c1-0-rerun.json` | 1 | `594e618c…330a` | 18:52:46Z |
| c2-0 | `record2.py --freeze $F --rev $F --json-out …/ctl-c2-0-rerun.json` | 1 | `f0bf3d66…ba2c` | 18:52:46Z |
| c2-1 (no-battery) | `record2.py … --profile v2 --no-battery --json-out …/ctl-c2-1-nobattery-rerun.json` | 0 | `9a5d2646…1510` | 18:52:46Z |
| c2-1 (battery) | `record2.py … --profile v2 --json-out …/ctl-c2-1-withbattery-rerun.json` | 0 | `9a5d2646…1510` | 18:52:46Z |
| c1-1 v2 (supplementary) | `meanings.py … --profile v2 --no-battery --json-out …/ctl-c1-1-v2-rerun.json` | 1 | `78ec19c9…6897c0` | 18:52:46Z |

## Committed-vs-rerun byte comparison

| committed control | rerun receipt | result |
|---|---|---|
| `ctl-c1-0-do-nothing.json` (532 B, `594e618c…330a`) | `ctl-c1-0-rerun.json` | **byte-identical** |
| `ctl-c2-0-do-nothing.json` (2011 B, `f0bf3d66…ba2c`) | `ctl-c2-0-rerun.json` | **byte-identical** |
| `ctl-c2-1-v2-profile.json` (746 B, `9a5d2646…1510`) | `ctl-c2-1-nobattery-rerun.json` | **byte-identical** |
| `ctl-c2-1-v2-profile.json` (same) | `ctl-c2-1-withbattery-rerun.json` | **byte-identical** (see discrepancy 3) |

Receipts carry no timestamps and no machine state, so the byte equality is
unqualified — there is no "modulo timestamps" remainder.

## Semantics of what reproduced

- `ctl-c1-0` exit 1: `marker_occurrences 0 != 1`, `marker_block_count 0 != 1`,
  `rule_blocks 24`, `battery.skipped` — the do-nothing red the claims file predicts.
- `ctl-c2-0` exit 1: `failing` = the round-47 seat-atom floor miss, no
  `## Record corrections — round 48`, `quoted numbers with no backing receipt: 1`
  (the `exempted 2` misquote against `c1-at-A7.json`/`c2-at-A7.json`);
  `axis_score_cells` holds `coverage` and `depth` rows — the A1 clause is live, not
  vacuous (`ctl-c2-a1-before.json`'s `axis_score_cells {}` confirmed reproduced only
  as history).
- `ctl-c2-1` exit 0 under v2: `met_target true`, oracle `atoms 44`, `mismatches []`
  — the ported profile green, i.e. the hole the round exists to close.
- `ctl-c1-1-v2` (my supplementary receipt, the missing committed control) exit 1:
  `failing ["marker_block_count 0"]`, `profile v2` — v2 still red on the do-nothing
  card because the do-nothing red is a block-absence, not a forgery.

## Discrepancy 1 — the frozen interpreter moved after the controls were committed (R47-CL1 class)

Timeline (lane `git log`):

- `15:41:23` `dc73587a` A1 — declared freeze; `meanings.py` blob `c33afbad`.
- `15:46:40` `ac02a79` A2 — declared freeze; drops the `not NOTMET` guard in `meaning_classes`.
- `15:50:03` `f3a7afc` A3 — declared freeze; `census_rederived_equal: derived == doc["paths"]`
  → `derived.get("paths") == doc["paths"]`.
- `15:52:02` `0f06251b` A4 — declared freeze; adds `NEGATED` for `0=not met` and
  `ROW_START` for indented rows; `meanings.py` blob `036709a9`.

`meanings.py` executes its **worktree** code against a `--rev` artefact
(`gate.show` reads committed bytes, `sys.path` imports and `meaning_classes`/
`registry_rows` run from the worktree). The committed controls were therefore
scored by the A1 interpreter; my rerun at `18:52:46Z` was scored by the **A4**
interpreter against the identical `--rev dc73587a` artefact. The output is
byte-identical only because every A2–A4 change sits *after* the early return for a
missing marker block (A3's census comparison and A4's classifier/row-parser fixes
are clause-8 code). After the L1 lands block 25, the same controls re-measured at
the landing revision will score through the A4 classifier, not the A1 one that
generated the committed receipts — the receipts carry no `interpreter_sha256`
field, so the drift is invisible inside them. The C1 block's own
`interpreter_sha256` pin partially covers this for the *block*, but the control
receipts remain unpinned. Also observed live: during the A4 in-flight window
(18:51:43Z pass) all five first-pass runs exited **2 `frozen_worktree_dirty`**
with `dirty: ["tools/round-48/meanings.py"]` — the freeze guard works
(capture: `receipts/dirty-window-capture.txt`).

Additional nuance: `git log -1 -- plans/round-48-claims.md` (the claims file's own
freeze re-derivation rule) now yields `0f06251b` (A4), not the wave's declared
`dc73587a`; both controls' `frozen_path_changed []` is only honest for the pinned
`--freeze` value. The last three freeze commits each declare themselves "the
declared freeze"; the wave spec pins `dc73587a`, which is what this report scored.

## Discrepancy 2 — `ctl-c1-1-v2-profile.json` never committed

The claims `## Controls` list (at every revision since `7fe1133`, including HEAD)
names `ctl-c1-1-v2-profile.json`; `.ufo/waves/round-48/controls/` does not contain
it. Present: `ctl-c1-0`, `ctl-c2-0`, `ctl-c2-1`, `ctl-c2-a1-before`,
`ctl-c1-a3-simulation` (added 15:50 by the A3 commit), `probe-c2-v2/v3`.
My v2 rerun (`ctl-c1-1-v2-rerun.json`, exit 1, `marker_block_count 0`) stands in
for the missing control's measured value — it shows v2 do-nothing red, consistent
with "forgeries green" being a post-landing clause, not a do-nothing one. Also:
the entire `controls/` directory is still **untracked** (`git status`: `??`),
i.e. wave evidence not yet committed by any lane commit — "committed control" in
this report means "present in the lane tree".

## Discrepancy 3 — `--no-battery` is a no-op under `--profile v2` (both counters)

`record2.py evaluate()` runs `run_battery` whenever `code == 0` regardless of
profile, then re-scores — but `score()` early-returns at the
`if not hard:` line before the battery block is merged. Proof: the with-battery
and `--no-battery` v2 runs are byte-identical (`9a5d2646…1510`, both exit 0,
no `battery` key). Consequences: (a) the committed `ctl-c2-1` cannot reveal which
flag produced it; (b) `run_battery` still executes and is discarded — silent work
and a silent channel (a crash inside `run_battery` under v2 → exit 2 would look
like a profile failure, not a battery failure). `meanings.py` has the identical
shape. Minor instrument defect, flag for routing; it does not change any control
verdict.

## Environment / provenance

- Python `python3` (system), no installs; pacman paused — none needed.
- `disk-guard.sh status` pre-pass: `/fast/scratch/hyaku` 32% used, 546.7 G free.
- All reads were committed bytes via the counters' own `gate.show`; worktree state
  at measurement: clean under `tools/round-48/` and `plans/round-48-claims.md`
  (`git status --porcelain` empty for those pathspecs at 18:52:46Z).
- No writes outside `.ufo/waves/round-48/w1/ExecControls/` + scratch; no git
  mutations; scratch `/fast/scratch/hyaku/kaidoku-r48/ExecControls` removed on yield.

## Not run (out of this seat's scope)

Battery-forgery attacks (C1Battery/C2Battery seats), census re-derivation walk
(C1Census), landing-revision re-measurement (post-landing, L1).
