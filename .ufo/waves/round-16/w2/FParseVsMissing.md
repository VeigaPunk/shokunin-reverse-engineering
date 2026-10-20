# FParseVsMissing — wave-2 falsification report (C1 depth, parse-vs-missing boundary)

Seat: `KaidokuR16.FParseVsMissing` (executor, leaf). Scope: attack the produced
round-16 C1 artifact `selection.py` + its fixture schema on the
parse-failure-vs-file-absence boundary, author independent schema-conforming
adversarial cases, and report. No implementation edits, no test execution
(L1 owns the single post-integration verification pass).

## Files changed

- `.ufo/waves/round-16/w2/ParseVsMissing-cases.json` — NEW, 16 cases
  (selfcheck schema: `{"cases":[...]}`, `id`/`request`/`goos`/`goarch`/`files`/
  `expected` or `expect_error`; raw-string and `raw_b64` payloads exercised).
  No other file touched.

## What the cases pin (all expectations handwritten from source law)

Unreadable **base** must raise `UnreadableError`, never degrade to
`missing_base` or a synthesized empty parse:

1. `w2-parse-unreadable-base-empty-file` — 0-byte present base → EOF at
   `beginObject` (GoApiSnapshot.java:215).
2. `w2-parse-unreadable-base-whitespace-only` — nonzero bytes, still EOF.
3. `w2-parse-unreadable-base-truncated-object` — `{"all": {` cut mid-value.
4. `w2-parse-unreadable-base-missing-colon` — `{"all" {"x":1}}`, strict
   gson-2.13.2 `MalformedJsonException` (installed jar
   `Ghidra/Framework/Generic/lib/gson-2.13.2.jar`).
5. `w2-parse-unreadable-base-top-level-empty-array` — `[]` fails
   `beginObject` (:215, BEGIN_ARRAY).
6. `w2-parse-unreadable-base-top-level-scalar-string` — `"all"` is a NAME
   token, not an object; guards name-sniffing shortcuts.
7. `w2-parse-unreadable-base-top-level-number` — `42`, NUMBER token.
8. `w2-parse-unreadable-base-top-level-null` — `null`: present document,
   wrong shape. Sharpest parse-vs-missing edge.
9. `w2-parse-unreadable-base-invalid-byte` — `raw_b64` `b'\xff'` alone.
10. `w2-parse-unreadable-base-control-char-in-name` — `raw_b64` of
    `{"a\x01ll": {}}`: unescaped control char inside a quoted member name.
11. `w2-parse-unreadable-base-not-rescued-by-diff` — corrupt base + valid
    `patchverdiffs/go1.21.3.json.diff` still raises: the runtime feeds the
    same unreadable bytes through `JsonPatchApplier` (:133-144).

Positive/calibration counterparts (exit-0 results, not errors):

12. `w2-parse-empty-object-base-with-exact-diff` — present valid `{}` base
    (3-byte fixture serialization, `size:3` pinned) → `exact_diff`,
    `base_matching_buckets: []`, `base_matching_buckets_source:
    "unpatched_base_file"`. Parsed-empty is NOT missing.
13. `w2-parse-missing-base-empty-root` — empty readable root →
    `missing_base` with `base_matching_buckets_source: null` and
    `selected_patch: null` (not 0). The `..._source` null-vs-string pair is
    the discriminator against a parsed-empty misreport.
14. `w2-parse-missing-base-empty-patchverdiffs` — populated `patchverdiffs/`
    (non-diff member) without base → `missing_base`; base check precedes the
    diff scan (:122-126).
15. `w2-parse-missing-base-directory-named-base` — a directory named
    `go1.21.0.json` → `missing_base`. Verified in source:
    `Application.getDataFileInModule` throws FileNotFoundException on
    `isDirectory()` (Application.java in Generic-src.zip, ~:368-371),
    caught by `getApiSnapshotFile` (:168-177) → null. Model's `is_file()`
    gate (selection.py:130) is the equivalent.
16. `w2-parse-base-only-patchverdiffs-is-file` — `patchverdiffs` as a
    regular file → `base_only`, `selected_patch:0`; source probes
    `patchverdiffs/go1.21.x.json.diff` under a non-directory and finds
    nothing (:152-157, :128-131).

