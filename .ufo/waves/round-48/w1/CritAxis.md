# CritAxis — Round 48 frozen-counter attack

Axes touched: **depth** (C1 verdict-meaning and arm semantics) and **calibration** (C2 record completeness/re-derivation). **Coverage** is intentionally untouched; round 48 claims explicitly prohibit coverage expansion. Harm check after landing remains `git diff --no-ext-diff 61b87d742032e65fca9c38267d7d6ed7e555edad <landing> -- corpus/knowledge corpus/README.md PROVINCE.md`.

## Review result

Inspected the claim contract and the frozen `meanings.py`, `census2.py`, and relevant `record2.py` implementation at `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`. Found a credible false-green in C1's registry coverage: registry rows are extracted only when a line starts with `| \``. Yet the exact-path check compares that extracted set to census. An extra registry row with whitespace before the opening backtick is silently ignored, so “every row's verdict map” is not actually checked. The line still visually/semantically appears as a registry row in a Markdown table, but it can carry a meaningless verdict map.

### Counterexample

Starting with a genuinely green artifact, append a duplicate census path row whose first cell has leading whitespace before the backtick, and give it `0=banana; 1=nope; 2=whatever`. The parser skips it, and the extracted paths remain exactly the census path set; consequently the forged row is outside the meaning check. A minimal fixture mutation is:

```python
skill = skill.replace(REG_CLOSE,
    "|  `tools/round-48/meanings.py` | forged | "
    "0=banana; 1=nope; 2=whatever | none | none | none | kaidoku |\n" + REG_CLOSE)
```

The suspicious exact implementation is frozen `tools/round-48/meanings.py`, `registry_rows()`: `if line.strip().startswith("| `")`. `line.strip()` removes whitespace at the line edges, not whitespace between `|` and `` ` ``; thus `|  ` is excluded. The relevant path-set and meaning checks later operate only on `rows_reg`, so cannot see it. The correction is to parse every table data row in the marker-bounded registry section, reject malformed rows (including leading whitespace variations only if they violate a deliberate canonical grammar), and enforce exactly one parsed row per census path; do not silently skip table-looking rows.

This attacks **depth**: an extra unvalidated row can preserve apparent exact coverage while carrying the exact meaning-forgery class C1 claims to prevent. Smallest safe correction: make row recognition robust to optional horizontal whitespace after `|`, then fail closed on any registry data row with a non-seven-cell structure; add this forged row to the C1 battery/selftest and require v3 red.

## Other clauses examined

C1's meaning classifier uses independent keyword regexes and distinct segment text; plausible legitimate prose may still be brittle, but the disclosed A2 change addresses the known `failing` false-red. C2 visibly invokes the round-47 oracle from committed revision bytes and checks quote receipts, axes corrections, score-cell binding, and a completeness floor. No additional demonstrated C2 false-green established in this review. The cited fixture above is a source-level falsifier, not an executed counter run; no verification command was run and no result is claimed.

No installs. No lane source edits; only this report was written.
