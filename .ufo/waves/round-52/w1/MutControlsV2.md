# MutControlsV2 — round-52 w1 (attack): dead-control report

Seat: MutControlsV2 (mutation-tester, leaf, no subagent dispatch). Status: settled.
Full table: `.ufo/waves/round-52/w1/MutControlsV2/findings.md`.

## Verdict

The claimed R52-C1 and R52-C2 control designs contain dead controls, one missing detector for the
central defect class, and one predicate-level defect that kills a control. Nothing was changed in the lane.

## Most important findings (measured)

1. **Zero claimed arms detect the central defect.** Mutant M-DEFECT-1 (empty `allowed[kind]` treated
   as allow-all) moves only an injected device-gap arm (0/4 -> 4/4). CTL-OLD, CTL-NEW, M1, CTL-JUNK,
   M2 stay unchanged. CTL-DN accepts exit 2, so any crash is green. M1's expected RED depends on
   `law_shape_ok`, which the v2 draft does not contain (its disposition-level result is 4/4 GREEN).
2. **Identity and provenance are unbound pre-freeze.** 8 of 9 passing four-carrier multisets score the
   wrong carrier set while passing CTL-OLD=2 and CTL-NEW=4. Pre-freeze controls waive provenance by
   design, so no pre-freeze arm binds a foreign-round receipt. Missing controls: identity, foreign-round,
   device fail-closed fixture, shape-neutral pair, retry-policy ENOENT, census re-derivation, depth-gap.
3. **Claim commands that cannot run as written.** C2 before-arm `--table tools/round-50-c3` is not a v5
   flag (exit 2, verified). `--freeze` must be an ancestor of `--rev`; the claimed before-arm with the
   round-52 freeze exits 2. **census_outside** at landing is 7 (simulated) unless `census3.json` is
   regenerated in the freeze commit; the claims name no regeneration.

## Scope and evidence

- Probes (scratch, copied to `MutControlsV2/`): `probe_disposition.py`, `probe_law_surface.py`,
  `probe_failclosed.py`, `probe_carrier_set.py`, `mutation_probe.py`; receipts in
  `MutControlsV2/receipts/` with `SHA256SUMS`; `MutControlsV2/mutation-probe.json`.
- Counter functions imported read-only from `tools/round-50/c1-counter.py`; v5 and census3 run with `-I -B`.
- Not run: REA, `--data-run`, carrier download, network. Rule-scoped results only; the full counter has
  no controls mode.
- `[code-read]` items: silent detail consulted only when `required` is true; driver's CTL-DN check.

## Lane hygiene

- No lane file modified; `git` read-only commands only. Lane `git status` shows pre-existing items
  (`M .ufo/waves/round-50/w3/ScribeEntryC1.md`, untracked round-52 dirs) that are not mine.
- I wrote one file to `/tmp` (`/tmp/pristine-hashes.txt`) by mistake and removed it.
- A lane `tools/round-50/__pycache__/c1-counter.cpython-314.pyc` exists, dated 2026-10-29 (before this
  seat); I did not create it and did not delete it.
- Tools installed or upgraded: none.

## Recommended claim amendments (L1 decides)

Listed in findings.md §5: fix CTL-DN; add DEVGAP, identity, foreign-round, shape-neutral pair,
retry-ENOENT and census-re-derivation arms; specify `law_shape_ok` before claiming M1; retire CTL-JUNK
and M3/M4 as separate arms; repair the C2 before-arm; add census regeneration to the freeze commit;
add exit-2 fail-closed gates to the audit and census guards.

Artifacts: `MutControlsV2/findings.md`, `MutControlsV2/receipts/`, `MutControlsV2/mutation-probe.json`,
`MutControlsV2/*.py`, `MutControlsV2/status.json`.
