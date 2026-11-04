# ExecGateRegistry — round 86 C2 gate-registry hardening (candidate)

Full detail: `.ufo/waves/round-86/w1/ExecGateRegistry/notes.md`.

- Candidate: `.ufo/waves/round-86/w1/ExecGateRegistry/candidate/tools/round-86/gate-registry.py`
  (sha256 `abdaafeaaf18d6574db8bb372ff045d0bf8dcfe2db9cd13e45885eea179bdf8b`). Production untouched.
- Atoms G1–G5, tool path and target 5/5 kept as frozen; control body unchanged.
- Selftest `SELFTEST cases=28 failures=0`, exit 0.
- BASE (`--rev 2cf0b7ff…`): agreed 0/5, exit 1. Control: mismatches 0, accepted.
- AFTER fixture (committed good row, real tool bytes): agreed 5/5, exit 0.

Main false-green found and closed: production executes the `--root` working-tree tool for G2/G3,
against the frozen committed-bytes rule. The candidate executes `git show REV:tool` bytes from
`--work/export`. Also closed: six-column rows, doubled markers, `12=` as `2=`, `python3 -c` and
`sh` as the self-test command, a silent exit 0, a wrong-N owner, and a `--work` inside `.ufo/waves`.

Decisions for the L1 (details in notes.md A–D):
- G4 requires every named pin to be a blob (stricter than the frozen "at least one").
- Landing changes the instrument digest pinned in `.ufo/waves/round-86/claims.json`; needs an
  `instrument_supersessions` entry.
- Silent exit 0 is refused as could-not-evaluate (exit 2), not an atom false.
- The 5/5 at a measured revision requires the registered row committed; the worktree row is not evidence.

No commit, no production edit, no installs.
