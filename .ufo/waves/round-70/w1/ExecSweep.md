# ExecSweep — round-70 w1 standing receipts duties (seat ExecSweep-2)

Date: 2026-11-04. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Measured state: freeze commit `4737a542ae3b1b910d8fe43efbd572bc578b07c6` (the operative freeze, the
commit that first adds `.ufo/waves/round-70/claims.json`). Lane HEAD at run time:
`67217e0987a2b31253d0b77f1490a1bfd031575a` (one commit past the freeze; `git diff --stat
4737a542… -- SKILL.md tools/round-56/receipt-audit.py tools/round-57/record-receipt-audit.py
tools/round-51/census3.py` empty, so the audited surfaces are byte-identical between the freeze
and the worktree).

Execution discipline (no mutation anywhere): each tool was read out of git objects at the freeze
(`git show 4737a542…:<path>`) into scratch `/fast/scratch/hyaku/kaidoku-r70/ExecSweep/freeze/` and
executed from those copies with `python3 -I -B`; `--root` pointed at the lane repo; all git reads
are object reads (`rev-parse`, `cat-file`, `ls-tree`); nothing was written outside my findings dir
and my scratch; scratch `HYAKU_SCRATCH` was set under my scratch root; no `/tmp` use.

Executed tool bytes (sha256, all match their standing pins):

| tool (freeze copy) | sha256 |
|---|---|
| tools/round-56/receipt-audit.py | `897df532d4707fc5c190b8c52b4c33176efe07ac878839efb14de56820d72512` |
| tools/round-57/record-receipt-audit.py | `3a5fff9adcb472e2cfb8ba42225520f49539b0493c2c144c9684fc296add8151` |
| tools/round-51/census3.py | `a7538e5f5174b5f69cc7537fc1bcdf97cc2f062747123d0eb6f57e60e9acc7c0` |

## Registry rows read (SKILL.md, round29-freeze and later)

- `tools/round-56/receipt-audit.py` — SKILL.md line 1846: gate, R56-C2 depth; freeze-receipt
  completeness; selftest `python -X utf8 -I -B tools/round-56/receipt-audit.py --selftest` (9
  in-memory cases); verdicts 0 clean / 1 RECEIPT_ABSENT|RECEIPT_AMBIGUOUS / 2 could-not-evaluate.
- `tools/round-57/record-receipt-audit.py` — SKILL.md line 1847: gate, R57-C2 depth; named-path
  completeness over one `##`-heading section of RECORD's committed bytes; selftest 9 in-memory
  cases; verdicts 0 clean / 1 NAMED_PATH_ABSENT / 2 could-not-evaluate (zero paths named is
  unevaluable, never vacuously clean).
- `tools/round-51/census3.py` — SKILL.md line 1840: gate, registry-inventory equality only;
  entry `python3 -I -B tools/round-51/census3.py --root LANE --rev REV --check`; verdicts 0 equal /
  1 missing-extra-duplicate / 2 malformed-unavailable.

## Runs (commands, exit codes, verdicts verbatim)

Environment for every run: `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r70/ExecSweep/hyaku-scratch`,
cwd = my scratch root, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`--rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6`.

1. `python3 -I -B $SCRATCH/freeze/tools/round-56/receipt-audit.py --selftest`
   → exit 0. Verbatim: `receipt-audit selftest: extraction 2 + audit 7 cases, failures 0`
2. `python3 -I -B $SCRATCH/freeze/tools/round-57/record-receipt-audit.py --selftest`
   → exit 0. Verbatim: `record-receipt-audit selftest: extraction 3 + section 2 + audit 4 cases, failures 0`
3. `python3 -I -B $SCRATCH/freeze/tools/round-51/census3.py --selftest`
   → exit 0. Verbatim: `{"cases": 20, "failures": [], "selftest": {"cli-clean": true, ..., "unknown": true}}` (all 20 true)
4. `python3 -I -B $SCRATCH/freeze/tools/round-56/receipt-audit.py --root $LANE --claims
   .ufo/waves/round-70/claims.json --rev 4737a542… --json-out <findings>/receipt-audit-round-70-at-freeze.json`
   → exit 1, verdict `"failed"`, `receipts_checked: 9`, findings (verbatim):
   - `{"finding": "RECEIPT_ABSENT", "name": ".ufo/waves/round-70/l1/scores/c3-at-landing.json", "scope": "repo"}`
   - `{"finding": "RECEIPT_ABSENT", "name": "package.json", "scope": "round-70"}`
5. `python3 -I -B $SCRATCH/freeze/tools/round-57/record-receipt-audit.py --root $LANE --record
   SCORECARD.md --heading "Round 70" --rev 4737a542… --json-out <findings>/record-receipt-audit-round-70-at-freeze.json`
   → exit 2 (no json-out written; the tool returns before writing on this path). Verbatim stderr:
   `2 could-not-evaluate: no '## ' heading matching 'Round 70' in SCORECARD.md at 4737a542ae3b1b910d8fe43efbd572bc578b07c6`
   (verified independently: `git show 4737a542…:SCORECARD.md | grep -c '^## Round 70'` = 0)
