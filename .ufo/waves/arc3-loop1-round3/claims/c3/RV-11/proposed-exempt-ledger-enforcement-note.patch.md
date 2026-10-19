# proposed patch TEXT — the `exempt` array is not instrument-enforced (RV-11, c3)

Target: `.ufo/gates/citation-drift/pointer-table.json` `_doc` string (+ one records
sentence in the round's SCORECARD/LOG section). Status: **proposal only — NOT applied.**

## What is measured

`citation-drift-probe.py` grades exactly two arrays — `entries` and `quoted`
(`run_check`, lines 319-324):

```python
for entry in table.get("entries", []):
    check_entry(entry, tree, findings)
for entry in table.get("quoted", []):
    entry = dict(entry, kind="quoted")
    check_entry(entry, tree, findings)
```

The `exempt` array (now 8 rows) is never read: an exemption is a **review-enforced
declaration**, and a token moved into `exempt` without a cause would be a silent
exemption — the r4 "laundering path refused" class applied to the table.

Two measurements (artifacts: `attacks/table-attacks.json`, `attacks/probe-vs-audit.txt`):

- `L1-laundered-exact` — an `exact` row on `SCORECARD.md:291` whose needle asserts the
  bare token `config.toml:1478` (a pinnable in-repo byte re-stating an unpinnable live
  value — the r4 laundering shape). Probe `--strict`: **silent, findings unchanged,
  the row is green**; the rule-#11 audit flags it
  `OM_LINE_TOKEN,LAUNDERED_PIN,NO_CONTENT_KEY`.
- `A2-anchor-launder` — an `anchor` row grading the *form* `config\.toml:\d+` instead of
  a content key. Probe: **silent**; audit flags `NO_CONTENT_KEY`.

So: rule #11 conformance is not instrument-enforced. The landed table's 8 exempt rows
all carry causes and none shelters a live citation (RV-11 reviewed each; E1's
"SKILL.md:371 now holds `## Refuses`" is verified true at HEAD). The note below keeps
that property visible to later rounds.

## Proposed `_doc` addition (append one sentence to the existing `_doc` string)

> The `exempt` array is a review-enforced NO-ENTRY ledger, not a graded surface: the
> probe reads `entries` and `quoted` only, so a token moved into `exempt` without a
> cause is an unreported exemption (the arc2-loop1-round4 'laundering path refused'
> class). Every exempt row states (a) the token, (b) its cause class, and (c) the
> measured evidence line; exemptions never shelter a citation that a current-scope
> sentence grades live.

## Proposed records sentence (round section, verbatim or equivalent)

> The table's exemption ledger grew 3 → 8 rows; all five new rows are adjudicated
> NO-ENTRY with causes, none shelters a live citation, and the ledger is
> review-enforced — the probe does not grade the `exempt` array (measured: a planted
> laundered `exact` row on `SCORECARD.md:291` passes the probe green while the
> rule-#11 audit flags it).

Cost: none beyond the F3 re-pin in the same commit (the `_doc` is part of the hashed
bytes). The records sentence is free if the section is still a draft.