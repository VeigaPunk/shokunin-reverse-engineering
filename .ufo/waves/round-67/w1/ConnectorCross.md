2026-11-03
# ConnectorCross — round 67 w1 sibling-overlap findings (read-only)

Scope: whether another shokunin lane already owns (a) a SquashFS gap/class-accounting rule or a
device-node publication rule, (b) a mutation-score battery that binds a counter's own selftest, or
(c) a receipt-revision convention for gate receipts. Evidence artifact with commands and hit counts:
`.ufo/waves/round-67/w1/ConnectorCross/overlap.md`.

Nothing was executed in any sibling lane; no sibling file was touched. 19 lanes scanned in the
working tree, each HEAD pinned in the evidence artifact.

## Verdicts

**(a) No owner.** `squashfs` returns **0** files across every sibling `tools/`, root `*.md` and
`plans/`. Fleet-wide the word appears in 134 files, and **0** of them is a rule, gate or counter: 90
under `.ufo/` wave records, 48 under `tests/` (souji fixture-vault copies), 20 under `census/`, 5 in
`corpus/` (mori `statfs.2.man-pages-6.19`; souji `glocalfile.c` snapshot), 3 in `reports/` (revenger
RE format atlas). Device-node vocabulary (`S_IFCHR|mknod|device node|char device|character device`)
appears in exactly **one** sibling tool — `tsukuroi tools/score-census-handoff-r32.py:336`, a comment
(`# root metadata arm, pci inventory, device nodes`) in a census inventory, not a publication rule.
R67-C1's gap rule and its `class_disposition` block have no competing owner.

Nearest same-shape precedent, cite as precedent and not as novelty: `kama tools/census-waiver-
boundary.py` rules per class on whether a member is waivable ("a failure is not waivable"; evaluated
vs not-evaluated), with a frozen 7-case boundary, exit-2 could-not-evaluate, and a specificity case
(case 7: the landed census bytes stay green). Same reasoning shape — a class decides creditability —
different subject: census members, not filesystem entry classes. Different-scope `disposition` nouns
that do **not** count: tameshi `evidence-disposition.py` (dispositions over frozen expected checks)
and `pin-disposition.py` (pin byte identity, `result_reuse=not_established`).

**(b) Same-class precedent exists — `kama tools/release-recheck-selftest-extra.py`.** Docstring:
"Each case kills one mutant that the built-in selftest (`release-recheck.py selftest`, 5 cases) fails
to kill … Against the pristine tool all 15 cases pass; against each survivor at least its target case
fails." It carries a case→survivor map and a pristine-stays-green requirement. That is R67-C2's
instrument class: a separate case set bound to the frozen tool's own selftest, killing survivors the
built-in selftest cannot see. Scope difference to keep in any R67 prose: B-1 targets one plain tool
with 15 named cases and no before/after scoring; R67-C2 loads two counters by path under sha256 pins,
composes exactly one binding case per survivor onto each counter's own selftest, and scores
`killed_before 0` / `killed_after 2` with `--control` = the round-66 selftests alone.

Second same-family instrument: `kama tools/census-waiver-boundary.py` (loads the frozen census
in-process, adds 7 cases, requires the landed bytes to stay green). Adjacent but a different
mechanism: `tsukuroi tools/score-counter-cheats-r51.py` scores a matcher counter against five
adversarial *substitutes* (`r50_cheats_rejected` as sensitivity control), not against byte mutants
re-scored by a new selftest.

**(c) Established, multiply owned.** Direct precedent: `tameshi tools/receipt-revision-gate.py` —
"bind a receipt to the revision it certifies … A verdict, or a positive control, is evidence only for
the content it was measured against", with roles `positive`/`verdict`/`control`, 11 named refusal
codes including `RECEIPT_REV_MISMATCH` and `RECEIPT_REV_CONTENT_DRIFT`, and a `GATE: receipts=N ok=N
refused=N` verdict line. Complement: `tameshi tools/receipt-commit-bind.py` (an empty commit can
never carry the receipt its message names). Judge over gates: `tsukuroi tools/check-revision-
binding.py`. Gate-receipt capture and replay: `kama tools/round33-gate-receipts.py`. 454 tools across
the fleet mention receipts; at least six lanes carry a receipt sequence/completeness/citation gate.
A round-67 gate receipt naming `rev=3663e6b2…` applies that convention; it does not invent one.

## Constraint this places on the wave

1. R67-C1 may claim the class disposition as *its decision* but never as a novel instrument class;
   if any wave text frames "class decides publishability" as new, cite A-3 as the precedent for the
   shape or drop the novelty claim.
2. R67-C2 must be scoped by object (two frozen counters, pin-loaded, one binding case each,
   before/after score) and cite B-1 as the class precedent. A wave sentence that calls a
   selftest-binding mutation battery new is an overclaim against a landed kama tool.
3. The four receipt files in `.ufo/waves/round-67/l1/pre/` should be described as instances of C-1's
   rule — a receipt is evidence only for the content its `rev=` names — not as a new convention.

## Contradiction recorded, not absorbed

`kama tools/release-recheck-selftest-extra.py` names `mutants.tsv` beside itself as its mutation
evidence; `ls -l kama-shokunin/tools/mutants.tsv` is **absent** at kama HEAD e2b860c8. The tool is
present, the evidence file it points at is not in the tree. This is kama's doc-pointer gap, not an R67
defect and not something this seat repairs; it is recorded because citing B-1 as precedent otherwise
implies its evidence is locatable. [INFERENCE] a renamed or wave-local copy may exist; no search for
one was run.

## Limits

- Candidate pools for §2 are `grep -l` co-occurrence counts (e.g. 41 mutant+selftest files in souji),
  not classifications; only the 12 files named across the evidence artifact were read and classified.
  Unread candidates are not claimed as matches.
- Working-tree greps, not `git show HEAD:` reads; a dirty sibling worktree could shift a hit. HEADs
  are pinned so any disagreement is re-checkable.
- No sibling instrument was run. Nothing here is a verdict on kama's, tameshi's or tsukuroi's gates;
  only on whether their scope duplicates R67's surfaces.
