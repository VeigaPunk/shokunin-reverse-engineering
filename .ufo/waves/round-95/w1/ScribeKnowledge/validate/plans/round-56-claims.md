# kaidoku round 56 — claims (carry-in repair round: the four round-55 closure carry-in items, and the M55-4 rule becomes an instrument)

Round base `fe3a804fa8c2d5ff078c6253a5df1bdbc2f28fca` (lane `main` tip at round
start, pushed; the round-55 verifier spot-check commit, whose section 7 routed
four status-neutral carry-in items to this round). This file is the round
declaration; the **freeze** is the single commit that adds the round-56 wave
artifacts (census-start receipt, before-arm receipts, instrument receipts, the
S256 snapshot) and the claims container `.ufo/waves/round-56/claims.json`,
recorded in `LOG.md` and `.ufo/waves/round-56/l1/FREEZE` before any repair data
lands. The freeze pins three instruments committed with the declaration:
`tools/round-56/receipt-audit.py` (new), `tools/round-55/corrections-pin.py`
(bytes revised this round — the V-3 docstring correction; the revision is
disclosed by an `instrument_supersessions` entry appended to the round-55
container per the gate's own disclosure mechanism, the r53 amendment pattern),
and `tools/round-29/freeze-gate.py` (unchanged since round 29, pin
`25b54339…`). All three are named in the container's frozen atoms so the R29
gate audits them. L1-inline round: no wave surface exists on this host (the
kaidoku round-53 L0 question stays open and unanswered; routed around, never
treated as answered).

## Fresh-start compliance (operator rule)

The rendered prompt section 7 binds this round as a fresh-start round and lists
the last three rejected closures: r50, r51, r52 (all `rejected-honest-stop`).
All three fleet reports (`.ufo/reports/round-50/kaidoku.md`,
`round-51/kaidoku.md`, `round-52/kaidoku.md`) and their lessons
(`corpus/lessons/round-50.md`, `round-51.md`, `round-52.md`) were read before
declaring; the r53-r55 spot-checks are re-read each round. Note: the three
listed rejections predate the admitted r53-r55 chain — the binding is honored
anyway. Ruled out this round, with reasons:

1. **AVM LE-SquashFS Frontier→Core (the r50/r51/r52 twin claim).** REA 6.5.0,
   sasquatch/sasquatch-v4be, unblob and vendor fetches are measurably absent on
   this host (PROVINCE `## Host migration — 2026-10-31`); three consecutive
   rounds (r50 attempt 1 through r52) died on it; the routed findings stay
   routed, untouched.
2. **A census-safe W04 supersedes set (the r55 planned item).** The census W04
   rule fires on every duplicate URL across scopes regardless of row status
   (`scripts/sources-census.sh` row_pass: the check runs before any status
   test), and SOURCES.md is append-only — no appended row can clear a W04; only
   removing or altering the older rows would, which the append-only contract
   forbids. The 19 standing warnings stay named debt.
3. **The registry-drift census (r53's sized-out census3 item; stays planned).**
   `tools/round-51/census3.py` exists but its consumer migration was sized out
   in r53; taking it up alongside the carry-in pair would repeat the r51/r52
   over-declaration shape that produced both rejections.
4. **Any wave dispatch.** No dispatch surface on this host (L0 open);
   L1-inline.

Section 9 sizing: both declared claims close artifacts and instruments that do
not exist at the base (four correction/clarification blocks, a revised pinned
instrument with a disclosed supersession, a new completeness gate with registry
and capability rows) — a do-nothing control cannot reach them; the before-arm
receipts at the base prove the open state.

**Lowest-axis rule.** Owned axes coverage/depth/calibration sit tied at 10.0
(`SCORECARD.md` `## Owned axes`; none retired): every owned axis is a lowest
axis, so C1 (calibration) satisfies the rule. **Stagnation nudge:** saturation
line 10.0, window N=10, last capability round 55 (the corrections-pin row) —
r56 is round 7 of the window, so the nudge has not fired. **Sourced claim:**
S256 (git-cat-file documentation, opened this round) grounds C2's
existence-check semantics (`git cat-file -e REV:path`) — the manual of the
command the gate actually executes, mirroring the S255 read discipline it
inherits.

## The claims

**R56-C1 — calibration: the four round-55 closure carry-in items close with
committed, content-checked artifacts.** Before at the base: 0 of 4 present
(`.ufo/waves/round-56/l1/scores/c1-before.txt`). After:

- (V-1) a wording correction appended to `corpus/lessons/round-55.md`:
  M55-2's parenthetical and the report's "four files landed under a `C:` tree
  directory" are superseded — the pushed garbage commit `29a7477b`'s entire
  delta is the ADDED `C:` subtree containing ONLY empty directory trees (the
  canonical empty tree at every level), zero blobs; the four intended files
  exist at no path in that commit; no content was lost (the replay
  `c191d8df` landed them properly).
- (V-2) a correction block appended to the same lesson for frozen atom T2:
  T2's "freeze receipts committed: … freeze-gate-tip-90f3a9b9.json" is
  superseded — the freeze commit `1f9be6eb` dropped it (pathspec slip, M55-4);
  the receipt landed at `627a9c20` under its true round-54 home; the frozen
  container text stays as filed.
- (V-3) `tools/round-55/corrections-pin.py`'s docstring prose corrected
  ("line 2's leading cell" → line 29; the green demo's placeholder
  "<measured rev>"/"rows_a 1" → the canonical frozen-receipt parameters) —
  bytes revised, selftest re-run green, both demonstrations re-run with
  unchanged verdicts, new sha pinned in this round's container, revision
  disclosed by supersession.
- (V-5) the canonical green-demo rev clarified: the receipt of record is the
  freeze-committed `records/pin-green-demo.txt` (`--base c753b24f… --rev
  79421b75…`, the round base at freeze time; exit 0, clean, rows 2, appended
  0); the report/record prose describing `c753b24f…→e21be31a…`/`→627a9c20…`
  names the landing re-run and the verifier's closure re-run — additional
  verifications, both clean, never a replacement of the frozen receipt's
  parameters.

**R56-C2 — depth, capability acquisition: `tools/round-56/receipt-audit.py`,
the freeze-receipt completeness gate.** M55-4's fix rule as an instrument: every
receipt path a claims container's strings claim must resolve at the named
revision — full wave paths repo-wide (`git cat-file -e`), bare names within the
container's own round scope (`git ls-tree -r`, fail-closed on ambiguity).
Before at the base: instrument absent, 0 registry rows, 0 capability rows
(`.ufo/waves/round-56/l1/scores/c2-before.txt`). After: selftest green (9
in-memory cases, extraction + audit), red demo exit 1 `RECEIPT_ABSENT` on the
historical M55-4 event (the r55 container at its freeze `1f9be6eb`, bare name
`freeze-gate-tip-90f3a9b9.json`), green demo exit 0 on this round's own freeze
container, registry row in SKILL, capability row in SCORECARD.
