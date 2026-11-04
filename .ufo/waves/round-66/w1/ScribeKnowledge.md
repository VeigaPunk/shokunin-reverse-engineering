# ScribeKnowledge — round 66, w1

Seat: scribe (leaf, no dispatch). Scope: draft the round's knowledge entry body, its
`corpus/README.md` coverage-map row, and the routed round-65 entry erratum. Prose only; the L1
lands them; nothing under `corpus/` was edited.

## Behavior

Three drafts written to the seat directory, each grounded in receipts read on disk and in the two
frozen counters' own code:

- `.ufo/waves/round-66/w1/ScribeKnowledge/entry.md` (180 lines, sha256
  `c94858e4fbed48283f29076657fdfa4672c80e34b8c532e8b3c9dc03f0dbe4e1`) — the
  `corpus/knowledge/2026-11-03-r66-closure-boundary.md` body: provenance trio first, what the two
  counters decide with every claim clause mapped to its emitted field, the five C1 arms and three
  C2 conditions as two tables, measured numbers at the base and at the freeze with receipt paths,
  and a `## Limits` list.
- `.ufo/waves/round-66/w1/ScribeKnowledge/map-row.md` (1 line, sha256
  `0c748bb43b0a541eb488304356ae4fcd27f175638989df3796a5d4b7a113868a`) — one pipe-free
  coverage-map row naming `2026-11-03-r66-closure-boundary`.
- `.ufo/waves/round-66/w1/ScribeKnowledge/erratum.md` (17 lines, sha256
  `04301fee7e46e4ce422a9b8a3da8c2bd6437e43bddcbca32b9cb1b19c2e111b1`) — appended-correction
  wording for the r65 entry's `venv identity 4` group count, no rewrite instruction.

## Evidence read (what each established)

- `plans/round-66-claims.md` and `.ufo/waves/round-66/claims.json` — claim predicates, declared
  atoms A0–A9. A8 requires this entry to cite the round's SOURCES row; the row was absent (below).
- `tools/round-66/closure-boundary.py` — arm conditions, emitted field names, exit codes, the
  fixture/real-manifest split, `skip_run_receipt`'s `closure: null`. Re-hashed:
  `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` (matches the pin).
- `tools/round-66/coverage-selfcheck.py` — `RECIPE_A_KEYS`, `recipe_hidden`, atom construction,
  `mismatches` sum, `ok` conjuncts, exit codes, the extracted-block subprocess. Re-hashed:
  `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa` (matches the pin).
- `tools/round-65/jsc-closure-matrix.py` `CLOSURE` — re-hashed
  `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` (matches the pin). Count
  command: `python3 -I -B -c "import importlib.util; s=importlib.util.spec_from_file_location('m','tools/round-65/jsc-closure-matrix.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(len(m.CLOSURE), sum(1 for k in m.CLOSURE if k.startswith('venv/')))"`
  → `27 5`, exit 0; `len(CLOSURE) + 3` → `30`.
- `SCORECARD.md:88-120` — the committed recipe-A block; its `get()` helper calls `git show` for
  README, SKILL and every cited knowledge file (grounds the `--equiv` cost limit).
- Base receipts: `l1/pre/dryrun-c1-verify.json` (5/5, exit 0), `l1/pre/dryrun-c2-selfcheck-at-base.json`
  (exit 1), `l1/controls/c1-do-nothing.json` (1/5), `l1/controls/c2-do-nothing.json` (0/3),
  `l1/pre/selftest-c1.txt` (30 cases, 0 failures), `l1/pre/selftest-c2.txt` (26 cases, 0 failures),
  `l1/records/r66-order.txt` (carry-in ancestor PASS, exit 0).
