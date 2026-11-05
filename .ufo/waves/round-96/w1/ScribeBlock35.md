# ScribeBlock35 — R96-C2 craft block 35, QUALITY 193/194, and the SKILL.md registry rows (round 96, wave w1, attempt 1)

Seat: `ScribeBlock35` (scribe). Lane: `kaidoku`. Round 96, attempt 1.
Lane repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` — **read-only for this seat**.
Clone used for verification: `/fast/scratch/hyaku/kaidoku-r96/ScribeBlock35/clone`
(`git clone --shared`, HEAD `3baac2ef4b9b2830d299125b8184ca06d9e6584d` — the disclosed
round-96 instrument-supersession commit that follows the declaration
`e4d1f7de9deae83e6d5f78d2d7f0157196002af0`).

Nothing in the lane was edited, created, deleted, staged or committed by this seat. The only
lane paths written are this seat's own directory
`.ufo/waves/round-96/w1/ScribeBlock35/` and this report. No git commit/add/stash/checkout/
switch/reset/pull/push and no jj command was run anywhere. `git diff --stat` in the lane is
empty; `sha256sum -c .ufo/waves/round-96/pins.sha256` is 60/60 OK with 0 mismatches.

## What this seat produced

Three drafts plus a verification receipt, all under
`.ufo/waves/round-96/w1/ScribeBlock35/`:

| file | what it is |
|---|---|
| `block35.md` | the exact markdown to append as craft rule block 35 at the end of `## Queue-drain craft` in `SKILL.md` (after block 34, before `## Config custody for live-probe rounds (SOP)`) |
| `quality-rows.md` | the two exact bullets to append to `corpus/QUALITY.md` (rows 193 and 194) |
| `registry-rows.md` | the ten `SKILL.md` instrument-registry rows to insert immediately before the `<!-- /instrument-registry -->` marker |
| `verify.txt` | every command line, exit code and receipt path of the verification, plus the lane-mutation check |
| `receipts/` | the JSON receipts and stdout captures of every command below |

## The R96-C2 candidate, as drafted

### Craft block 35 (`block35.md`)

Title: `- **35. A kill rule covers every gate its instrument asserts, and a green verdict exists only through a verified receipt.** <!-- kill-rule-gate-coverage v1 -->`

The naming paragraph names the failure class the item asked for — *gates a counter asserts but
its counting commands never reach* — and grounds it in the two routed round-95 defects:

- **M95-h** (`corpus/lessons/round-95.md`): the frozen round-95 kill rule killed 5 of 10
  mutants because its checks never called the counter's `main()` and never ran the probe, so
  M2 (fsync), M3 (forced self-verify), M4 (removed fail-closed exit), M6 (removed revision
  binding) and M10 (probe hard-coded verdict) survived. Evidence pointers:
  `.ufo/waves/round-95/w1/MutationC1.md`, `.ufo/waves/round-95/w1/MutationC1/mutants.md`,
  and the round-96 before receipt `.ufo/waves/round-96/pre/c1-legacy-rule-at-base.json`
  (killed 5 of 10; survivors exactly M2/M3/M4/M6/M10).
- **M95-g** (`corpus/lessons/round-95.md`): six receipt fields unbound, self-verification
  skippable, a run without `--json-out` exiting 0 on a met-True verdict with no receipt.
  Evidence pointers: `.ufo/waves/round-95/w1/CriticC1.md` and
  `.ufo/waves/round-96/pre/c1-v5-admits-unbound-at-base.json`.

The decision table has the header the item specifies, `| observed failure class | signature |
guard | criterion |`, and four body rows whose first cells are **exactly** the four frozen
manifest `row_snippet` strings:

| first cell | criterion |
|---|---|
| `writer durability gate` | `QUALITY 193` |
| `fail-closed exit and forced verdict` | `QUALITY 193` |
| `probe receipt verdict` | `QUALITY 193` |
| `green without a receipt` | `QUALITY 194` |

The `Refs:` line cites `corpus/QUALITY.md rows 193-194 (base e4d1f7de…)`, the three round-96
instruments (`kill-rule-v2.py`, `stop-boundary-repair-battery-v6.py`, `symlink-probe-v2.py`)
and the knowledge entry path `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`.

### QUALITY rows 193 and 194 (`quality-rows.md`)

- **Row 193 (a kill rule covers every gate its instrument asserts)** — carries the manifest
  keywords `instrumented count`, `survives every exit-code diff`, `main()-level negative
  control` and `receipt-content consistency check`, and is grounded in M95-h with its
  evidence pointers.
