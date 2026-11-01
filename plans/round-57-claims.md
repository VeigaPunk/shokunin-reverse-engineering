# kaidoku round 57 — claims (the eight r56-closure routed defects close, and the extended M56-4 rule becomes an instrument)

Round base `63413677ec0531e38722b8dbfb0b89a0bc113d04` (lane `main` tip at round
start, pushed = origin/main; the round-56 verifier spot-check commit, whose §7
routed eight status-neutral defects D1–D8 to this round as first-priority
repairs). This file is the round declaration; the **freeze** is the single
commit that adds the round-57 wave artifacts (census-start receipt, before-arm
receipts, instrument receipts, the S257 snapshot) and the claims container
`.ufo/waves/round-57/claims.json`, recorded in `LOG.md` and
`.ufo/waves/round-57/l1/FREEZE` before any repair data lands. The freeze pins
three instruments committed with the declaration: `tools/round-57/record-receipt-audit.py`
(new), `tools/round-55/corrections-pin.py` (unchanged since the r56 disclosed
revision, pin `22f77c34…`), and `tools/round-29/freeze-gate.py` (unchanged
since round 29, pin `25b54339…`). All three are named in the container's frozen
atoms so the R29 gate audits them. L1-inline round: no wave surface exists on
this host (the kaidoku round-53 L0 question stays open and unanswered; routed
around, never treated as answered).

## Fresh-start compliance (operator rule)

The rendered prompt §7 binds this round as a fresh-start round and lists the
last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`). All
three fleet reports were re-read before declaring (`.ufo/reports/round-50/kaidoku.md`,
`round-51/kaidoku.md`, `round-52/kaidoku.md`), spot-checked against the lane
record, and the r53–r56 spot-checks re-read. Spot-check findings: all three
rejections died on the same shape — the AVM LE-SquashFS Frontier→Core target
(r50's frozen counter measured 2-of-4 carriers, exit 1, honest stop; r51 and
r52 never completed a freeze or data run) plus wave-band/handoff defects
(r51's 36-seat single wave below the 64–128 band with no falsify wave and no
per-seat status; r52's inherited 64-seat wave with four blocked seats and an
incomplete instrument set). None died on offline committed-byte work — the
r53–r55 chain admitted on exactly that class, and r56 was admitted with
routed defects. The binding is honored; ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be, unblob and vendor fetches are measurably absent on
   this host (PROVINCE `## Host migration — 2026-10-31`); three consecutive
   rounds died on it; the routed findings stay routed, untouched.
2. **A census-safe W04 supersedes set (the r55 planned item).** The census W04
   rule fires on every duplicate URL across scopes regardless of row status,
   and SOURCES.md is append-only — no appended row can clear a W04; the 19
   standing warnings stay named debt (the r56 ruling recorded in LOG).
