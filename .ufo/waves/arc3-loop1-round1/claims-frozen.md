# arc3-loop1-round1 — frozen claims, 2026-10-19

Wave: 64 seats, `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round
robin starts here; key advances each opencode-go round). Roster frozen PRE-DISPATCH
per the r9 wire-it amendment: the dispatch items array must carry exactly the 64
seat names below; the parent counts the items array, not the intent.

Axis set: **coverage (owned)**, **operability (fleet)**, **freshness (fleet)**.
Lowest-axis rule: all three owned proxies are tied at 10.0 with none retired, so
the owned claim is selected by the lane's standing most-falsifiable-next-claim
tie-break (luna-round-2 precedent). Claims are causally separable: three
different instruments/surfaces, no shared edit targets.

## C1 — coverage (owned): EVM real-bytecode leg

Frontier debt (`PROVINCE.md` Frontier): selectors held on a synthetic 81-byte
dispatcher only (r3-07); "real solc/vyper-compiled bytecode untested".

Claim: after the round's commits, `rea inspect-evm-interface <file> <raw|hex>`
recovers selectors from a **real solc-compiled contract on this host**; the
result lands as a corpus knowledge entry with sealed receipts; the map gains one
line-neutral token; command A re-measures knowledge 81 → 82 with prior 81
byte-identical and rules 13/13.

Falsifiable before → after (counting):
- before: command A at HEAD → knowledge_files 81, mapped 81; EVM held = synthetic
  carrier only (3/3 planted selectors, r3-07).
- after: (a) npm `solc` install receipt (name, version, sha256) committed under
  `receipts/`; (b) real contract compiled on-host; planted selector count K
  recorded pre-probe; (c) probe recovers K/K selectors (or a typed refusal is
  sealed and the claim reports honest stop); (d) knowledge entry + map token
  landed; (e) command A at the records commit → 82/82, missing [], dangling [],
  13/13 rules, prior-81 diff empty.
Predictions frozen: install succeeds from npm; K ≥ 3 distinct selectors;
`dispatch:"abi"`; no config.toml drift. Honest-stop branches pre-written: typed
refusal on real bytecode (seal envelope, claim NOT verified, no costume retry);
encoding mismatch (positional raw|hex — verify both); install failure (record,
claim not verified).

## C2 — operability (fleet): citation-drift probe frozen-run guard

Named debt (`SCORECARD.md` arc2-loop1-round4 carried debt + r5 disposition):
"the probe's frozen-run guard (R6: expected.json pins no digest of
pointer-table.json — probe-exempt by kind, gate-blocking if ever promoted)".

Claim: after the round's commit, `.ufo/gates/citation-drift/` pins the sha256 of
`pointer-table.json` in `expected.json`; a tampered or absent table yields the
declared preflight could-not-evaluate class (exit 2), never silent findings; the
SKILL.md registry row states the guard semantics; selftest 11 → 13 cases
(clean-tree, tampered-table, absent-table) at exit 0; findings = 0 at HEAD.

Falsifiable before → after: selftest 11/11, no table digest pinned → selftest
13/13 with the two injection fixtures each demonstrating the declared exit-2
class in an isolated tree; probe findings=0 re-run at the work commit.

## C3 — freshness (fleet): census scope-table re-key at HEAD

Named debt (`SCORECARD.md` arc2-loop1-round3 carried debt, item E22): "census
scope-table drift (FAIL undeclared=2 … — re-key or retire next calibration
round)". Round 8 re-keyed three DATED rows (SCOPE +1); the drift finding itself
was never dispositioned against current HEAD.

Claim: after the round's commit, the E22 finding is dispositioned by measurement
— census v10 is run at HEAD; if any scope row is undeclared/stale, the scope
table is re-keyed (or the row retired with cause recorded in the census header);
the census then reports PASS 0/0/0/0 at the records commit.

Falsifiable before → after: census verdict at HEAD before the re-key (recorded
verbatim) → PASS 0/0/0/0 at the records commit with the disposition stated in
the instrument's own header; command A unchanged (no corpus/knowledge edit in
this claim).

## Cross-cutting rules (frozen)

- Custody: 5-path pre-pair before any install/probe
  (`receipts/config-pre-pair.txt`), post-pair at close; npm cache is outside the
  custody set — the install itself is receipted (name/version/sha256) instead.
- Install authorization (operator-wide, goal scope): npm `solc` + its dep tree
  only; nothing else installs without a new explicit record.
- Seat discipline: seats write ONLY their own report at
  `.ufo/waves/arc3-loop1-round1/seats/<SEAT>.md` and claim artifacts under
  `.ufo/waves/arc3-loop1-round1/claims/{c1,c2,c3}/`; no seat commits, no seat
  LOG/SCORECARD writes, no seat git mutations (the `1692acb` non-lane-identity
  defect class). Parent integrates records after the wave.
- Seat reports carry: work performed (evidence pointers), landed diff (if any,
  as proposed patch text, NOT applied), before→after measurement per the claim,
  attacks/refutations attempted.
- Round report: `.ufo/reports/arc3-loop1-round1/kaidoku.md` (parent-written).

## Roster (64 seats, items array = these names)

C1 chain (26): PL-1, EX-01..EX-15, SC-1..SC-3, RV-1..RV-4, CR-1, CR-2, VZ-1
C2 chain (20): PL-2, EX-16..EX-25, SC-4, SC-5, RV-5..RV-8, CR-3, CR-4, VZ-2
C3 chain (14): PL-3, EX-26..EX-31, SC-6, SC-7, RV-9..RV-11, CR-5, VZ-3
Cross (4): CN-1, CN-2 (connectors), CU-1 (custody), VZ-4 (wave integrator)

Per-chain counts (enumerated, the r5 counting lesson): C1 = 1+15+3+4+2+1 = 26.
C2 = 1+10+2+4+2+1 = 20. C3 = 1+6+2+3+1+1 = 14. Cross = 4. Total 64.
This roster supersedes the first frozen draft, which mislabeled the chain sums
(25/20/12) — the defect was caught parent-side by enumerating the roster before
dispatch, per the r5 lesson; recorded here, not silently replaced.

Assertions at dispatch: len(items) == 64; every item name in this roster; no
duplicate names.
