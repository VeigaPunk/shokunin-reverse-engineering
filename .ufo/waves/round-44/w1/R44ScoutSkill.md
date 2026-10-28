# R44ScoutSkill — SKILL.md / PROVINCE.md drift check for C1+C2, round 44 wave 1

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (base `c29360e3`, HEAD `fc5eb54a` draft claims).
`git diff c29360e3..HEAD -- SKILL.md PROVINCE.md` is empty and `git diff c29360e3 -- SKILL.md PROVINCE.md`
is empty: the worktree files are the base files, so every line number below is the base line.
Read-only; no lane files touched. Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-R44ScoutSkill/`.
Receipts (seat, cmd, exit, stdout sha256, wall): `.ufo/waves/round-44/w1/R44ScoutSkill/receipts.jsonl`
(+ per-check `*.stdout`); check script: `.ufo/waves/round-44/w1/artifacts/R44ScoutSkill/checks.sh`.

## (a) SKILL.md — v4 triage table and instrument registry vs repo state at base

### Mostly-current, verified

- **v4 table structurally intact** (SKILL.md:525-543): 15 data rows, 13 columns incl. `failing handler`;
  SCORECARD `## Round 42` declares "rule block 21, 13 columns, 15 rules" — consistent.
- **Legacy handler rows present** (SKILL.md:466-468): the precedence text enumerates the seven v1-v3
  handler names incl. `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`; the
  `legacy-body-failure` row (line 535) globs failing handler `squashfs_v[123]*`. Accurate at base.
- **C1's oracle choice is SKILL-endorsed**: the `cross-read-legacy` action prescribes cross-reading
  with `unsquashfs` "which reads 1:0-3:0 (measured on the v1, v2 and v3 fixtures this wave)"
  (line 535), citing `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/measurements.md`. C1's
  `unsquashfs` 4.7.5 oracle is thus the reader the table already recommends, not new ground.
  `unsquashfs -version` → `4.7.5` at `/usr/bin/unsquashfs` (receipt `oracle_version`).
- **Registry tool paths resolve at base** for every round-36/37/38/39/40 entry checked
  (receipt `tool_existence`: round-42 `c1-counter.py`, `sqfs-triage-v4.py`, `indep-eval-v4.py`,
  `fixtures.json`, round-40 `sqfs-triage-v2.py`, round-39 tools — all blobs at `c29360e3`).
- **Selftest counts parse**: every registry selftest cell is numeric ("70 cases", "45 cases",
  "42 cases", "51 cases", "43 checks", "8 cases", "7 cases", "13 cases", "6 checks",
  "33/27/35/18 cases" in the r35-39 block, "14/13 cases" round-36, "22/21/17" round-27/28) or an
  explicit `none` — no unparseable cell found. Spot-check: `tools/round-40/sqfs-triage-v2.py`
  defines exactly 45 case functions vs declared "45 cases" (receipt `selftest_count_spot`).
