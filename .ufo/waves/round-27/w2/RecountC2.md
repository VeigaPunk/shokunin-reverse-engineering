# RecountC2 — R27-C2 checker recount (wave 2, 2026-10-22)

Attacked item: the R27-C2 operability claim — "tools/round-27/xpin-attribute.mjs ... 24/24
round-26 envelopes, 3/3 red envelopes, capability row 1, source row 1 (S081), exit 0 at
97358f75" (claims.json R27-C2, counting command re-run verbatim).

**Verdict: holds.** The recount reproduces the claim at both revs with an identical
instrument, byte-identical output against the frozen after-receipt, and the selftest
failure found is a selftest design artifact, not a claim defect (analysis below).

Bounds kept: read-only on the lane (git show/log/ls-tree/diff/rev-parse/merge-base only);
no lane file mutated; scratch under /fast/scratch/hyaku/kaidoku-r27/seats/w2/RecountC2/.
No tools installed or upgraded (none needed). Runtime revs: main = 4084d897..., frozen
rev = 97358f75... (git rev-parse, 2026-10-22T15:35:30Z, exit 0). Working tree dirty files
are only untracked wave-2 dispatch/spec/report files (git status --porcelain, 15:35:30Z).

## Check 1 — instrument sha256 vs claims.json instruments

Command: `sha256sum tools/round-27/c2-xpin-check.py` and `git show <rev>:tools/round-27/c2-xpin-check.py | sha256sum` for main and 97358f75.
Excerpt (2026-10-22T15:40:38Z, exit 0): all three print
`d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3`.
claims.json instruments entry (read of .ufo/waves/round-27/claims.json):
`"tools/round-27/c2-xpin-check.py": "d8de667f...09bd3"`. The claims file is committed
(blob 050601ca at main) and unchanged between freeze commit a4f674b3 and main
(`git diff --name-only a4f674b main -- .ufo/waves/round-27/claims.json` is empty;
a4f674b is an ancestor of main, merge-base exit 0, 15:39:21Z).
Observation: worktree, both revs and the frozen claim all carry the same checker bytes.
Verdict: instrument identity holds.

## Check 2 — re-run at the frozen rev 97358f75

Command: `python3 -I -B tools/round-27/c2-xpin-check.py --root
/home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 97358f759a531f7ebc0354fb937d546da8d3b8bd`
(2026-10-22T15:37:24Z, exit 0). Excerpt:
`r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=97358f75...` and
`checker attribution of the round-26 envelopes: 6.5.0=21 6.7.0=0 both=3 none=0`.
Comparison (diff -u vs .ufo/waves/round-27/after/c2-at-97358f75.txt, 15:38:13Z): the two
content lines are byte-identical; the only delta is the receipt's trailing `exit=0` line,
which my capture records outside the file (wrapper echo EXIT=0). The receipt itself is
untouched since commit: its worktree sha256 9b2fa4c1... equals the main blob's
(15:38:13Z, exit 0). Observation. Verdict: frozen after-receipt reproduces exactly.

## Check 3 — re-run at the tip (main)

Command: same with `--rev main` (2026-10-22T15:37:24Z, exit 0). Excerpt:
`r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=4084d897...`.
Between the two revs the only C2-relevant input that changed is SCORECARD.md
(`git diff --stat 97358f75 main -- tools/round-27/ corpus/evidence/round-26/c1/
SCORECARD.md corpus/SOURCES.md corpus/lessons/round-27.md`: 1 file, +33, -0), a purely
additive round-27 section; the capability row that landed in 97358f75 is untouched
(grep -c xpin-attribute on SCORECARD: 0 at c6d619a3, 1 at 97358f75, 1 at main,
15:40:08Z, exit 0). Observation. Verdict: claim numbers hold at the tip; nothing regressed.

## Check 4 — selftest

Command: `python3 -I -B tools/round-27/c2-xpin-check.py --selftest`
(2026-10-22T15:37:28Z, exit 1). Case results:
- FAIL correct-stub: exit 0, expects 'r26_rows_ok=24/24 red_ok=3/3' (output line shows
  exactly `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=4084d897...`)
- PASS lazy-stub (echoes stored id for both pins; only the 3 both-rows pass): exit 1
- PASS only65-stub (no 6.7.0 rule; only the 3 both-rows pass): exit 1
- PASS skip-stub (drops one envelope): exit 1, expects 'r26_rows_ok=23/24'
- PASS tool-absent-at-base: exit 1, rows 0/24 red 0/3, rows 0/0 at cd32264f
- PASS rows-fixture good rows / tool named outside ## Capabilities / only a base-era row /
  row not in ## Gate / row status candidate (5 assertions, all as wanted)
- summary: `selftest cases=6 failures=1`

Why correct-stub FAILs (code reading, tools/round-27/c2-xpin-check.py selftest):
the case requires `want in text and got == 1`. The `want` substring IS in the output;
but the "correct" stub honestly recomputes both ids via the real recompute module, so
measure() sees 24/24, 3/3 and — because selftest runs against the live lane HEAD, where
the SCORECARD capability row and SOURCES S081 row now exist — capability_row=1,
source_row=1, hence exit 0. `got == 1` could only hold when those rows were ABSENT at
HEAD, i.e. before the C2 commit (proven: 0 xpin-attribute mentions in SCORECARD at
c6d619a3, the parent; observation). This is the "expected the rows absent" case.

Does it matter? For the claim, no: the claim's target is exactly rows present + exit 0,
which both measure runs show, and the row-parsing logic is independently pinned by the
5 PASSing rows-fixture cases and tool-absent-at-base. The FAIL is not a weakening of the
checker's red detection either — lazy/only65/skip stubs are still all caught. What it
does expose (hygiene defect in the instrument, minor): the selftest is not hermetic —
correct-stub reads live lane HEAD for the row checks, so `--selftest` can never exit 0
on any rev at or after 97358f75; its exit 1 is a permanent false alarm and the aggregate
"failures=1" line can no longer serve as a green signal (case lines remain readable).
Inference on intent, grounded in the quoted code; the FAILing expectation was satisfiable
only pre-commit.

## Residual risk and verification gaps

- The checker's `limits` field stands: 6.7.0 attribution is by rule fit against installed
  package code; no 6.7.0 run was made this round; the tool's avoidance of a retyped
  projection is a separate reviewer item (not attacked here).
- I did not re-derive the 24 envelope attributions independently of the checker's own
  recompute path; the recount trusts the frozen instrument (byte-identical) as the
  counter. Given the instrument identity check, that is the assigned scope.
- Selftest exit 1 on the committed instrument will stay red until correct-stub is
  re-anchored to a fixture rev; flagged, not fixed (bounds: read-only on the lane).

## Artifacts (under /fast/scratch/hyaku/kaidoku-r27/seats/w2/RecountC2/)

- out/rerun-at-97358f75.txt sha256 b91a22bad8a99395943fcf08c8ccf6ae09f321da1aae3c6939456790b40032f2
- out/rerun-at-main.txt sha256 e6290ce18c0b1b7fa61eb9f41505fe9018707e08619b14a67afb8d859bc82496
- out/selftest.txt sha256 ec5791e0155cabbd62460d74c58fe90aea043667b61b87c52d30c15b2d2eec9a
- tmp/ (checker scratch, emptied by the checker itself; no other artifacts)

Report: .ufo/waves/round-27/w2/RecountC2.md
