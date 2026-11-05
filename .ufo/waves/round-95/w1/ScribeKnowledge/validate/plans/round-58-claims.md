# kaidoku round 58 — claims (the r57-closure routed carry-in closes with receipts, and the registry-drift census runs again)

Round base `42c794afc5cdf2f72d80edb839cfbcbfe32e6bad` (lane `main` tip at round
start, pushed = origin/main; the round-57 verifier spot-check commit, which
admitted r57 and routed two status-neutral items to this round: the file-count
precision correction (spot-check §7 defect 2) and the orphaned-evidence hygiene
duty, the latter to be executed by running the lane's receipt-audit capability
and landing anything it names). This file is the round declaration; the
**freeze** is the single commit that adds the round-58 wave artifacts
(census-start receipt, before-arm receipts, hygiene-sweep receipts, the S258
snapshot) and the claims container `.ufo/waves/round-58/claims.json`, recorded
in `LOG.md` and `.ufo/waves/round-58/l1/FREEZE` before any repair data lands.
No new instrument is introduced this round: the round executes routed duties
and repairs data with six frozen instruments, all pinned in the container (the
R29 gate audits them). L1-inline round: no wave surface exists on this host
(the kaidoku round-53 L0 question stays open and unanswered; routed around,
never treated as answered).

## Fresh-start compliance (operator rule)

The rendered prompt §7 binds this round as a fresh-start round and lists the
last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`). All
three fleet reports were re-read before declaring, and spot-checked against the
lane record (probes pasted):

1. r50: the attempt-2 C1 miss reproduces from the committed counter receipt
   `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` — `carriers_matched
   2` of `target 4` (this round re-read it at HEAD).
2. r51: `python -X utf8 -I -B tools/round-51/census3.py --root . --rev
   f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab --historical` → exit 1, registry
   55 / census 42 / outside 13 — exactly the r51 report's diagnostic numbers.
3. r52: lane tip `00d0bfd00b2778c3e0b22b7d0f6ade11abcb07a2` is an ancestor of
   `refs/heads/main` and carries `plans/round-52-claims.md` (cat-file rc=0).

All three rejections died on the same shape — the AVM LE-SquashFS
Frontier→Core target plus wave-band/handoff defects (r50's frozen counter
missed 2-of-4; r51's 36-seat wave under the band with no falsify wave; r52's
inherited 64-seat wave with four blocked seats and incomplete instruments).
None died on offline committed-byte work — the admitted r53–r57 chain is
exactly that class. Ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be, unblob and vendor fetches remain measurably absent
   on this host (PROVINCE `## Host migration — 2026-10-31`); three consecutive
   rounds died on it; the routed findings stay routed, untouched.
2. **New wave-based claims of any kind.** No dispatch surface on this host
   (the r53 L0 question stays open); r51/r52's wave accounting was itself a
   rejection ground.
3. **Resuming the r51/r52 triage-v6 executability drafts.** Twice rejected as
   incomplete-instrument claims; the drafts stay wave evidence, not production
   tools.

Section 9 sizing: both declared claims close artifacts that do not exist at the
base (a hygiene-sweep receipt set naming and repairing a named-absent receipt,
a precision correction note, a 19-row disposition table, a parseable registry
whose drift census runs) — a do-nothing control cannot reach them; the
before-arm receipts at the base prove the open state.

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0
(`SCORECARD.md` `## Owned axes`; none retired): every owned axis is a lowest
axis, so C1 (calibration) satisfies the rule. **Stagnation nudge:** saturation
line 10.0, window N=10, last capability round 57 (the named-path completeness
gate row) — r58 is round 1 of the window, so the nudge has not fired.
**Sourced claim:** S258 (GitHub Flavored Markdown Spec, tables extension,
opened this round) grounds C2's defect class and repair side — the spec-legal
escaped-pipe cell content versus the frozen parser's plain-pipe grammar.

## The claims

**R58-C1 — calibration: the r57-closure routed carry-in set closes with
committed, append-only artifacts (four routed items R1–R4, one claim).**
Before at the base: all four open (`.ufo/waves/round-58/l1/scores/c1-before.txt`,
probes pasted with observed outputs). After (every filed byte stays as filed):

- (R1, spot-check §7 defect 2) the LOG correction note lands: the r57 report's
  "exactly the 26 files named above" counted named items (the `s257/` snapshot
  + digests named as one item) while the round's distinct filesystem paths
  number 27; the substance was verified by the spot-check itself (the delta
  contains exactly the named set, nothing else); the count phrasing is
  corrected by this append, never by editing filed text.
- (R2, the coordinator-routed orphaned-evidence hygiene duty) the sweep runs
  and its receipts land: (a) `tools/round-56/receipt-audit.py` over the five
  host-era claims containers at the base — one live finding
  (`RECEIPT_ABSENT freeze-gate-tip-90f3a9b9.json` in round-55 scope, the
  M55-4 pathspec defect's unrepaired remainder: the r55 container and the r55
  SCORECARD landing-receipts list name the path, whose bytes exist only under
  round-54); (b) `tools/round-57/record-receipt-audit.py` over the last three
  record sections — the same single miss inside the r55 section; (c) the
  worktree-vs-tree orphan census — three worktree-only paths (one unnamed
  orphan receipt of the discarded r55 first chain, two gitignored caches),
  each dispositioned in `records/orphan-census.txt`. **The named receipt
  lands**: a byte-identical copy of the committed round-54 bytes at
  `.ufo/waves/round-55/l1/scores/freeze-gate-tip-90f3a9b9.json` (the path the
  r55 records name), cmp/sha256-verified; after the landing the r55 container
  audits clean and the r55 record section resolves 13/13; the r55 freeze-era
  red demo stays red (history is not rewritten) and no frozen byte is edited;
  the r56 texts stay as filed and true at the revs they cite, with the
  supersession note carried in the round-58 LOG and lesson.
- (R3, the r57 planned item "a census-safe W04 supersedes set") the
  feasibility probe runs on the fleet census script's committed bytes
  (`records/w04-supersedes-probe.txt`): the supersedes guard exists in the E04
  branch only; the W04 branch tests neither status nor supersedes — the routed
  item is the empty set as named, closed vacuous-as-named, with the 19 standing
  warnings dispositioned row-by-row in `records/w04-disposition.tsv` (first
  holder named per row). W04 stays named debt.
- (R4, spot-check §7 "keep W04 on the named-debt list") satisfied by R3's
  table and the round census receipts (19 standing W04 at both ends).

**R58-C2 — depth: the routed registry-drift census runs again (the registry is
repaired into its own parser's grammar).** Before at the base:
`tools/round-51/census3.py --check` exits 2 — `registry row must have seven
cells` (`.ufo/waves/round-58/l1/scores/c2-before.txt`): the r55
`v6-block-digest.py` registry row's purpose cell contains the GFM-escaped pipe,
the frozen parser's plain-pipe split reads eight cells, and the drift census
has been unrunnable since the r55 landing — three rounds of routed "census3
outside-13" items that nobody could have executed. The repair is data-side
only (S258 grounds the side): the cell's escaped-pipe fragment is reworded
("the last consecutive table-pipe-leading line"), the parser and every
instrument stay frozen, and the SKILL delta is exactly one registry-row
fragment. After: the row parses (seven cells), `--generate` at the landing
derives the registry inventory (every registered path present at the
revision), `--check` at the record revision against the committed generated
inventory exits 0 (exact equality, no duplicates), the historical mode stays
exit 1 (frozen census2, the r51 authority note — reported as-is), and the
v6 triage-table digest `946e5359…` is unchanged at base and landing (no-harm).