3. **The registry-drift census (r53's sized-out census3 item).** Taking it up
   alongside the eight-defect carry-in would repeat the r51/r52
   over-declaration shape that produced both rejections; it stays planned.
4. **Any wave dispatch.** No dispatch surface on this host (L0 open);
   L1-inline, the r53–r56 precedent.

Section 9 sizing: both declared claims close artifacts and instruments that do
not exist at the base (an erratum set, a missing committed receipt, printed
disclosure shas, a committed gate receipt for an unreceipted run, a new
instrument with registry and capability rows) — a do-nothing control cannot
reach them; the before-arm receipts at the base prove the open state.

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0
(`SCORECARD.md` `## Owned axes`; none retired): every owned axis is a lowest
axis, so C1 (calibration) satisfies the rule. **Stagnation nudge:** saturation
line 10.0, window N=10, last capability round 56 (the freeze-receipt
completeness gate row) — r57 is round 2 of the window, so the nudge has not
fired. **Sourced claim:** S257 (git-ls-tree documentation, opened this round)
grounds C2's listing semantics — the manual of the command this gate's verdict
executes (`git ls-tree -r --name-only REV`), the R56 reject-1 boundary applied
consistently: the r56 gate anchored `cat-file -e` because its verdict was
existence-at-revision; this gate's verdict IS the ls-tree listing, so the
anchor moves to the ls-tree manual.

## The claims

**R57-C1 — calibration: the eight r56-closure routed defects (D1–D8) close
with committed, append-only artifacts.** Before at the base: all eight open
(`.ufo/waves/round-57/l1/scores/c1-before.txt`, probes pasted with observed
outputs). After (per-defect landing noted; every filed byte stays as filed):

- (D1/D2) an erratum appended to `corpus/lessons/round-56.md` as
  `## Corrections (round 57)`: the c1-after V-1/V-5 lines (probes print 0,
  annotations conclude ">=1 -> closed") and the report's "1 / 1 / 0 / 1"
  after-arm quote are superseded; the after-arm restates V-1/V-5 as
  content-checks on markers that occur in the committed correction wording
  (`planted empty directory trees mirroring the pathspec`,
  `canonical-parameter clarification`, `supersedes M55-2`), re-run with
  observed outputs in this round's after receipt.
- (D3) the same erratum's correction 2: the r55 lesson's "the four intended
  paths … exist at no path in that commit (`git cat-file -e` rc=128)" is
  overbroad — object facts re-verified this round at `29a7477b`: `LOG.md`
  EXISTS there (rc=0, blob `70d3f2af…`, byte-identical to parent `79421b75`'s,
  carrying no round-55 content — the append never landed); only the three
  NEW-file paths are absent (rc=128).
- (D4) the missed receipt `.ufo/waves/round-56/l1/records/receipt-audit-green-r56.txt`
  lands (worktree content already verified against the closure's own green
  run); the record section's receipts list resolves 13/13 in the tree; M56-4's
  "fully resolvable" sentence becomes true at this round's landing, and the
  M56-4 rule is extended (see C2) so the missed-path class is mechanically
  refused.
- (D5) the erratum notes the r56 report's "LOG insertions only: 45/0 across
  the round" is base→close `047bd98e`; at the report's cited tip `b9434858` it
  is 49/0 (direction conservative — 0 deletions at every one of the 7 commits).
- (D6) the LOG correction entry prints the discarded first-freeze sha the r56
  entry's "disclosed here" clause promised but never printed:
  `db3e94cdd155aea8c3cff2b0ced96bd16ceed1a9` (parent `31c2bd50`; located in the
  `main` reflog; not an ancestor of main, absent from origin/main — the
  disclosure is completed, the commit is never cited as evidence).
- (D7) the R29 gate is re-run at `047bd98e` (the r56 close tip whose run was
  transcribed only) and the receipt lands under this round's wave: the
  tip-run's verdict becomes a committed artifact.
- (D8) the round-57 SCORECARD section carries the corrected item list ("r55
  spot-check §7 items 1, 2, 3, 5 — V-4 is an operator note") and a correction
  line naming the r56 C1 row's "items 1-4" wording (the row stays as filed).

**R57-C2 — depth, capability acquisition: `tools/round-57/record-receipt-audit.py`,
the named-path completeness gate.** The M56-4 rule as D4's fix clause extends
it: EVERY file a record section names must resolve in the tree — not only the
receipts a prior audit happened to catch. Model: the record section's committed
bytes (`git show REV:RECORD`) are sliced to one `##`-heading section, every
backtick-quoted `.ufo/waves/round-N/` path is extracted, and each is resolved
by exact match against `git ls-tree -r --name-only REV` — one listing, one
revision, git objects only, nothing written. Verdict map 0/1/2; zero named
paths is unevaluable, never vacuously clean (the QUALITY #66 boundary).
Before at the base: instrument absent, 0 registry rows, 0 capability rows
(`.ufo/waves/round-57/l1/scores/c2-before.txt`). After: selftest green (9
in-memory cases: extraction 3 + section 2 + audit 4), red demo exit 1
`NAMED_PATH_ABSENT` on the D4 defect itself at the base (named 14, missing 1),
green demo exit 0 at this round's carry-in landing after the receipt lands
(named 14, missing 0), the round's own record section audited at its own tip
before filing, registry row in SKILL, capability row in SCORECARD.