## Findings (model-vs-source divergences, bounded)

**D1 — Trailing garbage after the top-level object: model rejects, source
accepts.** `_top_level_keys` (selection.py:154-163) uses `json.load`, which
requires whole-document EOF → `{"all": {}} }` raises UnreadableError. Java's
`JsonReader` returns after `endObject()` (:225); `close()` does not assert
EOF. Source-law: trailing bytes are ignored. No fixture encodes this
(handwritten expected values only); flagged for L1 adjudication — the
readable-but-corrupt outcome would be `base_only`/`exact_diff` with parsed
keys, not an error.

**D2 — `NaN`/`Infinity` literals: model accepts, source rejects.** Python
`json` maps `NaN`/`Infinity`/`−Infinity` to floats by default
(`parse_constant`); strict gson-2.13.2 `JsonReader` throws
`MalformedJsonException` on unquoted non-numeric constants. A base like
`{"all": NaN}` yields a parsed empty-ish object under the model where the
source fails at :216-222. Same class as D1 but inverted strictness.

**D3 — Invalid UTF-8: model strict, source tolerant.** `open("rb")` +
`json.load` strictly decodes UTF-8 → `UnicodeDecodeError` → UnreadableError.
`new InputStreamReader(is)` (:214) uses the default charset decoder, which
REPLACES malformed input → the Java reader parses (with mojibake content)
rather than throwing. Confirmed only as code-reading, not executed.

**D4 (calibration note, not a defect)** — For top-level non-object
documents the Java failure is `IllegalStateException` (RuntimeException)
from `beginObject` (:215), not `IOException`; it propagates out of `get()`
despite the `throws IOException` clause. The model's UnreadableError is an
API-level rejection claim, and fixture notes now state this explicitly
(cases 5-8). Consistent with the existing `unreadable-base-json-array`
note convention in `negative-fixtures.json`.

**D5 — Second-open TOCTOU on the base file.** `_describe_file`
(selection.py:124-144) stats+hashes the base, then `_top_level_keys`
(:154-167) re-opens and re-reads it. If the file changes between the two
opens, the reported `sha256`/`size` describe different bytes than the parsed
`base_matching_buckets`. A present-file consistency gap, only observable on
a mutating root; bounded.

**D6 — diff listing conflates OS errors with absence.** `except OSError:
entries = []` (selection.py:219-222) maps any `iterdir` failure
(e.g. permission-denied on a real `patchverdiffs/`) to "no diffs" →
`base_only`. The source probes exact paths (`getApiSnapshotFile`, :152-157)
and would still find a diff that `iterdir` cannot enumerate; conversely an
unreadable base is never probed by listing. Parent notes this lane is
already being repaired in the integrated selection; recorded here as the
falsified state of the wave-1 artifact I read. Not fixture-expressible
(runner creates a readable temp root).

## Non-findings (checked, no defect)

- `is_file()` on a directory-named base → `missing_base` matches
  `FileNotFoundException`+catch→null in source (case 15).
- `missing_base` early return precedes diff scan (:122-126 vs
  model :196-213) — diff never rescues absent base.
- `selected_patch` null (missing) vs 0 (patch-0 byte source, :266-267)
  correctly separates absence from base-only selection.
- Docstring line anchors checked against Base-src.zip member: get()
  arch-order List.of :108-109, base-always-patch-0 :122-123, diff null→base
  :128-131, derived provider :133-144, diff countdown :148-166, filename
  builder :168-177, IS_GOOS_UNIX :180-181, getApiFile two-part fallback
  (excluded by contract) :183-192, beginObject :215, LinkedHashMap/isEmpty
  filter :228-232, EMPTY :242. No drift.

## Limits

- No execution: expectations derived from Base-src.zip member source,
  gson-2.13.2 strictness, and the materialization rules in
  selfcheck.py:120-156 only. D1-D3 assert parser-semantics divergences that
  are certain on the Java side (code-visible) but unobserved on the running
  model.
- Filesystem-permission and symlink cases are not expressible through the
  `files` mapping; D5/D6 are reading-only findings.
- `expect_error` uses `{"type":"UnreadableError"}` type-substring matching
  per schema; no exception-message coupling asserted.
- Tool installs: none.
