# SOURCES.md row template and cell rules — kaidoku registry (pre-freeze, round 39 w1)

Basis: `/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a shokunin learns"
(contract v1, kaika 2026-10-19, frozen), the live header of
`kaidoku-shokunin/corpus/SOURCES.md`, and the gate
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (validated 2026-10-26).

## Exact 11-column template

Header row (as it exists in the registry, line 5 — do not re-add it):

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

New-row shape (fill every cell; 11 cells, no `|` inside any cell):

```
| S118 | <Title> — <canonical URL or DOI; repo path or command for own-work> | <kind> | <tier> | <claim/topic the tier applies to> | <exact section/heading/page/line + revision> | <one grounded learner benefit> | <status> | <YYYY-MM-DD> | <recheck> | <used-by> |
```

- `kind` ∈ `spec · docs · paper · code · tool · dataset · talk · book · community · own-work`
- `tier` ∈ `A · B · C` (scoped to `scope`; `community` never A)
- `status` ∈ `queued · mined · rejected`
- `recheck` ∈ ISO date · `NNd` (e.g. `90d`, `180d`) · symbolic cadence (`on-release`, `annual`)
- rejected rows: `teaches` starts `REJECTED: <reason>; flip: <what would change the verdict>`

## Placement (gate-enforced, discovered by test)

A new row goes **inside the `## Registry` section, immediately after the last row**
(currently S117, registry line 123), **before** the `## Paths` heading. The same
well-formed rows appended at EOF fail with `E12 … row outside Registry section`, exit 1
(artifact `mirror-eof-append-E12-demo.txt`).

## Cell rules

- `id` — `S` + ≥3 digits, the next unused id (next free: **S118**); never reused. No `|` in any cell.
- In-place edits are allowed **only** for `status`, `recheck`, `used-by`, each logged
  old→new in the round lesson (contract rule 2, append-only otherwise). A correction is a
  NEW row whose `teaches` opens `supersedes S0NN —`.
- `status` — `queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) ·
  `rejected` (kept; a rejection is evidence of taste). `watch` is NOT a status → E07.
- `recheck` — ISO date or `NNd` cadence or symbolic (`on-release`, `annual`); anything else
  → E09. `overdue` mode reports ISO/`NNd` rows on/after due date (due = opened + N days)
  and merely REPORTS symbolic cadences, never judging them overdue.
- `used-by` — repo-relative paths (lane-root-relative) of the knowledge entries or lessons
  citing the row, comma-separated, or `—`. Every path must exist on disk → E11 otherwise
  (the gate resolves each path against the lane root; this lane cites 54 distinct paths
  under `corpus/knowledge/`, `corpus/lessons/`, `tools/round-27/`, and lane-root `SKILL.md`).
  A `mined` row with `used-by = —` → W03. A tier-C `mined` row with non-`—` used-by → W01.

## Gate codes (sources-census.sh validate)

Errors (exit 1): E01 row ≠ 11 cells (message prints cells = awk NF−2) · E02 id shape ·
E03 duplicate id · E04 duplicate URL+scope without supersedes · E05 kind enum · E06 tier
enum · E07 status enum · E08 opened not past/present ISO · E09 invalid recheck · E10
community at tier A · E11 used-by path missing on disk · E12 row outside `## Registry`.
Warnings (never change exit/status): W01 tier-C mined with used-by · W02 thin rejected
`teaches` (<8 chars) · W03 mined with `used-by = —` · W04 same URL across scopes.
Exit 2: usage/env/missing registry. Run modes: `validate --root <fleet> <lane>` or
`validate --file <path>` (path base = grandparent dir of the file, i.e. lane root for
`corpus/SOURCES.md`).
