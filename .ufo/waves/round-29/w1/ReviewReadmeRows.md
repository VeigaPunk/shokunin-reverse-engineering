# ReviewReadmeRows — corpus/README.md rows added in round 29 (w1)

Seat: KaidokuR29.ReviewReadmeRows. Reviewed revision: `18be864a528873b2b70d8c94e31f880290249e90` (lane HEAD when I started; verified with `git rev-parse HEAD` → `18be864a…`). Base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`. All reads of entry/evidence/receipt bytes are `git show`/`git ls-tree` at `18be864a` — committed bytes, not the dirty worktree (see Residual risk). Command window: 2026-10-22 ≈20:19–20:27 UTC (in-session stamp `2026-10-22T20:27:28Z` recorded at the end of the batch). No tool installs; no pacman use; no git/jj writes anywhere; read-only git only, with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset on every call.

Diff under review (`git diff bacbe9cc 18be864a -- corpus/README.md`, exit 0): exactly 5 insertions — the two Coverage map rows (lines 79–80), the two Knowledge index rows (lines 175–176), the round-29 Lessons row (line 198).

## Command A (SCORECARD "Owned axes coverage row") at 18be864a

Command: SCORECARD.md lines 94–122 extracted byte-for-byte to scratch (`cmdA.py`, sha256 below), then `python3 cmdA.py 18be864a…` from the lane root (reads only `git show`/`git ls-tree` objects).

Output (exit 0):

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 114, "mapped": 114, "missing": [], "revision": "18be864a528873b2b70d8c94e31f880290249e90", "rule_blocks": 17}
```

**Map count: 114/114 knowledge files mapped** (coverage 10.0, missing `[]`, dangling `[]`). Same command at base `bacbe9cc` (exit 0): `knowledge_files: 112, mapped: 112` — the +2 is exactly the two new rows' entry tokens, and no token dangles. [observation]

## Per-row verdicts

### Coverage map row, line 79 — `2026-10-22-r29-evm-fresh-selector-naming` — **holds**
- Every number in the row matches the entry at `18be864a` (`git show 18be864a:corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`): "152 held-out selectors", "16 fresh" carriers, "named 122, right 122, wrong 0, no name 30", the 24/3/3 no-name breakdown, "one compiler, one REA pin, one lookup snapshot", "stubs, not deployed contracts" (entry Limits). [observation]
- "none written anywhere in the lane" is receipted: `.ufo/waves/round-29/before/preseen-c1-name.txt` at the tip reads `test_selectors=152 seen_set=58720 overlap=0`, `exit=0`; hex screen reads `carriers=16 fail=0`, `exit=0`. [observation]
- Independently reproduced by running the frozen counter offline at the tip: `python3 -I -B tools/round-29/c1-fresh-naming.py --root <lane> --rev 18be864a…` → `primary rule openchain_sole_unfiltered_args_consistent: named 122, right 122, wrong 0, no_name 30` / `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1`, exit 0. Evidence counts check out: `heldout.tsv` 153 lines = header+152; `runs.tsv` 17 lines = header+16; `envelopes/n01..n16.json` = 16; `c1/db/` 305 files − `manifest.json` = 304 saved lookups. [observation]

### Coverage map row, line 80 — `2026-10-22-r29-openchain-filtered-unseen` — **holds**
- Matches the entry at `18be864a` exactly: 178 selectors with no prior lane response (26 canonical + 152 C1), "mismatches 0 of 252 entries, 38 predicted true, 214 false" (38+214=252), "6 of the 31 kept canonical signatures do not hash to their key, so every candidate under those keys is filtered" (entry Rule section states the same, with the observed 5-of-6-returned-candidates corroboration), "deployed revision assumed, one fetch instant" (entry Limits). [observation]
- Receipted: `.ufo/waves/round-29/before/preseen-c2-flag.txt` → `test_selectors=178 seen_set=230 overlap=0`, `exit=0`. Counter at the tip: `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <lane> --rev 18be864a…` → `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`, exit 0. `selectors.tsv` 179 lines = header+178; `c2/db/` 179 files − `manifest.json` = 178 saved responses. [observation]
- Phrasing nit (not a defect): "every candidate under those keys is filtered" is the rule-level claim; 4 of the 6 mis-keyed-plus-magic keys observed here returned no candidate, so the flag held vacuously for those — the entry says this explicitly and the row does not contradict it. [inference]

