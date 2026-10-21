# R22-C2 Foreign — count-c2.py adversarial review (unknown foreign row / malformed table row)

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py` @ HEAD `2ee3d9f51c6a` (lane read-only; all mutation in a private temp git repo via `/tmp/c2_foreign_probe.py`).
No tool installs; `python3` + `git` already present.

## Positive controls (observed)

- Real lane: `python3 .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD` → exit `0`, `accounted_count:14`, `foreign_rows:[]`, `mismatched:[]`.
- `python3 .ufo/waves/round-22/tools/count-c2.py --selftest` → exit `0` (`counter_controls_clean`, all 7 fixture cases pass).
- Fixture `clean` → exit `0`. Fixture `foreign_row` (well-formed `| frida-kill | … |` appended) → exit `1`, `foreign_rows:["frida-kill"]`. Contract holds for well-formed input.

## Findings

### F1 — Silent drop of non-6-cell rows makes malformed *foreign* rows produce a false-clean exit 0 (implementation flaw)

`section_rows` (lines 72–74) skips any `|`-line whose cell count ≠ 6. Those lines never reach `rows`, so the `foreign` set (line 143) never sees them and the exit gate `not out["foreign_rows"]` (line 174) passes. A well-formed foreign row exits 1; the same row missing or carrying an extra `|`-cell exits 0 with `foreign_rows:[]` — indistinguishable from a clean run. Direction is asymmetric to severity: corruption of a foreign row *erases* the finding instead of preserving it.

Observed (each appended to a clean 14-verb table; `python3 count-c2.py --root <tmprepo> --rev <rev>`):

| case | row appended | exit | foreign_rows |
|---|---|---|---|
| `foreign_row_3cells` | `\| frida-kill \| adjacent \| rogue \|` | **0** | `[]` |
| `foreign_row_7cells` | `\| frida-kill \| adjacent \| frida-kill \| error:x \| r \| reason \| extra \|` | **0** | `[]` |
| `foreign_row_empty_verb` | `\| \| adjacent \| p \| error:x \| r \| rogue-empty-verb \|` (6 cells, empty verb cell) | **0** | `[]` |
| `foreign_row_header_verb` | `\| verb \| adjacent \| verb \| error:x \| r \| rogue \|` (verb cell = `verb`) | **0** | `[]` |

The last two are dropped by the header/empty guard `cells[0] in ("verb", "")` (line 73) — a rogue 6-cell row keyed `verb` is mistaken for the column header; an empty-verb row is mistaken for a blank row.

### F2 — Malformed T2 rows fail closed but are mislabeled `unaccounted` (implementation flaw, lower severity)

| case | mutation | exit | `stop-adb-app` status |
|---|---|---|---|
| `malformed_t2_5cells` | row rewritten with 5 cells (reason dropped) | 1 | `unaccounted` |
| `malformed_t2_pipe_in_reason` | reason contains `\|` → 7 cells | 1 | `unaccounted` |

Exit stays safe, but a present-but-corrupt row is reported identically to a genuinely absent row, and `foreign_rows`/`mismatched` give no hint the section is malformed. Note markdown tables have no escaped `\|` support here, so any pipe inside `reason` corrupts the row silently.

### F3 — `line.startswith(HEADING)` anchors on the *first* prefix-matching heading; a shadow section masks the real one (implementation flaw)

`section_rows` (line 63) takes the first line that merely *starts with* `### Round-22 catalog dispositions`. Any earlier heading with a suffix — e.g. `### Round-22 catalog dispositions (draft)` — wins; scanning then `break`s on the next `#`-line (the real heading), so the real table is never read.

| case | construction | exit | note |
|---|---|---|---|
| `shadow_heading` | complete stale 14-verb table under `… dispositions (draft)`, then identical real section | 0 | real section ignored; pass is attributable to shadow only |
| `shadow_heading_broken_real` | same shadow table, real heading present but **zero data rows** | **0** `accounted_count:14` | false-clean: the authoritative section is empty yet the counter reports full coverage |
| `fenced_shadow` | real heading quoted inside a ```` ``` ```` fence before the real section; fenced table has 1 row | 1, `accounted_count:1` | fail-closed but wrong: fenced code is parsed as section text, 13 genuine rows never examined |

Reachability: `startswith` makes `(draft)`-style headings easy, and fenced quoting of the heading (documentation of the schema inside PROVINCE.md) is plausible in this corpus. Also note the section terminator is *any* line starting `#` — one stray `#` comment line ends the table early.

## Declared limits (not findings)

- `foreign_rows` lists names only; a foreign row is *not* `check()`-validated (placement/probe/receipt unexamined). That is consistent with the contract (foreign ⇒ exit 1 anyway) — informational only.
- `error:`-code, `ok-empty`, `ok-field` grammar, strict-JSON receipts, `..` in receipt paths, and `probe == verb == meta.command` are all handled correctly; the strict-JSON and receipt-prefix logic showed no adversarial gaps.
- `limit` field honestly scopes: "receipt/row agreement at one revision".

## Proposed narrow fix (single function + output field + gate)

```python
def section_rows(province):
    rows, malformed = [], []
    in_fence = False
    starts = []
    lines = province.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.strip() == HEADING:   # exact match, outside fences
            starts.append(i)
    if len(starts) != 1:
        return rows, [("section_heading_count", len(starts))]
    for n, line in enumerate(lines[starts[0] + 1:], starts[0] + 2):
        if line.startswith("#"):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0] == "verb" and cells[1] == "placement":
            continue  # header
        if set(cells[0]) <= set("-: "):
            continue  # separator
        if len(cells) != 6 or not cells[0]:
            malformed.append((n, line))
            continue
        rows.append(dict(zip(("verb","placement","probe","observed","receipt","reason"), cells)))
    return rows, malformed
```

Then `measure` carries `malformed` into the report as `malformed_rows` and the clean gate becomes `… and not out["foreign_rows"] and not out["malformed_rows"]`. Effects: every F1/F2/F3 case converts from silent-exit-0 or `unaccounted`-mislabel to an explicit `malformed_rows` entry and exit 1; the header check now requires `placement` in cell 1 so a data row keyed `verb` is malformed rather than skipped; exact heading match kills prefix-shadows, and `len(starts) != 1` (duplicate or absent heading) is itself reported malformed. `empty_section` fixture behavior preserved (returns zero rows ⇒ all `unaccounted`, exit 1).

## Residual risk

- `reason` free-text still cannot contain `|` (no escape support) — flagged rather than fixed; a row needing it must use `｜`/`or` wording. Post-fix it lands in `malformed_rows` instead of vanishing.
- ATX heading with trailing `#`s (`### … ###`) matches exact-`strip()` only if stripped of trailing `#`; acceptable to leave.
- Verdict scope: findings are author-side only; no production edit was made.

## Reproduction

`/tmp/c2_foreign_probe.py` builds one temp git repo, commits each mutated `PROVINCE.md` + receipt JSONs, runs `python3 -I -B count-c2.py --root <repo> --rev <rev>`, prints per-case `{exit, accounted_count, foreign_rows, mismatched, stop_status}` — full stdout table above. Exact argv per run: `["/usr/bin/python3","-I","-B","…/count-c2.py","--root","/tmp/c2-foreign-XXXX","--rev","<commit>"]`; stderr empty in all runs.
