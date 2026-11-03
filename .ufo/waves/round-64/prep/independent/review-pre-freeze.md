# Kaidoku64 independent review — pre-freeze

Non-author parent-appointed reviewer `/root/judge_kaidoku_round64`.
Base c7fe6898e9a8b3ff04486b4a1d672e9db37610c9.

## Scope and evidence

One proposed depth capability: current-host standalone bounded ZIP occurrence
inventory preserving central-directory ordinal, decoded ASCII filename,
local-header offset, size, CRC32 and actual per-occurrence SHA256, plus explicit
duplicate ordinal groups. No extraction, member execution or inference of an
application's runtime selection. No REA/Ghidra availability claim.

Read lane AGENTS, QUALITY criteria including28/32/33/38/44/48–55/57/61/67–80,
latest63 lesson and non-author review; active fleet protocol and appendix rules.
Frozen independent oracle recipe must precede candidate execution; fresh scored
cases must follow first claims freeze. All current runs are development.

## Findings addressed before freeze

1. Initial draft silently inherited ZipInfo NUL truncation. Reader now refuses
   `orig_filename != filename` and non-ASCII names with `unsupported_name`.
   Owned NUL case passes expected refusal; ordinary backslash, slash, `../` and
   absolute-looking names remain literal metadata. These paths were not extracted.
2. Novelty targeted search missed historical line-wrapped APK occurrence evidence.
   `corpus/knowledge/2026-10-13-r3-apk-inventory.md:34–43` records130 ZIP occurrences,
   120 deduplicated nodes and ordinal edges. New contribution is narrower than
   first occurrence awareness. Wide tracked sweep and narrow sweep retained.
3. Independent comparator v1 accepted bool/int equality and duplicate JSON keys.
   Both first false accepts retained; strict v3 repairs them before freeze and
   exercises8 outer CLI selftest cases. This was reviewer-authored code weakness,
   not a defect in the candidate reader.

## Independent demonstration

Fixture generator uses raw struct records and construction-derived oracle, not
candidate decisions or Python zipfile writer. Frozen dev oracle then reader:
19/19 match in final strict comparator. Positive set includes changed/equal
name duplicates, payload order reversals, central order distinct from local
header order, empty archive, metadata path spellings, STORE/DEFLATE,
128-member and1MiB-member equality boundaries. Negatives include CRC failure,
truncation, local/central name mismatch, NUL, unknown compression, encryption,
count/member/total budgets and explicitly authorized8MiB+1 archive refusal.

Strict shortcut targets all fail: collapse-by-name14/19, local-order18/19,
name-based lookup15/19, noop0/19, allfalse0/19, prior dev basename replay on
rotated vocabulary/payload lengths12/19. Partial scores are not admission.
Noop/garbage must produce parseable exact receipt or fail; exit0 alone never
passes. Exact command/output/timestamp records in dev-run*.json and
strict-control-*.json. No continuity/non-execution claim from hashes.

## Pending admission review

Author wrapper received requested first-claims-freeze identity, claim/plan
history drift and strict numeric/schema type checks. Need inspect revised bytes,
actual-shape committed sandbox dry run, first claims freeze, fresh generated
scored cases, independently rerun frozen candidate, and final file-level no-harm
and craft/source review. No closed-round verdict is issued here.

### Admission wrapper review update

Revised wrapper now rejects non-first freeze, current claim/plan history drift,
and boolean schema/numeric fields. Independent copied-script outer CLI selftest
reexecuted11/11, exit0; preserved source `admit-reviewed.py`, digest
`admit-review-pin.txt`, results `admit-selftest.json`. No further prefreeze
candidate blocker found at that read. Actual19-case committed sandbox dry run
and fresh challenge/final review remain pending. Repeated deterministic rejection
fixture bytes must be disclosed as re-observation, not19 wholly novel carriers.
