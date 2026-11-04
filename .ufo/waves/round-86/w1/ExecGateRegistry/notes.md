# ExecGateRegistry — round 86 (kaidoku), C2 gate-registry counter candidate

Candidate: `candidate/tools/round-86/gate-registry.py` (sha256 `abdaafea…bdf8b`, 25,976 B).
Production `tools/round-86/gate-registry.py` is untouched (sha256 `b87ffb1b…c81a5`).
No commit, no `git add`/`commit`/`checkout`; fixture commit built with plumbing in scratch only.

## Frozen rules kept

- Five atoms G1–G5 and their ids; registered tool path `tools/round-85/predicate-bind.py`;
  target 5/5; `--control file-exists` body unchanged (still accepts the unregistered state).
- Reading rule: `--rev` reads every file with `git show REV:path`.

## Changes (robustness and selftest only)

1. **Committed bytes executed (was a false-green path).** Production runs G2/G3 from the `--root`
   working tree. The frozen reading rule says committed bytes only, so a dirty tool could satisfy
   G2/G3. Candidate writes `git show REV:TOOL` to `--work/export/TOOL` and runs the child there.
   Selftest proves it: committed FAIL tool + working-tree PASS tool → fail.
2. **Row shape.** Registry markers must each occur exactly once, open before close (else exit 2).
   A target-path row must be exactly seven cells (G1); six-column rows no longer slip past as absent.
3. **G2 verdict map.** `0=`, `1=`, `2=` must each be whole exits (`(?<!\d)`); `12=` no longer
   satisfies `2=`.
4. **G3 command.** Must be `python3 ` followed only by interpreter flags (`-I -B -E -s -S -u`) and
   then the exact tool path; `python3 -c '…' <tool>` and `sh <tool>` are refused. The command is the
   first backtick span; the declared exit is read from the rest of the cell (`exit N`).
5. **Silent exit.** A child that exits 0 with no stdout/stderr → unevaluable (exit 2, no receipt).
   Atom rule unchanged (G2/G3 still exit-code equality); the counter refuses to score the silence.
6. **G4 pins.** Every pin the cell names must be a blob at `--rev` (see flag A below).
7. **G5 owner.** Full match `kaidoku-r<N>`; `kaidoku-r850` vs tool `round-85` fails.
8. **Child bounds.** argv list, no shell, `stdin=DEVNULL`, env exactly PATH/HOME/TMPDIR/LANG with
   HOME and TMPDIR under `--work`, 600 s timeout, `last_line` recorded in G2 and G3 detail.
9. **Scope.** `--work` (or `$TMPDIR`) resolving inside `<root>/.ufo/waves` → exit 2. `--rev` must be
   40 lowercase hex, else exit 2.

## Selftest: `SELFTEST cases=28 failures=0`, exit 0 (`selftest.json`)

21 row/gate fixture cases (good row; absent row; duplicate row; six-column row missing owner; path only
in prose outside markers; doubled open marker → unevaluable; wrong declared exit; cell without
declared exit; silent exit-0 tool → unevaluable; tool exits 1 declared 0; tool file absent; pin absent
at rev; `round-85` pin with only `round-84` present; `kaidoku-r850`; owner round mismatch; incomplete
verdict map; `12=` digit suffix; command naming another tool; `python3 -c` naming the tool as a string;
`sh` instead of `python3`; env exactly four keys) + 2 rev-mode cases (committed tool red with a green
working-tree tool → fail; committed green → ok) + 5 scope checks (`.ufo/waves` tree refused; scratch
outside accepted; `.ufo/wavesX` sibling accepted; short rev refused; full rev accepted). Control is
checked on every fixture whose tool is present: it accepts all of them.

## Measurements

| receipt | command | result | exit |
|---|---|---|---|
| `base.json` | `--root <lane> --rev 2cf0b7ff… --work <scratch>/base-work` | agreed 0/5, mismatches G1–G5 | 1 |
| `control.json` | `--control file-exists` same rev | mismatches 0, accepted true | 0 |
| `after-fixture.json` | fixture commit `12f4204c…` (lane's real `predicate-bind.py`, `SKILL.md` with the registered row, `.ufo/waves/round-85/claims.json`) | agreed 5/5 | 0 |

AFTER details: G2 `observed_selftest_exit 0`, `last_line "SELFTEST cases=21 failures=0"`; G3
`argv [-I,-B,tools/round-85/predicate-bind.py,--selftest]`, `declared 0`, `observed 0`; G4 pin blob
present; G5 `kaidoku-r85` == `round-85`.

BASE shows G1 `rows 0`; the lane's *working-tree* `SKILL.md` already carries the row and scores 5/5
when read with `--worktree` (informational only, not citable: worktree bytes).

Refusals observed: `--work` inside `<lane>/.ufo/waves/…` → exit 2; `--rev 2cf0b7f` → exit 2.

## Flags for the L1 (not decided here)

A. **G4 is stricter than the frozen "at least one".** Candidate requires every named pin to be a blob
   at rev. Stricter refuses more; it cannot create a false green. The divergence is declared, not
   silent; the L1 decides whether to restore "at least one" (the selftest would then need a case
   changed).

B. **Instrument pin.** `.ufo/waves/round-86/claims.json` pins `tools/round-86/gate-registry.py` at
   `b87ffb1b…`. Landing this candidate changes the digest. Integration needs an `instrument_supersessions`
   entry recorded by the L1; claims.json was not edited.

C. **Silent-exit refusal.** Exit 2 (could-not-evaluate) rather than an atom false. The L1 should judge
   whether this is a rule change under the frozen plan. It was chosen so that G2/G3 atoms stay as frozen
   while the counter still refuses to call a silent exit 0 green.

D. **Measured revision.** BASE is 0/5 by design. A 5/5 at a real measured revision needs the registered
   `SKILL.md` row committed at that revision; the working-tree row is not evidence. The L1 owns the commit.

E. **Frontier S255/S305 and round-86 lesson:** not opened in this seat (outside the executor assignment);
   no claims about their contents are made here.

## Tooling

No installs. No pacman. No ~/.local/bin writes. Fixture repo created in scratch with
`git init`, `hash-object`, `mktree`, `commit-tree` (plumbing only). Scratch removed before yield.
