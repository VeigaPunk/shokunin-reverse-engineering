source: S295 `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html` (OPTIONS `-n`, snapshot line 97) and S296 `https://mutants.rs/` (Welcome to cargo-mutants, snapshot lines 184-186)
verified-at: 2026-11-04
recheck: 180d

# Two measurement rules: a pointer's own line, a mutant's own detector

Two reading rules the round-79 instruments rest on. Both are about what a piece of evidence
*names*, and both were already violated once in this lane.

## 1. A `path:line` pointer names the file's own 1-based line

POSIX.1-2024 `grep` defines the numbering a pointer inherits: "Precede each output line by its
relative line number in the file, each file starting at line 1." The counter resets per file, so a
line number is a property of the file, never of a search or of a concatenation.

That is the whole difference between round 78's pointer rule and round 79's. The round-78 surface
recheck compared `pointer.split(":")[0]` — the path — so a pointer whose line had moved still
scored green. Round 79's `tools/round-79/pointer-bind.py` reads the named line (or the named
range) and requires the token the pointer claims to occur there. Two facts that follow:

- **A moved line is a mismatch, not a match.** The OMP pin moved `:8` -> `:12` and the Kimi pin
  `:4126` -> `:4722` between the round-78 receipt and the round-79 base; a path-only rule cannot
  see either move (`pre/controls/c2-path-only.json` reports `mismatches 0` on the stale record).
- **A range is read as a range.** `.bashrc:28-29` is bound only when both declared tokens occur
  inside those two lines; comparing the range's first line only would pass a moved export.

The corresponding honest limits: the binder reads the file at the receipt's `checked_at`, so a
later host edit invalidates the receipt rather than the claim; and it retains a pointed line's
sha256, never its bytes, because the configs' other content is not evidence.

## 2. A surviving mutant is an inserted defect no case catches

The cargo-mutants book states the vocabulary the mutation battery uses: a mutation-testing tool
helps "by finding places where bugs can be inserted without causing any tests to fail". A mutant
that no test fails on has *survived*; a mutant a test fails on has been killed.

Round 78's wave applied eight exact edits to `tools/round-78/attack-gate.py` and two survived
(`m03`, `m08`) — not because the gate's rules were wrong, but because its **selftest had no case
for the two code paths**. Round 79 freezes the rule in `tools/round-79/gate-mutation.py`:

- a mutant is killed only when its **declared** case is present in the target's `--selftest`
  output and fails there;
- an **absent** declared case is a survivor, never a pass — a detector that does not exist cannot
  catch anything;
- an anchor that occurs zero or several times, or a copy that emits no `SELFTEST` summary, is
  **inconclusive**, never killed.

The base arm shows the rule doing work: at `29d2ca30`, `m03`, `m05` and `m08` survive and each of
their declared cases is absent from the base selftest's 26 cases; at the freeze the selftest has 29
cases and each of the three fails under its own mutant alone (`sole_detector`).

## Limits

Tier: S295 is a specification (A) for line-number semantics; S296 is a tool's book (B) for the
technique's vocabulary, not its specification. Neither source establishes that the lane's five
pointers are the right pointers to keep, nor that eight mutants cover the gate: both are curation,
recorded in `SCORECARD.md` and the round-79 lesson, not derived from the sources.
