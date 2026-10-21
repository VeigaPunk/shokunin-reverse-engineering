# ScoutOtherKind — `other` / `io_exception` findings

**Axes:** C1 calibration; C2 depth. **Scope:** read-only inspection of the named R20 extractor/contract/evidence and R21 C2 comparator/fixture contract. No source rows or production files changed; only this report was written. No external URLs were opened. No test, build, lint, smoke, REA, carrier, or provider run was performed.

## Observed source facts

- R20's producer recognizes more than `invalid_index` and `eof`: `.ufo/waves/round-20/tools/first-failure-extract.py:84-131` classifies in order as `invalid_index` with integer index, indexed `eof`, `eof` with null index for `EOFException`, `io_exception` with null index for `IOException`, then fallback `other` with null index. The `other_exception` marker is retained as `cause_line` when found; the fallback kind itself is returned even when no more specific marker matched. Thus `io_exception` and `other` are legitimate output kinds in this producer's schema, not speculative future names.
- The extractor's synthetic selftest includes `direct_other_io_exception` and expects `kind: io_exception, index: null` (`first-failure-extract.py:232-243`). That establishes a retained synthetic case, not an observed analyzer run. The R20 contract also leaves the kind alternatives open with `"invalid_index"|"eof"|...` (`.ufo/waves/round-20/contract.md:76-80`).
- R21's comparator currently avoids enum overrestriction: `.ufo/waves/round-21/tools/compare-first-failure.py:32-47` requires a nonempty string kind, nullable-or-integer `index`/`va`, and string phase; it has no kind allowlist. At lines 69-72 it compares exact `(kind, index)` and ignores `va`/`phase`. Consequently `io_exception` and `other` are evaluable with proper typed fields.
- The frozen C2 contract requires EOF with null index to remain valid and kind differences at equal index to remain a mismatch (`.ufo/waves/round-21/fixture-contract.json:19-26`). Its battery's `kind_mismatch_equal_index` case uses `other` with index 9 and expects mismatch/exit 1 (`.ufo/waves/round-21/fixtures/battery.json:161-174`). That is an intentional synthetic comparator control, not the R20 extractor's realistic `other` shape. Do not add cross-field kind/index restrictions that make this frozen case unevaluable.

## Retained-run limit and assessment

The R20 verifier spot-check records 19 retained comparisons: eight non-null `invalid_index` observations and eleven null/silent observations (`corpus/lessons/round-20-verifier-spotcheck.md:116-119`). The retained observations therefore do **not** show a real run producing `io_exception` or `other`; absence from this finite set is not evidence those kinds are invalid. The R20 source and synthetic test do establish those producer outputs. No external-source support is needed for this conclusion.

**Assessment:** preserve the current open, nonempty-string `kind` validation and exact kind/index comparison. If supplementary tests are desired, realistic `io_exception`/`other` records with null index can be added as extras, without changing the frozen C2 denominator; the existing frozen `other`/index-9 mismatch control must still pass as declared.

## Checks for parent

I ran no checks. After integration, parent should run the frozen C2 counting command against the stable lane/revision (`python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C2`), plus the parent-owned changed-path smoke and final suite once. No tools were installed or updated.

Report: `.ufo/waves/round-21/w1/ScoutOtherKind.md`