- **The four C1 carriers exist at base** (receipt `carriers_at_base`): all four v1/v2 LE/BE `.bin`
  fixtures are blobs at `c29360e3:corpus/evidence/round-42/c2/fixtures/`; `v2ns-*` siblings also
  present (held-out inputs, consistent with the draft's carrier set being a subset).

### Drift found (C2-rubric candidates; flagged, not judged)

1. **v4 status line is stale** — SKILL.md:523 reads "the table is unscored as a claim and round 43
   re-scores it under P43-C1". Repo state: `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` has
   `met_target true`, `exit_code 0`, `matched 78` of `n 78` (receipt `v4_status`), and
   `SCORECARD.md:3487-3494` records R43-C1 met. The future-tense "round 43 re-scores" and the
   nonstandard claim name "P43-C1" (actual: `R43-C1`, scored on the *calibration* axis, not a depth
   claim) both lag HEAD. Whether the sentence must now read "scored" is a statement the C2 census
   can enumerate; the counter-evidence exists and is green.
2. **Instrument registry ends at round 40** — the last registry heading is
   `### Round-40 instrument registry` (SKILL.md:1555). `tools/round-41/` (13 files),
   `tools/round-42/` (14 files incl. the scored v4 interpreter `sqfs-triage-v4.py`,
   `indep-eval-v4.py`, `c1-counter.py`, `c2-counter.py`, `fixtures.json`, `unblob-logtee.sh`) and
   `tools/round-43/` (7 files incl. `c1-counter.py`, `heldout-gen-v4r43.py`) hold instruments that
   carried scored rounds, none registered (receipts `registry_coverage`, `v4_interpreter`).
   The SCORECARD capability row at :3485 cites `tools/round-43/heldout-gen-v4r43.py` and
   `tools/round-43/c1-counter.py` — live instruments with no registry row. Lazy-registry precedent
   exists (round-36 §8 disclosed the missing r35 rows until round 39 discharged them), so this is
   disclosure debt, not an assertion error per se — but if the rubric enumerates "every scored
   round's counter has a registry row", it fails.
3. **Dangling registry pointers** — round24-C1 row (SKILL.md:1002) names self-invocation
   `tools/selftest.py`: no such blob exists at base or in history (receipt
   `dangling_pointers`). The row's own text mitigates ("post-hoc L1 … not a frozen independent
   oracle; BUILD selftest seats never spawned"), so it reads as historical record — rubric-worthy
   only if pointer existence is checked for self-invocation cells. Likewise `.ufo/waves/hyaku/…`
   (SKILL.md:1100) is a host-external checkout path, unresolvable in-lane.

## (b) PROVINCE.md `## Frontier` — SquashFS surfaces still named Frontier

**Inside `## Frontier` (lines 73-95) itself: zero SquashFS surfaces** (receipt
`province_frontier`: 0 matches for squashfs|sasquatch). The operative SquashFS frontier text is
elsewhere: the `### Round-4 frontier (post-unlock)` sasquatch bullet nested under `## Adjacent`
(lines 142-171), the residual chains at :374/:376/:384/:394/:408, and the **round-42 frontier
note at :416** — the operative statement C1 cites. (Note for the L1: the claims file calls it a
"round-42 frontier bullet"; it is a note paragraph, not a bullet — cosmetic.)

Still-Frontier SquashFS surfaces at base, union of live statements:

| surface | named at |
|---|---|
| **SquashFS v1/v2** (`squashfs_v1`, `squashfs_v2`) | :416 — the surface C1 moves |
| `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies | :416 |
| v4 Broadcom | :416 |
| LE AVM members (`hsqs`), AVM kernel images | :416, :408 |
| nested `filesystem_core` / sub-images below depth 1 | :416, :408 |
| other vendor-mangled images / vendor-mangled sasquatch packages | :408, :157, :422 (round-43 note) |
| `squashfs_v2_nonstandard` (`v2ns`) | **never named in PROVINCE** — only in the claims file :54 |

**C1 scope confirmed**: the move is `squashfs_v1`+`squashfs_v2` only. v3_broadcom/v3_nonstandard/
v4_broadcom/gzip-v3/v2ns all stay — matches the draft's disclosed limits exactly, with one gap:
PROVINCE never names `squashfs_v2_nonstandard`. **Recommendation for the C1 landing**: the
round-44 frontier note should name `squashfs_v2_nonstandard` explicitly (as the claims file does)
rather than leave it under "SquashFS v1/v2" residue, since v2ns is a distinct handler id whose
staying-Frontier reason (no independent reader) differs from v1/v2's promotion. No other PROVINCE
surface asserts v1/v2 held — the move is clean.

## (c) Registry selftest counts and tool files

Covered in (a): all parse; spot-verified 45/45 on `sqfs-triage-v2.py`; all round-36..40 registered
entry-command tool files exist at `c29360e3`. No selftest was *executed* (read-only seat; running
the counters' selftests belongs to control arms). Unexecuted verification is marked [unverified]
in the JSON.

## Remaining unknowns / out of scope

- Whether each declared count equals its script's actual case table beyond the two spot-checks —
  left for the C2 census (running `--selftest` is dev-arm work, not a read).
- `.ufo/waves/round-44/` wave-1 files appeared during this check (L1 installing `carriers.json`,
  sibling `.md`s) — expected live-tree churn, none of it touches the base blobs verified here.
- SKILL.md craft text has no statement asserting v1/v2 *held* or *unsupported* status; no
  contradiction created by promotion.