- **Row 194 (self-verification is mandatory on every exit)** — carries the manifest keywords
  `--json-out is mandatory` and `skipped self-verification`, and is grounded in M95-g with its
  evidence pointers.

Each row ends with a stated limit in the house style (193: coverage is claimed per named
command, not over the instrument in general; 194: the rule binds a receipt to the world it
claims and does not authenticate its provenance — the round-95 limit carried forward).

### Registry rows (`registry-rows.md`)

Ten rows, each in the seven-cell house format (`tool | gate or probe - purpose | verdict map
(exit codes) | self-test command | pinned-value path | write scope | owner`):

- the four **round-95** instruments (`c1-forgery-refusal.py`, `stop-boundary-repair-battery-v5.py`,
  `c1-agreement-v2.py`, `symlink-probe.py`) — the R95-VD-3 debt, owner `kaidoku-r95`, pinned
  values path `.ufo/waves/round-95/pins.sha256`;
- this round's **six** (`stop-boundary-repair-battery-v6.py`, `kill-rule-v2.py`,
  `symlink-probe-v2.py`, `legacy-kill-rule.py`, `r95-unbound-at-base.py`,
  `probe-writer-legs.py`) — owner `kaidoku-r96`, pinned values path
  `.ufo/waves/round-96/pins.sha256`.

Every row carries a verdict map naming all three exit codes under the round-68 `VERDICT_RE`
grammar (so no row is "thin"), the entry command, the selftest spelling with its **measured**
case count, the pinned-value path with the real digest prefix, the write scope, and the owner.
The selftest case counts were measured in this seat's clone, not copied from prose:

| tool | selftest spelling | cases | measured rc |
|---|---|---|---|
| `tools/round-95/c1-forgery-refusal.py` | `--selftest <dir>` | 3 | 0 |
| `tools/round-95/stop-boundary-repair-battery-v5.py` | `--selftest --work <dir>` | 6 | 0 |
| `tools/round-95/c1-agreement-v2.py` | `--selftest <dir>` | 5 | 0 |
| `tools/round-95/symlink-probe.py` | none — no `--selftest` in the tool | — | — |
| `tools/round-96/stop-boundary-repair-battery-v6.py` | `--selftest --work <dir>` | 13 | 0 |
| `tools/round-96/kill-rule-v2.py` | `--selftest --work <dir>` | 4 | 0 |
| `tools/round-96/symlink-probe-v2.py` | none — no `--selftest` in the tool | — | — |
| `tools/round-96/legacy-kill-rule.py` | none — no `--selftest` in the tool | — | — |
| `tools/round-96/r95-unbound-at-base.py` | none — no `--selftest` in the tool | — | — |
| `tools/round-96/probe-writer-legs.py` | none — no `--selftest` in the tool | — | — |

## Verification (every command run in this seat's clone; full detail in `verify.txt`)

The three drafts were applied to the clone only (`SKILL.md` craft section,
`corpus/QUALITY.md` tail, `SKILL.md` before the registry marker), together with a stand-in
`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` taken from the sibling seat's draft
at `.ufo/waves/round-96/w1/ScribeKnowledge/knowledge.md`.

**Frozen counting commands, after side, at the clone worktree**

| # | command | rc | stdout |
|---|---|---|---|
| V1 | `python3 -I -B tools/round-93/craft-citation-semantic.py --root <clone> --manifest .ufo/waves/round-96/manifests/block35-after.json --block 35 --worktree` | **0** | `ok exit 0` |
| V2 | same with `block35-junk.json` | **1** | `failing exit 1` + the four expected keyword reasons |
| V3 | `python3 -I -B tools/round-89/depth-blocks-v2.py --root <clone> --worktree --expect-blocks 35` | **0** | `blocks 35 resolved 35 expect 35 unresolved 0 met=True exit=0` |
| V4 | `python3 -I -B tools/round-91/depth-blocks-v3.py --root <clone> --worktree --expect-blocks 35 --shape-from 35` | **0** | `blocks 35, resolved 35, required-shaped 1/1 expect 35 shaped_required 1/1 unresolved 0 met=True exit=0` |