6. `python3 -I -B $SCRATCH/freeze/tools/round-51/census3.py --root $LANE --rev 4737a542… --check`
   → exit 2 (no stdout). Verbatim stderr/JSON: `{"error": "registry row must have seven cells", "exit": 2}`

Exit-code summary (also in `audits-summary.txt`): r56-selftest 0, r57-selftest 0, r51-selftest 0,
receipt-audit 1, record-receipt-audit 2, census3-check 2.

## Classification of the two container-naming findings (duty item 2)

NOT a clean bill anywhere; nothing here was recorded as clean.

- Expected-pending: `.ufo/waves/round-70/l1/scores/c3-at-landing.json` (run 4). The landing
  receipt is measured at the landing commit and committed with the record (container atom A9);
  it cannot exist at the freeze. Same class: run 5's exit 2 — the `## Round 70` SCORECARD section
  lands with the record commit, so the named-path audit is could-not-evaluate at the freeze. Both
  are the freeze-state shape the lane contract predicts.
- Defect named (will persist past the record): bare-name finding `package.json` (run 4). The
  container's frozen atom A8 sentence "the REA package is pinned by version 6.5.0 plus
  package.json sha256 a5003023…" trips the tool's bare-name grammar
  (`[A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:txt|json|tsv)`), and `package.json` resolves to zero paths
  under `.ufo/waves/round-70/` — the REA pin lives in the REA package, not the wave tree. The
  container is frozen and cannot be reworded, so the landing receipt-audit over this container
  will still exit 1 with this finding unless the record discloses it (the r64/r68 FLAGGED-row
  pattern). Flagging now so the record author discloses rather than discovers.

## Defect named: registry census unevaluable since round 69 (run 6)

`census3 --check` at the freeze exits 2 before any comparison because the frozen parser
(`registry_paths`, strict 7-cell rows, no GFM unescaping — the S258 lineage) hits the four
round-69 registry rows, which carry **eight** cells:

- SKILL.md line 1862 `` `tools/round-69/packed-elf.py` `` — 8 cells
- SKILL.md line 1863 `` `tools/round-69/mutation-check.py` `` — 8 cells
- SKILL.md line 1864 `` `tools/round-69/contract-probe.py` `` — 8 cells
- SKILL.md line 1865 `` `tools/round-69/controls.py` `` — 8 cells

Each splits as tool | purpose | verdicts | entry | evidence | **pins** | bounds | lane — the pins
material (e.g. `UPX_SHA256_PIN, UPX_VERSION_PIN, the CARRIERS table …`) was given its own cell
where the 7-cell schema (header line 1782 is 7 cells; census3's own selftest row grammar is 7
cells) folds it into evidence/bounds. Lineage check from git objects: the same four 8-cell rows
exist at the base `5cc845ca…` and already at the round-69 declaration `616a5f2f…` — the registry
census has been could-not-evaluate since the round-69 rows landed, and no round-69 record
disclosed it. No round-70 rows exist in the registry at the freeze (0 rows naming round-70; the
six round-70 instruments get their rows at the record commit), and my full scan of the 84-row
block at the freeze found exactly these four malformed rows — no other row is malformed, so the
census becomes evaluatable the moment those four rows are folded back to 7 cells (a record-time
registry edit, not a post-freeze instrument change).

Note on the duty phrasing "the registry census over corpus/SOURCES.md": the registered census3
entry command has no SOURCES.md surface (its CLI is `--root/--rev/--check/--generate/--historical/
--selftest/--out/--census`, all registry-block-scoped); I ran the registered entry command as
registered and recorded its behavior verbatim.

## Evidence files (this directory)

- `receipt-audit-round-70-at-freeze.json` — the run-4 receipt as written by the tool's `--json-out`
- `record-receipt-audit-round-70-at-freeze.stderr.txt` — run-5 verbatim verdict
- `census3-check-at-freeze.stderr.json`, `census3-check-at-freeze.stdout.txt` — run-6 verbatim
- `r56-receipt-audit-selftest.txt`, `r57-record-receipt-audit-selftest.txt`, `r51-census3-selftest.txt` — runs 1-3
- `audits-summary.txt` — exit codes

Tooling installs/updates this seat: none.

VERDICT: not-met as a clean bill — all three standing receipts duties executed at freeze 4737a542 (selftests 3/3 green); receipt-audit exit 1 failed with c3-at-landing.json expected-pending plus a persistent bare-name `package.json` grammar finding; record-receipt-audit exit 2 expected-pending (no Round 70 record section at freeze); census3 --check exit 2 — the four round-69 registry rows are 8-cell against the frozen 7-cell grammar, unevaluable since 616a5f2f, a named standing defect for the record commit to fix and disclose.