### Knowledge index row, line 175 — `2026-10-22-r29-evm-fresh-selector-naming` — **holds** (one observation)
- 4 cells matching `| entry | topic | source | verified-at |`; topic ("152 never-seen selectors from 16 fresh published-interface carriers; why 30 rows get no name") matches the entry's own section headings; counts verified as above; verified-at 2026-10-22 matches the entry's `verified-at:` line. [observation]
- Observation: the source cell cites only `S088`, while the entry's `source:` line also names the round-25 entry's rows S075–S078 (the databases) and S084/S087 (the `filtered` flag). This follows lane precedent rather than breaking it — the r28-C1 index row likewise cites a subset (`S086, S084, S085`) of its entry's source line, and claims.json requires only that the entry "cites S088 in its source: line", which it does. S087/S088 rows exist at the tip (`corpus/SOURCES.md` lines 93–94). [inference]

### Knowledge index row, line 176 — `2026-10-22-r29-openchain-filtered-unseen` — **holds**
- Source cell `S087` matches the entry's `source:` header exactly; "178 never-fetched selectors" and "mis-keyed canonical entries" match the entry (Rule section, 6 mis-keyed of 31); "178 saved responses in `corpus/evidence/round-29/c2/db/`" verified by file count (179 − manifest); verified-at 2026-10-22 matches. [observation]

### Lessons row, line 198 — `round-29` — **holds**
- "frozen with hex and pre-seen screens": receipts at the tip (hex-screen `carriers=16 fail=0` 20:01:29Z; preseen name `overlap=0` 20:01:29Z; preseen flag `overlap=0` 20:01:30Z; all `exit=0`), first REA call 20:03:21Z per the entry's `verified-at:` — freeze before data, as claimed. [observation]
- "r27 selftest repaired as a disclosed selftest-only revision": `.ufo/waves/round-27/claims.json` at the tip, `instrument_supersessions` entry for `tools/round-27/c2-xpin-check.py` at commit `7431096b…`, reason includes "INSTRUMENT_REVISED in round 29 … selftest-only revision". [observation]
- "freeze gate over every claims*.json": `tools/round-29/freeze-gate.py` docstring line 2 — "the R24-C2 gate, extended to every claims*.json"; audits `.ufo/waves/round-*/claims*.json`. [observation]
- "mistakes M29-1..3 (filing with a live seat, ledger out of step with its gate, unpinned name in the L1's own freeze)": the three glosses match `corpus/lessons/round-29.md`'s Mistakes table at the tip (M29-1 seat writing into the tree when filed; M29-2 freeze ledger vs gate mismatch `[round-26, round-28]` exit 1; M29-3 `INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py`). [observation]

### Format parity — **holds**
`fmtcheck.py` over the committed README (exit 0): each new row's pipe/cell count equals its section separator and immediate neighbour — line 79: 4 pipes/3 cells; line 80: 4/3; line 175: 5/4; line 176: 5/4; line 198: 4/3. Verdict-word register matches neighbours ("measured —", "held narrowly —"). Rows are appended in chronological position after the round-28 rows in all three sections. [observation]

## Findings by severity

No defects found in the five added rows. Zero blocking, zero major, zero minor findings; two observations (index source-cell subset citation, line 175; vacuous-filter phrasing, line 80), both consistent with entry text and lane precedent.

## Residual risk and verification gaps

- **Worktree drift (uncommitted):** at review time `git status --porcelain` showed `M corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`, `M corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md` (diff --stat: 22 insertions, 8 deletions across the two), plus `M LOG.md`, `M SCORECARD.md`, `M tools/round-29/prefile-check.sh` and 8 untracked `.ufo/waves/round-29/` paths. `corpus/README.md` itself is clean. This review binds to committed `18be864a` bytes; if those worktree edits land, they are unreviewed by this seat. [observation]
- The counters' `entry_ok=1` was observed with the dirty worktree present; the counters state they count "offline over committed bytes" at `--rev`, and every number they printed independently matches the committed entry text and the README rows, but I did not re-run them in a clean sandbox clone. [unknown, low risk]
- Pre-existing, out of scope: the Lessons table has no rows for rounds 20 and 26–28 although `corpus/lessons/round-20.md`, `round-26.md`, `round-27.md`, `round-28.md` exist at the tip; the round-29 row inherits that table's state (the diff adds only the round-29 line). [observation]
- SOURCES/entry claims about upstream bytes (Sourcify `0966a3bc`, ERC-4626 `3c0f7076`) were not re-fetched by this seat; the row review does not depend on them.

## Artifacts (scratch: /fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewReadmeRows/)

| file | sha256 |
|---|---|
| `cmdA.py` (SCORECARD lines 94–122 verbatim) | `236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01` |
| `fmtcheck.py` (format-parity check) | `62280348edf85b26f30d617ebe063483fda78cb2ee9f81c52c6de2183438cc58` |

No lane files were modified; the only lane write is this report.
