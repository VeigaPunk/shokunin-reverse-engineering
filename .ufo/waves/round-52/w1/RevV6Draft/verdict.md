# RevV6Draft — salvage verdict

**Salvage: NO as a port base. Start from committed v5.** Only the new row's selector/label/action is worth reusing as a design fragment; there is no completed v6 evaluator or audit to salvage.

Axes: syntactic validity; route/evaluator agreement; preservation of clean labels; audit/freeze completeness; evidence fidelity.

## Findings, severity ordered

### High — draft is syntactically invalid in three distinct regions

Source: `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py` (all line numbers below refer to this source unless stated).

- **288:** literal `CUT 1033.=1033` sits inside `READER_BACKED_V1V3`. Scratch `python3 -I -m py_compile …/sqfs-triage-v6.py` exits **1**, reporting `SyntaxError: invalid syntax` at line 288. Exact command, UTC, stdout hash, stderr and input hash: `compile.json`.
- **1018–1022:** `avm-marker-be-dropped` lost its source cell and closing `],`; the following legacy-row opener is nested into the unfinished row. Restore committed v5 **1021** rather than copying this region.
- **1033–1034:** duplicated `no-reader-failure` row opener leaves an additional unclosed list. Drop draft **1033**, retain the original complete row **1034–1042** only through its committed-v5 equivalent.

Only the first error was exercised by py_compile; the latter two are directly visible unmatched-list structural defects in the full 46-line comparison (`v5-v6.diff`). No repaired candidate was executed.

### High — the proposed new row has no evaluator counterpart

- **Take, as a fragment only: 1027–1029** — `legacy-body-unreadable`, `squashfs_v3_ddwrt`, `extractor-failure+`, zero published files, `preserve-unresolved`. This matches R52-C2's named failed-body route and does not itself alter clean rows.
- **Do not take 1030–1032 unchanged.** “both validated readers refuse” conflicts with the claim's explicit absence of a validated independent reader. State that the family's reader census does not validate an independent reader, cite the actual frozen evidence pointer, and use the R52 attribution. `R51-C2; ddwrt reader-census evidence` is not that pointer.
- **284–289:** the apparent intent is to remove ddwrt from `READER_BACKED_V1V3`. If only the literal CUT line were removed, **evaluate() 951–956** would route a zero-file failed ddwrt body to `body-extractor-failure/preserve-failure`: ddwrt is absent from both the reduced reader-backed set and **NO_READER_FAMILIES 276–280**. No `legacy-body-unreadable` return exists. Thus syntax repair is not a semantic port.
- Keep the existing clean-path separation (**967–972**) when implementing the actual failure-only route. Adding ddwrt to the shared `NO_READER_FAMILIES` would also change clean ddwrt labels, violating claims **221–224**. Preserve the other higher-priority routes (**936–950**), then implement matching table/evaluator precedence.
- Update **1527–1529**, **1866–1880**, and **2047–2051** in the eventual port: these retained v5 fixtures/assertions still encode the former ddwrt legacy route (or derive the expected set from the changed constant), not independent proof of the new contract.

### High — audit and freeze obligations are absent, not salvageable implementations

The comparison shows only three changed hunks: opening text, reader-backed tuple corruption, embedded row corruption. Everything else is v5.

- Canonical **run() 1297–1369** compares table and evaluator pairs and constructs a verdict solely from mismatches/evaluator abstentions. There is no executability or census audit, no corresponding result fields, and no audit-dependent verdict gate.
- **run() 1255–1284** records instrument equality and changed tool paths, but **1368** does not include them in the verdict. This is reporting, not R52 freeze-drift gating.
- Drop/rewrite draft-only **1–3**: the renamed heading's “distinct unreadable-body route and audits” claim is unsupported. Retained **230–234**, **299–320**, and **1343** still identify v5 markers, the R50 predicate/instrument path, and v5 receipt identity. Port these from v5 deliberately to R52; renaming the top is insufficient.

## Exact salvage/drop decision

- **Worth taking:** draft **1027–1029** only as the new table-row selector/label/action; reconstruct its cause/source cells from authoritative R52 claims and reader-census evidence.
- **Drop:** **288**, the malformed splice at **1018–1022**, duplicate **1033**, unsupported/misattributed **1030–1032**, weakened legacy explanation **1024–1026**, and the superficial header **1–3**.
- **Reuse through committed v5, not this draft:** parser, feature extraction, independent evaluator scaffolding, established higher-priority/clean routes, receipt writer, and existing tests. The draft adds no implemented audit, census integration, freeze gate, mutation, or CLI extension.

## Prior receipts and verification gaps

The source directory contains only `sqfs-triage-v6.py`; adjacent `ExecTriV6.md:3–8` says incomplete/do not integrate and explicitly records pre/post/selftests not run. Its description that only the docstring changed understates the actual three-hunk file diff; the captured bytes, not that prose, determine this review.

LSP fallback: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics server was available. Text search located relevant definitions; the unified comparison and cited source bodies supply the review evidence, not semantic-reference claims.

Executed: scratch py_compile (exit 1); Python unified comparison (successful API completion, differences present). Not run: v6 scoring, repaired draft, selftests, corpus probes, REA, downloads, or another runtime. No installs/updates. No lane source modifications. No saturation/runtime-identity/resume claims apply to this static triage instrument review.

Residual risk: a replacement must prove 126-envelope label preservation except the single named failed ddwrt pair, audit before=1/after=0, census_outside=0, fail-closed freeze drift, and the named R52 mutation controls. This review does not certify those unimplemented properties.
