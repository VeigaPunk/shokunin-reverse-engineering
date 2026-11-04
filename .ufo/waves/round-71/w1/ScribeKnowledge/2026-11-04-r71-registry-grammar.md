source: S273 — GitHub Flavored Markdown Spec, 4.10 Tables (extension), https://github.github.com/gfm/#tables-extension- (body-row cell-count tolerance); S258, same section, is the escaped-pipe authority. Own-work authority: tools/round-71/registry-census.py and plans/round-71-claims.md, pinned by .ufo/waves/round-71/claims.json.
verified-at: b827a8b5d54f2885ec9be7786389f356c59226ce (operative freeze; source/code reading, not a measured-after claim).
recheck: `python3 -I -B tools/round-71/registry-census.py --root . --rev "$MEASURED_REV" --generate --out "$SEAT_FINDINGS/registry-census.json"`; `TMPDIR="$SEAT_SCRATCH" python3 -I -B tools/round-71/registry-census.py --selftest` (use existing seat-owned absolute output/scratch directories).

# Round 71 — registry row grammar v2

## Evidence status and source boundary

This is a knowledge draft, not an execution receipt. R71-C3 is the operability capability-acquisition claim; R71-C1 is coverage and R71-C2 calibration. Promotion and first-working-round admission require the measured-revision receipts and wave findings, not this entry's contract description.

ScoutSource reports opening S273 on 2026-11-04T05:12:42Z: HTTP 200, 508310 bytes, sha256 `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220`, snapshot `.ufo/waves/round-71/w1/ScoutSource/gfm-4.10.html`, source filing `.ufo/waves/round-71/w1/ScoutSource/sources.md`. These are scout-attributed observations, not fetches performed by this scribe. The bytes match S258's round-58 snapshot but the scopes differ.

S273's body-row clause says: “The remainder of the table’s rows may vary in the number of cells.” Short rows receive empty cells; excess cells in long rows are ignored. S258 separately says: “Include a pipe in a cell’s content by escaping it, including inside other inline spans:”. Thus a short registry row can be valid GFM while violating lane occupancy requirements. The middle-cell join below is the lane's declared compatibility grammar, **not** GFM's rule for retaining excess cells.

## Grammar v2

Read only the block delimited by `<!-- instrument-registry v2 -->` and `<!-- /instrument-registry -->`. Strip surrounding whitespace, split table rows on unescaped pipes, and turn `\|` into a literal pipe inside a cell. Cells 0–3 hold tool, purpose, verdict map and selftest. Owner is the last cell; write scope is second-last; pinned value is all cells between selftest and those final two cells, joined with `|` (`cells[4:-2]`).

The frozen census declares conformance as at least six cells, a backtick-delimited normalized repository-relative tool path existing at the measured revision, and a nonempty joined pinned value (an em dash is empty). Exactly six cells leave no pinned middle cells and are therefore named `pinned-empty`. Duplicate registered paths are reported separately. This is a bounded structural census, not verification that every purpose, verdict, selftest, owner or pinned artifact is semantically correct.

## Two filed shapes, one disclosed repair

The four round-69 rows for `packed-elf.py`, `mutation-check.py`, `contract-probe.py` and `controls.py` have eight cells because their pinned-value text contains a bare pipe. Grammar v2 reads the two middle pieces as one pinned field while preserving owner/write positions. They are historical filed bytes: read them with the declared join rule, never rewrite them to make a newer parser convenient. GFM itself would treat their excess cells differently; this compatibility rule must remain explicit.

The six round-70 rows for `packed-elf.py`, `mutation-check.py`, `contract-probe.py`, `seam-probe.py`, `forged-receipts.py` and `controls.py` omitted the owner cell. The committed before receipt `.ufo/waves/round-71/l1/pre/c3-at-base.json` names all six with `['pinned-empty']`, among 88 rows/88 paths, four multicell rows, no duplicates, `ok false`, revision `82c8e620c9222fb218aa0260570a3765da2afb44`. The missing owner shifts the positional interpretation and collapses the pinned middle slice; the census does not diagnose this as invalid Markdown.

The declared round-71 repair appends the omitted owner to those six rows, with old→new disclosure in LOG.md and the lesson. This is a data repair, not permission to accept omitted owners. Its after-state must be established from the measured-revision census and disclosure; this scribe did not execute the repair or census.

## Capability and failability

`tools/round-71/registry-census.py` can enumerate the whole marked registry, report paths, four historical multicell rows, duplicates and each nonconformant row without the old exact-seven-cell parser dying first. Exit 0 means no named findings; exit 1 means nonconformant rows or duplicates; exit 2 means unavailable input or malformed markers/row structure. Rows with conformance defects are named rather than silently skipped.

Its frozen 14-case selftest covers clean seven-cell data, round-69 eight-cell joins, pinned-field reconstruction and final-column positions, escaped pipes, six-cell and undersized rows, absent paths, duplicates, and CLI clean/six-cell/duplicate/absent/marker cases. This documents the selftest's scope, not a claim that this seat ran it. R71-C3 requires all 14 green, zero after-state nonconformant rows/duplicates, paths equal to rows, the four historical multicell rows retained, and six repaired seven-cell round-70 rows; its base arm requires the six named findings and the legacy census exit 2.

## Limits

The parser is not a complete GFM implementation: it reads only the marked registry block, strips leading spaces (and other surrounding whitespace), and does not parse inline HTML or implement the full inline/block grammar. In particular, grammar-v2 middle-cell joining is a registry compatibility policy, not GFM renderer behavior. A nonconformant data row is named rather than skipped; structurally unevaluable input fails with exit 2.

The historical census remains frozen, not repaired in place: the assignment calls this “the round-50 census3 stays byte-identical”; the frozen instrument and R71-C3 actually identify `tools/round-51/census3.py`. No round-50 census3 file was found in the listed round-50 tool directory. This naming discrepancy is disclosed, not silently corrected; byte identity is a preservation obligation, not a comparison executed by this seat.

The census checks registry structure/path existence, not arbitrary row semantics or pinned-file contents. It does not establish seam runtime safety, cryptographic receipt authenticity, semantic equality of recovered binaries, or any other claim axis.
