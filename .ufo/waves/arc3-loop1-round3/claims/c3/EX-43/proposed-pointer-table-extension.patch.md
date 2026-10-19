# Proposed change — pointer-table arc3-era extension (chain C3, wave arc3-loop1-round3)

Author: seat EX-43 (before-state, executor) · applies to `.ufo/gates/citation-drift/pointer-table.json`
(the real target is EX-41's to write; this seat never touched it).

## What

Append the 17 entry objects in `claims/c3/EX-43/candidate-entries.json` → `entry_candidates`
to the table's `entries` array, and the 1 object in `quoted_candidate` to the table's `quoted` array.
**Single source of truth for the object text is that JSON** — this file deliberately does not restate
it (two copies would drift; rule #14 discipline).

Order is irrelevant to the probe (it iterates `entries` then `quoted`; no existing entry's `line` moves),
but appending after the last existing entry is the lowest-noise form.

## Before → after

- before: 31 entries / 4 quoted / 14,694 B / sha256 `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
- after (if all candidates land): 48 entries / 5 quoted; expected clean run (`findings=0`) in both modes.

## Landing procedure (the F3 coupling)

1. Apply the two appends.
2. `sha256sum .ufo/gates/citation-drift/pointer-table.json`
3. Update `.ufo/gates/citation-drift/expected.json` → `pointer_table.sha256` to that digest
   **in the same commit** (a stale pin is `pointer_table_tampered`, exit 2 — could-not-evaluate).
4. `TMPDIR=/var/tmp/<scratch> python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict`
   → expect `clean findings=0 exit=0`; then the default mode, then `--selftest` → `13/13`.
5. Re-run command A (census) — unchanged by this instrument.

## Evidence that this exact object set is green

`claims/c3/EX-43/census.out` + `scratch-table-ext.json` (sha256
`0b01f52142924ce96e2cdddb84c15102f005dac17f07852ff0e6eb2f3d3a388f`): probe `--strict` → clean 0 exit 0;
needle-flip teeth → 1 finding exit 1; drift-injection in a scratch clone → real table blind (0 findings),
extension catches both injected `citation_dead` (`drift-blind.txt` / `drift-caught.txt`).

## Coordination notes (not defects, but landing-order hazards)

- C2 rewrites the custody-pair **registry row** and the custody **README** this same round. The two
  row-existence anchors pin only the row prefix (`| custody-pair | tool / kaidoku |`), which survives
  body edits; the README is deliberately not line-pinned (its lines may move under C2's edit) — the
  receipt examples are anchored on the target files instead.
- The `LOG.md` candidate must pin `:1412` (the digest wraps off `:1411`; a `:1411` pin is a measured
  false RED).