V1's receipt (`receipts/v1-after.json`) carries `atoms: {block_present: true, marker: true,
shape: true}` and `checked:` four rows with `missing_keywords: []` and citations 193/193/193/194.
V2 fails on the **keyword atoms** of all four rows — not on a missing block — which is the
rubber-stamp control the claim requires.

**Regression and controls**

| # | check | rc | result |
|---|---|---|---|
| R1 | block-34 after-manifest at the modified worktree | 0 | `ok exit 0` — blocks 1–34 undisturbed |
| R2 | block-34 junk manifest at the modified worktree | 1 | the three expected keyword reasons |
| R3/R4/R5 | the three counters' own `--selftest` | 0 / 0 / 0 | `cases=10 failures=0`, `cases=10 failures=0`, `cases=6 failures=0` |
| R6 | block 35 absent at `3baac2ef` | 1 | `block 35 missing (craft has 34 blocks)` |
| R7 | depth v2 + v3 with the r96 knowledge entry **removed** | 1 / 1 | `resolved 34 … unresolved 1` |
| R8 | same with the knowledge entry restored | 0 / 0 | `blocks 35 resolved 35` |

**Structure checks on the drafts** (all true): the marker `kill-rule-gate-coverage v1` is
present; the table is 5 rows × 4 cells with no cell containing a `|`; each of the four
manifest `row_snippet` strings matches exactly one body row whose first cell **equals** it
verbatim; all eight manifest keyword sets are present verbatim in the cited QUALITY row text;
all eight junk-manifest keyword sets are absent from QUALITY 193/194; the applied text is
byte-identical to the seat drafts (`BLOCK-IDENTICAL`, `QUALITY-ROWS-IDENTICAL`,
`REGISTRY-ROWS-IDENTICAL`), and the registry rows sit immediately before the
`<!-- /instrument-registry -->` marker.

**Registry census** (`tools/round-68/registry-conformance.py` `census()` called in-memory on
the base `HEAD:SKILL.md` and on the worktree `SKILL.md`; receipt
`receipts/registry-census.json`): base mismatches 31 / unregistered 19 → after mismatches 21
/ unregistered 9. The ten paths the rows register are **exactly** the ten named instruments.
`duplicate_rows` 0, `row_absent` 0, `thin` unchanged at 12 — none of the twelve thin rows is
mine. (The CLI form of this counter reads `SKILL.md` at `--rev`, so it cannot see an
uncommitted row; the in-memory call is the measurement.)

## Findings the L1 must decide

1. **D1 — the knowledge entry must land in the same commit as craft block 35.** The depth
   counters resolve the block's `corpus/knowledge/…` citation; with the entry absent both go
   red (`resolved 34 … unresolved 1`, R7). This is the round-95 "citation check working"
   behaviour reproduced, and it means the block and
   `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` land together or the after-side
   receipts are red at the landing revision.
2. **D2 — two round-96 tools remain unregistered.** `plans/round-96-claims.md` names
   `tools/round-96/fresh-source2-check.py` and `tools/round-96/gen-forgery-fixtures.py`, and
   the round-68 census will still list both as unregistered after the ten rows land. Both are
   **outside this seat's frozen six**, so this seat did not write rows for them; the L1 must
   decide whether the R95-VD-3 debt is closed for the round or only for the six named
   instruments. (The ten rows do close the debt for all four round-95 instruments.)
3. **D3 — the after-side must be measured at the landing revision.** Every command here ran
   `--worktree` on a clone, because the landing commit does not exist yet. The declaration's
   frozen commands name `--rev <landing>`; per R95-VD-1 the landing receipts must carry that
   revision. This seat cannot produce that receipt.
4. **D4 — the `Refs:` base revision.** The block's `Refs:` line names
   `base e4d1f7de9deae83e6d5f78d2d7f0157196002af0`, the round-96 **declaration** commit, in
   the house style of block 34 (`base 4bda1d1d…`, the round-95 declaration). The knowledge
   entry and the QUALITY rows do not exist at that revision, so if the L1 prefers the
   landing revision in the parenthetical, that is a one-token edit to the draft.

## Out of scope (not done by this seat, deliberately)

- R96-C1's calibration instruments and the mutant table — another seat's claim; this seat
  neither re-ran nor re-declared them.
- Any edit to `SKILL.md`, `corpus/QUALITY.md`, the manifests, the pins or the counter bytes.
  This seat's lane writes are confined to its own seat directory and this report.
- The two round-96 tools named in D2 (outside the frozen six).
- The `tools/round-96/fresh-source2-check.py` S321 source claim — read only.

## Tooling

No package was installed or upgraded. The host's `git`, `python3` (3.14) and `sha256sum` were
sufficient; the scratch clone was made with `git clone --shared` from the lane, and every
fixture was created under `/fast/scratch/hyaku/kaidoku-r96/ScribeBlock35/` with `git -C
"$D" rev-parse --show-toplevel` asserted to equal the fixture dir before use. No mutating
git or jj command was run at any point.
