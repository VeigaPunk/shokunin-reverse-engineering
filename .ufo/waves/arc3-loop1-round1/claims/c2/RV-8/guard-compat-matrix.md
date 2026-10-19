# RV-8 guard-compatibility matrix (c2 reviewer, pre-landing analysis)

Consumer shapes (measured, see `consumer-inventory.md` §B and
`baseline-transcripts.txt`) × guard design options for the C2 frozen-run guard
("expected.json pins the sha256 of pointer-table.json; tampered or absent table
→ exit 2 could-not-evaluate, never silent findings").

| Shape | D1: digest scoped to the committed table path | D2: digest enforced for ANY `--table` path against the effective expected.json | D3: D2 + new opt-out flag |
|---|---|---|---|
| S1 default recipe (committed table + committed expected), probe/`--strict`/`--selftest` | unchanged (pin matches) | unchanged (pin matches) | unchanged |
| S2 custom `--table` + committed `--expected` (r10 practice: E16 `table-E8.json`, CR2 `t-faithful.json`, C4 extended, E22 candidate) | **unchanged** — 0/1 verdicts as measured | **BREAK** — every run becomes exit 2 `could-not-evaluate` (digest mismatch); experiment verdicts unreachable without editing the committed expected.json | **BREAK for unmodified invocations** — exit 2 unless the new flag is passed; all historical recipes would need rewriting |
| S3 custom table + custom expected (experimenter copies expected.json too) | unchanged | works only if the experimenter pins their table's digest in their own expected.json; otherwise exit 2 | same as D2 |
| S4 committed table tampered in place (worktree edit) or fixture with the tampered table at the default path | exit 2 (catches it) | exit 2 (catches it) | exit 2 |
| S5 committed table absent | exit 2 (already today: `pointer_table_unreadable`) | exit 2 | exit 2 |
| S6 selftest | 11 existing cases unchanged + 2 appended = 13; green under redirected TMPDIR | same | same |
| S7 parse patterns (`tail -1` = verdict line; `grep -c "^CITATION_DRIFT:"`; verbatim verdict-line compare) | preserved if format/labels/last-line unchanged | same | same |

## Verdict-relevant readings

- The **only** shape at risk is S2, and it is not hypothetical: it is the
  recorded r10 landing/experiment shape (`E16.md:117-119`, `CR2.md:91`,
  `C4.md:153-159`, `E22.md:144-150`), and the current round's own reviewers
  (RV-6 harness: custom tables + committed expected) run it again.
- D1 closes the claim's defect class on the committed artifact: an isolated-tree
  fixture that tampers the table at the default path is caught because
  `DEFAULT_TABLE` is derived from `HERE` (`citation-drift-probe.py:52-54`), so
  the fixture's own copy is the "committed" table for that run.
- D2 as written would additionally make `--table` a trap for any future
  experimenter unless the registry row declares the new contract; if EX-16 lands
  D2, the SKILL.md registry patch must say so explicitly and the r10-style
  recipes become historical.
- D1 detail: identify the committed table by realpath comparison against
  `DEFAULT_TABLE` (the SKILL recipe passes the relative path; `HERE` is
  absolute), so both spellings are covered.
- No consumer passes `--snapshot-dir`; the guard must not add a mandatory flag.
- The registry-row patch (`SKILL.md:371`) is safe to edit (the table's
  `skill-registry-row` anchor pins only the sibling row's text,
  `pointer-table.json:107-112`) and must state: digest pin + 11→13 cases +
  tampered/absent table → exit 2.
