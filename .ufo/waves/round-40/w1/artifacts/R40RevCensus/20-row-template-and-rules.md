# SOURCES.md row template and cell rules — R40RevCensus (round 40 w1)

Contract v1 is frozen (kaika, 2026-10-19) and carried in full in
`/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns".
Nothing below changes it; this is the working template for the next row (S123+).

## Exact 11-column row template

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S123 | <Title — canonical URL or DOI; own-work: repo path or command> | <kind> | <A|B|C> | <claim/topic the tier is scoped to> | <exact section/heading/page/line + revision (tag, commit, or date)> | <one grounded learner benefit; rejected rows: REJECTED: <reason>; flip: <what would flip>> | <queued|mined|rejected> | <YYYY-MM-DD> | <YYYY-MM-DD|NNd|symbolic> | <repo-rel path[, path…]|—> |
```

Append new rows immediately after the last existing row, still inside the
`## Registry` section (a row-shaped line outside it is E12), before `## Paths`.

## Per-cell rules (contract + gate semantics, scripts/sources-census.sh)

- **id** — `S` + 3+ digits, next unused, never reused; currently S123 (max S122).
- **source** — `Title — URL/DOI`. No `|` anywhere inside any cell: markdown
  escaping (`\|`) is NOT an escape for this table — awk `-F'|'` still splits, so an
  escaped pipe inflates the field count to 12 cells (NF=14) and the row fails E01.
  Use percent-encoding (`%7C`) if a URL needs a pipe. URLs wrapped in backticks leak
  the closing backtick into the gate's URL normalization (cosmetic W04 noise; S047).
- **kind** — enum: `spec docs paper code tool dataset talk book community own-work`
  (else E05).
- **tier** — `A|B|C`, scoped to `scope`, never global. `community` is never A (E10);
  C never sole support for an admitted entry.
- **anchor** — exact section/heading/page/line **plus revision** (tag, commit, or
  publication date). Never a bare homepage.
- **teaches** — one grounded learner benefit. Rejected rows: `REJECTED: <reason>;
  flip: <what would change the verdict>` (rejected with teaches shorter than 8
  chars is W02). A correction is a NEW row whose `teaches` opens
  `supersedes S0NN —` (this also exempts the URL collision from E04).
- **status** — enum `queued|mined|rejected` only (else E07). `watch` is not a status.
  - `queued` — opened, worth mining.
  - `mined` — cited by ≥1 path in `used-by` (mined with `used-by = —` is W03).
  - `rejected` — kept; a rejection is evidence of taste. Rejected rows are exempt
    from E04 URL-collision findings.
- **opened** — ISO `YYYY-MM-DD` ≤ today in UTC (future or invalid → E08).
- **recheck** — one of: ISO date (validated as a real calendar date), day cadence
  `NNd` (e.g. `90d`, `180d`, `365d`), or a symbolic cadence word (`on-release`,
  `annual`; any `[A-Za-z][A-Za-z0-9 _-]*`). Anything else is E09. Symbolic cadences
  are reported by `overdue`, never judged overdue.
- **used-by** — repo-relative paths (lane root = kaidoku-shokunin), comma-separated
  (`;` is not a separator in the maintained gate — use comma), or `—` when empty.
  Every path on a `mined` row must exist on disk (else E11, one finding per missing
  path). `tier C` + `mined` + non-`—` used-by is W01 (tier inflation of a lead).

## In-place edit policy (contract rule 2 — append-only)

Only `status`, `recheck`, and `used-by` may change in place, and each change is
logged old→new in the round lesson. Everything else: new row (`supersedes S0NN —`).

## Gate cheat sheet (validate mode)

Exit 0 = clean or warnings-only; exit 1 = any E-code or overdue finding; exit 2 =
usage/env/missing registry. Warnings (W01–W04) never change the exit code.
Run from the fleet root: `scripts/sources-census.sh validate --root <fleet-root> kaidoku`;
for a single file: `--file PATH` (E11 resolves paths against `dirname(PATH)/..`,
so a lane file copied outside the lane legitimately floods E11 — see report §6).
