# Round 49 — one freeze, and nine atoms the record must re-derive (title proposed)

Lane `kaidoku`, round 49, attempt 1. Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Declared freeze `<FREEZE>` — ONE commit (`plans/round-49-claims.md`, `tools/round-49/` and `tools/round-49/control-fixtures/**` land together in it). There is no amendment series: a counter bug found after `<FREEZE>` is reported as a miss and never patched.
Instruments: `tools/round-49/c1-counter.py` (R49-C1 coverage), `tools/round-49/c2-mismatch.py` (R49-C2 calibration).

<!-- L1: the `<FREEZE>` above, the `**Declared freeze:**` line of `## Round 49` in SCORECARD.md and the --freeze given to both counters must be the same 40-hex string. Check with grep before landing. This is M49-1 again if they differ. -->

## Mistakes

- **M49-1 · `reference-drift` · evidence `corpus/lessons/round-48.md:4` (`Declared freeze \`0f06251bf6a3a6964c715f67243d4df12e854258\`` with "series A1–A4") vs `SCORECARD.md:3730` (`## Round 48`, `**Declared freeze:** \`b6f7ca2a6391964dfdedd477cd560bd42159873a\``, A8; also `LOG.md:3439`) · captured-by `none`** — no lane instrument read the round-48 lesson header; the non-author closure `corpus/lessons/round-48-verifier-spotcheck.md` (Step-1, calibration row) found it after landing. **Fix:** atom A1 in `tools/round-49/c2-mismatch.py` (declared = SCORECARD `## Round 48`; stale = lesson header; `corpus/lessons/round-48.md` byte-identical to the base blob) and the append-only line `- A1 declared=<b6f7…> stale=<0f06…>` under `## Corrections to round 48`. The filed round-48 lesson is not rewritten. **Red:** battery mutation `A1 swap declared/stale` turns exactly `A1` red and no other atom (pre-freeze dev fixture `b6312f0d`, `battery.mutations`: `red ['A1']`, `noop []`; receipt `.ufo/waves/round-49/w1/C1ScribeLesson/receipts/c2-battery.json`). At `<FREEZE>` the unmodified lesson leaves A1 red (`lesson line A1 absent`; `mismatches 9`).

- **M49-2 · `<class: L1 to fill from wave 1>` · evidence `<L1 to fill>` · captured-by `<L1 to fill>` · MARKER — not yet a row.** Surfaced by wave-1 reports, unfolded at drafting time; the L1 keeps each as a row with its fix and red mutation once folded in, or removes it with the reason:
  - (a) `tools/round-49/c1-counter.py:1995` sets `res['frozen_tables_valid'] = True` before any check. The only other path raises `Unevaluable` (exit 2), so the clause cannot evaluate to false (`.ufo/waves/round-49/w1/C1SelfTest.md`, which also reports 34 clauses of which only 11 discriminate under forced-False mutation).
  - (b) `CTL-C1-4` plants the unaltered round-44 bytes; a relabel plus re-mint of the same copy reaches `carriers_matched 4` with the documentation bindings still false, so exit 1 and the kill rule does not fire. The run-provenance clause is the one it passes (`.ufo/waves/round-49/w1/C1CtlDoNothing.md`, row b3; not re-run by this seat).

## Gate

### Sources opened this round (2026-10-28)

