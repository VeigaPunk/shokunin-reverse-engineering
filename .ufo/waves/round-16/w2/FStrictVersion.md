# FStrictVersion — wave2 falsifier report (strict request grammar attack)

Attack: C1 strict-version parse surface — newline smuggling, non-ASCII (Unicode Nd)
digits, Java-int overflow/boundary — plus one bounded source-divergence note.
Artifact attacked: `.ufo/waves/round-16/selection.py` (+ `selfcheck.py` schema);
fixtures authored at `.ufo/waves/round-16/w2/StrictVersion-cases.json` (20 cases,
all handwritten expectations; no execution, per wave rules).

## Findings on the produced artifacts

1. **Strict-parse surface holds under all four attacks — no defect found in
   parse path.** `_VERSION_RE` uses literal `[0-9]` classes (selection.py:50),
   `fullmatch` at :77 (trailing `\n`, `\r\n`, embedded `\n`, trailing space all
   rejected; a `re.match`+`$` impl would wrongly accept trailing `\n`), a
   pre-`int()` >10-digit length guard at :83-88 (prevents a plain `ValueError`
   from Python's ~4300-digit `int()` limit escaping as an untyped traceback
   instead of RequestError/exit2), a per-component `> _JAVA_INT_MAX` range check
   at :90-94, and the `(0,0,*)` INVALID-sentinel check at :95-99. Boundary is
   inclusive: `2147483647` components parse and yield `missing_base`; `0.1.0`
   parses (only `0.0.x` is INVALID). Every rejection raises typed `RequestError`
   before any filesystem access, matching exit-2 contract.

2. **Duplicate `arch_search_order` entries — confirmed source-faithful, NOT a
   divergence (correction of my initial claim).** `arch_search_order`
   (selection.py:109-115) emits `goos` twice when `goos==goarch` or
   `goos=="all"`, e.g. `["linux-linux","linux","unix","linux","all"]`. I
   initially reported a `List.of` `IllegalArgumentException`-on-duplicates
   divergence; that conflated `List.of` with `Set.of`/`Map.of`. Verified
   against JDK 21 sources (`ImmutableCollections.listFromTrustedArray`
   null-checks only; `List` javadoc specifies no dup rejection) and the shipped
   source (`List.of(...)` at GoApiSnapshot.java:109-110 retains dups; `read()`
   iterates it against a `Set` membership test at :228-237). The emitted list
   carries the dup while bucket matching dedups — exactly the model's behavior
   (emitted at :109-115, dedup at :243-249). Pinned by case
   `strict-duplicate-order-dedup`; no defect.

3. **Bounded divergence (unexpressible in fixtures, not a defect): a directory
   named like a diff is skipped.** `_describe_file` requires `is_file()`
   (selection.py:124), so `patchverdiffs/go1.21.3.json.diff/` (directory) falls
   through to a lower patch instead of being selected-then-failing. Java
   `getPatchVerDiffFile` probes `exists()`-style and would return the directory
   as the diff file, failing later at `JsonPatch.read`. Not reachable via the
   files-mapping schema (no directory entry type); recorded as limitation only.

4. **Overflow in diff-scan is unreachable — confirmed, no defect.** `_DIFF_NAME_RE`
   (selection.py:55-56) feeds `int(m.group(3))` at :222 without a range check;
   an 11+-digit filename could raise plain `ValueError` (or overflow a Java
   int). Unreachable in practice: POSIX NAME_MAX=255 bounds the digit run to
   ≤249 chars, far under Python's 4300-digit `int()` limit, and any numeric
   value `> patch` is simply skipped by the `0 < cand <= patch` filter.
   Verified safe but worth a comment.

## Fixture coverage delivered (20 cases)

- **Newline/whitespace:** trailing `\n`, `\r\n`, embedded `\n`, trailing space —
  each with a planted resolvable base so a buggy accept produces a wrong
  success (base_only), not a masked error.
- **Non-ASCII digits:** fullwidth `５` (with planted `go1.21.5.json.diff` —
  a `\d`-regex + `int()` impl would normalize to 1.21.5 and wrongly return
  exact_diff), full Arabic-Indic version `١.٢١.٠`, mixed BMP+plane-1 `1.2𝟙.0`,
  plus fullwidth and leading-zero digits *inside diff filenames* (must be
  skipped → base_only/selected_patch=0).
- **Java-int overflow/boundary:** int-max+1 on each of major/minor/patch,
  11-digit component (length-guard path), `0.0.5` INVALID sentinel (with
  planted `go0.0.0.json` — buggy accept → wrong base_only), all-components
  `2147483647` → missing_base, and `0.1.0` → missing_base (calibration: only
  `0.0.*` is INVALID).
- **Selector validation:** empty `goos`/`goarch` → RequestError before fs access.
- **Int-max bounded by installed listing:** request `1.24.2147483647` with a
  tree mirroring installed 12.1.4 (`patchverdiffs/go1.24.{1,5,6}.json.diff`;
  real root tops at go1.24.6, bases go1.15.0–go1.25.0) →
  `fallback_diff`, `selected_patch: 6`, `selected_diff:
  patchverdiffs/go1.24.6.json.diff` — same outcome the installed root yields.

## Schema conformance

Bare-`{"cases":[...]}` form; error cases use `expect_error: {"type": ...,
"contains": ...}` (message substrings copied verbatim from selection.py:
"expected stable M.m.p" :79, "Java int range" :88/:93, "INVALID sentinel" :98,
"non-empty string" :105/:107). Positive cases pin `status`, `selected_patch`
(null on missing_base, 0 on base_only — both emitted forms), basename/relative
`base`/`selected_diff`, ordered `arch_search_order`, and `base_matching_buckets`.
`note` fields are out-of-schema but tolerated (runner ignores unknown keys).

## Limits

No execution per wave contract — expectations are handwritten from
selection.py source reading; L1's gate run is the check. Directory-in-diff
divergence is unfixtureable by design (files mapping has no dir type); reported
as text only.

## Tooling

None installed or updated.
