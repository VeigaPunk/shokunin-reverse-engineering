# QUALITY #17 — candidate row (supersedes #16)

status: draft record, not a corpus edit. L1 reports the final row 17 is already integrated at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:27` (observed 1222 characters, supersedes cell `16`, file SHA-256 `2052ed505888c5cc2e9cd78fa5eb9f76eb71c2dbbb31842107ca592849be1fb3`). This seat did not write that file. The row below is the drafted candidate, retained as a precision variant rather than a required replacement.

## Draft row

| 17 | Supersedes #16's manual-only ambiguity while retaining its fidelity rules: research Gate quotes must copy a contiguous located passage, never splice or reuse another rendering's locator. Machine-gradeable input is a captured raw UTF-8 prose excerpt with Markdown ATX or single-line HTML h1–h6 headings; retain its pinned `quote-fidelity` manifest and verdict. Missing or mislocated raw quotes are rejected; exit 2 is unevaluable, never clean. Code members, commit objects, JSON, command output, and rendered quotations that span, strip, or decode markup or character references MUST NOT be submitted as machine-gradeable: check the appropriate source manually under #1, and a raw green on them is not evidence for their rendered or representation-specific wording. Raw-copied tags are not the excluded rendered form. The script has no unsupported-representation classifier and normalizes neither quote nor source: an excluded submission follows the ordinary raw rules and may yield exit 0, exit 1 (`quote_not_contiguous` when a rendered form is absent from the raw bytes, `quote_location_mismatch` when the literal text lies outside the declared section, or `quote_too_long`), or exit 2 only through an invalid-manifest, source-tamper, or snapshot-tamper finding; no verdict on such an input is admissible evidence. Green raw checks prove only pinned substring/section consistency, not upstream authenticity, completeness, semantic support, or held capability; this row narrows admissible use and adds no gate capability. | `corpus/lessons/round-15.md`, Mistakes and Gate; routed defect 2 in `corpus/lessons/round-14-verifier-spotcheck.md:172`; gate exit map `.ufo/waves/round-14/tools/quote-fidelity.py:78,97-100,250-268` | 16 |

## Delta against the integrated final row (observed)

The final row already:

- retains #16's contiguous/located passage, no-splice/no-foreign-locator rule, pinned manifest+verdict, and "exit 2 is unevaluable, never clean";
- names the manual-only classes and extends them to character references, with "raw-copied tags are not the excluded rendered form";
- states there is no representation classifier, that an excluded submission may receive 0/1/2 through ordinary raw/malformed/tampered rules, and that such a verdict is void for the manual-only claim;
- records the isolated rendered control's raw-substring miss as exit 1, not an unsupported-input classification;
- cites `corpus/lessons/round-15.md` and uses supersedes cell `16`.

This draft's material additions are only the literal finding ids `quote_not_contiguous`, `quote_location_mismatch`, and `quote_too_long`, plus the named CNE triggers. That is precision, not a different policy: the integrated row already states the exit-1 outcome and denies classifier status. No replacement is requested.

## Static evidence for the draft

1. `quote-fidelity.py:35-36` applies no whitespace/tag/punctuation normalization; `:40-41` define `quote_not_contiguous` and `quote_location_mismatch`; `:78` limits exit 2 to `invalid_manifest`, `source_tampered`, `snapshot_tampered`; `:97-100` maps any other finding to exit 1.
2. `grade_quote` at `:250-268` checks word count first (`quote_too_long`, exit 1), then exact whole-source membership (`quote_not_contiguous`), then exact heading selectors and section body (`quote_location_mismatch`).
3. The sibling synthetic control `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json` quotes `Use raw bytes.` while `raw-source.md` contains `Use <em>raw</em> bytes.`; the rendered string is absent, so the code path is `quote_not_contiguous@rendered-text`, exit 1. The manifest's source digest `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270` matches the observed `sha256sum` of the source. Code-derived, not executed.
4. `corpus/lessons/round-15.md` exists (73 lines at read, uncommitted) and its Mistakes row at line 65 records routed defect 2 and the #17 policy; `LOG.md:1855-1858` records the same correction.

## Limits

- Static reading only; no gate invocation, selftest, frozen run, census, build, test, lint, or formatter.
- The integrated row is L1's final text; this file is not integrated and should not be inserted as a duplicate.
- Finding-name precision is code-derived; L1's recorded execution of the boundary control is the confirmation point.
- No installs or updates.
