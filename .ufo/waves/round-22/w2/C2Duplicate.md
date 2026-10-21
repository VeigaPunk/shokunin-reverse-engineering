# R22-C2 duplicate-disposition review

## Finding

### High (P1) — Markdown comment content can hide a duplicate disposition and produce a clean result

**Evidence:** `.ufo/waves/round-22/tools/count-c2.py`, `section_rows()` lines 69–73, stops the section at any raw line satisfying `line.startswith("#")`. It does not distinguish Markdown headings from a `#` line inside an HTML comment (or fenced code). The row scan therefore terminates before later disposition rows that are still under the selected section heading. `measure()` then checks `len(mine)` only over the rows returned by that scan (lines 149–164) and can report `dispositions_complete` despite a second row for a T2 verb.

**Adversarial fixture:** in a private temporary Git repo, started from the 14-row clean C2 fixture, appended an HTML comment and a second table containing a duplicate `inspect-packet-fields` row:

```markdown
<!--
# inert comment content
-->

| inspect-packet-fields | adjacent | inspect-packet-fields | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-packet-fields.json | duplicate |
```

The `#` is comment text, not a Markdown heading. The appended row remains a disposition under the same section. Nevertheless, `section_rows()` stops at the comment text, leaving only the original row visible to duplicate detection. The CLI returns exit **0**, `accounted_count: 14`, `finding: "dispositions_complete"`, `mismatched: []`, `foreign_rows: []`, and `inspect-packet-fields: matched`. A duplicate row is therefore accepted as fully accounted for; this is an implementation flaw affecting the coverage/calibration conclusion, not the stated limit about reason/placement semantics or provider availability.

**Positive and adversarial controls:** the clean 14-verb private fixture also returned exit 0, as expected. The built-in `--selftest` returned exit 0 with all seven C2 controls passing; its contiguous `duplicate_row` mutant correctly returned exit 1, count 13, status `duplicate_rows`. The HTML-comment mutant returned exit 0 and count 14 instead. Exact target argv, exit, stderr, and full one-line stdout for the clean and adversarial runs are preserved in `C2Duplicate.json`.

- Selftest command: `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-22/tools/count-c2.py --selftest` — **exit 0**.
- Private adversarial harness: `cd /tmp/c2dup && python3 probe.py` — **exit 0**; per-case target results are in the JSON attachment. Both the clean control and the HTML-comment duplicate invoke the counter with the same executable, `--root /tmp/c2dup-rmqejp63`, and their recorded `--rev` values.
- Reviewed target SHA-256 at probe time: `0a5f2a41a9801e2ac421fd61766ec926cc69f7f96d66be8a18b7ced780b8f7a0`.

**Narrow fix:** only treat actual Markdown headings as section boundaries. Track fenced-code and raw-HTML/comment blocks while scanning, so a `#` inside those blocks cannot end the section; alternatively use a Markdown parser configured for the document dialect and extract the target heading/table. Add this exact comment-plus-duplicate fixture and a fenced-code analogue; both must fail closed rather than report complete. The existing malformed-cell and multiple-exact-heading checks are useful fail-closed behavior and should remain.

## Residual risk

- A two-space-indented duplicate row also returned exit 0 because `line.startswith("|")` ignores it. Whether such a row is a table row under the exact renderer used for `PROVINCE.md` was not established here, so I do not elevate it to a separate finding; validate the row predicate against the repository's renderer or reject ambiguous indentation.
- The earlier prefix-shadow and extra-cell probes were closed by the in-flight changes observed during this review: heading matching is now exact/unique, and malformed rows produce `unevaluable`/exit 2. A straightforward contiguous duplicate remains rejected by the selftest.

## Verification gaps

- No `lsp` device was mounted: `read xd://lsp` returned “No such tool”. Consequently no LSP status/references/definition/diagnostics were available; no grep result is offered as semantic proof.
- No repository Markdown renderer was used to independently parse the GFM table. The report relies on the HTML-comment block syntax and the captured parser behavior; renderer-specific treatment of indented table rows remains unknown.
- No production source was edited and no tools were installed. All mutation fixtures and Git commits were private under `/tmp`; only this report and its same-name JSON attachment were written in the lane.