<!-- MARKER L1: paste the rows as landed from the seats' registry diffs (C1ScribeSources, C2 snapshots). Expected: S138 and S139 are existing rows updated in place (status `opened`, used-by the round-49 knowledge entry); S147 supersedes S145 (quote `if a theory is incompatible with possible empirical observations it is scientific`, located under the snapshot heading `2. Backdrop to Popper's Thought` (`id=BackPoppThou`), not `§3`); S148 supersedes S146 (reachable `sysexits.h.3head.html`, `EX_USAGE 64`). Each quote at most 25 words; each snapshot sha256-pinned under `corpus/evidence/round-49/c2/`. -->

### Admission and rejection

- **Assimilation: none.** Sweep, run at `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` on 2026-10-28: `test -e considerthese` → exit 1; `test -e merge/kaidoku` → exit 1; `git ls-tree -d e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9 -- considerthese merge | wc -l` → `0`. `considerthese/` is absent in this lane and no `merge/kaidoku/` theme applies; the round-44 quarantine refusals stand and nothing is adopted.
- **Census before → after:** `corpus/SOURCES.md` rows **146 → <AFTER>** (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; 146 at the base, verified by `git show e4f2cfa5…:corpus/SOURCES.md`). Expected `<AFTER>` = 148 (S147 and S148 added); S138, S139, S145 and S146 change in place and add no row. L1 confirms at landing.

## Corrections to round 48

<!-- PLACEHOLDER: filled from w1/C2ScribeCorrections/. Append-only lines the counter reads; the values are re-derived there, not copied from any dev fixture. Expected shape (the counter's regexes): `- A1 declared=<40hex> stale=<40hex>`; `- A2 dead=<40hex> actual=<40hex>`; `- A3 log_<8hex>=<line,…> log_<8hex>=<line,…> unnamed=<8hex,…>`; `- A4 seats=<n> reports=<n> missing=<names>`; `- A5 …c1_stripped=<64hex>…`; A6–A9 as in the counter docstring. Do not edit `corpus/lessons/round-48.md`. -->

## Census before -> after

- **Round start** (`.ufo/waves/round-49/l1/sources-census-start.txt`, sha256 `653a3be854ae6f923dceb33d412ad0615a213fedcc6e4ae1f0a10b03a7890c96`, 17 lines): 15 `W04` duplicate-URL lines (S033 … S142), then `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, then the trailer line. **Exit code `0`; final line `exit=0`.**
- **Re-run at drafting** (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`, 2026-10-28T21:13:11Z): exit 0; stdout sha256 `065a45eb8e760d65d76e55e35e49efc44ee47466c1ffa147205757ea2589a2ea`; final line `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. Its 15 W04 lines equal the start file's.
- **Round end:** `<MARKER: L1 runs the same validate command after landing and pastes exit code, stdout sha256 and final line.>`

## Routed defects (for round 49)

Round-48 closure items (`corpus/lessons/round-48-verifier-spotcheck.md`, `## Routed defects for next round`), numbered as there:

| closure # | round-49 disposition |
|---|---|
| 1 stale declared-freeze header | M49-1; atom A1; correction line under `## Corrections to round 48` |
| 2 S145 locator | atom A6; row S147 (S145's own line unchanged) |
| 3 S146 reason and `teaches` | atom A7; row S148 (S146's own line unchanged) |
| 4 search-log entry and census record | atom A8 (search log, round 48 marked late, round 49); the census before → after is in this lesson |
| 5 `tools/round-48/census2.json` binds `paths` only | **declined.** Round-48 claims stay frozen; repairing the file amends a frozen round-48 counter. Not counted, not claimed. |
| 6 `tools/round-48/record2.py` imports `tools/round-46/gate.py` from the worktree | **declined**, same reason. The closure recorded the worktree hash equal to HEAD (latent risk). Not counted, not claimed. |
| 7 wave accounting (72 of 75 reports) | atom A4 (seats, reports, missing). Not atomized: "the wave had no planner role". Round 49's L1 holds the section-3 planner seat, and this is disclosed in the plan header. |
| 8 dead hash, LOG pointers, digest normalization | atoms A2, A3, A5. **Not atomized, open:** the C2 receipt timestamp (four seconds after the report's shared timestamp) and the explicit cross-domain-evidence statement. |

Round-48 lesson items (`R48-CL1`–`CL5`), which the round-48 SCORECARD lists as `planned (round 49)`. The round-49 claims do not carry CL2, CL3 or CL5, and record no written decline:

- **R48-CL1** (worktree-sourced gate helper) = closure 6: declined as above.
- **R48-CL2** (lexical class is not source truth): **open**, not in the round-49 claims.
- **R48-CL3** (quote correction may cite an unrelated receipt): **open**, the cross-round case is not exercised.
- **R48-CL4** (structural floor is bounded, not record completeness): language preserved; not promoted to a completeness claim.
- **R48-CL5** (battery skips when the genuine card is red): **open**. Measured at `<FREEZE>`: `c2-mismatch.py --rev <FREEZE> --freeze <FREEZE> --battery` exits 1 with `mismatches 9`, `battery.failing ["genuine REV is not green", "mutation set incomplete: 0 of 11"]` and no mutant verdicts (`receipts/c2-freeze-battery.out`).
