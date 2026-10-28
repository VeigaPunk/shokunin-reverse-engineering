# ScribeReport — round 48 scoped findings

Seat: ScribeReport (leaf member, no dispatch). Axes judged: coverage, depth, calibration.
Declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`; base
`61b87d742032e65fca9c38267d7d6ed7e555edad`. Claims file read in full before any command:
`plans/round-48-claims.md` (tag D3D6, 167 lines).

## Behavior

Read `plans/round-48-claims.md` in full, the wave-1 receipt corpus (25 `.md` seat reports +
9 `receipt.json` files + fixture/JSON sidecars under `.ufo/waves/round-48/w1/`, the 6 control
JSONs under `.ufo/waves/round-48/controls/`, `w1/swarm-registry.json` (73 registered seats,
~27 reporting), and `l1/block25.md` + `l1/scores/probe-record47.json`), then drafted the
round report's `## Work performed` (21 bullets) and `## Landed changes` (5 pending slots),
each bullet carrying an evidence pointer, at
`.ufo/waves/round-48/w1/ScribeReport/report-draft.md`.

## Gates

- Read-only on the lane tree: honored — two files written, both inside the seat's allowed
  paths. No frozen byte, `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`,
  `.ufo/state/`, sibling lane, or fleet file touched. No git/jj mutating command run.
- Fixture discipline: not needed (drafting/analysis seat); no `git init` performed.
- Disk guard: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` run before
  the drafting pass — `/tmp` 19%, `/var/tmp` 38%, `/fast/scratch/hyaku` 32% (exit 0,
  2026-10-28).
- Exit-code semantics: no counter was re-run by this seat (receipts were read, not
  re-executed — honest-capture rule); every claim below is attributed to the receipt that
  observed it. Counters as measured by the wave: C1 exit 1 at freeze, exit 2 at base;
  C2 exit 1 at freeze / exit 0 under `--profile v2`.
- `Report:` trailer path written: `.ufo/waves/round-48/w1/ScribeReport.md` (this file).

## Touched surfaces

- `.ufo/waves/round-48/w1/ScribeReport/report-draft.md` (created, 11.9 KB)
- `.ufo/waves/round-48/w1/ScribeReport.md` (this report)
- Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeReport/` created (empty; removed before yield).

## Findings the L1 should weight when landing

1. **C1 has a frozen counter defect that blocks green by construction.** Clause 8's census
   equality compares `census_rederive()` (a dict) to `doc["paths"]` (a list)
   (`meanings.py:290-298`, `:429-444`) — false even when the derivation is byte-exact
   (C1Census proved the derivation is exact). No landing satisfies C1 as frozen; reconcile
   per the freeze amendment procedure or document the clause as unsatisfiable. Evidence:
   `w1/C1Census.md`.
2. **Three more C1 attack surfaces** (source-level, none executed end-to-end):
   `registry_rows()` misses `|  `-backtick rows (forged row escapes all checks);
   `0=not met; 1=violation; 2=usage` is classified success/not-met/unevaluable;
   probe/library instruments have no real three-way verdict partition. Evidence:
   `w1/CritAxis.md`, `w1/C1Gold.md`, `w1/C1RowsB.md`, `w1/C1Semantic.md`.
3. **Registry gap at freeze is exactly 2 rows** (40 vs 42 census paths: `meanings.py`,
   `record2.py` missing) — the registry landing is bounded. Evidence: `w1/C1Census.md`.
4. **C2 failing set at freeze is exactly 3 clauses** — round-47 seat atom/correction,
   round-48 corrections heading, unbacked `exempted 2` — and C2Quote already proved the
   `exempted 2`→1 `quote` correction clears `quotes_bad`; the C2 landing checklist is
   mechanically determined. Evidence: `w1/C2Floor/receipt.json`, `w1/C2Quote/report.md`.
5. **Both batteries are gated on genuine-green** and report `skipped` at freeze; the wave
   produced zero forgery measurements. The kill rules are untested — first battery numbers
   only exist post-landing. Evidence: `w1/C2Battery.md`, `controls/ctl-c1-0-do-nothing.json`.
6. **Provenance asymmetry**: the round-47 oracle executes from `--rev` bytes (stub-swap
   proof), but `tools/round-46/gate.py` is worktree-imported — C2 verdicts are not fully
   pinned to committed infrastructure. Evidence: `w1/C2Oracle.md`, `w1/C2OracleLimit.md`.
7. **Freeze-identity discrepancy, unresolved**: `git log --format=%H -1 --
   plans/round-48-claims.md` returns `ac02a79ff84133220d01ce3b59a4789b7004dbc5`, not the
   declared freeze. The claims file's own re-derivation sentence yields the *latest*
   claims-touching commit; a rev carrying different claims bytes exits 2
   `frozen_path_changed`. L1 must reconcile before citing `plans/round-48-claims.md@<freeze>`.
   Evidence: `w1/CritClaims.md`, `w1/C2LandingGate.md`.
8. **Worktree hazard**: `tools/round-48/meanings.py` shows dirty in the worktree (a
   pre-existing wave-side change, not this seat's); a receipt already recorded
   `frozen_worktree_dirty`. Post-landing measurements need a clean frozen pathspec or the
   counter's restore path will drive the result. Evidence: `w1/C1Meaning/receipt.json`.
9. **Honest negatives** carried into the draft verbatim: gold-artefact fixture, permuted-arm
   fixture, stale-score attack, tautology pair, v2-profile C1 control, landing preflight —
   all "not run", none presented as passed. Evidence: `w1/C1Gold.md`, `w1/C1IdsArms/report.md`,
   `w1/C2Axes.md`, `w1/C2Floor.md`, `w1/C1V2.md`, `w1/C2LandingGate.md`.

## Out of scope

No landing edits, no counter fixes (frozen), no LOG/SCORECARD writes, no fixture repos, no
battery execution (gated pre-landing), no installs (pacman paused host-wide; nothing needed).

## Artifact paths

- Draft: `.ufo/waves/round-48/w1/ScribeReport/report-draft.md`
- Report: `.ufo/waves/round-48/w1/ScribeReport.md`
- Evidence corpus read: `.ufo/waves/round-48/w1/*.{md,json}`, `.ufo/waves/round-48/controls/*.json`
