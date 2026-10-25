# R35Audit07 — C1 used-by scope audit (round 35, wave 1)

Seat: `R35Audit07` (leaf; no delegation, no lane writes beyond this report; read-only git probes and private `/tmp` scratch).
Frozen claim target: C1 (coverage) — `tools/round-35/c1-coverage-counter.py`, pin `e28792c7…`; predicate P35-c1 byte-identical in plan-receipt/claims-canonical.json (2323d197) and counter constant (verified both directions, 478 bytes).
Audit question: what does "used-by naming the entry" actually enforce, and can it be spuriously satisfied?

## 1. Evidence — how the counter scores used-by

Source: `tools/round-35/c1-coverage-counter.py:114-131` (`check()`).
- `ROW_RE` parses SOURCES.md 11-column rows; cells index: `[6]=status`, `[7]=opened`, `[9]=used-by`.
- Registry checks per row S125/S129: `status=="mined"`, `opened` starts `2026-10-25`, and `entry in cells[9]` — **substring presence** of the full repo-relative entry path (e.g. `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md`).
- No check that the used-by cell names *only* the entry or lists an existing file; no exact-cell/boundary match; no required separator format.
- Entry side: each entry must open with `source:`/`verified-at:`/`recheck:` lines and its `source:` line must contain the row id (S125/S129). Directionality is per-row enforced (probe P2).

Convention context: existing SOURCES rows (S001, S003, S048, …) use full repo-relative paths, comma-separated, so requiring the full path matches lane convention.

## 2. Executed probes (private /tmp synthetic repos, same frozen counter, `--freeze HEAD`)

| Probe | used-by cell content | exit | verdict |
|---|---|---|---|
| G0 baseline | full paths (selftest-style) | 0 | CLEAN (control green) |
| P1 | stem only, no `corpus/` prefix | 1 | `registry_usedby_missing` both (strict full-path) |
| P2 | rows swapped (S125 names inventory) | 1 | both fail (direction enforced) |
| P3 | path + `, corpus/lessons/round-99.md` | 0 | CLEAN (extra junk tolerated) |
| P4 | empty cell | 1 | both fail |
| P5 | same stem under `corpus/knowledge/x/` | 1 | both fail |
| P6 | `…mapper-contract.md.bak` (contains exact path substring) | 0 | **CLEAN — spurious pass** |
| P7 | `zz<full path>zz` (substring of longer token) | 0 | **CLEAN — spurious pass** |

Falsifications: P6/P7 prove the used-by gate passes when the cell names a near-match string (e.g. `.bak`, wrapped token) rather than the entry itself; the presence-substring test cannot distinguish `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` from a string merely containing it. Reachable only by an implementer who already fabricates the exact path text, but it weakens "naming the entry" to "containing the path text".

## 3. Instrument defects (evidence)

- **Receipt `checks` map always true** — `c1-coverage-counter.py:182`: `checks = {f"c1_{i}": (f not in fails) for i, f in enumerate(["entry_exist","trio","row_citation","registry_rows","province","readme"])}` compares label strings against detailed failure IDs (e.g. `entry_missing:…`, `registry_usedby_missing:…`), which never equal → every per-check flag reports `True` even when the claim fails. Reproduced on the committed control receipt `.ufo/waves/round-35/controls/c1-do-nothing.json` (`checks` all true, `failing` 8 items, `pass:false`) and on probe P6 receipt. Exit code / `pass` / `failing` are correct; only the per-check summary is cosmetic-broken.
- **Selftest red coverage gap** — `selftest()` only removes the provenance trio (entry level); no red fixture mutates used-by/status/opened/province/readme, so the registry branch (and P1/P2/P4/P5 failures) is untested by the instrument's own selftest.
- **Plan-sentence deviation (documentation only)** — `plans/round-35-claims.md` contains no `P35-c1` sentence (grep count 0); the claim-discipline bullet "Predicate sentence is byte-identical in this plan, claims.json, each counter constant and each receipt" is not literally satisfied by the plan file (the plan expresses the predicate as after-state bullets). No scoring impact: the counter compares only against `claims-canonical.json` (verified byte-identical).
- **`instrument_revision` semantic** — `claims-canonical.json` field `instrument_revision=d2729cba…` is the instruments-first *prep* commit (parent = base; contains counters, no claims JSON; counter content hash `cd4ab7e…` ≠ pin). The pinned file hash (`e28792c7…`) matches the worktree and commit `2323d197…` (the first commit adding `claims-canonical.json`, which is also the `--freeze` used in `controls/c1-do-nothing.json`). The `instrument_supersessions` row for `a85ca674…` does not match the pin (hash `018e96d0…`); the canonical freeze commit `2323d197` is the consistent freeze identity.

## 4. Do-nothing control (executed)

Base `aa04633a…`, freeze `2323d197…`:
`python3 -I -B tools/round-35/c1-coverage-counter.py --root . --rev aa04633a… --freeze 2323d197… --json-out /tmp/r35c1-base-receipt.json`
→ exit 1, `C1_FAIL` 8 items (entries, registry rows, province stems, readme filenames), matching the committed control receipt.

## 5. Limits

- No lane writes beyond this report; no VCS mutation; no network; no subagent delegation; no `find`/`du` under `/fast/scratch`.
- Current HEAD has no C1 entry files yet (only the C2 D-3 file `2026-10-25-r34b-…md`), so scoring-state cannot be exercised; audit is against the frozen instrument and synthetic probes only.

## 6. Bottom line

C1's used-by gate is a full-path **substring presence** test (strict about path form, loose about cell contents) — directionally sound and convention-consistent, but falsifiable by near-match strings (P6/P7). No scoring blocker; recommend (a) tightening to exact-cell match or entry-list membership if precision is wanted, (b) fixing the receipt `checks` labels, (c) adding a registry-red selftest case.
