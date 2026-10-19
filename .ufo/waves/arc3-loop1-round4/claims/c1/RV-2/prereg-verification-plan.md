# RV-2 pre-registered verification plan — arc3-loop1-round4, chain c1 (reviewer)

Seat RV-2 · chain c1 · role reviewer · 2026-10-19. Task (seat line): grade the
drafted entry against `corpus/QUALITY.md` + the r1/r3 entries (incl. the
honest-stop/partial forms if triggered); list required fixes. This file is
pre-registered BEFORE the drafted entry lands; the grade will be written against
whatever revision is current at grade time, with its identity re-derived
first-hand (rule #14).

## Grading target

The round-4 C1 entry draft (Vyper leg), wherever it lands under
`.ufo/waves/arc3-loop1-round4/claims/c1/` (expected: `records-drafts/` or a
scribe seat dir; the r3 precedent: `claims/c1/records-drafts/knowledge-entry-draft.md`
plus a `map-token-patch.md`). If multiple copies exist, grade the superset and
record the divergence (the r3 RV-3 R4 finding class).

## Hard gates (each re-derived first-hand, never trusted)

1. **Stem == map token.** The proposed entry stem must appear in the map-token
   patch's PRIMARY line; command A must read `dangling []` after the pair
   (rehearsed on a scratch tree, never applied).
2. **Command A before → after.** Before: re-run recipe A (`SCORECARD.md:86-124`)
   at HEAD from real Git objects — recorded in `evidence/commandA-before.txt`.
   After: rehearsal on a scratch tree with entry + token; expect
   `knowledge_files 83 → 84, mapped 84, missing [], dangling [], rules 14/14`.
3. **Prior-83 byte-identical.** `diff` of the prior 83 knowledge files against
   the pre-pinned `evidence/prior-83.sha256` set; only the one new file added.
4. **README line-neutrality.** Token patch must keep the line count (166 lines
   at this HEAD for README? — measured at grade time) and change exactly the
   one map row line; state the exact before/after sha256s.
5. **K/K or typed result.** For every probe leg the draft cites: recovered set
   == an oracle set derived independently by me (keccak from the compiled
   Vyper ABI, or a byte-level EQ/PUSH4 census), zero missing / zero extra;
   OR the honest-stop branch (venv infeasible / typed refusal / partial
   recovery) is landed with the exact envelope and no costume. I will not
   trust the draft's own planted-K files as oracles.
6. **Decoded-digest binding.** Each cited leg's decoded
   `normalized_result.bytecode.sha256` must equal the sha256 I compute over
   the cited carrier bytes; the recheck line must reproduce on this host
   (disk-backed TMPDIR).
7. **Citations resolve.** Every cited repo path resolves (`ls`/`test -e`);
   brace-expansion names all exist; no dead paths (r1/r3 review class).
8. **Label discipline.** Observation/Inference/Unknowns/Limitations/Scope
   present; no decompiler/static claim as observed behavior; no `held`/`works`
   verb; QUALITY 11 (parsed-and-empty vs excluded) honored wherever a zero
   result appears.
9. **Identity discipline (rule #14).** Any self-claimed byte-identity in the
   draft (its own hash, the entry literal hash, mirror identities) must match
   the file as it stands at grade time; stale revision pins are a fix.

## QUALITY.md criterion table (15 rows)

Each admission criterion 1-15 gets PASS/FAIL/N-A with the evidence pointer;
each of the 6 weak signals gets checked against the literal text. Precedent
row-map: r3 RV-3's `quality-grade-rev4.md` (same role, same chain).

## Honest-stop grading rules (pre-committed)

- If the Vyper install/venv was infeasible and the draft says so with the
  recorded attempt, that is a PASS for the claim's honest-stop branch — but
  the entry MUST NOT then carry K/K recovery language for an unrun leg.
- If the extractor returned a typed result (parsed-empty / partial), the
  entry must land the exact partial set (selectors recovered, selectors
  missing) with the exact envelope id — no costume ("selectors recovered"
  over a partial set is a must-fix).
- A "partial recovery" framed as K/K, or a venv-infeasible leg cited as
  verified, is a claim-blocking FAIL.

## Attack list (pre-registered)

- A1: falsify zero-extras with a PUSH4 byte sweep on the Vyper runtime.
- A2: falsify the oracle independence — derive the selector set myself from
  the Vyper-compiled ABI (pure-Python keccak, EX-05's `keccak_ref.py` if
  landed, else my own implementation).
- A3: re-run one cited probe leg verbatim (disk-backed TMPDIR) and compare
  envelope ids + payload.
- A4: check the draft's honest-stop/partial language against the envelopes
  byte-level (the round-3 false-JUMPDEST line class).
- A5: citation sweep by brace-expansion (the r3 R3 class).
- A6: cross-check the claim's asserted command A numbers against my own
  re-run at the records commit (or at the latest rehearsal if pre-commit).

## Deliverables

- This plan; `evidence/commandA-before.txt`; `evidence/prior-83.sha256`;
  `evidence/baseline-pins.txt`; the grade file `quality-grade.md`; the seat
  report `seats/RV-2.md`; `report.identity.txt` after the report's final
  revision.

Writes: only this dir + the seat report. Scratch `/var/tmp/rv2-r4` and
`/dev/shm/rv2-r4`. No git mutation. Custody paths read-only (untouched).
