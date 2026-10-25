# R35Audit06 — audit: C1 registry row parser

Seat: `R35Audit06` (leaf executor, wave 1, round 35)
Item: Audit C1 registry row parser (tools/round-35/c1-coverage-counter.py `ROW_RE` + `check()` registry block)
Lane: `kaidoku-shokunin` (base `aa04633`, HEAD `3ecf4298`)
Mode: read-only vs lane; analysis in private `/tmp` only. No lane files touched except this report. No VCS mutation.

## Scope

`c1-coverage-counter.py:21-25` `ROW_RE` and `check()` `:114-131` parse `corpus/SOURCES.md`
11-column rows (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`)
and validate the S125/S129 rows for C1.

## Evidence

### 1. Corpus parity (HEAD 3ecf4298, base aa04633)
Replicated `ROW_RE` exactly; compared against a strict column split of every `|`-line.

```
--- HEAD 3ecf4298: rows_parsed=106 strict_candidates=106
    mismatched_cell_counts=[] (n=0)
    strict_row_not_in_regex=[]
    regex_phantom_ids=[]
    escaped_pipes_lines=[]
    non-row_pipe_lines=[] (n=0)
--- BASE aa04633: rows_parsed=106 strict_candidates=106   (same, all empty)
S125/S129 in HEAD: False False   S125/S129 in BASE: False False
```

Parser is 106/106 exact on the live corpus at both revisions; no embedded pipes, no wrapped rows,
no non-row `|`-lines in the `## Paths` section. `S125`/`S129` do not exist yet (pre-data).

### 2. Live counter run at HEAD (read-only, git objects only)
```
$ python3 -I -B tools/round-35/c1-coverage-counter.py --root <lane> --freeze HEAD --rev HEAD
C1_FAIL: entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md; registry_row_missing:S125; registry_row_missing:S129; province_missing:...; readme_missing:...
exit=1
```
Predicate gate passed (claims-canonical.json at freeze rev contains P35-c1); exit 1 with exactly the
expected pre-data failing set — consistent with the committed do-nothing control (`3ecf4298`).

### 3. Adversarial mutation tests (same check logic, synthetic registry)
| case | result | classification |
|---|---|---|
| embedded pipe in `source` cell (`a\|b`) | fails (status/opened/usedby misread) | fail-safe |
| dropped `scope` cell (10 cells) | fails both rows | fail-safe |
| indented row | `registry_row_missing` | fail-safe |
| lowercase id `s125` | `registry_row_missing` | fail-safe |
| whitespace in cells | passes | handled via strip() |
| `opened` with time suffix | passes | prefix check by design |
| **extra trailing 12th column** | **passes** | not end-anchored; junk column ignored |
| **wrapped cell (embedded newline)** | **passes** | `[^|]*` swallows `\n` (only non-relevant cells tested) |
| **duplicate id (two S125 rows)** | **passes** | last occurrence silently wins (dict overwrite) |
| **empty `source` cell** | **passes** | `source`/`kind`/`tier`/`scope`/`anchor`/`teaches`/`recheck` cells are never validated |
| **used-by substring with longer name** | **passes** | `entry in cells[9]` substring; e.g. `...md.evil` would pass |

## Findings

- **Correct today:** `ROW_RE` parses the current registry exactly (106/106 at HEAD and base) and all
  realistic malformations I tested fail in the safe direction (missing row or cell misalignment →
  named failure, never a false pass).
- **Gap 1 (substantive):** the registry check validates only `status` (`cells[6]=="mined"`),
  `opened` (prefix `2026-10-25`) and `used-by` (substring). An S125/S129 row with an **empty
  `source` cell** (or any junk kind/tier/scope/anchor) would satisfy the counter, so the instrument
  enforces the *shape* of the row, not that the source cell carries the cited frontier source.
  The predicate sentence ("both rows are mined with used-by naming the entry") is met by such a row.
- **Gap 2:** the regex is not end-anchored and is not scoped to the `## Registry` section — a
  trailing 12th column is ignored, and any line anywhere in SOURCES.md beginning `| S### |` would
  register as a phantom row (none exists today).
- **Gap 3:** duplicate ids silently overwrite (last wins) — no duplicate detection.
- **Gap 4:** `used-by` and citation checks use substring `in`, accepting a longer filename that
  merely contains the entry path (low risk).
- Entry-file side (not this parser) behaves fail-safe: trio keys must start their lines
  (`^source\s*:`, `^verified-at\s*:`, `^recheck\s*:`), citation regex carries the exact row id.

## Risks

- No falsification of C1 found at HEAD: the claim is simply unevaluated (pre-data) and the
  do-nothing control fails as committed.
- Gaps 1–4 are advisory; per scope I did not alter the frozen counter or predicate. If desired by
  the L1, a future (non-frozen) counter could add `source` non-empty, `$` end-anchor/- section
  scoping/duplicate detection — but that would be a predicate/scope change outside this wave.

## Commands used (read-only / /tmp)

```
git -C <lane> show 3ecf4298:corpus/SOURCES.md > /tmp/s35_sources_head.md
git -C <lane> show aa04633:corpus/SOURCES.md > /tmp/s35_sources_base.md
python3 /tmp/audit_c1_parser.py          # corpus parity + adversarial cases
python3 -I -B tools/round-35/c1-coverage-counter.py --root <lane> --freeze HEAD --rev HEAD
```

## Limits

- Read-only audit; only file written: this report. No VCS/index/jj mutation, no lane production
  files, no delegated/background work, no pacman installs.
- `source`/`kind`/... cell content validity is out of the counter's contract; semantic review of
  row content must happen in the data authoring/wave review, not the instrument.
