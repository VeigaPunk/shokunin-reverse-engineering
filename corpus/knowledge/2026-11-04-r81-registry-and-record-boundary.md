source: S258 — https://github.github.com/gfm/ §Tables (extension); S255 — https://git-scm.com/docs/git-show §DESCRIPTION; both reopened 2026-11-04
verified-at: 2026-11-04; round-81 frozen declaration abdcfd3c28d98288a3dc6b4e98c88d115ed42b53; immutable base 5b59ae615a2ab68e3b421820d1c72751e1185385
recheck: python3 -I -B tools/round-71/registry-census.py --root . --rev main; TMPDIR=<private scratch> python3 -I -B tools/round-81/strictness-battery.py --selftest; rerun after registry/binder changes

# Two boundaries in kaidoku's REA evidence apparatus

This entry concerns the lane's own instrument registry and saved-record reader. It grants no new artifact format, target execution, provider availability or domain coverage.

## Registry: repair the columns without changing the reader

S258 documents escaping a literal pipe inside a table cell, even inside an inline span. The round-71 census implements that escape, unlike a naive split. Its four named round-69 exceptions are historical eight-cell rows; they are not permission to accept new eight-cell rows.

At the round-81 base, the unchanged census reports 129 rows and seven malformed ones: six `cells>7` and one `pinned-empty` (`.ufo/waves/round-81/pre/c1-base.json`, exit 1). Raw delimiter count is insufficient to repair their meanings:

- Five newer eight-cell rows carry separate output and read-only/write-root descriptions. Merge those descriptions into write scope, not into the pinned-input cell.
- The attack-gate row contains two unescaped pipes in its control alternatives and lacks explicit write/owner fields. Escape both purpose pipes, restore the actual verdict/selftest positions, then name the write scope and owner.
- The surface-recheck row lacks an owner. Its provider inputs and no-secret-output limitation must remain explicit; supply a separate write scope and owner.

ReviewerC1-12 independently preserved exactly the base's 129 paths, with 125 seven-cell rows and four byte-identical historical exceptions in the candidate (`.ufo/waves/round-81/w1/ReviewerC1/ReviewerC1.md`). Final scoring uses the frozen census against committed integrated bytes, not this prose or a candidate filename.

## Record reader: a fake working-file read cannot prove a git-object read

S255 states: “For plain blobs, it shows the plain contents.” The real binder's `git_show()` obtains PROVINCE at a named commit. The old strictness selftest instead uses FakeModule, which reads the current working file; omitting the fixture's commit therefore leaves all nine old cases passing. The frozen omission counter records one survivor (`pre/c2-base.json`).

The revised selftest keeps the real binder's battery, parser, declared-object check, git reader and token binder. Only the live-file content accessor and the Ghidra input location are redirected to controlled fixtures. After each fixture is committed, its working PROVINCE is replaced with invalid text. The genuine clean case still sees five matched cells; the duplicate case sees six matched cells with exactly `omp-pin` duplicated and rejects the record. Unknown live-input requests return no content, never fall back to a real configuration file.

The candidate's retained demonstration (`w1/ExecRecord/counter.json`) has pristine 11/0, mutant 11/2, with both integration cases reporting the absent HEAD object. Only the declared clean case determines the frozen mutation kill; the second case's failure is retained, not called an isolating sole detector. The old nine cases remain green. The canonical-layout selftest also runs without an unshipped sibling binder (`canonical-selftest.json`); measurement copies prefer the supplied sibling, normal layout falls back to the existing round-80 binder.

## Limits that affect use

- The frozen mutation counter's `ok` checks the named detector, not every prose obligation. Inspect pristine >=11/0, preservation of the nine original names and the binder's committed digest independently. ExecCounter retained false greens for undersized and dirty pristine summaries; they are not target changes or an authenticity guarantee.
- A crash or missing SELFTEST summary is not a kill. An absent or wrong detector is not a kill.
- Source selection: `git diff --no-index` compares filesystem paths, so it was refused as proof of this committed-object boundary. Its primary documentation remains authoritative for its own semantics. No duplicate URL row was added for a source already held as S261.
- No real client configuration, attached process, REA provider or inspected artifact was read by these synthetic integration cases. Neither this apparatus nor its unit fakes authenticates arbitrary receipts.
