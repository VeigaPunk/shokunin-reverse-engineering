# Round 70 claim falsification

Axes: R70-C1 calibration/provenance; R70-C2 operability; R70-C3 coverage.

## R70-C1 — counterexample found (checker predicate under-validates receipt)

Using the genuine declaration receipt as the template, I set its top-level `rev` and `instrument.rev` to `8b82516182a269482f3a7dc96b50cd2ac349f3a6`, preserving its genuine `instrument.path` and `instrument.sha256` (the frozen producer blob). For each shape below, I altered only the named field and ran:

`python3 -I -B tools/round-70/packed-elf.py --check-receipt <shape.json> --root <repo> --rev 8b82516182a269482f3a7dc96b50cd2ac349f3a6`

All returned 0 with `met: true`, `failing: []`: (1) `carriers[*].unpacked_counts` replaced by `{"procedure_count":999}`; (2) `carriers[*].refusal` replaced by `{"packed_rc":0}`; (3) `carriers[*].packed_sha256` set to 64 zeroes; (4) `carriers[*].runs` replaced by `{}`; (5) top-level `before_ceilings` replaced by `[]`; (6) `carriers[*].format` replaced with a false format object. This directly falsifies receipt-reader binding to verdict-relevant evidence for these fields. The specific omission is visible in frozen `packed-elf.py:365-485`: the checker derives/verifies row IDs, pins, source, kind, ceiling, arms, original procedure count, packed procedure ceiling and ratio, but never reads these six fields. Notably this is the frozen C3 checker, not proof that the separate forged-receipt probe's F1-F10 battery has those same blind spots.

## R70-C2 — requested seam subattacks

The frozen source establishes that the specified self-deleting-log impostor is not directly injectable: A1 constructs its own fixed shell script at `seam-probe.py:184-189` (`touch <log>; exit 0`) and passes that path to the instrument; there is no CLI parameter to replace that script. It checks both typed hash refusal and absence of that file at lines 190-194. Thus the requested self-deleting variant is rejected as an unavailable attack path, not a falsification of the actual frozen arm.

A2's potential vacuity is blocked by the implementation: `seam-probe.py:207-215` requires every carrier's `pack` and `unpack` argv to exist, records missing entries, and computes success only when `not defects and not missing`; earlier refusal therefore makes A2 false, rather than vacuously green.

A3 is more limited than its prose label: `seam-probe.py:225-237` tests committed `REGISTERED_CASES` names and green selftest count, but no direct assertion that each allowlist is passed to subprocess exists in this arm. However the producer's current implementation at `packed-elf.py:563,567,573,588` passes `env=packer_env_cenv` on every upx call. This inspection does not demonstrate an attack that meets the frozen claim predicate; it identifies that A3's predicate is a registry/selftest check, not an independent runtime audit of subprocess env.

A7 performs two sequential battery invocations (`seam-probe.py:284-301`), not concurrent runs. I did not establish an actual collision; its two-distinct-work-dir observation does not prove concurrent isolation. Treat concurrent-collision resistance as unverified by this arm, not as an observed defect.

## R70-C3 — checker accepts dynamic format in static carrier row

Starting with the genuine four-carrier declaration receipt and valid producer binding, I copied the `jq` row's `format` object (ELF `DYN`, position-independent executable) onto the `dinit` row, leaving its declared `id`, pin, source, `kind: static-exe`, original counts and other table-bound fields intact. Running the same frozen checker command returned 0, `met: true`, `target: 4`, `carriers_matched: 4`, `failing: []`. The checker never validates `format` or inspects source bytes; it only compares the row's reported kind against the table (lines 422-435). This is a receipt-level counterexample to the notion that the checker binds a static carrier to evidence that it is actually static. It does not establish that the measured genuine `/usr/bin/docker-init` is dynamic; the copied format is deliberately fabricated.

Control: replacing dinit `orig_counts` with libz `orig_counts` while keeping the rest of the receipt intact returned 1 and named `dinit: orig_procedures 184 != declared 1268` (checker lines 452-460). So the specific copied-count attack is rejected by the declared procedure-count clause.

## Smallest safe correction

For C1, extend the frozen receipt checker/probe contract to require and validate all verdict-relevant evidence fields rather than silently ignoring them (including unpacked identity/counts, refusal, packed hash, run records and ceiling table), with a clear clause per field. For C3, validate the measured ELF identity from reproducible artifact evidence (or bind a content hash plus format/type evidence to the pinned carrier); a receipt-supplied kind alone is not proof of static linkage. C2's requested A7 needs genuinely concurrent runs to claim concurrency coverage; A3 would need an explicit runtime child-env observation to prove env delivery.

VERDICT: R70-C1 not met for the six tested lying fields; R70-C2 requested A1/A2 attacks rejected or not demonstrated (A3/A7 coverage limitations noted); R70-C3 defect: fabricated dynamic format for static row is accepted, while copied libz original count is rejected.