- Freeze receipts: `w1/ExecClosure/verify.json` (5/5, exit 0), `w1/ExecClosure/manifest.json`
  (entries 30, count_ok true, exit 0), `w1/ExecClosure/skiprun.json` (closure null,
  closure_claimed false, exit 1), `w1/ExecCoverage/selfcheck-at-base.json` (exit 1),
  `w1/ExecCoverage/selfcheck-at-freeze.json` (exit 1), `w1/ExecCoverage/equiv-at-base.json`
  (equivalent true, diffs {}, exit 0), `w1/ExecCoverage/recipe-a-at-base.json` (mapped 142/145,
  coverage 9.79, depth 10.0 27/27), `w1/ExecCoverage/recipe-stem-at-base.json` (145/145,
  mismatches 0).
- Scout row: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-66/w1/ScoutSources/row.md`
  absent (`ls` → No such file or directory); `find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-66 -name row.md`
  returned nothing. Registry max id: `S266` (`grep -oE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
  → 173 rows, `sort -V | tail -1` → `S266`).

## Findings for the L1

1. **A8 is not yet satisfiable.** The scout's `row.md` was not on disk at any read, so
   `entry.md` cites `S???` and states why (seat dir absent, no `row.md` under the round, registry
   last row S266 ⇒ next free id S267, not assigned). It asserts no Gate quote. Landing this entry
   before the SOURCES row lands would fail A8; replace `S???` with the scout's id and the row's
   ≤25-word located quote when it lands.
2. **R66-C2 is not green at the freeze.** `w1/ExecCoverage/selfcheck-at-freeze.json` (exit 1)
   reports `recipe_a_equivalent` true, `recipe_a_hidden` 3, and `mismatches` 1 — `A2-cited-fraction`
   claimed `[142, 142]` against observed `[145, 145]`. The `## Owned axes` row is still the stale
   `142/142`, so the predicate's measured-revision clause is unmet at `7b63dd5d`. The after-arm is
   the landing's row repair; `entry.md` records the freeze number and claims no landing result.
   The base receipts show the same 1 (as the claim expects).
3. **R66-C1 is green at the freeze.** `w1/ExecClosure/verify.json` 5/5 exit 0; the manifest mode
   is 30 entries, `count_ok` true, empty `cache_before`/`cache_present`, no findings, exit 0; the
   skip arm emits `closure: null`, `closure_claimed: false`, exit 1.
4. **Erratum arithmetic verified.** `CLOSURE` holds 27 keys, 5 of them under `venv/`; with the
   three external pins the total is 30. The r65 table's group slots are 9 + 12 + 5 + 2 + 3 = 31
   over 30 distinct paths because the probe is pinned once under `artifacts` and again under
   `harness`. `erratum.md` states this as an appended correction, not a rewrite.
5. **Map row is one row, no pipe inside any cell**, names `2026-11-03-r66-closure-boundary`, and
   states the freeze status honestly (C1 5/5; C2 still stale at base and freeze).

## Gates honored

- No git or jj mutating command was run. Read-only only: `git log`, `git rev-parse HEAD`.
- Writes only to the three seat artifacts and this report. No scratch directory was created
  (nothing under `/fast/scratch/hyaku/kaidoku-r66/ScribeKnowledge`), no file under `corpus/`,
  `.ufo/state/`, the fleet root, `~/.local/share/kaidoku-jsc`, or `shokuknow` was touched.
- No network fetch, no package install, no pacman, no subagent dispatch. The toolchain was not run.

## Out of scope / not run

- The counters and their selftests were not re-run; their counts are cited from the committed
  receipts (`l1/pre/*`, `w1/Exec*`), and `entry.md` says so.
- `corpus/README.md`, `corpus/SOURCES.md`, the r65 knowledge entry and the SCORECARD were read,
  never edited. The L1 performs the landing, including the Owned-axes row repair that C2's
  after-arm needs.
- The landing after-arm for C2 was not measured at this seat.

## Artifact paths

- `.ufo/waves/round-66/w1/ScribeKnowledge/entry.md`
- `.ufo/waves/round-66/w1/ScribeKnowledge/map-row.md`
- `.ufo/waves/round-66/w1/ScribeKnowledge/erratum.md`
- `.ufo/waves/round-66/w1/ScribeKnowledge.md` (this report)
