# RV-8 pre-registration — r4 review protocol (written before the patch texts land)

Seat RV-8 · chain c3 · reviewer · wave `arc3-loop1-round4` · 2026-10-19.
Task: review the registry-row + README patch texts for the revised custody-pair
tool (new sha, case count, new classes) against the landed bytes.

## Review target (named before it exists)

Whatever pair lands under `.ufo/waves/arc3-loop1-round4/claims/` (any seat's
dir) naming a registry row (SKILL.md) and/or the gate README, together with the
revision of `.ufo/gates/custody-pair/custody-pair.py` it describes. If the
revision never lands inside this seat's window, this seat reviews the landed
HEAD bytes (`7cd19c3c…` at `015e1ba`) against any patch text that does land and
names the missing half.

## Checks (each one run, each one cited by command output or sha256)

1. **Identity.** Re-derive: tool sha256 + `wc -l`; README sha256 + `wc -l`;
   SKILL.md base sha256; every digest the patch text claims (base, patched,
   diff). An unrun check has not passed.
2. **Apply integrity.** Extract each fenced diff, apply to the named base on a
   scratch copy (`patch -p1`), `cmp` against the claimed patched digest, and
   re-apply to prove no silent double-apply.
3. **Line-neutrality.** Row patch: line count in == out. README patch: the
   stated line delta is the measured one.
4. **Class existence.** Every exit class / flag / finding the texts claim must
   exist in the tool bytes AND fire by command (my class-map harness:
   `evidence/class-map.sh`). Claims with no implementing code are refuted.
5. **Case count.** The claimed `cases=N` equals the landed
   `CUSTODY_PAIR_SELFTEST: CLEAN cases=N passed=N failed=0 exit=0` run of the
   landed bytes; the new case names exist in the bytes.
6. **New classes for the four named r4 residuals.** Each of (a) sidecar scope,
   (b) mkdir traceback, (c) stanza-vs-path coverage, (d) both-absent MATCH is
   checked in both directions: reproduced on the pre-revision bytes
   (`evidence/class-map-BEFORE.out`, already recorded) and exercised on the
   landed revision (before→after per injection).
7. **No-harm instruments.** command A (verbatim SCORECARD recipe), citation-
   drift probe (default + strict + selftest), c1 census — all at HEAD and on a
   scratch clone carrying the landed files. Baseline recorded:
   `evidence/commandA-head.json` (83/83, 14/14, 10.0/10.0 at `015e1ba`).
8. **Probe-anchor interplay.** The registry row carries strings the
   pointer-table's `skill-registry-custody-pair-row` anchor grades; any row
   rewrite must keep that anchor alive or land with a re-anchored table +
   re-pinned expected.json in the same commit (r3 EX-32/CN-1 precedent).
9. **Rule-#11 discipline.** No patch text or landed file pins a line number
   into an operator-mutable file.
10. **Rule-#14 identity discipline.** Any self-claimed byte-identity in the
    reviewed artifacts is re-derived after revision; a claim that a file cannot
    carry its own post-append digest is itself checked (compare against a
    hash taken at read time).

## Verdict vocabulary

EXISTS / REFUTED / NUANCE, per clause, each with the command that decided it.
