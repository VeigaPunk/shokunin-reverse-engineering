## Round 48 — a verdict map binds meanings, and the record is re-derived from committed bytes with a floor

Base `61b87d742032e65fca9c38267d7d6ed7e555edad`. The freeze is a disclosed series of four
amendments, all before any claim data: `7fe11332` (plan + both counters), A1 `dc73587a`
(the axis-score clause read the evidence cell, so it scored nothing), A2 `ac02a79f` (the
exit-0 classifier rejected a legitimate success meaning), A3 `f3a7afc4` (the census clause
compared a derived object with a committed list), A4 `0f06251b` (the exit-0 classifier
accepted `0=not met`; the row parser skipped an indented row). **The declared freeze is A4
`0f06251bf6a3a6964c715f67243d4df12e854258`.** Each amendment's red-before receipt is
committed: A1 `.ufo/waves/round-48/controls/ctl-c2-a1-before.json`, A3
`…/ctl-c1-a3-simulation.json`, A4 `…/w1/C1Gold.md` and `…/w1/CritAxis.md`. Waves: 75 + 0 = 75 seats (`.ufo/waves/round-48/w1/`), settled as `…/w1-results.json`.

| claim | axis / surface | before | after | counting command | measured at |
|---|---|---|---|---|---|
| R48-C1 | depth — craft rule block 25 (marker `<!-- verdict-meaning-table v1 -->`, two rows keyed by routed id, arms `meaning`/`floor`, a name+body mutation digest and the interpreter pin) and the instrument-registry section re-bound by meaning to `tools/round-48/census2.json` | at the declared freeze exit 1, `marker_occurrences 0`, `rule_blocks 24` (`…/controls/ctl-c1-0-do-nothing.json`); with the block simulated, 16 registry verdict maps name no meaning class for at least one digit | exit 0, `rule_blocks 25`, `rows 2`, `refs`, `meaning_rows_failed 0`, `registry_rows == census_paths`, `census_rederived_equal true`, battery `4/4/0/1` (`…/l1/scores/c1-at-<LANDING>.json`) | `python3 -I -B tools/round-48/meanings.py --root . --freeze 0f06251b --rev <REV>` | `<LANDING>` |
| R48-C2 | calibration — `tools/round-48/record2.py`: the round-47 atom oracle executed from the bytes at `--rev`, a per-section completeness floor, `axes`/`quote` corrections re-derived, quoted numbers bound to their receipt, and the Owned-axes score cell bound to its fraction | at the declared freeze exit 1: `round-47: no seat atom and no re-derived seats correction`, `no `## Record corrections — round 48` line re-derived`, `quoted numbers with no backing receipt: 1` (`…/controls/ctl-c2-0-do-nothing.json`); `--profile v2` exits 0 on the same card, which is the hole (`…/controls/ctl-c2-1-v2-profile.json`) | exit 0, oracle `mismatches []`, floor green with the round-47 seats correction, both correction lines re-derive, `quotes_bad []`, `axis_score_bad []`, battery `5/5/0/1` (`…/l1/scores/c2-at-<LANDING>.json`) | `python3 -I -B tools/round-48/record2.py --root . --freeze 0f06251b --rev <REV>` | `<LANDING>` |

Owned scores: coverage `10 → 10` (command A at the landing: `knowledge_files 138`,
`mapped 138`, `missing []`, `dangling []`; this round adds no knowledge entry, no coverage-map
row and no PROVINCE change — S145 is method documentation and S146 a rejection); depth
`10 → 10` (`rule_blocks 24 → 25`, `citation_resolved_rules 25/25`; the move is the
meaning-bound registry and its forgeries, not a number above the proxy); calibration `10 → 10`
(the record re-derives from committed bytes and now carries a floor; the numeric axis cannot
rise above 10).

Learning trends: expansion **unchanged** (no admitted knowledge entry, no coverage-map row, no
PROVINCE line; the two opened sources are method documentation and a rejection). Quality
**improved on the instruments**: the meaning counter scores its own four forgeries red under
v3 while the ported v2 profile greens all four, and the record counter scores five forgeries
red while the round-47 semantics green all five; the bound is that both grade the stated form
(MutC1Rows: a cell that says `0=met` and then contradicts it in the same segment still
passes). Discernment **improved**: the round found five of its own instrument defects before
the operator (A1 a clause that scored nothing, A2 a false red, A3 a comparison false by
construction, A4 two checks that accepted what they should reject — the classifier's
opposite polarity and the indented registry row), and each carries a committed red-before.

**Freeze-integrity disclosure.** The frozen set is derived from this round's claims file
(`plans/round-48-claims.md`, `tools/round-48/`), so a later restore cannot un-block either
counter; `git log --name-status 0f06251b..<tip> -- plans/round-48-claims.md tools/round-48` is
empty at the landing. The wave ran against A1's bytes (`dc73587a`) because it was dispatched
before A2–A4; no claim data had been scored, and every measurement above is taken at the
declared freeze or later. Limits, all measured by wave seats and routed, not closed: the
record counter's oracle delegates byte reads to `tools/round-46/gate.py`, which is imported
from the worktree (`w1/C2OracleLimit.md`); the meaning classifier grades a class word, not the
row's truth against its tool (`w1/MutC1Rows.md`); and the battery only runs when the genuine
artefact is green (`w1/C2Battery.md`).

- **planned (round 49):** calibration or depth from the routed list — (a) pin `gate.py` by
  committed bytes in both counters and add a worktree-tamper arm (R48-CL1); (b) bind each
  registry row's meaning class to the tool's own source at `--rev`, so a contradictory cell
  fails (R48-CL2); (c) let the battery run against a red genuine artefact so its mutants are
  always measured (R48-CL3). Second choice: coverage — resume the SquashFS v1/v2 promotion with
  a single, mutually consistent provenance clause (R44-CL2). R36-CL5, R40-CL2, R41-CL3, R46-CL1,
  R46-CL5, R46-CL8 remain open.
- **retired:** none. Coverage, depth and calibration stay tied at 10; no finite proxy saturates
  an axis, and the last capability entries are rounds 42–43.
