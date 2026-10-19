# Proposed safe ordering — arc3-loop1-round1 integration (CR-4, c2 critic)

Liftable text for the parent's integration and the round report. All claims
measured; transcripts in `claims/c2/CR-4/evidence/` (`01`–`05`), re-runnable
via `evidence/run-all.sh`.

## Finding

An honest census scope re-key (EX-28) **cannot** trip the citation-drift probe
guard falsely: the probe resolves exactly 14 target files, none under
`.ufo/gates/` (`01:46-62`); a simulated re-key commit leaves `findings=0`
(both modes) and `sha256(pointer-table.json)` byte-identical (`02`); the
declared guard classes fire only on table absence/tamper/unpin (`04`). The
cross-chain risk that *does* exist runs the other way and through text
tokens/line numbering, not through the census edit.

## Ordering rules (the ones that matter)

1. **No one edits `pointer-table.json` this wave.** SC-4's manifest already
   marks it "must be byte-stable" (its digest is what `expected.json` pins).
   If any late edit is unavoidable: recompute the pin and land it in the SAME
   commit — otherwise the probe exits 2 (CNE) by design (`04:8-11`).
2. **Text edits to the census's graded files land BEFORE the final census
   measurement** (PROVINCE.md, SKILL.md, SCORECARD.md), and stay
   **occurrence-free**: no `rea-agents@x.y.z`, no bare `6.x.y` inside a unit
   carrying a gate token (`rea-agents|rea|config.toml|mcp_config.json|
   mcp.json|mcp_servers|devin|omp|kimi|npx`), no `/path.{json,toml,yml}:N`
   pointers — outside the declared scope rows these read as UNDECLARED.
   Measured: EX-20's patched row (occurrence-free) → PASS (`05:18-29`); the
   same row plus `rea-agents@6.7.0` → FAIL undeclared=1 (`05:31-43`);
   token-free records block → PASS (`05:45-56`); one pin-bearing records line
   → FAIL undeclared=1 (`05:58-65`).
3. **Edits to the probe's table targets land BEFORE the final probe re-run**
   (here: C1's `corpus/README.md` map token). The claimed **line-neutral**
   shape measured clean (`03:1-3`); a single inserted line before `:175`
   trips 4 findings (`03:5-15`). If a line must be inserted, the table's
   README pins need re-keying and then rule 1 applies.
4. **C3's edit itself is order-free** w.r.t. the probe (finding above); its
   only ordering constraint is the census-side one: any edit to the census
   file must land before the census run that certifies it, and the PASS cannot
   certify the re-key (CR-5's A3) — record the before/after census sha256 in
   the records commit as the certificate.
5. **/tmp EDQUOT is standing.** Run the probe selftest with a writable
   `TMPDIR` and record the TMPDIR used (`01:1-2`; PL-2's measurement). The
   census needs no temp dir. Instrument imports can create untracked
   `.ufo/gates/__pycache__/` — keep it out of commits.

## Measurement sequence at the records commit

1. Land every chain edit (C1 receipts/knowledge/README token; C2 probe +
   expected pin + SKILL.md row; C3 census edit) → commit.
2. At that commit run, in order:
   - `sha256sum .ufo/gates/citation-drift/pointer-table.json` == the pin in
     `expected.json` (the guard's precondition);
   - probe default + `--strict` → `findings=0`, `clean`;
   - probe `--selftest` with writable `TMPDIR` → 13/13 (post-EX-16);
   - census → `PASS 0/0/0/0`.
3. Record the verdicts in the commit message (r10 precedent, `110cc08`) or as
   an addendum measured at the next commit — never claim a measurement at a
   revision whose content postdates the measured commit ("a run over a
   different revision is a different measurement").

## Open item flagged to RV-8/parent (not resolved here)

If EX-16 lands the digest check for ANY `--table` path (RV-8's D2), every
custom-table run against the committed `expected.json` becomes exit 2 — the
recorded r10 experiment shape (S2). The landed scoping (D1 recommended) must
be stated in the SKILL.md row and the round report.
