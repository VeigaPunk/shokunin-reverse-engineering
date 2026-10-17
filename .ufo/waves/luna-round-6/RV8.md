## CLAIM
All 10 required leg receipts are present, non-empty, and include command, stdout, stderr, and exit fields.

## METHOD
Read-only audit of `.ufo/waves/luna-round-6/receipts/leg-1.md` through `leg-10.md`, checking file existence and, for existing files, content and non-emptiness. `Glob` for `.ufo/waves/luna-round-6/receipts/leg-*.md` returned “No matches found.” A Python existence check reported `leg-1.md: MISSING` through `leg-10.md: MISSING`.

## FINDINGS
None of the ten expected receipt files exists. Consequently, none can be verified as non-empty or containing the four required fields. The target wave directory was absent at audit time (`test -d` output: `missing: .ufo/waves/luna-round-6`).

## THREATS
This completeness check cannot establish whether probes ran or what their outcomes were; it only establishes that the expected receipt artifacts were unavailable at the checked path.

## VERDICT
FINDING: all 10 expected receipt files are missing.
