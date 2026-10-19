# proposed-v1-compliance-mode — patch text for the v2 custody tool (EX-31's target)

Authored by SEAT EX-35 (chain c3, executor). **Patch text only**: `.ufo/gates/custody-pair/`
is EX-31's write target. Verified against tool revision
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`; measurements
and the full matrix are in `backcompat.md` §§3-6.

## What already works (no change needed)

Three v1 shapes parse and compare on the fields they carry; sha256 is compared
in every mode (`SHA256-CONTRACT: n/m paths agree on sha256`), the v1 label
defect is reproduced as a finding rather than swallowed, and the round-boundary
case verifies: round-1 v1 receipt vs round-2 v2 receipt → sha256 5/5, no
CONTENT-DRIFT/REWRITE-DRIFT (exit 12 attributable to the label finding alone).

## Change 1 — exit-code semantics for known-v1 references (the back-compat gate)

Measured problem: a v1-form reference can never exit 0 in `--live` mode
(v1 receipt vs live → exit 12; the same receipt with only the `MTIME_UTC:`
lines removed → exit 0). A gate keyed on `exit == 0` therefore fails every
round-1 receipt, so "v1 receipts remain verifiable" is readable only from the
`SHA256-CONTRACT` line. This is the *declared* contract, not an oversight —
`README.md:83` lists the v1 label defect under exit 12, `README.md:107-111`
defines the v1 comparison classes, and `README.md:109` states an unparsable
receipt is exit 2. So there are two acceptable resolutions; pick one and record
it (both leave the finding visible in every case):

```
# Option A (preferred): explicit mode, findings stay visible
verify ... [--v1-compliance]
  -> when the reference parses as v1 (stanza-v1/sums-v1/pipe-v1) and the ONLY
     non-MATCH findings are LABEL-DEFECT on v1 time strings, print the findings
     as before, add a summary line
       V1-COMPLIANCE: sha256 agreed on n/n paths; LABEL-DEFECT reproduced (round-1 form)
     and exit 0 (sha256 contract) instead of 12.

# Option B: --v1-label-defect=note|fail   (default fail = current behaviour)
     note -> LABEL-DEFECT is printed but not counted toward severity; exit per
             remaining findings.
```

Documented alternative (zero code change): the parent records that the
back-compat gate is the `SHA256-CONTRACT` line, **not** the exit code, and any
consumer of a v1 receipt must read that line. If this is chosen, the tool's
docstring should say so where it currently describes the exit-code contract
(`custody-pair.py:61-73`).

## Change 2 — reference coverage (measured gap A5)

Measured: a reference carrying 1 of the canonical 5 paths verifies clean
(`MATCH-V1-PARTIAL 1/1`, exit 0) with the other 4 custody paths unaccounted for.
That is the round-1 H1 shape (unaccounted scope reads as pass) applied to
receipts. Proposal:

```
verify ... [--require-paths N]      # or --cover-default-paths
  -> exit 2 (usage) when the reference's path count < N, with
     REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>
```

The default path list is already in the tool (`CUSTODY_PATHS`, `custody-pair.py:111-116`);
`--require-paths 5` on the canonical set is the natural gate for the round's own
pre/post pair.

## Change 3 — crash discipline (measured A6, transient)

An intermediate revision crashed with `KeyError: 'sha_agree'` inside
`verify_sets` (traceback, exit 1). Contract says usage errors are exit 2; a
crash must never present as a numeric drift class. Proposal: wrap the
subcommand dispatch in a `try/except Exception` that prints
`CUSTODY_PAIR_ERROR: <type>: <msg>` and returns 2.

## Test vectors (this directory, all scratch-safe)

| vector | expected under Option A / `--require-paths 5` |
|---|---|
| round-1 `config-pre-pair.txt` vs live | sha256 5/5; findings reported; exit 0 (A) |
| `fixtures/v1-swap-sha.txt` vs live | CONTENT-DRIFT ×2, exit 10 (unchanged) |
| `fixtures/v1-corrupt-sha.txt` vs live | CONTENT-DRIFT ×1, exit 10 (unchanged) |
| `fixtures/v1-absent-path.txt` vs live | ABSENT, exit 13 (unchanged) |
| `fixtures/v1-partial-1of5.txt` vs live | exit 2 under `--require-paths 5`; exit 0 today |
| `fixtures/empty.txt`, `fixtures/comment-only.txt` | exit 2 (already correct) |

Cross-reference: `backcompat.md` §5 (attack verdicts), §6 (residuals).
